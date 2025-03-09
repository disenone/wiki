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

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Get Started" />

#البدء في C++

##تقديم شرح للكود الأساسي

حاليا، الإضافة مقسمة إلى الوحدات التالية:

* **AIChatPlusCommon**: وحدة التشغيل (Runtime) ، المسؤولة عن معالجة طلبات إرسال وتحليل محتوى ردود الواجهة البرمجية لتطبيق الذكاء الاصطناعي المختلفة.

وظيفة AIChatPlusEditor هي تنفيذ وحدة التحرير (Editor)، التي تقوم بتنفيذ أداة الدردشة AI في القاعدة de données.

* **AIChatPlusCllama**: وحدة التشغيل (Runtime) المسؤولة عن تغليف واجهة ومعلمات llama.cpp، لتنفيذ نماذج كبيرة بشكل غير متصل عند التشغيل

Thirdparty/LLAMACpp: "Runtime" وحدة خارجية تجمع بين مكتبة الرموز الديناميكية llama.cpp وملفات الرأس.

الـ UClass المسؤولة عن إرسال الطلب هو FAIChatPlus_xxxChatRequest، كل خدمة API لها UClass طلب مستقل. يتم الحصول على رد الطلب عن طريق UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase اللذين ينبغي تسجيل التابع المناسب فقط.

قبل إرسال الطلب، يجب تعيين معلمات API والرسالة المُرسَلة أولاً، يتم تعيين هذا باستخدام FAIChatPlus_xxxChatRequestBody. يتم تحليل محتوى الإجابة أيضاً إلى FAIChatPlus_xxxChatResponseBody، يمكن الحصول على ResponseBody من خلال واجهة معينة عند استقبال الاستدعاء.

##الرمز يستخدم نموذجًا غير متصل بالإنترنت Cllama(llama.cpp)

يوضح النص التالي كيفية استخدام النموذج الغير متصل llama.cpp في الشيفرة.

أولاً، يجب تنزيل ملف النموذج إلى مجلد Content/LLAMA بنفس الطريقة.

قم بتعديل الشيفرة لإضافة أمر جديد، وأرسل رسالة إلى النموذج الغير متصل به من داخل الأمر.

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

بعد إعادة الترجمة، يمكنك رؤية نتائج إخراج النموذج الكبير في سجل OutputLog عند استخدام الأمر في محرر Cmd.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

--8<-- "footer_ar.md"


> تمت ترجمة هذه المشاركة باستخدام ChatGPT، يرجى إعطاء [**ردود فعل**](https://github.com/disenone/wiki_blog/issues/new)وضع الإشارة إلى أية نقص أو غياب. 
