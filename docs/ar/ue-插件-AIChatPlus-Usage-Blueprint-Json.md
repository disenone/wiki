---
layout: post
title: عمليات Json
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
- Editor
- Editor Plus
- Editor Plugin
- AI Chat
- Chatbot
- Image Generation
- OpenAI
- Azure
- Claude
- Gemini
- Ollama
- Json
- Blueprint
description: عمليات Json
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Json 操作" />

#المخطط الأزرق - عمليات Json

<!-- صورة مطلوبة: عرض عام لجميع عقد المخططات البرمجية المتعلقة بـ JSON، بما في ذلك العقد ضمن تصنيفات JsonObject وJsonArray وJsonLibrary -->
![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_all.png)

##ملخص

يوفر AIChatPlus دعمًا كاملاً لعمليات مخطط JSON، مما يسهل التعامل مع بيانات JSON ضمن المخططات. يشمل ذلك ثلاثة أصناف رئيسية:

* **UAIChatPlus_JsonObject**: فئة التعامل مع كائن JSON، تُستخدم لمعالجة JSON بتنسيق `{}`
* **UAIChatPlus_JsonArray**: فئة معالجة مصفوفات JSON، تُستخدم للتعامل مع JSON بتنسيق `[]`.
* **UAIChatPlus_JsonLibrary**: مكتبة أدوات JSON، توفر دوال أدوات ثابتة

تدعم هذه الفئات:
* إنشاء وتحليل وتسلسل JSON
* قراءة وتعيين قيم الحقول
* استعلامات المسارات المتداخلة
* التحويل المتبادل بين JSON و USTRUCT
* قراءة وكتابة الملفات
* استدعاء متسلسل (متسلسل السلسلة)

##العمليات الأساسية لـ JsonObject

###إنشاء JsonObject

استخدم `Create Json Object` لإنشاء كائن JSON فارغ:

<!-- تحتاج إلى صورة: لقطة شاشة تُظهر البحث بزر الماوس الأيمن في المخطط عن "إنشاء كائن Json" وإنشاء العقدة -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_create_1.png)

###التحليل من السلسلة النصية

استخدم `Parse Json Object` لإنشاء كائن من سلسلة JSON:

<!-- تحتاج إلى صورة: عرض عقدة Parse Json Object، إدخال سلسلة JSON مثل '{"name":"test","value":123}'، وإخراج JsonObject و bSuccess و ErrorMessage -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_parse_1.png)

###تعيين قيمة الحقل

يوفر JsonObject طرقًا متعددة لـ Set تدعم الاستدعاء المتسلسل:

| الوظيفة | الشرح |
|-----|------|
| `تعيين حقل النص` | تعيين حقل السلسلة النصية |
| `تعيين حقل رقمي` | تعيين حقل رقمي عائم |
| `Set Integer Field` | تعيين حقل عدد صحيح |
| `تعيين حقل منطقي` | ضبط حقل منطقي |
| `Set Object Field` | تعيين حقل الكائن المتداخل |
| `تعيين حقل المصفوفة` | 设置数组字段 |
| `Set Null Field` | تعيين حقل فارغ |

<!-- صورة مطلوبة: توضح سلسلة من التعليمات البرمجية المرئية لتعيين عدة حقول، مثل إنشاء كائن Json -> تعيين حقل نصي ("name", "player1") -> تعيين حقل رقمي ("level", 10) -> تعيين حقل منطقي ("active", true) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_set_1.png)

###احصل على قيمة الحقل

يقدم JsonObject عدة طرق للحصول على البيانات:

| الدالة | الشرح |
|------|------|
|-----|------|
| `الحصول على حقل السلسلة` | الحصول على حقل النص |
| `احصل على حقل الرقم` | احصل على حقل الرقم العائم |
| `Get Integer Field` | الحصول على حقل عدد صحيح |
| `Get Boolean Field` | الحصول على حقل منطقي |
| `احصل على حقل الكائن` | استرداد حقل الكائن المتداخل |
| `Get Array Field` | الحصول على حقل المصفوفة |

