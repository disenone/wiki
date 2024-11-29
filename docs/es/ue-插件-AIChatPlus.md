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
description: Documentación de UE Plug-in AIChatPlus
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE 插件 AIChatPlus Guía de Documentación

##Depósito público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complemento

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento de UnrealEngine que permite la comunicación con varios servicios de chat de IA GPT. Actualmente es compatible con OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama y llama.cpp en modo offline local. En el futuro, seguirá agregando soporte para más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que asegura un alto rendimiento y facilita a los desarrolladores de UE integrar estos servicios de chat de IA.

UE.AIChatPlus también incluye una herramienta de edición que permite utilizar directamente los servicios de chat de IA en el editor, generar texto e imágenes, y analizar imágenes, entre otras funciones.

##Instrucciones de uso

###Herramienta de chat del editor.

La barra de menú Tools -> AIChatPlus -> AIChat abre las herramientas de chat del editor proporcionadas por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


La herramienta es compatible con la generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente la siguiente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Función principal

* Modelo grande sin conexión: Integración de la biblioteca llama.cpp para admitir la ejecución sin conexión de modelos grandes a nivel local.

* Chat de texto: haz clic en el botón `Nuevo chat` en la esquina inferior izquierda para crear una nueva sesión de chat de texto.

* Generación de imágenes: haz clic en el botón `Nueva imagen pto de charla` en la esquina inferior izquierda para iniciar una nueva sesión de generación de imágenes.

Análisis de imágenes: Algunos servicios de chat en la función `New Chat` admiten el envío de imágenes, como Claude, Google Gemini. Simplemente haz clic en los botones de 🖼️ o 🎨 en la parte superior del cuadro de entrada para cargar la imagen que deseas enviar.

Translate these texts into Spanish language:

* Soporte de Blueprint: Soporte para la creación de solicitudes API a través de Blueprint, para funciones como chat de texto, generación de imágenes, entre otras.

Establecer el rol actual de la conversación: El menú desplegable en la parte superior del cuadro de chat puede definir el rol actual para enviar texto, lo que permite simular diferentes roles para ajustar la conversación con la inteligencia artificial.

Eliminar conversación: Al hacer clic en la ❌ en la parte superior del cuadro de chat se pueden borrar los mensajes anteriores de la conversación actual.

* Plantilla de diálogo: incorpora cientos de plantillas de configuración de diálogo para manejar fácilmente problemas comunes.

Traduce este texto al idioma español:

* Configuración global: al hacer clic en el botón `Setting` en la esquina inferior izquierda, se puede abrir la ventana de configuración global. Se pueden establecer el chat de texto predeterminado, los servicios de API para generar imágenes y los parámetros específicos de cada servicio de API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Translate these text into Spanish language:

* Configuración de la conversación: Al presionar el botón de ajustes en la parte superior de la ventana de chat, se puede abrir la ventana de configuración de la conversación actual. Permite modificar el nombre de la conversación, cambiar el servicio de API utilizado en la conversación, y ajustar parámetros específicos de API para cada conversación de manera independiente. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

Modificar contenido del chat: al desplazar el ratón sobre el contenido del chat, aparecerá un botón de configuración junto al contenido individual, que permite regenerar, modificar, copiar o eliminar el contenido, así como regenerar contenido debajo (para contenido de usuario).

* Visualización de imágenes: Para la generación de imágenes, al hacer clic en una imagen se abrirá la ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como PNG/Textura UE, las texturas se pueden ver directamente en el Explorador de contenido (Content Browser), lo que facilita su uso dentro del editor. También, se puede eliminar, volver a generar o continuar generando más imágenes. Para los editores en Windows, también se puede copiar imágenes, lo que permite copiarlas directamente al portapapeles para facilitar su uso. Las imágenes generadas en la sesión también se guardarán automáticamente en la carpeta de cada sesión, generalmente en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Planificación:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Configuración global:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Configuración de la conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Editar el contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visor de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Utilizar modelos grandes sin conexión.

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Plantilla de diálogo

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introducción al código central

En la actualidad, el complemento está dividido en los siguientes módulos:

* AIChatPlusCommon: Módulo de tiempo de ejecución, encargado de manejar las solicitudes de envío de diversas API de inteligencia artificial y analizar el contenido de las respuestas.

* AIChatPlusEditor: Módulo de editor, responsable de implementar la herramienta de chat de AI en el editor.

* AIChatPlusCllama: Módulo en tiempo de ejecución (Runtime), encargado de encapsular las interfaces y parámetros de llama.cpp, logrando así la ejecución offline de modelos grandes

* Thirdparty/LLAMACpp: Módulo de tercero en tiempo de ejecución (Runtime) que integra la biblioteca dinámica y archivos de cabecera de llama.cpp.

Traduce este texto al español:

