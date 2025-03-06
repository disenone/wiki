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

#القسم الأزرق - Cllama (llama.cpp)

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_all.png)

##النموذج غير متصل

Cllama تم تنفيذها بناءً على llama.cpp، وتدعم استخدام نماذج الذكاء الاصطناعي للتفكير دون اتصال بالإنترنت.

نظرًا لأنها خارج الاتصال، نحتاج أولاً إلى تحضير ملف النموذج، على سبيل المثال، يمكن تنزيل نموذج الخطاب الخارج الاتصال من موقع HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

ضع النموذج في مجلد معين، مثل وضعه في دليل المشروع للعبة Content/LLAMA

```shell
E:/UE/projects/FP_Test1/Content/LLAMA > ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

بمجرد الحصول على ملف النموذج الغير متصل بالإنترنت، يمكننا استخدام Cllama للقيام بالدردشة الذكية.

##الرد على الأسئلة

استخدم Cllama للدردشة النصية

في النموذج، انقر بزر الماوس الأيمن لإنشاء عقدة "Send Cllama Chat Request".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

أنشئُوا nOptions للعُقد، وقُوموا بتعيين "Stream=true, ModelPath=`E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf`"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

إنشاء Messages ، قم بإضافة رسالة من نوع System Message و User Message بشكل منفصل

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

إنشاء نائب Delegate يقوم بتلقي مخرجات النموذج وطباعتها على الشاشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

الترجمة إلى اللغة العربية:

"النص الكامل يبدو كما يلي، قم بتشغيل النص لترى رسالة إرجاع شاشة اللعبة الكبيرة المطبوعة."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##إنشاء نصوص الصور.

Cllama دعمت تجريبيًا مكتبة llava ، مما يوفر قدرة Vision.

قم بتحضير ملف النموذج اللاحق Multimodal، مثل Moondream ([moondream2-text-model-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-text-model-f16.gguf), [moondream2-mmproj-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-mmproj-f16.gguf)) أو Qwen2-VL([Qwen2-VL-7B-Instruct-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/Qwen2-VL-7B-Instruct-Q8_0.gguf), [mmproj-Qwen2-VL-7B-Instruct-f16.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-7B-Instruct-f16.gguf)أو نموذج Multimodal الذي يدعمه ملف llama.cpp أو غيره.

إنشاء عقدتي Options، وتعيين المعلمات "مسار النموذج" و"مسار نموذج MMProject" بملفات النموذج متعدد الوسائط المقابلة.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_1.png)

إنشاء العقدة لقراءة ملف الصور flower.png، وتعيين الرسائل

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_3.png)

أخيرًا، يتم إنشاء العقدة واستقبال المعلومات المُرجعة، ثم يتم طباعتها على الشاشة. الرسم البياني الكامل يبدو كما يلي:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_4.png)

يمكنك رؤية النص المُرجع عند تشغيل الشكل الأزرق

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_5.png)

##llama.cpp تستخدم وحدة المعالجة الرسومية (GPU)

"خيارات طلب المحادثة Cllama" قامت بإضافة المعلمة "Num Gpu Layer" ، حيث يمكن تعيين حمولة الـ GPU في llama.cpp ، مما يمكّن من التحكم في عدد الطبقات التي يجب حسابها على وحدة المعالجة الرسومية. يرجى الرجوع إلى الصورة المرفقة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

##تعامل مع ملفات النموذج في ملف .Pak بعد التعبئة

عند فتح ملف الـ Pak بعد التعبئة، سيتم وضع جميع ملفات الموارد للمشروع في ملف .Pak، بما في ذلك ملفات نماذج الـ gguf الخارجية.

نظرًا لعدم دعم llama.cpp لقراءة ملفات .Pak مباشرة، فمن الضروري نسخ ملفات النماذج غير المتصلة من ملف .Pak ووضعها في نظام الملفات.

AIChatPlus توفر وظيفة تقوم تلقائيًا بنسخ ومعالجة ملفات النموذج في .Pak ووضعها في مجلد Saved.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

أو يمكنك التعامل بنفسك مع ملفات النموذج في .Pak ، المهم هو نسخ الملفات لأنه لا يمكن لـ llama.cpp قراءة .Pak بشكل صحيح.

##نقطة الوظيفة

Cllama قدم بعض عقد الوظائف لتسهيل الحصول على حالة البيئة الحالية.


"Cllama Is Valid"：تقييم ما إذا كان الملف Cllama llama.cpp مُهيأ بشكل صحيح

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Llama هل لديها دعم لوحدة معالجة الرسوميات"：تحديد ما إذا كان ملف llama.cpp يدعم GPU backend في البيئة الحالية

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"الحصول على العناصر الخلفية المعتمدة حاليًا بواسطة llama.cpp"


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

جهز ملف النموذج Cllama في Pak: قم بنسخ ملفات النموذج في Pak تلقائيًا إلى النظام الملفاتية

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)


--8<-- "footer_ar.md"


> هذه المشاركة تمت ترجمتها باستخدام ChatGPT، يُرجى تقديم [**ردود**](https://github.com/disenone/wiki_blog/issues/new)يرجى تحديد أي نقص. 
