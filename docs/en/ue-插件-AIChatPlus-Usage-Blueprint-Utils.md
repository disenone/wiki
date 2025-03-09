---
layout: post
title: Functional node
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
description: Functional Node
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - 功能节点" />

#Blueprint Section - Feature Nodes

The plugin provides additional convenient blueprint nodes.

##Cllama Related

"Verify if Cllama Is Valid": Check whether Cllama llama.cpp is initialized correctly.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

Determine if llama.cpp supports GPU backend in the current environment.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

Retrieve all backends currently supported by llama.cpp.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

Automatically copy model files from Pak to the file system.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

##Image related

Convert the image of UTexture2D to png base64 format.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

Save UTexture2D as a .png file.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

Load the .png file into UTexture2D.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

Duplicate UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

##Audio-related

Load the .wav file into USoundWave.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

"Convert .wav data to USoundWave": Convert binary .wav data to USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

Save USoundWave as a .wav file.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

Convert USoundWave to raw PCM data.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

Convert USoundWave to Base64: Convert USoundWave to Base64 data

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

Duplicate USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

"Convert Audio Capture Data to USoundWave" : Convert the audio recording data from Audio Capture to USoundWave.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

--8<-- "footer_en.md"


> This post was translated using ChatGPT. Please provide [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
