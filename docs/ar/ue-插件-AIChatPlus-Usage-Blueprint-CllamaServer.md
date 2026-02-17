---
layout: post
title: CllamaServer (llama.cpp server)
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
- CllamaServer
description: CllamaServer (llama.cpp server)
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - CllamaServer (llama.cpp server)" />

#المخطط الأساسي - CllamaServer (خادم llama.cpp)

<!-- الصورة المطلوبة: عرض شامل لجميع عقد المخططات المرتبطة بـ CllamaServer، مشابه لملف xxx_all.png في الوثائق الأخرى -->
![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_all.png)

##ملخص

CllamaServer تم تطويره بناءً على وضع Server الخاص بـ llama.cpp، حيث يمكنه تشغيل خادم متوافق مع واجهة برمجة تطبيقات OpenAI محليًا، وهو يدعم مجموعة متنوعة من الميزات:

* **خدمة الاستدلال المحلية**: تشغيل خادم استدلال الذكاء الاصطناعي محلياً دون الحاجة إلى واجهات برمجة التطبيقات الخارجية
* **متوافق مع واجهة برمجة تطبيقات OpenAI**: استخدام تنسيق واجهة برمجة تطبيقات متوافق مع OpenAI لتسهيل الهجرة والتكامل
* **دعم متعدد للجلسات**: يدعم العديد من الطلبات المتزامنة
* **استدعاء الأدوات**: يدعم وظيفة استدعاء الوظائف
* **تحويل الصوت إلى نص**: يدعم ميزة الصوت إلى نص (Speech-to-Text)
* **الإدارة المرئية**: تتضمن الواجهة المدمجة في المحرر إدارة الخادم

الفرق بينه وبين Cllama:
* **Cllama**: تحميل النموذج مباشرة داخل العملية للاستدلال، يمكن معالجة طلب واحد فقط في المرة الواحدة
* **CllamaServer**: بدء تشغيل خادم HTTP مستقل قادر على معالجة طلبات متعددة متزامنة، مع توافق واجهة برمجة التطبيقات (API) مع تنسيق OpenAI

##الاستعدادات

نظرًا لتشغيله محليًا، يجب عليك أولاً إعداد ملف النموذج دون اتصال، مثل تحميله من HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

ضع النموذج في مجلد معين على سبيل المثال في دليل مشروع اللعبة `Content/LLAMA`.

##إنشاء CllamaServer

###إنشاء خادم باستخدام البلوبرينت

انقر بزر الماوس الأيمن في المخطط لإنشاء عقدة `إنشاء خادم كلاما في العالم`

<!-- صورة مطلوبة: لقطة شاشة تُظهر البحث بزر الفأرة الأيمن عن "إنشاء خادم Cllama" في المخطط وإنشاء العقدة -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_1.png)

###تهيئة معلمات الخادم

قم بإنشاء عقدة `Cllama Server Param` وقم بتكوين المعلمات الرئيسية:

* **النموذج**: مسار ملف النموذج (مطلوب)
* **المنفذ**: منفذ الخادم (0 يشير إلى التخصيص التلقائي)
* **المضيف**: عنوان الاستماع، افتراضيًا `127.0.0.1`
* **NGpuLayers**: عدد طبقات وحدة معالجة الرسومات (1- تعني استخدام وحدة معالجة الرسومات بالكامل)

<!-- صورة مطلوبة: لقطة شاشة توضح إنشاء عقدة FAIChatPlus_CllamaServerParam، وتعيين مسار النموذج والمنفذ وعدد طبقات وحدة معالجة الرسومات وغيرها من المعلمات -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_2.png)

###ربط أحداث رد الاتصال

ربط حدث رد الخادم Server:

* **عند البدء**: يتم التشغيل عند بدء تشغيل الخادم بنجاح
* **عند التوقف**: يتم تشغيله عندما يتوقف الخادم
* **عند الفشل**: يتم تشغيله عند فشل بدء تشغيل الخادم

