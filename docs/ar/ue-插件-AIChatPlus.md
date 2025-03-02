---
layout: post
title: مستندات شرح ملحق الذكاء الاصطناعي AIChatPlus UE
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
description: وثائق شرح UE AIChatPlus الإضافية
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#وثائق شرح مكون UE AIChatPlus

##المستودع العام

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##الحصول على الإضافة

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##مقدمة الإضافات

هذه الإضافة تدعم UE5.2+.

UE.AIChatPlus هو إضافة ل UnrealEngine تمكن التواصل مع مجموعة متنوعة من خدمات الدردشة الذكية GPT AI. حاليًا، يدعم الإضافة الخدمات الآتية: OpenAI (ChatGPT، DALL-E)، Azure OpenAI (ChatGPT، DALL-E)، Claude، Google Gemini، Ollama، وllama.cpp بوضع عدم الاتصال المحلي. في المستقبل، ستستمر في دعم مزيد من مزودي الخدمات. تعتمد تنفيذها على طلبات REST غير المتزامنة، مما يجعلها فعالة من حيث الأداء ويسهل على مطوري الـUE الوصول إلى هذه الخدمات الذكية محادثة الذكاء الاصطناعي.

يتضمن UE.AIChatPlus أيضًا أداة محرر تمكنك من استخدام خدمات الدردشة الذكية هذه مباشرة في المحرر ، لإنتاج النصوص والصور ، وتحليل الصور وما إلى ذلك.

##تعليمات الاستخدام

###أداة محادثة المحرر

يمكن فتح أداة محرر الدردشة المقدمة من خلال البرنامج الإضافي "AIChat" عن طريق الانتقال إلى Tools -> AIChatPlus -> AIChat في شريط القوائم.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


يدعم الأداة إنتاج النصوص، والدردشة النصية، وإنتاج الصور، وتحليل الصور.

واجهة الأدوات تبدو تقريبًا على النحو التالي:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####الميزات الرئيسية

النمط الكبير غير المتصل: يدمج مكتبة llama.cpp، ويدعم تنفيذ النماذج الكبيرة بشكل محلي خارج الاتصال بالإنترنت.

الدردشة النصية: انقر فوق الزر `New Chat` في الزاوية السفلي اليسار، لإنشاء جلسة دردشة نصية جديدة.

إنشاء الصورة: انقر فوق زر `New Image Chat` في الزاوية السفلي اليسار، لبدء جلسة إنشاء صورة جديدة.

تحليل الصور: جزء من خدمة الدردشة في "New Chat" تدعم إرسال الصور، مثل Claude، Google Gemini. يمكنك تحميل الصور التي ترغب في إرسالها عن طريق النقر فوق الزر 🖼️ أو 🎨 أعلى مربع الإدخال.

دعم التصميم الأساسي (Blueprint): دعم إنشاء طلبات واجهة برمجة تطبيقات البناء الأساسية، لإتمام المحادثات النصية، وإنشاء الصور، وغيرها من الوظائف.

قم بتعيين شخصية المحادثة الحالية: يمكنك تعيين شخصية الإرسال الحالية من خلال القائمة المنسدلة في أعلى مربع الدردشة، يمكنك محاكاة شخصيات مختلفة لضبط الدردشة الذكية.

امسح الدردشة: يمكنك مسح تاريخ الرسائل في الدردشة الحالية عن طريق النقر على العلامة ❌ في أعلى نافذة الدردشة.

قالب الحوارات: يحتوي على مئات النماذج المضمّنة لإعدادات الحوارات، مما يسهل التعامل مع المشكلات الشائعة.

الإعدادات العامة: انقر فوق زر "Setting" في الزاوية السفلى اليسرى لفتح نافذة الإعدادات العامة. يمكنك تعيين دردشة النص الافتراضية، وخدمة API لإنشاء الصور، وتعيين المعلمات الخاصة بكل خدمة. سيتم حفظ الإعدادات تلقائيًا في المسار "$(ProjectFolder)/Saved/AIChatPlusEditor" للمشروع.

