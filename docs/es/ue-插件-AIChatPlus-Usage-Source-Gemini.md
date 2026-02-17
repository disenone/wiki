---
layout: post
title: Gemini
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
- Gemini
- Google
description: Gemini
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Gemini" />

#C++ Capítulo - Gemini

Este documento explica cómo utilizar la API de Google Gemini en C++ para chat, análisis de imágenes y Tool Calling.

##Preparativos

Antes de usar, asegúrese de que:

1. Agregue dependencias de módulos en el archivo `.Build.cs` del proyecto:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

2. Incluir los archivos de cabecera necesarios:

```cpp
#include "Common_Gemini/AIChatPlus_GeminiChatRequest.h"
```

##Chat de texto

###Chat de texto básico

```cpp
#include "Common_Gemini/AIChatPlus_GeminiChatRequest.h"

void UMyClass::SendGeminiChatRequest()
{
// Configurar Opciones
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-google-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
Opciones.bStream = true;  // Habilitar salida en flujo continuo
    Options.MaxOutputTokens = 1024;
    Options.Temperature = 0.7f;

// El System Prompt de Gemini se establece mediante Options.System
    Options.System = TEXT("You are a helpful assistant.");

// Crear mensaje del usuario
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("What is the capital of Japan?"), EAIChatPlus_ChatRole::User});

// Crear solicitud
    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// enlazar callback
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Gemini: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);
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

###Diálogo Multiturno

```cpp
void UMyClass::MultiTurnGeminiChat()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant with a good memory.");

// Construir el historial de diálogo multiturno
    // Gemini utiliza los roles de "user" y "model"
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("My name is Alice."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("Hello Alice! Nice to meet you. How can I help you today?"), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my name?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);
// El modelo debe recordar que el nombre de usuario es Alice
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##Visión (análisis de imágenes)

El modelo Gemini admite la función Vision, capaz de analizar el contenido de las imágenes.

> **Nota**: Gemini Vision admite un máximo de 20 imágenes (`FAIChatPlus_Constants::FGemini::MaxSendImageNum = 20`).

###Cargar imagen desde archivo y analizar

```cpp
#include "Common_Gemini/AIChatPlus_GeminiChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithGemini()
{
    // Cargar imagen desde archivo
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image: %s"), *ImagePath);
        return;
    }

    // Crear objeto Texture disponible para el plugin
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

// Opciones de configuración
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
Opciones.Modelo = TEXTO("gemini-1.5-flash"); // o gemini-1.5-pro
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant that can analyze images.");

// Crear un mensaje con imágenes
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("Please describe this image in detail.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Gemini Vision: %s"), *Message);
    });

    Request->SendRequest();
}
```

###Análisis de múltiples imágenes

```cpp
void UMyClass::AnalyzeMultipleImagesWithGemini()
{
// Cargar múltiples imágenes
    TArray<UAIChatPlus_Texture*> ChatTextures;

    TArray<FString> ImagePaths = {
        FPaths::ProjectContentDir() / TEXT("Images/before.png"),
        FPaths::ProjectContentDir() / TEXT("Images/after.png")
    };

    for (const FString& Path : ImagePaths)
    {
        if (UTexture2D* Texture = UAIChatPlus_Util::LoadImage(Path))
        {
            ChatTextures.Add(UAIChatPlus_Texture::CreateFromTexture2D(Texture));
        }
    }

    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;

// Crear un mensaje con múltiples imágenes
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("Compare these two images and describe the differences.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images = ChatTextures;

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Comparison: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##Llamada de Herramientas (invocación de funciones)

Gemini admite la llamada a herramientas (Function Calling), lo que permite al modelo invocar funciones predefinidas.

###Definir herramienta y enviar solicitud

```cpp
void UMyClass::SendGeminiToolCallRequest()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant. Use tools when needed.");

// Define herramienta: obtener clima
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");

// definir los parámetros de la herramienta
    FAIChatPlus_ChatRequestToolProperty LocationProp;
    LocationProp.Name = TEXT("location");
    LocationProp.Description = TEXT("The city name, e.g. Tokyo, Paris, New York");
    LocationProp.Type = TEXT("string");
    LocationProp.Required = true;

    FAIChatPlus_ChatRequestToolProperty UnitProp;
    UnitProp.Name = TEXT("unit");
    UnitProp.Description = TEXT("The temperature unit: celsius or fahrenheit");
    UnitProp.Type = TEXT("string");
    UnitProp.Required = false;

    WeatherTool.Properties.Add(LocationProp);
    WeatherTool.Properties.Add(UnitProp);

    Options.Tools.Add(WeatherTool);

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("What's the weather like in Tokyo?"), EAIChatPlus_ChatRole::User}});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);

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

