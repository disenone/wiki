---
layout: post
title: Windows対応のメモリーリーク検出ツールの作成
categories:
- c++
tags:
- dev
description: 最近、『プログラマの自己啓発：リンク、ロード、およびライブラリ』（以下『リンク』と略す）を読了した。たくさんのことを学び、関連する小さなコードを書いてみることを考えている。ちょうどWindowsにメモリーリークを検出するツール
  [Visual Leak Detector](https://vld.codeplex.com/)このツールは、Windows のメモリ管理を担当するdllインターフェースを置き換えることでメモリの割り当てと解放を追跡するように設計されています。そのため、Visual
  Leak Detector（以下VLDと略す）を参考にして、簡易的なメモリリーク検出ツールを作成することに決定しました。dllリンクに関する理解も深めたいと考えています。
figures:
- assets/post_assets/2016-6-11-memory-leak-detector/depends.png
---

<meta property="og:title" content="编写 Windows 下的 Memory Leak Detector" />

![](https://img.shields.io/badge/windows-10-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##前書き

最近読み終えた『プログラマーの自己啓発：リンク、ロード、ライブラリ』（以下、「リンク」と略す）とても勉強になった。関連する小さなコードを書いてみようと思っているんだ。ちょうどWindowsにはメモリーリークを検出するツール [Visual Leak Detector](https://vld.codeplex.com/)このツールは、Windows のメモリ管理を担当している dll インターフェースを置き換えることで、メモリの割り当てと解放を追跡する仕組みです。そのため、Visual Leak Detector（以下、VLDと省略）を参考にして簡易的なメモリリーク検出ツールを作ることに決めました。dllリンクについて理解することが重要です。

##事前の知識
本書では、「リンク」というテーマについて、LinuxとWindowsでの実行可能ファイルのリンクの仕組みを詳しく説明しています。Windowsでは、実行可能ファイルの形式はPE（Portable Executable）ファイルと呼ばれています。そして、DLLファイルについての説明は以下の通りです：

> DLL（Dynamic-Link Library）は、Linuxにおける共有オブジェクトに相当するものであり、WindowsシステムではこのDLLメカニズムが広く採用されています。実際、Windowsのカーネル構造さえも大きくDLLメカニズムに依存しています。WindowsのDLLファイルとEXEファイルは実際には同じ概念です。両方ともPE形式のバイナリファイルで、わずかに異なるのはPEファイルヘッダーに、そのファイルがEXEかDLLかを示すシンボルビットがあることです。また、DLLファイルの拡張子は必ずしも.dllであるとは限らず、その他の拡張子である場合もあります。例えば、.ocx（OCXコントロール）や.CPL（コントロールパネルプログラム）などです。

Python の拡張子 .pyd のようなファイルもあります。そして、DLL に関しては、ここでのメモリーリーク検出概念は**symbol export/import table**です。

####符号导出表

> 他们所需要做的就是将一些函数或变量交给其他 PE 文件使用，这种行为被称为“Symbol Exporting”。

Windows PEにおいて、すべてのエクスポートシンボルは、**エクスポートテーブル（Export Table）**と呼ばれる構造に集約されて保存されます。これにより、シンボル名とシンボルアドレスのマッピング関係が提供されます。エクスポートする必要があるシンボルには、`__declspec(dllexport)`修飾子を追加する必要があります。

####記号インポートテーブル

符号導入表は、ここでの重要な概念です。符号導出表と対応しています。まずは概念の説明を見てみましょう：

> 「もし、あるプログラムで DLL からの関数や変数を使用している場合、そのような振る舞いを**シンボルインポート（Symbol Importing）**と呼びます。」

Windows PE 中保存模块需要导入的变量和函数的符号以及所在的模块等信息的结构叫做**インポート テーブル（Import Table）**。Windows が PE ファイルをロードする際、その1つの重要なステップは、すべてのインポート関数のアドレスを確定し、インポート テーブル内の要素を適切なアドレスに調整することです。これにより、実行時にプログラムはインポート テーブルを参照して実際の関数のアドレスを特定し、呼び出すことができます。インポート テーブル内で最も重要な構造は**インポート アドレス テーブル（Import Address Table, IAT）**であり、ここにはインポートされた関数の実際のアドレスが格納されています。

ここまで読んでいると、私たちが実装しようとしているメモリーリークの検出方法がすでにお分かりでしょう :)。そう、具体的には、インポートテーブルをハックして、検出したいモジュールのインポートテーブル内にあるメモリの割り当てと解放に関する関数のアドレスを自前の関数に変更することです。これにより、モジュールのメモリの割り当てと解放がいつ行われたかが分かり、自由に検出を行うことができます。

DLL リンクに関する詳細な知識については、「リンク」または他の資料をご参照ください。

## Memory Leak Detector

原理がわかったら、次はその原理に基づいてメモリリークの検出を実現する方法です。以下の説明は私自身の実装を基にしています。私のGithubに掲載しています: [LeakDetector](https://github.com/disenone/LeakDetector)I'm sorry, but since the text you provided contains only a punctuation mark ".", there is nothing to translate. If you provide more content, I will be happy to assist you with the translation.

####置き換え関数

[RealDetector.cpp](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)Sorry, I can't provide a translation for the colon ":" since it doesn't contain any linguistic content. If you have any other text you'd like me to translate, feel free to send it my way.

```cpp linenums="1"
importModule中のIAT (Import Address Table)の特定の関数を別の関数に置き換える
importModule は他のモジュールの関数を呼び出すことがあります。この関数が修正が必要な関数です。
私たちがしなければならないことは、import module を私たちが定義した関数を呼び出すように変更することです。
 *
importModule（IN）：パッチが必要な関数を呼び出す、処理する必要のあるモジュール
 *
- exportModuleName (IN): パッチが必要な関数が属するモジュールの名前
 *
- exportModulePath（IN）：エクスポートモジュールのパス。まずはパスを使用してエクスポートモジュールを読み込んでください。
失敗した場合は、`name`を使用してロードします。
- importName (IN): 関数名
 *
- replacement (IN): 代替関数ポインタ
 *
戻り値: 成功なら true、それ以外は false
*/
bool RealDetector::patchImport(
	HMODULE importModule,
	LPCSTR exportModuleName,
	LPCSTR exportModulePath,
	LPCSTR importName,
	LPCVOID replacement)
{
	HMODULE                  exportmodule;
	IMAGE_THUNK_DATA        *iate;
	IMAGE_IMPORT_DESCRIPTOR *idte;
	FARPROC                  import;
	DWORD                    protect;
	IMAGE_SECTION_HEADER    *section;
	ULONG                    size;

	assert(exportModuleName != NULL);

	idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
		TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
	if (idte == NULL) 
	{
		logMessage("patchImport failed: idte == NULL\n");
		return false;
	}
	while (idte->FirstThunk != 0x0) 
	{
		if (strcmp((PCHAR)R2VA(importModule, idte->Name), exportModuleName) == 0) 
		{
			break;
		}
		idte++;
	}
	if (idte->FirstThunk == 0x0) 
	{
		logMessage("patchImport failed: idte->FirstThunk == 0x0\n");
		return false;
	}

	if (exportModulePath != NULL) 
	{
		exportmodule = GetModuleHandleA(exportModulePath);
	}
	else 
	{
		exportmodule = GetModuleHandleA(exportModuleName);
	}
	assert(exportmodule != NULL);
	import = GetProcAddress(exportmodule, importName);
	assert(import != NULL);

	iate = (IMAGE_THUNK_DATA*)R2VA(importModule, idte->FirstThunk);
	while (iate->u1.Function != 0x0) 
	{
		if (iate->u1.Function == (DWORD_PTR)import) 
		{
			VirtualProtect(&iate->u1.Function, sizeof(iate->u1.Function), 
				PAGE_READWRITE, &protect);
			iate->u1.Function = (DWORD_PTR)replacement;
			VirtualProtect(&iate->u1.Function, sizeof(iate->u1.Function), 
				protect, &protect);
			return true;
		}
		iate++;
	}

	return false;
}

```

このテキストを日本語に翻訳します：

私たちはこの関数を分析してみましょう。コメントにあるように、この関数の機能は、IAT内のある関数のアドレスを別の関数のアドレスに変更することです。まずは34-35行を見てみましょう：

``` cpp
idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
	TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
```

`ImageDirectoryEntryToDataEx` 関数は、モジュールのファイルヘッダー内の特定の構造体のアドレスを返すことができます。`IMAGE_DIRECTORY_ENTRY_IMPORT` はインポートテーブル構造を指定しているため、返される `idte` はモジュールのインポートテーブルを指しています。

３６−４０行は、`idte` の有効性を確認する箇所だ。４１行では、`idte->FirstThunk` が実際のIATを指している。そのため、４１−４８行は、置換する必要のある関数を検索する際にモジュール名を基に探す箇所だ。もし見つからなければ、そのモジュールの関数が呼ばれていないことを示し、エラーを通知して処理を返す。

モジュールを見つけた後は、自然に、置き換える関数を見つける必要があります。55-62行目で関数が属するモジュールを開いて、64行目で関数のアドレスを見つけます。IATに名前が保存されていないため、元の関数のアドレスに基づいて関数を特定し、その後関数のアドレスを変更する必要があります。68-80行目ではこの作業を行っています。関数を正常に見つけた後は、単純にそのアドレスを「replacement」のアドレスに変更します。

この点で、私たちはIAT内の関数を正常に置き換えました。

####モジュールと関数名

`patchImport` 関数を置き換えているが、モジュール名と関数名を特定する必要がある。プログラムのメモリ割り当てと解放にどのモジュールと関数が使われているかを知るためには、Windows のツール [Dependency Walker](http://www.dependencywalker.com/)(https://github.com/disenone/LeakDetector/tree/master/LeakDetectorTest)（例）：

![](assets/img/2016-6-11-memory-leak-detector/depends.png)

LeakDetectorTest.exe が uscrtbased.dll 内の `malloc` と `_free_dbg` を使用していることが分かります（画面には表示されていませんが）。これらの関数が置き換える必要のある関数です。実際のモジュールの関数名は、Windows と Visual Studio のバージョンに依存する可能性があるので、私の場合は Windows 10 と Visual Studio 2015 です。あなたが必要なのは、depends.exe を使用して実際に呼び出されている関数を確認することです。

####解析コールスタック

記憶域の配分を記録するには、当時の呼び出しスタック情報を記録する必要があります。ここでは、Windowsで現在の呼び出しスタック情報を取得する方法について詳しく説明するつもりはありません。関連する関数は `RtlCaptureStackBackTrace` ですが、インターネットには多くの関連情報があり、私のコード内の関数 [`printTrace`](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)I'm sorry, but the text you provided is already in Japanese. It means "。" in English.

####メモリーリークの検出

ここまで、私たちはドラゴンボールをすべて集めましたね。では、神龍を正式に呼び出します。

私は部分的なメモリーリークの検出が可能なものを作りたいと思っています（これはVLDとは異なります。VLDはグローバルな検出を行い、マルチスレッドもサポートしています）。そこで、実際の関数を置換するクラス`RealDetector`にさらに`LeakDetector`という層を追加し、`LeakDetector`のインターフェースをユーザーに公開しました。使用時には、単純に`LeakDetector`を構築するだけで、関数の置換とメモリーリークの検出が完了し、`LeakDetector`が破棄されると元の関数が復元され、メモリーリークの検出が中止され、結果が出力されます。

以下のコードをテストしてみてください：

```cpp
#include "LeakDetector.h"
#include <iostream>
using namespace std;

void new_some_mem()
{
	char* c = new char[12];
	int* i = new int[4];
}

int main()
{
	auto ld = LDTools::LeakDetector("LeakDetectorTest.exe");
	new_some_mem();
    return 0;
}

```

コードはメモリを`new`して、それを解放せずに直ちに終了しました。プログラムは次の結果を出力しました：

```
============== LeakDetector::start ===============
LeakDetector init success.
============== LeakDetector::stop ================
Memory Leak Detected: total 2

Num 1:
    e:\program\github\leakdetector\leakdetector\realdetector.cpp (109): LeakDetector.dll!LDTools::RealDetector::_malloc() + 0x1c bytes
    f:\dd\vctools\crt\vcstartup\src\heap\new_scalar.cpp (19): LeakDetectorTest.exe!operator new() + 0x9 bytes
    f:\dd\vctools\crt\vcstartup\src\heap\new_array.cpp (15): LeakDetectorTest.exe!operator new[]() + 0x9 bytes
    e:\program\github\leakdetector\leakdetectortest\leakdetectortest.cpp (12): LeakDetectorTest.exe!new_some_mem() + 0x7 bytes
    e:\program\github\leakdetector\leakdetectortest\leakdetectortest.cpp (19): LeakDetectorTest.exe!main()
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (74): LeakDetectorTest.exe!invoke_main() + 0x1b bytes
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (264): LeakDetectorTest.exe!__scrt_common_main_seh() + 0x5 bytes
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (309): LeakDetectorTest.exe!__scrt_common_main()
    f:\dd\vctools\crt\vcstartup\src\startup\exe_main.cpp (17): LeakDetectorTest.exe!mainCRTStartup()
    KERNEL32.DLL!BaseThreadInitThunk() + 0x24 bytes
    ntdll.dll!RtlUnicodeStringToInteger() + 0x253 bytes
    ntdll.dll!RtlUnicodeStringToInteger() + 0x21e bytes

Num 2:
    e:\program\github\leakdetector\leakdetector\realdetector.cpp (109): LeakDetector.dll!LDTools::RealDetector::_malloc() + 0x1c bytes
    f:\dd\vctools\crt\vcstartup\src\heap\new_scalar.cpp (19): LeakDetectorTest.exe!operator new() + 0x9 bytes
    f:\dd\vctools\crt\vcstartup\src\heap\new_array.cpp (15): LeakDetectorTest.exe!operator new[]() + 0x9 bytes
    e:\program\github\leakdetector\leakdetectortest\leakdetectortest.cpp (11): LeakDetectorTest.exe!new_some_mem() + 0x7 bytes
    e:\program\github\leakdetector\leakdetectortest\leakdetectortest.cpp (19): LeakDetectorTest.exe!main()
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (74): LeakDetectorTest.exe!invoke_main() + 0x1b bytes
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (264): LeakDetectorTest.exe!__scrt_common_main_seh() + 0x5 bytes
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (309): LeakDetectorTest.exe!__scrt_common_main()
    f:\dd\vctools\crt\vcstartup\src\startup\exe_main.cpp (17): LeakDetectorTest.exe!mainCRTStartup()
    KERNEL32.DLL!BaseThreadInitThunk() + 0x24 bytes
    ntdll.dll!RtlUnicodeStringToInteger() + 0x253 bytes
    ntdll.dll!RtlUnicodeStringToInteger() + 0x21e bytes
```

このコードは、2箇所でメモリを確保したが解放しなかった箇所を正確に特定し、詳細な呼び出しスタック情報を出力することができた。必要な機能はここで完了した。

###結語

プログラムのリンク、ロード、およびライブラリについてまだ理解がない場合、共有ライブラリの関数を見つける方法について混乱するかもしれません。そしてその関数を自分たちの関数で置き換えることなど考えられないでしょう。ここでは、メモリリークの検出を例に、Windows DLLの関数を置き換える方法について考察します。より詳細な実装については、VLDのソースコードを参照してください。

もう一つ言いたいことは、『プログラマの自己修養：リンク、ロード、およびライブラリ』は本当にいい本だよね、純粋に感動した広告じゃない。

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遺漏之處。 
