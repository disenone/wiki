---
layout: post
title: CllamaServer
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
- llama.cpp
- Local Server
description: CllamaServer
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - CllamaServer" />

#C++ Capítulo - CllamaServer

Este documento explica cómo utilizar CllamaServer en C++ para administrar un servidor de IA local y enviar solicitudes de chat.

CllamaServer opera en modo servidor basado en llama.cpp, ofreciendo un servicio local compatible con la API de OpenAI y soportando solicitudes concurrentes de múltiples clientes.

##Diferencias con Cllama

| Característica | Cllama | CllamaServer |
|------|--------|--------------|
| Modo | Inferencia directa | Servidor HTTP |
| Multi-cliente | No | Sí |
| Estilo de API | Personalizado | Compatible con OpenAI |
| Acceso a la red      | No     | Opcional |
| Llamada de Herramienta | No | Sí |

##Preparativos

Antes de usar, asegúrese de que:

1. **Descargar archivos del modelo GGUF**: Desde [Hugging Face](https://huggingface.co)Descargar el archivo del modelo en formato GGUF compatible.

2. Agrega las dependencias del módulo en el archivo `.Build.cs` del proyecto:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

3. Incluir los archivos de cabecera necesarios:

```cpp
#include "Common_CllamaServer/AIChatPlus_CllamaServer.h"
#include "Common_CllamaServer/AIChatPlus_CllamaServerChatRequest.h"
```

##Administración del servidor

###Iniciar el servidor (básico)

```cpp
#include "Common_CllamaServer/AIChatPlus_CllamaServer.h"

UPROPERTY()
UAIChatPlus_CllamaServer* LocalServer = nullptr;

void UMyClass::StartCllamaServer()
{
// Configurar parámetros del servidor
    FAIChatPlus_CllamaServerParam Params;
    Params.Model = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Params.NGpuLayers = -1;      // -1 = Asignación automática de capas GPU
Parámetros.Puerto = 0;             // 0 = asignación automática de puerto disponible
    Params.Host = TEXT("127.0.0.1");

    // Crear e iniciar el servidor
    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params);

    // Vincular la devolución de llamada de inicio del servidor
    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnServerStarted);
    LocalServer->OnStoppedListeners.AddDynamic(this, &UMyClass::OnServerStopped);
    LocalServer->OnFailedListeners.AddDynamic(this, &UMyClass::OnServerFailed);

// Activar el servidor (iniciar el proceso de arranque)
    LocalServer->Activate();
}

void UMyClass::OnServerStarted(FGuid ServerID)
{
// Obtener información del servidor
    FAIChatPlus_CllamaServerInfo Info;
    if (LocalServer->GetServerInfo(Info))
    {
        UE_LOG(LogTemp, Display, TEXT("Server started at: %s"), *Info.HttpAddress);
        UE_LOG(LogTemp, Display, TEXT("Port: %d"), Info.Port);
    }
}

void UMyClass::OnServerStopped(FGuid ServerID)
{
    UE_LOG(LogTemp, Display, TEXT("Server stopped: %s"), *ServerID.ToString());
}

void UMyClass::OnServerFailed(FGuid ServerID, const FString& ErrorMessage)
{
    UE_LOG(LogTemp, Error, TEXT("Server failed: %s"), *ErrorMessage);
}
```

###Usar Handler para administrar servidores

```cpp
#include "Common_CllamaServer/AIChatPlus_CllamaServer.h"
#include "Common_CllamaServer/AIChatPlus_CllamaServerHandler.h"

void UMyClass::StartServerWithHandler()
{
    FAIChatPlus_CllamaServerParam Params;
    Params.Model = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Params.NGpuLayers = 99;
    Params.Port = 8080;

// Crear Handler
    auto ServerHandler = UAIChatPlus_CllamaServerHandler::CreateHandler();

    // Vincular devolución de llamada nativa (no dinámica)
    ServerHandler->OnStarted.AddLambda([](FGuid ServerID)
    {
        UE_LOG(LogTemp, Display, TEXT("Server started: %s"), *ServerID.ToString());
    });

    ServerHandler->OnStopped.AddLambda([](FGuid ServerID)
    {
        UE_LOG(LogTemp, Display, TEXT("Server stopped: %s"), *ServerID.ToString());
    });

    ServerHandler->OnFailed.AddLambda([](FGuid ServerID, const FString& Error)
    {
        UE_LOG(LogTemp, Error, TEXT("Server failed: %s - %s"), *ServerID.ToString(), *Error);
    });

// Usar Handler para crear un servidor
    LocalServer = UAIChatPlus_CllamaServer::CreateServerWithHandler(Params, ServerHandler);
    LocalServer->Activate();
}
```

###Especificar ID del servidor

```cpp
void UMyClass::StartServerWithCustomID()
{
    FAIChatPlus_CllamaServerParam Params;
    Params.Model = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Params.NGpuLayers = 99;

// Especificar un ID de servidor personalizado (para facilitar la gestión posterior mediante ID)
    FGuid CustomServerID = FGuid::NewGuid();

    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params, CustomServerID);

    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnServerStarted);
    LocalServer->Activate();
}
```

###Detener el servidor

```cpp
void UMyClass::StopServer()
{
    if (LocalServer)
    {
        LocalServer->StopServer();
    }
}

// Detener el servidor por ID
void UMyClass::StopServerByID(const FGuid& ServerID)
{
    UAIChatPlus_CllamaServer::StopServerByID(ServerID);
}

// Detener todos los servidores
void UMyClass::StopAllServers()
{
    UAIChatPlus_CllamaServer::StopAllServers();
}
```

###Consultar estado del servidor

```cpp
void UMyClass::CheckServerStatus()
{
// Verificar la instancia actual del servidor
    if (LocalServer && LocalServer->IsRunning())
    {
        FString Host = LocalServer->GetHost();
        int32 Port = LocalServer->GetPort();
        FString Address = LocalServer->GetAddress();

        UE_LOG(LogTemp, Display, TEXT("Server running at: %s:%d"), *Host, Port);
    }

// Verificar el estado del servidor por ID
    FGuid ServerID = LocalServer->GetServerID();
    if (UAIChatPlus_CllamaServer::IsServerRunning(ServerID))
    {
        FAIChatPlus_CllamaServerInfo Info = UAIChatPlus_CllamaServer::GetServerInfoByID(ServerID);
        UE_LOG(LogTemp, Display, TEXT("Server info: %s"), *Info.HttpAddress);
    }
}

void UMyClass::ListAllServers()
{
    TArray<FGuid> AllServerIDs = UAIChatPlus_CllamaServer::GetAllServerIDs();

    for (const FGuid& ServerID : AllServerIDs)
    {
        FAIChatPlus_CllamaServerInfo Info = UAIChatPlus_CllamaServer::GetServerInfoByID(ServerID);
        UE_LOG(LogTemp, Display, TEXT("Server: %s - Running: %s"),
            *ServerID.ToString(),
            Info.bIsRunning ? TEXT("Yes") : TEXT("No"));
    }
}
```

##Chat de texto

###Chat básico de texto

```cpp
#include "Common_CllamaServer/AIChatPlus_CllamaServerChatRequest.h"

void UMyClass::SendCllamaServerChatRequest()
{
// Asegurarse de que el servidor esté iniciado
    if (!LocalServer || !LocalServer->IsRunning())
    {
        UE_LOG(LogTemp, Error, TEXT("Server is not running"));
        return;
    }

// Configurar las opciones de solicitud (heredadas del estilo OpenAI)
    FAIChatPlus_CllamaServerChatRequestOptions Options;
Opciones.BaseUrl = ServidorLocal->ObtenerDireccion();  // Como "http://127.0.0.1:8080"
Opciones.Modelo = TEXTO("modelo-local");          // Nombre del modelo (personalizable)
    Options.bStream = true;
    Options.Temperature = 0.8f;

    // Crear mensaje
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is the meaning of life?"), EAIChatPlus_ChatRole::User});

// Crear solicitud
    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    // Vincular devolución de llamada
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("CllamaServer: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);
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

###Diálogo de múltiples turnos

```cpp
// Variables miembro
TArray<FAIChatPlus_ChatRequestMessage> CllamaServerConversation;

void UMyClass::InitializeCllamaServerChat()
{
    CllamaServerConversation.Empty();
    CllamaServerConversation.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}

void UMyClass::SendMessage(const FString& UserMessage)
{
    CllamaServerConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    FAIChatPlus_CllamaServerChatRequestOptions Options;
    Options.BaseUrl = LocalServer->GetAddress();
    Options.bStream = true;

    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(
        Options, CllamaServerConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);
        FString AssistantMessage = Response.GetMessage();
        CllamaServerConversation.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});

        UE_LOG(LogTemp, Display, TEXT("Assistant: %s"), *AssistantMessage);
    });

    Request->SendRequest();
}
```

##Visión (Análisis de imágenes)

Para utilizar Vision es necesario especificar el modelo MMProject al iniciar el servidor.

###Iniciar el servidor con compatibilidad para Vision

```cpp
void UMyClass::StartVisionServer()
{
    FAIChatPlus_CllamaServerParam Params;

    // Modelo LLaVA
    Params.Model = TEXT("D:/Models/llava-v1.6-mistral-7b.Q4_K_M.gguf");
    Params.MMProj = TEXT("D:/Models/mmproj-llava-v1.6-mistral-7b-f16.gguf");  // Clave: modelo MMProject

    Params.NGpuLayers = 99;
    Params.Port = 8080;

    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params);
    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnVisionServerStarted);
    LocalServer->Activate();
}
```

###Enviar solicitud de análisis de imagen

```cpp
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithCllamaServer()
{
    if (!LocalServer || !LocalServer->IsRunning())
    {
        UE_LOG(LogTemp, Error, TEXT("Vision server is not running"));
        return;
    }

// Cargar imagen
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image"));
        return;
    }

    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

