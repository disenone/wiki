---
layout: post
title: 'ترجمة هذا النص إلى اللغة العربية:


  وثائق شرح UE AIChatPlus المُتوصلة'
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
description: وثائق شرح ملحق UE AIChatPlus
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#وثائق شرح ملحق UE AIChatPlus

##المستودع العام

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##الحصول على المكون الإضافي

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##مقدمة عن الإضافات

هذا الإضافة تدعم UE5.2+‎.

UE.AIChatPlus هو إضافة لـ Unreal Engine تمكّن التواصل مع مجموعة متنوعة من خدمات المحادثات الذكية GPT AI. حالياً، يدعم الإضافة خدمات مثل OpenAI (ChatGPT، DALL-E)، Azure OpenAI (ChatGPT، DALL-E)، Claude، Google Gemini، Ollama، وllama.cpp للتشغيل المحلي. سيتم دعم مزيد من مقدمي الخدمات في المستقبل. تستند عملية التنفيذ على طلبات REST غير المتزامنة، مما يضمن أداءً فعّالاً ويسهل توصيل مطوري الـUE بهذه الخدمات الذكية للمحادثات.

ويشتمل UE.AIChatPlus أيضًا على أداة محرر يمكن استخدامها مباشرة في المحرر لاستخدام خدمات الدردشة الذكية هذه لإنشاء نصوص وصور، وتحليل الصور وما إلى ذلك.

##تعليمات الاستخدام

###أداة دردشة المحرر

يُمكن فتح محرر الدردشة الذي يوفره البرنامج الإضافي عن طريق الانتقال إلى Tools -> AIChatPlus -> AIChat في شريط القوائم.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


يدعم الأداة إنشاء نصوص، ومحادثة نصية، وتوليد صور، وتحليل الصور.

ترجمة النص إلى اللغة العربية:

واجهة الأدوات تعتمد تقريباً على الشكل التالي:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####الرئيسية

نموذج كبير للتشغيل دون اتصال: يتم دمج مكتبة llama.cpp لدعم تنفيذ النماذج الكبيرة محلياً.

الدردشة النصية: انقر فوق زر "New Chat" في الزاوية السفلى اليسرى لإنشاء محادثة نصية جديدة.

إنشاء الصور: انقر فوق زر "New Image Chat" في الزاوية السفلي اليسار لإنشاء جلسة جديدة لإنشاء الصور.

تحليل الصور: تدعم بعض خدمات الدردشة في `New Chat` إرسال الصور، مثل Claude و Google Gemini. يمكنك تحميل الصور التي تريد إرسالها ببساطة عن طريق النقر على الزر 🖼️ أو 🎨 الموجود أعلى مربع الإدخال.

دعم الخطط الزرقاء: دعم إنشاء طلبات API للخطط الزرقاء، لإتمام المحادثات النصية وإنشاء الصور وما إلى ذلك.

قم بتعيين شخصية المحادثة الحالية: يمكنك تعيين شخصية النص الذي ترسله حاليًا عبر القائمة المنسدلة في أعلى مربع الدردشة، حيث يمكنك محاكاة شخصيات مختلفة لضبط المحادثة بالذكاء الاصطناعي.

أفرغ الدردشة: يمكنك استخدام زر ❌ في أعلى نافذة الدردشة لمسح تاريخ الرسائل في الدردشة الحالية.

تم ترجمة النص إلى اللغة العربية:

* قالب المحادثة: يحتوي على مئات من القوالب الجاهزة للمحادثات، مما يسهل تناول المشكلات الشائعة.

الإعدادات العامة: بالنقر على زر "Setting" في الزاوية السفلي اليسارية، يمكنك فتح نافذة الإعدادات العامة. يمكنك تعيين الدردشة النصية الافتراضية، وخدمة توليد الصور البرمجية، وتحديد معلمات كل خدمة برمجية بشكل محدد. ستقوم الإعدادات بالحفظ تلقائياً في مسار المشروع "$(ProjectFolder)/Saved/AIChatPlusEditor" sub>.

