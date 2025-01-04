---
layout: post
title: وثائق شرح إضافة AIChatPlus لـ UE
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
description: وثائق شرح مُلحق AIChatPlus لـ UE
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#وثائق شرح UE مكمل الذكاء الاصطناعي AIChatPlus

##المستودعات العامة

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##الحصول على الإضافات

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##مقدمة الوصفة

هذا الملحق يدعم UE5.2+،

UE.AIChatPlus هو إضافة لـ UnrealEngine تقوم بالتواصل مع مجموعة متنوعة من خدمات الدردشة GPT AI. حاليًا، يدعم الإضافة خدمات OpenAI (ChatGPT، DALL-E)، و Azure OpenAI (ChatGPT، DALL-E)، و Claude، و Google Gemini، و Ollama، وllama.cpp المحلي بدون اتصال بالإنترنت. سيتم دعم مزيد من مزودي الخدمات في المستقبل. تعتمد تنفيذها على طلبات REST غير المتزامنة، مما يجعلها كفاءة من الناحية الأدائية وسهلة الاختيار لمطوري UE للوصول إلى خدمات الدردشة الذكية هذه.

UE.AIChatPlus تحتوي أيضًا على أداة محرر تُمكّنك من استخدام خدمات الدردشة الذكية هذه مباشرةً في المحرر، لإنشاء نصوص وصور، وتحليل الصور، وما إلى ذلك.

##تعليمات الاستخدام

###أداة محادثة المحرر

يمكن فتح شريط القوائم والانتقال إلى AIChatPlus -> AIChat لاستخدام أدوات محرر الدردشة المقدمة من الإضافة.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


يدعم الأداة إنشاء النصوص والدردشة النصية وإنشاء الصور وتحليل الصور.

واجهة الأداة تقريبًا:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####الميزات الرئيسية

النموذج الكبير دون اتصال: مدموج مع مكتبة llama.cpp ، تدعم التنفيذ اللاحق للنماذج الكبيرة محليًا

الدردشة النصية: انقر فوق زر "New Chat" في الزاوية السفلي اليساري، لإنشاء جلسة دردشة نصية جديدة.

إنشاء صورة: انقر فوق الزر `New Image Chat` في الزاوية السفلي اليسرى لإنشاء جلسة جديدة لإنشاء صورة.

تحليل الصور: تدعم خدمة الدردشة في 'New Chat' إمكانية إرسال الصور، مثل Claude و Google Gemini. يمكنك تحميل الصور التي تود إرسالها ببساطة عن طريق النقر على الزر 🖼️ أو 🎨 أعلى مربع الإدخال.

دعم الخطط الأساسية (Blueprint): دعم إنشاء طلبات API للخطط الأساسية، لإتمام محادثات النصوص، وإنشاء الصور وغيرها من الوظائف.

قم بتعيين دور الدردشة الحالي: يمكنك تعيين دور الشخصية التي سترسل النص الخاص بها حاليًا من خلال القائمة المنسدلة في أعلى نافذة الدردشة، ويمكنك من خلال تجسيد شخصيات مختلفة ضبط دردشة الذكاء الصناعي.

امسح الدردشة: يمكنك مسح تاريخ الرسائل الحالي في الدردشة عن طريق الضغط على ❌ في أعلى صندوق الدردشة.

نموذج الحوار: يتضمن مئات النماذج المدمجة لإعدادات الحوار، مما يسهل التعامل مع المشكلات الشائعة.

الإعدادات العامة: بالنقر على زر `Setting` في الزاوية السفلى اليسرى، يمكن فتح نافذة الإعدادات العامة. يمكنك تعيين الدردشة النصية الافتراضية، وخدمة API لإنشاء الصور، وضبط معلمات كل خدمة API بشكل محدد. ستحفظ الإعدادات تلقائيًا في مسار المشروع `$(ProjectFolder)/Saved/AIChatPlusEditor`.

