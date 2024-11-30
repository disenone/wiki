---
layout: post
title: Documentación sobre el complemento UE AIChatPlus.
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

#Documento de instrucciones del complemento AIChatPlus de UE

##Almacén público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complemento.

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento de UnrealEngine que permite la comunicación con varios servicios de chat basados en inteligencia artificial GPT. Actualmente, soporta servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama y llama.cpp para uso local sin conexión a internet. En el futuro, se añadirá soporte para más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que garantiza un alto rendimiento y facilita la integración de estos servicios de chat AI para los desarrolladores de Unreal Engine.

UE.AIChatPlus también incluye una herramienta de edición que te permite utilizar los servicios de chat de IA directamente en el editor, para generar texto, imágenes, analizar imágenes, ¡y mucho más!

##Instrucciones de uso

###Herramienta de chat del editor

La opción Tools -> AIChatPlus -> AIChat en la barra de menú abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


El software ofrece capacidad para generar texto, chatear por texto, crear imágenes y analizar imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Principales funciones

* Modelo de gran tamaño sin conexión: integración de la biblioteca llama.cpp, compatible con la ejecución sin conexión de modelos de gran tamaño a nivel local

* Chat de texto: Haz clic en el botón `Nuevo chat` en la esquina inferior izquierda para crear una nueva conversación de chat de texto.

* Generación de imágenes: haz clic en el botón `Nuevo chat de imagen` en la esquina inferior izquierda para crear una nueva sesión de generación de imágenes.

Análisis de imágenes: Algunos servicios de chat en 'New Chat' admiten el envío de imágenes, como Claude y Google Gemini. Simplemente haz clic en el botón 🖼️ o 🎨 encima del cuadro de entrada para cargar la imagen que deseas enviar.

* Soporte de Blueprint: admite la creación de solicitudes de API de Blueprint para completar funciones como chat de texto, generación de imágenes, entre otros.

Establecer el personaje de chat actual: El menú desplegable en la parte superior de la caja de chat puede configurar el personaje actual para enviar texto, permitiendo simular diferentes personajes para ajustar la conversación AI.

Borrar chat: El botón ❌ en la parte superior de la ventana de chat permite borrar el historial de mensajes de la conversación actual.

Plantilla de diálogo: Incorpora cientos de plantillas de configuración de diálogo para facilitar el manejo de problemas comunes.

Traduce este texto al idioma español:

* 全局设置：Haz clic en el botón `Setting` en la esquina inferior izquierda para abrir la ventana de configuración global. Puedes establecer el chat de texto predeterminado, el servicio de API para generación de imágenes y configurar los parámetros específicos de cada servicio de API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

**Configuración de la conversación:** Al hacer clic en el botón de configuración en la parte superior de la ventana de chat, puedes abrir la ventana de configuración de la conversación actual. Permite modificar el nombre de la conversación, cambiar el servicio API utilizado en la conversación, y ajustar los parámetros específicos del API para cada conversación de manera independiente. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

* Modificación del contenido del chat: al pasar el ratón sobre el contenido del chat, aparecerá un botón de configuración para ese contenido en particular, con opciones para regenerarlo, editarlo, copiarlo, eliminarlo y regenerarlo debajo (si el autor es el usuario).

* Visualización de imágenes: Para la generación de imágenes, al hacer clic en una imagen se abrirá una ventana de visualización de imágenes (ImageViewer), que admite guardar la imagen como PNG/Textura UE, las texturas se pueden ver directamente en el explorador de contenido (Content Browser) para facilitar su uso dentro del editor. También se admiten funciones como eliminar imágenes, regenerar imágenes, continuar generando más imágenes, entre otras. Para el editor en Windows, también se admite copiar imágenes, lo que permite copiarlas directamente al portapapeles para facilitar su uso. Las imágenes generadas en la sesión se guardarán automáticamente en la carpeta de cada sesión, generalmente en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Blueprint:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Ajustes generales:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Configuración de la conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modificar el contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visor de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Utilizar modelos grandes sin conexión

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Plantilla de diálogo

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introducción al código principal

En este momento, el complemento se divide en los siguientes módulos:

* AIChatPlusCommon: Módulo en tiempo de ejecución (Runtime), encargado de manejar las solicitudes de envío de interfaces de API de inteligencia artificial y analizar el contenido de las respuestas.

* AIChatPlusEditor: Módulo de editor, responsable de implementar la herramienta de chat de IA del editor.

* AIChatPlusCllama: Módulo de tiempo de ejecución (Runtime), responsable de encapsular la interfaz y los parámetros de llama.cpp, para llevar a cabo la ejecución fuera de línea de modelos grandes.

* Thirdparty/LLAMACpp: Módulo de tercero en tiempo de ejecución (Runtime) que integra la biblioteca dinámica y los archivos de encabezado de llama.cpp.

El UClass responsable específico de enviar solicitudes es FAIChatPlus_xxxChatRequest, cada servicio de API tiene su propio UClass de solicitud independiente. Las respuestas a las solicitudes se obtienen a través de dos UClass, UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase, solo es necesario registrar el delegado de callback correspondiente.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar, esto se hace estableciendo FAIChatPlus_xxxChatRequestBody. La respuesta específica también se analiza en FAIChatPlus_xxxChatResponseBody, lo que permite obtener el ResponseBody a través de una interfaz específica al recibir la devolución de llamada.

Puedes encontrar más detalles del código fuente en la Tienda de Epic Games: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Guía de uso

