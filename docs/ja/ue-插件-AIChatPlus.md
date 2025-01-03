---
layout: post
title: UEプラグインAIChatPlusの説明書
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
description: UE プラグイン AIChatPlus 説明書
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE プラグイン AIChatPlus の説明書

##公共倉庫

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##プラグインの取得

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##プラグインの紹介

This plugin supports UE5.2+.

UE.AIChatPlusはUnrealEngineのプラグインであり、様々なGPT AIチャットサービスとの通信を実現しています。現在サポートされているサービスにはOpenAI(ChatGPT, DALL-E)、Azure OpenAI(ChatGPT, DALL-E)、Claude、Google Gemini、Ollama、llama.cppローカルオフラインがあります。将来はさらに多くのサービスプロバイダーをサポートする予定です。実装は非同期RESTリクエストに基づいており、性能が高く、UE開発者がこれらのAIチャットサービスに簡単にアクセスできるようになっています。

UE.AIChatPlusには、エディターツールも含まれており、このツールを使用してAIチャットサービスを直接エディター内で利用し、テキストや画像を生成し、画像を解析することができます。

##使用説明

###エディター・チャットツール

メニューバーのTools -> AIChatPlus -> AIChatをクリックすると、プラグインが提供するチャットツールのエディタが開きます。

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


ツールサポートテキスト生成、テキストチャット、画像生成、画像分析。

ツールのインターフェースはおおよそ次のようになります：

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####主要な機能

オフラインビッグモデル：llama.cppライブラリを統合し、ローカルでのオフラインビッグモデルの実行をサポート

テキストチャット：左下の `New Chat` ボタンをクリックして、新しいテキストチャットセッションを作成します。

画像生成：左下の `New Image Chat` ボタンをクリックして、新しい画像生成セッションを作成します。

画像解析：`New Chat` の一部チャットサービスは、画像の送信をサポートしています。例えば、Claude、Google Gemini。送信する画像を読み込むには、入力ボックスの上にある 🖼️ または 🎨 ボタンをクリックしてください。

サポート ブループリント（Blueprint）：サポート ブループリントの作成 API リクエストを使用して、テキスト チャット、画像生成などの機能を実現します。

現在のチャットキャラクターを設定する：チャットボックスの上にあるドロップダウンメニューを使用して、テキストを送信する現在のキャラクターを設定できます。 AIチャットを調整するために異なるキャラクターを模倣できます。

セッションのクリア：チャットボックス上の❌ ボタンをタップすると、現在のセッションの履歴メッセージを削除できます。

対話テンプレート: 数百種類の対話設定テンプレートが内蔵されており、よくある問題を簡単に処理できます。

全局設定：左下の `Setting` ボタンをクリックすると、全体設定ウィンドウが開きます。デフォルトのテキストチャット、画像生成の API サービスを設定し、各 API サービスの具体的なパラメータを設定できます。設定はプロジェクトフォルダのパス `$(ProjectFolder)/Saved/AIChatPlusEditor` に自動的に保存されます。

会話設定：チャットボックスの上にある設定ボタンをクリックすると、現在の会話の設定ウィンドウが開きます。会話名を変更したり、会話で使用するAPIサービスを変更したり、各会話ごとにAPIの具体的なパラメータを個別に設定することができます。会話設定は自動的に「$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions」に保存されます。

チャット内容の編集: マウスをチャット内容の上にホバーすると、そのチャット内容に対する設定ボタンが表示されます。コンテンツの再生成、編集、コピー、削除、または下に新しいコンテンツを生成することができます（ユーザーのコンテンツに対して）。

* 画像閲覧：画像生成に関して、画像をクリックすると画像ビューアーウィンドウ（ImageViewer）が開き、画像の PNG/UE テクスチャとして保存できます。テクスチャはコンテンツブラウザー（Content Browser）で直接確認可能で、エディター内での画像使用を容易にします。さらに、画像の削除、再生成、追加生成などの機能をサポートしています。Windows用エディターでは、画像のコピーもサポートされており、画像をクリップボードに直接コピーして簡単に利用できます。セッション生成された画像は各セッションフォルダーに自動保存され、通常のパスは `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images` です。

設計図：

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

全体の設定：

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

会話設定:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

チャット内容の修正：

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

画像ビューア：

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

オフラインで大規模なモデルを使用します。

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

対話テンプレート

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###コアコードの紹介

現在のプラグインは、以下のモジュールに分かれています：

AIChatPlusCommon: 运行时模块 (Runtime)，负责处理各种 AI API 接口发送请求和解析回复内容。  
AIChatPlusCommon:ランタイムモジュールは、さまざまなAI APIインターフェースからのリクエストの送信および応答内容の解析を担当しています。

AIChatPlusEditor: エディターモジュール（Editor），は、エディターAIチャットツールを実装する責任があります。

AIChatPlusCllama: The runtime module that encapsulates the interface and parameters of llama.cpp to achieve offline execution of large models.

* Thirdparty/LLAMACpp: ランタイムサードパーティモジュールで、llama.cppのダイナミックライブラリとヘッダファイルを統合しています。

