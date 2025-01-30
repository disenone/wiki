---
layout: post
title: UE プラグイン AIChatPlus 説明文書
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

#UE プラグイン AIChatPlus 説明文書

##公共倉庫

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##プラグイン取得

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##プラグイン紹介

このプラグインは UE5.2+ をサポートしています。

UE.AIChatPlus は、UnrealEngine のプラグインです。このプラグインはさまざまな GPT AI チャットサービスと通信を実現しています。現在サポートされているサービスには、OpenAI（ChatGPT、DALL-E）、Azure OpenAI（ChatGPT、DALL-E）、Claude、Google Gemini、Ollama、llama.cpp ローカルオフラインがあります。将来的には、さらに多くのサービスプロバイダーをサポートする予定です。実装は非同期 REST リクエストに基づいており、パフォーマンスが高く、UE 開発者がこれらのAIチャットサービスにアクセスしやすくなっています。

UE.AIChatPlusには、エディターツールも含まれていて、このツールを使ってAIチャットサービスを直接編集して、テキストや画像を生成し、画像を解析することができます。

##ご使用方法

###エディターチャットツール

メニュー欄 Tools -> AIChatPlus -> AIChat を選択すると、プラグインが提供するエディターのチャットツールを開くことができます。

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


ツールはテキスト生成、テキストチャット、画像生成、画像分析をサポートしています。

工具のインターフェースは、大まかには次のようになります：

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####主要機能

* オフライン大モデル：llama.cppライブラリを統合し、ローカルでオフライン実行をサポートしています。

* テキストチャット：左下隅の `New Chat` ボタンをクリックして、新しいテキストチャットセッションを作成します。

画像生成: 左下の `New Image Chat` ボタンをクリックして、新しい画像生成セッションを作成します。

* 画像分析：`New Chat`の一部チャットサービスは、ClaudeやGoogle Geminiなどで画像の送信をサポートしています。送信する画像を読み込むには、入力ボックスの上にある 🖼️ または 🎨 ボタンをクリックしてください。

支持プラン（Blueprint）：サポートプランを作成するAPIリクエストで、テキストチャット、画像生成などの機能を実行します。

* 現在のチャットロールを設定する：チャットボックス上部のドロップダウンボックスで現在送信するテキストのロールを設定できます。異なるロールをシミュレートすることで、AIチャットを調整できます。

会話をクリア：チャットボックスの上にある❌のボタンをタップすると、現在の会話履歴をクリアできます。

* 対話テンプレート：数百種類の対話設定テンプレートが内蔵されており、よくある問題に便利に対処できます。

* 全局設定：左下隅の `Setting` ボタンをクリックすると、全体設定ウィンドウが開きます。デフォルトのテキストチャットや画像生成のAPIサービスを設定し、各APIサービスの具体的なパラメータを設定できます。設定はプロジェクトのパス `$(ProjectFolder)/Saved/AIChatPlusEditor` に自動的に保存されます。

* 会話設定：チャットボックス上部の設定ボタンをクリックすると、現在の会話の設定ウィンドウが開きます。会話名の変更、使用するAPIサービスの変更が可能で、各会話ごとに使用するAPIの具体的なパラメーターを独立して設定できます。会話設定は自動的に `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions` に保存されます。

* チャット内容の編集：チャット内容にマウスカーソルを合わせると、そのチャット内容の設定ボタンが表示されます。内容の再生成、修正、コピー、削除、下部での内容の再生成（ユーザーが役割の内容に対して）をサポートしています。

* 画像ブラウジング：画像生成において、画像をクリックすると画像ビューウィンドウ（ImageViewer）が開き、PNG/UEテクスチャとして画像を別名で保存することができます。テクスチャはコンテンツブラウザ（Content Browser）で直接確認できるため、エディタ内での画像利用が便利です。また、画像の削除、再生成、さらに多くの画像の生成などの機能もサポートしています。Windowsのエディタでは、画像をコピーすることも可能で、画像をクリップボードに直接コピーできるため、使用が簡単です。セッションで生成された画像は、各セッションフォルダの下に自動的に保存され、その通常のパスは`$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`です。

設計図：

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

全局設定：

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

会話設定：

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

チャット内容を修正する：

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

画像ビューア：

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

オフラインでの大規模モデルの使用

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

