---
layout: post
title: CllamaServer
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
- llama.cpp
- Local Server
description: CllamaServer
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - CllamaServer" />

#C++ 편 - CllamaServer

이 문서는 C++에서 CllamaServer를 사용하여 로컬 AI 서버를 관리하고 채팅 요청을 보내는 방법을 설명합니다.

CllamaServer는 llama.cpp의 서버 모드에서 실행되며, OpenAI API와 호환되는 로컬 서비스를 제공합니다. 여러 클라이언트의 동시 요청을 지원합니다.

##Cllama와의 차이점

| 특성 | Cllama | CllamaServer |
|------|--------|--------------|
| 모드 | 직접 추론 | HTTP 서버 |
| 다중 클라이언트 | 아니오 | 예 |
| API 스타일 | 커스터마이징 | OpenAI 호환 |
| 네트워크 접근 | 아니오 | 선택적 |
| 도구 호출 | 아니오 | 예 |

##준비 작업

사용하기 전에 다음 사항을 확인하십시오:

1. **GGUF 모델 파일 다운로드**: [Hugging Face](https://huggingface.co)호환 가능한 GGUF 형식 모델 파일을 다운로드하세요.

2. 프로젝트의 `.Build.cs` 파일에 모듈 종속성을 추가합니다:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

3. 필요한 헤더 파일 포함하기:

```cpp
#include "Common_CllamaServer/AIChatPlus_CllamaServer.h"
#include "Common_CllamaServer/AIChatPlus_CllamaServerChatRequest.h"
```

##서버 관리

###서버 시작하기 (기초)

```cpp
#include "Common_CllamaServer/AIChatPlus_CllamaServer.h"

UPROPERTY()
UAIChatPlus_CllamaServer* LocalServer = nullptr;

void UMyClass::StartCllamaServer()
{
// 서버 파라미터 설정
    FAIChatPlus_CllamaServerParam Params;
    Params.Model = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
Params.NGpuLayers = -1;      // -1 = GPU 레이어 수 자동 할당
Params.Port = 0;             // 0 = 사용 가능한 포트 자동 할당
    Params.Host = TEXT("127.0.0.1");

// 서버 생성 및 시작
    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params);

    // 서버 시작 콜백 바인딩
    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnServerStarted);
    LocalServer->OnStoppedListeners.AddDynamic(this, &UMyClass::OnServerStopped);
    LocalServer->OnFailedListeners.AddDynamic(this, &UMyClass::OnServerFailed);

// 서버 활성화(시작 프로세스 실행)
    LocalServer->Activate();
}

void UMyClass::OnServerStarted(FGuid ServerID)
{
// 서버 정보 가져오기
    FAIChatPlus_CllamaServerInfo Info;
    if (LocalServer->GetServerInfo(Info))
    {
        UE_LOG(LogTemp, Display, TEXT("Server started at: %s"), *Info.HttpAddress);
        UE_LOG(LogTemp, Display, TEXT("Port: %d"), Info.Port);
    }
}

void UMyClass::OnServerStopped(FGuid ServerID)
{
    UE_LOG(LogTemp, Display, TEXT("Server stopped: %s"), *ServerID.ToString());
}

void UMyClass::OnServerFailed(FGuid ServerID, const FString& ErrorMessage)
{
    UE_LOG(LogTemp, Error, TEXT("Server failed: %s"), *ErrorMessage);
}
```

###서버 관리를 위해 Handler 사용하기

```cpp
#include "Common_CllamaServer/AIChatPlus_CllamaServer.h"
#include "Common_CllamaServer/AIChatPlus_CllamaServerHandler.h"

void UMyClass::StartServerWithHandler()
{
    FAIChatPlus_CllamaServerParam Params;
    Params.Model = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Params.NGpuLayers = 99;
    Params.Port = 8080;

// 핸들러 생성
    auto ServerHandler = UAIChatPlus_CllamaServerHandler::CreateHandler();

// 네이티브 콜백 바인딩 (Non-Dynamic)
    ServerHandler->OnStarted.AddLambda([](FGuid ServerID)
    {
        UE_LOG(LogTemp, Display, TEXT("Server started: %s"), *ServerID.ToString());
    });

    ServerHandler->OnStopped.AddLambda([](FGuid ServerID)
    {
        UE_LOG(LogTemp, Display, TEXT("Server stopped: %s"), *ServerID.ToString());
    });

    ServerHandler->OnFailed.AddLambda([](FGuid ServerID, const FString& Error)
    {
        UE_LOG(LogTemp, Error, TEXT("Server failed: %s - %s"), *ServerID.ToString(), *Error);
    });

// Handler를 사용하여 서버 생성
    LocalServer = UAIChatPlus_CllamaServer::CreateServerWithHandler(Params, ServerHandler);
    LocalServer->Activate();
}
```

###지정 서버 ID

```cpp
void UMyClass::StartServerWithCustomID()
{
    FAIChatPlus_CllamaServerParam Params;
    Params.Model = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Params.NGpuLayers = 99;

// 사용자 지정 서버 ID 지정 (향후 ID를 통해 관리하기 위함)
    FGuid CustomServerID = FGuid::NewGuid();

    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params, CustomServerID);

    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnServerStarted);
    LocalServer->Activate();
}
```

###서버 중지

```cpp
void UMyClass::StopServer()
{
    if (LocalServer)
    {
        LocalServer->StopServer();
    }
}

// ID로 서버 중지하기
void UMyClass::StopServerByID(const FGuid& ServerID)
{
    UAIChatPlus_CllamaServer::StopServerByID(ServerID);
}

// 모든 서버 중지
void UMyClass::StopAllServers()
{
    UAIChatPlus_CllamaServer::StopAllServers();
}
```

###서버 상태 조회

```cpp
void UMyClass::CheckServerStatus()
{
// 현재 서버 인스턴스 확인
    if (LocalServer && LocalServer->IsRunning())
    {
        FString Host = LocalServer->GetHost();
        int32 Port = LocalServer->GetPort();
        FString Address = LocalServer->GetAddress();

        UE_LOG(LogTemp, Display, TEXT("Server running at: %s:%d"), *Host, Port);
    }

// ID를 통해 서버 상태 확인하기
    FGuid ServerID = LocalServer->GetServerID();
    if (UAIChatPlus_CllamaServer::IsServerRunning(ServerID))
    {
        FAIChatPlus_CllamaServerInfo Info = UAIChatPlus_CllamaServer::GetServerInfoByID(ServerID);
        UE_LOG(LogTemp, Display, TEXT("Server info: %s"), *Info.HttpAddress);
    }
}

void UMyClass::ListAllServers()
{
    TArray<FGuid> AllServerIDs = UAIChatPlus_CllamaServer::GetAllServerIDs();

    for (const FGuid& ServerID : AllServerIDs)
    {
        FAIChatPlus_CllamaServerInfo Info = UAIChatPlus_CllamaServer::GetServerInfoByID(ServerID);
        UE_LOG(LogTemp, Display, TEXT("Server: %s - Running: %s"),
            *ServerID.ToString(),
            Info.bIsRunning ? TEXT("Yes") : TEXT("No"));
    }
}
```

##텍스트 채팅

###기본 문자 채팅

```cpp
#include "Common_CllamaServer/AIChatPlus_CllamaServerChatRequest.h"

void UMyClass::SendCllamaServerChatRequest()
{
    // 서버가 시작되었는지 확인
    if (!LocalServer || !LocalServer->IsRunning())
    {
        UE_LOG(LogTemp, Error, TEXT("Server is not running"));
        return;
    }

// 요청 옵션 설정 (OpenAI 스타일에서 상속됨)
    FAIChatPlus_CllamaServerChatRequestOptions Options;
옵션.베이스URL = 로컬서버->주소얻기();  // 예: "http://127.0.0.1:8080"
옵션.모델 = TEXT("로컬-모델");          // 모델 이름(사용자 정의 가능)
    Options.bStream = true;
    Options.Temperature = 0.8f;

// 메시지 생성
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is the meaning of life?"), EAIChatPlus_ChatRole::User});

// 요청 생성
    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    // 콜백 바인딩
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("CllamaServer: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);
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

###다중 대화

```cpp
// 멤버 변수
TArray<FAIChatPlus_ChatRequestMessage> CllamaServerConversation;

void UMyClass::InitializeCllamaServerChat()
{
    CllamaServerConversation.Empty();
    CllamaServerConversation.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}

void UMyClass::SendMessage(const FString& UserMessage)
{
    CllamaServerConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    FAIChatPlus_CllamaServerChatRequestOptions Options;
    Options.BaseUrl = LocalServer->GetAddress();
    Options.bStream = true;

    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(
        Options, CllamaServerConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);
        FString AssistantMessage = Response.GetMessage();
        CllamaServerConversation.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});

        UE_LOG(LogTemp, Display, TEXT("Assistant: %s"), *AssistantMessage);
    });

    Request->SendRequest();
}
```

##Vision（이미지 분석）

Vision을 사용하려면 서버 시작 시 MMProject 모델을 지정해야 합니다.

###비전 지원 서버 시작하기

```cpp
void UMyClass::StartVisionServer()
{
    FAIChatPlus_CllamaServerParam Params;

// LLaVA 모델
    Params.Model = TEXT("D:/Models/llava-v1.6-mistral-7b.Q4_K_M.gguf");
Params.MMProj = TEXT("D:/Models/mmproj-llava-v1.6-mistral-7b-f16.gguf");  // 핵심: MMProject 모델

    Params.NGpuLayers = 99;
    Params.Port = 8080;

    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params);
    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnVisionServerStarted);
    LocalServer->Activate();
}
```

###이미지 분석 요청 전송

```cpp
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithCllamaServer()
{
    if (!LocalServer || !LocalServer->IsRunning())
    {
        UE_LOG(LogTemp, Error, TEXT("Vision server is not running"));
        return;
    }

// 이미지 로드
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image"));
        return;
    }

    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

