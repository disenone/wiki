---
layout: post
title: Get Started
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
description: Get Started
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Get Started" />

#藍圖篇 - 開始動工

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

## Get Started

以下以 OpenAI 為例，介紹藍圖的基本使用方法。

###文字訊息溝通

使用 OpenAI 進行文字聊天

在藍圖中右鍵創建一個節點 `Send OpenAI Chat Request In World`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

創建 Options 節點，並設置 `Stream=true, Api Key="您從 OpenAI 獲取的 API 金鑰"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

建立訊息，分別新增一條系統訊息和使用者訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

建立Delegate來接收模型輸出的資訊，並將其列印在螢幕上。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完整的藍圖長得像這樣，執行藍圖後，你會看到遊戲屏幕打印出返回的大型模型訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###This text content cannot be translated.

使用 OpenAI 創建圖片

在藍圖中右鍵創建一個節點 `Send OpenAI Image Request`，並設置 `In Prompt="a beautiful butterfly"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

建立 Options 節點，並設置 `Api Key="來自 OpenAI 的您的 API 金鑰"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

為圖片綁定事件，並將圖片保存至本地硬碟。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

完整的藍圖看起來是這樣的，運行藍圖，即可看到圖片保存在指定的位置上。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

###圖片生成文字

使用 OpenAI Vision 分析圖片

在藍圖中右鍵創建一個節點 `Send OpenAI Image Request`

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_1.png)

建立 Options 节点，並將 `Api Key="your api key from OpenAI"` 設置，模型設定為 `gpt-4o-mini`

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_2.png)

建立訊息。
請先建立"從檔案導入作為 2D 紋理"節點，從檔案系統中讀取一張圖片。
通過節點 "Create AIChatPlus Texture From Texture2D" 將圖片轉換為插件可用的物件；
將圖片通過「Make Array」節點連接到節點「AIChatPlus_ChatRequestMessage」的「Images」字段。
將「內容」欄位設置為「描述這幅圖像」。

如圖：

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_3.png)

完整的藍圖看起來是這樣的，運行藍圖，即可看到結果顯示在螢幕上。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_4.png)

--8<-- "footer_tc.md"


> 此篇文章是用ChatGPT翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
