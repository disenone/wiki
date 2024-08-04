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
description: Documento de instrucciones del complemento AIChatPlus de la UE.
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documento de instrucciones del complemento de UE AIChatPlus

##Repositorio público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complementos

[AIChatPlus]()

##Introducción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento para UnrealEngine que permite la comunicación con varios servicios de chat de inteligencia artificial GPT. Actualmente, es compatible con servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude y Google Gemini. En el futuro, se agregarán más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que garantiza un alto rendimiento y facilita a los desarrolladores de UnrealEngine integrar estos servicios de chat de inteligencia artificial.

Al mismo tiempo, UE.AIChatPlus también incluye una herramienta de edición que permite utilizar directamente estos servicios de chat de inteligencia artificial en el editor para generar texto e imágenes, analizar imágenes, entre otras funciones.

##Instrucciones de uso

###Herramienta de chat del editor

La barra de menú Herramientas -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


El soporte de la herramienta incluye la generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Función principal

* Text Chat: Haz clic en el botón `Nuevo Chat` en la esquina inferior izquierda para crear una nueva sesión de chat de texto.

* Generación de imágenes: Haz clic en el botón `New Image Chat` en la esquina inferior izquierda para crear una nueva sesión de generación de imágenes.

* Análisis de imágenes: algunos servicios de chat en la función `New Chat` admiten el envío de imágenes, como Claude, Google Gemini. Simplemente haz clic en el botón 🖼️ o 🎨 sobre el cuadro de entrada para cargar la imagen que deseas enviar.

* Establecer el rol de chat actual: el menú desplegable en la parte superior del cuadro de chat puede configurar el rol actual para enviar texto, permitiendo simular diferentes roles para ajustar la conversación de IA.

Limpiar chat: al pulsar la "❌" en la parte superior del cuadro de chat se pueden borrar los mensajes de historial de la conversación actual.

Translate these text into Spanish language:

* Configuración general: Al hacer clic en el botón `Setting` en la esquina inferior izquierda, se abrirá la ventana de configuración general. Puede configurar el chat de texto predeterminado, el servicio de API para la generación de imágenes y ajustar los parámetros específicos de cada servicio de API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

**Configuración de la conversación:** Al hacer clic en el botón de configuración en la parte superior del cuadro de chat, puedes abrir la ventana de configuración de la conversación actual. Permite modificar el nombre de la conversación, el servicio de API utilizado en la conversación y configurar específicamente los parámetros de API para cada conversación de forma independiente. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Modificar contenido del chat: al pasar el ratón sobre un mensaje en el chat, aparecerá un botón de ajustes para ese mensaje en particular. Esto permite regenerar, editar, copiar o eliminar el contenido, así como regenerarlo debajo (para mensajes de usuario).

* Visualización de imágenes: Para la generación de imágenes, al hacer clic en una imagen se abrirá la ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como PNG/UE Texture. Las Textures pueden verse directamente en el explorador de contenido (Content Browser), facilitando su uso dentro del editor. Además, se pueden eliminar, regenerar o seguir generando más imágenes. En el editor de Windows, también es posible copiar imágenes al portapapeles para un uso más conveniente. Las imágenes generadas en una sesión se guardarán automáticamente en la carpeta de cada sesión, generalmente en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Configuración global:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Configuración de la conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modificar el contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visor de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

###Introducción al código principal

Actualmente, el complemento se divide en dos módulos: AIChatPlusCommon (tiempo de ejecución) y AIChatPlusEditor (editor). Dos módulos en total.

AIChatPlusCommon es responsable de manejar el envío de solicitudes y analizar el contenido de las respuestas; AIChatPlusEditor es responsable de implementar el editor de herramientas de chat de inteligencia artificial.

Traduzca este texto al español:

El `UClass` responsable específico de enviar la solicitud es `FAIChatPlus_xxxChatRequest`, cada servicio de API tiene su propio `UClass` de solicitud independiente. Las respuestas de las solicitudes se obtienen a través de dos tipos de `UClass`: `UAIChatPlus_ChatHandlerBase` y `UAIChatPlus_ImageHandlerBase`, solo es necesario registrar el delegado de devolución de llamada correspondiente.

Antes de enviar una solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar. Esta configuración se realiza a través de FAIChatPlus_xxxChatRequestBody. La respuesta específica también se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir la devolución, se puede obtener el ResponseBody a través de una interfaz específica.

Puede encontrar más detalles del código fuente en la tienda de UE: [AIChatPlus]()


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
