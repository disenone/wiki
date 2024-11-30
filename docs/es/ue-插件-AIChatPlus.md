---
layout: post
title: Documento de instrucciones del complemento UE AIChatPlus.
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

##Almacén público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complemento

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Presentación del complemento

Este complemento es compatible con UE5.2+.


UE.AIChatPlus es un complemento para UnrealEngine que permite la comunicación con varios servicios de chat de inteligencia artificial GPT. Actualmente es compatible con OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, y llama.cpp en modo offline. En el futuro, se agregarán más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que garantiza un alto rendimiento y facilita a los desarrolladores de UE integrar estos servicios de chat de IA.

UE.AIChatPlus también incluye una herramienta de edición que te permite utilizar directamente los servicios de chat de IA en el editor, para generar texto e imágenes, y analizar imágenes, entre otras funciones.

##Instrucciones de uso

###Herramienta de chat del editor

La barra de menú Herramientas -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


La herramienta admite la generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Funciones principales

* Modelo grande fuera de línea: Integración de la biblioteca llama.cpp para admitir la ejecución de modelos grandes fuera de línea de forma local

* Chat de texto: haz clic en el botón `Nuevo Chat` en la esquina inferior izquierda para crear una nueva conversación de chat de texto.

* Generación de imágenes: haz clic en el botón `New Image Chat` en la esquina inferior izquierda para iniciar una nueva sesión de generación de imágenes.

* Análisis de imagen: Algunos servicios de chat de `New Chat` admiten el envío de imágenes, como Claude, Google Gemini. Simplemente haz clic en el botón 🖼️ o 🎨 en la parte superior del cuadro de entrada para cargar la imagen que deseas enviar.

* Soporte de Blueprint: soporte para la creación de solicitudes de API utilizando blueprints para funciones como chat de texto, generación de imágenes, entre otras.

Establecer el rol actual de la conversación: el menú desplegable en la parte superior de la ventana de chat permite seleccionar el rol actual para enviar texto y simular diferentes roles para ajustar la conversación de IA.

Borrar conversación: El botón ❌ en la parte superior de la ventana de chat permite eliminar el historial de mensajes de la conversación actual.

* Plantilla de conversación: incorpora cientos de plantillas de configuración de diálogo para facilitar el manejo de problemas comunes.

Translate these text into Spanish language:

* Configuración global: haz clic en el botón `Configuración` en la esquina inferior izquierda para abrir la ventana de configuración global. Puedes establecer el chat de texto predeterminado, el servicio de API para generación de imágenes y configurar los parámetros específicos de cada servicio de API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Traduce este texto al idioma español:

* Configuración de la conversación: Al hacer clic en el botón de configuración en la parte superior del cuadro de chat, puedes abrir la ventana de configuración de la conversación actual. Permite cambiar el nombre de la conversación, modificar el servicio API utilizado en la conversación y ajustar los parámetros específicos del API para cada conversación de forma independiente. La configuración de la conversación se guarda automáticamente en `$(CarpetaProyecto)/Saved/AIChatPlusEditor/Sessions`

Modificar contenido del chat: Al colocar el mouse sobre el contenido del chat, aparecerá un botón de ajustes para ese contenido de chat en particular, que permitirá regenerar, modificar, copiar, eliminar o regenerar debajo el contenido (para los mensajes del rol de usuario).

* Exploración de imágenes: Para la generación de imágenes, al hacer clic en una imagen se abrirá la ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como PNG/UE Texture. Las Textures se pueden ver directamente en el explorador de contenido (Content Browser), lo que facilita su uso en el editor. También se admiten funciones como eliminar imágenes, regenerarlas, continuar generando más imágenes, entre otras. En el editor de Windows, también se puede copiar imágenes, lo que permite copiarlas directamente al portapapeles para un uso conveniente. Las imágenes generadas en la sesión también se guardarán automáticamente en la carpeta de cada sesión, generalmente en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

**Traducción:**

**Blueprint:**

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Configuración global:

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

En la actualidad, el complemento se divide en los siguientes módulos:

* AIChatPlusCommon: Módulo de tiempo de ejecución, encargado de manejar solicitudes de envío de diversas API de IA y analizar el contenido de las respuestas.

* AIChatPlusEditor: Módulo de edición, encargado de implementar la herramienta de chat AI del editor.

* AIChatPlusCllama: Módulo de tiempo de ejecución (Runtime), encargado de encapsular la interfaz y los parámetros de llama.cpp, para llevar a cabo la ejecución sin conexión de grandes modelos.

* Thirdparty/LLAMACpp: Módulo de terceros en tiempo de ejecución (Runtime) que integra la biblioteca dinámica y los archivos de encabezado de llama.cpp.

Traduce estos textos al idioma español:

La UClass responsable específica de enviar la solicitud es FAIChatPlus_xxxChatRequest, cada servicio de API tiene su propia UClass de solicitud independiente. Las respuestas de la solicitud se obtienen a través de dos tipos de UClass, UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase, solo necesitas registrar el delegado de devolución de llamada correspondiente.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar, esto se hace utilizando FAIChatPlus_xxxChatRequestBody. La respuesta específica también se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir la devolución, se puede obtener el ResponseBody a través de una interfaz específica.

Puede encontrar más detalles del código fuente en la tienda UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##**Guía de uso**

###Utiliza el modelo fuera de línea llama.cpp en la herramienta del editor.

