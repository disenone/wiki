---
layout: post
title: 'Traduce el texto al español: "Documentación de instrucciones del complemento
  de UE AIChatPlus"'
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

#Documentación de UE Plugin AIChatPlus

##Repositorio público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complemento

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento de UnrealEngine que permite la comunicación con varios servicios de chat de inteligencia artificial GPT. Actualmente, admite servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude y Google Gemini. En el futuro, se agregarán más proveedores de servicios. Su implementación se basa en solicitudes REST asincrónicas, lo que garantiza un rendimiento eficiente y facilita a los desarrolladores de UnrealEngine acceder a estos servicios de chat de inteligencia artificial.

UE.AIChatPlus también incluye una herramienta de edición que te permite utilizar directamente los servicios de chat de inteligencia artificial en el editor para generar texto e imágenes, analizar imágenes, entre otras funciones.

##Instrucciones de uso

###Herramienta de chat del editor

El menú Tools -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


La herramienta admite la generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Función principal

* Chat de texto: haz clic en el botón `New Chat` en la esquina inferior izquierda para crear una nueva sesión de chat de texto.

* Generación de imagen: Haga clic en el botón `Nuevo chat de imagen` en la esquina inferior izquierda para crear una nueva sesión de generación de imagen.

* Análisis de imagen: Algunos servicios de chat en la sección `New Chat` admiten el envío de imágenes, como Claude, Google Gemini. Simplemente haz clic en los botones 🖼️ o 🎨 sobre la casilla de entrada para cargar la imagen que deseas enviar.

* Soporte de Blueprint: admite la creación de solicitudes de API de Blueprint para funciones como chat de texto, generación de imágenes, entre otros.

Establecer el rol actual de chat: el menú desplegable en la parte superior de la ventana de chat se puede utilizar para seleccionar el rol actual para enviar mensajes de texto, permitiendo simular diferentes roles para ajustar la conversación con la IA.

Eliminar conversación: El botón ❌ en la parte superior de la ventana de chat permite borrar el historial de mensajes de la conversación actual.

* Configuración general: Al hacer clic en el botón `Setting` en la esquina inferior izquierda, se abrirá la ventana de configuración general. Puedes establecer el chat de texto predeterminado, el servicio de API para generar imágenes y configurar los parámetros específicos de cada servicio de API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* **Configuración de la conversación:** Haz clic en el botón de configuración en la parte superior de la ventana de chat para abrir la ventana de configuración de la conversación actual. Permite modificar el nombre de la conversación, cambiar el servicio de API utilizado en la conversación, y ajustar los parámetros específicos de API para cada conversación de forma independiente. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

Modificar contenido del chat: Al pasar el ratón sobre el contenido del chat, aparecerá un botón de configuración para ese contenido en particular, que permitirá regenerar, modificar, copiar o borrar el contenido, así como regenerar contenido debajo (para contenido generado por el usuario).

* Visor de imágenes: En cuanto a la generación de imágenes, hacer clic en una imagen abrirá la ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como PNG/Textura UE, las texturas se pueden ver directamente en el explorador de contenidos (Content Browser), facilitando así su uso en el editor. Además, también se pueden eliminar imágenes, regenerarlas, generar más imágenes, entre otras funciones. Para los editores en Windows, también es posible copiar imágenes y pegarlas directamente en el portapapeles para facilitar su uso. Las imágenes generadas en la sesión se guardarán automáticamente en la carpeta de cada sesión, por lo general en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Plan:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Ajustes generales:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Configuración de la conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modificar el contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visor de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

###Introducción al código central

En este momento, el complemento se divide en dos módulos: AIChatPlusCommon (Tiempo de ejecución) y AIChatPlusEditor (Editor).

AIChatPlusCommon se encarga de manejar el envío de solicitudes y analizar el contenido de las respuestas; AIChatPlusEditor se encarga de implementar la herramienta de chat de inteligencia artificial del editor.

Traduce este texto al español:

La UClass responsable específicamente de enviar solicitudes es FAIChatPlus_xxxChatRequest; cada servicio de API tiene su propia UClass de solicitud independiente. Las respuestas a las solicitudes se obtienen a través de dos UClass diferentes: UAIChatPlus_ChatHandlerBase y UAIChatPlus_ImageHandlerBase; solo es necesario registrar los delegados de devolución de llamada correspondientes.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar, esto se hace a través de FAIChatPlus_xxxChatRequestBody. El contenido específico de la respuesta también se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir la devolución se puede obtener el ResponseBody a través de una interfaz específica.

Puedes obtener más detalles del código fuente en la tienda de Epic Games: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)


###**Registro de actualizaciones**

#### v1.0.0

* Funcionalidad básica completa
Apoyo a OpenAI, Azure, Claude, Gemini
Apoyar el plan proporicionado.
* Herramienta de chat con editor integrado y funciones completas. 


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
