---
layout: post
title: Get Started
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini, Ollama]
description: Get Started
---
<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Get Started" />

# C++ 篇 - Get Started

## 核心代码介绍

目前插件分成以下几个模块：

* **AIChatPlusCommon**: 运行时模块 (Runtime)，负责处理各种 AI API 接口发送请求和解析回复内容。

* **AIChatPlusEditor**: 编辑器模块 (Editor)， 负责实现编辑器 AI 聊天工具。

* **AIChatPlusCllama**: 运行时模块 (Runtime)，负责封装 llama.cpp 的接口和参数，实现离线执行大模型

* **Thirdparty/LLAMACpp**: 运行时第三方模块 (Runtime)，整合了 llama.cpp 的动态库和头文件。

具体负责发送请求的 UClass 是 FAIChatPlus_xxxChatRequest，每种 API 服务都分别有独立的 Request UClass。请求的回复通过 UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase 两种 UClass 来获取，只需要注册相应的回调委托。

发送请求之前需要先设置好 API 的参数和发送的消息，这块是通过 FAIChatPlus_xxxChatRequestBody 来设置。回复的具体内容也解析到 FAIChatPlus_xxxChatResponseBody 中，收到回调的时候可以通过特定接口获取 ResponseBody。

## 代码使用离线模型 Cllama(llama.cpp)

以下说明如何在代码中使用离线模型 llama.cpp

首先，同样需要下载模型文件到 Content/LLAMA 下

修改代码添加一条命令，并在命令里面给离线模型发送消息

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

重新编译后，在编辑器 Cmd 中使用命令，便可在日志 OutputLog 看到大模型的输出结果

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

--8<-- "footer.md"
