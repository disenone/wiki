---
layout: post
title: Claude
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
description: Claude
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Claude" />

#الصفحة الزرقاء - كلود

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/claude_all.png)

##الرسائل النصية

أنشئ "Options" الفرع، وقم بتعيين المعلمات "Model"، "Api Key"، "Anthropic Version"

![](assets/img/2024-ue-aichatplus/usage/blueprint/claude_chat_1.png)

قم بربط العقدة "طلب كلود" بالعقدة ذات الصلة "الرسائل"، ثم انقر على تشغيل، لترى معلومات الدردشة التي تم إرجاعها بواسطة كلود على الشاشة. كما هو موضح في الصورة.

![](assets/img/2024-ue-aichatplus/usage/blueprint/claude_chat_2.png)

##توليد نص من الصور

كلاود يدعم أيضًا وظيفة Vision

في الخريطة الزرقاء، انقر بزر الماوس الأيمن لإنشاء عقد `Send Claude Chat Request`

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

أنشئ عقد Options وحدد `Stream=true، Api Key="مفتاح API الخاص بك من Clude"، Max Output Tokens=1024`

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

إنشاء رسائل، إنشاء Texture2D من الملف، وإنشاء AIChatPlusTexture من Texture2D، ثم إضافة AIChatPlusTexture إلى الرسالة.

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

قم بتنفيذ الحدث واطبع البيانات على شاشة اللعبة.

النموذج الكامل يبدو كما يلي، قم بتشغيل النموذج لرؤية رسالة إرجاع شاشة اللعبة طباعة النموذج الكبير.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)


--8<-- "footer_ar.md"


> تمت ترجمة هذه المشاركة باستخدام ChatGPT، يرجى تقديم [**تعليقات**](https://github.com/disenone/wiki_blog/issues/new)أشر على أي شيء تم تفويته. 
