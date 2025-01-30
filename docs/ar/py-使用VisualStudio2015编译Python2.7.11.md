---
layout: post
title: استخدام Visual Studio 2015 لتجميع Python 2.7.11
categories:
- python
catalog: true
tags:
- dev
description: إصدار Python 2.7 الرسمي يدعم النسخ الأقدم من Visual Studio 2010 للتجميع،
  إذا كنت ترغب في تجربة Python بنفسك على نظام Windows، مثل تجميع نسخة Debug، أو تعديل
  الكود المصدري، فإن أسهل طريقة هي تثبيت VS2010. ولكن بالنسبة لي شخصياً، أفضل استخدام
  VS2015 لتجميع Python، والسبب في ذلك هو...
figures:
- https://img.shields.io/badge/python-2.7.11-brightgreen.svg
- https://img.shields.io/badge/vs-2015-68217A.svg
nowidth: 1
---

<meta property="og:title" content="使用 Visual Studio 2015 编译 Python 2.7.11" />

![](https://img.shields.io/badge/python-2.7.11-brightgreen.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##سبب

يدعم النسخة الرسمية من Python 2.7 الإصدارات السابقة من Visual Studio 2010 للتجميع، راجع `PCbuild\readme.txt`:


	1.  Install Microsoft Visual Studio 2008, any edition.
	2.  Install Microsoft Visual Studio 2010, any edition, or Windows SDK 7.1 and any version of Microsoft Visual Studio newer than 2010.


إذا كنت تريد العبث بـ Python على نظام Windows، مثل تجميع نسخة Debug أو تعديل الكود المصدر بنفسك، فإن الطريقة الأسهل هي تثبيت VS2010.
ولكن بالنسبة لي شخصيًا، أفضل استخدام VS2015 لتجميع Python، الأسباب الرئيسية هي:


- VS2010 بالفعل عتيق قليلاً، إذ أن الوظائف والتجربة الخاصة به أسوأ بكثير مقارنة بـ VS2015. لقد كنت أستخدم VS2015، ولا أرغب حقاً في تثبيت VS2010 مرة أخرى.
بسبب الاستخدام المستمر لـ VS2015، ستتمكن من استخدامه لكتابة بعض البرامج الخاصة بك. إذا كنت ترغب في تضمين Python فيها، ستحتاج إلى استخدام نفس إصدار VS لترجمة برنامجك. إذا استخدمت إصدارًا مختلفًا من VS، فسوف تواجه مجموعة من المشاكل التي لا يمكن توقعها. [هنا توجد شرحًا أكثر تفصيلًا](http://siomsystems.com/mixing-visual-studio-versions/)。

所以我开始着手用 VS2015 搞定 Python 2.7.11 版本（当前的 Python 2.7 最新版本）。

يجب ملاحظة أن **Python 3.x** يدعم الآن ترجمة باستخدام **VS2015**.

##تحميل المصدر

إصدار Python بالطبع هو 2.7.11، بالإضافة إلى بعض الوحدات الخارجية. يمكنك تشغيل النصوص البرمجية `PCbuild\get_externals.bat` في دليل مصدر Python للحصول على جميع الوحدات اللازمة للترجمة. يرجى ملاحظة أنه يجب تثبيت svn، وإضافة svn.exe إلى مسار النظام.

قد يكون تنزيل الملفات غير مستقر، وقد يتوقف العملية بأكملها بسبب مشاكل في الشبكة، لذا يُنصح بتنزيل محتويات مجلد externals مباشرة من GitHub الخاص بي: [إصدار Python الخاص بي](https://github.com/disenone/wpython-2.7.11/tree/e13f43a3b72ae2bdf4d2950c6364750ae668cbf4/externals)

##عملية الترجمة

###وحدة الطرف الثالث

أول ما يجب حله هو وحدات الطرف الثالث، الأساسية هي tcl و tk و tcltk.

قم بتعديل الملف `externals/tcl-8.5.15.0/win/makefile.vc`، وقم بتغيير السطر 434 إلى

	- cdebug = -Zi -WX $(DEBUGFLAGS)
	+ cdebug = -Zi -WX- $(DEBUGFLAGS)

بالنسبة للخيار `WX`، يمكنك الاطلاع على الوثائق الرسمية لمايكروسوفت: [/WX (Treat Linker Warnings as Errors)](https://msdn.microsoft.com/en-us/library/ms235592.aspx)

再来改`PCbuild/tk.vcxproj`，用文本编辑器打开，修改 63, 64 行

ترجمة: 

قم بتعديل `PCbuild/tk.vcxproj`، افتحه باستخدام محرر نصوص، وقم بتعديل السطرين 63 و 64.

	- <TkOpts>msvcrt</TkOpts>
	- <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt</TkOpts>
	+ <TkOpts>msvcrt,noxp</TkOpts>
	+ <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt,noxp</TkOpts>

عدِّل `PCbuild/tcltk.props` عن طريق فتحه بواسطة محرر نصوص، ثم قم بتعديل السطر 41.

	- <BuildDirTop>$(BuildDirTop)_VC9</BuildDirTop>
	+ <BuildDirTop>$(BuildDirTop)_VC13</BuildDirTop>

نظرًا لأن VS2015 ألغى تعريف `timezone` واستبدله بـ `_timezone`، فيجب تعديل جميع الأماكن في الشيفرة التي تستخدم `timezone` إلى `_timezone`، ويحتاج الموديل الخارجي فقط إلى تعديل الملف `externals/tcl-8.5.15.0/win/tclWinTime.c`، بإضافة ما يلي في بداية الملف:

	#if defined _MSC_VER && _MSC_VER >= 1900
	#define timezone _timezone
	#endif

###ترجمة: تعديل مصدر Python

لديك مشكلة في `timezone` في وحدة Python `time` أيضًا، قم بتعديل السطر 767.

	- #ifdef __CYGWIN__
	+ #if defined(__CYGWIN__) || defined(_MSC_VER) && _MSC_VER >= 1900

ونظرًا لاستخدام Python طريقة خاصة في التحقق من صحة مقبض الملف في Windows، وهذه الطريقة تم حظرها تمامًا في VS2015، مما يؤدي إلى وجود أخطاء في الترجمة، لذا يتعين تعديلها أولاً. الملف `Include/fileobject.h`، الأسطر 73 و80.

	73 - #if defined _MSC_VER && _MSC_VER >= 1400
	73 + #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

	80 - #elif defined _MSC_VER && _MSC_VER >= 1200
	80 + #elif defined _MSC_VER && _MSC_VER >= 1200 && _MSC_VER < 1400

ملف `Modules/posixmodule.c`، السطر 532:

	- #if defined _MSC_VER && _MSC_VER >= 1400
	+ #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

至此，Python 就可以编译通过。更具体的修改可以看我 commit 的内容：[modify to build by vs2015]

ترجمة: 

بهذا، يمكن لـ Python أن يُجمع بنجاح. لمزيد من التعديلات المحددة، يمكنك الاطلاع على محتوى الـ commit الخاص بي: [تعديل للبناء بواسطة vs2015](https://github.com/disenone/wpython-2.7.11/commit/4037e2d806518dbf06ffb8ee5c46f419ef8d7edf)


###تحقق من المقابض غير الصالحة

على الرغم من تمرير عملية الترجمة، إلا أنه بسبب تجاهل النظام بشكل فظيع لمعالجة المقبض غير الصالح، يتسبب ذلك مباشرة في حدوث فشل عند الوصول إلى مقبض غير صالح (مثل إغلاق نفس الملف مرتين)، حيث يقوم Python بالتحقق مباشرة والبرنامج يتوقف، هذا النوع من Python لا يمكن استخدامه على الإطلاق. ال Python يستخدم طريقة خاصة جدًا لتجنب هذا السيناريو، لكن للأسف لا يمكن استخدامها في VS2015، ويتم شرح هذا في التعليق.

	Microsoft CRT in VS2005 and higher will verify that a filehandle is valid and raise an assertion if it isn't.


لحسن الحظ، هناك بالفعل حل. لقد رأيت ذلك في قضية Python، العنوان هنا: [issue23524](http://psf.upfronthosting.co.za/roundup/tracker/issue23524), [issue25759](http://psf.upfronthosting.co.za/roundup/tracker/issue25759)هذه الطريقة تُستخدم أيضًا في Python 3.x الحالي.


قوم عند استخدام مقبض الملفات بتعطيل آلية كراش الـ Windows واستبدالها بفحص رموز الخطأ. كيف يمكن تعطيل آلية الـ assert في Windows؟ الجواب يكمن في استخدام وظيفة معالجة الأخطاء الخاصة بك بدلاً من الوظيفة الافتراضية لـ Windows، وهنا الكود الرئيسي:


أنشئ ملف `PC/invalid_parameter_handler.c`، وقم بتعريف دالتنا الخاصة لمعالجة الأخطاء، يُمكن تجاهل الأخطاء المحدثة مؤقتاً.

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

定义两个宏方便更换错误处理函数，要注意是暂时的更换，之后是需要换回系统默认的  
تعريف ماكروين لتسهيل استبدال دالة معالجة الأخطاء، مع مراعاة أن الاستبدال مؤقت، ومن ثم يجب العودة إلى الإعدادات الافتراضية للنظام.

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

في الأماكن التي قد تؤدي إلى حدوث أخطاء في مقبض ملفات Windows، يجب إضافة الـ ماكرو `_Py_BEGIN_SUPPRESS_IPH` و `_Py_END_SUPPRESS_IPH` قبل وبعد ذلك على التوالي، بعد ذلك يمكن فحص رمز الخطأ، هناك العديد من الأماكن التي يجب تعديلها، يُرجى الرجوع إلى commit الخاص بشخص آخر لإجراء التعديلات:
[في هنا](https://github.com/kovidgoyal/cpython/commit/a9ec814d466d3c0139d10b69666f88eed10e4940)

##انتهاء

حتى الآن يمكن ترجمة وتشغيل Python 2.7.11 بشكل طبيعي في VS2015، ولكن من الجدير بالذكر أن الفريق الرسمي لـ Python لا يوصي بهذا الإعداد.

	***WARNING***
	Building Python 2.7 for Windows using any toolchain that doesn't link
	against MSVCRT90.dll is *unsupported* as the resulting python.exe will
	not be able to use precompiled extension modules that do link against
	MSVCRT90.dll.

لذا من الأفضل الانتباه عند الاستخدام.

--8<-- "footer_ar.md"


> هذه المشاركة تم ترجمتها باستخدام ChatGPT. يرجى تقديم [**ردود فعل**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
