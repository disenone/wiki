---
layout: post
title: Ollama
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Ollama, Local LLM]
description: Ollama
---
<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Ollama" />

# C++ 篇 - Ollama

本文档介绍如何在 C++ 中使用 Ollama 本地 API 进行聊天、图片分析和 Tool Calling。

Ollama 是一个本地运行大语言模型的工具，默认地址为 `http://localhost:11434`。

## 准备工作

在使用前，请确保：

1. **安装并运行 Ollama**：从 [ollama.com](https://ollama.com) 下载并安装 Ollama，然后下载所需模型（如 `ollama pull llama3.2`）。

2. 在项目的 `.Build.cs` 文件中添加模块依赖：

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

3. 包含必要的头文件：

```cpp
#include "Common_Ollama/AIChatPlus_OllamaChatRequest.h"
```

## 文本聊天

### 基础文本聊天

```cpp
#include "Common_Ollama/AIChatPlus_OllamaChatRequest.h"

void UMyClass::SendOllamaChatRequest()
{
    // 配置 Options
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");  // 使用已下载的模型
    Options.BaseUrl = TEXT("http://localhost:11434");  // 默认地址
    Options.bStream = true;  // 启用流式输出
    Options.Temperature = 0.8f;

    // Ollama 不需要 API Key（本地服务）

    // 创建消息（包含 System 消息）
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is 2+2?"), EAIChatPlus_ChatRole::User});

    // 创建请求
    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    // 绑定回调
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Ollama: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Token Usage: %s"), *Response.Usage.GetDescription());
        UE_LOG(LogTemp, Display, TEXT("Done Reason: %s"), *Response.DoneReason);
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
void UMyClass::MultiTurnOllamaChat()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

    // 构建多轮对话历史
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("My name is Charlie."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("Hello Charlie! Nice to meet you."), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my name?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

### 使用 Generate API（非 Chat 模式）

```cpp
void UMyClass::UseOllamaGenerateAPI()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;
    Options.IsChat = false;  // 使用 /api/generate 而非 /api/chat
    Options.System = TEXT("You are a helpful assistant.");  // 仅在非 Chat 模式下生效

    // 非 Chat 模式只需要一条用户消息
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Write a haiku about programming."), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Generated: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

## Vision（图片分析）

支持 Vision 的 Ollama 模型（如 `llava`、`llama3.2-vision`）可以分析图片内容。

### 从文件加载图片并分析

```cpp
#include "Common_Ollama/AIChatPlus_OllamaChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithOllama()
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
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2-vision");  // 使用支持 Vision 的模型
    Options.bStream = true;

    // 创建带图片的消息
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("What do you see in this image?");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Ollama Vision: %s"), *Message);
    });

    Request->SendRequest();
}
```

## Tool Calling（函数调用）

部分 Ollama 模型支持 Tool Calling 功能。

### 定义工具并发送请求

```cpp
void UMyClass::SendOllamaToolCallRequest()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");  // 确保模型支持 Tool Calling
    Options.bStream = true;

    // 定义工具：获取天气
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");

    // 定义工具参数
    FAIChatPlus_ChatRequestToolProperty LocationProp;
    LocationProp.Name = TEXT("location");
    LocationProp.Description = TEXT("The city name, e.g. Tokyo, Paris");
    LocationProp.Type = TEXT("string");
    LocationProp.Required = true;

    WeatherTool.Properties.Add(LocationProp);
    Options.Tools.Add(WeatherTool);

    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What's the weather in London?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);

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
void UMyClass::HandleOllamaToolCallResult()
{
    FString ToolCallId = TEXT("call_123");
    FString FunctionName = TEXT("get_weather");
    FString FunctionResult = TEXT("{\"temperature\": 15, \"unit\": \"celsius\", \"description\": \"Rainy\"}");

    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

    // 重新定义工具
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");
    Options.Tools.Add(WeatherTool);

    // 构建消息历史
    TArray<FAIChatPlus_ChatRequestMessage> Messages;

    // 1. System 消息
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});

    // 2. 用户原始问题
    Messages.Add({TEXT("What's the weather in London?"), EAIChatPlus_ChatRole::User});

    // 3. Assistant 的 Tool Call 请求
    FAIChatPlus_ChatRequestMessage AssistantMessage;
    AssistantMessage.Role = EAIChatPlus_ChatRole::Assistant;
    AssistantMessage.Content = TEXT("");

    FAIChatPlus_ChatRequestToolCall ToolCallUse;
    ToolCallUse.Id = ToolCallId;
    ToolCallUse.Type = TEXT("function");
    ToolCallUse.FunctionName = FunctionName;
    ToolCallUse.FunctionArguments = TEXT("{\"location\": \"London\"}");
    AssistantMessage.ToolCallUses.Add(ToolCallUse);
    Messages.Add(AssistantMessage);

    // 4. Tool 执行结果
    FAIChatPlus_ChatRequestMessage ToolResultMessage;
    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;

    FAIChatPlus_ChatRequestToolCallResult ToolResult;
    ToolResult.Id = ToolCallId;
    ToolResult.FunctionName = FunctionName;
    ToolResult.FunctionResult = FunctionResult;
    ToolResultMessage.ToolCallResults.Add(ToolResult);
    Messages.Add(ToolResultMessage);

    // 发送请求
    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

### 完整的 Tool Call 循环

```cpp
// 存储对话历史
TArray<FAIChatPlus_ChatRequestMessage> OllamaConversation;
FAIChatPlus_OllamaChatRequestOptions OllamaOptions;

void UMyClass::InitializeOllamaToolChat()
{
    OllamaOptions.Model = TEXT("llama3.2");
    OllamaOptions.bStream = true;

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

    OllamaOptions.Tools.Add(WeatherTool);

    // 初始化对话（添加 System 消息）
    OllamaConversation.Empty();
    OllamaConversation.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}

void UMyClass::SendOllamaUserMessage(const FString& UserMessage)
{
    OllamaConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(OllamaOptions, OllamaConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
            ProcessOllamaToolCalls(ToolCalls, Response.GetMessage());
        }
        else
        {
            FString AssistantMessage = Response.GetMessage();
            OllamaConversation.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});
            OnOllamaResponse(AssistantMessage);
        }
    });

    Request->SendRequest();
}

