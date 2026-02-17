---
layout: post
title: Ollama
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
- Ollama
- Local LLM
description: Ollama
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Ollama" />

#C++ 편 - Ollama

이 문서는 C++에서 Ollama 로컬 API를 사용하여 채팅, 이미지 분석 및 Tool Calling을 수행하는 방법을 설명합니다.

Ollama는 로컬에서 대규모 언어 모델을 실행하는 도구이며, 기본 주소는 `http://localhost:11434`입니다.

##준비 작업

사용하기 전에 다음을 확인하세요:

1. **Ollama 설치 및 실행**: [ollama.com](https://ollama.com)Ollama를 다운로드하여 설치한 후 필요한 모델(예: `ollama pull llama3.2`)을 다운로드하세요.

2. 프로젝트의 `.Build.cs` 파일에 모듈 종속성을 추가합니다:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

3. 필요한 헤더 파일 포함:

```cpp
#include "Common_Ollama/AIChatPlus_OllamaChatRequest.h"
```

##문자 채팅

###기본 텍스트 채팅

```cpp
#include "Common_Ollama/AIChatPlus_OllamaChatRequest.h"

void UMyClass::SendOllamaChatRequest()
{
// 옵션 설정
    FAIChatPlus_OllamaChatRequestOptions Options;
Options.Model = TEXT("llama3.2");  // 다운로드된 모델 사용
옵션.BaseUrl = TEXT("http://localhost:11434");  // 기본 주소
    Options.bStream = true;  // 스트리밍 출력 활성화
    Options.Temperature = 0.8f;

// Ollama는 API 키가 필요하지 않습니다（로컬 서비스）

// 메시지 생성 (System 메시지 포함)
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is 2+2?"), EAIChatPlus_ChatRole::User});

// 요청 생성
    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// 콜백 바인딩
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

// 요청 보내기
    Request->SendRequest();
}
```

###다중 대화

```cpp
void UMyClass::MultiTurnOllamaChat()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

// 다중 턴 대화 기록 구성
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

###Generate API 사용하기(채팅 모드 아님)

```cpp
void UMyClass::UseOllamaGenerateAPI()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;
옵션.채팅 = 거짓;  // /api/chat 대신 /api/generate 사용
옵션.시스템 = TEXT("당신은 도움이 되는 조수입니다.");  // Chat 모드가 아닐 때만 적용됨

// Chat 모드가 아닐 경우에는 사용자 메시지만 하나면 됩니다
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

##비전(이미지 분석)

비전을 지원하는 Ollama 모델(예: `llava`, `llama3.2-vision`)은 이미지 내용을 분석할 수 있습니다.

###파일에서 사진을 불러와 분석하기

```cpp
#include "Common_Ollama/AIChatPlus_OllamaChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithOllama()
{
    // 파일에서 이미지 로드
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image: %s"), *ImagePath);
        return;
    }

// 플러그인에서 사용 가능한 Texture 객체 생성
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

// 설정 옵션
    FAIChatPlus_OllamaChatRequestOptions Options;
옵션.모델 = TEXT("llama3.2-vision");  // Vision을 지원하는 모델 사용
    Options.bStream = true;

// 이미지가 포함된 메시지 생성
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

##툴 호출(함수 호출)

일부 Ollama 모델은 Tool Calling 기능을 지원합니다.

###도구 정의 및 요청 전송

```cpp
void UMyClass::SendOllamaToolCallRequest()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
옵션.모델 = TEXT("llama3.2");  // 모델이 Tool Calling을 지원하는지 확인
    Options.bStream = true;

// 도구 정의: 날씨 가져오기
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");

// 도구 매개변수 정의
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

###툴 콜 결과 처리

```cpp
void UMyClass::HandleOllamaToolCallResult()
{
    FString ToolCallId = TEXT("call_123");
    FString FunctionName = TEXT("get_weather");
    FString FunctionResult = TEXT("{\"temperature\": 15, \"unit\": \"celsius\", \"description\": \"Rainy\"}");

    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

// 도구 재정의하기
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");
    Options.Tools.Add(WeatherTool);

// 메시지 기록 구성하기
    TArray<FAIChatPlus_ChatRequestMessage> Messages;

// 1. 시스템 메시지
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});

    // 2. 사용자 원래 질문
    Messages.Add({TEXT("What's the weather in London?"), EAIChatPlus_ChatRole::User});

// 3. 어시스턴트의 툴 호출 요청
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

// 4. 도구 실행 결과
    FAIChatPlus_ChatRequestMessage ToolResultMessage;
    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;

    FAIChatPlus_ChatRequestToolCallResult ToolResult;
    ToolResult.Id = ToolCallId;
    ToolResult.FunctionName = FunctionName;
    ToolResult.FunctionResult = FunctionResult;
    ToolResultMessage.ToolCallResults.Add(ToolResult);
    Messages.Add(ToolResultMessage);

// 요청 보내기
    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###완벽한 Tool Call 사이클

```cpp
// 대화 기록 저장
TArray<FAIChatPlus_ChatRequestMessage> OllamaConversation;
FAIChatPlus_OllamaChatRequestOptions OllamaOptions;

void UMyClass::InitializeOllamaToolChat()
{
    OllamaOptions.Model = TEXT("llama3.2");
    OllamaOptions.bStream = true;

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

    OllamaOptions.Tools.Add(WeatherTool);

// 대화 초기화 (System 메시지 추가)
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
// Assistant의 Tool Call 메시지 추가
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

// 도구 실행 및 결과 추가
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

// 대화 계속하기
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

##모델 목록 가져오기

`UAIChatPlus_OllamaModelRequest`를 사용하면 Ollama 서버에서 사용 가능한 모델 목록을 가져올 수 있습니다.

```cpp
#include "Common_Ollama/AIChatPlus_OllamaModelRequest.h"

void UMyClass::GetOllamaModels()
{
    FAIChatPlus_OllamaModelRequestOptions Options;
옵션.베이스Url = TEXT("http://localhost:11434");  // 기본 주소

    auto Request = UAIChatPlus_OllamaModelRequest::CreateWithOptions(Options);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaModelRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FString> ModelNames = Response.GetModelNames();
        for (const FString& ModelName : ModelNames)
        {
            UE_LOG(LogTemp, Display, TEXT("Available Model: %s"), *ModelName);
        }

// 상세 정보 가져오기
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

##고급 설정

###Ollama 특유의 매개변수

```cpp
void UMyClass::ConfigureOllamaAdvanced()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

// 샘플링 파라미터
    Options.Temperature = 0.7f;
Options.TopK = 40;           // Top-K 샘플링
    Options.TopP = 0.9f;         // 핵 샘플링
    Options.MinP = 0.05f;        // Min-P 샘플링

// Mirostat 샘플링 (퍼플렉서티 제어용)
옵션.Mirostat = 2;        // 0=비활성화, 1=Mirostat, 2=Mirostat 2.0
    Options.MirostatEta = 0.1f;
    Options.MirostatTau = 5.0f;

// 컨텍스트와 생성 제약
Options.NumCtx = 4096;       // 컨텍스트 윈도우 크기
Options.NumPredict = 256;    // 최대 생성 토큰 수

// 반복 패널티
    Options.RepeatLastN = 64;
    Options.RepeatPenalty = 1.1f;

// 시퀀스 정지
    Options.StopSequences.Add(TEXT("\n\n"));

    // 모델 유지 로딩 시간
옵션.계속유지 = 300;     // 초

// 랜덤 시드 (재현 가능한 생성을 위해)
    Options.Seed = 42;

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###API 키 사용하기 (원격 Ollama)

```cpp
void UMyClass::ConnectToRemoteOllama()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.BaseUrl = TEXT("https://your-ollama-server.com");
Options.ApiKey = TEXT("your-api-key");  // 서버 인증이 필요한 경우
    Options.bStream = true;

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello from remote!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###JSON 확장 옵션 사용하기

```cpp
void UMyClass::UseOllamaExtraOptions()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

// 추가 JSON 옵션 추가
    Options.ExtraJsonString = TEXT("{\"format\": \"json\"}");

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Return a JSON with name and age fields."), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

##오류 처리

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

// Ollama에 특화된 성능 지표
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

##중지 요청

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

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)누락된 부분을 지적합니다. 
