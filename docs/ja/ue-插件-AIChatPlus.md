---
layout: post
title: UEプラグイン AIChatPlus 説明文書
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
description: UE プラグイン AIChatPlus 説明文書
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UEプラグインAIChatPlus説明文書

##公共倉庫

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##プラグイン取得

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##プラグインの概要

このプラグインは UE5.2+ をサポートしています。

UE.AIChatPlus は、Unreal Engine のプラグインであり、さまざまな GPT AI チャットサービスとの通信を実現しています。現在サポートされているサービスには、OpenAI（ChatGPT、DALL-E）、Azure OpenAI（ChatGPT、DALL-E）、Claude、Google Gemini、Ollama、llama.cpp のローカルオフラインがあります。今後もさらに多くのサービスプロバイダーをサポートする予定です。このプラグインは非同期 REST リクエストに基づいて実装されており、高効率で UE 開発者がこれらの AI チャットサービスに接続しやすくなっています。

同時に、UE.AIChatPlusにはエディターツールも含まれており、これらのAIチャットサービスを直接エディター内で使用して、テキストや画像を生成したり、画像を分析したりすることができます。

##使用説明書

###エディターチャットツール

メニューバーのツール -> AIChatPlus -> AIChatを選択すると、プラグインが提供するエディターのチャットツールを開くことができます。

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


ツールはテキスト生成、テキストチャット、画像生成、画像分析をサポートしています。

工具のインターフェースは大まかに次のようになります：

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####主要機能

* オフライン大モデル：llama.cppライブラリを統合し、ローカルでオフライン実行をサポートしています。

* テキストチャット：左下隅の `New Chat` ボタンをクリックして、新しいテキストチャットセッションを作成します。

* 画像生成：左下の「New Image Chat」ボタンをクリックして、新しい画像生成セッションを作成します。

* 画像分析：`New Chat` の一部のチャットサービスは、Claude や Google Gemini のように画像の送信をサポートしています。入力ボックスの上にある 🖼️ または 🎨 ボタンをクリックすることで、送信する必要がある画像を読み込むことができます。

* サポートブループリント (Blueprint)：テキストチャットや画像生成などの機能を実現するためのブループリント作成APIリクエストをサポートします。

* 現在のチャットロールを設定する：チャットボックスの上部にあるドロップダウンメニューで、現在送信するテキストのロールを設定できます。異なるロールをシミュレートすることで、AIチャットを調整できます。

* 清空会话：チャットボックス上部の ❌ ボタンを押すことで、現在の会話の履歴メッセージをクリアできます。

* ダイアログテンプレート：数百種類のダイアログ設定テンプレートが内蔵されており、よくある問題の処理に便利です。

* 全局設定：左下隅の `Setting` ボタンをクリックすると、全局設定ウィンドウが開きます。デフォルトのテキストチャット、画像生成の API サービスを設定し、各 API サービスの具体的なパラメータを設定できます。設定はプロジェクトのパス `$(ProjectFolder)/Saved/AIChatPlusEditor` に自動的に保存されます。

* 会話設定：チャットボックス上部の設定ボタンをクリックすると、現在の会話の設定ウィンドウが開きます。会話名の変更、使用するAPIサービスの変更がサポートされており、各会話が使用するAPIの具体的なパラメータを独立して設定できます。会話設定は自動的に `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions` に保存されます。

* チャット内容の編集：チャット内容にマウスをホバーすると、そのチャット内容の設定ボタンが表示され、内容の再生成、内容の修正、内容のコピー、内容の削除、下に内容を再生成する（ユーザーが役割の内容に対して）ことがサポートされます。

* 画像ブラウジング：画像生成について、画像をクリックすると画像ビューア（ImageViewer）が開き、画像をPNG/UEテクスチャとして保存することができます。テクスチャはコンテンツブラウザ（Content Browser）で直接確認でき、エディター内での画像使用が便利です。さらに、画像の削除、再生成、追加生成などの機能もサポートされています。Windowsのエディターでは、画像のコピーもサポートされており、画像をクリップボードに直接コピーすることができ、使用が便利です。セッション生成された画像は、各セッションフォルダーの下に自動的に保存されます。通常のパスは `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images` です。

