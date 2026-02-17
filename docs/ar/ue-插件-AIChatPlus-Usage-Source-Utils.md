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

#++C قسم - أدوات مساعدة

يقدم هذا المستند شرحًا للأدوات التي يوفرها AIChatPlus، بما في ذلك وظائف مثل معالجة JSON ومعالجة الصور ومعالجة الصوت وغيرها من الوظائف.

##الاستعدادات

في ملف `.Build.cs` الخاص بالمشروع، أضف تبعيات الوحدة:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

يشمل ملفات الرأس اللازمة:

```cpp
#include "Common/AIChatPlus_Util.h"
#include "Common/Json/AIChatPlus_JsonObject.h"
#include "Common/Json/AIChatPlus_JsonArray.h"
```

##عمليات JSON

يقدم AIChatPlus فئة عمليات JSON صديقة لـ Blueprint، تدعم الاستدعاءات المتسلسلة والعمليات الآمنة للنوع.

###UAIChatPlus_JsonObject - كائن JSON

####إنشاء وتحليل

```cpp
#include "Common/Json/AIChatPlus_JsonObject.h"

void UMyClass::JsonObjectBasics()
{
// إنشاء كائن JSON فارغ
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Create();

    // التحليل من السلسلة النصية
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

####تعيين الحقول (استدعاء متسلسل)

```cpp
void UMyClass::SetJsonFields()
{
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Create();

// إعداد الحقول المتسلسلة
    JsonObj->SetStringField(TEXT("name"), TEXT("John"))
           ->SetIntegerField(TEXT("age"), 30)
           ->SetBooleanField(TEXT("active"), true)
           ->SetNumberField(TEXT("score"), 95.5f)
           ->SetNullField(TEXT("extra"));

// تعيين كائن متداخل
    UAIChatPlus_JsonObject* AddressObj = UAIChatPlus_JsonObject::Create();
    AddressObj->SetStringField(TEXT("city"), TEXT("Tokyo"))
              ->SetStringField(TEXT("country"), TEXT("Japan"));

    JsonObj->SetObjectField(TEXT("address"), AddressObj);

// الإخراج
FString Result = JsonObj->ToString(true);  // true = إخراج منسّق
    UE_LOG(LogTemp, Display, TEXT("%s"), *Result);
}
```

####الحصول على الحقل

```cpp
void UMyClass::GetJsonFields()
{
    FString JsonString = TEXT(R"({"name": "John", "age": 30, "scores": [85, 90, 95]})");
    bool bParseSuccess;
    FString ErrorMessage;
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Parse(JsonString, bParseSuccess, ErrorMessage);

    if (!bParseSuccess) return;

    bool bSuccess;

// استرداد حقل النص
    FString Name = JsonObj->GetStringField(TEXT("name"), TEXT("Unknown"), bSuccess);
    if (bSuccess)
    {
        UE_LOG(LogTemp, Display, TEXT("Name: %s"), *Name);
    }

    // استرداد الحقل الصحيح
    int32 Age = JsonObj->GetIntegerField(TEXT("age"), 0, bSuccess);

// الحصول على حقل منطقي
    bool bActive = JsonObj->GetBooleanField(TEXT("active"), false, bSuccess);

// الحصول على حقل المصفوفة
    UAIChatPlus_JsonArray* Scores = JsonObj->GetArrayField(TEXT("scores"), bSuccess);
    if (bSuccess && Scores)
    {
        for (int32 i = 0; i < Scores->Length(); ++i)
        {
            int32 Score = Scores->GetInteger(i, 0, bSuccess);
            UE_LOG(LogTemp, Display, TEXT("Score[%d]: %d"), i, Score);
        }
    }

// الحصول على حقول الكائن المتداخل
    UAIChatPlus_JsonObject* AddressObj = JsonObj->GetObjectField(TEXT("address"), bSuccess);
    if (bSuccess && AddressObj)
    {
        FString City = AddressObj->GetStringField(TEXT("city"), TEXT(""), bSuccess);
    }
}
```

####فحص وإدارة الحقول

```cpp
void UMyClass::ManageJsonFields()
{
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Create();
    JsonObj->SetStringField(TEXT("name"), TEXT("John"))
           ->SetIntegerField(TEXT("age"), 30);

    // التحقق من وجود الحقل
    if (JsonObj->HasField(TEXT("name")))
    {
        UE_LOG(LogTemp, Display, TEXT("Field 'name' exists"));
    }

// الحصول على نوع الحقل
    EAIChatPlus_JsonValueType FieldType = JsonObj->GetFieldType(TEXT("age"));
    // FieldType == EAIChatPlus_JsonValueType::Number

// استرداد جميع أسماء الحقول
    TArray<FString> FieldNames = JsonObj->GetFieldNames();
    for (const FString& Name : FieldNames)
    {
        UE_LOG(LogTemp, Display, TEXT("Field: %s"), *Name);
    }

// حذف الحقل
    JsonObj->RemoveField(TEXT("age"));

// مسح جميع الحقول
    JsonObj->Clear();
}
```

####استعلام المسار (الوصول المتداخل)

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

// الحصول على القيمة من خلال المسار
    FAIChatPlus_JsonQueryResult Result;
    FString Gold = JsonObj->GetStringByPath(TEXT("player.inventory.gold"), TEXT("0"), Result);
    // Gold = "1000"

    // تعيين القيمة عبر المسار
    FAIChatPlus_JsonPathOptions PathOptions;
    JsonObj->SetStringByPath(TEXT("player.inventory.gold"), TEXT("2000"), PathOptions);
}
```