إعدادات المحادثة: انقر فوق زر الإعدادات في أعلى نافذة الدردشة لفتح نافذة إعدادات الجلسة الحالية. يدعم تعديل اسم الجلسة، وتعديل خدمات واجهة برمجة التطبيقات المستخدمة في الجلسة، ودعم تعيين معلمات محددة لاستخدام واجهة برمجة التطبيقات في كل جلسة بشكل مستقل. يتم حفظ إعدادات الجلسة تلقائيًا في `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

تعديل محتوى المحادثة: عند توقف الماوس فوق محتوى المحادثة، سيظهر زر إعدادات المحتوى الفردي الذي يتيح إعادة إنشاء المحتوى، تعديل المحتوى، نسخ المحتوى، حذف المحتوى، إعادة إنشاء المحتوى في الجزء السفلي (بالنسبة للمحتوى المرتبط بالمستخدم)

عرض الصور: بالنسبة لإنشاء الصور، عند النقر فوق الصورة سيتم فتح نافذة عرض الصور (ImageViewer)، والتي تدعم حفظ الصور كملف PNG/UE Texture، ويمكن عرض الـTexture مباشرة في مستعرض المحتوى (Content Browser)، مما يسهل استخدام الصور في المحرر. بالإضافة إلى ذلك، يتم دعم حذف الصور وإعادة إنشاء الصور ومواصلة إنشاء المزيد من الصور وغيرها من الوظائف. بالنسبة لمحرر Windows، يتم دعم نسخ الصور أيضًا، بحيث يمكن نسخ الصور مباشرة إلى الحافظة لسهولة الاستخدام. ستحفظ الصور المُنشأة خلال الجلسة تلقائيًا في مجلد الجلسة الفردية، وعادة ما يكون المسار `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

السلام عليكم

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

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

###المقدمة للكود الأساسي

في الوقت الحالي، ينقسم الإضافة إلى الوحدات التالية:

* AIChatPlusCommon: وحدة التشغيل (Runtime)، مسؤولة عن معالجة طلبات إرسال وتحليل محتوى ردود API الذكاء الاصطناعي المختلفة.

AIChatPlusEditor: وحدة المحرر (Editor)، مسؤولة عن تنفيذ أداة دردشة الذكاء الصناعي في المحرر.

AIChatPlusCllama: "Runtime" هو الوحدة التشغيلية، المسؤولة عن تغليف واجهة ومعلمات llama.cpp ، وتنفيذ نماذج كبيرة في العمل خارج الاتصال.

Thirdparty/LLAMACpp: تشغيل وحدة خارجية في الوقت الذي يتم تحميله llama.cpp وملفات الرأس التي تم دمجها.

يتولى UClass المسؤول عن إرسال الطلبات بشكل محدد هو FAIChatPlus_xxxChatRequest، كل خدمة API لها UClass خاص بالطلب. يتم الحصول على ردود الطلبات عبر UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase UClass، ويكفي تسجيل الوكيل المناسب.

قبل إرسال الطلب، يجب تعيين معلمات ورسالة الAPI بشكل صحيح، يتم تعيين هذه القيم من خلال FAIChatPlus_xxxChatRequestBody. ويتم تحليل المحتوى المحدد من الرد في FAIChatPlus_xxxChatResponseBody، بحيث يمكن الحصول على ResponseBody عند استقبال الاستدعاء عبر واجهة محددة.

يمكن الحصول على مزيد من تفاصيل شفرة المصدر في متجر UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###استخدام أداة المحرر للنموذج الغير متصل Cllama (llama.cpp)

يرجى استخدام النموذج الخارجي llama.cpp في أداة تحرير AIChatPlus.

تفضل، الرجاء تحميل النموذج اللاحق من موقع HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

وضع النموذج في مجلد معين، مثل وضعه في دليل مشروع اللعبة باسم Content/LLAMA

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

افتح أداة تحرير AIChatPlus: Tools -> AIChatPlus -> AIChat، أنشئ جلسة دردشة جديدة وافتح صفحة إعدادات الجلسة

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

