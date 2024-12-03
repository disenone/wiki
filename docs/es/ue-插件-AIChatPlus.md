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
description: Documento de instrucciones de UE de la extensión AIChatPlus.
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documentación de la extensión UE AIChatPlus

##Almacén público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complementos

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento para UnrealEngine que permite la comunicación con varios servicios de chat de inteligencia artificial GPT. Actualmente admite servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, y llama.cpp en modo offline local. En el futuro, seguirá agregando soporte para más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que garantiza un alto rendimiento y facilita la integración de estos servicios de chat AI para los desarrolladores de UE.

Al mismo tiempo, UE.AIChatPlus también incluye una herramienta de edición que permite utilizar directamente estos servicios de chat de IA en el editor para generar texto e imágenes, analizar imágenes, etc.

##Instrucciones de uso

###Herramienta de chat del editor

El menú Tools -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


La herramienta admite la generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Función principal

* Modelo grande sin conexión: Integración de la biblioteca llama.cpp para admitir la ejecución sin conexión de modelos grandes a nivel local

* Chat de texto: haz clic en el botón `New Chat` en la esquina inferior izquierda para crear una nueva sesión de chat de texto.

* Generación de imagen: haz clic en el botón `New Image Chat` en la esquina inferior izquierda para crear una nueva sesión de generación de imágenes.

* Análisis de imagen: Algunos servicios de chat en la función `Nuevo Chat` admiten el envío de imágenes, como Claude y Google Gemini. Haz clic en el botón 🖼️ o 🎨 sobre el cuadro de texto para cargar la imagen que deseas enviar.

Apoyo a los planos (Blueprint): Apoyo a la creación de API de planos para realizar funciones como chat de texto, generación de imágenes, etc.

Establecer el rol actual del chat: el menú desplegable en la parte superior del cuadro de chat permite seleccionar el rol actual para enviar texto, lo que permite simular diferentes roles para ajustar la conversación de la IA.

Limpiar chat: al hacer clic en la ❌ en la parte superior de la ventana de chat, se borra el historial de mensajes de la conversación actual.

* Plantilla de diálogo: incorpora cientos de plantillas de configuración de diálogo para facilitar el manejo de problemas comunes.

Translate these text into Spanish language:

* Configuración global: al hacer clic en el botón `Setting` en la esquina inferior izquierda, se puede abrir la ventana de configuración global. Puede establecer el chat de texto predeterminado, el servicio API para generar imágenes y configurar los parámetros específicos de cada servicio API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Configuración de la conversación: al hacer clic en el botón de configuración en la parte superior de la ventana de chat, se puede abrir la ventana de configuración de la conversación actual. Permite cambiar el nombre de la conversación, modificar el servicio API utilizado por la conversación, y configurar parámetros específicos del API para cada conversación de manera independiente. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Modificar contenido del chat: Al hacer hover sobre el contenido del chat, aparecerá un botón de ajustes para ese contenido en particular, que permitirá regenerar, modificar, copiar o eliminar el contenido, así como regenerar contenido debajo (para contenido creado por un usuario).

* Visualización de imágenes: En cuanto a la generación de imágenes, al hacer clic en una imagen se abrirá una ventana de visualización de imágenes (ImageViewer), que admite guardar la imagen como PNG/UE Texture. Las Texturas se pueden ver directamente en el Explorador de contenido (Content Browser), facilitando su uso dentro del editor. También se permite eliminar imágenes, regenerarlas, continuar generando más imágenes, entre otras funciones. En el editor de Windows, también se puede copiar imágenes, lo que permite copiarlas al portapapeles para un uso más conveniente. Las imágenes generadas en una sesión se guardarán automáticamente en la carpeta de cada sesión, con la ruta generalmente como `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Plan:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Configuración global:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Configuración de la conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modificar contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visor de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Utilización de modelos de gran tamaño sin conexión.

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Plantilla de diálogo

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introducción al código central

Actualmente, el complemento se divide en los siguientes módulos:

* AIChatPlusCommon: Módulo de tiempo de ejecución, encargado de manejar las solicitudes de envío de API de IA y analizar el contenido de las respuestas.

* AIChatPlusEditor: Módulo de editor, responsable de implementar la herramienta de chat de IA en el editor.

* AIChatPlusCllama: Módulo de tiempo de ejecución (Runtime), encargado de encapsular la interfaz y los parámetros de llama.cpp, para realizar la ejecución fuera de línea de modelos grandes.

* Thirdparty/LLAMACpp: Módulo de terceros en tiempo de ejecución (Runtime), que integra la biblioteca dinámica y los archivos de cabecera de llama.cpp.

Traduce el texto a español:

El UClass responsable de enviar las solicitudes es FAIChatPlus_xxxChatRequest, cada servicio API tiene su propio UClass de solicitud independiente. Las respuestas a las solicitudes se obtienen a través de las clases UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase, solo se necesita registrar los delegados de devolución de llamada correspondientes.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar, esto se hace usando FAIChatPlus_xxxChatRequestBody. El contenido específico de la respuesta también se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir la devolución se puede obtener el ResponseBody a través de una interfaz específica.

Puede obtener más detalles del código fuente en la tienda de UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Guía de uso

###Utilizar la herramienta del editor con un modelo sin conexión llama.cpp

La siguiente explicación detalla cómo utilizar el modelo offline llama.cpp en la herramienta de edición AIChatPlus.

Descarga primero el modelo sin conexión desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloca el modelo en una carpeta específica, por ejemplo, en el directorio del proyecto de juego Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Abre la herramienta de edición AIChatPlus: Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat y abre la página de configuración de la sesión.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Establecer Api en Cllama, activar Configuración de Api Personalizada y agregar la ruta de búsqueda de modelos, luego seleccionar un modelo.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Comenzar a chatear!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###El código utiliza el modelo fuera de línea llama.cpp.

A continuación se describe cómo usar el modelo fuera de línea llama.cpp en el código.

* Primero, necesitas descargar el archivo del modelo en Content/LLAMA.

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

* Después de volver a compilar, al usar el comando en el Editor de Cmd, podrás ver los resultados de la salida del modelo grande en el registro OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Traduce este texto al idioma español:

 *El blueprint utiliza el modelo offline llama.cpp*

Instrucciones sobre cómo utilizar el modelo de aprendizaje automático fuera de línea llama.cpp en un diagrama de bloques.

En la vista de diseño, haz clic derecho para crear un nodo llamado `Enviar solicitud de chat de Cllama`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Crea el nodo Options y establece `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

