---
layout: post
title: UE ملحق AIChatPlus وثيقة الشرح
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
description: وثيقة توضيحية لإضافة UE AIChatPlus
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#وثيقة شرح المكون الإضافي UE AIChatPlus

##المستودع العام

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##الحصول على الإضافات

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##مقدمة عن الإضافة

هذا الملحق يدعم UE5.2+.

UE.AIChatPlus هو مكون إضافي لـ UnrealEngine، يتيح التواصل مع مجموعة متنوعة من خدمات الدردشة القائمة على الذكاء الاصطناعي GPT. حاليًا، تتضمن الخدمات المدعومة OpenAI (ChatGPT, DALL-E)، Azure OpenAI (ChatGPT, DALL-E)، Claude، Google Gemini، Ollama، و llama.cpp محليًا وعبر الإنترنت. في المستقبل، ستستمر المكونات الإضافية في دعم مزودي خدمات آخرين. تعتمد الطريقة التي تم تنفيذها على طلبات REST غير المتزامنة، مما يضمن أداءً عاليًا وسهولة لدمج هذه الخدمات في تطوير UE.

في الوقت نفسه، يتضمن UE.AIChatPlus أداة محرر، يمكن استخدامها مباشرة في المحرر لتطبيق خدمات الدردشة الذكية هذه، وتوليد النصوص والصور، وتحليل الصور، وغيرها.

##إرشادات الاستخدام

###أداة دردشة المحرر

شريط القوائم أدوات -> AIChatPlus -> AIChat يمكنه فتح أداة الدردشة المحرر المقدمة بواسطة الإضافة.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


تدعم الأدوات生成 النصوص，文本聊天，生成图像，分析图像。

أداة الواجهة بشكل عام هي:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####الوظائف الرئيسية

* نموذج كبير غير متصل بالإنترنت: يدمج مكتبة llama.cpp، ويدعم التشغيل المحلي غير المتصل لنماذج كبيرة.

* دردشة نصية: انقر على زر `New Chat` في الزاوية السفلى اليسرى لإنشاء جلسة دردشة نصية جديدة.

* توليد الصور: انقر على زر "دردشة صورة جديدة" في الزاوية اليسرى السفلية لإنشاء جلسة جديدة لتوليد الصور.

* تحليل الصور: تدعم بعض خدمات الدردشة في `New Chat` إرسال الصور، مثل Claude وGoogle Gemini. يمكنك تحميل الصورة التي ترغب في إرسالها من خلال الضغط على زر 🖼️ أو 🎨 الموجود أعلى مربع الإدخال.

* دعم المخططات (Blueprint)：يدعم إنشاء طلبات API للمخططات، ويكمل وظائف الدردشة النصية، وتوليد الصور، وغيرها.

* تعيين دور الدردشة الحالي: يمكن استخدام قائمة السحب الموجودة في أعلى نافذة الدردشة لتعيين الدور الحالي للنص المرسل، ويمكن ضبط محادثة الذكاء الاصطناعي من خلال تمثيل أدوار مختلفة.

* مسح المحادثة: يمكن زر ❌ الموجود في أعلى صندوق الدردشة مسح الرسائل السابقة في المحادثة الحالية.

* نموذج الحوار: يحتوي على مئات من نماذج إعداد الحوار المدمجة، مما يسهل التعامل مع الأسئلة الشائعة.

* الإعدادات العامة: انقر على زر `Setting` في الزاوية السفلية اليسرى لفتح نافذة الإعدادات العامة. يمكنك ضبط الدردشة النصية الافتراضية، وخدمة API لتوليد الصور، وتحديد المعلمات المحددة لكل خدمة API. سيتم حفظ الإعدادات تلقائيًا في مسار المشروع `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* إعدادات المحادثة: انقر على زر الإعدادات الموجود في أعلى نافذة الدردشة لفتح نافذة إعدادات المحادثة الحالية. يدعم تعديل اسم المحادثة، وتغيير خدمة API المستخدمة في المحادثة، ويدعم أيضًا إعداد كل محادثة على حدة باستخدام معلمات API المحددة. يتم حفظ إعدادات المحادثة تلقائيًا في `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

