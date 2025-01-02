---
layout: post
title: Documentación de UE para el complemento AIChatPlus
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
description: Documento de instrucciones del complemento AIChatPlus de UE.
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documento de instrucciones del complemento UE AIChatPlus

##Almacén público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complementos

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento de UnrealEngine que permite la comunicación con varios servicios de chat de inteligencia artificial GPT. Actualmente, admite servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, y llama.cpp en modo fuera de línea local. En el futuro, se añadirá soporte para más proveedores de servicios. Su implementación se basa en solicitudes REST asincrónicas, lo que garantiza un alto rendimiento y facilita la integración de estos servicios de chat de IA para los desarrolladores de UnrealEngine.

UE.AIChatPlus también incluye una herramienta de edición que te permite utilizar directamente los servicios de chat de inteligencia artificial en el editor para crear texto e imágenes, analizar imágenes, entre otras funciones.

##Instrucciones de uso

###Herramienta de chat del editor

La barra de menú Tools -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


La herramienta admite la generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Función principal

- Modelo grande sin conexión: Integración de la biblioteca llama.cpp para admitir la ejecución local sin conexión de modelos grandes

* Texto del chat: Haz clic en el botón `Nuevo chat` en la esquina inferior izquierda para crear una nueva conversación de chat de texto.

* Generación de imagen: haz clic en el botón `New Image Chat` en la esquina inferior izquierda para crear una nueva sesión de generación de imágenes.

Análisis de imagen: Algunos servicios de chat de `Nuevo Chat` admiten el envío de imágenes, como Claude y Google Gemini. Solo tienes que hacer clic en el botón 🖼️ o 🎨 encima del cuadro de texto para cargar la imagen que deseas enviar.

Apoyo a Blueprint: Apoyo a la creación de solicitudes de API con Blueprint, para realizar funciones como chat de texto, generación de imágenes, entre otros.

Establecer el rol actual de chat: el menú desplegable en la parte superior del cuadro de chat puede configurar el rol actual para enviar texto, lo que permite simular diferentes roles para ajustar la conversación de IA.

Eliminar conversación: La opción ❌ en la parte superior de la ventana de chat permite borrar el historial de mensajes de la conversación actual.

Plantilla de diálogo: incluye cientos de plantillas de configuración de diálogo para facilitar el manejo de problemas comunes.

* Configuración global: al hacer clic en el botón `Setting` en la esquina inferior izquierda, se abre la ventana de configuración global. Puede establecer el chat de texto predeterminado, el servicio de API para generar imágenes y configurar los parámetros específicos de cada servicio de API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Configuración de la conversación: al hacer clic en el botón de configuración en la parte superior de la ventana de chat, se puede abrir la ventana de configuración de la conversación actual. Permite cambiar el nombre de la conversación, modificar el servicio de API utilizado en la conversación y ajustar los parámetros específicos de la API para cada conversación de forma independiente. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

Modificar contenido del chat: al colocar el ratón sobre el contenido del chat, aparecerá un botón de configuración para ese contenido en particular, que permitirá regenerar, modificar, copiar o eliminar el contenido, o regenerarlo debajo (para el contenido del chat de un usuario).

* Visualización de imágenes: En cuanto a la generación de imágenes, al hacer clic en una imagen se abrirá la ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como PNG/Textura UE, la textura se puede ver directamente en el explorador de contenidos (Content Browser), facilitando su uso dentro del editor. También se admite la eliminación de imágenes, la regeneración de imágenes, la generación de más imágenes, entre otras funciones. Para los editores en Windows, también se puede copiar imágenes para pegarlas directamente en el portapapeles para un uso conveniente. Las imágenes generadas durante la sesión se guardarán automáticamente en la carpeta de cada sesión, generalmente ubicada en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Plan:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Configuración global:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Configuración de la conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Editar el contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visor de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Utilizar modelos grandes sin conexión

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Plantilla de diálogo

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Presentación del código central

