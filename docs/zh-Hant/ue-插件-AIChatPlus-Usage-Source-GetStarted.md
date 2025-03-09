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

#C++課程 - 入門指南

##核心代碼介紹

目前插件分成以下幾個模組：

**AIChatPlusCommon**：執行時模組（Runtime），負責處理各種 AI API 介面發送請求和解析回覆內容。

* **AIChatPlusEditor**: 編輯器模組 (Editor)， 負責實現編輯器 AI 聊天工具。

**AIChatPlusCllama**: 運行時模塊 (Runtime)，負責封裝 llama.cpp 的介面和參數，實現離線執行大型模型

* **Thirdparty/LLAMACpp**: Runtime第三方模組，整合了llama.cpp的動態庫和頭文件。

負責發送請求的 UClass 是 FAIChatPlus_xxxChatRequest，每種 API 服務都有獨立的 Request UClass。回覆請求則透過 UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase 兩種 UClass 來取得，只需要註冊相應的回調委託。

在發送請求之前，請確保設置好 API 參數和要發送的訊息，這些設定是通過 FAIChatPlus_xxxChatRequestBody 來完成的。回復的具體內容也可以透過 FAIChatPlus_xxxChatResponseBody 進行解析，收到回調時可以通過特定接口獲取 ResponseBody。

##程式碼使用離線模型 Cllama(llama.cpp)

以下說明如何在程式碼中使用離線模型 llama.cpp

首先，同樣需要將模型檔案下載至 Content/LLAMA 資料夾中。

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

重新編譯後，在編輯器 Cmd 中使用命令，便可在日誌 OutputLog 看到大型模型的輸出結果

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

--8<-- "footer_tc.md"


> 這則訊息是由 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
