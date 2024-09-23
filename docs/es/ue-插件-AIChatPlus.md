---
layout: post
title: Documento de instrucciones del complemento de UE AIChatPlus
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
description: Documento de instrucciones del complemento de UE AIChatPlus
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Traduce este texto al español:

Documento de instrucciones para el complemento UE AIChatPlus

##Almacén público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complementos.

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento


Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento de UnrealEngine que permite la comunicación con varios servicios de chat de inteligencia artificial GPT. Actualmente, es compatible con servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama y llama.cpp en modo offline local. En el futuro, se agregarán más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que garantiza un rendimiento eficiente y facilita la integración de estos servicios de chat de IA para los desarrolladores de Unreal Engine.

Al mismo tiempo, UE.AIChatPlus también incluye una herramienta de edición que te permite utilizar los servicios de chat de AI directamente en el editor para generar texto e imágenes, analizar imágenes, etc.

##Instrucciones de uso

###Herramienta de chat del editor

La barra de menú Herramientas -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


El sistema es compatible con la generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Funciones principales

* Modelo grande sin conexión: integración de la biblioteca llama.cpp que permite la ejecución sin conexión de modelos grandes a nivel local

* Chat de texto: haz clic en el botón `New Chat` en la esquina inferior izquierda para crear una nueva sesión de chat de texto.

* Generación de imágenes: Haz clic en el botón `New Image Chat` en la esquina inferior izquierda para crear una nueva sesión de generación de imágenes.

* Análisis de imagen: Algunos servicios de chat de `Nuevo Chat` admiten el envío de imágenes, como Claude, Google Gemini. Simplemente haz clic en el botón 🖼️ o 🎨 en la parte superior del campo de entrada para cargar la imagen que deseas enviar.

Traduce estos textos al idioma español:

* 支持蓝图 (Blueprint): Apoya la creación de API de Blueprint, completando funciones como chat de texto, generación de imágenes, etc.

Establecer el rol actual para el chat: El menú desplegable en la parte superior del cuadro de chat permite seleccionar el rol actual para enviar mensajes de texto, lo que facilita simular diferentes roles para ajustar la conversación con la inteligencia artificial.

Eliminar conversación: El botón ❌ en la parte superior de la ventana de chat te permite borrar el historial de mensajes de la conversación actual.

Traduce este texto al idioma español:

* Configuración global: Haz clic en el botón `Setting` en la esquina inferior izquierda para abrir la ventana de configuración global. Puedes establecer el chat de texto predeterminado, el servicio API para generar imágenes y configurar los parámetros específicos de cada servicio API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Configuración de la conversación: al hacer clic en el botón de configuración en la parte superior del cuadro de chat, puedes abrir la ventana de configuración de la conversación actual. Permite cambiar el nombre de la conversación, modificar el servicio API utilizado en la conversación y ajustar los parámetros específicos del API para cada conversación de forma independiente. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

Modificar contenido del chat: Al pasar el ratón sobre el contenido del chat, aparecerá un botón de ajustes para ese contenido en particular, que permitirá regenerar, modificar, copiar o eliminar el contenido, así como regenerar contenido debajo (solo para el contenido del usuario).

* Vista de imágenes: Para la generación de imágenes, al hacer clic en una imagen se abrirá la ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como PNG/UE Texture. Las Texturas se pueden ver directamente en el explorador de contenido (Content Browser), facilitando su uso en el editor. También se admiten funciones como eliminar imágenes, regenerarlas, continuar generando más imágenes, entre otras. En el editor de Windows, también se puede copiar imágenes y pegarlas en el portapapeles para un uso más sencillo. Las imágenes generadas en cada sesión se guardan automáticamente en la carpeta de cada sesión, por lo general en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

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

###Introducción al código central

En la actualidad, el complemento se divide en los siguientes módulos:

* AIChatPlusCommon: Módulo en tiempo de ejecución (Runtime), encargado de manejar las solicitudes de envío de varias API de IA y de analizar el contenido de las respuestas.

* AIChatPlusEditor: Módulo del Editor, encargado de implementar la herramienta de chat de IA en el editor.

* AIChatPlusCllama: El módulo en tiempo de ejecución (Runtime) que se encarga de encapsular las interfaces y parámetros de llama.cpp, para llevar a cabo la ejecución fuera de línea de modelos grandes.

* Thirdparty/LLAMACpp: Módulo de terceros en tiempo de ejecución (Runtime) que integra la biblioteca dinámica y los archivos de encabezado de llama.cpp.

El UClass responsable específico de enviar las peticiones es FAIChatPlus_xxxChatRequest, cada servicio API tiene su propio UClass de solicitud independiente. Las respuestas a las solicitudes se obtienen a través de dos UClases diferentes: UAIChatPlus_ChatHandlerBase y UAIChatPlus_ImageHandlerBase, solo es necesario registrar los delegados de devolución de llamada correspondientes.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar, esto se hace mediante el uso de FAIChatPlus_xxxChatRequestBody. El contenido específico de la respuesta también se analiza en FAIChatPlus_xxxChatResponseBody, el cual se puede obtener a través de una interfaz específica al recibir la llamada de respuesta.

Más detalles del código fuente están disponibles en la tienda de UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)


###Registro de actualizaciones

### v1.3.0 - 2024.9.23

Actualización importante

* Integración de llama.cpp, compatible con la ejecución offline de modelos grandes en local

#### v1.2.0 - 2024.08.20

Apoyo a OpenAI Image Edit/Image Variation

Compatible with the Ollama API, support for automatically fetching the list of models supported by Ollama.

#### v1.1.0 - 2024.08.07

Apoyar el plan.

#### v1.0.0 - 2024.08.05

* Funcionalidad básica completa

Apoyo a OpenAI, Azure, Claude, Gemini

* Herramienta de chat con editor integrado de funciones completas

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
