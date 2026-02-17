---
layout: post
title: Utils
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
- Json
- Image
- Sound
description: Utils
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Utils" />

#C++ 편 - Utils

이 문서는 AIChatPlus에서 제공하는 도구 클래스에 대해 설명하며, JSON 조작, 이미지 처리 및 오디오 처리 등의 기능을 포함합니다.

##준비 작업

프로젝트의 `.Build.cs` 파일에 모듈 의존성을 추가하세요:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

필요한 헤더 파일 포함하기:

```cpp
#include "Common/AIChatPlus_Util.h"
#include "Common/Json/AIChatPlus_JsonObject.h"
#include "Common/Json/AIChatPlus_JsonArray.h"
```

##JSON 조작

AIChatPlus는 Blueprint에 친숙한 JSON 조작 클래스를 제공하며, 체이닝 호출과 타입 안전 조작을 지원합니다.

###UAIChatPlus_JsonObject - JSON 객체

####생성 및 해석

```cpp
#include "Common/Json/AIChatPlus_JsonObject.h"

void UMyClass::JsonObjectBasics()
{
// 빈 JSON 객체 생성
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Create();

// 문자열에서 파싱
    FString JsonString = TEXT(R"({"name": "John", "age": 30, "active": true})");
    bool bSuccess;
    FString ErrorMessage;
    UAIChatPlus_JsonObject* ParsedObj = UAIChatPlus_JsonObject::Parse(JsonString, bSuccess, ErrorMessage);

    if (bSuccess)
    {
        UE_LOG(LogTemp, Display, TEXT("Parsed successfully"));
    }
    else
    {
        UE_LOG(LogTemp, Error, TEXT("Parse error: %s"), *ErrorMessage);
    }
}
```

####필드 설정(체이닝 호출)

```cpp
void UMyClass::SetJsonFields()
{
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Create();

// 체이닝 방식으로 필드 설정
    JsonObj->SetStringField(TEXT("name"), TEXT("John"))
           ->SetIntegerField(TEXT("age"), 30)
           ->SetBooleanField(TEXT("active"), true)
           ->SetNumberField(TEXT("score"), 95.5f)
           ->SetNullField(TEXT("extra"));

// 중첩 객체 설정하기
    UAIChatPlus_JsonObject* AddressObj = UAIChatPlus_JsonObject::Create();
    AddressObj->SetStringField(TEXT("city"), TEXT("Tokyo"))
              ->SetStringField(TEXT("country"), TEXT("Japan"));

    JsonObj->SetObjectField(TEXT("address"), AddressObj);

// 출력
FString Result = JsonObj->ToString(true);  // true = 포맷팅된 출력
    UE_LOG(LogTemp, Display, TEXT("%s"), *Result);
}
```

####필드 가져오기

```cpp
void UMyClass::GetJsonFields()
{
    FString JsonString = TEXT(R"({"name": "John", "age": 30, "scores": [85, 90, 95]})");
    bool bParseSuccess;
    FString ErrorMessage;
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Parse(JsonString, bParseSuccess, ErrorMessage);

    if (!bParseSuccess) return;

    bool bSuccess;

// 문자열 필드 가져오기
    FString Name = JsonObj->GetStringField(TEXT("name"), TEXT("Unknown"), bSuccess);
    if (bSuccess)
    {
        UE_LOG(LogTemp, Display, TEXT("Name: %s"), *Name);
    }

// 정수 필드 가져오기
    int32 Age = JsonObj->GetIntegerField(TEXT("age"), 0, bSuccess);

// 불리언 필드 가져오기
    bool bActive = JsonObj->GetBooleanField(TEXT("active"), false, bSuccess);

// 배열 필드 가져오기
    UAIChatPlus_JsonArray* Scores = JsonObj->GetArrayField(TEXT("scores"), bSuccess);
    if (bSuccess && Scores)
    {
        for (int32 i = 0; i < Scores->Length(); ++i)
        {
            int32 Score = Scores->GetInteger(i, 0, bSuccess);
            UE_LOG(LogTemp, Display, TEXT("Score[%d]: %d"), i, Score);
        }
    }

// 중첩 객체 필드 가져오기
    UAIChatPlus_JsonObject* AddressObj = JsonObj->GetObjectField(TEXT("address"), bSuccess);
    if (bSuccess && AddressObj)
    {
        FString City = AddressObj->GetStringField(TEXT("city"), TEXT(""), bSuccess);
    }
}
```