<!-- صورة مطلوبة: عرض مخطط الربط لأحداث OnStartedListeners وOnStoppedListeners وOnFailedListeners -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_3.png)

###المخطط الكامل للإنشاء

الخطة الكاملة لإنشاء الخادم (Server) هي كما يلي:

<!-- تحتاج إلى صورة: توضح الصورة الكاملة لمخطط إنشاء الخادم (Server Creation Blueprint)، بما في ذلك إعدادات المعاملات (Parameters)، وعقدة الإنشاء (Creation Node)، وربط الاستدعاءات (Callback Binding) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_4.png)

بعد تشغيل المخطط الزمني، سيؤدي بدء تشغيل الخادم بنجاح إلى تشغيل حدث `On Started`.

<!-- تحتاج إلى صورة: توضح نتيجة تشغيل الـ Server بعد نجاح بدء التشغيل، مع عرض سجلات النجاح أو ناتج الشاشة -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_5.png) -->

##تفصيل معايير الخادم

تحتوي بنية `FAIChatPlus_CllamaServerParam` على المعايير التالية:

###المعلمات الشائعة

| البارامتر | النوع | القيمة الافتراضية | الشرح |
|-----|------|-------|------|
| النموذج | FString | - | مسار ملف النموذج (إلزامي) |
| المنفذ | int32 | 0 | منفذ الاستماع، 0 يعني التخصيص التلقائي |
| المضيف | سلسلة المحارف | 127.0.0.1 | عنوان الاستماع |
| NGpuLayers | int32 | -1 | عدد طبقات وحدة المعالجة الرسومية، -1 تعني الكل |
| bUseJinja | قيمة منطقية | خطأ | استخدام قالب Jinja |
| MMProj | FString | - | مسار ملف الإسقاط متعدد الوسائط |
| درجة الحرارة | float | 0.8 | درجة حرارة العينة |

###حجج الاستدلال

| المعلمة | النوع | القيمة الافتراضية | الشرح |
|-----|------|-------|------|
| حجم النص السياقي | عدد صحيح 32 بت | 4096 | حجم السياق |
| NPredict | int32 | -1 | عدد التوكنات المتوقعة، -1 يعني بلا حدود |
| سلاسل المعالجة | int32 | -1 | عدد سلاسل المعالجة لوحدة المعالجة المركزية، -1 تعني تلقائي |
| BatchSize | int32 | 2048 | حجم الدُفعة |

###معايير أخذ العينات

| المعلمة | النوع | القيمة الافتراضية | الشرح |
|-----|------|-------|------|
نص الترجمة باللغة العربية:

| أعلى_ك | عدد_صحيح_٣٢ | ٤٠ | أخذ_العينات_أعلى_ك
| TopP | عدد عائم | 0.9 | أخذ عينات Top-P |
| MinP | عائم | 0.1 | أخذ عينات Min-P |
| RepeatPenalty | عشري | 1.0 | عقوبة التكرار |

###معلمات الخادوم

| المعلمة | النوع | القيمة الافتراضية | الشرح |
|-----|------|-------|------|
| ApiKey | FString | - | مفتاح API (اختياري) |
| مهلة | int32 | 600 | وقت المهلة (بالثواني) |
| Parallel | int32 | 1 | عدد التسلسلات المتوازية |
| bNoWebUI | منطقي | خطأ | تعطيل واجهة المستخدم على الويب |
| bVerbose | منطقي | خطأ | سجل مفصّل |

##الدردشة باستخدام CllamaServer

###إنشاء طلب محادثة

بعد نجاح تشغيل السيرفر، يمكنك استخدام العقدة `Send CllamaServer Chat Request` لإرسال طلب الدردشة.

<!-- صورة مطلوبة: لقطة شاشة توضح البحث بزر الماوس الأيمن في المخطط عن "CllamaServer Chat Request" وإنشاء عقدة. -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_1.png)