// 요청 구성
    FAIChatPlus_CllamaServerChatRequestOptions Options;
    Options.BaseUrl = LocalServer->GetAddress();
    Options.bStream = true;

// 이미지가 포함된 메시지 생성
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("What do you see in this image?");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(
        Options, {ImageMessage});

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Vision: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##도구 호출（함수 호출）

CllamaServer는 OpenAI 스타일의 Tool Call을 지원합니다(함수 호출을 지원하는 모델 필요).

###Tool Call을 지원하는 서버 시작하기

```cpp
void UMyClass::StartToolCallServer()
{
    FAIChatPlus_CllamaServerParam Params;
    Params.Model = TEXT("D:/Models/llama-3.1-8b-instruct-q4_k_m.gguf");
    Params.NGpuLayers = 99;
    Params.Port = 8080;
Params.bUseJinja = true;  // 툴 콜에 Jinja 템플릿 사용을 활성화해야 합니다

    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params);
    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnToolCallServerStarted);
    LocalServer->Activate();
}
```

###도구 정의 및 사용

```cpp
void UMyClass::SendToolCallRequest()
{
    if (!LocalServer || !LocalServer->IsRunning())
    {
        UE_LOG(LogTemp, Error, TEXT("Tool call server is not running"));
        return;
    }

    FAIChatPlus_CllamaServerChatRequestOptions Options;
    Options.BaseUrl = LocalServer->GetAddress();
Options.bStream = false;  // 툴 호출 시 스트리밍 비활성화 권장

// 도구 정의
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = TEXT("function");
    WeatherTool.Function.Name = TEXT("get_weather");
    WeatherTool.Function.Description = TEXT("Get the current weather for a location");
    WeatherTool.Function.Parameters = TEXT(R"({
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit"
            }
        },
        "required": ["location"]
    })");

    Options.Tools.Add(WeatherTool);

    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is the weather like in Tokyo?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);

// 도구 호출이 있는지 확인합니다
        if (Response.Choices.Num() > 0)
        {
            const auto& Choice = Response.Choices[0];
            const auto& ToolCalls = Choice.Message.ToolCalls;

            if (ToolCalls.Num() > 0)
            {
                for (const auto& ToolCall : ToolCalls)
                {
                    UE_LOG(LogTemp, Display, TEXT("Tool Call: %s(%s)"),
                        *ToolCall.Function.Name, *ToolCall.Function.Arguments);

// 도구 호출을 실행하고 대화를 계속합니다
                    ExecuteToolCall(ToolCall);
                }
            }
            else
            {
                UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
            }
        }
    });

    Request->SendRequest();
}
```

