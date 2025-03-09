---
layout: post
title: العقدة الوظيفية
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

#الجزء العملي - نقاط الوظائف

قدمت الإضافة مجموعة من نقاط الوظائف السهلة الاستخدام بشكل إضافي.

##Cllama ذات الصلة

تحقق ما إذا كان Cllama llama.cpp مهيأ بشكل صحيح

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"يتم دعم GPU بواسطة Cllama": تحديد ما إذا كان ملف llama.cpp مدعومًا من قبل واجهة النظام المؤثر الخاصة بوحدة المعالجة الرسومية في البيئة الحالية.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

احصل على العمليات الداعمة الخلفية المتاحة في llama.cpp الحالي

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

قم بتجهيز ملف النموذج في حزمة Pak: يقوم بنسخ ملفات النموذج في Pak تلقائيًا إلى النظام الملفات

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

##الصور المتعلقة

تحويل UTexture2D إلى Base64: تحويل صورة UTexture2D إلى تنسيق Base64 png

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

"حفظ UTexture2D إلى ملف .png"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

"Load .png file to UTexture2D" --> "تحميل ملف .png إلى UTexture2D"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"تكرار UTexture2D"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

##الصوتيات ذات الصلة

تحميل ملف .wav إلى USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

تحويل بيانات .wav إلى USoundWave: قم بتحويل البيانات الثنائية wav إلى USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

حفظ USoundWave إلى ملف .wav

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

"احصل على بعض البيانات الخام لتدفق USoundWave": قم بتحويل USoundWave إلى بيانات صوتية ثنائية عشرية

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"تحويل USoundWave إلى Base64"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicate USoundWave": استنساخ USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

تحويل بيانات التقاط الصوت إلى USoundWave: 把 Audio Capture 录音数据转成 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

--8<-- "footer_ar.md"


> تمت ترجمة هذه المشاركة باستخدام ChatGPT، يُرجى تقديم [**ردود**](https://github.com/disenone/wiki_blog/issues/new)يرجى تحديد أي نقص. 
