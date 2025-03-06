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

#設計図 - ジェミニ

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_all.png)

###テキストチャット

"ジェミニ チャットオプション" ノードを作成し、"Model"、 "Api Key" のパラメータを設定します。

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_chat_1.png)

"Gemini Chat Request" ノードを作成し、「Options」と「Messages」ノードに接続した後、実行をクリックしてください。そうすれば、画面に Gemini から返されたチャット情報が表示されます。よろしく。

![](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###画像をテキストに変換します。

"Gemini Chat Options" ノードを作成し、"Model"、"Api Key" パラメータを設定してください。

画像 flower.png をファイルから読み込んで、「Messages」に設定します。

![flower.png](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_vision_1.png)

「Gemini Chat Request」ノードを作成し、実行をクリックすると、画面にGeminiから返されたチャット情報が印刷されます。

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_vision_2.png)

###音声をテキストに変換

ジェミニは、音声をテキストに変換することをサポートしています。

以下の手順に従ってブループリントを作成し、音声ファイルを読み込み、Gemini Optionsを適切に設定します。その後、「実行」ボタンをクリックして、Geminiが音声を処理して返信したチャット情報が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

--8<-- "footer_ja.md"


> この投稿はChatGPTによって翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
