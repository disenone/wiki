---
layout: post
title: '# UE Plugin AIChatPlus Documentación


  '
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
description: Documentación de UE AIChatPlus Plugin
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE Plugin AIChatPlus Documento de Instrucciones

##Almacén público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtención del complemento

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Descripción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento de Unreal Engine que permite la comunicación con varios servicios de chat de IA de GPT. Actualmente, soporta servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama y llama.cpp para uso local sin conexión. En el futuro, se seguirán añadiendo más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, ofreciendo un rendimiento eficiente y facilitando a los desarrolladores de UE la integración de estos servicios de chat de IA.

Al mismo tiempo, UE.AIChatPlus también incluye una herramienta de edición que permite utilizar directamente estos servicios de chat con inteligencia artificial en el editor, generando texto e imágenes, analizando imágenes, entre otros.

##Instrucciones de uso

###Herramienta de chat del editor

La opción del menú Tools -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


La herramienta ofrece soporte para generar texto, chatear por texto, generar imágenes y analizar imágenes.

La interfaz de la herramienta es aproximadamente la siguiente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Funciones principales

* Modelo grande fuera de línea: integra la biblioteca llama.cpp, soporta la ejecución local y fuera de línea de modelos grandes.

Crear un nuevo chat de texto: haz clic en el botón `Nuevo chat` en la esquina inferior izquierda para iniciar una nueva conversación de texto.

* Generación de imágenes: haz clic en el botón `New Image Chat` en la esquina inferior izquierda para crear una nueva sesión de generación de imágenes.

Análisis de imágenes: Algunos servicios de chat en la función "Nuevo Chat" admiten el envío de imágenes, como Claude, Google Gemini. Simplemente haz clic en el ícono 🖼️ o 🎨 encima del cuadro de texto para cargar la imagen que quieres enviar.

Apoyo a Blueprint: Apoyo a la creación de Blueprint para realizar solicitudes de API, completar chat de texto, generación de imágenes, entre otras funciones.

* Configurar el rol actual del chat: el menú desplegable en la parte superior del cuadro de chat permite establecer el rol de los textos que se envían actualmente, lo que facilita ajustar la conversación de IA simulando diferentes personajes.

Vaciar la conversación: El botón ❌ en la parte superior de la ventana de chat permite borrar el historial de mensajes de la conversación actual.

* Plantilla de diálogo: incorpora cientos de plantillas de configuración de diálogo, facilitando el manejo de preguntas frecuentes.

Configuración global: haz clic en el botón `Setting` en la esquina inferior izquierda para abrir la ventana de configuración global. Aquí podrás establecer la configuración predeterminada para el chat de texto, el servicio de generación de imágenes mediante API y los parámetros específicos para cada tipo de servicio de API. Los ajustes se guardarán automáticamente en la carpeta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Configuración de la conversación: Haz clic en el botón de configuración en la parte superior del cuadro de chat para abrir la ventana de configuración de la conversación actual. Se puede modificar el nombre de la conversación, cambiar el servicio API utilizado en la conversación y ajustar de manera independiente los parámetros específicos que usa cada conversación. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

* Modificación del contenido del chat: Al pasar el mouse sobre el contenido del chat, aparecerá un botón de configuración para ese contenido específico, que permite regenerar el contenido, modificarlo, copiarlo, eliminarlo y regenerar contenido en la parte inferior (para el contenido cuyo rol es el de usuario).

Exploración de imágenes: para la generación de imágenes, al hacer clic en una imagen se abrirá una ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como PNG/UE Texture. Las texturas se pueden ver directamente en el navegador de contenido (Content Browser), facilitando su uso en el editor. También se admiten funciones como eliminar imágenes, regenerarlas, continuar generando más imágenes, entre otras. En el editor de Windows, también se puede copiar la imagen al portapapeles para facilitar su uso. Las imágenes generadas en la sesión se guardarán automáticamente en la carpeta de cada sesión, generalmente en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Plano:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Configuración general:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Configuración de la conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modificar el contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visor de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Uso de modelos grandes fuera de línea

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Plantilla de diálogo

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introducción al código central

Actualmente, el complemento se divide en los siguientes módulos:

AIChatPlusCommon: Módulo de tiempo de ejecución, encargado de manejar el envío de solicitudes a diversas interfaces de API de inteligencia artificial y de analizar el contenido de las respuestas.

