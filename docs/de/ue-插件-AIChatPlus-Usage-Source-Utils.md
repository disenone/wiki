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

#C++ Kapitel - Utils

Dieses Dokument beschreibt die von AIChatPlus bereitgestellten Dienstprogramme, einschließlich Funktionen zur JSON-Verarbeitung, Bildbearbeitung und Audiobearbeitung.

##Vorbereitungen

Fügen Sie im `.Build.cs`-File des Projekts die Modulabhängigkeiten hinzu:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

Einbindung der erforderlichen Headerdateien:

```cpp
#include "Common/AIChatPlus_Util.h"
#include "Common/Json/AIChatPlus_JsonObject.h"
#include "Common/Json/AIChatPlus_JsonArray.h"
```

##JSON-Verarbeitung

AIChatPlus bietet Blueprint-freundliche JSON-Operationen an, die verkettete Aufrufe und typsichere Operationen unterstützen.

###UAIChatPlus_JsonObject - JSON-Objekt

####Erstellen und Parsen

```cpp
#include "Common/Json/AIChatPlus_JsonObject.h"

void UMyClass::JsonObjectBasics()
{
    // Leeres JSON-Objekt erstellen
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Create();

// Aus dem String parsen
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

####Felder setzen (verketteter Aufruf)

```cpp
void UMyClass::SetJsonFields()
{
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Create();

    // Verkettetes Setzen der Felder
    JsonObj->SetStringField(TEXT("name"), TEXT("John"))
           ->SetIntegerField(TEXT("age"), 30)
           ->SetBooleanField(TEXT("active"), true)
           ->SetNumberField(TEXT("score"), 95.5f)
           ->SetNullField(TEXT("extra"));

    // Verschachteltes Objekt einrichten
    UAIChatPlus_JsonObject* AddressObj = UAIChatPlus_JsonObject::Create();
    AddressObj->SetStringField(TEXT("city"), TEXT("Tokyo"))
              ->SetStringField(TEXT("country"), TEXT("Japan"));

    JsonObj->SetObjectField(TEXT("address"), AddressObj);

    // Ausgabe
FString Result = JsonObj->ToString(true); // true = formatiert die Ausgabe
    UE_LOG(LogTemp, Display, TEXT("%s"), *Result);
}
```

####Feld abrufen

```cpp
void UMyClass::GetJsonFields()
{
    FString JsonString = TEXT(R"({"name": "John", "age": 30, "scores": [85, 90, 95]})");
    bool bParseSuccess;
    FString ErrorMessage;
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Parse(JsonString, bParseSuccess, ErrorMessage);

    if (!bParseSuccess) return;

    bool bSuccess;

// Zeichenkettenfeld abrufen
    FString Name = JsonObj->GetStringField(TEXT("name"), TEXT("Unknown"), bSuccess);
    if (bSuccess)
    {
        UE_LOG(LogTemp, Display, TEXT("Name: %s"), *Name);
    }

    // Ganzzahliges Feld abrufen
    int32 Age = JsonObj->GetIntegerField(TEXT("age"), 0, bSuccess);

    // Boolesches Feld abrufen
    bool bActive = JsonObj->GetBooleanField(TEXT("active"), false, bSuccess);

// Abrufen des Array-Felds
    UAIChatPlus_JsonArray* Scores = JsonObj->GetArrayField(TEXT("scores"), bSuccess);
    if (bSuccess && Scores)
    {
        for (int32 i = 0; i < Scores->Length(); ++i)
        {
            int32 Score = Scores->GetInteger(i, 0, bSuccess);
            UE_LOG(LogTemp, Display, TEXT("Score[%d]: %d"), i, Score);
        }
    }

    // Verschachtelte Objektfelder abrufen
    UAIChatPlus_JsonObject* AddressObj = JsonObj->GetObjectField(TEXT("address"), bSuccess);
    if (bSuccess && AddressObj)
    {
        FString City = AddressObj->GetStringField(TEXT("city"), TEXT(""), bSuccess);
    }
}
```

####Feldüberprüfung und -verwaltung

```cpp
void UMyClass::ManageJsonFields()
{
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Create();
    JsonObj->SetStringField(TEXT("name"), TEXT("John"))
           ->SetIntegerField(TEXT("age"), 30);

    // Überprüfen, ob das Feld existiert
    if (JsonObj->HasField(TEXT("name")))
    {
        UE_LOG(LogTemp, Display, TEXT("Field 'name' exists"));
    }

// Den Feldtyp abrufen
    EAIChatPlus_JsonValueType FieldType = JsonObj->GetFieldType(TEXT("age"));
    // FieldType == EAIChatPlus_JsonValueType::Number

    // Alle Feldnamen abrufen
    TArray<FString> FieldNames = JsonObj->GetFieldNames();
    for (const FString& Name : FieldNames)
    {
        UE_LOG(LogTemp, Display, TEXT("Field: %s"), *Name);
    }

// Feld löschen
    JsonObj->RemoveField(TEXT("age"));

    // Alle Felder leeren
    JsonObj->Clear();
}
```

####Pfadabfrage (verschachtelter Zugriff)

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

    // Wert über Pfad abrufen
    FAIChatPlus_JsonQueryResult Result;
    FString Gold = JsonObj->GetStringByPath(TEXT("player.inventory.gold"), TEXT("0"), Result);
    // Gold = "1000"

    // Wert über Pfad setzen
    FAIChatPlus_JsonPathOptions PathOptions;
    JsonObj->SetStringByPath(TEXT("player.inventory.gold"), TEXT("2000"), PathOptions);
}
```

