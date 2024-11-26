---
layout: post
title: Documento de instrucciones del complemento AIChatPlus de la UE.
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
description: Documentación de UE Plug-in AIChatPlus
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documento de instrucciones del complemento UE AIChatPlus

##Repositorio público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complemento

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

Este complemento es compatible con UE5.2+. 

UE.AIChatPlus es un complemento de UnrealEngine que implementa la comunicación con varios servicios de chat de IA GPT. Actualmente, admite servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, llama.cpp para uso local sin conexión. En el futuro, seguirá agregando soporte para más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que garantiza un rendimiento eficiente y facilita a los desarrolladores de Unreal Engine conectarse a estos servicios de chat de IA.

Al mismo tiempo, UE.AIChatPlus también incluye una herramienta de edición que le permite utilizar directamente estos servicios de chat de IA en el editor para crear texto e imágenes, analizar imágenes, etc.

##Instrucciones de Uso

###Herramienta de chat del editor

El menú Tools -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


El software ofrece soporte para generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Función principal

* Modelo grande sin conexión: Integración de la biblioteca llama.cpp, que permite la ejecución sin conexión de modelos grandes a nivel local

* Chat de texto: haz clic en el botón `New Chat` en la esquina inferior izquierda para crear una nueva conversación de chat de texto.

* Generación de imágenes: haz clic en el botón `New Image Chat` en la esquina inferior izquierda para iniciar una nueva sesión de generación de imágenes.

* Análisis de imagen: Algunos servicios de chat de `New Chat` admiten el envío de imágenes, como Claude, Google Gemini. Simplemente haz clic en el botón 🖼️ o 🎨 sobre el cuadro de entrada para cargar la imagen que deseas enviar.

Apoyo para Blueprint: apoyo para crear solicitudes de API con Blueprint, realizando funciones como chat de texto, generación de imágenes, entre otras.

Establecer el rol actual de la conversación: El menú desplegable en la parte superior del cuadro de chat permite seleccionar el rol actual del texto enviado, lo que permite simular diferentes roles para ajustar la conversación de la IA.

Borrar conversación: Pulsar la ❌ en la parte superior de la ventana de chat borra el historial de mensajes de la conversación actual.

* Plantilla de diálogo: Incorpora cientos de plantillas de configuración de diálogo para facilitar el manejo de problemas comunes.

Translate these text into Spanish language:

* Configuración global: hace clic en el botón `Setting` en la esquina inferior izquierda para abrir la ventana de configuración global. Puedes definir el chat de texto predeterminado, el servicio de API para generar imágenes y establecer los parámetros específicos para cada servicio de API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Configuración de la conversación: Al hacer clic en el botón de configuración en la parte superior de la ventana de chat, se puede abrir la ventana de configuración de la conversación actual. Se admite cambiar el nombre de la conversación, modificar el servicio API utilizado en la conversación y configurar de forma independiente los parámetros específicos de API utilizados en cada conversación. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

Modificar contenido del chat: Al pasar el mouse sobre el contenido del chat, aparecerá un botón de configuración para dicho contenido, que permitirá regenerarlo, editarlo, copiarlo, eliminarlo o regenerar contenido debajo (para contenido generado por el usuario).

* Visor de imágenes: para la generación de imágenes, al hacer clic en una imagen se abrirá la ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como PNG/Textura UE, las texturas pueden verse directamente en el explorador de contenido (Content Browser), facilitando su uso dentro del editor. También se puede eliminar, regenerar o seguir generando más imágenes. Para los editores en Windows, también es posible copiar imágenes, lo que permite copiarlas directamente al portapapeles para un uso más conveniente. Las imágenes generadas en la sesión se guardarán automáticamente en la carpeta de cada sesión, generalmente en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Plan:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Configuración Global:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Ajustes de la conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modificar el contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visor de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Utilización de modelos grandes sin conexión

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Plantilla de diálogo

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introducción al código central

En la actualidad, el complemento se divide en los siguientes módulos:

* AIChatPlusCommon: Módulo de tiempo de ejecución (Runtime), encargado de manejar diferentes solicitudes de API de inteligencia artificial y analizar el contenido de las respuestas.

* AIChatPlusEditor: Módulo de editor, encargado de implementar la herramienta de chat de IA del editor.

* AIChatPlusCllama: Módulo de tiempo de ejecución (Runtime), encargado de encapsular la interfaz y los parámetros de llama.cpp, para lograr la ejecución offline de modelos grandes

