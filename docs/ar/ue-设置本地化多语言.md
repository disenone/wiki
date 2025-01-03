---
layout: post
title: ضبط الـUE للغات المتعددة المحلية
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: سجل كيفية تحقيق التعدد اللغوي المحلي في الـ UE
---

<meta property="og:title" content="UE 设置本地化多语言" />

#قم بتعيين اللغات المحلية للواجهة في UE

> سجل كيفية تحقيق تعدد اللغات المحلية في UE.

إذا كنت غير مألوف بقائمة إضافات UE، فأنصح بالنظر فيها بشكل مبسّط أولاً: [قائمة محرر إضافات UE](ue-扩展编辑器菜单.md)，[ue- Expand menu using path form](ue-使用路径形式扩展菜单.md)

ترجمة النص إلى اللغة العربية:
هذا النص معتمد على الإضافة: [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##شرح الوظائف

يمكن لـ UE أن يتمتع بأدواته الخاصة التي تسمح بتنفيذ اللغات المتعددة، على سبيل المثال، يمكننا تحقيق التعريب لقوائم المحرر:

القائمة باللغة الصينية:

![](assets/img/2023-ue-localization/chinese.png)

القائمة بالإنجليزية:

![](assets/img/2023-ue-localization/english.png)

##بيان الشيفرة

لتحقيق تطبيق قوائم الطعام محليًا، نحن بحاجة إلى تحديد السلاسل التي تحتاج إلى معالجة UE بوضوح في الشيفرة، عبر استخدام الماكروهات المعرفة مسبقًا في UE `LOCTEXT` و `NSLOCTEXT` .

- يتم تعريف النطاق الكامل للملفات أولاً عن طريق تعريف ماكرو يُسمى `LOCTEXT_NAMESPACE` ، حيث يكون المحتوى هو اسم مساحة الأسماء التي يوجد بها النصوص متعددة اللغات الحالية، بعد ذلك يُمكن استخدام `LOCTEXT` لتعريف النصوص في الملف، وأخيرًا يتم إلغاء ماكرو `LOCTEXT_NAMESPACE` في نهاية الملف:


```cpp
// #define LOCTEXT(InKey, InTextLiteral)

#define LOCTEXT_NAMESPACE "EditorPlusTools"
LOCTEXT("Key", "Content");
#undef LOCTEXT_NAMESPACE

```

استخدام طريقة تعريف محلية، باستخدام `NSLOCTEXT` ، عند تعريف النص يرافقه معلمة الفضاء الاسم:

```cpp
// #define NSLOCTEXT(InNamespace, InKey, InTextLiteral)

NSLOCTEXT("EditorPlusTools", "Key", "Content");
```

يقوم أداة UE بجمع جميع النصوص التي تحتاج إلى ترجمة عن طريق البحث عن ظهور ماكرو `LOCTEXT` و `NSLOCTEXT`.

##استخدم الأداة لترجمة النص

لنفترض أن لدينا الشفرة التالية لتعريف النص:

```cpp
#define LOCTEXT_NAMESPACE "EditorPlusTools"
// register path node loctext
FEditorPlusPath::GetNodeByPath("/MenuTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/<Hook>Help/<MenuBar>MenuTest/<SubMenu>SubMenu1/<Section>Section1")->SetFriendlyName(LOCTEXT("Section1", "Section1"))->SetFriendlyTips(LOCTEXT("Section1Tips", "Section1Tips"));
#undef LOCTEXT_NAMESPACE
```

ابدأ بتشغيل أداة الترجمة، افتح إعدادات المحرر `تحرير - تفضيلات المحرر`، وحدد `عام - وظائف تجريبية - Tools - عنصر اختيار الترجمة`：

![](assets/img/2023-ue-localization/editor_enable_tool.png)


ثم قم بفتح أداة الترجمة `الأدوات - لوحة التحكم في التعريب`:

![](assets/img/2023-ue-localization/editor_open_tool.png)

قم بإنشاء هدف جديد (يمكنك وضعه تحت "اللعبة" الافتراضية، الهدف الجديد لسهولة إدارة ونقل هذه النصوص المترجمة).

![](assets/img/2023-ue-localization/tool_new_target.png)

قم بتعيين معلمات الهدف، حيث سيتم تغيير اسمي هنا إلى `EditorPlusTools`، وسيكون نوع التحميل `محرر`، وسيتم الحصول على البيانات من النص وإضافتها إلى دليل الإضافات، والاعتمادات المستهدفة هي `Engine, Editor`، أما بقية الإعدادات فستبقى كما هي.

![](assets/img/2023-ue-localization/tool_target_config.png)

يرجى إضافة اللغات لضمان توفر الصينية (المبسطة) والإنجليزية كخيارين، وتأكيد عرض `zh-Hans` و `en` عند تمرير الماوس فوق اسم اللغة بالواحدة، كما يُرجى تحديد اللغة الإنجليزية (لأن النصوص معرّفة بالإنجليزية في رمزنا، ونحتاج هنا لجمع هذه النصوص باللغة الإنجليزية):

![](assets/img/2023-ue-localization/tool_target_lang.png)

الرجاء جمع النصوص التالية:

![](assets/img/2023-ue-localization/tool_target_collect.png)

سيظهر صندوق تقدم جمع البيانات ، انتظر حتى يتم جمعها بنجاح، وسيظهر علامة صح باللون الأخضر:

![](assets/img/2023-ue-localization/tool_target_collected.png)

أغلق مربع تقدم الجمع، ثم ارجع إلى أداة الترجمة، حيث يمكنك رؤية الكمية المجمعة عند عرض سطر النص الإنجليزي. لا داعي لترجمة النصوص الإنجليزية بحد ذاتها، انقر زر الترجمة لسطر النص الصيني.

![](assets/img/2023-ue-localization/tool_go_trans.png)

افتح النص، وسوف تجد القسم الذي لم يُترجم يحتوي على محتوى. أدخل النص المُترجم في الجانب الأيمن من النص الإنجليزي. بمجرد اكتمال الترجمة، احفظ التغييرات وأغلق النافذة.

![](assets/img/2023-ue-localization/tool_trans.png)

الرجاء تقديم النص الذي ترغب في ترجمته.

![](assets/img/2023-ue-localization/tool_count.png)

ترجمة هذا النص إلى اللغة العربية:

أخيراً، النص المُترجم:

![](assets/img/2023-ue-localization/tool_build.png)

سيتم وضع بيانات الترجمة في المجلد `Content\Localization\EditorPlusTools`، حيث ستكون هناك مجلد لكل لغة، يمكن رؤية ملفين في مجلد `zh-Hans`، وهما `‏.archive‏` لتجميع النصوص وترجمتها و `‏.locres‏` بعد ترجمتها.

![](assets/img/2023-ue-localization/tool_ret.png)

![](assets/img/2023-ue-localization/tool_ret2.png)

##وضع النص المترجم في دليل الإضافة

قمنا بوضع النصوص المترجمة التي تم إنشاؤها بواسطة الإضافة في الدليل الخاص بالمشروع. نحتاج إلى نقل هذه النصوص إلى داخل الإضافة لتسهيل نشرها مع الإضافة.

انقل دليل `Content\Localization\EditorPlusTools` إلى دليل الإضافات تحت مجلد المكونات الإضافية `Plugins\UE.EditorPlus\Content\Localization\EditorPlusTools` عندي.

قم بتعديل ملف تكوين المشروع `DefaultEditor.ini`، وأضف المسار الجديد:

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```

بهذه الطريقة، بمجرد أن تحصل مشاريع أخرى على الوصلة، يمكنها استخدام النص المترجم مباشرة بدون الحاجة لإعادة تكوين الترجمة بتعديل ملف `DefaultEditor.ini`.

##ملاحظات

أثناء عملية إنشاء بيانات الترجمة، واجهت بعض المشاكل، وفيما يلي تلخيص للأمور التي ينبغي الانتباه لها:

- يجب تعريف النصوص داخل الكود باستخدام المحددات `LOCTEXT` و `NSLOCTEXT`، ويجب أن تكون النصوص ثوابت سلاسل لكي يقوم نظام التشغيل بجمعها.
لا يمكن أن يحتوي اسم الهدف المترجم على الرموز ".". يجب ألا تحتوي أسماء الدلائل في "Content\Localization\" على "."، لأن محرك Unreal Engine سيقوم بقص الجزء الذي يسبق النقطة ".". وهذا قد يؤدي إلى فشل قراءة Unreal Engine للنص المترجم بسبب خطأ في الاسم.
بالنسبة لملحقات المحرر، من الضروري التحقق من ما إذا كانت في وضع سطر الأوامر `IsRunningCommandlet()` ثم عدم إنشاء قائمة وواجهة المستخدم SlateUI، لأنه لا يوجد وحدة Slate في وضع سطر الأوامر، مما يمكن أن يؤدي إلى حدوث خطأ عند جمع النصوص `Assertion failed: CurrentApplication.IsValid()` . إذا واجهت أيضًا خطأ مماثلًا، جرب إضافة هذا التحقق. المعلومات الخطأ بشكل محدد:

    > Assertion failed: CurrentApplication.IsValid() [File:E:\UE\ue5.3_git\Engine\Source\Runtime\Slate\Public\Framework\Application\SlateApplication.h] [Line: 255] 

    ![](assets/img/2023-ue-localization/tool_error.png)

--8<-- "footer_ar.md"


> هذه المشاركة تمت ترجمتها باستخدام ChatGPT، يرجى تقديم [**ملاحظات**](https://github.com/disenone/wiki_blog/issues/new)يرجى تحديد أي نقص. 
