---
layout: post
title: Documento de instrucciones del complemento AIChatPlus de UE.
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
description: Documento de instrucciones del complemento UE AIChatPlus.
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documento de instrucciones del complemento UE AIChatPlus

##Repositorio público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complemento

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento de UnrealEngine que permite la comunicación con diversos servicios de chat de inteligencia artificial GPT. Actualmente admite servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, llama.cpp y modo offline local. En el futuro, se agregarán más proveedores de servicios compatibles. Su implementación se basa en solicitudes REST asíncronas, lo que garantiza un rendimiento eficiente y facilita la integración de estos servicios de chat de IA para desarrolladores de Unreal Engine.

Al mismo tiempo, UE.AIChatPlus también incluye una herramienta de edición que te permite utilizar directamente estos servicios de chat AI en el editor para generar texto e imágenes, analizar imágenes, etc.

##**Instrucciones de uso**

###Herramienta de chat del editor

El menú Tools -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


El software cuenta con funciones para la creación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Funciones principales

* Modelo de gran tamaño sin conexión: Integración de la biblioteca llama.cpp, compatible con la ejecución sin conexión de modelos de gran tamaño.

* Chat de texto: haz clic en el botón `Nuevo Chat` en la esquina inferior izquierda para crear una nueva sesión de chat de texto.

* Generación de Imágenes: Haz clic en el botón `New Image Chat` en la esquina inferior izquierda para iniciar una nueva sesión de generación de imágenes.

* Análisis de imágenes: Algunos servicios de chat en "New Chat" admiten el envío de imágenes, como Claude y Google Gemini. Simplemente haz clic en el botón 🖼️ o 🎨 encima del cuadro de texto para cargar la imagen que deseas enviar.

Translate these text into Spanish language:

* **Soporte de Blueprint**: Compatible con la creación de solicitudes de API de Blueprint para funciones como chat de texto, generación de imágenes, entre otros.

Establecer el rol de chat actual: el menú desplegable en la parte superior del cuadro de chat te permite seleccionar el rol actual para enviar texto, lo que te permite simular diferentes roles para ajustar la conversación de la IA.

Eliminar conversación: al hacer clic en la cruz en la parte superior de la ventana de chat, se eliminará el historial de mensajes de la conversación actual.

* Plantilla de diálogo: incorpora cientos de plantillas de configuración de diálogo para facilitar el manejo de problemas comunes.

Traduzca este texto al idioma español:

* Configuración global: al hacer clic en el botón `Setting` en la esquina inferior izquierda, puedes abrir la ventana de configuración global. Puedes establecer el chat de texto predeterminado, el servicio de API de generación de imágenes y configurar los parámetros específicos de cada servicio de API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Translate these text into Spanish language:

* Configuración de la conversación: al hacer clic en el botón de configuración en la parte superior del cuadro de chat, se puede abrir la ventana de configuración de la conversación actual. Permite cambiar el nombre de la conversación, modificar el servicio API utilizado en la conversación, y configurar de forma independiente los parámetros específicos de la API para cada conversación. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

* Edición de contenido de chat: Al desplazar el ratón sobre el contenido del chat, aparecerá un botón de configuración para ese contenido específico, que permite regenerar, modificar, copiar o eliminar el contenido, así como regenerar contenido debajo (para el contenido del usuario).

* Visualización de imágenes: Para la generación de imágenes, al hacer clic en una imagen se abrirá la ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como PNG/UE Texture. Las texturas se pueden ver directamente en el explorador de contenido (Content Browser), facilitando su uso en el editor. También se ofrecen funciones para eliminar imágenes, regenerarlas o seguir generando más. En el editor de Windows, también es posible copiar imágenes al portapapeles para un uso conveniente. Las imágenes generadas durante la sesión se guardan automáticamente en la carpeta de cada sesión, generalmente en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Plan:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Configuración general:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Configuración de la conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modificar contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visor de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Utilización de modelos grandes sin conexión

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Plantilla de diálogo

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Presentación del código principal