UClass、それはFAIChatPlus_xxxChatRequestという要求を送信するための具体的なクラスです。各APIサービスには、個別のRequest UClassがあります。要求の応答は、UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBaseという2種類のUClassを使用して取得され、対応するコールバックデリゲートを登録するだけです。

リクエストを送信する前に、APIのパラメータと送信メッセージを設定する必要があります。これには、FAIChatPlus_xxxChatRequestBodyを使用して設定します。返信の具体的な内容は、FAIChatPlus_xxxChatResponseBodyに解析され、コールバックを受け取った際には、特定のインタフェースを通じてResponseBodyを取得できます。

UE マーケットプレイスで[AICheatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###エディターツールは、オフラインモデル Cllama(llama.cpp) を使用します。

AIChatPlusエディターツールでオフラインモデル llama.cpp を使用する方法についての説明です。

最初に、HuggingFaceウェブサイトからオフラインモデルをダウンロードしてください：[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

特定のフォルダにモデルを保存します。たとえば、ゲームプロジェクトの Content/LLAMA ディレクトリに保存します。

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

AIChatPlusのエディターツールを開く：ツール -> AIChatPlus -> AIChat、新しいチャットセッションを作成して、セッション設定ページを開きます。

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

ApiをCllamaに設定し、カスタムApi設定を有効にして、モデル検索パスを追加し、モデルを選択してください。

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

チャットを開始しましょう！！

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###エディターツールは、オフラインモデルCllama(llama.cpp)を使用して画像を処理します。

HuggingFace ウェブサイトからオフラインモデル MobileVLM_V2-1.7B-GGUF をダウンロードし、Content/LLAMA ディレクトリに配置してください：[ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)(https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)申し訳ありませんが、そのテキストを翻訳することはできません。

会話モデルの設定：

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

画像を送ってチャットを始める

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###コードはオフラインモデルCllama（llama.cpp）を使用しています。

こちらは、コード内でオフラインモデル llama.cpp を使用する方法についての説明です。

最初に、Content/LLAMA フォルダにモデルファイルをダウンロードする必要があります。

コードを修正して1つのコマンドを追加し、コマンド内でオフラインモデルにメッセージを送信します。

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

再コンパイルした後、エディターのCmdでコマンドを使用すると、OutputLogで大規模モデルの出力結果を確認できます。

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###青写真使用离线模型 llama.cpp

青写真でオフラインモデル llama.cpp を使用する方法について説明します。

ブループリントでノード「Send Cllama Chat Request」を右クリックして作成してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Options ノードを作成し、`Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"` を設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Messages を作成し、System Message と User Message をそれぞれ追加してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Delegateを作成し、モデルの出力情報を受け取り、画面に表示します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完全なブループリントはこのように見えます。ブループリントを実行すると、ゲーム画面に大きなモデルが印刷されたメッセージが表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###エディターはOpenAIのチャットを使用しています。

チャットツールを開いて Tools -> AIChatPlus -> AIChat に移動し、新しいチャットセッション New Chat を作成し、セッションを ChatApi に設定してください。OpenAI とインターフェースパラメーターを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

チャットを始める：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

gpt-4o / gpt-4o-mini のモデルに切り替えると、OpenAI のビジョン機能を使用して画像を解析できます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###エディターがOpenAIを使用して画像を処理します（作成/編集/変更）

チャットツールで新しい画像チャットを作成し、会話設定をOpenAIに変更してパラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

画像を作成します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

画像を編集して、「会話 Image Chat Type」を「編集」に変更し、元の画像と、透明な部分（アルファチャンネルが0）が修正が必要な場所を示すマスク画像の2つをアップロードしてください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

画像を変更して、会話イメージタイプを「変異」に変更し、画像をアップロードします。OpenAIは元の画像の変異を返します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###ブループリントは OpenAI モデルチャットを使用します。

青写真で「Send OpenAI Chat Request In World」というノードを作成するには、右クリックしてください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Options ノードを作成して、`Stream=true, Api Key="you api key from OpenAI"` を設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Messagesを作成し、System MessageとUser Messageをそれぞれ追加してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Delegate を作成して、モデルの出力情報を受け取り、画面に表示します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完璧な設計図はこういう見た目だ。この設計図を稼働させると、ゲーム画面に大きなモデルがプリントされたメッセージが表示される。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###OpenAIを使用して画像を生成する設計図

青写真でノード「Send OpenAI Image Request」を右クリックして作成し、「In Prompt="a beautiful butterfly"」を設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Options ノードを作成し、`Api Key="OpenAI から取得したあなたの API キー"` を設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

画像に On Images イベントをバインドし、画像をローカルディスクに保存します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

完璧な設計図はこう見える。この設計図を実行すると、画像は指定された場所に保存される。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###エディターはAzureを使用しています。

新しいチャットを作成して、ChatApiをAzureに変更し、AzureのAPIパラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

チャットを開始します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###エディターを使用してAzureで画像を作成します。

新しい画像チャットセッション（New Image Chat）に移行し、ChatApi をAzureに変更し、AzureのAPIパラメータを設定します。ただし、dall-e-2モデルの場合は、パラメータQualityとStypeをnot_useに設定する必要があります。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

チャットを開始し、Azureに画像を作成させる

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###設計図を使った Azure チャット

以下の手順に従い、Azureオプションを設定し、実行をクリックしてください。そうすると、Azureから返されたチャット情報が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Azureを使用して設計図に画像を作成する

以下のブループリントを作成し、Azure Optionsを設定して、「実行」ボタンをクリックします。画像の作成に成功した場合、画面に「Create Image Done」というメッセージが表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

上記の設定に基づいて、画像はパス D:\Dwnloads\butterfly.png に保存されます。

## Claude

###エディターは、Claudeを使用してチャットして画像を分析します。

「新規チャット（New Chat）」を作成し、ChatApiをClaudeに変更して、ClaudeのAPIパラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

チャットを始める

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###設計図を使用して、クロードは画像を分析しています。

青写真で、ノード「Send Claude Chat Request」を右クリックして作成してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Options ノードを作成し、`Stream=true、Api Key="Clude からの API キー", Max Output Tokens=1024` と設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Messagesを作成し、ファイルからTexture2Dを作成し、Texture2DからAIChatPlusTextureを作成し、AIChatPlusTextureをMessageに追加します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Create an event just like the tutorial above and print the information on the game screen.

詳細な設計図は次のようになります。この設計図を実行すると、ゲーム画面に大きなモデルが表示されるメッセージが表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Ollamaを取得

Ollama公式ウェブサイトからインストーラーをローカルにダウンロードしてインストールできます：[ollama.com](https://ollama.com/)

Ollama を他の人から提供された Ollama インターフェースを通じて利用することができます。

###エディターはOllamaを使ってチャットし、画像を分析します。

新しいチャットを作成して、ChatApiをOllamaに変更し、OllamaのAPIパラメータを設定します。テキストチャットの場合はllama3.1などのテキストモデルにモデルを設定し、画像を処理する場合はvisionをサポートするモデル（moondreamなど）に設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

話を始める

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Ollamaを使ってブループリントを使ってチャットや画像の分析を行います。

以下のブループリントを作成し、Ollama Optionsを設定し、実行をクリックすると、Ollamaが返信したチャット情報が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###エディターはジェミニを使用します。

新規チャットを開始し、ChatApiをGeminiに変更してGeminiのApiパラメータを設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

チャットを開始する

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###ブループリントを使用してGeminiでチャットする

以下の手順に従い、Gemini Optionsを設定し、実行ボタンをクリックすると、Geminiからのチャット情報が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)


##更新履歴

### v1.4.1 - 2025.01.04

####問題修正

チャットツールは、画像のみ送信できる機能をサポートしています。

OpenAI のインターフェースの画像送信問題を修正できなかった文書の図を翻訳してください。

OpanAIとAzureのチャットツール設定で見落とされていたQuality、Style、ApiVersionパラメータの問題を修正しました。

### v1.4.0 - 2024.12.30

####新機能

（実験的機能）Cllama（llama.cpp）は、マルチモードモデルをサポートし、画像を処理できます。

すべてのブループリントのタイプのパラメーターには詳細なヒントが追加されました。

### v1.3.4 - 2024.12.05

####新機能

OpenAIはVision APIをサポートしています。

####問題修復

OpenAI stream=false のエラーを修正します

### v1.3.3 - 2024.11.25

####新しい機能

* Support for UE-5.5

####問題修復

一部藍写真が機能しない問題を修正します。

### v1.3.2 - 2024.10.10

####問題修復

手動停止リクエスト時の cllama のクラッシュを修正

商城のダウンロードバージョンwinの問題を修正する：ggml.dll、llama.dllファイルが見つからない問題。

GameThread 中进行的 CreateRequest 检查

### v1.3.1 - 2024.9.30

####新功能

システムテンプレートビューアーを追加しました。数百ものシステム設定テンプレートを閲覧および使用できます。

####問題修復

商城からダウンロードしたプラグインを修復すると、llama.cpp でリンクライブラリが見つかりません。

LLAMACpp のパスが長すぎる問題を修正

Windows パッケージング後のリンク llama.dll エラーを修正します。

iOSおよびAndroidのファイルパスの読み取り問題を修正します。

Cllameの設定名の修正

### v1.3.0 - 2024.9.23

####重要な新機能

llama.cpp has been integrated to support offline execution of large models locally.

### v1.2.0 - 2024.08.20

####新しい機能

OpenAI Image Edit/Image Variationのサポート

Ollama APIをサポートし、Ollamaがサポートするモデルリストを自動的に取得する。

### v1.1.0 - 2024.08.07

####新しい機能

支持ブループリント

### v1.0.0 - 2024.08.05

####新機能

基礎完備の機能

OpenAI、Azure、Claude、Gemini をサポートします。

組み込みされた高機能エディタ付きチャットツール

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。[**反響**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
Translate this text into Japanese language:
どんな見落としがあったか教えてください。 
