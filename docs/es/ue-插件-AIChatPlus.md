---
layout: post
title: Documentación sobre el complemento de UE AIChatPlus.
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
description: Documento de instrucciones de UE Plugin AIChatPlus
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documento de instrucciones del complemento AIChatPlus de UE

##Almacén público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complemento

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento para UnrealEngine que permite la comunicación con diversos servicios de chat de IA GPT. Actualmente admite servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama y llama.cpp local sin conexión. En el futuro, se seguirán agregando más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que garantiza un rendimiento eficiente y facilita la integración de estos servicios de chat de IA para desarrolladores de UE.

UE.AIChatPlus también incluye una herramienta de edición que te permite usar directamente los servicios de chat de inteligencia artificial en el editor para generar texto e imágenes, analizar imágenes, entre otras funciones.

##Instrucciones de uso

###Herramienta de chat del editor

El menú Tools -> AIChatPlus -> AIChat abre una herramienta de chat de editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


La herramienta es compatible con la generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Función principal

* Modelo grande fuera de línea: integra la biblioteca llama.cpp, compatible con la ejecución local fuera de línea de modelos grandes

* Chat de texto: haz clic en el botón `New Chat` en la esquina inferior izquierda para crear una nueva sesión de chat de texto.

* Generación de imágenes: haz clic en el botón `New Image Chat` en la esquina inferior izquierda para iniciar una nueva sesión de generación de imágenes.

* Análisis de imágenes: Algunos servicios de chat de `New Chat` admiten el envío de imágenes, como Claude, Google Gemini. Simplemente haz clic en el botón 🖼️ o 🎨 encima del cuadro de texto para cargar la imagen que deseas enviar.

Apoyo a Blueprint: Apoyo a la creación de Blueprint para realizar solicitudes de API, completar funciones como chat de texto, generación de imágenes, etc.

Establecer el rol actual en la conversación: el menú desplegable en la parte superior del cuadro de chat permite seleccionar el rol actual para enviar texto, lo que permite simular diferentes roles para ajustar la conversación de la inteligencia artificial (IA).

Vaciar conversación: El botón ❌ en la parte superior de la ventana de chat puede borrar el historial de mensajes de la conversación actual.

* Plantilla de diálogo: incluye cientos de plantillas de configuración de diálogo para facilitar el manejo de problemas comunes.

Traduce este texto al idioma español:

* Configuración global: Haz clic en el botón `Setting` en la esquina inferior izquierda para abrir la ventana de configuración global. Puedes establecer el chat de texto predeterminado, el servicio de API para generar imágenes y configurar los parámetros específicos de cada servicio de API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Configuración de la conversación: Haz clic en el botón de configuración en la parte superior del cuadro de chat para abrir la ventana de configuración de la conversación actual. Es posible cambiar el nombre de la conversación, modificar los servicios de API utilizados en la conversación y establecer parámetros específicos de API para cada conversación de forma independiente. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

Modificar contenido del chat: Al colocar el mouse sobre el contenido del chat, aparecerá un botón de configuración para ese contenido de chat en particular, que permitirá regenerar, modificar, copiar o eliminar dicho contenido, así como regenerar contenido debajo (si es contenido de usuario).

* Exploración de imágenes: Para la generación de imágenes, al hacer clic en una imagen se abrirá la ventana de visualización de imágenes (ImageViewer), que admite guardar imágenes como PNG/UE Texture. Las Texturas se pueden ver directamente en el explorador de contenido (Content Browser), facilitando su uso dentro del editor. También se ofrece soporte para eliminar imágenes, regenerarlas, continuar generando más imágenes, entre otras funciones. En el editor de Windows, también se puede copiar imágenes, lo que permite copiarlas directamente al portapapeles para facilitar su uso. Las imágenes generadas en la sesión se guardarán automáticamente en la carpeta de cada sesión, con la ruta habitualmente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

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

Utilizar grandes modelos sin conexión

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Plantilla de diálogo

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introducción al código principal

En la actualidad, el complemento se divide en los siguientes módulos:

* AIChatPlusCommon: Módulo de tiempo de ejecución (Runtime), encargado de manejar las solicitudes de envío de varias interfaces de API de IA y analizar el contenido de las respuestas.

* AIChatPlusEditor: Módulo de editor, responsable de implementar la herramienta de chat de inteligencia artificial en el editor.

* AIChatPlusCllama: Módulo en tiempo de ejecución (Runtime), encargado de encapsular la interfaz y los parámetros de llama.cpp, para lograr la ejecución offline de grandes modelos

