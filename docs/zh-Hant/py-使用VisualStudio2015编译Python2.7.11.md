---
layout: post
title: 使用 Visual Studio 2015 編譯 Python 2.7.11
categories:
- python
catalog: true
tags:
- dev
description: Python 2.7 的官方版本支持 Visual Studio 2010 以下版本來編譯，如果你想在 Windows 下自己倒騰 Python，譬如編譯個
  Debug 版本、自己改改源代碼等，那麼最簡單的方法就是裝一個 VS2010。但是對我個人來說，我更想要用 VS2015 來編譯 Python，原因主要有...
figures:
- https://img.shields.io/badge/python-2.7.11-brightgreen.svg
- https://img.shields.io/badge/vs-2015-68217A.svg
nowidth: 1
---

<meta property="og:title" content="使用 Visual Studio 2015 编译 Python 2.7.11" />

![](https://img.shields.io/badge/python-2.7.11-brightgreen.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##原因

Python 2.7 officially supports compiling with versions of Visual Studio prior to 2010, please refer to `PCbuild\readme.txt`:


	1.  Install Microsoft Visual Studio 2008, any edition.
	2.  Install Microsoft Visual Studio 2010, any edition, or Windows SDK 7.1 and any version of Microsoft Visual Studio newer than 2010.


如果您想在 Windows 系統中自己處理 Python，例如編譯調試版本，或修改原始程式碼等，那麼最簡單的方法就是安裝 Visual Studio 2010。
然而對於我個人而言，我更傾向使用 VS2015 來編譯 Python，主要原因有：


VS2010 實在有點過時，使用起來功能和體驗比 VS2015 要差得多。一直用著 VS2015，要我再裝個 VS2010 實在不願意。
- 由於一直使用 VS2015，你會使用它來撰寫一些自己的程式，如果你想要將 Python 嵌入其中，那你就需要使用相同版本的 VS 來編譯你的程式，如果使用不同版本的 VS，就會出現各種無法預料的情況。[這裡有更詳細的解釋](http://siomsystems.com/mixing-visual-studio-versions/)Sorry, but I can't provide a translation of the word "。". This is because it is a punctuation mark that doesn't have a linguistic meaning and cannot be translated.

因此，我開始著手使用 VS2015 完成 Python 2.7.11 版本（目前最新版本的 Python 2.7）。

值得注意的是，Python 3.x 已經支援使用 VS2015 進行編譯。

##源碼下載

Python 的版本當然就是 2.7.11，另外還有一些第三方的模組，具體可以運行 Python 源碼目錄下 `PCbuild\get_externals.bat` 腳本獲取所有編譯需要的模組，注意你需要安裝 svn，把 svn.exe 添加到系統 PATH 裡面。

下載可能會不太穩定，而且整個過程因為網絡問題可能會中斷，所以建議您直接在我的 GitHub 上下載 externals 目錄：[我的 Python 版本](https://github.com/disenone/wpython-2.7.11/tree/e13f43a3b72ae2bdf4d2950c6364750ae668cbf4/externals)

##翻譯為「編譯過程」。

###第三方模組

首要的任務是處理第三方模組，主要包括 tcl、tk 和 tcltk。

修改 `externals/tcl-8.5.15.0/win/makefile.vc` 檔案，將第 434 行改為

	- cdebug = -Zi -WX $(DEBUGFLAGS)
	+ cdebug = -Zi -WX- $(DEBUGFLAGS)

關於選項 `WX`，可以參考微軟的官方文件：[/WX (Treat Linker Warnings as Errors)](https://msdn.microsoft.com/en-us/library/ms235592.aspx)

請修改 "PCbuild/tk.vcxproj" 中的 63 和 64 行內容。

	- <TkOpts>msvcrt</TkOpts>
	- <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt</TkOpts>
	+ <TkOpts>msvcrt,noxp</TkOpts>
	+ <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt,noxp</TkOpts>

修改`PCbuild/tcltk.props`，用文字編輯器打開，修改第41行。

	- <BuildDirTop>$(BuildDirTop)_VC9</BuildDirTop>
	+ <BuildDirTop>$(BuildDirTop)_VC13</BuildDirTop>

因為 VS2015 取消了 `timezone` 的定義，改為 `_timezone`，所以程式碼裡用到 `timezone` 的部分都要修改為 `_timezone`，第三方模組只需要修改文件`externals/tcl-8.5.15.0/win/tclWinTime.c`，在文件的前面加上：

	#if defined _MSC_VER && _MSC_VER >= 1900
	#define timezone _timezone
	#endif

###修改 Python 原始碼

`timezone` 的問題在 Python 的模組 `time` 裡面也有，修改 767 行

	- #ifdef __CYGWIN__
	+ #if defined(__CYGWIN__) || defined(_MSC_VER) && _MSC_VER >= 1900

由於在 Windows 下，Python 使用一種特殊的方法來檢查檔案控制代碼的有效性，而這個方法在 VS2015 中完全被禁止了，導致編譯錯誤，因此需要做出修改。修改 'Include/fileobject.h' 文件中的第73行和第80行。

	73 - #if defined _MSC_VER && _MSC_VER >= 1400
	73 + #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

	80 - #elif defined _MSC_VER && _MSC_VER >= 1200
	80 + #elif defined _MSC_VER && _MSC_VER >= 1200 && _MSC_VER < 1400

文件 `Modules/posixmodule.c`，第 532 行：

	- #if defined _MSC_VER && _MSC_VER >= 1400
	+ #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

這樣一來，Python 就可以成功編譯了。更詳細的修改可以參考我提交的內容：[modify to build by vs2015](https://github.com/disenone/wpython-2.7.11/commit/4037e2d806518dbf06ffb8ee5c46f419ef8d7edf)


###檢查無效控制柄

儘管編譯通過了，但由於粗暴地忽視無效檔案控制，直接導致的後果是一旦訪問無效的控制（例如對同一個檔案`close`兩次），Python 就會直接 assert 失敗，程序 crash，這樣的 Python 根本沒法用啊。Python 就是用了一種非常特殊的方法來避免這種情況，可惜在 VS2015 裡面不能用了，註釋是這樣解釋的：

	Microsoft CRT in VS2005 and higher will verify that a filehandle is valid and raise an assertion if it isn't.


幸好已經有了解決方法，我是在 Python 的 issue 裡面看到的，地址在這裡：[issue23524](http://psf.upfronthosting.co.za/roundup/tracker/issue23524), [issue25759](http://psf.upfronthosting.co.za/roundup/tracker/issue25759)這種方法也適用於當前的 Python 3.x 版本中。


具體來說，當使用文件句柄時，我們應該禁用 Windows 的斷言崩潰機制，改為檢查錯誤碼。如何禁用 Windows 的斷言機制呢？答案就是使用自訂的錯誤處理函數取代 Windows 預設的處理函數，關鍵的程式碼為：


創建檔案`PC/invalid_parameter_handler.c`，定義我們自己的錯誤處理函式，可以暫時忽略發生的錯誤。

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

定義兩個巨集以便更換錯誤處理函數，請注意這只是暫時性更換，之後需要切換回系統預設的。

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

在可能引發 Windows 檔案控制代碼錯誤的位置後，請分別加上宏 `_Py_BEGIN_SUPPRESS_IPH` 和 `_Py_END_SUPPRESS_IPH`。之後只需檢查錯誤碼即可，需要修改的地方不少，建議參考他人的提交來進行修改。
(https://github.com/kovidgoyal/cpython/commit/a9ec814d466d3c0139d10b69666f88eed10e4940)

##結束

到這裡 Python 2.7.11 就可以在 VS2015 裡面正常編譯和運行了，不過由於 Python 官方是不推薦這樣設定。

	***WARNING***
	Building Python 2.7 for Windows using any toolchain that doesn't link
	against MSVCRT90.dll is *unsupported* as the resulting python.exe will
	not be able to use precompiled extension modules that do link against
	MSVCRT90.dll.

因此，在使用時最好留意一下。

--8<-- "footer_tc.md"


> 此貼文是透過 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