قم بتعيين Api إلى Cllama، وقم بتمكين Custom Api Settings، وأضف مسار البحث عن النماذج، ثم اختر النموذج.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

ابدأ الدردشة الآن!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###استخدام أداة المحرر لمعالجة الصور باستخدام النموذج الغير متصل Cllama(llama.cpp)

قم بتنزيل النموذج الغير متصل MobileVLM_V2-1.7B-GGUF من موقع HuggingFace وضعه في دليل Content/LLAMA تحت اسم [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)و [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but I can't provide a translation for "。".

قم بتعيين نموذج الدردشة:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

بدء الدردشة عند إرسال الصور.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###يستخدم الكود نموذجًا غير متصلًا بالإنترنت Cllama(llama.cpp)

أدناه كيفية استخدام النموذج الحالي llama.cpp في الشفرة.

أولاً ، يجب تنزيل ملف النموذج إلى مجلد Content/LLAMA.

قم بتعديل الشيفرة لإضافة أمر جديد، وقم بإرسال رسالة لنموذج الشبكة العصبية الخارجية داخل هذا الأمر.

```c++
#include "Common/AIChatPlus_Log.h"
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"

void AddTestCommand()
{
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("AIChatPlus.TestChat"),
		TEXT("Test Chat."),
		FConsoleCommandDelegate::CreateLambda([]()
		{
			if (!FModuleManager::GetModulePtr<FAIChatPlusCommon>(TEXT("AIChatPlusCommon"))) return;

			TWeakObjectPtr<UAIChatPlus_ChatHandlerBase> HandlerObject = UAIChatPlus_ChatHandlerBase::New();
			// Cllama
			FAIChatPlus_CllamaChatRequestOptions Options;
			Options.ModelPath.FilePath = FPaths::ProjectContentDir() / "LLAMA" / "qwen1.5-1_8b-chat-q8_0.gguf";
			Options.NumPredict = 400;
			Options.bStream = true;
			// Options.StopSequences.Emplace(TEXT("json"));
			auto RequestPtr = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(
				Options,
				{
					{"You are a chat bot", EAIChatPlus_ChatRole::System},
					{"who are you", EAIChatPlus_ChatRole::User}
				});

			HandlerObject->BindChatRequest(RequestPtr);
			const FName ApiName = TEnumTraits<EAIChatPlus_ChatApiProvider>::ToName(RequestPtr->GetApiProvider());

			HandlerObject->OnMessage.AddLambda([ApiName](const FString& Message)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] Message: [%s]"), *ApiName.ToString(), *Message);
			});
			HandlerObject->OnStarted.AddLambda([ApiName]()
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestStarted"), *ApiName.ToString());
			});
			HandlerObject->OnFailed.AddLambda([ApiName](const FAIChatPlus_ResponseErrorBase& InError)
			{
				UE_LOG(AIChatPlus_Internal, Error, TEXT("TestChat[%s] RequestFailed: %s "), *ApiName.ToString(), *InError.GetDescription());
			});
			HandlerObject->OnUpdated.AddLambda([ApiName](const FAIChatPlus_ResponseBodyBase& ResponseBody)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestUpdated"), *ApiName.ToString());
			});
			HandlerObject->OnFinished.AddLambda([ApiName](const FAIChatPlus_ResponseBodyBase& ResponseBody)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestFinished"), *ApiName.ToString());
			});

			RequestPtr->SendRequest();
		}),
		ECVF_Default
	);
}
```

بمجرد إعادة تجميع الشيفرة، يمكنك استخدام الأوامر في محرر الأوامر Cmd لعرض نتائج مخرجات النموذج الكبيرة في سجل الإخراج OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###استخدام النموذج غير المتصل llama.cpp في التصميم الأزرق

توضح هذه التعليمات كيفية استخدام نموذج البيانات دون اتصال llama.cpp في الرسوم التوضيحية.

في النموذج، انقر بزر الماوس الأيمن لإنشاء عقدة بعنوان `Send Cllama Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

أنشئ عقد Options وقم بتعيين `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf".`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

إنشاء رسائل، وإضافة رسالة نظام ورسالة مستخدم على التوالي

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

إنشاء Delegate لاستقبال معلومات إخراج النموذج وطباعتها على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

سيظهر النموذج الكامل للعمل البلوبرينت الخاص بك على الشاشة عند تشغيله، مما يسمح لك برؤية رسائل النموذج الكبيرة المطبوعة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###llama.cpp تستخدم وحدة المعالجة الرسومية

"خيارات طلب دردشة Cllama" تضيف المعلمة "Num Gpu Layer"، ويمكن تعيين حمولة gpu لملف llama.cpp كما في الصورة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

يمكن استخدام نُود الخريطة الزرقاء للتحقق مما إذا كان البيئة الحالية تدعم وحدة معالجة الرسوميات GPU والحصول على backends المدعومة في البيئة الحالية:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_2.png)

