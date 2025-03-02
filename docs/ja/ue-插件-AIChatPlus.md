---
layout: post
title: UE プラグイン AIChatPlus 説明書
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

##プラグインの概要

This plugin supports UE5.2+.

UE.AIChatPlus はUnrealEngineのプラグインであり、さまざまなGPT AIチャットサービスとの通信を実現しています。現在サポートされているサービスはOpenAI（ChatGPT、DALL-E）、Azure OpenAI（ChatGPT、DALL-E）、Claude、Google Gemini、Ollama、llama.cppローカルオフラインです。将来的にはさらに多くのサービスプロバイダーをサポートする予定です。この実装は非同期RESTリクエストに基づいており、高速かつ効率的な性能を持っており、UE開発者がこれらのAIチャットサービスに簡単にアクセスできるようになっています。

UE.AIChatPlusには、エディターツールも含まれており、このツールを使ってAIチャットサービスを直接エディター内で利用し、テキストや画像を生成し、画像を分析することができます。

##使用説明

###エディターチャットツール

メニューバーのTools -> AIChatPlus -> AIChatをクリックすると、プラグインが提供するチャットツールのエディターが開きます。

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


ツールはテキスト生成、テキストチャット、画像生成、画像分析をサポートしています。

ツールのインターフェースはおおまかに言うと以下の通りです：

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####主要機能

オフラインベースの巨大なモデル：llama.cppライブラリを統合し、大規模モデルのローカルオフライン実行をサポート

テキストチャット：左下の `New Chat` ボタンをクリックして、新しいテキストチャットセッションを作成してください。

画像生成：左下の `New Image Chat` ボタンをクリックして、新しい画像生成セッションを作成します。

画像解析：`New Chat` の一部のチャットサービスでは画像の送信をサポートしています。例えばClaude、Google Geminiなどです。送信したい画像をロードするには、入力ボックス上の 🖼️ または 🎨 ボタンをクリックしてください。

「支持蓝图（Blueprint）」: 支持蓝图を使ってAPIリクエストを作成し、テキストチャットや画像生成などの機能を実現します。

現在のチャットキャラクターを設定します：チャットボックスの上部にあるドロップダウンメニューを使用して、現在のテキスト送信キャラクターを設定できます。異なるキャラクターを模擬して AI チャットを調整することができます。

会話のクリア：チャットボックスの上にある ❌ ボタンをクリックすると、現在の会話の履歴メッセージがクリアされます。

対話テンプレート：数百種類の対話設定テンプレートが組み込まれており、使いやすく、よくある問題を処理します。

以下为日语翻译内容：

* 全局設定：左下の `Setting` ボタンをクリックすると、全局設定ウィンドウを開くことができます。デフォルトのテキストチャット、画像生成のAPIサービス、および各APIサービスの具体的なパラメータを設定できます。設定はプロジェクトフォルダのパス`$(ProjectFolder)/Saved/AIChatPlusEditor`に自動的に保存されます。

会話の設定：チャットボックス上部の設定ボタンをクリックすると、現在の会話の設定ウィンドウが開きます。会話名の変更、使用するAPIサービスの変更、および各会話で使用するAPIの具体的なパラメーターの個別設定がサポートされています。会話設定は自動的に `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions` に保存されます。

チャット内容の編集：チャット内容にマウスを重ねると、その個々のチャットの設定ボタンが表示されます。コンテンツの再生成、編集、コピー、削除、および下部に新しいコンテンツの生成をサポートします（ユーザーのコンテンツの場合）。

画像の閲覧: 画像生成について、画像をクリックすると画像ビューア(ImageViewer) が開きます。PNG / UE テクスチャとして画像を保存でき、テクスチャはコンテンツブラウザ(Content Browser) で直接閲覧でき、画像がエディタ内で使用しやすくなります。さらに、画像の削除、再生成、さらに多くの画像を生成する機能もサポートされています。Windowsエディタでは、画像のコピーもサポートされており、画像をクリップボードに直接コピーして簡単に使用できます。セッションで生成された画像は自動的に各セッションフォルダに保存されます。通常のパスは `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images` です。

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