###Procesando Resultados de la Llamada a Herramienta

```cpp
void UMyClass::HandleGeminiToolCallResult()
{
    // Supongamos que esta es la información de Tool Call devuelta por el modelo
    FString ToolCallId = TEXT("call_abc123");
    FString FunctionName = TEXT("get_weather");
    FString FunctionResult = TEXT("{\"temperature\": 25, \"unit\": \"celsius\", \"description\": \"Sunny\"}");

    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;

// Redefinir las herramientas
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");
    Options.Tools.Add(WeatherTool);

// Construir el historial de mensajes
    TArray<FAIChatPlus_ChatRequestMessage> Messages;

    // 1. Pregunta original del usuario
    Messages.Add({TEXT("What's the weather like in Tokyo?"), EAIChatPlus_ChatRole::User});

// 2. Solicitud de Tool Call del Asistente
    FAIChatPlus_ChatRequestMessage AssistantMessage;
    AssistantMessage.Role = EAIChatPlus_ChatRole::Assistant;
    AssistantMessage.Content = TEXT("");

    FAIChatPlus_ChatRequestToolCall ToolCallUse;
    ToolCallUse.Id = ToolCallId;
    ToolCallUse.Type = TEXT("function");
    ToolCallUse.FunctionName = FunctionName;
    ToolCallUse.FunctionArguments = TEXT("{\"location\": \"Tokyo\"}");
    AssistantMessage.ToolCallUses.Add(ToolCallUse);
    Messages.Add(AssistantMessage);

    // 3. Resultado de ejecución de la herramienta
    FAIChatPlus_ChatRequestMessage ToolResultMessage;
    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;

    FAIChatPlus_ChatRequestToolCallResult ToolResult;
    ToolResult.Id = ToolCallId;
    ToolResult.FunctionName = FunctionName;
    ToolResult.FunctionResult = FunctionResult;
    ToolResultMessage.ToolCallResults.Add(ToolResult);
    Messages.Add(ToolResultMessage);

// Enviar solicitud
    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###Ciclo completo de Tool Call

```cpp
// Almacenar historial de conversaciones
TArray<FAIChatPlus_ChatRequestMessage> GeminiConversation;
FAIChatPlus_GeminiChatRequestOptions GeminiOptions;

void UMyClass::InitializeGeminiToolChat()
{
    GeminiOptions.ApiKey = TEXT("your-api-key");
    GeminiOptions.Model = TEXT("gemini-1.5-flash");
    GeminiOptions.bStream = true;
    GeminiOptions.System = TEXT("You are a helpful assistant. Use tools when needed.");

    // Definir herramienta
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get weather for a location.");

    FAIChatPlus_ChatRequestToolProperty Prop;
    Prop.Name = TEXT("location");
    Prop.Type = TEXT("string");
    Prop.Required = true;
    WeatherTool.Properties.Add(Prop);

    GeminiOptions.Tools.Add(WeatherTool);

// Borrar historial de conversación
    GeminiConversation.Empty();
}

void UMyClass::SendGeminiUserMessage(const FString& UserMessage)
{
    GeminiConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(GeminiOptions, GeminiConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
            ProcessGeminiToolCalls(ToolCalls, Response.GetMessage());
        }
        else
        {
            FString AssistantMessage = Response.GetMessage();
            GeminiConversation.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});
            OnGeminiResponse(AssistantMessage);
        }
    });

    Request->SendRequest();
}