###معالجة ملفات النموذج داخل ملف .Pak بعد التجميع.

عندما تقوم بفتح ملف Pak بعد ضغطه، سيتم وضع جميع ملفات المشروع في ملف .Pak، بما في ذلك ملفات نموذج gguf للعمل دون اتصال.

نظرًا لعدم قدرة llama.cpp على دعم قراءة ملف .Pak مباشرة، فإنه من الضروري نسخ ملفات النماذج الغير متصلة من ملف .Pak إلى نظام الملفات.

AIChatPlus قدم وظيفة تسهل عملية نقل وتعامل ملفات النموذج في .Pak تلقائيًا، وتضعها في مجلد Saved.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

يمكنك أيضًا معالجة ملفات النموذج في .Pak بنفسك، الأمر الحاسم هو نسخ ومعالجة الملفات، حيث أن ملف llama.cpp غير قادر على قراءة .Pak بشكل صحيح.

## OpenAI

###يستخدم المحرر OpenAI للدردشة

افتح أداة الدردشة Tools -> AIChatPlus -> AIChat، وأنشئ جلسة دردشة جديدة New Chat، وقم بتعيين الجلسة ChatApi إلى OpenAI، وضبط معلمات الواجهة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

ابدأ الدردشة:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

قم بتبديل النموذج إلى gpt-4o / gpt-4o-mini ، يمكنك استخدام وظائف OpenAI لتحليل الصور البصرية.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###يستخدم المحرر OpenAI لمعالجة الصور (إنشاء/تعديل/تغيير)

إنشاء محادثة صور جديدة في أداة الدردشة، تعديل إعدادات المحادثة إلى OpenAI، وضبط البارامترات.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

إنشاء صورة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

قم بتعديل الصورة عن طريق تغيير نوع الدردشة Image Chat Type إلى Edit، ثم قم برفع صورتين، إحداهما الصورة الأصلية والأخرى mask حيث يجب أن تكون المناطق الشفافة (قناة alpha بقيمة 0) تمثل المناطق التي يجب تعديلها.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

تعديل صورة Image Chat Type إلى نوع Variation وتحميل صورة، سيقوم OpenAI بإرجاع تحويل للصورة الأصلية

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###استخدام النموذج الحواري OpenAI في الدردشة.

في الخطة، قم بالنقر باليمين لإنشاء نقطة "Send OpenAI Chat Request In World".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

أنشئُوا قسم Options، واضبطوا `Stream=true, Api Key="you api key from OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

إنشاء رسائل، وإضافة رسالة نظام ورسالة مستخدم بشكل منفصل

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

إنشاء الوكيل Delegate لاستقبال مخرجات النموذج وطباعتها على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

النص المترجم: الخطة الزرقاء الكاملة تبدو هكذا، قم بتشغيل الخطة الزرقاء لترى رسالة عودة النموذج الضخم المطبوع على شاشة اللعبة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###استخدام OpenAI لإنشاء صورة من التصميمات الأولية

أنشئ نقطة `Send OpenAI Image Request` في الرسم التخطيطي بالنقر بزر الماوس الأيمن، وقم بتعيين `In Prompt="فراشة جميلة"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

