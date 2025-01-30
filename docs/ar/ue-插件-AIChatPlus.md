---
layout: post
title: وثيقة شرح المكون الإضافي UE AIChatPlus
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

#وثيقة شرح ملحق UE AIChatPlus

##مخازن عامة

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##الحصول على المكونات الإضافية

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##مقدمة عن الإضافات

يدعم هذا الملحق UE5.2+.

UE.AIChatPlus هو مكون إضافي لـ UnrealEngine، يتيح التفاعل مع خدمات الدردشة متعددة GPT AI. حاليًا، تشمل الخدمات المدعومة OpenAI (ChatGPT، DALL-E)، Azure OpenAI (ChatGPT، DALL-E)، Claude، Google Gemini، Ollama، و llama.cpp المحلية غير المتصلة بالإنترنت. في المستقبل، سيتم دعم المزيد من مقدمي الخدمة. تعتمد تنفيذه على طلبات REST غير المتزامنة، مما يضمن كفاءة عالية ويسهل على مطوري UE الوصول إلى هذه الخدمات الخاصة بالدردشة بالذكاء الاصطناعي.

في الوقت نفسه، يحتوي UE.AIChatPlus أيضًا على أداة محرر، يمكن من خلالها استخدام خدمات الدردشة الذكية هذه مباشرة داخل المحرر، لتوليد النصوص والصور، وتحليل الصور، وغيرها.

##تعليمات الاستخدام

###أداة دردشة المحرر

شريط القوائم Tools -> AIChatPlus -> AIChat يمكنه فتح أداة الدردشة المحررة المتاحة من خلال الإضافة.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


تقدم الأداة دعمًا لإنشاء النصوص، والدردشة النصية، وإنشاء الصور، وتحليل الصور.

واجهة الأدوات تتكون تقريبًا من:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####الترجمة غير متاحة لهذا النص، يُرجى تقديم نص بلغة معروفة لترجمته.

* نماذج كبيرة غير متصلة بالإنترنت: تم دمج مكتبة llama.cpp، وتدعم التنفيذ المحلي غير المتصل بالإنترنت للنماذج الكبيرة.

* دردشة نصية: انقر على زر `الدردشة الجديدة` في الزاوية اليسرى السفلية لبدء محادثة نصية جديدة.

* توليد الصور: انقر على زر `New Image Chat` في الزاوية اليسرى السفلى، لإنشاء جلسة جديدة لتوليد الصور.

تحليل الصور: بعض خدمات المحادثة في "New Chat" تدعم إرسال الصور، مثل Claude و Google Gemini. يمكنك تحميل الصور التي ترغب في إرسالها عن طريق النقر على الزر الموجود أعلى مربع الإدخال، الذي يحتوي على رمز 🖼️ أو 🎨.

دعم المخطط الأولي (Blueprint): دعم إنشاء طلبات API للمخطط الأولي، لإتمام المحادثات النصية، وإنتاج الصور، وغيرها من الوظائف.

تعيين شخصية الدردشة الحالية: يمكنك تعيين شخصية الذي تريد إرسال النص باستخدام القائمة المنسدلة في أعلى صندوق الدردشة، حيث يمكنك محاكاة شخصيات مختلفة لتعديل دردشة الذكاء الاصطناعي.

* مسح المحادثة: زر ❌ في أعلى مربع المحادثة يمكنه مسح تاريخ الرسائل الحالية.

* نموذج الحوار: يتضمن مئات من نماذج الإعدادات للحوار لتسهيل معالجة المشكلات الشائعة.

يمكنك ضبط الإعدادات العامة عن طريق النقر على زر "Setting" في الزاوية السفلى اليسرى، وسيتم فتح نافذة الإعدادات العامة. يمكنك تعيين الدردشة النصية الافتراضية، وخدمة API لإنشاء الصور، وتحديد معلمات كل خدمة API بالتحديد. يتم حفظ الإعدادات تلقائيًا في مسار المشروع "$(ProjectFolder)/Saved/AIChatPlusEditor".