* تعديل محتوى الدردشة: عند التحليق بالماوس فوق محتوى الدردشة، ستظهر زر إعدادات محتوى الدردشة الفردية، يدعم إعادة生成 المحتوى، تعديل المحتوى، نسخ المحتوى، حذف المحتوى، وإعادة生成 المحتوى في الأسفل (بالنسبة للمحتوى الذي يكون فيه الدور هو المستخدم)

* تصفح الصور: بالنسبة لتوليد الصور، فإن النقر على الصورة سيفتح نافذة عرض الصور (ImageViewer)، والتي تدعم حفظ الصور بتنسيق PNG/UE Texture، ويمكن عرض Texture مباشرة في متصفح المحتوى (Content Browser)، مما يسهل استخدام الصور داخل المحرر. كما تدعم الوظائف الأخرى مثل حذف الصورة، وإعادة توليد الصورة، وتوليد المزيد من الصور. بالنسبة للمحرر على نظام Windows، يدعم أيضًا نسخ الصور، حيث يمكنك نسخ الصورة مباشرة إلى الحافظة لتسهيل استخدامها. الصور المولدة أثناء الجلسة ستُحفظ تلقائيًا في مجلد كل جلسة، وعادة ما يكون المسار هو `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

الخطط:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

الإعدادات العامة:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

إعدادات المحادثة:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

تعديل محتوى الدردشة:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

عارض الصور：

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

استخدام نموذج كبير غير متصل بالإنترنت

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

نموذج الحوار

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###مقدمة عن الشيفرة الأساسية

حاليًا، يتم تقسيم الملحقات إلى عدة وحدات كما يلي:

* AIChatPlusCommon: وحدة وقت التشغيل (Runtime) ، المسؤولة عن معالجة الطلبات المرسلة من واجهات برمجة تطبيقات الذكاء الاصطناعي المختلفة وتحليل محتوى الردود.

* AIChatPlusEditor: محرر模块 (Editor) ، مسؤول عن تنفيذ أداة الدردشة الذكية التحريرية.

* AIChatPlusCllama: وحدة التشغيل (Runtime) ، مسؤولة عن تغليف واجهة وبارامترات llama.cpp، لتحقيق التنفيذ غير المتصل لنموذج كبير.

* Thirdparty/LLAMACpp: وحدة الطرف الثالث أثناء التشغيل (Runtime) ، تجمع بين مكتبة llama.cpp الديناميكية وملفات الرأس.

المسؤول المحدد عن إرسال الطلبات هو UClass FAIChatPlus_xxxChatRequest، حيث يوجد لكل خدمة API UClass Request مستقلة. يتم الحصول على ردود الطلبات من خلال نوعين من UClass، وهما UAIChatPlus_ChatHandlerBase و UAIChatPlus_ImageHandlerBase، ويكفي تسجيل التفويضات المرجعية المناسبة.

قبل إرسال الطلب، يجب أولاً إعداد معلمات واجهة برمجة التطبيقات (API) والرسالة المرسلة، ويتم ذلك من خلال FAIChatPlus_xxxChatRequestBody. يتم تحليل المحتوى المحدد للرد في FAIChatPlus_xxxChatResponseBody، وعند استلام الاستجابة يمكن الحصول على ResponseBody من خلال واجهة محددة.

يمكن الحصول على مزيد من تفاصيل الكود المصدر في متجر UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###أداة المحرر تستخدم النموذج غير المتصل Cllama(llama.cpp)

以下说明如何在 AIChatPlus 编辑器工具中使用离线模型 llama.cpp 

توضح الفقرة التالية كيفية استخدام نموذج "llama.cpp" في أداة تحرير AIChatPlus.

* أولاً، قم بتنزيل النموذج غير المتصل من موقع HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

* ضع النموذج في مجلد معين، على سبيل المثال في دليل مشروع اللعبة Content/LLAMA

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

* افتح أداة محرر AIChatPlus: الأدوات -> AIChatPlus -> AIChat، أنشئ جلسة دردشة جديدة، وافتح صفحة إعدادات الجلسة

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

* قم بضبط Api ليكون Cllama، ثم قم بتفعيل إعدادات Api المخصصة، وأضف مسار بحث النموذج، واختر النموذج.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

* ابدأ الدردشة!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###أداة المحرر تستخدم نموذجًا غير متصل Cllama(llama.cpp) لمعالجة الصور

* من موقع HuggingFace، قم بتنزيل النموذج غير المتصل MobileVLM_V2-1.7B-GGUF وضعه في الدليل Content/LLAMA: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)。

* إعداد نموذج المحادثة:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

* إرسال الصورة لبدء المحادثة

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###الرمز يستخدم النموذج غير المتصل Cllama(llama.cpp)

يوضح ما يلي كيفية استخدام النموذج غير المتصل llama.cpp في الكود.

* أولاً، تحتاج أيضًا إلى تحميل ملف النموذج إلى Content/LLAMA.

* تعديل الكود لإضافة أمر واحد، وإرسال رسالة إلى النموذج غير المتصل ضمن هذا الأمر.

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

* بعد إعادة التجميع، يمكنك استخدام الأمر في محرر Cmd لرؤية نتائج مخرجات النموذج الكبير في سجل OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###الخطط تستخدم نموذج غير متصل llama.cpp

以下说明如何在蓝图中使用离线模型 llama.cpp  
以下说明如何在蓝图中使用离线模型 llama.cpp  
以下说明如何在蓝图中使用离线模型 llama.cpp  
以下说明如何在蓝图中使用离线模型 llama.cpp  

* انقر بزر الماوس الأيمن في المخطط لإنشاء عقدة `Send Cllama Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

