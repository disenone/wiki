---
layout: post
title: Functional Node
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
description: Functional node
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - 功能节点" />

#Blueprint Chapter - Functional Nodes

The plug-in also offers some convenient blueprint function nodes.

##Cllama related

Check if "Cllama Is Valid": Determine if Cllama llama.cpp is properly initialized.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

Determine if llama.cpp supports GPU backend in the current environment.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

Retrieve all backends that are supported by the current llama.cpp.


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

Automatic copying of model files in PAK to the file system has been prepared by Cllama.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###Image-related

Convert UTexture2D image to png base64 format.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

Save the UTexture2D as a .png file

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

Load a .png file into UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

Duplicate UTexture2D: Copy UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###Audio-related

Load the .wav file into USoundWave.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

Convert the .wav binary data to USoundWave.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

Save USoundWave as a .wav file.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

Convert USoundWave to binary audio data

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

Convert USoundWave to Base64: Convert USoundWave to Base64 data

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

Duplicate USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

Translate the text into English language:

"Convert Audio Capture Data to USoundWave": Convert audio capture recording data to USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

--8<-- "footer_en.md"


> This post was translated using ChatGPT. Please provide [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
