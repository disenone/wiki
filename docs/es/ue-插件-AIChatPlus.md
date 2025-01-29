---
layout: post
title: UE Plugin AIChatPlus Documentación
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
description: UE Plug-in AIChatPlus Documentación
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documento de instrucciones del plugin UE AIChatPlus

##almacén público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtención del complemento

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Descripción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un plugin de Unreal Engine que permite la comunicación con varios servicios de chat de IA GPT. Actualmente, admite servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama y llama.cpp de forma local y sin conexión. En el futuro, se continuará ampliando el soporte para más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que garantiza un alto rendimiento y facilita la integración de estos servicios de chat de IA para los desarrolladores de UE.

Al mismo tiempo, UE.AIChatPlus también incluye una herramienta de editor que permite utilizar estos servicios de chat de IA directamente en el editor, generando texto e imágenes, analizando imágenes, entre otras funciones.

##Instrucciones de uso

###Editor de herramientas de chat

Menú Herramientas -> AIChatPlus -> AIChat para abrir la herramienta de chat del editor proporcionada por el plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


La herramienta soporta generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

工具的界面大致为： 

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Función principal

* Modelo grande offline: Integra la biblioteca llama.cpp, soporta la ejecución offline del modelo grande en local.

* Chat de texto: Haz clic en el botón `Nuevo chat` en la esquina inferior izquierda para crear una nueva sesión de chat de texto.

* Generación de imágenes: haga clic en el botón `New Image Chat` en la esquina inferior izquierda para crear una nueva sesión de generación de imágenes.

* Análisis de imágenes: Algunas de las funciones de chat de `New Chat` admiten el envío de imágenes, como Claude y Google Gemini. Haga clic en el botón 🖼️ o 🎨 en la parte superior del cuadro de entrada para cargar la imagen que desea enviar.

* Soporte de Blueprint: Soporte para la creación de solicitudes API de Blueprint, completando funciones como chat de texto, generación de imágenes, etc.

* Establecer el rol de chat actual: El menú desplegable en la parte superior del cuadro de chat permite establecer el rol del texto que se envía actualmente, lo que permite ajustar la conversación con la IA simulando diferentes roles.

* Borrar conversación: El botón ❌ en la parte superior del cuadro de chat puede borrar el historial de mensajes de la conversación actual.

* Plantilla de diálogo: incorpora cientos de plantillas de configuración de diálogos, facilitando el manejo de preguntas comunes.

* Configuración global: Haz clic en el botón `Setting` en la esquina inferior izquierda para abrir la ventana de configuración global. Puedes ajustar el chat de texto predeterminado, el servicio API de generación de imágenes y establecer los parámetros específicos de cada servicio API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Configuración de la conversación: Haga clic en el botón de configuración ubicado en la parte superior del cuadro de chat para abrir la ventana de configuración de la conversación actual. Se puede modificar el nombre de la conversación, cambiar el servicio API utilizado, y ajustar los parámetros específicos del API para cada conversación de forma independiente. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

* Modificación del contenido del chat: Al pasar el ratón sobre el contenido del chat, aparecerá un botón de configuración para ese contenido específico, que permite regenerar el contenido, modificarlo, copiarlo, eliminarlo y regenerar el contenido en la parte inferior (para los contenidos cuyo rol es el usuario).

