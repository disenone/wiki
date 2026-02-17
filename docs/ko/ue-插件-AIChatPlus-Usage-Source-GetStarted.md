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

#C++ 편 - 시작하기

##모듈 소개

플러그인은 다음과 같은 모듈로 구성되어 있습니다:

* **AIChatPlusCommon**: 런타임 모듈(Runtime), 다양한 AI API 인터페이스의 요청 전송 및 응답 내용 파싱을 담당합니다.
* **AIChatPlusEditor**: 에디터 모듈(Editor), 에디터 AI 채팅 도구 구현을 담당합니다.
* **AIChatPlusCllama**: 런타임 모듈(Runtime), llama.cpp의 인터페이스와 파라미터를 캡슐화하여 오프라인에서 대형 모델을 실행하는 기능을 구현합니다.
* **Thirdparty/LLAMACpp**: 런타임 서드파티 모듈 (Runtime), llama.cpp의 동적 라이브러리와 헤더 파일을 통합했습니다.

##핵심 개념

소스 코드를 사용하기 전에 몇 가지 핵심 클래스와 그들 간의 관계를 이해해야 합니다:

###요청 (요청)

`UAIChatPlus_ChatRequestBase`는 모든 채팅 요청의 기본 클래스입니다. 각 API 공급자에 해당하는 하위 클래스가 있습니다:

* `UAIChatPlus_OpenAIChatRequest` - OpenAI 채팅 요청
* `UAIChatPlus_AzureChatRequest` - Azure 채팅 요청
* `UAIChatPlus_ClaudeChatRequest` - Claude 채팅 요청
* `UAIChatPlus_GeminiChatRequest` - 제미니 채팅 요청
* `UAIChatPlus_OllamaChatRequest` - 올라마 채팅 요청
* `UAIChatPlus_CllamaChatRequest` - Cllama 오프라인 모델 요청
* `UAIChatPlus_CllamaServerChatRequest` - CllamaServer 로컬 서버 요청

Request 객체는 요청 매개변수를 구성하고, 요청을 전송하며, 콜백을 수신하는 역할을 담당합니다.

###핸들러(처리기)

`UAIChatPlus_ChatHandlerBase`은 요청 콜백을 통합적으로 관리하기 위한 선택적인 핸들러 클래스입니다.

Handler는 다음과 같은 위임을 제공합니다:

* `OnStarted` - 요청이 시작될 때 트리거됨
* `OnMessage` - 스트리밍 메시지를 수신할 때 트리거됩니다(스트리밍 출력).
* `OnUpdated` - 업데이트가 수신될 때 트리거됩니다.
* `OnFinished` - 요청이 완료될 때 발생합니다
* `OnFailed` - 요청이 실패할 때 트리거됨

**핸들러를 언제 사용할까요?**

* 여러 요청의 콜백 로직을 통합적으로 관리해야 할 때
* 블루프린트와 C++ 간에 콜백 로직을 공유해야 할 때
* `OnStartedListeners`와 같은 Request의 위임을 직접 사용하여 콜백 리스너를 구현할 수도 있습니다

###옵션

각 API Provider에는 해당 API의 매개변수를 구성하기 위한 Options 구조체가 있습니다:

* `FAIChatPlus_OpenAIChatRequestOptions` - OpenAI 옵션(ApiKey, Model, Temperature 등)
* `FAIChatPlus_ClaudeChatRequestOptions` - Claude 옵션
`FAIChatPlus_GeminiChatRequestOptions` - Gemini 옵션
* 잠시만요...

Options는 API 키, 엔드포인트 URL, 모델 이름, 생성 파라미터 등 API 연결에 필요한 모든 설정을 포함하고 있습니다.

###메시지

`FAIChatPlus_ChatRequestMessage`는 AI에 보내는 메시지 구조체로, 다음을 포함합니다:

* `콘텐츠` - 텍스트 내용
* `역할` - 메시지 역할(System/User/Assistant/Developer/Tool)
* `Images` - 이미지 배열(Vision 기능)
* `Audios` - 오디오 배열 (Audio 기능)
* `ToolCallUses` - 도구 호출 요청
* `ToolCallResults` - 도구 호출 결과

###응답 (응답)

각 API Provider마다 해당하는 ResponseBody 구조체가 있습니다:

* `FAIChatPlus_OpenAIChatResponseBody`
* `FAIChatPlus_ClaudeChatResponseBody`
* 잠깐만...

