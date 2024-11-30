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
description: Documento de instrucciones del complemento AIChatPlus de la UE.
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documento de instrucciones del plugin AIChatPlus de UE

##Repositorio público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complemento

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento de Unreal Engine que permite la comunicación con varios servicios de chat de inteligencia artificial GPT. Actualmente, admite servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama y llama.cpp local fuera de línea. En el futuro, seguirá incorporando más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que garantiza un rendimiento eficiente y facilita la integración de estos servicios de chat de IA para desarrolladores de Unreal Engine.

UE.AIChatPlus también incluye una herramienta de edición que permite utilizar directamente los servicios de chat de IA en el editor para generar texto e imágenes, analizar imágenes, etc.

##Instrucciones de uso

###Herramienta de chat del editor

El menú Tools -> AIChatPlus -> AIChat abre la herramienta de edición proporcionada por el complemento para chatear.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


La herramienta admite la generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Función principal

* Modelo grande sin conexión: Integración de la biblioteca llama.cpp, compatible con la ejecución sin conexión de modelos grandes en el dispositivo local

* Chat de texto: haz clic en el botón `New Chat` en la esquina inferior izquierda para crear una nueva conversación de chat de texto.

* Generación de imágenes: haz clic en el botón `New Image Chat` en la esquina inferior izquierda para iniciar una nueva sesión de generación de imágenes.

* Análisis de imagen: Algunos servicios de chat dentro de `New Chat` admiten el envío de imágenes, como Claude, Google Gemini. Simplemente haz clic en el botón 🖼️ o 🎨 ubicado encima del cuadro de texto para cargar la imagen que deseas enviar.

* Soporte de Blueprint (Blueprint): admite la creación de solicitudes de API Blueprint para funciones como chat de texto, generación de imágenes, etc.

Establecer el rol actual en el chat: El menú desplegable en la parte superior del cuadro de chat puede configurar el rol actual para enviar texto, permitiendo simular diferentes roles para ajustar la conversación con la IA.

Vaciar conversación: El botón ❌ en la parte superior de la ventana de chat puede eliminar el historial de mensajes de la conversación actual.

* Plantilla de diálogo: Incorpora cientos de plantillas de configuración de diálogo para facilitar el manejo de problemas comunes.

Traduce este texto al idioma español:

* Configuración global: al hacer clic en el botón `Settings` en la esquina inferior izquierda, se puede abrir la ventana de configuración global. Puede configurar el chat de texto predeterminado, los servicios de API de generación de imágenes y establecer los parámetros específicos de cada servicio de API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Traduce este texto al idioma español:

* Configuración de la conversación: Haz clic en el botón de configuración en la parte superior del cuadro de chat para abrir la ventana de configuración de la conversación actual. Permite cambiar el nombre de la conversación, modificar el servicio API utilizado en la conversación y ajustar los parámetros específicos del API para cada conversación de forma independiente. La configuración de las conversaciones se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Modificar el contenido del chat: al desplazar el ratón sobre el contenido del chat, aparecerá un botón de configuración para cada mensaje, que permite regenerar, modificar, copiar o eliminar el contenido, así como regenerar contenido debajo (para mensajes de usuarios).

* Vista de Imágenes: Para la generación de imágenes, al hacer clic en una imagen se abrirá la ventana de visualización de imágenes (ImageViewer), que admite guardar imágenes como PNG/UE Texture. Las Texturas se pueden ver directamente en el explorador de contenido (Content Browser), lo que facilita su uso dentro del editor. También se admite la eliminación de imágenes, regeneración de imágenes, continuación de la generación de más imágenes, entre otras funciones. Para los editores en Windows, también se admite copiar imágenes, lo que permite copiar imágenes directamente al portapapeles para facilitar su uso. Las imágenes generadas en una sesión también se guardarán automáticamente en la carpeta de cada sesión, generalmente en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

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

Utilización de modelos grandes sin conexión.

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Plantilla de diálogo

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introducción al código principal.

En la actualidad, el complemento se divide en los siguientes módulos:

* AIChatPlusCommon: Módulo de tiempo de ejecución, encargado de gestionar diversas solicitudes de API de IA y analizar el contenido de las respuestas.

* AIChatPlusEditor: Módulo del editor, responsable de implementar la herramienta de chat de IA del editor.

* AIChatPlusCllama: Módulo de tiempo de ejecución (Runtime), encargado de encapsular la interfaz y los parámetros de llama.cpp, para realizar la ejecución fuera de línea de modelos grandes

* Thirdparty/LLAMACpp: Módulo de terceros en tiempo de ejecución (Runtime), que integra las bibliotecas dinámicas y archivos de cabecera de llama.cpp.

Translate these text into Spanish language:

El UClass responsable específico del envío de solicitudes es FAIChatPlus_xxxChatRequest, cada servicio de API tiene su propio UClass de solicitud independiente. Las respuestas a las solicitudes se obtienen a través de dos tipos de UClass, UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase, solo es necesario registrar delegados de devolución de llamada correspondientes.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar, esto se hace mediante el FAIChatPlus_xxxChatRequestBody. El contenido específico de la respuesta también se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir la devolución, se puede obtener el ResponseBody a través de una interfaz específica.

Más detalles del código fuente están disponibles en la tienda de UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Guía de uso

