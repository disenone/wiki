---
layout: post
title: Tool Call
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
- Tool Call
- Function Calling
description: Tool Call
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Tool Call" />

#الرؤية - استدعاء الأداة

يُعرف استدعاء الأداة أيضًا باستدعاء الوظيفة، وهو قدرة النموذج الكبير على تحديد ما إذا كان يحتاج إلى استدعاء أداة/وظيفة خارجية للحصول على معلومات أو تنفيذ عملية بناءً على محتوى الحوار. سيقوم النموذج بإرجاع اسم الوظيفة المطلوبة ومعاملاتها، ثم يقوم المطور بتنفيذ الاستدعاء الفعلي وإعادة النتائج إلى النموذج لمتابعة الحوار.

يدعم AIChatPlus ميزات Tool Call في المنصات التالية:

* OpenAI
* Claude
* Gemini
* Ollama
* CllamaServer (خادم llama.cpp)

##المفاهيم الأساسية

###تعريف الأداة

يتضمن تعريف الأداة الحقول الأساسية التالية:

**النوع**: نوع الأداة، يدعم حاليًا فقط ``Function``
* **الاسم**: اسم الدالة، يجب أن يتكون من الأحرف a-z أو A-Z أو الأرقام 0-9 أو الشرطة السفلية أو الواصلة، بحد أقصى 64 حرفًا
* **الوصف**: وصف الدالة، النموذج سيحدد متى يتم استدعاء هذه الدالة بناءً على هذا الوصف
* **الخصائص**: قائمة معاملات الدالة، حيث يحتوي كل معامل على خصائص مثل الاسم، والوصف، والنوع، والإلزامية

###سير عملية استدعاء الأداة

التدفق الكامل لـ Tool Call هو كما يلي:

1. **إرسال الطلب**: إرسال طلب محادثة إلى النموذج يتضمن تعريفات الأدوات
2. **حكم النموذج**: يحدد النموذج ما إذا كان بحاجة إلى استدعاء أداة بناءً على محتوى الحوار
3. **استدعاءات الأدوات**: في حالة الحاجة إلى الاستدعاء، يقوم النموذج بإرجاع اسم الدالة المعنية والمعاملات المطلوبة
4. **تنفيذ الوظيفة**: يقوم المطور بتنفيذ استدعاء الوظيفة الفعلي بناءً على المعلومات المرتجعة
5. **إرجاع النتائج**: يتم إرسال نتيجة تنفيذ الدالة كرسالة جديدة إلى النموذج
6. **مواصلة الحوار**: يقوم النموذج بإنشاء الرد النهائي بناءً على نتيجة الوظيفة

##مثال على استدعاء أداة OpenAI

فيما يلي مثال على استخدام OpenAI لتوضيح كيفية استخدام ميزة Tool Call.

###1. تعريف الأدوات

أولاً، قم بإنشاء تعريف الأداة. في هذا المثال، نعرف وظيفة تُدعى `get_delivery_date` للحصول على موعد وصول الطرد.

<!-- صورة مطلوبة: توضح إنشاء عقدة FAIChatPlus_ChatRequestTool، مع ضبط Type=Function، Name="get_current_weather"، Description="احصل على الطقس الحالي في موقع معين" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_1.png)

###2. تحديد معلمات الأداة

إضافة خصائص (Properties) للأداة (Tool). في هذا المثال، تتم إضافة معلمة `order_id` من نوع `string`، ويتم تعيينها كحقل إلزامي.

<!-- صورة مطلوبة: توضح إنشاء عقدة FAIChatPlus_ChatRequestToolProperty، وتعيين Name="location"، وDescription="المدينة والولاية، مثلاً سان فرانسيسكو، كاليفورنيا"، وType="string"، وRequired=true، ثم توصيلها بحقل Properties في الأداة عبر Make Array -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_2.png)

###3. خيارات التهيئة

إنشاء عقدة `OpenAI Chat Request Options`، وضبط مفتاح API والنموذج، ثم توصيل مصفوفة الأدوات بخيارات الطلب.

<!-- الصورة المطلوبة: توضح إنشاء عقدة OpenAI Chat Request Options، وتعيين ApiKey، Model="gpt-4o-mini"، مع ربط الأداة السابقة بحقل Tools عبر Make Array -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_3.png)

###4. إنشاء الرسائل

إنشاء رسالة مستخدم للاستفسار عن مشاكل متعلقة بطرود البريد السريع.

<!-- تحتاج صورة: توضح إنشاء مصفوفة Messages، إضافة رسالة مستخدم، تعيين المحتوى إلى "ما هو حال الطقس في بوسطن اليوم؟" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_4.png)

###5. إرسال الطلب ومعالجة نداء الأداة

إنشاء عقدة `Send OpenAI Chat Request In World`، وربطها بحدث `On Message Finished`. ضمن رد فعل الحدث، احصل على مجموعة `ToolCalls` من الحمولة.

عندما يقرر النموذج استدعاء أداة، فإن مصفوفة ToolCalls لا تكون فارغة. قم باجتياز المصفوفة للحصول على معلومات عن كل استدعاء أداة:

* **الرمز**: المعرّف الفريد لـ "طلب الأداة"
* **اسم الدالة**: اسم الدالة المراد استدعاؤها
* **FunctionArguments**: وسيطات الدالة (بتنسيق سلسلة JSON)

