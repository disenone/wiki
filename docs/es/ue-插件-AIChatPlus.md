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
description: Documento de instrucciones de UE sobre el complemento AIChatPlus
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documento de instrucciones del complemento UE AIChatPlus.

##Almacén público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complementos.

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento para UnrealEngine que permite la comunicación con varios servicios de chat de inteligencia artificial GPT. Actualmente, brinda soporte para servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama y llama.cpp en modo offline local. En el futuro, seguirá agregando soporte para más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que proporciona un alto rendimiento y facilita la integración de estos servicios de chat de IA para desarrolladores de UE.

UE.AIChatPlus también incluye una herramienta de edición que te permite utilizar directamente los servicios de chatbot de inteligencia artificial en el editor para generar texto e imágenes, analizar imágenes, entre otras funciones.

##Instrucciones de uso

###Herramienta de chat del editor.

La opción Tools -> AIChatPlus -> AIChat en la barra de menú abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


El software permite generar texto, chatear por escrito, crear imágenes y analizar imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Función principal

Modelo grande sin conexión: integración de la biblioteca llama.cpp para admitir la ejecución local sin conexión de modelos grandes.

Traducir estos textos al español:

* Chat de texto: Haz clic en el botón `Nuevo Chat` en la esquina inferior izquierda para crear una nueva sesión de chat de texto.

Generación de imágenes: Haz clic en el botón `Nueva imagen en el chat` en la esquina inferior izquierda para iniciar una nueva sesión de generación de imágenes.

Análisis de imágenes: Parte de los servicios de chat de `New Chat` admiten el envío de imágenes, como Claude, Google Gemini. Para cargar la imagen que desees enviar, simplemente haz clic en el botón 🖼️  o 🎨 ubicado encima del cuadro de texto.

Apoyo a los Blueprint: Apoyo para crear solicitudes de API utilizando Blueprint, lo que permite funciones como chat de texto, generación de imágenes, entre otras.

Establecer el personaje actual de la conversación: El menú desplegable en la parte superior de la ventana de chat te permite seleccionar el personaje actual para enviar mensajes, lo que te permite simular diferentes roles para ajustar la conversación con la IA.

Vaciar conversación: el botón ❌ en la parte superior del cuadro de chat permite borrar el historial de mensajes de la conversación actual.

Plantilla de diálogo: Incorpora cientos de configuraciones predefinidas para facilitar la gestión de problemas comunes.

* Configuración global: Al hacer clic en el botón `Configuración` en la esquina inferior izquierda, se puede abrir la ventana de configuración global. Se puede configurar el chat de texto predeterminado, el servicio API de generación de imágenes y establecer los parámetros específicos de cada servicio API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Configuración de la conversación: al hacer clic en el botón de configuración en la parte superior de la ventana de chat, puedes abrir la ventana de configuración de la conversación actual. Permite cambiar el nombre de la conversación, modificar los servicios de API utilizados en la conversación y ajustar parámetros específicos de API para cada conversación de manera independiente. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

Editar contenido del chat: Al colocar el ratón sobre el contenido del chat, aparecerá un botón de ajustes para ese chat en particular, que permitirá regenerar, modificar, copiar o borrar el contenido, así como regenerar contenido debajo (si es contenido del usuario).

