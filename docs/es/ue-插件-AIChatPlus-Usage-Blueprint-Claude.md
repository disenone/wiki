---
layout: post
title: Claude
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
description: Claude
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Claude" />

#Documento de diseño - Claude

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/claude_all.png)

##Conversación de texto

Crear un nodo "Opciones", configurar los parámetros "Modelo", "Clave API", "Versión Antropica"

![](assets/img/2024-ue-aichatplus/usage/blueprint/claude_chat_1.png)

Conecta el nodo "Claude Request" con el nodo relacionado "Messages", haz clic en ejecutar, y podrás ver en la pantalla la información de chat devuelta por Claude. Como se muestra en la imagen.

![](assets/img/2024-ue-aichatplus/usage/blueprint/claude_chat_2.png)

##Generación de texto a partir de imágenes.

Claude también apoya la función Vision.

En el diagrama, haz clic derecho para crear un nodo llamado `Enviar solicitud de chat de Claude`.

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Creación del nodo Options, y establecimiento de `Stream=true, Api Key="tu clave de API de Clude", Max Output Tokens=1024`.

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Crear Messages, crear un Texture2D desde un archivo y luego un AIChatPlusTexture desde el Texture2D, finalmente añadir el AIChatPlusTexture al Mensaje.

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Evento y mostrar la información en la pantalla del juego.

Una vez ejecutado el blueprint completo, verás cómo la pantalla del juego muestra el mensaje devuelto por la impresión del gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)


--8<-- "footer_es.md"


> Este mensaje ha sido traducido usando ChatGPT, por favor comente en [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Identifique cualquier omisión. 