En la actualidad, el complemento se divide en los siguientes módulos:

* AIChatPlusCommon: Módulo en tiempo de ejecución (Runtime) encargado de manejar el envío de solicitudes a diversas API de inteligencia artificial y analizar el contenido de las respuestas.

* AIChatPlusEditor: Módulo del editor, encargado de implementar la herramienta de chat de inteligencia artificial en el editor.

* AIChatPlusCllama: Módulo de tiempo de ejecución (Runtime), responsable de encapsular la interfaz y los parámetros de llama.cpp, para lograr la ejecución fuera de línea de modelos grandes.

* Thirdparty/LLAMACpp: Módulo de tercero (Thirdparty) en tiempo de ejecución (Runtime) que integra la biblioteca dinámica y archivos de cabecera de llama.cpp.

Traduce este texto al idioma español:

La UClass específica encargada de enviar las solicitudes es FAIChatPlus_xxxChatRequest, cada servicio de API tiene su propia UClass de solicitud independiente. Las respuestas de las solicitudes se obtienen a través de dos tipos de UClass: UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase, solo es necesario registrar el delegado de callback correspondiente.

Antes de enviar una solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar, esto se hace mediante el FAIChatPlus_xxxChatRequestBody. La respuesta específica también se analiza en el FAIChatPlus_xxxChatResponseBody, que se puede obtener a través de una interfaz específica al recibir la devolución de llamada.

Puedes obtener más detalles sobre el código fuente en la tienda de Unreal Engine: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Utiliza el modelo offline de la herramienta del editor Cllama(llama.cpp)

Traduce este texto al idioma español:

Las siguientes instrucciones detallan cómo utilizar el modelo sin conexión llama.cpp en la herramienta de edición AIChatPlus.

Descarga primero el modelo offline desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloca el modelo en una carpeta específica, por ejemplo en la carpeta Content/LLAMA del proyecto del juego.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Abre la herramienta de edición AIChatPlus: Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat y abre la página de configuración de la sesión.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Establece Api en Cllama, activa la Configuración Personalizada de Api, y agrega la ruta de búsqueda de modelos, luego selecciona el modelo.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Comienza a conversar!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Utiliza la herramienta del editor para procesar imágenes con el modelo sin conexión Cllama(llama.cpp).

Descarga el modelo MobileVLM_V2-1.7B-GGUF de forma local desde el sitio web de HuggingFace y colócalo en el directorio Content/LLAMA: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)Traduzca este texto al idioma español:

 和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf).

Establecer el modelo de sesión:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Enviar imágenes para iniciar una conversación.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###Traduce este texto al español:

El código utiliza el modelo offline Cllama(llama.cpp)

A continuación se explica cómo usar el modelo offline llama.cpp en el código.

* Primero, también necesitas descargar el archivo del modelo en Content/LLAMA.

* Modificar el código para agregar un comando y enviar un mensaje al modelo sin conexión dentro del comando.

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

* Después de recompilar, puedes ver los resultados de la salida del modelo grande en el registro OutputLog al usar comandos en el editor Cmd.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###El archivo blueprint usa el modelo offline llama.cpp.

Traduce este texto al idioma español:

Following the explanation of how to use the offline model llama.cpp in a blueprint.

