---
layout: post
title: Documentación de UE AIChatPlus Plugin.
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
description: Documento de instrucciones del complemento UE AIChatPlus
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documento de instrucciones del complemento UE AIChatPlus

##Repositorio público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complementos

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento de UnrealEngine que permite la comunicación con varios servicios de chat de inteligencia artificial GPT. Actualmente es compatible con OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini. En el futuro, se añadirán más proveedores de servicios. Está implementado mediante solicitudes REST asíncronas, ofreciendo un rendimiento eficiente y facilitando a los desarrolladores de UE la integración de estos servicios de chat de IA.

UE.AIChatPlus también incluye una herramienta de edición que permite utilizar los servicios de chat de IA directamente en el editor para crear texto e imágenes, analizar imágenes, entre otras funciones.

##Instrucciones de uso

###Herramienta de chat del editor

La opción Tools -> AIChatPlus -> AIChat en la barra de menú abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


La herramienta admite la generación de texto, conversaciones de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####**Función principal**

* Chat de texto: haz clic en el botón `Nueva Conversación` en la esquina inferior izquierda para crear una nueva sesión de chat de texto.

* Generación de imágenes: haz clic en el botón `New Image Chat` en la esquina inferior izquierda para iniciar una nueva sesión de generación de imágenes.

Análisis de imagen: Algunos servicios de chat de `New Chat` admiten el envío de imágenes, como Claude, Google Gemini. Simplemente haz clic en el botón 🖼️ o 🎨 sobre el cuadro de entrada para cargar la imagen que deseas enviar.

Translate these text into Spanish language:

* Soporte para Blueprints: Apoyo para la creación de solicitudes de API a través de Blueprints, lo que permite funciones como chat de texto, generación de imágenes, entre otros.

Establecer el rol de chat actual: El menú desplegable en la parte superior del cuadro de chat permite elegir el rol actual para enviar texto, lo que permite simular diferentes roles para ajustar la conversación de AI.

Borrar conversación: El icono ❌ en la parte superior de la ventana de chat puede eliminar el historial de mensajes de la conversación actual.

Translate these text into Spanish language: 

* Configuración global: Haz clic en el botón `Setting` en la esquina inferior izquierda para abrir la ventana de configuración global. Puedes establecer el chat de texto predeterminado, el servicio de API para generación de imágenes y los parámetros específicos de cada servicio de API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Configuración de la conversación: Hacer clic en el botón de ajustes en la parte superior de la ventana de chat, abrirá la ventana de configuración de la conversación actual. Permite cambiar el nombre de la conversación, modificar el servicio API utilizado en la conversación, y ajustar parámetros específicos de API para cada conversación de forma independiente. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

Modificar contenido del chat: Al situar el ratón sobre el contenido del chat, aparecerá un botón de configuración para ese contenido específico. Esto permite regenerar, modificar, copiar o eliminar el contenido, así como regenerar contenido debajo (solo para contenido creado por usuarios).

* Exploración de imágenes: Para la generación de imágenes, al hacer clic en una imagen se abrirá la ventana de visualización de imágenes (ImageViewer), que es capaz de guardar imágenes como PNG/UE Texture. Las texturas pueden visualizarse directamente en el explorador de contenidos (Content Browser), lo que facilita su uso dentro del editor. Además, también se pueden eliminar imágenes, regenerarlas, continuar generando más imágenes y otras funciones. En el editor de Windows, también es posible copiar imágenes para pegarlas directamente en el portapapeles, lo que facilita su uso. Las imágenes generadas durante la sesión se guardarán automáticamente en la carpeta de cada sesión, normalmente en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Plan:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Configuración global:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Configuración de la conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modificar el contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visor de Imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

###Introducción al código central

Actualmente, el complemento se divide en dos módulos: AIChatPlusCommon (Tiempo de ejecución) y AIChatPlusEditor (Editor).

AIChatPlusCommon se encarga de manejar el envío de solicitudes y analizar el contenido de las respuestas; AIChatPlusEditor se encarga de implementar la herramienta de chat de IA del editor.

Translate these text into Spanish language:

El UClass específico responsable de enviar la solicitud es FAIChatPlus_xxxChatRequest, cada tipo de servicio API tiene su propio UClass de solicitud independiente. Las respuestas a las solicitudes se obtienen a través de dos UClass: UAIChatPlus_ChatHandlerBase y UAIChatPlus_ImageHandlerBase, solo es necesario registrar los delegados de devolución de llamada correspondientes.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar, esto se hace utilizando FAIChatPlus_xxxChatRequestBody. La respuesta específica también se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir la devolución de llamada, se puede obtener el ResponseBody a través de una interfaz específica.

Puede encontrar más detalles del código fuente en la tienda de UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)


###Registro de actualizaciones

#### v1.2.0 - 2024.08.20

Apoyo a OpenAI Image Edit/Image Variation

Apoyo a la API de Ollama, apoyo para obtener automáticamente la lista de modelos compatibles con Ollama.

#### v1.1.0 - 2024.08.07

Apoyar el plan (Blueprint)

#### v1.0.0 - 2024.08.05

Función de base completa

Apoyo a OpenAI, Azure, Claude, Gemini

Incorporar una herramienta de chat con un editor completo como función integrada.

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
