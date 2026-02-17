---
layout: post
title: OpenAI / Azure
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
description: OpenAI / Azure
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - OpenAI / Azure" />

#C++ Section - OpenAI / Azure

This document explains how to use OpenAI and Azure APIs in C++ for chat, image analysis, speech input/output, and Tool Calling.

> **Note**: The Azure API is compatible with OpenAI, and the usage is largely the same—you only need to adjust the `BaseUrl` and `ApiKey`.

##Preparation Work

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
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"
#include "Common/AIChatPlus_Log.h"
```

##Text Chat

###Basic text chat

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"

void UMyClass::SendOpenAIChatRequest()
{
// Configuration Options
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-openai-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;  // Enable streaming output
    Options.Temperature = 0.7f;
    Options.MaxOutputTokens = 1024;

// Create message
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is the capital of France?"), EAIChatPlus_ChatRole::User});

// Create request
    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    // Bind callbacks
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Message: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Token Usage: %s"), *Response.Usage.GetDescription());
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_OpenAIChatResponseError>();
        UE_LOG(LogTemp, Error, TEXT("Request Failed: %s"), *Error.GetDescription());
    });

// Send request
    Request->SendRequest();
}
```

###Using Azure API

Azure API is compatible with OpenAI, requiring only URL modification and authentication method adjustment:

```cpp
#include "Common_Azure/AIChatPlus_AzureChatRequest.h"

void UMyClass::SendAzureChatRequest()
{
    FAIChatPlus_AzureChatRequestOptions Options;
    Options.ApiKey = TEXT("your-azure-api-key");
Options.ResourceName = TEXT("your-resource-name");  // Azure resource name
    Options.DeploymentName = TEXT("your-deployment-name");  // Deployment name
    Options.ApiVersion = TEXT("2024-02-01");  // API Version
    Options.bStream = true;

    auto Request = UAIChatPlus_AzureChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System},
            {TEXT("Hello!"), EAIChatPlus_ChatRole::User}
        });

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Azure Message: %s"), *Message);
    });

    Request->SendRequest();
}
```

###Multi-turn conversation

```cpp
void UMyClass::MultiTurnConversation()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

// Construct multi-turn dialogue history
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("My name is Alice."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("Hello Alice! Nice to meet you. How can I help you today?"), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my name?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
        // The model should remember that the user's name is Alice
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##Vision (Image Analysis)

OpenAI's Vision capability enables the model to analyze image content.

###Load and analyze an image from a file

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageFromFile()
{
// Load image from file
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image: %s"), *ImagePath);
        return;
    }

    // Create a Texture object usable by the plugin
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

// Configuration Options
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
Options.Model = TEXT("gpt-4o");  // Vision requires gpt-4o or gpt-4-turbo
    Options.bStream = true;

// Create a message with images
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("What is in this image? Describe it in detail.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant that can analyze images."), EAIChatPlus_ChatRole::System},
            ImageMessage
        });

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Vision Analysis: %s"), *Message);
    });

    Request->SendRequest();
}
```

###Analysis from Texture2D (In-game Screenshot)

```cpp
void UMyClass::AnalyzeGameTexture(UTexture2D* GameTexture)
{
    if (!GameTexture)
    {
        UE_LOG(LogTemp, Error, TEXT("Invalid texture"));
        return;
    }

// Convert to Texture Plugin
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(GameTexture);

    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o");
    Options.bStream = true;

    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("Analyze this game screenshot and describe what you see.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options, {{TEXT("You are a game analyst."), EAIChatPlus_ChatRole::System}, ImageMessage});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Game Analysis: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##Audio (Voice Input/Output)

OpenAI supports voice input and voice output features (requires the `gpt-4o-audio-preview` model).

###Voice Input (Speech-to-Text)

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::SendAudioMessage()
{
    // Load audio from file
    FString AudioPath = FPaths::ProjectContentDir() / TEXT("Audio/question.wav");
    USoundWave* SoundWave = UAIChatPlus_Util::LoadSoundWav(AudioPath);

    if (!SoundWave)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load audio: %s"), *AudioPath);
        return;
    }

    // Create Sound objects available for plugins
    UAIChatPlus_Sound* ChatSound = UAIChatPlus_Sound::CreateFromSoundWave(SoundWave);

    // Configure Options
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-audio-preview"); // Model supporting audio
    Options.bStream = false;  // Audio output does not support streaming

// Create a message with audio
    FAIChatPlus_ChatRequestMessage AudioMessage;
    AudioMessage.Content = TEXT("");  // Audio messages may not require text
    AudioMessage.Role = EAIChatPlus_ChatRole::User;
    AudioMessage.Audios.Add(ChatSound);

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant. Listen to the audio and respond."), EAIChatPlus_ChatRole::System},
            AudioMessage
        });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Response to audio: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###Voice Output (Text-to-Speech)

```cpp
void UMyClass::RequestAudioOutput()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-audio-preview");
Options.bStream = false;  // Audio output does not support streaming

    // Configure audio output
    Options.Modalities.Add(EAIChatPlus_OpenAIChatModality::Text);
    Options.Modalities.Add(EAIChatPlus_OpenAIChatModality::Audio);
    Options.AudioConfig.Format = TEXT("wav");