إعدادات الدردشة: انقر فوق زر الإعدادات في أعلى صندوق الدردشة لفتح نافذة إعدادات الدردشة الحالية. تدعم تغيير اسم الدردشة، وتغيير خدمة واجهة برمجة التطبيقات (API) المستخدمة في الدردشة، وتدعم ضبط معلمات API المحددة لكل دردشة على حدة. يتم حفظ إعدادات الدردشة تلقائيًا في `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

تعديل محتوى المحادثة: عند تحويل الماوس إلى المحتوى المحدد في المحادثة، ستظهر أزرار الإعدادات الخاصة بالمحتوى، تدعم إعادة إنشاء المحتوى، وتعديله، ونسخه، وحذفه، وإعادة إنشاء محتوى جديد أسفل ذلك (بالنسبة للمحتوى الخاص بمستخدمي الأدوار).

عرض الصور: بالنسبة لإنشاء الصور، يمكن فتح نافذة عرض الصور (ImageViewer) عند النقر فوق الصورة، وتدعم حفظ الصور كملف PNG/UE Texture، يمكن عرض الـ Texture مباشرة في مستعرض المحتوى (Content Browser)، مما يسهل استخدام الصور في المحرر. بالإضافة إلى ذلك، تدعم أيضًا حذف الصور، وإعادة إنشاء الصور، واستمرار توليد المزيد من الصور وغيرها من الوظائف. بالنسبة لمحرر Windows، تدعم أيضًا نسخ الصور، مما يسمح بنسخ الصور مباشرة إلى الحافظة لسهولة الاستخدام. يتم حفظ الصور التي تم إنشاؤها خلال الجلسة تلقائيًا في مجلد الجلسة الخاص بكل جلسة، والمسار الافتراضي عادة هو '$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images'.

الرسم البياني:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

إعدادات عامة:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

إعدادات المحادثة:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

قم بتعديل محتوى المحادثة:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

عارض الصور:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

استخدام نماذج كبيرة دون اتصال بالإنترنت

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

قالب الحوار

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###شرح الكود الأساسي

حالياً، يتم تقسيم الإضافات إلى عدة وحدات كالتالي:

AIChatPlusCommon: وحدة التشغيل (Runtime) ، المسؤولة عن معالجة طلبات إرسال وتحليل محتوى ردود واجهة برمجة تطبيقات الذكاء الصناعي (AI API) المختلفة.

AIChatPlusEditor: موديل المحرر، مسؤول عن تنفيذ أداة محادثة AI للمحرر.

AIChatPlusCllama: Runtime module responsible for encapsulating the interface and parameters of llama.cpp, enabling offline execution of large models

تمت ترجمة النص إلى اللغة العربية:

* Thirdparty/LLAMACpp: تشغيل الوحدة الخارجية (Runtime)، والتي تدمج مكتبة لاما.cpp الديناميكية والملفات الرأسية.

يُسند على UClass المسؤول تحديد نوع طلب FAIChatPlus_xxxChatRequest الذي سيتم إرساله، ولكل خدمة API يوجد UClass طلب مستقل. سيتم الحصول على ردود الطلبات من خلال UClass UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase، حيث يتطلب الأمر تسجيل الاستدعاءات المناسبة فقط.

قبل إرسال الطلبات، يجب تعيين معلمات ورسائل الـ API بشكل مسبق، يتم تعيين ذلك باستخدام FAIChatPlus_xxxChatRequestBody. يتم تحليل المحتوى الخاص بالردود أيضًا في FAIChatPlus_xxxChatResponseBody، يمكنك الحصول على ResponseBody من خلال واجهة معينة عند استلام التعليق.

يمكن الحصول على مزيد من تفاصيل الشفرة المصدرية عبر UE Marketplace: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###استخدام أداة المحرر لنموذج غير متصل بالإنترنت Cllama(llama.cpp)

سيرين توضح كيفية استخدام نموذج الغياب llama.cpp في أداة تحرير AIChatPlus.

قم بتحميل النموذج الفردي من موقع HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

ضع النموذج في مجلد معين، على سبيل المثال ضعه في دليل المشروع اللعبة تحت مجلد Content/LLAMA

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

افتح أداة تحرير AIChatPlus: Tools -> AIChatPlus -> AIChat، أنشئ جلسة دردشة جديدة وافتح صفحة إعدادات الجلسة

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

قم بتعيين Api إلى Cllama، وفتح إعدادات الـ Custom Api، وأضف مسار بحث للنموذج، واختر نموذجًا.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

البدء في الدردشة!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###استخدمت أداة المحرر نموذجًا غير متصل بالإنترنت بعنوان Cllama(llama.cpp) لمعالجة الصور.

قم بتنزيل نموذج MobileVLM_V2-1.7B-GGUF من موقع HuggingFace وضعه في دليل Content/LLAMA: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)(https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but the text you provided does not contain any content to be translated.

ضبط نموذج الجلسة:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

بدء الدردشة بإرسال الصور

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###استخدام الشيفرة للنموذج غير المتصل بالإنترنت Cllama(llama.cpp)

توضح الإرشادات التالية كيفية استخدام النموذج الغير متصل llama.cpp في الشفرة.

أولاً، يجب تحميل ملفات النموذج إلى Content/LLAMA.

إضافة سطر في الشفرة لإدخال أمر وإرسال رسالة للنموذج غير المتصل داخل هذا الأمر.

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

بعد إعادة تجميعها، يمكنك استخدام الأوامر في محرر الأوامر Cmd لرؤية نتائج النموذج الكبير في سجل الإخراج OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###استخدام النموذج غير المتصل llama.cpp في الرسم البياني.

كيفية استخدام نموذج llama.cpp دون اتصال في الخطط التفصيلية.

إنشاء نقطة "Send Cllama Chat Request" بالنقر بزر اليمين في الخريطة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

إنشاء عقد Options ، وتعيين 'Stream=true ، ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"'

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

إنشاء رسائل Messages، وإضافة رسالة نظامية ورسالة مستخدم على التوالي

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

إنشاء delegate لاستقبال مخرجات النموذج وطباعتها على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

النص المطلوب ترجمته هو: * إن النسخة الكاملة من التصميم على هذا الشكل، عند تشغيل التصميم، يمكن رؤية رسالة تظهر على الشاشة تعود إليك بطباعة النموذج الكبير

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###تستخدم المحررات دردشة OpenAI.

قم بفتح أداة الدردشة Tools -> AIChatPlus -> AIChat، وانشئ محادثة جديدة New Chat، وضبط جلسة الدردشة ChatApi على OpenAI، ثم قم بضبط معلمات الواجهة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

بدء المحادثة:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

قم بتغيير النموذج إلى GPT-4o / GPT-4o-mini ، يمكنك استخدام وظيفة الرؤية من OpenAI لتحليل الصور.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###يستخدم المحرر OpenAI لمعالجة الصور (إنشاء / تعديل / تغيير)

إنشاء محادثة جديدة للصور في أداة الدردشة ، وتعديل إعدادات المحادثة إلى OpenAI وضبط المعلمات

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

إنشاء صورة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

يرجى تعديل الصورة، وتغيير نوع الدردشة في الصورة إلى "تحرير"، ثم قم برفع صورتين، إحداهما الصورة الأصلية، والأخرى "قناع" حيث يُظهر المكان الذي يجب تعديله بوضوح (جعل القناع فيه شفافية بقيمة 0 في قناة ألفا).

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

قم بتعديل نوع الدردشة الصورية إلى "تعديل" وارفع صورة جديدة، ستقوم OpenAI بإرجاع نسخة معدلة من الصورة الأصلية.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###استخدام النموذج OpenAI للدردشة

أنشئ مُحظوظة "Send OpenAI Chat Request In World" في المُخطَّط عن طريق النقر بزر الماوس الأيمن.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

إنشاء مقطع Options، وتعيين `Stream=true، Api Key="مفتاح الواجهة البرمجية الخاص بك من OpenAI"`‎.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

أنشئ رسائل، ثم أضف رسالة نظام ورسالة مستخدم بشكل منفصل

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

إنشاء Delegate يستقبل معلومات النموذج الصادرة ويقوم بطباعتها على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

تبدو الخطة الزرقاء الكاملة كما هو موضح، قم بتشغيل الخطة الزرقاء لعرض رسالة العودة التي تُظهر الشاشة الخاصة باللعبة بطباعة نموذج كبير.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###استخدام OpenAI لإنشاء الصور.

إنشاء نقطة "Send OpenAI Image Request" في الخريطة الذهنية بالضغط الأيمن، وتعيين "In Prompt" إلى "فراشة جميلة".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

إنشاء "Options" العقدة، وتعيين `Api Key="your api key from OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

