---
layout: post
title: Gemini
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
- Gemini
- Google
description: Gemini
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Gemini" />

#C++ 편 - Gemini

이 문서는 C++에서 Google Gemini API를 사용해 채팅, 이미지 분석 및 Tool Calling을 수행하는 방법을 설명합니다.

##준비 작업

사용하기 전에 다음 사항을 확인하세요:

1. 프로젝트의 `.Build.cs` 파일에 모듈 의존성을 추가하세요:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

2. 필요한 헤더 파일 포함하기:

```cpp
#include "Common_Gemini/AIChatPlus_GeminiChatRequest.h"
```

##텍스트 채팅

###기본 텍스트 채팅

```cpp
#include "Common_Gemini/AIChatPlus_GeminiChatRequest.h"

void UMyClass::SendGeminiChatRequest()
{
// 옵션 설정
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-google-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
Options.bStream = true;  // 스트리밍 출력 활성화
    Options.MaxOutputTokens = 1024;
    Options.Temperature = 0.7f;

// Gemini의 System Prompt는 Options.System을 통해 설정됩니다
    Options.System = TEXT("You are a helpful assistant.");

// 사용자 메시지 생성
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("What is the capital of Japan?"), EAIChatPlus_ChatRole::User});

// 요청 생성
    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// 콜백 바인딩
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

    // 요청 보내기
    Request->SendRequest();
}
```

###다중대화

```cpp
void UMyClass::MultiTurnGeminiChat()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant with a good memory.");

// 다중 대화 기록 구성
// Gemini는 "user"와 "model"을 역할로 사용합니다
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("My name is Alice."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("Hello Alice! Nice to meet you. How can I help you today?"), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my name?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);
        // 모델은 사용자 이름이 Alice라는 것을 기억해야 함
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##비전 (이미지 분석)

Gemini 모델은 Vision 기능을 지원하여 이미지 내용을 분석할 수 있습니다.

> **참고**: Gemini Vision은 최대 20장의 이미지를 지원합니다(`FAIChatPlus_Constants::FGemini::MaxSendImageNum = 20`).

###파일에서 이미지를 로드하고 분석하기

```cpp
#include "Common_Gemini/AIChatPlus_GeminiChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithGemini()
{
// 파일에서 이미지 불러오기
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image: %s"), *ImagePath);
        return;
    }

// 플러그인에서 사용할 수 있는 Texture 객체 생성
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

// 옵션 설정
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
옵션.모델 = 텍스트("gemini-1.5-flash");  // 또는 gemini-1.5-pro
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant that can analyze images.");

// 이미지가 포함된 메시지 생성
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

###다중 이미지 분석

```cpp
void UMyClass::AnalyzeMultipleImagesWithGemini()
{
// 여러 이미지 불러오기
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

// 여러 장의 사진이 포함된 메시지 생성
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

##도구 호출 (함수 호출)

제미니는 툴 콜링(Function Calling)을 지원하여 모델이 미리 정의된 함수를 호출할 수 있도록 합니다.

###도구 정의 및 요청 보내기

```cpp
void UMyClass::SendGeminiToolCallRequest()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant. Use tools when needed.");

// 도구 정의: 날씨 가져오기
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");

// 도구 매개변수 정의
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

###툴 콜 결과 처리

```cpp
void UMyClass::HandleGeminiToolCallResult()
{
// 가정하자면 모델이 반환한 Tool Call 정보이다
    FString ToolCallId = TEXT("call_abc123");
    FString FunctionName = TEXT("get_weather");
    FString FunctionResult = TEXT("{\"temperature\": 25, \"unit\": \"celsius\", \"description\": \"Sunny\"}");

    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;

// 도구 재정의하기
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");
    Options.Tools.Add(WeatherTool);

// 메시지 기록 구성
    TArray<FAIChatPlus_ChatRequestMessage> Messages;

// 1. 사용자 원본 질문
    Messages.Add({TEXT("What's the weather like in Tokyo?"), EAIChatPlus_ChatRole::User});

// 2. Assistant의 Tool Call 요청
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

// 3. 도구 실행 결과
    FAIChatPlus_ChatRequestMessage ToolResultMessage;
    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;

    FAIChatPlus_ChatRequestToolCallResult ToolResult;
    ToolResult.Id = ToolCallId;
    ToolResult.FunctionName = FunctionName;
    ToolResult.FunctionResult = FunctionResult;
    ToolResultMessage.ToolCallResults.Add(ToolResult);
    Messages.Add(ToolResultMessage);

// 요청 보내기
    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###완전한 Tool Call 사이클

```cpp
// 대화 기록 저장
TArray<FAIChatPlus_ChatRequestMessage> GeminiConversation;
FAIChatPlus_GeminiChatRequestOptions GeminiOptions;

void UMyClass::InitializeGeminiToolChat()
{
    GeminiOptions.ApiKey = TEXT("your-api-key");
    GeminiOptions.Model = TEXT("gemini-1.5-flash");
    GeminiOptions.bStream = true;
    GeminiOptions.System = TEXT("You are a helpful assistant. Use tools when needed.");

// 도구 정의
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

// 대화 기록 초기화
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
// Assistant의 Tool 호출 메시지 추가
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

// 도구를 실행하고 결과를 추가합니다
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

// 대화 계속하기
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
// 실제 날씨 조회 실행
        return TEXT("{\"temperature\": 25, \"unit\": \"celsius\", \"description\": \"Sunny\"}");
    }

    return TEXT("{\"error\": \"Unknown tool\"}");
}

void UMyClass::OnGeminiResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Gemini: %s"), *Response);
}
```

##고급 구성

###JSON 확장 옵션 사용하기

```cpp
void UMyClass::UseGeminiExtraOptions()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");

// 추가 JSON 옵션 설정
    Options.ExtraJsonString = TEXT("{\"safetySettings\": [{\"category\": \"HARM_CATEGORY_HARASSMENT\", \"threshold\": \"BLOCK_NONE\"}]}");

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###사용자 정의 엔드포인트 URL

```cpp
void UMyClass::UseCustomGeminiEndpoint()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");

// 사용자 정의 엔드포인트 사용 (예: 프록시 서버)
    Options.BaseUrl = TEXT("https://your-proxy-server.com/v1beta/models");
옵션.메서드 = 텍스트("콘텐츠 생성");  // 또는 스트림 생성 콘텐츠

    // 또는 직접 전체 URL 설정
    // Options.FullUrl = TEXT("https://your-proxy-server.com/v1beta/models/gemini-1.5-flash:generateContent?key=xxx");

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###샘플링 매개변수 설정

```cpp
void UMyClass::ConfigureGeminiSampling()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-pro");

// 샘플링 파라미터
Options.Temperature = 0.3f;  // 낮은 온도로, 더 결정적인 출력
Options.TopK = 40;           // Top-K 샘플링
Options.TopP = 0.95f;        // 뉴클리어스 샘플링
    Options.MaxOutputTokens = 2048;

// 시퀀스 중지
    Options.StopSequences.Add(TEXT("\n\n"));
    Options.StopSequences.Add(TEXT("END"));

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a short story."), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

##에러 처리

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

// FinishReason 확인
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

##정지 요청

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

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)누락된 부분을 지적합니다. 