対話テンプレート

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###コアコードの紹介

現在のプラグインは、以下のモジュールに分かれています：

AIChatPlusCommon: The runtime module is responsible for handling various AI API interface requests and parsing response content.

* AIChatPlusEditor: エディタモジュール (Editor)、エディタAIチャットツールの実装を担当します。

* AIChatPlusCllama: ランタイムモジュール（Runtime）は、llama.cppのインターフェースとパラメータをカプセル化し、大規模モデルのオフライン実行を実現します。

* Thirdparty/LLAMACpp: 実行時のサードパーティモジュール (Runtime)で、llama.cpp の動的ライブラリとヘッダーファイルを統合しています。

具体的にリクエストを送信する責任を持つUClassはFAIChatPlus_xxxChatRequestであり、各APIサービスにはそれぞれ独立したRequest UClassがあります。リクエストの応答は、UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBaseの2つのUClassを通じて取得でき、対応するコールバックデリゲートを登録するだけで済みます。

リクエストを送信する前に、APIのパラメータと送信するメッセージを設定する必要があります。これにはFAIChatPlus_xxxChatRequestBodyを使用します。返信の具体的な内容はFAIChatPlus_xxxChatResponseBodyに解析されており、コールバックを受け取った際には特定のインターフェースを通じてResponseBodyを取得できます。