En la actualidad, el complemento se divide en los siguientes módulos:

* AIChatPlusCommon: Módulo de tiempo de ejecución, encargado de manejar las solicitudes de envío de diversas API de IA y analizar el contenido de las respuestas.

* AIChatPlusEditor: Módulo de edición, responsable de implementar la herramienta de chat AI del editor.

* AIChatPlusCllama: Módulo de tiempo de ejecución (Runtime) responsable de encapsular la interfaz y los parámetros de llama.cpp, para llevar a cabo la ejecución offline de modelos grandes.

* Thirdparty/LLAMACpp: Módulo de tercero en tiempo de ejecución (Runtime) que integra la biblioteca dinámica y los archivos de cabecera de llama.cpp.

La UClass responsable de enviar la solicitud específica es FAIChatPlus_xxxChatRequest, cada servicio de API tiene su propia UClass de solicitud independiente. Las respuestas a las solicitudes se obtienen a través de dos types de UClass: UAIChatPlus_ChatHandlerBase y UAIChatPlus_ImageHandlerBase, solo es necesario registrar los delegados de devolución de llamada correspondientes.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar, esto se hace a través de FAIChatPlus_xxxChatRequestBody. La respuesta específica también se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir la devolución, se puede obtener el ResponseBody a través de interfaces específicas.

Puede encontrar más detalles del código fuente en la tienda de UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Utiliza el modelo offline Cllama (llama.cpp) en la herramienta del editor.

La siguiente explicación detalla cómo utilizar el modelo offline llama.cpp en la herramienta de edición AIChatPlus.

Descargue el modelo sin conexión desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloca el modelo en una carpeta específica, por ejemplo, en el directorio Content/LLAMA del proyecto de juego.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Abre la herramienta de edición AIChatPlus: Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat y abre la página de configuración de la sesión.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Establecer Api como Cllama, activar Configuración de Api Personalizada, agregar la ruta de búsqueda de modelos y seleccionar un modelo.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

¡Comienza a charlar!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Utilice el modelo fuera de línea Cllama (llama.cpp) en la herramienta del editor para procesar imágenes.

Descargue el modelo fuera de línea MobileVLM_V2-1.7B-GGUF del sitio web de HuggingFace y colóquelo en el directorio Content/LLAMA también: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)Traduzca este texto al español:

Establecer el modelo de la sesión:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Enviar imagen para comenzar la conversación

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###Traduce este texto al idioma español:

Código de uso del modelo sin conexión Cllama(llama.cpp)

Traduce este texto al español:

El siguiente texto explica cómo usar el modelo fuera de línea llama.cpp en el código.

* Primero, también necesitas descargar el archivo del modelo en Content/LLAMA.

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

* Después de volver a compilar, puedes ver los resultados de la salida del modelo grande en el registro de salida OutputLog al usar comandos en la terminal del editor Cmd.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Traduce este texto al idioma español:

 蓝图使用离线模型 llama.cpp

Instrucciones sobre cómo utilizar el modelo offline llama.cpp en el blueprint.

