---
layout: post
title: Documento de instrucciones de UE del complemento AIChatPlus.
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

#UE 插件 AIChatPlus 说明文档

##Depósito público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtener complemento

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introducción del complemento

Este complemento es compatible con UE5.2+.

UE.AIChatPlus es un complemento para Unreal Engine que permite la comunicación con diversos servicios de chat AI GPT. Actualmente, admite servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, y llama.cpp en modo local sin conexión a internet. En el futuro, se añadirá soporte para más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que garantiza un alto rendimiento y facilita la integración de estos servicios de chat AI en Unreal Engine para los desarrolladores.

Al mismo tiempo, UE.AIChatPlus también incluye una herramienta de edición que permite utilizar directamente estos servicios de chat de IA en el editor para generar texto e imágenes, analizar imágenes, y más.

##Instrucciones de Uso

###Herramienta de chat del editor

La barra de menú Herramientas -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


La herramienta admite la generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es más o menos así:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####**Características principales**

* Modelo grande sin conexión: integración de la biblioteca llama.cpp para admitir la ejecución sin conexión de modelos grandes a nivel local

* **Texto del chat**: Haz clic en el botón `New Chat` en la esquina inferior izquierda para crear una nueva conversación de chat de texto.

* Generación de imagen: haz clic en el botón `New Image Chat` en la esquina inferior izquierda para iniciar una nueva sesión de generación de imágenes.

* Análisis de imágenes: Algunos servicios de chat en `New Chat` admiten el envío de imágenes, como Claude, Google Gemini. Simplemente haz clic en el botón 🖼️ o 🎨 ubicado encima del cuadro de texto para cargar la imagen que deseas enviar.

Apoyo de Blueprints (Blueprint): Apoyo para la creación de solicitudes de API de Blueprints, para completar funciones como chat de texto, generación de imágenes, entre otras.

Establecer el rol actual del chat: el menú desplegable en la parte superior de la ventana de chat puede seleccionar el rol actual para enviar texto, lo que permite simular diferentes roles para ajustar la conversación de la inteligencia artificial.

Limpiar conversación: al presionar la equis ❌ en la parte superior de la ventana de chat, se pueden eliminar los mensajes históricos de la conversación actual.

* Plantilla de diálogo: incorpora cientos de plantillas de configuración de diálogo para facilitar el manejo de problemas comunes.

Establecimientos generales: al pulsar el botón `Setting` en la esquina inferior izquierda, se abrirá la ventana de establecimientos generales. Puede configurar el chat de texto predeterminado, el servicio API para generar imágenes y especificar los parámetros de cada servicio API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Configuración de la conversación: Al hacer clic en el botón de configuración en la parte superior de la ventana de chat, se puede abrir la ventana de configuración de la conversación actual. Permite cambiar el nombre de la conversación, modificar el servicio de API utilizado en la conversación, y ajustar parámetros específicos de API para cada conversación de forma independiente. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

Editar contenido del chat: al pasar el mouse sobre el contenido del chat, aparecerá un botón de configuración para ese contenido en particular, que permite regenerarlo, editarlo, copiarlo, eliminarlo o regenerar un nuevo contenido debajo (para el contenido generado por el usuario).

* Visor de imágenes: Para la generación de imágenes, haz clic en una imagen para abrir la ventana de visualización de imágenes (ImageViewer), que admite guardar imágenes como PNG/UE Texture, las cuales se pueden ver directamente en el explorador de contenido (Content Browser) para facilitar su uso en el editor. También se pueden eliminar imágenes, regenerarlas, continuar generando más imágenes, entre otras funciones. Para el editor en Windows, también se puede copiar imágenes para pegarlas directamente en el portapapeles para facilitar su uso. Las imágenes generadas en la sesión se guardarán automáticamente en la carpeta de cada sesión, generalmente en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

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

Utilizar modelos grandes sin conexión

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Plantilla de conversación

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introducción al código principal

En la actualidad, el complemento se divide en los siguientes módulos:

* AIChatPlusCommon: Módulo en tiempo de ejecución (Runtime) responsable de manejar las solicitudes de envío de diversas interfaces de API de IA y analizar el contenido de las respuestas.

* AIChatPlusEditor: Módulo de editor, encargado de implementar la herramienta de chat de IA del editor.

* AIChatPlusCllama: El módulo de tiempo de ejecución (Runtime), que encapsula la interfaz y los parámetros de llama.cpp, para llevar a cabo la ejecución sin conexión de modelos grandes.

* Thirdparty/LLAMACpp: Módulo de terceros en tiempo de ejecución (Runtime) que integra la biblioteca dinámica y los archivos de cabecera de llama.cpp.

El UClass responsable de enviar las solicitudes específicas es FAIChatPlus_xxxChatRequest; cada servicio de API tiene su propio UClass de solicitud independiente. Las respuestas a las solicitudes se obtienen a través de dos tipos de UClass: UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase; solo es necesario registrar los delegados de devolución de llamada correspondientes.

Antes de enviar una solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar. Esto se hace mediante FAIChatPlus_xxxChatRequestBody. La respuesta específica se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir la devolución de llamada, se puede obtener el ResponseBody a través de una interfaz específica.

Más detalles del código fuente están disponibles en la tienda de UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)


###Guía de uso

####Utilice el modo sin conexión del editor de herramientas llama.cpp

A continuación se explica cómo utilizar el modelo fuera de línea llama.cpp en la herramienta de edición AIChatPlus.

Primero, descarga el modelo offline desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloca el modelo en una carpeta específica, por ejemplo, en el directorio Content/LLAMA del proyecto del juego.

	```shell
	E:/UE/projects/FP_Test1/Content/LLAMA
	> ls
	qwen1.5-1_8b-chat-q8_0.gguf*
	```

Abre la herramienta de edición AIChatPlus: Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat y abre la página de configuración de la sesión.

	![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Establece Api como Cllama, activa la Configuración de Api Personalizada, añade la ruta de búsqueda de modelos y selecciona un modelo.

	![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

¡Comencemos a charlar!

	![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

####El código utiliza el modelo fuera de línea llama.cpp

todo

####La utilización del modelo fuera de línea de llama.cpp.

todo

###Registro de actualizaciones

#### v1.3.1 - 2024.9.30

Añadir un SystemTemplateViewer, que permite ver y utilizar cientos de plantillas de configuración del sistema.

##### Bugfix

Reparar el complemento descargado desde la tienda, llama.cpp no puede encontrar la biblioteca de vínculos.
Corregir problema de ruta demasiado larga en LLAMACpp
Corregir el error de enlace llama.dll después de empaquetar en Windows
Corregir problema de lectura de ruta de archivo en iOS/Android.
Corregir el error de configuración de Cllame que establece mal el nombre

#### v1.3.0 - 2024.9.23

Actualización importante

Integré llama.cpp para admitir la ejecución sin conexión local de modelos grandes.

#### v1.2.0 - 2024.08.20

Apoyo a OpenAI Image Edit/Image Variation.

Apoyo la API de Ollama, que permite obtener automáticamente la lista de modelos admitidos por Ollama.

#### v1.1.0 - 2024.08.07

Apoyar el plan.

#### v1.0.0 - 2024.08.05

* Función completa y básica.

Apoyo a OpenAI, Azure, Claude, Gemini

* Herramienta de chat con editor integrado y funciones completas.

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
