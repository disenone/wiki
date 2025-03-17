---
layout: post
title: Cllama (llama.cpp)
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
- llama.cpp
description: Cllama (llama.cpp)
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Cllama (llama.cpp)" />

#الفصل الأزرق - Cllama (llama.cpp)

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_all.png)

##النموذج الغير متصل

تستند Cllama إلى llama.cpp وتدعم استخدام نماذج الذكاء الاصطناعي للتحليل دون اتصال بالإنترنت.

نظرًا لأنها خارج الاتصال، نحتاج أولاً إلى تجهيز ملفات النموذج، على سبيل المثال، يمكن تنزيل نموذج خارج الاتصال من موقع HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

ضع النموذج في مجلد معين، مثل وضعه في دليل مشروع اللعبة تحت المسار Content/LLAMA

```shell
E:/UE/projects/FP_Test1/Content/LLAMA > ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

بعد الحصول على ملف النموذج غير المتصل، يمكننا استخدام Cllama لإجراء محادثات AI.

##الدردشة النصية

استخدام Cllama لمحادثات النص

أنشئ عقدًا باسم `Send Cllama Chat Request` باستخدام زر الماوس الأيمن في الرسم البياني.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

أنشئ `Options` العقد، وقم بتعيين `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

أنشئ رسائل، وأضف رسالة نظام ورسالة مستخدم على التوالي.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

إنشاء الـ Delegate الذي يقبل مخرجات النموذج ويقوم بطباعتها على الشاشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

النسخة الكاملة من المخطط تبدو كما هو موضح، عند تشغيل المخطط، سترى رسالة تعود بناء النموذج الكبير المطبوع على شاشة اللعبة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##توليف الصور إلى نصوص llava

Cllama اعطت دعمًا تجريبيًا أيضًا لمكتبة llava، مما يوفر إمكانية Vision

أعد ملف نموذج Multimodal للعمل دون اتصال بالإنترنت، مثل Moondream ([moondream2-text-model-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-text-model-f16.gguf), [moondream2-mmproj-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-mmproj-f16.gguf)）أو Qwen2-VL（[Qwen2-VL-7B-Instruct-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/Qwen2-VL-7B-Instruct-Q8_0.gguf), [mmproj-Qwen2-VL-7B-Instruct-f16.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-7B-Instruct-f16.gguf)نموذج Multimodal المدعوم بواسطة llama.cpp أو غيرها.

إنشاء عقد Options، وتعيين المعلمات "Model Path" و "MMProject Model Path" بملفات النموذج متعددة الوسائط المقابلة.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_1.png)

إنشاء ​​العقدة لقراءة ملف الصور flower.png وتعيين الرسائل

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_3.png)

أنشئ العقدة النهائية لاستقبال المعلومات المرتجعة واطبعها على الشاشة. هكذا تبدو النسخة الكاملة من الخطة.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_4.png)

يمكنك رؤية النص الذي تم إرجاعه عند تشغيل المخطط الأزرق.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_5.png)

##llama.cpp تستخدم وحدة المعالجة الرسومية (GPU)

"خيارات طلب محادثة Cllama" تحتوي على معلمة "Num Gpu Layer" الجديدة، حيث يمكن تعيين حمولة ال GPU في ملف llama.cpp، والتحكم في عدد الطبقات التي يجب حسابها على وحدة المعالجة الرسومية. تفضلوا بالاطلاع على الصورة."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

## KeepAlive

"خيارات طلب الدردشة Cllama" تقوم بإضافة معلمة "KeepAlive"، والتي تسمح بالاحتفاظ بملف النموذج بالذاكرة بعد القراءة، لتسهيل الاستخدام المباشر في المرات القادمة وتقليل عدد مرات قراءة النموذج. يُعبر KeepAlive عن وقت احتفاظ النموذج، حيث 0 يعني عدم الاحتفاظ والإفراج فور الاستخدام؛ بينما -1 يعني الاحتفاظ الدائم. يمكن تعيين قيم مختلفة لـ KeepAlive لكل طلب بمرة، وسيحل القيمة الجديدة محل القيمة القديمة، مثلما يمكن تعيين KeepAlive=-1 في الطلبات السابقة للإبقاء على النموذج في الذاكرة حتى تحديد كيفية الإفراج عن ملف النموذج في الطلب الأخير بوضع KeepAlive=0.

##معالجة ملفات النموذج في ملف .Pak بعد الضغط

عندما تقوم بتشغيل Pak بعد ضغطه، سيتم وضع جميع ملفات موارد المشروع في ملف .Pak، بما في ذلك ملفات نماذج الرسومات ثلاثية الأبعاد.

نظرًا لعدم قدرة llama.cpp على قراءة ملف .Pak مباشرة ، فإنه من الضروري نسخ ملفات النماذج الغير متصلة من ملف .Pak ووضعها في نظام الملفات.

AIChatPlus يوفر وظيفة تلقائية لنسخ ومعالجة ملفات النموذج في .Pak ووضعها في مجلد Saved.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

يمكنك تولي معالجة ملفات النموذج في .Pak بنفسك، المهم هو نسخ الملفات لأنه لا يمكن لـ llama.cpp قراءة .Pak بشكل صحيح.

##نقطة الوظيفة

Cllama قدم بعضًا من العقد الوظيفية لتسهيل الحصول على حالة البيئة الحالية


"Cllama Is Valid": تقييم ما إذا كان Cllama llama.cpp تم تهيئته بشكل صحيح

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

تحقق مما إذا كانت llama.cpp تدعم بيئة GPU الحالية.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"احصل على دعم الخلفيات الحالية من llama.cpp"


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

قم بإعداد ملف النموذج في Pak: تقوم تلقائيًا بنسخ ملفات النموذج في Pak إلى النظام الملفاتية

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)


--8<-- "footer_ar.md"


> هذه المشاركة تمت ترجمتها باستخدام ChatGPT، يرجى تقديم [**تعليقات**](https://github.com/disenone/wiki_blog/issues/new)يرجى تحديد أي عنصر ناقص. 
