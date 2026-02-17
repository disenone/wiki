---
layout: post
title: Cllama (obsoleto)
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

#C++ Capítulo - Cllama (obsoleto)

##Obsoleto

Cllama ha sido marcado como **obsoleto** y ya no se mantiene.

Las funciones originales de Cllama fueron proporcionadas por [CllamaServer](ue-插件-AIChatPlus-Usage-Source-CllamaServer.md)para soportar.

##Modelo sin conexión

Este documento explica cómo utilizar Cllama (integrando llama.cpp) para inferencia local sin conexión en C++.

Cllama permite ejecutar modelos de lenguaje grandes sin necesidad de conexión a Internet, lo que lo hace ideal para escenarios que requieren inferencia fuera de línea o protección de la privacidad.

##Preparativos

Antes de usar, asegúrese de que:

1. **Descargar archivos del modelo GGUF**: Desde [Hugging Face](https://huggingface.co)Descargar el archivo de modelo en formato GGUF compatible.

2. En el archivo `.Build.cs` del proyecto, añade las dependencias del módulo:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

3. Incluir los archivos de cabecera necesarios:

```cpp
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"
```

##Verificar disponibilidad de Cllama

Antes de usar, puedes verificar si Cllama está disponible y los backends compatibles:

```cpp
#include "Common/AIChatPlus_Util.h"

void UMyClass::CheckCllamaSupport()
{
    // Verificar si Cllama está disponible
    if (UAIChatPlus_Util::Cllama_IsValid())
    {
        UE_LOG(LogTemp, Display, TEXT("Cllama is available"));

// Verificar si hay soporte para GPU
        if (UAIChatPlus_Util::Cllama_IsSupportGpu())
        {
            UE_LOG(LogTemp, Display, TEXT("GPU acceleration is supported"));
        }

// Obtener la lista de backends admitidos
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

##Chat de texto

###Chat básico de texto

```cpp
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"

void UMyClass::SendCllamaChatRequest()
{
// Configurar Opciones
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
Opciones.bStream = verdadero;  // Activar salida en flujo
    Options.Temperature = 0.8f;
Opciones.NumCapasGpu = 99; // Número de capas aceleradas por GPU (0 = solo CPU)

// crear mensaje
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is the meaning of life?"), EAIChatPlus_ChatRole::User});

// Crear solicitud
    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    // Vincular devolución de llamada
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

// enviar solicitud
    Request->SendRequest();
}
```

###Usar rutas relativas (relativas al directorio Content)

```cpp
void UMyClass::UseRelativeModelPath()
{
    FAIChatPlus_CllamaChatRequestOptions Options;

    // Ruta relativa al directorio Content del proyecto
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

###Cargar modelo desde archivo Pak

```cpp
void UMyClass::LoadModelFromPak()
{
// Si los modelos están empaquetados en archivos Pak, primero es necesario preparar la ruta del modelo
    FString ModelPath = TEXT("Models/my_model.gguf");

// Esta función extraerá los modelos del Pak al directorio temporal y devolverá la ruta real
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

###Diálogo Multiturno

```cpp
void UMyClass::MultiTurnCllamaChat()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;

// Construir historial de conversación en múltiples turnos
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

###El modelo sigue cargando.

```cpp
void UMyClass::KeepModelLoaded()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;

    // KeepAlive controla cuánto tiempo permanece cargado el modelo después de una solicitud
// 0 = Descargar inmediatamente después de la solicitud
// -1 = mantener permanentemente cargado
    // >0 = mantener cargando durante los segundos especificados
    Options.KeepAlive = -1;  // Mantener cargado permanentemente

    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Hello!"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);
    Request->SendRequest();
}
```

##Visión (Análisis de imágenes)

Cllama admite la función Vision, requiere el uso de un modelo multimodal (como LLaVA) y debe proporcionar el archivo del modelo MMProject.

> **Nota**: Cllama Vision admite un máximo de 1 imagen (`FAIChatPlus_Constants::FCllama::MaxSendImageNum = 1`).

###Cargar y analizar imagen desde archivo

```cpp
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithCllama()
{
// Cargar la imagen desde el archivo
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image: %s"), *ImagePath);
        return;
    }

    // Crear un objeto Texture disponible para el complemento
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

    // Opciones de Configuración
    FAIChatPlus_CllamaChatRequestOptions Options;

// El modelo LLaVA requiere dos archivos: el modelo principal y el modelo MMProyecto
    Options.ModelPath.FilePath = TEXT("D:/Models/llava-v1.6-mistral-7b.Q4_K_M.gguf");
    Options.MMProjectModelPath.FilePath = TEXT("D:/Models/mmproj-llava-v1.6-mistral-7b-f16.gguf");

    Options.bStream = true;
    Options.NumGpuLayers = 99;
    Options.MMProjectUseGpu = true;  // El modelo MMProject también utiliza GPU

    // Crear un mensaje con imagen
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("What do you see in this image?");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
ImageMessage.Images.Add(ChatTexture);  // Solo se puede añadir 1 imagen

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

###Analizar imágenes desde Texture2D

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

##Configuración avanzada

###Configuración de parámetros de muestreo

```cpp
void UMyClass::ConfigureCllamaSampling()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;

// Aceleración por GPU
Opciones.NumCapasGpu = 99;  // Cuantas más capas en GPU, mejor

// Parámetros de muestreo
Opciones.Temperatura = 0.7f;  // Temperatura
Opciones.TopK = 40;           // Muestreo Top-K
Opciones.TopP = 0.95f;        // Muestreo de núcleo
    Options.MinP = 0.05f;        // Muestreo Min-P

// Muestreo Mirostat (utilizado para controlar la perplejidad)
Opciones.Mirostat = 2;        // 0=desactivado, 1=Mirostat, 2=Mirostat 2.0
    Options.MirostatEta = 0.1f;
    Options.MirostatTau = 5.0f;

// Contexto y restricciones generativas
Opciones.NumCtx = 4096;       // Tamaño de la ventana de contexto
Opciones.NumPredicciones = 256;    // Número máximo de tokens generados (-1 = ilimitado)

    // Penalización por repetición
Opciones.RepetirUltimosN = 64;    // Verificar repetidos en los últimos N tokens
    Options.RepeatPenalty = 1.1f;

// Muestreo libre en cola
Opciones.TfsZ = 1.0f;         // 1.0 = deshabilitado

    // Detener secuencia
    Options.StopSequences.Add(TEXT("\n\n"));
    Options.StopSequences.Add(TEXT("User:"));

    // Semilla aleatoria (para generación reproducible)
    Options.Seed = 42;

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a short poem."), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###Usar plantilla personalizada

```cpp
void UMyClass::UseCustomTemplate()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/my_model.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;

// Plantilla de prompt personalizada (sobrescribe la plantilla incorporada del modelo)
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

##Manejo de errores

```cpp
void UMyClass::RobustCllamaRequest()
{
// Primero verificar si Cllama está disponible
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

// Indicadores de rendimiento
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

##Solicitud de detención

```cpp
UPROPERTY()
UAIChatPlus_CllamaChatRequest* CurrentCllamaRequest = nullptr;

void UMyClass::StartCllamaRequest()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;
Opciones.NumPredecir = -1;  // Generación infinita

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

##Ejemplo completo de gestión de diálogos

```cpp
// Variables miembro
TArray<FAIChatPlus_ChatRequestMessage> CllamaConversation;
FAIChatPlus_CllamaChatRequestOptions CllamaOptions;

void UMyClass::InitializeCllamaChat()
{
    CllamaOptions.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    CllamaOptions.bStream = true;
    CllamaOptions.NumGpuLayers = 99;
    CllamaOptions.KeepAlive = -1;  // Mantener el modelo cargado

// inicializar el diálogo
    CllamaConversation.Empty();
    CllamaConversation.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}

void UMyClass::SendCllamaUserMessage(const FString& UserMessage)
{
    CllamaConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(CllamaOptions, CllamaConversation);

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        // Mostrar el contenido generado en tiempo real
        UE_LOG(LogTemp, Display, TEXT("Generating: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);

        // Agregar la respuesta del Assistant al historial de conversación
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

--8<-- "footer_es.md"


> Esta publicación está traducida usando ChatGPT, por favor déjanos tu [**retroalimentación**](https://github.com/disenone/wiki_blog/issues/new)Señalar cualquier omisión. 
