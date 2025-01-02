---
layout: post
title: Documentación de la extensión AIChatPlus de la UE
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
description: Documento de instrucciones del complemento AIChatPlus de UE
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documento de especificaciones del complemento AIChatPlus de UE

##Repositorio público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complemento

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

This plugin supports UE5.2+.

UE.AIChatPlus es un complemento de UnrealEngine que permite la comunicación con diversos servicios de chat de inteligencia artificial GPT. Actualmente, admite servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama y llama.cpp en modo local sin conexión a internet. En el futuro, se incorporarán más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que garantiza un rendimiento eficiente y facilita a los desarrolladores de Unreal Engine conectarse a estos servicios de chat de inteligencia artificial.

UE.AIChatPlus también incluye una herramienta de edición que te permite utilizar directamente los servicios de chat de IA en el editor, generar texto e imágenes, y analizar imágenes, entre otras funciones.

##Instrucciones de uso

###Herramienta de chat del editor

El menú Tools -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


La herramienta admite la generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es más o menos así:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####**Función principal**

* Modelo grande sin conexión: Integración de la librería llama.cpp para admitir la ejecución sin conexión de modelos grandes a nivel local.

* Chat de texto: haz clic en el botón `Nuevo Chat` en la esquina inferior izquierda para crear una nueva conversación de chat de texto.

* Generación de imágenes: Haz clic en el botón `New Image Chat` en la esquina inferior izquierda para crear una nueva sesión de generación de imágenes.

Análisis de imágenes: Algunos servicios de chat en la función `Nueva Conversación` admiten el envío de imágenes, como Claude y Google Gemini. Simplemente haz clic en el botón 🖼️ o 🎨 ubicado encima del cuadro de texto para cargar la imagen que deseas enviar.

Traduce estos textos al idioma español:

* Soporte de Blueprint: admite la creación de solicitudes de API en Blueprint para realizar funciones como chat de texto, generación de imágenes, entre otros.

Establecer el personaje actual en el chat: el menú desplegable en la parte superior del cuadro de chat permite seleccionar el personaje actual para enviar texto, lo que permite simular diferentes personajes para ajustar la conversación con la inteligencia artificial.

Limpiar conversación: al pulsar la ❌ en la parte superior de la ventana de chat, puedes borrar el historial de mensajes de la conversación actual.

* Plantilla de diálogo: incorpora cientos de plantillas de configuración de diálogo para facilitar el manejo de problemas comunes.

Traduce este texto al idioma español:

* Configuración global: al hacer clic en el botón `Configuración` en la esquina inferior izquierda, se puede abrir la ventana de configuración global. Se pueden configurar el chat de texto predeterminado, el servicio de API para generar imágenes y especificar los parámetros de cada servicio de API en concreto. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Conversación configuración: al hacer clic en el botón de configuración en la parte superior del cuadro de chat, se puede abrir la ventana de configuración de la conversación actual. Permite cambiar el nombre de la conversación, modificar el servicio API utilizado para la conversación y ajustar los parámetros específicos de API para cada conversación de forma independiente. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

* Modificación de contenido de chat: Al pasar el ratón sobre el contenido del chat, aparecerá un botón de ajustes para ese contenido de chat, que permite regenerar, modificar, copiar o borrar el contenido, así como regenerar el contenido debajo (para el contenido creado por usuarios).

