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

#C++ Section - Get Started

##Module Introduction

The plugin is divided into the following modules:

* **AIChatPlusCommon**: Runtime module responsible for handling requests to various AI API interfaces and parsing response content.
* **AIChatPlusEditor**: Editor module responsible for implementing the AI chat tool within the editor.
* **AIChatPlusCllama**: Runtime module, responsible for encapsulating the interfaces and parameters of llama.cpp to enable offline execution of large models.
* **Thirdparty/LLAMACpp**: Runtime third-party module (Runtime), integrating the dynamic library and header files of llama.cpp.

##Core Concepts

Before using the source code, it's necessary to understand several core classes and their relationships:

###Request

`UAIChatPlus_ChatRequestBase` is the base class for all chat requests. Each API Provider has its corresponding subclass:

* `UAIChatPlus_OpenAIChatRequest` - OpenAI Chat Request
* `UAIChatPlus_AzureChatRequest` - Azure Chat Request
* `UAIChatPlus_ClaudeChatRequest` - Claude Chat Request
* `UAIChatPlus_GeminiChatRequest` - Gemini Chat Request
`UAIChatPlus_OllamaChatRequest` - Ollama Chat Request
* `UAIChatPlus_CllamaChatRequest` - Cllama Offline Model Request
* `UAIChatPlus_CllamaServerChatRequest` - CllamaServer Local Server Request

The Request object is responsible for configuring request parameters, sending requests, and receiving callbacks.

###Handler

`UAIChatPlus_ChatHandlerBase` is an optional handler class designed to uniformly manage request callbacks.

Handler provides the following delegates:

* `OnStarted` - Triggered when the request begins
* `OnMessage` - Triggered upon receiving a streaming message (streaming output)
* `OnUpdated` - Triggered when an update is received
* `OnFinished` - Triggered when the request is completed
* `OnFailed` - Triggered when the request fails

**When to Use Handler?**

* When the callback logic for multiple requests needs to be managed uniformly
* When callback logic needs to be shared between Blueprints and C++
* Using Request's delegates directly (such as `OnStartedListeners`) can also achieve callback monitoring

###Options

Each API Provider has a corresponding Options struct used to configure API parameters:

`FAIChatPlus_OpenAIChatRequestOptions` - OpenAI options (ApiKey, Model, Temperature, etc.)
* `FAIChatPlus_ClaudeChatRequestOptions` - Claude Options
* `FAIChatPlus_GeminiChatRequestOptions` - Gemini Options
* Wait...

Options encompass all the configurations needed for API connections, including the API key, endpoint URL, model name, generation parameters, and more.

###Messages

`FAIChatPlus_ChatRequestMessage` is the message struct sent to the AI, which includes:

* `Content` - Text content
* `Role` - Message role (System/User/Assistant/Developer/Tool)
* `Images` - Images array (Vision feature)
* `Audios` - Audio array (Audio function)
* `ToolCallUses` - Tool invocation request
* `ToolCallResults` - Tool Call Results

###Response

Each API Provider has its corresponding ResponseBody structure:

* `FAIChatPlus_OpenAIChatResponseBody`
* `FAIChatPlus_ClaudeChatResponseBody`
* Wait...

The ResponseBody contains all the information returned by the AI, including: message text, Token usage, tool invocation, audio output, and more.

##Basic Usage Flow (5-Step Model)

The basic process for sending requests using AIChatPlus is as follows:

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"

void SendChatRequest()
{
    // ===== Step 1: Create Handler (Optional) =====
// Handler is used for uniformly managing callbacks, and you can also directly use the delegate of Request
    TWeakObjectPtr<UAIChatPlus_ChatHandlerBase> Handler = UAIChatPlus_ChatHandlerBase::New();

// ===== Step 2: Configure Options =====
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;  // Enable streaming output

// ===== Step 3: Create Request =====
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("Hello, who are you?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// ===== Step 4: Bind Callback =====
    // Method A: Using Handler
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

    // Method B: Directly using the delegation of Request (no Handler required)
    // Request->OnMessageListeners.AddDynamic(this, &UMyClass::OnMessageReceived);
    // Request->OnFinishedListeners.AddDynamic(this, &UMyClass::OnRequestFinished);

    // ===== Step 5: Send Request =====
    Request->SendRequest();
}
```

##Simplified notation

If fine-grained callback control is not needed, you can use a more concise writing style:

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

// Bind Lambda directly to Request
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

##Creating requests via API Provider enumeration

If there's a need to dynamically select an API Provider based on configurations, the factory method can be utilized:

```cpp
void CreateRequestByProvider(EAIChatPlus_ChatApiProvider Provider)
{
// Create corresponding Request based on the enumeration
    auto Request = UAIChatPlus_ChatRequestBase::CreateByApi(Provider);

// Set Options based on the actual type
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
    // ... Other Providers
    }

// Set the message and send it
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Hello!"), EAIChatPlus_ChatRole::User});
    Request->SetMessages(Messages);
    Request->SendRequest();
}
```

##Callback Instructions

###Main Callback Delegates

| Delegation | Trigger Timing | Parameters |
|------|----------|------|
| `OnStarted` | When the request starts sending | None |
| `OnMessage` | Triggered upon receiving a streaming message (each token) | `const FString& Message` - Accumulated message content |
| `OnUpdated` | When receiving response updates | `const FAIChatPlus_ResponseBodyBase& Response` |
| `OnFinished` | When the request is successfully completed | `const FAIChatPlus_ResponseBodyBase& Response` |
| `OnFailed` | When the request fails | `const FAIChatPlus_ResponseErrorBase& Error` |
| `OnMessageFinished` | When message reception is completed | `const FAIChatPlus_MessageFinishedPayload& Payload` |

###Streaming Output vs Non-Streaming Output

* **Streaming Output** (`bStream = true`): `OnMessage` triggers multiple times, each time returning the accumulated message content
* **Non-streaming output** (`bStream = false`): `OnMessage` triggers only once upon completion, delivering the full message.

##Next Step

For more detailed usage, please refer to the respective API Provider's documentation:

* [OpenAI / Azure Usage](ue-插件-AIChatPlus-Usage-Source-OpenAI.md)
* [Using Claude](ue-插件-AIChatPlus-Usage-Source-Claude.md)
* [Gemini Usage](ue-插件-AIChatPlus-Usage-Source-Gemini.md)
* [Using Ollama](ue-插件-AIChatPlus-Usage-Source-Ollama.md)
* [Cllama offline model](ue-插件-AIChatPlus-Usage-Source-Cllama.md)
* [CllamaServer Local Server](ue-插件-AIChatPlus-Usage-Source-CllamaServer.md)
* [Utility Class](ue-插件-AIChatPlus-Usage-Source-Utils.md)

--8<-- "footer_en.md"

> This post was translated using ChatGPT. Please provide feedback at [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Please point out any omissions therein. 
