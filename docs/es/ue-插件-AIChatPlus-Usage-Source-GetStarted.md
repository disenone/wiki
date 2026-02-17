---
layout: post
title: Get Started
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
- Claude
- Gemini
- Ollama
description: Get Started
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Get Started" />

#C++ - Primeros Pasos

##Introducción del módulo

El complemento se divide en los siguientes módulos:

* **AIChatPlusCommon**: Módulo de tiempo de ejecución (Runtime), encargado de manejar el envío de solicitudes a varias interfaces de API de IA y analizar las respuestas.
* **AIChatPlusEditor**: Módulo del Editor (Editor), responsable de implementar la herramienta de chat AI del editor.
* **AIChatPlusCllama**: Módulo de tiempo de ejecución (Runtime) responsable de encapsular las interfaces y parámetros de llama.cpp, implementando la ejecución fuera de línea de modelos grandes.
* **Thirdparty/LLAMACpp**: Módulo de terceros (Runtime) que integra las bibliotecas dinámicas y archivos de cabecera de llama.cpp.

##Conceptos fundamentales

Antes de usar el código fuente, es necesario entender algunas clases clave y sus relaciones:

###Solicitud (Solicitud)

`UAIChatPlus_ChatRequestBase` es la clase base para todas las solicitudes de chat. Cada API Provider tiene su correspondiente subclase:

* `UAIChatPlus_OpenAIChatRequest` - Solicitud de chat de OpenAI
* `UAIChatPlus_AzureChatRequest` - Solicitud de chat de Azure
* `UAIChatPlus_ClaudeChatRequest` - Solicitud de chat con Claude
* `UAIChatPlus_GeminiChatRequest` - Solicitud de chat Gemini
* `UAIChatPlus_OllamaChatRequest` - Solicitud de chat de Ollama
* `UAIChatPlus_CllamaChatRequest` - Solicitud del modelo fuera de línea Cllama
* `UAIChatPlus_CllamaServerChatRequest` - Solicitud del servidor local CllamaServer

El objeto Request se encarga de configurar los parámetros de la solicitud, enviar la solicitud y recibir las respuestas.

###Manejador (Handler)

`UAIChatPlus_ChatHandlerBase` es una clase de manejador opcional utilizada para gestionar de manera unificada las devoluciones de llamada de las solicitudes.

Handler proporciona los siguientes delegados:

* `OnStarted` - Se activa cuando comienza la solicitud
* `OnMessage`: Se activa cuando se recibe un mensaje en flujo (salida en flujo).
* `OnUpdated` - Se activa cuando se recibe una actualización
* `OnFinished` - Se activa cuando la solicitud se completa
* `OnFailed` - Se activa cuando la solicitud falla

**¿Cuándo usar Handler?**

* Cuando se necesita gestionar de manera unificada la lógica de devolución de llamada de múltiples solicitudes.
* Cuando se necesita compartir lógica de devolución de llamada entre Blueprints y C++
* Utilizar directamente los delegados de Request (como `OnStartedListeners`) también permite implementar escuchas de devolución de llamada.

###Opciones

Cada proveedor de API tiene su estructura de Options correspondiente para configurar los parámetros de la API:

* `FAIChatPlus_OpenAIChatRequestOptions` - Opciones de OpenAI (ApiKey, Modelo, Temperatura, etc.)
* `FAIChatPlus_ClaudeChatRequestOptions` - Opciones de Claude
* `FAIChatPlus_GeminiChatRequestOptions` - Opciones de Gemini
* Espera...

Options incluye todas las configuraciones necesarias para la conexión API, como la clave API, la URL del endpoint, el nombre del modelo, los parámetros de generación, etc.

###Mensajes

`FAIChatPlus_ChatRequestMessage` es el struct del mensaje enviado al AI, que contiene:

* `Contenido` - Texto
* `Role` - Rol del mensaje (System/User/Assistant/Developer/Tool)
* `Images` - Arreglo de imágenes (función Visión)
* `Audios` - Arreglo de audios (Función Audio)
* `ToolCallUses` - Solicitud de llamada a herramienta
* `ToolCallResults` - Resultados de llamada a herramientas

###Respuesta

Cada proveedor de API tiene su estructura ResponseBody correspondiente:

* `FAIChatPlus_OpenAIChatResponseBody`
* `FAIChatPlus_ClaudeChatResponseBody`
* Espera...

ResponseBody contiene toda la información devuelta por la IA, incluyendo: texto del mensaje, consumo de tokens, llamadas a herramientas, salida de audio, etc.

##Flujo de uso básico (modo de 5 pasos)

El proceso básico para enviar solicitudes usando AIChatPlus es el siguiente:

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"