* Exploración de imágenes: En cuanto a la generación de imágenes, al hacer clic en una imagen se abrirá una ventana de visualización de imágenes (ImageViewer), que admite guardar las imágenes como PNG/UE Texture. Las Textures se pueden ver directamente en el explorador de contenido (Content Browser), lo que facilita su uso dentro del editor. También se permite eliminar imágenes, volver a generar imágenes, continuar generando más imágenes, entre otras funciones. Para el editor en Windows, también es posible copiar imágenes, lo que permite copiarlas directamente al portapapeles para un uso más conveniente. Las imágenes generadas en la sesión se guardarán automáticamente en la carpeta de cada sesión, con la ruta habitual siendo `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

**Blueprint:**

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Configuración global:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Configuración de la conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modifica el contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visor de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Utilizar modelos grandes sin conexión.

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Plantilla de diálogo

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Presentación del código principal

Actualmente, el complemento se divide en los siguientes módulos:

* AIChatPlusCommon: Módulo de tiempo de ejecución (Runtime), encargado de manejar solicitudes de envío de diversas API de IA y analizar el contenido de las respuestas.

* AIChatPlusEditor: Módulo del editor, encargado de implementar la herramienta de chat de IA en el editor.

* AIChatPlusCllama: Módulo de tiempo de ejecución (Runtime) que encapsula la interfaz y los parámetros de llama.cpp, permitiendo la ejecución offline de grandes modelos.

* Thirdparty/LLAMACpp: Módulo de terceros en tiempo de ejecución (Runtime), que integra la biblioteca dinámica y los archivos de cabecera de llama.cpp.

Translate these text into Spanish language:

El UClass responsable específico de enviar las solicitudes es el FAIChatPlus_xxxChatRequest; cada tipo de servicio API tiene su UClass de solicitud independiente respectivo. Para obtener las respuestas de las solicitudes, se utilizan dos UClass diferentes: UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase. Solo es necesario registrar el delegado de devolución de llamada correspondiente.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar, lo cual se realiza a través de FAIChatPlus_xxxChatRequestBody. La respuesta se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir la devolución, se puede obtener el ResponseBody a través de una interfaz específica.

Se puede obtener más detalles del código fuente en la tienda de UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Los editores de herramientas usan el modelo fuera de línea en Cllama(llama.cpp)

Traduce el siguiente texto al idioma español:

Instrucciones sobre cómo utilizar el modelo fuera de línea llama.cpp en la herramienta de edición AIChatPlus.

Descarga primero el modelo offline desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloca el modelo en una carpeta específica, por ejemplo dentro del directorio del proyecto de videojuegos Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Abre la herramienta de edición AIChatPlus: Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat y abre la página de configuración de la sesión.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Establezca Api en Cllama, active la configuración de Api personalizada, agregue la ruta de búsqueda de modelos y seleccione el modelo.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

¡Comencemos a charlar!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Utiliza el modelo sin conexión Cllama(llama.cpp) en la herramienta del editor para procesar imágenes.

Descarga el modelo MobileVLM_V2-1.7B-GGUF de HuggingFace y colócalo en el directorio Content/LLAMA: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)。

Establecer el modelo de sesión:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

*Iniciar una conversación enviando una imagen*

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###Traduce este texto al idioma español:

Código utilizando el modelo fuera de línea Cllama(llama.cpp)

La siguiente descripción explica cómo usar el modelo offline llama.cpp en el código.

Por supuesto, aquí está la traducción solicitada:

* Primero, también necesitas descargar el archivo del modelo en Content/LLAMA.

* Modifica el código para agregar un comando y enviar un mensaje al modelo sin conexión dentro del comando.

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

Después de volver a compilar, simplemente utiliza el comando en el editor Cmd y podrás ver los resultados de la salida del modelo grande en el registro OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###El archivo blueprint está utilizando el modelo offline llama.cpp.

Estas instrucciones detallan cómo utilizar el modelo fuera de línea llama.cpp en el blueprint.

* En el panel de control, haz clic derecho para crear un nodo `Enviar solicitud de chat de Cllama`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Crear el nodo Options y establecer `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

*Crear Messages, agregar un System Message y un User Message respectivamente*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

*Crear Delegate para recibir la información de salida del modelo y mostrarla en la pantalla*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Traduce este texto al español:

* The complete blueprint looks like this, run the blueprint, and you will see the message returned on the game screen printing a large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###El editor utiliza chat de OpenAI

Abre la herramienta de chat Herramientas -> IAChatPlus -> IAChat, crea una nueva sesión de chat Nuevo Chat, establece la sesión de chat ChatApi como OpenAI, establece <api_key>.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

*Comenzar la conversación:*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Cambiar el modelo a gpt-4o / gpt-4o-mini permite utilizar la función de análisis visual de OpenAI en las imágenes.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###El editor utiliza OpenAI para procesar imágenes (crear/modificar/variaciones)

* Al crear una nueva sesión de chat de imágenes en ChatGPT, modifique la configuración de la sesión a OpenAI y establezca \<api_key\>.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

* Crear imagen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

* Modifique la imagen, cambie el tipo de chat de imagen a Edit, y cargue dos imágenes, una es la imagen original y la otra es la máscara donde las áreas transparentes (canal alfa igual a 0) indican las partes que necesitan ser modificadas.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

* Transformación de imagen: cambia el tipo de chat de imagen a Edit y carga una imagen. OpenAI devolverá una variante de la imagen original.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###La fundación Blueprint utiliza modelos de charla de OpenAI.

Cree un nodo llamado `Enviar solicitud de chat OpenAI en el mundo` haciendo clic derecho en el diagrama.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Cree un nodo de Options y establezca `Stream=true, Api Key="tu clave de API de OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

*Crear Messages, agregar un mensaje del sistema y un mensaje de usuario.*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Crear un delegado que reciba la información de salida del modelo y la imprima en pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Traduce este texto al idioma español:

* Un plano completo se vería así, ejecuta el plano y verás un mensaje en la pantalla del juego imprimiendo el gran modelo devuelto.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Traduce este texto al español:

Blueprint utilizando OpenAI para crear imágenes

Cree un nodo `Send OpenAI Image Request` haciendo clic derecho en el diagrama y configure `In Prompt="a beautiful butterfly"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

