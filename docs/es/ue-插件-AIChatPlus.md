---
layout: post
title: 'Traduzca el texto a español:


  Documentación de la extensión UE AIChatPlus.'
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
description: 'Traduce este texto al español:


  Documento de instrucciones del complemento UE AIChatPlus'
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documento de instrucciones del complemento UE AIChatPlus

##Repositorio público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complemento

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

Esta extensión es compatible con UE5.2+.

UA.AIChatPlus es un complemento de UnrealEngine que permite la comunicación con diversos servicios de chat de inteligencia artificial GPT. Actualmente, admite servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, y llama.cpp en modo offline local. En el futuro, se seguirán añadiendo más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que garantiza un rendimiento eficiente y facilita la integración de estos servicios de chat de IA para los desarrolladores de Unreal Engine.

Al mismo tiempo, UE.AIChatPlus también incluye una herramienta de edición que permite utilizar directamente estos servicios de chat de IA en el editor para generar texto e imágenes, analizar imágenes, y más.

##Instrucciones de uso

###Herramienta de chat del editor

La barra de menú Herramientas -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


El soporte de la herramienta incluye generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es, en términos generales:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####**Función principal**

* Modelo grande sin conexión: Integración de la biblioteca llama.cpp para admitir la ejecución sin conexión de modelos grandes a nivel local

Crear un nuevo chat de texto: haz clic en el botón `New Chat` en la esquina inferior izquierda para iniciar una nueva conversación de texto.

* Generación de imágenes: haz clic en el botón `New Image Chat` en la esquina inferior izquierda para iniciar una nueva sesión de generación de imágenes.

Análisis de imágenes: Algunos servicios de chat de `New Chat` admiten el envío de imágenes, como Claude, Google Gemini. Simplemente haz clic en los botones 🖼️ o 🎨 encima del cuadro de entrada para cargar la imagen que deseas enviar.

* Apoyo a Blueprint: Apoyo para la creación de solicitudes de API de Blueprint, para funciones como chat de texto, generación de imágenes, entre otros.

Establecer el personaje de chat actual: El menú desplegable en la parte superior del cuadro de chat se puede utilizar para seleccionar el personaje actual que enviará el texto, lo que permite simular diferentes roles para ajustar la conversación de IA.

Borrar conversación: El botón ❌ en la parte superior de la ventana de chat permite eliminar el historial de mensajes de la conversación actual.

* Plantilla de diálogo: incorpora cientos de plantillas de configuración de diálogo para facilitar el manejo de problemas comunes.

Establecimientos globales: al hacer clic en el botón `Setting` en la esquina inferior izquierda, se abre la ventana de establecimientos globales. Puede configurar el chat de texto predeterminado, el servicio de API para generar imágenes y ajustar los parámetros específicos de cada servicio de API. Los establecimientos se guardarán automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Configuración de conversación: al hacer clic en el botón de configuración en la parte superior del cuadro de chat, se puede abrir la ventana de configuración de la conversación actual. Permite modificar el nombre de la conversación, el servicio de API utilizado en la conversación, y establecer parámetros específicos de API para cada conversación de manera independiente. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

* Modificación de contenido del chat: Al colocar el ratón sobre el contenido del chat, aparecerá un botón de configuración del contenido individual del chat, que permite regenerar, modificar, copiar o eliminar el contenido, así como regenerar contenido debajo (para el contenido de usuario).

* Exploración de imágenes: Para la generación de imágenes, al hacer clic en una imagen se abrirá la ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como PNG/UE Texture. Las Texturas se pueden ver directamente en el Explorador de contenido (Content Browser), facilitando su uso dentro del editor. También se cuenta con funciones para eliminar imágenes, regenerarlas, continuar generando más imágenes, entre otras. Para los editores en Windows, también se puede copiar imágenes, permitiendo copiarlas directamente al portapapeles para un uso conveniente. Las imágenes generadas en la sesión se guardarán automáticamente en la carpeta de cada sesión, generalmente en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Plan:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Configuración global:

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

