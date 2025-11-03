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

## v1.8.0 - 2025.11.03

llama.cpp b6792のアップグレード

## v1.7.0 - 2025.07.06

llama.cppをb5536にアップグレード

* Support UE5.6

Androidのリリースバージョンがクラッシュする問題が発生していますので、llama.cppを無効にしてください。

## v1.6.2 - 2025.03.17

###新機能

Cllamaは、KeepContextパラメータをデフォルトでfalseに設定し、チャット終了後にContextが自動的に破棄されるように増加しました。

Cllamaは、KeepAliveパラメータを追加しました。これにより、モデルの繰り返し読み込みが減少します。

## v1.6.1 - 2025.03.07

### Bug Fix

OpenAI Image Chatの設計図は画像の入力をサポートしています。

エディターツールCllama mmprojは、モデルが空であることを許可します。

## v1.6.0 - 2025.03.02

###新機能

llama.cpp を b4604 バージョンにアップグレードします。

Cllama supports GPU backends: cuda and metal.

チャットツール Cllama は GPU を利用することができます。

Pak 中のモデルファイルを読み込むサポート

### Bug Fix

推論中にリロードすると、Cllamaがクラッシュする問題を修正します。

iOSのコンパイルエラーを修正します。

## v1.5.1 - 2025.01.30

###新機能

Gemini だけが音声を送信できます。

PCMDataの取得方法を最適化し、音声データをB64に変換する際に解凍するように修正します。

リクエスト: OnMessageFinishedとOnImagesFinishedの2つのコールバックを追加してください。

* Gemini Method を最適化し、bStream に基づいて Method を自動的に取得します。

実際のタイプに Wrapper を変換し、Response メッセージとエラーを取得できるように、いくつかのブループリント関数を追加しました。

### Bug Fix

修正要求完成时多次调用的问题。

## v1.5.0 - 2025.01.29

###新機能

ジェミニに音声ファイルを送信

エディターツールは、音声や録音の送信をサポートしています。

### Bug Fix

セッションのコピーに失敗するバグを修正します。

## v1.4.1 - 2025.01.04

###問題修復

チャットツールは画像のみを送信できますが、テキストは送信できません。

OpenAI のインターフェースで画像送信の問題の修正に失敗しました文の図。

OpanAI、Azure 聊天工具の設定で Quality、Style、ApiVersion パラメータが抜けている問題を修正しました。

## v1.4.0 - 2024.12.30

###新機能

（実験的な機能）Cllama(llama.cpp) は、マルチモードモデルをサポートし、画像を処理できます。

すべての設計図のタイプパラメータに詳細なヒントが追加されました。

## v1.3.4 - 2024.12.05

###新機能

OpenAIはVision APIをサポートしています。

###問題修復

OpenAI stream=false でのエラーの修正

## v1.3.3 - 2024.11.25

###新機能

* Support UE-5.5

###問題修正

一部分の設計図が機能しない問題を修正します。

## v1.3.2 - 2024.10.10

###問題修正

手動停止リクエスト時のcllamaのクラッシュを修正しました。

商店のダウンロード版の修復で、winパッケージでggml.dll llama.dllファイルが見つからない問題を修正します。

ゲームスレッド内でCreateRequestをチェックします。

## v1.3.1 - 2024.9.30

###新機能

システムテンプレートビューアが追加され、数百のシステム設定テンプレートを表示して使用できるようになりました。

###問題修復

商城からダウンロードしたプラグインの修正を行いましたが、llama.cpp のリンクライブラリが見つかりません。

LLAMACppのパスが長すぎる問題を修正

Windows パッケージング後の llama.dll のリンクエラーを修正します。

iOSおよびAndroidでのファイルパスの読み取りの問題を修正します。

Cllameの設定名の修正。

## v1.3.0 - 2024.9.23

###重要な新機能

llama.cppが統合され、大規模モデルのオフライン実行をサポートしています。

## v1.2.0 - 2024.08.20

###新機能

OpenAI Image Edit/Image Variation のサポート

Ollama APIに対応し、Ollamaがサポートするモデルのリストを自動的に取得します。

## v1.1.0 - 2024.08.07

###新しい機能

サポートプラン

## v1.0.0 - 2024.08.05

###新機能

基礎完備機能

OpenAI、Azure、Claude、Gemini をサポートします。

組み込まれた機能が充実したエディタ付きチャットツール

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されたものです。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出遺漏處。 
