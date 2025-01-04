---
layout: post
title: UE 插件 AIChatPlus 说明文档
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
description: UE Plugin AIChatPlus Documentation
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documento de instrucciones para el complemento de UE AIChatPlus.

##Almacén público.

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complementos

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento.

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento para Unreal Engine que permite la comunicación con diversos servicios de chat de inteligencia artificial GPT. Actualmente, es compatible con servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, y llama.cpp para uso local sin conexión a internet. En el futuro, se agregarán más proveedores de servicios. Esta implementación se basa en solicitudes REST asíncronas, lo que garantiza un rendimiento eficiente y facilita la integración de estos servicios de chat de IA para desarrolladores de Unreal Engine.

UE.AIChatPlus también incluye una herramienta de edición que permite utilizar directamente los servicios de chatbot de inteligencia artificial en el editor para generar texto e imágenes, analizar imágenes, entre otras funciones.

##Instrucciones de uso

###Herramienta de chat del editor.

La barra de menú Herramientas -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


El software admite la generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Función principal

Modelo grande sin conexión: Integración de la biblioteca llama.cpp para admitir la ejecución sin conexión de modelos grandes a nivel local.

Iniciar un chat de texto: Haz clic en el botón `Nuevo Chat` en la esquina inferior izquierda para crear una nueva conversación de chat de texto.

Generación de imagen: Haz clic en el botón `New Image Chat` en la esquina inferior izquierda para iniciar una nueva sesión de generación de imagen.

Análisis de imágenes: Algunos servicios de chat de "New Chat" admiten el envío de imágenes, como Claude, Google Gemini. Solo tienes que hacer clic en los botones 🖼️ o 🎨 encima del cuadro de texto para cargar la imagen que deseas enviar.

Apoyo a Blueprint: permite crear peticiones de API a través de Blueprint para realizar funciones como chat de texto, generación de imágenes, entre otras.

Establecer el personaje de chat actual: El menú desplegable en la parte superior del cuadro de chat permite seleccionar el personaje actual para enviar texto, lo que permite simular diferentes personajes para ajustar la conversación de IA.

Vaciar conversación: El icono ❌ en la parte superior de la ventana de chat te permite borrar el historial de mensajes de la conversación actual.

Plantilla de conversación: Incorpora cientos de modelos de configuración de diálogos para facilitar el manejo de problemas comunes.

Configuración global: Al hacer clic en el botón `Setting` en la esquina inferior izquierda, se abrirá la ventana de configuración global. Aquí puedes establecer el chat de texto predeterminado, el servicio de API para generar imágenes y ajustar parámetros específicos para cada servicio de API. Las configuraciones se guardarán automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Configuración de la conversación: Haga clic en el botón de configuración en la parte superior del cuadro de chat para abrir la ventana de configuración de la conversación actual. Permite modificar el nombre de la conversación, el servicio API utilizado en la conversación y configurar de forma independiente los parámetros específicos de API para cada conversación. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Modificar contenido del chat: Al posicionar el cursor sobre el contenido del chat, aparecerá un botón de configuración para ese contenido individual, permitiendo regenerar, modificar, copiar o eliminar el contenido, así como regenerar contenido debajo (para contenido generado por usuarios).

- Exploración de imágenes: Cuando se genera una imagen, al hacer clic en la imagen se abrirá la ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como archivo PNG o Textura UE. Las Texturas se pueden ver directamente en el Explorador de Contenidos (Content Browser), facilitando su uso dentro del editor. Además, se admiten funciones como eliminar imágenes, regenerarlas, generar más imágenes, entre otras. En el editor de Windows, también se puede copiar imágenes, lo que permite copiarlas directamente al portapapeles para facilitar su uso. Las imágenes generadas durante la sesión también se guardarán automáticamente en la carpeta de cada sesión, generalmente en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Plan:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Configuración global:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Configuración de conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modificar el contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visor de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Utilizar modelos grandes sin conexión.

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Plantilla de diálogo

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introducción al código principal

