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

## v1.6.0 - 2025.03.02

###新機能

lama.cpp ファイルを b4604 バージョンにアップグレードします。

CllamaはGPUバックエンドをサポートしています：cudaとmetal.

チャットツール Cllama は GPU の使用をサポートしています。

Pak ファイル内のモデルファイルの読み込みをサポートします。

### Bug Fix

ロジックの推論中に Cllama の再読み込み時にクラッシュする問題を修正しました。

iOSのコンパイルエラーを修正します。

## v1.5.1 - 2025.01.30

###新機能

Gemini だけが音声を送信することが許可されています。

PCMData の取得方法を最適化し、音声データを再度圧縮して B64 を生成するようにします。

リクエストをして、OnMessageFinishedとOnImagesFinishedの2つのコールバックを追加してください。

ジェミニメソッドを最適化し、bStreamに応じて自動的にメソッドを取得します。

一部分のブループリント機能を追加して、Wrapperを実際のタイプに変換し、レスポンスメッセージとエラーを取得しやすくしました。

### Bug Fix

リクエストの完了に関する問題を複数回呼び出す修正

## v1.5.0 - 2025.01.29

###新機能

ジェミニに音声を送る支援

エディターツールは、音声や録音の送信をサポートしています。

### Bug Fix

セッションコピーの失敗バグを修正

## v1.4.1 - 2025.01.04

###問題修正

チャットツールは画像のみ送信できますが、テキストは送信できません。

OpenAIインターフェイス経由の画像送信問題の修正に失敗しました。

OpenAIやAzureのチャットツール設定でQuality、Style、ApiVersionのパラメータが抜けている問題を修正する=

## v1.4.0 - 2024.12.30

###新機能

（実験的機能）Cllama(llama.cpp)は複数のモードモデルをサポートし、画像を処理できます。

すべてのブループリントタイプのパラメータには詳細なヒントが追加されています。

## v1.3.4 - 2024.12.05

###新機能

OpenAIはVision APIをサポートしています。

###問題修復

OpenAI stream=falseのエラーを修正する

## v1.3.3 - 2024.11.25

###新機能

* Supports UE-5.5

###問題修復

一部の設計図が機能しない問題を修復します。

## v1.3.2 - 2024.10.10

###問題修復

* 手動停止要求時の cllama クラッシュ時の修復

商店のダウンロードバージョンwinのパッケージでggml.dll llama.dllファイルが見つからない問題を修正します。

* 创建请求时检查是否在 GameThread 中，CreateRequest check in game thread
* ゲームスレッド内で CreateRequest をチェックします。

## v1.3.1 - 2024.9.30

###新機能

SystemTemplateViewer を追加し、数百種類のシステム設定テンプレートを閲覧および使用できるようにします。

###問題修復

商城からダウンロードしたプラグインの修復中に、llama.cpp がリンク ライブラリが見つかりません。

LLAMACppのパスが長すぎる問題を修正します。

Windows パッケージ化後の llama.dll のリンクエラーを修正します。

iOS/Androidのファイルパスの読み取り問題を修正

Cllameの設定名の修正

## v1.3.0 - 2024.9.23

###重要な新機能

llama.cpp が統合され、大規模モデルのローカルオフライン実行がサポートされました。

## v1.2.0 - 2024.08.20

###新機能

OpenAI Image Edit/Image Variation サポート

Ollama APIをサポートし、Ollamaがサポートするモデルリストを自動的に取得するサポートをしています。

## v1.1.0 - 2024.08.07

###新機能

サポート図です。

## v1.0.0 - 2024.08.05

###新機能

基礎完整機能

OpenAI、Azure、Claude、Gemini をサポートします。

内蔵の機能豊富なエディター付きチャットツール

--8<-- "footer_ja.md"


> この投稿はChatGPTによって翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
