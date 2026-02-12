---
layout: post
title: Claude
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Claude, Anthropic]
description: Claude
---
<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Claude" />

# C++ 篇 - Claude

本文档介绍如何在 C++ 中使用 Anthropic Claude API 进行聊天、图片分析和 Tool Calling。

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
#include "Common_Claude/AIChatPlus_ClaudeChatRequest.h"
```

## 文本聊天

### 基础文本聊天

```cpp
#include "Common_Claude/AIChatPlus_ClaudeChatRequest.h"

void UMyClass::SendClaudeChatRequest()
{
    // 配置 Options
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-anthropic-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;  // 启用流式输出
    Options.MaxOutputTokens = 1024;
    Options.Temperature = 0.7f;

    // Claude 的 System Prompt 通过 Options.System 设置
    Options.System = TEXT("You are a helpful assistant.");

    // 创建用户消息
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("What is the capital of France?"), EAIChatPlus_ChatRole::User});

    // 创建请求
    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    // 绑定回调
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

    // 发送请求
    Request->SendRequest();
}
```

### 多轮对话

```cpp
void UMyClass::MultiTurnClaudeChat()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant with a good memory.");

    // 构建多轮对话历史（不包含 System，Claude 的 System 在 Options 中）
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("My name is Bob."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("Hello Bob! Nice to meet you. How can I assist you today?"), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my name?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);
        // 模型应该记住用户名字是 Bob
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

## Vision（图片分析）

Claude 3 系列模型支持 Vision 功能，可以分析图片内容。

> **注意**: Claude Vision 最多支持 20 张图片（`FAIChatPlus_Constants::FClaude::MaxSendImageNum = 20`）。

### 从文件加载图片并分析

```cpp
#include "Common_Claude/AIChatPlus_ClaudeChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithClaude()
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
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");  // 使用 Claude 3 系列
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant that can analyze images.");

    // 创建带图片的消息
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

### 多图片分析

```cpp
void UMyClass::AnalyzeMultipleImages()
{
    // 加载多张图片
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

    // 创建带多张图片的消息
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

## Tool Calling（函数调用）

Claude 支持 Tool Calling，允许模型调用预定义的函数。

### 定义工具并发送请求

```cpp
void UMyClass::SendClaudeToolCallRequest()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
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

    // 可选：设置 ToolChoice
    // Options.ToolChoice.Type = TEXT("auto");  // auto, any, or tool
    // Options.ToolChoice.Name = TEXT("get_weather");  // 仅当 Type == "tool" 时使用

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("What's the weather like in Paris?"), EAIChatPlus_ChatRole::User}});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);

        // 检查停止原因是否为 tool_use
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

### 处理 Tool Call 结果

```cpp
void UMyClass::HandleClaudeToolCallResult()
{
    // 假设这是模型返回的 Tool Call 信息
    FString ToolCallId = TEXT("toolu_01abc123");
    FString FunctionName = TEXT("get_weather");
    FString FunctionResult = TEXT("{\"temperature\": 18, \"unit\": \"celsius\", \"description\": \"Cloudy\"}");

    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant. Use tools when needed.");

    // 重新定义工具
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");
    Options.Tools.Add(WeatherTool);

    // 构建消息历史
    TArray<FAIChatPlus_ChatRequestMessage> Messages;

    // 1. 用户原始问题
    Messages.Add({TEXT("What's the weather like in Paris?"), EAIChatPlus_ChatRole::User});

    // 2. Assistant 的 Tool Use 请求
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
    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

### 完整的 Tool Call 循环

```cpp
// 存储对话历史
TArray<FAIChatPlus_ChatRequestMessage> ClaudeConversation;
FAIChatPlus_ClaudeChatRequestOptions ClaudeOptions;

void UMyClass::InitializeClaudeToolChat()
{
    ClaudeOptions.ApiKey = TEXT("your-api-key");
    ClaudeOptions.Model = TEXT("claude-3-5-sonnet-20240620");
    ClaudeOptions.bStream = true;
    ClaudeOptions.System = TEXT("You are a helpful assistant. Use tools to get real-time information.");

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

    ClaudeOptions.Tools.Add(WeatherTool);

    // 清空对话历史
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
    ClaudeConversation.Add(AssistantMsg);

    // 执行工具并添加结果
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

    // 继续对话
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
        // 实际执行天气查询
        return TEXT("{\"temperature\": 18, \"unit\": \"celsius\", \"description\": \"Cloudy\"}");
    }

    return TEXT("{\"error\": \"Unknown tool\"}");
}

void UMyClass::OnClaudeResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Claude: %s"), *Response);
}
```

## 高级配置

### 使用 JSON 扩展选项

```cpp
void UMyClass::UseClaudeExtraOptions()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");

    // 添加额外的 JSON 选项
    Options.ExtraJsonString = TEXT("{\"metadata\": {\"user_id\": \"12345\"}}");

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

### 自定义端点 URL

```cpp
void UMyClass::UseCustomClaudeEndpoint()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");

    // 使用自定义端点（如代理服务器）
    Options.BaseUrl = TEXT("https://your-proxy-server.com");
    Options.EndPointUrl = TEXT("v1/messages");

    // 或者直接设置完整 URL
    // Options.FullUrl = TEXT("https://your-proxy-server.com/v1/messages");

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

### 设置 Anthropic 版本

```cpp
void UMyClass::SetAnthropicVersion()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");

    // 设置 API 版本
    Options.AnthropicVersion = TEXT("2023-06-01");

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

## 错误处理

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

## 停止请求

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

--8<-- "footer.md"