Visualización de imágenes: Para la generación de imágenes, al hacer clic en una imagen se abrirá la ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como PNG/UE Texture. Las Texturas se pueden ver directamente en el Explorador de Contenidos, facilitando su uso en el editor. También se pueden borrar imágenes, regenerarlas o seguir generando más. En el editor de Windows, también se puede copiar imágenes para facilitar su uso al copiarlas al portapapeles. Las imágenes generadas en la sesión se guardarán automáticamente en la carpeta de cada sesión, cuya ruta normalmente es `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Blueprint:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Configuración general:

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

###Introducción al código central

En la actualidad, el complemento se divide en los siguientes módulos:

AIChatPlusCommon: El módulo de tiempo de ejecución, responsable de manejar solicitudes de envío de API de inteligencia artificial y analizar el contenido de las respuestas.

AIChatPlusEditor: Módulo de editor, responsable de implementar la herramienta de chat de IA del editor.

AIChatPlusCllama: "运行时模块 (Runtime)" es responsable de encapsular las interfaces y parámetros de llama.cpp, permitiendo la ejecución offline de modelos grandes.

Terceros/LLAMACpp: Módulo de terceros en tiempo de ejecución que integra la biblioteca dinámica y los archivos de cabecera de llama.cpp.

El UClass específico encargado de enviar la solicitud es FAIChatPlus_xxxChatRequest. Cada servicio API tiene su propio UClass de solicitud independiente. Las respuestas de las solicitudes se obtienen a través de UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase. Solo es necesario registrar los delegados de devolución de llamada correspondientes.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar, esto se hace utilizando FAIChatPlus_xxxChatRequestBody. La respuesta detallada también se analiza en FAIChatPlus_xxxChatResponseBody, la cual se puede obtener a través de una interfaz específica al recibir la devolución de llamada.

Más detalles del código fuente están disponibles en la tienda de Unreal Engine: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Utilizando el modelo fuera de línea Cllama(llama.cpp) en la herramienta del editor.

La siguiente explicación muestra cómo utilizar el modelo offline llama.cpp en la herramienta de edición AIChatPlus.

(https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloca el modelo en una carpeta específica, como por ejemplo en el directorio Content/LLAMA del proyecto de juego.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Abre la herramienta de edición AIChatPlus: Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat y abre la página de configuración de la sesión.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Establezca la API como Cllama, active la configuración personalizada de la API y agregue la ruta de búsqueda de modelos, luego elija el modelo.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

¡Comencemos a chatear!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Utilizando el modelo fuera de línea Cllama (llama.cpp) en la herramienta del editor para procesar imágenes.

Descarga el modelo MobileVLM_V2-1.7B-GGUF de HuggingFace y colócalo en el directorio Content/LLAMA con el nombre [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)Lo siento, no puedo traducir esos caracteres. ¿Hay algo más en lo que pueda ayudarte?

Establecer el modelo de la sesión:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Enviar imagen para comenzar la conversación

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###El código utiliza el modelo fuera de línea Cllama(llama.cpp)

Se proporcionan instrucciones sobre cómo usar el modelo fuera de línea llama.cpp en el código.

Primero, también necesitas descargar el archivo del modelo en la carpeta Content/LLAMA.

Modificar el código para agregar un comando y enviar un mensaje al modelo sin conexión dentro del comando.

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

Después de compilar nuevamente, al utilizar el comando en la ventana de comandos del editor, podrás ver los resultados de la salida del modelo en el registro OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###El archivo llama.cpp utiliza el modelo fuera de línea del diagrama.

A continuación se explica cómo usar el modelo sin conexión llama.cpp en el blueprint.

En el blueprint, haz clic derecho para crear un nodo `Enviar Solicitud de Chat de Llama`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Cree el nodo Options y establezca `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Crear Messages, añadir un mensaje del sistema y un mensaje de usuario.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Crear un Delegado para recibir la información de salida del modelo y mostrarla en pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Una vez ejecutada la impresión de la maqueta grande, se podrá visualizar la pantalla de juego mostrando el mensaje de retorno.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###El archivo llama.cpp utiliza la GPU.

"Añadir opción de solicitud de chat de Cllama" incluye el parámetro "Num Gpu Layer", que se puede configurar en gpu payload de llama.cpp, como se muestra en la imagen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

Puedes utilizar nodos de blueprints para determinar si el entorno actual es compatible con GPU y obtener los backends soportados por dicho entorno.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_2.png)

###Procesar archivos de modelos en el archivo .Pak después de empaquetar.

Una vez que se activa el empaquetado Pak, todos los archivos de recursos del proyecto se guardarán en el archivo .Pak, incluyendo los archivos de modelo offline gguf.

