---
layout: post
title: Ollama
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
- Ollama
- Local LLM
description: Ollama
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Ollama" />

#C++ Capítulo - Ollama

Este documento explica cómo utilizar la API local de Ollama en C++ para conversar, analizar imágenes y realizar llamadas a herramientas.

Ollama es una herramienta para ejecutar modelos de lenguaje grandes localmente, con la dirección predeterminada `http://localhost:11434`.

##Preparativos

Antes de usar, asegúrese de que:

1. **Instala y ejecuta Ollama**: Desde [ollama.com](https://ollama.com)Descarga e instala Ollama, luego descarga el modelo necesario (como `ollama pull llama3.2`).

2. En el archivo `.Build.cs` del proyecto, añade las dependencias del módulo:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

3. Incluir los archivos de encabezado necesarios:

```cpp
#include "Common_Ollama/AIChatPlus_OllamaChatRequest.h"
```

##Chat de texto

###Chat básico de texto

```cpp
#include "Common_Ollama/AIChatPlus_OllamaChatRequest.h"

void UMyClass::SendOllamaChatRequest()
{
// Configurar Opciones
    FAIChatPlus_OllamaChatRequestOptions Options;
Opciones.Modelo = TEXTO("llama3.2");  // Utiliza el modelo descargado
Opciones.BaseUrl = TEXT("http://localhost:11434");  // Dirección por defecto
Opciones.bStream = verdadero;  // Habilitar salida en flujo
    Options.Temperature = 0.8f;

// Ollama no necesita una clave API (servicio local)

// Crear mensaje (incluye mensaje del Sistema)
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is 2+2?"), EAIChatPlus_ChatRole::User});

// crear solicitud
    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// enlazar devolución de llamada
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Ollama: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Token Usage: %s"), *Response.Usage.GetDescription());
        UE_LOG(LogTemp, Display, TEXT("Done Reason: %s"), *Response.DoneReason);
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_ResponseErrorBase>();
        UE_LOG(LogTemp, Error, TEXT("Request Failed: %s"), *Error.GetDescription());
    });

    // Enviar solicitud
    Request->SendRequest();
}
```

###Diálogo multironda

```cpp
void UMyClass::MultiTurnOllamaChat()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

// Construir historial de diálogo multironda
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("My name is Charlie."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("Hello Charlie! Nice to meet you."), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my name?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###Utilizar la API Generate (modo no Chat)

```cpp
void UMyClass::UseOllamaGenerateAPI()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;
Opciones.EsChat = falso;  // Utilizar /api/generar en lugar de /api/chat
Opciones.Sistema = TEXTO("Eres un asistente útil.");  // Solo tiene efecto en modo no Chat

    // El modo No Chat solo necesita un mensaje del usuario
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Write a haiku about programming."), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Generated: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##Visión (análisis de imágenes)

Los modelos de Ollama compatibles con Vision (como `llava`, `llama3.2-vision`) pueden analizar el contenido de las imágenes.

###Cargar y analizar imágenes desde un archivo

```cpp
#include "Common_Ollama/AIChatPlus_OllamaChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithOllama()
{
// Cargar imagen desde archivo
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image: %s"), *ImagePath);
        return;
    }

// Crear el objeto Texture disponible para el plugin
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

// Configurar Opciones
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2-vision");  // Usa un modelo que soporte Vision
    Options.bStream = true;

// Crear un mensaje con imagen
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("What do you see in this image?");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Ollama Vision: %s"), *Message);
    });

    Request->SendRequest();
}
```

##Llamada de Herramientas (invocación de funciones)

Algunos modelos de Ollama admiten la función Tool Calling.

###Definir herramientas y enviar solicitud

```cpp
void UMyClass::SendOllamaToolCallRequest()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXTO("llama3.2");  // Asegúrate de que el modelo soporte Tool Calling
    Options.bStream = true;

    // Definir herramienta: obtener el clima
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");

// Definir parámetros de la herramienta
    FAIChatPlus_ChatRequestToolProperty LocationProp;
    LocationProp.Name = TEXT("location");
    LocationProp.Description = TEXT("The city name, e.g. Tokyo, Paris");
    LocationProp.Type = TEXT("string");
    LocationProp.Required = true;

    WeatherTool.Properties.Add(LocationProp);
    Options.Tools.Add(WeatherTool);

    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What's the weather in London?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
            for (const auto& ToolCall : ToolCalls)
            {
                UE_LOG(LogTemp, Display, TEXT("Tool Call - ID: %s, Function: %s, Args: %s"),
                    *ToolCall.Id, *ToolCall.FunctionName, *ToolCall.FunctionArguments);
            }
        }
        else
        {
            UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
        }
    });

    Request->SendRequest();
}
```

###Procesar Resultados de la Llamada de Herramientas

```cpp
void UMyClass::HandleOllamaToolCallResult()
{
    FString ToolCallId = TEXT("call_123");
    FString FunctionName = TEXT("get_weather");
    FString FunctionResult = TEXT("{\"temperature\": 15, \"unit\": \"celsius\", \"description\": \"Rainy\"}");

    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

// Redefinir herramientas
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");
    Options.Tools.Add(WeatherTool);

// Construir historial de mensajes
    TArray<FAIChatPlus_ChatRequestMessage> Messages;

// 1. Mensajes del Sistema
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});

// 2. Problema original del usuario
    Messages.Add({TEXT("What's the weather in London?"), EAIChatPlus_ChatRole::User});

// 3. Solicitud de Tool Call del Asistente
    FAIChatPlus_ChatRequestMessage AssistantMessage;
    AssistantMessage.Role = EAIChatPlus_ChatRole::Assistant;
    AssistantMessage.Content = TEXT("");

    FAIChatPlus_ChatRequestToolCall ToolCallUse;
    ToolCallUse.Id = ToolCallId;
    ToolCallUse.Type = TEXT("function");
    ToolCallUse.FunctionName = FunctionName;
    ToolCallUse.FunctionArguments = TEXT("{\"location\": \"London\"}");
    AssistantMessage.ToolCallUses.Add(ToolCallUse);
    Messages.Add(AssistantMessage);

// 4. Resultado de ejecución de la herramienta
    FAIChatPlus_ChatRequestMessage ToolResultMessage;
    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;

    FAIChatPlus_ChatRequestToolCallResult ToolResult;
    ToolResult.Id = ToolCallId;
    ToolResult.FunctionName = FunctionName;
    ToolResult.FunctionResult = FunctionResult;
    ToolResultMessage.ToolCallResults.Add(ToolResult);
    Messages.Add(ToolResultMessage);

// enviar solicitud
    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###Ciclo completo de Tool Call

```cpp
// Almacenar historial de conversación
TArray<FAIChatPlus_ChatRequestMessage> OllamaConversation;
FAIChatPlus_OllamaChatRequestOptions OllamaOptions;

void UMyClass::InitializeOllamaToolChat()
{
    OllamaOptions.Model = TEXT("llama3.2");
    OllamaOptions.bStream = true;

// definir herramientas
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get weather for a location.");

    FAIChatPlus_ChatRequestToolProperty Prop;
    Prop.Name = TEXT("location");
    Prop.Type = TEXT("string");
    Prop.Required = true;
    WeatherTool.Properties.Add(Prop);

    OllamaOptions.Tools.Add(WeatherTool);

// Inicializar el diálogo (añadir mensaje del Sistema)
    OllamaConversation.Empty();
    OllamaConversation.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}

void UMyClass::SendOllamaUserMessage(const FString& UserMessage)
{
    OllamaConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(OllamaOptions, OllamaConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
            ProcessOllamaToolCalls(ToolCalls, Response.GetMessage());
        }
        else
        {
            FString AssistantMessage = Response.GetMessage();
            OllamaConversation.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});
            OnOllamaResponse(AssistantMessage);
        }
    });

    Request->SendRequest();
}