####دمج ونسخ

```cpp
void UMyClass::MergeAndDuplicate()
{
    UAIChatPlus_JsonObject* Obj1 = UAIChatPlus_JsonObject::Create();
    Obj1->SetStringField(TEXT("name"), TEXT("John"));

    UAIChatPlus_JsonObject* Obj2 = UAIChatPlus_JsonObject::Create();
    Obj2->SetIntegerField(TEXT("age"), 30)
->SetStringField(TEXT("name"), TEXT("Jane"));  // تغطية الاسم

// الدمج (كتابة فوق الحقول الموجودة إذا كانت bOverwrite = true)
    Obj1->Merge(Obj2, true);
// Obj1 تحتوي الآن على {"name": "Jane", "age": 30}

// النسخ العميق
    UAIChatPlus_JsonObject* Copy = Obj1->Duplicate();
}
```

####التحويل المتبادل مع UStruct

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
// تحويل UStruct إلى JsonObject
    FMyData Data;
    Data.Name = TEXT("John");
    Data.Age = 30;

    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::FromStruct(Data);

    // تحويل JsonObject إلى UStruct
    FMyData OutData;
    bool bSuccess = JsonObj->ToStruct(OutData);

    if (bSuccess)
    {
        UE_LOG(LogTemp, Display, TEXT("Name: %s, Age: %d"), *OutData.Name, OutData.Age);
    }
}
```

###UAIChatPlus_JsonArray - مصفوفة JSON

####إنشاء وتشغيل

```cpp
#include "Common/Json/AIChatPlus_JsonArray.h"