*Crear mensajes, agregar un mensaje del sistema y un mensaje de usuario respectivamente*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Establecer un Delegado que reciba la información de salida del modelo y la imprima en la pantalla

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* La apariencia de un plan detallado se ve así, al ejecutar el plan, podrás ver un mensaje devuelto en la pantalla del juego imprimiendo un modelo grande.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###Utiliza el modelo de OpenAI en el blueprint

Crea un nodo `Enviar solicitud de chat de OpenAI en el mundo` con clic derecho en el blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Cree el nodo de opciones y configure `Stream=true, Api Key="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

*Crear Mensajes, añadir un mensaje del Sistema y un mensaje de Usuario respectivamente*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Establecer un Delegado que reciba la información de salida del modelo y la imprima en la pantalla

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* La apariencia de un plano completo sería así. Al ejecutar el plano, podrás ver en la pantalla del juego el mensaje que retorna al imprimir el modelo grande.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Traduce este texto al idioma Español:

Diagrama utiliza Claude para analizar imágenes

Crea un nodo `Enviar solicitud de chat a Claude` con clic derecho en el blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Crea el nodo Options y configura `Stream=true, Api Key="tu clave API de Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Crear Messages, crear Texture2D desde archivos, y luego crear AIChatPlusTexture desde Texture2D, para finalmente añadir AIChatPlusTexture a Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

* Igual que el tutorial anterior, crea un Event y muestra la información en la pantalla del juego.

Traduce estos textos al idioma español:

* La representación visual completa se ve así, ejecutar el plano y verá el mensaje devuelto por la pantalla del juego al imprimir el modelo en gran escala.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

###El plano utiliza OpenAI para crear imágenes.

* En el Blueprint, haz clic derecho para crear un nodo `Enviar solicitud de imagen de OpenAI` y establece `In Prompt="una hermosa mariposa"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Cree el nodo Options y establezca `Api Key="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

* Vincular el evento On Images y guardar la imagen en el disco duro local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

Translate these text into Spanish language:

* La apariencia completa de los planos es así, ejecuta los planos y podrás ver la imagen guardada en la ubicación especificada

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

##Registro de actualizaciones

### v1.3.4 - 2024.12.05

####Nueva funcionalidad

* OpenAI apoya la API de visión

####Reparación de problemas

Corregir el error de OpenAI cuando stream=false

### v1.3.3 - 2024.11.25

####Nueva característica

Apoyo para UE-5.5

####Reparación de problemas

Corrija el problema de que algunas blueprints no surtan efecto.

### v1.3.2 - 2024.10.10

####Reparación de problemas

Reparar el fallo de cllama al detener manualmente la solicitud.

Corrige el problema de la versión de descarga de Win en la tienda donde no se encuentra el archivo ggml.dll o llama.dll.

* Al crear la solicitud, se verifica si se encuentra en el hilo de juego. CreateRequest revisa en el hilo de juego.

### v1.3.1 - 2024.9.30

####Nueva función

Agregar un SystemTemplateViewer que permita ver y utilizar cientos de plantillas de configuración del sistema.

####Reparación de problemas

Reparar el complemento descargado de la tienda, llama.cpp no puede encontrar la biblioteca de enlace.

* Corregir problema de ruta demasiado larga en LLAMACpp

Corregir el error de enlace llama.dll después de empaquetar en Windows.

Corregir problema de lectura de ruta de archivo en ios/android.

Corregir error al configurar el nombre de Cllame

### v1.3.0 - 2024.9.23

####Traduce este texto al idioma español:

 Función nueva y significativa

* Integrado llama.cpp, compatible con la ejecución offline de grandes modelos locales.

### v1.2.0 - 2024.08.20

####Nueva característica

Apoyo a OpenAI Image Edit/Image Variation.

Apoyamos la API de Ollama, que permite obtener automáticamente la lista de modelos admitidos por Ollama.

### v1.1.0 - 2024.08.07

####Nuevas características

Apoyo al plan estratégico

### v1.0.0 - 2024.08.05

####Nueva funcionalidad

Funcionalidad básica completa

Apoyar OpenAI, Azure, Claude, Gemini

* Herramienta de chat con editor completo incorporado

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