AIChatPlusEditor: Módulo de Editor encargado de implementar la herramienta de chat de IA del editor.

* AIChatPlusCllama: Módulo de tiempo de ejecución (Runtime), encargado de encapsular la interfaz y los parámetros de llama.cpp, logrando la ejecución offline de grandes modelos.

Thirdparty/LLAMACpp: Un módulo de terceros en tiempo de ejecución que integra la biblioteca dinámica y archivos de cabecera de llama.cpp.

El UClass responsable de enviar las solicitudes específicas es FAIChatPlus_xxxChatRequest, cada servicio de API tiene su propio UClass de solicitud independiente. Las respuestas de las solicitudes se obtienen a través de las dos clases UClass UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase, solo necesitas registrar el delegado de callback correspondiente.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar; esto se realiza a través de FAIChatPlus_xxxChatRequestBody. El contenido específico de la respuesta también se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir la llamada de retorno, se puede obtener el ResponseBody a través de una interfaz específica.

Más detalles del código fuente pueden obtenerse en la tienda de UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Herramientas de editor utilizan el modelo offline Cllama (llama.cpp)

A continuación se explica cómo utilizar el modelo fuera de línea llama.cpp en la herramienta de edición AIChatPlus.

* Primero, descarga el modelo offline desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloca el modelo en una carpeta específica, como por ejemplo en el directorio Content/LLAMA del proyecto de juego.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Abre la herramienta de edición AIChatPlus: Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat y accede a la página de configuración de la sesión.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Establece la API en Cllama, activa la configuración personalizada de la API y agrega la ruta de búsqueda de modelos, luego elige un modelo.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

* ¡Comencemos a chatear!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Las herramientas del editor utilizan el modelo offline Cllama (llama.cpp) para procesar imágenes.

* Descargar el modelo offline MobileVLM_V2-1.7B-GGUF desde el sitio web de HuggingFace y colocarlo en el directorio Content/LLAMA: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)。

* Configurar el modelo de la sesión:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Enviar imágenes para iniciar una conversación.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###El código utiliza el modelo offline Cllama (llama.cpp)

A continuación se explica cómo utilizar el modelo offline llama.cpp en el código.

Primero, también es necesario descargar el archivo del modelo en la carpeta Content/LLAMA.

* Modificar el código para añadir un comando y enviar un mensaje al modelo offline dentro del comando.

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

Después de recompilar, simplemente utiliza el comando en el editor Cmd y podrás ver los resultados de la salida del modelo grande en el registro OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###El archivo llama.cpp utiliza el modelo fuera de línea del plan.

A continuación se explica cómo utilizar el modelo offline llama.cpp en Blueprint.

En el panel de control, haz clic derecho para crear un nodo llamado `Enviar solicitud de chat de Cllama`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

* Crear un nodo de Options y establecer `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Crear mensajes, agregar un mensaje del sistema y un mensaje del usuario en Messages. 

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Crear un Delegate que acepte la información de salida del modelo y la imprima en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

La traducción al español es la siguiente:

* La apariencia de un blueprint completo es la siguiente: luego de ejecutar el blueprint, podrás ver en la pantalla del juego el mensaje que devuelve la impresión de un gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###El editor utiliza OpenAI Chat.

Abre la herramienta de chat Tools -> AIChatPlus -> AIChat, crea una nueva conversación de chat New Chat, establece la conversación ChatApi como OpenAI, y configura los parámetros de la interfaz.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Comenzar conversación:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Cambiar el modelo a gpt-4o / gpt-4o-mini permite utilizar la función de análisis visual de imágenes de OpenAI.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###El editor utiliza OpenAI para procesar imágenes (crear/modificar/variar).

Crear una nueva conversación de imagen en la herramienta de chat, modificar la configuración de la conversación a OpenAI y establecer los parámetros.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

* Crear imagen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

* Modifica la imagen, cambia el tipo de conversación de Image Chat a Edit, y sube dos imágenes, una es la imagen original y la otra es la máscara en la que las áreas transparentes (canal alfa igual a 0) indican los lugares que necesitan ser modificados.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

* Cambia el tipo de conversación de Image Chat a Variación y sube una imagen; OpenAI te devolverá una variación de la imagen original.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Utilizando el modelo de chat de OpenAI para la creación de un plan de conversación.

En el diagrama, haz clic derecho para crear un nodo llamado `Enviar solicitud de chat OpenAI en el mundo`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

* Crea un nodo Options y establece `Stream=true, Api Key="tu clave de API de OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

