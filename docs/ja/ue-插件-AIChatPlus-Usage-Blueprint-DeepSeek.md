---
layout: post
title: DeepSeek
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
description: DeepSeek
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - DeepSeek" />

#設計図部分 - DeepSeek

DeepSeekはOpenAIのAPIインターフェース形式と互換性があるため、DeepSeekにアクセスするには関連するURLをDeepSeekのURLに変更するだけで簡単にOpenAIの関連ノードにアクセスできます。

#テキストチャット

"OpenAI Chat Options" ノードを作成し、Model、Url、Api Key パラメータを設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/deepseek_chat_1.png)

他の設定はOpenAIと同じです。完全な設計図は次のようになります：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

DeepSeekの返戻を画面でご確認いただけます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

--8<-- "footer_ja.md"


> この投稿はChatGPTによって翻訳されましたので、[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
指摘して誤りを見逃さないでください。 