####Zusammenführen und Duplizieren

```cpp
void UMyClass::MergeAndDuplicate()
{
    UAIChatPlus_JsonObject* Obj1 = UAIChatPlus_JsonObject::Create();
    Obj1->SetStringField(TEXT("name"), TEXT("John"));

    UAIChatPlus_JsonObject* Obj2 = UAIChatPlus_JsonObject::Create();
    Obj2->SetIntegerField(TEXT("age"), 30)
        ->SetStringField(TEXT("name"), TEXT("Jane"));  // überschreibt name

// Zusammenführen (überschreibt vorhandene Felder, wenn bOverwrite = true)
    Obj1->Merge(Obj2, true);
// Obj1 enthält jetzt {"name": "Jane", "age": 30}

// Tiefe Kopie
    UAIChatPlus_JsonObject* Copy = Obj1->Duplicate();
}
```

####Umwandlung mit UStruct

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
// UStruct zu JsonObject konvertieren
    FMyData Data;
    Data.Name = TEXT("John");
    Data.Age = 30;

    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::FromStruct(Data);

    // JsonObject zu UStruct konvertieren
    FMyData OutData;
    bool bSuccess = JsonObj->ToStruct(OutData);

    if (bSuccess)
    {
        UE_LOG(LogTemp, Display, TEXT("Name: %s, Age: %d"), *OutData.Name, OutData.Age);
    }
}
```

###UAIChatPlus_JsonArray - JSON-Array

####Erstellen und Verwalten

```cpp
#include "Common/Json/AIChatPlus_JsonArray.h"

