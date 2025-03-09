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

#エディターセクション - スタートする

##エディターチャットツール

メニューバーのTools -> AIChatPlus -> AIChatをクリックすると、プラグインが提供する編集ツールチャットが開きます。

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


ツールはテキスト生成、テキストチャット、画像生成、画像分析をサポートしています。

ツールのインターフェースは大まかに言えば以下のとおりです：

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

##主要機能

オフライン大規模モデル：llama.cppライブラリを統合し、大規模モデルのローカルオフライン実行をサポート

**テキストチャット**：左下の `New Chat` ボタンをクリックして、新しいテキストチャットセッションを作成してください。

**画像生成**: 左下の `New Image Chat` ボタンをクリックして、新しい画像生成セッションを作成してください。

**画像分析**：`New Chat` の一部のチャットサービスでは、画像の送信がサポートされています。例えば Claude、Google Gemini です。送信したい画像をロードするには、入力ボックスの上にある 🖼️ または 🎨 ボタンをクリックしてください。

**音声処理**: ツールは音声ファイル (.wav) の読み込みと録音機能を提供し、取得した音声をAIと会話に使用できます。

「現在のチャットキャラクターを設定」：チャットボックス上部のドロップダウンメニューで、テキストを送信する現在のキャラクターを設定でき、異なるキャラクターをシミュレーションして AI チャットを調整できます。

**クリアチャット**：チャットボックスの上部にある ❌ ボタンをクリックすると、現在の会話の履歴メッセージを消去できます。

**対話テンプレート**：数百種類の対話設定テンプレートが組み込まれており、よくある問題を簡単に処理できます。

**全局设置**：左下の `Setting` ボタンをクリックすると、全局設定ウィンドウが開きます。デフォルトのテキストチャット、画像生成APIサービスを設定し、各種APIサービスの具体的なパラメータを設定できます。設定はプロジェクトのパス `$(ProjectFolder)/Saved/AIChatPlusEditor` に自動的に保存されます。

**会話設定**：チャットボックス上部の設定ボタンをクリックすると、現在の会話の設定ウィンドウが開きます。会話の名前を変更したり、使用するAPIサービスを切り替えたり、各会話ごとにAPIの具体的なパラメーターを個別に設定することができます。会話設定は自動的に `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions` に保存されます。

**Chat content editing**: When hovering over a chat message, a settings button for that specific message appears, enabling options such as regenerating content, editing, copying, deleting, and regenerating content below (for content authored by the user).

**画像ブラウズ**：画像生成に関しては、画像をクリックすると画像ビューアーが開きます（ImageViewer）。PNG/UEテクスチャ形式で画像を保存する機能があり、テクスチャはコンテンツブラウザで直接確認でき、エディタ内で画像を利用するのが容易です。また、画像の削除、再生成、追加生成などの機能もサポートされています。Windows向けエディタでは、画像のコピーもサポートされており、画像をクリップボードに直接コピーして利用することができます。セッション生成の画像は各セッションフォルダに自動的に保存され、通常のパスは `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images` です。

全局设置：

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

会話設定：

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

チャット内容を編集します：

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

画像ビューア：

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

オフラインで大規模なモデルを使用します。

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

対話テンプレート

![system template](assets/img/2024-ue-aichatplus/system_template.png)

##エディターツールは、オフラインモデルCllama(llama.cpp)を使用します。

AIChatPlusエディターツールでオフラインモデルllama.cppを使用する方法について説明します。

ますように、「HuggingFace」ウェブサイトからオフラインモデル「[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

特定のフォルダにモデルを配置してください。たとえば、ゲームプロジェクトのディレクトリ Content/LLAMA に配置してください。

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

AIChatPlusのエディターツールを開く：ツール -> AIChatPlus -> AIChat、新しいチャットセッションを作成して、セッション設定ページを開く

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Api を Cllama に設定し、Custom Api Settings を有効にして、モデル検索パスを追加し、モデルを選択します。

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

チャットを開始しましょう！！

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

##エディターツールは、オフラインモデルCllama（llama.cpp）を使用して画像を処理します。

HuggingFace ウェブサイトからオフラインモデル MobileVLM_V2-1.7B-GGUF をダウンロードし、同じく [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but I can't provide a translation for just a single punctuation mark. If you have more text that needs translation, feel free to ask!

会話モデルの設定：

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

画像を送ってチャットを開始する

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

##エディターはOpenAIのチャットを使用しています。

チャットツールを開く Tools -> AIChatPlus -> AIChat し、新しいチャットセッション New Chat を作成し、セッション ChatApi を OpenAI に設定し、インターフェースパラメータを設定します

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

チャットを開始します：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

GPT-4o / GPT-4o-miniモデルに切り替えると、OpenAIのビジョン機能を使って画像を解析できます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

##エディターはOpenAIを使用して画像を処理します（作成/編集/変換）

チャットツールで新しい画像チャットを作成し、チャット設定をOpenAIに変更してパラメータを設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

画像を作成します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

画像を修正して、「画像チャットタイプ」を「編集」に変更し、元の画像と、修正が必要な場所を示す透明な部分（アルファチャンネルが0）をマスクした画像の2枚をアップロードしてください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

画像を変え、Image Chat Type を Variation に修正して、画像をアップロードしてください。OpenAI が元の画像の変種を返します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

##エディタはAzureを使用しています。

新しいチャットを作成して、ChatApi をAzureに変更し、AzureのAPIパラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

チャットを開始します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

##エディターを使用してAzureで画像を作成します。

新しい画像チャットセッション（New Image Chat）を作成し、ChatApiをAzureに変更し、AzureのAPIパラメータを設定します。dall-e-2モデルの場合は、QualityとStypeパラメータをnot_useに設定する必要があります。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

チャットを開始し、Azure に画像を作成させる

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

##エディターは Claude とチャットして画像を分析します。

新しいチャットセッション（New Chat）を作成して、ChatApiをClaudeに変更し、ClaudeのAPIパラメータを設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

チャットを開始します

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

##エディターはOllamaを使ってチャットしたり画像を分析したりします。

新しいチャットを作成し、ChatApiをOllamaに変更し、OllamaのAPIパラメータを設定します。テキストチャットの場合は、テキストモデル（例：llama3.1）にモデルを設定し、画像を処理する必要がある場合は、ビジョンをサポートするモデル（例：moondream）にモデルを設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

チャットを始める

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###エディタはGeminiを使用しています。

新しいチャットを作成し、ChatApiをGeminiに変更してGeminiのAPIパラメータを設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

チャットを開始します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

##エディターは、Gemini を使用して音声を送信します。

ファイルからオーディオを読み込む / アセットからオーディオを読み込む / マイクからオーディオを録音し、送信するためのオーディオを生成します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

チャットを開始します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

##エディターはDeepseekを使用します。

新しいチャット（New Chat）、ChatApiをOpenAiに変更し、DeepseekのAPIパラメータを設定します。Candidate Modelsを新しくdeepseek-chatと呼び、Modelをdeepseek-chatに設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

チャットを始める

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

--8<-- "footer_ja.md"


> この投稿はChatGPTによって翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)Please point out any omissions. 
