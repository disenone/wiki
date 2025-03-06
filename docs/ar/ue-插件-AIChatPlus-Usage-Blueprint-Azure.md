---
layout: post
title: Azure
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
description: Azure
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Azure" />

#القسم الذي يدور حول Azure من بستة الأزرق

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_all.png)

استخدام Azure مشابه جدًا لـ OpenAI، لذلك سنقدم هنا مقدمة موجزة

##الرسائل النصية

إنشاء "Azure Chat Options" العقدة، وتعيين المعلمات "Deployment Name"، "Base Url"، "Api Key"

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_chat_1.png)

أنشئ "Messages" node ، ثم قم بربطه بـ "Azure Chat Request" ، انقر فوق تشغيل، وسترى معلومات المحادثة التي تم إرجاعها بواسطة Azure على الشاشة. كما هو موضح في الصورة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

##إنشاء صورة

إنشاء العقدة "خيارات صور Azure"، وتعيين المعلمات "Deployment Name"، "Base Url"، "Api Key"

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_image_1.png)

قم بإعداد عقد "Azure Image Request" وغيرها من العقد، ثم انقر فوق تشغيل. سترى على الشاشة طباعة معلومات الدردشة المُرسلة من Azure. كما في الصورة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

وفقًا لإعدادات الرسم البياني أعلاه، سيتم حفظ الصورة في المسار D:\Dwnloads\butterfly.png

--8<-- "footer_ar.md"


> هذه المشاركة تمت ترجمتها باستخدام ChatGPT، يرجى تقديم [**ردود**](https://github.com/disenone/wiki_blog/issues/new)تحدث عن أي شيء تأخير. 