void UMyClass::JsonArrayBasics()
{
// Leeres Array erstellen
    UAIChatPlus_JsonArray* JsonArray = UAIChatPlus_JsonArray::Create();

// Element hinzufügen (verketteter Aufruf)
    JsonArray->AddString(TEXT("apple"))
             ->AddString(TEXT("banana"))
             ->AddInteger(42)
             ->AddBoolean(true)
             ->AddNull();

// Objektelement hinzufügen
    UAIChatPlus_JsonObject* ItemObj = UAIChatPlus_JsonObject::Create();
    ItemObj->SetStringField(TEXT("name"), TEXT("sword"));
    JsonArray->AddObject(ItemObj);

    // Verschachteltes Array hinzufügen
    UAIChatPlus_JsonArray* NestedArray = UAIChatPlus_JsonArray::Create();
    NestedArray->AddInteger(1)->AddInteger(2)->AddInteger(3);
    JsonArray->AddArray(NestedArray);

    // Ausgabe
    FString Result = JsonArray->ToString(true);
    UE_LOG(LogTemp, Display, TEXT("%s"), *Result);
}
```

####Element abrufen

```cpp
void UMyClass::GetArrayElements()
{
    FString JsonString = TEXT(R"(["apple", "banana", 42, true, {"name": "item"}])");
    bool bParseSuccess;
    FString ErrorMessage;
    UAIChatPlus_JsonArray* JsonArray = UAIChatPlus_JsonArray::Parse(JsonString, bParseSuccess, ErrorMessage);

    if (!bParseSuccess) return;

    bool bSuccess;

// Stringelement abrufen
    FString Fruit = JsonArray->GetString(0, TEXT(""), bSuccess);  // "apple"

    // Ganze Zahlen-Elemente abrufen
    int32 Number = JsonArray->GetInteger(2, 0, bSuccess);  // 42

    // Boolesches Element abrufen
    bool bValue = JsonArray->GetBoolean(3, false, bSuccess);  // true

// Abrufen der Objektelemente
    UAIChatPlus_JsonObject* Obj = JsonArray->GetObject(4, bSuccess);
    if (bSuccess && Obj)
    {
        FString Name = Obj->GetStringField(TEXT("name"), TEXT(""), bSuccess);
    }

    // Das Array durchlaufen
    for (int32 i = 0; i < JsonArray->Length(); ++i)
    {
        EAIChatPlus_JsonValueType Type = JsonArray->GetElementType(i);
        UE_LOG(LogTemp, Display, TEXT("Element[%d] type: %d"), i, static_cast<int32>(Type));
    }
}
```

####Array-Operationen

```cpp
void UMyClass::ArrayOperations()
{
    UAIChatPlus_JsonArray* JsonArray = UAIChatPlus_JsonArray::Create();
    JsonArray->AddString(TEXT("a"))
             ->AddString(TEXT("b"))
             ->AddString(TEXT("c"));

    // Länge abrufen
    int32 Len = JsonArray->Length();  // 3

    // Überprüfen, ob der Index gültig ist
    bool bValid = JsonArray->IsValidIndex(1);  // true

// Elemente festlegen
    bool bSuccess;
    JsonArray->SetString(1, TEXT("B"), bSuccess);

// Elemente löschen
    JsonArray->RemoveAt(0, bSuccess);

// Array leeren
    JsonArray->Clear();

    // Tiefe Kopie
    UAIChatPlus_JsonArray* Copy = JsonArray->Duplicate();
}
```

####Stapelkonvertierung

```cpp
void UMyClass::BatchConversion()
{
// Aus einem String-Array erstellen
    TArray<FString> StringArray = {TEXT("a"), TEXT("b"), TEXT("c")};
    UAIChatPlus_JsonArray* JsonArray = UAIChatPlus_JsonArray::FromStringArray(StringArray);

    // Zurück zum String-Array konvertieren
    bool bSuccess;
    TArray<FString> OutArray = JsonArray->ToStringArray(bSuccess);

// Aus einem Ganzzahl-Array erstellen
    TArray<int32> IntArray = {1, 2, 3, 4, 5};
    UAIChatPlus_JsonArray* IntJsonArray = UAIChatPlus_JsonArray::FromIntegerArray(IntArray);

    // Zurück zum Integer-Array
    TArray<int32> OutIntArray = IntJsonArray->ToIntegerArray(bSuccess);
}
```

###UAIChatPlus_Util - JSON Hilfsfunktionen

```cpp
void UMyClass::JsonUtilFunctions()
{
// Zwei JSON-Strings zusammenführen
    FString Json1 = TEXT(R"({"name": "John"})");
    FString Json2 = TEXT(R"({"age": 30, "name": "Jane"})");
    FString Merged = UAIChatPlus_Util::MergeJsonObjects(Json1, Json2);
    // Merged = {"name": "Jane", "age": 30}

    // JSON-Zeichenkette als Objekt laden
    TSharedPtr<FJsonObject> JsonObj = UAIChatPlus_Util::LoadJsonString(Json1);

// Objekt in String umwandeln
    FString JsonString = UAIChatPlus_Util::ToJsonString(JsonObj);
}
```

##Bildwerkzeuge

###Bilder laden und speichern

```cpp
#include "Common/AIChatPlus_Util.h"