إعدادات المحادثة: انقر فوق زر الإعدادات في الجزء العلوي من صندوق الدردشة لفتح نافذة الإعدادات الخاصة بالمحادثة الحالية. يمكن تعديل اسم المحادثة، وتعديل خدمة API المستخدمة في المحادثة، ويدعم ضبط معلمات كل محادثة بشكل مستقل لاستخدام خدمة API. يتم حفظ إعدادات المحادثة تلقائيًا في `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

* تعديل محتوى الدردشة: عند تحريك الماوس فوق محتوى الدردشة، سيظهر زر إعدادات محتوى الدردشة الفردي، يدعم إعادة توليد المحتوى، تعديل المحتوى، نسخ المحتوى، حذف المحتوى، وإعادة توليد المحتوى في الأسفل (بالنسبة لمحتوى المستخدمين).

* استعراض الصور: بالنسبة لتوليد الصور، النقر على الصورة سيفتح نافذة عرض الصور (ImageViewer)، تدعم حفظ الصور كملف PNG/UE Texture، ويمكن عرض Texture مباشرة في مستعرض المحتوى (Content Browser)، مما يسهل استخدام الصور في المحرر. بالإضافة إلى ذلك، تدعم أيضًا حذف الصور، إعادة توليد الصور، وتوليد المزيد من الصور. بالنسبة لمحرر Windows، يتم دعم نسخ الصور، حيث يمكن نسخ الصور مباشرة إلى الحافظة لسهولة الاستخدام. يتم حفظ الصور التي تم إنشاؤها خلال الجلسة تلقائيًا في مجلد كل جلسة، والمسار النموذجي هو `${GUID}/images/Sessions/Editor/AIChatPlus/Saved/ProjectFolder)`.

المخطط:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

إعدادات عامة:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

إعدادات المحادثة:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

تعديل محتوى المحادثة:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

عارض الصور:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

استخدام نماذج كبيرة دون اتصال بالإنترنت

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

قالب الحوار.

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###مقدمة عن الشفرة الأساسية

تُقسم المكونات الحالية إلى الوحدات التالية:

* AIChatPlusCommon: وحدة وقت التشغيل (Runtime) ، المسؤولة عن معالجة الطلبات المرسلة من واجهات برمجة التطبيقات (API) للذكاء الاصطناعي وفك تشفير محتوى الردود.

* AIChatPlusEditor: محرر模块 (Editor) ، مسؤول عن实现 محرر أدوات الدردشة الذكية.

AIChatPlusCllama: The Runtime module responsible for encapsulating the interface and parameters of llama.cpp to enable offline execution of large models.

* Thirdparty/LLAMACpp: وحدة طرف ثالث للتشغيل (Runtime)، تجمع بين المكتبة الديناميكية وملفات الرأس لـ llama.cpp.

تتولى فئة UClass المسؤولة عن إرسال الطلبات في FAIChatPlus_xxxChatRequest، كل خدمة API لها فئة Request UClass مستقلة. يتم الحصول على رد الطلبات عبر فئتي UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase، حيث يكفي تسجيل الوفود المناسبة فقط.

قبل إرسال الطلب، يجب تعيين معلمات ورسالة ال API أولاً، يتم ذلك من خلال إعداد FAIChatPlus_xxxChatRequestBody. يتم تحليل المحتوى الرد المحدد أيضًا في FAIChatPlus_xxxChatResponseBody، وعند استلام الاستدعاء يمكن الحصول على ResponseBody عبر واجهة معينة.

يمكن الحصول على مزيد من تفاصيل شفرات المصدر عبر متجر UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###استخدام أداة المحرر لنموذج غير متصل Cllama(llama.cpp)

يرجى اتباع هذه التعليمات لاستخدام نموذج الوضع عدم الاتصال llama.cpp في أداة تحرير AIChatPlus.

* أولاً، قم بتنزيل النموذج غير المتصل من موقع HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

ضع النموذج في مجلد معيّن، مثل وضعه في دليل المشروع اللعبة تحت Content/LLAMA

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

افتح أداة تحرير AIChatPlus: Tools -> AIChatPlus -> AIChat، وأنشئ جلسة دردشة جديدة ثم افتح صفحة إعدادات الجلسة

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

* قم بتعيين API إلى Cllama، وافتح إعدادات API المخصصة، ثم أضف مسار بحث النموذج، واختر النموذج.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

* ابدأ الدردشة!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###أداة التحرير تستخدم النموذج غير المتصل Cllama (llama.cpp) لمعالجة الصور

(https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)و [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)。

تعيين نموذج الجلسة:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

بدء الدردشة عند إرسال الصورة

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###تستخدم الشيفرة نموذجًا غير متصل بالإنترنت Cllama(llama.cpp)

توضح الفقرات التالية كيفية استخدام نموذج عدم الاتصال llama.cpp في الكود.

* أولاً، يحتاج أيضاً إلى تنزيل ملف النموذج إلى Content/LLAMA

* تعديل الشيفرة لإضافة أمر، وإرسال رسالة إلى النموذج غير المتصل داخل هذا الأمر.

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

بمجرد إعادة تجميعها، يمكنك استخدام الأوامر في محرر Cmd لرؤية نتائج الإخراج للنموذج الكبير في سجل OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###استخدام النموذج الغير متصل llama.cpp في التصميم الهندسي

以下说明如何在蓝图中使用离线模型 llama.cpp  
توضح الخطوات التالية كيفية استخدام نموذج لاما.كوم في المخطط.

* انقر بزر الماوس الأيمن في المخطط لإنشاء عقدة `Send Cllama Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

