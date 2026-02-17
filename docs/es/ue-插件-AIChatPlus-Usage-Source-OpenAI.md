---
layout: post
title: OpenAI / Azure
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
description: OpenAI / Azure
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - OpenAI / Azure" />

#C++ Parte - OpenAI / Azure

Este documento explica cómo usar OpenAI y la API de Azure en C++ para chat, análisis de imágenes, entrada y salida de voz y Tool Calling.

> **Nota**: La API de Azure es compatible con OpenAI y su uso es básicamente el mismo, solo necesitas modificar la `BaseUrl` y la `ApiKey`.

##Preparativos

Antes de usar, asegúrese de que:

1. Agrega las dependencias de módulo en el archivo `.Build.cs` del proyecto:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

2. Incluir los archivos de cabecera necesarios:

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"
#include "Common/AIChatPlus_Log.h"
```

##Chat de texto

###Chat de texto básico

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"

void UMyClass::SendOpenAIChatRequest()
{
// Configurar Opciones
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-openai-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;  // Habilitar salida en flujo
    Options.Temperature = 0.7f;
    Options.MaxOutputTokens = 1024;

// Crear mensaje
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is the capital of France?"), EAIChatPlus_ChatRole::User});

// crear solicitud
    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    // Enlace de devolución de llamada
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Message: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Token Usage: %s"), *Response.Usage.GetDescription());
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_OpenAIChatResponseError>();
        UE_LOG(LogTemp, Error, TEXT("Request Failed: %s"), *Error.GetDescription());
    });

// Enviar solicitud
    Request->SendRequest();
}
```

###Usar la API de Azure

Azure API es compatible con OpenAI, solo necesitas modificar la URL y el método de autenticación:

```cpp
#include "Common_Azure/AIChatPlus_AzureChatRequest.h"

void UMyClass::SendAzureChatRequest()
{
    FAIChatPlus_AzureChatRequestOptions Options;
    Options.ApiKey = TEXT("your-azure-api-key");
    Options.ResourceName = TEXT("nombre-de-tu-recurso");  // Nombre del recurso en Azure
    Options.DeploymentName = TEXT("tu-nombre-de-despliegue");  // Nombre del despliegue
Opciones.VersionApi = TEXT("2024-02-01");  // Versión de la API
    Options.bStream = true;

    auto Request = UAIChatPlus_AzureChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System},
            {TEXT("Hello!"), EAIChatPlus_ChatRole::User}
        });

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Azure Message: %s"), *Message);
    });

    Request->SendRequest();
}
```

###Diálogo multironda

```cpp
void UMyClass::MultiTurnConversation()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

// Construir historial de diálogo multiturno
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("My name is Alice."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("Hello Alice! Nice to meet you. How can I help you today?"), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my name?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
// El modelo debería poder recordar que el nombre de usuario es Alice
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##Visión (Análisis de imágenes)

La función Vision de OpenAI permite al modelo analizar el contenido de las imágenes.

###Cargar imagen desde archivo y analizar

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageFromFile()
{
// cargar imagen desde archivo
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image: %s"), *ImagePath);
        return;
    }

    // Crear un objeto Texture para el complemento
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

// Configurar Opciones
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
Opciones.Modelo = TEXTO("gpt-4o");  // Visión requiere gpt-4o o gpt-4-turbo
    Options.bStream = true;

// crear mensaje con imagen
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("What is in this image? Describe it in detail.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant that can analyze images."), EAIChatPlus_ChatRole::System},
            ImageMessage
        });

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Vision Analysis: %s"), *Message);
    });

    Request->SendRequest();
}
```

###Análisis desde Texture2D (captura de pantalla in-game)

```cpp
void UMyClass::AnalyzeGameTexture(UTexture2D* GameTexture)
{
    if (!GameTexture)
    {
        UE_LOG(LogTemp, Error, TEXT("Invalid texture"));
        return;
    }

// Convertir a complemento Textura
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(GameTexture);

    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o");
    Options.bStream = true;

    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("Analyze this game screenshot and describe what you see.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options, {{TEXT("You are a game analyst."), EAIChatPlus_ChatRole::System}, ImageMessage});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Game Analysis: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##Audio (entrada y salida de voz)

OpenAI admite funciones de entrada y salida de voz (se requiere el modelo `gpt-4o-audio-preview`).

###Entrada de voz (Speech-to-Text)

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::SendAudioMessage()
{
// Cargar audio desde el archivo
    FString AudioPath = FPaths::ProjectContentDir() / TEXT("Audio/question.wav");
    USoundWave* SoundWave = UAIChatPlus_Util::LoadSoundWav(AudioPath);

    if (!SoundWave)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load audio: %s"), *AudioPath);
        return;
    }

// Crear un objeto Sound disponible para el plugin
    UAIChatPlus_Sound* ChatSound = UAIChatPlus_Sound::CreateFromSoundWave(SoundWave);

// Configurar Opciones
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
Opciones.Modelo = TEXTO("gpt-4o-vista-previa-audio");  // Modelo compatible con audio
    Options.bStream = false;  // La salida de audio no admite transmisión en flujo

// crear un mensaje con audio
    FAIChatPlus_ChatRequestMessage AudioMessage;
    AudioMessage.Content = TEXT("");  // Los mensajes de audio pueden no requerir texto
    AudioMessage.Role = EAIChatPlus_ChatRole::User;
    AudioMessage.Audios.Add(ChatSound);

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant. Listen to the audio and respond."), EAIChatPlus_ChatRole::System},
            AudioMessage
        });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Response to audio: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###Salida de voz (Text-to-Speech)

```cpp
void UMyClass::RequestAudioOutput()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-audio-preview");
    Options.bStream = false;  // La salida de audio no admite transmisión en flujo