<!-- صورة مطلوبة: عرض مخطط طلب الإرسال الكامل، إنشاء عقدة Send OpenAI Chat Request In World، توصيل الخيارات والرسائل، ربط حدث On Message Finished، في ردود الافعال للحدث استخدم عقدة Break للحصول على ToolCalls من الحمولة -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_5.png)

<!-- تحتاج إلى صورة: توضح مخططًا لاجتياز مصفوفة ToolCalls باستخدام حلقة For Each Loop، واستخدام عُقَد Break لكل عنصر لاستخراج الحقول Id و FunctionName و FunctionArguments، ثم طباعتها بشكل مخرجات -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_6.png) -->

###6. تنفيذ الدالة وإرجاع النتيجة

قم بتنفيذ المنطق المطابق للدالة بناءً على FunctionName (في هذا المثال يتم محاكاة الحصول على وقت وصول الطرد البريدي)، ثم إرجاع النتيجة كرسالة من نوع ToolCallResult إلى النموذج.

لإنشاء رسالة جديدة، يجب تعيين:

* **الدور**: تم تعيينه على `أداة`
* **المحتوى**: نتيجة تنفيذ الوظيفة
* **نتائج نداء الأداة**: أضف `FAIChatPlus_ChatRequestToolCallResult`، وحدد المعرف (باستخدام معرف نداء الأداة السابق)، واسم الوظيفة ونتيجة الوظيفة

<!-- صورة مطلوبة: تعرض مخططًا لإنشاء رسالة دور الأداة، إنشاء رسالة جديدة، Role=Tool، يتم تعيين المحتوى على بيانات الطقس المحاكاة مثل '{"temperature": "22", "unit": "celsius", "description": "Sunny"}'، وإضافة معلومات النتائج المقابلة في ToolCallResults -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_7.png)

###7. متابعة المحادثة

إضافة رسالة تحتوي على نتيجة أداة (ToolCallResult) إلى سجل الرسائل، ثم إعادة إرسال الطلب. سيقوم النموذج بإنشاء رد نهائي بلغة طبيعية بناءً على النتائج التي تم إرجاعها من الوظيفة.

<!-- صورة مطلوبة: عرض المخطط الكامل للطلب الثاني، حيث يتم دمج رسالة المستخدم الأصلية ورسالة المساعد التي يُرجعها النموذج (بما في ذلك ToolCalls) ورسالة نتائج الأداة في مجموعة رسائل جديدة، ثم يتم استدعاء "إرسال طلب محادثة OpenAI في العالم" مرة أخرى -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_8.png)

### 9. المخطط الكامل

<!-- المخطط الكامل لـ Tool Call يبدو بهذا الشكل: -->

<!-- تحتاج إلى صورة: توضح مخططًا كاملًا لسير عملية استدعاء الأداة، يتضمن تعريف الأداة، الطلب الأول، معالجة استدعاء الأداة، والطلب الثاني في سير العمل الكامل -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_9.png) -->

### 10. نتائج التشغيل

<!-- تشغيل المخطط، يمكنك رؤية النموذج يعيد ردود لغة طبيعية تحتوي على معلومات الطقس. -->

<!-- صورة مطلوبة: لقطة شاشة توضح نتيجة التشغيل، تظهر على الشاشة الرد النهائي للنموذج، على شاكلة "الطقس الحالي في بوسطن مشمس بدرجة حرارة 22°C." -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_10.png) -->

##استخدامات متقدمة

###أدوات متعددة

يمكن تعريف أدوات متعددة في الوقت نفسه، وسيقوم النموذج باختيار أي وظيفة أو وظائف سيتم استدعاؤها حسب الحاجة.

<!-- صورة مطلوبة: توضح مخططًا لتعريف عدة أدوات، مثل تعريف أداة get_current_weather وأداة get_stock_price في نفس الوقت، ثم دمجهما في مصفوفة أدوات باستخدام Make Array -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_multi_tools.png)

###أنواع المعاملات المعقدة

يدعم مُعامل الأداة أنواعًا متعددة، ويمكن إضافة تعريفات مُعاملات أكثر تعقيدًا مثل النوع المُعدَّد عبر حقل `ExtraJsonString` أو `ExtraJsonObject`، على سبيل المثال:

```json
{"enum": ["Beijing", "HongKong"]}
```

<!-- صورة مطلوبة: تُظهر مخططًا لاستخدام ExtraJsonString لتعيين معلمات التعداد، في حقل ExtraJsonString الخاص بعقدة Property، قم بإدخال '{"enum": ["celsius", "fahrenheit"]}' -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_extra_json.png)

###منصات أخرى

يتم استخدام Tool Call لـ Claude و Gemini و Ollama و CllamaServer بشكل مشابه لـ OpenAI، كل ما عليك هو استبدال عقدة Request و Options المقابلة. الهياكل الأساسية للبيانات لكل منصة (مثل `FAIChatPlus_ChatRequestTool`، `FAIChatPlus_ChatResponseToolCall` وما إلى ذلك) هي عالمية.

--8<-- "footer_ar.md"


> هذا المنشور تمت ترجمته باستخدام ChatGPT، يُرجى تقديم ملاحظاتكم عبر [**نموذج الملاحظات**](https://github.com/disenone/wiki_blog/issues/new)أشر إلى أي نقص ملحوظ. 
