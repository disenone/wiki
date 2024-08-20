---
layout: post
title: Documento de instrucciones del complemento AIChatPlus de UE.
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
description: 'Por favor traduce este texto al idioma español:


  Documentación de UE Plug-in AIChatPlus'
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documento de instrucciones del complemento UE AIChatPlus

##Repositorio público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complemento

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento


This plugin supports UE5.2+.

UE.AIChatPlus es un complemento de UnrealEngine que permite la comunicación con varios servicios de chat de inteligencia artificial GPT. Actualmente soporta servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude y Google Gemini. En el futuro, se añadirán más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que garantiza un rendimiento eficiente y facilita la integración de estos servicios de chat de IA para desarrolladores de Unreal Engine.

UE.AIChatPlus también incluye una herramienta de edición que te permite utilizar directamente los servicios de chat AI en el editor para crear texto e imágenes, analizar imágenes, y más.

##Instrucciones de uso

###Herramienta de chat del editor

La opción Tools -> AIChatPlus -> AIChat en la barra de menú abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


La herramienta ofrece soporte para la generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Función principal

* Chat de texto: Haz clic en el botón `Nuevo Chat` en la esquina inferior izquierda para crear una nueva conversación de chat de texto.

* Generación de imagen: haz clic en el botón `Nueva imagen Chat` en la esquina inferior izquierda para iniciar una nueva sesión de generación de imagen.

Análisis de imágenes: Algunos servicios de chat de `New Chat` admiten el envío de imágenes, como Claude, Google Gemini. Simplemente haz clic en el botón 🖼️ o 🎨 encima del cuadro de texto para cargar la imagen que deseas enviar.

* Apoyo a Blueprint: Apoyo para la creación de solicitudes de API de Blueprint, completando funciones como chat de texto, generación de imágenes, entre otras.

Establecer el rol actual en la conversación: El menú desplegable en la parte superior del cuadro de chat puede definir el rol actual para enviar texto, permitiendo simular diferentes roles para ajustar la conversación con la IA.

Vaciar chat: Puedes borrar el historial de mensajes de la conversación actual con el botón ❌ en la parte superior del cuadro de chat.

* Configuración global: al hacer clic en el botón `Setting` en la esquina inferior izquierda, se abrirá la ventana de configuración global. Puede establecer el chat de texto predeterminado, el servicio de API para la generación de imágenes y configurar parámetros específicos para cada tipo de servicio de API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Configuración de la conversación: Al hacer clic en el botón de configuración en la parte superior de la ventana de chat, puedes abrir la ventana de configuración de la conversación actual. Permite modificar el nombre de la conversación, cambiar el servicio API utilizado en la conversación, y ajustar parámetros específicos del API para cada conversación de forma independiente. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Modificar contenido de chat: Al colocar el ratón sobre el contenido del chat, aparecerá un botón de configuración para ese contenido específico, que permitirá regenerar, modificar, copiar o eliminar el contenido, y regenerar contenido debajo (para contenido creado por usuarios).

* Visualización de imágenes: Para la generación de imágenes, al hacer clic en una imagen se abrirá una ventana de visualización de imágenes (ImageViewer), que admite guardar la imagen como PNG/Textura UE, las texturas se pueden ver directamente en el explorador de contenido (Content Browser), facilitando su uso dentro del editor. También se pueden eliminar imágenes, volver a generar imágenes, continuar generando más imágenes, entre otras funciones. Para los editores en Windows, también se puede copiar imágenes y pegarlas directamente en el portapapeles para facilitar su uso. Las imágenes generadas en la sesión se guardarán automáticamente en la carpeta de cada sesión, generalmente en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Planificación:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Configuración global:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Configuración de la conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modificar el contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visor de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

###Presentación del código central

En la actualidad, el complemento se divide en dos módulos: AIChatPlusCommon (Tiempo de ejecución) y AIChatPlusEditor (Editor).

AIChatPlusCommon se encarga de manejar el envío de solicitudes y analizar el contenido de las respuestas; AIChatPlusEditor se encarga de implementar el editor de la herramienta de chat de inteligencia artificial.

El UClass responsable de enviar las solicitudes es FAIChatPlus_xxxChatRequest, cada servicio de API tiene su propio UClass de solicitud independiente. Las respuestas a las solicitudes se obtienen a través de dos tipos de UClass: UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase; solo es necesario registrar los delegados de devolución de llamada correspondientes.

Antes de enviar la solicitud, es necesario configurar los parámetros del API y el mensaje a enviar, esto se hace mediante FAIChatPlus_xxxChatRequestBody. El contenido específico de la respuesta también se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir el callback se puede obtener el ResponseBody a través de una interfaz específica.

Se pueden obtener más detalles del código fuente en la tienda de Epic Games: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)


###**Registro de actualizaciones**

#### v1.2.0 - 2024.08.20

Apoyo a OpenAI Image Edit/Image Variation.
Apoyo a la API de Ollama, apoyo para obtener automáticamente la lista de modelos admitidos por Ollama.

#### v1.1.0 - 2024.08.07

Apoyo al plan.

#### v1.0.0 - 2024.08.05

Funcionalidad básica completa
Apoyo a OpenAI, Azure, Claude, Gemini.
* Herramienta de chat con editor incorporado y funcionalidades completas

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