Translate these text into Spanish language:

A continuación se explica cómo utilizar el modelo fuera de línea llama.cpp en la herramienta de edición AIChatPlus.

Descargue el modelo fuera de línea desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloca el modelo en una carpeta específica, por ejemplo en el directorio Content/LLAMA del proyecto de juego.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Abre la herramienta del editor AIChatPlus: Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat y abre la página de configuración de la sesión.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Establece Api en Cllama, activa Configuraciones de Api Personalizadas y agrega la ruta de búsqueda de modelos, luego selecciona el modelo.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

¡Comencemos a chatear!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###El código utiliza el modelo offline llama.cpp

Traduzca el texto a continuación al español:

Cómo usar el modelo fuera de línea llama.cpp en el código.

Primero, de igual manera es necesario descargar el archivo del modelo en Content/LLAMA.

* Modifica el código para agregar un comando y enviar un mensaje al modelo fuera de línea dentro del comando.

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

* Después de volver a compilar, simplemente utiliza el comando en la ventana Cmd del editor para visualizar los resultados de la salida del gran modelo en el registro OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###El archivo del modelo offline del plano se llama llama.cpp.

La siguiente explicación detalla cómo utilizar el modelo offline llama.cpp en un blueprint.

Crea un nodo `Enviar solicitud de chat de Cllama` haciendo clic derecho en el diagrama.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Cree el nodo Options y establezca `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

* Crea Mensajes, añade un Mensaje de Sistema y un Mensaje de Usuario respectivamente

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Crear un Delegado que acepte la salida del modelo e imprima la información en la pantalla

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Traduce este texto al idioma español:

* Una vez que pongamos en funcionamiento el blueprint completo, veremos un mensaje en la pantalla de juego que nos indica la creación del modelo a gran escala.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###Utilizar un modelo de OpenAI para el diseño de planos.

Crea un nodo `Enviar solicitud de chat de OpenAI en el mundo` haciendo clic derecho en el mapa.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Cree el nodo Options y configure `Stream=true, Api Key="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

*Crear Mensajes, añadir un Mensaje del Sistema y un Mensaje del Usuario respectivamente*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Crea un Delegado que reciba la información de salida del modelo y la imprima en la pantalla

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Traduce este texto al idioma español:

* La apariencia completa del blueprint es la siguiente: al ejecutar el blueprint, podrás ver un mensaje que devuelve la pantalla del juego imprimiendo un gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###El plano emplea Claude para analizar imágenes.

Crea un nodo `Enviar solicitud de chat a Claude` haciendo clic derecho en el esquema.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

*Crear un nodo de opciones y establecer `Stream=true, Api Key="tu clave API de Clude", Max Output Tokens=1024`.*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

*Crear Messages, crear Texture2D desde archivo, y crear AIChatPlusTexture desde Texture2D, luego agregar AIChatPlusTexture a Message*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

*Al igual que en el tutorial anterior, crea un Event y muestra la información en la pantalla del juego*

Traduce este texto al idioma español:

* Una vista completa del blueprint se vería así, al ejecutar el blueprint, verás en la pantalla del juego el mensaje devuelto al imprimir el gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

###Traduce este texto al español:

Blueprint usa OpenAI para crear imágenes.

Crea un nodo `Send OpenAI Image Request` haciendo clic derecho en el blueprint y establece `In Prompt="una hermosa mariposa"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Crea un nodo de Opciones y establece `Api Key="tu clave de API de OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Vincula el evento On Images y guarda la imagen en el disco local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

Translate these text into Spanish language:

* La apariencia completa del diagrama de flujo es así, al ejecutar el diagrama de flujo, se puede ver que la imagen se guarda en la ubicación especificada.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

##Actualización de registro

### v1.3.3 - 2024.11.25

Apoyo a UE-5.5

* **Bugfix**: Corrección de problemas con la ejecución de ciertos blueprints

### v1.3.2 - 2024.10.10

#### Bugfix

Reparar el fallo de cllama al detener manualmente la solicitud.

Corregir el problema de la versión de descarga de win en la tienda de aplicaciones que no encuentra los archivos ggml.dll y llama.dll.

* Al crear la solicitud, se verifica si se encuentra en el hilo de juego. CreateRequest se comprueba en el hilo de juego.

### v1.3.1 - 2024.9.30

Agregar un SystemTemplateViewer, para ver y utilizar cientos de plantillas de configuración del sistema.

#### Bugfix

Reparar el complemento descargado desde la tienda, llama.cpp no puede encontrar la biblioteca de vínculos.

Corregir problema de ruta demasiado larga en LLAMACpp

Corregir el error de enlace llama.dll después de empaquetar Windows.

Corregir problema de lectura de ruta de archivo en ios/android.

Corregir el error al establecer el nombre de Cllame

### v1.3.0 - 2024.9.23

Actualización importante

Se ha integrado llama.cpp para admitir la ejecución en modo fuera de línea de modelos grandes de forma local.

### v1.2.0 - 2024.08.20

Apoyo a OpenAI Image Edit/Image Variation

Apoyar la API de Ollama, apoyar la obtención automática de la lista de modelos admitidos por Ollama

### v1.1.0 - 2024.08.07

Apoyo al plan.

### v1.0.0 - 2024.08.05

Base de datos completa.

Apoyo a OpenAI, Azure, Claude, Gemini

* Editor de chat integrado con funciones completas

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