* Thirdparty/LLAMACpp: Módulo de terceros en tiempo de ejecución (Runtime) que integra la biblioteca dinámica y archivos de encabezado de llama.cpp.

El UClass responsable de enviar las solicitudes concretas es FAIChatPlus_xxxChatRequest. Cada servicio de API tiene su propio UClass de solicitud independiente. Las respuestas a las solicitudes se obtienen a través de dos UClass diferentes: UAIChatPlus_ChatHandlerBase y UAIChatPlus_ImageHandlerBase. Solo es necesario registrar los delegados de devolución de llamada correspondientes.

Antes de enviar una solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar. Esto se hace a través de FAIChatPlus_xxxChatRequestBody. La respuesta específica también se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir una respuesta, se puede obtener el ResponseBody a través de una interfaz específica.

Se pueden encontrar más detalles sobre el código fuente en la tienda de UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Guía de uso

###Utilice el modelo fuera de línea del editor de herramientas llama.cpp.

Traduce este texto al idioma español:

Las siguientes instrucciones detallan cómo utilizar el modelo fuera de línea llama.cpp en la herramienta de edición AIChatPlus.

(https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloca el modelo en una carpeta específica, como por ejemplo en el directorio Content/LLAMA del proyecto del juego.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Abre la herramienta de edición AIChatPlus: Herramientas -> AIChatPlus -> AIChat, crea una sesión de chat y abre la página de configuración de la sesión.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Establecer Api como Cllama, activar Configuraciones de Api Personalizadas, añadir ruta de búsqueda de modelos y seleccionar un modelo.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

¡Comenzar a chatear!¡¡

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###El código utiliza el modelo fuera de línea llama.cpp

Traduce este texto al idioma Español:

El siguiente texto explica cómo utilizar el modelo fuera de línea llama.cpp en el código.

Primero, también necesitas descargar el archivo del modelo en Content/LLAMA.

Modifique el código para agregar un comando y enviar un mensaje al modelo sin conexión dentro del comando.

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

Después de volver a compilar, puedes usar comandos en la consola del editor para ver los resultados de la salida del modelo grande en el registro OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Translate these text into Spanish language:

 El archivo de plano de planta utiliza el modelo fuera de línea llama.cpp

A continuación se explica cómo usar el modelo sin conexión llama.cpp en un blueprint.

Crea un nodo `Enviar solicitud de chat a Cllama` con clic derecho en el blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Crear un nodo de Opciones y establecer `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

* Crear mensajes, agregar un mensaje del sistema y un mensaje del usuario respectivamente

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

*Crear un delegado que reciba la información de salida del modelo y la imprima en la pantalla*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Translate these text into Spanish language:

* La representación completa del blueprint se ve así, ejecuta el blueprint y verá el mensaje devuelto en la pantalla del juego al imprimir el modelo grande.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##Registro de actualizaciones

### v1.3.2 - 2024.10.10

#### Bugfix

Reparar cllama que se bloquea al detener manualmente la solicitud.
Corregir el problema de falta de archivos ggml.dll y llama.dll al empaquetar la versión de descarga de Win en la tienda.
* Al crear una solicitud, se verifica si se encuentra en el hilo del juego, se comprueba en el hilo del juego.

### v1.3.1 - 2024.9.30

Agregue un SystemTemplateViewer, que le permitirá ver y utilizar cientos de plantillas de configuración del sistema.

#### Bugfix

Reparar el plugin descargado de la tienda, llama.cpp no puede encontrar la biblioteca de enlaces.
* Corregir el problema de la ruta demasiado larga en LLAMACpp
Corregir el error de enlace de llama.dll después de empaquetar en Windows.
Corrija el problema de lectura de la ruta de archivos en ios/android.
Corregir el error al establecer el nombre de Cllame

### v1.3.0 - 2024.9.23

Actualización importante

* Se ha integrado llama.cpp, para admitir la ejecución sin conexión local de modelos grandes

### v1.2.0 - 2024.08.20

Apoyando la Edición de Imágenes de OpenAI/Variedad de Imágenes.

Apoya la API de Ollama, que permite obtener automáticamente la lista de modelos admitidos por Ollama.

### v1.1.0 - 2024.08.07

Apoyar el plan (blueprint)

### v1.0.0 - 2024.08.05

*Funcionalidad básica completa*

Apoyo a OpenAI, Azure, Claude, Gemini

* Herramienta de chat con editor integrado y funciones completas

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
