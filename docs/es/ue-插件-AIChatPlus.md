---
layout: post
title: Documento de instrucciones del complemento UE AIChatPlus
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
description: Manual de instrucciones del complemento UE AIChatPlus
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documentación de UE AIChatPlus Plugin

##Depósito público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complemento

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento de UnrealEngine que implementa la comunicación con varios servicios de chat de IA GPT. Actualmente admite servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama y llama.cpp en modo offline local. En el futuro seguirá agregando soporte para más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que lo hace eficiente y conveniente para que los desarrolladores de Unreal Engine se integren con estos servicios de chat de IA.

UE.AIChatPlus también incluye una herramienta de edición que permite utilizar directamente los servicios de chat de AI en el editor para generar texto e imágenes, y analizar imágenes, entre otras funciones.

##Instrucciones de uso

###Herramienta de chat del editor.

El menú Herramientas -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


El software ofrece funciones de generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Función principal

* Modelo grande sin conexión: Integración de la biblioteca llama.cpp para admitir la ejecución sin conexión de modelos grandes a nivel local

* Chat de texto: haz clic en el botón `Nuevo Chat` en la esquina inferior izquierda para crear una nueva sesión de chat de texto.

* Generación de imágenes: haz clic en el botón `New Image Chat` en la esquina inferior izquierda para crear una nueva sesión de generación de imágenes.

Análisis de imágenes: Algunos servicios de chat en la función 'New Chat' admiten el envío de imágenes, como Claude, Google Gemini. Simplemente haz clic en los botones 🖼️ o 🎨 encima del cuadro de entrada para cargar la imagen que deseas enviar.

* Soporte de Blueprint: permite la creación de solicitudes de API con Blueprint para funciones como chat de texto, generación de imágenes, entre otras.

Establecer el rol actual de la conversación: El menú desplegable en la parte superior del cuadro de chat permite seleccionar el rol actual para enviar mensajes, lo que permite simular diferentes roles para ajustar la conversación con IA.

Eliminar chat: Pulsar la ✖️ en la parte superior de la ventana del chat permite borrar el historial de mensajes de la conversación actual.

* Plantilla de diálogo: incorpora cientos de configuraciones de diálogo para facilitar el manejo de problemas comunes.

* Configuración global: al hacer clic en el botón `Setting` en la esquina inferior izquierda, se abrirá la ventana de configuración global. Puede configurar el chat de texto predeterminado, los servicios de API de generación de imágenes y establecer los parámetros específicos de cada servicio de API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Translate these text into Spanish language:

* **Configuración de la conversación:** Haga clic en el botón de configuración en la parte superior del cuadro de chat para abrir la ventana de configuración de la conversación actual. Permite modificar el nombre de la conversación, cambiar el servicio API utilizado en la conversación y configurar parámetros específicos del API para cada conversación por separado. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

Modificar el contenido del chat: al pasar el ratón por encima del contenido del chat, aparecerá un botón de configuración para ese contenido específico, que permitirá regenerar, modificar, copiar o eliminar el contenido, así como regenerar el contenido debajo (en el caso de que el personaje sea un usuario).

* Visualización de imágenes: para la generación de imágenes, al hacer clic en una imagen se abrirá una ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como PNG/UE Texture. Las Textures se pueden ver directamente en el Explorador de contenido (Content Browser), facilitando su uso en el editor. También es posible eliminar imágenes, regenerarlas, continuar generando más imágenes, entre otras funciones. Para los editores en Windows, también se puede copiar imágenes para así tenerlas disponibles en el portapapeles, lo que facilita su uso. Las imágenes generadas durante una sesión también se guardarán automáticamente en la carpeta de cada sesión, generalmente en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Blueprint:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Configuración general:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Configuración de la conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modificar el contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visor de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Utilización de modelos grandes sin conexión

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Plantilla de diálogo

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Presentación del código principal

En la actualidad, el complemento se divide en los siguientes módulos:

* AIChatPlusCommon: Módulo de tiempo de ejecución (Runtime), encargado de manejar solicitudes de envío de diversas interfaces de API de IA y analizar el contenido de las respuestas.