###완전한 Tool Call 사이클

```cpp
TArray<FAIChatPlus_ChatRequestMessage> ToolCallConversation;
FAIChatPlus_CllamaServerChatRequestOptions ToolCallOptions;

void UMyClass::InitializeToolCallChat()
{
    ToolCallOptions.BaseUrl = LocalServer->GetAddress();
    ToolCallOptions.bStream = false;

// 도구 정의하기
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = TEXT("function");
    WeatherTool.Function.Name = TEXT("get_weather");
    WeatherTool.Function.Description = TEXT("Get the current weather");
    WeatherTool.Function.Parameters = TEXT(R"({
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City name"}
        },
        "required": ["location"]
    })");
    ToolCallOptions.Tools.Add(WeatherTool);

    ToolCallConversation.Empty();
    ToolCallConversation.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}

void UMyClass::SendToolCallMessage(const FString& UserMessage)
{
    ToolCallConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(
        ToolCallOptions, ToolCallConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.Choices.Num() > 0)
        {
            const auto& Choice = Response.Choices[0];
            const auto& ToolCalls = Choice.Message.ToolCalls;

            if (ToolCalls.Num() > 0)
            {
// 1. Assistant의 도구 호출 요청을 기록에 추가
                FAIChatPlus_ChatRequestMessage AssistantMessage;
                AssistantMessage.Role = EAIChatPlus_ChatRole::Assistant;
                AssistantMessage.ToolCallUses = ToolCalls;
                ToolCallConversation.Add(AssistantMessage);

// 2. 도구 실행 후 결과 추가
                for (const auto& ToolCall : ToolCalls)
                {
                    FString Result = ExecuteToolFunction(ToolCall.Function.Name, ToolCall.Function.Arguments);

                    FAIChatPlus_ChatRequestMessage ToolResultMessage;
                    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;
                    ToolResultMessage.Content = Result;
                    ToolResultMessage.ToolCallId = ToolCall.Id;
                    ToolCallConversation.Add(ToolResultMessage);
                }

// 3. 대화를 계속하여 모델이 도구 결과를 처리하게 합니다
                ContinueToolCallConversation();
            }
            else
            {
// 일반적인 답변
                FString AssistantResponse = Response.GetMessage();
                ToolCallConversation.Add({AssistantResponse, EAIChatPlus_ChatRole::Assistant});
                UE_LOG(LogTemp, Display, TEXT("Final: %s"), *AssistantResponse);
            }
        }
    });

    Request->SendRequest();
}

FString UMyClass::ExecuteToolFunction(const FString& FunctionName, const FString& Arguments)
{
    if (FunctionName == TEXT("get_weather"))
    {
// 매개변수를 분석하고 결과를 반환합니다
        return TEXT("{\"temperature\": \"22\", \"condition\": \"sunny\", \"unit\": \"celsius\"}");
    }
    return TEXT("{\"error\": \"Unknown function\"}");
}

void UMyClass::ContinueToolCallConversation()
{
    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(
        ToolCallOptions, ToolCallConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);
        FString FinalResponse = Response.GetMessage();
        ToolCallConversation.Add({FinalResponse, EAIChatPlus_ChatRole::Assistant});

        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *FinalResponse);
    });

    Request->SendRequest();
}
```

