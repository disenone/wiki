---
layout: post
title: Cllama(폐기됨)
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
- Cllama
- llama.cpp
- Offline LLM
description: Cllama
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Cllama" />

#C++ 편 - Cllama(폐기됨)

##폐기됨

Cllama는 **폐기**됨으로 표시되었으며, 더 이상 유지되지 않습니다.

Cllama의 기존 기능은 [CllamaServer](ue-插件-AIChatPlus-Usage-Source-CllamaServer.md)담아 올.

##오프라인 모델

이 문서는 C++에서 Cllama(llama.cpp를 통합)를 사용하여 오프라인 로컬 추론을 수행하는 방법을 설명합니다.

Cllama는 네트워크 연결 없이도 대규모 언어 모델을 실행할 수 있게 해주며, 오프라인 추론이 필요하거나 개인 정보 보호가 중요한 상황에 적합합니다.

##준비 작업

사용하기 전에 다음 사항을 확인하세요:

1. **GGUF 모델 파일 다운로드**: [Hugging Face](https://huggingface.co)호환 가능한 GGUF 형식 모델 파일을 다운로드하세요.

2. 프로젝트의 `.Build.cs` 파일에 모듈 의존성을 추가하세요:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

3. 필요한 헤더 파일 포함:

```cpp
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"
```

##Cllama 사용 가능 여부 확인

사용 전 Cllama가 사용 가능한지 및 지원되는 백엔드를 확인할 수 있습니다:

```cpp
#include "Common/AIChatPlus_Util.h"

void UMyClass::CheckCllamaSupport()
{
// Cllama 사용 가능 여부 확인
    if (UAIChatPlus_Util::Cllama_IsValid())
    {
        UE_LOG(LogTemp, Display, TEXT("Cllama is available"));

// GPU 지원 여부 확인
        if (UAIChatPlus_Util::Cllama_IsSupportGpu())
        {
            UE_LOG(LogTemp, Display, TEXT("GPU acceleration is supported"));
        }

// 지원되는 백엔드 목록 가져오기
        TArray<FString> Backends = UAIChatPlus_Util::Cllama_GetSupportBackends();
        for (const FString& Backend : Backends)
        {
            UE_LOG(LogTemp, Display, TEXT("Supported backend: %s"), *Backend);
        }
    }
    else
    {
        UE_LOG(LogTemp, Error, TEXT("Cllama is not available on this platform"));
    }
}
```

##텍스트 채팅

###기본 텍스트 채팅

```cpp
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"

void UMyClass::SendCllamaChatRequest()
{
// 옵션 설정
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
Options.bStream = true;  // 스트리밍 출력 활성화
    Options.Temperature = 0.8f;
옵션.NumGpuLayers = 99;  // GPU 가속 레이어 수 (0 = CPU 전용)

// 메시지 생성
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is the meaning of life?"), EAIChatPlus_ChatRole::User});

// 요청 생성
    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// 콜백 바인딩
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Cllama: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
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

###Content 디렉토리를 기준으로 한 상대 경로 사용

```cpp
void UMyClass::UseRelativeModelPath()
{
    FAIChatPlus_CllamaChatRequestOptions Options;

// 프로젝트 Content 디렉터리에 상대적인 경로
    Options.ModelPath.FilePath = TEXT("Models/llama-3.2-1b-instruct-q4_k_m.gguf");

    Options.bStream = true;
    Options.NumGpuLayers = 99;

    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Hello!"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###Pak 파일에서 모델 로드

```cpp
void UMyClass::LoadModelFromPak()
{
// 모델이 Pak 파일에 패키징된 경우, 먼저 모델 경로를 준비해야 합니다
    FString ModelPath = TEXT("Models/my_model.gguf");

// 이 함수는 Pak 안의 모델을 임시 디렉토리에 압축 해제하고 실제 경로를 반환합니다
    FString ActualPath = UAIChatPlus_Util::Cllama_PrepareModelPathFromPak(ModelPath);

    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = ActualPath;
    Options.bStream = true;

    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Hello from Pak!"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);
    Request->SendRequest();
}
```

###다중 대화

```cpp
void UMyClass::MultiTurnCllamaChat()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;

// 다중 대화 기록 구축
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("My favorite color is blue."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("That's a great choice! Blue is often associated with calmness."), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my favorite color?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###모델이 계속 로딩 중입니다

```cpp
void UMyClass::KeepModelLoaded()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;

// KeepAlive는 요청 이후 모델이 로드된 상태를 유지하는 시간을 제어합니다
// 0 = 요청 후 즉시 언로드
// -1 = 영구히 로딩 유지
// >0 = 지정된 초 동안 로드 상태 유지
Options.KeepAlive = -1;  // 영구적으로 로드 상태 유지

    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Hello!"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);
    Request->SendRequest();
}
```

##비전(이미지 분석)

Cllama는 Vision 기능을 지원하기 위해 다중 모달 모델(예: LLaVA)을 사용해야 하며 MMProject 모델 파일이 필요합니다.

> **주의**: Cllama Vision은 최대 1장의 이미지를 지원합니다(`FAIChatPlus_Constants::FCllama::MaxSendImageNum = 1`).

###파일에서 이미지 불러와 분석하기

```cpp
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithCllama()
{
// 파일에서 이미지 로드
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image: %s"), *ImagePath);
        return;
    }

// 플러그인에서 사용할 수 있는 Texture 객체 생성
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

// 옵션 구성
    FAIChatPlus_CllamaChatRequestOptions Options;

// LLaVA 모델에는 두 개의 파일이 필요합니다: 메인 모델과 MMProject 모델
    Options.ModelPath.FilePath = TEXT("D:/Models/llava-v1.6-mistral-7b.Q4_K_M.gguf");
    Options.MMProjectModelPath.FilePath = TEXT("D:/Models/mmproj-llava-v1.6-mistral-7b-f16.gguf");

    Options.bStream = true;
    Options.NumGpuLayers = 99;
Options.MMProjectUseGpu = true;  // MMProject 모델도 GPU 사용

// 이미지를 포함한 메시지 생성
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("What do you see in this image?");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
ImageMessage.Images.Add(ChatTexture);  // 이미지는 단 1장만 추가할 수 있습니다

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Cllama Vision: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###Texture2D에서 이미지 분석하기

```cpp
void UMyClass::AnalyzeTextureWithCllama(UTexture2D* InTexture)
{
    if (!InTexture)
    {
        UE_LOG(LogTemp, Error, TEXT("Invalid texture"));
        return;
    }

    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(InTexture);

    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llava-v1.6-mistral-7b.Q4_K_M.gguf");
    Options.MMProjectModelPath.FilePath = TEXT("D:/Models/mmproj-llava-v1.6-mistral-7b-f16.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;
    Options.MMProjectUseGpu = true;

    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("Describe this image in detail.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Description: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##고급 설정

###샘플링 파라미터 설정

```cpp
void UMyClass::ConfigureCllamaSampling()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;

// GPU 가속
옵션.NumGpuLayers = 99;  // 가능한 많은 레이어를 GPU에 올리기

// 샘플링 파라미터
Options.Temperature = 0.7f; // 온도
옵션.탑K = 40;           // Top-K 샘플링
Options.TopP = 0.95f;        // 뉴클리어스 샘플링
Options.MinP = 0.05f;        // Min-P 샘플링

// Mirostat 샘플링 (혼란도 제어용)  

// 后面的括号内容是为了说明该注释用途，翻译时保留专业术语的一致性和清晰性
    Options.Mirostat = 2;        // 0=비활성화, 1=Mirostat, 2=Mirostat 2.0
    Options.MirostatEta = 0.1f;
    Options.MirostatTau = 5.0f;

// 컨텍스트와 생성 제한
Options.NumCtx = 4096;       // 컨텍스트 윈도우 크기
Options.NumPredict = 256;    // 최대 생성 토큰 수 (-1 = 무제한)

    // 반복 패널티
Options.RepeatLastN = 64;    // 반복 검사할 마지막 토큰 개수
    Options.RepeatPenalty = 1.1f;

// 테일 부분 자유 샘플링
옵션.TfsZ = 1.0f;         // 1.0 = 비활성화

    // 시퀀스 중지
    Options.StopSequences.Add(TEXT("\n\n"));
    Options.StopSequences.Add(TEXT("User:"));

// 랜덤 시드 (재현 가능한 생성을 위해)
    Options.Seed = 42;

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a short poem."), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###사용자 정의 템플릿 사용하기

```cpp
void UMyClass::UseCustomTemplate()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/my_model.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;

// 사용자 정의 프롬프트 템플릿 (모델 내장 템플릿 덮어쓰기)
    Options.Template = TEXT("<|im_start|>system\n{{system}}<|im_end|>\n<|im_start|>user\n{{prompt}}<|im_end|>\n<|im_start|>assistant\n");

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System},
            {TEXT("Hello!"), EAIChatPlus_ChatRole::User}
        });

    Request->SendRequest();
}
```

##오류 처리

```cpp
void UMyClass::RobustCllamaRequest()
{
// 먼저 Cllama를 사용할 수 있는지 확인합니다
    if (!UAIChatPlus_Util::Cllama_IsValid())
    {
        UE_LOG(LogTemp, Error, TEXT("Cllama is not available"));
        return;
    }

    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->OnStartedListeners.AddLambda([]()
    {
        UE_LOG(LogTemp, Display, TEXT("Cllama request started, loading model..."));
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.HasError())
        {
            UE_LOG(LogTemp, Error, TEXT("Response error: %s"), *Response.Error.GetDescription());
            return;
        }

        UE_LOG(LogTemp, Display, TEXT("Success: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Tokens: %s"), *Response.Usage.GetDescription());

// 성능 지표
        UE_LOG(LogTemp, Display, TEXT("Total Duration: %lld ns"), Response.TotalDuration);
        UE_LOG(LogTemp, Display, TEXT("Load Duration: %lld ns"), Response.LoadDuration);
        UE_LOG(LogTemp, Display, TEXT("Prompt Eval Duration: %lld ns"), Response.PromptEvalDuration);
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
UAIChatPlus_CllamaChatRequest* CurrentCllamaRequest = nullptr;

void UMyClass::StartCllamaRequest()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;
Options.NumPredict = -1;  // 무한 생성

    CurrentCllamaRequest = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a very long story about adventures."), EAIChatPlus_ChatRole::User}});

    CurrentCllamaRequest->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Generating: %s"), *Message);
    });

    CurrentCllamaRequest->SendRequest();
}

void UMyClass::CancelCllamaRequest()
{
    if (CurrentCllamaRequest && CurrentCllamaRequest->IsActivated())
    {
        CurrentCllamaRequest->StopRequest();
        UE_LOG(LogTemp, Display, TEXT("Cllama request cancelled"));
    }
}
```

##완전한 대화 관리 예시

```cpp
// 멤버 변수
TArray<FAIChatPlus_ChatRequestMessage> CllamaConversation;
FAIChatPlus_CllamaChatRequestOptions CllamaOptions;

void UMyClass::InitializeCllamaChat()
{
    CllamaOptions.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    CllamaOptions.bStream = true;
    CllamaOptions.NumGpuLayers = 99;
CllamaOptions.KeepAlive = -1;  // 모델 로딩 유지

    // 대화 초기화
    CllamaConversation.Empty();
    CllamaConversation.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}

void UMyClass::SendCllamaUserMessage(const FString& UserMessage)
{
    CllamaConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(CllamaOptions, CllamaConversation);

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
// 생성되는 내용을 실시간으로 표시합니다
        UE_LOG(LogTemp, Display, TEXT("Generating: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);

// 어시스턴트의 답변을 대화 기록에 추가
        FString AssistantMessage = Response.GetMessage();
        CllamaConversation.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});

        OnCllamaResponse(AssistantMessage);
    });

    Request->SendRequest();
}

void UMyClass::OnCllamaResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Cllama: %s"), *Response);
}

void UMyClass::ClearCllamaConversation()
{
    CllamaConversation.Empty();
    CllamaConversation.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}
```

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 누락된 점도 지적하세요. 