ブループリント：

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

全局設定：

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

会話設定：

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

チャット内容を修正する：

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

画像ビューア：

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

オフライン大モデルを使用する

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

対話テンプレート

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###核心コードの紹介

現在、プラグインは以下のいくつかのモジュールに分かれています：

* AIChatPlusCommon: 実行時モジュール (Runtime)、さまざまな AI API インターフェースからのリクエストの処理と返信内容の解析を担当します。

* AIChatPlusEditor: 編集モジュール（Editor）は、編集者 AI チャットツールの実装を担当します。

* AIChatPlusCllama: 実行時モジュール (Runtime)で、llama.cpp のインターフェースとパラメータを封装し、大規模モデルのオフライン実行を実現します。

* Thirdparty/LLAMACpp: 実行時のサードパーティモジュール (Runtime) で、llama.cpp の動的ライブラリとヘッダーファイルを統合しています。

具体的にリクエストを送信する担当の UClass は FAIChatPlus_xxxChatRequest であり、各 API サービスにはそれぞれ独立した Request UClass があります。リクエストの返信は UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase の2種類の UClass を通じて取得され、対応するコールバックデリゲートを登録するだけで済みます。

リクエストを送信する前に、APIのパラメータと送信するメッセージを設定する必要があります。これには、FAIChatPlus_xxxChatRequestBodyを使用します。返信の具体的な内容は、FAIChatPlus_xxxChatResponseBodyに解析され、コールバックを受け取ったときに特定のインターフェースを通じてResponseBodyを取得することができます。

