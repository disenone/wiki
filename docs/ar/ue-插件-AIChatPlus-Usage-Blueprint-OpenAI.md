---
layout: post
title: OpenAI
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
description: OpenAI
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - OpenAI" />

#الجزء الخاص بالتصميم - OpenAI

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_all.png)

في [ابدأ](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)لقد قامت الفقرة السابقة بتقديم استخدام OpenAI الأساسي، سنقدم هنا استخدامًا مفصلًا آخر.

##الدردشة النصية

استخدام OpenAI للدردشة النصية

أنشئُ نود `Send OpenAI Chat Request In World` بالضغط الأيمن في النَّموذج.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

أنشئَ قَسم "Options" وحدد الإعدادات `Stream=true, Api Key="you api key from OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

إنشاء رسائل، وإضافة رسالة نظام ورسالة مستخدم على التوالي

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

أنشئ Delegate لاستقبال مخرجات النموذج وطباعتها على الشاشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

النسخة الكاملة من الخطة تبدو كما هو مبين، قم بتشغيل الخطة لترى رسالة عودة تظهر على شاشة اللعب تطبع نموذجًا كبيرًا.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

##إنشاء صورة من النص

استخدام OpenAI لإنشاء الصور

أنشئُوا نقطةً بالضغط بزر اليمين في الخطة باسم "Send OpenAI Image Request"، وحددوا النص "a beautiful butterfly" كمدخل.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

أنشئ قُسم Options واضبط "Api Key=your api key from OpenAI"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

ربط حدث On Images وحفظ الصور في القرص المحلي

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

تبدو الخطة الزرقاء كاملة بهذا الشكل، قم بتشغيل الخطة الزرقاء لرؤية الصورة المحفوظة في الموقع المحدد.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

##إنشاء نص من الصور

استخدام OpenAI Vision لتحليل الصور

أنشئ نقطة "Send OpenAI Image Request" بالنقر بزر الفأرة الأيمن في الخريطة.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_1.png)

أنشئُوا عقدة Options وحددوا `Api Key="your api key from OpenAI"`، وقُوموا بتعيين النموذج على `gpt-4o-mini`

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_2.png)

إنشاء رسائل.
أنشئ أولاً عقد "Import File as Texture 2D" لقراءة صورة من نظام الملفات؛
قم بتحويل الصورة إلى كائن قابل للاستخدام كإضافة عبر العقدة "Create AIChatPlus Texture From Texture2D".
قم بتوصيل الصورة بحقل "Images" في العقدة "AIChatPlus_ChatRequestMessage" باستخدام عقدة "Make Array".
قم بتعيين محتوى حقل "المحتوى" إلى "وصف هذه الصورة".

كما هو موضح في الصورة:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_3.png)

العملية الكاملة تبدو على هذا النحو، بمجرد تشغيل العملية، يمكنك رؤية النتائج على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_4.png)

##تعديل الصورة

OpenAI تدعم تعديل مناطق تسمية الصور.

أولاً، قم بتحضير صورتين

صورة بحاجة للتعديل: src.png

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_1.png)

صورة mask.png هي صورة تم تحديد المناطق التي يجب تعديلها فيها. يمكنك تعديل الصورة الأصلية عن طريق ضبط شفافية منطقة التعديل إلى القيمة 0، أي تغيير قيمة قناة الألفا إلى 0.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_2.png)

قم بقراءة الصورتين أعلاه بشكل منفصل وضعهما في مصفوفة

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_3.png)

إنشاء عقد "OpenAI Image Options" ، وتعيين ChatType = Edit ، وتعديل "End Point Url" = v1/images/edits

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_4.png)

أنشئ "OpenAI Image Request"، ثبت "Prompt" على "تحويل إلى فراشتين"، اربط العقد "Options" مع مجموعة الصور واحفظ الصورة المُنتجة في نظام الملفات.

الرسم التخطيطي الكامل يبدو هكذا:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_5.png)

تشغيل المخطط، وحفظ الصور المولدة في الموقع المحدد

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_6.png)

##الصورة المتحورة

OpenAI يدعم إنشاء تحويرات مماثلة للصور المُدخلة.

أولاً، قم بتحضير صورة بصيغة src.png وقم بتحميلها في المخطط الأزرق.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_1.png)

أنشئ "OpenAI Image Options" العقدة، واضبط ChatType = Variation، وغير "End Point Url" = v1/images/variations.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_2.png)

أنشئ "OpenAI Image Request"، احتفظ بـ "Prompt" كفارغ، اربط نقطة "Options" بالصورة واحفظ الصورة المُنشأة في نظام الملفات.

الطبعة الأصلية للتصميم تبدو على النحو التالي:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_3.png)

قم بتشغيل النموذج الأساسي، واحفظ الصورة المُولّدة في الموقع المحدد.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_4.png)

--8<-- "footer_ar.md"


> هذا المنشور تمت ترجمته باستخدام ChatGPT، يرجى تقديم [**ردود فعل**](https://github.com/disenone/wiki_blog/issues/new)يرجى تحديد أي نقص. 
