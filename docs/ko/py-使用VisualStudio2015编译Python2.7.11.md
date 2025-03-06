---
layout: post
title: Visual Studio 2015을 사용하여 Python 2.7.11을 컴파일합니다.
categories:
- python
catalog: true
tags:
- dev
description: Python 2.7의 공식 버전은 Visual Studio 2010 이하 버전을 지원합니다. Windows에서 Python을
  직접 다루고 싶다면, 예를 들어 디버그 버전을 컴파일하거나 소스 코드를 수정하고 싶다면, 가장 간단한 방법은 VS2010을 설치하는 것입니다.
  그러나 개인적으로는, 저는 Python을 컴파일할 때 VS2015를 사용하고 싶습니다. 그 이유는 주로...
figures:
- https://img.shields.io/badge/python-2.7.11-brightgreen.svg
- https://img.shields.io/badge/vs-2015-68217A.svg
nowidth: 1
---

<meta property="og:title" content="使用 Visual Studio 2015 编译 Python 2.7.11" />

![](https://img.shields.io/badge/python-2.7.11-brightgreen.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##이 텍스트를 한국어로 번역하세요:
원인

Python 2.7의 공식 버전은 Visual Studio 2010 이하 버전을 지원하여 컴파일할 수 있습니다. `PCbuild\readme.txt`를 참조하세요:


	1.  Install Microsoft Visual Studio 2008, any edition.
	2.  Install Microsoft Visual Studio 2010, any edition, or Windows SDK 7.1 and any version of Microsoft Visual Studio newer than 2010.


Windows에서 Python을 컴파일하거나 디버그 버전을 만들거나 소스 코드를 직접 수정하려면 가장 간단한 방법은 VS2010을 설치하는 것입니다.
하지만 제 개인적으로는, Python을 컴파일하는 데 VS2015을 사용하고 싶습니다. 그 이유는 주로 다음과 같습니다:


- VS2010은 좀 구시대 같아. VS2015보다 기능과 경험이 훨씬 떨어져. 계속 VS2015 쓰고 있는데, 다시 VS2010 깔라니 귀찮네.
VS2015를 계속 사용해 왔으니 너도 네 프로그램을 쓸 때 자주 쓸 것이지. 만약 파이썬을 넣고 싶다면, 같은 버전의 VS를 써야 해. 다른 버전 쓰면 예상 못 한 문제들이 생길 수도 있어. [자세한 설명은 여기를 참고해](http://siomsystems.com/mixing-visual-studio-versions/)"。"Translation cannot be provided as it does not contain any content.

그래서 저는 VS2015를 사용하여 Python 2.7.11 버전(현재 Python 2.7의 최신 버전)을 처리하기 시작했습니다.

주의해야 할 점은, Python 3.x에서는 VS2015을 사용하여 컴파일하는 것이 지원된다는 점이다.

##소스 코드 다운로드

파이썬 버전은 물론 2.7.11이고, 그외 몇 가지 타사 모듈도 있습니다. 구체적인 내용은 Python 소스 코드 디렉터리 아래의 `PCbuild\get_externals.bat` 스크립트를 실행하여 컴파일에 필요한 모든 모듈을 얻을 수 있습니다. 주의해야 할 점은 svn을 설치해야 하고, svn.exe를 시스템 PATH에 추가해야 합니다.

다운로드는 매우 불안정할 수 있으며 전체 프로세스가 네트워크 문제로 인해 중단될 수 있으므로 제 Github에서 externals 디렉터리를 직접 다운로드하는 것을 권장합니다: [나의 Python 버전](https://github.com/disenone/wpython-2.7.11/tree/e13f43a3b72ae2bdf4d2950c6364750ae668cbf4/externals)

##컴파일링 프로세스

###제삼자 모듈

먼저 해결해야 할 것은 제3자 모듈인 tcl, tk, tcltk 입니다.

`externals/tcl-8.5.15.0/win/makefile.vc` 파일을 수정하여 434번 행을 변경하세요.

	- cdebug = -Zi -WX $(DEBUGFLAGS)
	+ cdebug = -Zi -WX- $(DEBUGFLAGS)

`WX` 옵션에 대한 자세한 내용은 마이크로소프트 공식 문서를 참고하십시오: [/WX (Treat Linker Warnings as Errors)](https://msdn.microsoft.com/en-us/library/ms235592.aspx)

'PCbuild/tk.vcxproj' 파일을 다시 열어서 63, 64번 라인을 수정해주세요.

	- <TkOpts>msvcrt</TkOpts>
	- <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt</TkOpts>
	+ <TkOpts>msvcrt,noxp</TkOpts>
	+ <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt,noxp</TkOpts>

'PCbuild/tcltk.props' 파일을 수정하려면 텍스트 편집기로 열어서 41번째 줄을 수정하십시오.

	- <BuildDirTop>$(BuildDirTop)_VC9</BuildDirTop>
	+ <BuildDirTop>$(BuildDirTop)_VC13</BuildDirTop>

VS2015에서 `timezone` 정의를 취소하여 `_timezone`으로 변경했기 때문에 코드 내에서 `timezone`을 사용하는 모든 곳을 `_timezone`으로 변경해야 합니다. 제3자 모듈은 `externals/tcl-8.5.15.0/win/tclWinTime.c` 파일만 수정하면 됩니다. 파일 맨 위에 다음을 추가하십시오:

	#if defined _MSC_VER && _MSC_VER >= 1900
	#define timezone _timezone
	#endif

###파이썬 소스 코드 수정하기

`timezone`의 문제는 Python 모듈 `time`에서도 발생하며, 767번 라인을 수정합니다.

	- #ifdef __CYGWIN__
	+ #if defined(__CYGWIN__) || defined(_MSC_VER) && _MSC_VER >= 1900

Windows에서 Python은 파일 핸들의 유효성을 확인하기 위해 특수한 방법을 사용하며, 이 방법은 VS2015에서 완전히 금지되어 컴파일 오류가 발생할 수 있으므로 먼저 수정해야 합니다. 'Include/fileobject.h' 파일의 73번과 80번 줄에서:

	73 - #if defined _MSC_VER && _MSC_VER >= 1400
	73 + #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

	80 - #elif defined _MSC_VER && _MSC_VER >= 1200
	80 + #elif defined _MSC_VER && _MSC_VER >= 1200 && _MSC_VER < 1400

`Modules/posixmodule.c` 파일의 532번째 라인:

	- #if defined _MSC_VER && _MSC_VER >= 1400
	+ #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

이제 Python이 컴파일될 수 있습니다. 더 구체적인 수정은 제 커밋 내용에서 확인할 수 있습니다: [modify to build by vs2015](https://github.com/disenone/wpython-2.7.11/commit/4037e2d806518dbf06ffb8ee5c46f419ef8d7edf)


###핸들이 유효하지 않습니다.

비록 컴파일은 통과했지만 무효한 파일 핸들을 거칠게 무시하여 발생하는 결과는 무효한 핸들에 액세스하면 (예: 동일 파일을 두 번 'close'한다면) Python이 직접 실패를 주장하고 프로그램이 충돌하게 됩니다. 이러한 Python은 전혀 사용할 수 없습니다. Python은 이러한 상황을 피하기 위해 매우 특별한 방법을 사용하며, 안타깝게도 VS2015에서는 사용할 수 없습니다. 주석에는 다음과 같이 설명되어 있습니다:

	Microsoft CRT in VS2005 and higher will verify that a filehandle is valid and raise an assertion if it isn't.


다행히도 해결 방법이 이미 있습니다. 저는 Python의 이슈에서 확인했는데요. 주소는 여기 있어요: [issue23524](http://psf.upfronthosting.co.za/roundup/tracker/issue23524), [issue25759](http://psf.upfronthosting.co.za/roundup/tracker/issue25759)이 방법은 현재 Python 3.x에서도 사용됩니다.


파일 핸들을 사용할 때 Windows의 assert crash 메커니즘을 비활성화하고 오류 코드를 확인하도록 변경하는 것입니다. Windows의 assert 메커니즘을 비활성화하려면 Windows 기본 처리 함수 대신 사용자 정의 오류 처리 함수를 사용해야 합니다. 중요한 코드는:


`PC/invalid_parameter_handler.c`라는 새 파일을 만들어서, 우리만의 오류 처리 함수를 정의해요. 발생한 에러를 일단 무시해도 괜찮아요.

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

두 가지 매크로를 정의하여 오류 처리 함수를 쉽게 교체할 수 있도록 합니다. 임시로 교체하는 것에 유의해야 하며, 이후에는 시스템 기본값으로 돌아가야 합니다.

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

해당하는 위치에서 Windows 파일 핸들 오류가 발생할 가능성이 있는 곳에는 매크로 '_Py_BEGIN_SUPPRESS_IPH'와 '_Py_END_SUPPRESS_IPH'를 앞뒤로 추가한 후 오류 코드를 확인하면 됩니다. 수정해야 할 부분이 많으므로 다른 사람의 커밋을 참고하여 수정하십시오.
이 텍스트를 한국어로 번역해주세요: 

[여기에서](https://github.com/kovidgoyal/cpython/commit/a9ec814d466d3c0139d10b69666f88eed10e4940)

##종료

여기까지 Python 2.7.11은 VS2015에서 정상적으로 컴파일 및 실행될 수 있습니다. 그러나 Python 공식 사이트는 이러한 방식을 권장하지는 않습니다.

	***WARNING***
	Building Python 2.7 for Windows using any toolchain that doesn't link
	against MSVCRT90.dll is *unsupported* as the resulting python.exe will
	not be able to use precompiled extension modules that do link against
	MSVCRT90.dll.

따라서 사용할 때 주의하는 것이 좋습니다.

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT로 번역되었습니다. "[**Feedback**](https://github.com/disenone/wiki_blog/issues/new)사소한 것도 놓치지 않고 제시하세요. 