Crea un nodo `Enviar solicitud de chat de Cllama` con el botón derecho en el diagrama.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Cree un nodo de Opciones y establezca `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Crear Messages, agregar un mensaje de System y un mensaje de Usuario respectivamente.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Crear un delegado que reciba la salida del modelo e imprima en la pantalla

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Traduce este texto al idioma español:

* La apariencia de un plano completo es la siguiente, ejecuta el plano y verás en la pantalla del juego el mensaje de retorno que imprime el modelo grande.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###El editor está utilizando OpenAI para chatear.

Abre la herramienta de chat Tools -> AIChatPlus -> AIChat, crea una nueva sesión de chat New Chat, establece la sesión ChatApi como OpenAI, y configura los parámetros de la interfaz.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

* Comenzar la conversación:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Cambiar el modelo a gpt-4o / gpt-4o-mini, permite utilizar la función de análisis visual de OpenAI en imágenes.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###Translate these text into Spanish language:

El editor utiliza OpenAI para procesar imágenes (crear/modificar/variaciones)

* En la herramienta de chat, crear una nueva conversación de imagen "New Image Chat", cambiar la configuración de la conversación a OpenAI y ajustar los parámetros.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

*Crear imagen*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

* Modificar la imagen, cambiar el tipo de chat de la imagen a "Editar" y subir dos imágenes, una que sea la imagen original y otra que sea la máscara donde las áreas transparentes (canal alfa en 0) representen las zonas que necesitan ser modificadas.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

* Transformación de imagen, cambia el tipo de chat de imagen a Variación, y sube una imagen, OpenAI generará una variante de la imagen original.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###La implementación del modelo de chat de OpenAI Blueprint.

* En el Editor de Blueprints, haz clic derecho para crear un nodo `Enviar solicitud de chat de OpenAI en el mundo`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Cree el nodo de Opciones y establezca `Stream=true, Api Key="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

* Crear Mensajes, añadir un Mensaje del Sistema y un Mensaje de Usuario respectivamente

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

*Crear un Delegado que reciba la información de salida del modelo y la imprima en la pantalla*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Traduce este texto al idioma español:

* Una vez que se ejecute el diseño completo, podrás ver en la pantalla del juego el mensaje que devuelve la impresión del gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Las impresiones usan OpenAI para crear imágenes

Crea un nodo `Enviar solicitud de imagen OpenAI` en el blueprint con clic derecho, y establece `En Prompt="una hermosa mariposa"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Crear un nodo de Options y establecer `Api Key="tu clave de API de OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Vincula el evento 'On Images' y guarda la imagen en el disco local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

* La versión completa del plan se ve así, al ejecutar el plan, puedes ver que la imagen se guarda en la ubicación especificada.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###El editor utiliza Azure.

* Crear una nueva conversación (New Chat), cambiar ChatApi a Azure y configurar los parámetros de la API de Azure

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

* Comenzar la conversación

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###El editor utiliza Azure para crear imágenes.

*Crear sesión de chat de imágenes (New Image Chat), cambiar ChatApi a Azure y configurar los parámetros de la API de Azure. Ten en cuenta que si es el modelo dall-e-2, es necesario establecer los parámetros Quality y Stype en not_use.*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Comienza la conversación para que Azure cree la imagen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Utilizar Azure Chat en el plano de Azure

Cree el siguiente blueprint, configure las opciones de Azure, haga clic en Ejecutar y verá en pantalla la información de chat devuelta por Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Crear imágenes con Azure mediante el uso de planos.

Cree el siguiente plan, configure las opciones de Azure, haga clic en ejecutar. Si la creación de la imagen tiene éxito, verá el mensaje "Create Image Done" en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

De acuerdo con la configuración del plano azul anterior, la imagen se guardará en la ruta D:\Descargas\mariposa.png.

## Claude

###El editor utiliza Claude para chatear y analizar imágenes

* Crear nueva conversación (New Chat), cambia ChatApi a Claude y configura los parámetros de la API de Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

*Comenzar a chatear*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Utiliza Blueprint para chatear con Claude y analizar imágenes.

En el diagrama, haz clic derecho para crear un nodo `Enviar solicitud de chat a Claude`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

* Crear nodo de Opciones, y establecer `Stream=true, Api Key="tu clave de API de Clude", Máximo de Tokens de Salida=1024`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

* Crear Messages, crear Texture2D desde el archivo y crear AIChatPlusTexture desde Texture2D, luego añadir AIChatPlusTexture a Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Sigue las instrucciones anteriores, crea un Event y muestra la información en la pantalla del juego.

Traduce este texto al idioma español:

* Un diseño completo se vería así, ejecuta el diseño y verás el mensaje devuelto en la pantalla del juego imprimiendo un modelo grande.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Obtener Ollama