// Configurar la solicitud
    FAIChatPlus_CllamaServerChatRequestOptions Options;
    Options.BaseUrl = LocalServer->GetAddress();
    Options.bStream = true;

// Crear mensaje con imagen
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("What do you see in this image?");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(
        Options, {ImageMessage});

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Vision: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##Llamada de Herramienta (Función de Llamada)

CllamaServer soporta Tool Call al estilo de OpenAI (requiere modelos compatibles con function calling).

###Iniciar el servidor con soporte para Tool Call

```cpp
void UMyClass::StartToolCallServer()
{
    FAIChatPlus_CllamaServerParam Params;
    Params.Model = TEXT("D:/Models/llama-3.1-8b-instruct-q4_k_m.gguf");
    Params.NGpuLayers = 99;
    Params.Port = 8080;
    Params.bUseJinja = true;  // Las llamadas a herramientas requieren habilitar la plantilla Jinja

    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params);
    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnToolCallServerStarted);
    LocalServer->Activate();
}
```

###Definición y uso de herramientas

```cpp
void UMyClass::SendToolCallRequest()
{
    if (!LocalServer || !LocalServer->IsRunning())
    {
        UE_LOG(LogTemp, Error, TEXT("Tool call server is not running"));
        return;
    }

    FAIChatPlus_CllamaServerChatRequestOptions Options;
    Options.BaseUrl = LocalServer->GetAddress();
    Options.bStream = false;  // Se recomienda deshabilitar el flujo en Tool Call

// definir herramienta
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = TEXT("function");
    WeatherTool.Function.Name = TEXT("get_weather");
    WeatherTool.Function.Description = TEXT("Get the current weather for a location");
    WeatherTool.Function.Parameters = TEXT(R"({
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit"
            }
        },
        "required": ["location"]
    })");

    Options.Tools.Add(WeatherTool);

    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is the weather like in Tokyo?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);

// Comprobar si hay llamadas a herramientas
        if (Response.Choices.Num() > 0)
        {
            const auto& Choice = Response.Choices[0];
            const auto& ToolCalls = Choice.Message.ToolCalls;

            if (ToolCalls.Num() > 0)
            {
                for (const auto& ToolCall : ToolCalls)
                {
                    UE_LOG(LogTemp, Display, TEXT("Tool Call: %s(%s)"),
                        *ToolCall.Function.Name, *ToolCall.Function.Arguments);

// Ejecuta la llamada a la herramienta y continúa la conversación
                    ExecuteToolCall(ToolCall);
                }
            }
            else
            {
                UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
            }
        }
    });

    Request->SendRequest();
}
```