Crea un nodo `Enviar Solicitud de Chat de Cllama` con el botón derecho del ratón en el diagrama.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Cree el nodo de Opciones y establezca `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

* Crear mensajes, añadir un mensaje del sistema y un mensaje de usuario.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Crea un Delegado que acepte la salida del modelo e imprímala en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Traduce este texto al idioma español:

* El aspecto completo del blueprint es este, al ejecutarlo se puede ver el mensaje devuelto en la pantalla del juego, imprimiendo un modelo a gran escala.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###El editor utiliza OpenAI para chatear

Abre la herramienta de chat Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat Nuevo Chat, establece la sesión ChatApi en OpenAI, configura <api_key>

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

* Comienzo de la conversación:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Cambiar el modelo a gpt-4o / gpt-4o-mini, permitirá utilizar la funcionalidad de visión de OpenAI para analizar imágenes.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###Traduce estos textos al idioma español:

El editor utiliza OpenAI para procesar imágenes (crear/modificar/variaciones)

*En la función de Chat Fear, crea una nueva sesión de imagen New Image Chat, modifica la configuración de la sesión a OpenAI y configura <api_key>.*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Crear imagen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

* Modifica la imagen, cambia el tipo de chat de imagen a Edit, y sube dos imágenes, una es la imagen original, y la otra es la máscara donde las áreas transparentes (canal alfa igual a 0) indican las zonas que necesitan ser modificadas.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

* **Variante de imagen: cambiar el tipo de chat de imagen a 'Editar' y cargar una imagen. OpenAI devolverá una variante de la imagen original.**

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###La conversación con el modelo de OpenAI Blueprint

* En el proyecto, haz clic derecho para crear un nodo llamado `Enviar solicitud de chat de OpenAI en el mundo`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

*Crear nodo de Opciones y establecer `Stream=true, Clave API="tu clave API de OpenAI"`*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

*Crear Mensajes, agregue un Mensaje del Sistema y un Mensaje del Usuario respectivamente*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

*Crear un Delegado que reciba la información de salida del modelo y la imprima en la pantalla*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Traduce este texto al español:

* La apariencia completa del plan se ve así, ejecuta el plan y verás en la pantalla del juego el mensaje que devuelve al imprimir el gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Elaborar una imagen utilizando OpenAI.

Crea un nodo `Send OpenAI Image Request` haciendo clic derecho en el diagrama y establece `In Prompt="a beautiful butterfly"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Cree el nodo Options y establezca `Api Key="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Vincula el evento "On Images" y guarda las imágenes en el disco duro local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

Traduce este texto al idioma español:

* La apariencia completa del diseño se ve así, al ejecutar el diseño, se puede ver que la imagen se guarda en la ubicación especificada.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###El editor utiliza Azure.

* Crear nueva conversación (New Chat), cambiar ChatApi a Azure y configurar los parámetros de la API de Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

*Comienza a chatear*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###El editor utiliza Azure para crear imágenes.

* Crear una nueva sesión de imagen (New Image Chat), cambiar ChatApi a Azure, y configurar los parámetros de la API de Azure. Ten en cuenta que si se trata del modelo dall-e-2, es necesario establecer los parámetros Quality y Stype en not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

* Comience la conversación para que Azure cree la imagen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Utilice Azure Chat en sus diseños.

Crea el siguiente diagrama, configura las Opciones de Azure, haz clic en Ejecutar y verás en la pantalla impresa la información de chat devuelta por Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Crear imágenes con Azure utilizando blueprints.

Crea el siguiente diagrama, configura las Opciones de Azure, haz clic en Ejecutar, si la creación de la imagen tiene éxito, verás el mensaje "Crear Imagen Completado" en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

De acuerdo con la configuración del diagrama anterior, la imagen se guardará en la ruta D:\Descargas\mariposa.png.

## Claude

###El editor utiliza Claude para chatear y analizar imágenes.

* Nueva Conversación (New Chat), cambia ChatApi a Claude, y configura los parámetros de la Api de Claude

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

* Comenzar la conversación

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Traduce este texto al idioma español:

 El plan utiliza a Claude para conversar y analizar imágenes

Crea un nodo llamado `Enviar Solicitud de Chat a Claude` haciendo clic derecho en el mapa.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

*Crear un nodo de Opciones y establecer `Sensor=true, Clave de API="tu clave de API de Clude", Máximo de Tokens de Salida=1024`.*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

*Crear Messages, crear Texture2D desde un archivo, y a partir de Texture2D crear AIChatPlusTexture, luego añadir AIChatPlusTexture a Message*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

* Al igual que en el tutorial anterior, crea un Event y muestra la información en la pantalla del juego.

Traduce este texto al idioma español:

* La apariencia completa del plano es esta, al ejecutar el plano, podrás ver en la pantalla del juego el mensaje devuelto al imprimir el gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Obtener Ollama

Puede obtener el paquete de instalación localmente a través del sitio web oficial de Ollama: [ollama.com](https://ollama.com/)

Puede utilizar Ollama a través de la interfaz Ollama proporcionada por otra persona.

###El editor utiliza Ollama para chatear y analizar imágenes.

* Nuevo Chat, cambie ChatApi a Ollama y configure los parámetros Api de Ollama. Si se trata de un chat de texto, configure el modelo como el modelo de texto, como llama3.1; si es necesario procesar imágenes, configure el modelo como un modelo compatible con vision, por ejemplo, moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Comenzar a chatear

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Traduce este texto al español:

Diagrama utilizando Ollama para chatear y analizar imágenes

Crea el siguiente esquema, configura las opciones de Ollama, haz clic en ejecutar y verás la información de chat que devuelve Ollama impresa en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###El editor utiliza Gemini

* Crear una nueva conversación (New Chat), cambiar ChatApi a Gemini y configurar los parámetros de la Api de Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

**Comenzar a chatear**

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Utiliza la aplicación "Gemini Chat" para el diseño de tu proyecto.

Cree el siguiente esquema, configure las Opciones de Gemini, haga clic en Ejecutar y verá la información del chat que Gemini devuelve impresa en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)


##Registro de actualizaciones

### v1.4.1 - 2025.01.04

####Reparación de problemas

Utiliza la herramienta de chat que te permita enviar solo imágenes sin texto.

* Reparar el problema de envío de imágenes en la interfaz de OpenAI falló. 

Reparar el problema de configuración omitida de los parámetros Quality, Style, ApiVersion en OpanAI y Azure herramientas de chat.

### v1.4.0 - 2024.12.30

####Nueva funcionalidad

* (Función experimental) Cllama (llama.cpp) admite modelos multimodales y puede procesar imágenes.

Todos los parámetros del tipo Blueprint ahora cuentan con indicaciones detalladas.

### v1.3.4 - 2024.12.05

####Nueva característica

* OpenAI supporta la API de visión.

####Reparación de problemas

Corregir el error en OpenAI cuando stream=false

### v1.3.3 - 2024.11.25

####Nueva característica

* Soporte UE-5.5

####Resolución de problemas

Reparar problemas en los que algunas partes de los planos no funcionaban.

### v1.3.2 - 2024.10.10

####Solución de problemas

Reparar el error de cllama que ocurre al detener manualmente la solicitud.

Corregir el problema de la versión de descarga de Win en la tienda donde no se puede encontrar el archivo ggml.dll llama.dll.

* Durante la creación de la solicitud, se verifica si se encuentra en el hilo del juego, CreateRequest revisa en el hilo del juego.

### v1.3.1 - 2024.9.30

####Nueva funcionalidad.

Añadir un SystemTemplateViewer, que permite ver y usar cientos de plantillas de configuración del sistema.

####Reparación de Problemas

* Reparando el complemento descargado desde la tienda, llama.cpp no puede encontrar la biblioteca de enlaces.

Corregir problema de ruta demasiado larga en LLAMACpp

* Corregir el error de enlace llama.dll después de empaquetar en Windows

* Corregir problema de lectura de ruta de archivo en ios/android

Corregir el error de configuración de nombre de Cllame

### v1.3.0 - 2024.9.23

####Traduce este texto al idioms español:

 New significant feature

Se ha integrado llama.cpp para admitir la ejecución local sin conexión de grandes modelos.

### v1.2.0 - 2024.08.20

####Nueva característica

Apoyo a la Edición de Imágenes/Variación de Imágenes de OpenAI

Respaldar Ollama API, respaldar la recuperación automática de la lista de modelos admitidos por Ollama.

### v1.1.0 - 2024.08.07

####Nueva función

Apoyo al plan.

### v1.0.0 - 2024.08.05

####Nueva funcionalidad

* Funcionalidad básica completa

Apoyo a OpenAI, Azure, Claude, Gemini

* Herramienta de chat con editor integrado y funciones completas

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
