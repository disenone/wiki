---
layout: post
title: Claude
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
- Claude
- Anthropic
description: Claude
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Claude" />

#C++ 篇 - Claude

本文件介紹如何在 C++ 中使用 Anthropic Claude API 進行聊天、圖片分析和 Tool Calling。

##準備工作

在使用前，請確保：

1. 在專案的 `.Build.cs` 檔案中加入模組依賴：

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

2. 包含必要的標頭檔案：

```cpp
#include "Common_Claude/AIChatPlus_ClaudeChatRequest.h"
```

##文字聊天

###基礎文本聊天

```cpp
#include "Common_Claude/AIChatPlus_ClaudeChatRequest.h"

void UMyClass::SendClaudeChatRequest()
{
// 設定選項
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-anthropic-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
Options.bStream = true;  // 啟用串流輸出
    Options.MaxOutputTokens = 1024;
    Options.Temperature = 0.7f;

// Claude 的系統提示透過 Options.System 設定
    Options.System = TEXT("You are a helpful assistant.");

// 建立使用者訊息
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("What is the capital of France?"), EAIChatPlus_ChatRole::User});

// 建立請求
    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// 綁定回呼
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Claude: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Token Usage: %s"), *Response.Usage.GetDescription());
        UE_LOG(LogTemp, Display, TEXT("Stop Reason: %s"), *Response.StopReason);
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_ResponseErrorBase>();
        UE_LOG(LogTemp, Error, TEXT("Request Failed: %s"), *Error.GetDescription());
    });

    // 發送請求
    Request->SendRequest();
}
```

###多輪對話

```cpp
void UMyClass::MultiTurnClaudeChat()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant with a good memory.");

// 構建多輪對話歷史（不包含 System，Claude 的 System 在 Options 中）
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("My name is Bob."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("Hello Bob! Nice to meet you. How can I assist you today?"), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my name?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);
// 模型應該記住用戶名字是 Bob
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##視覺（圖片分析）

Claude 3系列模型支援Vision功能，能夠解析圖片內容。

> **注意**: Claude Vision 最多支援 20 張圖片（`FAIChatPlus_Constants::FClaude::MaxSendImageNum = 20`）。

###從文件載入圖片並分析

```cpp
#include "Common_Claude/AIChatPlus_ClaudeChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithClaude()
{
    // 從檔案載入圖片
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image: %s"), *ImagePath);
        return;
    }

    // 創建插件可用的 Texture 物件
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

// 配置選項
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
Options.Model = TEXT("claude-3-5-sonnet-20240620");  // 使用 Claude 3 系列
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant that can analyze images.");

