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

#C++ Capítulo - Utils

Este documento presenta las clases de herramientas que ofrece AIChatPlus, incluidas funciones como manipulación de JSON, procesamiento de imágenes y manejo de audio.

##Preparativos

En el archivo `.Build.cs` del proyecto, añade las dependencias del módulo:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

Incluir los archivos de cabecera necesarios:

```cpp
#include "Common/AIChatPlus_Util.h"
#include "Common/Json/AIChatPlus_JsonObject.h"
#include "Common/Json/AIChatPlus_JsonArray.h"
```

##Operaciones con JSON

AIChatPlus ofrece clases de operación JSON compatibles con Blueprint, que admiten llamadas en cadena y operaciones con seguridad de tipos.

###UAIChatPlus_JsonObject - Objeto JSON

####Creación y análisis

```cpp
#include "Common/Json/AIChatPlus_JsonObject.h"

void UMyClass::JsonObjectBasics()
{
// Crear objeto JSON vacío
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Create();

    // Analizar desde la cadena
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

####Configurar campos (llamada encadenada)

```cpp
void UMyClass::SetJsonFields()
{
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Create();

// Configuración encadenada de campos
    JsonObj->SetStringField(TEXT("name"), TEXT("John"))
           ->SetIntegerField(TEXT("age"), 30)
           ->SetBooleanField(TEXT("active"), true)
           ->SetNumberField(TEXT("score"), 95.5f)
           ->SetNullField(TEXT("extra"));

// Establecer objeto anidado
    UAIChatPlus_JsonObject* AddressObj = UAIChatPlus_JsonObject::Create();
    AddressObj->SetStringField(TEXT("city"), TEXT("Tokyo"))
              ->SetStringField(TEXT("country"), TEXT("Japan"));

    JsonObj->SetObjectField(TEXT("address"), AddressObj);

// salida
FString Result = JsonObj->ToString(true);  // true = salida formateada
    UE_LOG(LogTemp, Display, TEXT("%s"), *Result);
}
```

####Obtener campo

```cpp
void UMyClass::GetJsonFields()
{
    FString JsonString = TEXT(R"({"name": "John", "age": 30, "scores": [85, 90, 95]})");
    bool bParseSuccess;
    FString ErrorMessage;
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Parse(JsonString, bParseSuccess, ErrorMessage);

    if (!bParseSuccess) return;

    bool bSuccess;

// obtener campo de cadena
    FString Name = JsonObj->GetStringField(TEXT("name"), TEXT("Unknown"), bSuccess);
    if (bSuccess)
    {
        UE_LOG(LogTemp, Display, TEXT("Name: %s"), *Name);
    }

// obtener el campo entero
    int32 Age = JsonObj->GetIntegerField(TEXT("age"), 0, bSuccess);

// obtener campo booleano
    bool bActive = JsonObj->GetBooleanField(TEXT("active"), false, bSuccess);

// obtener campo del arreglo
    UAIChatPlus_JsonArray* Scores = JsonObj->GetArrayField(TEXT("scores"), bSuccess);
    if (bSuccess && Scores)
    {
        for (int32 i = 0; i < Scores->Length(); ++i)
        {
            int32 Score = Scores->GetInteger(i, 0, bSuccess);
            UE_LOG(LogTemp, Display, TEXT("Score[%d]: %d"), i, Score);
        }
    }

// Obtener campo de objeto anidado
    UAIChatPlus_JsonObject* AddressObj = JsonObj->GetObjectField(TEXT("address"), bSuccess);
    if (bSuccess && AddressObj)
    {
        FString City = AddressObj->GetStringField(TEXT("city"), TEXT(""), bSuccess);
    }
}
```

####Verificación y gestión de campos

```cpp
void UMyClass::ManageJsonFields()
{
    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::Create();
    JsonObj->SetStringField(TEXT("name"), TEXT("John"))
           ->SetIntegerField(TEXT("age"), 30);

    // Comprobar si el campo existe
    if (JsonObj->HasField(TEXT("name")))
    {
        UE_LOG(LogTemp, Display, TEXT("Field 'name' exists"));
    }

// Obtener el tipo de campo
    EAIChatPlus_JsonValueType FieldType = JsonObj->GetFieldType(TEXT("age"));
    // FieldType == EAIChatPlus_JsonValueType::Number

    // Obtener todos los nombres de campos
    TArray<FString> FieldNames = JsonObj->GetFieldNames();
    for (const FString& Name : FieldNames)
    {
        UE_LOG(LogTemp, Display, TEXT("Field: %s"), *Name);
    }

    // Eliminar campo
    JsonObj->RemoveField(TEXT("age"));

// Vaciar todos los campos
    JsonObj->Clear();
}
```

####Consulta de ruta (acceso anidado)

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

// Obtener el valor mediante la ruta
    FAIChatPlus_JsonQueryResult Result;
    FString Gold = JsonObj->GetStringByPath(TEXT("player.inventory.gold"), TEXT("0"), Result);
    // Gold = "1000"

// Establecer valor mediante ruta
    FAIChatPlus_JsonPathOptions PathOptions;
    JsonObj->SetStringByPath(TEXT("player.inventory.gold"), TEXT("2000"), PathOptions);
}
```

