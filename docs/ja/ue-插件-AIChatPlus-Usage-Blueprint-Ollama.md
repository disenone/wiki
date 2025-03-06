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

#*Blueprint Part - Ollama*

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_all.png)

##「Ollama 取得」

Ollama公式サイトからインストーラーを取得して、ローカルにインストールすることができます：[ollama.com](https://ollama.com/)

他人が提供するOllama APIインタフェースを使用して、Ollamaを利用できます。

ローカルでOllamaを使用してモデルをダウンロード：

```shell
> ollama run qwen:latest
> ollama run moondream:latest
```

##テキストチャット

"Ollama Options" ノードを作成し、"Model"、"Base Url" パラメータを設定します。Ollama がローカルで実行されている場合、"Base Url" は通常 "http://localhost:11434" になります。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_chat_1.png)

"Ollama Request" ノードと "Messages" 関連ノードを接続し、実行をクリックすると、Ollama が返信したチャット情報が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

##そのテキストを日本語に翻訳します: 

画像生成テキスト llava

Ollama also supports the llava library, providing the ability of Vision.

まずは、Multimodalモデルファイルを取得してください：

```shell
> ollama run moondream:latest
```

"Options" ノードを設定し、"Model" を moondream:latest に設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_1.png)

画像 flower.png を読み込んで、メッセージを設定してください。

![flower.png](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_3.png)

「Ollama Request」ノードに接続し、実行をクリックすると、画面にOllamaから返されたチャット情報が表示されます。画像を参照ください。

![](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_4.png)

![](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_5.png)

--8<-- "footer_ja.md"


> この投稿はChatGPTによって翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 -> どこか見落としている箇所があれば指摘してください。 