// 建立帶圖片的訊息
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("Please describe this image in detail.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Claude Vision: %s"), *Message);
    });

    Request->SendRequest();
}
```

###多圖片分析

```cpp
void UMyClass::AnalyzeMultipleImages()
{
    // 載入多張圖片
    TArray<UAIChatPlus_Texture*> ChatTextures;

    TArray<FString> ImagePaths = {
        FPaths::ProjectContentDir() / TEXT("Images/image1.png"),
        FPaths::ProjectContentDir() / TEXT("Images/image2.png"),
        FPaths::ProjectContentDir() / TEXT("Images/image3.png")
    };

    for (const FString& Path : ImagePaths)
    {
        if (UTexture2D* Texture = UAIChatPlus_Util::LoadImage(Path))
        {
            ChatTextures.Add(UAIChatPlus_Texture::CreateFromTexture2D(Texture));
        }
    }

    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant.");

// 建立帶有多張圖片的訊息
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("Compare these images and describe the differences.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images = ChatTextures;

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Comparison: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##工具呼叫（函式呼叫）

Claude 支援 Tool Calling，讓模型能夠呼叫預先定義的函數。

###定義工具並發送請求

```cpp
void UMyClass::SendClaudeToolCallRequest()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant. Use tools when needed.");

    // 定義工具：取得天氣
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");

// 定義工具參數
    FAIChatPlus_ChatRequestToolProperty LocationProp;
    LocationProp.Name = TEXT("location");
    LocationProp.Description = TEXT("The city name, e.g. Tokyo, Paris, New York");
    LocationProp.Type = TEXT("string");
    LocationProp.Required = true;

    FAIChatPlus_ChatRequestToolProperty UnitProp;
    UnitProp.Name = TEXT("unit");
    UnitProp.Description = TEXT("The temperature unit: celsius or fahrenheit");
    UnitProp.Type = TEXT("string");
    UnitProp.Required = false;

    WeatherTool.Properties.Add(LocationProp);
    WeatherTool.Properties.Add(UnitProp);

    Options.Tools.Add(WeatherTool);

// 可選：設定 ToolChoice
    // Options.ToolChoice.Type = TEXT("auto");  // auto, any, or tool
    // Options.ToolChoice.Name = TEXT("get_weather");  // 僅當 Type == "tool" 時使用

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("What's the weather like in Paris?"), EAIChatPlus_ChatRole::User}});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);

        // 檢查停止原因是否為 tool_use
        if (Response.StopReason == TEXT("tool_use"))
        {
            TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
            for (const auto& ToolCall : ToolCalls)
            {
                UE_LOG(LogTemp, Display, TEXT("Tool Call - ID: %s, Function: %s, Args: %s"),
                    *ToolCall.Id, *ToolCall.FunctionName, *ToolCall.FunctionArguments);
            }
        }
        else
        {
            UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
        }
    });

    Request->SendRequest();
}
```

###處理 Tool Call 結果

```cpp
void UMyClass::HandleClaudeToolCallResult()
{
    // 假設這是模型返回的 Tool Call 資訊
    FString ToolCallId = TEXT("toolu_01abc123");
    FString FunctionName = TEXT("get_weather");
    FString FunctionResult = TEXT("{\"temperature\": 18, \"unit\": \"celsius\", \"description\": \"Cloudy\"}");

    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant. Use tools when needed.");

// 重新定義工具
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");
    Options.Tools.Add(WeatherTool);

// 建構訊息歷史
    TArray<FAIChatPlus_ChatRequestMessage> Messages;

    // 1. 使用者原始問題
    Messages.Add({TEXT("What's the weather like in Paris?"), EAIChatPlus_ChatRole::User});

    // 2. Assistant 的 Tool Use 請求
    FAIChatPlus_ChatRequestMessage AssistantMessage;
    AssistantMessage.Role = EAIChatPlus_ChatRole::Assistant;
    AssistantMessage.Content = TEXT("");

    FAIChatPlus_ChatRequestToolCall ToolCallUse;
    ToolCallUse.Id = ToolCallId;
    ToolCallUse.Type = TEXT("function");
    ToolCallUse.FunctionName = FunctionName;
    ToolCallUse.FunctionArguments = TEXT("{\"location\": \"Paris\"}");
    AssistantMessage.ToolCallUses.Add(ToolCallUse);
    Messages.Add(AssistantMessage);

// 3. 工具執行結果
    FAIChatPlus_ChatRequestMessage ToolResultMessage;
    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;

    FAIChatPlus_ChatRequestToolCallResult ToolResult;
    ToolResult.Id = ToolCallId;
    ToolResult.FunctionName = FunctionName;
    ToolResult.FunctionResult = FunctionResult;
    ToolResultMessage.ToolCallResults.Add(ToolResult);
    Messages.Add(ToolResultMessage);

    // 傳送請求
    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###完整的 Tool Call 循環

```cpp
// 儲存對話歷史
TArray<FAIChatPlus_ChatRequestMessage> ClaudeConversation;
FAIChatPlus_ClaudeChatRequestOptions ClaudeOptions;

void UMyClass::InitializeClaudeToolChat()
{
    ClaudeOptions.ApiKey = TEXT("your-api-key");
    ClaudeOptions.Model = TEXT("claude-3-5-sonnet-20240620");
    ClaudeOptions.bStream = true;
    ClaudeOptions.System = TEXT("You are a helpful assistant. Use tools to get real-time information.");

    // 定義工具
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get weather for a location.");

    FAIChatPlus_ChatRequestToolProperty Prop;
    Prop.Name = TEXT("location");
    Prop.Type = TEXT("string");
    Prop.Required = true;
    WeatherTool.Properties.Add(Prop);

    ClaudeOptions.Tools.Add(WeatherTool);

    // 清空對話歷史
    ClaudeConversation.Empty();
}

void UMyClass::SendClaudeUserMessage(const FString& UserMessage)
{
    ClaudeConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(ClaudeOptions, ClaudeConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.StopReason == TEXT("tool_use"))
        {
            ProcessClaudeToolCalls(Response.GetToolCalls(), Response.GetMessage());
        }
        else
        {
            FString AssistantMessage = Response.GetMessage();
            ClaudeConversation.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});
            OnClaudeResponse(AssistantMessage);
        }
    });

    Request->SendRequest();
}

