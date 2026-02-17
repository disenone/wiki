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

#C++ Chapter - Claude

This document explains how to use the Anthropic Claude API in C++ for chat, image analysis, and Tool Calling.

##Preparatory Work

Before use, please ensure:

1. Add module dependencies in the project's `.Build.cs` file:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

2. Include necessary header files:

```cpp
#include "Common_Claude/AIChatPlus_ClaudeChatRequest.h"
```

##Text Chat

###Basic Text Chat

```cpp
#include "Common_Claude/AIChatPlus_ClaudeChatRequest.h"

void UMyClass::SendClaudeChatRequest()
{
// Configuration Options
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-anthropic-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
Options.bStream = true;  // Enable streaming output
    Options.MaxOutputTokens = 1024;
    Options.Temperature = 0.7f;

    // Claude's System Prompt is set via Options.System
    Options.System = TEXT("You are a helpful assistant.");

// Create user message
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("What is the capital of France?"), EAIChatPlus_ChatRole::User});

    // Create request
    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    // Bind callback
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

// Send request
    Request->SendRequest();
}
```

###Multi-turn dialogue

```cpp
void UMyClass::MultiTurnClaudeChat()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant with a good memory.");

    // Build multi-turn dialog history (excluding System, Claude's System is in Options)
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("My name is Bob."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("Hello Bob! Nice to meet you. How can I assist you today?"), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my name?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);
// The model should remember the user's name is Bob
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##Vision (Image Analysis)

The Claude 3 series models support Vision capabilities, allowing them to analyze image content.

> **Note**: Claude Vision supports a maximum of 20 images (`FAIChatPlus_Constants::FClaude::MaxSendImageNum = 20`).

###Load image from file and analyze

```cpp
#include "Common_Claude/AIChatPlus_ClaudeChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithClaude()
{
    // Load an image from a file
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image: %s"), *ImagePath);
        return;
    }

// Create a Texture object usable by plugins
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

    // Configuration Options
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");  // Using Claude 3 series
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant that can analyze images.");

// Create a message with an image
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

###Multi-image analysis

```cpp
void UMyClass::AnalyzeMultipleImages()
{
// Load multiple images
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

// Create a message with multiple images
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

##Tool Calling (Function Invocation)

Claude supports Tool Calling, enabling the model to invoke predefined functions.

###Define the tool and send the request

```cpp
void UMyClass::SendClaudeToolCallRequest()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant. Use tools when needed.");

// Define tool: Get weather
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");

// Define tool parameters
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

// Optional: Set ToolChoice
    // Options.ToolChoice.Type = TEXT("auto");  // auto, any, or tool
    // Options.ToolChoice.Name = TEXT("get_weather");  // Only used when Type == "tool"

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("What's the weather like in Paris?"), EAIChatPlus_ChatRole::User}});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);

// Check if the stop reason is tool_use
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

###Processing Tool Call Result

```cpp
void UMyClass::HandleClaudeToolCallResult()
{
    // Assume this is the Tool Call information returned by the model
    FString ToolCallId = TEXT("toolu_01abc123");
    FString FunctionName = TEXT("get_weather");
    FString FunctionResult = TEXT("{\"temperature\": 18, \"unit\": \"celsius\", \"description\": \"Cloudy\"}");

    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant. Use tools when needed.");

// Redefine tools
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");
    Options.Tools.Add(WeatherTool);

// Build message history
    TArray<FAIChatPlus_ChatRequestMessage> Messages;

    // 1. User's original question
    Messages.Add({TEXT("What's the weather like in Paris?"), EAIChatPlus_ChatRole::User});

// 2. Assistant's Tool Use Request
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

// 3. Tool Execution Result
    FAIChatPlus_ChatRequestMessage ToolResultMessage;
    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;

    FAIChatPlus_ChatRequestToolCallResult ToolResult;
    ToolResult.Id = ToolCallId;
    ToolResult.FunctionName = FunctionName;
    ToolResult.FunctionResult = FunctionResult;
    ToolResultMessage.ToolCallResults.Add(ToolResult);
    Messages.Add(ToolResultMessage);

// Send request
    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###Complete Tool Call Cycle

```cpp
// Store conversation history
TArray<FAIChatPlus_ChatRequestMessage> ClaudeConversation;
FAIChatPlus_ClaudeChatRequestOptions ClaudeOptions;

void UMyClass::InitializeClaudeToolChat()
{
    ClaudeOptions.ApiKey = TEXT("your-api-key");
    ClaudeOptions.Model = TEXT("claude-3-5-sonnet-20240620");
    ClaudeOptions.bStream = true;
    ClaudeOptions.System = TEXT("You are a helpful assistant. Use tools to get real-time information.");

// Define tools
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

// Clear conversation history
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
// Add Assistant's Tool Call message
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

// Execute the tool and append the results
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

// Continue conversation
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
// Actually perform weather query
        return TEXT("{\"temperature\": 18, \"unit\": \"celsius\", \"description\": \"Cloudy\"}");
    }

    return TEXT("{\"error\": \"Unknown tool\"}");
}

void UMyClass::OnClaudeResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Claude: %s"), *Response);
}
```

##Advanced Configuration

###Use JSON extension options

```cpp
void UMyClass::UseClaudeExtraOptions()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");

// Add additional JSON options
    Options.ExtraJsonString = TEXT("{\"metadata\": {\"user_id\": \"12345\"}}");

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###Custom Endpoint URL

```cpp
void UMyClass::UseCustomClaudeEndpoint()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");

    // Using custom endpoints (like a proxy server)
    Options.BaseUrl = TEXT("https://your-proxy-server.com");
    Options.EndPointUrl = TEXT("v1/messages");

// Or set the complete URL directly
    // Options.FullUrl = TEXT("https://your-proxy-server.com/v1/messages");

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###Set Anthropic Version

```cpp
void UMyClass::SetAnthropicVersion()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");

// Set API version
    Options.AnthropicVersion = TEXT("2023-06-01");

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

##Error Handling

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

##Stop Request

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

--8<-- "footer_en.md"


> This post was translated using ChatGPT, please provide your feedback at [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions herein. 
