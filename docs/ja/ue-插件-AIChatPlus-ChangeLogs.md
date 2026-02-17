---
layout: post
title: バージョンログ
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
description: バージョンログ
---

<meta property="og:title" content="UE 插件 AIChatPlus 版本日志" />

#UEプラグイン「AIChatPlus」バージョン変更ログ

## v2.0.0 - 2026.02.14

* **Tool Calling マルチプラットフォームサポート**: OpenAI、Claude、Gemini、Ollama、CllamaServerの5大プラットフォーム向けにツールコール/関数コール機能を新たに追加
* **Cllama Server 統合**: ローカル llama.cpp Server を完全サポート。作成、管理、音声認識機能を含み、編集画面からの視覚的な管理インターフェースを提供します
* **JSON ブループリントライブラリ**: JsonObject/JsonArray のブループリント操作クラスを新たに追加。JSON と USTRUCT の相互変換をサポート
* **OpenAI Audio**: OpenAIオーディオの入出力をサポート、エディタでオーディオレスポンスをプレビュー可能

## v1.8.0 - 2025.11.03

* llama.cpp b6792へのアップグレード

## v1.7.0 - 2025.07.06

* llama.cpp b5536 にアップグレード

* UE5.6に対応

* Androidのリリース時にcrashが発生するため、llama.cppを無効化しました

## v1.6.2 - 2025.03.17

###新機能

* CllamaにKeepContextパラメータを追加、デフォルトはfalse、Chat終了後にContextは自動的に破棄されます

* Cllama は KeepAlive パラメータを追加し、モデルの繰り返し読み込みを減らすことができます

## v1.6.1 - 2025.03.07

### Bug Fix

* OpenAI Image Chat のブループリントは画像の入力をサポートします

* Editor Tool Cllama mmproj モデルは空を許可します

## v1.6.0 - 2025.03.02

###新機能

* llama.cpp を b4604 バージョンにアップグレード

* Cllama は GPU バックエンドとして cuda と metal をサポートしています

* チャットツール「Cllama」はGPUの使用をサポートしています

* Pak にパックされたモデルファイルの読み取りをサポート

### Bug Fix

* Cllamaが推論中にreloadするとクラッシュする問題を修正

* iOSのコンパイルエラーを修正

## v1.5.1 - 2025.01.30

###新機能

* Geminiだけがオーディオを送信することが許可されています

* PCMData の取得方法を最適化し、B64 を生成する際にオーディオデータを解凍する

* リクエスト 2つのコールバックを追加 OnMessageFinished OnImagesFinished

* Gemini Methodを最適化し、bStreamに基づいて自動的にMethodを取得する

* Wrapperを実際の型に変換するため、およびResponse MessageとErrorを取得するためのブループリント関数をいくつか追加します

### Bug Fix

* Request Finish の多重呼び出し問題を修正

## v1.5.0 - 2025.01.29

###新機能

* Geminiにオーディオを送信する機能をサポート

* エディターツールは音声と録音の送信をサポートします

### Bug Fix

* Sessionコピー失敗のバグを修正

## v1.4.1 - 2025.01.04

###問題修正

* チャットツールは画像のみを送信し、メッセージを送らない機能をサポートしています

* OpenAIインターフェースでの画像送信の問題を修正

* OpenAI、Azureチャットツールの設定においてパラメータQuality、Style、ApiVersionが抜けていた問題を修正=

## v1.4.0 - 2024.12.30

###新機能

* （実験的機能）Cllama(llama.cpp) がマルチモーダルモデルをサポートし、画像を処理可能

* 全てのブループリント型パラメータに詳細なツールチップを追加しました

## v1.3.4 - 2024.12.05

###新機能

* OpenAIがvision APIをサポート

###問題修正

* OpenAI stream=false 時のエラーを修正

## v1.3.3 - 2024.11.25

###新機能

* UE-5.5をサポート

###問題修正

* 一部のブループリントが有効にならない問題を修正

## v1.3.2 - 2024.10.10

###不具合修正

* 手動停止リクエスト時に cllama がクラッシュする問題を修正

* ショップダウンロード版 win パッケージで ggml.dll と llama.dll ファイルが見つからない問題を修正

* リクエスト作成時にGameThread内にあるかをチェック、CreateRequestはゲームスレッドで確認

## v1.3.1 - 2024.9.30

###新機能

* SystemTemplateViewerを追加し、数百のシステム設定テンプレートを閲覧・使用できるようにしました

###問題修正

* マーケットプレイスからダウンロードしたプラグインを修正、llama.cppがリンクライブラリを見つけられない問題を解決

* LLAMACpp のパスが長すぎる問題を修正

* Windowsパッケージ化後のリンクllama.dllエラーを修正

* iOS/Androidにおけるファイルパスの読み取り問題を修正

* Cllameの名前設定エラーを修正

## v1.3.0 - 2024.9.23

###重大新機能

* llama.cppを統合し、ローカルでの大規模モデルのオフライン実行をサポートしました

## v1.2.0 - 2024.08.20

###新機能

* OpenAIの画像編集/画像バリエーションをサポート

* Ollama APIをサポートし、Ollamaがサポートするモデルリストの自動取得をサポート

## v1.1.0 - 2024.08.07

###新機能

* ブループリントのサポート

## v1.0.0 - 2024.08.05

###新機能

* 基本の完全な機能

* OpenAI、Azure、Claude、Geminiをサポート

* 機能が充実したエディターを内蔵したチャットツール

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されています。ご意見・ご感想は[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)指摘すべき抜け目があればご指摘ください。 