إنشاء عقدة Options وتعيين `Stream=true، ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

إنشاء رسائل، وإضافة رسالة النظام ورسالة المستخدم على التوالي.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* إنشاء Delegate لاستقبال معلومات ناتج النموذج، وطباعتها على الشاشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* يبدو أن المخطط الكامل يشبه هذا، قم بتشغيل المخطط، وسترى شاشة اللعبة تعرض الرسائل التي تعيدها النماذج الكبيرة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###يستخدم المحرر محادثات OpenAI

* افتح أداة الدردشة Tools -> AIChatPlus -> AIChat، أنشئ جلسة دردشة جديدة New Chat، واضبط جلسة ChatApi على OpenAI، واضبط معلمات الواجهة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

ابدأ الدردشة:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

قم بتغيير النموذج إلى GPT-4o / GPT-4o-mini، يمكنك استخدام خاصية التحليل البصري لصور OpenAI

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###المحرر يستخدم OpenAI لمعالجة الصور (إنشاء/ تعديل/ تغيير)

إنشاء محادثة جديدة للصور في أداة الدردشة، وتعديل إعدادات المحادثة لـ OpenAI وضبط المعلمات.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

* إنشاء صورة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

* تعديل الصورة، قم بتغيير نوع محادثة الصورة إلى تعديل، وقم بتحميل صورتين، واحدة هي الصورة الأصلية، والأخرى هي القناع حيث تمثل الأماكن透明 (قناة ألفا تساوي 0) الأماكن التي تحتاج إلى تعديل.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

قم بتعديل نوع الدردشة الصورية إلى "تبديل" وقم برفع صورة. سوف تُعيد OpenAI صورة مُعدلة من الصورة الأصلية.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###蓝图使用 OpenAI 模型聊天的阿拉伯语翻译是：

"يستخدم النموذج المخطط دردشة نموذج OpenAI"

في العنصر الرئيسي، انقر بزر الماوس الأيمن لإنشاء وحدة "Send OpenAI Chat Request In World"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

* إنشاء عقدة Options، وتعيين `Stream=true, Api Key="مفتاح API الخاص بك من OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

أنشئ رسائل جديدة، وأضف رسالة نظام ورسالة مستخدم على التوالي.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* إنشاء Delegate لاستقبال معلومات ناتج النموذج، وعرضها على الشاشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* يبدو أن المخطط الكامل يبدو هكذا، عند تشغيل المخطط، يمكنك رؤية شاشة اللعبة تطبع الرسالة التي يعيدها النموذج الكبير.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###ترجمة النص إلى اللغة العربية:

صُممت الصورة باستخدام OpenAI.

* انقر بزر الماوس الأيمن على المخطط لإنشاء عقدة `Send OpenAI Image Request`، واضبط `In Prompt="فراشة جميلة"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

* أنشئ عقدة Options، واضبط `Api Key="مفتاح API الخاص بك من OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

ربط حدث On Images وحفظ الصورة على القرص الصلب المحلي

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

* تبدو الخطة كاملة على النحو التالي، عند تشغيل الخطة، يمكنك رؤية الصورة محفوظة في المكان المحدد.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###يستخدم المحرر Azure.

* إنشاء محادثة جديدة (New Chat)، تغيير ChatApi إلى Azure، وضبط معلمات Azure Api.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

ابدأ الدردشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###استخدمت البرنامج لإنشاء صورة باستخدام Azure.

إنشاء جلسة دردشة الصور الجديدة (New Image Chat)، قم بتغيير ChatApi إلى Azure، وقم بضبط معلمات Api لـ Azure. يرجى ملاحظة، إذا كانت النموذج dall-e-2، يجب ضبط معلمات الجودة والنمط (Quality و Stype) على not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

* ابدأ الدردشة واسمح لـ Azure بإنشاء صورة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###استخدام Azure للدردشة