void UMyClass::ProcessOllamaToolCalls(const TArray<FAIChatPlus_ChatResponseToolCall>& ToolCalls, const FString& AssistantContent)
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
    OllamaConversation.Add(AssistantMsg);

    // 执行工具并添加结果
    FAIChatPlus_ChatRequestMessage ToolResultMsg;
    ToolResultMsg.Role = EAIChatPlus_ChatRole::Tool;

    for (const auto& ToolCall : ToolCalls)
    {
        FString Result = ExecuteOllamaTool(ToolCall.FunctionName, ToolCall.FunctionArguments);

        FAIChatPlus_ChatRequestToolCallResult ToolResult;
        ToolResult.Id = ToolCall.Id;
        ToolResult.FunctionName = ToolCall.FunctionName;
        ToolResult.FunctionResult = Result;
        ToolResultMsg.ToolCallResults.Add(ToolResult);
    }
    OllamaConversation.Add(ToolResultMsg);

    // 继续对话
    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(OllamaOptions, OllamaConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
            ProcessOllamaToolCalls(ToolCalls, Response.GetMessage());
        }
        else
        {
            FString FinalMessage = Response.GetMessage();
            OllamaConversation.Add({FinalMessage, EAIChatPlus_ChatRole::Assistant});
            OnOllamaResponse(FinalMessage);
        }
    });

    Request->SendRequest();
}

FString UMyClass::ExecuteOllamaTool(const FString& FunctionName, const FString& Arguments)
{
    if (FunctionName == TEXT("get_weather"))
    {
        return TEXT("{\"temperature\": 15, \"unit\": \"celsius\", \"description\": \"Rainy\"}");
    }
    return TEXT("{\"error\": \"Unknown tool\"}");
}

void UMyClass::OnOllamaResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Ollama: %s"), *Response);
}
```

## 获取模型列表

使用 `UAIChatPlus_OllamaModelRequest` 可以获取 Ollama 服务器上可用的模型列表。

```cpp
#include "Common_Ollama/AIChatPlus_OllamaModelRequest.h"