Actualmente, el complemento se divide en los siguientes módulos:

AIChatPlusCommon: El módulo de tiempo de ejecución, responsable de manejar diversas solicitudes de API de IA y analizar el contenido de las respuestas.

AIChatPlusEditor: Módulo del editor encargado de implementar la herramienta de chat AI del editor.

AIChatPlusCllama: Módulo de tiempo de ejecución (Runtime), encargado de encapsular la interfaz y parámetros de llama.cpp, para llevar a cabo la ejecución sin conexión de modelos grandes.

Thirdparty/LLAMACpp: Un módulo de tercero en tiempo de ejecución (Runtime), que integra la biblioteca dinámica y archivos de cabecera de llama.cpp.

El UClass responsable específico de enviar la solicitud es FAIChatPlus_xxxChatRequest. Cada servicio de API tiene su propio UClass de solicitud independiente. Las respuestas de la solicitud se obtienen a través de dos UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase. Solo hay que registrar el delegado de devolución de llamada correspondiente.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar, esto se hace a través de FAIChatPlus_xxxChatRequestBody. El contenido específico de la respuesta también se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir la devolución, se puede obtener el ResponseBody a través de una interfaz específica.

Puede encontrar más detalles del código fuente en la tienda de UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Utilizar la herramienta del editor con el modelo fuera de línea Cllama(llama.cpp)

A continuación se explica cómo utilizar el modelo sin conexión llama.cpp en la herramienta de edición AIChatPlus.

(https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloque el modelo en una carpeta específica, por ejemplo en el directorio Content/LLAMA del proyecto de juego.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Abre la herramienta de edición AIChatPlus: Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat y accede a la página de configuración de la sesión.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Establezca la API en Cllama, active la Configuración de API Personalizada, y añada la ruta de búsqueda del modelo y seleccione el modelo.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Comienza la conversación!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Utiliza la herramienta del editor con el modelo sin conexión Cllama (llama.cpp) para procesar imágenes.

Descarga el modelo offline MobileVLM_V2-1.7B-GGUF desde el sitio web de HuggingFace y colócalo en el directorio Content/LLAMA: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf] se traduce como "和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)Lo siento, no puedo realizar la traducción ya que el texto que proporcionaste está en blanco. ¿Puedes enviarme un nuevo texto para traducir?

Establecer el modelo de la sesión:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Enviar imagen para comenzar la conversación.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###El código utiliza el modelo fuera de línea Cllama(llama.cpp)

Las siguientes indicaciones detallan cómo utilizar el modelo sin conexión llama.cpp en el código.

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

Una vez recompilado, puedes utilizar el comando en la consola del editor Cmd para visualizar los resultados de la salida del modelo en el registro OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Utilice el modelo fuera de línea llama.cpp en el plan.

Se describe cómo utilizar el modelo offline llama.cpp en un blueprint.

En el blueprint, haz clic derecho para crear un nodo llamado `Enviar solicitud de chat de Cllama`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

*Crear un nodo Options y establecer `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.*

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Crear Mensajes, agregar un Mensaje del Sistema y un Mensaje de Usuario.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Crea un Delegado que reciba la información de salida del modelo y la imprima en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

El aspecto de un diagrama completo es este, al ejecutarlo, verás en la pantalla del juego el mensaje devuelto al imprimir el gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###El editor utiliza OpenAI para chatear.

Abre la herramienta de chat Tools -> AIChatPlus -> AIChat, crea una nueva sesión de chat New Chat, y configura la sesión ChatApi en OpenAI, ajustando los parámetros de la interfaz.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Comience a chatear:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Cambiar el modelo a gpt-4o / gpt-4o-mini te permitirá utilizar la funcionalidad de análisis visual de imágenes de OpenAI.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###El editor utiliza OpenAI para procesar imágenes (crear/modificar/variar)

Crear una nueva conversación de imagen en la herramienta de chat, modificar la configuración de la conversación a OpenAI y ajustar los parámetros.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Crear imagen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Modificar la imagen cambiando el tipo de chat de imagen a "Editar", y subir dos imágenes: una imagen original y otra donde la máscara muestra las áreas a modificar con transparencia (canal alfa a 0).

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Modificar la variante de la imagen cambiando el tipo de chat de imagen a "Variación" y subir una imagen. OpenAI generará una variante de la imagen original.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Utilizando el modelo de chat de OpenAI para la conversación del proyecto.

En el plano, haz clic derecho para crear un nodo "Send OpenAI Chat Request In World".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Crear un nodo de Opciones y establecer `Stream=true, Api Key="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Crear Messages, añadir un mensaje de Sistema y un mensaje de Usuario.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Crear un Delegate que reciba la información de salida del modelo y la imprima en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

