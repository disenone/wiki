---
layout: post
title: Gemini
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Gemini, Google]
description: Gemini
---
<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Gemini" />

# C++ 篇 - Gemini

本文档介绍如何在 C++ 中使用 Google Gemini API 进行聊天、图片分析和 Tool Calling。

## 准备工作

在使用前，请确保：

1. 在项目的 `.Build.cs` 文件中添加模块依赖：

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

2. 包含必要的头文件：

```cpp
#include "Common_Gemini/AIChatPlus_GeminiChatRequest.h"
```

## 文本聊天

### 基础文本聊天

```cpp
#include "Common_Gemini/AIChatPlus_GeminiChatRequest.h"

void UMyClass::SendGeminiChatRequest()
{
    // 配置 Options
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-google-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;  // 启用流式输出
    Options.MaxOutputTokens = 1024;
    Options.Temperature = 0.7f;

    // Gemini 的 System Prompt 通过 Options.System 设置
    Options.System = TEXT("You are a helpful assistant.");

    // 创建用户消息
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("What is the capital of Japan?"), EAIChatPlus_ChatRole::User});

    // 创建请求
    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    // 绑定回调
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Gemini: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Token Usage: %s"), *Response.Usage.GetDescription());
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_ResponseErrorBase>();
        UE_LOG(LogTemp, Error, TEXT("Request Failed: %s"), *Error.GetDescription());
    });

    // 发送请求
    Request->SendRequest();
}
```

### 多轮对话