* إنشاء عقدة الخيارات، وتعيين `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

* إنشاء الرسائل، وإضافة رسالة نظام ورسالة مستخدم بشكل منفصل.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* إنشاء Delegate لاستقبال معلومات نموذج المخرجات وعرضها على الشاشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* يبدو أن المخطط الكامل على هذا النحو، قم بتشغيل المخطط، وستتمكن من رؤية شاشة اللعبة تعرض الرسائل التي يتم إرجاعها بواسطة النموذج الكبير.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###محرر يستخدم دردشة OpenAI

* افتح أداة الدردشة Tools -> AIChatPlus -> AIChat، أنشئ محادثة جديدة New Chat، قم بتعيين جلسة ChatApi إلى OpenAI، واضبط معلمات واجهة البرمجة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

* بدء المحادثة:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

* قم بتبديل النموذج إلى gpt-4o / gpt-4o-mini، يمكنك استخدام وظائف OpenAI البصرية لتحليل الصور.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###المحرر يستخدم OpenAI لمعالجة الصور (إنشاء/تعديل/تغيير)

* في أدوات الدردشة، قم بإنشاء محادثة صور جديدة New Image Chat، وغيّر إعدادات المحادثة إلى OpenAI، واضبط المعلمات.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

* إنشاء صورة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

* تعديل الصورة، تغيير نوع المحادثة Image Chat Type إلى Edit، ورفع صورتين، واحدة هي الصورة الأصلية والأخرى هي القناع حيث أن الأماكن الشفافة (قناة alpha تساوي 0) تمثل الأماكن التي تحتاج إلى تعديل.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

* قم بتغيير نوع المحادثة Image Chat Type إلى Variation، وارفع صورة، ستقوم OpenAI بإرجاع نسخة متغيرة من الصورة الأصلية.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###蓝图使用 OpenAI 模型聊天

* في مخطط العمل، انقر بزر الفأرة الأيمن لإنشاء عقدة `Send OpenAI Chat Request In World`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

* إنشاء عقدة الخيارات، وضبط `Stream=true, Api Key="مفتاح API الخاص بك من OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

* إنشاء رسائل، بالإضافة إلى إضافة رسالة نظام ورسالة مستخدم.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* إنشاء Delegate لاستقبال مخرجات النموذج وطباعة المعلومات على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* تبدو الخريطة الكاملة هكذا، قم بتشغيل الخريطة، وستتمكن من رؤية شاشة اللعبة تعرض الرسائل التي يرجعها النموذج الكبير.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###استخدام OpenAI لإنشاء الصور

* اضغط بالزر الأيمن لإنشاء عقدة `Send OpenAI Image Request` في المخطط، وقم بتعيين `In Prompt="فراشة جميلة"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

* إنشاء عقدة Options، وتعيين `Api Key="مفتاح API الخاص بك من OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

* ربط حدث الصور وحفظ الصور على القرص الصلب المحلي

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

* تبدو المخططات الكاملة على هذا النحو، قم بتشغيل المخطط لرؤية الصورة المحفوظة في المكان المحدد.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###المحرر يستخدم Azure

