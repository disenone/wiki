---
layout: post
title: バージョン履歴
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
description: バージョン履歴
---

<meta property="og:title" content="UE 插件 AIChatPlus 版本日志" />

#UEプラグインAIChatPlusのバージョンログ

## v1.6.1 - 2025.03.07

### Bug Fix

OpenAI Image Chatの計画に、画像の入力がサポートされています。

エディターツールCllama mmprojはモデルの空を認めます。

## v1.6.0 - 2025.03.02

###新機能

llama.cpp を b4604 バージョンにアップグレードします。

Cllamaは、GPUバックエンドでcudaとmetalをサポートしています。

チャットツールCllamaはGPUの使用をサポートしています。

Pak 中にあるモデルファイルを読み込んでパッケージをサポートします。

### Bug Fix

推論時にCllamaがリロードするとクラッシュする問題を修正しました。

iOSのコンパイルエラーを修正します。

## v1.5.1 - 2025.01.30

###新機能

Geminiだけが音声を送信できます。

PCMDataを取得する方法を最適化し、音声データをB64に変換する際にデータを展開するように変更されました。

要求增加两个回調 OnMessageFinished 和 OnImagesFinished。

Geminiメソッドを最適化し、bStreamに基づいて自動的にメソッドを取得します。

いくつかのブループリント関数を追加し、Wrapperを実際のタイプに変換し、レスポンスメッセージとエラーを取得できるようにします。

### Bug Fix

* 修复リクエスト終了の複数回呼び出しの問題

## v1.5.0 - 2025.01.29

###新機能

ジェミニにオーディオファイルをサポートします。

エディターツールはオーディオと録音の送信をサポートしています。

### Bug Fix

セッションコピーが失敗するバグを修正します。

## v1.4.1 - 2025.01.04

###問題の修正

チャットツールが画像のみ送信できる機能をサポートしています。

OpenAI のインターフェイスで画像を送信する問題の修正に失敗しました。

OpenAIやAzureのチャットツールの設定で見落とされたQuality、Style、ApiVersionのパラメータの問題を修正する。

## v1.4.0 - 2024.12.30

###新しい機能

* （実験的機能）Cllama(llama.cpp) は、マルチモードモデルをサポートし、画像を処理できます。

すべてのブループリントタイプのパラメータには、詳細なヒントが追加されました。

## v1.3.4 - 2024.12.05

###新機能

OpenAIはVision APIをサポートしています。

###問題修復

OpenAI stream=falseのエラーを修正します。

## v1.3.3 - 2024.11.25

###新機能

サポート対象：UE-5.5

###問題修復

一部の設計図の有効化が正常に行われない問題を修正します。

## v1.3.2 - 2024.10.10

###問題修復

手動停止リクエスト時の cllama クラッシュを修正します。

商城のダウンロードバージョンwinパッケージでggml.dll llama.dllファイルが見つからない問題を修正します。

GameThread で CreateRequest をチェックする、リクエスト作成時の検証

## v1.3.1 - 2024.9.30

###新しい機能

* 「SystemTemplateViewer」というものを追加しました。数百種類のシステム設定テンプレートを閲覧および使用できます。

###問題が修正されました。

商城からダウンロードしたプラグイン、llama.cppがリンクライブラリを見つけられません

LLAMACppパスが長すぎる問題を修正

Windows パッケージング後の llama.dll 関連の問題を修正します。

iOSおよびAndroidのファイルパスの読み取り問題を修正します。

Cllameの設定名が誤っている修正

## v1.3.0 - 2024.9.23

###重要な新機能

* 「llama.cpp」を統合し、大規模なモデルのローカルオフライン実行をサポートするようにしました。

## v1.2.0 - 2024.08.20

###新機能

OpenAI Image Edit/Image Variation のサポート

Ollama APIをサポートし、Ollamaがサポートするモデルリストを自動取得する機能もサポートしています。

## v1.1.0 - 2024.08.07

###新しい機能

支持蓝图

## v1.0.0 - 2024.08.05

###新機能

基礎完全機能

OpenAI、Azure、Claude、Gemini をサポートします。

組み込み機能を備えた優れたエディター付きチャットツール

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