void SendChatRequest()
{
// ===== Paso 1: Crear un Handler (opcional) =====
    // Handler se utiliza para gestionar de manera uniforme las devoluciones de llamada, también se pueden usar directamente los delegados de Request
    TWeakObjectPtr<UAIChatPlus_ChatHandlerBase> Handler = UAIChatPlus_ChatHandlerBase::New();

// ===== Paso 2: Configurar Opciones =====
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
Opciones.bStream = verdadero;  // Habilitar salida en flujo

// ===== Paso 3: Crear Solicitud =====
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("Hello, who are you?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// ===== Paso 4: Vincular la devolución de llamada =====
    // Método A: Usar Handler
    Handler->BindChatRequest(Request);
    Handler->OnMessage.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Stream Message: %s"), *Message);
    });
    Handler->OnFinished.AddLambda([](const FAIChatPlus_ChatResponseBodyBase& Response)
    {
        UE_LOG(LogTemp, Display, TEXT("Request Finished"));
    });
    Handler->OnFailed.AddLambda([](const FAIChatPlus_ResponseErrorBase& Error)
    {
        UE_LOG(LogTemp, Error, TEXT("Request Failed: %s"), *Error.GetDescription());
    });

// método B: usar directamente el delegado de Request (no requiere Handler)
    // Request->OnMessageListeners.AddDynamic(this, &UMyClass::OnMessageReceived);
    // Request->OnFinishedListeners.AddDynamic(this, &UMyClass::OnRequestFinished);

// ===== Paso 5: Enviar la solicitud =====
    Request->SendRequest();
}
```

##Escritura simplificada

Si no se necesita un control detallado de la devolución de llamada, se puede utilizar una escritura más concisa:

```cpp
void SendSimpleChatRequest()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System},
            {TEXT("Hello!"), EAIChatPlus_ChatRole::User}
        });

// Vinculación directa de Lambda en Request
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Message: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final Message: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##Crear una solicitud mediante la enumeración de API Provider.

Si necesitas seleccionar dinámicamente un proveedor de API según la configuración, puedes utilizar el método de fábrica:

```cpp
void CreateRequestByProvider(EAIChatPlus_ChatApiProvider Provider)
{
// Crear una solicitud correspondiente según la enumeración
    auto Request = UAIChatPlus_ChatRequestBase::CreateByApi(Provider);

// Establecer las Options según el tipo real
    switch (Provider)
    {
    case EAIChatPlus_ChatApiProvider::OpenAI:
        {
            auto OpenAIRequest = Cast<UAIChatPlus_OpenAIChatRequest>(Request);
            FAIChatPlus_OpenAIChatRequestOptions Options;
            Options.ApiKey = TEXT("your-api-key");
            OpenAIRequest->SetOptions(Options);
        }
        break;

    case EAIChatPlus_ChatApiProvider::Claude:
        {
            auto ClaudeRequest = Cast<UAIChatPlus_ClaudeChatRequest>(Request);
            FAIChatPlus_ClaudeChatRequestOptions Options;
            Options.ApiKey = TEXT("your-api-key");
            ClaudeRequest->SetOptions(Options);
        }
        break;
    // ... Otros Providers
    }

// Configurar el mensaje y enviarlo
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Hello!"), EAIChatPlus_ChatRole::User});
    Request->SetMessages(Messages);
    Request->SendRequest();
}
```

##Descripción de la devolución de llamada

###Delegado de devolución de llamada principal

| Delegado | Momento de activación | Parámetros |
|------|----------|------|
| `OnStarted` | Cuando la solicitud comienza a enviarse | Ninguno |
| `OnMessage` | Cuando se recibe un mensaje en flujo (por cada token) | `const FString& Message` - Contenido acumulado del mensaje |
| `OnUpdated` | Cuando se recibe una actualización de respuesta | `const FAIChatPlus_ResponseBodyBase& Response` |
| `OnFinished` | Cuando la solicitud se completa con éxito | `const FAIChatPlus_ResponseBodyBase& Response` |
| `OnFailed` | Cuando falla la solicitud | `const FAIChatPlus_ResponseErrorBase& Error` |
| `OnMessageFinished` | Cuando se completa la recepción del mensaje | `const FAIChatPlus_MessageFinishedPayload& Payload` |

###Salida en flujo vs. salida no en flujo.

* **Salida en flujo** (`bStream = true`): `OnMessage` se activará múltiples veces, devolviendo cada vez el contenido acumulado del mensaje.
* **Salida no fluida** (`bStream = false`): `OnMessage` se activa solo una vez al completarse, devolviendo el mensaje completo

##Siguiente paso

Para un uso más detallado, consulta la documentación específica de cada Proveedor de API:

* [Uso de OpenAI / Azure](ue-插件-AIChatPlus-Usage-Source-OpenAI.md)
* [Uso de Claude](ue-插件-AIChatPlus-Usage-Source-Claude.md)
* [Uso de Gemini](ue-插件-AIChatPlus-Usage-Source-Gemini.md)
* [Uso de Ollama](ue-插件-AIChatPlus-Usage-Source-Ollama.md)
* [Modelo sin conexión de Cllama](ue-插件-AIChatPlus-Usage-Source-Cllama.md)
* [Servidor Local CllamaServer](ue-插件-AIChatPlus-Usage-Source-CllamaServer.md)
* [Herramientas](ue-插件-AIChatPlus-Usage-Source-Utils.md)

--8<-- "footer_es.md"

> Este post fue traducido usando ChatGPT, por favor proporcione sus comentarios en [**retroalimentación**](https://github.com/disenone/wiki_blog/issues/new)Señalar cualquier omisión en la indicación. 