La descripción completa del blueprint es la siguiente; al ejecutar el blueprint, podrás ver el mensaje devuelto en la pantalla del juego.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Usa OpenAI para crear imágenes de planos.

En la interfaz azul, haz clic derecho para crear un nodo llamado `Enviar solicitud de imagen a OpenAI`, y establece `En Propmt="una hermosa mariposa"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Crear un nodo de opciones y establecer `Api Key="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Asociar el evento de imágenes y guardar las imágenes en el disco duro local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

La interpretación completa del diseño se ve así, ejecuta el diseño y verás la imagen guardada en la ubicación específica.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###El editor utiliza Azure.

Crear nueva conversación (New Chat), cambiar ChatApi a Azure y configurar los parámetros de la API de Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Comenzar la conversación.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###Utilizar Azure para crear imágenes en el editor.

Crear una nueva sesión de chat de imágenes (New Image Chat), cambiar ChatApi a Azure y configurar los parámetros de la API de Azure. Tenga en cuenta que, si se trata del modelo dall-e-2, es necesario configurar los parámetros Quality y Stype en not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Iniciar conversación para que Azure cree una imagen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Utilizar Azure Chat en Blueprint

Cree el siguiente plan, configure las opciones de Azure, haga clic en ejecutar y verá en pantalla la información de chat devuelta por Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Utilizando Azure para crear imágenes según el plano.

Cree el plan siguiendo estas indicaciones, configure las opciones de Azure, haga clic en ejecutar. Si la creación de la imagen tiene éxito, verá el mensaje "Create Image Done" en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

De acuerdo con la configuración del diagrama anterior, la imagen se guardará en la ruta D:\Descargas\mariposa.png.

## Claude

###El editor utiliza Claude para conversar y analizar imágenes.

Crear nuevo chat, cambiar ChatApi a Claude y configurar los parámetros de Api de Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Comenzar la conversación

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Utilizando Blueprint para chatear y analizar imágenes con Claude.

