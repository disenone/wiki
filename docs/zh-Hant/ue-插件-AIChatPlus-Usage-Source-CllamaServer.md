---
layout: post
title: CllamaServer
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
- llama.cpp
- Local Server
description: CllamaServer
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - CllamaServer" />

#C++ 篇 - Cllama伺服器

本文檔介紹如何在 C++ 中使用 CllamaServer 管理本機 AI 伺服器並發送聊天請求。

CllamaServer 基於 llama.cpp 的 server 模式運行，提供與 OpenAI API 相容的本機服務，支援多客戶端並行請求。

##與 Cllama 的區別

| 特性 | Cllama | Cllama伺服器 |
|------|--------|--------------|
| 模式 | 直接推理 | HTTP 伺服器 |
| 多客戶端 | 否 | 是 |
| API 風格 | 自訂 | OpenAI 相容 |
| 網路存取 | 否 | 選用 |
| 工具呼叫 | 否 | 是 |

##準備工作

在使用前，請確保：

1. **下載 GGUF 模型檔案**：從 [Hugging Face](https://huggingface.co)下載相容的 GGUF 格式模型檔案。

2. 在專案的 `.Build.cs` 檔案中新增模組相依性：

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

3. 包含必要的標頭檔：

```cpp
#include "Common_CllamaServer/AIChatPlus_CllamaServer.h"
#include "Common_CllamaServer/AIChatPlus_CllamaServerChatRequest.h"
```

##伺服器管理

###啟動伺服器（基礎）

```cpp
#include "Common_CllamaServer/AIChatPlus_CllamaServer.h"

UPROPERTY()
UAIChatPlus_CllamaServer* LocalServer = nullptr;

void UMyClass::StartCllamaServer()
{
// 設定伺服器參數
    FAIChatPlus_CllamaServerParam Params;
    Params.Model = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
Params.NGpuLayers = -1;      // -1 = 自動分配 GPU 層數
Params.Port = 0;             // 0 = 自動分配可用端口
    Params.Host = TEXT("127.0.0.1");

    // 創建並啟動伺服器
    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params);

// 綁定伺服器啟動回調
    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnServerStarted);
    LocalServer->OnStoppedListeners.AddDynamic(this, &UMyClass::OnServerStopped);
    LocalServer->OnFailedListeners.AddDynamic(this, &UMyClass::OnServerFailed);

// 啟動伺服器（開始啟動流程）
    LocalServer->Activate();
}

void UMyClass::OnServerStarted(FGuid ServerID)
{
// 取得伺服器資訊
    FAIChatPlus_CllamaServerInfo Info;
    if (LocalServer->GetServerInfo(Info))
    {
        UE_LOG(LogTemp, Display, TEXT("Server started at: %s"), *Info.HttpAddress);
        UE_LOG(LogTemp, Display, TEXT("Port: %d"), Info.Port);
    }
}

void UMyClass::OnServerStopped(FGuid ServerID)
{
    UE_LOG(LogTemp, Display, TEXT("Server stopped: %s"), *ServerID.ToString());
}

void UMyClass::OnServerFailed(FGuid ServerID, const FString& ErrorMessage)
{
    UE_LOG(LogTemp, Error, TEXT("Server failed: %s"), *ErrorMessage);
}
```

###使用 Handler 管理伺服器

```cpp
#include "Common_CllamaServer/AIChatPlus_CllamaServer.h"
#include "Common_CllamaServer/AIChatPlus_CllamaServerHandler.h"

void UMyClass::StartServerWithHandler()
{
    FAIChatPlus_CllamaServerParam Params;
    Params.Model = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Params.NGpuLayers = 99;
    Params.Port = 8080;

// 建立處理器
    auto ServerHandler = UAIChatPlus_CllamaServerHandler::CreateHandler();

// 綁定原生回調（非 Dynamic）
    ServerHandler->OnStarted.AddLambda([](FGuid ServerID)
    {
        UE_LOG(LogTemp, Display, TEXT("Server started: %s"), *ServerID.ToString());
    });

    ServerHandler->OnStopped.AddLambda([](FGuid ServerID)
    {
        UE_LOG(LogTemp, Display, TEXT("Server stopped: %s"), *ServerID.ToString());
    });

    ServerHandler->OnFailed.AddLambda([](FGuid ServerID, const FString& Error)
    {
        UE_LOG(LogTemp, Error, TEXT("Server failed: %s - %s"), *ServerID.ToString(), *Error);
    });

// 使用 Handler 建立伺服器
    LocalServer = UAIChatPlus_CllamaServer::CreateServerWithHandler(Params, ServerHandler);
    LocalServer->Activate();
}
```

###指定伺服器 ID

```cpp
void UMyClass::StartServerWithCustomID()
{
    FAIChatPlus_CllamaServerParam Params;
    Params.Model = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Params.NGpuLayers = 99;

// 指定自訂 Server ID（便於後續透過 ID 管理）
    FGuid CustomServerID = FGuid::NewGuid();

    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params, CustomServerID);

    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnServerStarted);
    LocalServer->Activate();
}
```

###停止伺服器

```cpp
void UMyClass::StopServer()
{
    if (LocalServer)
    {
        LocalServer->StopServer();
    }
}

// 透過 ID 停止伺服器
void UMyClass::StopServerByID(const FGuid& ServerID)
{
    UAIChatPlus_CllamaServer::StopServerByID(ServerID);
}

// 停止所有伺服器
void UMyClass::StopAllServers()
{
    UAIChatPlus_CllamaServer::StopAllServers();
}
```

###查詢伺服器狀態

```cpp
void UMyClass::CheckServerStatus()
{
// 檢查當前伺服器實例
    if (LocalServer && LocalServer->IsRunning())
    {
        FString Host = LocalServer->GetHost();
        int32 Port = LocalServer->GetPort();
        FString Address = LocalServer->GetAddress();

        UE_LOG(LogTemp, Display, TEXT("Server running at: %s:%d"), *Host, Port);
    }

// 透過 ID 檢查伺服器狀態
    FGuid ServerID = LocalServer->GetServerID();
    if (UAIChatPlus_CllamaServer::IsServerRunning(ServerID))
    {
        FAIChatPlus_CllamaServerInfo Info = UAIChatPlus_CllamaServer::GetServerInfoByID(ServerID);
        UE_LOG(LogTemp, Display, TEXT("Server info: %s"), *Info.HttpAddress);
    }
}

void UMyClass::ListAllServers()
{
    TArray<FGuid> AllServerIDs = UAIChatPlus_CllamaServer::GetAllServerIDs();

    for (const FGuid& ServerID : AllServerIDs)
    {
        FAIChatPlus_CllamaServerInfo Info = UAIChatPlus_CllamaServer::GetServerInfoByID(ServerID);
        UE_LOG(LogTemp, Display, TEXT("Server: %s - Running: %s"),
            *ServerID.ToString(),
            Info.bIsRunning ? TEXT("Yes") : TEXT("No"));
    }
}
```

##文本聊天

###基礎文字聊天

```cpp
#include "Common_CllamaServer/AIChatPlus_CllamaServerChatRequest.h"

void UMyClass::SendCllamaServerChatRequest()
{
    // 確保伺服器已啟動
    if (!LocalServer || !LocalServer->IsRunning())
    {
        UE_LOG(LogTemp, Error, TEXT("Server is not running"));
        return;
    }

    // 設定請求選項（繼承自 OpenAI 風格）
    FAIChatPlus_CllamaServerChatRequestOptions Options;
Options.BaseUrl = LocalServer->GetAddress();  // 例如 "http://127.0.0.1:8080"
    Options.Model = TEXT("local-model");          // 模型名稱（可自定義）
    Options.bStream = true;
    Options.Temperature = 0.8f;

    // 建立訊息
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is the meaning of life?"), EAIChatPlus_ChatRole::User});

    // 建立請求
    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// 綁定回調
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("CllamaServer: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Token Usage: %s"), *Response.Usage.GetDescription());
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_ResponseErrorBase>();
        UE_LOG(LogTemp, Error, TEXT("Request Failed: %s"), *Error.GetDescription());
    });

// 傳送請求
    Request->SendRequest();
}
```

###多輪對話

```cpp
// 成員變量
TArray<FAIChatPlus_ChatRequestMessage> CllamaServerConversation;

void UMyClass::InitializeCllamaServerChat()
{
    CllamaServerConversation.Empty();
    CllamaServerConversation.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}

void UMyClass::SendMessage(const FString& UserMessage)
{
    CllamaServerConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    FAIChatPlus_CllamaServerChatRequestOptions Options;
    Options.BaseUrl = LocalServer->GetAddress();
    Options.bStream = true;

    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(
        Options, CllamaServerConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);
        FString AssistantMessage = Response.GetMessage();
        CllamaServerConversation.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});

        UE_LOG(LogTemp, Display, TEXT("Assistant: %s"), *AssistantMessage);
    });

    Request->SendRequest();
}
```

##視覺（圖片分析）

要在伺服器啟動時使用 Vision，需指定 MMProject 模型。

###啟動支援 Vision 的伺服器

```cpp
void UMyClass::StartVisionServer()
{
    FAIChatPlus_CllamaServerParam Params;

    // LLaVA 模型
    Params.Model = TEXT("D:/Models/llava-v1.6-mistral-7b.Q4_K_M.gguf");
Params.MMProj = TEXT("D:/Models/mmproj-llava-v1.6-mistral-7b-f16.gguf");  // 關鍵：MMProject 模型

    Params.NGpuLayers = 99;
    Params.Port = 8080;

    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params);
    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnVisionServerStarted);
    LocalServer->Activate();
}
```

###傳送圖片分析請求

```cpp
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithCllamaServer()
{
    if (!LocalServer || !LocalServer->IsRunning())
    {
        UE_LOG(LogTemp, Error, TEXT("Vision server is not running"));
        return;
    }

// 載入圖片
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image"));
        return;
    }

    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

    // 配置請求
    FAIChatPlus_CllamaServerChatRequestOptions Options;
    Options.BaseUrl = LocalServer->GetAddress();
    Options.bStream = true;

// 建立帶圖片的消息
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("What do you see in this image?");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(
        Options, {ImageMessage});

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Vision: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##工具呼叫（函數呼叫）

CllamaServer 支援 OpenAI 風格的 Tool Call（需搭配支援 function calling 的模型）。

###啟動支援 Tool Call 的伺服器

```cpp
void UMyClass::StartToolCallServer()
{
    FAIChatPlus_CllamaServerParam Params;
    Params.Model = TEXT("D:/Models/llama-3.1-8b-instruct-q4_k_m.gguf");
    Params.NGpuLayers = 99;
    Params.Port = 8080;
Params.bUseJinja = true;  // 工具呼叫需啟用 Jinja 模板

    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params);
    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnToolCallServerStarted);
    LocalServer->Activate();
}
```

###定義與使用工具

```cpp
void UMyClass::SendToolCallRequest()
{
    if (!LocalServer || !LocalServer->IsRunning())
    {
        UE_LOG(LogTemp, Error, TEXT("Tool call server is not running"));
        return;
    }

    FAIChatPlus_CllamaServerChatRequestOptions Options;
    Options.BaseUrl = LocalServer->GetAddress();
Options.bStream = false;  // 工具呼叫建議停用流式

// 定義工具
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = TEXT("function");
    WeatherTool.Function.Name = TEXT("get_weather");
    WeatherTool.Function.Description = TEXT("Get the current weather for a location");
    WeatherTool.Function.Parameters = TEXT(R"({
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit"
            }
        },
        "required": ["location"]
    })");

    Options.Tools.Add(WeatherTool);

    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is the weather like in Tokyo?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);

