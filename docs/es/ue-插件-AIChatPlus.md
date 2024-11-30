---
layout: post
title: Documentación de UE Plugin AIChatPlus
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
description: Documento de instrucciones del complemento UE AIChatPlus
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documento de instrucciones del complemento UE AIChatPlus

##Repositorio público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complemento

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

Esta extensión es compatible con UE5.2+.

UE.AIChatPlus es un plugin de UnrealEngine que implementa la comunicación con varios servicios de chat de inteligencia artificial GPT. Actualmente, los servicios compatibles son OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, y llama.cpp para uso local sin conexión. En el futuro, se seguirá añadiendo compatibilidad con más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, ofreciendo un rendimiento eficiente y facilitando a los desarrolladores de UE integrar estos servicios de chat de inteligencia artificial.

Al mismo tiempo, UE.AIChatPlus también incluye una herramienta de edición que permite utilizar directamente estos servicios de chat de IA en el editor para generar texto e imágenes, analizar imágenes, entre otras funciones.

##Instrucciones de uso

###Herramienta de chat del editor

La opción Tools -> AIChatPlus -> AIChat en la barra de menú puede abrir la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


El soporte de la herramienta incluye la generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente: 

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Características principales

* Modelo grande fuera de línea: Integración de la biblioteca llama.cpp, compatible con la ejecución en local fuera de línea de modelos grandes

* Chat de texto: Haz clic en el botón `Nuevo Chat` en la esquina inferior izquierda para crear una nueva conversación de chat de texto.

* Generación de imágenes: haz clic en el botón `New Image Chat` en la esquina inferior izquierda para iniciar una nueva sesión de generación de imágenes.

Análisis de imágenes: Algunos servicios de chat en `New Chat` admiten el envío de imágenes, como Claude y Google Gemini. Simplemente haz clic en el botón 🖼️ o 🎨 encima del cuadro de entrada para cargar la imagen que deseas enviar.

Apoyo al Blueprint: Apoyo para la creación de solicitudes de API utilizando Blueprint, para funciones como chat de texto, generación de imágenes, entre otros.

Establecer el rol actual del chat: El menú desplegable en la parte superior del cuadro de chat puede configurar el rol actual para enviar texto, permitiendo simular diferentes roles para ajustar la conversación con la inteligencia artificial (IA).

Limpiar conversación: al pulsar la ❌ en la parte superior del cuadro de chat, se pueden borrar los mensajes anteriores de la conversación actual.

* Plantilla de diálogo: incorpora cientos de plantillas de configuración de diálogo para facilitar el manejo de problemas comunes.

Translate these text into Spanish language:

* Configuración global: Haz clic en el botón `Configuración` en la esquina inferior izquierda para abrir la ventana de configuración global. Puedes establecer el chat de texto predeterminado, el servicio de API para generar imágenes y configurar los parámetros específicos de cada servicio API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Configuración de la conversación: al hacer clic en el botón de configuración en la parte superior de la ventana de chat, se puede abrir la ventana de configuración de la conversación actual. Permite cambiar el nombre de la conversación, modificar los servicios de API utilizados en la conversación, y ajustar los parámetros específicos de API para cada conversación de forma independiente. La configuración de las conversaciones se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

Modificar contenido del chat: al pasar el ratón sobre el contenido del chat, aparecerá un botón de configuración para ese contenido en particular, que permite regenerar, modificar, copiar o eliminar el contenido, así como regenerar un nuevo contenido debajo (para el contenido creado por el usuario).

* Exploración de imágenes: Para la generación de imágenes, al hacer clic en una imagen se abrirá la ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como PNG/UE Texture. Las Textures se pueden ver directamente en el navegador de contenido (Content Browser) para facilitar su uso dentro del editor. También se brinda soporte para eliminar, regenerar y generar más imágenes. En el caso del editor en Windows, se puede copiar imágenes directamente al portapapeles para facilitar su uso. Las imágenes generadas en la sesión se guardarán automáticamente en la carpeta de cada sesión, con la ruta comúnmente siendo `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Plan:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Configuración general:

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

###Introducción al código principal.

En la actualidad, el complemento se divide en los siguientes módulos:

* AIChatPlusCommon: Módulo de tiempo de ejecución, encargado de manejar las solicitudes de envío y análisis de respuestas de varios API de IA.

* AIChatPlusEditor: Módulo del editor, responsable de implementar la herramienta de chat AI del editor.

* AIChatPlusCllama: Módulo de tiempo de ejecución (Runtime), encargado de encapsular la interfaz y los parámetros de llama.cpp, para lograr la ejecución offline de modelos grandes.

* Thirdparty/LLAMACpp: Módulo de terceros en tiempo de ejecución (Runtime) que integra la biblioteca dinámica y archivos de cabecera de llama.cpp.

El UClass responsable de enviar la solicitud de forma específica es FAIChatPlus_xxxChatRequest. Cada servicio de API tiene su propio Request UClass independiente. Las respuestas a las solicitudes se obtienen a través de dos UClass: UAIChatPlus_ChatHandlerBase y UAIChatPlus_ImageHandlerBase. Solo es necesario registrar los delegados de devolución de llamada correspondientes.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar, esto se hace mediante FAIChatPlus_xxxChatRequestBody. El contenido específico de la respuesta también se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir la devolución, se puede obtener el ResponseBody a través de una interfaz específica.

Más detalles del código fuente están disponibles en la tienda de UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Guía de uso

###Utiliza el modelo fuera de línea del editor de herramientas llama.cpp.

Las siguientes instrucciones explican cómo utilizar el modelo fuera de línea llama.cpp en la herramienta de edición AIChatPlus.

Descargue el modelo sin conexión desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloque el modelo en una carpeta específica, por ejemplo, en el directorio de contenido del proyecto de juegos Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Abre la herramienta de edición AIChatPlus: Herramientas -> AIChatPlus -> AIChat, crea una nueva conversación y abre la página de configuración de la misma.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Establece la Api en Cllama, activa la Configuración Personalizada de la Api y añade la ruta de búsqueda de modelos, luego selecciona el modelo.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

¡Comencemos a chatear!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###El código utiliza el modelo fuera de línea llama.cpp.

Traduce este texto al idioma español:

El siguiente texto explica cómo utilizar el modelo fuera de línea llama.cpp en el código.

* Primero, necesitas descargar el archivo del modelo en la carpeta Content/LLAMA.

Agrega una línea de código para incluir un comando y enviar un mensaje al modelo sin conexión dentro del comando.

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

Una vez recompilado, simplemente utiliza el comando en la consola de comandos del editor para visualizar los resultados de la salida del gran modelo en el registro OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###El archivo blueprint utiliza el modelo sin conexión llama.cpp

Se explica cómo usar el modelo fuera de línea llama.cpp en un pizarrón.

Crea un nodo en el plano llamado `Enviar solicitud de chat de Cllama` con clic derecho.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Crea un nodo Options y establece `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

