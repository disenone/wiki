---
layout: post
title: كتابة كاشف تسرب الذاكرة في نظام Windows
categories:
- c++
tags:
- dev
description: 'ترجمتُ هذا النص إلى اللغة العربية:


  قرأت مؤخرًا "تنمية البرمجيات الذاتية للمبرمجين: الربط، والتحميل، والمكتبة" (المختصرة
  بـ "الربط" فيما بعد) واستفدت كثيرًا، وأنا أقوم بالتفكير في إمكانية إعداد بعض الشيفرات
  البرمجية الصغيرة ذات الصلة. لقد علمت عن أداة كشف تسريب الذاكرة في Windows تُدعى
  [Visual Leak Detector](https://vld.codeplex.com/)،هذه الأداة تتتبع تخصيص وإطلاق
  الذاكرة من خلال استبدال واجهات dll المسؤولة عن إدارة الذاكرة في نظام التشغيل Windows.
  لذلك قررت الاستفادة من Visual Leak Detector (يُشار إليه اختصارًا باسم VLD) لإنشاء
  أداة بسيطة لاكتشاف تسرب الذاكرة وفهم روابط الملفات dll.'
figures:
- assets/post_assets/2016-6-11-memory-leak-detector/depends.png
---

<meta property="og:title" content="编写 Windows 下的 Memory Leak Detector" />

![](https://img.shields.io/badge/windows-10-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##المقدمة

قرأت مؤخرًا "التطوير الشخصي للمبرمج: الربط، التحميل والمكتبة" (سنشير إليه فيما بعد باسم "الربط")، وقد استفدت كثيرًا منه، وأفكر في إمكانية كتابة بعض الشيفرات الصغيرة المتعلقة به. لقد عرفت بالصدفة أن هناك أداة في Windows لاكتشاف تسريب الذاكرة [Visual Leak Detector](https://vld.codeplex.com/)، يتم تتبع تخصيص وإطلاق الذاكرة من خلال استبدال واجهات DLL المسؤولة عن إدارة الذاكرة في Windows. لذا تم اتخاذ قرار بالاستعانة بأداة Visual Leak Detector (المُختصرة بـVLD فيما بعد) كنموذج لأداة فحص تسريب الذاكرة البسيطة، لفهم روابط ملفات DLL.

##معرفة مسبقة
"الروابط" يفصيح كتاب عن مبادئ روابط الملفات التنفيذية في Linux وWindows، حيث يسمى شكل الملف التنفيذي في Windows بـ PE (Portable Executable). أما تفسير الملفات DLL هو كما يلي:

> ملفات DLL هي اختصار لمكتبات الربط الديناميكي، تعادل بمكتبات الأشياء المشتركة في نظام Linux. يعتمد النظام الويندوز بشكل كبير على آلية الـ DLL، حتى بنية نواة الويندوز تعتمد بشكل كبير على ذلك. يعتبر الملفات الـ DLL والملفات القابلة للتنفيذ (EXE) تقريبًا نفس المفهوم في ويندوز، فكليهما عبارة عن ملفات ثنائية بتنسيق PE، الاختلاف البسيط بينهما يكمن في وجود علامة في رأس ملف PE تشير إلى ما إذا كان الملف تنفيذيًا أم مكتبة ربط ديناميكية. عادة ما يكون امتداد الملفات الـ DLL .dll، ولكن يمكن أيضًا أن يكون مثلا .ocx (مراقبة OCX) أو .CPL (برنامج لوحة التحكم).

ثمَّ تيجأ صُناديق توسيع اللغات مثل Python مثل الملفات .pyd. بينما مفهوم الكشف عن تسرب الذاكرة هنا هو **جدول التصدير والاستيراد الرمزي** في ملفات DLL.

####جدول التصدير الرمزي

> عندما يحتاج ملف PE ما إلى توفير بعض الدوال أو المتغيرات لاستخدامها من قبل ملفات PE أخرى، نسمي هذا السلوك باسم **تصدير الرموز (Symbol Exporting)**.

فهم ببساطة، في بيئة Windows PE، يتم تخزين جميع الرموز المصدرية المصدرة في هيكل يسمى جدول التصدير (Export Table)، حيث يوفر هذا الهيكل علاقة تعيين بين اسم الرمز وعنوان الرمز. والرموز التي تحتاج إلى تصديرها يجب أن تُضاف إليها المحدد "__declspec(dllexport)".

####الرموز جدول الاستيراد

جدول استيراد الرموز هو المفهوم الرئيسي هنا، وهو يقابل جدول تصدير الرموز، دعنا نلقي نظرة أولاً على شرح المفهوم:

> إذا استخدمنا في برنامج ما دوالاً أو متغيرات من ملف DLL ، فإننا نُسمي هذا السلوك **استيراد الرموز (Symbol Importing)**.

يُطلق على الهيكل الذي يحتوي على رموز المتغيرات والدوال التي يجب استيرادها، بالإضافة إلى معلومات الموديول التي تحتوي عليها، والمحفوظ في نظام Windows PE باسم **جدول الاستيراد (Import Table)**. عندما يُحمّل ملف PE في نظام Windows، يقوم بتحديد عناوين جميع الدوال المطلوبة للاستيراد وضبط عناصر جدول الاستيراد إلى العناوين الصحيحة، ليتمكن البرنامج أثناء التشغيل من تحديد عنوان الدوال الفعلي عبر الاستعلام عن جدول الاستيراد واستدعائها. أهم هيكل في جدول الاستيراد هو **جدول عناوين الاستيراد (Import Address Table، IAT)**، حيث يتم تخزين عناوين الدوال المستوردة فيه.

عند رؤية هذا المكان، هل لديكم فكرة عن كيفية إجراء الكشف عن تسرب الذاكرة الذي نريد تحقيقه :)؟ الإجابة الصحيحة هي اختراق جدول الاستيراد، بمعنى أنه يتم تغيير عناوين الدوال المسؤولة عن طلب وإطلاق الذاكرة في جدول الاستيراد للوحدات التي نحتاج إلى مراقبتها، ليتم تعيينها بدوال تم تعريفها من قبلنا. بهذه الطريقة، نحن قادرون على معرفة كيفية طلب وإطلاق الذاكرة في كل مرة لوحدة معينة، مما يتيح لنا إجراء الكشف الذي نريده بحرية.

يمكنك العثور على معلومات أكثر تفصيلاً حول روابط ملفات DLL في "الربط" أو مصادر أخرى.

## Memory Leak Detector

بعد معرفة المبدأ، الخطوة التالية هي تنفيذ كشف تسرب الذاكرة بناءً على هذا المبدأ. سيستند شرح الخطوة التالية إلى التنفيذ الخاص بي، والذي نشرته على موقعي على Github: [LeakDetector](https://github.com/disenone/LeakDetector)I am unable to translate the text as it does not contain any meaningful content. If you have any other text you would like me to translate, please provide it.

####استبدال الدالة

الآن سنلقي نظرة على الدوال الحيوية، الموجودة في [RealDetector.cpp](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)I'm sorry, but I cannot provide a translation for this text as it does not contain any content to be translated. If you have more text to translate, please provide it so I can assist you.

```cpp linenums="1"
قم بتبديل وظيفة معينة في جدول عناوين الاستيراد (IAT) في importModule بوظيفة أخرى.
importModule سيستدعي وظيفةً من وحدة أخرى، وهذه الوظيفة هي التي تحتاج إلى تعديل.
ما علينا سوى تحويل import module إلى استدعاء وظيفتنا المخصصة.
 *
- استيراد الوحدة (IN): الوحدة التي يجب معالجتها، هذه الوحدة تستدعي وظائف يتعين تعديلها في وحدات أخرى
 *
- exportModuleName (IN): اسم الوحدة التي تأتي منها الدوال التي تحتاج إلى تعديل
 *
exportModulePath (IN): مسار وجود وحدة التصدير، يتم محاولة تحميل وحدة التصدير أولاً باستخدام المسار،
إذا فشل، استخدم name للتحميل
- اسم الاستيراد (IN): اسم الوظيفة
 *
- استبدال: 替代的函数指针
 *
قيمة العودة: true إذا نجحت، وإلا فإنها تكون false
*/
bool RealDetector::patchImport(
	HMODULE importModule,
	LPCSTR exportModuleName,
	LPCSTR exportModulePath,
	LPCSTR importName,
	LPCVOID replacement)
{
	HMODULE                  exportmodule;
	IMAGE_THUNK_DATA        *iate;
	IMAGE_IMPORT_DESCRIPTOR *idte;
	FARPROC                  import;
	DWORD                    protect;
	IMAGE_SECTION_HEADER    *section;
	ULONG                    size;

	assert(exportModuleName != NULL);

	idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
		TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
	if (idte == NULL) 
	{
		logMessage("patchImport failed: idte == NULL\n");
		return false;
	}
	while (idte->FirstThunk != 0x0) 
	{
		if (strcmp((PCHAR)R2VA(importModule, idte->Name), exportModuleName) == 0) 
		{
			break;
		}
		idte++;
	}
	if (idte->FirstThunk == 0x0) 
	{
		logMessage("patchImport failed: idte->FirstThunk == 0x0\n");
		return false;
	}

	if (exportModulePath != NULL) 
	{
		exportmodule = GetModuleHandleA(exportModulePath);
	}
	else 
	{
		exportmodule = GetModuleHandleA(exportModuleName);
	}
	assert(exportmodule != NULL);
	import = GetProcAddress(exportmodule, importName);
	assert(import != NULL);

	iate = (IMAGE_THUNK_DATA*)R2VA(importModule, idte->FirstThunk);
	while (iate->u1.Function != 0x0) 
	{
		if (iate->u1.Function == (DWORD_PTR)import) 
		{
			VirtualProtect(&iate->u1.Function, sizeof(iate->u1.Function), 
				PAGE_READWRITE, &protect);
			iate->u1.Function = (DWORD_PTR)replacement;
			VirtualProtect(&iate->u1.Function, sizeof(iate->u1.Function), 
				protect, &protect);
			return true;
		}
		iate++;
	}

	return false;
}

```

لنحلل هذه الوظيفة، كما ورد في التعليق، فوظيفة هذه الوظيفة هي تغيير عنوان دالة معينة داخل IAT إلى عنوان دالة أخرى. دعونا نلقي نظرة على السطرين 34-35:

``` cpp
idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
	TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
```

يمكن لوظيفة ImageDirectoryEntryToDataEx إرجاع عنوان هيكل معين في رأس الملف للوحدة، وبما أن IMAGE_DIRECTORY_ENTRY_IMPORT يحدد هيكل جدول الاستيراد الذي يجب استدعاؤه، فإن العائد idte سيشير مباشرة إلى جدول استيراد الوحدة.

36-40 السطور هي للتحقق من صحة `idte`. السطر 41، `idte->FirstThunk` يشير فعلاً إلى IAT الفعلية. لذا، 41-48 السطور هي للبحث عن الوحدة النمطية التي تحتاج إلى استبدال وظائفها بناءً على اسم الوحدة النمطية. إذا تعذر العثور عليها، فهذا يعني أنه لم يتم استدعاء وظائف هذه الوحدة النمطية، ويجب فقط عرض رسالة خطأ والعودة.

بمجرد العثور على الوحدة، بطبيعة الحال، نحن بحاجة إلى العثور على الدالة التي سيتم استبدالها، انتقل إلى السطر 55-62 لفتح الوحدة التابعة للدالة، ثم السطر 64 للعثور على عنوان الدالة. نظرًا لعدم حفظ IAT للاسم، فإنه من الضروري أولاً تحديد الدالة بناءً على عنوان الدالة الأصلي، ثم تعديل عنوان هذه الدالة، السطور 68-80 هي ببساطة تنفيذ هذه العملية. بعد العثور الناجح على الدالة، يتم تعديل العنوان ببساطة إلى عنوان "replacement".

بهذا، تمكنا بنجاح من استبدال الدوال في IAT.

####الموديولات وأسماء الدوال

على الرغم من أننا قمنا بتنفيذ استبدال وظيفة IAT `patchImport`، إلا أن هذه الوظيفة تتطلب تحديد اسم الوحدة واسم الوظيفة، فكيف نعرف أي وحدة ووظيفة تم استخدامها لتخصيص وتحرير الذاكرة في البرنامج؟ لفهم هذه المشكلة، نحتاج إلى الاعتماد على أداة في Windows تدعى [Dependency Walker](http://www.dependencywalker.com/)أنشئ مشروع جديد في Visual Studio، واستخدم الأمر `new` في دالة `main` لطلب تخصيص ذاكرة، ثم قم بتصحيح إصدار Debug. بعد ذلك، استخدم الأداة `depends.exe` لفتح ملف exe الذي تم تصحيحه. سترى واجهة مشابهة للتالية (باستخدام مشروعي [LeakDetectorTest](https://github.com/disenone/LeakDetector/tree/master/LeakDetectorTest)وُجِبَتـْ تۤرجَمَه أو التحريـف الىِ اللغةِ العربيـة.

![](assets/img/2016-6-11-memory-leak-detector/depends.png)

يمكن رؤية أن LeakDetectorTest.exe استخدمت `malloc` و `_free_dbg` من داخل uscrtbased.dll (غير معروضة في الصورة)، هذين الدالتين هما اللذان يجب علينا استبدالهما. يجب الانتباه إلى أن أسماء الدوال الفعلية قد تختلف اعتمادًا على إصدار ويندوز وفيجوال ستوديو الخاص بك، أنا استخدم ويندوز 10 وفيجوال ستوديو 2015، كل ما عليك فعله هو استخدام depends.exe لمعرفة الدوال التي تم استدعاؤها فعليًا.

####تحليل استدعاء الكومة

تحتاج تسجيل تخصيص الذاكرة إلى تسجيل معلومات الكومة التي تم تحديدها في ذلك الوقت. هنا لا أنوي تقديم شرح مفصل حول كيفية الحصول على معلومات الكومة الحالية في نظام Windows. الوظيفة ذات الصلة هي `RtlCaptureStackBackTrace` وهناك العديد من الموارد عبر الإنترنت ذات الصلة التي يمكن الاطلاع عليها، يمكنك أيضًا النظر في الوظيفة داخل كودي [`printTrace`](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)I'm sorry, but the text you provided appears to be a punctuation mark and does not contain any content to be translated.

####فحص تسرب الذاكرة

حتى الآن، لقد جمعنا كل كرات التنين، الآن نحن نستدعي الطائر الأسطوري.

أرغب في تنفيذ قدرة على اكتشاف تسرب الذاكرة محليًا (وهذا يختلف عن VLD، حيث يقوم VLD بالكشف عالميًا ويدعم عدة خيوط). لذا، في قمة الإحترافية قمت بتغليف كائن الاستبيان `LeakDetector` الذي يُعمل عن طريق استبدال الوظائف بطبقة أُخرى من البرمجة في كائن `RealDetector`، وقمت بعرض واجهة `LeakDetector` للمستخدمين. كل ما عليهم القيام به هو بناء `LeakDetector` عند الاستخدام، وستكتمل عملية استبدال الوظائف وبدء اكتشاف تسرب الذاكرة. عند تدمير `LeakDetector`، سيتم استعادة الوظائف الأصلية، وإيقاف اكتشاف تسرب الذاكرة، مع طباعة نتائج اكتشاف تسرب الذاكرة.

استخدم الكود التالي لاختباره:

```cpp
#include "LeakDetector.h"
#include <iostream>
using namespace std;

void new_some_mem()
{
	char* c = new char[12];
	int* i = new int[4];
}

int main()
{
	auto ld = LDTools::LeakDetector("LeakDetectorTest.exe");
	new_some_mem();
    return 0;
}

```

أنشأ الكود ذاكرة جديدة مباشرةً باستخدام `new`، ولم يقم بتحريرها قبل الخروج مباشرةً، ونتيجة ذلك، طبع البرنامج:

```
============== LeakDetector::start ===============
LeakDetector init success.
============== LeakDetector::stop ================
Memory Leak Detected: total 2

Num 1:
    e:\program\github\leakdetector\leakdetector\realdetector.cpp (109): LeakDetector.dll!LDTools::RealDetector::_malloc() + 0x1c bytes
    f:\dd\vctools\crt\vcstartup\src\heap\new_scalar.cpp (19): LeakDetectorTest.exe!operator new() + 0x9 bytes
    f:\dd\vctools\crt\vcstartup\src\heap\new_array.cpp (15): LeakDetectorTest.exe!operator new[]() + 0x9 bytes
    e:\program\github\leakdetector\leakdetectortest\leakdetectortest.cpp (12): LeakDetectorTest.exe!new_some_mem() + 0x7 bytes
    e:\program\github\leakdetector\leakdetectortest\leakdetectortest.cpp (19): LeakDetectorTest.exe!main()
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (74): LeakDetectorTest.exe!invoke_main() + 0x1b bytes
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (264): LeakDetectorTest.exe!__scrt_common_main_seh() + 0x5 bytes
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (309): LeakDetectorTest.exe!__scrt_common_main()
    f:\dd\vctools\crt\vcstartup\src\startup\exe_main.cpp (17): LeakDetectorTest.exe!mainCRTStartup()
    KERNEL32.DLL!BaseThreadInitThunk() + 0x24 bytes
    ntdll.dll!RtlUnicodeStringToInteger() + 0x253 bytes
    ntdll.dll!RtlUnicodeStringToInteger() + 0x21e bytes

Num 2:
    e:\program\github\leakdetector\leakdetector\realdetector.cpp (109): LeakDetector.dll!LDTools::RealDetector::_malloc() + 0x1c bytes
    f:\dd\vctools\crt\vcstartup\src\heap\new_scalar.cpp (19): LeakDetectorTest.exe!operator new() + 0x9 bytes
    f:\dd\vctools\crt\vcstartup\src\heap\new_array.cpp (15): LeakDetectorTest.exe!operator new[]() + 0x9 bytes
    e:\program\github\leakdetector\leakdetectortest\leakdetectortest.cpp (11): LeakDetectorTest.exe!new_some_mem() + 0x7 bytes
    e:\program\github\leakdetector\leakdetectortest\leakdetectortest.cpp (19): LeakDetectorTest.exe!main()
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (74): LeakDetectorTest.exe!invoke_main() + 0x1b bytes
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (264): LeakDetectorTest.exe!__scrt_common_main_seh() + 0x5 bytes
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (309): LeakDetectorTest.exe!__scrt_common_main()
    f:\dd\vctools\crt\vcstartup\src\startup\exe_main.cpp (17): LeakDetectorTest.exe!mainCRTStartup()
    KERNEL32.DLL!BaseThreadInitThunk() + 0x24 bytes
    ntdll.dll!RtlUnicodeStringToInteger() + 0x253 bytes
    ntdll.dll!RtlUnicodeStringToInteger() + 0x21e bytes
```

يتم اكتشاف المكانين الذان لم يُفرج فيهما عن الذاكرة التي تم طلبها بشكل صحيح في البرنامج، وتُطبع معلومات كاملة عن مكدس الاستدعاء، لقد تم إتمام الوظيفة التي نحتاج إليها حتى الآن.

###ختام

عندما لا تزال غير ملم بالروابط البرمجية والتحميل والمكتبات، قد تجد صعوبة في فهم كيفية العثور على وظائف مكتبة روابط مشتركة، لا تتحدثوا عن استبدال وظائف مكتبة الروابط بالوظائف الخاصة بنا. هنا سنأخذ كشف تسرب الذاكرة كمثال، ونناقش كيفية استبدال وظائف ملفّات DLL في Windows، يمكنكم الرجوع إلى مصدر VLD للحصول على التفاصيل الأكثر تفصيلاً.

ما أريد قوله هو أن "برمجة تطوير الذات: الارتباط، التحميل، والمكتبة" كتاب جيد حقًا، ويثير المشاعر بدون دعاية.

--8<-- "footer_ar.md"


> هذا المنشور تمت ترجمته باستخدام ChatGPT، يرجى تقديم [**ردود**](https://github.com/disenone/wiki_blog/issues/new)تحدث إذا وجدت أي شيء مفقودًا. 