####필드 검사 및 관리

```cpp
void UMyClass::ManageJsonFields()
{
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Create();
    JsonObj->SetStringField(TEXT("name"), TEXT("John"))
           ->SetIntegerField(TEXT("age"), 30);

// 필드 존재 여부 확인
    if (JsonObj->HasField(TEXT("name")))
    {
        UE_LOG(LogTemp, Display, TEXT("Field 'name' exists"));
    }

// 필드 타입 가져오기
    EAIChatPlus_JsonValueType FieldType = JsonObj->GetFieldType(TEXT("age"));
    // FieldType == EAIChatPlus_JsonValueType::Number

// 모든 필드명 가져오기
    TArray<FString> FieldNames = JsonObj->GetFieldNames();
    for (const FString& Name : FieldNames)
    {
        UE_LOG(LogTemp, Display, TEXT("Field: %s"), *Name);
    }

    // 필드 삭제
    JsonObj->RemoveField(TEXT("age"));

// 모든 필드 비우기
    JsonObj->Clear();
}
```

####경로 조회(중첩 접근)

```cpp
void UMyClass::PathQuery()
{
    FString JsonString = TEXT(R"({
        "player": {
            "inventory": {
                "gold": 1000,
                "items": ["sword", "shield"]
            }
        }
    })");

    bool bParseSuccess;
    FString ErrorMessage;
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Parse(JsonString, bParseSuccess, ErrorMessage);

// 경로를 통해 값 가져오기
    FAIChatPlus_JsonQueryResult Result;
    FString Gold = JsonObj->GetStringByPath(TEXT("player.inventory.gold"), TEXT("0"), Result);
    // Gold = "1000"

    // 경로로 값 설정하기
    FAIChatPlus_JsonPathOptions PathOptions;
    JsonObj->SetStringByPath(TEXT("player.inventory.gold"), TEXT("2000"), PathOptions);
}
```

####병합 및 복사

```cpp
void UMyClass::MergeAndDuplicate()
{
    UAIChatPlus_JsonObject* Obj1 = UAIChatPlus_JsonObject::Create();
    Obj1->SetStringField(TEXT("name"), TEXT("John"));

    UAIChatPlus_JsonObject* Obj2 = UAIChatPlus_JsonObject::Create();
    Obj2->SetIntegerField(TEXT("age"), 30)
->SetStringField(TEXT("name"), TEXT("Jane"));  // name 덮어쓰기

    // 병합 (bOverwrite = true일 때 기존 필드를 덮어씁니다)
    Obj1->Merge(Obj2, true);
// Obj1은 현재 {"name": "Jane", "age": 30}을 포함합니다

// 깊은 복사
    UAIChatPlus_JsonObject* Copy = Obj1->Duplicate();
}
```

####UStruct와 상호 변환

```cpp
USTRUCT(BlueprintType)
struct FMyData
{
    GENERATED_BODY()

    UPROPERTY()
    FString Name;

    UPROPERTY()
    int32 Age;
};

void UMyClass::StructConversion()
{
// UStruct를 JsonObject로 변환
    FMyData Data;
    Data.Name = TEXT("John");
    Data.Age = 30;

    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::FromStruct(Data);

// JsonObject에서 UStruct로 변환
    FMyData OutData;
    bool bSuccess = JsonObj->ToStruct(OutData);

    if (bSuccess)
    {
        UE_LOG(LogTemp, Display, TEXT("Name: %s, Age: %d"), *OutData.Name, OutData.Age);
    }
}
```

###UAIChatPlus_JsonArray - JSON 배열

####생성과 조작

```cpp
#include "Common/Json/AIChatPlus_JsonArray.h"

void UMyClass::JsonArrayBasics()
{
// 빈 배열 생성
    UAIChatPlus_JsonArray* JsonArray = UAIChatPlus_JsonArray::Create();

// 요소 추가 (체이닝 호출)
    JsonArray->AddString(TEXT("apple"))
             ->AddString(TEXT("banana"))
             ->AddInteger(42)
             ->AddBoolean(true)
             ->AddNull();

// 객체 요소 추가
    UAIChatPlus_JsonObject* ItemObj = UAIChatPlus_JsonObject::Create();
    ItemObj->SetStringField(TEXT("name"), TEXT("sword"));
    JsonArray->AddObject(ItemObj);

// 중첩 배열 추가
    UAIChatPlus_JsonArray* NestedArray = UAIChatPlus_JsonArray::Create();
    NestedArray->AddInteger(1)->AddInteger(2)->AddInteger(3);
    JsonArray->AddArray(NestedArray);

// 출력
    FString Result = JsonArray->ToString(true);
    UE_LOG(LogTemp, Display, TEXT("%s"), *Result);
}
```