オフラインでの大規模モデルの使用

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

対話テンプレート

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###コアコードの紹介

現在のプラグインは次のモジュールに分かれています：

AIChatPlusCommon: Runtimeモジュールは、さまざまなAI APIインターフェースからのリクエストの処理と応答内容の解析を担当しています。

AIChatPlusEditor: エディターモジュール（Editor）は、エディターAIチャットツールの実装を担当しています。

AIChatPlusCllama: Runtime Moduleは、llama.cppのインタフェースとパラメータをカプセル化し、大規模なモデルのオフライン実行を実現します。

Thirdparty/LLAMACpp: A runtime third-party module that integrates the dynamic library and header files of llama.cpp.

UClass でリクエストを送信する責任を持つ具体的なクラスは FAIChatPlus_xxxChatRequest です。それぞれの API サービスにはそれぞれ独自の Request UClass があります。リクエストへの応答は UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase の 2 つの UClass を使用して取得し、対応するコールバックデリゲートを登録するだけです。

リクエストを送信する前に、APIのパラメータと送信メッセージを設定する必要があります。これは、FAIChatPlus_xxxChatRequestBodyを使用して設定します。返信の具体的な内容は、FAIChatPlus_xxxChatResponseBodyに解析され、コールバックを受信する際には、特定のインターフェースを介してResponseBodyを取得できます。