<!-- تحتاج إلى صورة: توضح مخططاً لاستخراج قيم الحقول من JsonObject، باستخدام Get String Field لاسترداد حقل "name"، مع عرض المعلمات DefaultValue و bSuccess -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_get_1.png)

###فحص الحقول

| الوظيفة | الشرح |
|---|---|
| COUNT | حساب عدد الخلايا التي تحتوي على أرقام أو تواريخ في نطاق محدد |
| COUNTA | حساب عدد الخلايا غير الفارغة في نطاق محدد، بغض النظر عن نوع البيانات |
| COUNTBLANK | حساب عدد الخلايا الفارغة في نطاق محدد |
| COUNTIF | حساب عدد الخلايا في نطاق محدد التي تفي بشرط معين |
| COUNTIFS | حساب عدد الخلايا في نطاق محدد التي تفي بمتعددة شروط |
| SUM | جمع جميع الأرقام في نطاق محدد |
| SUMIF | جمع القيم في نطاق محدد التي تفي بشرط معين |
| SUMIFS | جمع القيم في نطاق محدد التي تفي بمتعددة شروط |
| AVERAGE | حساب متوسط الأرقام في نطاق محدد |
| AVERAGEIF | حساب متوسط القيم في نطاق محدد التي تفي بشرط معين |
| AVERAGEIFS | حساب متوسط القيم في نطاق محدد التي تفي بمتعددة شروط |
| MAX | استعادة أكبر قيمة في نطاق محدد |
| MIN | استعادة أصغر قيمة في نطاق محدد |
|-----|------|
| `Has Field` | التحقق من وجود الحقل |
| `Get Field Type` | الحصول على نوع الحقل |
في الجدول التالي الترجمة إلى اللغة العربية للنص المقدم:

| `Get Field Names` | الحصول على أسماء جميع الحقول |
| `Remove Field` | حذف الحقل |
| `Clear` | مسح جميع الحقول |

<!-- صورة مطلوبة: إظهار استخدام Has Field للتحقق من وجود حقل، Get Field Type للحصول على مخطط أنواع الحقول -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_check_1.png)

###تحويل السلسلة إلى تسلسل

استخدم `To Json String` لتحويل JsonObject إلى سلسلة نصية:

<!— مطلوب صورة: عرض عقدة To Json String، مع إدخال JsonObject، معلمة bPrettyPrint، وإخراج سلسلة JSON منسقة -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_tostring_1.png)

##عمليات أساسية في JsonArray

###إنشاء JsonArray

استخدم `إنشاء مصفوفة JSON` لإنشاء مصفوفة JSON فارغة:

<!-- صورة مطلوبة: لقطة شاشة توضح إنشاء عقدة Create Json Array في المخطط الزمني -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_create_1.png)

###إضافة عنصر

يوفر JsonArray عدة طرق لإضافة العناصر (`Add`) تدعم الاستدعاء المتسلسل:

| الوظيفة | الشرح |
|-----|------|
| `Add String` | إضافة عنصر سلسلة نصية |
| `Add Number` | إضافة عنصر رقم عائم |
| `إضافة عدد صحيح` | إضافة عنصر عدد صحيح |
| `إضافة منطقية` | إضافة عنصر منطقي |
| `Add Object` | إضافة عنصر كائن |
| `Add Array` | إضافة عناصر المصفوفة |
| `إضافة Null` | إضافة عنصر null |

<!-- تحتاج إلى صورة: تعرض قالباً لإضافة عدة عناصر عن طريق الاستدعاء المتسلسل، مثل إنشاء مصفوفة Json -> إضافة سلسلة نصية ("أ") -> إضافة سلسلة نصية ("ب") -> إضافة عدد صحيح (123) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_add_1.png)

###الحصول على العنصر

يوفر JsonArray طرقًا للحصول على العناصر وفقًا للفهرس:

| الدالة | الوصف |
|------|------|
|-----|------|
| `Get String` | الحصول على عنصر السلسلة النصية |
| `الحصول على الرقم` | الحصول على عنصر الرقم العشري |
| `الحصول على عدد صحيح` | استرجاع عنصر عدد صحيح |
| `احصل على قيمة منطقية` | الحصول على العنصر المنطقي |
| `Get Object` | الحصول على عنصر الكائن |
| `الحصول على المصفوفة` | استرجاع عناصر المصفوفة |

<!-- صورة مطلوبة: توضح المخطط البصري لاستخدام 'Get Object' للحصول على عنصر الكائن في المصفوفة بواسطة الفهرس -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_get_1.png)

###معالجة المصفوفات

| الدالة | الوصف |
|-----|------|
| `الطول` | الحصول على طول المصفوفة |
| `هل الفهرس صالح` | التحقق مما إذا كان الفهرس صالحًا |
| `Get Element Type` | الحصول على نوع العنصر |
| `Remove At` | حذف العنصر عند الفهرس المحدد |
| `Clear` | مسح المصفوفة |

<!-- صورة مطلوبة: توضح استخدام Length للحصول على طول المصفوفة، بالتنسيق مع For Loop لاجتياز المصفوفة -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_loop_1.png)

###تحويل جماعي

JsonArray يدعم التحويل المجمع مع مصفوفات UE:

| الدالة | الشرح |
| ---- | ---- |
|-----|------|
 | `من مصفوفة السلاسل` | إنشاء من مصفوفة السلاسل |
| `To String Array` | تحويل إلى مصفوفة سلسلة نصية |
| `From Integer Array` | إنشاء من مصفوفة الأعداد الصحيحة |
| `To Integer Array` | تحويل إلى مصفوفة أعداد صحيحة |

<!-- صورة مطلوبة: توضح مثالاً لاستخدام From String Array و To String Array -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_batch_1.png)

##استعلام المسار

يدعم JsonObject الوصول إلى البيانات المتداخلة باستخدام مسار مفصول بنقاط، مثل `player.inventory.gold`.

###الحصول على القيمة حسب المسار

استخدم `Get String By Path` لاسترداد قيمة السلسلة النصية حسب المسار:

```json
{
    "player": {
        "name": "Hero",
        "inventory": {
            "gold": 1000
        }
    }
}
```

<!-- صورة مطلوبة: توضح استخدام عقدة Get String By Path مع تعيين Path إلى "player.name" للحصول على قيمة متداخلة في المخطط الزمني -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_get_1.png)

###تعيين القيمة حسب المسار

استخدم `Set String By Path` لتعيين القيمة عبر المسار:

<!-- الصورة المطلوبة: عرض مخطط باستخدام عقدة Set String By Path لتعيين قيم المسار المتداخل، مع إظهار معلمات FAIChatPlus_JsonPathOptions (bCaseSensitive و bCreateMissing) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_set_1.png)

###نتائج الاستعلام

استعلام المسار يُرجع هيكل `FAIChatPlus_JsonQueryResult` ويتضمن ما يلي:

* **bSuccess**: التحقق مما إذا كان الاستعلام ناجحًا
* **نوع القيمة**: نوع القيمة المُرجَعة
* **ErrorMessage**: رسالة الخطأ (في حالة الفشل)

<!-- صورة مطلوبة: عرض العقدة Break FAIChatPlus_JsonQueryResult، مع إظهار الحقول bSuccess و ValueType و ErrorMessage -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_result_1.png)

##تحويل JSON إلى USTRUCT

يدعم AIChatPlus التحويل بين JSON وUSTRUCT، مما يسهل استخدامه مع هياكل البيانات في المخططات الزرقاء.

###تحويل سلسلة JSON إلى USTRUCT

استخدم `Json String To Struct` لتحويل سلسلة JSON مباشرة إلى USTRUCT:

