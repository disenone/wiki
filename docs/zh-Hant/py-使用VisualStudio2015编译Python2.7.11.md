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

Python 2.7 的官方版本支持 Visual Studio 2010 以前的版本來編譯，參考 `PCbuild\readme.txt`：


	1.  Install Microsoft Visual Studio 2008, any edition.
	2.  Install Microsoft Visual Studio 2010, any edition, or Windows SDK 7.1 and any version of Microsoft Visual Studio newer than 2010.


如果你想在 Windows 下自己玩弄 Python，例如编译一个 Debug 版本、自己修改源代码等等，最简单的方法就是安装一个 VS2010。
但是對我個人來說，我更想要用 VS2015 來編譯 Python，原因主要有：


VS2010 實在有點過時，使用起來功能和體驗比 VS2015 要差得多。一直用著 VS2015，要我再裝個 VS2010 實在不願意。
因為你長期使用 VS2015，所以你會用它來寫一些程式。如果你想要將 Python 嵌入其中，就需要使用相同版本的 VS 來編譯。如果使用不同版本的 VS，可能會出現各種意想不到的問題。[這裡有更詳細的解釋](http://siomsystems.com/mixing-visual-studio-versions/)。

因此，我開始著手使用 VS2015 完成 Python 2.7.11 版本（目前 Python 2.7 的最新版本）。

請注意，Python 3.x 已經支援使用 VS2015 進行編譯。

##源码下載

Python 的版本當然就是 2.7.11，另外還有一些第三方的模組，具體可以運行 Python 源碼目錄下 `PCbuild\get_externals.bat` 腳本獲取所有編譯需要的模組，注意你需要安裝 svn，把 svn.exe 添加到系統 PATH 裡面。

下載可能很不穩定，並且整個過程都有可能因為網絡問題而終止，所以還是推薦直接在我的 github 上下載 externals 目錄：[我的 Python 版本](https://github.com/disenone/wpython-2.7.11/tree/e13f43a3b72ae2bdf4d2950c6364750ae668cbf4/externals)

##編譯過程

###第三方模組

首先要解決的是第三方的模組，主要是 tcl、tk 和 tcltk。

修改文件 `externals/tcl-8.5.15.0/win/makefile.vc`，將 434 行改成

	- cdebug = -Zi -WX $(DEBUGFLAGS)
	+ cdebug = -Zi -WX- $(DEBUGFLAGS)

關於選項`WX`，可以查看微軟的官方文件：[/WX (Treat Linker Warnings as Errors)](https://msdn.microsoft.com/en-us/library/ms235592.aspx)

請再次打開`PCbuild/tk.vcxproj`文件，在文本編輯器中修改第 63 和 64 行。

	- <TkOpts>msvcrt</TkOpts>
	- <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt</TkOpts>
	+ <TkOpts>msvcrt,noxp</TkOpts>
	+ <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt,noxp</TkOpts>

修改 `PCbuild/tcltk.props`，用文本編輯器打開，修改第41行。

	- <BuildDirTop>$(BuildDirTop)_VC9</BuildDirTop>
	+ <BuildDirTop>$(BuildDirTop)_VC13</BuildDirTop>

由於 VS2015 取消了 `timezone` 的定義，改為 `_timezone`，所以代碼裡面用到 `timezone` 的地方都要改成 `_timezone`，第三方模組只需要改文件 `externals/tcl-8.5.15.0/win/tclWinTime.c`，在文件的前面加上：

	#if defined _MSC_VER && _MSC_VER >= 1900
	#define timezone _timezone
	#endif

###改 Python 源碼

`timezone` 的問題在 Python 的模塊 `time` 裡面也有，修改 767 行。

	- #ifdef __CYGWIN__
	+ #if defined(__CYGWIN__) || defined(_MSC_VER) && _MSC_VER >= 1900

另外，由於在 Windows 下 Python 使用了一種特殊的方法來檢查文件句柄的有效性，而這種方法在 VS2015 中被徹底禁止了，會出現編譯錯誤，因此需要先進行改動。文件 `Include/fileobject.h`，第 73 和 80 行：

	73 - #if defined _MSC_VER && _MSC_VER >= 1400
	73 + #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

	80 - #elif defined _MSC_VER && _MSC_VER >= 1200
	80 + #elif defined _MSC_VER && _MSC_VER >= 1200 && _MSC_VER < 1400

文件 `Modules/posixmodule.c`，532 行：

	- #if defined _MSC_VER && _MSC_VER >= 1400
	+ #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

至此，Python 就可以編譯通過了。更具體的修改可以查看我的 commit 內容：[modify to build by vs2015](https://github.com/disenone/wpython-2.7.11/commit/4037e2d806518dbf06ffb8ee5c46f419ef8d7edf)


###檢查無效的處理程序

雖然編譯通過了，但由於是粗暴地忽略無效文件句柄，直接導致的後果是一旦訪問無效的句柄（譬如對同一個文件`close`兩次），Python 就會直接 assert failed，程序崩潰，這樣的 Python 根本沒法用啊。Python 就是用了一種很特殊的方法來避免這種情況，可惜在 VS2015 裡面不能用了，註釋是這樣解釋的：

	Microsoft CRT in VS2005 and higher will verify that a filehandle is valid and raise an assertion if it isn't.


幸好已經有了解決方法，我是在 Python 的問題裡看到的，地址在這裡：[issue23524](http://psf.upfronthosting.co.za/roundup/tracker/issue23524), [issue25759](http://psf.upfronthosting.co.za/roundup/tracker/issue25759)這個方法也適用於目前的 Python 3.x 中。


具體來說，在使用文件控制代碼時，禁用 Windows 的 assert crash 機制，改為檢查錯誤碼。如何禁用 Windows 的 assert 機制呢？答案就是使用自訂的錯誤處理函數取代 Windows 預設的處理函數，關鍵程式碼：


新建文件 `PC/invalid_parameter_handler.c`，定義我們自己的錯誤處理函數，可以暫時忽略發生的錯誤。

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

定義兩個宏方便更換錯誤處理函數，要注意是暫時的更換，之後需要換回系統默認的。

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

在可能觸發 Windows 檔案控制代碼錯誤的地方，請分別在前後加上宏`_Py_BEGIN_SUPPRESS_IPH` 和 `_Py_END_SUPPRESS_IPH`，之後再檢查錯誤碼即可。需要修改的地方相當多，建議參考他人的 commit 來進行修改：
(https://github.com/kovidgoyal/cpython/commit/a9ec814d466d3c0139d10b69666f88eed10e4940)

##結束

Python 2.7.11現在可以在VS2015中正常編譯和運行了，但由於Python官方不建議這樣設定。

	***WARNING***
	Building Python 2.7 for Windows using any toolchain that doesn't link
	against MSVCRT90.dll is *unsupported* as the resulting python.exe will
	not be able to use precompiled extension modules that do link against
	MSVCRT90.dll.

所以在使用時最好要留意一下。

--8<-- "footer_tc.md"


> 此貼文是由 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