####요소 가져오기

```cpp
void UMyClass::GetArrayElements()
{
    FString JsonString = TEXT(R"(["apple", "banana", 42, true, {"name": "item"}])");
    bool bParseSuccess;
    FString ErrorMessage;
    UAIChatPlus_JsonArray* JsonArray = UAIChatPlus_JsonArray::Parse(JsonString, bParseSuccess, ErrorMessage);

    if (!bParseSuccess) return;

    bool bSuccess;

// 문자열 요소 가져오기
    FString Fruit = JsonArray->GetString(0, TEXT(""), bSuccess);  // "apple"

// 정수 요소 가져오기
    int32 Number = JsonArray->GetInteger(2, 0, bSuccess);  // 42

    // 불리언 요소 가져오기
    bool bValue = JsonArray->GetBoolean(3, false, bSuccess);  // true

    // 객체 요소 가져오기
    UAIChatPlus_JsonObject* Obj = JsonArray->GetObject(4, bSuccess);
    if (bSuccess && Obj)
    {
        FString Name = Obj->GetStringField(TEXT("name"), TEXT(""), bSuccess);
    }

// 배열을 순회하다
    for (int32 i = 0; i < JsonArray->Length(); ++i)
    {
        EAIChatPlus_JsonValueType Type = JsonArray->GetElementType(i);
        UE_LOG(LogTemp, Display, TEXT("Element[%d] type: %d"), i, static_cast<int32>(Type));
    }
}
```

####배열 조작

```cpp
void UMyClass::ArrayOperations()
{
    UAIChatPlus_JsonArray* JsonArray = UAIChatPlus_JsonArray::Create();
    JsonArray->AddString(TEXT("a"))
             ->AddString(TEXT("b"))
             ->AddString(TEXT("c"));

// 길이 가져오기
    int32 Len = JsonArray->Length();  // 3

// 인덱스가 유효한지 확인합니다
    bool bValid = JsonArray->IsValidIndex(1);  // true

// 요소 설정
    bool bSuccess;
    JsonArray->SetString(1, TEXT("B"), bSuccess);

// 요소 삭제
    JsonArray->RemoveAt(0, bSuccess);

// 배열 비우기
    JsonArray->Clear();

// 깊은 복사
    UAIChatPlus_JsonArray* Copy = JsonArray->Duplicate();
}
```

####일괄 변환

```cpp
void UMyClass::BatchConversion()
{
// 문자열 배열로부터 생성
    TArray<FString> StringArray = {TEXT("a"), TEXT("b"), TEXT("c")};
    UAIChatPlus_JsonArray* JsonArray = UAIChatPlus_JsonArray::FromStringArray(StringArray);

// 문자열 배열로 변환
    bool bSuccess;
    TArray<FString> OutArray = JsonArray->ToStringArray(bSuccess);

// 정수 배열로부터 생성
    TArray<int32> IntArray = {1, 2, 3, 4, 5};
    UAIChatPlus_JsonArray* IntJsonArray = UAIChatPlus_JsonArray::FromIntegerArray(IntArray);

// 정수 배열로 변환
    TArray<int32> OutIntArray = IntJsonArray->ToIntegerArray(bSuccess);
}
```

###UAIChatPlus_Util - JSON 헬퍼 함수

```cpp
void UMyClass::JsonUtilFunctions()
{
// 두 JSON 문자열 병합
    FString Json1 = TEXT(R"({"name": "John"})");
    FString Json2 = TEXT(R"({"age": 30, "name": "Jane"})");
    FString Merged = UAIChatPlus_Util::MergeJsonObjects(Json1, Json2);
    // Merged = {"name": "Jane", "age": 30}

// JSON 문자열을 객체로 로드
    TSharedPtr<FJsonObject> JsonObj = UAIChatPlus_Util::LoadJsonString(Json1);

// 객체를 문자열로 변환
    FString JsonString = UAIChatPlus_Util::ToJsonString(JsonObj);
}
```

##이미지 도구

