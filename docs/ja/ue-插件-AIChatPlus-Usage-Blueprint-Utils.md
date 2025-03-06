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

#設計図セクション - 機能ノード

プラグインは、いくつかの便利なブループリント機能ノードを追加提供します。

##Cllama 関連

"Cllama Is Valid"：判断 Cllama llama.cpp 是否正常初始化

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

「Cllama Is Support Gpu」：現在の環境で llama.cpp が GPU バックエンドをサポートしているかどうかを判定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Cllama Get Support Backends": 現在の llama.cpp でサポートされているすべてのバックエンドを取得


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Pakの中のモデルファイルを自動的にファイルシステムにコピーします。"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###画像に関連する

「UTexture2D を Base64 に変換する」: UTexture2D の画像を PNG の base64 形式に変換

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

UTexture2D を .png ファイルに保存します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

「.png ファイルを UTexture2D に読み込む」

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

UTexture2Dの複製

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###オーディオ関連

USoundWave に .wav ファイルをロードします。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

".wav データを USoundWave に変換する": .wav データを USoundWave に変換する

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

USoundWave を.wav ファイルに保存します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

"Get USoundWave Raw PCM Data" : "USoundWaveの生のPCMデータを取得します"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"Convert USoundWave to Base64" を日本語にすると、「USoundWave を Base64 に変換する」になります。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicate USoundWave": USoundWave の複製

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

"Convert Audio Capture Data to USoundWave": 音声キャプチャーデータをUSoundWaveに変換

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されましたので、[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)どんな抜け漏れも指摘してください。 