####Combinar y duplicar

```cpp
void UMyClass::MergeAndDuplicate()
{
    UAIChatPlus_JsonObject* Obj1 = UAIChatPlus_JsonObject::Create();
    Obj1->SetStringField(TEXT("name"), TEXT("John"));

    UAIChatPlus_JsonObject* Obj2 = UAIChatPlus_JsonObject::Create();
    Obj2->SetIntegerField(TEXT("age"), 30)
        ->SetStringField(TEXT("name"), TEXT("Jane"));  // Sobrescribir name

    // Combinar (sobrescribir campos existentes cuando bOverwrite = true)
    Obj1->Merge(Obj2, true);
// Obj1 ahora contiene {"name": "Jane", "age": 30}

// Copia profunda
    UAIChatPlus_JsonObject* Copy = Obj1->Duplicate();
}
```

####Convertir a/desde UStruct

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
// Conversión de UStruct a JsonObject
    FMyData Data;
    Data.Name = TEXT("John");
    Data.Age = 30;

    UAIChatPlus_JsonObject* JsonObj = UAIChatPlus_JsonObject::FromStruct(Data);

    // JsonObject a UStruct
    FMyData OutData;
    bool bSuccess = JsonObj->ToStruct(OutData);

    if (bSuccess)
    {
        UE_LOG(LogTemp, Display, TEXT("Name: %s, Age: %d"), *OutData.Name, OutData.Age);
    }
}
```

###UAIChatPlus_JsonArray - Matriz JSON

####Creación y Operación

```cpp
#include "Common/Json/AIChatPlus_JsonArray.h"

