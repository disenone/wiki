---
layout: post
title: Gemini
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
description: Gemini
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Gemini" />

#藍圖篇 - 雙子座

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_all.png)

###文字聊天

建立 "雙子聊天選項" 節點，並設置參數 "Model"、"Api Key"。

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_chat_1.png)

建立 "雙子 Chat Request" 節點，再將其連接至 "選項" 和 "訊息" 節點，點擊運行，您將能夠在屏幕上看到打印出來的 Gemini 聊天訊息，如示：

![](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###圖片轉文字

建立一個 "Gemini Chat Options" 節點，並設置 "Model"、"Api Key" 參數。

從檔案讀取圖片 flower.png，並設定到「Messages」上。

![flower.png](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_vision_1.png)

建立 "Gemini Chat Request" 節點，點選執行，即可在螢幕上看到 Gemini 回傳的聊天資訊，如下圖所示：

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_vision_2.png)

###音頻轉文字

雙子座支援將音訊轉換為文字。

建立以下藍圖，設定加載音頻，設置好 Gemini 選項，點擊運行，即可看到螢幕上列印 Gemini 處理音頻後返回的聊天訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

--8<-- "footer_tc.md"


> 這篇文章是由 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
