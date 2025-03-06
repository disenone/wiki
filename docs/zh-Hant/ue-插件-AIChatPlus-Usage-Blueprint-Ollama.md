---
layout: post
title: Ollama
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
description: Ollama
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Ollama" />

#藍圖篇 - Ollama

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_all.png)

##獲取 Ollama

您可前往Ollama官方網站下載安裝程式進行本地安裝：[ollama.com](https://ollama.com/)

您可以利用其他人提供的 Ollama API 接口来使用 Ollama。

使用本地檢索Ollama下載模型:

```shell
> ollama run qwen:latest
> ollama run moondream:latest
```

##文字聊天

建立 "Ollama Options" 節點，設定 "Model"、"Base Url" 參數，若是在本機執行 Ollama，通常 "Base Url" 為 "http://localhost:11434"。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_chat_1.png)

連接 "Ollama Request" 節點 和 "Messages" 相關節點，點擊運行，即可看到屏幕上打印 Ollama 返回的聊天信息。如圖

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

##圖片生成文字 llava

Ollama 同樣支持了 llava 庫，提供了 Vision 的能力。

首先取得 Multimodal 模型檔案：

```shell
> ollama run moondream:latest
```

設置 "Options" 節點，"Model" 設置為 moondream:latest

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_1.png)

讀取圖片 flower.png，並設置消息

![flower.png](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_3.png)

連接 "Ollama Request" 節點，點擊運行，即可在螢幕上看到 Ollama 返回的聊天信息。

![](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_4.png)

![](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_5.png)

--8<-- "footer_tc.md"


> 這篇貼文是透過 ChatGPT 翻譯的，請在 [**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
