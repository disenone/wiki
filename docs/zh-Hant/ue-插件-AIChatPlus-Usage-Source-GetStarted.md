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

#C++ 章節 - 開始吧

##核心程式碼介紹

目前插件分為以下幾個模組：

AIChatPlusCommon: Runtime 模块，負責處理各種 AI API 介面的請求和解析回應內容。

AIChatPlusEditor: 編輯器模組(Editor)，負責實現編輯器 AI 聊天工具。

AIChatPlusCllama: 運行時模塊（Runtime），負責封裝 llama.cpp 的介面和參數，實現離線執行大型模型

Thirdparty/LLAMACpp: 在運行時整合了 llama.cpp 的動態庫和頭文件的第三方模塊。

負責發送請求的 UClass 是 FAIChatPlus_xxxChatRequest，每一種 API 服務都有獨立的 Request UClass。回應請求通過 UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase 兩種 UClass 進行處理，只需要註冊相應的回調函數即可。

在發送請求之前，需要先設定好 API 的參數和發送的訊息，這部分是通過 FAIChatPlus_xxxChatRequestBody 來設定。回覆的具體內容也解析到 FAIChatPlus_xxxChatResponseBody 中，收到回撥的時候可以透過特定介面獲取 ResponseBody。

##代碼使用離線模型 Cllama(llama.cpp)

以下說明了如何在程式碼中使用離線模型 llama.cpp。

首先，同樣需要將模型檔案下載至 Content/LLAMA 資料夾下。

修改程式碼以新增一個指令，並在指令中向離線模型發送訊息。

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

重新編譯後，在編輯器 Cmd 中使用命令，便可在日誌 OutputLog 看到大模型的輸出結果。

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

--8<-- "footer_tc.md"


> 這篇文章是由 ChatGPT 翻譯的，請在 [**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