Debido a que llama.cpp no admite la lectura directa de archivos .Pak, es necesario copiar los archivos de modelos sin conexión del archivo .Pak al sistema de archivos.

AIChatPlus ofrece una función que automáticamente copia y procesa los archivos de modelo en .Pak, y los guarda en la carpeta Saved.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

O bien, puedes encargarte tú mismo de los archivos de modelo en el archivo .Pak, la clave está en copiar y gestionar los archivos, llama.cpp no puede leer correctamente el archivo .Pak.

## OpenAI

###El editor está utilizando OpenAI para chatear.

Abre la herramienta de chat Tools -> AIChatPlus -> AIChat, crea una nueva conversación New Chat, establece la sesión ChatApi en OpenAI, y configura los parámetros de la interfaz.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Comenzar chat:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Cambiar el modelo a gpt-4o / gpt-4o-mini permite utilizar la función de análisis visual de imágenes de OpenAI.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###Utilizar OpenAI para procesar imágenes en el editor (crear/modificar/variar)

Crear una nueva conversación de imagen en la herramienta de chat, cambiar la configuración de la conversación a OpenAI y ajustar los parámetros.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Crear imagen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Modificar la imagen, cambiar el tipo de chat de la imagen a editar y subir dos imágenes: una imagen original y otra donde la máscara muestre las áreas que necesitan ser modificadas, identificadas por las zonas transparentes (canal alfa igual a 0).

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Modifica la variante de la imagen cambiando el tipo de chat de imagen a "Variation", y sube una imagen. OpenAI generará una variante de la imagen original.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Utilizando el modelo de chat de OpenAI en Blueprint.

Crea un nodo llamado `Send OpenAI Chat Request In World` haciendo clic derecho en el plano de trabajo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Crea el nodo Options y asigna `Stream=true, Api Key="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Crear mensajes, agregar un mensaje de sistema y un mensaje de usuario.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Crear un delegado que reciba la información de salida del modelo y la imprima en pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

La apariencia completa del blueprint es la siguiente, al ejecutar el blueprint, podrás ver en la pantalla del juego el mensaje devuelto al imprimir el modelo en gran formato.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Utilizando OpenAI para crear imágenes conforme al diseño.

En el blueprint, haz click derecho para crear un nodo llamado `Send OpenAI Image Request`, y configura `In Prompt="una hermosa mariposa"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Crea un nodo de opciones y establece `Api Key="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Vincula el evento On Images y guarda las imágenes en el disco local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

El diseño completo se ve así, ejecuta el diseño y verás que la imagen se guarda en la ubicación especificada.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###El editor utiliza Azure.

Crear una nueva conversación (New Chat), cambiar ChatApi por Azure y configurar los parámetros de la API de Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Comience la conversación.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###Use Azure to create images in the editor.

Crear una nueva sesión de imagen (New Image Chat), cambiar ChatApi a Azure y configurar los parámetros de la API de Azure. Ten en cuenta que, si es el modelo dall-e-2, los parámetros Quality y Stype deben configurarse como not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Comience la conversación para que Azure cree la imagen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Utilizando Azure Chat para planificar.

Cree el siguiente diagrama, configure las opciones de Azure, haga clic en 'Ejecutar' y podrá ver en la pantalla la información del chat devuelta por Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Utilizando Azure, se crea la imagen según el plano.

Crea el siguiente plan, configura las opciones de Azure, haz clic en ejecutar. Si la creación de la imagen se realiza con éxito, verás el mensaje "Create Image Done" en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

De acuerdo con la configuración del diagrama anterior, la imagen se guardará en la ruta D:\Descargas\mariposa.png

## Claude

###El editor usa Claude para chatear y analizar imágenes.

Crear una nueva conversación (New Chat), cambiar ChatApi a Claude y configurar los parámetros de la Api de Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Comenzar a chatear

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Utilizar Blueprint para chatear y analizar imágenes con Claude.

En la interfaz azul, haz clic derecho para crear un nodo llamado `Enviar solicitud de chat a Claude`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Crear un nodo de Opciones y establecer `Stream=true, Api Key="tu clave API de Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Crear mensajes, crear un Texture2D desde un archivo, y luego a partir de ese Texture2D crear un AIChatPlusTexture para luego añadirlo al mensaje.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Crear un evento como se describe en el tutorial anterior y mostrar la información en la pantalla del juego.

