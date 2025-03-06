---
layout: post
title: OpenAI
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
description: OpenAI
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - OpenAI" />

#藍圖篇 - OpenAI

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_all.png)

在 [開始](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)這些部分已經介紹過 OpenAI 的基本用法，我們在這裡再提供詳細的用法。

##文字聊天

使用 OpenAI 進行文本聊天

在藍圖中按右鍵建立一個節點 `在世界中發送 OpenAI 聊天請求`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

建立 Options 節點，並設置 `Stream=true, Api Key="來自 OpenAI 的 API 金鑰"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

建立 Messages，分別新增一條 System Message 和 User Message

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

建立 Delegate 接收模型輸出的資訊，並在螢幕上列印出來。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完整的藍圖看起來是這樣的，運行藍圖，即可看到遊戲螢幕在列印大模型返回的訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

##本文生成圖片

使用 OpenAI 創建圖片

在藍圖中右鍵建立一個節點 `Send OpenAI Image Request`，並設定 `In Prompt="a beautiful butterfly"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

建立 Options 节点，並設定 `Api Key="you api key from OpenAI"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

為圖像添加事件綁定，並將圖片保存到本地硬碟。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

完整的藍圖看起來是這樣的，運行藍圖，即可看到圖片保存在指定的位置上。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

##圖片轉文字

使用 OpenAI Vision 分析圖片

在藍圖中按右鍵建立一个節點 `Send OpenAI Image Request`

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_1.png)

建立 Options 节点，並設置 `Api Key="you api key from OpenAI"`，設置模型為 `gpt-4o-mini`

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_2.png)

建立訊息。
首先建立一個名為「將文件導入為 2D 紋理」的節點，從檔案系統中讀取一張圖片；
通過節點「從Texture2D創建AIChatPlus紋理」將圖片轉換為插件可用的物件；
通過 "Make Array" 節點將圖片連接到節點 "AIChatPlus_ChatRequestMessage" 的 "Images" 欄位上；
將"Content"欄位設置為"描述此圖片"。

請參考以下圖片：

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_3.png)

完整的藍圖看起來就像這樣，運行藍圖，便可在螢幕上看到結果顯示。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_4.png)

##修改圖片

OpenAI支持對圖片標記的區域進行修改。

請準備兩張圖片。

需要修改的圖片為 src.png。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_1.png)

一張是把需要修改的區域標記出來的圖片 mask.png，可以通過修改源圖片，把修改區域的透明度設置成 0，即 Alpha 通道數值改成 0。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_2.png)

讀取那兩張照片，並組合成陣列。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_3.png)

建立「OpenAI圖像選項」節點，設定ChatType = 編輯，並修改「端點網址」= v1/images/edits

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_4.png)

建立 "OpenAI Image Request"，將 "Prompt" 設置為 "變成兩只蝴蝶"，連接到 "Options" 節點和圖片陣列，然後將生成的圖片保存到檔案系統中。

完整的藍圖看起來是這樣的：

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_5.png)

執行藍圖，生成的圖片將保存在指定位置上。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_6.png)

##圖片變種

OpenAI 支援根據輸入的圖片生成類似的變異 (Variation)。

首先請準備一張名為 src.png 的圖片，並在藍圖中將其讀取進來。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_1.png)

建立"OpenAI Image Options"節點，將 ChatType 設置為 Variation，並修改"End Point Url"為 v1/images/variations。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_2.png)

建立"OpenAI Image Request"，將"Prompt"保留為空，連接至"Options"節點和圖片，並將生成的圖片儲存至檔案系統中。

完整的藍圖看起來是這樣的：

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_3.png)

執行藍圖，將生成的圖片保存在指定位置上。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_4.png)

--8<-- "footer_tc.md"


> 這篇文章是由 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
