---
layout: post
title: Windows上のメモリリーク検出ツールを作成する
categories:
- c++
tags:
- dev
description: 最近《プログラマーの自己修養：リンク、ロード、ライブラリ》（以下《リンク》）を読み終わり、多くのことを学びました。それに関連する小さなコードを作れないかなと考えています。ちょうど
  Windows で使えるメモリリーク検出ツール [Visual Leak Detector](https://vld.codeplex.com/)このツールは、Windowsでメモリ管理を担当するdllインターフェースを置き換えることによって、メモリの割り当てと解放を追跡することを実現しています。そこで、Visual
  Leak Detector（以下VLDと略します）を参考にして、簡易的なメモリリーク検出ツールを作成し、dllリンクを理解することにしました。
figures:
- assets/post_assets/2016-6-11-memory-leak-detector/depends.png
---

<meta property="og:title" content="编写 Windows 下的 Memory Leak Detector" />

![](https://img.shields.io/badge/windows-10-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##前言

最近《プログラマーの自己修養：リンク、ロードとライブラリ》（以下略して『リンク』）を読み終え、多くの収穫がありました。それに関連する小さなコードを書いてみようと考えています。ちょうどWindows用のメモリリーク検出ツール [Visual Leak Detector](https://vld.codeplex.com/)このツールは、Windowsでメモリ管理を担当するdllインターフェースを置き換えることによって、メモリの割り当てと解放を追跡することが実現されています。そこで、Visual Leak Detector（以下VLDと略します）を参考にして、簡易的なメモリリーク検出ツールを作成し、dllリンクを理解することに決めました。

##用日语翻译这段文字:
予備知識
「リンク」という書籍は、LinuxとWindowsで実行可能なファイルのリンク原理を詳しく説明しており、Windowsでの実行可能ファイル形式はPE（Portable Executable）ファイルと呼ばれています。そして、DLLファイルの説明は次のようになります：

> DLLは「Dynamic-Link Library」の略で、Linuxの共有オブジェクトに相当します。WindowsシステムではこのDLLメカニズムが広く採用されており、Windowsのカーネル構造さえも大きくDLLメカニズムに依存しています。WindowsのDLLファイルとEXEファイルは実際には同じコンセプトであり、両方ともPEフォーマットのバイナリファイルです。わずかな違いとしてはPEファイルヘッダーに、ファイルがEXEであるかDLLであるかを示すシンボルビットが存在し、DLLファイルの拡張子は必ずしも.dllである必要はなく、たとえば.ocx（OCXコントロール）や.CPL（コントロールパネルプログラム）など、他の拡張子を取ることもあります。

例えば、Pythonの拡張ファイルである.pydもあります。また、DLLにおいて私たちがここで扱うメモリリーク検出の概念は**シンボルのエクスポートインポートテーブル**です。

####符号エクスポート表

> 当一个 PE 需要将一些函数或变量提供给其他 PE 文件使用时，我们把这种行为叫做**シンボルエクスポート（Symbol Exporting）**

Windows PE内では、すべてのエクスポートされたシンボルは、**Export Table**と呼ばれる構造に集中して格納されます。これは、シンボル名とシンボルアドレスのマッピングを提供します。エクスポートする必要のあるシンボルには、修飾子`__declspec(dllexport)`を付ける必要があります。

####符号インポートテーブル

符号インポート表は、ここでの重要な概念です。これは符号エクスポート表に対応しており、まずは概念の説明を見ていきましょう。

> もし私たちがあるプログラムでDLLからの関数や変数を使用する場合、この行為を**シンボルインポート（Symbol Importing）**と呼びます。

Windows PE 中に保存されているモジュールが必要とする変数や関数、およびその所属するモジュールに関する情報を保持する構造体を**インポートテーブル(Import Table)**と呼びます。Windows が PE ファイルをロードする際、行う作業の一つは、すべての必要なインポート関数のアドレスを特定し、インポートテーブル内の要素を正しいアドレスに調整することです。ランタイム時に、プログラムは実際の関数のアドレスを特定し、それを呼び出すためにインポートテーブルをクエリしています。インポートテーブルの中で最も重要な構造は**インポートアドレステーブル (Import Address Table、IAT)**であり、ここにはインポートされた関数の実際のアドレスが格納されています。

ここまで読んで、私たちが実装しようとしているメモリーリーク検出の方法がすでにお分かりですね :)。その通り、インポートテーブルをハックすることです。具体的には、検出する必要のあるモジュールのインポートテーブル内にあるメモリの割り当てと解放に関する関数のアドレスを、独自の関数に変更することです。これにより、モジュールのメモリの割り当てと解放がどのように行われているかを把握し、必要な検出を行うことができます。

DLLリンクについての詳細な知識は、「リンク」または他の資料を参照してください。

## Memory Leak Detector

原理を理解したら、次にその原理に基づいてメモリリーク検出を実装します。以下の説明は私自身の実装に基づいており、私のGitHubに置いています：[LeakDetector](https://github.com/disenone/LeakDetector)I'm sorry, but there is no text to translate in your request.

####置換関数

(https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)申し訳ありませんが、翻訳するテキストが見当たりません。翻訳してほしい具体的な内容を教えていただけますか？

```cpp linenums="1"
/* importModule の IAT (インポートアドレステーブル) の特定の関数を別の関数に置き換える、
* importModule は他のモジュールの関数を呼び出し、その関数がパッチを当てる必要のある関数です。
私たちがやるべきことは、import moduleを私たちのカスタム関数を呼び出すように変更することです。
 *
- importModule (IN): The module to be processed, which calls functions that need to be patched in other modules.
 *
* - exportModuleName (IN): 需要パッチの関数が属するモジュール名
 *
- exportModulePath（IN）：エクスポートモジュールのパス。まずパスを使用してエクスポートモジュールを読み込みます。
失敗したら、nameを使用してロードします。
-importName (IN): 関数名
 *
* - replacement (IN): 代替関数ポインタ
 *
返り値: 成功 true，それ以外は false
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

この関数を解析してみましょう。コメントに書かれているように、この関数の目的はIAT内のある関数のアドレスを別の関数のアドレスに変更することです。34-35行を見てみましょう：

``` cpp
idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
	TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
```

`ImageDirectoryEntryToDataEx` 関数は、モジュールのファイルヘッダー内の特定の構造体のアドレスを返すことができます。`IMAGE_DIRECTORY_ENTRY_IMPORT` はインポートテーブル構造を指定するので、返される `idte` はモジュールのインポートテーブルを指すようになります。

36-40 行では、`idte` の有効性をチェックしています。41 行では、`idte->FirstThunk` が実際のIATを指しています。そのため、41-48 行は、置換が必要な関数を見つけるためにモジュール名を検索しています。見つからない場合は、そのモジュールの関数が呼び出されていないことを意味し、エラーを表示して戻ります。

モジュールを見つけたら、次に置き換える関数を見つける必要があります。55-62行で関数が所属するモジュールを開き、64行で関数のアドレスを見つけます。IATは名前を保存していないため、最初に元の関数のアドレスに基づいて関数を特定し、その後でその関数のアドレスを変更します。68-80行はこの作業を行っています。関数を成功裏に見つけた後は、単純にアドレスを `replacement` のアドレスに変更します。

Here is the translated text:

ここまで、私たちはIAT中の関数を成功裏に置き換えました。

####モジュール名と関数名

IAT 関数 `patchImport` をすでに置き換えたとはいえ、この関数にはモジュール名と関数名を指定する必要があるから、プログラムがどのモジュールと関数を使ってメモリ割り当てと解放を行っているかをどうやって知ればいいのかな？この問題を解明するために、Windows のツール [Dependency Walker](http://www.dependencywalker.com/)Visual Studioで新しいプロジェクトを作成し、`main`関数の中で`new`を使ってメモリを割り当てます。Debug版をコンパイルした後、`depends.exe`を使用してコンパイルされたexeファイルを開くと、以下のようなインターフェースが表示されます（私のプロジェクト[LeakDetectorTest](https://github.com/disenone/LeakDetector/tree/master/LeakDetectorTest)例として：

![](assets/img/2016-6-11-memory-leak-detector/depends.png)

LeakDetectorTest.exe が uscrtbased.dll 内の `malloc` と `_free_dbg` を使用していることが分かりました（画像には表示されていませんが）。これらの関数が私たちが置き換える必要がある関数です。実際のモジュール関数名は、Windows と Visual Studio のバージョンによって異なる可能性があります。私の場合は、Windows 10 と Visual Studio 2015 を使用していますが、あなたがやることは depends.exe を使用して実際に呼び出されている関数を調べることです。

####解析コールスタック

メモリ割り当ての記録には、その時の呼び出しスタック情報を記録する必要があります。ここでは、Windows上で現在の呼び出しスタック情報を取得する方法を詳しく説明するつもりはありませんが、関連する関数は `RtlCaptureStackBackTrace` です。ネット上には多くの関連資料がありますし、私のコードの中の関数 [`printTrace`](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)てください。

####メモリーリークを検出します。

ここまで来て、私たちはすべてのドラゴンボールを集めました。これから正式にシェンロンを呼び出します。

局部的なメモリリーク検出ができるようにしたいと思っています（これは VLD とは異なり、VLD はグローバルな検出を行い、マルチスレッドをサポートしています）。そのため、実際に関数を置き換えるクラス `RealDetector` の上に、もう一層 `LeakDetector` をラップしました。そして、`LeakDetector` のインターフェースを利用者に公開しました。使用時には、`LeakDetector` を構築するだけで関数の置き換えが完了し、メモリリークの検出が始まります。`LeakDetector` が破棄されると、元の関数に戻り、メモリリーク検出を中止し、メモリリーク検出の結果を表示します。

以下のコードを使ってテストしてください：

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

直訳： "コードは直接メモリを`new`して、解放せずに終了しました。プログラムは次の出力をしました："

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

プログラムは正しく2つの場所で要求されたメモリを解放せず、完全な呼び出しスタック情報を出力しました。必要な機能はここで完了しました。

###結語

プログラムのリンク、ロード、ライブラリについてまだ理解していないと、共有リンクライブラリの関数を見つける方法については混乱するかもしれませんし、リンクライブラリの関数を自分の関数に置き換えることに関してはなおさらです。ここでは、メモリリークの検出を例として、Windows DLL の関数を置き換える方法について探ってみます。より詳細な実装については、VLD のソースコードを参照してください。

その他に言いたいことは、「プログラマのための自己啓発：リンク、ロード、ライブラリ」は本当にいい本だよね、完全に感動で広告じゃない。

--8<-- "footer_ja.md"


> この投稿は ChatGPT を使って翻訳されました。フィードバックは[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