###Utilice el modelo sin conexión del editor de herramientas llama.cpp.

Traduce este texto al español:

Instrucciones sobre cómo utilizar el modelo fuera de línea llama.cpp en la herramienta de edición AIChatPlus.

Descarga primero el modelo sin conexión desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloca el modelo en una carpeta específica, por ejemplo, en el directorio del proyecto de juegos Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Abre la herramienta AIChatPlus en el editor: Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat y abre la página de ajustes de la sesión.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Establezca Api en Cllama, active Custom Api Settings y agregue la ruta de búsqueda de modelos, luego seleccione el modelo.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

¡Comienza a chatear!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###El código utiliza el modelo offline llama.cpp

A continuación se explica cómo utilizar el modelo fuera de línea llama.cpp en el código.

Primero, también necesitas descargar el archivo del modelo en la carpeta Content/LLAMA.

Modificar el código para agregar un comando y enviar un mensaje al modelo sin conexión dentro de ese comando.

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

Después de volver a compilar, al usar el comando en el editor Cmd, puedes ver los resultados de la salida del modelo grande en el registro OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###La herramienta de diseño utiliza el modelo fuera de línea llama.cpp

La siguiente descripción explica cómo utilizar el modelo offline llama.cpp en un blueprint.

Crea un nodo `Enviar solicitud de chat Cllama` haciendo clic derecho en el diagrama.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Crear un nodo de opciones y establecer `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

*Crear Messages, añadir un mensaje del sistema y un mensaje de usuario respectivamente*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Crear un Delegado que reciba la información de salida del modelo y la imprima en pantalla

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Traduce este texto al español:

* La apariencia de un plano completo sería así, al ejecutar el plano se visualizará en la pantalla del juego el mensaje que regresa al imprimir el gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###Translate these text into Spanish language:

El modelo de OpenAI se utiliza para el blueprint

Crea un nodo llamado `Send OpenAI Chat Request In World` haciendo clic derecho en el diagrama.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Cree el nodo Options y configure `Stream=true, Api Key="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

* Cree Messages, agregue un Mensaje del Sistema y un Mensaje de Usuario respectivamente

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

*Crear un Delegate que reciba la información de salida del modelo y la imprima en pantalla*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* La apariencia de un plano completo es la siguiente: ejecutando el plano, podrás ver en la pantalla del juego el mensaje que devuelve al imprimir el modelo grande.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Traduzca el texto al idioma español: 

Blueprint utiliza la imagen de Claude para el análisis.

Crea un nodo "Enviar solicitud de chat a Claude" haciendo clic derecho en el blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Crear un nodo de Opciones y configurar `Stream=true, Api Key="tu clave de API de Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

* Crear Messages, crear Texture2D desde archivo y luego AIChatPlusTexture, finalmente agregar AIChatPlusTexture a Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

* Al igual que en el tutorial anterior, crea un Event y muestra la información en la pantalla del juego.

Traduce este texto al idioma español:

* Una vez que ejecutes el blueprint completo, podrás ver en la pantalla del juego el mensaje devuelto al imprimir el modelo en gran escala.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

###Traducir el texto al lenguaje español:

Blueprint utiliza OpenAI para crear imágenes

Crea un nodo `Send OpenAI Image Request` en el blueprint con un clic derecho, y establece `In Prompt="una hermosa mariposa"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Cree el nodo Options y establezca `Api Key="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Vincula el evento "On Images" y guarda las imágenes en el disco local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

* La versión completa del diseño se ve así, al ejecutar el diseño, se puede ver que la imagen se guarda en la ubicación especificada

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

##Registro de actualizaciones

### v1.3.3 - 2024.11.25

####Nueva función

* Compatible con UE-5.5

####Reparación de problemas

* Corregir problemas en los que no se activan algunas partes de los planos.

### v1.3.2 - 2024.10.10

####Nueva funcionalidad

Reparar el fallo de cllama al detener manualmente la solicitud.

Corregir el problema de la versión de descarga de la tienda win que no puede encontrar los archivos ggml.dll y llama.dll.

* Al crear la solicitud, se verifica si se encuentra en el hilo del juego, CreateRequest check en el hilo del juego

### v1.3.1 - 2024.9.30

####**Nueva característica**

Añadir un SystemTemplateViewer que permita visualizar y utilizar cientos de plantillas de configuración del sistema.

####Corrección de problemas

Repara el complemento descargado desde la tienda, llama.cpp no puede encontrar la biblioteca de vínculos.

Corregir problema de ruta demasiado larga en LLAMACpp

Reparar el error de enlace de llama.dll después de empaquetar en Windows.

Solucionar el problema de lectura de rutas de archivo en ios/android

Corregir el error en la configuración de Cllame.

### v1.3.0 - 2024.9.23

####Traduce este texto al idioma español:

Característica importante de nueva implementación.

* Integración de llama.cpp, compatible con la ejecución offline de modelos grandes a nivel local.

### v1.2.0 - 2024.08.20

####Nueva función

Apoyo a OpenAI Image Edit/Image Variation.

Compatibilidad con la API de Ollama, compatible con la obtención automática de la lista de modelos admitidos por Ollama

### v1.1.0 - 2024.08.07

####Nueva característica

Apoyar el plan.

### v1.0.0 - 2024.08.05

####Nueva característica

Base de funciones completas

Apoyo a OpenAI, Azure, Claude, Gemini.

* Herramienta de chat con editor integrado y funciones completas

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
