---
layout: post
title: Get Started
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
description: Get Started
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Get Started" />

#البداية - الجزء الأول: الخطة العامة

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

## Get Started

سأقدم لكم اليوم مثالًا باستخدام OpenAI لشرح كيفية استخدام الخطة الأساسية.

###الرسائل النصية

استخدام OpenAI للدردشة النصية

قم بإنشاء نقطة "Send OpenAI Chat Request In World" بالنقر بزر اليمين في الرسم التخطيطي.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

أنشئُوا نقطة Options وحددوا `Stream=true, Api Key="your api key from OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

إنشاء رسائل، وإضافة رسالة نظام ورسالة مستخدم على التوالي.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

إنشاء الوكيل Delegate لاستقبال مخرجات النموذج وطباعتها على الشاشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

النسخة الكاملة من الخطة تبدو كما يلي: قم بتشغيل الخطة، وسترى رسالة تعود من الشاشة تقوم بطباعة نموذج كبير.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###هل يمكنك تقديم ترجمة لهذا النص؟

استخدام OpenAI لإنشاء الصور

أنشئ نقطة بيانات `Send OpenAI Image Request` في الرسم البياني بالنقر بزر الفأرة الأيمن، ثم قم بتعيين `In Prompt="a beautiful butterfly"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

أنشئُوا العقدَ Options واضبطُوا `Api Key="your api key from OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

ربط الحدث على الصور وحفظ الصورة على القرص المحلي

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

الخطة الكاملة تبدو كما هو موضح، قم بتشغيل الخطة لترى الصورة محفوظة في الموقع المحدد.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

###إنشاء نص من الصور

استخدم OpenAI Vision لتحليل الصور.

في النّموذج الأساسي، انقر بزر الماوس الأيمن لإنشاء عقد "Send OpenAI Image Request"

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_1.png)

إنشاء ٍقًٍode> ٍوتعيين `Api Key="your api key from OpenAI"`وتعيين  الموديل كٍgpt-4o-mini.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_2.png)

إنشاء رسائل.
إنشاء العنصر "استيراد ملف كنسيجة ثنائية الأبعاد" أولاً لقراءة صورة من نظام الملفات؛
استخدم نقطة "Create AIChatPlus Texture From Texture2D" لتحويل الصورة إلى كائن يمكن استخدامه بواسطة المكون الإضافي؛
من خلال "Make Array" الوصلة، اربط الصور بحقل "Images" في الوحدة "AIChatPlus_ChatRequestMessage"؛
قم بتعيين محتوى الحقل "Content" كـ "وصف هذه الصورة".

كما هو مبين في الصورة:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_3.png)

المخطط الكامل يبدو كما هو موضح، بمجرد تشغيل المخطط، يمكنك رؤية النتائج التي تظهر على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_4.png)

--8<-- "footer_ar.md"


> هذه المشاركة تمت ترجمتها باستخدام ChatGPT، يُرجى تقديم [**تعليقات**](https://github.com/disenone/wiki_blog/issues/new)يرجى تحديد أي نقص. 