ربط حدث On Images وحفظ الصورة على القرص الصلب المحلي

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

سيبدو النسخ الكاملة للمخطط كما هو مبين هنا، قم بتشغيل المخطط لرؤية الصورة محفوظة في الموقع المحدد.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###تستخدم الواجهة البرمجية Azure

إنشاء محادثة جديدة (New Chat)، قم بتغيير ChatApi إلى Azure، وضبط معلمات Api الخاصة بـ Azure

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

بدء المحادثة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###استخدمت المحرر Azure لإنشاء الصور.

إنشاء جلسة صور جديدة (New Image Chat)، قم بتغيير ChatApi إلى Azure، وقم بضبط معلمات Azure الخاصة به، يرجى ملاحظة، إذا كانت النموذج dall-e-2، يجب ضبط معلمات الجودة (Quality) والنمط (Stype) على not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

ابدأ الدردشة لإنشاء صورة Azure

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###استخدام Azure Chat Blueprint

إنشاء الخطة الزرقاء التالية، ضبط خيارات Azure، انقر على تشغيل، وسترى رسائل المحادثة المُرجعة من Azure تظهر على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###استخدام Azure في إنشاء الصورة.

إنشاء الرسم البياني التالي، ثم ضبط خيارات أزور، وانقر على "تشغيل". إذا نجح إنشاء الصورة، سترى عبارة "تم إنشاء الصورة" على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