void UMyClass::GetOllamaModels()
{
    FAIChatPlus_OllamaModelRequestOptions Options;
    Options.BaseUrl = TEXT("http://localhost:11434");  // 默认地址

    auto Request = UAIChatPlus_OllamaModelRequest::CreateWithOptions(Options);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaModelRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FString> ModelNames = Response.GetModelNames();
        for (const FString& ModelName : ModelNames)
        {
            UE_LOG(LogTemp, Display, TEXT("Available Model: %s"), *ModelName);
        }

        // 获取详细信息
        for (const auto& Model : Response.Models)
        {
            UE_LOG(LogTemp, Display, TEXT("Model: %s, Size: %lld, Family: %s"),
                *Model.Name, Model.Size, *Model.Details.Family);
        }
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_ResponseErrorBase>();
        UE_LOG(LogTemp, Error, TEXT("Failed to get models: %s"), *Error.GetDescription());
    });

    Request->SendRequest();
}
```

## 高级配置

### Ollama 特有参数

```cpp
void UMyClass::ConfigureOllamaAdvanced()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

    // 采样参数
    Options.Temperature = 0.7f;
    Options.TopK = 40;           // Top-K 采样
    Options.TopP = 0.9f;         // Nucleus 采样
    Options.MinP = 0.05f;        // Min-P 采样

    // Mirostat 采样（用于控制困惑度）
    Options.Mirostat = 2;        // 0=禁用, 1=Mirostat, 2=Mirostat 2.0
    Options.MirostatEta = 0.1f;
    Options.MirostatTau = 5.0f;

    // 上下文和生成限制
    Options.NumCtx = 4096;       // 上下文窗口大小
    Options.NumPredict = 256;    // 最大生成 token 数

    // 重复惩罚
    Options.RepeatLastN = 64;
    Options.RepeatPenalty = 1.1f;

    // 停止序列
    Options.StopSequences.Add(TEXT("\n\n"));

    // 模型保持加载时间
    Options.KeepAlive = 300;     // 秒

    // 随机种子（用于可重复生成）
    Options.Seed = 42;

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

### 使用 API Key（远程 Ollama）

```cpp
void UMyClass::ConnectToRemoteOllama()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.BaseUrl = TEXT("https://your-ollama-server.com");
    Options.ApiKey = TEXT("your-api-key");  // 如果服务器需要认证
    Options.bStream = true;

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello from remote!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

### 使用 JSON 扩展选项

```cpp
void UMyClass::UseOllamaExtraOptions()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

    // 添加额外的 JSON 选项
    Options.ExtraJsonString = TEXT("{\"format\": \"json\"}");

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Return a JSON with name and age fields."), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

## 错误处理

```cpp
void UMyClass::RobustOllamaRequest()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->OnStartedListeners.AddLambda([]()
    {
        UE_LOG(LogTemp, Display, TEXT("Ollama request started..."));
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.HasError())
        {
            UE_LOG(LogTemp, Error, TEXT("Response error: %s"), *Response.Error.GetDescription());
            return;
        }

        UE_LOG(LogTemp, Display, TEXT("Success: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Done Reason: %s"), *Response.DoneReason);
        UE_LOG(LogTemp, Display, TEXT("Tokens: %s"), *Response.Usage.GetDescription());

        // Ollama 特有的性能指标
        UE_LOG(LogTemp, Display, TEXT("Total Duration: %lld ns"), Response.TotalDuration);
        UE_LOG(LogTemp, Display, TEXT("Load Duration: %lld ns"), Response.LoadDuration);
        UE_LOG(LogTemp, Display, TEXT("Eval Duration: %lld ns"), Response.EvalDuration);
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
UAIChatPlus_OllamaChatRequest* CurrentOllamaRequest = nullptr;

void UMyClass::StartOllamaRequest()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

    CurrentOllamaRequest = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a very long story."), EAIChatPlus_ChatRole::User}});

    CurrentOllamaRequest->SendRequest();
}

void UMyClass::CancelOllamaRequest()
{
    if (CurrentOllamaRequest && CurrentOllamaRequest->IsActivated())
    {
        CurrentOllamaRequest->StopRequest();
        UE_LOG(LogTemp, Display, TEXT("Ollama request cancelled"));
    }
}
```

--8<-- "footer.md"