###Ciclo completo de Tool Call

```cpp
TArray<FAIChatPlus_ChatRequestMessage> ToolCallConversation;
FAIChatPlus_CllamaServerChatRequestOptions ToolCallOptions;

void UMyClass::InitializeToolCallChat()
{
    ToolCallOptions.BaseUrl = LocalServer->GetAddress();
    ToolCallOptions.bStream = false;

// definir la herramienta
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = TEXT("function");
    WeatherTool.Function.Name = TEXT("get_weather");
    WeatherTool.Function.Description = TEXT("Get the current weather");
    WeatherTool.Function.Parameters = TEXT(R"({
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City name"}
        },
        "required": ["location"]
    })");
    ToolCallOptions.Tools.Add(WeatherTool);

    ToolCallConversation.Empty();
    ToolCallConversation.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}

void UMyClass::SendToolCallMessage(const FString& UserMessage)
{
    ToolCallConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(
        ToolCallOptions, ToolCallConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.Choices.Num() > 0)
        {
            const auto& Choice = Response.Choices[0];
            const auto& ToolCalls = Choice.Message.ToolCalls;

            if (ToolCalls.Num() > 0)
            {
// 1. Agregar la solicitud de invocación de herramienta del Asistente al historial
                FAIChatPlus_ChatRequestMessage AssistantMessage;
                AssistantMessage.Role = EAIChatPlus_ChatRole::Assistant;
                AssistantMessage.ToolCallUses = ToolCalls;
                ToolCallConversation.Add(AssistantMessage);

// 2. Ejecutar herramienta y añadir resultados
                for (const auto& ToolCall : ToolCalls)
                {
                    FString Result = ExecuteToolFunction(ToolCall.Function.Name, ToolCall.Function.Arguments);

                    FAIChatPlus_ChatRequestMessage ToolResultMessage;
                    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;
                    ToolResultMessage.Content = Result;
                    ToolResultMessage.ToolCallId = ToolCall.Id;
                    ToolCallConversation.Add(ToolResultMessage);
                }

// 3. Continuar la conversación, permite al modelo procesar los resultados de la herramienta.
                ContinueToolCallConversation();
            }
            else
            {
// respuesta normal
                FString AssistantResponse = Response.GetMessage();
                ToolCallConversation.Add({AssistantResponse, EAIChatPlus_ChatRole::Assistant});
                UE_LOG(LogTemp, Display, TEXT("Final: %s"), *AssistantResponse);
            }
        }
    });

    Request->SendRequest();
}

FString UMyClass::ExecuteToolFunction(const FString& FunctionName, const FString& Arguments)
{
    if (FunctionName == TEXT("get_weather"))
    {
// Analizar los parámetros y devolver el resultado
        return TEXT("{\"temperature\": \"22\", \"condition\": \"sunny\", \"unit\": \"celsius\"}");
    }
    return TEXT("{\"error\": \"Unknown function\"}");
}

void UMyClass::ContinueToolCallConversation()
{
    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(
        ToolCallOptions, ToolCallConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);
        FString FinalResponse = Response.GetMessage();
        ToolCallConversation.Add({FinalResponse, EAIChatPlus_ChatRole::Assistant});

        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *FinalResponse);
    });

    Request->SendRequest();
}
```

