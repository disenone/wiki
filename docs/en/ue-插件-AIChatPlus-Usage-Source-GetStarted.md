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

#C++ Article - Get Started

##Introduction to core code

Currently, the plugin is divided into the following modules:

* **AIChatPlusCommon**: Runtime module responsible for handling various AI API interface requests and parsing response content.

* **AIChatPlusEditor**: Editor module responsible for implementing the AI chat tool within the editor.

* **AIChatPlusCllama**: The Runtime module is responsible for encapsulating the interface and parameters of llama.cpp, enabling the offline execution of large models.

* **Thirdparty/LLAMACpp**: Runtime third-party module that integrates the dynamic library and header files of llama.cpp.

The specific UClass responsible for sending requests is FAIChatPlus_xxxChatRequest. Each API service has its own unique Request UClass. The responses to requests are obtained through two types of UClass, UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase, and only require registering the corresponding callback delegates.

Before sending a request, you need to set the API parameters and the message to be sent. This is done by setting up the FAIChatPlus_xxxChatRequestBody. The specific response content is also parsed into the FAIChatPlus_xxxChatResponseBody. When receiving a callback, you can retrieve the ResponseBody through a specific interface.

##The code uses the offline model Cllama (llama.cpp).

The following explains how to use the offline model llama.cpp in the code.

First, you also need to download the model file to Content/LLAMA.

Modify the code to add a command and send a message to the offline model within the command.

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

After recompiling, by using the command in the editor Cmd, you can see the output results of the large model in the log OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

--8<-- "footer_en.md"


> This post has been translated using ChatGPT. Please provide feedback in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