void UMyClass::ImageLoadSave()
{
// Bild aus Datei laden
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
UTexture2D* Textur = UAIChatPlus_Util::BildLaden(BildPfad, true);  // true = Kompilierung abgeschlossen

    if (Texture)
    {
        UE_LOG(LogTemp, Display, TEXT("Image loaded: %dx%d"),
            Texture->GetSizeX(), Texture->GetSizeY());
    }

    // Bild in Datei speichern
    FString SavePath = FPaths::ProjectSavedDir() / TEXT("output.png");
    bool bSaved = UAIChatPlus_Util::SaveImage(Texture, SavePath);

    if (bSaved)
    {
        UE_LOG(LogTemp, Display, TEXT("Image saved to: %s"), *SavePath);
    }
}
```

###Bild zu Base64 konvertieren

```cpp
void UMyClass::ImageToBase64()
{
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(TEXT("D:/image.png"));

// In Base64-String umwandeln
    // InQuality: 0 = PNG, 1-100 = JPEG-Qualität
FString B64String = UAIChatPlus_Util::ImageToB64(Texture, 0);  // PNG Format

    UE_LOG(LogTemp, Display, TEXT("Base64 length: %d"), B64String.Len());
}
```

###Bild kopieren

```cpp
void UMyClass::CopyTexture()
{
    UTexture2D* Original = UAIChatPlus_Util::LoadImage(TEXT("D:/image.png"));

    // Textur kopieren
    UTexture2D* Copy = UAIChatPlus_Util::CopyTexture2D(
        Original,
nullptr,        // Äußeres (nullptr = GetTransientPackage())
NAME_None,      // Name
RF_NoFlags      // Flags
    );

    // Blueprint-Version (mit Standardflaggen)
    UTexture2D* BPCopy = UAIChatPlus_Util::CopyTexture2DInBlueprint(Original);
}
```

###Bild von URL abrufen

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

###Bild aus Base64 abrufen

```cpp
void UMyClass::GetImageFromBase64()
{
FString B64String = TEXT("iVBORw0KGgoAAAANSUhEUg...");  // Base64-Daten

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

###Bild in die Zwischenablage kopieren

```cpp
void UMyClass::CopyToClipboard()
{
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(TEXT("D:/image.png"));

    // Prüfen, ob unterstützt
    if (UAIChatPlus_Util::IsCanCopyTexture2DToClipboard())
    {
        UAIChatPlus_Util::CopyTexture2DToClipboard(Texture);
        UE_LOG(LogTemp, Display, TEXT("Image copied to clipboard"));
    }
}
```

##Audiowerkzeuge

###WAV-Datei laden

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

###Audio als WAV-Datei speichern

```cpp
void UMyClass::SaveWavFile()
{
    // Angenommen, Sound ist eine vorhandene USoundWave
USoundWave* Sound = /* Audio abrufen */;

    FString SavePath = FPaths::ProjectSavedDir() / TEXT("output.wav");
    bool bSaved = UAIChatPlus_Util::SaveSoundWav(Sound, SavePath);

    if (bSaved)
    {
        UE_LOG(LogTemp, Display, TEXT("Sound saved to: %s"), *SavePath);
    }
}
```

###Audio zu Base64 konvertieren

```cpp
void UMyClass::SoundToBase64()
{
    USoundWave* Sound = UAIChatPlus_Util::LoadSoundWav(TEXT("D:/audio.wav"));

// In eine Base64-Zeichenkette umwandeln
    FString B64String = UAIChatPlus_Util::SoundToB64(Sound);

    UE_LOG(LogTemp, Display, TEXT("Audio Base64 length: %d"), B64String.Len());
}
```

###WAV-Daten in SoundWave konvertieren

```cpp
void UMyClass::WavDataToSound()
{
    // Rohdaten aus der Datei lesen
    TArray<uint8> RawData;
    FFileHelper::LoadFileToArray(RawData, TEXT("D:/audio.wav"));

// Konvertieren in SoundWave
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

###Kopieren Sie SoundWave

```cpp
void UMyClass::CopySoundWave()
{
    USoundWave* Original = UAIChatPlus_Util::LoadSoundWav(TEXT("D:/audio.wav"));

    // Audio kopieren
    USoundWave* Copy = UAIChatPlus_Util::CopySoundWave(
        Original,
        nullptr,    // Outer
NAME_None   // Name
    );
}
```

###Roh-PCM-Daten abrufen

```cpp
void UMyClass::GetPCMData()
{
    USoundWave* Sound = UAIChatPlus_Util::LoadSoundWav(TEXT("D:/audio.wav"));

    // Rohe PCM-Daten abrufen
    TArray<uint8> PCMData = UAIChatPlus_Util::GetSoundWavePCMData(Sound);

    UE_LOG(LogTemp, Display, TEXT("PCM data size: %d bytes"), PCMData.Num());
}
```

###Erstellen einer SoundWave aus Audiokrippendaten

```cpp
void UMyClass::RecorderDataToSound()
{
    // Angenommen, die Aufnahmedaten werden von Audio Capture bezogen
TArray<float> RecorderData;  // Audiodatenabtastung
int32 NumChannels = 1;       // Monokanal
int32 SampleRate = 16000;    // Abtastrate

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

##Protokollsteuerung

```cpp
void UMyClass::ControlLogging()
{
// Internes Log-Level setzen
    UAIChatPlus_Util::SetInternalLogVerbosity(EAIChatPlus_LogVerbosityType::Verbose);

// Verfügbare Ebenen:
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

##Hilfsfunktionen für Antwortwrapper

Bei der Verarbeitung der Antwort im Callback muss der `FAIChatPlus_PointerWrapper` in einen konkreten Typ umgewandelt werden:

```cpp
void UMyClass::HandleCallbackResponse()
{
// Im OnFinished-Rückruf
    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
// Die Antwortnachricht abrufen
        FString Message = UAIChatPlus_Util::GetResponseWrapperMessage(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Message: %s"), *Message);

// oder in einen grundlegenden Antworttyp umwandeln
        FAIChatPlus_ChatResponseBodyBase& Response = UAIChatPlus_Util::CastWrapperToResponse(ResponseWrapper);
    });

// Im OnFailed-Rückruf
    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        // Fehlerbeschreibung abrufen
        FString ErrorDesc = UAIChatPlus_Util::GetErrorWrapperDescription(ErrorWrapper);
        UE_LOG(LogTemp, Error, TEXT("Error: %s"), *ErrorDesc);

        // Oder in den Fehlertyp konvertieren
        FAIChatPlus_ResponseErrorBase& Error = UAIChatPlus_Util::CastWrapperToError(ErrorWrapper);
    });
}
```

##Modellinformationen abfragen

```cpp
void UMyClass::QueryModelInfo()
{
    // Standardmodellliste von OpenAI abrufen
    const TArray<FName>& OpenAIModels = UAIChatPlus_Util::GetOpenAIChatDefaultModels();

    // Abrufen spezifischer Modellinformationen
    FAIChatPlus_ChatModelInfo ModelInfo = UAIChatPlus_Util::GetOpenAIChatModelInfo(TEXT("gpt-4o"));
    UE_LOG(LogTemp, Display, TEXT("Model: %s, MaxTokens: %d, SupportImage: %s"),
        *ModelInfo.Name.ToString(),
        ModelInfo.MaxTokens,
        ModelInfo.IsSupportSendImage ? TEXT("Yes") : TEXT("No"));

// Claude-Modell
    const TArray<FName>& ClaudeModels = UAIChatPlus_Util::GetClaudeChatDefaultModels();
    FAIChatPlus_ChatModelInfo ClaudeInfo = UAIChatPlus_Util::GetClaudeChatModelInfo(TEXT("claude-3-5-sonnet"));

// Gemini-Modell
    const TArray<FName>& GeminiModels = UAIChatPlus_Util::GetGeminiChatDefaultModels();
    FAIChatPlus_ChatModelInfo GeminiInfo = UAIChatPlus_Util::GetGeminiChatModelInfo(TEXT("gemini-1.5-pro"));
}
```

##Cllama Hilfsfunktionen

```cpp
void UMyClass::CllamaUtilities()
{
    // Überprüfen, ob Cllama verfügbar ist
    if (UAIChatPlus_Util::Cllama_IsValid())
    {
        UE_LOG(LogTemp, Display, TEXT("Cllama is available"));
    }

    // Überprüfung der GPU-Unterstützung
    if (UAIChatPlus_Util::Cllama_IsSupportGpu())
    {
        UE_LOG(LogTemp, Display, TEXT("GPU acceleration supported"));
    }

    // Unterstützte Backends abrufen
    TArray<FString> Backends = UAIChatPlus_Util::Cllama_GetSupportBackends();
    for (const FString& Backend : Backends)
    {
        UE_LOG(LogTemp, Display, TEXT("Backend: %s"), *Backend);
    }

    // Bereiten Sie den Modellpfad im Pak vor
    FString ModelPath = TEXT("Models/my_model.gguf");
    FString ActualPath = UAIChatPlus_Util::Cllama_PrepareModelPathFromPak(ModelPath);
// Falls das Modell in einem Paket ist, wird es in ein temporäres Verzeichnis entpackt und der neue Pfad zurückgegeben
}
```

##Datei-Hilfsfunktionen

```cpp
void UMyClass::FileUtilities()
{
    // Basisverzeichnis des Plugins abrufen
    FString PluginDir = UAIChatPlus_Util::GetPluginBaseDir(TEXT("AIChatPlus"));
    UE_LOG(LogTemp, Display, TEXT("Plugin dir: %s"), *PluginDir);

    // Verzeichnis kopieren
    FString SourceDir = FPaths::ProjectContentDir() / TEXT("Source");
    FString DestDir = FPaths::ProjectSavedDir() / TEXT("Backup");
bool bCopied = UAIChatPlus_Util::CopyDirectory(SourceDir, DestDir, true);  // true = Überschreiben
}
```

##Prompt-Vorlage

```cpp
void UMyClass::PromptTemplates()
{
    // Abrufen der Liste der JSON-Dateien für Prompt-Vorlagen
TArray<FDirectoryPath> ExtraDirs;  // Zusätzliche Suchverzeichnisse (optional)
    TArray<FFilePath> TemplateFiles = UAIChatPlus_Util::GetPromptTemplateJsonFiles(ExtraDirs);

// Prompt-Vorlage laden
    TArray<FAIChatPlus_PromptTemplate> Templates = UAIChatPlus_Util::GetPromptTemplates(TemplateFiles);

    for (const FAIChatPlus_PromptTemplate& Template : Templates)
    {
        UE_LOG(LogTemp, Display, TEXT("Template: %s"), *Template.Name);
    }
}
```

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte hinterlassen Sie Ihr Feedback unter [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Weist auf etwaige Auslassungen hin. 