###Utiliza el archivo offline del modelo llama.cpp en la herramienta del editor.

Translada el siguiente texto al español:

Instrucciones sobre cómo utilizar el modelo offline llama.cpp en la herramienta de edición AIChatPlus.

Descargue el modelo sin conexión desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloca el modelo en una carpeta específica, como por ejemplo en el directorio del proyecto de juego Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Abre la herramienta de edición AIChatPlus: Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat y abre la página de configuración de la sesión

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Establece la API en Cllama, activa la Configuración Personalizada de la API, añade la ruta de búsqueda de modelos y elige un modelo.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

* ¡Comenzar a chatear!¡¡

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###El código utiliza el modelo fuera de línea llama.cpp

La siguiente descripción explica cómo usar el modelo offline llama.cpp en tu código.

Primero, también necesitas descargar el archivo del modelo en la carpeta Content/LLAMA.

Agrega una línea de código para enviar un mensaje al modelo sin conexión dentro de un comando.

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

* Después de volver a compilar, simplemente usa el comando en el editor Cmd para ver los resultados de la salida del modelo grande en el registro OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Traduce estos textos al idioma español:

 蓝图使用离线模型 llama.cpp

A continuación se explica cómo utilizar el modelo offline llama.cpp en un blueprint.

Crea un nodo `Enviar solicitud de chat Cllama` con clic derecho en el plano de trabajo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Cree el nodo Options y establezca `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Cree Messages, agregue respectivamente un System Message y un User Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Crear un delegado que reciba la información de salida del modelo y la imprima en la pantalla

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Traduce este texto al idioma español:

* Una vez que ejecutes el blueprint completo, verás que la pantalla del juego imprime el mensaje devuelto por el modelo grande.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###Utilizar el modelo de OpenAI en el blueprint.

Crea un nodo llamado `Send OpenAI Chat Request In World` haciendo clic derecho en el blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Cree el nodo Options y configure `Stream=true, Api Key="tu clave API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Crear Messages, añadir un Mensaje del Sistema y un Mensaje del Usuario respectivamente.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Create un Delegado que reciba la información de salida del modelo y la imprima en la pantalla

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Traduce este texto al idioma español:

* La versión completa del diagrama se ve así, al ejecutarlo, se puede ver en la pantalla del juego el mensaje devuelto al imprimir el gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###La impresión azul utiliza Claude para analizar imágenes.

Crea un nodo `Enviar solicitud de chat a Claude` haciendo clic derecho en el diagrama.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

*Crear un nodo de Opciones y establecer `Stream=true, Api Key="tu clave de API de Clude", Max Output Tokens=1024`*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

* Crear Messages, crear Texture2D desde el archivo y luego crear AIChatPlusTexture a partir de Texture2D, y finalmente agregar AIChatPlusTexture al Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Siguiendo el tutorial mencionado, crea un Event y muestra la información en la pantalla del juego.

Traduce este texto al idioma español:

* Una vez que ejecutes el blueprint completo, podrás ver en la pantalla del juego el mensaje de retorno que imprime el gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

###La creación de imágenes con OpenAI Blueprint.

Crea un nodo `Send OpenAI Image Request` haciendo clic derecho en el diagrama y establece `In Prompt="una hermosa mariposa"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Crear un nodo de Opciones y establecer `Clave de API="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Vincular el evento On Images y guardar las imágenes en el disco duro local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

Traduce este texto al idioma español:

* La imagen completa del diagrama de flujo se ve así, al correr el diagrama de flujo se puede ver que la imagen se guarda en la ubicación especificada.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

##Registro de actualizaciones

### v1.3.3 - 2024.11.25

* Compatible con UE-5.5

* **Bugfix**: Solución de errores: Se corrigió el problema en el que algunas partes del diagrama no funcionaban.

### v1.3.2 - 2024.10.10

#### Bugfix

Reparar el fallo de cllama al detener manualmente la solicitud.

Corregir el problema de no poder encontrar los archivos ggml.dll llama.dll al empaquetar la versión de descarga de la tienda para Windows.

* Al crear la solicitud, se verifica si se encuentra en el hilo del juego, CreateRequest check in game thread

### v1.3.1 - 2024.9.30

Agregar un SystemTemplateViewer que permita ver y utilizar cientos de plantillas de configuración del sistema.

#### Bugfix

Repara el complemento descargado desde la tienda, no se puede encontrar la biblioteca de vínculos `llama.cpp`

Corregir el problema de la ruta demasiado larga en LLAMACpp

Arreglar el error de enlace de llama.dll después de empaquetar en Windows.

Corregir problema de lectura de rutas de archivo en iOS/Android

Corregir el error en la configuración del nombre de Cllame

### v1.3.0 - 2024.9.23

Actualización importante

* Se ha integrado llama.cpp para admitir la ejecución sin conexión local de modelos grandes.

### v1.2.0 - 2024.08.20

Apoyo para OpenAI Image Edit/Image Variation

Apoyo a la API de Ollama, compatible con la obtención automática de la lista de modelos admitidos por Ollama

### v1.1.0 - 2024.08.07

Apoyo al plan.

### v1.0.0 - 2024.08.05

Función Básica Completa

Apoyo a OpenAI, Azure, Claude, Gemini

Una herramienta de chat con un editor integrado y funciones completas.

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