###이미지 불러오기 및 저장하기

```cpp
#include "Common/AIChatPlus_Util.h"

void UMyClass::ImageLoadSave()
{
// 파일에서 이미지 로드하기
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath, true);  // true = 컴파일 완료

    if (Texture)
    {
        UE_LOG(LogTemp, Display, TEXT("Image loaded: %dx%d"),
            Texture->GetSizeX(), Texture->GetSizeY());
    }

    // 이미지를 파일로 저장
    FString SavePath = FPaths::ProjectSavedDir() / TEXT("output.png");
    bool bSaved = UAIChatPlus_Util::SaveImage(Texture, SavePath);

    if (bSaved)
    {
        UE_LOG(LogTemp, Display, TEXT("Image saved to: %s"), *SavePath);
    }
}
```

###이미지를 Base64로 변환

```cpp
void UMyClass::ImageToBase64()
{
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(TEXT("D:/image.png"));

// Base64 문자열로 변환
// 인퀄리티: 0 = PNG, 1-100 = JPEG 품질
FString B64String = UAIChatPlus_Util::ImageToB64(Texture, 0);  // PNG 포맷

    UE_LOG(LogTemp, Display, TEXT("Base64 length: %d"), B64String.Len());
}
```

###사진 복사하기

```cpp
void UMyClass::CopyTexture()
{
    UTexture2D* Original = UAIChatPlus_Util::LoadImage(TEXT("D:/image.png"));

// 텍스처 복사
    UTexture2D* Copy = UAIChatPlus_Util::CopyTexture2D(
        Original,
nullptr,        // Outer (nullptr = GetTransientPackage())
이름 없음,      // 이름
RF_NoFlags      // 플래그
    );

// 블루프린트 버전 (기본 플래그 포함)
    UTexture2D* BPCopy = UAIChatPlus_Util::CopyTexture2DInBlueprint(Original);
}
```

###URL에서 이미지 가져오기

```cpp
void UMyClass::GetImageFromUrl()
{
    FString ImageUrl = TEXT("https://example.com/image.png");

    UAIChatPlus_Util::GetImageFromUrl(ImageUrl,
        UAIChatPlus_Util::OnImageCreated::CreateLambda([](UTexture2D* Texture, const FString& Error)
        {
            if (Texture)
            {
                UE_LOG(LogTemp, Display, TEXT("Image downloaded: %dx%d"),
                    Texture->GetSizeX(), Texture->GetSizeY());
            }
            else
            {
                UE_LOG(LogTemp, Error, TEXT("Download failed: %s"), *Error);
            }
        }));
}
```

###Base64에서 이미지 가져오기

```cpp
void UMyClass::GetImageFromBase64()
{
FString B64String = TEXT("iVBORw0KGgoAAAANSUhEUg...");  // Base64 데이터

    UAIChatPlus_Util::GetImageFromB64(B64String,
        UAIChatPlus_Util::OnImageCreated::CreateLambda([](UTexture2D* Texture, const FString& Error)
        {
            if (Texture)
            {
                UE_LOG(LogTemp, Display, TEXT("Image decoded successfully"));
            }
            else
            {
                UE_LOG(LogTemp, Error, TEXT("Decode failed: %s"), *Error);
            }
        }));
}
```

###이미지를 클립보드에 복사

```cpp
void UMyClass::CopyToClipboard()
{
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(TEXT("D:/image.png"));

// 지원 여부 확인
    if (UAIChatPlus_Util::IsCanCopyTexture2DToClipboard())
    {
        UAIChatPlus_Util::CopyTexture2DToClipboard(Texture);
        UE_LOG(LogTemp, Display, TEXT("Image copied to clipboard"));
    }
}
```

##오디오 도구

###WAV 파일 불러오기

```cpp
void UMyClass::LoadWavFile()
{
    FString WavPath = FPaths::ProjectContentDir() / TEXT("Audio/sample.wav");
    USoundWave* Sound = UAIChatPlus_Util::LoadSoundWav(WavPath);

    if (Sound)
    {
        UE_LOG(LogTemp, Display, TEXT("Sound loaded: Duration=%.2f, Channels=%d, SampleRate=%d"),
            Sound->Duration,
            Sound->NumChannels,
            Sound->GetSampleRateForCurrentPlatform());
    }
}
```

###오디오를 WAV 파일로 저장하기