<!-- صورة مطلوبة: تُعرض عقدة Json String To Struct، يتم إدخال سلسلة JSON، ويتم ربط مُخرج المعلمات بمتغير USTRUCT مخصص (مثل FAIChatPlus_OpenAIChatRequestOptions) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_1.png)

###تحويل USTRUCT إلى سلسلة JSON

استخدم `Struct To Json String` لتحويل USTRUCT إلى سلسلة JSON:

<!-- صورة مطلوبة: عرض عقدة Struct To Json String، يتم إدخال متغير USTRUCT، معلمة bPrettyPrint، وإخراج سلسلة JSON -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_2.png)

###JsonObject إلى USTRUCT

استخدام طريقة `To Struct` الخاصة بـ JsonObject:

<!-- صورة مطلوبة: توضح استخدام عقدة To Struct الخاصة بـ JsonObject -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_3.png)

###USTRUCT إلى JsonObject

استخدام الطريقة الثابتة `From Struct` لإنشاء JsonObject من USTRUCT:

<!-- صورة مطلوبة: تُظهر عقدة From Struct، بإدخال USTRUCT وإخراج JsonObject -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_4.png)

##وظائف أداة JsonLibrary

يوفر `UAIChatPlus_JsonLibrary` مجموعة من دوائل الأدوات الثابتة.

###إنشاء سريع

| الدالة | الشرح |
|---|---|
|-----|------|
| `إنشاء كائن Json بحقل نصي` | إنشاء سريع لكائن Json مع حقل مفرد |
| `إنشاء كائن Json من خريطة نصية` | إنشاء JsonObject من خريطة |  

ملاحظة: حاولت الحفاظ على البنية الأصلية للجملة مع ترجمة المصطلحات الفنية بدقة. بالنسبة للجزء الثاني، "从 Map 创建 JsonObject" تُرجم حرفياً إلى "إنشاء JsonObject من خريطة"، حيث أن "Map" في البرمجة تُترجم عربياً إلى "خريطة" أو "ماب" حسب السياق، واخترت استخدام الترجمة العربية الشائعة في المجال التقني.

<!-- صورة مطلوبة: توضح استخدام "إنشاء كائن JSON من خريطة نصية"، حيث تدخل TMap<FString, FString> ويخرج JsonObject في مخطط الإجراءات -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_make_1.png)

###تحقق

| الدالة | الشرح |
|-----|------|
| `Validate Json String` | التحقق من صحة سلسلة JSON |
| `Is Json Object` | التحقق مما إذا كان كائن JSON |
| `Is Json Array` | التحقق مما إذا كان مصفوفة JSON |

<!-- صورة مطلوبة: توضح استخدام مخطط التحقق من صحة سلسلة JSON للتحقق من صحة سلسلة JSON -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_validate_1.png)

###تنسيق

| الدالة | الوصف |
|-----|------|
| `Prettify Json` | تنسيق JSON (إضافة مسافة بادئة وأسطر جديدة) |
| `تصغير Json` | ضغط JSON (إزالة المسافات البيضاء) |

<!-- صورة مطلوبة: توضح استخدام Prettify Json لتهيئة سلسلة JSON، مع عرض إدخال JSON المضغوط وإخراج JSON المهيأ -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_format_1.png)

###عمليات الملفات

| الدالة | الشرح |
| --- | --- |
|-----|------|
| `تحميل كائن Json من ملف` | تحميل JsonObject من ملف |
| `حفظ كائن Json في ملف` | حفظ JsonObject في ملف |
| `Load Json Array From File` | تحميل صفيف Json من ملف |
| `حفظ مصفوفة Json في ملف` | حفظ JsonArray إلى ملف |

<!-- تحتاج إلى صورة: توضح مثال استخدام Save Json Object To File و Load Json Object From File -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_file_1.png)

###مقارنة