// 檢查是否有工具調用
        if (Response.Choices.Num() > 0)
        {
            const auto& Choice = Response.Choices[0];
            const auto& ToolCalls = Choice.Message.ToolCalls;

            if (ToolCalls.Num() > 0)
            {
                for (const auto& ToolCall : ToolCalls)
                {
                    UE_LOG(LogTemp, Display, TEXT("Tool Call: %s(%s)"),
                        *ToolCall.Function.Name, *ToolCall.Function.Arguments);

// 執行工具調用並繼續對話
                    ExecuteToolCall(ToolCall);
                }
            }
            else
            {
                UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
            }
        }
    });

    Request->SendRequest();
}
```

###完整 Tool Call 循環

```cpp
TArray<FAIChatPlus_ChatRequestMessage> ToolCallConversation;
FAIChatPlus_CllamaServerChatRequestOptions ToolCallOptions;

void UMyClass::InitializeToolCallChat()
{
    ToolCallOptions.BaseUrl = LocalServer->GetAddress();
    ToolCallOptions.bStream = false;

    // 定義工具
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = TEXT("function");
    WeatherTool.Function.Name = TEXT("get_weather");
    WeatherTool.Function.Description = TEXT("Get the current weather");
    WeatherTool.Function.Parameters = TEXT(R"({
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City name"}
        },
        "required": ["location"]
    })");
    ToolCallOptions.Tools.Add(WeatherTool);

    ToolCallConversation.Empty();
    ToolCallConversation.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}

