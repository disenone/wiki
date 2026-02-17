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

#C++ Section - Utils

This document introduces the utility classes provided by AIChatPlus, including functions such as JSON manipulation, image processing, and audio processing.

##Preparatory Work

Add module dependencies in the project's `.Build.cs` file:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

Include necessary header files:

```cpp
#include "Common/AIChatPlus_Util.h"
#include "Common/Json/AIChatPlus_JsonObject.h"
#include "Common/Json/AIChatPlus_JsonArray.h"
```

##JSON Operations

AIChatPlus offers a Blueprint-friendly JSON operation class, supporting chained calls and type-safe operations.

###UAIChatPlus_JsonObject - JSON Object

####Creation and Parsing

```cpp
#include "Common/Json/AIChatPlus_JsonObject.h"

void UMyClass::JsonObjectBasics()
{
    // Create an empty JSON object
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Create();

// Parsing from string
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

####Set Fields (Chaining Calls)

```cpp
void UMyClass::SetJsonFields()
{
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Create();

// Chaining field settings
    JsonObj->SetStringField(TEXT("name"), TEXT("John"))
           ->SetIntegerField(TEXT("age"), 30)
           ->SetBooleanField(TEXT("active"), true)
           ->SetNumberField(TEXT("score"), 95.5f)
           ->SetNullField(TEXT("extra"));

// Set nested object
    UAIChatPlus_JsonObject* AddressObj = UAIChatPlus_JsonObject::Create();
    AddressObj->SetStringField(TEXT("city"), TEXT("Tokyo"))
              ->SetStringField(TEXT("country"), TEXT("Japan"));

    JsonObj->SetObjectField(TEXT("address"), AddressObj);

// Output
    FString Result = JsonObj->ToString(true);  // true = formatted output
    UE_LOG(LogTemp, Display, TEXT("%s"), *Result);
}
```

####Retrieve field

```cpp
void UMyClass::GetJsonFields()
{
    FString JsonString = TEXT(R"({"name": "John", "age": 30, "scores": [85, 90, 95]})");
    bool bParseSuccess;
    FString ErrorMessage;
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Parse(JsonString, bParseSuccess, ErrorMessage);

    if (!bParseSuccess) return;

    bool bSuccess;

// Get string field
    FString Name = JsonObj->GetStringField(TEXT("name"), TEXT("Unknown"), bSuccess);
    if (bSuccess)
    {
        UE_LOG(LogTemp, Display, TEXT("Name: %s"), *Name);
    }

// Get integer field
    int32 Age = JsonObj->GetIntegerField(TEXT("age"), 0, bSuccess);

// Get the boolean field
    bool bActive = JsonObj->GetBooleanField(TEXT("active"), false, bSuccess);

// Get array field
    UAIChatPlus_JsonArray* Scores = JsonObj->GetArrayField(TEXT("scores"), bSuccess);
    if (bSuccess && Scores)
    {
        for (int32 i = 0; i < Scores->Length(); ++i)
        {
            int32 Score = Scores->GetInteger(i, 0, bSuccess);
            UE_LOG(LogTemp, Display, TEXT("Score[%d]: %d"), i, Score);
        }
    }

// Get nested object fields
    UAIChatPlus_JsonObject* AddressObj = JsonObj->GetObjectField(TEXT("address"), bSuccess);
    if (bSuccess && AddressObj)
    {
        FString City = AddressObj->GetStringField(TEXT("city"), TEXT(""), bSuccess);
    }
}
```

####Field Inspection and Management

```cpp
void UMyClass::ManageJsonFields()
{
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Create();
    JsonObj->SetStringField(TEXT("name"), TEXT("John"))
           ->SetIntegerField(TEXT("age"), 30);

// Check if the field exists
    if (JsonObj->HasField(TEXT("name")))
    {
        UE_LOG(LogTemp, Display, TEXT("Field 'name' exists"));
    }

// Get field type
    EAIChatPlus_JsonValueType FieldType = JsonObj->GetFieldType(TEXT("age"));
    // FieldType == EAIChatPlus_JsonValueType::Number

// Retrieve all field names
    TArray<FString> FieldNames = JsonObj->GetFieldNames();
    for (const FString& Name : FieldNames)
    {
        UE_LOG(LogTemp, Display, TEXT("Field: %s"), *Name);
    }

// Delete field
    JsonObj->RemoveField(TEXT("age"));

    // Clear all fields
    JsonObj->Clear();
}
```

####Path Query (Nested Access)

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

    // Get value by path
    FAIChatPlus_JsonQueryResult Result;
    FString Gold = JsonObj->GetStringByPath(TEXT("player.inventory.gold"), TEXT("0"), Result);
    // Gold = "1000"

// Set value by path
    FAIChatPlus_JsonPathOptions PathOptions;
    JsonObj->SetStringByPath(TEXT("player.inventory.gold"), TEXT("2000"), PathOptions);
}
```