###تهيئة خيارات الدردشة

إنشاء عقدة `CllamaServer Chat Request Options`، وتعيين عنوان BaseUrl ليصبح عنوان الخادم.

يمكن الحصول على معلومات الخادم من خلال العُقدة `Get Server Info By ID`.

<!-- صورة مطلوبة: توضح إنشاء عقدة FAIChatPlus_CllamaServerChatRequestOptions، واستخدام Get Http Address للحصول على عنوان الخادم وتعيينه إلى BaseUrl في المخطط -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_2.png)

###إنشاء رسائل

إنشاء مصفوفة الرسائل، وإضافة رسالة النظام ورسالة المستخدم.

<!-- تحتاج إلى صورة: توضح مخطط إنشاء مصفوفة الرسائل، التي تحتوي على رسالة النظام (تعيين دور المساعد) ورسالة المستخدم (سؤال المستخدم) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_3.png)

###ربط ردود الافعال لمعالجة الاستجابة

اربط حدث `On Message` أو `On Message Finished` لاستقبال استجابة النموذج.

<!-- صورة مطلوبة: عرض مخطط يوضح ربط أحداث OnMessageListeners وطباعة الرسائل في الشاشة عند الاستدعاء -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_4.png)

###الخطة الكاملة للمحادثة

المخطط الكامل للمحادثة هو كما يلي:

<!-- تحتاج إلى صورة: تعرض مخطط المحادثة الكامل، بما في ذلك إنشاء خادم، وانتظار بدء التشغيل، وإرسال طلب المحادثة، ومعالجة الاستجابة بالكامل -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_5.png)

###نتيجة التشغيل

تشغيل المخطط، ستظهر الرسالة التي يعيدها النموذج على الشاشة.

<!-- حاجة لصورة: عرض نتائج تشغيل المحادثة، تُظهر الشاشة محتوى الرد الذي أعاده النموذج -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_6.png) -->

##إدارة الخادم

###احصل على معلومات الخادم

استخدم عقدة `Get Server Info` للحصول على تفاصيل الخادم.

<!-- صورة مطلوبة: تُظهر مخططًا لاستخدام العقدة Get Server Info لاسترداد FAIChatPlus_CllamaServerInfo، ثم تفكيك الحقول لعرضها -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_info_1.png)

معلومات الخادم تتضمن المعلومات التالية:
* **ServerID**: معرف الخادم الفريد
* **المضيف**: عنوان الاستماع
* **المنفذ (Port)**: منفذ الاستماع
* **العنوان**: العنوان الكامل (host:port)
* **HttpAddress**: عنوان HTTP (http://host:port)
* **bIsRunning**: هل يعمل حاليًا
* **بارام**: معلمات الخادم

###إيقاف الخادم

استخدم العقدة `Stop Server By ID` لإيقاف الخادم الحالي.

<!-- صورة مطلوبة: تُظهر مخططًا لعقدة استدعاء خادم Stop Cllama -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_stop_1.png)

###الدوال الإدارية الثابتة

يوفر AIChatPlus مجموعة من الوظائف الثابتة لإدارة جميع الخوادم Server:

| الوظيفة | الشرح |
|-----|------|
| `هل الخادم صالح (ثابت)` | التحقق من صلاحية الخادم |
| هل يعمل السيرفر (ثابت) | التحقق مما إذا كان السيرفر يعمل |
إيقاف الخادم بواسطة المعرف
| `إيقاف جميع الخوادم` | توقيف جميع السيرفرات |
| `الحصول على معلومات الخادم بواسطة المعرف` | الحصول على معلومات الخادم من خلال المعرف |
| `الحصول على كافة معرفات الخادم` | جلب جميع معرفات الخادم |
| `Get Server By ID` | الحصول على مثيل الخادم عبر المعرف |