* Vista de imágenes: Para la generación de imágenes, al hacer clic en la imagen se abrirá una ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como PNG/UE Texture. La textura se puede visualizar directamente en el navegador de contenido (Content Browser), lo que facilita su uso dentro del editor. Además, soporta funciones como eliminar imágenes, regenerar imágenes y continuar generando más imágenes. En el editor para Windows, también se admite la copia de imágenes, permitiendo copiar la imagen directamente al portapapeles para facilitar su uso. Las imágenes generadas durante la sesión también se guardarán automáticamente en la carpeta de cada sesión, cuyo camino suele ser `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Plano:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Configuración general:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Configuración de conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modificar el contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visor de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Uso de modelos grandes fuera de línea

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Plantilla de conversación

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introducción al código fuente

Actualmente, el complemento se divide en los siguientes módulos:

* AIChatPlusCommon: Módulo en tiempo de ejecución (Runtime), encargado de manejar las solicitudes enviadas a través de diversas interfaces de API de IA y de analizar el contenido de las respuestas.

* AIChatPlusEditor: Módulo de editor (Editor), responsable de implementar la herramienta de chat AI del editor.

* AIChatPlusCllama: Módulo de tiempo de ejecución (Runtime), encargado de encapsular la interfaz y los parámetros de llama.cpp, logrando la ejecución offline de un gran modelo.

* Thirdparty/LLAMACpp: Módulo de terceros en tiempo de ejecución (Runtime), que integra la biblioteca dinámica y los archivos de cabecera de llama.cpp.

El UClass que se encarga de enviar las solicitudes es FAIChatPlus_xxxChatRequest, y cada servicio de API tiene un Request UClass independiente. Las respuestas a las solicitudes se obtienen a través de dos UClass: UAIChatPlus_ChatHandlerBase y UAIChatPlus_ImageHandlerBase, solo es necesario registrar el delegado de retorno correspondiente.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje que se enviará. Esto se realiza a través de FAIChatPlus_xxxChatRequestBody. El contenido específico de la respuesta también se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir la notificación, se puede obtener el ResponseBody a través de una interfaz específica.

Más detalles sobre el código fuente se pueden obtener en la tienda UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Herramienta de edición que utiliza el modelo offline Cllama (llama.cpp)

A continuación se explica cómo utilizar el modelo offline llama.cpp en la herramienta del editor AIChatPlus.

* Primero, descarga el modelo offline desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

* Coloca el modelo en una carpeta, por ejemplo, en el directorio del proyecto del juego Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

* Abre la herramienta del editor AIChatPlus: Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat y abre la página de configuración de la sesión.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

* Configura la Api como Cllama, activa la Configuración de Api Personalizada, añade la ruta de búsqueda del modelo y selecciona el modelo.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

* ¡Comienza a chatear!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Las herramientas del editor utilizan el modelo offline Cllama (llama.cpp) para procesar imágenes.

* Descarga el modelo offline MobileVLM_V2-1.7B-GGUF desde el sitio web de HuggingFace y colócalo en el directorio Content/LLAMA: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf).

* Configurar el modelo de la conversación:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

* Enviar imagen para empezar a chatear

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###El código utiliza el modelo offline Cllama (llama.cpp)

A continuación se explica cómo utilizar el modelo offline llama.cpp en el código.

* Primero, también se necesita descargar el archivo del modelo en Content/LLAMA.

* Modifica el código para añadir un comando y envía un mensaje al modelo offline dentro de ese comando.

```c++
#include "Common/AIChatPlus_Log.h"
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"

void AddTestCommand()
{
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("AIChatPlus.TestChat"),
		TEXT("Test Chat."),
		FConsoleCommandDelegate::CreateLambda([]()
		{
			if (!FModuleManager::GetModulePtr<FAIChatPlusCommon>(TEXT("AIChatPlusCommon"))) return;

			TWeakObjectPtr<UAIChatPlus_ChatHandlerBase> HandlerObject = UAIChatPlus_ChatHandlerBase::New();
			// Cllama
			FAIChatPlus_CllamaChatRequestOptions Options;
			Options.ModelPath.FilePath = FPaths::ProjectContentDir() / "LLAMA" / "qwen1.5-1_8b-chat-q8_0.gguf";
			Options.NumPredict = 400;
			Options.bStream = true;
			// Options.StopSequences.Emplace(TEXT("json"));
			auto RequestPtr = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(
				Options,
				{
					{"You are a chat bot", EAIChatPlus_ChatRole::System},
					{"who are you", EAIChatPlus_ChatRole::User}
				});

			HandlerObject->BindChatRequest(RequestPtr);
			const FName ApiName = TEnumTraits<EAIChatPlus_ChatApiProvider>::ToName(RequestPtr->GetApiProvider());

			HandlerObject->OnMessage.AddLambda([ApiName](const FString& Message)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] Message: [%s]"), *ApiName.ToString(), *Message);
			});
			HandlerObject->OnStarted.AddLambda([ApiName]()
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestStarted"), *ApiName.ToString());
			});
			HandlerObject->OnFailed.AddLambda([ApiName](const FAIChatPlus_ResponseErrorBase& InError)
			{
				UE_LOG(AIChatPlus_Internal, Error, TEXT("TestChat[%s] RequestFailed: %s "), *ApiName.ToString(), *InError.GetDescription());
			});
			HandlerObject->OnUpdated.AddLambda([ApiName](const FAIChatPlus_ResponseBodyBase& ResponseBody)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestUpdated"), *ApiName.ToString());
			});
			HandlerObject->OnFinished.AddLambda([ApiName](const FAIChatPlus_ResponseBodyBase& ResponseBody)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestFinished"), *ApiName.ToString());
			});

			RequestPtr->SendRequest();
		}),
		ECVF_Default
	);
}
```

* Después de recompilar, puedes utilizar el comando en el editor Cmd para ver los resultados de salida del modelo grande en el registro OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###La hoja de ruta utiliza el modelo fuera de línea llama.cpp.

A continuación se explica cómo utilizar el modelo offline llama.cpp en el blueprint.

* Haz clic derecho en el plano para crear un nodo `Send Cllama Chat Request`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

* Crea un nodo de Opciones y establece `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

