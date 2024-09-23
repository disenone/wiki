---
layout: post
title: Documento de instrucciones del complemento AIChatPlus de la UE.
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
description: Documento de instrucciones del complemento UE AIChatPlus.
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documento de instrucciones del complemento UE AIChatPlus

##Repositorio público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complemento.

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento de UnrealEngine que implementa la comunicación con varios servicios de chat de inteligencia artificial GPT. Actualmente, admite servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama y llama.cpp en modo offline. En el futuro se agregarán más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que proporciona un rendimiento eficiente y facilita la integración de estos servicios de chat de IA para desarrolladores de Unreal Engine.

UE.AIChatPlus también incluye una herramienta de edición que te permite utilizar directamente los servicios de chat de IA en el editor para crear texto e imágenes, analizar imágenes, entre otras funciones.

##Instrucciones de uso

###Herramienta de chat del editor

El menú Tools -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


El soporte de herramientas incluye generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Funciones principales

* Modelo grande sin conexión: Integración de la librería llama.cpp que permite ejecutar modelos grandes sin conexión localmente

* Chat de texto: haz clic en el botón `New Chat` en la esquina inferior izquierda para crear una nueva sesión de chat de texto.

* Generación de imagen: haga clic en el botón `New Image Chat` en la esquina inferior izquierda para iniciar una nueva sesión de generación de imagen.

Análisis de imagen: parte de los servicios de chat en `New Chat` admiten el envío de imágenes, como Claude, Google Gemini. Simplemente haz clic en el botón 🖼️ o 🎨 encima del cuadro de texto para cargar la imagen que desees enviar.

* Soporte de Blueprint: admite la creación de solicitudes de API de Blueprint, completando funciones como chat de texto, generación de imágenes, entre otros.

Establecer el rol actual del chat: El menú desplegable en la parte superior del cuadro de chat puede configurar el rol actual para enviar texto, lo que permite simular diferentes roles para ajustar la conversación de IA.

Limpiar chat: La opción de la ✖ en la parte superior de la ventana de chat permite borrar el historial de mensajes de la conversación actual.

**Configuración global:** Al hacer clic en el botón `Configuración` en la esquina inferior izquierda, se abrirá la ventana de configuración global. Puede establecer el chat de texto predeterminado, los servicios de generación de imágenes API y configurar los parámetros específicos de cada servicio API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Configuración de la conversación: al hacer clic en el botón de configuración en la parte superior del cuadro de chat, puedes abrir la ventana de configuración de la conversación actual. Permite modificar el nombre de la conversación, el servicio API utilizado en la conversación, y establecer parámetros específicos de API para cada sesión de forma independiente. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

Editar contenido del chat: Al pasar el ratón por encima del contenido del chat, aparecerá un botón de configuración para ese contenido en particular, que permite regenerar, modificar, copiar o borrar el contenido, además de regenerar contenido debajo (para el contenido creado por un usuario).

* Visualización de imágenes: Para la generación de imágenes, al hacer clic en una imagen se abrirá la ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como PNG/Textura UE, las cuales se pueden ver directamente en el explorador de contenido (Content Browser), facilitando su uso dentro del editor. También se cuenta con funciones para eliminar imágenes, regenerarlas, seguir generando más imágenes, entre otras. En el editor de Windows, también se puede copiar imágenes, lo que permite copiarlas directamente al portapapeles para un uso más sencillo. Las imágenes generadas durante la sesión se guardarán automáticamente en la carpeta de cada sesión, con la ruta generalmente siendo `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Plan:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Configuración general:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Configuración de la conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modifica el contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visor de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

###Presentación del código central

En la actualidad, el complemento se divide en los siguientes módulos:

* AIChatPlusCommon: Módulo en tiempo de ejecución (Runtime), encargado de manejar las solicitudes de envío de diversas interfaces API de IA y analizar el contenido de las respuestas.

* AIChatPlusEditor: Módulo del editor, encargado de implementar la herramienta de chat AI del editor.

* AIChatPlusCllama: Módulo de tiempo de ejecución (Runtime), responsable de encapsular la interfaz y los parámetros de llama.cpp, para lograr la ejecución fuera de línea de modelos grandes.

* Thirdparty/LLAMACpp: Módulo de tercero en tiempo de ejecución (Runtime), que integra la biblioteca dinámica y los archivos de cabecera de llama.cpp.

Translate these text into Spanish language:

El UClass específico responsable de enviar la solicitud es FAIChatPlus_xxxChatRequest, cada tipo de servicio de API tiene su UClass de solicitud independiente. Las respuestas a las solicitudes se obtienen a través de dos UClass distintos: UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase, solo es necesario registrar los delegados de devolución de llamada correspondientes.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar, esto se hace a través de FAIChatPlus_xxxChatRequestBody. El contenido específico de las respuestas también se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir la devolución de llamada, se puede obtener el ResponseBody a través de una interfaz específica.

Puede encontrar más detalles del código fuente en la tienda de UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)


###Registro de actualizaciones

#### v1.3.0 - 2024.9.23

Actualización importante

Se ha integrado llama.cpp para admitir la ejecución fuera de línea de modelos grandes de forma local.

#### v1.2.0 - 2024.08.20

Apoyo a OpenAI Image Edit/Image Variation.

Apoyo a la API de Ollama, apoyo para obtener automáticamente la lista de modelos admitidos por Ollama.

#### v1.1.0 - 2024.08.07

Apoyar el plan en inglés.

#### v1.0.0 - 2024.08.05

Función básica completa

Apoyo a OpenAI, Azure, Claude, Gemini.

* Herramienta de chat con editor integrado bien equipado

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