قم بإنشاء عقد Options، وقم بتعيين `Api Key="your api key from OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

* قم بربط حدث الصور واحتفظ بالصورة على القرص الثابت المحلي

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

يبدو الخطة الكاملة كما هو موضح هنا، بمجرد تشغيل الخطة، سترى الصورة تم حفظها في الموقع المحدد

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###المحرر يستخدم Azure

أنشئ دردشة جديدة (New Chat) ، قم بتغيير ChatApi إلى Azure، وحدد بارامترات Api ل Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

بدء الدردشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###استخدام Azure لإنشاء صورة في المحرر.

إنشاء جلسة صور جديدة (New Image Chat)، قم بتغيير ChatApi إلى Azure وضبط معلمات Api الخاصة بAzure. تنبيه: إذا كان النموذج dall-e-2، فيجب تعيين معلمات Quality وStype إلى not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

بدء المحادثة ، وجعل Azure ينشئ صورة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###استخدام تصميم Azure تحدث الرسائل

إنشاء الخطة الزرقاء كما يلي، ثم قم بتعيين خيارات Azure، انقر على تشغيل، وسترى رسائل المحادثة التي تعود من Azure تظهر على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###استخدام Azure لإنشاء الصور الشابه.

قم بإنشاء الخطة كما هو موضح، وحدد الخيارات في أزور، ثم اضغط تشغيل. إذا نجحت عملية إنشاء الصورة، ستظهر رسالة "Create Image Done" على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

وفقًا للإعدادات في الخريطة الزرقاء أعلاه، سيتم حفظ الصورة في المسار D:\Dwnloads\butterfly.png

## Claude

###استخدام المحرر Claude للدردشة وتحليل الصور.

أنشئ محادثة جديدة (New Chat)، غير ChatApi إلى Claude، وقم بضبط معلمات Api الخاصة بـ Claude

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

ابدأ المحادثة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###استخدام السيد كلود للدردشة وتحليل الصور.

في الخريطة الزرقاء، قم بالنقر بالزر الأيمن وإنشاء نقطة `Send Claude Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

إنشاء nتعيين API Key="your api key from Clude", Stream=true, و Max Output Tokens=1024 للعقد Options.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

إنشاء رسائل، إنشاء Texture2D من ملف، وإنشاء AIChatPlusTexture من Texture2D، ثم إضافة AIChatPlusTexture إلى الرسالة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

ابتكر حدثًا مشابهًا للبرنامج التعليمي أعلاه وقم بطباعة المعلومات على شاشة اللعب.

النّسخة الكاملة من الخطة تبدو كما هو موضح هنا، قم بتشغيل الخطة، وستشاهد رسالة تظهر على الشاشة تطبع نموذجًا كبيرًا.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###الحصول على Ollama