*Crear mensajes, agregar un mensaje del sistema y un mensaje del usuario respectivamente.*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Crea un Delegado que acepte la información de salida del modelo y la imprima en la pantalla

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Traduce este texto al idioma español:

* Una vez que ejecutes por completo el diagrama de diseño, verás en la pantalla del juego el mensaje que devuelve al imprimir el modelo en grande.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###El uso de modelos OpenAI en el diseño.

* En el panel de diseño, haz clic derecho para crear un nodo `Enviar solicitud de chat OpenAI en el mundo`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Cree el nodo Options y establezca `Stream=true, Api Key="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

*Crear Messages, agrega un System Message y un User Message respectivamente*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Crear un Delegate que acepte la información de salida del modelo y la imprima en la pantalla

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Traduce este texto al idioma español:

* El aspecto completo del plano es así, al ejecutarlo, verás en la pantalla del juego el mensaje devuelto al imprimir el modelo grande.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Utiliza el blueprint de Claude para analizar imágenes.

Cree un nodo llamado `Enviar solicitud de chat a Claude` haciendo clic derecho en el diagrama.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Crear un nodo de Opciones y configurar `Stream=true, Api Key="tu clave de API de Clude", Max Output Tokens=1024`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Crea Messages, crea un Texture2D desde un archivo y luego crea un AIChatPlusTexture a partir de ese Texture2D, luego agrega el AIChatPlusTexture al Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

* Siguiendo el tutorial anterior, crea un Event y muestra la información en la pantalla del juego.

Traduce este texto al idioma español:

* La apariencia de un blueprint completo sería esta; al ejecutar el blueprint, se puede observar en la pantalla del juego el mensaje devuelto al imprimir el modelo grande.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

###La creación de imágenes con OpenAI.

Crea un nodo `Enviar solicitud de imagen a OpenAI` en el blueprint con clic derecho, y establece `En Prompt="una hermosa mariposa"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Cree el nodo Options y establezca `Api Key="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Vincular el evento On Images y guardar las imágenes en el disco local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

Translate these text into Spanish language:

* El aspecto completo del plano se ve así, al ejecutar el plano se podrá ver la imagen guardada en la ubicación especificada.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

##Registro de actualizaciones

### v1.3.3 - 2024.11.25

####Nueva función

* Compatible con UE-5.5

####Corrección de problemas

Corregir problemas de algunas plantillas que no funcionan.

### v1.3.2 - 2024.10.10

####Solución de problemas

Reparar cllama se bloquea al detener manualmente la solicitud.

Resolver el problema en el paquete de descarga de la versión de Windows en la tienda, donde no se puede encontrar el archivo ggml.dll llama.dll.

* Al crear una solicitud, se verifica si se está en el hilo del juego, revisar en GameThread.

### v1.3.1 - 2024.9.30

####Nuevas funciones

Añadir un SystemTemplateViewer que permita ver y utilizar cientos de plantillas de configuración del sistema.

####Reparación de problemas

Repara el plugin descargado desde la tienda, llama.cpp no puede encontrar la biblioteca de vínculos.

Actualizar el problema de la ruta demasiado larga en LLAMACpp

Reparar error de enlace llama.dll después de empaquetar en Windows.

* Corregir problema de lectura de ruta de archivos en ios/android

Corregir error de configuración del nombre de la llamada.

### v1.3.0 - 2024.9.23

####Traduce este texto al idioma español:  

 Característica principal.

* Integrado llama.cpp, con soporte para la ejecución sin conexión local de modelos grandes

### v1.2.0 - 2024.08.20

####Nueva función

Apoyo a OpenAI Image Edit/Image Variation.

Apoyo a la API de Ollama, compatibilidad con la obtención automática de la lista de modelos admitidos por Ollama.

### v1.1.0 - 2024.08.07

####Nueva función

Apoyar el plan.

### v1.0.0 - 2024.08.05

####Nueva característica

Funcionalidad básica completa

Apoyo a OpenAI, Azure, Claude, Gemini

* Herramienta de chat con editor incorporado de funciones completas

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