إعدادات المحادثة: انقر فوق زر الإعدادات في أعلى مربع الدردشة لفتح نافذة الإعدادات الخاصة بالمحادثة الحالية. مع دعم تغيير اسم المحادثة، وتعديل خدمة API المستخدمة في المحادثة، ومع دعم ضبط بارامترات API المحددة لكل محادثة بشكل مستقل. يتم حفظ إعدادات المحادثة تلقائيًا في `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

تعديل محتوى المحادثة: عند تحويل الماوس فوق محتوى المحادثة، سيظهر زر إعدادات المحتوى الفردي الذي يسمح بإعادة إنشاء المحتوى، تعديله، نسخه، حذفه، إعادة إنشاء المحتوى أسفله (بالنسبة للمحتوى الذي تكون شخصيته للمستخدم).

عرض الصور: بالنسبة لإنشاء الصور، يمكن النقر فوق الصورة لفتح نافذة عرض الصور (ImageViewer) ، ودعم حفظ الصور كصيغة PNG/UE Texture، يمكن عرض الـ Texture مباشرة في مستعرض المحتوى (Content Browser) لسهولة استخدام الصور داخل المحرر. بالإضافة إلى دعم حذف الصور، وإعادة إنشاء الصور، ومواصلة إنشاء المزيد من الصور وغيرها من الوظائف. بالنسبة لمحرر النوافذ، يتوفر أيضًا دعم نسخ الصور، مما يتيح نسخ الصور مباشرة إلى الحافظة لسهولة الاستخدام. تُحفظ الصور التي تم إنشاؤها خلال الجلسة تلقائيًا في مجلد كل جلسة، والمسار الافتراضي عادةً هو `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

التصميم الأساسي:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

إعدادات عامة:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

إعدادات المحادثة:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

تعديل محتوى المحادثة:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

عارض الصور:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

استخدام نماذج كبيرة دون اتصال.

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

نموذج المحادثة

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###يُرجى ترجمة هذه النص إلى اللغة العربية: "مقدمة حول الشيفرة الأساسية"

حالياً، ينقسم الإضافة إلى الوحدات التالية:

AIChatPlusCommon: موديل التشغيل (Runtime)، المسؤول عن معالجة طلبات إرسال وتحليل محتوى ردود واجهات API الذكاء الاصطناعي المختلفة.

AIChatPlusEditor: مكون المحرر (Editor)، المسؤول عن تنفيذ أداة تحدث AI المحرر.

AIChatPlusCllama: وحدة التشغيل (Runtime) ، المسؤولة عن تجميع واجهة ومعلمات llama.cpp ، لتنفيذ نماذج كبيرة دون اتصال بالإنترنت

Thirdparty/LLAMACpp: تشغيل الوحدة النمطية الخارجية (Runtime)، التي تدمج معها ملفات المكتبة الديناميكية وملفات الرأس لـ llama.cpp.

تتولى فئة UClass المسؤولة عن إرسال الطلبات في هذه الحالة هي FAIChatPlus_xxxChatRequest، حيث تحتوي كل خدمة API على فئة UClass خاصة بها للطلب. سيتم الحصول على ردود الطلبات عن طريق فئتي UClass UAIChatPlus_ChatHandlerBase و UAIChatPlus_ImageHandlerBase، حيث يكفي فقط تسجيل المهمة التابعة للرد المناسبة.

قبل إرسال الطلب، يجب تعيين معلمات ورسالة الAPI أولاً، يتم ذلك من خلال FAIChatPlus_xxxChatRequestBody. يتم تحليل المحتوى الدقيق للرد في FAIChatPlus_xxxChatResponseBody، ويمكن الحصول على ResponseBody عند استقبال رد من خلال واجهة معينة.

يمكن الحصول على مزيد من تفاصيل شفرة المصدر في متجر UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###استخدام أداة محرر النص Cllama (llama.cpp) لنموذج دون اتصال

هذه التعليمات توضح كيفية استخدام نموذج العمل lama.cpp في أداة تحرير AIChatPlus.

قم بتحميل النموذج غير المتصل من موقع HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

قم بوضع النموذج في مجلد معين، مثل وضعه في دليل المشروع الخاص باللعبة تحت مسار Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

افتح أداة تحرير AIChatPlus: Tools -> AIChatPlus -> AIChat، قم بإنشاء جلسة دردشة جديدة وافتح صفحة إعدادات الجلسة

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

قم بتعيين Api إلى Cllama، وقم بتفعيل Custom Api Settings، ثم أضف مسار البحث عن النموذج واختر النموذج.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

ابدأ الدردشة!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###استخدام أداة المحرر لمعالجة الصور باستخدام نموذج غير متصل بالإنترنت الموجود في ملف Cllama (llama.cpp)