وفقًا للإعدادات في الخريطة الزرقاء أعلاه، سيتم حفظ الصورة في المسار D:\Dwnloads\butterfly.png

## Claude

###يستخدم المحرر Claude المحادثات وتحليل الصور.

إنشاء محادثة جديدة (New Chat)، قم بتغيير ChatApi إلى Claude، وضبط معلمات Api لـ Claude

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

ابدأ الدردشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###استخدم كلود النموذج الأزرق للدردشة وتحليل الصور.

قم بإنشاء نقطة "Send Claude Chat Request" بالنقر بزر الماوس الأيمن في النموذج الأزرق.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

إنشاء عقدة Options، وتعيين 'Stream=true، Api Key="مفتاح الواجهة البرمجية الخاص بك من Clude'، Max Output Tokens=1024.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

إنشاء رسائل، إنشاء Texture2D من الملفات، ومن Texture2D إنشاء AIChatPlusTexture، ثم إضافة AIChatPlusTexture إلى الرسالة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

انشئ حدثًا مشابهًا للبرنامج التعليمي السابق واطبع المعلومات على شاشة اللعبة.

تبدو النسخة الكاملة من الخطة الزرقاء مثل هذا، تشغيل الخطة الزرقاء سوف تظهر رسالة عائدة على شاشة اللعب تطبع نموذجًا كبيرًا.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###الحصول على Ollama

