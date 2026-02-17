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

#UEプラグイン AIChatPlus 説明書

##プラグインストア

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##公共倉庫

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##プラグイン概要

最新バージョン v2.0.0。

本プラグインはUE5.2からUE5.7をサポートしています。

UE.AIChatPlus は UnrealEngine プラグインで、さまざまな GPT AI チャットサービスとの通信を実現します。現在サポートしているサービスは OpenAI (ChatGPT, DALL-E)、Azure OpenAI (ChatGPT, DALL-E)、Claude、Google Gemini、Ollama、llama.cpp ローカルオフライン版です。今後もさらに多くのサービスプロバイダーをサポートする予定です。非同期 REST リクエストを基に実装されており、パフォーマンスが高く、UE 開発者がこれらの AI チャットサービスに簡単に接続できるよう設計されています。

同時に、UE.AIChatPlusにはエディターツールも含まれており、これらのAIチャットサービスを直接エディター内で利用して、テキストや画像を生成したり、画像を分析したりすることが可能です。

##主な機能

**新機能！**すべての API が ToolCall をサポート。

**新登場！**OpenAI/Azureが音声テキスト化とテキスト音声化をサポート。

**新登場！** 設計図がJsonに対応しました。

**新規！**オフラインAI llama.cppがバージョンb6792にアップグレードされました。

**新発売！**オフラインAI llama.cppがGPU CudaとMetalに対応しました。

**新登場！**Gemini による音声文字変換をサポート。

**API**：OpenAI、Azure OpenAI、Claude、Gemini、Ollama、llama.cpp、DeepSeek をサポート

**オフラインリアルタイム API**：llama.cpp を使用したAIのオフライン実行をサポートし、GPU CudaおよびMetalに対応しています。

**テキストからテキストへ**: 様々なAPIがテキスト生成をサポートします。

**テキストから画像へ**：OpenAI Dall-E

**画像からテキストへ**：OpenAI Vision、Claude、Gemini、Ollama、llama.cpp

**画像から画像へ**：OpenAI Dall-E

**音声からテキストへ**：Gemini

**ブループリント**: すべてのAPIと機能はブループリントに対応しています

**エディターチャットツール**：機能豊富で洗練されたエディター AI チャットツール

**非同期呼び出し**：すべてのAPIは非同期で呼び出すことができます

**便利ツール**：さまざまな画像・音声ツール

##サポートされているAPI：

**オフライン llama.cpp**：llama.cpp ライブラリと統合され、オフラインで AI モデルを実行可能！実験的ではありますが、マルチモーダルモデルもサポートしています。Win64/Mac/Android/IOS に対応。GPU CUDA および METAL にも対応。

**OpenAI**：/chat/completions、/completions、/images/generations、/images/edits、/images/variations

**Azure OpenAI**:/チャット/コンプリート、/画像/ジェネレーション

**Claude**：/messages、/complete

**ジェミニ**：:generateText、:generateContent、:streamGenerateContent

**Ollama**：/api/chat、/api/generate、/api/tags

**DeepSeek**：/chat/completions  
（注：此处英文专有名词“DeepSeek”和API路径“/chat/completions”通常保留原样，日语环境中直接使用。若需全译可作「ディープシーク」）

##取扱説明書

[**使い方 - ブループリント編**](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

[**使用説明 - C++ 編**](ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

[**使い方 - エディター篇**](ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

[**使い方 - パッケージング**](ue-插件-AIChatPlus-Usage-Package-GetStarted.md)

##変更履歴

[**変更履歴**](ue-插件-AIChatPlus-ChangeLogs.md)

##テクニカルサポート

**コメント**：ご質問がございましたら、下記のコメント欄にどうぞ

**メール**：メールでも連絡できます（disenonec@gmail.com）

**discord**: 近日公開予定

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されたものです。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)以下の点で不備を指摘する。 
