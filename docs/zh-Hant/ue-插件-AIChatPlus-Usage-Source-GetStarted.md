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

#C++ 篇 - 快速入門

##模組介紹

插件可分為以下幾個模塊：

* **AIChatPlusCommon**：運行時模組（Runtime），負責處理各類 AI API 介面的請求發送及回覆內容解析。
* **AIChatPlus編輯器**: 編輯器模組 (Editor)，負責實現編輯器 AI 聊天工具。
* **AIChatPlusCllama**：運行時模組 (Runtime)，負責封裝 llama.cpp 的介面與參數，實現離線執行大型模型。
* **第三方/LLAMACpp**：運行時第三方模組 (Runtime)，整合了 llama.cpp 的動態庫和標頭檔。

##核心概念

在使用源碼之前，需要了解幾個核心類別及其關係：

###請求

`UAIChatPlus_ChatRequestBase` 是所有聊天請求的基類。每種 API Provider 都有對應的子類：

* `UAIChatPlus_OpenAIChatRequest` - OpenAI 聊天請求
* `UAIChatPlus_AzureChatRequest` - Azure 聊天請求
* `UAIChatPlus_ClaudeChatRequest` - Claude 聊天請求
* `UAIChatPlus_GeminiChatRequest` - Gemini 聊天請求
* `UAIChatPlus_OllamaChatRequest` - Ollama 聊天請求
* `UAIChatPlus_CllamaChatRequest` - Cllama 離線模型請求
* `UAIChatPlus_CllamaServerChatRequest` - CllamaServer 本地伺服器請求

Request 物件負責配置請求參數、發送請求、接收回調。

###處理器（Handler）

`UAIChatPlus_ChatHandlerBase` 是一個可選的處理器類，用於統一管理請求的回調。

處理器提供了以下的委託：

* `OnStarted` - 請求開始時觸發
* `OnMessage` - 接收串流訊息時觸發（串流輸出）
* `OnUpdated` - 當收到更新時觸發
* `OnFinished` - 請求完成時觸發
* `OnFailed` - 當請求失敗時觸發

**何時使用 Handler？**

當需要統一管理多個請求的回調邏輯時
* 當需要在藍圖和 C++ 之間共享回調邏輯時
* 直接使用 Request 的委託（如 `OnStartedListeners`）同樣可以實現回調監聽

###選項

每種 API Provider 都對應一個 Options 結構體，用於配置 API 參數：

* `FAIChatPlus_OpenAIChatRequestOptions` - OpenAI 選項（ApiKey、Model、Temperature 等）
* `FAIChatPlus_ClaudeChatRequestOptions` - Claude 選項
* `FAIChatPlus_GeminiChatRequestOptions` - Gemini 選項
* 等等……

Options 包含了 API 連接所需的所有配置，如 API Key、端點 URL、模型名稱、生成參數等。

###訊息（消息）

`FAIChatPlus_ChatRequestMessage` 是發送給 AI 的訊息結構體，包含：

* `內容` - 文本內容
* `角色` - 消息角色（系統/使用者/助理/開發者/工具）
* `Images` - 圖片陣列（Vision 功能）
* `Audios` - 音頻陣列（Audio 功能）
* `ToolCallUses` - 工具調用請求
* `ToolCallResults` - 工具呼叫結果

###回應（響應）

每種 API Provider 都有對應的 ResponseBody 結構體：

* `FAIChatPlus_OpenAIChatResponseBody`
* `FAIChatPlus_ClaudeChatResponseBody`
* 等等...

ResponseBody 包含了 AI 回傳的全部資訊，包括：訊息文字、Token 用量、工具調用、音訊輸出等。

##基礎使用流程（5 步模式）

使用AIChatPlus發送請求的基本流程如下：

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"

