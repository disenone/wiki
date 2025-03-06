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

#設計図パート - Cllama (llama.cpp)

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_all.png)

##オフラインモデル

Cllamaは、llama.cppに基づいて実装され、オフラインでAI推論モデルをサポートしています。

オフラインなので、まずモデルファイルを準備する必要があります。たとえば、HuggingFaceウェブサイトからオフラインモデルをダウンロードする必要があります: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

特定のフォルダーにモデルを置いてください。例えば、ゲームプロジェクトのディレクトリ Content/LLAMA の下に配置します。

```shell
E:/UE/projects/FP_Test1/Content/LLAMA > ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

オフラインモデルファイルがあれば、Cllamaを使ってAIチャットを行うことができます。

##テキストチャット

Cllamaを使用してテキストチャットを行う

青写真でノードを右クリックして「Send Cllama Chat Request」を作成してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Options ノードを作成して、`Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"` を設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Messagesを作成し、System MessageとUser Messageをそれぞれ1つ追加します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Delegateを作成し、モデルからの出力情報を受け取り、画面に表示する。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完全な設計図はこう見えるよ。設計図を実行すれば、ゲーム画面で大規模なモデルの印刷結果が表示されるよ。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##画像を生成するテキスト llava

Cllamaはllavaライブラリを実験的にサポートし、Visionの機能を提供しました。

ます。こちらが翻訳です：

まず、Multimodalオフラインモデルファイルを準備します。例えば、Moondream（[moondream2-text-model-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-text-model-f16.gguf), [moondream2-mmproj-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-mmproj-f16.gguf)Qwen2-VL（[Qwen2-VL-7B-Instruct-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/Qwen2-VL-7B-Instruct-Q8_0.gguf), [mmproj-Qwen2-VL-7B-Instruct-f16.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-7B-Instruct-f16.gguf)）または他の llama.cpp がサポートするMultimodalモデル。

Options ノードを作成し、"Model Path" と "MMProject Model Path" のパラメータをそれぞれ対応する Multimodal モデルファイルに設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_1.png)

画像ファイル flower.png を読み込んでノードを作成し、Messages を設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_3.png)

最後、ノードを作成し、返された情報を受け取り、画面に出力します。完全な設計図は次のようになります。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_4.png)

フロー図を実行すると、返されるテキストが表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_5.png)

##llama.cppを使ってGPUを活用します。

"Cllama Chat Request Options" has added the parameter "Num Gpu Layer", which allows setting the GPU payload of llama.cpp, enabling control over the number of layers that need to be computed on the GPU. See the figure for reference.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

##モデルファイルを.Pakにパッケージ化した後の処理

Pak パッケージングを開始すると、プロジェクトのすべてのリソースファイルが .Pak ファイルに保存されます。もちろん、オフラインモデルである gguf ファイルも含まれています。

LLama.cpp は .Pak ファイルを直接読むことができないので、オフラインモデルファイルを .Pak ファイルからファイルシステムにコピーする必要があります。

AIChatPlusは、.Pak内のモデルファイルを自動的にコピーしてSavedフォルダに配置する機能関数を提供しています。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

または、.Pak内のモデルファイルを自分で操作することもできますが、重要なのはファイルをコピーして出力する必要があるということです。なぜなら、llama.cppは.Pakを正しく読み取れないからです。

##機能ノード

Cllamaは、現在の状況を取得するのに便利ないくつかの機能ノードを提供しています。


"Cllama Is Valid"：Cllama llama.cpp の初期化が正常かどうかを判断します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu"：判断 llama.cpp 在当前环境下是否支持 GPU backend

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"「Cllama Get Support Backends」: Get all the backends supported by the current llama.cpp"


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama Prepare ModelFile In Pak": Pak内のモデルファイルを自動的にファイルシステムにコピーします。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)


--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)指摘してくれたら見逃しはないよ。 
