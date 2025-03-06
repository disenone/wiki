---
layout: post
title: Gemini
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
description: Gemini
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Gemini" />

#Sección de Planes - Géminis

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_all.png)

###Conversación de texto.

Crear el nodo "Opciones de Chat de Gemini", y configurar los parámetros "Modelo" y "Clave API".

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_chat_1.png)

Crear un nodo "Petición de Chat de Gemini" y conectarlo con los nodos "Opciones" y "Mensajes", luego haz clic en ejecutar. En la pantalla podrás ver impresa la información de chat de Gemini devuelta, como se muestra en la imagen:

![](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###Generación de texto a partir de imágenes

Crear un nodo "Opciones de Chat de Gemini", y configurar los parámetros "Modelo" y "Clave Api".

Leer la imagen flower.png del archivo y establecerla en "Messages".

![flower.png](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_vision_1.png)

Cree un nodo "Solicitud de Chat de Géminis", haga clic en ejecutar y podrá ver en la pantalla la información del chat devuelta por Géminis, como se muestra en la imagen:

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_vision_2.png)

###Generación de texto a partir de audio.

Gemini supports converting audio into text.

Crea el siguiente esquema, configura la carga de audio, ajusta las Opciones de Géminis, haz clic en Ejecutar, y verás en pantalla la información de chat devuelta por Géminis después de procesar el audio. 

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor, [**proporciona feedback**](https://github.com/disenone/wiki_blog/issues/new)Señalar cualquier omisión. 