* Thirdparty/LLAMACpp: Módulo de terceros en tiempo de ejecución (Runtime) que integra la biblioteca dinámica y los archivos de cabecera de llama.cpp.

Traduzca este texto al idioma español:

El UClass responsable específico de enviar la solicitud es FAIChatPlus_xxxChatRequest; cada servicio API tiene su propio UClass de solicitud independiente. Las respuestas a las solicitudes se obtienen a través de dos UClass diferentes, UAIChatPlus_ChatHandlerBase y UAIChatPlus_ImageHandlerBase; solo es necesario registrar los delegados de devolución de llamada correspondientes.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar, esto se hace a través de la FAIChatPlus_xxxChatRequestBody. La respuesta específica también se analiza en el FAIChatPlus_xxxChatResponseBody, y al recibir la devolución de llamada, se puede obtener el ResponseBody a través de una interfaz específica.

Más detalles del código fuente disponibles en la tienda de Unreal Engine: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Guía de uso

###Utilice el modelo fuera de línea llama.cpp con la herramienta del editor.

Traduce este texto al idioma español:

Instrucciones para usar el modelo sin conexión llama.cpp en la herramienta de edición AIChatPlus.

Descargue el modelo sin conexión desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloque el modelo en una carpeta específica, por ejemplo en el directorio Content/LLAMA del proyecto de juego.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Abra la herramienta de edición AIChatPlus: Herramientas -> AIChatPlus -> AIChat, cree una nueva sesión de chat y abra la página de configuración de la sesión.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Establece Api en Cllama, activa la Configuración de Api Personalizada, añade rutas de búsqueda de modelos y elige un modelo.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Comenzar a chatear!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###El código utiliza el modelo fuera de línea llama.cpp.

Translate these text into Spanish language:

La siguiente explicación muestra cómo utilizar el modelo offline llama.cpp en el código.

Primero, también necesitas descargar el archivo del modelo en Content/LLAMA.

Modifica el código para agregar un comando y enviar un mensaje al modelo sin conexión dentro del comando.

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

* Después de volver a compilar, simplemente utiliza el comando en el editor Cmd para ver los resultados de la salida del gran modelo en el registro OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Traduce este texto al español:

Diagrama de uso del modelo fuera de línea llama.cpp

La siguiente explicación detalla cómo usar el modelo fuera de línea llama.cpp en un blueprint.

En el blueprint, crea un nodo haciendo clic derecho llamado `Enviar solicitud de chat de Cllama`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Crear nodo de Options y establecer `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

* Cree mensajes, agregue un mensaje de sistema y un mensaje de usuario respectivamente

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

*Establecer un Delegado que reciba la salida del modelo e imprima en la pantalla*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Traduzca este texto al idioma español:

* La apariencia de un diseño completo es así; al ejecutarlo, se puede ver en la pantalla del juego el mensaje que devuelve la impresión del modelo grande.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##Registros de actualización

### v1.3.3 - 2024.11.25

Soporte para UE-5.5

### v1.3.2 - 2024.10.10

#### Bugfix

* Reparar el choque de cllama al detener manualmente la solicitud
Corregir el problema de no poder encontrar los archivos ggml.dll y llama.dll al empaquetar la versión de descarga de la tienda en Windows.
* Durante la creación de la solicitud, verificar si se encuentra en el GameThread.

### v1.3.1 - 2024.9.30

Añadir un SystemTemplateViewer que te permita ver y utilizar cientos de plantillas de configuración del sistema.

#### Bugfix

Reparar el complemento descargado desde la tienda, llama.cpp no puede encontrar la biblioteca de enlaces.
Corregir problema de ruta demasiado larga en LLAMACpp
Reparar el error de enlace llama.dll después de empaquetar en Windows
* Resolver problema de lectura de ruta de archivos en ios/android
Corregir el error de configuración del nombre de `Cllame`.

### v1.3.0 - 2024.9.23

Actualización importante

* Integración de llama.cpp, compatible con la ejecución local sin conexión de modelos grandes.

### v1.2.0 - 2024.08.20

Apoyar OpenAI Image Edit/Image Variation

Apoyo a la API de Ollama, apoyo para obtener automáticamente la lista de modelos admitidos por Ollama.

### v1.1.0 - 2024.08.07

Apoyar el plan.

### v1.0.0 - 2024.08.05

Función básica completa

Apoyo a OpenAI, Azure, Claude, Gemini.

* Herramienta de chat con editor incorporado totalmente funcional

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
