---
layout: post
title: نقطة الوظيفة
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
description: نقطة الوظيفة
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - 功能节点" />

#العنوان الأزرق - عقد الوظائف

قدم الإضافة مجموعة إضافية من عقد الوظائف الهامة والمفيدة.

##Cllama ذات الصلة

"Cllama Is Valid"：قم بتقييم ما إذا كان ملف Cllama llama.cpp قد تمت مبادلته بشكل صحيح

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

تحقق مما إذا كان ملف llama.cpp يدعم واجهة الـ GPU في البيئة الحالية.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"احصل على دعم الخلفيات المدعومة حاليًا في llama.cpp"


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

قم بإعداد ملف النموذج في ملف Pak: يقوم تلقائيًا بنسخ ملفات النموذج من Pak إلى النظام الملفي

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###الصور والصور ذات الصلة

تحويل UTexture2D إلى Base64: تحويل صورة UTexture2D إلى شكل png base64

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

حفظ UTexture2D إلى ملف .png

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

"تحميل ملف .png إلى UTexture2D": قراءة ملف png كـ UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Duplicate UTexture2D": استنسخ UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###العنصر الصوتي

"تحميل ملف .wav لـ USoundWave"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

تحويل بيانات صوت .wav إلى USoundWave: 把 wav بيانات  ثنائية إلى USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

"احفظ USoundWave في ملف .wav"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

"احصل على بعض بيانات USoundWave Raw PCM": قم بتحويل USoundWave إلى بيانات صوتية ثنائيةية

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

تحويل USoundWave إلى Base64

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"ستُكرر الصوت USoundWave": 复制 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

تحويل بيانات تسجيل الصوت إلى USoundWave: 把 Audio Capture 录音数据转成 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

--8<-- "footer_ar.md"


> تمت ترجمة هذا المنشور باستخدام ChatGPT، الرجاء تقديم [**تعليقاتك**](https://github.com/disenone/wiki_blog/issues/new)الرجاء تحديد أي نقص. 