* AIChatPlusCommon: El módulo de tiempo de ejecución, responsable de manejar las solicitudes de envío de diversas interfaces de API de IA y de analizar el contenido de las respuestas.

* AIChatPlusEditor: Módulo de edición, encargado de implementar la herramienta de chat de IA del editor.

* AIChatPlusCllama: Módulo de tiempo de ejecución (Runtime), encargado de encapsular la interfaz y los parámetros de llama.cpp, para llevar a cabo la ejecución sin conexión de grandes modelos.

* Thirdparty/LLAMACpp: Módulo de terceros en tiempo de ejecución (Runtime) que integra la biblioteca dinámica y archivos de cabecera de llama.cpp.

El UClass responsable de enviar las solicitudes es FAIChatPlus_xxxChatRequest, cada servicio API tiene su propio UClass de solicitud independiente. Las respuestas a las solicitudes se obtienen a través de UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase, solo es necesario registrar los delegados de devolución de llamada correspondientes.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar, esto se hace a través de FAIChatPlus_xxxChatRequestBody. El contenido específico de la respuesta también se analiza en FAIChatPlus_xxxChatResponseBody, se puede obtener el ResponseBody a través de una interfaz específica al recibir la devolución de llamada.

Más detalles del código fuente están disponibles en la tienda de Unreal Engine: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

###Guía de uso

####Utilice el modelo fuera de línea del editor de herramientas llama.cpp

Traduce este texto al idioma español:

El siguiente texto describe cómo utilizar el modelo offline llamado llama.cpp en la herramienta del editor AIChatPlus.

* En primer lugar, descarga el modelo sin conexión desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloque el modelo en una carpeta específica, por ejemplo, en el directorio Content/LLAMA del proyecto de juegos.

	```shell
	E:/UE/projects/FP_Test1/Content/LLAMA
	> ls
	qwen1.5-1_8b-chat-q8_0.gguf*
	```

Abre la herramienta de edición AIChatPlus: Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat y abre la página de ajustes de la sesión.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Establecer Api en Cllama, activar Configuraciones de Api Personalizadas, y agregar la ruta de búsqueda de modelos, luego seleccionar el modelo.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Comience la conversación!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

####El código utiliza el modelo offline llama.cpp

Traduce este texto al idioma español:

El siguiente documento describe cómo utilizar el modelo sin conexión llama.cpp en el código.

* Primero, también necesitas descargar el archivo del modelo en Content/LLAMA.

Modificar el código para agregar un comando y enviar un mensaje al modelo sin conexión dentro del comando.

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

* Después de volver a compilar, puedes ver los resultados de la salida del modelo grande en el registro de salida OutputLog al usar comandos en la ventana Cmd del editor.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

####La impresión azul utiliza el modelo fuera de línea llama.cpp

todo

###Actualización del registro

#### v1.3.1 - 2024.9.30

Agrega un SystemTemplateViewer que permita ver y utilizar cientos de plantillas de configuración de sistema.

##### Bugfix

Reparar el plugin descargado desde la tienda, llama.cpp no puede encontrar la biblioteca de enlaces.
修复 LLAMACpp 路径过长问题

Solucionar el problema de ruta demasiado larga de LLAMACpp
Reparar el error de enlace llama.dll después de empaquetar Windows
Corregir problema de lectura de ruta de archivos en iOS/Android.
* Corregido el error de configuración de Cllame establecer nombre

#### v1.3.0 - 2024.9.23

Actualización importante

* Integrado llama.cpp, compatible con la ejecución offline de grandes modelos localmente

#### v1.2.0 - 2024.08.20

Apoyo a OpenAI Image Edit / Image Variation

Apoya la API de Ollama, apoya la obtención automática de la lista de modelos admitidos por Ollama

#### v1.1.0 - 2024.08.07

Apoyar el plan.

#### v1.0.0 - 2024.08.05

Funcionalidad básica completa

Apoyo a OpenAI, Azure, Claude, Gemini.

* Herramienta de chat con editor integrado y funciones completas

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