void UMyClass::JsonArrayBasics()
{
// Crear array vacío
    UAIChatPlus_JsonArray* JsonArray = UAIChatPlus_JsonArray::Create();

// Agregar elementos (llamada en cadena)
    JsonArray->AddString(TEXT("apple"))
             ->AddString(TEXT("banana"))
             ->AddInteger(42)
             ->AddBoolean(true)
             ->AddNull();

// agregar elemento de objeto
    UAIChatPlus_JsonObject* ItemObj = UAIChatPlus_JsonObject::Create();
    ItemObj->SetStringField(TEXT("name"), TEXT("sword"));
    JsonArray->AddObject(ItemObj);

    // Añadir matriz anidada
    UAIChatPlus_JsonArray* NestedArray = UAIChatPlus_JsonArray::Create();
    NestedArray->AddInteger(1)->AddInteger(2)->AddInteger(3);
    JsonArray->AddArray(NestedArray);

// salida
    FString Result = JsonArray->ToString(true);
    UE_LOG(LogTemp, Display, TEXT("%s"), *Result);
}
```

####Obtener elemento

```cpp
void UMyClass::GetArrayElements()
{
    FString JsonString = TEXT(R"(["apple", "banana", 42, true, {"name": "item"}])");
    bool bParseSuccess;
    FString ErrorMessage;
    UAIChatPlus_JsonArray* JsonArray = UAIChatPlus_JsonArray::Parse(JsonString, bParseSuccess, ErrorMessage);

    if (!bParseSuccess) return;

    bool bSuccess;

    // obtener elementos de cadena
    FString Fruit = JsonArray->GetString(0, TEXT(""), bSuccess);  // "apple"

    // Obtener elemento entero
    int32 Number = JsonArray->GetInteger(2, 0, bSuccess);  // 42

    // Obtener elemento booleano
    bool bValue = JsonArray->GetBoolean(3, false, bSuccess);  // true

    // Obtener elementos del objeto
    UAIChatPlus_JsonObject* Obj = JsonArray->GetObject(4, bSuccess);
    if (bSuccess && Obj)
    {
        FString Name = Obj->GetStringField(TEXT("name"), TEXT(""), bSuccess);
    }

// recorrer el array
    for (int32 i = 0; i < JsonArray->Length(); ++i)
    {
        EAIChatPlus_JsonValueType Type = JsonArray->GetElementType(i);
        UE_LOG(LogTemp, Display, TEXT("Element[%d] type: %d"), i, static_cast<int32>(Type));
    }
}
```

####Operaciones con arreglos

```cpp
void UMyClass::ArrayOperations()
{
    UAIChatPlus_JsonArray* JsonArray = UAIChatPlus_JsonArray::Create();
    JsonArray->AddString(TEXT("a"))
             ->AddString(TEXT("b"))
             ->AddString(TEXT("c"));

    // Obtener longitud
    int32 Len = JsonArray->Length();  // 3

    // Verificar si el índice es válido
    bool bValid = JsonArray->IsValidIndex(1);  // true

// establecer elementos
    bool bSuccess;
    JsonArray->SetString(1, TEXT("B"), bSuccess);

    // eliminar elemento
    JsonArray->RemoveAt(0, bSuccess);

    // Vaciar el arreglo
    JsonArray->Clear();

// Copia profunda
    UAIChatPlus_JsonArray* Copy = JsonArray->Duplicate();
}
```

####Conversión por lotes

```cpp
void UMyClass::BatchConversion()
{
// Crear desde un arreglo de cadenas
    TArray<FString> StringArray = {TEXT("a"), TEXT("b"), TEXT("c")};
    UAIChatPlus_JsonArray* JsonArray = UAIChatPlus_JsonArray::FromStringArray(StringArray);

// Convertir de nuevo a un arreglo de cadenas
    bool bSuccess;
    TArray<FString> OutArray = JsonArray->ToStringArray(bSuccess);

// crear desde un arreglo de enteros
    TArray<int32> IntArray = {1, 2, 3, 4, 5};
    UAIChatPlus_JsonArray* IntJsonArray = UAIChatPlus_JsonArray::FromIntegerArray(IntArray);

    // Volver a la matriz de números enteros
    TArray<int32> OutIntArray = IntJsonArray->ToIntegerArray(bSuccess);
}
```

###UAIChatPlus_Util - Funciones auxiliares JSON

```cpp
void UMyClass::JsonUtilFunctions()
{
// Combinar dos cadenas JSON
    FString Json1 = TEXT(R"({"name": "John"})");
    FString Json2 = TEXT(R"({"age": 30, "name": "Jane"})");
    FString Merged = UAIChatPlus_Util::MergeJsonObjects(Json1, Json2);
    // Merged = {"name": "Jane", "age": 30}

// Cargar cadena JSON como objeto
    TSharedPtr<FJsonObject> JsonObj = UAIChatPlus_Util::LoadJsonString(Json1);

// Convertir objeto a cadena
    FString JsonString = UAIChatPlus_Util::ToJsonString(JsonObj);
}
```

##Herramientas de imágenes

###Cargar y guardar imágenes

```cpp
#include "Common/AIChatPlus_Util.h"