Puedes obtener el paquete de instalación para instalar localmente desde el sitio web oficial de Ollama: [ollama.com](https://ollama.com/)

Puedes usar Ollama a través de la interfaz de Ollama proporcionada por otra persona.

###El editor utiliza Ollama para chatear y analizar imágenes.

* Nueva Conversación, cambia ChatApi a Ollama y establece los parámetros de la API de Ollama. Si es un chat de texto, establece el modelo como modelo de texto, como llama3.1; si necesitas manejar imágenes, establece el modelo como un modelo compatible con visión, como moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

* Comenzar la conversación

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###El plano utiliza Ollama para chatear y analizar imágenes.

Cree el siguiente diagrama, configure las Ollama Options, haga clic en Ejecutar, y verá la información de chat devuelta por Ollama impresa en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###El editor utiliza Gemini.

* Iniciar nueva conversación (Nuevo Chat), cambiar ChatApi a Gemini y configurar los parámetros de la Api de Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

* Comenzar la conversación

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###Utilice Gemini Chat para planificar.

Cree el siguiente plan, configure las opciones de Gemini, haga clic en ejecutar y verá impresas en la pantalla la información del chat que Gemini devuelve.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)


##Registro de actualizaciones

### v1.4.1 - 2025.01.04

####Solución de problemas

* La herramienta de chat admite enviar solo imágenes sin mensajes.

Corregir fallo en el envío de imágenes a través de la API de OpenAI.

Corregir la omisión de los parámetros Quality, Style y ApiVersion en la configuración de las herramientas de chat de OpanAI y Azure.

### v1.4.0 - 2024.12.30

####Nueva función

* (Función experimental) Llama(llama.cpp) soporta modelos multimodales, capaz de procesar imágenes

Todos los parámetros de tipo de planos han sido provistos con indicaciones detalladas.

### v1.3.4 - 2024.12.05

####Nueva característica

OpenAI apoya la API de visión.

####Reparación de problemas

Corregir error al configurar OpenAI stream=false.

### v1.3.3 - 2024.11.25

####Nueva función

Apoyo para UE-5.5

####Solución de problemas

Corrección de problemas en los que algunas plantillas no funcionaban correctamente.

### v1.3.2 - 2024.10.10

####Reparación de problemas

* Corregido el fallo de cllama al detener manualmente la solicitud

Corregido el problema de no encontrar los archivos ggml.dll y llama.dll al empaquetar la versión de descarga de win en la tienda.

* Al realizar la solicitud, se verifica si se encuentra en el hilo del juego, CreateRequest verifica en el hilo del juego.

### v1.3.1 - 2024.9.30

####Nueva función

Agrega un SystemTemplateViewer que te permita ver y utilizar varios cientos de plantillas de configuración del sistema.

####Reparación de problemas

Reparar el plugin descargado desde la tienda, no se puede encontrar la biblioteca de enlace llama.cpp

Arreglar problema de ruta demasiado larga en LLAMACpp.

Reparar el error de enlace de llama.dll después de empaquetar en Windows.

Corregir problema de lectura de ruta de archivos en iOS/Android.

* Corregir el error de configuración de Cllame estableciendo el nombre correctamente

### v1.3.0 - 2024.9.23

####Traduzca este texto al idioma español:

Nueva e importante funcionalidad

* Integrado llama.cpp, compatible con la ejecución offline de modelos grandes en local.

### v1.2.0 - 2024.08.20

####Nueva función.

Apoyo a OpenAI Image Edit/Image Variation

Admite la API de Ollama, admite la obtención automática de la lista de modelos admitidos por Ollama.

### v1.1.0 - 2024.08.07

####Nueva funcionalidad

Apoyo al plan.

### v1.0.0 - 2024.08.05

####Nueva función

Funciones básicas completas

Apoyo a OpenAI, Azure, Claude, Gemini

* Herramienta de chat integrada con un editor completo.

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