void UMyClass::SendToolCallMessage(const FString& UserMessage)
{
    ToolCallConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(
        ToolCallOptions, ToolCallConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.Choices.Num() > 0)
        {
            const auto& Choice = Response.Choices[0];
            const auto& ToolCalls = Choice.Message.ToolCalls;

            if (ToolCalls.Num() > 0)
            {
// 1. 將 Assistant 的工具調用請求加入歷史紀錄
                FAIChatPlus_ChatRequestMessage AssistantMessage;
                AssistantMessage.Role = EAIChatPlus_ChatRole::Assistant;
                AssistantMessage.ToolCallUses = ToolCalls;
                ToolCallConversation.Add(AssistantMessage);

// 2. 執行工具並添加結果
                for (const auto& ToolCall : ToolCalls)
                {
                    FString Result = ExecuteToolFunction(ToolCall.Function.Name, ToolCall.Function.Arguments);

                    FAIChatPlus_ChatRequestMessage ToolResultMessage;
                    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;
                    ToolResultMessage.Content = Result;
                    ToolResultMessage.ToolCallId = ToolCall.Id;
                    ToolCallConversation.Add(ToolResultMessage);
                }

// 3. 繼續對話，讓模型處理工具結果
                ContinueToolCallConversation();
            }
            else
            {
// 一般回覆
                FString AssistantResponse = Response.GetMessage();
                ToolCallConversation.Add({AssistantResponse, EAIChatPlus_ChatRole::Assistant});
                UE_LOG(LogTemp, Display, TEXT("Final: %s"), *AssistantResponse);
            }
        }
    });

    Request->SendRequest();
}

