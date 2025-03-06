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

#Artículo sobre el editor - Empezar

##Herramienta de chat del editor.

En la barra de menú, ir a Herramientas -> AIChatPlus -> AIChat abre la herramienta de chat del editor proporcionada por el complemento.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


El software admite la generación de texto, chat de texto, generación de imágenes y análisis de imágenes.

La interfaz de la herramienta es aproximadamente:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

##Función principal

* **Modelo grande sin conexión**: Integración de la librería llama.cpp, que permite ejecutar modelos grandes en modo local sin conexión.

* **Text chat**: Haz clic en el botón `Nuevo chat` en la esquina inferior izquierda, para iniciar una nueva sesión de chat de texto.

**Generación de imágenes**: Haga clic en el botón `New Image Chat` en la esquina inferior izquierda para iniciar una nueva sesión de generación de imágenes.

* **Análisis de imágenes**: Algunos servicios de chat de `New Chat` admiten el envío de imágenes, como Claude y Google Gemini. Simplemente haz clic en el botón 🖼️ o 🎨 encima del campo de entrada para cargar la imagen que deseas enviar.

* **Procesamiento de audio**: La herramienta permite leer archivos de audio (.wav) y grabar sonidos, lo que te permite conversar con la inteligencia artificial utilizando el audio obtenido.

* **Establecer el rol actual en la conversación**: El menú desplegable en la parte superior del cuadro de chat permite seleccionar el rol actual desde el cual se enviará el texto, lo que permite simular diferentes roles para ajustar la conversación con la inteligencia artificial.

* **Limpiar conversación**: El ícono de ❌ en la parte superior de la ventana de chat permite borrar el historial de mensajes de la conversación actual.

* **Plantilla de diálogo**: Incorpora cientos de plantillas de configuración de diálogo para facilitar el tratamiento de problemas comunes.

* **Global Settings**: By clicking on the `Setting` button in the bottom left corner, you can open the global settings window. Here you can configure default text chat, the API service for image generation, and specify parameters for each API service. The settings will be automatically saved in the project path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

**Configuración de la conversación**: Al hacer clic en el botón de configuración en la parte superior del cuadro de chat, se puede abrir la ventana de configuración de la conversación actual. Permite modificar el nombre de la conversación, cambiar el servicio API utilizado en la conversación, y ajustar parámetros específicos de API para cada conversación de forma individual. La configuración de la conversación se guarda automáticamente en `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Modificar el contenido del chat: al pasar el mouse sobre el contenido del chat, se mostrará un botón de configuración para ese mensaje en particular, que permite regenerar, modificar, copiar o eliminar el contenido, así como regenerarlo debajo (para los mensajes generados por el usuario).

* **Visor de imágenes**: Para la generación de imágenes, al hacer clic en una imagen se abrirá la ventana de visualización de imágenes (ImageViewer), que permite guardar la imagen como PNG/UE Texture. Las Textures pueden ser visualizadas directamente en el Explorador de Contenido (Content Browser), facilitando su uso dentro del editor. También se ofrece soporte para eliminar imágenes, regenerarlas, continuar generando más imágenes, entre otras funciones. En el editor de Windows, también se puede copiar la imagen al portapapeles para un uso conveniente. Las imágenes generadas durante la sesión se guardarán automáticamente en la carpeta de cada sesión, generalmente en la ruta `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Ajustes generales:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Ajustes de conversación:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Editar el contenido del chat:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visor de imágenes:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Utilización de modelos de gran escala sin conexión.

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Plantilla de diálogo

![system template](assets/img/2024-ue-aichatplus/system_template.png)

##Utiliza el modelo offline Cllama(llama.cpp) en la herramienta del editor.

The following explains how to use the offline model llama.cpp in the AIChatPlus editor tool.

Primero, descarga el modelo sin conexión desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloca el modelo en una carpeta específica, por ejemplo, en el directorio Content/LLAMA del proyecto de juego.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Abre la herramienta de edición AIChatPlus: Herramientas -> AIChatPlus -> AIChat, crea una nueva sesión de chat y abre la página de configuración de la sesión.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Configure Api as Cllama, enable Custom Api Settings, add model search paths, and select model.


![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Comenzar a chatear!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

##Utiliza el modelo sin conexión Cllama (llama.cpp) en la herramienta del editor para procesar imágenes.

Descarga el modelo móvil MobileVLM_V2-1.7B-GGUF de la página web de HuggingFace y colócalo en el directorio Content/LLAMA con el nombre [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)Lo siento, pero no puedo traducir caracteres que no contienen ninguna información. ¿Hay algo más en lo que pueda ayudarte?

Establecer el modelo de sesión:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)


Enviar una imagen para comenzar a chatear.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

##El editor utiliza el chat de OpenAI.

Abra la herramienta de chat Tools -> AIChatPlus -> AIChat, cree una nueva conversación en New Chat, configure la conversación ChatApi en OpenAI, y establezca los parámetros de la interfaz.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Iniciar conversación:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Cambiar el modelo a gpt-4o / gpt-4o-mini te permitirá utilizar la función de análisis visual de OpenAI en las imágenes.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

##El editor utiliza OpenAI para procesar imágenes (crear/modificar/variaciones).

Crear un nuevo chat de imágenes en la herramienta de mensajería, cambiar la configuración del chat a OpenAI y ajustar los parámetros.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Crear imagen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Modifica la imagen cambiando el tipo de chat de "Image Chat Type" a "Edit", y sube dos imágenes: una es la imagen original y la otra es la máscara donde las áreas transparentes (canal alfa 0) indican las zonas a modificar.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Transforma la imagen, cambia el tipo de chat de imagen a Variación, y sube una imagen. OpenAI generará una variante de la imagen original.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

##El editor utiliza Azure.

Crear una nueva conversación ("New Chat"), cambiar ChatApi a Azure y configurar los parámetros de la API de Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Comenzar la conversación.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

##Use Azure to create images in the editor.

Crear una nueva sesión de imagen (New Image Chat), cambiando ChatApi a Azure y configurando los parámetros de la API de Azure. Tenga en cuenta que si es el modelo dall-e-2, los parámetros de Calidad y Estilo deben configurarse en not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Comience a chatear para que Azure cree la imagen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

##Utilice el editor para chatear con Claude y analizar imágenes.

Crear nueva conversación (New Chat), cambiar ChatApi a Claude y configurar los parámetros de Api de Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Iniciar conversación.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

##El editor utiliza Ollama para chatear y analizar imágenes.

Cree una nueva conversación (New Chat), cambie ChatApi a Ollama y configure los parámetros de la API de Ollama. Si es un chat de texto, establezca el modelo como modelo de texto, como llama3.1; si necesita procesar imágenes, establezca el modelo como un modelo que admita visión, como moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Iniciar chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)


###El editor utiliza Gemini.

Crear una nueva conversación (New Chat), cambiar ChatApi por Gemini y configurar los parámetros de la API de Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Iniciar conversación

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

##El editor utiliza Gemini para enviar contenido de audio.

Seleccionar entre leer audio de un archivo, leer audio de un recurso o grabar audio desde un micrófono para generar el audio a enviar.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

Comenzar la conversación

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

##El editor utiliza Deepseek.

Crear una nueva conversación (New Chat), cambiar ChatApi a OpenAi y configurar los parámetros de la Api de Deepseek. Agregar el modelo de candidato llamado deepseek-chat y establecer el modelo como deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Comenzar la conversación.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor [**反馈**](https://github.com/disenone/wiki_blog/issues/new)Señalar cualquier omisión. 
