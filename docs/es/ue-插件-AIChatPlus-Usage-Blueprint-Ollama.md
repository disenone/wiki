---
layout: post
title: Ollama
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
description: Ollama
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Ollama" />

#Capítulo del Blueprint - Ollama

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_all.png)

##Obtener Ollama

Puedes descargar el paquete de instalación de Ollama desde su página web oficial para instalarlo localmente: [ollama.com](https://ollama.com/)

Puedes utilizar Ollama a través de la API proporcionada por terceros.

Utilice Ollama para descargar modelos localmente:

```shell
> ollama run qwen:latest
> ollama run moondream:latest
```

##Mensajes de texto

Crea el nodo "Ollama Options", configura los parámetros "Model" y "Base Url". Si estás corriendo Ollama localmente, el "Base Url" generalmente es "http://localhost:11434".

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_chat_1.png)

Conecta el nodo "Ollama Request" con el nodo relacionado "Messages", haz clic en ejecutar, y podrás ver en pantalla la información de chat devuelta por Ollama.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

##Generador de texto de imagen 3D.

Ollama también apoya la biblioteca llava, brindando capacidades de Vision.

Primero, obten el archivo del modelo Multimodal:

```shell
> ollama run moondream:latest
```

Establezca el nodo "Opciones", y seleccione "Modelo" como moondream:latest.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_1.png)

Lee la imagen flower.png y establece el mensaje.

![flower.png](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_3.png)

Conecta al nodo "Ollama Request", haz clic en ejecutar y verás en pantalla la información de chat que Ollama devuelve.

![](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_4.png)

![](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_5.png)

--8<-- "footer_es.md"


> Este mensaje ha sido traducido con ChatGPT. Por favor, envía tus [**comentarios**](https://github.com/disenone/wiki_blog/issues/new)Indique cualquier omisión. 
