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

## v1.6.2 - 2025.03.17

###新功能

CllamaのKeepContextパラメータを、デフォルト値であるfalseから増やし、Chatが終了した後に自動的にContextが破棄されるようにします。

CllamaはKeepAliveパラメータを追加して、モデルの重複読み込みを減らすことができます。

## v1.6.1 - 2025.03.07

### Bug Fix

OpenAI Image Chat の設計図は画像の入力をサポートしています。

エディターツールCllama mmprojは、modelを空白許可する。

## v1.6.0 - 2025.03.02

###新機能

llama.cppをb4604バージョンにアップグレードしました。

CllamaサポートGPUバックエンド：cudaとmetal

チャットツールCllamaはGPUの使用をサポートしています。

パック内のモデルファイルを読み込んでサポートする

### Bug Fix

推論中の Cllama でのリロード時にクラッシュする問題を修正

iOS のビルドエラーを修正します。

## v1.5.1 - 2025.01.30

###新しい機能

Geminiだけが音声を送信できます。

PCMData の取得方法を最適化し、音声データを再圧縮して B64 を生成します。

リクエスト: OnMessageFinishedとOnImagesFinishedの2つのコールバックを追加してください。

Gemini Methodを最適化し、bStreamに基づいてMethodを自動取得します。

一部分ブループリント関数を追加して、ラッパーを実際の型に変換し、レスポンスメッセージとエラーを取得することを容易にします。

### Bug Fix

リクエストの完了を複数回呼び出す問題を修正しました。

## v1.5.0 - 2025.01.29

###新機能

ジェミニにオーディオを送信します。

エディターツールは音声や録音の送信をサポートしています。

### Bug Fix

セッションコピーの失敗バグを修正します。

## v1.4.1 - 2025.01.04

###問題修復

チャットツールは画像だけを送信し、テキストメッセージは送信しない機能をサポートしています。

OpenAIのインターフェースにおける画像送信の問題を修正できず、失敗した文書です。

OpenAI、Azure チャットツールの設定で見落とされたパラメータ Quality、Style、ApiVersion の問題を修正する。

## v1.4.0 - 2024.12.30

###新機能

（実験的機能）Cllama（llama.cpp）は、マルチモードモデルをサポートし、画像を処理できます。

すべてのブループリントの種類パラメータには詳細なヒントが追加されています。

## v1.3.4 - 2024.12.05

###新機能

OpenAIはVision APIをサポートしています。

###問題の修復

OpenAI stream=false のエラー修正

## v1.3.3 - 2024.11.25

###新機能

* 支持 UE-5.5

###問題が修正されました。

一部分の設計図の効果が現れない問題を修正します。

## v1.3.2 - 2024.10.10

###問題の修正

手動停止リクエストの修復中に、cllamaがクラッシュする問題を修正します。

商城のダウンロード版winのパッケージングで、ggml.dllやllama.dllファイルが見つからない問題を修正します。

ゲームスレッド内でCreateRequestをチェックします。

## v1.3.1 - 2024.9.30

###新機能

システムテンプレートビューアーを追加しました。数百のシステム設定テンプレートを表示して使用できます。

###問題修復

商城からダウンロードしたプラグインを修正すると、llama.cpp がリンクライブラリを見つけられない問題が発生します。

LLAMACppのパスが長すぎる問題を修正します。

Windows パッケージング後の llama.dll リンクエラーを修正します。

iOSおよびAndroidのファイルパスの読み取り問題を修正します。

Cllame設定の名前エラーを修正します。

## v1.3.0 - 2024.9.23

###重要な新機能

llama.cppが統合され、ローカルで大規模モデルをオフラインで実行できるようになりました。

## v1.2.0 - 2024.08.20

###新しい機能

OpenAI Image Edit/Image Variationのサポート

Ollama APIをサポートし、Ollamaがサポートしているモデルリストを自動取得できるようサポートします。

## v1.1.0 - 2024.08.07

###新機能

サポートブループリント

## v1.0.0 - 2024.08.05

###新機能

基礎完整機能

OpenAI、Azure、Claude、Gemini を支持しています。

組み込まれた優れたエディター付きチャットツール

--8<-- "footer_ja.md"


> この投稿はChatGPTを使って翻訳されました、ご意見・ご感想は[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)すべての遺漏部分を指摘してください。 