```cpp
void UMyClass::SaveWavFile()
{
// 가정 Sound는 기존의 USoundWave입니다
USoundWave* Sound = /* 오디오 가져오기 */;

    FString SavePath = FPaths::ProjectSavedDir() / TEXT("output.wav");
    bool bSaved = UAIChatPlus_Util::SaveSoundWav(Sound, SavePath);

    if (bSaved)
    {
        UE_LOG(LogTemp, Display, TEXT("Sound saved to: %s"), *SavePath);
    }
}
```

###오디오를 Base64로 변환

```cpp
void UMyClass::SoundToBase64()
{
    USoundWave* Sound = UAIChatPlus_Util::LoadSoundWav(TEXT("D:/audio.wav"));

// Base64 문자열로 변환
    FString B64String = UAIChatPlus_Util::SoundToB64(Sound);

    UE_LOG(LogTemp, Display, TEXT("Audio Base64 length: %d"), B64String.Len());
}
```

###WAV 데이터를 SoundWave로 변환

```cpp
void UMyClass::WavDataToSound()
{
// 파일에서 원시 데이터 읽기
    TArray<uint8> RawData;
    FFileHelper::LoadFileToArray(RawData, TEXT("D:/audio.wav"));

// SoundWave로 변환
    USoundWave* Sound = UAIChatPlus_Util::WavDataToSoundWave(
        RawData,
        false,  // bIsAmbiX
        false   // bIsFuMa
    );

    if (Sound)
    {
        UE_LOG(LogTemp, Display, TEXT("Sound created from data"));
    }
}
```

###SoundWave 복사하기

```cpp
void UMyClass::CopySoundWave()
{
    USoundWave* Original = UAIChatPlus_Util::LoadSoundWav(TEXT("D:/audio.wav"));

// 오디오 복사
    USoundWave* Copy = UAIChatPlus_Util::CopySoundWave(
        Original,
        nullptr,    // Outer
NAME_None   // 이름
    );
}
```

### 원시 PCM 데이터 가져오기

```cpp
void UMyClass::GetPCMData()
{
    USoundWave* Sound = UAIChatPlus_Util::LoadSoundWav(TEXT("D:/audio.wav"));

// 원본 PCM 데이터 가져오기
    TArray<uint8> PCMData = UAIChatPlus_Util::GetSoundWavePCMData(Sound);

    UE_LOG(LogTemp, Display, TEXT("PCM data size: %d bytes"), PCMData.Num());
}
```

###녹음 데이터로부터 SoundWave 생성하기

```cpp
void UMyClass::RecorderDataToSound()
{
// Audio Capture로부터 얻은 녹음 데이터라고 가정합니다
TArray<float> RecorderData;  // 오디오 샘플 데이터
int32 NumChannels = 1;       // 모노 채널
int32 SampleRate = 16000;    // 샘플링 레이트

    USoundWave* Sound = UAIChatPlus_Util::RecorderDataToSoundWave(
        RecorderData,
        NumChannels,
        SampleRate
    );

    if (Sound)
    {
        UE_LOG(LogTemp, Display, TEXT("Sound created from recorder data"));
    }
}
```

##로그 제어

```cpp
void UMyClass::ControlLogging()
{
// 내부 로그 레벨 설정
    UAIChatPlus_Util::SetInternalLogVerbosity(EAIChatPlus_LogVerbosityType::Verbose);

// 사용 가능한 레벨:
    // - NoLogging
    // - Fatal
    // - Error
    // - Warning
    // - Display
    // - Log
    // - Verbose
    // - VeryVerbose
}
```

##응답 래퍼 헬퍼 함수

콜백에서 응답을 처리할 때 `FAIChatPlus_PointerWrapper`를 구체적인 타입으로 변환해야 합니다:

```cpp
void UMyClass::HandleCallbackResponse()
{
// OnFinished 콜백 내에서
    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
// 응답 메시지 가져오기
        FString Message = UAIChatPlus_Util::GetResponseWrapperMessage(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Message: %s"), *Message);

// 혹은 기본 응답 유형으로 변환합니다
        FAIChatPlus_ChatResponseBodyBase& Response = UAIChatPlus_Util::CastWrapperToResponse(ResponseWrapper);
    });

// OnFailed 콜백에서
    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
// 오류 설명 가져오기
        FString ErrorDesc = UAIChatPlus_Util::GetErrorWrapperDescription(ErrorWrapper);
        UE_LOG(LogTemp, Error, TEXT("Error: %s"), *ErrorDesc);

// 또는 오류 유형으로 변환합니다
        FAIChatPlus_ResponseErrorBase& Error = UAIChatPlus_Util::CastWrapperToError(ErrorWrapper);
    });
}
```

