---
layout: post
title: 使用 Visual Studio 2015 編譯 Python 2.7.11
categories:
- python
catalog: true
tags:
- dev
description: Python 2.7 的官方版本支持 Visual Studio 2010 以下版本來編譯，如果你想在 Windows 下自己搞Python，比方說編譯個
  Debug 版本、自己改改原始碼等，那麼最簡單的方法就是裝一個 VS2010。但是對我個人來說，我更想要用 VS2015 來編譯Python，原因主要有...
figures:
- https://img.shields.io/badge/python-2.7.11-brightgreen.svg
- https://img.shields.io/badge/vs-2015-68217A.svg
nowidth: 1
---

<meta property="og:title" content="使用 Visual Studio 2015 编译 Python 2.7.11" />

![](https://img.shields.io/badge/python-2.7.11-brightgreen.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##原因

Python 2.7 的官方版本支持 Visual Studio 2010 以下版本来编译，参考 `PCbuild\readme.txt`：


	1.  Install Microsoft Visual Studio 2008, any edition.
	2.  Install Microsoft Visual Studio 2010, any edition, or Windows SDK 7.1 and any version of Microsoft Visual Studio newer than 2010.


如果您想在Windows上自行操作Python，例如编译调试版本、修改源代码等，那么最简单的方法就是安装Visual Studio 2010。
然而對於我個人而言，我更想要使用VS2015來編譯Python，主要原因是：


VS2010 實在有點過時，使用起來功能和體驗比 VS2015 要差得多。一直用著 VS2015，要我再裝個 VS2010 實在不願意。
因為一直在用 VS2015，你會使用它來寫一些自己的程式，如果你想要把 Python 嵌入進去，那你就需要使用相同版本的 VS 來編譯你的程式，如果使用不同版本的 VS，那會出現各種無法預料的事情。[這裡有更詳細的解釋](http://siomsystems.com/mixing-visual-studio-versions/)抱歉，我無法為你翻譯這種無意義的短語。如果有任何其他需要幫助的地方，請隨時告訴我。

因此我開始著手使用VS2015來處理Python 2.7.11版（目前最新的Python 2.7版本）。

請注意，Python 3.x 已經支援使用 VS2015 來編譯。

##原始碼下載

Python 的版本當然就是 2.7.11，另外還有一些第三方的模組，具體可以運行 Python 源碼目錄下 `PCbuild\get_externals.bat` 腳本獲取所有編譯需要的模組，注意你需要安裝 svn，把 svn.exe 添加到系統 PATH 裡面。

請直接在我的GitHub上下載externals目錄，因為下載過程可能不穩定且可能因網路問題而中斷。這樣比較推薦喔：[我的Python版本](https://github.com/disenone/wpython-2.7.11/tree/e13f43a3b72ae2bdf4d2950c6364750ae668cbf4/externals)

##編譯過程

###第三方模組

首要處理的是第三方模組，主要是 tcl、tk、tcltk。

修改文件 `externals/tcl-8.5.15.0/win/makefile.vc`，把 434 行改成

	- cdebug = -Zi -WX $(DEBUGFLAGS)
	+ cdebug = -Zi -WX- $(DEBUGFLAGS)

關於選項 `WX`，您可以查看微軟的官方文件：[/WX (Treat Linker Warnings as Errors)](https://msdn.microsoft.com/en-us/library/ms235592.aspx)

再來修改`PCbuild/tk.vcxproj`，用文本編輯器打開，修改 63 和 64 行。

	- <TkOpts>msvcrt</TkOpts>
	- <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt</TkOpts>
	+ <TkOpts>msvcrt,noxp</TkOpts>
	+ <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt,noxp</TkOpts>

修改`PCbuild/tcltk.props`，打開文本編輯器，調整第41行。

	- <BuildDirTop>$(BuildDirTop)_VC9</BuildDirTop>
	+ <BuildDirTop>$(BuildDirTop)_VC13</BuildDirTop>

由於 VS2015 取消了 `timezone` 的定義，改為 `_timezone`，所以程式碼中所有使用 `timezone` 的地方都應更改為 `_timezone`。第三方模組只需修改文件 `externals/tcl-8.5.15.0/win/tclWinTime.c`，並在該文件的前面添加：

	#if defined _MSC_VER && _MSC_VER >= 1900
	#define timezone _timezone
	#endif

###修改 Python 原始碼

在Python模塊`time`裡面，也有關於`時區`的問題，您可以在第767行進行修改。

	- #ifdef __CYGWIN__
	+ #if defined(__CYGWIN__) || defined(_MSC_VER) && _MSC_VER >= 1900

由於 Windows 下 Python 使用了一種特殊的方法來檢查文件句柄的有效性，而這種方法在 VS2015 中被完全禁止，將會出現編譯錯誤，因此需要先進行修改。請檢查檔案 `Include/fileobject.h` 中的第73和80行。

	73 - #if defined _MSC_VER && _MSC_VER >= 1400
	73 + #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

	80 - #elif defined _MSC_VER && _MSC_VER >= 1200
	80 + #elif defined _MSC_VER && _MSC_VER >= 1200 && _MSC_VER < 1400

文件 `Modules/posixmodule.c`，第532行：

	- #if defined _MSC_VER && _MSC_VER >= 1400
	+ #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

到這裡，Python 就可以成功編譯了。更詳細的修改內容可以查看我 commit 的內容：[modify to build by vs2015](https://github.com/disenone/wpython-2.7.11/commit/4037e2d806518dbf06ffb8ee5c46f419ef8d7edf)


###檢查無效指標

即使編譯通過了，但因為粗暴地忽略無效文件句柄，導致一旦訪問無效句柄（例如對同一個文件`close`兩次），Python 將直接 assert 失敗，程序崩潰，這樣的 Python 簡直無法使用。Python 用了一種特殊方法來避免這種情況，但在 VS2015 中不可使用，註釋就是這樣解釋的：

	Microsoft CRT in VS2005 and higher will verify that a filehandle is valid and raise an assertion if it isn't.


幸好已有解決方案，我是從 Python 的問題追蹤中看到的，地址在這裡：[issue23524](http://psf.upfronthosting.co.za/roundup/tracker/issue23524), [issue25759](http://psf.upfronthosting.co.za/roundup/tracker/issue25759)這種方法同樣適用於目前的 Python 3.x 版本。


具體而言，當使用文件句柄時，我們會禁用 Windows 的 assert crash 機制，改為檢查錯誤碼。那要如何禁用 Windows 的 assert 機制呢？答案就是使用自訂的錯誤處理函數來取代 Windows 預設的處理函數，關鍵的程式碼：


在新建檔案`PC/invalid_parameter_handler.c`中定義我們自己的錯誤處理函式，可暫時忽略所發生的錯誤。

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

定義兩個巨集方便更換錯誤處理函數，要注意是暫時的更換，之後是需要換回系統預設的。

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

在可能觸發 Windows 檔案控制項錯誤的地方，前後分別加上宏`_Py_BEGIN_SUPPRESS_IPH`和`_Py_END_SUPPRESS_IPH`，然後檢查錯誤碼就可以了。需要修改到的地方不少，請參考其他人的 commit 來修改。
(https://github.com/kovidgoyal/cpython/commit/a9ec814d466d3c0139d10b69666f88eed10e4940)

##結束

截至這裡，Python 2.7.11 現在可以在 VS2015 中正常編譯和運行，但由於 Python 官方不建議這樣設置。

	***WARNING***
	Building Python 2.7 for Windows using any toolchain that doesn't link
	against MSVCRT90.dll is *unsupported* as the resulting python.exe will
	not be able to use precompiled extension modules that do link against
	MSVCRT90.dll.

因此，在使用時最好要注意一下。

--8<-- "footer_tc.md"


> 此篇文章由 ChatGPT 翻譯而成，請在 [**反饋**](https://github.com/disenone/wiki_blog/issues/new)請指出任何遺漏之處。 