El texto traducido al español sería:

"La representación completa del blueprint se ve así, ejecuta el blueprint y podrás ver en la pantalla del juego el mensaje devuelto al imprimir el modelo grande."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Obtener Ollama

Puedes descargar el paquete de instalación directamente desde el sitio web oficial de Ollama: [ollama.com](https://ollama.com/)

Se puede usar Ollama a través de la interfaz de Ollama proporcionada por otra persona.

###El editor usa Ollama para chatear y analizar imágenes.

Crear una nueva conversación (Nuevo Chat), cambiar ChatApi a Ollama, y configurar los parámetros de la API de Ollama. Si es un chat de texto, establecer el modelo como llama3.1; si se requiere procesamiento de imágenes, configurar el modelo como uno que admita visión, por ejemplo, moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Iniciar chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Utilizamos Ollama para chatear y analizar imágenes en BluePrint.

Genera el siguiente diagrama, configura las Ollama Options, haz clic en "Ejecutar" y podrás ver en pantalla la información de chat retornada por Ollama.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###Utilizando Gemini como editor.

Crear un nuevo chat, cambiar ChatApi a Gemini y configurar los parámetros de la API de Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Comenzar la conversación.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###El editor utiliza Gemini para enviar audio.

Seleccionar entre leer audio desde un archivo, desde un activo o grabar desde un micrófono para generar el audio que se debe enviar.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

Comenzar la conversación.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###Utilice la función de chat de Gemini en el plano de trabajo.

Cree el siguiente plan, configure las opciones de Gemini, haga clic en Ejecutar y verá en la pantalla la información de chat devuelta por Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###Utiliza Blueprint para enviar audio con Gemini.

Crear el siguiente plan, configurar la carga de audio, ajustar las opciones de Géminis, hacer clic en ejecutar, y verás en pantalla la información de chat devuelta tras el procesamiento de audio por Géminis.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###El editor utiliza Deepseek.

Crear una nueva conversación (New Chat), cambiar ChatApi por OpenAi y configurar los parámetros de la API de Deepseek. Agregar un nuevo modelo candidato llamado deepseek-chat y establecer el modelo como deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Iniciar conversación.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Utilizar Deepseek para chatear en Blueprint.

Cree un plan como se indica a continuación, configure las opciones de solicitud relacionadas con Deepseek, como el Modelo, la URL base, la URL final, la clave de API, entre otros parámetros. Haga clic en Ejecutar y verá en la pantalla la información de chat devuelta por Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##Nodo de función de diagrama adicional proporcionado.

###Llama 相关

"Cllama Is Valid" translates to "Cllama es válido"：判断 Cllama llama.cpp 是否正常初始化"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Comprueba si llama.cpp es compatible con GPU en el entorno actual."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Obtener Soporte Backend de Llama": Obtén todos los backends soportados por llama.cpp actualmente.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama Prepare ModelFile In Pak": Copia automáticamente los archivos de modelo de Pak al sistema de archivos.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###Imágenes relacionadas.

"Convertir UTexture2D a Base64": Convierte la imagen de UTexture2D a formato png en Base64.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

Guardar UTexture2D en un archivo .png.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

Cargar archivo .png en UTexture2D: Cargar archivo .png en UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Duplicar UTexture2D"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###Audio relacionado

"Load .wav file to USoundWave": Cargar archivo .wav en USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

Convertir datos .wav a USoundWave: Convertir los datos binarios .wav a USoundWave.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

Guardar USoundWave como archivo .wav

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

"Obtener datos PCM brutos de USoundWave": Convertir USoundWave en datos binarios de audio.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"Convierte USoundWave a Base64"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicar USoundWave"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

Convertir los datos de captura de audio en USoundWave: Convert Audio Capture Data to USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

##Registro de actualizaciones

### v1.6.0 - 2025.03.02

####Nueva función

Actualización del archivo llama.cpp a la versión b4604.

Cllama supports GPU backends: cuda and metal.

La herramienta de chat Cllama es compatible con el uso de GPU.

Soporte para leer archivos de modelos empaquetados en Pak.

#### Bug Fix

Corregido el problema de fallo de Cllama al recargar durante el razonamiento.

Reparar errores de compilación en iOS.

### v1.5.1 - 2025.01.30

####Nuevas características

* Solo se permite a Gemini enviar archivos de audio.

Optimizar el método para obtener los datos de PCM y descomprimir los datos de audio al generar B64.

Solicitud de agregar dos callbacks OnMessageFinished y OnImagesFinished.

Optimizar el Método Gemini, para automáticamente obtener el Método según bStream.

Agregar algunas funciones de blueprint para facilitar la conversión del Wrapper al tipo real, y obtener el mensaje de respuesta y el error.

#### Bug Fix

Reparar el problema de múltiples llamadas a Request Finish.

### v1.5.0 - 2025.01.29

####Nueva funcionalidad.

Apoyar el envío de archivos de audio a Gemini.

Las herramientas del editor admiten el envío de audio y grabaciones.

#### Bug Fix

Corregir el error de falla al copiar la sesión.

### v1.4.1 - 2025.01.04

####Reparación de problemas.

La herramienta de mensajería permite enviar solo imágenes sin incluir texto.

* Corregir el problema de envío de imágenes en la interfaz de OpenAI.

Reparar el problema omitido en la configuración de las herramientas de chat OpanAI y Azure, que se refiere a los parámetros Quality, Style y ApiVersion.

### v1.4.0 - 2024.12.30

####Nueva función.

* (Función experimental) Cllama (llama.cpp) es compatible con modelos multimodales y puede procesar imágenes.

Todos los parámetros de tipo de plano han sido provistos con detalles de orientación.

### v1.3.4 - 2024.12.05

####Nueva función

OpenAI soporta la API de visión.

####Reparación de problemas

Corregir el error al establecer OpenAI stream=false.

### v1.3.3 - 2024.11.25

####Nueva función

Soporta UE-5.5.

####Reparación de problemas

Corregir el problema de que algunas partes del diseño no funcionen correctamente.

### v1.3.2 - 2024.10.10

####Reparación de problemas

Reparar el fallo de cllama al detener manualmente la solicitud.

Solucionar el problema de no encontrar los archivos ggml.dll y llama.dll al empaquetar la versión de descarga de la tienda en Windows.

Crear solicitud comprueba en el hilo del juego.

### v1.3.1 - 2024.9.30

####Nueva función

Agregar un SystemTemplateViewer que permita visualizar y utilizar cientos de plantillas de configuración del sistema.

####Reparación de problemas

Reparar el complemento descargado desde la tienda, llama.cpp no puede encontrar la biblioteca de vínculos.

Corregir el problema de la longitud excesiva de la ruta en LLAMACpp

Reparar el error llama.dll después de empaquetar en Windows.

Corregir problema de acceso a la ruta de archivo en iOS/Android.

Corregir el error de configuración del nombre en Cllame.

### v1.3.0 - 2024.9.23

####Importante nueva función

Integrating la llama.cpp, supporting la ejecución fuera de línea local de modelos grandes.

### v1.2.0 - 2024.08.20

####Nueva función

Apoyo a OpenAI Image Edit / Image Variation

Admite la API de Ollama, admite la obtención automática de la lista de modelos admitidos por Ollama.

### v1.1.0 - 2024.08.07

####Nueva característica.

Apoyo a la propuesta.

### v1.0.0 - 2024.08.05

####Nueva función.

Funcionalidad básica completa

Apoyo a OpenAI, Azure, Claude y Gemini.

Herramienta de chat con un editor integrado y funciones completas.

--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor en [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