void UMyClass::ProcessGeminiToolCalls(const TArray<FAIChatPlus_ChatResponseToolCall>& ToolCalls, const FString& AssistantContent)
{
// Añadir mensaje de llamada de herramienta de Assistant
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
    GeminiConversation.Add(AssistantMsg);

// Ejecutar herramienta y agregar resultados
    FAIChatPlus_ChatRequestMessage ToolResultMsg;
    ToolResultMsg.Role = EAIChatPlus_ChatRole::Tool;

    for (const auto& ToolCall : ToolCalls)
    {
        FString Result = ExecuteGeminiTool(ToolCall.FunctionName, ToolCall.FunctionArguments);

        FAIChatPlus_ChatRequestToolCallResult ToolResult;
        ToolResult.Id = ToolCall.Id;
        ToolResult.FunctionName = ToolCall.FunctionName;
        ToolResult.FunctionResult = Result;
        ToolResultMsg.ToolCallResults.Add(ToolResult);
    }
    GeminiConversation.Add(ToolResultMsg);

// Continuar conversación
    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(GeminiOptions, GeminiConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
            ProcessGeminiToolCalls(ToolCalls, Response.GetMessage());
        }
        else
        {
            FString FinalMessage = Response.GetMessage();
            GeminiConversation.Add({FinalMessage, EAIChatPlus_ChatRole::Assistant});
            OnGeminiResponse(FinalMessage);
        }
    });

    Request->SendRequest();
}

FString UMyClass::ExecuteGeminiTool(const FString& FunctionName, const FString& Arguments)
{
    if (FunctionName == TEXT("get_weather"))
    {
        // Ejecución real de la consulta del clima
        return TEXT("{\"temperature\": 25, \"unit\": \"celsius\", \"description\": \"Sunny\"}");
    }

    return TEXT("{\"error\": \"Unknown tool\"}");
}

void UMyClass::OnGeminiResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Gemini: %s"), *Response);
}
```

##Configuración avanzada

###Usar opciones de extensión JSON

```cpp
void UMyClass::UseGeminiExtraOptions()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");

// Agregar opciones JSON adicionales
    Options.ExtraJsonString = TEXT("{\"safetySettings\": [{\"category\": \"HARM_CATEGORY_HARASSMENT\", \"threshold\": \"BLOCK_NONE\"}]}");

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###URL de punto final personalizado

```cpp
void UMyClass::UseCustomGeminiEndpoint()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");

// Usar un punto final personalizado (como un servidor proxy)
    Options.BaseUrl = TEXT("https://your-proxy-server.com/v1beta/models");
Opciones.Método = TEXTO("generarContenido");  // o transmitirGenerarContenido

// o establecer directamente la URL completa
    // Options.FullUrl = TEXT("https://your-proxy-server.com/v1beta/models/gemini-1.5-flash:generateContent?key=xxx");

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###Configuración de parámetros de muestreo

```cpp
void UMyClass::ConfigureGeminiSampling()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-pro");

// Parámetros de muestreo
Opciones.Temperatura = 0.3f; // Temperatura más baja para resultados más deterministas
    Opciones.TopK = 40;           // Muestreo Top-K
Opciones.TopP = 0.95f;        // Muestreo de Núcleo
    Options.MaxOutputTokens = 2048;

// secuencia de parada
    Options.StopSequences.Add(TEXT("\n\n"));
    Options.StopSequences.Add(TEXT("END"));

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a short story."), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

##Manejo de errores

```cpp
void UMyClass::RobustGeminiRequest()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->OnStartedListeners.AddLambda([]()
    {
        UE_LOG(LogTemp, Display, TEXT("Gemini request started..."));
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.HasError())
        {
            UE_LOG(LogTemp, Error, TEXT("Response error: %s"), *Response.Error.GetDescription());
            return;
        }

        // Verificar FinishReason
        if (!Response.Messages.IsEmpty())
        {
            FString FinishReason = Response.Messages[0].FinishReason;
            UE_LOG(LogTemp, Display, TEXT("Finish Reason: %s"), *FinishReason);
        }

        UE_LOG(LogTemp, Display, TEXT("Success: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Tokens: %s"), *Response.Usage.GetDescription());
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
UAIChatPlus_GeminiChatRequest* CurrentGeminiRequest = nullptr;

void UMyClass::StartGeminiRequest()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;

    CurrentGeminiRequest = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a very long essay about technology."), EAIChatPlus_ChatRole::User}});

    CurrentGeminiRequest->SendRequest();
}

void UMyClass::CancelGeminiRequest()
{
    if (CurrentGeminiRequest && CurrentGeminiRequest->IsActivated())
    {
        CurrentGeminiRequest->StopRequest();
        UE_LOG(LogTemp, Display, TEXT("Gemini request cancelled"));
    }
}
```

--8<-- "footer_es.md"


> Este mensaje fue traducido usando ChatGPT, por favor deja tu [**comentario**](https://github.com/disenone/wiki_blog/issues/new)Señalar cualquier omisión en el texto. 
