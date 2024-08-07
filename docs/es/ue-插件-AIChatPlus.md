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
description: Por favor traduzca el texto completo para poder brindarle la traducción
  requerida.
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documentación de UE Plugin AIChatPlus

##Repositorio público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complemento

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento para UnrealEngine que permite la comunicación con diversos servicios de chat de inteligencia artificial GPT. Actualmente admite servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude y Google Gemini. En el futuro se agregarán más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que garantiza un rendimiento eficiente y facilita la integración de estos servicios de chat de IA para desarrolladores de UE.

Al mismo tiempo, UE.AIChatPlus también incluye una herramienta de edición que te permite utilizar directamente estos servicios de chat de inteligencia artificial en el editor para generar texto e imágenes, y analizar imágenes, entre otras funciones.

##Instrucciones de uso

###Herramienta de chat del editor

La barra de menú Herramientas -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


El software permite generar texto, chatear por texto, generar imágenes y analizar imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Función principal

Traducción al español:

* Chat de texto: haz clic en el botón `Nuevo Chat` en la esquina inferior izquierda para crear una nueva conversación de chat de texto.

* Generación de imágenes: haz clic en el botón `Nueva imagen de chat` en la esquina inferior izquierda para crear una nueva sesión de generación de imágenes.

Análisis de imágenes: Algunos servicios de chat en la función "New Chat" admiten el envío de imágenes, como Claude, Google Gemini. Haz clic en los botones 🖼️ o 🎨 ubicados encima del cuadro de texto para cargar la imagen que deseas enviar.

* Soporte para Blueprint: Soporte para la creación de peticiones de API de Blueprint, completando funciones como chat de texto, generación de imágenes, entre otros.

Establecer el rol actual de la conversación: el menú desplegable en la parte superior del cuadro de chat puede definir el personaje actual que envía el texto, permitiendo simular diferentes roles para ajustar el chat de IA.

Borrar conversación: El botón ❌ en la parte superior de la ventana de chat permite borrar el historial de mensajes de la conversación actual.

Translate these text into Spanish language:

* Global settings: Click on the `Setting` button in the bottom left corner to open the global settings window. Here you can set default text chat, API services for image generation, and specify parameters for each type of API service. The settings will be automatically saved in the project's path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Configuración de la conversación: Haz clic en el botón de configuración en la parte superior de la ventana de chat para abrir la ventana de configuración de la conversación actual. Permite cambiar el nombre de la conversación, modificar los servicios de API utilizados en la conversación, y configurar parámetros específicos de API para cada conversación de forma independiente. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

Modificar contenido de chat: Al pasar el ratón sobre el contenido del chat, aparecerá un botón de configuración para ese contenido de chat en particular, que permitirá regenerar, modificar, copiar o eliminar el contenido, así como regenerar contenido debajo (para los mensajes de los usuarios).

* Visualización de imágenes: Para la generación de imágenes, al hacer clic en una imagen se abrirá la ventana de visualización de imágenes (ImageViewer), con soporte para guardar la imagen como PNG/Textura UE, las texturas se pueden ver directamente en el Explorador de contenido (Content Browser), facilitando así su uso dentro del editor. Además, se permite eliminar imágenes, regenerarlas, continuar generando más imágenes, entre otras funciones. Para el editor en Windows, también se admite copiar imágenes, pudiendo pegarlas directamente en el portapapeles para un uso más conveniente. Las imágenes generadas en la sesión se guardarán automáticamente en la carpeta de cada sesión, generalmente en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Plan:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Configuración global:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Configuración de la conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modifica el contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visor de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

###Presentación del código central

En la actualidad, el complemento se divide en dos módulos: AIChatPlusCommon (Tiempo de ejecución) y AIChatPlusEditor (Editor).

AIChatPlusCommon se encarga de manejar el envío de solicitudes y analizar el contenido de las respuestas; AIChatPlusEditor es responsable de implementar el editor de la herramienta de chat de IA.

Traduce el siguiente texto al idioma Español:

El UClass responsable específico de enviar las solicitudes es FAIChatPlus_xxxChatRequest, cada servicio API tiene su propio UClass de solicitud independiente. Las respuestas a las solicitudes se obtienen a través de dos tipos de UClass: UAIChatPlus_ChatHandlerBase y UAIChatPlus_ImageHandlerBase, solo es necesario registrar los delegados de devolución de llamada correspondientes.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar. Esto se hace a través de FAIChatPlus_xxxChatRequestBody. El contenido específico de la respuesta también se analiza en FAIChatPlus_xxxChatResponseBody, que se puede obtener a través de una interfaz específica al recibir una devolución de llamada.

Puedes encontrar más detalles del código fuente en la tienda UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)


###Registro de actualizaciones

#### v1.0.0 - 2024.08.07

Funcionalidad básica completa
Apoyo a OpenAI, Azure, Claude, Gemini
Favor de apoyar el plan.
* Herramienta de chat con editor integrado y funciones completas.

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
