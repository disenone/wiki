---
layout: post
title: 功能节点
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini, Ollama]
description: 功能节点
---
<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - 功能节点" />

# 蓝图篇 - 功能节点

插件额外提供了一些便利的蓝图功能节点

## Cllama 相关

"Cllama Is Valid"：判断 Cllama llama.cpp 是否正常初始化

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu"：判断 llama.cpp 在当前环境下是否支持 GPU backend

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Cllama Get Support Backends": 获取当前 llama.cpp 支持的所有 backends


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama Prepare ModelFile In Pak": 自动把 Pak 中的模型文件复制到文件系统中

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

### 图像相关

"Convert UTexture2D to Base64": 把 UTexture2D 的图像转成 png base64 格式

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

"Save UTexture2D to .png file": 把 UTexture2D 保存成 png 文件

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

"Load .png file to UTexture2D": 读取 png 文件为 UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Duplicate UTexture2D": 复制 UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

### 音频相关

"Load .wav file to USoundWave": 读取 wav 文件为 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

"Convert .wav data to USoundWave": 把 wav 二进制数据转成 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

"Save USoundWave to .wav file": 把 USoundWave 保存为 .wav 文件

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

"Get USoundWave Raw PCM Data": 把 USoundWave 转成二进制音频数据

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"Convert USoundWave to Base64": 把 USoundWave 转成 Base64 数据

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicate USoundWave": 复制 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

"Convert Audio Capture Data to USoundWave": 把 Audio Capture 录音数据转成 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

--8<-- "footer.md"