En el plano, haz clic derecho para crear un nodo `Enviar solicitud de chat a Claude`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Crear un nodo de opciones y establecer `Stream=true, Api Key="tu clave de API de Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Crear Messages, crear Texture2D desde el archivo y luego crear AIChatPlusTexture desde el Texture2D. Después, añadir AIChatPlusTexture al Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Crear un evento como se describe en el tutorial anterior y luego imprimir la información en la pantalla del juego.

La traducción al español es la siguiente:

* El aspecto de un blueprint completo es este, ejecutando el blueprint, se puede ver el mensaje que devuelve en la pantalla del juego al imprimir el gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Obtener Ollama

Puedes obtener el paquete de instalación para instalar localmente a través de la página web oficial de Ollama: [ollama.com](https://ollama.com/)

Puedes utilizar Ollama a través de la interfaz Ollama proporcionada por otra persona.

###El editor utiliza Ollama para chatear y analizar imágenes.

Crear un nuevo chat, cambiar ChatApi a Ollama y configurar los parámetros de la API de Ollama. Si es un chat de texto, establecer el modelo como modelo de texto, como llama3.1; si se necesita procesar imágenes, establecer el modelo como un modelo compatible con visión, como moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Iniciar chat

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Utiliza Ollama para chatear y analizar imágenes.

Por favor, crea el siguiente esquema, configura las opciones de Ollama, haz clic en ejecutar y podrás ver en la pantalla la información de chat que devuelve Ollama.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###Utiliza Gemini en el editor.

Crear una nueva conversación (Nuevo Chat), cambiar ChatApi a Gemini y configurar los parámetros de la API de Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Iniciar chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###Utiliza el chat de Gemini en Blueprint.

Cree el siguiente plan, configure las Opciones de Gemini, haga clic en Ejecutar y verá en la pantalla la información del chat que devuelva Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

## Deepseek

###El editor utiliza Deepseek.

Crear un nuevo chat, cambiar ChatApi a OpenAi, y configurar los parámetros de la API de Deepseek. Añadir un nuevo modelo de candidato llamado deepseek-chat, y establecer el modelo como deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Comenzar la conversación

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Utilizar Deepseek para chatear en Blueprint.

Por favor, configura el plan detallado como se muestra a continuación, establece las opciones de solicitud relacionadas con Deepseek, incluyendo el Modelo, URL Base, URL de Punto Final, Clave API, y otros parámetros. Haz clic en ejecutar para visualizar en pantalla la información de chat que regresa Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##Registro de actualizaciones

### v1.4.1 - 2025.01.04

####Reparación de problemas.

La herramienta de chat permite enviar solo imágenes sin mensajes.

Reparar el problema de fallo al enviar imágenes a través de la API de OpenAI.

Corrige el problema de configuración de las herramientas de chat OpanAI y Azure que omitió los parámetros Quality, Style y ApiVersion.

### v1.4.0 - 2024.12.30

####Nueva característica.

* (功能处于实验阶段) Cllama (llama.cpp) admite modelos multimodales y puede procesar imágenes.

Todos los parámetros de tipo blueprint ahora incluyen instrucciones detalladas.

### v1.3.4 - 2024.12.05

####Nueva función

OpenAI supports la API de visión.

####Reparación de problemas

Corregir el error al establecer OpenAI stream=false.

### v1.3.3 - 2024.11.25

####Nueva función

Compatible con UE-5.5.

####Reparación de problemas.

Reparar problema de algunas plantillas que no funcionan correctamente.

### v1.3.2 - 2024.10.10

####Reparación de problemas

Reparar el fallo de cllama al detener manualmente la solicitud

Corregir el problema en la versión de descarga de la tienda win donde no se puede encontrar el archivo ggml.dll o llama.dll.

Comprobar si se está en el hilo del juego al crear la solicitud.

### v1.3.1 - 2024.9.30

####Nueva función

Agregar un SystemTemplateViewer que permita visualizar y utilizar cientos de plantillas de configuración del sistema.

####Reparación de problemas

Reparar el plugin descargado desde la tienda, llama.cpp no puede encontrar la biblioteca de enlace.

Corregir el problema de la ruta demasiado larga en LLAMACpp

Reparar el error llama.dll después de empaquetar en Windows.

Corregir problema de lectura de ruta de archivo en iOS/Android.

Corregir el error en la configuración de Cllame para establecer el nombre correctamente.

### v1.3.0 - 2024.9.23

####Nueva característica importante.

Se ha integrado llama.cpp para admitir la ejecución offline de modelos grandes en local.

### v1.2.0 - 2024.08.20

####Nueva funcionalidad.

Apoyo a OpenAI Image Edit/Image Variation.

* Admite la API de Ollama, admite la obtención automática de la lista de modelos admitidos por Ollama. 

### v1.1.0 - 2024.08.07

####Nueva funcionalidad

Apoyo al plan/ Apoyar el plan.

### v1.0.0 - 2024.08.05

####Nueva función.

Funcionalidad básica completa.

Apoyo a OpenAI, Azure, Claude y Gemini.

* Herramienta de chat con editor incorporado y funciones completas.

--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT. Por favor, [**反馈**](https://github.com/disenone/wiki_blog/issues/new)Señala cualquier omisión. 
