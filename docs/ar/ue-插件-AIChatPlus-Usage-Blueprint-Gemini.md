---
layout: post
title: Gemini
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
description: Gemini
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Gemini" />

#النسخة الزرقاء - جيميني

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_all.png)

###دردشة نصية

إنشاء 节点 "خيارات Gemini Chat"، ثم ضبط المعلمات "Model" و "Api Key"

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_chat_1.png)

أنشئُ العقد الذي يحمل اسم "Gemini Chat Request"، وقُم بربطه بالعقدَي "Options" و "Messages"، ثُمّ دَوّن على زِرّ التّشغِيل، وستتمكّن من رؤية معلومات الدردشة الّتي تُعيد Gemini على الشّاشة، كما في الصورة:

![](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###إنشاء نص من الصور

أنشيّ "خيارات دردشة جيميني" وضبط المعلمات "النموذج"، "مفتاح الواجهة"

قم بقراءة الصورة flower.png من الملف وضعها على "Messages"

![flower.png](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_vision_1.png)

أنشئُ "نقطة طلب دردشة جميني"، انقر على تشغيل، حيث يُمكنك رؤية معلومات الدردشة التي تم إرجاعها مِن غيميني على الشاشة، كما هو موضّح في الصورة:

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_vision_2.png)

###توليف الصوت إلى نص

جيميني يدعم تحويل الصوت إلى نص.

قم بإنشاء الخطة الزرقاء التالية، ثم قم بتحميل الصوت، وقم بضبط خيارات Gemini، وانقر على تشغيل، سترى بعدها عرض معلومات المحادثة التي تم إرجاعها من Gemini بعد معالجة الصوت على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

--8<-- "footer_ar.md"


> تم ترجمة هذه المشاركة باستخدام ChatGPT ، يرجى تزويدنا ب[**ردود فعل**](https://github.com/disenone/wiki_blog/issues/new)هياحدد أي اهمال. 
