---
layout: post
title: Get Started
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
description: Get Started
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 编辑器篇 - Get Started" />

#النص المطلوب ترجمته هو: البدء - فصل المحرر

##أداة محادثة المحرر

يمكن فتح أداة تحرير الدردشة المقدمة من قبل البرنامج الإضافي AIChatPlus -> AIChat عند الانتقال إلى Tools في شريط القوائم.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


يدعم الأداة إنتاج النصوص، ومحادثات النصوص، وإنشاء الصور، وتحليل الصور.

واجهة الأدوات تقريبًا كالتالي:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

##الرئيسية الوظائف

"النموذج الكبير للعمل بدون اتصال: يدعم تنفيذ النماذج الكبيرة محليًا عبر دمج مكتبة llama.cpp."

**الدردشة النصية**: انقر على زر `New Chat` في الزاوية السفلي اليسرى لإنشاء جلسة دردشة نصية جديدة.

**إنشاء صورة**: انقر فوق زر `New Image Chat` في الزاوية السفلي اليسرى، لبدء جلسة إنشاء صورة جديدة.

**تحليل الصور**: يدعم بعض خدمات الدردشة في `New Chat` إرسال الصور، مثل Claude، Google Gemini. يمكنك تحميل الصور التي ترغب في إرسالها عن طريق النقر على الزر 🖼️ أو 🎨 أعلى مربع الإدخال.

معالجة الصوت: توفير الأداة قراءة ملفات الصوت (.wav) ووظيفة التسجيل، يمكن استخدام الصوت المحصل عليه للتحدث مع الذكاء الاصطناعي.

تغيير دور المحادثة الحالي: يمكنك تعيين دور المرسل الحالي من خلال قائمة التحديد أعلى نافذة المحادثة، يمكنك تحديد شخصيات مختلفة لتعديل المحادثة مع الذكاء الاصطناعي.

امسح المحادثة: يمكنك مسح تاريخ رسائل الدردشة الحالية عن طريق النقر على علامة ❌ في أعلى المربع.

**نموذج حوار**: يحتوي على مئات النماذج المضمنة لإعدادات الحوار، مما يسهل معالجة المشاكل الشائعة.

**الإعدادات العامة**: انقر فوق زر `Setting` في الزاوية السفلية اليسرى لفتح نافذة الإعدادات العامة. يمكنك تعيين الدردشة النصية الافتراضية، وخدمة API لتوليد الصور، وتحديد معلمات كل نوع من خدمات API بشكل محدد. سيتم حفظ الإعدادات تلقائيًا في مسار المشروع `$(ProjectFolder)/Saved/AIChatPlusEditor`.

**إعدادات الحوار**: انقر على زر الإعدادات في أعلى صندوق الدردشة لفتح نافذة إعدادات الحوار الحالي. يدعم تعديل اسم الحوار، تعديل الخدمة API المستخدمة في الحوار، ويدعم إعداد معلمات ال API الخاصة بكل حوار على حدة. ستحفظ إعدادات الحوار تلقائيًا في `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

تعديل محتوى المحادثة: عند تحويل الماوس فوق محتوى المحادثة، سيظهر زر الإعدادات لهذا المحتوى، يدعم إعادة إنشاء المحتوى، وتعديله، ونسخه، وحذفه، وإعادة إنشاء المحتوى في الأسفل (بالنسبة لمحتوى الشخصية المستخدم).

**عارض الصور**: بالنسبة لإنشاء الصور، يمكن النقر على الصورة لفتح نافذة عرض الصور (ImageViewer)، ودعم حفظ الصور كـ PNG / UE Texture، ويمكن عرض الـ Texture مباشرة في متصفح المحتوى (Content Browser)، مما يجعل من السهل استخدام الصور في المحرر. بالإضافة إلى ذلك، يتم دعم حذف الصور وإعادة إنشائها والاستمرار في إنشاء المزيد من الصور وغير ذلك. بالنسبة لمحرر النوافذ، يتم دعم نسخ الصور أيضًا، ويمكن نسخ الصور مباشرة إلى الحافظة لسهولة الاستخدام. يتم حفظ الصور المولدة تلقائيًا أيضًا في مجلد كل جلسة، والمسار العام هو `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

الإعدادات العامة:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

إعدادات المحادثة:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

تعديل محتوى المحادثة:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

عارض الصور:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

استخدام نماذج كبيرة غير متصلة

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

قالب الحوار

![system template](assets/img/2024-ue-aichatplus/system_template.png)

##استخدام أداة المحرر لنموذج غير متصل بالإنترنت Cllama(llama.cpp)

سأشرح لك كيفية استخدام نموذج الإنترنت llama.cpp في أداة تحرير AIChatPlus.

