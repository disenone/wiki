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

#設計図 - はじめの一歩

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

## Get Started

OpenAIを例にとって、ブループリントの基本的な使用方法を紹介します。

###テキストチャット

OpenAIを使用してテキストチャットを行う

設計図で「Send OpenAI Chat Request In World」というノードを右クリックして作成します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Options ノードを作成し、`Stream=true, Api Key="you api key from OpenAI"` を設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Messages を作成し、System Message と User Message をそれぞれ追加します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

モデルの出力情報を受け取り、それを画面に表示する Delegate を作成する。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完璧な設計図はこう見える。この設計図を実行すると、ゲーム画面に大きなモデルが印刷されたメッセージが表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###テキストを日本語に翻訳してください：

本文生成画像

OpenAIを使用して画像を作成します。

設計図で右クリックしてノード「Send OpenAI Image Request」を作成し、「In Prompt="a beautiful butterfly"」を設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Options ノードを作成し、`Api Key="OpenAI からのあなたの API キー"` を設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

画像のOn Imagesイベントをバインドして、画像をローカルディスクに保存します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

完全な設計図はこう見える。設計図を実行すると、指定された場所に画像が保存されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

###画像をテキスト化

OpenAI Vision 画像解析を使用します。

青写真で、`Send OpenAI Image Request` ノードを右クリックして作成します。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_1.png)

Options ノードを作成し、`Api Key="OpenAI から提供されたあなたの API キー"` を設定し、モデルを `gpt-4o-mini` に設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_2.png)

メッセージを作成します。
ファイルシステムから画像を読み込むための「Import File as Texture 2D」というノードを作成してください。
ノード「Create AIChatPlus Texture From Texture2D」を使用して、画像をプラグインで使用可能なオブジェクトに変換します。
"Make Array" ノードを使用して、画像をノード "AIChatPlus_ChatRequestMessage" の "Images" フィールドに接続します。
"Content" フィールドの内容を "この画像を説明する" に設定してください。

図をご覧ください：

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_3.png)

完整な設計図はこのように見えます。設計図を実行すると、結果が画面上に表示されます。 

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_4.png)

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されましたので、[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)指摘された箇所は遺漏なきようご指摘ください。 
