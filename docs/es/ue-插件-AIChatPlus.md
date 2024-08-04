---
layout: post
title: Plugin UE.EditorPlus documentation.
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
description: Plugin del editor UE  UE.EditorPlus Documentación
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documento de instrucciones del complemento UE AIChatPlus


##Presentación de video

![type:video]()

##Repositorio público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complemento

[AIChatPlus]()

##Introducción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento de UnrealEngine que permite la comunicación con varios servicios de chat de inteligencia artificial GPT. Actualmente soporta servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude y Google Gemini. En el futuro se añadirán más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que lo hace eficiente y facilita a los desarrolladores de Unreal Engine integrar estos servicios de chat de IA.

UE.AIChatPlus también incluye una herramienta de edición que te permite utilizar directamente los servicios de chat de IA en el editor para generar texto e imágenes, analizar imágenes, entre otras funciones.

##Instrucciones de uso

###Herramienta de chat del editor

El menú Tools -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


La herramienta admite la generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

Las traducciones al español de los textos solicitados son:

Funciones principales incluyen:

* Chat de texto: haz clic en el botón `New Chat` en la esquina inferior izquierda para crear una nueva conversación de chat de texto.
* Generación de imagen: haz clic en el botón `New Image Chat` en la esquina inferior izquierda para crear una nueva sesión de generación de imagen.
* Análisis de imagen: Algunos servicios de chat de `New Chat` admiten el envío de imágenes, como Claude, Google Gemini. Simplemente haz clic en el botón 🖼️ o 🎨 arriba del cuadro de texto para cargar la imagen que deseas enviar.
Establecer el rol actual en el chat: El menú desplegable en la parte superior del cuadro de chat te permite seleccionar el rol actual para enviar mensajes de texto, lo que te permite simular diferentes roles para ajustar la conversación con la IA.
Eliminar conversación: El botón ❌ en la parte superior de la ventana de chat puede borrar el historial de mensajes de la conversación actual.
Translate these text into Spanish language:

**Configuración global:** Haz clic en el botón `Configuración` en la esquina inferior izquierda para abrir la ventana de configuración global. Puedes establecer el chat de texto predeterminado, el servicio de API para generar imágenes y configurar los parámetros específicos de cada servicio de API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.
* Configuración de la conversación: al hacer clic en el botón de configuración en la parte superior de la ventana de chat, se puede abrir la ventana de configuración de la conversación actual. Permite cambiar el nombre de la conversación, modificar los servicios de API utilizados en la conversación, y ajustar los parámetros específicos de API para cada conversación de forma individual. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.
Modificar el contenido del chat: al colocar el cursor sobre el contenido del chat, aparecerá un botón de configuración para dicho contenido, que permitirá regenerarlo, editarlo, copiarlo, eliminarlo o regenerar otro contenido debajo de él (para el contenido del chat generado por el usuario).
* Visualización de imágenes: Para la generación de imágenes, hacer clic en una imagen abrirá la ventana de visualización de imágenes (ImageViewer), que admite guardar la imagen como PNG/UE Texture. Las Texturas se pueden ver directamente en el Explorador de contenido (Content Browser), lo que facilita su uso dentro del editor. También se admiten funciones como eliminar imágenes, regenerar imágenes, seguir generando más imágenes, entre otras. Para el editor en Windows, también se permite copiar imágenes, lo que permite copiar directamente imágenes al portapapeles para un uso más conveniente. Las imágenes generadas durante la sesión también se guardan automáticamente en la carpeta de cada sesión, generalmente en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Configuración global:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Configuración de la conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modificar el contenido del chat:
![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visualizador de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

###Introducción del código principal

En este momento, el complemento se divide en dos módulos: AIChatPlusCommon (Tiempo de ejecución) y AIChatPlusEditor (Editor).

AIChatPlusCommon es responsable de manejar el envío de solicitudes y analizar el contenido de las respuestas; AIChatPlusEditor se encarga de implementar el editor de herramientas de chat de IA.

Translate these text into Spanish language:

El UClass encargado específicamente de enviar la solicitud es FAIChatPlus_xxxChatRequest, cada tipo de servicio de API tiene su propio UClass de solicitud independiente. Las respuestas de las solicitudes se obtienen a través de dos UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase UClass, solo es necesario registrar los delegados de devolución de llamada correspondientes.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar, esto se realiza a través de FAIChatPlus_xxxChatRequestBody. El contenido específico de la respuesta también se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir la devolución, se puede obtener el ResponseBody a través de una interfaz específica.

Puede obtener más detalles del código fuente en la tienda de UE: [AIChatPlus]()


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
