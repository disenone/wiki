---
layout: post
title: Cllama (llama.cpp)
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
- llama.cpp
description: Cllama (llama.cpp)
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Cllama (llama.cpp)" />

#設計図 - Cllama（llama.cpp）

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_all.png)

##オフラインモデル

Cllama is implemented based on llama.cpp and supports offline use of AI inference models.

オフラインですので、まずモデルファイルを準備する必要があります。たとえば、HuggingFaceウェブサイトからオフラインモデルをダウンロードすることができます：[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

特定のフォルダーにモデルを配置してください。たとえば、ゲームプロジェクトのディレクトリ Content/LLAMA の下に配置します。

```shell
E:/UE/projects/FP_Test1/Content/LLAMA > ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

オフラインモデルファイルがあると、Cllama を使用して AI チャットを行うことができます。

##テキストチャット

Cllamaを使用してテキストチャットを行います。

青写真でノードを作成するために右クリックして、「Send Cllama Chat Request」を選択してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Options ノードを作成し、`Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"` を設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Messages を作成し、System Message と User Message のそれぞれを追加してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Delegateを作成し、モデルの出力情報を受け取り、画面に表示します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

詳細な設計図はこのようになります。設計図を実行すると、ゲーム画面に大規模なモデルが印刷されたメッセージが表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##画像を生成します llava

Cllamaはllavaライブラリを実験的にサポートし、Visionの機能を提供しました。

最初に、Multimodal オフラインモデルファイルを用意してください。例えば、Moondream（[moondream2-text-model-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-text-model-f16.gguf), [moondream2-mmproj-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-mmproj-f16.gguf)）または Qwen2-VL（[Qwen2-VL-7B-Instruct-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/Qwen2-VL-7B-Instruct-Q8_0.gguf), [mmproj-Qwen2-VL-7B-Instruct-f16.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-7B-Instruct-f16.gguf)）または llama.cpp がサポートする他の Multimodal モデル。

Options ノードを作成し、"Model Path" と "MMProject Model Path" のパラメータをそれぞれ対応するマルチモーダルモデルファイルに設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_1.png)

ノードを作成して、画像ファイル flower.png を読み込み、Messages を設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_3.png)

最終的にノードを作成し、返された情報を受け取って画面に表示し、完全な設計図は次のようになります。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_4.png)

実行ブループリントを表示して、返されたテキストを確認できます。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_5.png)

##lama.cppをGPUで使用

"Cllama Chat Request Options" に追加された "Num Gpu Layer" パラメーターは、llama.cpp の GPU ペイロードを設定でき、GPU で計算する必要のある層数を制御できます。画像を参照してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

## KeepAlive

「Cllama Chat リクエストオプション」に "KeepAlive" パラメータが追加されました。これにより、読み込んだモデルファイルをメモリに保持し、次回に簡単に使用できるようになり、モデル読み込みの回数が減ります。KeepAlive はモデルを保持する時間を表し、0 は保持しないことを意味し、使用後すぐに解放されます。-1 は永久に保持します。各リクエストごとに異なる KeepAlive を設定でき、新しい KeepAlive は古い値を置き換えます。例えば、初めの数回のリクエストでは KeepAlive=-1 を設定してモデルをメモリに保持し、最後のリクエストで KeepAlive=0 を設定してモデルファイルを解放します。

##.Pak ファイル内のモデルファイルを処理します。

Pak パッケージングを開始すると、プロジェクトのすべてのリソースファイルが .Pak ファイルに保存され、オフラインモデルの gguf ファイルも含まれています。

llama.cpp では .Pak ファイルを直接読み込めないため、オフラインモデルファイルを .Pak ファイルからファイルシステムにコピーする必要があります。

AIChatPlusは、.Pakファイルの中のモデルファイルを自動的にコピーしてSavedフォルダに配置する機能関数を提供しています：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

たとえば、あなた自身で .Pak 内のモデルファイルを処理することもできます。肝心なのは、ファイルをコピーして取り出す必要があることです。なぜなら、llama.cpp が .Pak を正しく読み取れないからです。

##機能ノード

Cllamaは、現在の状況を簡単に取得するためのいくつかの機能ノードを提供しています。


「Cllama Is Valid」：Cllama llama.cpp の正当性を確認します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu"：Check if llama.cpp supports GPU backend in the current environment

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"取得サポートされているバックエンドのリストを取得します": llama.cpp がサポートしているすべてのバックエンドを取得します.


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

“Cllama Prepare ModelFile In Pak”を日本語に訳すと、「Pak内のモデルファイルを自動的にファイルシステムに準備する」です。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)


--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 -> どんな抜け漏れがあるか指摘してください。 