Options.AudioConfig.Voice = TEXT("alloy");  // Optional: alloy, ash, ballad, coral, echo, sage, shimmer, verse

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System},
            {TEXT("Tell me a short joke."), EAIChatPlus_ChatRole::User}
        });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

// Get text response
        UE_LOG(LogTemp, Display, TEXT("Text Response: %s"), *Response.GetMessage());

        // Get audio response
        TArray<FAIChatPlus_ChatResponseAudioOutput> AudioOutputs = Response.GetAudioOutputs();
        for (const auto& AudioOutput : AudioOutputs)
        {
            if (AudioOutput.Sound)
            {
// Play audio
// AudioOutput.Sound is UAIChatPlus_Sound*, which can retrieve the USoundWave from it.
                UE_LOG(LogTemp, Display, TEXT("Audio Transcript: %s"), *AudioOutput.Transcript);

// Save audio to file
                FString SavePath = FPaths::ProjectSavedDir() / TEXT("Audio/response.wav");
                UAIChatPlus_Util::SaveSoundWav(AudioOutput.Sound->GetSoundWave(), SavePath);
            }
        }
    });

    Request->SendRequest();
}
```

##Tool Calling (Function Calling)

Tool Calling enables models to invoke predefined functions for accessing external data.

###Define tools and send requests

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"

void UMyClass::SendToolCallRequest()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

// Define tool: Get Weather
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a location.");

// Define tool parameters
    FAIChatPlus_ChatRequestToolProperty LocationProp;
    LocationProp.Name = TEXT("location");
    LocationProp.Description = TEXT("The city name, e.g. Beijing, Tokyo, New York");
    LocationProp.Type = TEXT("string");
    LocationProp.Required = true;

    FAIChatPlus_ChatRequestToolProperty UnitProp;
    UnitProp.Name = TEXT("unit");
    UnitProp.Description = TEXT("The temperature unit");
    UnitProp.Type = TEXT("string");
    UnitProp.Required = false;
    UnitProp.ExtraJsonString = TEXT("{\"enum\": [\"celsius\", \"fahrenheit\"]}");

    WeatherTool.Properties.Add(LocationProp);
    WeatherTool.Properties.Add(UnitProp);

    Options.Tools.Add(WeatherTool);

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant. Use tools when needed."), EAIChatPlus_ChatRole::System},
            {TEXT("What's the weather like in Tokyo?"), EAIChatPlus_ChatRole::User}
        });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

// Check for Tool Call
        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
            for (const auto& ToolCall : ToolCalls)
            {
                UE_LOG(LogTemp, Display, TEXT("Tool Call - ID: %s, Function: %s, Args: %s"),
                    *ToolCall.Id, *ToolCall.FunctionName, *ToolCall.FunctionArguments);

// Execute the actual function call here, then send the result back to the model
// Refer to the example below titled "Handling Tool Call Results"
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

###Processing Tool Call Results

When the model returns a Tool Call, you need to execute the function and send the result back to the model:

```cpp
void UMyClass::HandleToolCallAndSendResult()
{
// Assuming this is the Tool Call returned by the model
    FString ToolCallId = TEXT("call_abc123");
    FString FunctionName = TEXT("get_weather");
    FString FunctionResult = TEXT("{\"temperature\": 22, \"unit\": \"celsius\", \"description\": \"Sunny\"}");

    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

// Redefine tools (keep consistent)
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a location.");
    Options.Tools.Add(WeatherTool);

    // Build message history containing Tool Call results
    TArray<FAIChatPlus_ChatRequestMessage> Messages;

// 1. System Message
    Messages.Add({TEXT("You are a helpful assistant. Use tools when needed."), EAIChatPlus_ChatRole::System});

    // 2. User's original question
    Messages.Add({TEXT("What's the weather like in Tokyo?"), EAIChatPlus_ChatRole::User});

// 3. Assistant's Tool Call Request
    FAIChatPlus_ChatRequestMessage AssistantMessage;
    AssistantMessage.Role = EAIChatPlus_ChatRole::Assistant;
AssistantMessage.Content = TEXT("");  // May not contain text content during Tool Call

    FAIChatPlus_ChatRequestToolCall ToolCallUse;
    ToolCallUse.Id = ToolCallId;
    ToolCallUse.Type = TEXT("function");
    ToolCallUse.FunctionName = FunctionName;
    ToolCallUse.FunctionArguments = TEXT("{\"location\": \"Tokyo\"}");
    AssistantMessage.ToolCallUses.Add(ToolCallUse);
    Messages.Add(AssistantMessage);

// 4. Tool Execution Result
    FAIChatPlus_ChatRequestMessage ToolResultMessage;
    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;

    FAIChatPlus_ChatRequestToolCallResult ToolResult;
    ToolResult.Id = ToolCallId;
    ToolResult.FunctionName = FunctionName;
    ToolResult.FunctionResult = FunctionResult;
    ToolResultMessage.ToolCallResults.Add(ToolResult);
    Messages.Add(ToolResultMessage);

// Send request
    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
// The model will generate the final response based on the tool's results.
        UE_LOG(LogTemp, Display, TEXT("Final Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###Complete Tool Call cycle

Here is a complete example of a Tool Calling loop:

```cpp
// Store conversation history
TArray<FAIChatPlus_ChatRequestMessage> ConversationHistory;
FAIChatPlus_OpenAIChatRequestOptions CurrentOptions;

void UMyClass::InitializeToolChat()
{
    CurrentOptions.ApiKey = TEXT("your-api-key");
    CurrentOptions.Model = TEXT("gpt-4o-mini");
    CurrentOptions.bStream = true;

// Define tools
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a location.");

    FAIChatPlus_ChatRequestToolProperty LocationProp;
    LocationProp.Name = TEXT("location");
    LocationProp.Type = TEXT("string");
    LocationProp.Required = true;
    WeatherTool.Properties.Add(LocationProp);

    CurrentOptions.Tools.Add(WeatherTool);

// Initialize conversation
    ConversationHistory.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}

void UMyClass::SendUserMessage(const FString& UserMessage)
{
    ConversationHistory.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(CurrentOptions, ConversationHistory);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
// Handling Tool Call
            ProcessToolCalls(ToolCalls, Response.GetMessage());
        }
        else
        {
// Normal reply
            FString AssistantMessage = Response.GetMessage();
            ConversationHistory.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});
            OnAssistantResponse(AssistantMessage);
        }
    });

    Request->SendRequest();
}

void UMyClass::ProcessToolCalls(const TArray<FAIChatPlus_ChatResponseToolCall>& ToolCalls, const FString& AssistantContent)
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
    ConversationHistory.Add(AssistantMsg);

// Execute each tool and add the results
    FAIChatPlus_ChatRequestMessage ToolResultMsg;
    ToolResultMsg.Role = EAIChatPlus_ChatRole::Tool;

    for (const auto& ToolCall : ToolCalls)
    {
        FString Result = ExecuteTool(ToolCall.FunctionName, ToolCall.FunctionArguments);

        FAIChatPlus_ChatRequestToolCallResult ToolResult;
        ToolResult.Id = ToolCall.Id;
        ToolResult.FunctionName = ToolCall.FunctionName;
        ToolResult.FunctionResult = Result;
        ToolResultMsg.ToolCallResults.Add(ToolResult);
    }
    ConversationHistory.Add(ToolResultMsg);

    // Send the request with tool results
    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(CurrentOptions, ConversationHistory);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> NewToolCalls = Response.GetToolCalls();
        if (NewToolCalls.Num() > 0)
        {
// May need to continue invoking the tool
            ProcessToolCalls(NewToolCalls, Response.GetMessage());
        }
        else
        {
            FString FinalMessage = Response.GetMessage();
            ConversationHistory.Add({FinalMessage, EAIChatPlus_ChatRole::Assistant});
            OnAssistantResponse(FinalMessage);
        }
    });

    Request->SendRequest();
}

FString UMyClass::ExecuteTool(const FString& FunctionName, const FString& Arguments)
{
    if (FunctionName == TEXT("get_weather"))
    {
// Parse the parameters and execute the actual weather query
// Here returns simulated data
        return TEXT("{\"temperature\": 22, \"unit\": \"celsius\", \"description\": \"Sunny\"}");
    }

    return TEXT("{\"error\": \"Unknown function\"}");
}

void UMyClass::OnAssistantResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Assistant: %s"), *Response);
}
```

##Image Generation

Generating images using OpenAI's DALL-E model:

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIImageRequest.h"

void UMyClass::GenerateImage()
{
    FAIChatPlus_OpenAIImageRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("dall-e-3");
    Options.ChatType = EAIChatPlus_ImageChatType::Generation;
    Options.Size = TEXT("1024x1024");
    Options.Quality = EAIChatPlus_OpenAIImageQuality::Standard;
    Options.ResponseFormat = EAIChatPlus_OpenAIImageResponseFormat::Url;

    auto Request = UAIChatPlus_OpenAIImageRequest::CreateWithOptions(Options);
    Request->SetPrompt(TEXT("A beautiful sunset over mountains, digital art style"));

    Request->OnImagesListeners.AddLambda([](const TArray<UTexture2D*>& Images, bool bFinished)
    {
        for (int32 i = 0; i < Images.Num(); ++i)
        {
            if (Images[i])
            {
// Save image
                FString SavePath = FString::Printf(TEXT("%s/GeneratedImages/image_%d.png"),
                    *FPaths::ProjectSavedDir(), i);
                UAIChatPlus_Util::SaveImage(Images[i], SavePath);
                UE_LOG(LogTemp, Display, TEXT("Image saved to: %s"), *SavePath);
            }
        }
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_OpenAIChatResponseError>();
        UE_LOG(LogTemp, Error, TEXT("Image generation failed: %s"), *Error.GetDescription());
    });

    Request->SendRequest();
}
```

##Advanced Configuration

###Using JSON Extension Options

Add options not directly supported by the API through `ExtraJsonString` or `ExtraJsonObject`:

```cpp
void UMyClass::UseExtraJsonOptions()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");

// Add extra options using a JSON string
    Options.ExtraJsonString = TEXT("{\"store\": false, \"metadata\": {\"user_id\": \"12345\"}}");

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###Custom Endpoint URL

Support using custom API endpoints (such as proxy servers):

```cpp
void UMyClass::UseCustomEndpoint()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");

// Method 1: Set BaseUrl and EndPointUrl separately
    Options.BaseUrl = TEXT("https://your-proxy-server.com");
    Options.EndPointUrl = TEXT("v1/chat/completions");

// Method 2: Set the complete URL directly (BaseUrl and EndPointUrl will be ignored)
    // Options.FullUrl = TEXT("https://your-proxy-server.com/v1/chat/completions");

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

##Error Handling

###Complete Error Handling Example

```cpp
void UMyClass::RobustChatRequest()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->OnStartedListeners.AddLambda([]()
    {
        UE_LOG(LogTemp, Display, TEXT("Request started..."));
    });

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
// Streaming message
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

// Check if the response contains any errors
        if (Response.HasError())
        {
            UE_LOG(LogTemp, Error, TEXT("Response error: %s"), *Response.Error.GetDescription());
            return;
        }

        UE_LOG(LogTemp, Display, TEXT("Success: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Tokens used: %s"), *Response.Usage.GetDescription());
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_OpenAIChatResponseError>();
        UE_LOG(LogTemp, Error, TEXT("Request failed!"));
        UE_LOG(LogTemp, Error, TEXT("  Code: %s"), *Error.Code);
        UE_LOG(LogTemp, Error, TEXT("  Type: %s"), *Error.Type);
        UE_LOG(LogTemp, Error, TEXT("  Message: %s"), *Error.Message);
        UE_LOG(LogTemp, Error, TEXT("  Param: %s"), *Error.Param);
    });

    Request->SendRequest();
}
```

##Stop Request

Ongoing requests can be stopped:

```cpp
// Store request reference
UPROPERTY()
UAIChatPlus_OpenAIChatRequest* CurrentRequest = nullptr;

void UMyClass::StartRequest()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    // ... configuration options

    CurrentRequest = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a very long story."), EAIChatPlus_ChatRole::User}});

    CurrentRequest->SendRequest();
}

void UMyClass::CancelRequest()
{
    if (CurrentRequest && CurrentRequest->IsActivated())
    {
        CurrentRequest->StopRequest();
        UE_LOG(LogTemp, Display, TEXT("Request cancelled"));
    }
}
```

--8<-- "footer_en.md"


> This post was translated using ChatGPT, please provide feedback at [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions therein. 