El UClass encargado específicamente de enviar las solicitudes es FAIChatPlus_xxxChatRequest, cada servicio de API tiene su propia UClass de solicitud independiente. Las respuestas a las solicitudes se obtienen a través de dos UClass diferentes: UAIChatPlus_ChatHandlerBase y UAIChatPlus_ImageHandlerBase, simplemente hay que registrar los delegados de devolución de llamada correspondientes.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar, esto se realiza mediante FAIChatPlus_xxxChatRequestBody. El contenido específico de la respuesta también se analiza en FAIChatPlus_xxxChatResponseBody, que se puede obtener a través de una interfaz específica al recibir una devolución de llamada.

Más detalles del código fuente disponibles en la tienda de UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Guía de uso

###Utiliza el modelo sin conexión del archivo llama.cpp en la herramienta del editor.

A continuación se explica cómo utilizar el modelo offline llama.cpp en la herramienta de edición AIChatPlus.

* Primero, descarga el modelo offline desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloca el modelo en una carpeta específica, por ejemplo, dentro del directorio del proyecto de juegos Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Abre la herramienta de edición AIChatPlus: Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat y abre la página de configuración de la sesión.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Establece la Api en Cllama, activa la Configuración de Api Personalizada, agrega la ruta de búsqueda de modelos y elige un modelo.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

¡Comienza a conversar!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###El código utiliza el modelo offline llamado llama.cpp

La siguiente explicación muestra cómo utilizar el modelo sin conexión llama.cpp en el código.

Primero, también es necesario descargar el archivo del modelo en Content/LLAMA.

Modifique el código para agregar un comando y enviar un mensaje al modelo sin conexión dentro de dicho comando.

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

* Después de compilar de nuevo, simplemente utiliza el comando en la consola del editor Cmd y podrás ver los resultados de la salida del gran modelo en el registro OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###La implementación del modelo fuera de línea de blueprint se llama llama.cpp.

Instrucciones sobre cómo utilizar el modelo fuera de línea llama.cpp en un blueprint.

* En el blueprint, crea un nodo con el botón derecho llamado `Enviar solicitud de chat de Cllama`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Cree el nodo Options y establezca `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

*Crear Messages, agregar un System Message y un User Message respectivamente*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

*Crear Delegate para recibir información de salida del modelo y mostrarla en pantalla*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Traduce este texto al idioma español:

* La apariencia completa del diagrama es la siguiente, ejecuta el diagrama y verás en la pantalla del juego el mensaje devuelto al imprimir el modelo grande.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###Utilizando el modelo de OpenAI en el plan de acción

* En el panel de control, haz clic derecho para crear un nodo `Enviar solicitud de chat OpenAI en el mundo`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Cree el nodo Options y configure `Stream=true, Api Key="su clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Cree Mensajes, añada un Mensaje del Sistema y un Mensaje de Usuario respectivamente.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Crear un delegado que acepte la información de salida del modelo y la imprima en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Traduce este texto al idioma español:

* Una vez que ejecutes el blueprint completo, podrás ver en la pantalla del juego el mensaje que devuelve al imprimir el gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

##Registro de actualizaciones

### v1.3.3 - 2024.11.25

Apoyo a UE-5.5

* **Corrección de errores**: Se ha solucionado el problema de que ciertos diseños no funcionaban.

### v1.3.2 - 2024.10.10

#### Bugfix

Corregir el fallo de cllama al detener manualmente la solicitud.

Corregir el problema en la versión de descarga de la tienda en Windows donde no se puede encontrar el archivo ggml.dll o llama.dll al empaquetar.

* Al crear una solicitud, se verifica si se encuentra en el hilo del juego, CreateRequest se comprueba en el hilo del juego

### v1.3.1 - 2024.9.30

Añadir un SystemTemplateViewer, para ver y utilizar cientos de plantillas de configuración del sistema.

#### Bugfix

Reparar el plugin descargado desde la tienda, llama.cpp no puede encontrar la biblioteca de enlace.

* Solución al problema de la longitud excesiva de la ruta de LLAMACpp

Corregir el error de enlace de llama.dll después de empaquetar Windows.

* Corregir el problema de lectura de la ruta del archivo en iOS/Android

Corregir el error al establecer el nombre de Cllame

### v1.3.0 - 2024.9.23

Actualización importante

Se ha integrado llama.cpp para admitir la ejecución local sin conexión de modelos grandes.

### v1.2.0 - 2024.08.20

Apoyo a OpenAI Image Edit/Image Variation

Soporta la API de Ollama, capaz de obtener automáticamente la lista de modelos admitidos por Ollama.

### v1.1.0 - 2024.08.07

Respaldar el plan

### v1.0.0 - 2024.08.05

* Funcionalidad básica completa

Apoyo a OpenAI, Azure, Claude, Gemini

* Herramienta de chat con editor integrado y funciones completas.

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
