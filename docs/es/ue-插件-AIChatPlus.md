---
layout: post
title: Manual de instrucciones del complemento de UE AIChatPlus.
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
description: Documento de instrucciones para el complemento UE AIChatPlus.
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documento de instrucciones del complemento de UE AIChatPlus

##Depósito público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complemento

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento de UnrealEngine que implementa la comunicación con varios servicios de chat de IA GPT. Actualmente, admite servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, y llama.cpp offline local. En el futuro, seguirá agregando soporte para más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que garantiza un rendimiento eficiente y facilita a los desarrolladores de UE integrar estos servicios de chat de IA.

UE.AIChatPlus también incluye una herramienta de edición que permite utilizar los servicios de chat de IA directamente en el editor para generar texto e imágenes, analizar imágenes, entre otras funciones.

##Instrucciones de uso

###Herramienta de chat del editor

La barra de menús Tools -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


El software es compatible con la generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Función principal

* Modelo grande sin conexión: Integrado con la librería llama.cpp, compatible con la ejecución sin conexión de modelos grandes a nivel local.

* Chat de texto: haz clic en el botón `Nuevo Chat` en la esquina inferior izquierda para crear una nueva sesión de chat de texto.

- **Generación de imágenes:** Haz clic en el botón `Nueva Conversación de Imagen` en la esquina inferior izquierda para crear una nueva sesión de generación de imágenes.

Análisis de imagen: Algunos servicios de chat de "New Chat" admiten el envío de imágenes, como Claude y Google Gemini. Simplemente haz clic en el botón 🖼️ o 🎨 encima del cuadro de texto para cargar la imagen que deseas enviar.

* Soporte de Blueprint: admite la creación de solicitudes de API con Blueprint, lo que permite realizar funciones como chats de texto, generación de imágenes, entre otros.

Establecer el rol de chat actual: El menú desplegable en la parte superior del cuadro de chat puede configurar el rol actual para enviar texto, lo que permite simular diferentes roles para ajustar la conversación de la IA.

Eliminar chat: pulsando en la ❌ en la parte superior de la ventana de chat, se puede borrar el historial de mensajes de la conversación actual.

* Plantilla de diálogo: incorpora cientos de plantillas de configuración de diálogo para facilitar el manejo de problemas comunes.

* Configuración global: Al hacer clic en el botón `Setting` en la esquina inferior izquierda, puede abrir la ventana de configuración global. Puede configurar el chat de texto predeterminado, el servicio de API de generación de imágenes y establecer los parámetros específicos de cada servicio de API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Translate these text into Spanish language:

* Sesión de configuración: Al hacer clic en el botón de configuración en la parte superior de la ventana de chat, se puede abrir la ventana de configuración de la sesión actual. Permite modificar el nombre de la sesión, cambiar el servicio API utilizado en la sesión, y ajustar los parámetros específicos de API para cada sesión individualmente. La configuración de la sesión se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

* Edición de contenido de chat: Cuando se coloca el ratón sobre el contenido del chat, aparecerá un botón de configuración para ese contenido en particular, que permite regenerar, modificar, copiar o borrar el contenido, así como regenerar el contenido debajo (para contenido generado por el usuario).

* Exploración de imágenes: Para la generación de imágenes, al hacer clic en una imagen se abrirá la ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como PNG/UE Texture. Las Textures se pueden visualizar directamente en el explorador de contenido (Content Browser), facilitando su uso dentro del editor. También se pueden eliminar imágenes, regenerarlas, continuar generando más imágenes, entre otras funciones. En el editor de Windows, además, se puede copiar imágenes para pegarlas directamente en el portapapeles, lo que facilita su uso. Las imágenes generadas durante una sesión se guardarán automáticamente en la carpeta de cada sesión, generalmente en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

**Traduce este texto al español:**

**Blueprint:**

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

En la actualidad, el complemento se divide en los siguientes módulos:

* AIChatPlusCommon: Módulo de tiempo de ejecución (Runtime), responsable de manejar solicitudes de envío de API de inteligencia artificial y analizar el contenido de las respuestas.

* AIChatPlusEditor: Módulo de editor, responsable de implementar la herramienta de chat de inteligencia artificial en el editor.

* AIChatPlusCllama: El módulo de tiempo de ejecución (Runtime) es responsable de encapsular las interfaces y parámetros de llama.cpp, permitiendo la ejecución sin conexión de grandes modelos.

* Thirdparty/LLAMACpp: Módulo de tercero (Runtime) que integra la biblioteca dinámica y archivos de cabecera de llama.cpp.

El UClass responsable de enviar las solicitudes es FAIChatPlus_xxxChatRequest, cada servicio de API tiene su propio UClass de solicitud independiente. Las respuestas a las solicitudes se obtienen a través de UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase, solo es necesario registrar el delegado de devolución de llamada correspondiente.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar, esto se hace a través de FAIChatPlus_xxxChatRequestBody. El contenido específico de la respuesta también se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir la llamada de vuelta se puede obtener el ResponseBody a través de una interfaz específica.

Más detalles del código fuente disponibles en la tienda de UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)


###Registro de actualizaciones

#### v1.3.1 - 2024.9.30

Agregue un SystemTemplateViewer, que le permita ver y utilizar cientos de plantillas de configuración del sistema.

##### Bugfix

* Reparar el complemento descargado desde la tienda, llama.cpp no puede encontrar la biblioteca de vínculos
* Corregir problema de longitud de ruta en LLAMACpp
Reparar el error llama.dll después de empaquetar en Windows.
Corregir problema de lectura de rutas de archivos en iOS/Android.
Corregir el error de configuración del nombre de Cllame

#### v1.3.0 - 2024.9.23

Actualización importante

* Integración de llama.cpp para admitir la ejecución sin conexión local de modelos grandes

#### v1.2.0 - 2024.08.20

Apoyo a OpenAI Image Edit/Image Variation

Apoyo a la API de Ollama, soporte para obtener automáticamente la lista de modelos admitidos por Ollama.

#### v1.1.0 - 2024.08.07

Apoyo al plan.

#### v1.0.0 - 2024.08.05

Función completa básica

Apoyo a OpenAI, Azure, Claude, Gemini.

* Herramienta de chat con editor integrado de funciones completas.

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
