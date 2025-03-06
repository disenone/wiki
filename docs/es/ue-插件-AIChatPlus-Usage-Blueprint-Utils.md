---
layout: post
title: Nodo de función
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
description: Nodo de función
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - 功能节点" />

#Traducción: Capítulo de la Plataforma - Nodos Funcionales

El complemento incluye funciones de nodos de conveniencia adicionales para los gráficos de diseño.

##Llama 相关.

"Cllama Is Valid"：Verificar si Cllama está correctamente inicializado en el archivo llama.cpp

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu" se traduce como "Cllama es compatible con GPU"：判断 llama.cpp 在当前环境下是否支持 GPU backend.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Obtener Soporte de Backends de Llama": Obtener todos los backends soportados por llama.cpp actualmente.


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Copia y prepara el archivo del modelo en Pak": Automatically copies model files from Pak to the file system

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###Imagen relacionada

"Convertir UTexture2D a Base64": Convertir la imagen de UTexture2D al formato base64 de png.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

Guardar UTexture2D en un archivo .png.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

"Load .png file to UTexture2D": Cargar archivo .png en UTexture2D. 

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Duplicar UTexture2D"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###Audio relacionado

"Cargar archivo .wav en USoundWave"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

Convertir datos .wav a USoundWave: convertir datos binarios .wav a USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

Guardar USoundWave en un archivo .wav.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

Obtener datos PCM sin procesar de USoundWave: Convertir USoundWave en datos de audio binario.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"Convertir USoundWave a Base64": Convertir USoundWave a datos Base64

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicar USoundWave"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

"Convertir datos de captura de audio a USoundWave": Convertir datos de captura de audio a USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor, [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