##모델 정보 조회

```cpp
void UMyClass::QueryModelInfo()
{
// OpenAI 기본 모델 목록 가져오기
    const TArray<FName>& OpenAIModels = UAIChatPlus_Util::GetOpenAIChatDefaultModels();

// 특정 모델 정보 가져오기
    FAIChatPlus_ChatModelInfo ModelInfo = UAIChatPlus_Util::GetOpenAIChatModelInfo(TEXT("gpt-4o"));
    UE_LOG(LogTemp, Display, TEXT("Model: %s, MaxTokens: %d, SupportImage: %s"),
        *ModelInfo.Name.ToString(),
        ModelInfo.MaxTokens,
        ModelInfo.IsSupportSendImage ? TEXT("Yes") : TEXT("No"));

// 클로드 모델
    const TArray<FName>& ClaudeModels = UAIChatPlus_Util::GetClaudeChatDefaultModels();
    FAIChatPlus_ChatModelInfo ClaudeInfo = UAIChatPlus_Util::GetClaudeChatModelInfo(TEXT("claude-3-5-sonnet"));

// 제미니 모델
    const TArray<FName>& GeminiModels = UAIChatPlus_Util::GetGeminiChatDefaultModels();
    FAIChatPlus_ChatModelInfo GeminiInfo = UAIChatPlus_Util::GetGeminiChatModelInfo(TEXT("gemini-1.5-pro"));
}
```

##Cllama 헬퍼 함수

```cpp
void UMyClass::CllamaUtilities()
{
// Cllama 사용 가능 여부 확인
    if (UAIChatPlus_Util::Cllama_IsValid())
    {
        UE_LOG(LogTemp, Display, TEXT("Cllama is available"));
    }

// GPU 지원 확인
    if (UAIChatPlus_Util::Cllama_IsSupportGpu())
    {
        UE_LOG(LogTemp, Display, TEXT("GPU acceleration supported"));
    }

// 지원되는 백엔드 가져오기
    TArray<FString> Backends = UAIChatPlus_Util::Cllama_GetSupportBackends();
    for (const FString& Backend : Backends)
    {
        UE_LOG(LogTemp, Display, TEXT("Backend: %s"), *Backend);
    }

// Pak 내부의 모델 경로 준비하기
    FString ModelPath = TEXT("Models/my_model.gguf");
    FString ActualPath = UAIChatPlus_Util::Cllama_PrepareModelPathFromPak(ModelPath);
// 모델이 Pak에 있을 경우 임시 디렉토리에 압축을 풀고 새 경로를 반환합니다
}
```

##파일 보조 함수

```cpp
void UMyClass::FileUtilities()
{
// 플러그인 기본 디렉토리 가져오기
    FString PluginDir = UAIChatPlus_Util::GetPluginBaseDir(TEXT("AIChatPlus"));
    UE_LOG(LogTemp, Display, TEXT("Plugin dir: %s"), *PluginDir);

// 디렉토리 복사
    FString SourceDir = FPaths::ProjectContentDir() / TEXT("Source");
    FString DestDir = FPaths::ProjectSavedDir() / TEXT("Backup");
bool bCopied = UAIChatPlus_Util::CopyDirectory(SourceDir, DestDir, true);  // true = 덮어쓰기
}
```

##프롬프트 템플릿

```cpp
void UMyClass::PromptTemplates()
{
    // 프롬프트 템플릿 JSON 파일 목록 가져오기
TArray<FDirectoryPath> ExtraDirs;  // 추가 검색 디렉터리 (선택 사항)
    TArray<FFilePath> TemplateFiles = UAIChatPlus_Util::GetPromptTemplateJsonFiles(ExtraDirs);

// 프롬프트 템플릿 로드
    TArray<FAIChatPlus_PromptTemplate> Templates = UAIChatPlus_Util::GetPromptTemplates(TemplateFiles);

    for (const FAIChatPlus_PromptTemplate& Template : Templates)
    {
        UE_LOG(LogTemp, Display, TEXT("Template: %s"), *Template.Name);
    }
}
```

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 누락된 부분이라도 지적해 주세요. 