void SendChatRequest()
{
    // ===== 步驟 1: 創建 Handler（可選）=====
// Handler用於統一管理回調，也可以直接使用Request的委託
    TWeakObjectPtr<UAIChatPlus_ChatHandlerBase> Handler = UAIChatPlus_ChatHandlerBase::New();

    // ===== 步驟 2: 配置選項 =====
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
Options.bStream = true;  // 啟用串流輸出

    // ===== 步驟 3: 建立 Request =====
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("Hello, who are you?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    // ===== 步驟 4: 綁定回調 =====
    // 方式 A: 使用 Handler
    Handler->BindChatRequest(Request);
    Handler->OnMessage.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Stream Message: %s"), *Message);
    });
    Handler->OnFinished.AddLambda([](const FAIChatPlus_ChatResponseBodyBase& Response)
    {
        UE_LOG(LogTemp, Display, TEXT("Request Finished"));
    });
    Handler->OnFailed.AddLambda([](const FAIChatPlus_ResponseErrorBase& Error)
    {
        UE_LOG(LogTemp, Error, TEXT("Request Failed: %s"), *Error.GetDescription());
    });

    // 方式 B: 直接使用 Request 的委託（不需要 Handler）
    // Request->OnMessageListeners.AddDynamic(this, &UMyClass::OnMessageReceived);
    // Request->OnFinishedListeners.AddDynamic(this, &UMyClass::OnRequestFinished);

    // ===== 步驟 5: 發送請求 =====
    Request->SendRequest();
}
```

##簡化寫法

若無需細膩的回調控制，可使用更簡潔的寫法：

```cpp
void SendSimpleChatRequest()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System},
            {TEXT("Hello!"), EAIChatPlus_ChatRole::User}
        });

// 直接在 Request 上綁定 Lambda
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Message: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final Message: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##透過 API Provider 枚舉建立請求

如果需要根據配置動態選擇 API Provider，可以使用工廠方法：

```cpp
void CreateRequestByProvider(EAIChatPlus_ChatApiProvider Provider)
{
// 根據枚舉創建對應的 Request
    auto Request = UAIChatPlus_ChatRequestBase::CreateByApi(Provider);

    // 根據實際類型設置 Options
    switch (Provider)
    {
    case EAIChatPlus_ChatApiProvider::OpenAI:
        {
            auto OpenAIRequest = Cast<UAIChatPlus_OpenAIChatRequest>(Request);
            FAIChatPlus_OpenAIChatRequestOptions Options;
            Options.ApiKey = TEXT("your-api-key");
            OpenAIRequest->SetOptions(Options);
        }
        break;

    case EAIChatPlus_ChatApiProvider::Claude:
        {
            auto ClaudeRequest = Cast<UAIChatPlus_ClaudeChatRequest>(Request);
            FAIChatPlus_ClaudeChatRequestOptions Options;
            Options.ApiKey = TEXT("your-api-key");
            ClaudeRequest->SetOptions(Options);
        }
        break;
    // ... 其他 Provider
    }

    // 設定訊息並發送
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Hello!"), EAIChatPlus_ChatRole::User});
    Request->SetMessages(Messages);
    Request->SendRequest();
}
```

##回撥說明

###主要回調委託

| 委託 | 觸發時機 | 參數 |
|------|----------|------|
| `OnStarted` | 請求開始發送時 | 無 |
| `OnMessage` | 收到串流訊息時（每個 token） | `const FString& Message` - 累積的訊息內容 |
| `OnUpdated` | 收到回應更新時 | `const FAIChatPlus_ResponseBodyBase& Response` |
| `OnFinished` | 請求成功完成時 | `const FAIChatPlus_ResponseBodyBase& Response` |
| `OnFailed` | 請求失敗時 | `const FAIChatPlus_ResponseErrorBase& Error` |
| `OnMessageFinished` | 消息接收完成時 | `const FAIChatPlus_MessageFinishedPayload& Payload` |

###串流輸出 vs 非串流輸出

* **流式輸出** (`bStream = true`)：`OnMessage` 會多次觸發，每次回傳累積的訊息內容
* **非串流輸出** (`bStream = false`)：`OnMessage` 僅在完成時觸發一次，回傳完整訊息

##下一步

欲了解更多詳細用法，請參閱各API供應商的專題文件：

* [OpenAI / Azure 使用方式](ue-插件-AIChatPlus-Usage-Source-OpenAI.md)
* [Claude 使用](ue-插件-AIChatPlus-Usage-Source-Claude.md)
* [Gemini 使用](ue-插件-AIChatPlus-Usage-Source-Gemini.md)
* [Ollama 使用](ue-插件-AIChatPlus-Usage-Source-Ollama.md)
* [Cllama 離線模型](ue-插件-AIChatPlus-Usage-Source-Cllama.md)
* [CllamaServer 本地伺服器](ue-插件-AIChatPlus-Usage-Source-CllamaServer.md)
* [工具類](ue-插件-AIChatPlus-Usage-Source-Utils.md)

--8<-- "footer_tc.md"

> 此貼文是由 ChatGPT 翻譯的，請在[**意見回饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