##Configuración avanzada del servidor

###Ejemplo de configuración completa

```cpp
void UMyClass::StartAdvancedServer()
{
    FAIChatPlus_CllamaServerParam Params;

// ===== Configuración del modelo =====
    Params.Model = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
Params.Alias = TEXT("mi-modelo-local");    // Alias del modelo
Params.MMProj = TEXT("");                 // Ruta del modelo Vision MMProject

// ===== Configuración de hardware =====
Params.NGpuLayers = 99;      // Capas de GPU (-1 = automático)
Params.Threads = -1;         // Número de hilos de CPU (-1 = automático)
    Params.ThreadsBatch = -1;    // Número de hilos en lote

// ===== Configuración de contexto =====
    Params.CtxSize = 4096;       // Tamaño de la ventana de contexto
    Params.NPredict = -1;        // Número máximo de tokens generados (-1 = infinito)
    Params.BatchSize = 2048;     // Tamaño del lote lógico
Params.UbatchSize = 512;     // Tamaño del lote físico
Params.Keep = 0;             // Cantidad inicial de tokens a conservar

// ===== Configuración de muestreo =====
    Params.Temperature = 0.8f;
    Params.TopK = 40;
    Params.TopP = 0.9f;
    Params.MinP = 0.1f;
    Params.RepeatLastN = 64;
    Params.RepeatPenalty = 1.0f;
    Params.PresencePenalty = 0.0f;
    Params.FrequencyPenalty = 0.0f;
    Params.Seed = 0xFFFFFFFF;    // Semilla aleatoria (0xFFFFFFFF = aleatorio)

// ===== Configuración del servidor =====
    Params.Host = TEXT("127.0.0.1");
    Params.Port = 8080;          // 0 = asignación automática
    Params.Timeout = 600;        // Tiempo de espera (segundos)
Params.Parallel = 1;         // Número de solicitudes paralelas
Params.bContBatching = true; // Procesamiento por lotes continuo
Parámetros.bSlots = verdadero;    // Habilita el punto final de monitoreo de slots

// ===== Configuración de funciones =====
Params.bUseJinja = true;     // Utilizar plantilla Jinja (necesario para Tool Call)
Params.bNoWebUI = false;     // Deshabilitar la interfaz web
    Params.ApiKey = TEXT("");    // Clave API para autenticación
    Params.ChatTemplate = TEXT("");  // Plantilla de chat personalizada

    // ===== Configuración de depuración =====
Params.bVerbose = true;      // Registros detallados

    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params);
    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnServerStarted);
    LocalServer->Activate();
}
```