* Crear mensajes, añadiendo un Mensaje del Sistema y un Mensaje del Usuario por separado.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Crear un Delegado que reciba la información de salida del modelo y la imprima en pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* El plano completo se ve así; al ejecutar el plano, podrás ver en la pantalla del juego el mensaje devuelto por el gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###El plano utiliza OpenAI para crear imágenes.

* Haz clic derecho en el plano para crear un nodo `Send OpenAI Image Request` y establece `In Prompt="a beautiful butterfly"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

* Crear un nodo de Options y configurar `Api Key="tu clave de API de OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

* Vincular el evento On Images y guardar las imágenes en el disco duro local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

El diseño completo se ve así, ejecuta el diseño y verás que la imagen se guarda en la ubicación especificada.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###El editor utiliza Azure.

* Nueva conversación (New Chat), cambia ChatApi a Azure y configura los parámetros de la API de Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Iniciar conversación.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###El editor utiliza Azure para crear imágenes.

Crear una nueva sesión de chat de imagen (New Image Chat), cambiar ChatApi a Azure y configurar los parámetros de la API de Azure. Ten en cuenta que si es el modelo dall-e-2, es necesario establecer los parámetros Quality y Stype en not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

* Comienza a chatear y deja que Azure cree imágenes.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Plano utiliza Azure Chat

Crea el siguiente plano, configura las Opciones de Azure, haz clic en ejecutar y podrás ver en la pantalla los mensajes de chat devueltos por Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Plano para crear imágenes con Azure

Crea el siguiente plano, configura las opciones de Azure y haz clic en ejecutar. Si la creación de la imagen es exitosa, verás en la pantalla el mensaje "Create Image Done".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

De acuerdo con la configuración del plano anterior, la imagen se guardará en la ruta D:\Descargas\mariposa.png.

## Claude

###El editor utiliza Claude para chatear y analizar imágenes.

Crear un nuevo chat, cambia ChatApi por Claude y configura los parámetros de la API de Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Comenzar conversación.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Utilizar el plano de Claude para chatear y analizar imágenes.