يمكن الحصول على حزمة التثبيت محليًا من خلال موقع Ollama الرسمي: [ollama.com](https://ollama.com/)

يمكنك استخدام واجهة Ollama المقدمة من قبل الآخرين لاستخدام Ollama.

###المحرر يستخدم Ollama للدردشة وتحليل الصور.

أنشئ محادثة جديدة (New Chat)، غيّر ChatApi إلى Ollama، وقم بضبط معلمات Api Ollama. إذا كانت المحادثة نصية، فقم بتعيين النموذج كنموذج نصي، مثل llama3.1؛ وإذا كنت بحاجة لمعالجة الصور، فقم بتعيين النموذج كنموذج يدعم vision، مثل moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

بدء المحادثة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###استخدام Ollama للدردشة وتحليل الصور في التصميم الأزرق

أنشئ المخطط التالي ، قم بضبط خيارات الـ Ollama ، انقر على تشغيل ، وسترى معلومات الدردشة التي تم إرجاعها بواسطة Ollama على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###المحرر يستخدم Gemini

قم بإنشاء محادثة جديدة (New Chat) ، وقم بتغيير ChatApi إلى Gemini، ثم قم بضبط معلمات Api الخاصة بـ Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

بدء المحادثة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###استخدام التصميم الأزرق Gemini للدردشة

أنشئ الخطة الزرقاء كما هو موضح، ثم قم بضبط خيارات Gemini، انقر على تشغيل، وسترى على الشاشة طباعة معلومات المحادثة التي تم إرجاعها من Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

## Deepseek

###المحرر يستخدم Deepseek

إنشاء محادثة جديدة (New Chat)، غير ChatApi إلى OpenAi، وضبط معلمة Deepseek للواجهة البرمجية. إضافة نماذج المرشحين تسمى deepseek-chat وتعيين النموذج كـ deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

ابدأ الدردشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###استخدام Deepseek في الدردشة البصرية

قم بإنشاء نسق مشروع كـ Deepseek وحدد خيارات الطلب المتعلقة بـ Deepseek، بما في ذلك نموذج البيانات وعنوان URL الأساسي وعنوان URL النهائي ومفتاح الواجهة البرمجية وما إلى ذلك. انقر فوق تشغيل لرؤية معلومات المحادثة التي تعود من Gemini يتم طباعتها على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##سجل التحديثات

### v1.4.1 - 2025.01.04

####إصلاح المشكلة

واجهة دردشة تدعم إمكانية إرسال الصور فقط دون إرسال رسائل.

إصلاح مشكلة إرسال الصور في واجهة OpenAI فشل الصورة والنص

إصلاح مشكلة غياب الإعدادات Quality، Style، ApiVersion من إعدادات أدوات الدردشة OpanAI وAzure.

### v1.4.0 - 2024.12.30

####الميزة الجديدة

（وظيفة تجريبية） Cllama (llama.cpp) تدعم نموذج متعدد الأوضاع لمعالجة الصور.

تم إضافة توجيهات مفصلة إلى جميع معلمات أنواع الخرائط.

### v1.3.4 - 2024.12.05

####النص الأصلي: 新功能


OpenAI تدعم واجهة برمجة تطبيقات الرؤية.

####تصحيح المشكلة

إصلاح الخطأ عند تعيين OpenAI stream=false

### v1.3.3 - 2024.11.25

####الميزة الجديدة

دعم UE-5.5

####إصلاح المشكلة

قم بإصلاح مشكلة عدم فعالية جزء من التصميمات الزرقاء.

### v1.3.2 - 2024.10.10

####إصلاح المشكلة

إصلاح الانهيار الذي يحدث في cllama عند إيقاف طلب الإيقاف يدويًا.

إصلاح مشكلة عدم العثور على ملفات ggml.dll و llama.dll أثناء تحزيم إصدار win لتنزيل من المتجر.

عند إنشاء الطلب، تحقق مما إذا كان ذلك في خيط اللعب.

### v1.3.1 - 2024.9.30

####وظيفة جديدة

إضافة SystemTemplateViewer جديد، يمكنك الاطلاع على واستخدام مئات القوالب النظام المختلفة.

####تصليح المشكلات

إصلاح الإضافات التي تم تنزيلها من المتجر ، llama.cpp لا يمكن العثور على مكتبة الربط

إصلاح مشكلة الطول الزائد في مسار LLAMACpp

إصلاح خطأ رابط ملف llama.dll بعد تجميع نظام Windows.

إصلاح مشكلة قراءة مسار الملف في نظام التشغيل iOS/Android.

إصلاح خطأ في تسمية إعدادات Cllame

### v1.3.0 - 2024.9.23

####ميزة جديدة مهمة

دمج ملف llama.cpp، يدعم تنفيذ النماذج الكبيرة محلياً وخارج الاتصال.

### v1.2.0 - 2024.08.20

####ميزة جديدة

دعم تعديل الصور/التباين في OpenAI

دعم واجهة برمجة تطبيقات Ollama، دعم الحصول التلقائي على قائمة النماذج المدعومة من قبل Ollama

### v1.1.0 - 2024.08.07

####الميزة الجديدة

دعم الخطة الزرقاء

### v1.0.0 - 2024.08.05

####ترجمة: "وظيفة جديدة".

الوظائف الأساسية كاملة

دعم OpenAI، Azure، Claude، Gemini

أداة تحرير مدمجة مع ميزات شاملة للدردشة

--8<-- "footer_ar.md"


> هذا المنشور تمت ترجمته باستخدام ChatGPT، يرجى تقديم [**تغذية راجعة**](https://github.com/disenone/wiki_blog/issues/new)أشير إلى أي شيء مفتقد. 