ResponseBody에는 AI가 반환한 메시지 텍스트, 토큰 사용량, 도구 호출, 오디오 출력 등 모든 정보가 포함되어 있습니다.

##기본 사용 절차 (5단계 모드)

AIChatPlus를 사용하여 요청을 보내는 기본적인 절차는 다음과 같습니다:

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"

void SendChatRequest()
{
// ===== 단계 1: 핸들러 생성(선택 사항) =====
// Handler는 콜백을 통합 관리하는 데 사용되며, Request의 대리자를 직접 사용할 수도 있습니다.
    TWeakObjectPtr<UAIChatPlus_ChatHandlerBase> Handler = UAIChatPlus_ChatHandlerBase::New();

// ===== 단계 2: 옵션 구성 =====
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
Options.bStream = true;  // 스트리밍 출력 활성화

// ===== 단계 3: 요청 생성 =====
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("Hello, who are you?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// ===== 4단계: 콜백 바인딩 =====
    // 방법 A: Handler 사용하기
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

// 방법 B: Request의 위임을 직접 사용하기 (Handler 불필요)
    // Request->OnMessageListeners.AddDynamic(this, &UMyClass::OnMessageReceived);
    // Request->OnFinishedListeners.AddDynamic(this, &UMyClass::OnRequestFinished);

// ===== 단계 5: 요청 보내기 =====
    Request->SendRequest();
}
```

##간략한 표기

미세한 콜백 제어가 필요하지 않다면 더 간결한 작성 방식을 사용할 수 있습니다:

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

// Request에 직접 Lambda 바인딩하기
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

##API Provider 열거형을 통해 요청 생성하기

구성에 따라 API Provider를 동적으로 선택해야 하는 경우, 팩토리 메서드를 사용할 수 있습니다:

```cpp
void CreateRequestByProvider(EAIChatPlus_ChatApiProvider Provider)
{
// 열거형에 따라 해당하는 Request 생성
    auto Request = UAIChatPlus_ChatRequestBase::CreateByApi(Provider);

// 실제 유형에 따라 Options 설정
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
// ... 다른 Provider
    }

// 메시지를 설정하고 전송합니다
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Hello!"), EAIChatPlus_ChatRole::User});
    Request->SetMessages(Messages);
    Request->SendRequest();
}
```

##콜백 설명

###주요 콜백 위임

| 위임 | 트리거 시점 | 매개변수 |
|------|----------|------|
| `OnStarted` | 요청 전송이 시작될 때 | 없음 |
| `OnMessage` | 스트리밍 메시지 수신 시(각 토큰마다) | `const FString& Message` - 누적된 메시지 내용 |
| `OnUpdated` | 응답 업데이트를 받을 때 | `const FAIChatPlus_ResponseBodyBase& Response` |
| `OnFinished` | 요청이 성공적으로 완료될 때 | `const FAIChatPlus_ResponseBodyBase& Response` |
| `OnFailed` | 요청이 실패했을 때 | `const FAIChatPlus_ResponseErrorBase& Error` |
| `OnMessageFinished` | 메시지 수신 완료 시 | `const FAIChatPlus_MessageFinishedPayload& Payload` |

###스트리밍 출력 vs 비스트리밍 출력

* **스트리밍 출력** (`bStream = true`): `OnMessage`가 여러 번 트리거되며, 매번 누적된 메시지 내용을 반환합니다
* **비스트리밍 출력** (`bStream = false`): `OnMessage`는 완료 시에만 한 번 트리거되며, 완성된 메시지를 반환합니다.

##다음 단계

더 자세한 사용법은 각 API 제공자의 전용 문서를 참고하세요:

* [OpenAI / Azure 사용](ue-插件-AIChatPlus-Usage-Source-OpenAI.md)
* [클로드 사용](ue-插件-AIChatPlus-Usage-Source-Claude.md)
* [제미니 사용](ue-插件-AIChatPlus-Usage-Source-Gemini.md)
* [Ollama 사용하기](ue-插件-AIChatPlus-Usage-Source-Ollama.md)
* [Cllama 오프라인 모델](ue-插件-AIChatPlus-Usage-Source-Cllama.md)
* [CllamaServer 로컬 서버](ue-插件-AIChatPlus-Usage-Source-CllamaServer.md)
* [유틸리티 클래스](ue-插件-AIChatPlus-Usage-Source-Utils.md)

--8<-- "footer_ko.md"

> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. 의견이 있으시면 [**피드백**](https://github.com/disenone/wiki_blog/issues/new)누락된 부분을 지적해 주세요. 
