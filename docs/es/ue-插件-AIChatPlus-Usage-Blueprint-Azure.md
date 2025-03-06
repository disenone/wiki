---
layout: post
title: Azure
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
description: Azure
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Azure" />

#Capítulo del Libro Azul - Azure

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_all.png)

El uso de Azure es muy similar al de OpenAI, por lo que aquí se presenta de forma concisa.

##Conversación de texto.

Crear el nodo "Opciones de Chat de Azure", configurar los parámetros "Nombre de Implementación", "URL Base", "Clave API".

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_chat_1.png)

Crear un nodo relacionado con "Mensajes" y vincularlo con "Solicitud de Chat de Azure", haz clic en ejecutar y podrás ver en la pantalla la información de chat devuelta por Azure. Referirse a la imagen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

##Crear imagen

Crear el nodo "Opciones de Imagen de Azure", y configurar los parámetros "Nombre del Despliegue", "URL Base", "Clave de API".

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_image_1.png)

Configure los nodos "Azure Image Request" y otros, haga clic en Ejecutar y verá la información del chat devuelta por Azure impresa en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

Según la configuración del esquema anterior, la imagen se guardará en la ruta D:\Dwnloads\butterfly.png.

--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor deja tu [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Indique cualquier omisión. 
