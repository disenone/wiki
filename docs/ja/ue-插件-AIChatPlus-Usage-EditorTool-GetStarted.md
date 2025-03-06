---
layout: post
title: Get Started
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
description: Get Started
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 编辑器篇 - Get Started" />

#エディター - はじめよう

##エディターのチャットツール

メニューバーの Tools -> AIChatPlus -> AIChat をクリックすると、プラグインが提供するエディターチャットツールが開きます。

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


ツールはテキスト生成、テキストチャット、画像生成、画像分析をサポートします。

ツールのインターフェースはおおむね次のようになります：

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

##主要機能

オフライン大規模モデル：llama.cppライブラリを統合し、大規模モデルのローカルオフライン実行をサポート

* **テキストチャット**：左下の `New Chat` ボタンをクリックして、新しいテキストチャットセッションを作成してください。

「画像生成」：左下の `New Image Chat` ボタンをクリックして、新しい画像生成セッションを作成してください。

* **画像分析**：`New Chat`の一部のチャットサービスでは、画像を送信する機能がサポートされています。例えば Claude、Google Gemini。 送信する画像を読み込むには、入力ボックスの上にある 🖼️ または 🎨 ボタンをクリックしてください。

* **音声処理**：このツールでは音声ファイル（.wav）の読み取りおよび録音機能が提供されているため、取得した音声をAIと会話に活用できます。

現在のチャットキャラクターを設定します：チャットボックスの上にあるドロップダウンメニューで、テキスト送信の際のキャラクターを設定できます。AIチャットを調整するために、異なるキャラクターをシミュレートすることができます。

「Clear Session」：チャットボックスの上部にある❌ボタンを押すと、現在のセッションのメッセージ履歴を消去できます。

このテキストを日本語に翻訳します:
* **ダイアログテンプレート**：数百種類のダイアログ設定テンプレートが組み込まれており、よくある問題を簡単に処理できます。

* **全局设置**：左下の `Setting` ボタンをクリックすると、全局設定ウィンドウが開きます。デフォルトのテキストチャット、画像生成APIサービスを設定し、各APIサービスの具体的なパラメータを設定できます。設定はプロジェクトフォルダのパス `$(ProjectFolder)/Saved/AIChatPlusEditor` に自動保存されます。

* **会話設定**：チャットボックス上部の設定ボタンをクリックすると、現在の会話の設定ウィンドウを開くことができます。会話名の変更、使用する API サービスの変更、個々の会話ごとに API の具体的なパラメータを設定することができます。会話設定は自動的に `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions` に保存されます。

* **Chat Content Editing**: チャットコンテンツにマウスを重ねると、個々のチャットコンテンツの設定ボタンが表示され、内容の再生成、編集、コピー、削除、および下部に新しいコンテンツの生成（ユーザーがキャラクターである場合）がサポートされます。

* **Image browsing**: For image generation, clicking on an image will open the image viewing window (ImageViewer), supporting saving images as PNG/UE Texture. Textures can be directly viewed in the Content Browser, making it convenient to use images within the editor. Furthermore, functionalities such as deleting images, regenerating images, and continuing to generate more images are supported. For editors on Windows, image copying is also available, allowing images to be copied directly to the clipboard for easy use. Images generated during sessions will automatically be saved in each session folder, usually located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

全局设置：

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

会话设置：

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

チャット内容を修正：

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

画像ビューア：

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

オフラインで大規模モデルを使用します。

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

対話テンプレート

![system template](assets/img/2024-ue-aichatplus/system_template.png)

##エディターツールは、オフラインモデルCllama（llama.cpp）を使用しています。

AIChatPlusエディターツールでオフラインモデル llama.cpp を使用する方法を説明します。

(https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

特定のフォルダーにモデルを保存してください。例えば、ゲームプロジェクトのContent/LLAMAディレクトリに保存してください。

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

AIChatPlusのエディターツールを開く：ツール->AIChatPlus->AIChat、新しいチャットセッションを作成して、セッション設定ページを開きます。

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Api を Cllama に設定し、カスタム Api 設定を有効にして、モデルの検索パスを追加し、モデルを選択します。


![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

チャットを開始しましょう！！

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

##エディターツールを使用して、オフラインモデルCllama(llama.cpp)を使って画像を処理します。

HuggingFace ウェブサイトから MobileVLM_V2-1.7B-GGUF オフラインモデルをダウンロードし、[ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)Sure, the translation of this text into Japanese is: 「。」.

会話モデルの設定：

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)


画像を送信してチャットを開始

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

##エディターがOpenAIのチャットを使っています。

チャットツールを開きます Tools -> AIChatPlus -> AIChat で、新しいチャットセッション New Chat を作成し、セッション ChatApi を OpenAI に設定して、インタフェースパラメーターを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

チャットを開始する:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

GPT-4o / GPT-4o-mini にモデルを切り替えると、OpenAI のビジョン機能を使用して画像を分析できます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

##エディターはOpenAIを利用して画像を処理します（作成/編集/変更）。

チャットツールで新しい画像チャットを作成し、セッティングをOpenAIに変更してパラメータを設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

画像を作成します

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

画像を編集して、会話画像タイプを「編集」に変更し、元の画像と透明部分（アルファチャンネルが 0 である）を示すマスク画像の2枚をアップロードしてください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

写真を変更し、Image Chat TypeをVariationに変更して画像をアップロードすると、OpenAIは元の画像のバリエーションを返します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

##エディターはAzureを使用しています。

「新規チャット（New Chat）」を作成し、ChatApiをAzureに変更し、AzureのApiパラメーターを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

チャットを開始します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

##エディターはAzureを使用して画像を作成します。

新しい画像チャットセッション（New Image Chat）を作成し、ChatApiをAzureに変更し、AzureのAPIパラメータを設定します。なお、dall-e-2モデルの場合は、QualityとStypeパラメータをnot_useに設定する必要があります。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

チャットを開始し、Azureに画像を作成させる

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

##エディターは、Claudeを使用してチャットし、画像を分析します。

新しいチャットを作成し、ChatApiをClaudeに変更し、ClaudeのAPIパラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

チャットを始めます

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

##エディタは Ollama を使用してチャットや画像を分析します。

新しいチャットを作成し、ChatApiをOllamaに変更してOllamaのAPIパラメータを設定します。テキストチャットの場合は、モデルをテキストモデル（例：llama3.1）に設定し、画像を処理する必要がある場合は、visionをサポートするモデル（例：moondream）に設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

チャットを開始します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)


###エディタはGeminiを使用しています。

新規チャット（New Chat）、ChatApiをGeminiに変更し、GeminiのAPIパラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

チャットを始める

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

##エディターは Gemini を使用してオーディオを送信します。

ファイルから音声を読み取る/アセットから音声を読み取る/マイクから音声を録音し、送信する必要のある音声を生成する

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

チャットを開始します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

##Deepseekを使用したエディタ

新しいチャットを作成し、「ChatApi」を「OpenAi」に変更し、「Deepseek」のAPIパラメータを設定します。また、「Candidate Models」に「deepseek-chat」を追加し、モデルを「deepseek-chat」に設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

チャットを開始

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)ご指摘の抜け落ちを見つけてください。 
