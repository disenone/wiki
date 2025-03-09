---
layout: post
title: 機能ノード
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
description: 機能ノード
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - 功能节点" />

#ブループリントセクション - 機能ノード

プラグインはいくつかの便利なブループリント機能ノードを追加しています。

##Cllama 関連

「Cllama Is Valid」：Cllama llama.cpp が適切に初期化されているかどうかを判断

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"判断 llama.cpp 在当前环境下是否支持 GPU backend"：Check if llama.cpp supports GPU backend in the current environment.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"取得サポートバックエンド llama.cpp がサポートするバックエンドを全て"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

「Cllama Prepare ModelFile In Pak」の場合は、「Pak内のモデルファイルを自動的にファイルシステムに準備する」になります。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

##イメージ関連

"Convert UTexture2D to Base64": UTexture2D を Base64 に変換

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

UTexture2D を .png ファイルに保存します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

UTexture2D へ .png ファイルを読み込む

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Duplicate UTexture2D": UTexture2D の複製

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

##オーディオに関連する

"USoundWave に .wav ファイルを読み込む"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

「.wav データを USoundWave に変換する」：.wav データを USoundWave に変換します

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

USoundWave を .wav ファイルに保存します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

「Get USoundWave Raw PCM Data」を、USoundWaveの生のPCMデータに変換してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"Convert USoundWave to Base64": USoundWaveをBase64に変換します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicate USoundWave": USoundWave を複製

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

"Convert Audio Capture Data to USoundWave": オーディオキャプチャデータをUSoundWaveに変換します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遺漏之處。 
