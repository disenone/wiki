---
layout: post
title: '## UE 设置本地化多语言


  تعيين اللغة المحلية متعددة UE'
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: سجل كيفية تحقيق اللغات المتعددة المحلية في UE
---

<meta property="og:title" content="UE 设置本地化多语言" />

#إعدادات UE للغات متعددة المحلية

> سجل كيفية تحقيق التعدد اللغوي والتدويل في UE

إذا كنت غير معتاد على قائمة توسيع UE، يُنصح بتفقدها بإيجاز أولاً: [قائمة محرر التوسع UE](ue-扩展编辑器菜单.md)，[التوسيع القائمة باستخدام شكل المسار](ue-使用路径形式扩展菜单.md)

هذا النص يعتمد على المكون الإضافي: [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##تقديم الوظائف

يمكن لـ UE أن يحقق تعدد اللغات المحلية من خلال أدواته المدمجة، على سبيل المثال، يمكننا تحقيق التعريب لقائمة المحرر:

القائمة باللغة الصينية:

![](assets/img/2023-ue-localization/chinese.png)

القائمة باللغة الصينية:

![](assets/img/2023-ue-localization/english.png)

##شهادة الشفرة

من أجل تحقيق توطين القائمة، نحتاج إلى التصريح بوضوح في الكود عن السلاسل النصية التي تحتاج UE إلى معالجتها، باستخدام الماكرو المعرف من قبل UE `LOCTEXT` و `NSLOCTEXT`:

طريقة تعريف ملف النطاق الكامل، تبدأ أولاً بتعريف ماكرو يسمى `LOCTEXT_NAMESPACE`، ويحتوي على اسم مساحة الاسم الحالية للنصوص متعددة اللغات، ومن ثم يمكن استخدام `LOCTEXT` لتحديد النصوص في الملف، وفي النهاية يتم إلغاء ماكرو `LOCTEXT_NAMESPACE` في نهاية الملف.

```cpp
// #define LOCTEXT(InKey, InTextLiteral)

#define LOCTEXT_NAMESPACE "EditorPlusTools"
LOCTEXT("Key", "Content");
#undef LOCTEXT_NAMESPACE

```

يرجى استخدام `NSLOCTEXT` لتحديد النص بشكل محلي، وتضمين معلمة الفضاء الاسمي عند تعريف النص.

```cpp
// #define NSLOCTEXT(InNamespace, InKey, InTextLiteral)

NSLOCTEXT("EditorPlusTools", "Key", "Content");
```

تجمع أدوات UE كل النصوص التي تحتاج إلى ترجمة من خلال البحث عن ظهور الماكرو `LOCTEXT` و `NSLOCTEXT`.

##استخدام الأدوات لترجمة النصوص

لنفترض أن لدينا الكود التالي لتعريف نصّ:

```cpp
#define LOCTEXT_NAMESPACE "EditorPlusTools"
// register path node loctext
FEditorPlusPath::GetNodeByPath("/MenuTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/<Hook>Help/<MenuBar>MenuTest/<SubMenu>SubMenu1/<Section>Section1")->SetFriendlyName(LOCTEXT("Section1", "Section1"))->SetFriendlyTips(LOCTEXT("Section1Tips", "Section1Tips"));
#undef LOCTEXT_NAMESPACE
```

أولا، قم بفتح أداة الترجمة، ثم افتح إعدادات المحرر `تحرير - تفضيلات المحرر`، وحدد الخيار `عام - الميزات التجريبية - الأدوات - محدد الترجمة`:

![](assets/img/2023-ue-localization/editor_enable_tool.png)


ثم افتح أداة الترجمة `أدوات - لوحة التحكم المحلية`:

![](assets/img/2023-ue-localization/editor_open_tool.png)

أنشئ هدفًا جديدًا (يُمكن أيضًا إنشاؤه تحت "اللعبة" الافتراضية، وإنشاء هدفٍ جديد يُسهل إدارة ونقل هذه النصوص المترجمة).

![](assets/img/2023-ue-localization/tool_new_target.png)

قم بتعديل معلمات الهدف، حيث سيتم تغيير اسمي إلى `EditorPlusTools`، وسيكون نوع التحميل `المحرر`، وذلك بجمع النصوص وإضافة دليل الإضافات، والاعتمادات المستهدفة تشمل `المحرك، المحرر`، والاحتفاظ ببقية الإعدادات كما هي:

![](assets/img/2023-ue-localization/tool_target_config.png)

إضافة اللغة، والتأكد من وجود الصينية (المبسطة) والإنجليزية كلغتين، والتأكد من أن عند تمرير مؤشر الفأرة فوق اسم اللغة ستظهر `zh-Hans` و `en` على التوالي، ثم تحديد الإنجليزية (نظرًا لأننا نستخدم النصوص المحددة باللغة الإنجليزية في الشيفرة، نحتاج هنا لجمع هذه النصوص الإنجليزية).

![](assets/img/2023-ue-localization/tool_target_lang.png)

انقر لجمع النص:

![](assets/img/2023-ue-localization/tool_target_collect.png)

سيظهر مربع تقدم التجميع، انتظر حتى يكتمل التجميع بنجاح، وسيظهر علامة صح باللون الأخضر:

![](assets/img/2023-ue-localization/tool_target_collected.png)

اغلق صندوق جمع التقدم، وعد إلى أداة الترجمة حيث يمكنك رؤية عدد العناصر التي تم جمعها في السطر الإنجليزي. لا نحتاج لترجمة النص الإنجليزي نفسه، اضغط على زر الترجمة في السطر الصيني:

![](assets/img/2023-ue-localization/tool_go_trans.png)

افتحوا الصفحة وستجدون محتوى في الجدول الذي لم يتم ترجمته بعد، اكتبوا الترجمة في الجدول الأيمن للنص الإنجليزي. عند الانتهاء من ترجمة جميع المحتويات، احفظوا التغييرات واغلقوا النافذة:

![](assets/img/2023-ue-localization/tool_trans.png)

الرجاء تقديم الترجمة الخاصة بك فيما يلي:
الرجاء تحديد الإحصائيات اللغوية بمجرد الانتهاء لعرض عدد الترجمة باللغة الصينية:

![](assets/img/2023-ue-localization/tool_count.png)

最后编译文本：  
النص النهائي المترجم:

![](assets/img/2023-ue-localization/tool_build.png)

سوف توضع البيانات المترجمة في `Content\Localization\EditorPlusTools`، حيث يوجد مجلد لكل لغة. داخل مجلد zh-Hans، يمكنك رؤية ملفين؛ `.archive` هو النصوص التي تم جمعها وترجمتها، بينما `.locres` هو البيانات بعد التجميع:

![](assets/img/2023-ue-localization/tool_ret.png)

![](assets/img/2023-ue-localization/tool_ret2.png)

##قم بوضع النص المترجم في دليل الإضافات

لقد وضعنا النصوص المترجمة التي تم إنشاؤها بواسطة الوحدة الإضافية أعلى المجلد الخاص بالمشروع. نحتاج إلى نقل هذه النصوص إلى داخل الوحدة الإضافية لتسهيل نشرها مع الوحدة الإضافية.

قم بنقل دليل `Content\Localization\EditorPlusTools` إلى دليل المكون الإضافي "Content"، وهنا سيكون `Plugins\UE.EditorPlus\Content\Localization\EditorPlusTools`.

تعديل ملف تكوين المشروع `DefaultEditor.ini`، وأضف المسار الجديد:

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```

بهذه الطريقة، بعد أن يحصل مشروع آخر على الإضافة، يمكنه تعديل ملف DefaultEditor.ini واستخدام النص المترجم مباشرة، دون الحاجة إلى إعادة تكوين الترجمة.

##ملاحظات

في عملية生成 بيانات الترجمة، واجهنا بعض المشاكل، وفيما يلي بعض النقاط التي يجب الانتباه إليها:

- يجب تعريف النص في الشيفرة باستخدام الماكرو `LOCTEXT` و `NSLOCTEXT`، ويجب أن يكون النص ثابتًا كسلسلة، حتى يتمكن UE من جمعه.
يجب أن لا يحتوي اسم الهدف على الرموز `.`، ولا يجب أن تحتوي أسماء الدلائل تحت `Content\Localiztion\` على `.`. سيقوم محرك الألعاب UE بقطع الجزء الذي قبل `.` فقط. قد يؤدي وجود أخطاء في الأسماء إلى فشل قراءة نص الترجمة من قبل محرك الألعاب UE.
- بالنسبة لملحقات المحرر، يجب التحقق مما إذا كان في وضع سطر الأوامر `IsRunningCommandlet()`، فلا يتم إنشاء القائمة وSlateUI، لأنه في وضع سطر الأوامر لا يوجد وحدة Slate، مما قد يؤدي إلى حدوث خطأ أثناء جمع النص `Assertion failed: CurrentApplication.IsValid()` . إذا واجهت خطأ مماثلاً، يمكنك محاولة إضافة هذا التحقق. معلومات الخطأ المحددة:

    > Assertion failed: CurrentApplication.IsValid() [File:E:\UE\ue5.3_git\Engine\Source\Runtime\Slate\Public\Framework\Application\SlateApplication.h] [Line: 255] 

    ![](assets/img/2023-ue-localization/tool_error.png)

--8<-- "footer_ar.md"


> هذا المنشور تم ترجمته باستخدام ChatGPT، يرجى تقديم [**ملاحظات**](https://github.com/disenone/wiki_blog/issues/new)يرجى تحديد أي نقص. 
