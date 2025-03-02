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
description: Documentación de instrucciones del complemento UE AIChatPlus
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documento de instrucciones del complemento UE AIChatPlus

##Almacén público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complemento.

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento para UnrealEngine que permite la comunicación con diversos servicios de chat AI GPT. Actualmente, soporta servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, y llama.cpp en modo offline local. En el futuro se añadirán más servicios proveedores. Su implementación se basa en solicitudes REST asíncronas para lograr un alto rendimiento, facilitando así a los desarrolladores de Unreal Engine integrar estos servicios de chat AI.

UE.AIChatPlus también incluye una herramienta de edición que permite utilizar directamente los servicios de chat AI en el editor para generar texto e imágenes, analizar imágenes, entre otras funciones.

##Instrucciones de uso

###Herramienta de chat del editor.

En la barra de menú, selecciona Herramientas -> AIChatPlus -> AIChat para abrir la herramienta de edición de chat proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


El software admite generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Función principal

Modelo grande sin conexión: Integración de la biblioteca llama.cpp que permite la ejecución sin conexión de modelos grandes a nivel local.

Crear una nueva conversación de texto: haz clic en el botón `Nuevo Chat` en la esquina inferior izquierda para iniciar una nueva conversación de texto.

Generación de imágenes: Haz clic en el botón `New Image Chat` en la esquina inferior izquierda para iniciar una nueva sesión de generación de imágenes.

Análisis de imágenes: Algunos servicios de chat de "New Chat" admiten el envío de imágenes, como Claude, Google Gemini. Simplemente haz clic en el botón 🖼️ o 🎨 encima del campo de entrada para cargar la imagen que deseas enviar.

Apoyo a los planos (Blueprint): apoyo a la creación de planos API, para llevar a cabo funciones como chat de texto, generación de imágenes, etc.

Establecer el personaje de chat actual: el menú desplegable en la parte superior del cuadro de chat te permite seleccionar el personaje desde el cual se enviará el texto, lo que te permitirá simular diferentes roles para ajustar la conversación con la inteligencia artificial.

Vaciar conversación: al hacer clic en la ❌ en la parte superior del cuadro de chat, se pueden borrar los mensajes históricos de la conversación actual.

Plantilla de conversación: Incorpora cientos de configuraciones de plantillas de diálogo para facilitar el manejo de problemas comunes.

Configuración general: Al hacer clic en el botón `Configuración` en la esquina inferior izquierda, se abrirá la ventana de configuración general. Aquí podrás ajustar la configuración predeterminada para el chat de texto, los servicios de API de generación de imágenes y definir los parámetros específicos para cada servicio de API. Los ajustes se guardarán automáticamente en la ruta del proyecto `$(CarpetaProyecto)/Guardado/AIChatPlusEditor`.

Configuración de la conversación: al hacer clic en el botón de configuración en la parte superior del cuadro de chat, puedes abrir la ventana de configuración de la conversación actual. Permite modificar el nombre de la conversación, el servicio API utilizado en la conversación, así como establecer parámetros específicos para cada uso de API en la conversación. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Editar contenido del chat: al colocar el cursor sobre el contenido del chat, aparecerá un botón de configuración para ese contenido en particular, que permitirá regenerar, modificar, copiar o eliminar el contenido, así como regenerar contenido debajo (para el contenido creado por el usuario).

Visor de imágenes: Para la generación de imágenes, al hacer clic en una imagen se abrirá una ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como PNG/Textura UE, la cual puede ser visualizada directamente en el explorador de contenido (Content Browser) para su conveniente uso en el editor. También se admiten funciones como eliminar imágenes, regenerarlas, y continuar generando más imágenes. En el editor de Windows, también es posible copiar imágenes directamente al portapapeles para facilitar su uso. Las imágenes generadas en cada sesión se guardarán automáticamente en la carpeta de cada sesión, generalmente en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Plan:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Configuración general:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Configuración de conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modificar el contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visualizador de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Utilización de modelos grandes sin conexión.

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Plantilla de diálogo

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introducción al código central.

En este momento, el complemento se divide en los siguientes módulos:

AIChatPlusCommon: Módulo de tiempo de ejecución, responsable de manejar las solicitudes enviadas a través de varias API de IA y analizar el contenido de las respuestas.

AIChatPlusEditor: Módulo de editor, encargado de implementar la herramienta de chat de IA del editor.

AIChatPlusCllama: Módulo de tiempo de ejecución (Runtime), encargado de encapsular la interfaz y parámetros de llama.cpp, para llevar a cabo la ejecución sin conexión de grandes modelos.

Thirdparty/LLAMACpp: Módulo de terceros en tiempo de ejecución que integra la biblioteca dinámica y los archivos de encabezado de llama.cpp.

El UClass responsable específico de enviar la solicitud es FAIChatPlus_xxxChatRequest, cada servicio API tiene su propio UClass de solicitud independiente. Las respuestas de la solicitud se obtienen a través de UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase dos UClass, solo es necesario registrar el delegado de devolución de llamada correspondiente.

Antes de enviar la solicitud, es necesario configurar los parámetros API y el mensaje a enviar. Esto se hace a través de FAIChatPlus_xxxChatRequestBody. El contenido específico de la respuesta también se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir la devolución se puede obtener el ResponseBody a través de una interfaz específica.

Puedes encontrar más detalles del código fuente en la tienda de UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Utiliza la herramienta del editor para trabajar con el modelo sin conexión Cllama(llama.cpp).

A continuación se explica cómo utilizar el modelo fuera de línea llama.cpp en la herramienta de edición AIChatPlus.

Primero, descarga el modelo sin conexión desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloque el modelo en una carpeta específica, por ejemplo, en el directorio Content/LLAMA del proyecto del juego.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Abre la herramienta de edición AIChatPlus: Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat y accede a la página de configuración de la sesión.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Configura la API como Cllama, activa la Configuración Personalizada de la API, añade la ruta de búsqueda de modelos y selecciona el modelo.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Comenzar la conversación!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Utiliza la herramienta del editor para procesar imágenes con el modelo fuera de línea Cllama(llama.cpp).

Descarga el modelo MobileVLM_V2-1.7B-GGUF de HuggingFace y colócalo en el directorio Content/LLAMA bajo el nombre [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)Lo siento, no hay texto para traducir. ¿Hay algo más en lo que pueda ayudarte?

Configura el modelo de la sesión:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Enviar una imagen para comenzar la conversación.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###El código utiliza el modelo fuera de línea Cllama (llama.cpp).

Estas indicaciones muestran cómo utilizar el modelo offline llama.cpp en el código.

Primero, también debes descargar el archivo del modelo en Content/LLAMA.

Agregar una orden al código para enviar un mensaje al modelo sin conexión dentro de esa orden.

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

Después de recompilar, simplemente utiliza el comando en el editor Cmd y podrás ver los resultados de la gran modelo en el registro OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###El uso del modelo fuera de línea del plano se llama llama.cpp.

Translate these text into Spanish language:

Cómo usar el modelo fuera de línea llama.cpp en un diagrama de conector.