* Crear nodo Options y establecer `Api Key="tu clave de API de OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Vincular el evento En imágenes y guardar la imagen en el disco duro local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

Traduce estos textos al idioma español:

* Una vez finalizado el blueprint, éste se ejecutará y podrás ver la imagen guardada en la ubicación especificada.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_5.png)

## Azure

###El editor utiliza Azure

* Crear nueva conversación (New Chat), cambiar ChatApi a Azure y configurar los parámetros de la Api de Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

* Comenzar a chatear

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###El editor utiliza Azure para crear imágenes.

* Crear una sesión de imagen nueva (New Image Chat), cambiar ChatApi a Azure y configurar los parámetros de la Api de Azure. Ten en cuenta que, si es el modelo dall-e-2, es necesario establecer los parámetros Quality y Stype en not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

* Comienza a chatear para que Azure cree la imagen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Traduce este texto al español:

Blueprint utilizando Azure Chat.

Cree el siguiente diagrama, configure las opciones de Azure, haga clic en Ejecutar y verá impresa en pantalla la información de chat devuelta por Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Utilice Azure para crear imágenes de referencia.

Cree el siguiente diagrama, configure las Opciones de Azure, haga clic en Ejecutar. Si la creación de la imagen es exitosa, verá el mensaje "Creación de imagen completada" en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

De acuerdo con la configuración del plano azul anterior, la imagen se guardará en la ruta D:\Descargas\mariposa.png

## Claude

###El editor utiliza Claude para chatear y analizar imágenes.

* Crear nueva conversación (New Chat), cambiar ChatApi a Claude, y configurar los parámetros de la API de Claude

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Comience a conversar

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###El plano usa Claude para chatear y analizar imágenes.

Crea un nodo `Enviar solicitud de chat a Claude` haciendo clic derecho en el plano de trabajo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Cree el nodo de opciones y establezca `Stream=true, Api Key="clave de API de Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

* Crear Messages, crear Texture2D desde archivo y luego crear AIChatPlusTexture desde Texture2D, finalmente agregar AIChatPlusTexture a Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Siguiendo el tutorial anterior, crea un Event y muestra la información en la pantalla del juego.

Traduce este texto al idioma español:

* Un plano completo se ve así, ejecuta el plano y verás en la pantalla de juego el mensaje devuelto al imprimir el gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Obtener Ollama

Puedes obtener el paquete de instalación para instalar localmente a través del sitio web oficial de Ollama: [ollama.com](https://ollama.com/)

Se puede utilizar Ollama a través de la interfaz Ollama proporcionada por otras personas.

###El editor utiliza Ollama para chatear y analizar imágenes.

* Crea una nueva conversación (New Chat), cambia ChatApi por Ollama y configura los parámetros de la API de Ollama. Si es un chat de texto, establece el modelo como modelo de texto, como llama3.1; si necesitas procesar imágenes, configura el modelo como un modelo compatible con visión, como moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

* Comenzar la conversación

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###El plano utiliza Ollama para chatear y analizar imágenes

Cree el siguiente diagrama, configure las opciones de Ollama, haga clic en Ejecutar y verá la información de chat devuelta por Ollama impresa en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###El editor utiliza Gemini

* Nueva conversación (New Chat), cambia ChatApi por Gemini y configura los parámetros de la API de Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

*Comenzar a chatear*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###El diagrama de Gemini utiliza el chat.

Crea el siguiente plan, configura las Opciones de Gemini, haz clic en Ejecutar y verás impresa en la pantalla la información de chat devuelta por Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)


##**Registro de actualizaciones**

### v1.4.0 - 2024.12.30

####Nuevas características

* (Función experimental) Llama (llama.cpp) admite modelos multimodales y puede procesar imágenes

Todos los parámetros de tipo blueprint ahora tienen instrucciones detalladas.

### v1.3.4 - 2024.12.05

####Nueva característica

OpenAI supports la API de visión

####Reparación de problemas

Corregir el error al establecer stream=false en OpenAI.

### v1.3.3 - 2024.11.25

####Nuevas características

Apoyar UE-5.5

####Corrección de problemas

* Corregir el problema de que algunas blueprints no funcionen.

### v1.3.2 - 2024.10.10

####Solución de problemas

Reparar el fallo de cllama al detener manualmente la solicitud.

* Corregir el problema de la versión de descarga de Win en la tienda que no puede encontrar los archivos ggml.dll llama.dll al empaquetar.

* Al crear una solicitud, se comprueba si se encuentra en el hilo del juego, Comprobar en GameThread al crear solicitud

### v1.3.1 - 2024.9.30

####Nueva funcionalidad

Agregar un SystemTemplateViewer para poder ver y utilizar cientos de plantillas de configuración del sistema.

####Solución de problemas

Reparar el plugin descargado de la tienda, llama.cpp no encuentra la biblioteca de enlace.

* Solucionar problema de trayectoria demasiado larga en LLAMACpp

Corregir el error de enlace llama.dll después de empaquetar en Windows

* Corregir problema de lectura de rutas de archivo en iOS/Android

Corregir el error de configuración del nombre en Cllame

### v1.3.0 - 2024.9.23

####**Importante nueva característica**

Integra llama.cpp para admitir la ejecución sin conexión local de grandes modelos.

### v1.2.0 - 2024.08.20

####Nueva función

Apoyo a OpenAI Image Edit/Image Variation.

Apoyo a la API de Ollama, apoyo para obtener automáticamente la lista de modelos admitidos por Ollama.

### v1.1.0 - 2024.08.07

####Nueva característica

Apoyar el plan 


### v1.0.0 - 2024.08.05

####Nueva característica

Función básica completa

Apoyo a OpenAI, Azure, Claude, Gemini.

* Herramienta de chat con editor integrado bien equipado

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
