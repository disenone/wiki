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

#設計図部分 - アズール

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_all.png)

Azureの使用方法はOpenAIと非常に類似しているため、ここでは簡単に説明します。

##テキストチャット

"Azure Chat Options" ノードを作成し、"Deployment Name"、"Base Url"、"Api Key" のパラメータを設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_chat_1.png)

"Messages" ノードを作成し、"Azure Chat Request" に接続して、実行をクリックすると、Azure から返されたチャット情報が画面に印刷されます。場合によっては画像を参照してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

##画像を作成します。

"Azure Image Options" ノードを作成し、"Deployment Name"、"Base Url"、"Api Key" のパラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_image_1.png)

"Azure Image Request" ノードなどを設定し、実行ボタンをクリックすると、画面に Azure から返されたチャット情報が表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

上記の設定に基づくと、画像はパス D:\Downloads\butterfly.png に保存されます。

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)指摘していただいた漏れがあればどうぞ。 