void UMyClass::ProcessOllamaToolCalls(const TArray<FAIChatPlus_ChatResponseToolCall>& ToolCalls, const FString& AssistantContent)
{
// Agregar mensaje de Tool Call del Assistant
    FAIChatPlus_ChatRequestMessage AssistantMsg;
    AssistantMsg.Role = EAIChatPlus_ChatRole::Assistant;
    AssistantMsg.Content = AssistantContent;

    for (const auto& ToolCall : ToolCalls)
    {
        FAIChatPlus_ChatRequestToolCall Use;
        Use.Id = ToolCall.Id;
        Use.Type = ToolCall.Type;
        Use.FunctionName = ToolCall.FunctionName;
        Use.FunctionArguments = ToolCall.FunctionArguments;
        AssistantMsg.ToolCallUses.Add(Use);
    }
    OllamaConversation.Add(AssistantMsg);

// Ejecutar herramienta y añadir resultado
    FAIChatPlus_ChatRequestMessage ToolResultMsg;
    ToolResultMsg.Role = EAIChatPlus_ChatRole::Tool;

    for (const auto& ToolCall : ToolCalls)
    {
        FString Result = ExecuteOllamaTool(ToolCall.FunctionName, ToolCall.FunctionArguments);

        FAIChatPlus_ChatRequestToolCallResult ToolResult;
        ToolResult.Id = ToolCall.Id;
        ToolResult.FunctionName = ToolCall.FunctionName;
        ToolResult.FunctionResult = Result;
        ToolResultMsg.ToolCallResults.Add(ToolResult);
    }
    OllamaConversation.Add(ToolResultMsg);

// Continuar la conversación
    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(OllamaOptions, OllamaConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
            ProcessOllamaToolCalls(ToolCalls, Response.GetMessage());
        }
        else
        {
            FString FinalMessage = Response.GetMessage();
            OllamaConversation.Add({FinalMessage, EAIChatPlus_ChatRole::Assistant});
            OnOllamaResponse(FinalMessage);
        }
    });

    Request->SendRequest();
}

FString UMyClass::ExecuteOllamaTool(const FString& FunctionName, const FString& Arguments)
{
    if (FunctionName == TEXT("get_weather"))
    {
        return TEXT("{\"temperature\": 15, \"unit\": \"celsius\", \"description\": \"Rainy\"}");
    }
    return TEXT("{\"error\": \"Unknown tool\"}");
}

