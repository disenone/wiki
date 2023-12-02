---
layout: post
title: Compile Python 2.7.11 using Visual Studio 2015.
categories:
- python
catalog: true
tags:
- dev
description: The official version of Python 2.7 supports compilation using Visual
  Studio versions up to 2010. If you want to tinker with Python on Windows, such as
  compiling a debug version or modifying the source code, the simplest method is to
  install VS2010. However, personally, I prefer to compile Python using VS2015 for
  several reasons...
figures:
- https://img.shields.io/badge/python-2.7.11-brightgreen.svg
- https://img.shields.io/badge/vs-2015-68217A.svg
nowidth: 1
---

<meta property="og:title" content="使用 Visual Studio 2015 编译 Python 2.7.11" />

![](https://img.shields.io/badge/python-2.7.11-brightgreen.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

## Reason

The official version of Python 2.7 supports compiling with Visual Studio versions prior to 2010. Please refer to `PCbuild\readme.txt` for more information.


	1.  Install Microsoft Visual Studio 2008, any edition.
	2.  Install Microsoft Visual Studio 2010, any edition, or Windows SDK 7.1 and any version of Microsoft Visual Studio newer than 2010.


If you want to mess around with Python on Windows, like compiling a debug version or modifying the source code yourself, the simplest method is to install VS2010.

However, personally, I would prefer to compile Python using VS2015 for the following reasons:


- VS2010 is a bit outdated and its functionality and user experience are much worse than VS2015. I have been using VS2015 all along, so I really don't want to install VS2010 again.
- Since you have been using VS2015, you will use it to write your own programs. If you want to embed Python into your programs, you need to use the same version of VS to compile your programs. If different versions of VS are used, various unforeseen issues may occur. [Here is a more detailed explanation](http://siomsystems.com/mixing-visual-studio-versions/).

So I started to work on Python version 2.7.11 using VS2015 (the latest version of Python 2.7).

**Note that Python 3.x now supports compilation with VS2015**.

## Source Code Download

The version of Python is, of course, 2.7.11. Additionally, there are some third-party modules. You can run the `PCbuild\get_externals.bat` script in the Python source code directory to obtain all the modules required for compilation. Please note that you need to install svn and add svn.exe to the system PATH.

Downloading could be unstable, and the whole process may be terminated due to network problems. Therefore, it is recommended to directly download the "externals" directory from my GitHub: [My Python Version](https://github.com/disenone/wpython-2.7.11/tree/e13f43a3b72ae2bdf4d2950c6364750ae668cbf4/externals)

## Compilation Process

### Third-party modules

The first thing to address is the third-party modules, mainly tcl, tk, tcltk.

Modify the file `externals/tcl-8.5.15.0/win/makefile.vc` and change line 434 to

	- cdebug = -Zi -WX $(DEBUGFLAGS)
	+ cdebug = -Zi -WX- $(DEBUGFLAGS)

Regarding the option `WX`, you can refer to Microsoft's official documentation: [/WX (Treat Linker Warnings as Errors)](https://msdn.microsoft.com/en-us/library/ms235592.aspx)

再来改`PCbuild/tk.vcxproj`，用文本编辑器打开，修改 63, 64 行

Go ahead and make changes to `PCbuild/tk.vcxproj`. Open it with a text editor and modify lines 63 and 64.

	- <TkOpts>msvcrt</TkOpts>
	- <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt</TkOpts>
	+ <TkOpts>msvcrt,noxp</TkOpts>
	+ <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt,noxp</TkOpts>

Change `PCbuild/tcltk.props`, open it with a text editor, and modify line 41.

	- <BuildDirTop>$(BuildDirTop)_VC9</BuildDirTop>
	+ <BuildDirTop>$(BuildDirTop)_VC13</BuildDirTop>

Due to the cancellation of the definition of `timezone` in VS2015, it has been changed to `_timezone`. Therefore, wherever `timezone` is used in the code, it needs to be changed to `_timezone`. For third-party modules, only the file `externals/tcl-8.5.15.0/win/tclWinTime.c` needs to be modified. Add the following at the beginning of the file:

	#if defined _MSC_VER && _MSC_VER >= 1900
	#define timezone _timezone
	#endif

### Modify Python Source Code

The issue with `timezone` also exists in the Python module `time`. Modify line 767.

	- #ifdef __CYGWIN__
	+ #if defined(__CYGWIN__) || defined(_MSC_VER) && _MSC_VER >= 1900

In addition, due to a special method used by Python on Windows to check the validity of file handles, this method has been completely disabled in VS2015, which would result in compilation errors, so it needs to be changed first. Modify the file `Include/fileobject.h`, lines 73 and 80:

	73 - #if defined _MSC_VER && _MSC_VER >= 1400
	73 + #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

	80 - #elif defined _MSC_VER && _MSC_VER >= 1200
	80 + #elif defined _MSC_VER && _MSC_VER >= 1200 && _MSC_VER < 1400

File `Modules/posixmodule.c`, line 532:

	- #if defined _MSC_VER && _MSC_VER >= 1400
	+ #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

So far, Python can be compiled successfully. For more specific modifications, you can refer to the contents of my commit: [modify to build by vs2015](https://github.com/disenone/wpython-2.7.11/commit/4037e2d806518dbf06ffb8ee5c46f419ef8d7edf)


### Invalid Handle Check

Although the compilation passed, the consequence of forcefully ignoring invalid file handles is that once an invalid handle is accessed (such as closing the same file twice), Python will directly trigger an assertion failure and the program will crash. In this way, Python is simply unusable. Python utilizes a special method to prevent this situation, but unfortunately it cannot be used in VS2015. The explanation in the comments is as follows:

	Microsoft CRT in VS2005 and higher will verify that a filehandle is valid and raise an assertion if it isn't.


Fortunately, there is already a solution, which I found in the Python issue tracker. You can find it here: [issue23524](http://psf.upfronthosting.co.za/roundup/tracker/issue23524), [issue25759](http://psf.upfronthosting.co.za/roundup/tracker/issue25759). This method is also used in Python 3.x.


To be specific, it means disabling the assert crash mechanism in Windows when using file handles and replacing it with error code checking. So how do you disable the assert mechanism in Windows? The answer is to use your own error handling function to replace the default Windows handling function. The key code is:

[to_be_replace[x]]


Create a new file `PC/invalid_parameter_handler.c` to define our own error handling function that can temporarily ignore the occurred errors.

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

Define two macros to facilitate the replacement of error handling functions. Note that the replacement is temporary, and the system's default functions need to be restored afterwards.

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

Afterwards, in the places where Windows file handle errors may be triggered, add the macro `_Py_BEGIN_SUPPRESS_IPH` before and `_Py_END_SUPPRESS_IPH` after, and then check the error code. There are quite a few places that need to be modified, refer to someone else's commit for modification:
[Here](https://github.com/kovidgoyal/cpython/commit/a9ec814d466d3c0139d10b69666f88eed10e4940)

## End

By now, Python 2.7.11 can be compiled and run normally in VS2015. However, Python official does not recommend this configuration.

	***WARNING***
	Building Python 2.7 for Windows using any toolchain that doesn't link
	against MSVCRT90.dll is *unsupported* as the resulting python.exe will
	not be able to use precompiled extension modules that do link against
	MSVCRT90.dll.

So it's best to pay attention when using it.

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
