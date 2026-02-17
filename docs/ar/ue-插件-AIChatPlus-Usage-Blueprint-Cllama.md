---
layout: post
title: كلاما (llama.cpp) (مهجور)
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

#الرؤية المستقبلية - سي لاما (لاما.cpp) (متقادم)

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_all.png)

##مهمل

تم تحديد Cllama على أنها **مهجورة** ولن يتم صيانتها بعد الآن.

تم توفير الوظائف الأصلية لـ Cllama بواسطة [CllamaServer](ue-插件-AIChatPlus-Usage-Blueprint-CllamaServer.md)لتحمل.

##نموذج غير متصل

Clama مبنية على llama.cpp، وتدعم استخدام نماذج استنتاج الذكاء الاصطناعي دون اتصال بالإنترنت.

نظرًا لأن العملية بدون اتصال، نحتاج إلى تحضير ملف النموذج مسبقًا، مثل تنزيل نموذج غير متصل من موقع HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

ضع النموذج في مجلد معين، على سبيل المثال تحت دليل مشروع اللعبة في مسار Content/LLAMA

```shell
E:/UE/projects/FP_Test1/Content/LLAMA > ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

بعد الحصول على ملفات النموذج بدون اتصال، يمكننا استخدام Cllama لإجراء محادثات الذكاء الاصطناعي

##المحادثة النصية

استخدام Cllama للدردشة النصية

انقر بزر الماوس الأيمن في المخطط لإنشاء عقدة تُسمى `Send Cllama Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

إنشاء عقدة Options وتعيين `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

إنشاء رسائل، إضافة رسالة نظام ورسالة مستخدم بشكل منفصل

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

إنشاء مُفوّض يَتلَقّى مُخرَجات النموذج ويُطبعها على الشاشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

تبدو الخريطة الكاملة هكذا، قم بتشغيل الخريطة وسوف ترى شاشة اللعبة وهي تطبع الرسالة التي يعيدها النموذج الكبير

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##إنشاء النصوص من الصور ليافا

يدعم Cllama أيضًا مكتبة llava تجريبيًا، مما يوفر قدرات Vision.

أولاً، قم بإعداد ملفات نموذج Multimodal دون اتصال، مثل Moondream ([moondream2-text-model-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-text-model-f16.gguf), [moondream2-mmproj-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-mmproj-f16.gguf)) أو Qwen2-VL ([Qwen2-VL-7B-Instruct-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/Qwen2-VL-7B-Instruct-Q8_0.gguf), [mmproj-Qwen2-VL-7B-Instruct-f16.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-7B-Instruct-f16.gguf)) أو أي نموذج متعدد الوسائط آخر تدعمه llama.cpp.

إنشاء عقدة Options، وتعيين المعلمات "Model Path" و"MMProject Model Path" إلى ملفات النموذج متعدد الوسائط المقابلة.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_1.png)

إنشاء عقدة لقراءة ملف الصورة flower.png، وتحديد الرسائل

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_3.png)

أخيرًا يأخذ العقدة المُنشأة المعلومات المرتجَعة ويطبعها على الشاشة، تبدو الخطة الكاملة هكذا

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_4.png)

شغّل المخطط لرؤية النص المعاد

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_5.png)

##llama.cpp يستخدم وحدة معالجة الرسومات (GPU)

"خيارات طلب الدردشة في Cllama" تمت إضافة معلمة "Num Gpu Layer"، التي تتيح ضبط حمل وحدة معالجة الرسوميات في llama.cpp، مما يسمح بالتحكم في عدد الطبقات المطلوب حسابها على وحدة معالجة الرسوميات. كما هو موضح في الصورة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

## KeepAlive

مُخصَّصات طلب الدردشة Cllama  

تمت إضافة المعلمة **"KeepAlive"** التي تتيح إبقاء ملف النموذج محملًا في الذاكرة بعد قراءته، مما يُسهل استخدامه مباشرةً في المرة التالية ويقلل من عدد مرات إعادة قراءة النموذج.  
القيمة **KeepAlive** تمثل المدة التي يظل فيها النموذج محتفظًا به:  
- **0** تعني عدم الاحتفاظ به، وسيتم تحريره فور الاستخدام.  
- **-1** تعني الاحتفاظ به بشكل دائم.  

يمكنك تعيين قيمة **KeepAlive** مختلفة في كل طلب **Options**، حيث ستستبدل القيمة الجديدة القيمة القديمة. على سبيل المثال:  
- يُمكنك ضبط الطلبات الأولى على **KeepAlive=-1** للاحتفاظ بالنموذج في الذاكرة.  
- ثم ضبط الطلب الأخير على **KeepAlive=0** لتحرير ملف النموذج.

##معالجة ملفات النماذج داخل حزمة .Pak بعد التعبئة

بعد تفعيل حزمة Pak، سيتم وضع جميع ملفات موارد المشروع في ملف .Pak، بما في ذلك ملف نموذج غير المتصل gguf.

بما أن llama.cpp لا يدعم القراءة المباشرة لملفات .Pak، لذا يجب نسخ ملفات النموذج دون اتصال من ملف .Pak إلى نظام الملفات.

يوفر AIChatPlus وظيفة تعمل تلقائيًا على نسخ ومعالجة ملفات النماذج من ملفات .Pak، ثم وضعها في مجلد Saved:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

أو يمكنك التعامل مع ملفات النماذج في `.Pak` بنفسك، الأمر الأساسي هو أنك بحاجة إلى نسخ الملفات خارجها، لأن `llama.cpp` لا يمكنه قراءة ملفات `.Pak` بشكل صحيح.

##العقدة الوظيفية

يقدم Cllama بعض العُقَد الوظيفية لتسهيل الحصول على حالة البيئة الحالية.


"كللاما صالح": للتحقق مما إذا كان Cllama llama.cpp مهيأ بشكل صحيح

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"كلاما يدعم جي بي يو"： يحدد ما إذا كان llama.cpp يدعم واجهة جي بي يو الخلفية في البيئة الحالية.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"الحصول على دعم خلفيات cllama": استرجاع جميع الخلفيات المدعومة حاليًا في llama.cpp


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"كلاما تحضير ملف النموذج في باك": نسخ ملفات النموذج من باك إلى نظام الملفات تلقائيًا

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)


--8<-- "footer_ar.md"


> هذا المنشور مترجم باستخدام ChatGPT، يُرجى تقديم [**ملاحظات**](https://github.com/disenone/wiki_blog/issues/new)الإشارة إلى أي أوجه قصور في النص. 