أولاً، قم بتنزيل النموذج الخارجي من موقع HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

وضع النموذج في مجلد معين، مثل وضعه في دليل المشروع اللعبة Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

افتح أداة تحرير AIChatPlus: Tools -> AIChatPlus -> AIChat، ثم أنشئ جلسة دردشة جديدة وافتح صفحة إعدادات الجلسة.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

قم بتعيين Api على Cllama، وفتح إعدادات Api المخصصة، وأضف مسارات بحث النماذج، ثم اختر النموذج

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

البدء في الدردشة!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

##استخدام أداة المحرر لمعالجة الصور باستخدام نموذج Cllama(llama.cpp) في وضع عدم الاتصال بالإنترنت.

قم بتحميل نموذج MobileVLM_V2-1.7B-GGUF من موقع HuggingFace وضعه في المجلد المسمى Content/LLAMA: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)و [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but there is no text to translate.

ضبط نموذج الجلسة:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

بدء الدردشة عبر إرسال صورة

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

##يستخدم المحرر محادثة OpenAI

افتح أداة الدردشة Tools -> AIChatPlus -> AIChat، وأنشئ جلسة دردشة جديدة New Chat، واضبط الجلسة ChatApi على OpenAI، وحدد معلمات الواجهة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

بدء المحادثة:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

قم بتبديل النموذج إلى gpt-4o / gpt-4o-mini، يمكنك استخدام ميزة الرؤية من OpenAI لتحليل الصور.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

##تستخدم المحررات OpenAI لمعالجة الصور (إنشاء/تعديل/تحويل)

أنشئ دردشة صور جديدة في أداة الدردشة، غيّر إعدادات الدردشة إلى OpenAI، وضبط البارامترات.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

إنشاء صورة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

قم بتعديل الصورة، وقم بتغيير نوع الحوار الخاص بالصورة إلى "تعديل"، ثم قم برفع صورتين، إحداهما الصورة الأصلية والأخرى mask حيث يتمثل المكان الذي يجب تعديله عندما تكون المنطقة شفافة (قناة ألفا تساوي 0).

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

قم بتعديل نوع الدردشة الصورية إلى "تغيير" وارفع صورة، ستقوم شركة OpenAI بإرجاع نسخة معدلة من الصورة الأصلية.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

##المحرر يستخدم Azure

إنشاء محادثة جديدة (New Chat)، قم بتغيير ChatApi إلى Azure، وقم بضبط معلمات Api الخاصة بـ Azure

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

البدء في الدردشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

##استخدام محرر Azure لإنشاء الصور

قم بإنشاء جلسة دردشة الصور الجديدة (New Image Chat)، وقم بتغيير ChatApi إلى Azure، وقم بضبط معلمات Azure API. يرجى الملاحظة، إذا كانت النموذج dall-e-2، يجب تعيين معلمات الجودة (Quality) والنمط (Stype) كـ not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

ابدأ الدردشة لإنشاء الصورة على Azure

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

##يستخدم المحرر Claude للدردشة وتحليل الصور.

إنشاء دردشة جديدة، قم بتغيير ChatApi إلى Claude، وقم بتعيين معلمات Api لـ Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

الرجاء إعادة صياغة العبارة السابقة في الصندوق أدناه.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

##يستخدم المحرر Ollama للدردشة وتحليل الصور.

إنشاء محادثة جديدة (New Chat)، وتغيير ChatApi إلى Ollama، وضبط معلمات Ollama الخاصة. إذا كان الدردشة نصية، فحدد النموذج كنموذج نصي، مثل llama3.1؛ وإذا كان هناك حاجة لمعالجة الصور، فحدد النموذج كنموذج يدعم الرؤية، مثل moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

بدء المحادثة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###المحرر يستخدم Gemini

إنشاء محادثة جديدة، قم بتغيير ChatApi إلى Gemini، وضبط معلمات Api الخاصة بـGemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

البدء في المحادثة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

##استخدم Gemini المحرر لإرسال الصوت.

اختيار قراءة الصوت من الملف / اختيار قراءة الصوت من الأصول / اختيار تسجيل الصوت من الميكروفون، لإنشاء الصوت الذي يجب إرساله

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

البدء في الدردشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

##المحرر يستخدم Deepseek

إنشاء محادثة جديدة (New Chat)، قم بتغيير ChatApi إلى OpenAi، وقم بضبط معلمات Api لـ Deepseek. أضف نماذج مرشحة جديدة تسمى deepseek-chat، وضبط النموذج كـ deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

بدء المحادثة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

--8<-- "footer_ar.md"


> هذا المنشور تمت ترجمته باستخدام ChatGPT، يُرجى تقديم [**ردود فعل**](https://github.com/disenone/wiki_blog/issues/new)يرجى إشارة أي غياب. 