* Crear Messages, adicionando un System Message y un User Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Crear un Delegate que acepte la información de salida del modelo y la imprima en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* El plano completo se ve así; al ejecutar el plano, podrás ver en la pantalla del juego el mensaje que devuelve el modelo grande.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###El editor utiliza OpenAI Chat.

* Abre la herramienta de chat Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat Nuevo Chat, configura la sesión ChatApi como OpenAI, configura los parámetros de la interfaz.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

* Iniciar chat:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

* Cambia el modelo a gpt-4o / gpt-4o-mini para utilizar las funciones visuales de OpenAI para analizar imágenes.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###El editor utiliza OpenAI para procesar imágenes (crear/modificar/variar)

* Crear una nueva sesión de imagen en la herramienta de chat New Image Chat, modificar la configuración de la sesión a OpenAI y establecer los parámetros.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

* Crear imágenes

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

* Modifica la imagen, cambia el tipo de conversación de Image Chat a Edit y sube dos imágenes, una es la imagen original y la otra es la máscara donde las áreas transparentes (con el canal alfa en 0) indican los lugares que necesitan ser modificados.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

* Cambia el tipo de conversación de Image Chat a Variación y sube una imagen; OpenAI devolverá una variación de la imagen original.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Plano utiliza el modelo de chat de OpenAI.

* Haz clic derecho en el blueprint para crear un nodo `Send OpenAI Chat Request In World`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

* Crea un nodo de Opciones y configura `Stream=true, Api Key="tu clave de API de OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

* Crea mensajes, añadiendo una Mensaje del Sistema y un Mensaje del Usuario.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Crear un Delegate que acepte la información de salida del modelo y la imprima en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* El plano completo se ve así, ejecuta el plano y podrás ver en la pantalla del juego el mensaje devuelto por el gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###El plano utiliza OpenAI para crear imágenes.

* Haz clic derecho en el plano para crear un nodo `Send OpenAI Image Request` y establece `In Prompt="a beautiful butterfly"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