##Manejo de errores

```cpp
void UMyClass::RobustCllamaServerRequest()
{
// Verificar estado del servidor
    if (!LocalServer)
    {
        UE_LOG(LogTemp, Error, TEXT("Server instance is null"));
        return;
    }

    if (!LocalServer->IsRunning())
    {
        UE_LOG(LogTemp, Error, TEXT("Server is not running"));
        return;
    }

    FAIChatPlus_CllamaServerChatRequestOptions Options;
    Options.BaseUrl = LocalServer->GetAddress();
    Options.bStream = true;

    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->OnStartedListeners.AddLambda([]()
    {
        UE_LOG(LogTemp, Display, TEXT("Request started"));
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.HasError())
        {
            UE_LOG(LogTemp, Error, TEXT("Response error: %s"), *Response.Error.GetDescription());
            return;
        }

        UE_LOG(LogTemp, Display, TEXT("Success: %s"), *Response.GetMessage());
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_ResponseErrorBase>();
        UE_LOG(LogTemp, Error, TEXT("Request failed: %s"), *Error.GetDescription());
    });

    Request->SendRequest();
}
```

##Limpiar recursos

```cpp
void UMyClass::CleanupCllamaServer()
{
// Detener todas las solicitudes
    // ...

// Detener el servidor
    if (LocalServer)
    {
        LocalServer->StopServer();
        LocalServer = nullptr;
    }

    // o detener todos los servidores
    UAIChatPlus_CllamaServer::StopAllServers();
}

// Limpieza al destruir el Actor
void AMyActor::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    CleanupCllamaServer();
    Super::EndPlay(EndPlayReason);
}
```

--8<-- "footer_es.md"


> Este mensaje ha sido traducido usando ChatGPT, por favor envíe sus comentarios en [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Señalar cualquier omisión en el texto. 
