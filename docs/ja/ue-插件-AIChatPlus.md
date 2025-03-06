---
layout: post
title: 説明書
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
description: 説明書
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE プラグイン AIChatPlus 説明書

##プラグインストア

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##公共倉庫

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##プラグインの紹介

最新バージョンv1.6.0。

このプラグインはUE5.2からUE5.5をサポートしています。

UE.AIChatPlus は、Unreal Engine のプラグインであり、様々な GPT AI チャットサービスとの通信を実現しています。現在サポートされているサービスは、OpenAI（ChatGPT、DALL-E）、Azure OpenAI（ChatGPT、DALL-E）、Claude、Google Gemini、Ollama、llama.cpp、そしてローカルオフラインです。将来的にはさらに多くのサービスプロバイダーをサポートする予定です。この実装は非同期の REST リクエストに基づいており、パフォーマンスが高く、UE 開発者がこれらのAIチャットサービスに簡単にアクセスできるようになっています。

UE.AIChatPlusには、エディタツールも含まれており、このツールを使用してAIチャットサービスを直接エディタ内で利用し、テキストや画像を生成したり、画像を分析したりすることができます。

##主要な機能

**Brand new!** オフラインAI llama.cpp がバージョンb4604にアップグレードされました。

新しい！オフラインAI llama.cppはGPUのCudaとMetalをサポートしています。

新着！Geminiの音声からテキストへの変換をサポートしています。

**API**：OpenAI、Azure OpenAI、Claude、Gemini、Ollama、llama.cpp、DeepSeek をサポート

**オフラインリアルタイムAPI**：llama.cppのオフライン実行AIをサポートし、GPUのCudaとMetalに対応しています。

これらのテキストを日本語に翻訳してください：

**Text to text**：さまざまなAPIがテキスト生成をサポートしています。

**Text Translation**: OpenAI DALL-E

**画像をテキストに変換する**：OpenAI Vision、Claude、Gemini、Ollama、llama.cpp

**画像から画像へ**：OpenAI DALL-E

**音声テキスト変換**：ジェミニ

**設計図**：すべてのAPIと機能が設計図をサポートしています。

**Editor Chat Tool**: A feature-rich, meticulously crafted editor AI chat tool.

非同期呼び出し：すべてのAPIは非同期で呼び出すことができます。

**実用ツール**：さまざまな画像、音声ツール

##APIサポート：

**オフライン llama.cpp**：llama.cppライブラリと統合してAIモデルをオフラインで実行できます！実験的に、マルチモードモデルもサポートされます。Win64/Mac/Android/IOSをサポートしています。GPU CUDAとMETALをサポートしています。

OpenAI：/chat/completions、/completions、/images/generations、/images/edits、/images/variations

**Azure OpenAI**: /chat/completions、/images/generations

**クロード**：/メッセージ、/完了

**Gemini**：generateText、generateContent、streamGenerateContent

**Ollama**：/api/chat、/api/generate、/api/tags

**DeepSeek**：/chat/completions

##使用説明

(ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

[**Instructions for Use - C++ Chapter**](ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

[**Instructions for Use - Editor Section**](ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

##変更ログ

(ue-插件-AIChatPlus-ChangeLogs.md)

##技術サポート

「コメント」：何か質問があれば、以下のコメント欄にメッセージを残してください。

"Email: または電子メールで私にメッセージを送ることもできます (disenonec@gmail.com)"

**discord**: Coming soon.

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)どんなミスでも指摘してください。 