####Merge and Copy

```cpp
void UMyClass::MergeAndDuplicate()
{
    UAIChatPlus_JsonObject* Obj1 = UAIChatPlus_JsonObject::Create();
    Obj1->SetStringField(TEXT("name"), TEXT("John"));

    UAIChatPlus_JsonObject* Obj2 = UAIChatPlus_JsonObject::Create();
    Obj2->SetIntegerField(TEXT("age"), 30)
        ->SetStringField(TEXT("name"), TEXT("Jane"));  // Override name

    // Merge (overwrite existing fields when bOverwrite = true)
    Obj1->Merge(Obj2, true);
// Obj1 now contains {"name": "Jane", "age": 30}

// Deep copy
    UAIChatPlus_JsonObject* Copy = Obj1->Duplicate();
}
```

####Interoperability with UStruct

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
// Converting UStruct to JsonObject
    FMyData Data;
    Data.Name = TEXT("John");
    Data.Age = 30;

    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::FromStruct(Data);

    // Convert JsonObject to UStruct
    FMyData OutData;
    bool bSuccess = JsonObj->ToStruct(OutData);

    if (bSuccess)
    {
        UE_LOG(LogTemp, Display, TEXT("Name: %s, Age: %d"), *OutData.Name, OutData.Age);
    }
}
```

###UAIChatPlus_JsonArray - JSON Array

####Creation and Manipulation

```cpp
#include "Common/Json/AIChatPlus_JsonArray.h"