حمّل نموذج MobileVLM_V2-1.7B-GGUF من موقع HuggingFace وانقله إلى المجلد Content/LLAMA: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)و [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but the text provided does not contain any content to be translated.

تعيين نموذج الجلسة:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

بدء المحادثة بإرسال صورة

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###الرمز يستخدم نموذج غير متصل بالإنترنت Cllama(llama.cpp)

يوضح النص التالي كيفية استخدام نموذج llama.cpp في الشيفرة البرمجية.

أولاً، يجب أن تقوم بتنزيل ملفات النموذج إلى المجلد Content/LLAMA.

قم بتعديل الشيفرة لإضافة أمر جديد، وقم بإرسال رسالة لنموذج الحوسبة غير المتصل داخل الأمر.

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

بمجرد إعادة ترجمته، يمكنك استخدام الأمر في محرر Cmd لرؤية نتائج الإخراج للنموذج الكبير في سجل OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###استخدام النموذج الغير متصل llama.cpp في التصميم الهندسي

توضح الخطوات التالية كيفية استخدام النموذج غير المتصل llama.cpp في الخطة الزرقاء.

إنشاء نقطة "إرسال طلب دردشة Cllama" بالنقر بزر الماوس الأيمن في المخطط.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

إنشاء عقد خيارات وتعيين `Stream=true، ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"` في القوائم.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

إنشاء رسائل، بإضافة رسالة نظام ورسالة مستخدم بشكل منفصل

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

إنشاء Delegate يقبل معلومات النموذج الناتجة ويقوم بطباعتها على الشاشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

يبدو النموذج الأزرق الكامل كما هو، قم بتشغيل النموذج الزرق وسترى رسالة تعود بطباعة نموذج كبير على شاشة اللعبة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###llama.cpp يستخدم وحدة المعالجة الرسومية (GPU)

"خيارات طلب الدردشة Cllama" تمت إضافة المعلمة "Num Gpu Layer" ، يمكن تعيين حمولة بطاقة الرسوميات في llama.cpp كما هو موضح في الصورة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

يمكن استخدام معالم الرسم البياني لتحديد ما إذا كان البيئة الحالية تدعم وحدة معالجة الرسومات (GPU) والحصول على الأنظمة الأساسية المدعومة في البيئة الحالية:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_2.png)

###تعامل مع ملفات النماذج في ملف .Pak بعد الضغط

عندما تُشغَّل عملية التعبئة Pak، سيتم وضع جميع ملفات الموارد الخاصة بالمشروع في ملف .Pak، بما في ذلك ملفات نموذج gguf الخارجية.

نظرًا لعدم دعم llama.cpp لقراءة ملفات .Pak مباشرة، يتعين نسخ ملفات النماذج الغير متصلة من ملف .Pak إلى نظام الملفات.

AIChatPlus قدم وظيفة تسمح بنسخ ومعالجة ملفات النموذج في .Pak تلقائيًا ووضعها في مجلد Saved.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

يمكنك التعامل مع ملفات النموذج في .Pak بنفسك، المهم هو نسخ ومعالجة الملفات حتى يمكن لـ llama.cpp قراءة .Pak بشكل صحيح.

## OpenAI

###تستخدم المحرر OpenAI للدردشة

افتح أداة الدردشة Tools -> AIChatPlus -> AIChat، انشئ محادثة جديدة New Chat، ثم قم بضبط جلسة الدردشة ChatApi على OpenAI، وضبط معلمات الواجهة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

بدء المحادثة:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

قم بتبديل النموذج إلى gpt-4o / gpt-4o-mini ، يمكنك استخدام وظيفة الرؤية لصور من OpenAI

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###يستخدم المحرر OpenAI لمعالجة الصور (إنشاء/تعديل/تغيير)

في صندوق الدردشة، قم بإنشاء محادثة جديدة للصور تحت عنوان "New Image Chat"، غيّر إعدادات المحادثة إلى OpenAI وحدد الإعدادات.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

إنشاء صورة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

قم بتعديل الصورة عن طريق تغيير نوع الدردشة من Image Chat إلى Edit، ثم قم برفع صورتين، الأولى هي الصورة الأصلية والثانية تظهر مناطق الشفافية (حيث تكون قيمة قناة الألفا 0) والتي تشير إلى الأماكن التي يجب تعديلها.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