##서버 고급 구성

###전체 구성 예시

```cpp
void UMyClass::StartAdvancedServer()
{
    FAIChatPlus_CllamaServerParam Params;

// ===== 모델 구성 =====
    Params.Model = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
Params.Alias = TEXT("my-local-model");    // 모델 별칭
Params.MMProj = TEXT("");                 // 비전 MMProject 모델 경로

// ===== 하드웨어 구성 =====
Params.NGpuLayers = 99;      // GPU 레이어 수 (-1 = 자동)
Params.Threads = -1;         // CPU 스레드 수(-1 = 자동)
Params.ThreadsBatch = -1;    // 배치 처리 스레드 수

// ===== 컨텍스트 설정 =====
Params.CtxSize = 4096;       // 컨텍스트 윈도우 크기
Params.NPredict = -1;        // 최대 생성 토큰 수 (-1 = 무제한)
Params.BatchSize = 2048;     // 논리적 배치 크기
Params.UbatchSize = 512;     // 물리적 배치 크기
Params.Keep = 0;             // 유지할 초기 토큰 수

// ===== 샘플링 설정 =====
    Params.Temperature = 0.8f;
    Params.TopK = 40;
    Params.TopP = 0.9f;
    Params.MinP = 0.1f;
    Params.RepeatLastN = 64;
    Params.RepeatPenalty = 1.0f;
    Params.PresencePenalty = 0.0f;
    Params.FrequencyPenalty = 0.0f;
Params.Seed = 0xFFFFFFFF;    // 랜덤 시드 (0xFFFFFFFF = 랜덤)

// ===== 서버 설정 =====
    Params.Host = TEXT("127.0.0.1");
Params.Port = 8080;          // 0 = 자동 할당
Params.Timeout = 600;        // 타임아웃 시간(초)
Params.Parallel = 1;         // 병렬 요청 수
Params.bContBatching = true; // 연속 배치 처리
Params.bSlots = true;        // 슬롯 모니터링 엔드포인트 활성화

// ===== 기능 설정 =====
Params.bUseJinja = true;     // Jinja 템플릿 사용 (Tool Call에 필요)
Params.bNoWebUI = false;     // 웹 UI 비활성화
Params.ApiKey = TEXT("");    // API 키 인증
Params.ChatTemplate = TEXT("");  // 사용자 지정 채팅 템플릿

// ===== 디버그 설정 =====
Params.bVerbose = true;      // 상세 로그

    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params);
    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnServerStarted);
    LocalServer->Activate();
}
```