* إنشاء محادثة جديدة (New Chat)، تغيير ChatApi إلى Azure، وضبط معلمات Api الخاصة بـ Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

* ابدأ المحادثة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###المحرر يستخدم Azure لإنشاء صور

* إنشاء جلسة صور جديدة (New Image Chat)، قم بتغيير ChatApi إلى Azure، وتعيين معلمات Api الخاصة بـ Azure، لاحظ أنه إذا كان النموذج dall-e-2، يجب تعيين معلمات الجودة (Quality) ونوع الصورة (Stype) إلى not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

* ابدأ الدردشة، دع Azure ينشئ الصور

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###استخدام الدردشة في Azure

قم بإنشاء المخطط التالي، واضبط خيارات Azure، واضغط على تشغيل، وستتمكن من رؤية رسائل الدردشة التي يعيدها Azure مطبوعة على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###استخدام Azure لإنشاء صور بلوحة التصميم

أنشئ المخطط التالي، واضبط خيارات Azure، ثم انقر على تشغيل. إذا تم إنشاء الصورة بنجاح، ستظهر على الشاشة رسالة "Create Image Done".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

وفقًا لإعدادات المخطط أعلاه، ستُحفظ الصورة في المسار D:\Dwnloads\butterfly.png

## Claude

###المحرر يستخدم Claude للدردشة وتحليل الصور

* 新建会话（New Chat），把 ChatApi 改为 Claude，并设置 Claude 的 Api 参数  
* بدء محادثة جديدة (New Chat)، قم بتغيير ChatApi إلى Claude، وضبط معلمات Api لـ Claude

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

* ابدأ الدردشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###蓝图使用 Claude 聊天和分析图片  
استخدام المخطط لحديث كلود وتحليل الصور

