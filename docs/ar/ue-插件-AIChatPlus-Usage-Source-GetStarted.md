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

#المقالة عن C++ - البدء

##مقدمة للشيفرة الأساسية

النص المُطلوب ترجمته هو: 

"目前插件分成以下几个模块："

AIChatPlusCommon: وحدة التشغيل (Runtime)، المسؤولة عن معالجة طلبات إرسال وتحليل محتوى ردود واجهات برمجة التطبيقات الذكية المختلفة.

AIChatPlusEditor: وحدة التحرير (Editor) ، المسؤولة عن تنفيذ أدوات دردشة الذكاء الاصطناعي.

AIChatPlusCllama: وحدة التشغيل (Runtime) ، مسؤولة عن تغليف واجهة ومعلمات llama.cpp ، لتنفيذ نماذج كبيرة دون اتصال بالإنترنت

ثريد بارتي/إل إل أيه أم أي سي بي بي: الوحدة النمطية الطرفية للتشغيل (Runtime) ، تضمنت مكتبة llama.cpp الديناميكية والملفات الرأسية.

الـ UClass المسؤولة عن إرسال الطلب هو FAIChatPlus_xxxChatRequest، كل خدمة API لها UClass Request مستقل. يتم الحصول على رد الطلب من خلال UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase UClass، ما عليك سوى تسجيل الوفد المناسب.

قبل إرسال الطلب، يجب تعيين معلمات API ورسالة الإرسال أولاً، يتم ذلك من خلال تعيين FAIChatPlus_xxxChatRequestBody. يتم تحليل المحتوى المحدد للرد في FAIChatPlus_xxxChatResponseBody، ويمكن الحصول على ResponseBody عند استقبال الاستدعاء عبر واجهة معينة.

##يستخدم الكود نموذجًا غير متصل Cllama (llama.cpp)

يوضح النص التالي كيفية استخدام نموذج llama.cpp في البرنامج.

أولاً، يجب تنزيل ملف النموذج إلى المسار Content/LLAMA.

قم بتعديل الشيفرة لإضافة أمر جديد، وارسل رسالة إلى النموذج الغير متصل في داخل الأمر.

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

بعد إعادة الترجمة، يمكن استخدام الأوامر في محرر Cmd لرؤية نتائج النموذج الكبير في سجل الإخراج OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

--8<-- "footer_ar.md"


> هذه المشاركة تمت ترجمتها باستخدام ChatGPT، يرجى تقديم [**تعليقات**](https://github.com/disenone/wiki_blog/issues/new)يرجى تحديد أي نقص. 