يمكنك الحصول على حزمة التثبيت محليًا من موقع Ollama الرسمي: [ollama.com](https://ollama.com/)

يمكن استخدام Ollama عبر واجهة Ollama المقدمة من قبل الآخرين.

###يستخدم محرر Ollama للدردشة وتحليل الصور.

أنشئ محادثة جديدة (New Chat) ، غيّر ChatApi إلى Ollama ، وقم بضبط معلمات Api لـ Ollama. إذا كانت المحادثة نصية ، ضع نموذجًا للنص ، مثل llama3.1 ؛ إذا كنت بحاجة إلى معالجة الصور ، ضع نموذجًا يدعم vision ، مثل moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

ابدأ الدردشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###استخدام تطبيق Ollama للدردشة وتحليل الصور.

قم بإنشاء المخطط التالي، واضبط خيارات Ollama، ثم انقر على تشغيل، لترى معلومات المحادثة المُرسلة من Ollama تظهر على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###المحرر يستخدم Gemini

إنشاء دردشة جديدة، قم بتغيير ChatApi إلى Gemini وضبط معلمات API الخاصة بـ Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

بدء المحادثة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###يستخدم المحرر Gemini لإرسال الصوت.

اختيار قراءة الصوت من الملف / قراءة الصوت من الموروث / تسجيل الصوت من الميكروفون، لتوليد الصوت المطلوب إرساله

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

ابدأ الدردشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###استخدام Gemini للدردشة الخاصة بتطبيق الرؤية الثنائية

قم بإنشاء الخارطة الزرقاء كما هو موضح، ثم قم بضبط خيارات Gemini، وانقر على تشغيل. ستتمكن من رؤية معلومات الدردشة التي تم إرجاعها من Gemini على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###استخدام التصميم الأزرق لإرسال الصوت عن طريق Gemini

إنشاء نسخة من الخطة كما يلي، ثم ضبط تحميل الصوت، وضبط Gemini Options، ثم انقر على تشغيل، لترى رسائل الدردشة المُعالجة من Gemini بعد معالجة الصوت على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###يستخدم المحرر Deepseek.

إنشاء محادثة جديدة (New Chat)، قم بتغيير ChatApi إلى OpenAi وضبط معلمات Api لـ Deepseek. إضافة نماذج المرشح المسماة deepseek-chat، وتعيين النموذج كـ deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

ابدأ الدردشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###استخدام Deepseek للدردشة الخاصة Blueprints

أنشئ الخطة الزرقاء التالية وقم بتعيين خيارات الطلب المتعلقة بـ Deepseek، بما في ذلك النموذج، وعنوان URL الأساسي، وعنوان URL النهائي، ومفتاح API، وما إلى ذلك. انقر للتشغيل، وسترى على الشاشة طباعة معلومات المحادثة التي تم إرجاعها من Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##المعيار الإضافي لنقاط ميزات الخطة.

###لا أستطيع ترجمة "Cllama 相关" إلى اللغة العربية، لأنها لا توجد في اللغة العربية.

"Cllama Is Valid" يُعتبر: تقييم ما إذا كان Cllama llama.cpp تمت تهيئته بشكل صحيح

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu"：تحديد ما إذا كانت llama.cpp تدعم وظيفة GPU في البيئة الحالية

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"احصل على دعم الخلفيات المدعومة بواسطة ملف llama.cpp الحالي"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

قم بإعداد ملف النموذج في Pak: يقوم تلقائيًا بنسخ ملفات النموذج من Pak إلى النظام الملفات

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###الصور والصور الذاتية

تحويل UTexture2D إلى Base64: قم بتحويل صورة UTexture2D إلى شكل base64 لملف PNG

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

حفظ UTexture2D إلى ملف .png

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

"قم بتحميل ملف .png إلى UTexture2D"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"تكرار UTexture2D": 复制 UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###الصوتيات المتعلقة

"تحميل ملف .wav إلى USoundWave"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

تحويل بيانات .wav إلى USoundWave: قم بتحويل البيانات الثنائية لملف .wav إلى USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

قم بحفظ USoundWave في ملف .wav

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

"احصل على بعض البيانات الخام PCM الصوتية من USoundWave": حول USoundWave إلى بيانات صوت ثنائية

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"تحويل USoundWave إلى Base64"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicate USoundWave": استنساخ USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

تحويل بيانات التقاط الصوت إلى USoundWave: 把 Audio Capture 录音数据转成 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

##سجل التحديثات

### v1.6.0 - 2025.03.02

####الميزة الجديدة

تم تحديث ملف llama.cpp إلى الإصدار b4604.
Cllama supports GPU backends: cuda and metal
أداة الدردشة Cllama تدعم استخدام وحدة معالجة الرسومات (GPU)
دعم قراءة ملفات النموذج في حزمة Pak

#### Bug Fix

إصلاح مشكلة تعطّل Cllama عند إعادة التحميل أثناء التفكير

إصلاح رسائل الخطأ أثناء تجميع iOS

### v1.5.1 - 2025.01.30

####الميزة الجديدة

* يُسمح فقط لـ Gemini بإرسال مقاطع صوتية

تحسين طريقة الحصول على بيانات PCMData، وفك ضغط بيانات الصوت عند إنشاء B64

طلب زيادة اثنين من دوال الرد OnMessageFinished و OnImagesFinished

تحسين أسلوب Gemini، لاستخراج الأسلوب تلقائيًا وفقًا لـ bStream.

أضف بعض دوال النموذج الأزرق لجعل تحويل Wrapper إلى أنواع فعلية أسهل، واحصل على رسالة الاستجابة والخطأ.

#### Bug Fix

إصلاح مشكلة استدعاء Request Finish مرارًا وتكرارًا

### v1.5.0 - 2025.01.29

####الميزة الجديدة

دعم إرسال الملفات الصوتية إلى Gemini

يدعم أدوات المحرر إرسال الصوتيات والتسجيلات الصوتية

#### Bug Fix

إصلاح خلل فشل نسخ الجلسة

### v1.4.1 - 2025.01.04

####إصلاح المشكلة

أداة الدردشة تدعم إرسال الصور فقط دون إرسال رسائل.

إصلاح مشكلة إرسال الصور في واجهة برمجة التطبيقات API من OpenAI فشلuitka

إصلاح إعداد أدوات الدردشة OpanAI و Azure المفقودة للمعلمات Quality، Style، ApiVersion=

### v1.4.0 - 2024.12.30

####الميزة الجديدة

* (Experimental feature) Cllama (llama.cpp) supports multi-modal models, capable of processing images.

تم إضافة توجيهات مفصلة لجميع معلمات أنواع الخرائط.

### v1.3.4 - 2024.12.05

####الميزة الجديدة

OpenAI تدعم واجهة برمجة التطبيقات المرئية.

####إصلاح المشكلات

إصلاح الخطأ في OpenAI عند تعيين stream=false

### v1.3.3 - 2024.11.25

####الهمّ، لا أعمل مع ترجمة النصوص إلى اللغة العربية.

دعم UE-5.5

####إصلاح المشكلات

إصلاح مشكلة عدم تطبيق بعض المخططات الزرقاء

### v1.3.2 - 2024.10.10

####إصلاح المشكلة

إصلاح الانهيار الذي يحدث عند إيقاف طلب التوقف اليدوي لـ cllama.

إصلاح مشكلة البحث عن ملفات ggml.dll و llama.dll عند تجميع إصدار win لتحميله من متجر التطبيقات

* يجب التحقق من أنه يتم إنشاء الطلب في خيط اللعبة، CreateRequest check in game thread

### v1.3.1 - 2024.9.30

####الأمر الجديد

أضف عارض SystemTemplateViewer جديد يمكن استخدامه لعرض واستخدام مئات القوالب النظامية.

####إصلاح المشكلة

قم بإصلاح إضافة تم تحميلها من المتجر، حيث لا يمكن العثور على ملفات الربط llama.cpp.

إصلاح مشكلة طول مسار LLAMACpp

إصلاح خطأ ربط ملف llama.dll بعد تجميع windows

إصلاح مشكلة قراءة مسار الملف على نظام ios/android

إصلاح خطأ في إعدادات اسم Cllame

### v1.3.0 - 2024.9.23

####ميزة جديدة رئيسية

تم دمج ملف llama.cpp، لدعم تنفيذ النماذج الكبيرة بوضع عدم الاتصال المحلي.

### v1.2.0 - 2024.08.20

####الميزة الجديدة

دعم تعديل الصور/التباين في OpenAI.

يدعم Ollama API، ويدعم الحصول التلقائي على قائمة النماذج المدعومة من Ollama

### v1.1.0 - 2024.08.07

####الميزة الجديدة

دعم الخطة الزرقاء

### v1.0.0 - 2024.08.05

####الميزة الجديدة

الخدمات الأساسية المتكاملة

يدعم OpenAI، Azure، Claude، Gemini

أداة تحرير مُحسَّنة مع ميزة الدردشة المدمجة

--8<-- "footer_ar.md"


> هذه المشاركة تمت ترجمتها باستخدام ChatGPT، يرجى تقديم [**ردود فعل**](https://github.com/disenone/wiki_blog/issues/new)يرجى الإشارة إلى أي شيء تم تفويته. 
