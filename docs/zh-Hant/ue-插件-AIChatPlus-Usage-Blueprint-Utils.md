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

插件額外提供了一些便利的藍圖功能節點。

##Cllama 相關

"Cllama Is Valid": 判斷 Cllama llama.cpp 是否正確初始化

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu"：判斷 llama.cpp 在目前環境下是否支持 GPU 後端。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

獲取目前llama.cpp支援的所有後端。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama 在 Pak 中准备模型文件": 自動將 Pak 中的模型文件複製到檔案系統中

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

##圖像相關

將 UTexture2D 轉換為 Base64：將 UTexture2D 圖像轉換為 PNG Base64 格式。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

將 UTexture2D 儲存為 .png 檔案。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

將 .png 檔案載入至 UTexture2D：讀取 png 檔案為 UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Duplicate UTexture2D": 複製 UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

##音頻相關

將.wav檔案加載到USoundWave: 將.wav檔案加載到USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

將.wav數據轉換成USoundWave：把wav二進制數據轉換成USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

將 USoundWave 存為 .wav 檔案

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

將 USoundWave 轉換為原始 PCM 資料

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

將USoundWave轉換為Base64：將USoundWave轉換為Base64資料

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicate USoundWave": 複製 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

將音頻擷取資料轉換為 USoundWave：將音頻擷取資料轉換為 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

--8<-- "footer_tc.md"


> 這篇帖文是由 ChatGPT 翻譯而來的，敬請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