يرجى تعديل صنف الدردشة الصوتية Image Chat Type إلى صنف Variation وتحميل صورة جديدة. ستقوم OpenAI بإرجاع نسخة معدلة من الصورة الأصلية.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###استخدام نموذج OpenAI للدردشة.

إنشاء نقطة "Send OpenAI Chat Request In World" بالنقر الأيمن في النظام الأساسي.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

إنشاء العقد Options وتعيين `Stream=true, Api Key="you api key from OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

إنشاء الرسائل Messages، وإضافة رسالة نظام System Message ورسالة مستخدم User Message على التوالي

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

أنشئ Delegate لاستقبال معلومات النموذج الناتجة وطباعتها على الشاشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

يبدو الرسم البياني الكامل هكذا، قم بتشغيل الرسم البياني وسترى رسالة تعود بطباعة نموذج كبير على شاشة اللعب

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###استخدام OpenAI لإنشاء الصور

في الرسم البياني، انقر بزر الماوس الأيمن لإنشاء عقد "Send OpenAI Image Request"، وحدد "In Prompt="a beautiful butterfly""

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

أنشئ قسم Options وحدد "Api Key="مفتاح الواجهة البرمجية الخاص بك من OpenAI"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

قم بربط حدث "On Images" وحفظ الصورة على القرص المحلي.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

النسخة الكاملة من الخطة الزرقاء تبدو هكذا، قم بتشغيل الخطة الزرقاء لترى الصورة محفوظة في الموقع المحدد.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###يستخدم المحرر Azure

قم بإنشاء محادثة جديدة (New Chat)، وقم بتغيير ChatApi إلى Azure، ثم قم بتعيين معلمات Api لشركة Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

ابدأ الدردشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###استخدام محرر Azure لإنشاء الصور

إنشاء جلسة صورة جديدة (New Image Chat)، قم بتغيير ChatApi إلى Azure، وضبط معلمات API الخاصة بـ Azure. يرجى ملاحظة: إذا كان النموذج dall-e-2، فيجب تعيين جودة الصورة (Quality) ونمط الصورة (Stype) على not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

ابدأ الدردشة، واسمح لـ Azure بإنشاء الصورة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###استخدام Azure Chat في الرسم البياني

أنشئ الخطة الزرقاء التالية، قم بتعيين خيارات Azure، ثم انقر على تشغيل، لترى رسائل المحادثة التي تعود من Azure مطبوعة على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###استخدام Azure لإنشاء الصورة في الرسم الهندسي.

أنشئ الخطة الزرقاء كما هو موضح، حدد خيارات Azure بشكل صحيح، انقر فوق تشغيل، إذا نجح إنشاء الصورة، سترى رسالة "تم إنشاء الصورة" على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

وفقًا لإعدادات النظام أعلاه، سيتم حفظ الصورة في المسار D:\Dwnloads\butterfly.png.

## Claude

###قامت المحررة بالتواصل مع Claude وتحليل الصور.

إنشاء محادثة جديدة (New Chat)، قم بتغيير ChatApi إلى Claude، وضبط معلمات Api الخاصة بـ Claude

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

بدء المحادثة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###استخدمت Claude للدردشة وتحليل الصور في الشرح الأولي.

في الرسم البياني، انقر بزر الماوس الأيمن لإنشاء عقدة بإسم `Send Claude Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

إنشاء عقد `Options` وتعيين `Stream=true ، Api Key="يتمثل مفتاحك الخاص هنا" ، Max Output Tokens=1024`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

أنشئ Messages ، قم بإنشاء Texture2D من الملف ، ومن ثم أنشئ AIChatPlusTexture من Texture2D ، وأضف AIChatPlusTexture إلى Message

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

انشئ حدثًا مشابهًا للبرنامج التعليمي أعلاه واطبع المعلومات على شاشة اللعب.

النسخة الكاملة من الخطة تبدو كما يلي، قم بتشغيل الخطة لترى رسالة عودة تطبع شاشة اللعب النموذج الكبير

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###الحصول على Ollama