void UMyClass::JsonArrayBasics()
{
// Create an empty array
    UAIChatPlus_JsonArray* JsonArray = UAIChatPlus_JsonArray::Create();

// Add an element (chaining call)
    JsonArray->AddString(TEXT("apple"))
             ->AddString(TEXT("banana"))
             ->AddInteger(42)
             ->AddBoolean(true)
             ->AddNull();

// Add object element
    UAIChatPlus_JsonObject* ItemObj = UAIChatPlus_JsonObject::Create();
    ItemObj->SetStringField(TEXT("name"), TEXT("sword"));
    JsonArray->AddObject(ItemObj);

// Add nested array
    UAIChatPlus_JsonArray* NestedArray = UAIChatPlus_JsonArray::Create();
    NestedArray->AddInteger(1)->AddInteger(2)->AddInteger(3);
    JsonArray->AddArray(NestedArray);

// Output
    FString Result = JsonArray->ToString(true);
    UE_LOG(LogTemp, Display, TEXT("%s"), *Result);
}
```

####Retrieve elements

```cpp
void UMyClass::GetArrayElements()
{
    FString JsonString = TEXT(R"(["apple", "banana", 42, true, {"name": "item"}])");
    bool bParseSuccess;
    FString ErrorMessage;
    UAIChatPlus_JsonArray* JsonArray = UAIChatPlus_JsonArray::Parse(JsonString, bParseSuccess, ErrorMessage);

    if (!bParseSuccess) return;

    bool bSuccess;

// Retrieve string elements
    FString Fruit = JsonArray->GetString(0, TEXT(""), bSuccess);  // "apple"

// Retrieve integer elements
    int32 Number = JsonArray->GetInteger(2, 0, bSuccess);  // 42

// Retrieve boolean element
    bool bValue = JsonArray->GetBoolean(3, false, bSuccess);  // true

// Get object elements
    UAIChatPlus_JsonObject* Obj = JsonArray->GetObject(4, bSuccess);
    if (bSuccess && Obj)
    {
        FString Name = Obj->GetStringField(TEXT("name"), TEXT(""), bSuccess);
    }

// Iterate through the array
    for (int32 i = 0; i < JsonArray->Length(); ++i)
    {
        EAIChatPlus_JsonValueType Type = JsonArray->GetElementType(i);
        UE_LOG(LogTemp, Display, TEXT("Element[%d] type: %d"), i, static_cast<int32>(Type));
    }
}
```

####Array Operations

```cpp
void UMyClass::ArrayOperations()
{
    UAIChatPlus_JsonArray* JsonArray = UAIChatPlus_JsonArray::Create();
    JsonArray->AddString(TEXT("a"))
             ->AddString(TEXT("b"))
             ->AddString(TEXT("c"));

    // Get length
    int32 Len = JsonArray->Length();  // 3

    // Check if the index is valid
    bool bValid = JsonArray->IsValidIndex(1);  // true

// Set element
    bool bSuccess;
    JsonArray->SetString(1, TEXT("B"), bSuccess);

    // Delete element
    JsonArray->RemoveAt(0, bSuccess);

// Clear the array
    JsonArray->Clear();

// Deep copy
    UAIChatPlus_JsonArray* Copy = JsonArray->Duplicate();
}
```

####Batch Conversion

```cpp
void UMyClass::BatchConversion()
{
// Create from string array
    TArray<FString> StringArray = {TEXT("a"), TEXT("b"), TEXT("c")};
    UAIChatPlus_JsonArray* JsonArray = UAIChatPlus_JsonArray::FromStringArray(StringArray);

// Convert back to string array
    bool bSuccess;
    TArray<FString> OutArray = JsonArray->ToStringArray(bSuccess);

// Create from an integer array
    TArray<int32> IntArray = {1, 2, 3, 4, 5};
    UAIChatPlus_JsonArray* IntJsonArray = UAIChatPlus_JsonArray::FromIntegerArray(IntArray);

// Convert back to integer array
    TArray<int32> OutIntArray = IntJsonArray->ToIntegerArray(bSuccess);
}
```

###UAIChatPlus_Util - JSON Helper Functions

```cpp
void UMyClass::JsonUtilFunctions()
{
// Merge two JSON strings
    FString Json1 = TEXT(R"({"name": "John"})");
    FString Json2 = TEXT(R"({"age": 30, "name": "Jane"})");
    FString Merged = UAIChatPlus_Util::MergeJsonObjects(Json1, Json2);
    // Merged = {"name": "Jane", "age": 30}

    // Load JSON string as an object
    TSharedPtr<FJsonObject> JsonObj = UAIChatPlus_Util::LoadJsonString(Json1);

// Convert object to string
    FString JsonString = UAIChatPlus_Util::ToJsonString(JsonObj);
}
```

##Image Tool

###Load and Save Images

```cpp
#include "Common/AIChatPlus_Util.h"

void UMyClass::ImageLoadSave()
{
// Load image from file
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath, true);  // true = complete compilation

    if (Texture)
    {
        UE_LOG(LogTemp, Display, TEXT("Image loaded: %dx%d"),
            Texture->GetSizeX(), Texture->GetSizeY());
    }

