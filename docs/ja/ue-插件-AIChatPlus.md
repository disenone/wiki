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

#UEプラグインAIChatPlusの説明書

##プラグインストア

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##公共倉庫

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##プラグイン紹介

最新バージョンはv1.6.0です。

このプラグインはUE5.2からUE5.5をサポートしています。

UE.AIChatPlus は UnrealEngine プラグインで、さまざまな GPT AI チャットサービスとの通信を実現しています。現在サポートされているサービスは OpenAI（ChatGPT、DALL-E）、Azure OpenAI（ChatGPT、DALL-E）、Claude、Google Gemini、Ollama、llama.cpp のローカルオフラインです。将来的にはさらに多くのサービスプロバイダーをサポートする予定です。実装は非同期の REST リクエストに基づいており、性能が高く、UE 開発者がこれらのAIチャットサービスにアクセスしやすくなっています。

UE.AIChatPlusにはエディターツールも含まれており、このツールを使用すると、AIチャットサービスを直接エディターで利用してテキストや画像を生成し、画像を分析することができます。

##主要機能

**新登場！** オフライン AI llama.cpp がバージョン b4604 にアップグレードされました。

新しい！オフラインAI llama.cppは、GPUのCudaとMetalをサポートしています。

新発売！Geminiの音声からテキストへの変換に対応。

**API**: OpenAI、Azure OpenAI、Claude、Gemini、Ollama、llama.cpp、DeepSeek をサポート

オフラインリアルタイムAPI：llama.cppのオフラインでのAI実行をサポートし、GPUのCudaとMetalをサポートします。

このテキストは、日本語に翻訳されました：

**文本转文本**：さまざまなAPIがテキスト生成をサポートしています。

**テキストから画像への変換**：OpenAI Dall-E

**画像からテキストへの変換**：OpenAI Vision、Claude、Gemini、Ollama、llama.cpp

画像から画像へ：OpenAIのDALL-E

**音声テキスト変換**：ジェミニ

**設計図**: すべてのAPIと機能は設計図をサポートしています。

**Editor Chat Tool**: A feature-rich, carefully crafted editor AI chat tool.

「非同期呼び出し」：すべての API は非同期で呼び出すことができます

**実用ツール**：さまざまな画像、音声ツール

##サポートされている API：

**オフライン llama.cpp**：llama.cppライブラリと統合して、AIモデルをオフラインで実行できます！さらに、マルチモードモデル（実験的）もサポートしています。Win64/Mac/Android/IOSをサポートしています。GPU CUDAとMETALにも対応しています。

**OpenAI**：/chat/completions、/completions、/images/generations、/images/edits、/images/variations

**Azure OpenAI**: /chat/completions、/images/generations

**クロード**：/メッセージ、/完了

**ジェミニ**：generateText、generateContent、streamGenerateContent

**Ollama**：/api/chat、/api/generate、/api/tags

**DeepSeek**：/chat/completions

##ご使用案内

[**Instructions for Use - Blueprint Section**](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

(ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

(ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

[**Instructions for use - Packing**](ue-插件-AIChatPlus-Usage-Package-GetStarted.md)

##変更履歴

(ue-插件-AIChatPlus-ChangeLogs.md)

##技術サポート

「コメント」：何か質問があれば、下記のコメント欄にメッセージを残してください。

"メール：または私にメールを送ることもできます（disenonec@gmail.com）"

**discord**: 即将上線

--8<-- "footer_ja.md"


> この投稿はChatGPTを使って翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)指定されたテキストを日本語に翻訳します:

どんな遺漏も指摘してください。 