* انقر بزر الماوس الأيمن على المخطط لإنشاء عقدة `Send Claude Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

* أنشئ عقدة الخيارات، وقم بتعيين `Stream=true, Api Key="مفتاح API الخاص بك من Clude", Max Output Tokens=1024`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

* إنشاء Messages، وإنشاء Texture2D من ملف، ثم إنشاء AIChatPlusTexture من Texture2D، وإضافة AIChatPlusTexture إلى Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

* مثل الدرس أعلاه، قم بإنشاء حدث وطباعة المعلومات على شاشة اللعبة.

* يبدو أن المخطط الكامل يبدو هكذا، عند تشغيل المخطط، ستظهر شاشة اللعبة الرسائل التي يرجعها الموديل الكبير.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###احصل على Ollama

* يمكنك الحصول على حزمة التثبيت للتثبيت المحلي من موقع Ollama الرسمي: [ollama.com](https://ollama.com/)

* يمكنك استخدام Ollama من خلال واجهة Ollama التي يقدمها أشخاص آخرون.

###المحرر يستخدم Ollama للدردشة وتحليل الصور

* 新建会话（New Chat），把 ChatApi 改为 Ollama，并设置 Ollama 的 Api 参数。如果是文本聊天，则设置模型为文本模型，如 llama3.1；如果需要处理图片，则设置模型为支持 vision 的模型，例如 moondream。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

* ابدأ الدردشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###蓝图使用 Ollama 聊天和分析图片 translates to:

استخدام Ollama في الدردشة وتحليل الصور

قم بإنشاء الرسم التخطيطي كما هو موضح، واضبط خيارات Ollama، ثم انقر على تشغيل، وستتمكن من رؤية الرسائل النصية التي يعيدها Ollama على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###المحرر يستخدم جمنيا

* إنشاء محادثة جديدة (New Chat)، قم بتغيير ChatApi إلى Gemini، وضبط معلمات Api الخاصة بـ Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

* ابدأ الدردشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###استخدام محادثة الجمنيسي في المخطط

قم بإنشاء المخطط التالي، واضبط خيارات Gemini، ثم انقر على التشغيل، وسترى المعلومات التي تم إرجاعها من Gemini تظهر على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

## Deepseek

###المحرر يستخدم Deepseek

* 新建会话（New Chat），把 ChatApi 改为 OpenAi，并设置 Deepseek 的 Api 参数。新增 Candidate Models 叫做 deepseek-chat，并把 Model 设置为 deepseek-chat
  
* إنشاء محادثة جديدة (New Chat) ، تغيير ChatApi إلى OpenAi ، وضبط معلمات Api لـ Deepseek. إضافة نموذج مرشح باسم deepseek-chat ، وضبط النموذج ليكون deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

* ابدأ الدردشة

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###استخدام Deepseek للدردشة

قم بإنشاء المخطط أدناه، وضبط خيارات الطلب المتعلقة بـ Deepseek، بما في ذلك النموذج، وعنوان قاعدة البيانات، وعنوان نقطة النهاية، ومفتاح API، وغيرها من المعلمات. انقر على زر التشغيل، وستتمكن من رؤية المعلومات التي يرجعها Gemini على الشاشة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##سجل التحديثات

### v1.5.0 - 2025.01.29

####ميزة جديدة

* دعم إرسال الصوت إلى جمنيو

* أدوات المحرر تدعم إرسال الصوت والتسجيلات

#### Bug Fix

* إصلاح عيب فشل نسخ الجلسة

### v1.4.1 - 2025.01.04

####إصلاح المشكلات

* أدوات الدردشة تدعم إرسال الصور فقط دون إرسال نصوص.

* إصلاح مشكلة إرسال الصور عبر واجهة OpenAI فشلت文图

* إصلاح مشكلة إعدادات أداة الدردشة OpanAI وAzure التي فقدت معلمات الجودة، الأسلوب، وإصدار API.

### v1.4.0 - 2024.12.30

####ميزة جديدة

* （实验性功能）Cllama(llama.cpp) تدعم النماذج متعددة الأنماط، يمكنها معالجة الصور

* تمت إضافة تفاصيل دقيقة لجميع معلمات نوع المخطط الأزرق.

### v1.3.4 - 2024.12.05

####ميزات جديدة

* OpenAI تدعم واجهة برمجة التطبيقات للرؤية

####إصلاح الأخطاء

* إصلاح الخطأ عند تعيين OpenAI stream=false

### v1.3.3 - 2024.11.25

####وظيفة جديدة

* دعم UE-5.5

####إصلاح المشكلة

* إصلاح بعض مشاكل عدم سريان المخطط

### v1.3.2 - 2024.10.10

####إصلاح المشكلة

* إصلاح انهيار cllama عند التوقف اليدوي عن الطلب

* إصلاح مشكلة عدم العثور على ملفات ggml.dll و llama.dll في إصدار تحميل متجر الإصلاحات لنظام ويندوز.

* عند إنشاء الطلب ، تحقق مما إذا كان في GameThread ، تحقق من CreateRequest في خيط اللعبة

### v1.3.1 - 2024.9.30

####ميزة جديدة

* إضافة عرض نظام نظام القوالب، والذي يتيح لك عرض واستخدام مئات من قوالب إعدادات النظام.

####إصلاح المشكلة

* إصلاح المكون الإضافي الذي تم تنزيله من المتجر، llama.cpp لا يمكن العثور على مكتبة الروابط.

* إصلاح مشكلة طول مسار LLAMACpp

* إصلاح خطأ الرابط llama.dll بعد تعبئة windows

* إصلاح مشكلة قراءة مسار الملفات على ios/android

* إصلاح اسم إعدادات Cllame الخاطئ

### v1.3.0 - 2024.9.23

####وظائف جديدة هامة

* تم دمج llama.cpp، دعم التنفيذ المحلي غير المتصل للأنموذج الكبير

### v1.2.0 - 2024.08.20

####وظيفة جديدة

* دعم تعديل الصور من OpenAI / تنويع الصور

* دعم Ollama API، ودعم الحصول التلقائي على قائمة النماذج المدعومة من قبل Ollama

### v1.1.0 - 2024.08.07

####ميزة جديدة

* دعم المخططات

### v1.0.0 - 2024.08.05

####وظيفة جديدة

* الوظائف الكاملة الأساسية

* دعم OpenAI، Azure، Claude، Gemini

* أداة دردشة مع محرر وظائف متكاملة مدمج

--8<-- "footer_ar.md"


> هذا المنشور تم ترجمته باستخدام ChatGPT، يرجى إرسال [**تعليق**](https://github.com/disenone/wiki_blog/issues/new)أي نقاط نسيان تم الإشارة إليها. 
