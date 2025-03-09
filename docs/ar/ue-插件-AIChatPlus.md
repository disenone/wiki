---
layout: post
title: الوثيقة الشرحية
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
description: وثيقة توضيحية
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#ترجمة هذه النص إلى اللغة العربية: 

وثيقة شرح UE إضافة AIChatPlus

##متجر الإضافات

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##المستودع العام

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##مقدمة حول الإضافة

أحدث إصدار v1.6.0.

هذا الإضافة تدعم UE5.2 - UE5.5.

UE.AIChatPlus هو إضافة لـ UnrealEngine تمكن التواصل مع مختلف خدمات GPT AI ، والتي تدعم حاليًا خدمات مثل OpenAI (ChatGPT، DALL-E) ،و Azure OpenAI (ChatGPT، DALL-E) ، Claude ، Google Gemini ، Ollama ، llama.cpp ، بالإضافة إلى التشغيل المحلي. وسيتم دعم المزيد من مزودي الخدمات في المستقبل. تعتمد تنفيذها على طلبات REST غير متزامنة، مما يجعلها كفءة من حيث الأداء ويسهل على مطوري UnrealEngine الوصول إلى هذه الخدمات ذات الصلة بالذكاء الاصطناعي.

تتضمن UE.AIChatPlus أيضًا أداة محرر تمكّنك من استخدام خدمات الدردشة هذه مباشرة في المحرر، لإنشاء نصوص وصور، وتحليل الصور، وما إلى ذلك.

##الميزات الرئيسية

**جديد تمامًا!** تم ترقية الملف AI llama.cpp غير المتصل إلى الإصدار b4604.

**جديد تمامًا!** يدعم Llama.cpp للذكاء الاصطناعي والعمل دون اتصال GPU Cuda و Metal.

**جديد!** يدعم تحويل الصوت إلى نص في Gemini.

**API**: دعم OpenAI، Azure OpenAI، Claude، Gemini، Ollama، llama.cpp، DeepSeek

API الحية بدون اتصال: دعم تشغيل AI الخادم المزود llama.cpp بدون اتصال، ودعم GPU Cuda و Metal.


ترجمة النص إلى النص: تدعم كافة واجهات برمجة التطبيقات إنتاج النصوص.

**نص إلى صورة**: OpenAI DALL-E

**تحويل الصور إلى نص**: OpenAI Vision، Claude، Gemini، Ollama، llama.cpp

**تحويل الصورة إلى صورة**: OpenAI Dall-E

**تحويل الصوت إلى نص**: Gemini

**التصميم الأساسي**: جميع واجهات برمجة التطبيقات والميزات تدعم التصميم الأساسي

أداة محادثة AI المحررة: أداة محادثة AI محررة ذات ميزات غنية ومصممة بعناية

**الاستدعاء الغير متزامن**: يمكن الاستدعاء الغير متزامن لجميع واجهات برمجة التطبيقات (API).

**أدوات مفيدة**: مجموعة متنوعة من الأدوات للصور والصوت

##API المدعومة:

ترجمة النص إلى اللغة العربية:

ملف **Llama.cpp** في وضع عدم الاتصال: يتم دمجه مع مكتبة Llama.cpp ويمكن تشغيل نماذج الذكاء الاصطناعي دون اتصال! كما يدعم نماذج متعددة الوسائط (تجريبي). متوافق مع Win64/Mac/Android/IOS. يدعم GPU CUDA وMETAL.

**OpenAI**：/الدردشة/اكتمالات،/اكتمالات،/الصور/أجيال،/الصور/تحريرات،/الصور/تنويعات

Azure OpenAI: /chat/completions، /images/generations

**كلود**: /الرسائل، /اكتمال

**الجوزاء** : generateText ،: generateContent ،: streamGenerateContent

**Ollama**：/api/chat، /api/generate، /api/tags

**DeepSeek**：/chat/completions

##تعليمات الاستخدام

[**Blueprints Guide - Instructions for Use**](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

Translate these text into Arabic language:

[**دليل الاستخدام - C++**](ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

ترجمة هذا النص إلى اللغة العربية:

[**دليل الاستخدام - قسم المحرر**](ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

[**تعليمات الاستخدام - التعبئة**](ue-插件-AIChatPlus-Usage-Package-GetStarted.md)

##تعديل السجل

(ue-插件-AIChatPlus-ChangeLogs.md)

##الدعم الفني

**التعليقات**: إذا كانت لديك أي أسئلة، فلا تتردد في ترك تعليق في منطقة التعليقات أدناه.

**البريد الإلكتروني**: يمكنك أيضًا إرسال بريد إلكتروني لي عبر البريد الإلكتروني (disenonec@gmail.com)

**Discord**: سيتم الإطلاق قريبًا

--8<-- "footer_ar.md"


> هذه المشاركة تم ترجمتها باستخدام ChatGPT، يرجى تقديم [**ردود فعل**](https://github.com/disenone/wiki_blog/issues/new)يرجى تحديد أي نقص. 