void UMyClass::OnOllamaResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Ollama: %s"), *Response);
}
```

##Obtener lista de modelos

Usar `UAIChatPlus_OllamaModelRequest` permite obtener la lista de modelos disponibles en el servidor Ollama.

```cpp
#include "Common_Ollama/AIChatPlus_OllamaModelRequest.h"

void UMyClass::GetOllamaModels()
{
    FAIChatPlus_OllamaModelRequestOptions Options;
Opciones.BaseUrl = TEXT("http://localhost:11434");  // Dirección por defecto

    auto Request = UAIChatPlus_OllamaModelRequest::CreateWithOptions(Options);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaModelRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FString> ModelNames = Response.GetModelNames();
        for (const FString& ModelName : ModelNames)
        {
            UE_LOG(LogTemp, Display, TEXT("Available Model: %s"), *ModelName);
        }

// obtener detalles
        for (const auto& Model : Response.Models)
        {
            UE_LOG(LogTemp, Display, TEXT("Model: %s, Size: %lld, Family: %s"),
                *Model.Name, Model.Size, *Model.Details.Family);
        }
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_ResponseErrorBase>();
        UE_LOG(LogTemp, Error, TEXT("Failed to get models: %s"), *Error.GetDescription());
    });

    Request->SendRequest();
}
```

##Configuración avanzada

###Parámetros exclusivos de Ollama

```cpp
void UMyClass::ConfigureOllamaAdvanced()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

    // Parámetros de muestreo
    Options.Temperature = 0.7f;
Opciones.TopK = 40;           // Muestreo Top-K
    Options.TopP = 0.9f;         // Muestreo de núcleo
Opciones.MinP = 0.05f;        // Muestreo Min-P

    // Muestreo Mirostat (para controlar la perplejidad)
Opciones.Mirostat = 2;        // 0=desactivado, 1=Mirostat, 2=Mirostat 2.0
    Options.MirostatEta = 0.1f;
    Options.MirostatTau = 5.0f;

// Contexto y limitaciones de generación
Opciones.NumCtx = 4096;       // Tamaño de la ventana de contexto
Opciones.NumPredicción = 256;    // Número máximo de tokens generados

    // Castigo por repetición
    Options.RepeatLastN = 64;
    Options.RepeatPenalty = 1.1f;

    // detener secuencia
    Options.StopSequences.Add(TEXT("\n\n"));

// Tiempo de carga persistente del modelo
Opciones.MantenerVivo = 300;     // segundos

    // Semilla aleatoria (para generación reproducible)
    Options.Seed = 42;

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###Usar clave de API (Ollama remoto)

```cpp
void UMyClass::ConnectToRemoteOllama()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.BaseUrl = TEXT("https://your-ollama-server.com");
Opciones.ApiKey = TEXT("tu-clave-de-api"); // Si el servidor requiere autenticación
    Options.bStream = true;

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello from remote!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###Usar opciones de extensión JSON

```cpp
void UMyClass::UseOllamaExtraOptions()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

// Añadir opciones JSON adicionales
    Options.ExtraJsonString = TEXT("{\"format\": \"json\"}");

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Return a JSON with name and age fields."), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

##Manejo de errores

```cpp
void UMyClass::RobustOllamaRequest()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->OnStartedListeners.AddLambda([]()
    {
        UE_LOG(LogTemp, Display, TEXT("Ollama request started..."));
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.HasError())
        {
            UE_LOG(LogTemp, Error, TEXT("Response error: %s"), *Response.Error.GetDescription());
            return;
        }

        UE_LOG(LogTemp, Display, TEXT("Success: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Done Reason: %s"), *Response.DoneReason);
        UE_LOG(LogTemp, Display, TEXT("Tokens: %s"), *Response.Usage.GetDescription());

// Métricas de rendimiento específicas de Ollama
        UE_LOG(LogTemp, Display, TEXT("Total Duration: %lld ns"), Response.TotalDuration);
        UE_LOG(LogTemp, Display, TEXT("Load Duration: %lld ns"), Response.LoadDuration);
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

##Detener solicitud

```cpp
UPROPERTY()
UAIChatPlus_OllamaChatRequest* CurrentOllamaRequest = nullptr;

void UMyClass::StartOllamaRequest()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

    CurrentOllamaRequest = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a very long story."), EAIChatPlus_ChatRole::User}});

    CurrentOllamaRequest->SendRequest();
}

void UMyClass::CancelOllamaRequest()
{
    if (CurrentOllamaRequest && CurrentOllamaRequest->IsActivated())
    {
        CurrentOllamaRequest->StopRequest();
        UE_LOG(LogTemp, Display, TEXT("Ollama request cancelled"));
    }
}
```

--8<-- "footer_es.md"


> Esta publicación está traducida utilizando ChatGPT, por favor proporciona tus comentarios en [**retroalimentación**](https://github.com/disenone/wiki_blog/issues/new)Señalar cualquier omisión en lo mencionado. 