void UMyClass::ImageLoadSave()
{
// Cargar imagen desde archivo
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath, true);  // true = compilación completada

    if (Texture)
    {
        UE_LOG(LogTemp, Display, TEXT("Image loaded: %dx%d"),
            Texture->GetSizeX(), Texture->GetSizeY());
    }

    // Guardar imagen en archivo
    FString SavePath = FPaths::ProjectSavedDir() / TEXT("output.png");
    bool bSaved = UAIChatPlus_Util::SaveImage(Texture, SavePath);

    if (bSaved)
    {
        UE_LOG(LogTemp, Display, TEXT("Image saved to: %s"), *SavePath);
    }
}
```

###Imagen a Base64

```cpp
void UMyClass::ImageToBase64()
{
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(TEXT("D:/image.png"));

// Convertir a cadena Base64
// InQuality: 0 = PNG, 1-100 = calidad JPEG
FString B64String = UAIChatPlus_Util::ImageToB64(Texture, 0);  // Formato PNG

    UE_LOG(LogTemp, Display, TEXT("Base64 length: %d"), B64String.Len());
}
```

###Copiar imagen

```cpp
void UMyClass::CopyTexture()
{
    UTexture2D* Original = UAIChatPlus_Util::LoadImage(TEXT("D:/image.png"));

// copiar textura
    UTexture2D* Copy = UAIChatPlus_Util::CopyTexture2D(
        Original,
nullptr,        // Exterior (nullptr = GetTransientPackage())
NAME_None,      // Nombre
RF_SinBanderas      // Banderas
    );

    // Versión de Blueprint (con marca predeterminada)
    UTexture2D* BPCopy = UAIChatPlus_Util::CopyTexture2DInBlueprint(Original);
}
```

###Obtener imagen desde URL

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

###Obtener imagen desde Base64

```cpp
void UMyClass::GetImageFromBase64()
{
    FString B64String = TEXT("iVBORw0KGgoAAAANSUhEUg...");  // Datos en Base64

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

###Copiar imagen al portapapeles

```cpp
void UMyClass::CopyToClipboard()
{
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(TEXT("D:/image.png"));

// Comprobar si es compatible
    if (UAIChatPlus_Util::IsCanCopyTexture2DToClipboard())
    {
        UAIChatPlus_Util::CopyTexture2DToClipboard(Texture);
        UE_LOG(LogTemp, Display, TEXT("Image copied to clipboard"));
    }
}
```

##Herramientas de audio

###Cargar archivo WAV

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

###Guardar audio como archivo WAV

```cpp
void UMyClass::SaveWavFile()
{
// Suponiendo que Sound es un USoundWave preexistente
USoundWave* Sonido = /* 获取音频 */;

    FString SavePath = FPaths::ProjectSavedDir() / TEXT("output.wav");
    bool bSaved = UAIChatPlus_Util::SaveSoundWav(Sound, SavePath);

    if (bSaved)
    {
        UE_LOG(LogTemp, Display, TEXT("Sound saved to: %s"), *SavePath);
    }
}
```

###Convertir audio a Base64

```cpp
void UMyClass::SoundToBase64()
{
    USoundWave* Sound = UAIChatPlus_Util::LoadSoundWav(TEXT("D:/audio.wav"));

// Convertir a cadena Base64
    FString B64String = UAIChatPlus_Util::SoundToB64(Sound);

    UE_LOG(LogTemp, Display, TEXT("Audio Base64 length: %d"), B64String.Len());
}
```

###Datos WAV a SoundWave

```cpp
void UMyClass::WavDataToSound()
{
    // Leer datos originales desde un archivo
    TArray<uint8> RawData;
    FFileHelper::LoadFileToArray(RawData, TEXT("D:/audio.wav"));

// Convertir a SoundWave
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

###Copiar SoundWave

```cpp
void UMyClass::CopySoundWave()
{
    USoundWave* Original = UAIChatPlus_Util::LoadSoundWav(TEXT("D:/audio.wav"));

    // Copiar audio
    USoundWave* Copy = UAIChatPlus_Util::CopySoundWave(
        Original,
        nullptr,    // Outer
        NOMBRE_Ninguno   // Nombre
    );
}
```

###Obtener los datos PCM originales

```cpp
void UMyClass::GetPCMData()
{
    USoundWave* Sound = UAIChatPlus_Util::LoadSoundWav(TEXT("D:/audio.wav"));

    // Obtener los datos PCM originales
    TArray<uint8> PCMData = UAIChatPlus_Util::GetSoundWavePCMData(Sound);

    UE_LOG(LogTemp, Display, TEXT("PCM data size: %d bytes"), PCMData.Num());
}
```

###Crear SoundWave a partir de datos de grabación

```cpp
void UMyClass::RecorderDataToSound()
{
// Suponiendo los datos de grabación obtenidos desde Audio Capture
TArray<float> DatosDeGrabacion;  // Datos de muestreo de audio
    int32 NumChannels = 1;       // Mono
int32 SampleRate = 16000;    // Frecuencia de muestreo

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

##Control de registros

```cpp
void UMyClass::ControlLogging()
{
// Establecer el nivel de registro interno
    UAIChatPlus_Util::SetInternalLogVerbosity(EAIChatPlus_LogVerbosityType::Verbose);

// Niveles disponibles:
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

##Funciones auxiliares del envoltorio de respuesta

Al manejar la respuesta en la devolución de llamada, es necesario convertir `FAIChatPlus_PointerWrapper` al tipo específico:

```cpp
void UMyClass::HandleCallbackResponse()
{
    // En la devolución de llamada OnFinished
    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
// Obtener el mensaje de respuesta
        FString Message = UAIChatPlus_Util::GetResponseWrapperMessage(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Message: %s"), *Message);

// o convertir al tipo de respuesta básico
        FAIChatPlus_ChatResponseBodyBase& Response = UAIChatPlus_Util::CastWrapperToResponse(ResponseWrapper);
    });

    // En la devolución de llamada OnFailed
    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
// Obtener la descripción del error
        FString ErrorDesc = UAIChatPlus_Util::GetErrorWrapperDescription(ErrorWrapper);
        UE_LOG(LogTemp, Error, TEXT("Error: %s"), *ErrorDesc);

        // o convertir al tipo de error
        FAIChatPlus_ResponseErrorBase& Error = UAIChatPlus_Util::CastWrapperToError(ErrorWrapper);
    });
}
```

##Consulta de información del modelo

```cpp
void UMyClass::QueryModelInfo()
{
// obtener la lista de modelos predeterminados de OpenAI
    const TArray<FName>& OpenAIModels = UAIChatPlus_Util::GetOpenAIChatDefaultModels();

    // Obtener información de un modelo específico
    FAIChatPlus_ChatModelInfo ModelInfo = UAIChatPlus_Util::GetOpenAIChatModelInfo(TEXT("gpt-4o"));
    UE_LOG(LogTemp, Display, TEXT("Model: %s, MaxTokens: %d, SupportImage: %s"),
        *ModelInfo.Name.ToString(),
        ModelInfo.MaxTokens,
        ModelInfo.IsSupportSendImage ? TEXT("Yes") : TEXT("No"));

// Modelo Claude
    const TArray<FName>& ClaudeModels = UAIChatPlus_Util::GetClaudeChatDefaultModels();
    FAIChatPlus_ChatModelInfo ClaudeInfo = UAIChatPlus_Util::GetClaudeChatModelInfo(TEXT("claude-3-5-sonnet"));

// Modelo Gemini
    const TArray<FName>& GeminiModels = UAIChatPlus_Util::GetGeminiChatDefaultModels();
    FAIChatPlus_ChatModelInfo GeminiInfo = UAIChatPlus_Util::GetGeminiChatModelInfo(TEXT("gemini-1.5-pro"));
}
```

##Funciones auxiliares de Cllama

```cpp
void UMyClass::CllamaUtilities()
{
// Comprobar si Cllama está disponible
    if (UAIChatPlus_Util::Cllama_IsValid())
    {
        UE_LOG(LogTemp, Display, TEXT("Cllama is available"));
    }

// Comprobar compatibilidad de GPU
    if (UAIChatPlus_Util::Cllama_IsSupportGpu())
    {
        UE_LOG(LogTemp, Display, TEXT("GPU acceleration supported"));
    }

// Obtener los backends compatibles
    TArray<FString> Backends = UAIChatPlus_Util::Cllama_GetSupportBackends();
    for (const FString& Backend : Backends)
    {
        UE_LOG(LogTemp, Display, TEXT("Backend: %s"), *Backend);
    }

    // Preparar las rutas de los modelos en Pak
    FString ModelPath = TEXT("Models/my_model.gguf");
    FString ActualPath = UAIChatPlus_Util::Cllama_PrepareModelPathFromPak(ModelPath);
    // Si el modelo está en un Pak, se descomprimirá en un directorio temporal y devolverá la nueva ruta
}
```

##Funciones auxiliares de archivos

```cpp
void UMyClass::FileUtilities()
{
    // Obtener el directorio base del complemento
    FString PluginDir = UAIChatPlus_Util::GetPluginBaseDir(TEXT("AIChatPlus"));
    UE_LOG(LogTemp, Display, TEXT("Plugin dir: %s"), *PluginDir);

    // Copiar directorio
    FString SourceDir = FPaths::ProjectContentDir() / TEXT("Source");
    FString DestDir = FPaths::ProjectSavedDir() / TEXT("Backup");
bool bCopied = UAIChatPlus_Util::CopiarDirectorio(DirectorioOrigen, DirectorioDestino, true);  // true = sobrescribir
}
```

##Prompt plantilla

```cpp
void UMyClass::PromptTemplates()
{
    // Obtener lista de archivos JSON de plantillas de Prompt
    TArray<FDirectoryPath> ExtraDirs;  // Directorios de búsqueda adicionales (opcional)
    TArray<FFilePath> TemplateFiles = UAIChatPlus_Util::GetPromptTemplateJsonFiles(ExtraDirs);

// Cargar plantilla de Prompt
    TArray<FAIChatPlus_PromptTemplate> Templates = UAIChatPlus_Util::GetPromptTemplates(TemplateFiles);

    for (const FAIChatPlus_PromptTemplate& Template : Templates)
    {
        UE_LOG(LogTemp, Display, TEXT("Template: %s"), *Template.Name);
    }
}
```

--8<-- "footer_es.md"


> Este post está traducido con ChatGPT; si tienes comentarios, por favor [**envía tus comentarios**](https://github.com/disenone/wiki_blog/issues/new)Señalar cualquier omisión en el texto. 
