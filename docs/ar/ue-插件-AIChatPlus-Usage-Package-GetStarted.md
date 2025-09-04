---
layout: post
title: حزم
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
description: حزمة
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - Package 篇 - Get Started" />

#حزم

##حزمة الإضافة

عند تجميع Unreal، سيتم تجميع الملفات الديناميكية المطلوبة من قبل الإضافات تلقائيًا، مما يجعلها جاهزة للاستخدام فور تمكين الإضافة.

مثال على ذلك في حالة نظام التشغيل Windows، سيتم ضمّ llama.cpp وملفات dll ذات الصلة بـ CUDA تلقائيًا إلى دليل الحزم بعد الضغط. وبالنسبة للمنصات الأخرى مثل Android / Mac / IOS سيتم ذلك بنفس الطريقة.

يمكنك تنفيذ الأمر "AIChatPlus.PrintCllamaInfo" في النسخة Development بعد التعبئة للعبة، لعرض حالة بيئة Cllama الحالية، وتأكيد ما إذا كانت الحالة طبيعية، وما إذا كانت تدعم وحدة المعالجة الرسومية GPU.

##حزم النموذج

من المفترض أنه إذا تم وضع ملفات النموذج المضافة للمشروع في الدليل Content/LLAMA، يمكن تعيين ضم هذا الدليل أثناء التعبئة.

افتح "Project Setting"، اختر علامة التبويب Packaging، أو ابحث مباشرة عن "asset package"، ابحث عن إعداد "Additional Non-Asset Directories to Package"، ثم أضف الدليل Content/LLAMA.

![](assets/img/2024-ue-aichatplus/usage/package/getstarted_1.png)

عند إضافة الجدول، سيقوم Unreal تلقائيًا بتجميع جميع ملفات الدليل عند قيامه بعملية التعبئة.

##قراءة ملف النموذج الغير متصل بعد تجميعه

يعتاد Uneal عادةً تعبئة جميع ملفات المشروع في ملف .Pak، وعندما يتم تمرير مسارات الملفات من .Pak إلى نموذج Cllam الغير متصل، سيؤدي ذلك إلى فشل التنفيذ، لأن ملف llama.cpp لا يمكنه قراءة ملفات النموذج المعبأة في .Pak مباشرة.

لذلك، من الضروري نسخ ملفات النموذج من .Pak أولاً إلى النظام الملفي. يوفر المكون إحدى الدوال المريحة التي تقوم بنسخ ملفات النموذج من .Pak مباشرة وتعيد مسار الملف المنسوخ، مما يمكن Cllama من قراءته بكل سهولة.

نقطة "Cllama Prepare ModelFile In Pak" في الرسم البياني: تقوم تلقائيًا بنسخ ملفات النموذج من Pak إلى النظام الملفاتية.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

الرمز في لغة C++ هو:

```
#include <Cllama/AIChatPlusCllama_Util.h>

auto ModelPath = FAIChatPlusCllama_Util::PrepareModelFileInPak(InContentPath);
```

--8<-- "footer_ar.md"


> هذا المنشور تمت ترجمته باستخدام ChatGPT، يرجى تقديم [**تعليقات**](https://github.com/disenone/wiki_blog/issues/new)إشرح أي فراغات تم إهمالها. 