更なるソースコードの詳細は、UEストアで入手できます：[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###エディターツールはオフラインモデルCllama（llama.cpp）を使用します。

以下は AIChatPlus エディターツールでオフラインモデル llama.cpp を使用する方法についての説明です。

* まず、HuggingFace のウェブサイトからオフラインモデルをダウンロードします：[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

* モデルを特定のフォルダーに置きます。例えば、ゲームプロジェクトのディレクトリ Content/LLAMA の下に置いてください。

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

* AIChatPlusエディタツールを開く：Tools -> AIChatPlus -> AIChat、新しいチャットセッションを作成し、セッション設定ページを開く

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

* ApiをCllamaに設定し、カスタムApi設定を有効にし、モデル検索パスを追加して、モデルを選択します。

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

* チャットを始めましょう！！

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###エディタツールはオフラインモデルCllama(llama.cpp)を使用して画像を処理します。

* HuggingFace サイトからオフラインモデル MobileVLM_V2-1.7B-GGUF をダウンロードし、同様に Content/LLAMA ディレクトリに配置します：[ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)。

* セッションのモデルを設定する：

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

画像を送信してチャットを開始する

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###コードはオフラインモデル Cllama(llama.cpp) を使用しています。

以下の説明は、コード内でオフラインモデル llama.cpp を使用する方法です。

* まず、同様にモデルファイルを Content/LLAMA にダウンロードする必要があります。

* コードを修正し、コマンドを追加して、オフラインモデルにメッセージを送信します。

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

* 再コンパイル後、エディタCmdでコマンドを使用すると、ログOutputLogに大規模モデルの出力結果が表示されます。

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###青写真はオフラインモデル llama.cpp を使用します。

以下は、ブループリントでオフラインモデル llama.cpp を使用する方法についての説明です。

* ブループリント内で右クリックしてノード `Send Cllama Chat Request` を作成します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

* Options ノードを作成し、`Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"` を設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

* Messagesを作成し、それぞれシステムメッセージとユーザーメッセージを追加します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Delegateを作成してモデルの出力情報を受け取り、画面に表示します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* 完整なブループリントはこのようになります。ブループリントを実行すると、大きなモデルからのメッセージがゲーム画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###エディターは OpenAI チャットを使用しています

* チャットツールを開く Tools -> AIChatPlus -> AIChat、新しいチャットセッションを作成する New Chat、セッション ChatApi を OpenAI に設定し、インターフェースパラメータを設定する。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

* チャットを開始：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

* gpt-4o / gpt-4o-mini モデルに切り替えると、OpenAI の視覚機能を使用して画像を分析できます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###エディターは OpenAI を使用して画像を処理します（作成/変更/変種）

* チャットツールで新しい画像チャットを作成し、セッション設定をOpenAIに変更し、パラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

* 画像を作成する

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

* 画像を修正し、会話の Image Chat Type を Edit に変更し、オリジナル画像と、マスクの透明部分（アルファチャンネルが 0 の部分）を示す2枚の画像をアップロードします。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

* 画像のバリエーションを変更し、会話の画像チャットタイプをバリエーションに設定して、画像をアップロードすると、OpenAIは元の画像のバリエーションを返します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###蓝图使用 OpenAI 模型聊天の日本語翻訳は以下の通りです：

オープンAIモデルチャットを使用するブループリント

* ブループリント内で右クリックしてノード `Send OpenAI Chat Request In World` を作成します

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

* Optionsノードを作成し、`Stream=true, Api Key="あなたのOpenAIのAPIキー"`を設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

* メッセージを作成し、それぞれにシステムメッセージとユーザーメッセージを追加します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Delegate を作成し、モデルの出力情報を受け取り、画面に表示します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完全な設計図はこのように見え、設計図を実行すると、ゲーム画面に大きなモデルから返されたメッセージが表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###ブループリントはOpenAIを使用して画像を作成します。

* ブループリント内で右クリックしてノード `Send OpenAI Image Request` を作成し、 `In Prompt="a beautiful butterfly"` を設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

* Options ノードを作成し、`Api Key="あなたの OpenAI からの API キー"` を設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

* 画像にイベントをバインドし、画像をローカルハードディスクに保存します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

* 完整な青写真はこのように見え、青写真を実行すると、指定された場所に画像が保存されているのが確認できます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###エディターは Azure を使用しています

* 新しいチャット（New Chat）を作成し、ChatApiをAzureに変更し、AzureのAPIパラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

* チャットを始める

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###エディターは Azure を使用して画像を作成します。

* 新しい画像チャット（New Image Chat）で、ChatApiをAzureに変更し、AzureのAPIパラメータを設定します。注意してください、dall-e-2モデルの場合、パラメータQualityとStypeをnot_useに設定する必要があります。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

* チャットを開始し、Azure に画像を作成させます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###青写真は Azure チャットを使用します

以下の青写真を作成し、Azure Optionsを設定して、実行をクリックすると、画面にAzureから返されたチャットメッセージが表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###青写真を使用して Azure で画像を作成

次のブループリントを作成し、Azure Optionsを設定して実行をクリックします。画像の作成が成功すると、画面に「Create Image Done」というメッセージが表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

上記の設計に基づいて、画像はパス D:\Dwnloads\butterfly.png に保存されます。

## Claude

###エディターはClaudeを使用してチャットおよび画像を分析します。

* 新しいチャット（New Chat）を作成し、ChatApiをClaudeに変更し、ClaudeのApiパラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

* チャットを始める

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###ブループリントはClaudeチャットと画像分析を使用します。

* ブループリント内で右クリックしてノード `Send Claude Chat Request` を作成します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

* Options ノードを作成し、`Stream=true, Api Key="あなたの Clude からのAPIキー", Max Output Tokens=1024` を設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

* メッセージを作成し、ファイルから Texture2D を作成し、Texture2D から AIChatPlusTexture を作成し、AIChatPlusTexture をメッセージに追加します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

* 上記のチュートリアルと同様に、イベントを作成し、情報をゲーム画面に表示します。

* 完整なブループリントはこのように見えます。ブループリントを実行すると、ゲーム画面に大きなモデルからのメッセージが表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Ollamaを取得する

* Ollamaの公式サイトからインストーラをダウンロードしてローカルにインストールできます：[ollama.com](https://ollama.com/)

* 他の人が提供するOllamaインターフェースを通じてOllamaを使用できます。

###エディターはOllamaを使用してチャットと画像分析を行います。

* 新しいチャット（New Chat）では、ChatApiをOllamaに変更し、OllamaのApiパラメータを設定します。テキストチャットの場合は、モデルをテキストモデルに設定します（例：llama3.1）。画像処理が必要な場合は、ビジョンをサポートするモデルに設定します（例：moondream）。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

* チャットを始める

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###ブループリントはOllamaを使用してチャットと画像解析を行います。

以下のブループリントを作成し、Ollamaオプションを設定して、実行をクリックすると、画面にOllamaが返すチャット情報が表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###エディタはGeminiを使用しています。

* 新規チャット（New Chat）を作成し、ChatApiをGeminiに変更し、GeminiのApiパラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

* チャットを始める

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###青写真はGeminiチャットを使用します

以下のブループリントを作成し、Gemini Optionsを設定して実行をクリックすると、画面上にGeminiから返されたチャット情報が表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

## Deepseek

###エディターは Deepseek を使用しています。

* 新しいチャット（New Chat）を作成し、ChatApi を OpenAi に変更し、Deepseek の Api パラメータを設定します。新しい候補モデルを deepseek-chat と呼び、モデルを deepseek-chat に設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

* チャットを始める

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###ブループリントはDeepseekチャットを使用します。

以下のブループリントを作成し、Deepseekに関連するリクエストオプション（モデル、ベースURL、エンドポイントURL、ApiKeyなどのパラメータ）を設定します。実行ボタンをクリックすると、画面にGeminiから返されたチャット情報が表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##更新ログ

### v1.5.0 - 2025.01.29

####新機能

* ジェミニに音声をサポートする

* エディターツールは音声と録音の送信をサポートしています。

#### Bug Fix

* セッションコピー失敗のバグを修正する

### v1.4.1 - 2025.01.04

####問題修正

* チャットツールは画像のみを送信し、メッセージを送信しないことをサポートしています。

* OpenAIインターフェースの画像送信問題修正失敗文图

* OpanAI、Azure チャットツール設定でパラメータ Quality、Style、ApiVersion が欠落している問題を修正する=

### v1.4.0 - 2024.12.30

####新機能

* （実験的機能）Cllama(llama.cpp) はマルチモーダルモデルをサポートし、画像を処理することができます。

* 所有的蓝图类型参数都加上了详细提示

### v1.3.4 - 2024.12.05

####新機能

* OpenAIはvision APIをサポートしています

####問題修正

* OpenAI stream=false の際のエラーを修正しました

### v1.3.3 - 2024.11.25

####新機能

* UE-5.5をサポートしています

####問題修正

* 一部のブループリントが効果を発揮しない問題を修正しました。

### v1.3.2 - 2024.10.10

####問題修正

* 手動停止リクエストの際、cllamaがクラッシュする問題を修正しました。

* 修正したモールのダウンロード版のWindowsパッケージでggml.dllおよびllama.dllファイルが見つからない問題

* リクエストを作成する際に GameThread にいるか確認する、CreateRequest はゲームスレッドでチェックします

### v1.3.1 - 2024.9.30

####新機能

* システムテンプレートビューアを追加し、数百のシステム設定テンプレートを表示および使用できるようにします。

####問題修正

* マーケットプレイスからダウンロードしたプラグインの修正、llama.cpp のリンクライブラリが見つかりません

* LLAMACppのパスが長すぎる問題を修正しました

* Windowsでパッケージ化した後のリンク llama.dll エラーを修正する

* iOS/Androidのファイルパス読み取り問題を修正しました。

* Cllameの設定名の誤りを修正する

### v1.3.0 - 2024.9.23

####重大な新機能

* llama.cppを整合し、ローカルオフラインで大規模モデルを実行することをサポートしました。

### v1.2.0 - 2024.08.20

####新機能

* OpenAIの画像編集/画像バリエーションをサポートしています

* Ollama APIをサポートし、Ollamaがサポートするモデルのリストを自動取得する機能を提供します。

### v1.1.0 - 2024.08.07

####新機能

* ブループリントを支持する

### v1.0.0 - 2024.08.05

####新機能

* 基礎完全機能

* OpenAI、Azure、Claude、Geminiを支持します。

* 自带機能が充実したエディタチャットツール

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。フィードバックを[**こちら**](https://github.com/disenone/wiki_blog/issues/new)指摘された不足する部分。 