قم بإنشاء مخطط كما هو موضح، واضبط خيارات Azure، ثم انقر على التشغيل، لتتمكن من رؤية معلومات الدردشة التي تعيدها Azure مطبوعة على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###استخدام Azure لإنشاء صور蓝图

قم بإنشاء المخطط التالي، واضبط خيارات Azure، ثم اضغط على تشغيل. إذا تم إنشاء الصورة بنجاح، ستظهر على الشاشة رسالة "تم إنشاء الصورة".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

وفقًا لإعدادات المخطط أعلاه، سيتم حفظ الصورة في المسار D:\Dwnloads\butterfly.png

## Claude

###يستخدم المحرر Claude للدردشة وتحليل الصور

* إنشاء محادثة جديدة (New Chat)، قم بتغيير ChatApi إلى Claude، واضبط معلمات Api الخاصة بـ Claude

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

* ابدأ المحادثة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###蓝图使用 Claude 聊天和分析图片  
استخدام خطة العمل في الدردشة مع Claude وتحليل الصور

أنشئ نود "Send Claude Chat Request" بالنقر اليمين في الرسم التخطيطي.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

أنشئُواَ ًعُقُدَ إخْتِيَارَاتْ وَحَدِدُوا `Stream=true, Api Key="your api key from Clude", Max Output Tokens=1024`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

* إنشاء الرسائل، وإنشاء Texture2D من ملف، وإنشاء AIChatPlusTexture من Texture2D، ثم إضافة AIChatPlusTexture إلى الرسالة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

إلى اللغة العربية:

* كما هو موضح في البرنامج التعليمي أعلاه، أنشئ حدثًا وقم بطباعة المعلومات على شاشة اللعبة.

النسخة الكاملة من الخطة تبدو بهذا الشكل، عند تشغيل الخطة، يمكنك رؤية رسالة تعود بناء النموذج الكبير المطبوع على شاشة اللعبة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###الحصول على Ollama