FString UMyClass::ExecuteToolFunction(const FString& FunctionName, const FString& Arguments)
{
    if (FunctionName == TEXT("get_weather"))
    {
// 解析參數並返回結果
        return TEXT("{\"temperature\": \"22\", \"condition\": \"sunny\", \"unit\": \"celsius\"}");
    }
    return TEXT("{\"error\": \"Unknown function\"}");
}

void UMyClass::ContinueToolCallConversation()
{
    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(
        ToolCallOptions, ToolCallConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);
        FString FinalResponse = Response.GetMessage();
        ToolCallConversation.Add({FinalResponse, EAIChatPlus_ChatRole::Assistant});

        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *FinalResponse);
    });

    Request->SendRequest();
}
```

##伺服器進階設定

###完整配置範例

```cpp
void UMyClass::StartAdvancedServer()
{
    FAIChatPlus_CllamaServerParam Params;

// ===== 模型配置 =====
    Params.Model = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
Params.Alias = TEXT("my-local-model");    // 模型別名
Params.MMProj = TEXT("");                 // Vision MMProject 模型路徑

// ===== 硬體配置 =====
Params.NGpuLayers = 99;      // GPU 層數（-1 = 自動）
Params.Threads = -1;         // CPU 執行緒數（-1 = 自動）
Params.ThreadsBatch = -1;    // 批次處理執行緒數

// ===== 上下文配置 =====
Params.CtxSize = 4096;       // 上下文視窗大小
Params.NPredict = -1;        // 最大生成 token 數（-1 = 無限）
Params.BatchSize = 2048;     // 邏輯批次大小
Params.UbatchSize = 512;     // 實體批次大小
Params.Keep = 0;             // 保留的初始 token 數量

// ===== 取樣配置 =====
    Params.Temperature = 0.8f;
    Params.TopK = 40;
    Params.TopP = 0.9f;
    Params.MinP = 0.1f;
    Params.RepeatLastN = 64;
    Params.RepeatPenalty = 1.0f;
    Params.PresencePenalty = 0.0f;
    Params.FrequencyPenalty = 0.0f;
Params.Seed = 0xFFFFFFFF;    // 隨機種子（0xFFFFFFFF = 隨機）

    // ===== 伺服器配置 =====
    Params.Host = TEXT("127.0.0.1");
    Params.Port = 8080;          // 0 = 自動分配
Params.Timeout = 600;        // 超時時間（秒）
Params.Parallel = 1;         // 並行請求數
Params.bContBatching = true; // 連續批處理
Params.bSlots = true;        // 啟用 slots 監控端點

// ===== 功能配置 =====
    Params.bUseJinja = true;     // 使用 Jinja 模板（Tool Call 所需）
Params.bNoWebUI = false;     // 停用 Web UI
Params.ApiKey = TEXT("");    // API 金鑰認證
Params.ChatTemplate = TEXT("");  // 自訂聊天模板

// ===== 調試配置 =====
Params.bVerbose = true;      // 詳細日誌

    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params);
    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnServerStarted);
    LocalServer->Activate();
}
```

##錯誤處理

```cpp
void UMyClass::RobustCllamaServerRequest()
{
// 檢查伺服器狀態
    if (!LocalServer)
    {
        UE_LOG(LogTemp, Error, TEXT("Server instance is null"));
        return;
    }

    if (!LocalServer->IsRunning())
    {
        UE_LOG(LogTemp, Error, TEXT("Server is not running"));
        return;
    }

    FAIChatPlus_CllamaServerChatRequestOptions Options;
    Options.BaseUrl = LocalServer->GetAddress();
    Options.bStream = true;

    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->OnStartedListeners.AddLambda([]()
    {
        UE_LOG(LogTemp, Display, TEXT("Request started"));
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.HasError())
        {
            UE_LOG(LogTemp, Error, TEXT("Response error: %s"), *Response.Error.GetDescription());
            return;
        }

        UE_LOG(LogTemp, Display, TEXT("Success: %s"), *Response.GetMessage());
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_ResponseErrorBase>();
        UE_LOG(LogTemp, Error, TEXT("Request failed: %s"), *Error.GetDescription());
    });

    Request->SendRequest();
}
```

##清理資源

```cpp
void UMyClass::CleanupCllamaServer()
{
    // 停止所有請求
    // ...

    // 停止伺服器
    if (LocalServer)
    {
        LocalServer->StopServer();
        LocalServer = nullptr;
    }

    // 或者停止所有伺服器
    UAIChatPlus_CllamaServer::StopAllServers();
}

// 在 Actor 銷毀時清理
void AMyActor::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    CleanupCllamaServer();
    Super::EndPlay(EndPlayReason);
}
```

--8<-- "footer_tc.md"


> 這篇文章是由ChatGPT翻譯的，若有任何意見請到[**回饋**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遺漏之處。 