##오류 처리

```cpp
void UMyClass::RobustCllamaServerRequest()
{
// 서버 상태 확인
    if (!LocalServer)
    {
        UE_LOG(LogTemp, Error, TEXT("Server instance is null"));
        return;
    }

    if (!LocalServer->IsRunning())
    {
        UE_LOG(LogTemp, Error, TEXT("Server is not running"));
        return;
    }

    FAIChatPlus_CllamaServerChatRequestOptions Options;
    Options.BaseUrl = LocalServer->GetAddress();
    Options.bStream = true;

    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->OnStartedListeners.AddLambda([]()
    {
        UE_LOG(LogTemp, Display, TEXT("Request started"));
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.HasError())
        {
            UE_LOG(LogTemp, Error, TEXT("Response error: %s"), *Response.Error.GetDescription());
            return;
        }

        UE_LOG(LogTemp, Display, TEXT("Success: %s"), *Response.GetMessage());
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_ResponseErrorBase>();
        UE_LOG(LogTemp, Error, TEXT("Request failed: %s"), *Error.GetDescription());
    });

    Request->SendRequest();
}
```

##자원 정리

```cpp
void UMyClass::CleanupCllamaServer()
{
// 모든 요청 중지
    // ...

// 서버 중지
    if (LocalServer)
    {
        LocalServer->StopServer();
        LocalServer = nullptr;
    }

// 또는 모든 서버 중지
    UAIChatPlus_CllamaServer::StopAllServers();
}

// Actor가 파괴될 때 정리하기
void AMyActor::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    CleanupCllamaServer();
    Super::EndPlay(EndPlayReason);
}
```

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)누락된 부분을 지적합니다. 
