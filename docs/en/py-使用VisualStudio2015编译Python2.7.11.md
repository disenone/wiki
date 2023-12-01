---
layout: post
title: Compile Python 2.7.11 with Visual Studio 2015
categories:
- python
catalog: true
tags:
- dev
description: The official version of Python 2.7 supports compiling with Visual Studio
  versions below 2010. If you want to tinker with Python on Windows, such as compiling
  a debug version or making changes to the source code, the easiest method is to install
  VS2010. However, personally, I prefer to compile Python using VS2015 for several
  reasons...
figures:
- https://img.shields.io/badge/python-2.7.11-brightgreen.svg
- https://img.shields.io/badge/vs-2015-68217A.svg
nowidth: 1
---


![](https://img.shields.io/badge/python-2.7.11-brightgreen.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

## Cause

Python 2.7 official version supports compiling with Visual Studio versions below 2010. Refer to `PCbuild\readme.txt` for details.


	1.  Install Microsoft Visual Studio 2008, any edition.
	2.  Install Microsoft Visual Studio 2010, any edition, or Windows SDK 7.1 and any version of Microsoft Visual Studio newer than 2010.


If you want to mess around with Python on Windows, such as compiling a debug version or modifying the source code yourself, the easiest way is to install VS2010.
But for me personally, I prefer to compile Python using VS2015, and the main reasons are:




- VS2010 is a bit outdated, its functionality and user experience are much worse than VS2015. I have been using VS2015 all along and I really don't want to install VS2010 again.
- Since you have been using VS2015, you will use it to write your own programs. If you want to embed Python into your programs, you need to use the same version of VS to compile them. If you use a different version of VS, various unforeseen issues may arise. [Here is a more detailed explanation](http://siomsystems.com/mixing-visual-studio-versions/).

So I started to tackle Python 2.7.11 version using VS2015 (the latest version of Python 2.7).

Note that **Python 3.x now supports compilation with VS2015**.

## Source Code Download

Python version is of course 2.7.11. In addition, there are some third-party modules. You can run the `PCbuild\get_externals.bat` script under the Python source code directory to obtain all the modules needed for compilation. Note that you need to install svn and add svn.exe to the system PATH.

The download may be unstable and the entire process may be terminated due to network issues, so it is recommended to directly download the externals directory from my GitHub: [My Python version](https://github.com/disenone/wpython-2.7.11/tree/e13f43a3b72ae2bdf4d2950c6364750ae668cbf4/externals)

## Compilation Process

### Third-party Module

First, we need to deal with third-party modules, mainly tcl, tk, and tcltk.

Modify file `externals/tcl-8.5.15.0/win/makefile.vc`, change line 434 to

	- cdebug = -Zi -WX $(DEBUGFLAGS)
	+ cdebug = -Zi -WX- $(DEBUGFLAGS)

Regarding the option `WX`, you can refer to Microsoft's official documentation: [/WX (Treat Linker Warnings as Errors)](https://msdn.microsoft.com/en-us/library/ms235592.aspx)

To further modify `PCbuild/tk.vcxproj`, open it with a text editor and make changes to lines 63 and 64.

	- <TkOpts>msvcrt</TkOpts>
	- <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt</TkOpts>
	+ <TkOpts>msvcrt,noxp</TkOpts>
	+ <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt,noxp</TkOpts>

Change `PCbuild/tcltk.props`, open it with a text editor, and modify line 41.

	- <BuildDirTop>$(BuildDirTop)_VC9</BuildDirTop>
	+ <BuildDirTop>$(BuildDirTop)_VC13</BuildDirTop>

Due to the cancellation of the definition of `timezone` in VS2015, it was changed to `_timezone`. So, in the code, all occurrences of `timezone` need to be changed to `_timezone`. For third-party modules, only the file `externals/tcl-8.5.15.0/win/tclWinTime.c` needs to be modified. At the beginning of the file, add:

	#if defined _MSC_VER && _MSC_VER >= 1900
	#define timezone _timezone
	#endif

### Modify Python source code

The problem with `timezone` also exists in the `time` module of Python. Modify line 767.

	- #ifdef __CYGWIN__
	+ #if defined(__CYGWIN__) || defined(_MSC_VER) && _MSC_VER >= 1900

In addition, due to a special method used by Python on Windows to check the validity of file handles, this method has been completely prohibited in VS2015, causing a compilation error. Therefore, it needs to be modified first. File `Include/fileobject.h`, lines 73 and 80:

	73 - #if defined _MSC_VER && _MSC_VER >= 1400
	73 + #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

	80 - #elif defined _MSC_VER && _MSC_VER >= 1200
	80 + #elif defined _MSC_VER && _MSC_VER >= 1200 && _MSC_VER < 1400

File `Modules/posixmodule.c`, line 532:

	- #if defined _MSC_VER && _MSC_VER >= 1400
	+ #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

Up to this point, Python can be compiled successfully. For more specific modifications, please refer to the content of my commit: [modify to build by vs2015](https://github.com/disenone/wpython-2.7.11/commit/4037e2d806518dbf06ffb8ee5c46f419ef8d7edf)


### Invalid handle check

Although the compilation has passed, because the invalid file handle is roughly ignored, the consequence directly leads to Python asserting failure and program crashing once an invalid handle is accessed (such as closing the same file twice). This kind of Python is simply unusable. Python uses a special method to avoid this situation, but unfortunately it cannot be used in VS2015. The explanation is as follows in the comments:

	Microsoft CRT in VS2005 and higher will verify that a filehandle is valid and raise an assertion if it isn't.


Fortunately, there is already a solution available, I found it in the Python issue, the link is here: [issue23524](http://psf.upfronthosting.co.za/roundup/tracker/issue23524), [issue25759](http://psf.upfronthosting.co.za/roundup/tracker/issue25759). This method is also used in the current Python 3.x.


Specifically, it means disabling the assert crash mechanism in Windows when using file handles and instead checking error codes. How do you disable Windows assert mechanism? The answer is to use your own error handling function to replace the default Windows handling function. The key code is:

```cpp
// to_be_replace[key_code]
```

Where `key_code` is the code you are replacing.


Create a new file `PC/invalid_parameter_handler.c`, define our own error handling function to temporarily ignore the occurred errors.

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

Define two macros to facilitate the replacement of error handling functions. Note that the replacement is temporary and the system default needs to be restored afterwards.

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

After that, add the macro `_Py_BEGIN_SUPPRESS_IPH` before the possible locations that could trigger a Windows file handle error, and add `_Py_END_SUPPRESS_IPH` after that. Then, simply check the error code. There are several places that need to be modified, please refer to this [commit](https://github.com/kovidgoyal/cpython/commit/a9ec814d466d3c0139d10b69666f88eed10e4940) for guidance.

## End

From now on, Python 2.7.11 can be compiled and run normally in VS2015. However, since Python official does not recommend this setting, [to_be_replace]

	***WARNING***
	Building Python 2.7 for Windows using any toolchain that doesn't link
	against MSVCRT90.dll is *unsupported* as the resulting python.exe will
	not be able to use precompiled extension modules that do link against
	MSVCRT90.dll.

So it's better to pay attention when using it.

> Original: <https://disenone.github.io/wiki>  
> This post is protected by [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by/4.0/deed.en) agreement, should be reproduced with attribution.


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
