---
layout: post
title: DeepSeek
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
description: DeepSeek
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - DeepSeek" />

#Sección de Blueprint - DeepSeek

Debido a que DeepSeek es compatible con el formato de interfaz API de OpenAI, podemos acceder fácilmente a DeepSeek utilizando nodos relacionados con OpenAI, simplemente modificando la URL relevante a la URL de DeepSeek.

#Charla de texto

Crear el nodo "Opciones de Chat de OpenAI", configurar los parámetros Model, Url y Api Key.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/deepseek_chat_1.png)

El resto de la configuración es la misma que la de OpenAI, y el esquema completo se ve así:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

Ejecute para ver la salida de DeepSeek en la pantalla:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor, informa en [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
