---
layout: post
title: "编写 Windows 下的 Memory Leak Detector  \nكتابة كاشف تسرب الذاكرة في نظام ويندوز"
categories:
- c++
tags:
- dev
description: 'ترجم هذه النصوص إلى اللغة العربية:


  في الوقت الحالي، انتهيت من قراءة "برمجيات التنمية الذاتية للمبرمجين: الروابط والتحميل
  والمكتبات" (يشار إليها فيما بعد باسم "الروابط")، وقد اكتسبت العديد من الفوائد، وأنا
  أفكر في إمكانية كتابة بعض الشفرات الصغيرة ذات الصلة. لقد اكتشفت بالصدفة أن هناك
  أداة لفحص تسرب الذاكرة في Windows تُعرف باسم [Visual Leak Detector](https://vld.codeplex.com/)يتم
  تتبع تخصيص الذاكرة وإطلاقها من خلال استبدال واجهات dll المسؤولة عن إدارة الذاكرة
  في Windows. لذا قررت الاستعانة بأداة الكشف البسيطة عن تسرب الذاكرة مستوحاة من Visual
  Leak Detector (يُشار إليها فيما بعد ب VLD)، حتى أفهم روابط ملفات dll.'
figures:
- assets/post_assets/2016-6-11-memory-leak-detector/depends.png
---

<meta property="og:title" content="编写 Windows 下的 Memory Leak Detector" />

![](https://img.shields.io/badge/windows-10-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##المقدمة

لقد انتهيت مؤخرًا من قراءة "برمجية النمو الذاتي: الربط، والتحميل، والمكتبات" (اختصارها كـ "الربط") وكانت تجربة مفيدة. أنا أفكر في إنشاء بعض الشيفرات الصغيرة ذات الصلة. لدي معرفة بأن هناك أداة في Windows تُستخدم للكشف عن تسرّب الذاكرة، تدعى [Visual Leak Detector](https://vld.codeplex.com/)هذه الأداة تتبع تخصيص وإطلاق الذاكرة عن طريق استبدال واجهات dll المسؤولة عن إدارة الذاكرة في نظام Windows. لذا تم اتخاذ قرار بالاستعانة بـ Visual Leak Detector (يشار إليه فيما بعد بـ VLD) لإنشاء أداة بسيطة للكشف عن تسرب الذاكرة وفهم روابط dll.

##الجاهزية الأولية
ترجمة النص إلى اللغة العربية:

"الروابط" تفسر بالتفصيل مبدأ روابط الملفات التنفيذية في Linux و Windows، حيث يُشار إلى تنسيق الملفات التنفيذية في Windows بـ PE (Portable Executable). وأما تفسير ملفات DLL، فيكون على النحو التالي:

> مختصر DLL يُشير إلى مكتبة الروابط الديناميكية (Dynamic-Link Library)، وهي ما يعادل الكائن المشترك (Shared Object) بنظام Linux. يتم استخدام هذه الآلية بشكل كبير في نظام Windows، حتى هيكل نواة ويندوز يعتمد إلى حد كبير على آلية DLL. الملفات DLL وملفات EXE تحت نظام Windows في الواقع نفس المفهوم، حيث إنهما يكونان من الملفات الثنائية بتنسيق PE، الفرق البسيط هو أن رأس ملف PE يحتوي على رمز يُشير إلى ما إذا كان الملف ملف EXE أو DLL، وقد لا تنتهي اسماء ملفات DLL بالضرورة بـ .dll، بل يمكن أن تكون مثلاً .ocx (تحكم OCX) أو .CPL (برنامج لوحة التحكم).

还有比如 Python 的扩展文件 .pyd。而 DLL 中有关我们这里内存泄露检测的概念是**符号导出导入表**。 

وأيضًا مثل ملف توسيع بايثون .pyd. أما مفهوم كشف تسرب الذاكرة هنا في DLL فهو **جدول تصدير واستيراد الرموز**.

####جدول تصدير الرموز

> عندما يحتاج PE إلى تقديم بعض الدوال أو المتغيرات لاستخدامها بواسطة ملفات PE الأخرى، فإننا نسمي هذا السلوك **تصدير الرموز (Symbol Exporting)**.

ببساطة، في Windows PE، يتم تخزين جميع الرموز المصدرة في هيكل يُسمى **جدول التصدير (Export Table)**، الذي يوفر علاقة بين أسماء الرموز وعناوينها. يجب إضافة المُعدِّل `__declspec(dllexport)` للرموز التي تحتاج إلى التصدير.

####جدول استيراد الرموز

الجدول المستورد للرموز هو المفهوم الرئيسي هنا، ويتوافق مع جدول التصدير للرموز، دعنا نلقي نظرة أولًا على شرح المفهوم:

> إذا استخدمنا دالة أو متغير من DLL في برنامج معين، فإننا نسمي هذا السلوك **استيراد الرموز (Symbol Importing)**.

عندما يُطلب من ويندوز PE أن يحتفظ بمعلومات الشخصيات والدوال التي يجب عليه استيرادها وأين توجد، يتم تسمية الهيكل الناتج عن ذلك باسم **جدول الاستيراد (Import Table)**. عندما يُحمّل ملف PE في نظام ويندوز، أحد الأمور التي يجب القيام بها هو تحديد عناوين جميع الدوال التي يجب استيرادها وضبط عناصر جدول الاستيراد إلى العناوين الصحيحة. يتيح ذلك للبرنامج، عند التشغيل، تحديد عناوين الدوال الفعلية عن طريق الاستعلام عن جدول الاستيراد والقيام بالاستدعاءات. أما أهم هيكل في جدول الاستيراد فهو **جدول عناوين الاستيراد (Import Address Table، IAT)**، حيث يتم تخزين عناوين الدوال المستوردة بشكل فعلي فيه.

عند رؤية هذا المحتوى هل تعقد أنك قد تخمنت بالفعل كيف يتم اكتشاف تسرب الذاكرة الذي نريد تحقيقه :)؟ بالضبط، نعم، يتم ذلك عن طريق اختراق جدول الاستيراد، بمعنى أدق، هو تغيير عنوان وظائف طلب الذاكرة وإطلاقها في جدول الاستيراد للوحدات التي نريد فحصها بواسطة وظيفتنا المخصصة. وهكذا، يمكننا معرفة كل عملية طلب وإطلاق للذاكرة التي تتم في الوحدة، مما يسمح لنا بإجراء الفحوصات التي نرغب في تنفيذها بحرية.

يمكنك الاطلاع على المزيد من المعلومات المفصلة حول روابط مكتبات دايناميكية (DLL) في كتاب "الروابط" أو في مصادر أخرى.

## Memory Leak Detector

عرفت المبدأ، الآن سأتحدث عن كيفية تنفيذ كشف تسرب الذاكرة استنادًا إلى هذا المبدأ. الشرح أدناه سيكون بناءً على تنفيذ الخاص بي، وقد وضعته على GitHub الخاص بي: [LeakDetector](https://github.com/disenone/LeakDetector)。

####استبدال الدالة

أولاً، دعنا نلقي نظرة على الدالة الرئيسية الموجودة في [RealDetector.cpp](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)يرجى تقديم النص الذي ترغب في ترجمته إلى العربية.

```cpp linenums="1"
قم بتبديل وظيفة معينة في جدول عناوين الاستيراد (IAT) في importModule بوظيفة أخرى،
سيقوم importModule باستدعاء دالة في وحدة أخرى، وهذه الدالة هي الدالة التي تحتاج إلى التغيير،
ما علينا سوى تعديل import module لاستدعاء وظيفتنا المخصصة.
 *
* - importModule (IN): الوحدة التي تحتاج إلى المعالجة، وهذه الوحدة تستدعي وظائف من وحدات أخرى تحتاج إلى تصحيح.
 *
* - exportModuleName (IN): اسم الوحدة التي تأتي منها الدالة التي تحتاج إلى تصحيح
 *
- exportModulePath (IN): مسار حيث يتواجد وحدة التصدير، يتم محاولة تحميل وحدة التصدير باستخدام المسار أولاً،
إذا فشلت العملية، استخدم الاسم للتحميل
* - importName (IN): اسم الدالة
 *
* - replacement (IN): مؤشّر دالة بديلة
 *
قيمة العودة: نجاح صحيح، خلاف ذلك خطأ
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

دعونا نحلل هذه الوظيفة، كما هو مذكور في التعليق، وظيفة هذه الدالة هي تغيير عنوان وظيفة معينة داخل IAT إلى عنوان وظيفة أخرى. دعونا نراجع السطور 34-35 أولاً:

``` cpp
idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
	TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
```

تستطيع الدالة `ImageDirectoryEntryToDataEx` إرجاع عنوان لهيكل معين في رأس ملف الوحدة. يُحدد `IMAGE_DIRECTORY_ENTRY_IMPORT` الهيكل الذي يتعلق بجدول الاستيراد، لذا يشير `idte` المُرجع إلى جدول استيراد الوحدة.

السطور من 36 إلى 40 هي للتحقق من صحة `idte`. السطر 41، `idte->FirstThunk`، يشير إلى جدول استيراد الوظائف الفعلي. لذلك، السطور من 41 إلى 48 هي للبحث عن الوحدة التي تحتوي على الوظائف التي يجب استبدالها باستخدام اسم الوحدة، وإذا لم يتم العثور، فإن ذلك يعني عدم استدعاء وظائف تلك الوحدة، لذا يتوجب إظهار رسالة الخطأ والعودة.

بعد العثور على الوحدة، من الطبيعي أن نحتاج إلى تحديد الدالة البديلة. يتم فتح الوحدة التابعة للدالة بين السطور 55-62، وفي السطر 64 يتم العثور على عنوان الدالة. نظرًا لأن جدول عنوان الاستيراد (IAT) لا يحتفظ بالأسماء، يجب أولاً تحديد الدالة بناءً على عنوان الدالة الأصلية، ثم تعديل عنوان تلك الدالة. من السطور 68-80، يتم تنفيذ هذا الأمر. بعد العثور على الدالة بنجاح، يتم ببساطة تعديل العنوان ليصبح عنوان `replacement`.

حتى الآن، لقد نجحنا في استبدال الدالة في IAT.

####اسماء الوحدات والوظائف

虽然我们已经实现了替换 IAT 函数 `patchImport`，但这个函数需要指定模块名字和函数名字呀，那我们怎么知道程序的内存分配和释放用了什么模块和函数呢？为了搞清楚这个问题，我们需要借助 Windows 下的工具 [Dependency Walker] 

على الرغم من أننا قد نفذنا استبدال دالة IAT `patchImport`، إلا أن هذه الدالة تتطلب تحديد اسم الوحدة واسم الوظيفة. كيف نعرف إذن ما هي الوحدات والوظائف التي تم استخدامها لتخصيص وإطلاق الذاكرة في البرنامج؟ لتوضيح هذه المسألة، نحتاج إلى الاستعانة بأداة [Dependency Walker](http://www.dependencywalker.com/)في Visual Studio، قم بإنشاء مشروع جديد، واستخدم `new` في دالة `main` لطلب الذاكرة. قم بتجميع نسخة Debug، ثم استخدم `depends.exe` لفتح ملف exe الذي تم تجميعه، يمكنك رؤية واجهة مشابهة (بالاعتماد على مشروعي [LeakDetectorTest](https://github.com/disenone/LeakDetector/tree/master/LeakDetectorTest)例如）:

![](assets/img/2016-6-11-memory-leak-detector/depends.png)

يمكن أن نلاحظ أن LeakDetectorTest.exe يستخدم `malloc` و `_free_dbg` الموجودة في uscrtbased.dll (غير موضحة في الصورة)، وهذه الدالتان هما التي نحتاج إلى استبدالهما. يجب أن تكون حذرًا لأن أسماء الدوال الفعلية قد تختلف اعتمادًا على إصدار Windows وVisual Studio الذي تستخدمه. لدي إصدار Windows 10 وVisual Studio 2015، ما عليك سوى استخدام depends.exe لمعرفة الدالة التي يتم فعليًا استدعائها.

####تحليل مكدس الاستدعاءات

يجب تسجيل معلومات تخصيص الذاكرة من أجل تسجيل معلومات الوظيفة المستدعاة في ذلك الوقت. هنا، لا أنوي تقديم شرح مفصل حول كيفية الحصول على معلومات الوظيفة المستدعاة الحالية في Windows. الوظائف ذات الصلة هي `RtlCaptureStackBackTrace`، وهناك العديد من الموارد عبر الإنترنت تتعلق بذلك، ويمكنك أيضًا الاطلاع على الوظيفة الموجودة في كودي [`printTrace`](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp).

####كشف تسرب الذاكرة

حتى الآن، لقد جمعنا جميع كرات التنين، والآن سنستدعي زمردة الشينرو بشكل رسمي.

أريد أن أصنع شيئًا يمكنه الكشف عن تسرب الذاكرة بشكل جزئي (وهذا هو الفرق مع VLD، حيث يقوم VLD بالكشف الشامل ويدعم تعدد الخيوط). لذلك، قمت بإضافة طبقة أخرى حول الفئة `RealDetector` التي تحل محل الدوال، وهي `LeakDetector`، وكشفت واجهة `LeakDetector` للمستخدمين. عند الاستخدام، كل ما عليك هو إنشاء `LeakDetector`، مما سيؤدي إلى استبدال الدالة والبدء في كشف تسرب الذاكرة، وعند تدمير `LeakDetector`، ستعود الدالة الأصلية، وتتوقف عملية الكشف عن تسرب الذاكرة، وتتم طباعة نتائج كشف تسرب الذاكرة.

استخدم الكود أدناه للاختبار:

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

الكود مباشرة `new` بعض الذاكرة، ولم يتم تحريرها ثم خرج مباشرة، نتيجة البرنامج المطبوعة:

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

程序正确地找出有两个地方申请的内存没有释放，并且打印出了完整的调用栈信息，我们需要的功能至此已经完成了。

###ختامية

عندما لا تزال غير ملم بربط البرامج وتحميلها ومكتباتها، ربما تشعر بالارتباك حول كيفية العثور على وظائف مكتبة الارتباط المشتركة، ولا تتحدث عن استبدال وظائف مكتبة الارتباط بوظائفنا الخاصة. سنأخذ كحالة على فحص تسرب الذاكرة، ونناقش كيفية استبدال وظائف ملفات DLL في ويندوز، ويمكنكم الرجوع إلى مصدر VLD للحصول على تفاصيل تنفيذ أكثر.

ما أريد قوله هو أن "تحسين مهارات المبرمج: الربط، والتحميل، والمكتبة" هو كتاب جيد حقًا، إنها مجرد تعبير شخصي وليس إعلان ترويجي.

--8<-- "footer_ar.md"


> هذه المشاركة تم ترجمتها باستخدام ChatGPT، يرجى تقديم [**ردود فعل**](https://github.com/disenone/wiki_blog/issues/new)يرجى الإشارة إلى أي نقاط مفقودة. 
