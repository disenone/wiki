---
layout: post
title: 使用 Visual Studio 2015 で Python 2.7.11 をコンパイルする
categories:
- python
catalog: true
tags:
- dev
description: Python 2.7の公式版はVisual Studio 2010以下のバージョンをサポートしており、Windows上でPythonを自分でいじりたい場合、例えばデバッグ版をコンパイルしたり、ソースコードを修正したりする場合、最も簡単な方法はVS2010をインストールすることです。しかし私個人としては、PythonをコンパイルするためにVS2015を使用したいと考えています。その理由は主に…
figures:
- https://img.shields.io/badge/python-2.7.11-brightgreen.svg
- https://img.shields.io/badge/vs-2015-68217A.svg
nowidth: 1
---

<meta property="og:title" content="使用 Visual Studio 2015 编译 Python 2.7.11" />

![](https://img.shields.io/badge/python-2.7.11-brightgreen.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##原因

Python 2.7の公式バージョンは、Visual Studio 2010以下のバージョンをサポートしてコンパイルします。詳細は`PCbuild\readme.txt`を参照してください。


	1.  Install Microsoft Visual Studio 2008, any edition.
	2.  Install Microsoft Visual Studio 2010, any edition, or Windows SDK 7.1 and any version of Microsoft Visual Studio newer than 2010.


Windows で Python を自分でいじりたい場合、デバッグバージョンをコンパイルしたり、ソースコードを編集したりしたいなら、一番簡単な方法は VS2010 をインストールすることです。
個人的観点から言えば、PythonのコンパイルにはVS2015を使用したいと考えています。理由は主に以下の通りです。


VS2010はちょっと古すぎて、機能や使い勝手がVS2015に比べてかなり劣っているよね。ずっとVS2015を使っているから、再びVS2010をインストールするのは本当に嫌だ。
VS2015をずっと使っていたので、自分のプログラムを書く際にはそれを使用することに慣れています。Pythonを組み込みたい場合は、同じバージョンのVSを使ってプログラムをコンパイルする必要があります。異なるバージョンのVSを使用すると、予期しない問題が発生する可能性があります。[こちらで詳細を確認してください](http://siomsystems.com/mixing-visual-studio-versions/)I apologize, but I am unable to provide a translation for this text as it does not contain any content to be translated.

だから、私は VS2015 を使って Python 2.7.11 バージョン（現在の Python 2.7 の最新バージョン）を解決する作業に着手し始めました。

要注意，**Python 3.x はすでに VS2015 でコンパイルすることをサポートしています**。

##ソースコードのダウンロード

Pythonのバージョンはもちろん2.7.11です。他にもいくつかサードパーティのモジュールがあります。Pythonのソースコードディレクトリで`PCbuild\get_externals.bat`スクリプトを実行すると、必要な全てのモジュールを取得できます。ただし、svnをインストールし、svn.exeをシステムのPATHに追加する必要があります。

ダウンロードは非常に不安定な場合があり、全体のプロセスがネットワークの問題によって中断される可能性があるため、私のGitHubからexternalsディレクトリを直接ダウンロードすることをお勧めします：[私のPythonバージョン](https://github.com/disenone/wpython-2.7.11/tree/e13f43a3b72ae2bdf4d2950c6364750ae668cbf4/externals)

##コンパイルプロセス

###サードパーティーモジュール

まず解決すべきは、第三者のモジュールで、主に tcl、tk、tcltk です。

外部ファイル 'externals/tcl-8.5.15.0/win/makefile.vc' を修正して、434行目を変更してください。

	- cdebug = -Zi -WX $(DEBUGFLAGS)
	+ cdebug = -Zi -WX- $(DEBUGFLAGS)

`WX`オプションについては、Microsoftの公式ドキュメントをご覧ください：[/WX (リンクエラーをエラーとして扱う)](https://msdn.microsoft.com/en-us/library/ms235592.aspx)

`PCbuild/tk.vcxproj`ファイルを再度開いて、テキストエディターで63行目と64行目を修正してください。

	- <TkOpts>msvcrt</TkOpts>
	- <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt</TkOpts>
	+ <TkOpts>msvcrt,noxp</TkOpts>
	+ <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt,noxp</TkOpts>

`PCbuild/tcltk.props`をテキストエディタで開き、41行を修正してください。

	- <BuildDirTop>$(BuildDirTop)_VC9</BuildDirTop>
	+ <BuildDirTop>$(BuildDirTop)_VC13</BuildDirTop>

VS2015は`timezone`の定義をキャンセルし、代わりに`_timezone`に変更したため、コード内の`timezone`を`_timezone`に変更する必要があります。サードパーティーモジュールは`externals/tcl-8.5.15.0/win/tclWinTime.c`ファイルを変更するだけで十分で、ファイルの先頭に次の行を追加してください：

	#if defined _MSC_VER && _MSC_VER >= 1900
	#define timezone _timezone
	#endif

###Pythonのソースコードを改変します。

Pythonの`time`モジュールには`timezone`という問題もある。767行を修正する。

	- #ifdef __CYGWIN__
	+ #if defined(__CYGWIN__) || defined(_MSC_VER) && _MSC_VER >= 1900

Windows 上の Python では、ファイルハンドルの有効性をチェックする特殊な方法が使用されていますが、この方法がVS2015で完全に禁止されているため、コンパイルエラーが発生する可能性があります。そのため、まずこれを修正してください。ファイル `Include/fileobject.h` の73、80行をご確認ください。

	73 - #if defined _MSC_VER && _MSC_VER >= 1400
	73 + #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

	80 - #elif defined _MSC_VER && _MSC_VER >= 1200
	80 + #elif defined _MSC_VER && _MSC_VER >= 1200 && _MSC_VER < 1400

ファイル `Modules/posixmodule.c` の532行：

	- #if defined _MSC_VER && _MSC_VER >= 1400
	+ #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

これで、Pythonはコンパイルに成功しました。より具体的な修正内容は、私のコミットを参照してください：[modify to build by vs2015](https://github.com/disenone/wpython-2.7.11/commit/4037e2d806518dbf06ffb8ee5c46f419ef8d7edf)


###無効なハンドルをチェックします。

コンパイルが通ったけど、無効なファイルハンドルを乱暴に無視するため、無効なハンドルにアクセスしようとすると（例えば同じファイルを2回`close`しようとする）、Python は直ちにアサートに失敗してプログラムがクラッシュしてしまうんだ。そんな Python じゃ全然使えないよ。Python はこのような状況を回避するために、非常に特別な方法を使っているんだ。残念ながら、VS2015 では使えないみたいだ。コメントにはこんな風に説明されている：

	Microsoft CRT in VS2005 and higher will verify that a filehandle is valid and raise an assertion if it isn't.


幸好問題已被解決，我是在 Python 的議題中看到的，地址在這裡：[issue23524](http://psf.upfronthosting.co.za/roundup/tracker/issue23524), [issue25759](http://psf.upfronthosting.co.za/roundup/tracker/issue25759)この手法は現在の Python 3.x でも使用されています。


具体的には、ファイルハンドルを使用する際にWindowsのアサートクラッシュメカニズムを無効にし、エラーコードをチェックするようにします。では、Windowsのアサートメカニズムをどう無効にするのでしょうか？その答えは、Windowsのデフォルトの処理関数を自分のエラーハンドリング関数に置き換えることです。重要なコード：


新しいファイル`PC/invalid_parameter_handler.c`を作成し、独自のエラーハンドリング関数を定義します。発生したエラーは一時的に無視することができます。

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

エラーハンドリング関数の交換を便利にするために2つのマクロを定義しますが、これは一時的な交換であることに注意し、その後はシステムのデフォルトに戻す必要があります。

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

その後、Windowsファイルハンドルエラーを引き起こす可能性がある箇所には、それぞれマクロ`_Py_BEGIN_SUPPRESS_IPH`と`_Py_END_SUPPRESS_IPH`を追加し、その後にエラーコードを確認すればよいです。修正が必要な箇所は多く、他の人のコミットを参考にして修正してください。
[ここに](https://github.com/kovidgoyal/cpython/commit/a9ec814d466d3c0139d10b69666f88eed10e4940)

##終了

Python 2.7.11 はこれで VS2015 で正しくコンパイルおよび実行できるようになりましたが、Python 公式ではこのような設定を推奨していないため、注意が必要です。

	***WARNING***
	Building Python 2.7 for Windows using any toolchain that doesn't link
	against MSVCRT90.dll is *unsupported* as the resulting python.exe will
	not be able to use precompiled extension modules that do link against
	MSVCRT90.dll.

なので、使用する際には注意が必要です。

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。フィードバックは[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 -> どこか見落としている点を指摘してください。 