void UMyClass::JsonArrayBasics()
{
// إنشاء مصفوفة فارغة
    UAIChatPlus_JsonArray* JsonArray = UAIChatPlus_JsonArray::Create();

// إضافة عنصر (استدعاء تسلسلي)
    JsonArray->AddString(TEXT("apple"))
             ->AddString(TEXT("banana"))
             ->AddInteger(42)
             ->AddBoolean(true)
             ->AddNull();

// إضافة عنصر كائن
    UAIChatPlus_JsonObject* ItemObj = UAIChatPlus_JsonObject::Create();
    ItemObj->SetStringField(TEXT("name"), TEXT("sword"));
    JsonArray->AddObject(ItemObj);

// إضافة مصفوفة متداخلة
    UAIChatPlus_JsonArray* NestedArray = UAIChatPlus_JsonArray::Create();
    NestedArray->AddInteger(1)->AddInteger(2)->AddInteger(3);
    JsonArray->AddArray(NestedArray);

// الإخراج
    FString Result = JsonArray->ToString(true);
    UE_LOG(LogTemp, Display, TEXT("%s"), *Result);
}
```

####الحصول على العنصر

```cpp
void UMyClass::GetArrayElements()
{
    FString JsonString = TEXT(R"(["apple", "banana", 42, true, {"name": "item"}])");
    bool bParseSuccess;
    FString ErrorMessage;
    UAIChatPlus_JsonArray* JsonArray = UAIChatPlus_JsonArray::Parse(JsonString, bParseSuccess, ErrorMessage);

    if (!bParseSuccess) return;

    bool bSuccess;

// الحصول على عنصر السلسلة النصية
    FString Fruit = JsonArray->GetString(0, TEXT(""), bSuccess);  // "apple"

// الحصول على عنصر عدد صحيح
    int32 Number = JsonArray->GetInteger(2, 0, bSuccess);  // 42

// الحصول على العنصر المنطقي
    bool bValue = JsonArray->GetBoolean(3, false, bSuccess);  // true

// الحصول على عناصر الكائن
    UAIChatPlus_JsonObject* Obj = JsonArray->GetObject(4, bSuccess);
    if (bSuccess && Obj)
    {
        FString Name = Obj->GetStringField(TEXT("name"), TEXT(""), bSuccess);
    }

// اجتياز المصفوفة
    for (int32 i = 0; i < JsonArray->Length(); ++i)
    {
        EAIChatPlus_JsonValueType Type = JsonArray->GetElementType(i);
        UE_LOG(LogTemp, Display, TEXT("Element[%d] type: %d"), i, static_cast<int32>(Type));
    }
}
```

####عمليات المصفوفة

```cpp
void UMyClass::ArrayOperations()
{
    UAIChatPlus_JsonArray* JsonArray = UAIChatPlus_JsonArray::Create();
    JsonArray->AddString(TEXT("a"))
             ->AddString(TEXT("b"))
             ->AddString(TEXT("c"));

// الحصول على الطول
    int32 Len = JsonArray->Length();  // 3

// التحقق مما إذا كان الفهرس صالحًا
    bool bValid = JsonArray->IsValidIndex(1);  // true

// تعيين العنصر
    bool bSuccess;
    JsonArray->SetString(1, TEXT("B"), bSuccess);

// حذف العنصر
    JsonArray->RemoveAt(0, bSuccess);

// إفراغ المصفوفة
    JsonArray->Clear();

// النسخ العميق
    UAIChatPlus_JsonArray* Copy = JsonArray->Duplicate();
}
```

####تحويل مجمّع

```cpp
void UMyClass::BatchConversion()
{
// الإنشاء من مصفوفة السلاسل
    TArray<FString> StringArray = {TEXT("a"), TEXT("b"), TEXT("c")};
    UAIChatPlus_JsonArray* JsonArray = UAIChatPlus_JsonArray::FromStringArray(StringArray);

// تحويلها مرة أخرى إلى مصفوفة من السلاسل النصية
    bool bSuccess;
    TArray<FString> OutArray = JsonArray->ToStringArray(bSuccess);

// الإنشاء من مصفوفة أعداد صحيحة
    TArray<int32> IntArray = {1, 2, 3, 4, 5};
    UAIChatPlus_JsonArray* IntJsonArray = UAIChatPlus_JsonArray::FromIntegerArray(IntArray);

// التحويل مرة أخرى إلى مصفوفة من الأعداد الصحيحة
    TArray<int32> OutIntArray = IntJsonArray->ToIntegerArray(bSuccess);
}
```

###UAIChatPlus_Util - وظائف مساعدة لـ JSON

```cpp
void UMyClass::JsonUtilFunctions()
{
// دمج سلسلتين JSON
    FString Json1 = TEXT(R"({"name": "John"})");
    FString Json2 = TEXT(R"({"age": 30, "name": "Jane"})");
    FString Merged = UAIChatPlus_Util::MergeJsonObjects(Json1, Json2);
    // Merged = {"name": "Jane", "age": 30}

// تحميل سلسلة JSON ككائن
    TSharedPtr<FJsonObject> JsonObj = UAIChatPlus_Util::LoadJsonString(Json1);

// تحويل الكائن إلى سلسلة نصية
    FString JsonString = UAIChatPlus_Util::ToJsonString(JsonObj);
}
```

##أداة الصور

###تحميل وحفظ الصور

```cpp
#include "Common/AIChatPlus_Util.h"