| الدالة | الوصف |
|-----|------|
| `يساوي كائن Json` | مقارنة ما إذا كان كائنا Json متساويين |
| `يساوي مصفوفة جيسون` | مقارنة ما إذا كان مصفوفتا جيسون متساويتين |

<!-- صورة مطلوبة: تعرض مخططًا لاستخدام Equals Json Object لمقارنة كائنين JsonObject -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_compare_1.png)

###استعلام المسار المتقدم

| الوظيفة | الشرح |
| -------- | -------- |
|-----|------|
النص المترجم إلى العربية:

| `سلسلة الاستعلام عن طريق المسار` | البحث عن سلسلة نصية حسب المسار (يدعم فهرسة المصفوفات، مثل `items[0].name`) |
| `Query Object By Path` | البحث عن كائن حسب المسار |
| `Query Array By Path` | استعلام عن المصفوفة حسب المسار |

<!-- تحتاج إلى صورة: توضح استخدام Query String By Path لاستعلام المسار بمؤشر المصفوفة، مثل "data.items[0].name" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_query_1.png)

###العمليات المجمعة

| الدالة | الشرح |
|-----|------|
| `تعيين حقول السلسلة من الخريطة` | تحديد حقول النص بشكل جماعي |
| `الحصول على حقول النص لتعيينها` | الحصول على حقول النص دفعة واحدة |

<!-- صورة مطلوبة: توضح استخدام مخطط Set String Fields From Map لتعيين الحقول بشكل جماعي -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_batch_1.png)

##إجراءات أخرى

###دمج JsonObject

استخدام طريقة `Merge` لدمج كائنين JsonObject:

<!-- صورة مطلوبة: عرض عقدة Merge، دمج كائني JsonObject، مع عرض المعلمة bOverwrite -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_merge_1.png)

###نسخ JsonObject

استخدم طريقة `Duplicate` لعمل نسخة عميقة من JsonObject:

<!-- تحتاج إلى صورة: عرض مخطط Duplicate لعقدة نسخ JsonObject -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_dup_1.png)

##أمثلة عملية للتطبيق

###تحليل استجابة API

استخراج معلمات Tool Call من استجابة محادثة الذكاء الاصطناعي:

<!-- تحتاج إلى صورة: عرض مخطط مثال تحليل كامل: من سلسلة FunctionArguments تحويلها إلى JsonObject، ثم استخدام Get String Field لاستخراج قيمة المعلمة -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_1.png)

###بناء معلمات الطلب

استخدام كائن JsonObject لبناء معاملات الطلب المعقدة:

<!-- صورة مطلوبة: تُظهر مخططًا لبناء بنية JSON متداخلة، تُنشئ JsonObject مع تعيين عدة حقول، تتضمن JsonObject متداخل و JsonArray -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_2.png)

###قراءة وكتابة ملف التكوين

قم بتحميل الإعدادات من ملف JSON، وقم بتعديلها ثم احفظها:

<!-- تحتاج إلى صورة: توضح سيرورة تكوين القراءة والكتابة الكاملة: تحميل كائن Json من الملف -> تعديل الحقل -> حفظ كائن Json إلى الملف -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_3.png)

##تعداد الأنواع

يُعرّف التعداد `EAIChatPlus_JsonValueType` نوع قيمة JSON:

| القيم المحددة | الشرح |
|-------|------|
| `None` | نوع غير معروف |
| `Null` | قيمة فارغة (null) |
| `String` | سلسلة نصية |
| `الرقم` | الرقم |
| `Boolean` | القيمة المنطقية |
| `Array` | مصفوفة |
| `Object` | كائن |

<!-- تحتاج إلى صورة: عرض مخطط يستخدم عقدة Switch للتعامل المختلف بناءً على JsonValueType -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_type_1.png)

--8<-- "footer_ar.md"


> هذا المنشور مترجم باستخدام ChatGPT، يرجى تقديم [**ملاحظاتكم**](https://github.com/disenone/wiki_blog/issues/new)أشر إلى أي إغفالات في النص. 
