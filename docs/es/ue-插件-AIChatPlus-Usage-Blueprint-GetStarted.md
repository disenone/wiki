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

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Get Started" />

#Sección de Planes: Empezar

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

## Get Started

A continuación, se describe el método básico de uso de un blueprint, tomando como ejemplo OpenAI.

###Conversación de texto

Utilizar OpenAI para chatear por texto

En el blueprint, crea un nodo con clic derecho llamado `Enviar solicitud de chat de OpenAI en el mundo`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Crea el nodo Options y establece `Stream=true, Api Key="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Crear mensajes, agregar un mensaje del sistema y un mensaje del usuario.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Crear un delegado para recibir la información del modelo y mostrarla en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

La traducción al español sería:

El aspecto completo del blueprint es este, ejecuta el blueprint y podrás ver en la pantalla del juego el mensaje devuelto al imprimir el modelo grande.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Crear imagen a partir del texto.

Utilizar OpenAI para crear imágenes.

En el panel de Blueprints, haz clic derecho para crear un nodo llamado `Send OpenAI Image Request`, y configura `In Prompt="una mariposa hermosa"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Crea un nodo de Options y establece `Api Key="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Vincula el evento "On Images" y guarda las imágenes en el disco duro local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

El aspecto completo del diseño es el siguiente, al ejecutarlo, podrás ver que la imagen se guarda en la ubicación especificada.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

###Generación de texto a partir de imágenes.

Utilizar OpenAI Vision para analizar imágenes.

En el diagrama, haz clic derecho para crear un nodo llamado `Send OpenAI Image Request`.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_1.png)

Crear un nodo de opciones y establecer `Api Key="tu clave de API de OpenAI"`, configurar el modelo como `gpt-4o-mini`.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_2.png)

Crear Mensajes.
Primero, crea un nodo "Importar archivo como textura 2D" para cargar una imagen desde el sistema de archivos.
Utiliza el nodo "Create AIChatPlus Texture From Texture2D" para convertir la imagen en un objeto utilizable por el complemento.
Conecta las imágenes al campo "Imágenes" del nodo "AIChatPlus_ChatRequestMessage" usando el nodo "Crear arreglo".
Establecer el contenido del campo "Content" como "describe this image".

"Como se muestra en la imagen:"

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_3.png)

Una vez que se ejecuta el diagrama completo, los resultados se mostrarán en pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_4.png)

--8<-- "footer_es.md"


> Este mensaje ha sido traducido con ChatGPT, por favor [**proporcionar comentarios**](https://github.com/disenone/wiki_blog/issues/new)Señala cualquier omisión. 