En el diagrama, haz clic derecho para crear un nodo llamado `Enviar solicitud de chat de Cllama`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Cree un nodo Options y establezca `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Crear mensajes, agregar un mensaje del sistema y un mensaje del usuario.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Crear un Delegado que reciba la información de salida del modelo y la imprima en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

La traducción al español es la siguiente:

* La apariencia de un blueprint completo es la siguiente, activa el blueprint y podrás ver en la pantalla del juego el mensaje devuelto al imprimir el modelo grande.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###El archivo llama.cpp utiliza la GPU.

Agregar la opción "Num Gpu Layer" a "Cllama Chat Request Options" para configurar la carga de GPU en llama.cpp, como se muestra en la imagen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

Puedes usar nodos de blueprints para determinar si el entorno actual es compatible con GPU y obtener los backends compatibles con dicho entorno.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_2.png)

###Procesar archivos de modelos en el archivo .Pak después de la empaquetación.

Una vez que se crea el archivo Pak, todos los recursos del proyecto se almacenan en el archivo .Pak, incluyendo los archivos gguf del modelo sin conexión.

Debido a que llama.cpp no puede leer directamente archivos .Pak, es necesario copiar los archivos de modelos fuera del archivo .Pak en el sistema de archivos.

AIChatPlus ofrece una función que automáticamente copia y procesa los archivos de modelos dentro de un archivo .Pak, y los guarda en la carpeta Saved:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

O puedes manejar los archivos de modelo en .Pak tú mismo, lo importante es copiar y procesar los archivos, ya que llama.cpp no puede leer correctamente .Pak.

## OpenAI

###El editor utiliza el chat de OpenAI.

Abre la herramienta de chat Tools -> AIChatPlus -> AIChat, crea una nueva conversación New Chat, establece la sesión ChatApi en OpenAI, configura los parámetros de la interfaz

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Iniciar chat:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Cambiar el modelo a gpt-4o / gpt-4o-mini permitirá utilizar la función de análisis visual de OpenAI en las imágenes.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###El editor utiliza OpenAI para trabajar con imágenes (crear/modificar/variar).

Crear una nueva conversación de imagen en la herramienta de chat, etiquetarla como OpenAI y ajustar la configuración según sea necesario.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Crear imagen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Modificar la imagen cambiando el tipo de chat de la imagen a "Editar", luego subir dos imágenes: una imagen original y otra donde la máscara muestre las áreas que necesitan ser modificadas (donde el canal alfa es 0).

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Modificar el tipo de chat de imagen a "Variation" y subir una imagen. OpenAI devolverá una variante de la imagen original.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Utilizando el modelo de OpenAI para chatear con el plano de ejecución.

En el mapa, haz clic derecho para crear un nodo llamado `Enviar solicitud de chat de OpenAI en el mundo`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Crear el nodo de opciones y establecer `Stream=true, Api Key="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Crear mensajes, añadir un mensaje del sistema y un mensaje de usuario respectivamente.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Crear un delegado para recibir la información de salida del modelo y mostrarla en pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

La versión completa del plan se ve así, ejecuta el plan y podrás ver en la pantalla del juego el mensaje devuelto al imprimir el modelo grande.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Utilizando OpenAI para crear imágenes.

En el panel de control, haz clic derecho para crear un nodo 'Send OpenAI Image Request' y configura 'In Prompt="una hermosa mariposa"'.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Crea un nodo Options y establece `Api Key="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Asociar el evento "On Images" y guardar las imágenes en el disco duro local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

La apariencia de un plano detallado completo es esta, al ejecutar el programa, podrás ver la imagen guardada en la ubicación especificada.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###El editor utiliza Azure.

Crear nueva conversación (New Chat), cambiar ChatApi a Azure y establecer los parámetros de la Api de Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Comenzar la conversación

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###Utilizar Azure para crear imágenes en el editor.

Crear una nueva sesión de chat de imágenes (New Image Chat), cambiar ChatApi a Azure y configurar los parámetros de la API de Azure. Ten en cuenta que, si se trata del modelo dall-e-2, es necesario establecer los parámetros Quality y Stype en not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Comience la conversación para que Azure cree la imagen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Utilizando Azure Chat para el Blueprint.

Crea el siguiente diseño, configura las opciones de Azure, haz clic en Ejecutar y verás en pantalla la información de chat que Azure devuelve.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Utilizando Azure para crear imágenes de manera profesional.

Establezca el plan detallado a continuación, configure las opciones de Azure, haga clic en "Ejecutar". Si la creación de la imagen tiene éxito, verá el mensaje "Imagen creada" en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

Según la configuración del esquema anterior, la imagen se guardará en la ruta D:\Descargas\mariposa.png

## Claude

###El editor utiliza a Claude para chatear y analizar imágenes.

Crear nueva conversación (Nuevo Chat), cambiar ChatApi a Claude y configurar los parámetros de la API de Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Comenzar a chatear

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Utilizando Blueprint para chatear y analizar imágenes con Claude.

En el plano, haz clic derecho para crear un nodo llamado `Enviar solicitud de chat a Claude`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Crear un nodo de opciones y configurar `Stream=true, Api Key="tu clave de API de Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Crear mensajes, crear una Texture2D desde un archivo, y luego usar esa Texture2D para crear un AIChatPlusTexture, y finalmente agregar ese AIChatPlusTexture al mensaje.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Sigue el tutorial mencionado para crear un evento y mostrar la información en la pantalla del juego.

