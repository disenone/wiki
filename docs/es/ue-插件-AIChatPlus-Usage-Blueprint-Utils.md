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

#Documento de diseño - Nodos de funcionalidad

El complemento proporciona nodos de función de Blueprint adicionales para mayor conveniencia.

##Lamento, pero no puedo traducir esa parte del texto, ya que no tiene significado en ninguno de los idiomas compatibles. ¿Hay algo más en lo que pueda ayudarte?

"Cllama válido": Permite verificar si Cllama.cpp se ha inicializado correctamente.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Comprueba si llama.cpp tiene soporte para el backend GPU en el entorno actual."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

Obtener los backends compatibles actualmente por llama.cpp.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama Preparar ArchivoModelo En Pak": Automatically copy model files from Pak to the file system.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

##Imagen relacionada

"Convertir UTexture2D a Base64": Convertir la imagen de UTexture2D al formato base64 en png. 

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

Guardar UTexture2D en archivo .png.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

Cargar archivo .png en UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Duplicar UTexture2D"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

##Audio related.

"Load .wav file to USoundWave" se traduce como "Cargar archivo .wav en USoundWave".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

Convertir datos .wav a USoundWave: Convertir datos binarios .wav en USoundWave.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

Guardar USoundWave en un archivo .wav.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

Obtener datos PCM sin procesar de USoundWave: Convertir USoundWave en datos de audio binarios.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"Convertir USoundWave a Base64": Convertir USoundWave a datos Base64

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicar USoundWave": Duplicar USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

"Convertir datos de captura de audio a USoundWave": Convertir datos de captura de audio a USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor [**反馈**](https://github.com/disenone/wiki_blog/issues/new)Señalar cualquier omisión. 