* Crea un nodo de Options y establece `Api Key="tu clave de API de OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

* Vincula el evento On Images y guarda las imágenes en el disco duro local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

* El plano completo se ve así; al ejecutar el plano, puedes ver la imagen guardada en la ubicación designada.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###El editor utiliza Azure

* Nueva Conversación (New Chat), cambia ChatApi a Azure y configura los parámetros de la API de Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

* Iniciar chat

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###Editor utiliza Azure para crear imágenes

* Nueva sesión de imagen (New Image Chat), cambie ChatApi a Azure y configure los parámetros de Api de Azure. Tenga en cuenta que si se trata del modelo dall-e-2, es necesario establecer los parámetros Quality y Stype en not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

* Comienza a chatear, deja que Azure cree la imagen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Usar Azure Chat en Blueprint

Crea el siguiente plano, configura las opciones de Azure, haz clic en ejecutar y podrás ver en la pantalla el mensaje de chat devuelto por Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Crear imágenes con Azure usando un plano.

Crea el siguiente plano, configura las Opciones de Azure, haz clic en ejecutar, si la creación de la imagen es exitosa, verás en la pantalla el mensaje "Create Image Done".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

Según la configuración del plano anterior, la imagen se guardará en la ruta D:\Dwnloads\butterfly.png.

## Claude

###El editor utiliza Claude para chatear y analizar imágenes.

* Nueva conversación (New Chat), cambiar ChatApi a Claude y configurar los parámetros de Api de Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

* Iniciar chat

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###El plano utiliza Claude para chatear y analizar imágenes.

* Haga clic derecho en el plano para crear un nodo `Enviar solicitud de chat a Claude`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

* Crea un nodo de Options y establece `Stream=true, Api Key="tu clave de API de Clude", Max Output Tokens=1024`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

* Crear Messages, crear Texture2D desde un archivo y crear AIChatPlusTexture desde Texture2D, añadir AIChatPlusTexture a Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

* Al igual que en el tutorial anterior, crea un Evento y muestra la información en la pantalla del juego.

* El plano completo se ve así; al ejecutar el plano, podrás ver en la pantalla del juego el mensaje que devuelve el gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Obtener Ollama

* Puedes obtener el paquete de instalación para la instalación local a través del sitio web de Ollama: [ollama.com](https://ollama.com/)

* Se puede utilizar Ollama a través de la interfaz de Ollama proporcionada por otras personas.

###El editor utiliza Ollama para chatear y analizar imágenes.

* Nueva conversación (New Chat), cambie ChatApi a Ollama y configure los parámetros de la Api de Ollama. Si es un chat de texto, configure el modelo como un modelo de texto, como llama3.1; si necesita procesar imágenes, configure el modelo como un modelo que soporte visión, por ejemplo moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

* Comenzar a chatear

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###El plano utiliza Ollama para chatear y analizar imágenes.

Crea el siguiente esquema, configura las opciones de Ollama, haz clic en ejecutar y podrás ver en pantalla la información del chat devuelta por Ollama.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###El editor utiliza Gemini

* Nueva conversación (New Chat), cambiar ChatApi a Gemini y configurar los parámetros de la API de Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

* Comenzar a chatear

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###El plano utiliza el chat de Gemini.

Crea el siguiente plano, configura las Opciones de Gemini, haz clic en ejecutar y podrás ver la información del chat devuelta por Gemini impresa en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

## Deepseek

###El editor utiliza Deepseek.

* Nueva conversación (New Chat), cambia ChatApi a OpenAi y configura los parámetros de la Api de Deepseek. Agrega modelos candidatos llamados deepseek-chat y configura el modelo a deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

* Comenzar a chatear

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Chat de Deepseek en el plano.

Crea el siguiente plano, configura las opciones de solicitud relacionadas con Deepseek, incluyendo parámetros como Modelo, URL base, URL de punto final, ApiKey, etc. Haz clic en ejecutar y podrás ver en la pantalla la información del chat devuelta por Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##Registro de cambios

### v1.5.0 - 2025.01.29

####Nuevas características

* Soporte para enviar audio a Gemini

* Las herramientas del editor permiten enviar audio y grabaciones.

#### Bug Fix

* Corregir el error de fallo en la copia de sesión.

### v1.4.1 - 2025.01.04

####Corrección de problemas

* La herramienta de chat solo admite el envío de imágenes sin mensajes.

* Reparar el problema de envío de imágenes en la interfaz de OpenAI.

* Arreglar el problema de omisión de los parámetros Quality, Style y ApiVersion en la configuración de la herramienta de chat de OpanAI y Azure.

### v1.4.0 - 2024.12.30

####Nuevas funciones

* （功能 experimental）Cllama(llama.cpp) soporta modelos multimodales y puede manejar imágenes.

* Todos los parámetros de tipo de plano han sido complementados con indicaciones detalladas.

### v1.3.4 - 2024.12.05

####Nuevas funciones

* OpenAI soporta la API de visión

####Corrección de problemas

* Corregir el error cuando OpenAI stream=false.

### v1.3.3 - 2024.11.25

####nuevas funciones

* Soporta UE-5.5

####Corrección de problemas

* Solucionar el problema de que algunos planos no surten efecto.

### v1.3.2 - 2024.10.10

####Corrección de problemas

* Reparar el colapso de cllama al detener la solicitud manualmente.

* Solucionar el problema de que no se encuentran los archivos ggml.dll y llama.dll en la versión de descarga de la tienda en el paquete win.

* Verifica si está en el GameThread al crear la solicitud, verificación de CreateRequest en el hilo del juego.

### v1.3.1 - 2024.9.30

####Nuevas funciones

* Agregar un SystemTemplateViewer, que permite ver y utilizar cientos de plantillas de configuración del sistema.

####Corrección de problemas

* Reparar el plugin descargado del centro comercial, no se puede encontrar la biblioteca vinculada llama.cpp.

* Reparar el problema de ruta demasiado larga en LLAMACpp

* Solucionar el error de enlace llama.dll después de empaquetar Windows.

* Reparar el problema de lectura de la ruta de archivos en ios/android.

* Corregir el error en el nombre de configuración de Cllame

### v1.3.0 - 2024.9.23

####Nuevas funciones importantes

* Se ha integrado llama.cpp, que soporta la ejecución local y fuera de línea de grandes modelos.

### v1.2.0 - 2024.08.20

####Nuevas funciones

* Soporte para OpenAI Image Edit/Image Variation

* Soporta la API de Ollama, permite obtener automáticamente la lista de modelos compatibles con Ollama.

### v1.1.0 - 2024.08.07

####Nuevas funcionalidades

* Apoyo a la plantilla

### v1.0.0 - 2024.08.05

####Nueva función

* Función completa básica

* Soporte para OpenAI, Azure, Claude, Gemini

* Herramienta de chat con un editor de funciones completas incorporado

--8<-- "footer_es.md"


> Este post fue traducido usando ChatGPT, por favor en [**retroalimentación**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
