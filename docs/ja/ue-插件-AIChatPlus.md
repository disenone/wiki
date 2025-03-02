---
layout: post
title: UE プラグイン AIChatPlus の説明書
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
description: UE プラグイン AIChatPlus の説明書
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE プラグイン AIChatPlus の説明書

##公共倉庫

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##プラグイン取得

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##プラグインの紹介

This plugin supports UE5.2+.

UE.AIChatPlusはUnrealEngineのプラグインで、様々なGPT AIチャットサービスと通信する機能を実装しています。現在サポートされているサービスはOpenAI(ChatGPT、DALL-E)、Azure OpenAI(ChatGPT、DALL-E)、Claude、Google Gemini、Ollama、llama.cppのローカルオフラインです。将来的にはさらに多くのサービスプロバイダーをサポートする予定です。非同期RESTリクエストに基づいており、性能が高く、UEの開発者がこれらのAIチャットサービスに簡単にアクセスできるようになっています。

UE.AIChatPlus には、エディターツールも含まれており、このツールを使用するとAIチャットサービスを直接エディター上で活用できるようになり、テキストや画像を生成し、画像を分析することができます。

##利用手順

###エディタ チャットツール

メニューバーの Tools -> AIChatPlus -> AIChat を選択すると、プラグインが提供するチャットツールのエディターが開きます。

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


ツールがテキスト生成、テキストチャット、画像生成、画像分析をサポートします。

ツールのインターフェイスはおおよそ次の通りです：

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####主要機能

オフライン大規模モデル：llama.cppライブラリを統合し、ローカルでのオフライン実行をサポート

テキストチャット：左下の `New Chat` ボタンをクリックして、新しいテキストチャットセッションを作成します。

画像生成: 「New Image Chat」ボタンをクリックして、新しい画像生成セッションを作成します。

画像分析: `New Chat` での一部のチャットサービスは、画像の送信をサポートしています。例えば、ClaudeやGoogle Geminiのような画像です。送信したい画像をロードするには、入力ボックスの上にある 🖼️ または 🎨 ボタンをクリックしてください。

「Support Blueprint」：Support BlueprintはAPIリクエストを作成し、テキストチャット、画像生成などの機能を実行します。

現在のチャットキャラクターを設定します：チャットボックスの上にあるドロップダウンメニューから、テキストを送信するキャラクターを設定できます。異なるキャラクターをシミュレートして、AIチャットを調整できます。

セッションをクリア：チャットボックス上の❌ボタンで現在のセッションの履歴メッセージを消去できます。

数百種の対話設定テンプレートが組み込まれており、よくある問題を簡単に処理できます。

全局設定: 左下の `Setting` ボタンをクリックすると、全局設定ウィンドウが開きます。デフォルトのテキストチャット、画像生成APIサービス、および各APIサービスの具体的なパラメータを設定できます。設定は自動的にプロジェクトフォルダーのパス `$(ProjectFolder)/Saved/AIChatPlusEditor` に保存されます。

* チャットの設定： チャットボックス上部の設定ボタンをクリックすると、現在のチャットの設定ウィンドウが開きます。 セッション名の変更、使用されるAPIサービスの変更、それぞれのセッションでのAPI使用の具体的なパラメーターの個別設定をサポートしています。 セッションの設定は自動的に`$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`に保存されます。

チャット内容の編集: チャット内容上でマウスをホバーすると、それぞれのチャット内容の設定ボタンが表示され、コンテンツを再生成、編集、コピー、削除、または下部に再生成する（ユーザーの内容の場合）をサポートします。

画像閲覧: 画像生成に関して、画像をクリックすると画像ビューア（ImageViewer）が開きます。PNG/UE Texture形式での画像の保存をサポートし、Textureは内容ブラウザ（Content Browser）で直接閲覧でき、エディタ内での画像使用が容易になります。さらに、画像の削除、再生成、さらなる画像生成などの機能もサポートしています。Windows向けエディタでは、画像のコピーもサポートしており、画像をクリップボードに直接コピーして利用できます。セッション生成の画像は自動的に各セッションフォルダに保存され、通常のパスは `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images` です。

設計図：

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

全局设置：

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

会話設定：

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

チャット内容を変更する：

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

画像ビューア：

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

オフラインで大規模なモデルを使用します。

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

会話テンプレート

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###コアコードの紹介

現在のプラグインは以下のモジュールに分かれています：