La interpretación del texto sería la siguiente:

* La apariencia completa del blueprint es así, al ejecutar el blueprint, se puede ver en la pantalla del juego el mensaje de retorno de la impresión de un gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Obtener Ollama

Puedes descargar el paquete de instalación localmente desde el sitio web oficial de Ollama: [ollama.com](https://ollama.com/)

Se puede usar Ollama a través de la interfaz Ollama proporcionada por otros.

###El editor utiliza Ollama para chatear y analizar imágenes.

Por favor traduzca el texto al español:

* 新建会话（New Chat），把 ChatApi 改为 Ollama，并设置 Ollama 的 Api 参数。如果是文本聊天，则设置模型为文本模型，如 llama3.1；如果需要处理图片，则设置模型为支持 vision 的模型，例如 moondream。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Comenzar a chatear

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Utilizando Ollama, la aplicación permite chatear y analizar imágenes.

Crear el siguiente plan, configurar las Ollama Options, hacer clic en ejecutar y verás la información de chat devuelta por Ollama impresa en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###Utilizar Gemini en el editor.

Crear nuevo chat, cambiar ChatApi a Gemini y configurar los parámetros de la API de Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Iniciar chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###El editor utiliza Gemini para enviar el audio.

Seleccionar entre leer el audio desde un archivo / desde un recurso / grabarlo desde el micrófono, para generar el audio que se desea enviar.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

Iniciar el chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###Utilizar el chat Gemini en Blueprints.

Crear el siguiente plan, configurar las Opciones de Gemini, hacer clic en Ejecutar y verás en la pantalla la información de chat devuelta por Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###Utilizando Gemini, se envía el audio del plano.

Crea el siguiente plan, configura la carga de audio, establece las opciones de Gemini, haz clic en ejecutar y verás en pantalla la información de chat devuelta después de que Gemini haya procesado el audio.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###El editor utiliza Deepseek.

Crear una nueva conversación (New Chat), cambiar ChatApi por OpenAi y configurar los parámetros de la API de Deepseek. Agregar un nuevo modelo de candidato llamado deepseek-chat y configurar el modelo como deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Comenzar la conversación.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Utilizar el chat Deepseek en Blueprint.

Crea el siguiente esquema, configura las Opciones de Solicitud relacionadas con Deepseek, incluyendo Modelo, URL base, URL de punto final, ApiKey, entre otros parámetros. Haz clic en ejecutar y podrás ver en pantalla la información de chat devuelta por Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##Nodo de función adicional proporcionado en el plano de diseño.

###Llama 相关

"La llama de Cllama es válida": Determine si Cllama llama.cpp está inicializado correctamente

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Comprueba si llama.cpp es compatible con el backend de GPU en el entorno actual".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Obtener Soporte de Backends de Llama": Obtener todos los backends compatibles con llama.cpp actuales.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Preparar archivo de modelo de Cllama en Pak": Automáticamente copia los archivos de modelo en Pak al sistema de archivos.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###Imagen relacionada

"Convertir UTexture2D a Base64": Convertir la imagen de UTexture2D en formato base64 PNG.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

Guardar UTexture2D en un archivo .png.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

"Cargar archivo .png en UTexture2D": Cargar archivo .png en UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Duplicar UTexture2D"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###Audio-related.

Cargar archivo .wav en USoundWave.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

"Convertir datos .wav a USoundWave": Convertir datos binarios .wav a USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

Guardar USoundWave en un archivo .wav.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

Obtener datos PCM sin procesar de USoundWave: Convierte USoundWave en datos binarios de audio.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"Convertir USoundWave a Base64": Convertir USoundWave a datos Base64

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicar USoundWave": Duplicar USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

"Convertir datos de captura de audio a USoundWave": Convert Audio Capture 录音数据转成 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

##Registro de actualizaciones

### v1.6.0 - 2025.03.02

####Nueva característica.

Actualización del archivo llama.cpp a la versión b4604.
Cllama supports GPU backends: cuda and metal.
La herramienta de chat Cllama es compatible con el uso de GPU.
Soportar la lectura de archivos de modelo empaquetados en Pak.

#### Bug Fix

Corregir el problema de Cllama que provocaba que se bloqueara al recargar durante la deducción.

Reparar error de compilación en iOS.

### v1.5.1 - 2025.01.30

####Nueva característica

Solo se permite el envío de audio a través de Gemini.

Optimizamos el método para obtener PCMData, descomprimiendo los datos de audio al generar B64.

Solicitar agregar dos funciones de callback OnMessageFinished y OnImagesFinished.

Optimizar el Método Gemini para obtener automáticamente el Método basándose en bStream.

Agregar algunas funciones de blueprint para facilitar la conversión de Wrapper a tipos reales, y obtener el Mensaje de Respuesta y el Error.

#### Bug Fix

Corregir el problema de múltiples llamadas a Request Finish.

### v1.5.0 - 2025.01.29

####Nueva característica

Apoyar el envío de audio a Gemini.

Las herramientas del editor admiten el envío de audio y grabaciones.

#### Bug Fix

Corregir el error de copia fallida de la sesión.

### v1.4.1 - 2025.01.04

####Reparación de problemas

La herramienta de chat admite enviar solo imágenes sin texto.

Reparar problema de envío de imágenes en la interfaz de OpenAI.

Reparar el problema de parámetros faltantes Quality, Style, ApiVersion en la configuración de herramientas de chat OpanAI y Azure.

### v1.4.0 - 2024.12.30

####Nueva característica

* (Función experimental) Cllama (llama.cpp) admite modelos multimodales y puede procesar imágenes.

Se han añadido indicaciones detalladas a todos los parámetros de tipo Blueprint.

### v1.3.4 - 2024.12.05

####Nueva característica.

OpenAI admite la API de visión.

####Reparación de problemas

Reparar el error al establecer OpenAI stream=false.

### v1.3.3 - 2024.11.25

####Nueva característica.

Compatibilidad con UE-5.5.

####Reparación de problemas

Corregir el problema de que algunas partes del plano no funcionen.

### v1.3.2 - 2024.10.10

####Reparación de problemas

Reparar el bloqueo de la aplicación cuando se detiene la solicitud manualmente.

Solucionar el problema de no encontrar los archivos ggml.dll y llama.dll al empaquetar la versión de descarga de Win en la tienda.

Crear solicitud y verificar si está en el hilo del juego.

### v1.3.1 - 2024.9.30

####Nueva función

Agregar un SystemTemplateViewer, que permite visualizar y utilizar cientos de plantillas de configuración del sistema.

####Reparación de problemas

Reparar el plugin descargado desde la tienda, no se encuentra la biblioteca de enlace llama.cpp.

Corregido el problema de la longitud excesiva de la ruta en LLAMACpp.

Reparar el error de enlace de llama.dll después de empaquetar en Windows.

Corregir el problema de lectura de la ruta del archivo en iOS/Android.

Repare el error al establecer el nombre de la llamada.

### v1.3.0 - 2024.9.23

####Importante nueva característica

Integración de llama.cpp para permitir la ejecución offline de modelos grandes en el entorno local.

### v1.2.0 - 2024.08.20

####Nueva funcionalidad.

Apoyo a OpenAI Image Edit/Image Variation

Admite la API de Ollama, admite la obtención automática de la lista de modelos admitidos por Ollama.

### v1.1.0 - 2024.08.07

####Nueva función

Apoyo de la propuesta.

### v1.0.0 - 2024.08.05

####Nueva característica.

Funcionalidad básica completa

Apoyo a OpenAI, Azure, Claude, Gemini.

Herramienta de chat con editor integrado y funciones completas.

--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor [**反馈**](https://github.com/disenone/wiki_blog/issues/new)Señalar cualquier omisión. 