يمكن الحصول على حزمة التثبيت المحلية من موقع Ollama الرسمي: [ollama.com](https://ollama.com/)

يمكن استخدام منصة Ollama من خلال واجهة برمجة التطبيقات (API) التي تم توفيرها من قبل شخص آخر.

###يستخدم المحرر Ollama للدردشة وتحليل الصور

إنشاء محادثة جديدة (New Chat)، قم بتغيير ChatApi إلى Ollama وضبط معلمات Api لـ Ollama. إذا كانت المحادثة نصية، قم بتعيين النموذج كنموذج نصي، مثل llama3.1. وإذا كنت بحاجة لمعالجة الصور، فعين النموذج كنموذج يدعم الرؤية، مثل moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

ابدأ الدردشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###استخدم Ollama الرسوم البيانية وتحاليل الصور.

أنشئ الخطة التوضيحية التالية، ضبط خيارات الألما، انقر فوق "تشغيل"، وستظهر معلومات المحادثة التي تم إرجاعها من قبل الألما على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###يستخدم Gemini المحرر

إنشاء محادثة جديدة (New Chat)، قم بتغيير ChatApi إلى Gemini، وضبط معلمات Api الخاصة بـ Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

ابدأ المحادثة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###المحرر يستخدم Gemini لإرسال الصوت

اختر قراءة الصوت من الملف / الصوت من المورد / تسجيل الصوت من الميكروفون لإنشاء الصوت الذي يجب إرساله.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

بدء المحادثة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###استخدام Gemini للرسائل النصية الآزرق

قم بإنشاء الخطة الزرقاء التالية، حدد خيارات الجوزاء، انقر فوق تشغيل، وسترى معلومات الدردشة التي تعود بها Gemini تُطبع على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###استخدمت الخريطة الزرقاء Gemini لإرسال الصوت

قم بإنشاء الخطة الزرقاء التالية، ضبط تحميل الصوت، ثم قم بضبط خيارات Gemini، انقر على تشغيل، وسترى رسائل الدردشة التي تعود بعد معالجة Gemini للصوت على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###تستخدم المحرر Deepseek

إنشاء محادثة جديدة (New Chat)، قم بتغيير ChatApi إلى OpenAi، وحدد معلمات Api لـ Deepseek. أضف نماذج مرشحة جديدة تسمى deepseek-chat، وقم بتعيين النموذج ك deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

بدء المحادثة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###استخدام النموذج الأساسي للدردشة Deepseek

قم بإنشاء الخريطة الزرقاء كما هو موضح، وقم بضبط خيارات الطلب المتعلقة بـ Deepseek، بما في ذلك النموذج وعنوان URL الرئيسي وعنوان URL النهائي ومعلمة ApiKey. انقر فوق تشغيل لرؤية معلومات المحادثة التي تعيد Gemini على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##المقاطعات الوظيفية الإضافية المقدمة

###Cllama المتعلقة

"Cllama Is Valid": تحقق من ما إذا كان Cllama llama.cpp قد تم تهيئته بشكل صحيح.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu"：تحديد ما إذا كان ملف llama.cpp يدعم واجهة GPU في البيئة الحالية

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"الحصول على الأدعية المدعومة من cat.cpp حالياً"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

قم بتحضير ملف النموذج في ملف باك: يقوم تلقائيًا بنسخ ملفات النموذج من باك إلى نظام الملفات.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###الرسوم البيانية المتعلقة

تحويل UTexture2D إلى Base64: تحويل صورة UTexture2D إلى تنسيق base64 PNG

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

حفظ UTexture2D كملف .png

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

"تحميل ملف .png إلى UTexture2D":  قراءة ملف png إلى UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"تكرار UTexture2D"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###الصوتيات ذات الصلة

قُم بتحميل ملف .wav إلى USoundWave: قم بتحميل ملف .wav إلى USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

تحويل بيانات wav إلى USoundWave: 把 wav 二进制数据转成 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

حفظ USoundWave في ملف .wav

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

"احصل على بعض بيانات USoundWave الخام بتنسيق PCM" : 把 USoundWave 转成二进制音频数据

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"تحويل USoundWave إلى Base64"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicate USoundWave": نسخ USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

تحويل بيانات التقاط الصوت إلى USoundWave: 把 Audio Capture 录音数据转成 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

##سجل التحديثات.

### v1.6.0 - 2025.03.02

####الميزة الجديدة

* قم بترقية ملف llama.cpp إلى الإصدار b4604

Cllama تدعم GPU backends: cuda و metal

أداة الدردشة Cllama تدعم استخدام وحدة المعالجة الرسومية (GPU)

دعم قراءة ملفات النموذج داخل حزمة Pak

#### Bug Fix

إصلاح مشكلة تعطل Cllama أثناء إعادة التحميل أثناء التفكير

إصلاح خطأ الترجمة في iOS

### v1.5.1 - 2025.01.30

####الأداء الجديد

يُسمح فقط بإرسال ملفات صوتية عبر جيميني

تحسين طريقة الحصول على بيانات PCMData، وفك ضغط بيانات الصوت عند توليد B64

* طلب زيادة صنع رد فعلين OnMessageFinished و OnImagesFinished

تحسين طريقة Gemini Method، واسترجاع الـ Method تلقائيًا استناداً إلى bStream.

أضف بعض الدوال الخاصة بالتصميمات الزرقاء، لتيسير تحويل الإطار الخارجي إلى أنواع فعلية، والحصول على رسالة الاستجابة والخطأ.

#### Bug Fix

إصلاح مشكلة تكرار استدعاء Request Finish.

### v1.5.0 - 2025.01.29

####الميزة الجديدة

دعم إرسال الصوت لـ جيميني

تدعم أدوات المحرر إرسال الصوتيات والتسجيلات الصوتية.

#### Bug Fix

إصلاح خلل نسخ جلسة الجلسة.

### v1.4.1 - 2025.01.04

####إصلاح المشكلات

يدعم أداة الدردشة إرسال الصور فقط دون إرسال رسائل.

اصلح مشكلة إرسال الصور عبر واجهة OpenAI.

إصلاح إعدادات أدوات المحادثة OpanAI وAzure التي تغفلت عن المعلمات Quality وStyle وApiVersion =

### v1.4.0 - 2024.12.30

####الميزة الجديدة

الدعم النموذجي المتعدد لبرنامج Cllama(llama.cpp) (وظيفة تجريبية)، يمكنه معالجة الصور

تمت إضافة توجيهات تفصيلية لجميع معلمات أنواع التصميم.

### v1.3.4 - 2024.12.05

####الميزة الجديدة

OpenAI تدعم واجهة برمجة التطبيقات للرؤية.

####إصلاح المشكلات

إصلاح الخطأ في OpenAI stream=false

### v1.3.3 - 2024.11.25

####ميزة جديدة

دعم UE-5.5

####إصلاح المشكلات

إصلاح مشكلة عدم تنفيذ جزء من الخرائط الزرقاء

### v1.3.2 - 2024.10.10

####إصلاح المشكلة

إصلاح تعطل cllama عند إيقاف طلب الإيقاف يدويًا

إصلاح مشكلة عدم العثور على ملفات ggml.dll و llama.dll أثناء تعبئة إصدار تنزيل متجر win.

عند إنشاء الطلب، تحقق من أنك في خط اللعبة

### v1.3.1 - 2024.9.30

####الميزة الجديدة

أضف SystemTemplateViewer جديد، يمكنك من خلاله استعراض واستخدام مئات القوالب النظامية.

####إصلاح المشكلة

إصلاح الإضافات التي تم تحميلها من المتجر، llama.cpp لا يمكن العثور على مكتبة الارتباط.

إصلاح مشكلة طول مسار LLAMACpp

إصلاح خطأ رابط llama.dll بعد تعبئة windows

إصلاح مشكلة قراءة مسار الملف في نظام التشغيل iOS/Android

إصلاح خطأ في ضبط اسم Cllame

### v1.3.0 - 2024.9.23

####ميزة جديدة هامة

دمج ملف llama.cpp لدعم تنفيذ نماذج كبيرة بشكل محلي وغير متصل بالإنترنت.

### v1.2.0 - 2024.08.20

####الوظيفة الجديدة

دعم تعديل الصور/ التنويع في الصور من OpenAI.

يدعم واجهة برمجة تطبيقات Ollama، ويمكنه الحصول التلقائي على قائمة النماذج المدعومة بواسطة Ollama.

### v1.1.0 - 2024.08.07

####الوظيفة الجديدة

دعم الخطة الزرقاء

### v1.0.0 - 2024.08.05

####الوظيفة الجديدة

وظيفة أساسية ومكتملة

دعم OpenAI، Azure، Claude، Gemini

يحمل معه أداة تحرير محادثات متكاملة

--8<-- "footer_ar.md"


> هذا المنشور مترجم باستخدام ChatGPT، يرجى تقديم [**ردود فعل**](https://github.com/disenone/wiki_blog/issues/new)أشر على أي نقص. 
