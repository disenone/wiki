---
layout: post
title: 功能節點
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
description: 功能節點
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - 功能节点" />

#藍圖篇 - 功能節點

插件提供了一些額外的方便的藍圖功能節點。

##Cllama相關

"Cllama Is Valid": 判斷 Cllama llama.cpp 是否正確初始化

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu": 判斷 llama.cpp 在當前環境下是否支持 GPU backend

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

獲取支援 llama.cpp 目前支援的所有後端。


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama Prepare ModelFile In Pak": 自動將 Pak 中的模型文件複製到檔案系統中

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###圖像相關

將 UTexture2D 轉換為 Base64：將 UTexture2D 圖像轉換為 PNG Base64 格式

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

將 UTexture2D 儲存為 .png 檔案

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

將 .png 檔案載入至 UTexture2D：讀取 png 檔案為 UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Duplicate UTexture2D": 複製 UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###音頻相關

將 .wav 檔案載入至 USoundWave：加载 .wav 文件到 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

將 .wav 數據轉換為 USoundWave：將 wav 二進制數據轉換為 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

將 USoundWave 保存為 .wav 檔案

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

獲取 USoundWave 原始 PCM 數據：轉換 USoundWave 為原始 PCM 數據

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

將 USoundWave 轉換為 Base64 格式

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicate USoundWave": 複製 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

將音訊捕捉資料轉換為 USoundWave：將音訊捕捉資料轉換成 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

--8<-- "footer_tc.md"


> 此貼文是由 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出一切遺漏之處。 
