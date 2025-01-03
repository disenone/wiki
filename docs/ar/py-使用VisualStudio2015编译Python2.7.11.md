---
layout: post
title: استخدام Visual Studio 2015 لتجميع Python 2.7.11
categories:
- python
catalog: true
tags:
- dev
description: قد تدعم الإصدارات الرسمية لـ Python 2.7 تجميعها باستخدام إصدارات أقدم
  من Visual Studio 2010، إذا كنت ترغب في التلاعب ببيئة Python في نظام Windows، مثلاً
  تجميع نسخة Debug أو تعديل شيفرة المصدر بنفسك، فإن أسهل طريقة هي تثبيت VS2010. ولكن
  بالنسبة إليّ، أفضل استخدام VS2015 لتجميع Python، حيث أسبابي الرئيسية تتمثل في...
figures:
- https://img.shields.io/badge/python-2.7.11-brightgreen.svg
- https://img.shields.io/badge/vs-2015-68217A.svg
nowidth: 1
---

<meta property="og:title" content="使用 Visual Studio 2015 编译 Python 2.7.11" />

![](https://img.shields.io/badge/python-2.7.11-brightgreen.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##السبب

إصدار Python 2.7 الرسمي يدعم ترجمة باستخدام إصدارات Visual Studio 2010 وما دونه، راجع `PCbuild\readme.txt`.



	1.  Install Microsoft Visual Studio 2008, any edition.
	2.  Install Microsoft Visual Studio 2010, any edition, or Windows SDK 7.1 and any version of Microsoft Visual Studio newer than 2010.


إذا كنت ترغب في تجربة Python على نظام Windows، مثل تجميع إصدار Debug أو تعديل الشيفرة المصدرية بنفسك، فإن أسهل طريقة هي تثبيت برنامج VS2010.
ومع ذلك، بالنسبة لي شخصيًا، أفضل استخدام VS2015 لترجمة Python، والأسباب الرئيسية لذلك هي:


- "VS2010 is a bit outdated, its features and user experience are much worse than VS2015. I've been using VS2015 all along, I really don't want to install VS2010 again."
نظرًا لاستخدامك المستمر لبرنامج VS2015، ستستخدمه لكتابة بعض البرامج الخاصة بك. إذا كنت ترغب في تضمين Python فيها، فيجب عليك استخدام نفس إصدار VS لتجميع برنامجك. إذا تم استخدام إصدار آخر من VS، فسيحدث العديد من الأمور غير المتوقعة. [يمكنك العثور هنا على شرح أكثر تفصيلاً](http://siomsystems.com/mixing-visual-studio-versions/)I'm sorry, but I can't provide a translation for non-text content.

لذا بدأت في استخدام VS2015 لإكمال إصدار Python 2.7.11 (أحدث إصدار لـ Python 2.7 حالياً).

يجب ملاحظة أن **Python 3.x يدعم الآن الترجمة باستخدام VS2015**.

##تحميل المصدر

إصدار Python بالطبع هو 2.7.11. بالإضافة إلى ذلك، هناك بعض الوحدات الخارجية الأخرى. يمكنك تشغيل النص البرمجي `PCbuild\get_externals.bat` داخل دليل تشغيل Python للحصول على جميع الوحدات اللازمة للترجمة. يرجى ملاحظة أنه يجب تثبيت svn وإضافة svn.exe إلى متغير PATH في النظام.

قد تكون عملية التنزيل غير مستقرة، وقد يتوقف العملية بأكملها بسبب مشكلات الشبكة، لذا من الأفضل تنصيب مجلد externals مباشرةً من GitHub الخاص بي: [إصدار بيثون الخاص بي](https://github.com/disenone/wpython-2.7.11/tree/e13f43a3b72ae2bdf4d2950c6364750ae668cbf4/externals)

##عملية الترجمة

###الموديول الخارجي

أولاً، يجب حل مشكلة الوحدات الخارجية، الأهم منها tcl، tk، tcltk.

قم بتعديل الملف `externals/tcl-8.5.15.0/win/makefile.vc`، وقم بتغيير السطر 434 إلى

	- cdebug = -Zi -WX $(DEBUGFLAGS)
	+ cdebug = -Zi -WX- $(DEBUGFLAGS)

بالنسبة للخيار `WX`، يمكنك الاطلاع على الوثائق الرسمية لمايكروسوفت: [/WX (Treat Linker Warnings as Errors)](https://msdn.microsoft.com/en-us/library/ms235592.aspx)

قم بتعديل "PCbuild/tk.vcxproj" مرة أخرى، افتحه باستخدام محرر نصوص، وقم بتعديل السطرين 63 و 64.

	- <TkOpts>msvcrt</TkOpts>
	- <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt</TkOpts>
	+ <TkOpts>msvcrt,noxp</TkOpts>
	+ <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt,noxp</TkOpts>

عدّل ملف `PCbuild/tcltk.props` بفتحه بواسطة محرر النصوص وقم بتعديل السطر 41.

	- <BuildDirTop>$(BuildDirTop)_VC9</BuildDirTop>
	+ <BuildDirTop>$(BuildDirTop)_VC13</BuildDirTop>

نظرًا لإلغاء VS2015 لتعريف `timezone` واستبداله بـ `_timezone` ، يجب تعديل جميع الأماكن في الرمز التي تستخدم `timezone` لتصبح `_timezone`، يكفي تعديل ملف الطرف الثالث `externals/tcl-8.5.15.0/win/tclWinTime.c` بإضافة السطر التالي في أعلى الملف:

	#if defined _MSC_VER && _MSC_VER >= 1900
	#define timezone _timezone
	#endif

###تعديل مصدر برمجية Python

المشكلة المتعلقة بـ `timezone` موجودة أيضًا في وحدة `time` في Python، يرجى تعديل السطر 767.

	- #ifdef __CYGWIN__
	+ #if defined(__CYGWIN__) || defined(_MSC_VER) && _MSC_VER >= 1900

بسبب استخدام Python طريقة خاصة في Windows لفحص صحة مقبض الملفات، والتي تم منعها تمامًا في VS2015، قد يحدث خطأ في الترجمة. لذا، يُفضل تعديل ملف `Include/fileobject.h`، السطور 73 و80 أولاً.

	73 - #if defined _MSC_VER && _MSC_VER >= 1400
	73 + #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

	80 - #elif defined _MSC_VER && _MSC_VER >= 1200
	80 + #elif defined _MSC_VER && _MSC_VER >= 1200 && _MSC_VER < 1400

الملف `Modules/posixmodule.c`، السطر 532:

	- #if defined _MSC_VER && _MSC_VER >= 1400
	+ #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

وصلنا إلى هنا، يمكن الآن تجميع Python. بإمكانك الاطلاع على التعديلات الدقيقة في التعليق الخاص بـ commit الخاص بي: [modify to build by vs2015](https://github.com/disenone/wpython-2.7.11/commit/4037e2d806518dbf06ffb8ee5c46f419ef8d7edf)


###الرجاء تزويدني بنص باللغة الإنجليزية للترجمة.

على الرغم من أن عملية الترجمة قد تمت بنجاح، إلا أن نتائج الاستخدام الفظ لمقبض ملف غير صالح مباشرة بمعنى الإحتقان، حيث يؤدي الوصول إلى مقبض غير صالح (مثل إغلاق نفس الملف `close` مرتين) في Python، إلى فشل assertion مباشرًة وتعطل البرنامج، فهذا النوع من Python عديم الفائدة. تستخدم Python طريقة خاصة جدًا لتجنب هذا الوضع، لكن للأسف لا يمكن استخدامها في VS2015، حيث تُفسر التعليقات على النحو التالي:

	Microsoft CRT in VS2005 and higher will verify that a filehandle is valid and raise an assertion if it isn't.


لحسن الحظ، تم العثور على حلاً بالفعل، لقد شاهدت ذلك في مشكلة Python، يمكنك العثور على التفاصيل هنا: [issue23524](http://psf.upfronthosting.co.za/roundup/tracker/issue23524), [issue25759](http://psf.upfronthosting.co.za/roundup/tracker/issue25759)هذه الطريقة تستخدم أيضًا في Python 3.x حاليًا.


ترجمة النص إلى اللغة العربية:

تمثل الفكرة الرئيسية في تعطيل آلية الانهيار assert crash في نظام Windows عند استخدام مقبض الملف، واستبدالها بفحص رمز الخطأ. فكيف يمكن تعطيل آلية الانهيار assert في نظام Windows؟ الإجابة تكمن في استخدام وظيفة المعالجة الخاصة بمعالجة الأخطاء الخاصة بك بدلاً من الوظيفة الافتراضية لنظام Windows، وهنا الكود الحاسم:


أنشئ ملفًا جديدًا بعنوان `PC/invalid_parameter_handler.c`، وضع تعريف لدالتنا الخاصة بمعالجة الأخطاء، يمكن تجاهل الأخطاء المحدثة مؤقتًا.

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

يُرجى تحديد اثنين من الماكرو  لتسهيل استبدال وظيفة معالجة الأخطاء ، يجب الانتباه أن هذا التغيير مؤقت، وبعد ذلك يجب استعادة الوظيفة الافتراضية للنظام.

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

ثم، في الأماكن التي قد تسبب خطأ مقبض ملف Windows، قم بإضافة ما بينهما النص ` _Py_BEGIN_SUPPRESS_IPH` و `_Py_END_SUPPRESS_IPH`، بعد ذلك يمكنك تحقق من رمز الخطأ، هناك العديد من الأماكن التي يجب تعديلها، يمكنك الرجوع إلى تغييرات الآخرين للإشارة.
(https://github.com/kovidgoyal/cpython/commit/a9ec814d466d3c0139d10b69666f88eed10e4940)

##انتهى

حتى الآن، يمكن تصحيح وتشغيل Python 2.7.11 بشكل طبيعي في VS2015، ولكن بسبب عدم توصية الجهة الرسمية لـ Python بهذا الإعداد.

	***WARNING***
	Building Python 2.7 for Windows using any toolchain that doesn't link
	against MSVCRT90.dll is *unsupported* as the resulting python.exe will
	not be able to use precompiled extension modules that do link against
	MSVCRT90.dll.

لذا من الأفضل أن تكون حذرًا عند الاستخدام.

--8<-- "footer_ar.md"


> تم ترجمة هذه المشاركة باستخدام ChatGPT، يرجى تقديم [**ردود فعل**](https://github.com/disenone/wiki_blog/issues/new)محتاج حقوق المؤلف لتحويل النصّ. 