void UMyClass::ImageLoadSave()
{
    // تحميل الصورة من الملف
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath, true);  // true = اكتمال التجميع

    if (Texture)
    {
        UE_LOG(LogTemp, Display, TEXT("Image loaded: %dx%d"),
            Texture->GetSizeX(), Texture->GetSizeY());
    }

// حفظ الصورة في ملف
    FString SavePath = FPaths::ProjectSavedDir() / TEXT("output.png");
    bool bSaved = UAIChatPlus_Util::SaveImage(Texture, SavePath);

    if (bSaved)
    {
        UE_LOG(LogTemp, Display, TEXT("Image saved to: %s"), *SavePath);
    }
}
```

###تحويل الصورة إلى Base64

```cpp
void UMyClass::ImageToBase64()
{
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(TEXT("D:/image.png"));

// تحويل إلى سلسلة Base64
// الجودة: 0 = PNG، 100-1 = جودة JPEG
FString B64String = UAIChatPlus_Util::ImageToB64(Texture, 0);  // تنسيق PNG

    UE_LOG(LogTemp, Display, TEXT("Base64 length: %d"), B64String.Len());
}
```

###نسخ الصورة

```cpp
void UMyClass::CopyTexture()
{
    UTexture2D* Original = UAIChatPlus_Util::LoadImage(TEXT("D:/image.png"));

// نسخ النسيج
    UTexture2D* Copy = UAIChatPlus_Util::CopyTexture2D(
        Original,
nullptr,        // الخارجي (nullptr = GetTransientPackage())
NAME_None,      // الاسم
        RF_NoFlags      // العلامات
    );

    // الإصدار الأزرق (مع العلامة الافتراضية)
    UTexture2D* BPCopy = UAIChatPlus_Util::CopyTexture2DInBlueprint(Original);
}
```

###الحصول على الصور من الرابط

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

###الحصول على الصورة من Base64

```cpp
void UMyClass::GetImageFromBase64()
{
سلسلة نصية نصية64 = TEXT("iVBORw0KGgoAAAANSUhEUg..."); // بيانات بتنسيق Base64

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

###نسخ الصورة إلى الحافظة

```cpp
void UMyClass::CopyToClipboard()
{
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(TEXT("D:/image.png"));

// التحقق مما إذا كان مدعومًا
    if (UAIChatPlus_Util::IsCanCopyTexture2DToClipboard())
    {
        UAIChatPlus_Util::CopyTexture2DToClipboard(Texture);
        UE_LOG(LogTemp, Display, TEXT("Image copied to clipboard"));
    }
}
```

##أدوات الصوت

###تحميل ملف WAV

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

###حفظ الصوت كملف WAV

```cpp
void UMyClass::SaveWavFile()
{
// لنفترض أن Sound هو USoundWave موجود بالفعل
    USoundWave* الصوت = /* الحصول على الصوت */;

    FString SavePath = FPaths::ProjectSavedDir() / TEXT("output.wav");
    bool bSaved = UAIChatPlus_Util::SaveSoundWav(Sound, SavePath);

    if (bSaved)
    {
        UE_LOG(LogTemp, Display, TEXT("Sound saved to: %s"), *SavePath);
    }
}
```

###تحويل الصوت إلى Base64

```cpp
void UMyClass::SoundToBase64()
{
    USoundWave* Sound = UAIChatPlus_Util::LoadSoundWav(TEXT("D:/audio.wav"));

// التحويل إلى سلسلة Base64
    FString B64String = UAIChatPlus_Util::SoundToB64(Sound);

    UE_LOG(LogTemp, Display, TEXT("Audio Base64 length: %d"), B64String.Len());
}
```

###تحويل بيانات WAV إلى SoundWave

```cpp
void UMyClass::WavDataToSound()
{
// قراءة البيانات الأصلية من الملف
    TArray<uint8> RawData;
    FFileHelper::LoadFileToArray(RawData, TEXT("D:/audio.wav"));

// التحويل إلى SoundWave
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

###نسخ SoundWave

```cpp
void UMyClass::CopySoundWave()
{
    USoundWave* Original = UAIChatPlus_Util::LoadSoundWav(TEXT("D:/audio.wav"));

// نسخ الصوت
    USoundWave* Copy = UAIChatPlus_Util::CopySoundWave(
        Original,
        nullptr,    // Outer
الاسم
    );
}
```

###الحصول على بيانات PCM الأصلية

```cpp
void UMyClass::GetPCMData()
{
    USoundWave* Sound = UAIChatPlus_Util::LoadSoundWav(TEXT("D:/audio.wav"));

// الحصول على بيانات PCM الأصلية
    TArray<uint8> PCMData = UAIChatPlus_Util::GetSoundWavePCMData(Sound);

    UE_LOG(LogTemp, Display, TEXT("PCM data size: %d bytes"), PCMData.Num());
}
```

###إنشاء SoundWave من بيانات التسجيل

```cpp
void UMyClass::RecorderDataToSound()
{
// افترض الحصول على بيانات التسجيل من Audio Capture
TArray<float> RecorderData;  // بيانات عينات الصوت
int32 NumChannels = 1;       // أحادي القناة
int32 SampleRate = 16000;    // معدل العينة

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

##تحكم السجل

```cpp
void UMyClass::ControlLogging()
{
// تعيين مستوى السجل الداخلي
    UAIChatPlus_Util::SetInternalLogVerbosity(EAIChatPlus_LogVerbosityType::Verbose);

المستويات المتاحة:
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

##وظائف مساعدة لمُغلِّف الاستجابة

عند التعامل مع الاستجابة في رد الاتصال، يجب تحويل `FAIChatPlus_PointerWrapper` إلى نوع محدد:

```cpp
void UMyClass::HandleCallbackResponse()
{
// في رد الاتصال OnFinished
    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
// الحصول على رسالة الرد
        FString Message = UAIChatPlus_Util::GetResponseWrapperMessage(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Message: %s"), *Message);

// أو تحويله إلى نوع الاستجابة الأساسية
        FAIChatPlus_ChatResponseBodyBase& Response = UAIChatPlus_Util::CastWrapperToResponse(ResponseWrapper);
    });

// في رد الاتصال OnFailed
    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
// الحصول على وصف الخطأ
        FString ErrorDesc = UAIChatPlus_Util::GetErrorWrapperDescription(ErrorWrapper);
        UE_LOG(LogTemp, Error, TEXT("Error: %s"), *ErrorDesc);

// أو تحويل إلى نوع خطأ
        FAIChatPlus_ResponseErrorBase& Error = UAIChatPlus_Util::CastWrapperToError(ErrorWrapper);
    });
}
```

##استعلام معلومات النموذج

```cpp
void UMyClass::QueryModelInfo()
{
// الحصول على القائمة الافتراضية لنماذج OpenAI
    const TArray<FName>& OpenAIModels = UAIChatPlus_Util::GetOpenAIChatDefaultModels();

// الحصول على معلومات نموذج معين
    FAIChatPlus_ChatModelInfo ModelInfo = UAIChatPlus_Util::GetOpenAIChatModelInfo(TEXT("gpt-4o"));
    UE_LOG(LogTemp, Display, TEXT("Model: %s, MaxTokens: %d, SupportImage: %s"),
        *ModelInfo.Name.ToString(),
        ModelInfo.MaxTokens,
        ModelInfo.IsSupportSendImage ? TEXT("Yes") : TEXT("No"));

// نموذج Claude
    const TArray<FName>& ClaudeModels = UAIChatPlus_Util::GetClaudeChatDefaultModels();
    FAIChatPlus_ChatModelInfo ClaudeInfo = UAIChatPlus_Util::GetClaudeChatModelInfo(TEXT("claude-3-5-sonnet"));

// نموذج جيميني
    const TArray<FName>& GeminiModels = UAIChatPlus_Util::GetGeminiChatDefaultModels();
    FAIChatPlus_ChatModelInfo GeminiInfo = UAIChatPlus_Util::GetGeminiChatModelInfo(TEXT("gemini-1.5-pro"));
}
```

##وظائف مساعدة Cllama

```cpp
void UMyClass::CllamaUtilities()
{
// التحقق مما إذا كان Cllama متاحًا للاستخدام
    if (UAIChatPlus_Util::Cllama_IsValid())
    {
        UE_LOG(LogTemp, Display, TEXT("Cllama is available"));
    }

    // التحقق من دعم وحدة معالجة الرسومات
    if (UAIChatPlus_Util::Cllama_IsSupportGpu())
    {
        UE_LOG(LogTemp, Display, TEXT("GPU acceleration supported"));
    }

// الحصول على الواجهة الخلفية المدعومة
    TArray<FString> Backends = UAIChatPlus_Util::Cllama_GetSupportBackends();
    for (const FString& Backend : Backends)
    {
        UE_LOG(LogTemp, Display, TEXT("Backend: %s"), *Backend);
    }

// تحضير مسار النموذج في Pak
    FString ModelPath = TEXT("Models/my_model.gguf");
    FString ActualPath = UAIChatPlus_Util::Cllama_PrepareModelPathFromPak(ModelPath);
// إذا كان النموذج موجودًا في Pak، فسيتم فك ضغطه إلى دليل مؤقت وإعادة المسار الجديد
}
```

##وظائف مساعدة للملفات

```cpp
void UMyClass::FileUtilities()
{
// الحصول على الدليل الأساسي للمكون الإضافي
    FString PluginDir = UAIChatPlus_Util::GetPluginBaseDir(TEXT("AIChatPlus"));
    UE_LOG(LogTemp, Display, TEXT("Plugin dir: %s"), *PluginDir);

// نسخ الدليل
    FString SourceDir = FPaths::ProjectContentDir() / TEXT("Source");
    FString DestDir = FPaths::ProjectSavedDir() / TEXT("Backup");
bool bCopied = UAIChatPlus_Util::CopyDirectory(SourceDir, DestDir, true);  // true = الكتابة فوق الموجود
}
```

##قالب المُطالبة

```cpp
void UMyClass::PromptTemplates()
{
// الحصول على قائمة ملفات JSON لقوالب موجهة
    TArray<FDirectoryPath> ExtraDirs;  // أدوار بحث إضافية (اختياري)
    TArray<FFilePath> TemplateFiles = UAIChatPlus_Util::GetPromptTemplateJsonFiles(ExtraDirs);

// تحميل قالب موجه
    TArray<FAIChatPlus_PromptTemplate> Templates = UAIChatPlus_Util::GetPromptTemplates(TemplateFiles);

    for (const FAIChatPlus_PromptTemplate& Template : Templates)
    {
        UE_LOG(LogTemp, Display, TEXT("Template: %s"), *Template.Name);
    }
}
```

--8<-- "footer_ar.md"


> هذه المشاركة مترجمة باستخدام ChatGPT، يُرجى تقديم ملاحظاتكم في قسم [**الملاحظات**](https://github.com/disenone/wiki_blog/issues/new)أشير إلى أي نقص موجود. 
