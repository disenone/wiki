---
layout: post
title: Documento de instrucciones para el complemento AIChatPlus de la UE.
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
description: Documento de instrucciones del complemento AIChatPlus de la UE.
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE 插件 AIChatPlus 说明文档

##Repositorio público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complementos

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento para UnrealEngine que permite la comunicación con varios servicios de chat de inteligencia artificial GPT. Actualmente es compatible con OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, y llama.cpp en modo offline local. En el futuro, se agregarán más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que garantiza un rendimiento eficiente y facilita la integración de estos servicios de chat de IA para desarrolladores de UE.

Al mismo tiempo, UE.AIChatPlus también incluye una herramienta de edición que te permite utilizar directamente los servicios de chat de IA en el editor para crear texto e imágenes, analizar imágenes, y más.

##Instrucciones de uso

###Herramienta de chat del editor

El menú Tools -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


El soporte de la herramienta incluye la generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Función principal

* Modelo grande sin conexión: Integración de la librería llama.cpp que permite la ejecución offline de modelos grandes de forma local

* Chat de texto: haz clic en el botón `New Chat` en la esquina inferior izquierda para crear una nueva sesión de chat de texto.

**Generación de imágenes:** Haz clic en el botón `Nuevo Chat de Imágenes` en la esquina inferior izquierda para iniciar una nueva sesión de generación de imágenes.

* Análisis de imágenes: Algunos servicios de chat dentro de `New Chat` admiten el envío de imágenes, como Claude y Google Gemini. Simplemente haz clic en el botón 🖼️ o 🎨 ubicado encima del cuadro de texto para cargar la imagen que deseas enviar.

* Soporte de Blueprint: admitir la creación de solicitudes de API a través de Blueprint para funciones como chat de texto, generación de imágenes, entre otros.

Establecer el rol de chat actual: el menú desplegable en la parte superior de la ventana de chat puede configurar el rol actual del texto enviado, permitiendo simular diferentes roles para ajustar la conversación de IA.

Vaciar conversación: Toca la ❌ en la parte superior de la ventana de chat para borrar el historial de mensajes de la conversación actual.

* Plantilla de diálogo: incorpora cientos de plantillas de configuración de diálogo para facilitar el manejo de problemas comunes.

Traduce este texto al idioma español:

* Configuración general: Haz clic en el botón `Configuración` en la esquina inferior izquierda para abrir la ventana de configuración general. Puedes establecer el chat de texto predeterminado, el servicio de API para generar imágenes y configurar los parámetros específicos de cada servicio de API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Configuración de la conversación: al hacer clic en el botón de configuración en la parte superior de la ventana de chat, se puede abrir la ventana de configuración de la conversación actual. Permite cambiar el nombre de la conversación, modificar el servicio de API utilizado en la conversación, y ajustar los parámetros específicos de la API para cada conversación de forma individual. La configuración de la conversación se guardará automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Modificar contenido del chat: al colocar el mouse sobre el contenido del chat, aparecerá un botón de ajustes para ese contenido específico, que permite regenerar, modificar, copiar o eliminar el contenido, así como regenerar contenido debajo (si el contenido pertenece al rol de usuario).

* Visualización de imágenes: al generar imágenes, al hacer clic en una imagen se abrirá una ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como PNG/Textura UE, las texturas se pueden ver directamente en el Explorador de contenido (Content Browser), facilitando su uso en el editor. También se puede eliminar, regenerar o seguir generando más imágenes. Para editores en Windows, también es posible copiar imágenes, lo que permite copiarlas directamente al portapapeles para un uso más sencillo. Las imágenes generadas en la sesión se guardarán automáticamente en la carpeta de cada sesión, generalmente en la ruta `$(CarpetaDelProyecto)/Guardado/AIChatPlusEditor/Sesiones/${GUID}/imágenes`.

Plan:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Configuración global:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Configuración de la conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Editar contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visor de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Utilizar modelos grandes sin conexión

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Plantilla de diálogo

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introducción al código central

En este momento, el complemento se divide en los siguientes módulos:

* AIChatPlusCommon: Módulo de tiempo de ejecución, responsable de manejar solicitudes de envío de API de IA y analizar el contenido de las respuestas.

* AIChatPlusEditor: Módulo de Editor, responsable de implementar la herramienta de chat de inteligencia artificial en el editor.

* AIChatPlusCllama: El módulo en tiempo de ejecución, se encarga de encapsular la interfaz y los parámetros de llama.cpp, para lograr la ejecución fuera de línea de modelos grandes.

* Thirdparty/LLAMACpp: Módulo de terceros en tiempo de ejecución (Runtime), que integra la biblioteca dinámica y archivos de cabecera de llama.cpp.

El UClass responsable específico de enviar la solicitud es FAIChatPlus_xxxChatRequest, cada servicio de API tiene su propio UClass de solicitud independiente. Las respuestas a las solicitudes se obtienen a través de dos UClass distintos: UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase, solo es necesario registrar los delegados de devolución de llamada correspondientes.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar. Esto se hace a través de FAIChatPlus_xxxChatRequestBody. El contenido específico de la respuesta también se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir la devolución se puede obtener el ResponseBody a través de una interfaz específica.

Puede encontrar más detalles del código fuente en la tienda de Unreal Engine: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Guía de uso

###Utilice el modelo sin conexión del editor de herramientas llama.cpp.

Traduce este texto al idioma español:

Instrucciones sobre cómo utilizar el modelo fuera de línea llama.cpp en la herramienta de edición AIChatPlus.

Descarga primero el modelo sin conexión desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloca el modelo en una carpeta específica, por ejemplo, en el directorio del proyecto de juego Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Abre la herramienta de edición AIChatPlus: Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat y accede a la página de configuración de la sesión.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Establezca Api en Cllama, active la configuración de Api personalizada y agregue una ruta de búsqueda de modelos, luego seleccione el modelo.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

¡Comienza la conversación!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###El código utiliza el modelo offline llama.cpp

Translate these text into Spanish language:

La siguiente explicación describe cómo usar el modelo offline llama.cpp en el código.

* Primero, también necesitas descargar el archivo del modelo en Content/LLAMA.

* Modificar el código para agregar un comando y enviar un mensaje al modelo sin conexión dentro de dicho comando.

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

Después de recompilar, puedes ver los resultados de la salida del gran modelo en el registro OutputLog utilizando comandos en la consola Cmd del editor.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###El archivo llama.cpp se utiliza en el plano de diseño con modelos offline.

La siguiente descripción explica cómo utilizar el modelo fuera de línea llama.cpp en un blueprint.

Crea un nodo llamado `Enviar solicitud de chat de Cllama` haciendo clic derecho en el blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Creación de un nodo Options y establecimiento de `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

*Crear mensajes, agregar un mensaje del sistema y un mensaje de usuario respectivamente*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Crear un delegado que reciba la información de salida del modelo y la imprima en pantalla

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Traduce este texto al idioma español:

* La apariencia general de un blueprint completo sería así, y al ejecutar el blueprint verás en pantalla del juego el mensaje devuelto al imprimir el gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###Utilice el modelo de OpenAI en el diseño.

* En el Blueprint, haz clic derecho para crear un nodo `Enviar solicitud de chat OpenAI en el mundo`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Crear un nodo de Opciones y establecer `Stream=true, Clave de API="tu clave de API de OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

* Crea Messages, agrega un Mensaje de Sistema y un Mensaje de Usuario respectivamente

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Crear un Delegado que reciba la información de salida del modelo y la imprima en la pantalla

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Traduce este texto al idioma español:

* El plano completo se verá así, ejecuta el plano y verás un mensaje devuelto en la pantalla del juego imprimiendo el modelo grande.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###El plano emplea Claude para analizar las imágenes.

Crea un nodo `Enviar solicitud de chat a Claude` haciendo clic derecho en el blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

*Crear nodo de Opciones y establecer `Stream=true, Clave de API="tu clave de API de Clude", Máximo de Tokens de Salida=1024`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

* Crear Messages, crear Texture2D desde archivo, y crear AIChatPlusTexture a partir de Texture2D, luego agregar AIChatPlusTexture a Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

* Al igual que el tutorial mencionado anteriormente, crea un Event y muestra la información en la pantalla del juego

Traduce este texto al idioma español:

* La representación visual del plano completo se ve así, al ejecutar el plano se puede ver el mensaje devuelto en la pantalla del juego imprimiendo un modelo grande.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

###Elaboramos imágenes con OpenAI mediante un plano.

Crear un nodo `Enviar solicitud de imagen de OpenAI` en el blueprint con clic derecho, y configurar `En Prompt="una hermosa mariposa"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Cree un nodo Options y establezca `Api Key="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Asociar el evento On Images y guardar la imagen en el disco local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

Traduce este texto al español:

* El aspecto de un plano completo es así, al ejecutar el plano, se puede ver que la imagen se guarda en la ubicación específica.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

##Registro de actualizaciones

### v1.3.3 - 2024.11.25

####Nuevas características

Apoyo a UE-5.5

###Solución de problemas

Reparar problemas con la ejecución de ciertos diseños.

### v1.3.2 - 2024.10.10

####Nueva característica

Reparar el fallo de cllama al detener manualmente la solicitud.

Arreglar el problema que impide encontrar los archivos ggml.dll y llama.dll al empaquetar la versión de descarga de win en la tienda.

* Durante la creación de la solicitud, verificar si se encuentra en el hilo del juego.

### v1.3.1 - 2024.9.30

####Nueva función

Añadir un SystemTemplateViewer, que permite ver y usar cientos de plantillas de configuración del sistema.

####Corrección de problemas

Reparar el complemento descargado desde la tienda, llama.cpp no puede encontrar la biblioteca de enlace.

* Corregido el problema de la ruta demasiado larga en LLAMACpp

Reparar el error de vinculación de llama.dll después de empaquetar en Windows.

Corregir el problema de lectura de la ruta del archivo en iOS/Android.

Corregir el error de configuración del nombre de Cllame

### v1.3.0 - 2024.9.23

####Traduce este texto al idioma español:

Función importante.

* Integración de llama.cpp que permite ejecutar modelos grandes de forma local sin conexión a internet

### v1.2.0 - 2024.08.20

####Nueva función

Apoyo a OpenAI Image Edit/Image Variation.

Compatible con la API de Ollama, admite la obtención automática de la lista de modelos admitidos por Ollama.

### v1.1.0 - 2024.08.07

####Nueva función

Apoyar el plan estratégico

### v1.0.0 - 2024.08.05

####Nueva funcionalidad

Función básica completa

Apoyo a OpenAI, Azure, Claude, Gemini

Un editor de chat integrado con funciones completas.

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