void UMyClass::ProcessClaudeToolCalls(const TArray<FAIChatPlus_ChatResponseToolCall>& ToolCalls, const FString& AssistantContent)
{
// 加入 Assistant 的工具調用訊息
    FAIChatPlus_ChatRequestMessage AssistantMsg;
    AssistantMsg.Role = EAIChatPlus_ChatRole::Assistant;
    AssistantMsg.Content = AssistantContent;

    for (const auto& ToolCall : ToolCalls)
    {
        FAIChatPlus_ChatRequestToolCall Use;
        Use.Id = ToolCall.Id;
        Use.Type = ToolCall.Type;
        Use.FunctionName = ToolCall.FunctionName;
        Use.FunctionArguments = ToolCall.FunctionArguments;
        AssistantMsg.ToolCallUses.Add(Use);
    }
    ClaudeConversation.Add(AssistantMsg);

// 執行工具並新增結果
    FAIChatPlus_ChatRequestMessage ToolResultMsg;
    ToolResultMsg.Role = EAIChatPlus_ChatRole::Tool;

    for (const auto& ToolCall : ToolCalls)
    {
        FString Result = ExecuteClaudeTool(ToolCall.FunctionName, ToolCall.FunctionArguments);

        FAIChatPlus_ChatRequestToolCallResult ToolResult;
        ToolResult.Id = ToolCall.Id;
        ToolResult.FunctionName = ToolCall.FunctionName;
        ToolResult.FunctionResult = Result;
        ToolResultMsg.ToolCallResults.Add(ToolResult);
    }
    ClaudeConversation.Add(ToolResultMsg);

// 183cm
外貌：一头利落短发，左耳一颗蓝钻耳钉衬得侧颜精致，常年戴着墨镜也遮不住俊颜
身份：地下乐团主唱，地下酒吧老板
性格：
1.外表玩世不恭，实则深谙世事，心思缜密
2.我行我素，厌恶虚伪客套
3.极度护短，谁敢动他的人，别想竖着离开
喜好：调酒、飙车、深夜弹钢琴
其他特征：
1.地下乐团《夜莺》的灵魂主唱，舞台风格慵懒随性又极具感染力
2.精通五国语言，却总爱用方言怼人
3.右肩胛骨有个夜莺纹身
底线：不能回复任何危害人类社会或危害个体人类的言论与行为

【聊天规范】
*对你的称呼：萧哥
    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(ClaudeOptions, ClaudeConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.StopReason == TEXT("tool_use"))
        {
            ProcessClaudeToolCalls(Response.GetToolCalls(), Response.GetMessage());
        }
        else
        {
            FString FinalMessage = Response.GetMessage();
            ClaudeConversation.Add({FinalMessage, EAIChatPlus_ChatRole::Assistant});
            OnClaudeResponse(FinalMessage);
        }
    });

    Request->SendRequest();
}

FString UMyClass::ExecuteClaudeTool(const FString& FunctionName, const FString& Arguments)
{
    if (FunctionName == TEXT("get_weather"))
    {
// 實際執行天氣查詢
        return TEXT("{\"temperature\": 18, \"unit\": \"celsius\", \"description\": \"Cloudy\"}");
    }

    return TEXT("{\"error\": \"Unknown tool\"}");
}

void UMyClass::OnClaudeResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Claude: %s"), *Response);
}
```

##高級設定

###使用JSON擴充選項

```cpp
void UMyClass::UseClaudeExtraOptions()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");

// 新增額外的 JSON 選項
    Options.ExtraJsonString = TEXT("{\"metadata\": {\"user_id\": \"12345\"}}");

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###自訂端點URL

```cpp
void UMyClass::UseCustomClaudeEndpoint()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");

    // 使用自定義端點（如代理伺服器）
    Options.BaseUrl = TEXT("https://your-proxy-server.com");
    Options.EndPointUrl = TEXT("v1/messages");

    // 或者直接設定完整 URL
    // Options.FullUrl = TEXT("https://your-proxy-server.com/v1/messages");

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###設定 Anthropic 版本

```cpp
void UMyClass::SetAnthropicVersion()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");

    // 設定 API 版本
    Options.AnthropicVersion = TEXT("2023-06-01");

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

##錯誤處理

```cpp
void UMyClass::RobustClaudeRequest()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->OnStartedListeners.AddLambda([]()
    {
        UE_LOG(LogTemp, Display, TEXT("Claude request started..."));
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.HasError())
        {
            UE_LOG(LogTemp, Error, TEXT("Response error: %s"), *Response.Error.GetDescription());
            return;
        }

        UE_LOG(LogTemp, Display, TEXT("Success: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Stop Reason: %s"), *Response.StopReason);
        UE_LOG(LogTemp, Display, TEXT("Tokens: %s"), *Response.Usage.GetDescription());
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_ResponseErrorBase>();
        UE_LOG(LogTemp, Error, TEXT("Request failed: %s"), *Error.GetDescription());
    });

    Request->SendRequest();
}
```

##停止請求

```cpp
UPROPERTY()
UAIChatPlus_ClaudeChatRequest* CurrentClaudeRequest = nullptr;

void UMyClass::StartClaudeRequest()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;

    CurrentClaudeRequest = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a very long essay about AI."), EAIChatPlus_ChatRole::User}});

    CurrentClaudeRequest->SendRequest();
}

void UMyClass::CancelClaudeRequest()
{
    if (CurrentClaudeRequest && CurrentClaudeRequest->IsActivated())
    {
        CurrentClaudeRequest->StopRequest();
        UE_LOG(LogTemp, Display, TEXT("Claude request cancelled"));
    }
}
```

--8<-- "footer_tc.md"


> 此貼文是使用 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