さらにソースコードの詳細は、UEストアで入手できます：[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###エディターツールはオフラインモデルCllama(llama.cpp)を使用します。

以下に、AIChatPlusエディターツールでオフラインモデル llama.cpp を使用する方法を説明します。

* まず、HuggingFaceのウェブサイトからオフラインモデルをダウンロードします：[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

* モデルを特定のフォルダーに置いてください。例えば、ゲームプロジェクトのディレクトリ Content/LLAMA に置くことができます。

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

* AIChatPlus エディターツールを開く：ツール -> AIChatPlus -> AIChat、新しいチャットセッションを作成し、セッション設定ページを開く

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

* ApiをCllamaに設定し、カスタムApi設定を有効にし、モデル検索パスを追加して、モデルを選択します。

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

チャットを始めよう!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###エディターツールはオフラインモデルCllama(llama.cpp)を使用して画像を処理します。

HuggingFace ウェブサイトからオフラインモデル MobileVLM_V2-1.7B-GGUF をダウンロードし、Content/LLAMA ディレクトリに配置してください：[ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)。

* セッションのモデルを設定する：

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

* 画像を送信してチャットを始める

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###コードはオフラインモデル Cllama(llama.cpp)を使用しています。

以下は、オフラインモデル llama.cpp をコード内で使用する方法について説明しています。

まず、同様にモデルファイルを Content/LLAMA にダウンロードする必要があります。

コードを変更して、1つのコマンドを追加し、そのコマンドでオフラインモデルにメッセージを送信します。

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

再コンパイルした後、エディターのCmdでコマンドを使用すると、OutputLogのログに大規模なモデルの出力結果が表示されます。

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###ブループリントはオフラインモデル llama.cpp を使用します。

以下に、ブループリントでオフラインモデル llama.cpp を使用する方法を説明します。

* ブループリントでノード `Send Cllama Chat Request` を右クリックして作成します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

* オプションノードを作成し、`Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`を設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

* Messagesを作成し、System MessageとUser Messageをそれぞれ追加します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Delegateを作成して、モデルの出力情報を受け取り、それを画面に表示します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完全な設計図はこう見えます。設計図を実行すると、ゲーム画面に大きなモデルが返されるメッセージが表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###エディタは OpenAI チャットを使用しています

これらのテキストを日本語に翻訳します:

* チャットツールを開く Tools -> AIChatPlus -> AIChat で、新しいチャットセッション New Chat を作成し、セッション ChatApi を OpenAI に設定し、インターフェースパラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

チャットを開始する:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

* gpt-4o / gpt-4o-mini モデルに切り替えると、OpenAI の視覚機能を使用して画像を分析できます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###エディタは OpenAI を使用して画像を処理します（作成/変更/変種）

* チャットツールで新しい画像チャットを作成し、会話設定をOpenAIに変更し、パラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

画像を作成します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

* 画像を修正し、会話の Image Chat Type を Edit に変更し、2つの画像をアップロードします。1つは元の画像、もう1つはマスクで、透明な部分（アルファチャンネルが0の部分）が修正が必要な箇所を示します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

画像を変異させ、会話 Image Chat Type を変更して Variation とし、画像をアップロードしてください。OpenAI は元の画像の変異を返します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###OpenAIモデルでのBlueprintの使用。

* ブループリント内で右クリックしてノード `Send OpenAI Chat Request In World` を作成します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

* オプションノードを作成し、`Stream=true, Api Key="あなたのOpenAIのAPIキー"`を設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

* Messagesを作成し、それぞれにSystem MessageとUser Messageを追加します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Delegateを作成し、モデルの出力情報を受け取り、画面に表示します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完璧な設計図はこう見えます。設計図を実行すれば、ゲーム画面に大きなモデルが出力されるメッセージを見ることができます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###ブループリントを使用して、OpenAI が画像を作成します。

右键点击蓝图中创建一个节点`Send OpenAI Image Request`，然后设置`In Prompt="a beautiful butterfly"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Options ノードを作成して、「Api Key="OpenAI から提供された API キー"」を設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

* イメージイベントにバインドし、画像をローカルハードディスクに保存する

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

完全な設計図はこう見える。設計図を実行すれば、指定された場所に画像が保存されているのが分かります。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###エディターはAzureを使用しています。

新しいチャットを作成し、ChatApiをAzureに変更してAzureのAPIパラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

* チャットを始める

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###エディターを使用して、Azure で画像を作成します。

新しい画像チャットセッション（New Image Chat）を作成し、ChatApiをAzureに変更し、AzureのAPIパラメータを設定します。dall-e-2モデルの場合は、QualityとStypeパラメータをnot_useに設定する必要があります。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

チャットを始めて、Azureに画像を作成させる

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Azure チャットを使用する設計図

以下の手順に従って、Azure Optionsを設定し、ブループリントを作成して、実行をクリックすると、Azureから返されるチャット情報が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###青写真を使用して Azure で画像を作成する

以下のブループリントを作成し、Azureオプションを設定し、実行をクリックします。画像の作成に成功した場合、画面に「Create Image Done」というメッセージが表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

上記のブループリントに従い、画像が D:\Downloads\butterfly.png のパスに保存されます。

## Claude

###エディターは、Claudeを使用してチャットし、画像を分析します。

* 新しいチャット（New Chat）で、ChatApiをClaudeに変更し、ClaudeのApiパラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

チャットを開始します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Blueprint utilizes Claude to chat and analyze images.

* ブループリントで右クリックしてノード `Send Claude Chat Request` を作成します

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Options ノードを作成し、`Stream=true, Api Key="Clude からの API キー", Max Output Tokens=1024` を設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

* メッセージを作成し、ファイルから Texture2D を作成し、Texture2D から AIChatPlusTexture を作成し、AIChatPlusTexture をメッセージに追加します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

* 上述のチュートリアルと同様に、イベントを作成し、情報をゲーム画面に表示します。

該藍圖的完整版本看起來像這樣，運行藍圖後可以在遊戲屏幕上看到返回的大型模型打印信息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Ollamaを取得する

Ollamaの公式ウェブサイトでインストールパッケージを入手し、ローカルにインストールすることができます：[ollama.com](https://ollama.com/)

他の人が提供するOllamaインターフェースを使用してOllamaを利用できます。

###エディタを使用して、Ollamaとチャットし、画像を分析します。

新しいチャットを作成し、ChatApiをOllamaに変更して、OllamaのAPIパラメータを設定します。テキストチャットの場合は、テキストモデル（例：llama3.1）に設定し、画像の処理が必要な場合は、visionをサポートするモデル（例：moondream）に設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

チャットを開始

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Ollamaを使用して、図面をチャットして画像を分析します。

以下の設計図を作成し、Ollama オプションを設定して、実行ボタンをクリックすると、Ollama から返されたチャット情報が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###編集者はGeminiを使用します。

* 新しいチャット（New Chat）を作成し、ChatApiをGeminiに変更し、GeminiのApiパラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

チャットを開始する

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###エディターはGeminiを使用して音声を送信します。

ファイルから音声を読み取る/アセットから音声を読み取る/マイクで音声を録音し、送信する音声を生成します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

チャットを開始します.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###「蓝图使用 Gemini 聊天」

以下のブループリントを作成し、Geminiオプションを設定してから実行をクリックすると、スクリーンにGeminiから返されたチャット情報が表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###音声を送信するためのブループリントをGeminiで使用する

以下のブループリントを作成し、オーディオの読み込みを設定し、Gemini Optionsを設定したら、実行をクリックします。これで、画面にGeminiがオーディオ処理後に返すチャット情報が表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###エディタはDeepseekを使用しています。

* 新しいチャットを作成し、ChatApiをOpenAiに変更し、DeepseekのAPIパラメータを設定します。Candidate Modelsを"deepseek-chat"として追加し、モデルを"deepseek-chat"に設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

* チャットを始める

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###ブループリントは Deepseek チャットを使用します

以下の手順に従い、Deepseekに関連するリクエストオプションを設定したブループリントを作成してください。これには、モデル、ベースURL、エンドポイントURL、APIキーなどのパラメータが含まれます。実行ボタンをクリックすると、Geminiから返されたチャット情報が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##更新履歴

### v1.5.1 - 2025.01.30

####新機能

* 只允许 Gemini 発音頻度

PCMDataを取得する方法を最適化し、音声データをB64に変換する際に音声データを展開します。

* リクエスト 増加2つのコールバック OnMessageFinished OnImagesFinished

* Gemini メソッドを最適化し、bStream に基づいてメソッドを自動取得します。

* 一部のブループリント関数を追加して、Wrapperから実際のタイプへの変換を容易にし、Response MessageとErrorを取得できるようにします。

#### Bug Fix

* Request Finishの多重呼び出し問題を修正しました。

### v1.5.0 - 2025.01.29

####新機能

* 支持Geminiの音声を提供する

* エディタツールは音声や録音の送信をサポートしています。

#### Bug Fix

セッションコピーが失敗するバグを修正します。

### v1.4.1 - 2025.01.04

####問題修正

チャットツールは画像のみを送信してメッセージを送信しない機能をサポートしています。

* OpenAI インターフェースの画像送信問題修正失敗文图

* OpanAI、Azure チャットツールの設定でパラメータ Quality、Style、ApiVersion の問題が修正されました。

### v1.4.0 - 2024.12.30

####新しい機能

（実験機能）Cllama（llama.cpp）は、マルチモードモデルをサポートし、画像を処理できます。

* 所有的蓝图类型参数都加上了详细提示

### v1.3.4 - 2024.12.05

####新しい機能

OpenAIはVision APIをサポートしています。

####問題修正

* OpenAIのstream=false時のエラーを修正しました

### v1.3.3 - 2024.11.25

####新機能

* Support UE-5.5

####問題修正

* 一部のブループリントが無効になる問題を修正しました

### v1.3.2 - 2024.10.10

####問題修復

* 修正: 手動停止リクエスト時にcllamaがクラッシュする問題

修复商城下载版本 win 打包找不到 ggml.dll llama.dll 文件的问题

GameThread 内で CreateRequest をチェックします。

### v1.3.1 - 2024.9.30

####新機能

* システムテンプレートビューアを追加して、数百のシステム設定テンプレートを表示および利用できるようにします。

####問題修正

商城からダウンロードしたプラグインを修正する際に、llama.cpp がリンクライブラリが見つからないというエラーが発生しています。

* LLAMACpp のパスが長すぎる問題を修正しました

Windowsのパッケージング後に発生するllama.dllのリンクエラーを修正

iOSおよびAndroidのファイルパスの読み取り問題を修正します。

Cllameの設定名の修正

### v1.3.0 - 2024.9.23

####重大な新機能

* llama.cppを統合し、ローカルオフラインでの大規模モデルの実行をサポートしました。

### v1.2.0 - 2024.08.20

####新しい機能

* OpenAI Image Edit/Image Variationをサポートしています

Ollama API をサポートし、Ollama がサポートするモデルリストを自動取得します。

### v1.1.0 - 2024.08.07

####新機能

* サポートブループリント

### v1.0.0 - 2024.08.05

####新機能

* 基础完整機能

* OpenAI、Azure、Claude、Geminiを支持します。

組み込みされた高機能エディター付きチャットツール

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されています。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 -> どんな見逃しも指摘してください。 
