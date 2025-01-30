---
layout: post
title: Compile Python 2.7.11 using Visual Studio 2015
categories:
- python
catalog: true
tags:
- dev
description: The official version of Python 2.7 supports versions of Visual Studio
  2010 and below for compilation. If you want to tinker with Python on Windows, such
  as compiling a Debug version or making changes to the source code, the easiest method
  is to install VS2010. However, personally, I would prefer to use VS2015 to compile
  Python, mainly for the following reasons…
figures:
- https://img.shields.io/badge/python-2.7.11-brightgreen.svg
- https://img.shields.io/badge/vs-2015-68217A.svg
nowidth: 1
---

<meta property="og:title" content="使用 Visual Studio 2015 编译 Python 2.7.11" />

![](https://img.shields.io/badge/python-2.7.11-brightgreen.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##Reason

The official version of Python 2.7 supports versions of Visual Studio 2010 and earlier for compilation. Please refer to `PCbuild\readme.txt`:


	1.  Install Microsoft Visual Studio 2008, any edition.
	2.  Install Microsoft Visual Studio 2010, any edition, or Windows SDK 7.1 and any version of Microsoft Visual Studio newer than 2010.


If you want to tinker with Python on Windows, such as compiling a debug version or making changes to the source code yourself, the easiest way to do it is to install Visual Studio 2010.
However, personally, I prefer to compile Python using VS2015, the main reasons being:


- VS2010 is indeed a bit outdated; the functionality and experience are significantly worse compared to VS2015. I've been using VS2015, and I really don't want to install VS2010 again.
Due to always using VS2015, you might use it to write some of your own programs. If you want to embed Python into them, you'll need to compile your programs using the same version of Visual Studio. If you use a different version of Visual Studio, various unforeseen issues may arise. [Here is a more detailed explanation](http://siomsystems.com/mixing-visual-studio-versions/)".

So I started working on Python 2.7.11 version using VS2015 (the latest version of Python 2.7).

Please note that Python 3.x now supports compilation using VS2015.

##Source code download

The version of Python is of course 2.7.11. Additionally, there are some third-party modules. You can run the `PCbuild\get_externals.bat` script in the Python source code directory to obtain all the modules needed for compilation. Note that you need to install SVN and add svn.exe to the system PATH.

The download may be quite unstable, and the entire process could be interrupted due to network issues, so it's still recommended to download the externals directory directly from my GitHub: [My Python version](https://github.com/disenone/wpython-2.7.11/tree/e13f43a3b72ae2bdf4d2950c6364750ae668cbf4/externals)

##Compilation process

###Third-party modules

The first thing to address is the third-party modules, primarily tcl, tk, tcltk.

Modify the file `externals/tcl-8.5.15.0/win/makefile.vc`, change line 434 to...

	- cdebug = -Zi -WX $(DEBUGFLAGS)
	+ cdebug = -Zi -WX- $(DEBUGFLAGS)

Regarding the option `WX`, you can refer to Microsoft's official documentation: [/WX (Treat Linker Warnings as Errors)](https://msdn.microsoft.com/en-us/library/ms235592.aspx)

Please come and modify `PCbuild/tk.vcxproj` again, open it with a text editor, and make changes to lines 63 and 64.

	- <TkOpts>msvcrt</TkOpts>
	- <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt</TkOpts>
	+ <TkOpts>msvcrt,noxp</TkOpts>
	+ <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt,noxp</TkOpts>

Edit `PCbuild/tcltk.props`, open it with a text editor, and modify line 41.

	- <BuildDirTop>$(BuildDirTop)_VC9</BuildDirTop>
	+ <BuildDirTop>$(BuildDirTop)_VC13</BuildDirTop>

Due to the cancellation of the definition of `timezone` in VS2015, it is now changed to `_timezone`. Therefore, everywhere in the code where `timezone` is used, it should be changed to `_timezone`. Only the file `externals/tcl-8.5.15.0/win/tclWinTime.c` from third-party modules needs to be modified. Add the following at the beginning of the file:

	#if defined _MSC_VER && _MSC_VER >= 1900
	#define timezone _timezone
	#endif

###Modify Python source code

The issue with `timezone` also exists in the Python module `time`, modify it in line 767.

	- #ifdef __CYGWIN__
	+ #if defined(__CYGWIN__) || defined(_MSC_VER) && _MSC_VER >= 1900

In addition, due to a special method used by Python in Windows to check the validity of file handles, which has been completely prohibited in VS2015, compilation errors may occur, so it needs to be modified first. The files `Include/fileobject.h`, lines 73 and 80:

	73 - #if defined _MSC_VER && _MSC_VER >= 1400
	73 + #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

	80 - #elif defined _MSC_VER && _MSC_VER >= 1200
	80 + #elif defined _MSC_VER && _MSC_VER >= 1200 && _MSC_VER < 1400

File `Modules/posixmodule.c`, line 532:

	- #if defined _MSC_VER && _MSC_VER >= 1400
	+ #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

At this point, Python should compile successfully. For more specific modifications, you can refer to the changes in my commit: [modify to build by vs2015](https://github.com/disenone/wpython-2.7.11/commit/4037e2d806518dbf06ffb8ee5c46f419ef8d7edf)


###Check for invalid handles

Although the compilation succeeded, the consequence of brutally ignoring invalid file handles is that once an invalid handle is accessed (for example, calling `close` on the same file twice), Python will directly assert failed, causing the program to crash. Such a version of Python is simply unusable. Python employs a very special method to avoid this situation, but unfortunately, it can't be used in VS2015. The comment explains this as follows:

	Microsoft CRT in VS2005 and higher will verify that a filehandle is valid and raise an assertion if it isn't.


Fortunately, there is already a solution. I saw it in a Python issue, and the address is here: [issue23524](http://psf.upfronthosting.co.za/roundup/tracker/issue23524), [issue25759](http://psf.upfronthosting.co.za/roundup/tracker/issue25759)This method is also used in the current Python 3.x version.


Specifically, it means disabling Windows' assert crash mechanism when using file handles, and replacing it with error code checking. How can we disable Windows' assert mechanism? The answer is to use our own error handling function to replace the default Windows handler. The key code is:


Create a new file `PC/invalid_parameter_handler.c`, define our custom error handling function, you can temporarily ignore the errors that occur.

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

Define two macros for easy replacement of error handling functions. Note that this replacement should be temporary, and the system default needs to be restored later.

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

After that, at the places where a Windows file handle error might be triggered, respectively add the macros `_Py_BEGIN_SUPPRESS_IPH` and `_Py_END_SUPPRESS_IPH`, and then check the error code. There are quite a few places that need modification, so refer to others' commits for adjustments.
[Here](https://github.com/kovidgoyal/cpython/commit/a9ec814d466d3c0139d10b69666f88eed10e4940)

##End

At this point, Python 2.7.11 can be compiled and run normally in VS2015. However, it is worth mentioning that the official Python team does not recommend this setup.

	***WARNING***
	Building Python 2.7 for Windows using any toolchain that doesn't link
	against MSVCRT90.dll is *unsupported* as the resulting python.exe will
	not be able to use precompiled extension modules that do link against
	MSVCRT90.dll.

So it's best to pay attention when using it.

--8<-- "footer_en.md"


> This post was translated using ChatGPT, please provide feedback in [**反馈**](https://github.com/disenone/wiki_blog/issues/new)Please point out any omissions. 