```cpp
void UMyClass::MultiTurnGeminiChat()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant with a good memory.");

    // 构建多轮对话历史
    // Gemini 使用 "user" 和 "model" 作为角色
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("My name is Alice."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("Hello Alice! Nice to meet you. How can I help you today?"), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my name?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);
        // 模型应该记住用户名字是 Alice
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

## Vision（图片分析）

Gemini 模型支持 Vision 功能，可以分析图片内容。

> **注意**: Gemini Vision 最多支持 20 张图片（`FAIChatPlus_Constants::FGemini::MaxSendImageNum = 20`）。

### 从文件加载图片并分析

```cpp
#include "Common_Gemini/AIChatPlus_GeminiChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithGemini()
{
    // 从文件加载图片
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image: %s"), *ImagePath);
        return;
    }

    // 创建插件可用的 Texture 对象
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

    // 配置 Options
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");  // 或 gemini-1.5-pro
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant that can analyze images.");

    // 创建带图片的消息
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("Please describe this image in detail.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Gemini Vision: %s"), *Message);
    });

    Request->SendRequest();
}
```

### 多图片分析

```cpp
void UMyClass::AnalyzeMultipleImagesWithGemini()
{
    // 加载多张图片
    TArray<UAIChatPlus_Texture*> ChatTextures;

    TArray<FString> ImagePaths = {
        FPaths::ProjectContentDir() / TEXT("Images/before.png"),
        FPaths::ProjectContentDir() / TEXT("Images/after.png")
    };

    for (const FString& Path : ImagePaths)
    {
        if (UTexture2D* Texture = UAIChatPlus_Util::LoadImage(Path))
        {
            ChatTextures.Add(UAIChatPlus_Texture::CreateFromTexture2D(Texture));
        }
    }

    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;

    // 创建带多张图片的消息
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("Compare these two images and describe the differences.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images = ChatTextures;

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Comparison: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

## Tool Calling（函数调用）

Gemini 支持 Tool Calling（Function Calling），允许模型调用预定义的函数。

### 定义工具并发送请求

```cpp
void UMyClass::SendGeminiToolCallRequest()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant. Use tools when needed.");

    // 定义工具：获取天气
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");

    // 定义工具参数
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

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("What's the weather like in Tokyo?"), EAIChatPlus_ChatRole::User}});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
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

### 处理 Tool Call 结果

```cpp
void UMyClass::HandleGeminiToolCallResult()
{
    // 假设这是模型返回的 Tool Call 信息
    FString ToolCallId = TEXT("call_abc123");
    FString FunctionName = TEXT("get_weather");
    FString FunctionResult = TEXT("{\"temperature\": 25, \"unit\": \"celsius\", \"description\": \"Sunny\"}");

    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;

    // 重新定义工具
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");
    Options.Tools.Add(WeatherTool);

    // 构建消息历史
    TArray<FAIChatPlus_ChatRequestMessage> Messages;

    // 1. 用户原始问题
    Messages.Add({TEXT("What's the weather like in Tokyo?"), EAIChatPlus_ChatRole::User});

    // 2. Assistant 的 Tool Call 请求
    FAIChatPlus_ChatRequestMessage AssistantMessage;
    AssistantMessage.Role = EAIChatPlus_ChatRole::Assistant;
    AssistantMessage.Content = TEXT("");

    FAIChatPlus_ChatRequestToolCall ToolCallUse;
    ToolCallUse.Id = ToolCallId;
    ToolCallUse.Type = TEXT("function");
    ToolCallUse.FunctionName = FunctionName;
    ToolCallUse.FunctionArguments = TEXT("{\"location\": \"Tokyo\"}");
    AssistantMessage.ToolCallUses.Add(ToolCallUse);
    Messages.Add(AssistantMessage);

    // 3. Tool 执行结果
    FAIChatPlus_ChatRequestMessage ToolResultMessage;
    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;

    FAIChatPlus_ChatRequestToolCallResult ToolResult;
    ToolResult.Id = ToolCallId;
    ToolResult.FunctionName = FunctionName;
    ToolResult.FunctionResult = FunctionResult;
    ToolResultMessage.ToolCallResults.Add(ToolResult);
    Messages.Add(ToolResultMessage);

    // 发送请求
    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

### 完整的 Tool Call 循环

```cpp
// 存储对话历史
TArray<FAIChatPlus_ChatRequestMessage> GeminiConversation;
FAIChatPlus_GeminiChatRequestOptions GeminiOptions;

void UMyClass::InitializeGeminiToolChat()
{
    GeminiOptions.ApiKey = TEXT("your-api-key");
    GeminiOptions.Model = TEXT("gemini-1.5-flash");
    GeminiOptions.bStream = true;
    GeminiOptions.System = TEXT("You are a helpful assistant. Use tools when needed.");

    // 定义工具
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get weather for a location.");

    FAIChatPlus_ChatRequestToolProperty Prop;
    Prop.Name = TEXT("location");
    Prop.Type = TEXT("string");
    Prop.Required = true;
    WeatherTool.Properties.Add(Prop);

    GeminiOptions.Tools.Add(WeatherTool);

    // 清空对话历史
    GeminiConversation.Empty();
}

void UMyClass::SendGeminiUserMessage(const FString& UserMessage)
{
    GeminiConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(GeminiOptions, GeminiConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
            ProcessGeminiToolCalls(ToolCalls, Response.GetMessage());
        }
        else
        {
            FString AssistantMessage = Response.GetMessage();
            GeminiConversation.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});
            OnGeminiResponse(AssistantMessage);
        }
    });

    Request->SendRequest();
}

void UMyClass::ProcessGeminiToolCalls(const TArray<FAIChatPlus_ChatResponseToolCall>& ToolCalls, const FString& AssistantContent)
{
    // 添加 Assistant 的 Tool Call 消息
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
    GeminiConversation.Add(AssistantMsg);

    // 执行工具并添加结果
    FAIChatPlus_ChatRequestMessage ToolResultMsg;
    ToolResultMsg.Role = EAIChatPlus_ChatRole::Tool;

    for (const auto& ToolCall : ToolCalls)
    {
        FString Result = ExecuteGeminiTool(ToolCall.FunctionName, ToolCall.FunctionArguments);

        FAIChatPlus_ChatRequestToolCallResult ToolResult;
        ToolResult.Id = ToolCall.Id;
        ToolResult.FunctionName = ToolCall.FunctionName;
        ToolResult.FunctionResult = Result;
        ToolResultMsg.ToolCallResults.Add(ToolResult);
    }
    GeminiConversation.Add(ToolResultMsg);

    // 继续对话
    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(GeminiOptions, GeminiConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
            ProcessGeminiToolCalls(ToolCalls, Response.GetMessage());
        }
        else
        {
            FString FinalMessage = Response.GetMessage();
            GeminiConversation.Add({FinalMessage, EAIChatPlus_ChatRole::Assistant});
            OnGeminiResponse(FinalMessage);
        }
    });

    Request->SendRequest();
}

FString UMyClass::ExecuteGeminiTool(const FString& FunctionName, const FString& Arguments)
{
    if (FunctionName == TEXT("get_weather"))
    {
        // 实际执行天气查询
        return TEXT("{\"temperature\": 25, \"unit\": \"celsius\", \"description\": \"Sunny\"}");
    }

    return TEXT("{\"error\": \"Unknown tool\"}");
}

void UMyClass::OnGeminiResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Gemini: %s"), *Response);
}
```

## 高级配置

### 使用 JSON 扩展选项

```cpp
void UMyClass::UseGeminiExtraOptions()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");

    // 添加额外的 JSON 选项
    Options.ExtraJsonString = TEXT("{\"safetySettings\": [{\"category\": \"HARM_CATEGORY_HARASSMENT\", \"threshold\": \"BLOCK_NONE\"}]}");

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

### 自定义端点 URL

```cpp
void UMyClass::UseCustomGeminiEndpoint()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");

    // 使用自定义端点（如代理服务器）
    Options.BaseUrl = TEXT("https://your-proxy-server.com/v1beta/models");
    Options.Method = TEXT("generateContent");  // 或 streamGenerateContent

    // 或者直接设置完整 URL
    // Options.FullUrl = TEXT("https://your-proxy-server.com/v1beta/models/gemini-1.5-flash:generateContent?key=xxx");

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

### 采样参数配置

```cpp
void UMyClass::ConfigureGeminiSampling()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-pro");

    // 采样参数
    Options.Temperature = 0.3f;  // 较低温度，更确定性的输出
    Options.TopK = 40;           // Top-K 采样
    Options.TopP = 0.95f;        // Nucleus 采样
    Options.MaxOutputTokens = 2048;

    // 停止序列
    Options.StopSequences.Add(TEXT("\n\n"));
    Options.StopSequences.Add(TEXT("END"));

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a short story."), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

## 错误处理

```cpp
void UMyClass::RobustGeminiRequest()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->OnStartedListeners.AddLambda([]()
    {
        UE_LOG(LogTemp, Display, TEXT("Gemini request started..."));
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.HasError())
        {
            UE_LOG(LogTemp, Error, TEXT("Response error: %s"), *Response.Error.GetDescription());
            return;
        }

        // 检查 FinishReason
        if (!Response.Messages.IsEmpty())
        {
            FString FinishReason = Response.Messages[0].FinishReason;
            UE_LOG(LogTemp, Display, TEXT("Finish Reason: %s"), *FinishReason);
        }

        UE_LOG(LogTemp, Display, TEXT("Success: %s"), *Response.GetMessage());
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

## 停止请求

```cpp
UPROPERTY()
UAIChatPlus_GeminiChatRequest* CurrentGeminiRequest = nullptr;

void UMyClass::StartGeminiRequest()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;

    CurrentGeminiRequest = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a very long essay about technology."), EAIChatPlus_ChatRole::User}});

    CurrentGeminiRequest->SendRequest();
}

void UMyClass::CancelGeminiRequest()
{
    if (CurrentGeminiRequest && CurrentGeminiRequest->IsActivated())
    {
        CurrentGeminiRequest->StopRequest();
        UE_LOG(LogTemp, Display, TEXT("Gemini request cancelled"));
    }
}
```

--8<-- "footer.md"