// Configurar la salida de audio
    Options.Modalities.Add(EAIChatPlus_OpenAIChatModality::Text);
    Options.Modalities.Add(EAIChatPlus_OpenAIChatModality::Audio);
    Options.AudioConfig.Format = TEXT("wav");
Opciones.ConfiguracionAudio.Voz = TEXT("alloy");  // Opcional: alloy, ash, ballad, coral, echo, sage, shimmer, verse

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System},
            {TEXT("Tell me a short joke."), EAIChatPlus_ChatRole::User}
        });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

// obtener la respuesta del texto
        UE_LOG(LogTemp, Display, TEXT("Text Response: %s"), *Response.GetMessage());

// obtener respuesta de audio
        TArray<FAIChatPlus_ChatResponseAudioOutput> AudioOutputs = Response.GetAudioOutputs();
        for (const auto& AudioOutput : AudioOutputs)
        {
            if (AudioOutput.Sound)
            {
// reproducir audio
// AudioOutput.Sound es un UAIChatPlus_Sound* del cual se puede obtener el USoundWave
                UE_LOG(LogTemp, Display, TEXT("Audio Transcript: %s"), *AudioOutput.Transcript);

// guardar audio en archivo
                FString SavePath = FPaths::ProjectSavedDir() / TEXT("Audio/response.wav");
                UAIChatPlus_Util::SaveSoundWav(AudioOutput.Sound->GetSoundWave(), SavePath);
            }
        }
    });

    Request->SendRequest();
}
```

##Llamada de Herramientas (invocación de funciones)

Tool Calling permite que el modelo invoque funciones predefinidas para obtener datos externos.

###Definir herramienta y enviar solicitud

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"

void UMyClass::SendToolCallRequest()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

// Definir herramienta: Obtener clima
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a location.");

// definir los parámetros de la herramienta
    FAIChatPlus_ChatRequestToolProperty LocationProp;
    LocationProp.Name = TEXT("location");
    LocationProp.Description = TEXT("The city name, e.g. Beijing, Tokyo, New York");
    LocationProp.Type = TEXT("string");
    LocationProp.Required = true;

    FAIChatPlus_ChatRequestToolProperty UnitProp;
    UnitProp.Name = TEXT("unit");
    UnitProp.Description = TEXT("The temperature unit");
    UnitProp.Type = TEXT("string");
    UnitProp.Required = false;
    UnitProp.ExtraJsonString = TEXT("{\"enum\": [\"celsius\", \"fahrenheit\"]}");

    WeatherTool.Properties.Add(LocationProp);
    WeatherTool.Properties.Add(UnitProp);

    Options.Tools.Add(WeatherTool);

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant. Use tools when needed."), EAIChatPlus_ChatRole::System},
            {TEXT("What's the weather like in Tokyo?"), EAIChatPlus_ChatRole::User}
        });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

// Verificar si hay una llamada a Tool
        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
            for (const auto& ToolCall : ToolCalls)
            {
                UE_LOG(LogTemp, Display, TEXT("Tool Call - ID: %s, Function: %s, Args: %s"),
                    *ToolCall.Id, *ToolCall.FunctionName, *ToolCall.FunctionArguments);

// Aquí se realiza la llamada real a la función y luego se envía el resultado de vuelta al modelo
Ver el ejemplo a continuación "Manejo de resultados de Tool Call"
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

###Procesamiento del Resultado de Tool Call

Cuando el modelo devuelve una llamada a herramienta (Tool Call), es necesario ejecutar la función y enviar el resultado de vuelta al modelo:

```cpp
void UMyClass::HandleToolCallAndSendResult()
{
// Supongamos que esta es la llamada de herramienta devuelta por el modelo
    FString ToolCallId = TEXT("call_abc123");
    FString FunctionName = TEXT("get_weather");
    FString FunctionResult = TEXT("{\"temperature\": 22, \"unit\": \"celsius\", \"description\": \"Sunny\"}");

    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

// Redefinir herramientas (mantener la consistencia)
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a location.");
    Options.Tools.Add(WeatherTool);

// Construir el historial de mensajes que incluye los resultados de Tool Call
    TArray<FAIChatPlus_ChatRequestMessage> Messages;

// 1. Mensajes del sistema
    Messages.Add({TEXT("You are a helpful assistant. Use tools when needed."), EAIChatPlus_ChatRole::System});

    // 2. Problema original del usuario
    Messages.Add({TEXT("What's the weather like in Tokyo?"), EAIChatPlus_ChatRole::User});

    // 3. Solicitud de Tool Call del Asistente
    FAIChatPlus_ChatRequestMessage AssistantMessage;
    AssistantMessage.Role = EAIChatPlus_ChatRole::Assistant;
AssistantMessage.Content = TEXT("");  // Puede que no haya contenido de texto durante la llamada a Tool Call

    FAIChatPlus_ChatRequestToolCall ToolCallUse;
    ToolCallUse.Id = ToolCallId;
    ToolCallUse.Type = TEXT("function");
    ToolCallUse.FunctionName = FunctionName;
    ToolCallUse.FunctionArguments = TEXT("{\"location\": \"Tokyo\"}");
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

// Enviar solicitud
    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
// El modelo generará la respuesta final basándose en los resultados de las herramientas
        UE_LOG(LogTemp, Display, TEXT("Final Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###Ciclo completo de Tool Call

Aquí tienes un ejemplo completo de un ciclo de Tool Calling:

```cpp
// Almacenar el historial de conversación
TArray<FAIChatPlus_ChatRequestMessage> ConversationHistory;
FAIChatPlus_OpenAIChatRequestOptions CurrentOptions;

void UMyClass::InitializeToolChat()
{
    CurrentOptions.ApiKey = TEXT("your-api-key");
    CurrentOptions.Model = TEXT("gpt-4o-mini");
    CurrentOptions.bStream = true;

// Definir herramienta
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a location.");

    FAIChatPlus_ChatRequestToolProperty LocationProp;
    LocationProp.Name = TEXT("location");
    LocationProp.Type = TEXT("string");
    LocationProp.Required = true;
    WeatherTool.Properties.Add(LocationProp);

    CurrentOptions.Tools.Add(WeatherTool);

// inicializar diálogo
    ConversationHistory.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}

void UMyClass::SendUserMessage(const FString& UserMessage)
{
    ConversationHistory.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(CurrentOptions, ConversationHistory);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
// Manejar Tool Call
            ProcessToolCalls(ToolCalls, Response.GetMessage());
        }
        else
        {
// Respuesta normal
            FString AssistantMessage = Response.GetMessage();
            ConversationHistory.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});
            OnAssistantResponse(AssistantMessage);
        }
    });

    Request->SendRequest();
}

void UMyClass::ProcessToolCalls(const TArray<FAIChatPlus_ChatResponseToolCall>& ToolCalls, const FString& AssistantContent)
{
// Agregar mensaje de Tool Call del Asistente
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
    ConversationHistory.Add(AssistantMsg);

    // Ejecuta cada herramienta y añade los resultados
    FAIChatPlus_ChatRequestMessage ToolResultMsg;
    ToolResultMsg.Role = EAIChatPlus_ChatRole::Tool;

    for (const auto& ToolCall : ToolCalls)
    {
        FString Result = ExecuteTool(ToolCall.FunctionName, ToolCall.FunctionArguments);

        FAIChatPlus_ChatRequestToolCallResult ToolResult;
        ToolResult.Id = ToolCall.Id;
        ToolResult.FunctionName = ToolCall.FunctionName;
        ToolResult.FunctionResult = Result;
        ToolResultMsg.ToolCallResults.Add(ToolResult);
    }
    ConversationHistory.Add(ToolResultMsg);

    // Enviar la solicitud con los resultados de las herramientas
    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(CurrentOptions, ConversationHistory);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> NewToolCalls = Response.GetToolCalls();
        if (NewToolCalls.Num() > 0)
        {
// Puede que sea necesario seguir llamando a las herramientas
            ProcessToolCalls(NewToolCalls, Response.GetMessage());
        }
        else
        {
            FString FinalMessage = Response.GetMessage();
            ConversationHistory.Add({FinalMessage, EAIChatPlus_ChatRole::Assistant});
            OnAssistantResponse(FinalMessage);
        }
    });

    Request->SendRequest();
}

FString UMyClass::ExecuteTool(const FString& FunctionName, const FString& Arguments)
{
    if (FunctionName == TEXT("get_weather"))
    {
// Analizar los parámetros y ejecutar la consulta real del clima
// Aquí se devuelven datos simulados
        return TEXT("{\"temperature\": 22, \"unit\": \"celsius\", \"description\": \"Sunny\"}");
    }

    return TEXT("{\"error\": \"Unknown function\"}");
}

void UMyClass::OnAssistantResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Assistant: %s"), *Response);
}
```

##Generación de imágenes

Generar imágenes utilizando el modelo DALL-E de OpenAI:

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIImageRequest.h"

void UMyClass::GenerateImage()
{
    FAIChatPlus_OpenAIImageRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("dall-e-3");
    Options.ChatType = EAIChatPlus_ImageChatType::Generation;
    Options.Size = TEXT("1024x1024");
    Options.Quality = EAIChatPlus_OpenAIImageQuality::Standard;
    Options.ResponseFormat = EAIChatPlus_OpenAIImageResponseFormat::Url;

    auto Request = UAIChatPlus_OpenAIImageRequest::CreateWithOptions(Options);
    Request->SetPrompt(TEXT("A beautiful sunset over mountains, digital art style"));

    Request->OnImagesListeners.AddLambda([](const TArray<UTexture2D*>& Images, bool bFinished)
    {
        for (int32 i = 0; i < Images.Num(); ++i)
        {
            if (Images[i])
            {
// guardar la imagen
                FString SavePath = FString::Printf(TEXT("%s/GeneratedImages/image_%d.png"),
                    *FPaths::ProjectSavedDir(), i);
                UAIChatPlus_Util::SaveImage(Images[i], SavePath);
                UE_LOG(LogTemp, Display, TEXT("Image saved to: %s"), *SavePath);
            }
        }
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_OpenAIChatResponseError>();
        UE_LOG(LogTemp, Error, TEXT("Image generation failed: %s"), *Error.GetDescription());
    });

    Request->SendRequest();
}
```

##Configuración avanzada

###Usar opciones de extensión JSON

Agregar opciones no admitidas directamente por la API mediante `ExtraJsonString` o `ExtraJsonObject`:

```cpp
void UMyClass::UseExtraJsonOptions()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");

// Agregar opciones adicionales usando una cadena JSON
    Options.ExtraJsonString = TEXT("{\"store\": false, \"metadata\": {\"user_id\": \"12345\"}}");

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###URL de punto final personalizado

Admite el uso de puntos de conexión API personalizados (como servidores proxy):

```cpp
void UMyClass::UseCustomEndpoint()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");

    // Método 1: Establecer BaseUrl y EndPointUrl por separado
    Options.BaseUrl = TEXT("https://your-proxy-server.com");
    Options.EndPointUrl = TEXT("v1/chat/completions");

// Método 2: Establecer directamente la URL completa (se ignorarán BaseUrl y EndPointUrl)
    // Options.FullUrl = TEXT("https://your-proxy-server.com/v1/chat/completions");

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

##Manejo de errores

###Ejemplo completo de manejo de errores

```cpp
void UMyClass::RobustChatRequest()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->OnStartedListeners.AddLambda([]()
    {
        UE_LOG(LogTemp, Display, TEXT("Request started..."));
    });

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
// Mensajes en flujo
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

// verificar si la respuesta contiene errores
        if (Response.HasError())
        {
            UE_LOG(LogTemp, Error, TEXT("Response error: %s"), *Response.Error.GetDescription());
            return;
        }

        UE_LOG(LogTemp, Display, TEXT("Success: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Tokens used: %s"), *Response.Usage.GetDescription());
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_OpenAIChatResponseError>();
        UE_LOG(LogTemp, Error, TEXT("Request failed!"));
        UE_LOG(LogTemp, Error, TEXT("  Code: %s"), *Error.Code);
        UE_LOG(LogTemp, Error, TEXT("  Type: %s"), *Error.Type);
        UE_LOG(LogTemp, Error, TEXT("  Message: %s"), *Error.Message);
        UE_LOG(LogTemp, Error, TEXT("  Param: %s"), *Error.Param);
    });

    Request->SendRequest();
}
```

##Detener solicitud

Las solicitudes en curso pueden detenerse:

```cpp
// Almacenar referencia de la solicitud
UPROPERTY()
UAIChatPlus_OpenAIChatRequest* CurrentRequest = nullptr;

void UMyClass::StartRequest()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    // ... opciones de configuración

    CurrentRequest = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a very long story."), EAIChatPlus_ChatRole::User}});

    CurrentRequest->SendRequest();
}

void UMyClass::CancelRequest()
{
    if (CurrentRequest && CurrentRequest->IsActivated())
    {
        CurrentRequest->StopRequest();
        UE_LOG(LogTemp, Display, TEXT("Request cancelled"));
    }
}
```

--8<-- "footer_es.md"


> Este mensaje ha sido traducido usando ChatGPT. Por favor, proporciona tus comentarios en [**retroalimentación**](https://github.com/disenone/wiki_blog/issues/new)Señalar cualquier omisión en el texto. 
