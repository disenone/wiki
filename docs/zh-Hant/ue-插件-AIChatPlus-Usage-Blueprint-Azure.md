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

#藍圖篇 - Azure

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_all.png)

Azure 的使用方式與 OpenAI 非常相似，因此這裡簡單介紹一下。

##文字聊天

建立 "Azure Chat Options" 節點，設定參數 "Deployment Name", "Base Url", "Api Key"

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_chat_1.png)

建立 "消息" 相關節點，並連接 "Azure 聊天請求"，點擊執行，即可在螢幕上看到列印出來的 Azure 回傳的聊天訊息。如圖。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

##建立圖片

建立 "Azure Image Options" 節點，設定 "Deployment Name"、 "Base Url" 和 "Api Key" 參數。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_image_1.png)

設置好 "Azure Image Request" 等節點，點擊運行，即可看到螢幕上打印 Azure 返回的聊天信息。如圖。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

根據上述藍圖設置，圖片將保存在路徑 D:\Dwnloads\butterfly.png。

--8<-- "footer_tc.md"


> 這篇文章是由 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)請指出任何遺漏之處。 