// Save the image to file
    FString SavePath = FPaths::ProjectSavedDir() / TEXT("output.png");
    bool bSaved = UAIChatPlus_Util::SaveImage(Texture, SavePath);

    if (bSaved)
    {
        UE_LOG(LogTemp, Display, TEXT("Image saved to: %s"), *SavePath);
    }
}
```

###Image to Base64

```cpp
void UMyClass::ImageToBase64()
{
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(TEXT("D:/image.png"));

// Convert to Base64 string
    // InQuality: 0 = PNG, 1-100 = JPEG quality
    FString B64String = UAIChatPlus_Util::ImageToB64(Texture, 0);  // PNG format

    UE_LOG(LogTemp, Display, TEXT("Base64 length: %d"), B64String.Len());
}
```

###Copy Image

```cpp
void UMyClass::CopyTexture()
{
    UTexture2D* Original = UAIChatPlus_Util::LoadImage(TEXT("D:/image.png"));

    // Copy texture
    UTexture2D* Copy = UAIChatPlus_Util::CopyTexture2D(
        Original,
        nullptr,        // Outer (nullptr = GetTransientPackage())
NAME_None,      // Name
RF_NoFlags      // Flags
    );

// Blueprint version (with default flags)
    UTexture2D* BPCopy = UAIChatPlus_Util::CopyTexture2DInBlueprint(Original);
}
```

###Get images from URL

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

###Get the image from Base64

```cpp
void UMyClass::GetImageFromBase64()
{
    FString B64String = TEXT("iVBORw0KGgoAAAANSUhEUg...");  // Base64 data

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

###Copy image to clipboard

```cpp
void UMyClass::CopyToClipboard()
{
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(TEXT("D:/image.png"));

// Check if supported
    if (UAIChatPlus_Util::IsCanCopyTexture2DToClipboard())
    {
        UAIChatPlus_Util::CopyTexture2DToClipboard(Texture);
        UE_LOG(LogTemp, Display, TEXT("Image copied to clipboard"));
    }
}
```

##Audio Tools

###Loading WAV file

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

###Save audio as WAV file

```cpp
void UMyClass::SaveWavFile()
{
    // Assuming Sound is an existing USoundWave
USoundWave* Sound = /* Get audio */;

    FString SavePath = FPaths::ProjectSavedDir() / TEXT("output.wav");
    bool bSaved = UAIChatPlus_Util::SaveSoundWav(Sound, SavePath);

    if (bSaved)
    {
        UE_LOG(LogTemp, Display, TEXT("Sound saved to: %s"), *SavePath);
    }
}
```

###Audio to Base64

```cpp
void UMyClass::SoundToBase64()
{
    USoundWave* Sound = UAIChatPlus_Util::LoadSoundWav(TEXT("D:/audio.wav"));

// Convert to Base64 string
    FString B64String = UAIChatPlus_Util::SoundToB64(Sound);

    UE_LOG(LogTemp, Display, TEXT("Audio Base64 length: %d"), B64String.Len());
}
```

###WAV data to SoundWave.

```cpp
void UMyClass::WavDataToSound()
{
    // Read raw data from file
    TArray<uint8> RawData;
    FFileHelper::LoadFileToArray(RawData, TEXT("D:/audio.wav"));

// Convert to SoundWave
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

###Copy SoundWave

```cpp
void UMyClass::CopySoundWave()
{
    USoundWave* Original = UAIChatPlus_Util::LoadSoundWav(TEXT("D:/audio.wav"));

// Copy audio
    USoundWave* Copy = UAIChatPlus_Util::CopySoundWave(
        Original,
        nullptr,    // Outer
NAME_None   // Name
    );
}
```

###Obtaining Raw PCM Data

```cpp
void UMyClass::GetPCMData()
{
    USoundWave* Sound = UAIChatPlus_Util::LoadSoundWav(TEXT("D:/audio.wav"));

// Retrieve original PCM data
    TArray<uint8> PCMData = UAIChatPlus_Util::GetSoundWavePCMData(Sound);

    UE_LOG(LogTemp, Display, TEXT("PCM data size: %d bytes"), PCMData.Num());
}
```

###Create SoundWave from audio data

```cpp
void UMyClass::RecorderDataToSound()
{
    // Assume the recorded data obtained from Audio Capture
    TArray<float> RecorderData;  // Audio sample data
int32 NumChannels = 1;       // Mono
    int32 SampleRate = 16000;    // Sample rate

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

##Log Control

```cpp
void UMyClass::ControlLogging()
{
// Set internal log level
    UAIChatPlus_Util::SetInternalLogVerbosity(EAIChatPlus_LogVerbosityType::Verbose);

// Available levels:
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

##Response wrapper helper function

When handling responses in the callback, it's necessary to cast `FAIChatPlus_PointerWrapper` to its specific type:

```cpp
void UMyClass::HandleCallbackResponse()
{
// Inside the OnFinished callback
    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
// Get the response message
        FString Message = UAIChatPlus_Util::GetResponseWrapperMessage(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Message: %s"), *Message);

// Or convert to a basic response type
        FAIChatPlus_ChatResponseBodyBase& Response = UAIChatPlus_Util::CastWrapperToResponse(ResponseWrapper);
    });

// Inside the OnFailed callback
    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
// Get the error description
        FString ErrorDesc = UAIChatPlus_Util::GetErrorWrapperDescription(ErrorWrapper);
        UE_LOG(LogTemp, Error, TEXT("Error: %s"), *ErrorDesc);

// Or convert to error type
        FAIChatPlus_ResponseErrorBase& Error = UAIChatPlus_Util::CastWrapperToError(ErrorWrapper);
    });
}
```

##Model Information Query

```cpp
void UMyClass::QueryModelInfo()
{
// Retrieve the default model list from OpenAI
    const TArray<FName>& OpenAIModels = UAIChatPlus_Util::GetOpenAIChatDefaultModels();

// Retrieve specific model information
    FAIChatPlus_ChatModelInfo ModelInfo = UAIChatPlus_Util::GetOpenAIChatModelInfo(TEXT("gpt-4o"));
    UE_LOG(LogTemp, Display, TEXT("Model: %s, MaxTokens: %d, SupportImage: %s"),
        *ModelInfo.Name.ToString(),
        ModelInfo.MaxTokens,
        ModelInfo.IsSupportSendImage ? TEXT("Yes") : TEXT("No"));

    // Claude model
    const TArray<FName>& ClaudeModels = UAIChatPlus_Util::GetClaudeChatDefaultModels();
    FAIChatPlus_ChatModelInfo ClaudeInfo = UAIChatPlus_Util::GetClaudeChatModelInfo(TEXT("claude-3-5-sonnet"));

    // Gemini Model
    const TArray<FName>& GeminiModels = UAIChatPlus_Util::GetGeminiChatDefaultModels();
    FAIChatPlus_ChatModelInfo GeminiInfo = UAIChatPlus_Util::GetGeminiChatModelInfo(TEXT("gemini-1.5-pro"));
}
```

##Cllama Helper Functions

```cpp
void UMyClass::CllamaUtilities()
{
// Check if Cllama is available
    if (UAIChatPlus_Util::Cllama_IsValid())
    {
        UE_LOG(LogTemp, Display, TEXT("Cllama is available"));
    }

// Check GPU support
    if (UAIChatPlus_Util::Cllama_IsSupportGpu())
    {
        UE_LOG(LogTemp, Display, TEXT("GPU acceleration supported"));
    }

// Get supported backends
    TArray<FString> Backends = UAIChatPlus_Util::Cllama_GetSupportBackends();
    for (const FString& Backend : Backends)
    {
        UE_LOG(LogTemp, Display, TEXT("Backend: %s"), *Backend);
    }

// Prepare the model path in Pak
    FString ModelPath = TEXT("Models/my_model.gguf");
    FString ActualPath = UAIChatPlus_Util::Cllama_PrepareModelPathFromPak(ModelPath);
    // If the model is in Pak, it will be extracted to a temporary directory and the new path will be returned
}
```

##File Helper Functions

```cpp
void UMyClass::FileUtilities()
{
// Get the base directory of the plugin
    FString PluginDir = UAIChatPlus_Util::GetPluginBaseDir(TEXT("AIChatPlus"));
    UE_LOG(LogTemp, Display, TEXT("Plugin dir: %s"), *PluginDir);

    // Copy directory
    FString SourceDir = FPaths::ProjectContentDir() / TEXT("Source");
    FString DestDir = FPaths::ProjectSavedDir() / TEXT("Backup");
bool bCopied = UAIChatPlus_Util::CopyDirectory(SourceDir, DestDir, true);  // true = overwrite
}
```

##Prompt Template

```cpp
void UMyClass::PromptTemplates()
{
// Retrieve the list of Prompt template JSON files
TArray<FDirectoryPath> ExtraDirs; // Additional search directories (optional)
    TArray<FFilePath> TemplateFiles = UAIChatPlus_Util::GetPromptTemplateJsonFiles(ExtraDirs);

    // Load Prompt template
    TArray<FAIChatPlus_PromptTemplate> Templates = UAIChatPlus_Util::GetPromptTemplates(TemplateFiles);

    for (const FAIChatPlus_PromptTemplate& Template : Templates)
    {
        UE_LOG(LogTemp, Display, TEXT("Template: %s"), *Template.Name);
    }
}
```

--8<-- "footer_en.md"


> This post was translated using ChatGPT. Please provide feedback **[here](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions therein. 