يمكن الحصول على حزمة التثبيت محليًا من خلال موقع Ollama الرسمي: [ollama.com](https://ollama.com/)

يمكن استخدام Ollama من خلال واجهة Ollama التي يوفرها الآخرون.

###محرر يستخدم Ollama للدردشة وتحليل الصور

* 新建会话（New Chat），把 ChatApi 改为 Ollama，并设置 Ollama 的 Api 参数。如果是文本聊天，则设置模型为文本模型，如 llama3.1；如果需要处理图片，则设置模型为支持 vision 的模型，例如 moondream。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

* بدء المحادثة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###الخطط استخدم Ollama للدردشة وتحليل الصور

قم بإنشاء المخطط التالي، واضبط خيارات Ollama، ثم انقر على التشغيل، وستتمكن من رؤية معلومات الدردشة التي تعيدها Ollama على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###استخدام Gemini كمحرر

* إنشاء محادثة جديدة (New Chat)، قم بتغيير ChatApi إلى Gemini، وقم بضبط معلمات Api الخاصة بـ Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

بدء المحادثة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###يستخدم المحرر Gemini لإرسال الصوتية.

* اختر قراءة الصوت من ملف / قراءة الصوت من الأصول / تسجيل الصوت من الميكروفون، لإنتاج الصوت المراد إرساله

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

* ابدأ الدردشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###استخدام الدردشة مع جمنيس

إنشاء مخطط كما يلي، إعداد خيارات Gemini، ثم النقر على تشغيل، ستتمكن من رؤية معلومات الدردشة التي أرجعتها Gemini على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###استخدم النسخة الزرقاء من Gemini لإرسال الصوت.

قم بإنشاء المخطط التالي، وضبط تحميل الصوت، وضبط خيارات Gemini، ثم انقر على تشغيل، وستتمكن من رؤية الرسالة الناتجة من معالجة Gemini للصوت مطبوعة على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###محرر يستخدم Deepseek

قم بإنشاء دردشة جديدة (New Chat)، غيّر ChatApi إلى OpenAi، وضبط معلمات Deepseek's Api. أضف نماذج مرشحة جديدة تسمى deepseek-chat، وقم بتعيين النموذج كـ deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

* بدء المحادثة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###استخدم Deepseek للدردشة

قم بإنشاء المخطط التالي، واضبط خيارات الطلب المتعلقة بـ Deepseek، بما في ذلك النموذج، وعنوان القاعدة، وعنوان نقطة النهاية، ومفتاح API وغيرها من المعلمات. انقر على تشغيل، وستتمكن من رؤية المعلومات التي تم إرجاعها من محادثة Gemini على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##سجل التحديثات

### v1.5.1 - 2025.01.30

####وظيفة جديدة

لا تُسمح إلا لجيميني بتنفيذ الصوت

تحسين طريقة الحصول على بيانات PCMData، وفك ضغط بيانات الصوت عند توليد B64

* طلب زيادة ردين على OnMessageFinished و OnImagesFinished

تحسين طريقة Gemini، والحصول على الطريقة تلقائياً استناداً إلى bStream

إضافة بعض وظائف النموذج الأزرق لتسهيل تحويل Wrapper إلى أنواع فعلية، والحصول على رسالة الاستجابة والخطأ.

#### Bug Fix

إصلاح مشكلة استدعاء Request Finish مرات عديدة

### v1.5.0 - 2025.01.29

####ميزة جديدة

* دعم إرسال الصوت إلى جمنيا

* أدوات المحرر تدعم إرسال الصوت والتسجيلات

#### Bug Fix

* إصلاح خطأ فشل نسخة الجلسة

### v1.4.1 - 2025.01.04

####إصلاح المشاكل

يمكن لأدوات الدردشة دعم إرسال الصور فقط دون إرسال الرسائل.

* 修复 OpenAI 接口发送图片问题失败文图

إصلاح خطأ في ضبط أدوات الدردشة OpanAI وAzure الذي تغاضى عن إعدادات الجودة (Quality)، الأسلوب (Style)، ونسخة الواجهة (ApiVersion)=

### v1.4.0 - 2024.12.30

####الميزة الجديدة

（دعم للوظيفة التجريبية）Cllama（llama.cpp）يدعم النماذج متعددة الأوضاع ويتمكن من معالجة الصور

* تم إضافة تلميحات تفصيلية لجميع معلمات نوع المخططات.

### v1.3.4 - 2024.12.05

####الميزة الجديدة

OpenAI تدعم واجهة رؤية vision api.

####إصلاح المشاكل

* إصلاح الخطأ عند تشغيل OpenAI stream=false

### v1.3.3 - 2024.11.25

####ميزة جديدة

* دعم UE-5.5

####إصلاح المشاكل

قم بإصلاح مشكلة عدم تنفيذ جزء من التصاميم الزرقاء

### v1.3.2 - 2024.10.10

####إصلاح المشكلة

* إصلاح انهيار cllama عند إيقاف الطلب يدويًا

إصلاح مشكلة عدم العثور على ملفات ggml.dll وllama.dll أثناء تعبئة إصدار التنزيل الخاص بنظام التشغيل Windows في متجر التطبيقات.

عند إنشاء الطلب ، يتم التحقق مما إذا كان ذلك في GameThread.

### v1.3.1 - 2024.9.30

####الميزة الجديدة

أضف SystemTemplateViewer جديد لعرض واستخدام المئات من قوالب إعدادات النظام.

####إصلاح المشكلة

* إصلاح المكون الإضافي الذي تم تنزيله من السوق، llama.cpp لا يمكنه العثور على مكتبة الروابط.

إصلاح مشكلة الطريق الطويل لـ LLAMACpp

* إصلاح خطأ ربط llama.dll بعد حزمة Windows

* إصلاح مشكلة قراءة مسار الملفات على ios/android

* إصلاح خطأ اسم إعدادات Cllame

### v1.3.0 - 2024.9.23

####من فضلك، أنا متخصص في الترجمة الاحترافية. يرجى تقديم طلب يتضمن محتوى محدد للترجمة.

دمجت llama.cpp، مع دعم التنفيذ الغير متصل بالإنترنت لنماذج كبيرة محليا

### v1.2.0 - 2024.08.20

####ميزة جديدة

دعم تحرير الصور/تغيير الصور من OpenAI.

تدعم واجهة Ollama API، وتدعم الحصول التلقائي على قائمة النماذج المدعومة من Ollama.

### v1.1.0 - 2024.08.07

####الوظيفة الجديدة

دعم الخطة الزرقاء

### v1.0.0 - 2024.08.05

####الميزة الجديدة

وظائف كاملة وأساسية

* دعم OpenAI و Azure و Claude و Gemini

* أداة دردشة بمحرر متكامل الميزات

--8<-- "footer_ar.md"


> نصّ هذه المشاركة تم ترجمته باستخدام ChatGPT. الرجاء تقديم [**ردود فعل**](https://github.com/disenone/wiki_blog/issues/new)يرجى تحديد أي نقص. 
