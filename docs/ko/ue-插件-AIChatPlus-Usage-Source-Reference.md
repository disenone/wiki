---
layout: post
title: API Reference
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
- llama.cpp
description: API Reference
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - API Reference" />

#C++ 편 - API 참조 문서

이 문서는 AIChatPlus 플러그인의 C++ API 참조를 제공하며, 모든 공개 클래스, 구조체, 열거형 및 주요 메서드에 대한 설명을 포함합니다.

##목차

- [열거형(Enum) 타입](##枚举类型)
- [핵심 기본 클래스](##核心基类)
- [핸들러 클래스](##handler-类)
- [Request 클래스](##request-类)
- [도구류](##工具类)
- [JSON 클래스](##json-类)

---

##열거형

### EAIChatPlus_ChatApiProvider

AI 채팅 API 제공자 열거.

```cpp
enum class EAIChatPlus_ChatApiProvider : uint8
{
    OpenAI,         // OpenAI API
    Azure,          // Azure OpenAI API
    Claude,         // Anthropic Claude API
    Gemini,         // Google Gemini API
Ollama,         // Ollama 로컬 서비스
클라마,         // llama.cpp 직접 호출(더 이상 사용되지 않음)
CllamaServer    // llama.cpp 서버 모드
};
```

### EAIChatPlus_ImageApiProvider

이미지 생성 API 제공업체 열거.

```cpp
enum class EAIChatPlus_ImageApiProvider : uint8
{
    OpenAI,   // OpenAI DALL-E
    Azure     // Azure OpenAI DALL-E
};
```

### EAIChatPlus_ChatRole

메시지 역할 열거형.

```cpp
enum class EAIChatPlus_ChatRole : uint8
{
시스템,     // 시스템 명령(구형 모델)
사용자,       // 사용자 메시지
어시스턴트,   // AI 응답
개발자,  // 개발자 명령어(o1+ 모델)
도구        // 도구 호출 결과
};
```

### EAIChatPlus_ImageChatType

이미지 조작 유형 열거.

```cpp
enum class EAIChatPlus_ImageChatType : uint8
{
생성,  // 이미지 생성
편집,        // 이미지 편집
변형    // 이미지 변형
};
```

### EAIChatPlus_JsonValueType

JSON 값 타입 열거형.

```cpp
enum class EAIChatPlus_JsonValueType : uint8
{
없음,     // 무효
Null,     // 널값
문자열,   // 문자열
번호,   // 숫자
불린(Boolean),  // 불리언
배열,    // 어레이
오브젝트    // 객체
};
```

---

##핵심 기반 클래스

### UAIChatPlus_RequestBase

모든 요청의 기본 클래스(추상 클래스).

**주요 방법:**

| 방법      | 반환 유형  | 설명          |
|------|---------|------|
| `SendRequest()` | `bool` | 요청 전송 |
| `StopRequest()` | `void` | 요청 중지 |
| `Activate()` | `void` | 요청 객체 활성화 |
| `IsActivated()` | `bool` | 활성화 여부 확인 |
| `SetIsAutoDestroy(bool)` | `void` | 설정 완료 후 자동 소멸 |

**위임:**

| 위탁명 | 서명 | 설명 |
|--------|------|------|
| `OnStartedListeners` | `void()` | 요청 시작 |
| `OnMessageListeners` | `void(const FString&)` | 스트리밍 메시지 수신 |
| `OnFinishedListeners` | `void(const FAIChatPlus_PointerWrapper&)` | 요청 완료 |
| `OnFailedListeners` | `void(const FAIChatPlus_PointerWrapper&)` | 요청 실패 |

---

### UAIChatPlus_ChatRequestBase

채팅 요청 베이스 클래스, `UAIChatPlus_RequestBase`를 상속받습니다.

**정적 팩토리 메서드:**

```cpp
// Provider별로 요청 생성하기
static UAIChatPlus_ChatRequestBase* CreateByApi(EAIChatPlus_ChatApiProvider InApiProvider);
static UAIChatPlus_ChatRequestBase* CreateByApiInWorld(EAIChatPlus_ChatApiProvider InApiProvider, const UObject* InWorldContext);
```

**핵심 방법:**

| 방법 | 반환 유형 | 설명 |
|------|---------|------|
| `SetMessages(const TArray<FAIChatPlus_ChatRequestMessage>&)` | `void` | 메시지 목록 설정 |
| `GetFullUrl()` | `FString` | 전체 요청 URL 가져오기 |
| `GetModelText()` | `FString` | 모델 이름 가져오기 |
| `GetTokenUsageText()` | `FString` | 토큰 사용량 설명 가져오기 |
| `GetApiProvider()` | `EAIChatPlus_ChatApiProvider` | API 프로바이더 유형 가져오기 |

---

### UAIChatPlus_ImageRequestBase

이미지 요청 기본 클래스, `UAIChatPlus_RequestBase`를 상속받습니다.

**정적 팩토리 메소드:**

```cpp
static UAIChatPlus_ImageRequestBase* CreateByApi(EAIChatPlus_ImageApiProvider InApiProvider);
static UAIChatPlus_ImageRequestBase* CreateByApiInWorld(EAIChatPlus_ImageApiProvider InApiProvider, const UObject* InWorldContext);
```

**주요 방법:**

| 방법 | 반환 유형 | 설명 |
|------|---------|------|
| `SetPrompt(const FString&)` | `void` | 이미지 생성 프롬프트 설정 |
| `SetImages(const TArray<UAIChatPlus_Texture*>&)` | `void` | 입력 이미지 설정 (편집/변형) |
| `GetModelText()` | `FString` | 모델 이름 가져오기 |
| `GetStyleText()` | `FString` | 스타일 이름 가져오기 |
다음은 한국어로 번역된 내용입니다:

| `GetRevisedPrompt()` | `FString` | 수정된 프롬프트 가져오기 |
| `GetImageChatType()` | `FString` | 이미지 작업 유형 가져오기 |

---

### UAIChatPlus_ModelRequestBase

모델 목록 요청 기본 클래스, `UAIChatPlus_RequestBase`를 상속받습니다.

**정적 팩터리 메서드:**

```cpp
static UAIChatPlus_ModelRequestBase* CreateByApi(EAIChatPlus_ChatApiProvider InApiProvider);
static UAIChatPlus_ModelRequestBase* CreateByApiInWorld(EAIChatPlus_ChatApiProvider InApiProvider, const UObject* InWorldContext);
```

---

##핸들러 클래스

### UAIChatPlus_HandlerBase

모든 Handler의 기본 클래스입니다.

**핵심 방법:**

| 방법 | 반환 유형 | 설명 |
|------|---------|------|
| `SetIsAutoDestroy(bool)` | `void` | 자동 소멸 설정 |
| `AutoDestroy()` | `void` | 자동으로 파괴를 실행 |
| `Destroy()` | `void` | 즉시 파괴 |

---

### UAIChatPlus_ChatHandlerBase

채팅 요청 핸들러, `UAIChatPlus_HandlerBase`를 상속받음.

**정적 팩토리 메소드:**

```cpp
static UAIChatPlus_ChatHandlerBase* New();
```

**바인딩 방법:**

| 방법 | 설명 |
|------|------|
| `BindChatRequest(UAIChatPlus_ChatRequestBase*)` | 채팅 요청 바인딩 |
| `BindImageRequest(UAIChatPlus_ImageRequestBase*)` | 이미지 요청 바인딩 |
| `BindModelRequest(UAIChatPlus_ModelRequestBase*)` | 모델 요청 바인딩 |
| `ClearDelegates()` | 모든 델리게이트 바인딩을 제거합니다 |

**위탁:**

| 위임명 | 서명 | 설명 |
|--------|------|------|
| `OnStarted` | `void()` | 요청 시작 |
| `OnStopped` | `void()` | 정지 요청 |
| `OnMessage` | `void(const FString&)` | 스트리밍 메시지 |
| `OnMessageFinished` | `void(const FAIChatPlus_MessageFinishedPayload&)` | 메시지 완료 |
| `OnUpdated` | `void(const FAIChatPlus_PointerWrapper&)` | 업데이트 요청 |
| `OnFinished` | `void(const FAIChatPlus_PointerWrapper&)` | 요청 완료 |
| `OnFailed` | `void(const FAIChatPlus_PointerWrapper&)` | 요청 실패 |
| `OnImages` | `void(const TArray<UTexture2D*>&, bool)` | 이미지 생성 |
| `OnModels` | `void(const TArray<FString>&)` | 모델 목록 |

---

### UAIChatPlus_CllamaServerHandler

CllamaServer 전용 핸들러.

**정적 팩토리 메서드:**

```cpp
static UAIChatPlus_CllamaServerHandler* CreateHandler();
```

**위탁:**

| 위임명 | 서명 | 설명 |
|--------|------|------|
| `OnServerStarted` | `void(FGuid)` | 서버 시작됨 |
| `OnServerStopped` | `void(FGuid)` | 서버 중지 |
| `OnServerFailed` | `void(FGuid, const FString&)` | 서버 실패 |

---

##요청(Request) 클래스

모든 Provider의 Request 클래스는 동일한 팩토리 메소드 패턴을 따릅니다:

###일반적인 팩토리 메서드 패턴

```cpp
// OpenAI를 예로 들면, 다른 Provider도 유사합니다
static UAIChatPlus_OpenAIChatRequest* Create();
static UAIChatPlus_OpenAIChatRequest* CreateWithOptions(const FAIChatPlus_OpenAIChatRequestOptions& InOptions);
static UAIChatPlus_OpenAIChatRequest* CreateWithOptionsAndMessages(
    const FAIChatPlus_OpenAIChatRequestOptions& InOptions,
    const TArray<FAIChatPlus_ChatRequestMessage>& InMessages);
static UAIChatPlus_OpenAIChatRequest* CreateInWorld(const UObject* InWorldContext);
static UAIChatPlus_OpenAIChatRequest* CreateInWorldWithOptions(
    const UObject* InWorldContext,
    const FAIChatPlus_OpenAIChatRequestOptions& InOptions);
static UAIChatPlus_OpenAIChatRequest* CreateInWorldWithOptionsAndMessages(
    const UObject* InWorldContext,
    const FAIChatPlus_OpenAIChatRequestOptions& InOptions,
    const TArray<FAIChatPlus_ChatRequestMessage>& InMessages);
```

###일반 정적 메소드

모든 Request 클래스는 타입 변환을 위해 `CastWrapperToResponse` 메서드를 제공합니다:

```cpp
// PointerWrapper에서 응답 데이터 추출
static FAIChatPlus_XXXResponseBody& CastWrapperToResponse(const FAIChatPlus_PointerWrapper& InWrapper);
static FAIChatPlus_PointerWrapper CastResponseToWrapper(const FAIChatPlus_XXXResponseBody& InResponse);
```

---

### UAIChatPlus_OpenAIChatRequest

OpenAI 채팅 요청.

**헤더 파일:** `Common_OpenAI/AIChatPlus_OpenAIChatRequest.h`

**옵션 타입:** `FAIChatPlus_OpenAIChatRequestOptions`

**응답 유형:** `FAIChatPlus_OpenAIChatResponseBody`

---

### UAIChatPlus_AzureChatRequest

Azure OpenAI 채팅 요청.

**헤더 파일:** `Common_Azure/AIChatPlus_AzureChatRequest.h`

**옵션 유형:** `FAIChatPlus_AzureChatRequestOptions`

**응답 유형:** `FAIChatPlus_AzureChatResponseBody`

---

### UAIChatPlus_ClaudeChatRequest

클로드 채팅 요청.

**헤더 파일:** `Common_Claude/AIChatPlus_ClaudeChatRequest.h`

**옵션 유형:** `FAIChatPlus_ClaudeChatRequestOptions`

**응답 유형:** `FAIChatPlus_ClaudeChatResponseBody`

---

### UAIChatPlus_GeminiChatRequest

Gemini 채팅 요청.

**헤더 파일:** `Common_Gemini/AIChatPlus_GeminiChatRequest.h`

**옵션 유형:** `FAIChatPlus_GeminiChatRequestOptions`

**응답 유형:** `FAIChatPlus_GeminiChatResponseBody`

---

### UAIChatPlus_OllamaChatRequest

Ollama 채팅 요청.

**헤더 파일:** `Common_Ollama/AIChatPlus_OllamaChatRequest.h`

**옵션 유형:** `FAIChatPlus_OllamaChatRequestOptions`

**응답 유형:** `FAIChatPlus_OllamaChatResponseBody`

---

### UAIChatPlus_OllamaModelRequest

Ollama 모델 목록 요청.

**헤더 파일:** `Common_Ollama/AIChatPlus_OllamaModelRequest.h`

**옵션 유형:** `FAIChatPlus_OllamaModelRequestOptions`

**응답 유형:** `FAIChatPlus_OllamaModelResponseBody`

**특유의 방법:**

| 방법 | 반환 유형 | 설명 |
|------|---------|------|
| `GetModelNames()` | `TArray<FString>` | 모델 이름 목록 가져오기 |

---

###UAIChatPlus_CllamaChatRequest (더 이상 사용되지 않음)

Cllama 오프라인 채팅 요청 (더 이상 사용되지 않음, CllamaServer 사용을 권장합니다).

**헤더 파일:** `Common_Cllama/AIChatPlus_CllamaChatRequest.h`

**옵션 유형:** `FAIChatPlus_CllamaChatRequestOptions`

**응답 유형:** `FAIChatPlus_CllamaChatResponseBody`

---

### UAIChatPlus_CllamaServerChatRequest

CllamaServer 채팅 요청.

**헤더 파일:** `Common_CllamaServer/AIChatPlus_CllamaServerChatRequest.h`

**옵션 유형:** `FAIChatPlus_CllamaServerChatRequestOptions`

**응답 유형:** `FAIChatPlus_CllamaServerChatResponseBody`

---

### UAIChatPlus_OpenAIImageRequest

OpenAI 이미지 생성 요청.

**헤더 파일:** `Common_OpenAI/AIChatPlus_OpenAIImageRequest.h`

**옵션 타입:** `FAIChatPlus_OpenAIImageRequestOptions`

**응답 유형:** `FAIChatPlus_OpenAIImageResponseBody`

---

### UAIChatPlus_AzureImageRequest

Azure 이미지 생성 요청.

**헤더 파일:** `Common_Azure/AIChatPlus_AzureImageRequest.h`

**옵션 유형:** `FAIChatPlus_AzureImageRequestOptions`

**응답 유형:** `FAIChatPlus_AzureImageResponseBody`

---

### UAIChatPlus_CllamaServer

CllamaServer 서버 관리 클래스.

**헤더 파일:** `Common_CllamaServer/AIChatPlus_CllamaServer.h`

**정적 팩토리 메서드:**

```cpp
static UAIChatPlus_CllamaServer* CreateServer(
    const FAIChatPlus_CllamaServerParam& InParams,
    FGuid InServerID = FGuid());
static UAIChatPlus_CllamaServer* CreateServerInWorld(
    const UObject* InWorldContext,
    const FAIChatPlus_CllamaServerParam& InParams,
    FGuid InServerID = FGuid());
static UAIChatPlus_CllamaServer* CreateServerWithHandler(
    const FAIChatPlus_CllamaServerParam& InParams,
    UAIChatPlus_CllamaServerHandler* InHandler,
    FGuid InServerID = FGuid());
```

**인스턴스 메서드:**

| 메서드 | 반환 유형 | 설명 |
|------|---------|------|
| `Activate()` | `void` | 서버 시작 |
| `StopServer()` | `void` | 서버 중지 |
| `IsRunning()` | `bool` | 실행 중인지 확인 |
| `GetServerID()` | `FGuid` | 서버 ID 가져오기 |
| `GetHost()` | `FString` | 호스트 주소를 가져옵니다 |
| `GetAddress()` | `FString` | 전체 주소 가져오기 |
| `GetServerInfo(FAIChatPlus_CllamaServerInfo&)` | `bool` | 서버 정보 가져오기 |

**정적 관리 방법:**

| 방법 | 반환 유형 | 설명 |
|------|---------|------|
| `IsServerValid(const FGuid&)` | `bool` | 서버가 유효한지 확인합니다 |
| `IsServerRunning(const FGuid&)` | `bool` | 서버가 실행 중인지 확인 |
| `StopServerByID(const FGuid&)` | `void` | ID로 서버 중지 |
| `StopAllServers()` | `void` | 모든 서버 중지 |
| `GetServerByID(const FGuid&)` | `UAIChatPlus_CllamaServer*` | ID로 서버 가져오기 |
| `GetAllServerIDs()` | `TArray<FGuid>` | 서버의 모든 ID 가져오기 |

---

##유틸리티 클래스

### UAIChatPlus_Util

범용 유틸리티 클래스로, 다양한 정적 지원 메소드를 제공합니다.

**헤더 파일:** `Common/AIChatPlus_Util.h`

####로그 관련

| 방법 | 반환 유형 | 설명 |
|------|---------|------|
| `SetInternalLogVerbosity(EAIChatPlus_LogVerbosityType)` | `void` | 내부 로그 레벨 설정 |

####래퍼 변환

| 방법 | 반환 유형 | 설명 |
|------|---------|------|
| `CastWrapperToError(const FAIChatPlus_PointerWrapper&)` | `FAIChatPlus_ResponseErrorBase&` | 에러 정보 추출 |
| `CastWrapperToResponse(const FAIChatPlus_PointerWrapper&)` | `FAIChatPlus_ChatResponseBodyBase&` | 응답 데이터 추출 |
| `GetErrorWrapperDescription(const FAIChatPlus_PointerWrapper&)` | `FString` | 에러 설명 가져오기 |
| `GetResponseWrapperMessage(const FAIChatPlus_PointerWrapper&)` | `FString` | 응답 메시지 가져오기 |

####이미지 도구

| 방법 | 반환 유형 | 설명 |
|------|---------|------|
| `LoadImage(const FString&, bool)` | `UTexture2D*` | 파일에서 이미지 로드 |
| `SaveImage(UTexture2D*, const FString&)` | `bool` | 이미지를 파일로 저장 |
| `ImageToB64(UTexture2D*, int32)` | `FString` | 이미지를 Base64로 변환 |
| `CopyTexture2D(UTexture2D*, UObject*, FName, EObjectFlags)` | `UTexture2D*` | 텍스처 복사 |
`FitImageSize(const FVector2D&, const FVector2D&)` | `FVector2D` | 적절한 크기 계산하기 |
| `CopyTexture2DToClipboard(UTexture2D*)` | `void` | 클립보드로 복사하기 |
| `IsCanCopyTexture2DToClipboard()` | `bool` | 지원 여부 확인 |

####오디오 도구

| 방법 | 반환 유형 | 설명 |
|------|---------|------|
| `LoadSoundWav(const FString&)` | `USoundWave*` | 파일에서 오디오 로드 |
| `SaveSoundWav(USoundWave*, const FString&)` | `bool` | 오디오를 파일로 저장 |
| `SoundToB64(USoundWave*)` | `FString` | 오디오를 Base64로 변환 |
| `CopySoundWave(const USoundWave*, UObject*, FName)` | `USoundWave*` | 사운드 웨이브 복사 |
| `WavDataToSoundWave(const TArray<uint8>&, bool, bool)` | `USoundWave*` | WAV 데이터를 사운드웨이브로 변환 |
| `GetSoundWavePCMData(USoundWave*)` | `TArray<uint8>` | PCM 데이터 가져오기 |

####JSON 도구

| 방법 | 반환 유형 | 설명 |
|------|---------|------|
| `MergeJsonObjects(const FString&, const FString&)` | `FString` | JSON 문자열 합치기 |
| `LoadJsonString(const FString&)` | `TSharedPtr<FJsonObject>` | JSON 문자열 파싱 |
| `ToJsonString(const TSharedPtr<FJsonObject>&)` | `FString` | JSON 문자열로 변환 |

####Cllama 도구

방법 | 반환 유형 | 설명 |
|------|---------|------|
| `Cllama_IsValid()` | `bool` | Cllama가 사용 가능한지 확인 |
| `Cllama_IsSupportGpu()` | `bool` | GPU 지원 여부 확인 |
| `Cllama_GetSupportBackends()` | `TArray<FString>` | 지원되는 백엔드 목록 가져오기 |
| `Cllama_PrepareModelPathFromPak(const FString&)` | `FString` | 팩에서 모델 경로 준비하기 |

####모델 정보

| 방법 | 반환 유형 | 설명 |
|------|---------|------|
| `GetOpenAIChatDefaultModels()` | `const TArray<FName>&` | OpenAI 기본 모델 목록 |
| `GetOpenAIChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | OpenAI 모델 정보 가져오기 |
| `GetClaudeChatDefaultModels()` | `const TArray<FName>&` | Claude 기본 모델 목록 |
| `GetClaudeChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | 클로드 모델 정보 가져오기 |
| `GetGeminiChatDefaultModels()` | `const TArray<FName>&` | 제미니 기본 모델 목록 |
| `GetGeminiChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | Gemini 모델 정보 가져오기 |

---

### UAIChatPlus_Texture

이미지 래핑 클래스, 비동기 로딩 및 Base64 변환을 지원합니다.

**헤더 파일:** `Common/AIChatPlus_Texture.h`

**정적 팩토리 메서드:**

```cpp
static UAIChatPlus_Texture* New(UTexture2D* InTexture = nullptr, const FString& InSourcePath = "");
static UAIChatPlus_Texture* CreateInBlueprint(UObject* WorldContextObject, UTexture2D* InTexture);
```

**방법:**

| 메서드 | 반환 유형 | 설명 |
|------|---------|------|
| `LoadFromFile(const FString&)` | `bool` | 파일로부터 로드 (동기 방식) |
| `LoadFromFileAsync(const FString&, Callback)` | `FLoadingTaskType*` | 파일에서 비동기적으로 불러오기 |
| `LoadFromAsset(UObject*, const FString&)` | `bool` | 에셋에서 로드(동기) |
| `LoadFromAssetAsync(UObject*, Callback, const FString&)` | `FLoadingTaskType*` | 에셋에서 로딩 (비동기) |
| `ToB64()` | `const FString&` | Base64로 변환 (동기적) |
| `ToB64Async(Callback)` | `FLoadingTaskType*` | Base64로 변환 (비동기) |
| `GetBrush(bool)` | `const FSlateBrush*` | Slate 브러시 가져오기 |
| `GetBrushCopy(bool)` | `FSlateBrush` | 브러시 사본 얻기 |
| `GetSize()` | `FIntVector2` | 크기 가져오기 |
| `GetSize2D()` | `FVector2D` | 크기 가져오기 (부동 소수점) |
| `IsValid()` | `bool` | 유효한지 확인 |
| `IsLoading()` | `bool` | 로딩 중인지 확인 |
| `Reset()` | `void` | 초기화 |
| `WaitLoadingComplete()` | `void` | 로딩 완료 대기 |

---

### UAIChatPlus_Sound

오디오 래핑 클래스, 비동기 로딩과 Base64 변환을 지원합니다.

**헤더 파일:** `Common/AIChatPlus_Sound.h`

**정적 팩토리 메서드:**

```cpp
static UAIChatPlus_Sound* New(USoundWave* InSound = nullptr, const FString& InSourcePath = "");
static UAIChatPlus_Sound* CreateInBlueprint(UObject* WorldContextObject, USoundWave* InSound);
```

**방법:**

| 방법 | 반환 유형 | 설명 |
|------|---------|------|
| `LoadFromFile(const FString&)` | `bool` | 파일에서 로드 (동기 방식) |
| `LoadFromFileAsync(const FString&, Callback)` | `FLoadingTaskType*` | 파일에서 불러오기(비동기) |
| `LoadFromAsset(UObject*, const FString&)` | `bool` | 에셋에서 로드 (동기화) |
| `LoadFromAssetAsync(UObject*, Callback, const FString&)` | `FLoadingTaskType*` | 에셋에서 로드 (비동기) |
| `ToB64()` | `const FString&` | Base64로 변환 (동기화) |
| `ToB64Async(Callback)` | `FLoadingTaskType*` | Base64로 변환 (비동기) |
| `IsValid()` | `bool` | 유효한지 확인 |
| `IsLoading()` | `bool` | 로딩 중인지 확인합니다 |
| `Reset()` | `void` | 초기화 |
| `WaitLoadingComplete()` | `void` | 로딩 완료 대기 |
| `PlayInEditor()` | `void` | 에디터에서 재생 |

---

##JSON 클래스

### UAIChatPlus_JsonObject

JSON 객체 래퍼 클래스.

**헤더 파일:** `Common/Json/AIChatPlus_JsonObject.h`

**정적 팩토리 메소드:**

```cpp
static UAIChatPlus_JsonObject* Create();
static UAIChatPlus_JsonObject* Parse(const FString& JsonString, bool& bSuccess, FString& ErrorMessage);
static UAIChatPlus_JsonObject* FromStruct(const int32& Struct);  // CustomThunk
```

**필드 설정 메서드(체이닝 호출 지원):**

| 방법 | 반환 유형 | 설명 |
|------|---------|------|
| `SetStringField(const FString&, const FString&)` | `UAIChatPlus_JsonObject*` | 문자열 필드 설정 |
| `SetNumberField(const FString&, float)` | `UAIChatPlus_JsonObject*` | 숫자 필드 설정 |
| `SetIntegerField(const FString&, int32)` | `UAIChatPlus_JsonObject*` | 정수 필드 설정 |
| `SetBooleanField(const FString&, bool)` | `UAIChatPlus_JsonObject*` | 불리언 필드 설정 |
| `SetObjectField(const FString&, UAIChatPlus_JsonObject*)` | `UAIChatPlus_JsonObject*` | 오브젝트 필드 설정 |
| `SetArrayField(const FString&, UAIChatPlus_JsonArray*)` | `UAIChatPlus_JsonObject*` | 배열 필드 설정 |
| `SetNullField(const FString&)` | `UAIChatPlus_JsonObject*` | 빈 필드 설정 |

**필드 가져오기 방법:**

| 방법 | 반환 유형 | 설명 |
|------|---------|------|
| `GetStringField(const FString&, const FString&, bool&)` | `FString` | 문자열 가져오기 |
| `GetNumberField(const FString&, float, bool&)` | `float` | 숫자 가져오기 |
| `GetIntegerField(const FString&, int32, bool&)` | `int32` | 정수 가져오기 |
| `GetBooleanField(const FString&, bool, bool&)` | `bool` | 불리언 값 가져오기 |
| `GetObjectField(const FString&, bool&)` | `UAIChatPlus_JsonObject*` | 객체 가져오기 |
| `GetArrayField(const FString&, bool&)` | `UAIChatPlus_JsonArray*` | 배열 가져오기 |

**기타 방법:**

| 방식 | 반환 유형 | 설명 |
|------|---------|------|
| `HasField(const FString&)` | `bool` | 필드 존재 여부 확인 |
| `GetFieldType(const FString&)` | `EAIChatPlus_JsonValueType` | 필드 타입 가져오기 |
| `RemoveField(const FString&)` | `UAIChatPlus_JsonObject*` | 필드 제거 |
| `Clear()` | `UAIChatPlus_JsonObject*` | 모든 필드 비우기 |
| `ToString(bool)` | `FString` | 문자열로 변환 |
| `ToStruct(int32&)` | `bool` | 구조체로 변환 |
| `Merge(UAIChatPlus_JsonObject*, bool)` | `UAIChatPlus_JsonObject*` | 객체 병합 |
| `Duplicate()` | `UAIChatPlus_JsonObject*` | 객체 복사하기 |
| `IsValid()` | `bool` | 유효성 검사 |

**경로 조회 방법:**

| 방법 | 반환 유형 | 설명 |
|------|---------|------|
| `SetStringByPath(const FString&, const FString&, const FAIChatPlus_JsonPathOptions&)` | `UAIChatPlus_JsonObject*` | 경로로 문자열 설정 |
| `GetStringByPath(const FString&, const FString&, FAIChatPlus_JsonQueryResult&)` | `FString` | 경로로 문자열 가져오기 |

---

### UAIChatPlus_JsonArray

JSON 배열 래퍼 클래스.

**헤더 파일:** `Common/Json/AIChatPlus_JsonArray.h`

**정적 팩토리 메소드:**

```cpp
static UAIChatPlus_JsonArray* Create();
static UAIChatPlus_JsonArray* Parse(const FString& JsonString, bool& bSuccess, FString& ErrorMessage);
static UAIChatPlus_JsonArray* FromStringArray(const TArray<FString>& Values);
static UAIChatPlus_JsonArray* FromIntegerArray(const TArray<int32>& Values);
```

**요소 추가 방법 (체이닝 호출 지원):**

| 방법 | 반환 형식 | 설명 |
|------|---------|------|
| `AddString(const FString&)` | `UAIChatPlus_JsonArray*` | 문자열 추가 |
| `AddNumber(float)` | `UAIChatPlus_JsonArray*` | 숫자 추가 |
| `AddInteger(int32)` | `UAIChatPlus_JsonArray*` | 정수 추가 |
| `AddBoolean(bool)` | `UAIChatPlus_JsonArray*` | 불리언 값 추가 |
| `AddObject(UAIChatPlus_JsonObject*)` | `UAIChatPlus_JsonArray*` | 객체 추가 |
| `AddArray(UAIChatPlus_JsonArray*)` | `UAIChatPlus_JsonArray*` | 배열 추가 |
| `AddNull()` | `UAIChatPlus_JsonArray*` | 빈 값 추가 |

**요소 가져오는 방법:**

| 방법 | 반환 유형 | 설명 |
|-----|---------|------|
|------|---------|------|
| `GetString(int32, const FString&, bool&)` | `FString` | 문자열 가져오기 |
| `GetNumber(int32, float, bool&)` | `float` | 숫자 가져오기 |
| `GetInteger(int32, int32, bool&)` | `int32` | 정수 가져오기 |
| `GetBoolean(int32, bool, bool&)` | `bool` | 부울 값 가져오기 |
| `GetObject(int32, bool&)` | `UAIChatPlus_JsonObject*` | 객체 가져오기 |
| `GetArray(int32, bool&)` | `UAIChatPlus_JsonArray*` | 배열 가져오기 |

**다른 방법:**

| 방법 | 반환 유형 | 설명 |
|------|---------|------|
| `Length()` | `int32` | 길이 조회 |
| `GetElementType(int32)` | `EAIChatPlus_JsonValueType` | 요소 타입 가져오기 |
| `SetString(int32, const FString&, bool&)` | `UAIChatPlus_JsonArray*` | 문자열 설정 |
| `SetObject(int32, UAIChatPlus_JsonObject*, bool&)` | `UAIChatPlus_JsonArray*` | 객체 설정 |
| `RemoveAt(int32, bool&)` | `UAIChatPlus_JsonArray*` | 요소 제거 |
| `Clear()` | `UAIChatPlus_JsonArray*` | 배열 비우기 |
| `ToString(bool)` | `FString` | 문자열로 변환 |
| `Duplicate()` | `UAIChatPlus_JsonArray*` | 배열 복사 |
| `IsValid()` | `bool` | 유효성 확인 |

---

### UAIChatPlus_JsonLibrary

JSON 정적 유틸리티 라이브러리.

**헤더 파일:** `Common/Json/AIChatPlus_JsonLibrary.h`

**생성 방법:**

| 방법 | 반환 유형 | 설명 |
|------|---------|------|
| `MakeJsonObjectWithStringField(const FString&, const FString&)` | `UAIChatPlus_JsonObject*` | 단일 필드 객체 생성 |
| `MakeJsonObjectFromStringMap(const TMap<FString, FString>&)` | `UAIChatPlus_JsonObject*` | Map에서 객체 생성 |

**검증 방법:**

| 방법 | 반환 타입 | 설명 |
|------|---------|------|
| `ValidateJsonString(const FString&, FString&)` | `bool` | JSON 문자열 유효성 검사 |
다음은 번역된 텍스트입니다:

| `IsJsonObject(const FString&)` | `bool` | 객체인지 확인 |
| `IsJsonArray(const FString&)` | `bool` | 배열인지 확인 |

**포맷 방법:**

| 방식 | 반환 유형 | 설명 |
|------|---------|------|
| `PrettifyJson(const FString&)` | `FString` | JSON 예쁘게 출력하기 |
| `MinifyJson(const FString&)` | `FString` | JSON 압축 |

**구조체 변환(CustomThunk):**

| 메소드 | 반환 유형 | 설명 |
|------|---------|------|
| `JsonStringToStruct(const FString&, int32&)` | `bool` | JSON을 구조체로 변환 |
| `StructToJsonString(const int32&, bool)` | `FString` | 구조체를 JSON으로 변환 |

**파일 작업:**

| 방법 | 반환 유형 | 설명 |
|------|---------|------|
| `LoadJsonObjectFromFile(const FString&, bool&, FString&)` | `UAIChatPlus_JsonObject*` | 파일에서 객체 불러오기 |
| `SaveJsonObjectToFile(UAIChatPlus_JsonObject*, const FString&, bool, FString&)` | `bool` | 객체를 파일에 저장 |
| `LoadJsonArrayFromFile(const FString&, bool&, FString&)` | `UAIChatPlus_JsonArray*` | 파일에서 배열 로드하기 |
| `SaveJsonArrayToFile(UAIChatPlus_JsonArray*, const FString&, bool, FString&)` | `bool` | 배열을 파일에 저장 |

**비교 방법:**

| 메소드 | 반환 형식 | 설명 |
|------|---------|------|
| `EqualsJsonObject(UAIChatPlus_JsonObject*, UAIChatPlus_JsonObject*)` | `bool` | 객체 비교 |
| `EqualsJsonArray(UAIChatPlus_JsonArray*, UAIChatPlus_JsonArray*)` | `bool` | 배열 비교 |

**경로 조회:**

| 메서드 | 반환 유형 | 설명 |
|------|---------|------|
| `QueryStringByPath(UAIChatPlus_JsonObject*, const FString&, const FString&, FAIChatPlus_JsonQueryResult&)` | `FString` | 경로로 문자열 조회하기 |
| `QueryObjectByPath(UAIChatPlus_JsonObject*, const FString&, FAIChatPlus_JsonQueryResult&)` | `UAIChatPlus_JsonObject*` | 경로별 객체 조회 |
| `QueryArrayByPath(UAIChatPlus_JsonObject*, const FString&, FAIChatPlus_JsonQueryResult&)` | `UAIChatPlus_JsonArray*` | 경로를 따라 배열 조회하기 |

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT로 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)누락된 부분을 지적합니다. 
