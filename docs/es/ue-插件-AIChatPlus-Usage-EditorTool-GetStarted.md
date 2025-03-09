---
layout: post
title: Get Started
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
description: Get Started
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 编辑器篇 - Get Started" />

#Editorial - Comenzar

##Herramienta de chat del editor

La barra de menú Herramientas -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


La herramienta admite la generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

##Función principal

**Modelo de gran escala sin conexión**: Integración de la biblioteca llama.cpp que permite la ejecución sin conexión de modelos de gran tamaño en el ordenador local

**Chat de texto**: Haz clic en el botón `New Chat` en la esquina inferior izquierda para crear una nueva conversación de chat de texto.

**Generación de imágenes**: Haz clic en el botón `New Image Chat` en la esquina inferior izquierda para iniciar una nueva sesión de generación de imágenes.

**Análisis de imágenes**: Algunos servicios de chat de `New Chat` admiten el envío de imágenes, como Claude, Google Gemini. Simplemente haz clic en el icono 🖼️ o 🎨 ubicado encima del cuadro de texto para cargar la imagen que deseas enviar.

**Procesamiento de audio**: La herramienta permite leer archivos de audio (.wav) y tiene una función de grabación para poder conversar con inteligencia artificial utilizando el audio obtenido.

**Establecer el personaje de chat actual**: El menú desplegable en la parte superior del cuadro de chat puede establecer el personaje actual que está enviando texto, lo que le permite simular diferentes personajes para ajustar la conversación de la IA.

**Limpiar Conversación**: El icono ❌ en la parte superior del cuadro de chat te permite borrar el historial de mensajes de la conversación actual.

**Plantilla de Conversación**: Incorpora cientos de plantillas de configuración de diálogo para facilitar el manejo de problemas comunes.

**Configuración global**: Al hacer clic en el botón `Configuración` en la esquina inferior izquierda, se abrirá la ventana de configuración global. Puedes establecer el chat de texto predeterminado, los servicios de API de generación de imágenes y definir los parámetros específicos de cada servicio de API. La configuración se guardará automáticamente en la ruta del proyecto `$(ProjectFolder)/Saved/AIChatPlusEditor`.

**Configuración de la conversación**: Al hacer clic en el botón de configuración en la parte superior del cuadro de chat, puedes abrir la ventana de configuración de la conversación actual. Permite cambiar el nombre de la conversación, modificar el servicio API utilizado en la conversación, e incluso ajustar parámetros específicos del uso del API para cada conversación. Las configuraciones de la conversación se guardan automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

**Edición de mensajes**: Al posar el ratón sobre un mensaje en el chat, aparecerá un botón de ajustes para ese mensaje en particular. Permite regenerar, editar, copiar o eliminar el mensaje, así como regenerar un nuevo mensaje debajo (para los mensajes de usuarios).

**Visor de imágenes**: Cuando se genera una imagen, al hacer clic en ella se abrirá una ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como PNG/Textura UE, la cual se puede ver directamente en el explorador de contenido (Content Browser), facilitando su uso dentro del editor. También se puede eliminar, regenerar o seguir generando más imágenes. En el editor de Windows, también es posible copiar imágenes, lo que permite copiarlas al portapapeles para un uso más sencillo. Las imágenes generadas durante la sesión se guardarán automáticamente en la carpeta de cada sesión, generalmente en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Configuración general:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Configuración de la conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Editar el contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visor de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Utilización de modelos grandes sin conexión.

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Plantilla de diálogo

![system template](assets/img/2024-ue-aichatplus/system_template.png)

##Utilizando el modelo fuera de línea Cllama (llama.cpp) en la herramienta del editor.

Estas instrucciones te muestran cómo usar el modelo offline llama.cpp en la herramienta de edición AIChatPlus.

Descarga primero el modelo offline desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloca el modelo en una carpeta específica, por ejemplo en la ruta del proyecto de juegos Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Abre la herramienta de edición AIChatPlus: Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat y accede a la página de configuración de sesión.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Establece la API como Cllama, activa la configuración personalizada de la API y añade la ruta de búsqueda de modelos, luego selecciona el modelo.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

¡Comencemos la conversación!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

##Utilizando el modelo sin conexión Cllama (llama.cpp) en la herramienta del editor para procesar imágenes.

Descarga el modelo offline MobileVLM_V2-1.7B-GGUF desde el sitio web de HuggingFace y colócalo en el directorio Content/LLAMA con el nombre [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)Traduce este texto al español:

 和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)Lo siento, pero no puedo traducir un carácter individual. ¿Hay algo más en lo que pueda ayudarte?

Establecer el modelo de la sesión:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Comenzar la conversación enviando imágenes.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

##El editor utiliza OpenAI para chatear.

Abre la aplicación de chat Herramientas -> AIChatPlus -> AIChat, crea una nueva conversación Nueva conversación, configura la sesión ChatApi como OpenAI, establece los parámetros de la interfaz.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Comenzar chat:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Cambiar el modelo a gpt-4o / gpt-4o-mini para utilizar la función de análisis visual de imágenes de OpenAI.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

##El editor utiliza OpenAI para procesar imágenes (crear/modificar/variar).

Crear una nueva conversación de imágenes en la herramienta de chat, llama esta conversación "OpenAI" y configura los parámetros.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Crear imagen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Por favor, edita la imagen cambiando el tipo de Chat de imagen a Edit, y carga dos imágenes: una será la imagen original y la otra será la máscara donde las áreas transparentes (canal alfa 0) indicarán las zonas a modificar.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Modificar la variante de imagen conversacional a "Variación" y subir una imagen. OpenAI generará una variante de la imagen original.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

##El editor utiliza Azure

Crear una nueva conversación (New Chat), cambiar ChatApi a Azure y configurar los parámetros de la API de Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Iniciar conversación

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

##Utilizando Azure, el editor crea imágenes.

Crear una nueva sesión de imágenes llamada "New Image Chat", cambiar ChatApi a Azure y configurar los parámetros de la API de Azure. Recuerda, si se trata del modelo dall-e-2, es necesario configurar los parámetros Quality y Stype como not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Comience la conversación para que Azure cree la imagen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

##Utilizar a Claude en el editor para chatear y analizar imágenes.

Crear nueva conversación (New Chat), cambiar ChatApi a Claude y configurar los parámetros de la API de Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Comenzar conversación.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

##El editor utiliza Ollama para chatear y analizar imágenes.

Crear una nueva conversación (New Chat), renombrar ChatApi a Ollama y configurar los parámetros de la API de Ollama. Si es una conversación de texto, establecer el modelo como el modelo de texto, como por ejemplo llama3.1; si es necesario procesar imágenes, configurar el modelo como un modelo que admita visión, como por ejemplo moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Comenzar conversación

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Utilizando Gemini como editor.

Crear una nueva conversación (New Chat), cambiar ChatApi por Gemini y configurar los parámetros de la API de Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Iniciar conversación

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

##El editor utiliza Gemini para enviar archivos de audio.

Leer audio desde archivo / Leer audio desde Asset / Grabar audio desde el micrófono, y generar el audio a enviar.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

Comenzar la conversación.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

##El editor utiliza Deepseek.

Crear una nueva conversación (New Chat), cambiar ChatApi por OpenAi y configurar los parámetros de la API de Deepseek. Añadir un nuevo modelo de candidato llamado deepseek-chat y establecer el modelo como deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Comenzar a chatear

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor [**proporcione retroalimentación**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
