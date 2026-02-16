---
layout: post
title: Get Started
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini, Ollama]
description: Get Started
---
<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Get Started" />

# C++ 篇 - Get Started

## 模块介绍

插件分成以下几个模块：

* **AIChatPlusCommon**: 运行时模块 (Runtime)，负责处理各种 AI API 接口发送请求和解析回复内容。
* **AIChatPlusEditor**: 编辑器模块 (Editor)，负责实现编辑器 AI 聊天工具。
* **AIChatPlusCllama**: 运行时模块 (Runtime)，负责封装 llama.cpp 的接口和参数，实现离线执行大模型。
* **Thirdparty/LLAMACpp**: 运行时第三方模块 (Runtime)，整合了 llama.cpp 的动态库和头文件。

## 核心概念

在使用源码之前，需要了解几个核心类及其关系：

### Request（请求）

`UAIChatPlus_ChatRequestBase` 是所有聊天请求的基类。每种 API Provider 都有对应的子类：

* `UAIChatPlus_OpenAIChatRequest` - OpenAI 聊天请求
* `UAIChatPlus_AzureChatRequest` - Azure 聊天请求
* `UAIChatPlus_ClaudeChatRequest` - Claude 聊天请求
* `UAIChatPlus_GeminiChatRequest` - Gemini 聊天请求
* `UAIChatPlus_OllamaChatRequest` - Ollama 聊天请求
* `UAIChatPlus_CllamaChatRequest` - Cllama 离线模型请求
* `UAIChatPlus_CllamaServerChatRequest` - CllamaServer 本地服务器请求

Request 对象负责配置请求参数、发送请求、接收回调。

### Handler（处理器）

`UAIChatPlus_ChatHandlerBase` 是一个可选的处理器类，用于统一管理请求的回调。

Handler 提供了以下委托：

* `OnStarted` - 请求开始时触发
* `OnMessage` - 收到流式消息时触发（流式输出）
* `OnUpdated` - 收到更新时触发
* `OnFinished` - 请求完成时触发
* `OnFailed` - 请求失败时触发

**何时使用 Handler？**

* 需要将多个请求的回调逻辑统一管理时
* 需要在蓝图和 C++ 之间共享回调逻辑时
* 直接使用 Request 的委托（如 `OnStartedListeners`）同样可以实现回调监听

### Options（选项）

每种 API Provider 都有对应的 Options 结构体，用于配置 API 参数：

* `FAIChatPlus_OpenAIChatRequestOptions` - OpenAI 选项（ApiKey、Model、Temperature 等）
* `FAIChatPlus_ClaudeChatRequestOptions` - Claude 选项
* `FAIChatPlus_GeminiChatRequestOptions` - Gemini 选项
* 等等...

Options 包含了 API 连接所需的所有配置，如 API Key、端点 URL、模型名称、生成参数等。

### Messages（消息）

`FAIChatPlus_ChatRequestMessage` 是发送给 AI 的消息结构体，包含：

* `Content` - 文本内容
* `Role` - 消息角色（System/User/Assistant/Developer/Tool）
* `Images` - 图片数组（Vision 功能）
* `Audios` - 音频数组（Audio 功能）
* `ToolCallUses` - 工具调用请求
* `ToolCallResults` - 工具调用结果

### Response（响应）

每种 API Provider 都有对应的 ResponseBody 结构体：

* `FAIChatPlus_OpenAIChatResponseBody`
* `FAIChatPlus_ClaudeChatResponseBody`
* 等等...

ResponseBody 包含了 AI 返回的全部信息，包括：消息文本、Token 用量、工具调用、音频输出等。

## 基础使用流程（5 步模式）

使用 AIChatPlus 发送请求的基本流程如下：

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"

void SendChatRequest()
{
    // ===== 步骤 1: 创建 Handler（可选）=====
    // Handler 用于统一管理回调，也可以直接使用 Request 的委托
    TWeakObjectPtr<UAIChatPlus_ChatHandlerBase> Handler = UAIChatPlus_ChatHandlerBase::New();

    // ===== 步骤 2: 配置 Options =====
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;  // 启用流式输出

    // ===== 步骤 3: 创建 Request =====
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("Hello, who are you?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    // ===== 步骤 4: 绑定回调 =====
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

    // 方式 B: 直接使用 Request 的委托（不需要 Handler）
    // Request->OnMessageListeners.AddDynamic(this, &UMyClass::OnMessageReceived);
    // Request->OnFinishedListeners.AddDynamic(this, &UMyClass::OnRequestFinished);

    // ===== 步骤 5: 发送请求 =====
    Request->SendRequest();
}
```

## 简化写法

如果不需要精细的回调控制，可以使用更简洁的写法：

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

    // 直接在 Request 上绑定 Lambda
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

## 通过 API Provider 枚举创建请求

如果需要根据配置动态选择 API Provider，可以使用工厂方法：

```cpp
void CreateRequestByProvider(EAIChatPlus_ChatApiProvider Provider)
{
    // 根据枚举创建对应的 Request
    auto Request = UAIChatPlus_ChatRequestBase::CreateByApi(Provider);

    // 根据实际类型设置 Options
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

    // 设置消息并发送
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Hello!"), EAIChatPlus_ChatRole::User});
    Request->SetMessages(Messages);
    Request->SendRequest();
}
```

## 回调说明

### 主要回调委托

| 委托 | 触发时机 | 参数 |
|------|----------|------|
| `OnStarted` | 请求开始发送时 | 无 |
| `OnMessage` | 收到流式消息时（每个 token） | `const FString& Message` - 累积的消息内容 |
| `OnUpdated` | 收到响应更新时 | `const FAIChatPlus_ResponseBodyBase& Response` |
| `OnFinished` | 请求成功完成时 | `const FAIChatPlus_ResponseBodyBase& Response` |
| `OnFailed` | 请求失败时 | `const FAIChatPlus_ResponseErrorBase& Error` |
| `OnMessageFinished` | 消息接收完成时 | `const FAIChatPlus_MessageFinishedPayload& Payload` |

### 流式输出 vs 非流式输出

* **流式输出** (`bStream = true`)：`OnMessage` 会多次触发，每次返回累积的消息内容
* **非流式输出** (`bStream = false`)：`OnMessage` 只在完成时触发一次，返回完整消息

## 下一步

更多详细用法请参考各 API Provider 的专题文档：

* [OpenAI / Azure 使用](ue-插件-AIChatPlus-Usage-Source-OpenAI.md)
* [Claude 使用](ue-插件-AIChatPlus-Usage-Source-Claude.md)
* [Gemini 使用](ue-插件-AIChatPlus-Usage-Source-Gemini.md)
* [Ollama 使用](ue-插件-AIChatPlus-Usage-Source-Ollama.md)
* [Cllama 离线模型](ue-插件-AIChatPlus-Usage-Source-Cllama.md)
* [CllamaServer 本地服务器](ue-插件-AIChatPlus-Usage-Source-CllamaServer.md)
* [工具类](ue-插件-AIChatPlus-Usage-Source-Utils.md)

--8<-- "footer.md"