AIChatPlusCommon: Runtimeモジュールは、さまざまなAI APIインターフェースのリクエストを処理し、応答内容を解析する責任があります。

AIChatPlusEditor: エディターモジュール(Editor)は、エディターAIチャットツールの実装を担当します。

AIChatPlusCllama: Runtimeモジュール - llama.cppのインターフェースとパラメータをカプセル化し、大規模モデルのオフライン実行を実現します。

Thirdparty/LLAMACpp: ランタイムサードパーティモジュールで、llama.cppのダイナミックライブラリとヘッダファイルが統合されています。

UClass による具体的なリクエスト送信を担当するのは、FAIChatPlus_xxxChatRequestです。各APIサービスにはそれぞれ独自のRequest UClassがあります。リクエストへの返信は、UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBaseの2つのUClassを介して取得されます。該当するコールバックデリゲートを登録するだけです。

リクエストを送信する前に、APIのパラメータと送信メッセージを設定する必要があります。これはFAIChatPlus_xxxChatRequestBodyを使用して設定されます。返信の具体的な内容はFAIChatPlus_xxxChatResponseBodyにも解析され、コールバックを受け取った際には特定のインターフェースを介してResponseBodyを取得できます。

UEストアで[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###エディターツールは、オフラインモデルCllama(llama.cpp)を使用しています。

AIChatPlus エディターツールでオフラインモデル llama.cpp を使用する方法について説明します。

(https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

特定のフォルダーにモデルを置く。たとえば、ゲームプロジェクトの Content/LLAMA ディレクトリに置く。

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

AIChatPlus のエディターツールを開く：ツール -> AIChatPlus -> AIChat 、新しいチャットセッションを作成し、セッションの設定ページを開く

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

ApiをCllamaに設定し、カスタムApi設定を有効にして、モデル検索パスを追加してモデルを選択してください。

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

チャットを開始！！

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###エディタツールは、オフラインモデルCllama(llama.cpp)を使用して画像を処理します。

HuggingFace ウェブサイトからオフラインモデル MobileVLM_V2-1.7B-GGUF をダウンロードし、それを同じく Content/LLAMA ディレクトリに置いてください：[ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but the text provided is already in Japanese.

セッションモデルの設定:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

画像を送信してチャットを開始

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###コードはオフラインモデル Cllama(llama.cpp)を使用しています。

下記は、コードでオフラインモデル llama.cpp を使用する方法についての説明です。

最初に、同じくモデルファイルを Content/LLAMA ディレクトリにダウンロードする必要があります。

コードを変更して、1つのコマンドを追加し、そのコマンド内でオフラインモデルにメッセージを送信します。

```c++
#include "Common/AIChatPlus_Log.h"
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"

void AddTestCommand()
{
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("AIChatPlus.TestChat"),
		TEXT("Test Chat."),
		FConsoleCommandDelegate::CreateLambda([]()
		{
			if (!FModuleManager::GetModulePtr<FAIChatPlusCommon>(TEXT("AIChatPlusCommon"))) return;

			TWeakObjectPtr<UAIChatPlus_ChatHandlerBase> HandlerObject = UAIChatPlus_ChatHandlerBase::New();
			// Cllama
			FAIChatPlus_CllamaChatRequestOptions Options;
			Options.ModelPath.FilePath = FPaths::ProjectContentDir() / "LLAMA" / "qwen1.5-1_8b-chat-q8_0.gguf";
			Options.NumPredict = 400;
			Options.bStream = true;
			// Options.StopSequences.Emplace(TEXT("json"));
			auto RequestPtr = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(
				Options,
				{
					{"You are a chat bot", EAIChatPlus_ChatRole::System},
					{"who are you", EAIChatPlus_ChatRole::User}
				});

			HandlerObject->BindChatRequest(RequestPtr);
			const FName ApiName = TEnumTraits<EAIChatPlus_ChatApiProvider>::ToName(RequestPtr->GetApiProvider());

			HandlerObject->OnMessage.AddLambda([ApiName](const FString& Message)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] Message: [%s]"), *ApiName.ToString(), *Message);
			});
			HandlerObject->OnStarted.AddLambda([ApiName]()
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestStarted"), *ApiName.ToString());
			});
			HandlerObject->OnFailed.AddLambda([ApiName](const FAIChatPlus_ResponseErrorBase& InError)
			{
				UE_LOG(AIChatPlus_Internal, Error, TEXT("TestChat[%s] RequestFailed: %s "), *ApiName.ToString(), *InError.GetDescription());
			});
			HandlerObject->OnUpdated.AddLambda([ApiName](const FAIChatPlus_ResponseBodyBase& ResponseBody)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestUpdated"), *ApiName.ToString());
			});
			HandlerObject->OnFinished.AddLambda([ApiName](const FAIChatPlus_ResponseBodyBase& ResponseBody)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestFinished"), *ApiName.ToString());
			});

			RequestPtr->SendRequest();
		}),
		ECVF_Default
	);
}
```

再コンパイルした後、エディタのCmdでコマンドを使用すると、OutputLogのログで大規模モデルの出力結果を確認できます。

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###No problem! Here is the translation:

ブループリントは、オフラインモデル llama.cpp を使用しています。

蓝图中使用离线模型 llama.cpp 的指南如下：

青写真でノード「Send Cllama Chat Request」を右クリックして作成してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Optionsノードを作成し、`Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`を設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Messages を作成し、System Message と User Message をそれぞれ追加してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Delegateを作成して、モデルの出力情報を受け取り、画面に表示します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完全な設計図はこう見えます。この設計図を実行すると、ゲーム画面に大きなモデルの印刷メッセージが表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###llama.cppをGPUを使用しています。

「Cllama Chat Request Options」に「Num Gpu Layer」というパラメータが追加され、llama.cppのGPUペイロードを設定できるようになりました。画像を参照してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

現在の環境でGPUがサポートされているかどうかを判断し、現在の環境でサポートされているバックエンドを取得するためにブループリントノードを使用できます：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_2.png)

###モデルファイルを.Pak内で処理してください。

Pakファイルを作成すると、プロジェクトのすべてのリソースファイルがPakファイルに保存され、オフラインモデルのggufファイルも含まれます。

.llama.cppは.Pakファイルを直接読み込めないため、オフラインモデルファイルを.Pakファイルからファイルシステムにコピーする必要があります。

AIChatPlusは、.Pakファイル内のモデルファイルを自動的にコピーしてSavedフォルダに保存する機能関数を提供しています。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

あるいは、.Pak内のモデルファイルを直接処理することもできます。重要なのは、ファイルをコピーして処理する必要があるということです。llama.cppは.Pakを正しく読み取ることができません。

## OpenAI

###エディターはOpenAIのチャットを使用しています。

チャットツールを開き、Tools -> AIChatPlus -> AIChatに移動し、新しいチャットセッションNew Chatを作成し、セッションChatApiをOpenAIに設定し、インターフェースパラメーターを設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

チャットを始めます：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

gpt-4o / gpt-4o-mini モデルに切り替えると、OpenAI の画像解析機能を使用できます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###エディターはOpenAIを使用して画像を処理します（作成/変更/変異）。

チャットツールで新しい画像チャットを作成し、「OpenAI」という名前を付けて会話設定を変更し、パラメータを設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

画像を作成します.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

画像を編集して、会話イメージの種類を「編集」に変更して、元の画像と、マスクされた透明な部分（アルファチャネルが 0 で示される）の2枚の画像をアップロードしてください。それが修正が必要な場所を示します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

画像の種類を Image Chat Type から Variation に変更して画像をアップロードすると、OpenAI が元の画像の変種を返します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Blueprint using OpenAI model chat

設計図で右クリックして、ノード `Send OpenAI Chat Request In World` を作成します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Options ノードを作成し、`Stream=true, Api Key="you api key from OpenAI"` と設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Messages を作成し、System Message と User Message をそれぞれ追加してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

デリゲートを作成して、モデルの出力情報を受け取り、画面に出力する。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完整な設計図はこう見える。設計図を実行すると、ゲーム画面に大きなモデルが返されるメッセージが表示される。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###ブループリントが OpenAI を利用して画像を作成します。

日本語に翻訳すると、以下のようになります:

* ブループリント内で、"Send OpenAI Image Request"というノードを作成して、"In Prompt="a beautiful butterfly""と設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Options ノードを作成して、「Api Key="you api key from OpenAI"」を設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

画像に関する On Images イベントをバインドし、画像をローカルディスクに保存します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

完璧な設計図はこう見える。設計図を実行すると、指定された場所に画像が保存されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###エディターはAzureを使用しています。

新しいチャットを作成し、ChatApiをAzureに変更してAzureのAPIパラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

チャットを開始します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###エディタを使用して、Azure で画像を作成します。

新しい画像チャットセッション（New Image Chat）を作成し、ChatApiをAzureに変更し、AzureのAPIパラメータを設定します。なお、dall-e-2モデルの場合は、QualityとStypeパラメータをnot_useに設定する必要があります。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

チャットを開始し、Azureに画像を作成させる

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Azure チャットを使用した設計図

以下の手順に従い、Azure オプションを設定し、実行をクリックすると、Azure から返されたチャット情報が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Azureを使用して図面を作成します。

以下は、Azureオプションを設定したブループリントを作成し、実行ボタンをクリックします。画像の作成が成功した場合、画面上に "Create Image Done" というメッセージが表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

上記の設定に従い、画像はパス D:\Dwnloads\butterfly.png に保存されます。

## Claude

###エディターは、Claudeとチャットして画像を分析します。

新しいチャット（New Chat）を作成し、ChatApiをClaudeに変更し、ClaudeのAPIパラメータを設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

チャットを開始します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###設計図には、Claudeを使用してチャットして画像を分析します。

青写真でノードを右クリックして `Send Claude Chat Request` を作成します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Options ノードを作成し、`Stream=true, Api Key="Clude からの API キー", Max Output Tokens=1024` を設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Messagesを作成し、ファイルからTexture2Dを作成し、Texture2DからAIChatPlusTextureを作成して、AIChatPlusTextureをMessageに追加します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

前述の手順に従い、イベントを作成してゲーム画面に情報を表示します。

要将这段文字翻译为日语，它会是这样的：

完全な設計図はこう見える。この設計図を実行すると、ゲーム画面に大きなモデルが印刷されたメッセージが表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Ollamaを取得

Ollama公式ウェブサイトからインストールパッケージをダウンロードして、ローカルにインストールすることができます：[ollama.com](https://ollama.com/)

他人が提供した Ollama インターフェースを使用して Ollama を利用することができます。

###エディタは Ollama を使用してチャットと画像を分析します。

新しいチャットを作成し、ChatApiをOllamaに変更してOllamaのAPIパラメータを設定します。テキストチャットの場合は、モデルをテキストモデル（例：llama3.1）に設定し、画像を処理する必要がある場合は、ビジョンをサポートするモデル（例：moondream）に設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

* チャットを始める

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###ブループリントでは、Ollamaを使用してチャットし、画像を解析します。

以下のブループリントを作成し、Ollamaオプションを設定してから実行ボタンをクリックすると、Ollamaからのチャット情報が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###エディタはGeminiを使用します。

新しいチャットを開始し、ChatApiをGeminiに変更し、GeminiのAPIパラメータを設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

チャットを開始します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###エディターはGeminiを使用してオーディオを送信します。

ファイルからオーディオを読み込む/アセットからオーディオを読み込む/マイクからオーディオを録音して、送信するオーディオを作成します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

* チャットを開始

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###Blueprint utilizing Gemini chat

以下のブループリントを作成し、Gemini Optionsを設定してから「実行」をクリックすると、Geminiが返すチャット情報が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###ブループリントはGeminiを使用してオーディオを送信します。

以下のブループリントを作成し、オーディオの読み込みを設定し、Gemini Options を設定し、実行をクリックすると、画面に Gemini が処理したオーディオの戻りチャット情報が表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###エディタはDeepseekを使用しています。

新しいチャットセッションを開始し、ChatApiをOpenAiに変更してDeepseekのAPIパラメータを設定します。Candidate Modelsにdeepseek-chatを追加し、モデルをdeepseek-chatに設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

チャットを開始します

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###設計図をDeepseekチャットで利用します。

以下テキスト内容を日本語に翻訳します：

以下の設計図を作成し、Deepseekに関連するリクエストオプションを設定します。それには、モデル、ベースURL、エンドポイントURL、APIキーなどのパラメータが含まれます。実行ボタンをクリックすると、Geminiから返されたチャット情報が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##提供される特別な設計図の機能ノード

###Cllamaに関連

"Cllama Is Valid"：Cllama llama.cpp の正常な初期化を確認します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu"：データを解析し、llama.cpp が現在の環境で GPU バックエンドをサポートしているか判断します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"「Cllama Get Support Backends」を日本語に翻訳すると、「llama.cpp」でサポートされているすべてのバックエンドを取得します。"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Pak内のモデルファイルを自動的にファイルシステムに準備する"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###画像に関する

"UTexture2DをBase64に変換する": UTexture2Dをpngのbase64形式に変換します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

UTexture2D を .png ファイルに保存します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

UTexture2D へ .png ファイルを読み込む。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Duplicate UTexture2D": UTexture2D の複製

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###オーディオ関連

USoundWave に .wav ファイルをロードします。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

".wav データをUSoundWaveに変換する": .wav データをUSoundWaveに変換します.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

USoundWave を .wav ファイルに保存します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

"Get USoundWave Raw PCM Data": USoundWave の生のPCMデータを取得します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"Convert USoundWave to Base64" を日本語にすると、"USoundWave を Base64 に変換する" です。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicate USoundWave": USoundWave を複製

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

"USoundWave にオーディオキャプチャーデータを変換する"：Audio Capture のデータを USoundWave に変換します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

##更新履歴

### v1.6.0 - 2025.03.02

####新しい機能

「llama.cpp」を b4604 バージョンにアップグレードします。
Cllama supports GPU backends: cuda and metal.
チャットツールCllamaはGPUを使用しています。
Pak 中のモデルファイルを読み込むサポートを提供します。

#### Bug Fix

推理中 Cllama 在重新加载时会崩溃的问题已修复

iOSのコンパイルエラーを修正します。

### v1.5.1 - 2025.01.30

####新機能

Geminiだけが音声を送信することができます。

PCMDataの取得方法を最適化し、音声データをB64に変換する際に再度解凍します。

リクエスト: OnMessageFinishedとOnImagesFinishedの2つのコールバックを追加してください。

Gemini Method を最適化し、bStream に基づいて Method を自動的に取得します。

一部のブループリント機能を追加して、Wrapperを実際のタイプに変換し、レスポンスメッセージとエラーを取得できるようにしています。

#### Bug Fix

Request Finishが複数回呼び出される問題を修正しました。

### v1.5.0 - 2025.01.29

####新機能

Geminiに音声サポートを提供

エディターツールは、音声と録音の送信をサポートしています。

#### Bug Fix

Sessionコピーが失敗する不具合を修正します。

### v1.4.1 - 2025.01.04

####問題修復

チャットツールは画像のみを送信してメッセージを送信しない機能をサポートしています。

OpenAIのインターフェースにおける画像の送信問題の修正に失敗したドキュメント絵を訂正してください。

OpanAI、Azureのチャットツール設定にQuality、Style、ApiVersionパラメーターが抜けている問題を修正してください。

### v1.4.0 - 2024.12.30

####新機能

（実験的機能）Cllama(llama.cpp)は、マルチモーダルモデルをサポートし、画像を処理することができます。

すべての設計図の種類のパラメータには詳細な説明が追加されました。

### v1.3.4 - 2024.12.05

####新機能

OpenAIはVision APIをサポートしています。

####問題の修正

OpenAI stream=false時のエラー修正

### v1.3.3 - 2024.11.25

####新機能

サポートされるのは UE-5.5 です。

####問題を修正します。

部分の設計図が機能しない問題を修正します。

### v1.3.2 - 2024.10.10

####問題の修正

* 手動で停止リクエストを修正すると、cllamaがクラッシュします。

商城のダウンロード版winパッケージでggml.dllまたはllama.dllファイルが見つからない問題を修正する

* 创建请求时检查是否在 GameThread 中，CreateRequest check in game thread
* ゲームスレッド内でのCreateRequestのチェック

### v1.3.1 - 2024.9.30

####新機能

「SystemTemplateViewer」を追加しました。これにより、数百のシステム設定テンプレートを閲覧および使用できるようになります。

####問題修復

商城からダウンロードしたプラグインを修正し、llama.cpp がリンクライブラリを見つけられない

LLAMACppのパスが長すぎる問題を修正

* Windows パッケージング後の llama.dll リンクエラーを修正

iOSおよびAndroidのファイルパスの読み取り問題を修正します。

Cllame設定名の修正

### v1.3.0 - 2024.9.23

####重要な新機能

- llama.cppを統合し、大規模モデルのローカルオフライン実行をサポートしています。

### v1.2.0 - 2024.08.20

####新機能

OpenAI Image Edit/Image Variationサポート

Ollama APIに対応し、Ollamaがサポートするモデルリストを自動取得する機能をサポートします。

### v1.1.0 - 2024.08.07

####新機能

支持蓝图

### v1.0.0 - 2024.08.05

####新機能

基礎完整機能

OpenAI、Azure、Claude、Gemini をサポートしています。

組み込まれた優れた編集機能を持つチャットツール

--8<-- "footer_ja.md"


> この投稿は ChatGPT によって翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)指定の部分があれば指摘してください。 
