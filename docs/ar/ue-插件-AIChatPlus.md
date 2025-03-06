---
layout: post
title: وثيقة توضيحية
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
description: وثيقة الشرح
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#مستند تعليمات ملحق UE AIChatPlus

##متجر الإضافات

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##المستودع العام

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##مقدمة الإضافة

الإصدار الأحدث v1.6.0.

هذا الملحق يدعم UE5.2 - UE5.5.

UE.AIChatPlus هو إضافة لـ UnrealEngine، تمنحك القدرة على التواصل مع مختلف خدمات الدردشة الاصطناعية مثل GPT AI، حيث يدعم حاليا خدمات مثل OpenAI (ChatGPT، DALL-E)، Azure OpenAI (ChatGPT، DALL-E)، Claude، Google Gemini، Ollama، وllama.cpp للعمل دون الحاجة إلى الاتصال بالإنترنت. كما سيتم دعم المزيد من مقدمي الخدمات في المستقبل. يستند تنفيذه على طلبات REST غير المتزامنة، مما يجعله فعالاً من حيث الأداء وملائماً لمطوري UnrealEngine للوصول إلى هذه الخدمات الذكية للدردشة.

تتضمن UE.AIChatPlus أيضًا أداة محرر تسمح بالوصول المباشر إلى خدمات الدردشة الذكية هذه من خلال المحرر، مما يسمح بإنشاء نصوص وصور، وتحليل الصور، وما إلى ذلك.

##الرئيسيةية

**جديد!** ترقية ملف AI llama.cpp إلى الإصدار b4604 دون اتصال.

**جديد تمامًا!** دعم GPU Cuda و Metal لـ llama.cpp AI غير متصل.

**جديد تمامًا!** دعم تحويل الصوت إلى نص للجوال Gemini.

**API**: يدعم OpenAI و Azure OpenAI و Claude و Gemini و Ollama و llama.cpp و DeepSeek

**API في الوقت الفعلي دون اتصال**: يدعم تشغيل AI بدون اتصال عبر llama.cpp، بدعم لـ GPU Cuda وMetal.

نص إلى نص: يدعم جميع أنواع واجهات برمجة التطبيقات إنتاج النص.

**تحويل النص إلى صورة**: OpenAI Dall-E

الرفات الطيّبة: OpenAI Vision، Claude، Gemini، Ollama، llama.cpp

"تحويل الصورة إلى صورة": OpenAI Dall-E

تحويل الصوت إلى نص: جيميني

الخطة: جميع وظائف وواجهات برمجة التطبيقات تدعم الخطة.

أداة المحادثة الذكية Editor: أداة محادثة AI للمحرر مصممة بعناية وتحتوي على ميزات غنية

الاستدعاء الغير متزامن: يمكن استدعاء جميع واجهات البرمجة الخاصة بالتطبيقات بشكل غير متزامن.

**أدوات عملية**: مجموعة متنوعة من أدوات الصور والصوت

##الواجهة البرمجية القابلة للتطبيق المدعومة:

ترجمة النص إلى اللغة العربية:

**llama.cpp خارطة ذهنية** : تكامل مع مكتبة llama.cpp لتشغيل نماذج الذكاء الاصطناعي حتى بدون اتصال بالإنترنت! ويدعم أيضا نماذج متعددة الوسائط (بشكل تجريبي). متوافق مع Win64/Mac/Android/IOS. ويدعم CUDA و METAL للـ GPU.

**OpenAI**：/chat/completions، /completions، /images/generations، /images/edits، /images/variations

Azure OpenAI: /chat/completions، /images/generations

**كلود**: / الرسائل ، / الاكتمال

**جيميني**: :إنشاءالنص، :إنشاءالمحتوى، :توليفالمحتوى البثّي

**Ollama**：/api/chat، /api/generate، /api/tags

**DeepSeek**：/الدردشة/اكتمال

##الرجاء ترجمة النص إلى اللغة العربية:

(ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

(ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

الرجاء تحويل هذا النص إلى اللغة العربية:

[**تعليمات الاستخدام - جزء المحرر**](ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

##تغيير سجل

(ue-插件-AIChatPlus-ChangeLogs.md)

##الدعم التقني

**التعليقات**: لا تتردد في ترك تعليق في الجزء أدناه إذا كان لديك أي استفسار

**البريد الإلكتروني**: يمكنك أيضًا مراسلتي عبر البريد الإلكتروني ( disenonec@gmail.com)

**discord**: قريبًا سيتم الإطلاق.

--8<-- "footer_ar.md"


> تمت ترجمة هذه المشاركة باستخدام ChatGPT، يرجى تزويدنا بال[**تغذية راجعة**](https://github.com/disenone/wiki_blog/issues/new)يرجى تحديد أي علتات. 