En el plano, haz clic derecho para crear un nodo llamado `Enviar solicitud de chat a Claude`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Crea un nodo de opciones y configura `Stream=true, Api Key="tu clave de API de Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Crear mensajes, crear Texture2D desde un archivo y luego utilizar esa Texture2D para crear AIChatPlusTexture, finalmente agregar AIChatPlusTexture al mensaje.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

* Al igual que en el tutorial anterior, crea un Evento y muestra la información en la pantalla del juego.

La traducción al español de este texto es:

"* La versión completa del diagrama de flujo se ve así, al ejecutar el diagrama de flujo, podrás ver en la pantalla del juego el mensaje que devuelve la impresión del modelo grande."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Obtener Ollama

Puede obtener el paquete de instalación para instalar localmente a través del sitio web oficial de Ollama: [ollama.com](https://ollama.com/)

Se puede utilizar Ollama a través de la interfaz de Ollama proporcionada por otra persona.

###El editor utiliza Ollama para chatear y analizar imágenes.

Crear una nueva conversación (New Chat), cambiar ChatApi a Ollama y configurar los parámetros de la API de Ollama. Si es un chat de texto, establecer el modelo como modelo de texto, como llama3.1; si es necesario procesar imágenes, configurar el modelo como un modelo compatible con visión, como moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

* Comenzar a chatear

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Utilizar Ollama para chatear y analizar imágenes en BluePrint.

Crea el siguiente plano, configura las opciones de Ollama, haz clic en ejecutar y podrás ver en la pantalla la información del chat devuelta por Ollama.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###El editor utiliza Gemini.

Crear una nueva conversación (New Chat), cambiar ChatApi a Gemini y configurar los parámetros de la API de Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

* Iniciar chat

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###El editor utiliza Gemini para enviar audio.

* Seleccionar Leer audio desde archivo / Leer audio desde Asset / Grabar audio desde micrófono, generar el audio que se necesita enviar.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

* Comenzar a chatear

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###Utiliza Gemini Chat en Blueprint.

Crea el siguiente plano, configura correctamente Gemini Options, haz clic en ejecutar y podrás ver los mensajes de chat devueltos por Gemini impresos en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###Utiliza Gemini para enviar audio en Blueprint.

Crear el siguiente plan, configurar la carga de audio, establecer las opciones de Gemini, hacer clic en ejecutar y podrás ver en la pantalla la información de chat devuelta por Gemini después de procesar el audio.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###Editor utiliza Deepseek

Crear una nueva conversación (New Chat), cambiar ChatApi por OpenAi y configurar los parámetros de la API de Deepseek. Agregar un nuevo modelo de candidato llamado deepseek-chat y configurar el modelo como deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Iniciar conversación.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Utiliza Deepseek en tu chat de Blueprints.

Para crear el siguiente plan, configure las opciones de solicitud relacionadas con Deepseek, incluyendo el Modelo, la URL base, la URL del punto final y el ApiKey. Haga clic en "Ejecutar" y podrá ver en pantalla la información de chat devuelta por Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##Registro de actualizaciones

### v1.5.1 - 2025.01.30

####Nueva característica

* Solo se permite que Gemini pronuncie audio.

Optimiza el método para obtener PCMData, descomprimiendo los datos de audio al generar B64.

* solicitud de añadir dos callbacks OnMessageFinished OnImagesFinished

* Optimizar el Método Gemini, obteniendo automáticamente el Método según bStream.

* Agregar algunas funciones de blueprint que faciliten la conversión de Wrapper a tipos reales y permitan obtener el Mensaje de Respuesta y el Error.

#### Bug Fix

* Corregir el problema de llamadas múltiples de Request Finish

### v1.5.0 - 2025.01.29

####Nueva funcionalidad

* Soporte para enviar audio a Gemini

Las herramientas del editor admiten el envío de audio y grabaciones.

#### Bug Fix

* Reparar el error de fallo en la copia de sesión

### v1.4.1 - 2025.01.04

####Reparación de problemas

Las herramientas de chat admiten enviar solo imágenes sin mensajes.

* Reparar el problema de envío de imágenes en la interfaz de OpenAI.

* Arreglar el problema de que en la configuración de la herramienta de chat de OpanAI y Azure faltan los parámetros Quality, Style, ApiVersion.

### v1.4.0 - 2024.12.30

####Nueva característica

* (Función experimental) Cllama (llama.cpp) admite modelos multimodales y puede procesar imágenes.

Todos los parámetros de tipo blueprint ahora vienen con instrucciones detalladas.

### v1.3.4 - 2024.12.05

####Nueva función

* OpenAI apoya la API de visión

####Corrección de problemas

* Corregir el error cuando OpenAI stream=false

### v1.3.3 - 2024.11.25

####Nueva función

* Soporte para UE-5.5

####Corrección de problemas

Corregir el problema de que algunas de las plantillas no están funcionando correctamente.

### v1.3.2 - 2024.10.10

####Solución de problemas

Reparar el fallo de cllama que ocurre al detener manualmente la solicitud.

Corregir el problema de la versión de descarga de la tienda donde no se encuentra el archivo ggml.dll o llama.dll en el paquete win.

* Verificar si está en GameThread al crear la solicitud, CrearSolicitud verificar en el hilo del juego.

### v1.3.1 - 2024.9.30

####Nuevas funciones

* Agregar un SystemTemplateViewer, que permita ver y utilizar cientos de plantillas de configuración del sistema.

####Reparación de problemas

Reparar el complemento descargado desde la tienda, llama.cpp no encuentra la biblioteca de enlace.

* Solucionar el problema de la ruta demasiado larga en LLAMACpp

* Reparar el error de enlace llama.dll después de empaquetar en Windows

Corregir problema de lectura de ruta de archivos en iOS/Android.

* Reparar el error en el nombre de configuración de Cllame

### v1.3.0 - 2024.9.23

####Funcionalidades importantes

* Integra llama.cpp, soportando la ejecución local y offline de grandes modelos.

### v1.2.0 - 2024.08.20

####Nueva funcionalidad

Apoyo a OpenAI Image Edit/Image Variation.

* Soporte para la API de Ollama, permite obtener automáticamente la lista de modelos soportados por Ollama.

### v1.1.0 - 2024.08.07

####Nueva función

Apoyo a la propuesta decisiva.

### v1.0.0 - 2024.08.05

####Nueva función.

* Funcionalidad completa básica

* Soporte para OpenAI, Azure, Claude, Gemini

* Editor de chat con funciones completas integradas.

--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor [**proporcionar comentarios**](https://github.com/disenone/wiki_blog/issues/new)Señalar cualquier omisión. 
