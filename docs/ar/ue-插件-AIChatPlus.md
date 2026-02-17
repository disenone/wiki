---
layout: post
title: وثائق التوضيحية
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
description: '# وثائق التوضيحية'
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#وثائق شرح إضافة UE AIChatPlus

##سوق الملحقات

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##المستودع العام

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##وصف الملحق

أحدث إصدار v2.0.0.

يدعم هذا الإضافة إصدارات UE5.2 إلى UE5.7.

UE.AIChatPlus هو ملحق لـ UnrealEngine يُنفّذ التواصل مع مختلف خدمات الدردشة بالذكاء الاصطناعي من نوع GPT. الخدمات المدعومة حالياً تشمل OpenAI (ChatGPT, DALL-E)، Azure OpenAI (ChatGPT, DALL-E)، Claude، Google Gemini، Ollama، و llama.cpp للعمل المحلي دون اتصال. ومن المخطط دعم المزيد من مزودي الخدمات في المستقبل. يعتمد هذا الملحق على طلبات REST غير المتزامنة لتحقيق كفاءة عالية في الأداء، مما يسهّل على مطوّري UE دمج هذه الخدمات الذكية في مشاريعهم.

في الوقت نفسه، يتضمن UE.AIChatPlus أيضًا أداة محرر تتيح لك استخدام خدمات الدردشة بالذكاء الاصطناعي مباشرةً داخل المحرر، وإنشاء نصوص وصور، وتحليل الصور وما إلى ذلك.

##الوظائف الرئيسية

**جديد!** جميع واجهات برمجة التطبيقات تدعم استدعاء الأداة ToolCall.

**جديد!** دعم OpenAI/Azure للتحويل من الكلام إلى النص ومن النص إلى الكلام.

**جديد!** Blueprint تدعم Json الآن.

**جديد!** تم تحديث الذكاء الاصطناعي دون اتصال llama.cpp إلى الإصدار b6792.

**جديد!** دعم AI llama.cpp للعمل بدون اتصال مع تقنيتي GPU Cuda و Metal.

**جديد!** يدعم جيميني تحويل الصوت إلى نص.

**API** : يدعم OpenAI و Azure OpenAI و Claude و Gemini و Ollama و llama.cpp و DeepSeek

**واجهة برمجة التطبيقات (API) المباشرة دون اتصال بالإنترنت**: تدعم تشغيل الذكاء الاصطناعي من خلال llama.cpp دون اتصال، مع دعم وحدات معالجة الرسومات Cuda وMetal.

**نص إلى نص**: تدعم واجهات برمجة التطبيقات المختلفة توليد النص.

**تحويل النص إلى صورة**: OpenAI Dall-E

**تحويل الصور إلى نص**: OpenAI Vision، Claude، Gemini، Ollama، llama.cpp

**صورة إلى صورة**: أوپن إي آي دال-إي

تحويل الكلام إلى نص: جيمناي

**المخطط الزرقاء** : جميع واجهات برمجة التطبيقات والميزات تدعم المخطط الزرقاء

**أداة الدردشة للمحرر**: أداة ذكاء اصطناعي للمحرر غنية بالميزات ومصممة بعناية

**استدعاء غير متزامن**: يمكن استدعاء جميع APIs بشكل غير متزامن

**أدوات عملية**: مجموعة متنوعة من أدوات الصور والصوت

##واجهات برمجة التطبيقات المدعومة:

**Llama.cpp بدون اتصال**: مُتكامل مع مكتبة llama.cpp، يُمكن تشغيل نماذج الذكاء الاصطناعي دون اتصال بالإنترنت! كما يدعم النماذج متعددة الوسائط (بشكل تجريبي). يدعم أنظمة التشغيل ويندوز 64 بت/ماك/أندرويد/آي أو إس. بالإضافة إلى دعم وحدات معالجة الرسومات CUDA و METAL.

**OpenAI**: /chat/completions، /completions، /images/generations، /images/edits، /images/variations

**Azure OpenAI**: /chat/completions، /images/generations

**كلود**: /messages، /complete

**جيميني**: generateText، generateContent، streamGenerateContent

**أولاما**: /api/chat، /api/generate، /api/tags

**DeepSeek**: /chat/completions

##دليل الاستخدام

[**دليل الاستخدام - قسم المخططات**](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

[**دليل الاستخدام - لغة C++**](ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

**[تعليمات الاستخدام - قسم المحرر](ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

[**تعليمات الاستخدام - التغليف**](ue-插件-AIChatPlus-Usage-Package-GetStarted.md)

##سجل التغييرات

[**سجل التغييرات**](ue-插件-AIChatPlus-ChangeLogs.md)

##دعم فني

**تعليق**: لأي استفسارات، يرجى ترك تعليق أدناه في قسم التعليقات

**بريد إلكتروني**: يمكنك أيضًا مراسلتي عبر البريد الإلكتروني (disenonec@gmail.com)

**ديскор드**: قريباً سيتم إطلاقه

--8<-- "footer_ar.md"


> هذا المنشور مترجم باستخدام ChatGPT، يُرجى تقديم [**تقييمك**](https://github.com/disenone/wiki_blog/issues/new)الإشارة إلى أي إغفالات. 