* AIChatPlusEditor: Módulo de editor, encargado de implementar la herramienta de chat AI del editor.

* AIChatPlusCllama: Módulo de tiempo de ejecución (Runtime), responsable de encapsular la interfaz y los parámetros de llama.cpp, para llevar a cabo la ejecución de modelos grandes sin conexión.

* Thirdparty/LLAMACpp: Módulo de terceros en tiempo de ejecución (Runtime) que integra la biblioteca dinámica y archivos de cabecera de llama.cpp.

Traduce estos textos al idioma español:

El UClass específico responsable de enviar la solicitud es FAIChatPlus_xxxChatRequest, cada tipo de servicio API tiene su propio UClass de solicitud independiente. Las respuestas de las solicitudes se obtienen a través de dos tipos de UClass, UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase, solo necesitas registrar el delegado de devolución de llamada correspondiente.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar. Esto se hace mediante FAIChatPlus_xxxChatRequestBody. El contenido específico de la respuesta también se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir la llamada de vuelta, se puede obtener el ResponseBody a través de una interfaz específica.

Más detalles del código fuente están disponibles en la tienda de UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Guía de uso

###Utiliza el modelo fuera de línea del editor de herramientas llama.cpp.

Traduce este texto al idioma español:

**Instrucciones sobre cómo utilizar el modelo offline llama.cpp en la herramienta de edición AIChatPlus**

Descargue el modelo sin conexión desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloca el modelo en una carpeta específica, por ejemplo, dentro del directorio del proyecto de juego Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Abre la herramienta de edición AIChatPlus: Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat y abre la página de configuración de la sesión.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Establecer Api como Cllama, activar Configuración Personalizada de Api y agregar la ruta de búsqueda de modelos, luego seleccionar un modelo.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Comience a chatear!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###El código utiliza el modelo fuera de línea llama.cpp

Traduce este texto al español:

El siguiente texto explica cómo usar el modelo fuera de línea llama.cpp en el código.

Primero, también necesitas descargar el archivo del modelo en Content/LLAMA.

Añade una línea de código para incluir un comando y enviar un mensaje al modelo fuera de línea desde dicho comando.

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

* Después de volver a compilar, puedes utilizar comandos en la terminal del editor para ver los resultados de la salida del modelo grande en el registro OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###La utilización de un modelo fuera de línea en el archivo llama.cpp.

La siguiente descripción explica cómo utilizar el modelo offline llama.cpp en un blueprint.

Crea un nodo `Send Cllama Chat Request` haciendo clic derecho en el diagrama.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Cree el nodo Options y configure `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

* Crea Mensajes, añade un Mensaje de Sistema y un Mensaje de Usuario respectivamente

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Establecer un delegado que reciba la información de salida del modelo y la imprima en la pantalla

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Translate these text into Spanish language: 

* El aspecto de un diagrama completo es así, al ejecutarlo, verá en la pantalla del juego el mensaje devuelto al imprimir el gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##Registro de actualizaciones

### v1.3.1 - 2024.9.30

Agregar un SystemTemplateViewer que permita ver y utilizar cientos de plantillas de configuración del sistema.

#### Bugfix

Repare el complemento descargado desde la tienda, no se encuentra la biblioteca de enlace llamada llama.cpp
Corregir problema de ruta demasiado larga en LLAMACpp
Reparar el error llama.dll después de empaquetar en Windows.
* Resolver problema de lectura de ruta de archivo en ios/android
Corregir el error de configuración del nombre de Cllame.

### v1.3.0 - 2024.9.23

Actualización importante

* Se ha integrado llama.cpp, lo que permite la ejecución offline de grandes modelos localmente

### v1.2.0 - 2024.08.20

Apoyo a OpenAI Image Edit/Image Variation.

Apoyar la API de Ollama, apoyar la obtención automática de la lista de modelos admitidos por Ollama

### v1.1.0 - 2024.08.07

Apoyo al plan.

### v1.0.0 - 2024.08.05

* Funcionalidad completa y básica

Apoyo a OpenAI, Azure, Claude, Gemini.

* Herramienta de chat con un editor incorporado completa

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
