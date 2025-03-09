---
layout: post
title: حزمة
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
description: حزم
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - Package 篇 - Get Started" />

#تعبئة

##الرجاء تقديم نص آخر يتطلب ترجمة.

عند تجميع Unreal، سيتم ضمن العملية تجميع جميع ملفات المكتبة الديناميكية اللازمة للإضافات تلقائيًا، كل ما عليك فعله هو تمكين الإضافة.

مثلاً بالنسبة لنظام Windows، سيتم وضع ملف llama.cpp وملفات dll ذات الصلة بـ CUDA تلقائياً في الدليل الناتج بعد عملية التعبئة. وهو نفس الأمر بالنسبة لمنصات أخرى مثل Android / Mac / IOS.

يمكنك تنفيذ الأمر "AIChatPlus.PrintCllamaInfo" في نسخة لعبة Development المعبأة لعرض حالة بيئة Cllama الحالية والتحقق مما إذا كانت الحالة طبيعية وما إذا كانت تدعم وحدة المعالجة الرسومية.

##تعبئة النموذج

وضعت ملفات النموذج الخاص بالمشروع في المجلد Content/LLAMA، يمكنك بالتالي تعيين ضم هذا المجلد أثناء عملية التعبئة.

افتح "إعداد المشروع"، اختر علامة التبويب التعبئة، أو ابحث مباشرة عن "asset package"، ابحث عن إعداد "Additional Non-Asset Directories to Package"، ثم أضف الدليل Content/LLAMA.

![](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_6.png)

بعد إضافة جدول المحتويات، سيقوم Unreal تلقائيًا بتجميع جميع ملفات الدليل أثناء عملية التعبئة.


##قراءة الملف النمطي الذي تم ضغطه بعد التحميل الغير متصل

عادة ما يقوم Uneal بتعبئة ملفات المشروع في ملف .Pak، وفي هذه الحالة إذا تم تمرير مسارات الملفات في .Pak إلى نموذج Cllam للعمل دون اتصال، سيؤدي ذلك إلى فشل التنفيذ، لأن llama.cpp لا يمكنه قراءة ملفات النموذج المعبأة في .Pak مباشرة.

لذا يجب نسخ ملفات النماذج من ملف .Pak أولاً إلى نظام الملفات. يوفر المكون وظيفة مريحة لنسخ ملفات النموذج من .Pak مباشرة وإعادة مسار النسخ، مما يجعل Cllama قادرًا على قراءتها بسهولة.

نقطة الرسم البياني هي "Cllama Prepare ModelFile In Pak": تقوم تلقائيًا بنسخ ملفات النموذج في Pak إلى النظام الملفات

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

النص المراد ترجمته هو:
C++ function code is:

```
#include <Cllama/AIChatPlusCllama_Util.h>

auto ModelPath = FAIChatPlusCllama_Util::PrepareModelFileInPak(InContentPath);
```

--8<-- "footer_ar.md"


> هذا المنشور تم ترجمته باستخدام ChatGPT، يرجى تقديم [**ردود فعل**](https://github.com/disenone/wiki_blog/issues/new)يُرجى تحديد أي نقص. 