<!-- تحتاج إلى صورة: مثال على مخطط يوضح استخدام وظائف الإدارة الثابتة مثل "Get All Server IDs" و "Stop All Servers" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_static_1.png)

##دعم متعدد الوسائط

يدعم CllamaServer نماذج متعددة الوسائط مثل Moondream وQwen2-VL وغيرها.

###ضبط المعلمات متعددة الوسائط

في معلمة Server، قم بتعيين `MMProj` (مسار ملف الإسقاط متعدد الوسائط):

<!-- صورة مطلوبة: توضح مخطط الإعداد الخاص بـ Model و MMProj في Server Param -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_1.png)

###إرسال رسالة صورة

إضافة صورة في الرسائل:

<!-- صورة مطلوبة: عرض مخطط يوضح قراءة ملف الصورة، وإنشاء رسالة تحتوي على الصورة، وإرسال الطلب عبر CllamaServer -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_2.png)

<!-- ### نتائج التشغیل -->

<!-- تحتاج إلى صورة: عرض نتائج تشغيل التعرف على الصور، حيث تظهر الشاشة وصف النموذج لمحتوى الصورة -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_3.png) -->

## Tool Calling

يدعم CllamaServer خاصية Tool Calling (استدعاء الدوال)، حيث يكون استخدامها مشابهًا لـ OpenAI.

للحصول على تفاصيل الاستخدام، يرجى الرجوع إلى [Tool Call](ue-插件-AIChatPlus-Usage-Blueprint-ToolCall.md)مستند.

عند استخدام CllamaServer لإجراء مكالمة الأداة (Tool Call)، تحتاج إلى:
1. ضع `bUseJinja = true` في معاملات الـ Server
2. تعريف الأدوات في حقل Tools ضمن خيارات الدردشة (Chat Options)

<!-- صورة مطلوبة: توضح المخطط الكامل لأداة CllamaServer Tool Call، بما في ذلك إعداد bUseJinja=true وتعريفات الأدوات Tools -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_tool_1.png)

##محرر إدارة الخادم

يوفر AIChatPlus في أدوات المحرر واجهة رسومية لإدارة CllamaServer، مما يسهل إنشاء ومراقبة وإدارة عدة خواديم (Servers) بشكل ملائم.

افتح أداة المحرر: `Tools -> AIChatPlus -> AIChat`، ثم افتح علامة تبويب مدير خادم Cllama.

<!-- صورة مطلوبة: لقطة شاشة لواجهة إدارة CllamaServer في المحرر، تُظهر قائمة الخوادم، زر الإنشاء، معلومات الحالة، وغيرها -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_editor_1.png)

في المحرّر يمكنك:
* إنشاء خادم جديد
* عرض حالة الخادم قيد التشغيل
* إيقاف الخادم المحدد
* تكوين معلمات الخادم
* سيتم حفظ تكوين السيرفر تلقائيًا

<!-- صورة مطلوبة: توضح واجهة إنشاء خادم (Server) جديد في المحرر، مع عرض لوحة تكوين المعلمات -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_editor_2.png)

##العلاقة مع واجهات برمجة التطبيقات الأخرى

نظرًا لأن CllamaServer متوافق مع صيغة واجهة برمجة التطبيقات (API) الخاصة بـ OpenAI، يمكنك أيضًا استخدام عقدة Chat Request من OpenAI للتواصل مع CllamaServer، فقط قم بتعيين `BaseUrl` إلى عنوان CllamaServer.

<!-- صورة مطلوبة: عرض مثال على مخطط يستخدم عقدة OpenAI Chat Request، ولكن مع تعيين BaseUrl إلى عنوان CllamaServer -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_openai_1.png) -->

--8<-- "footer_ar.md"


> هذه المشاركة مترجمة باستخدام ChatGPT، يُرجى تقديم [**ملاحظات**](https://github.com/disenone/wiki_blog/issues/new)أشر إلى أي نقص ملحوظ. 
