---
layout: post
title: Visual Studio 2015を使用してPython 2.7.11をコンパイル
categories:
- python
catalog: true
tags:
- dev
description: Python 2.7 の公式バージョンは、Visual Studio 2010 以前のバージョンをサポートしています。Windows で
  Python をカスタマイズしたい場合、デバッグ版をコンパイルしたり、ソースコードを変更したりしたい場合は、最も簡単な方法は VS2010 をインストールすることです。個人的には、Python
  をビルドする際には、VS2015 を使用したいと考えています。その理由は主に次の通りです...
figures:
- https://img.shields.io/badge/python-2.7.11-brightgreen.svg
- https://img.shields.io/badge/vs-2015-68217A.svg
nowidth: 1
---

<meta property="og:title" content="使用 Visual Studio 2015 编译 Python 2.7.11" />

![](https://img.shields.io/badge/python-2.7.11-brightgreen.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##原因

Python 2.7 公式版は Visual Studio 2010 より前のバージョンをサポートし、`PCbuild\readme.txt` を参照してください。


	1.  Install Microsoft Visual Studio 2008, any edition.
	2.  Install Microsoft Visual Studio 2010, any edition, or Windows SDK 7.1 and any version of Microsoft Visual Studio newer than 2010.


WindowsでPythonをカスタマイズしたい場合、デバッグバージョンをコンパイルしたり、ソースコードを編集したりするなら、最も簡単な方法はVS2010をインストールすることです。
個人的立場から言えば、Python をコンパイルするのに VS2015 を使用したいです。理由は主に以下のとおりです：


VS2010は少し時代遅れで、機能や使い勝手がVS2015よりも遥かに劣っています。ずっとVS2015を使っているので、今さらVS2010をインストールするのは本当に嫌です。
Visual Studio 2015 一貫使ってるから、自分のプログラムを書く時もそれを使ってるんですね。Python を組み込みたい場合、同じバージョンの Visual Studio を使ってプログラムをコンパイルする必要がある。違うバージョンの Visual Studio を使うと、予期せぬ問題が発生する可能性があるからね。[詳細な説明はこちら](http://siomsystems.com/mixing-visual-studio-versions/)I'm sorry, but I cannot provide a translation for this text as it does not contain any readable content.

したがって、私はVS2015を使用してPython 2.7.11（現在のPython 2.7の最新バージョン）を処理することに取り掛かりました。

Python 3.x では、VS2015 でのコンパイルがサポートされています。

##ソースコードのダウンロード

Python のバージョンは当然 2.7.11 で、さらにいくつかのサードパーティモジュールが存在します。Python ソースコードディレクトリ内の `PCbuild\get_externals.bat` スクリプトを実行することで、コンパイルに必要なすべてのモジュールを取得できます。ただし、svn をインストールしておく必要があり、svn.exe をシステムの PATH に追加する必要があります。

ダウンロードは非常に不安定であり、ネットワークの問題によりプロセス全体が中断される可能性があるため、私のGitHubからexternalsディレクトリを直接ダウンロードすることをお勧めします：[私のPythonバージョン](https://github.com/disenone/wpython-2.7.11/tree/e13f43a3b72ae2bdf4d2950c6364750ae668cbf4/externals)

##コンパイルプロセス

###第三者モジュール

まず最初に対処すべき課題は第三者モジュールで、主にtcl、tk、tcltkです。

ファイル `externals/tcl-8.5.15.0/win/makefile.vc` の 434 行目を変更してください。

	- cdebug = -Zi -WX $(DEBUGFLAGS)
	+ cdebug = -Zi -WX- $(DEBUGFLAGS)

選択肢 `WX` に関しては、Microsoft の公式ドキュメントをご覧ください：[/WX (Treat Linker Warnings as Errors)](https://msdn.microsoft.com/en-us/library/ms235592.aspx)

`PCbuild/tk.vcxproj`を再度開いて、テキストエディタで63、64行を修正してください。

	- <TkOpts>msvcrt</TkOpts>
	- <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt</TkOpts>
	+ <TkOpts>msvcrt,noxp</TkOpts>
	+ <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt,noxp</TkOpts>

"Edit `PCbuild/tcltk.props` file, open it with a text editor, and modify line 41."

	- <BuildDirTop>$(BuildDirTop)_VC9</BuildDirTop>
	+ <BuildDirTop>$(BuildDirTop)_VC13</BuildDirTop>

VS2015 が `timezone` の定義をキャンセルし、`_timezone` に変更されたため、コード内の `timezone` の部分はすべて `_timezone` に変更する必要があります。サードパーティのモジュールは、`externals/tcl-8.5.15.0/win/tclWinTime.c` ファイルを変更するだけで十分で、ファイルの先頭に以下を追加してください：

	#if defined _MSC_VER && _MSC_VER >= 1900
	#define timezone _timezone
	#endif

###Pythonソースコードを変更します。

Pythonの`time`モジュールには`timezone`という問題がある。767行を修正してください。

	- #ifdef __CYGWIN__
	+ #if defined(__CYGWIN__) || defined(_MSC_VER) && _MSC_VER >= 1900

Windows上でPythonはファイルハンドルの有効性を確認するために特殊な方法を使用していますが、これはVS2015で完全に禁止されており、コンパイルエラーが発生しますので、まず修正してください。`Include/fileobject.h`ファイルの73、80行：

	73 - #if defined _MSC_VER && _MSC_VER >= 1400
	73 + #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

	80 - #elif defined _MSC_VER && _MSC_VER >= 1200
	80 + #elif defined _MSC_VER && _MSC_VER >= 1200 && _MSC_VER < 1400

`Modules/posixmodule.c`ファイルの532行：

	- #if defined _MSC_VER && _MSC_VER >= 1400
	+ #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

この段階で、Python はコンパイルできるようになりました。さらに詳細な変更については、私のコミット内容を参照してください: [modify to build by vs2015](https://github.com/disenone/wpython-2.7.11/commit/4037e2d806518dbf06ffb8ee5c46f419ef8d7edf)


###無効なハンドルをチェックします。

コンパイルは通ったけど、無効なファイルハンドルを乱暴に無視した結果、無効なハンドルにアクセスすると（例えば同じファイルを2回`close`する場合）、Python は直ちに assert に失敗し、プログラムがクラッシュしてしまう。こんな Python じゃ全然使えない。Python はこのような状況を避けるために非常に特別な方法を採用している。残念ながら、VS2015 では使えないそうだ。コメントには以下のように説明されている：

	Microsoft CRT in VS2005 and higher will verify that a filehandle is valid and raise an assertion if it isn't.


幸運なことに、私はPythonのissueで解決策を見つけました。こちらがそのアドレスです: [issue23524](http://psf.upfronthosting.co.za/roundup/tracker/issue23524), [issue25759](http://psf.upfronthosting.co.za/roundup/tracker/issue25759)この手法は現在、Python 3.x でも使用されています。


具体に言うと、ファイルハンドルを使用する際に Windows の assert crash メカニズムを無効にし、代わりにエラーコードをチェックするようにします。Windows の assert メカニズムを無効にするにはどうすればいいか？答えは、Windows のデフォルト処理関数の代わりに独自のエラー処理関数を使用することです。重要なコードは次の通り：


`PC/invalid_parameter_handler.c`という新しいファイルを作成し、独自のエラー処理関数を定義します。発生したエラーを一時的に無視することができます。

```c++
#ifdef _MSC_VER

#include <stdlib.h>

#if _MSC_VER >= 1900
/* pyconfig.h uses this function in the _Py_BEGIN_SUPPRESS_IPH/_Py_END_SUPPRESS_IPH
 * macros. It does not need to be defined when building using MSVC
 * earlier than 14.0 (_MSC_VER == 1900).
 */

static void __cdecl _silent_invalid_parameter_handler(
    wchar_t const* expression,
    wchar_t const* function,
    wchar_t const* file,
    unsigned int line,
	uintptr_t pReserved) 
{}

_invalid_parameter_handler _Py_silent_invalid_parameter_handler = _silent_invalid_parameter_handler;

#endif

#endif
```

エラー処理関数を簡単に切り替えるための2つのマクロを定義します。一時的な変更に留意し、後でシステムのデフォルトに戻す必要があります。

```c++
#if defined _MSC_VER && _MSC_VER >= 1900

extern _invalid_parameter_handler _Py_silent_invalid_parameter_handler;
#define _Py_BEGIN_SUPPRESS_IPH { _invalid_parameter_handler _Py_old_handler = \
    _set_thread_local_invalid_parameter_handler(_Py_silent_invalid_parameter_handler);
#define _Py_END_SUPPRESS_IPH _set_thread_local_invalid_parameter_handler(_Py_old_handler); }

#else

#define _Py_BEGIN_SUPPRESS_IPH
#define _Py_END_SUPPRESS_IPH

#endif /* _MSC_VER >= 1900 */
```

可能な部分で Windows ファイルハンドルエラーが発生する可能性がある箇所には、それぞれ`_Py_BEGIN_SUPPRESS_IPH`と`_Py_END_SUPPRESS_IPH` マクロを追加し、エラーコードを確認してください。変更が必要な場所は多いので、他の方のコミットを参考に修正してください。
(https://github.com/kovidgoyal/cpython/commit/a9ec814d466d3c0139d10b69666f88eed10e4940)

##終了

ここまでくると、Python 2.7.11 はVS2015で正常にコンパイルおよび実行できるようになりました。ただし、Python 公式ではこのような設定はお勧めしていないことから、注意が必要です。

	***WARNING***
	Building Python 2.7 for Windows using any toolchain that doesn't link
	against MSVCRT90.dll is *unsupported* as the resulting python.exe will
	not be able to use precompiled extension modules that do link against
	MSVCRT90.dll.

使用する際は注意が必要です。

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 -> どこか見落としている点があれば教えてください。 