UE 商城で[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###エディターツールを使用してオフラインモデル Cllama(llama.cpp) を編集します。

AIChatPlusエディターツールでオフラインモデルllama.cppを使用する方法について説明します。

(https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

あるフォルダーにモデルを配置します。例えば、ゲームプロジェクトのディレクトリであるContent/LLAMAの下に配置してください。

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

AIChatPlus エディターツールを開きます：ツール -> AIChatPlus -> AIChat、新しいチャットセッションを作成し、セッションの設定ページを開きます。

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

ApiをCllamaに設定し、カスタムApi設定を有効にして、モデル検索パスを追加してモデルを選択します。

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

チャットを始めましょう！

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###エディターツールはオフラインモデルCllama（llama.cpp）を使用して画像を処理します。

HuggingFace ウェブサイトからオフラインモデル MobileVLM_V2-1.7B-GGUF をダウンロードし、同じく Content/LLAMA ディレクトリに保存してください：[ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)(https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but there is no text to translate.

会話モデルの設定：

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

画像を送って、チャットを開始します。

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###コードはオフラインモデルCllama(llama.cpp)を使用しています。

指示如何在代码中使用离线模型 llama.cpp。

ます。

コードを変更し、1つのコマンドを追加して、そのコマンド内でオフラインモデルにメッセージを送信します。

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

再コンパイルした後、エディタのCmdでコマンドを使用すると、OutputLogで大型モデルの出力結果を確認できます。

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###ブループリントは、オフラインモデル llama.cpp を使用しています。

青写真にオフラインモデル llama.cpp を使用する方法について説明します。

青写真から、`Send Cllama Chat Request` ノードを右クリックして作成してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Optionsノードを作成し、`Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`を設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Messages を作成し、System Message と User Message のそれぞれを追加してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Delegateを作成し、モデルの出力情報を受け取り、画面に出力します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完全な設計図はこう見えるよ。この設計図を実行してみると、ゲーム画面に大きなモデルが印刷されたメッセージが表示されるんだ。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###llama.cppをGPUで使用します。

"Cllama Chat Request Options" に「Num Gpu Layer」というオプションを追加しました。これにより、llama.cppのGPUペイロードを設定できます。以下に示す通りです。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

青写真ノードを使用して、現在の環境で GPU がサポートされているかどうかを判断し、現在の環境でサポートされているバックエンドを取得できます：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_2.png)

###.Pak内のモデルファイルを処理してください。

パック（Pak）ファイルの作成が開始されると、プロジェクトのすべてのリソースファイルが.Pakファイルに格納されます。もちろん、オフラインモデルのggufファイルも含まれています。

llama.cpp は .Pak ファイルの直接読み取りをサポートしていないため、オフラインモデルファイルを .Pak ファイルからファイルシステムにコピーする必要があります。

AIChatPlusは、.Pakファイル内のモデルファイルを自動的にコピーしてSavedフォルダに配置する機能関数を提供しています：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

あるいは、.Pakファイル内のモデルファイルを自分で処理することもできます。重要なのは、ファイルをコピーして処理することです。llama.cppは.Pakを正しく読み取れません。

## OpenAI

###エディターはOpenAIのチャットを使用しています。

これらのテキストを日本語に翻訳します:

* チャットツールを開く Tools -> AIChatPlus -> AIChat で新しいチャットセッション New Chat を作成し、セッション ChatApi を OpenAI に設定し、インターフェースパラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

チャットを始める：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

gpt-4o / gpt-4o-mini モデルに切り替えると、OpenAI の画像解析機能を利用できます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###エディターはOpenAIを使用して画像を処理します（作成/変更/変異）

チャットツール内で新しい画像チャットを作成し、会話設定をOpenAIに変更してパラメータを設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

画像を作成します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

画像を変更し、会話 Image Chat Type を Edit に変更し、元の画像と mask 画像（透明な領域の場所を示すアルファチャンネルが 0 ）の2枚をアップロードしてください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

写真を変化させて、会話イメージの種類を「変異」に変更して、画像をアップロードしてください。OpenAIは元の画像の変異を返します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###OpenAIモデルを使ったBlueprintチャット

藍プリントでノードを作成するには、右クリックして「Send OpenAI Chat Request In World」というノードを作成してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Options ノードを作成し、`Stream=true, Api Key="OpenAI からの API キー"` と設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Messages を作成し、System Message と User Message をそれぞれ追加してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Delegateを作成し、モデルの出力情報を受け取り、画面に出力します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完全な設計図はこのように見えます。設計図を実行すると、ゲーム画面に返される大規模なモデルの出力が表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###OpenAI を使用して画像を作成する青写真

青写真に`Send OpenAI Image Request`というノードを右クリックして作成し、`In Prompt="a beautiful butterfly"`を設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Options ノードを作成し、`Api Key="you api key from OpenAI"` を設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

イメージでの On Images イベントをバインドし、画像をローカルディスクに保存します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

完整なブループリントはこういう風に見えます。ブループリントを実行すれば、画像が指定された位置に保存されているのが分かります。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###エディターはAzureを使用しています。

新しいチャットを作成し、ChatApiをAzureに変更して、AzureのAPIパラメータを設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

チャットを開始します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###エディターを使用してAzureで画像を作成します。

新しい画像チャットを作成し、ChatApiをAzureに変更してAzureのAPIパラメータを設定します。ただし、dall-e-2モデルの場合は、QualityとStypeパラメータをnot_useに設定する必要があります。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

チャットを開始して、Azureに画像を作成させます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Azure チャットを使用した設計図

以下のブループリントを作成し、Azureオプションを設定し、実行をクリックすると、Azureからのチャット情報が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Azureを使用して画像を作成するための設計図

以下の手順に従い、Azureのオプションを設定してください。操作が完了したら「Create Image Done」というメッセージが画面上に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

上記のブループリントの設定によると、画像はパスD:\Downloads\butterfly.pngに保存されます。

## Claude

###エディターを使って、Claudeとチャットして画像を分析します。

新しいチャット（New Chat）を作成して、ChatApiをClaudeに変更し、ClaudeのAPIパラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

チャットを始める

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###青写真使用 Claude 进行聊天和图像分析。

青写真でノードを右クリックして`Send Claude Chat Request`を作成してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Options ノードを作成し、`Stream=true, Api Key="Clude からの API キー", Max Output Tokens=1024` を設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Messages を作成し、ファイルからTexture2Dを作成し、Texture2DからAIChatPlusTextureを作成し、AIChatPlusTextureをMessageに追加します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

前述のチュートリアルと同じように、イベントを作成してゲーム画面に情報を表示します。

完整的青写真看起来就像这样，运行这个写真，您会看到游戏屏幕上打印大型模型返回的消息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Ollama を取得する

Ollamaの公式ウェブサイトからインストールパッケージを入手し、ローカルにインストールすることができます：[ollama.com](https://ollama.com/)

他人が提供する Ollama インターフェースを介して Ollama を使用することができます。

###エディタは Ollama を使用してチャットし、画像を分析します。

新しいチャットを作成し、ChatApiをOllamaに変更し、OllamaのAPIパラメータを設定します。テキストチャットの場合は、テキストモデル（llama3.1など）にモデルを設定し、画像を取り扱う場合はビジョンをサポートするモデル（moondreamなど）に設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

チャットを始める

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Ollamaを使って、画像をチャットして分析するブループリント

以下のブループリントを作成し、Ollamaオプションを設定して、「実行」をクリックすると、Ollamaが返信するチャット情報が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###エディタは Gemini を使用しています。

新規チャットを作成し、ChatApiをGeminiに変更してGeminiのAPIパラメータを設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

チャットを始める

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###エディターはGeminiを使用して音声を送信します。

ファイルから音声を読み取るか、アセットから音声を読み取るか、マイクから音声を録音して送信する音声を生成する。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

チャットを開始します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###Blueprint is using Gemini chat.

以下の手順に従い、Gemini Options を設定した後に実行ボタンをクリックすると、Gemini から返されたチャット情報が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###ブループリントを使ってGeminiでオーディオを送信します。

以下の手順に従って、オーディオの読み込みとGemini Optionsの設定を行い、実行ボタンをクリックすると、Geminiがオーディオを処理した後に返されるチャット情報が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###エディタはDeepseekを使用しています。

新しいチャットを作成し、ChatApiをOpenAiに変更して、DeepseekのApiパラメータを設定します。Candidate Modelsに deepseek-chat を追加し、モデルを deepseek-chat に設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

チャットを開始します

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Blueprints are using Deepseek chat.

以下の内容に基づいて、Deepseek 関連のリクエストオプションを設定し、モデル、ベースURL、エンドポイントURL、APIキーなどのパラメータを設定してください。実行をクリックすると、Gemini から返されたチャット情報が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##提供された追加の設計図機能ノード

###Cllama関連

"Cllama Is Valid"：Cllama llama.cpp の正当性を判断します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu"を日本語にすると、判断 llama.cpp が現在の環境で GPU バックエンドをサポートしているかどうかです。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Cllama Get Support Backends" を日本語に訳すと、「現在の llama.cpp でサポートされているすべてのバックエンドを取得」になります。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Pak ファイル内のモデルファイルをファイルシステムにコピーするように Cllama が準備します"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###画像に関する

UTexture2D を Base64 に変換する：UTexture2D の画像を png base64 形式に変換

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

UTexture2D を .png ファイルに保存します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

UTexture2D に .png ファイルをロードします。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Duplicate UTexture2D": UTexture2D の複製

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###オーディオに関連する

"USoundWave へ .wav ファイルをロードする"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

「.wavデータをUSoundWaveに変換する」: .wavデータをUSoundWaveに変換します

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

USoundWaveを.wavファイルに保存してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

"Get USoundWave Raw PCM Data": USoundWaveを生のPCMデータに変換します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"Convert USoundWave to Base64": USoundWaveをBase64に変換します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicate USoundWave": USoundWave を複製

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

"Convert Audio Capture Data to USoundWave": 音声キャプチャーデータをUSoundWaveに変換します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

##更新履歴

### v1.6.0 - 2025.03.02

####新機能

llama.cpp を b4604 バージョンにアップグレードします。

CllamaはGPUバックエンドをサポートしています: cudaとmetal

チャットツールCllamaはGPUの使用をサポートしています。

Pak 中のモデルファイルを読み込むサポートを提供します。

#### Bug Fix

推理中の Cllama がリロードするとクラッシュする問題を修正しました。

iOSのコンパイルエラーを修正します。

### v1.5.1 - 2025.01.30

####新しい機能

Geminiだけが音声を投稿できます。

PCMData の取得方法を最適化し、音声データを B64 に変換する際に音声データを解凍するように変更しました。

* request 增加两个回调 OnMessageFinished OnImagesFinished

* リクエスト　OnMessageFinished と OnImagesFinished の 2 つのコールバックを追加してください。

Gemini Method を最適化して、bStream から Method を自動的に取得します。

実際のタイプにラッパーを変換し、レスポンスメッセージとエラーを取得するためのいくつかのブループリント関数を追加してください。

#### Bug Fix

"Request Finish" の複数回呼び出しの問題を修正します。

### v1.5.0 - 2025.01.29

####新しい機能

ジェミニにオーディオファイルを送信してください。

エディターツールは、音声や録音の送信をサポートしています。

#### Bug Fix

Sessionコピー失敗のバグを修正します。

### v1.4.1 - 2025.01.04

####問題修復

チャットツールは画像のみを送信できますが、テキストは送信できません。

OpenAI インターフェイスの画像送信エラー文の修正に失敗しました。

OpenAIおよびAzureチャットツールの設定がQuality、Style、ApiVersionパラメータを欠落している問題を修正=

### v1.4.0 - 2024.12.30

####新しい機能

（実験的機能）Cllama(llama.cpp)は、マルチモードモデルをサポートし、画像を処理できます。

すべてのブループリントのタイプのパラメータには、詳細な説明が付いています。

### v1.3.4 - 2024.12.05

####新機能

OpenAIはVision APIをサポートしています。

####問題が解決されました

OpenAI stream=false のエラーを修正

### v1.3.3 - 2024.11.25

####新機能

サポート UE-5.5

####問題の修正

特定のブループリントの効果が現れない問題を修正します。

### v1.3.2 - 2024.10.10

####問題修正

手動停止リクエスト時にcllamaがクラッシュする問題を修正します。

修复商城下载版本 win 打包找不到 ggml.dll llama.dll 文件的问题

ゲームスレッド内でCreateRequestがチェックされるかどうかを確認します。

### v1.3.1 - 2024.9.30

####新機能

システムテンプレートビューアーを追加しました。数百種類のシステム設定テンプレートを閲覧および使用できます。

####問題修復

商城からダウンロードしたプラグインを修復する際に、llama.cpp がリンクライブラリを見つけられません。

LLAMACppのパスが長すぎる問題を修正します。

Windowsパッケージング後のllama.dllのリンクエラーを修正します。

iOS/Androidのファイルパスの読み取り問題を修正する

Cllameの設定名の修正

### v1.3.0 - 2024.9.23

####重要な新機能

カルミンさん.cppを統合し、大規模モデルのオフライン実行をサポートしました。

### v1.2.0 - 2024.08.20

####新機能

OpenAI Image Edit/Image Variationのサポート

Ollama APIに対応し、Ollamaがサポートするモデルリストの自動取得をサポートします。

### v1.1.0 - 2024.08.07

####新機能

サポートプラン

### v1.0.0 - 2024.08.05

####新機能

基礎完整機能

OpenAI、Azure、Claude、Gemini をサポートしています。

組み込み機能が備わった高機能エディター付きチャットツール

--8<-- "footer_ja.md"


> この投稿はChatGPTを使って翻訳されたものです。何か[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。--> どんな見逃しも指摘してください。 
