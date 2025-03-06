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

#青写真 - OpenAI

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_all.png)

[はじめる](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)OpenAIの基本的な使い方はすでに章で紹介しましたが、ここではより詳細な使用方法を説明します。

##テキストチャット

OpenAIを使用してテキストチャットを行う

設計図内でノードを作成するには、「Send OpenAI Chat Request In World」と名付けます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Options ノードを作成し、`Stream=true, Api Key="あなたのOpenAIからのAPIキー"` を設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Messagesを作成し、System MessageとUser Messageをそれぞれ追加してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Delegateを作成し、モデルの出力情報を受け取り、それを画面に表示します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

詳細な計画図はこういうものです。 この計画図を実行すると、ゲーム画面に大きなモデルが返されたメッセージが表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

##テキストを日本語に翻訳している間にエラーが発生しました.

OpenAI を使用して画像を作成します。

青写真の中で、`Send OpenAI Image Request` というノードを右クリックして作成し、`In Prompt="a beautiful butterfly"` を設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Options ノードを作成し、`Api Key="OpenAI からの API キー"` を設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

画像の On Images イベントをバインドし、画像をローカルディスクに保存します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

完全な設計図は、このように見えます。 設計図を実行すると、画像が指定された場所に保存されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

##画像をテキストに変換します。

OpenAI Vision を使用して画像を分析します。

ブループリント内で、ノードを右クリックして `Send OpenAI Image Request` を作成してください。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_1.png)

Options ノードを作成し、`Api Key="you api key from OpenAI"` を設定し、モデルを `gpt-4o-mini` に設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_2.png)

メッセージを作成してください。
ファイルシステムから画像を読み込むためのノード「Import File as Texture 2D」を作成してください。
"Create AIChatPlus Texture From Texture2D" ノードを使用して、画像をプラグインで使用できるオブジェクトに変換します。
「'Make Array' ノードを使用して、画像をノード 'AIChatPlus_ChatRequestMessage' の 'Images' フィールドに接続します。」
"Content"フィールドの内容を「この画像を説明する」に設定します。

図に示す通り：

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_3.png)

完整な設計図はこのように見えます。設計図を実行すると、結果が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_4.png)

##画像を編集します。

OpenAIは画像の領域を変更することをサポートしています。

最初に、2枚の画像を準備してください。

修正が必要な画像は、src.pngです。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_1.png)

修正が必要な領域を示した mask.png という画像が1枚あります。この画像を修正して、修正領域の透明度を0に設定します。つまり、アルファチャンネルの値を0に変更します。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_2.png)

上記の2枚の写真をそれぞれ見て、配列に組み合わせます。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_3.png)

"OpenAI Image Options" ノードを作成し、ChatType = Edit に設定し、"End Point Url" = v1/images/edits に変更してください。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_4.png)

「OpenAI Image Request」を作成し、「Prompt」を「change into two butterfly」に設定し、 「Options」ノードと画像配列を接続し、生成された画像をファイルシステムに保存します。

完璧な設計図はこのように見えます：

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_5.png)

ブループリントを実行して生成された画像を指定された場所に保存します。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_6.png)

##画像変種

OpenAIは、入力された画像に基づいて類似の変種（Variation）を生成することをサポートしています。

ます。最初に、画像 src.png を用意して、ブループリントで読み込んでください。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_1.png)

「OpenAI Image Options」ノードを作成し、ChatTypeをVariationに設定し、「End Point Url」をv1/images/variationsに変更してください。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_2.png)

"OpenAI Image Request"を作成し、「Prompt」を空白のままにして、「Options」ノードと画像を接続して、生成された画像をファイルシステムに保存します。

完璧な設計図はこう見える：

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_3.png)

ブループリントを実行し、生成された画像を指定された場所に保存します。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_4.png)

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されています。[**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Please point out any omissions. 
