---
layout: post
title: Claude
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
description: Claude
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Claude" />

#設計図パート - クロード

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/claude_all.png)

##テキストチャット

"Options" ノードを作成し、"Model"、"Api Key"、"Anthropic Version" のパラメータを設定してください。

![](assets/img/2024-ue-aichatplus/usage/blueprint/claude_chat_1.png)

"クロード・リクエスト"ノードと "メッセージ"関連ノードを接続し、実行をクリックすると、画面にクロードが返信したチャット情報が表示されます。画像の通りです。

![](assets/img/2024-ue-aichatplus/usage/blueprint/claude_chat_2.png)

##画像をテキスト化します。

クロードは Vision 機能も同様にサポートしています。

ブループリントで、「Send Claude Chat Request」というノードを右クリックして作成してください。

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Optionsノードを作成し、 `Stream=true、Api Key="CludeからのあなたのAPIキー"、Max Output Tokens=1024` を設定します。

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Messages を作成し、ファイルから Texture2D を作成し、その Texture2D から AIChatPlusTexture を作成し、AIChatPlusTexture を Message に追加します。

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

イベントを実行し、情報をゲーム画面に表示します。

完璧な設計図はこういったものです。設計図を実行すると、ゲーム画面に大きなモデルが印刷されたメッセージが表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)


--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されています。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出遺漏之部分。 
