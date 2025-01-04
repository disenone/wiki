---
layout: post
title: UEプラグインAIChatPlus説明書
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

#UEプラグインAIChatPlusの説明書

##公共倉庫

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##プラグイン入手

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##プラグインの紹介

This plugin supports UE5.2+.

UE.AIChatPlus は UnrealEngine のプラグインで、様々な GPT AI チャットサービスとの通信を実現します。現在サポートされているサービスには OpenAI（ChatGPT, DALL-E）、Azure OpenAI（ChatGPT, DALL-E）、Claude、Google Gemini、Ollama、llama.cpp ローカルオフライン が含まれています。将来的にはさらに多くのプロバイダーをサポートする予定です。この実装は非同期 REST リクエストに基づいており、高効率なパフォーマンスであり、UE 開発者がこれらのAIチャットサービスに簡単にアクセスできるようになっています。

UE.AIChatPlusには、編集ツールも含まれており、このツールを使用してAIチャットサービスを直接編集エディターで使用し、テキストや画像を生成し、画像を分析することができます。

##ご使用方法

###エディターチャットツール

メニューバーのTools -> AIChatPlus -> AIChat をクリックすると、プラグインが提供する編集ツールチャットが開きます。

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


ツールはテキスト生成、テキストチャット、画像生成、画像分析をサポートします。

ツールのインターフェースはおおむね次のようになります：

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####主要機能

オフラインビッグモデル：llama.cppライブラリを統合し、ローカルでのオフラインビッグモデルの実行をサポート

テキストチャット：左下の`New Chat`ボタンをクリックして、新しいテキストチャットセッションを作成します。

画像生成：左下の `New Image Chat` ボタンをクリックして新しい画像生成セッションを作成してください。

画像解析：`New Chat` のチャット機能では、Claude、Google Geminiなどの画像を送信することができます。送信したい画像を読み込むには、入力ボックスの上にある 🖼️ または 🎨 ボタンをクリックしてください。

サポートマップ（Blueprint）：サポートマップの作成APIリクエストをサポートし、テキストチャット、画像生成などの機能を実現します。

現在のチャットキャラクターを設定する：チャットボックス上のドロップダウンメニューで、現在のテキスト送信キャラクターを設定できます。AIチャットを調整するために、異なるキャラクターをシミュレートできます。

セッションクリア：チャットボックスの上部にある❌アイコンをタップすると、現在のセッションの履歴メッセージをクリアできます。

会話のテンプレート: 数百種類の会話設定テンプレートが組み込まれており、一般的な問題を簡単に処理できます。

全局設定：左下の「設定」ボタンをクリックすると、全局設定ウィンドウを開くことができます。デフォルトのテキストチャット、画像生成APIサービスを設定し、各APIサービスの具体的なパラメータを設定できます。設定は自動的にプロジェクトのパス `$(ProjectFolder)/Saved/AIChatPlusEditor` に保存されます。

会話の設定：チャットボックス上部の設定ボタンをクリックすると、現在の会話の設定ウィンドウが開きます。会話の名前を変更したり、使用されるAPIサービスを変更したり、各会話で使用するAPIの具体的なパラメータを個別に設定したりできます。 会話の設定は自動的に `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions` に保存されます。

チャット内容の編集：チャット内容上でマウスをホバーさせると、その個々のチャット内容の設定ボタンが表示され、内容の再生成、編集、コピー、削除、および下に新しい内容を生成する機能がサポートされます（ユーザーの役割であるコンテンツの場合）。

画像の閲覧：画像生成に関して、画像をクリックすると画像ビューア（ImageViewer）が開きます。PNG/UE Texture として画像を保存でき、Texture はコンテンツブラウザ（Content Browser）で直接閲覧でき、編集器内での画像の使用が容易になります。また、画像の削除、再生成、さらに多くの画像を生成する機能もサポートされています。Windows の編集器では、画像のコピーもサポートされており、画像をクリップボードに直接コピーして便利に使用できます。会話生成の画像は自動的に各会話フォルダーに保存され、通常のパスは `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images` です。

設計図:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

オール局面設定：

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

会話設定：

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

チャット内容を改変する:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

画像ビューアー：

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

オフラインでの大規模モデルの使用

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

対話テンプレート

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###コアコードの紹介

現在のプラグインは以下のモジュールに分かれています：

AIChatPlusCommon: The runtime module is responsible for processing various AI API interface requests and parsing reply content.

AIChatPlusEditor: エディターモジュール，AIチャットツールのエディターを実装する責任があります。

AIChatPlusCllama: Runtimeモジュールは、llama.cppのインターフェースとパラメータをカプセル化し、大規模モデルのオフライン実行を実現します。

Thirdparty/LLAMACpp: The runtime third-party module that integrates llama.cpp's dynamic library and header files.

具体責任を持つ UClass は FAIChatPlus_xxxChatRequest で、各種のAPIサービスにはそれぞれ独自のRequest UClass があります。応答は UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase の2つの UClass を介して取得し、対応するコールバックデリゲートを登録するだけです。

APIのパラメータと送信メッセージを設定する前に、FAIChatPlus_xxxChatRequestBodyを使用してこの部分を設定する必要があります。返信の具体的な内容も、FAIChatPlus_xxxChatResponseBodyに解析され、コールバックを受け取った時にはResponseBodyを特定のインタフェースで取得することができます。

UEストアで[AIC hatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###エディタツールは、オフラインモデルCllama(llama.cpp)を使用します。

AIChatPlusエディターツールでオフラインモデルllama.cppを使用する方法について説明します。

(https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

特定のフォルダーにモデルを保存してください。たとえば、ゲームプロジェクトのContent/LLAMAディレクトリに保存してください。

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

AIChatPlus ツールを開く: Tools -> AIChatPlus -> AIChat。新しいチャットセッションを作成し、セッション設定ページを開いてください。

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

API を Cllama に設定し、カスタム API 設定を有効にし、モデル検索パスを追加してモデルを選択します。

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

チャットを始めよう！

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###エディタツールはオフラインモデルCllama（llama.cpp）を使用して画像を処理します。

HuggingFace ウェブサイトから、MobileVLM_V2-1.7B-GGUF のオフラインモデルをダウンロードし、[ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but the text provided does not contain any content to be translated. If you have more text or information you would like to translate, please provide it. Thank you.

セッションモデルの設定：

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

画像を送って、チャットを始める

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###Cllama（llama.cpp）を使用したオフラインモデルのコード

コード内でオフラインモデル llama.cpp を使用する方法について説明します。

ます。

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

###テキストを日本語に翻訳します。

蓝图中のオフラインモデル llama.cpp の使用方法について説明します。

青写真で`Send Cllama Chat Request`というノードを右クリックして作成してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Optionsノードを作成し、「Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf」を設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

メッセージを作成し、システムメッセージとユーザーメッセージそれぞれを追加してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Delegateを作成し、モデルの出力情報を受け取り、その情報を画面に出力します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完全な設計図はこう見える。設計図を実行すると、ゲーム画面に返されるメッセージが大きなモデルで表示される。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###エディターは OpenAI チャットを使用しています。

チャットツールを開き、ツール -> AIChatPlus -> AIChatを選択し、新しいチャットセッション「New Chat」を作成し、会話「ChatApi」をOpenAIに設定し、インターフェースパラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

チャットを開始します：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

gpt-4o / gpt-4o-miniモデルに切り替えると、OpenAIのビジョン機能を使用して画像を分析できます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###エディターはOpenAIを使用して画像を処理します（作成/変更/変種）

チャットツールで新しい画像チャットを作成し、チャットの設定をOpenAIに変更してパラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

画像を作成します

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

画像を編集して、会話イメージの種類を「編集」に変更し、元の画像と、修正が必要な部分を透明にするためのマスク画像の2枚をアップロードしてください。透明な部分（アルファチャネルが0）が修正が必要な箇所を示します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

画像を変異させ、会話画像タイプを「変異」に変更して画像を1枚アップロードしてください。OpenAIは元の画像の変異版を返します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###開発図を使用して OpenAI のモデルとチャット

青写真でノード「Send OpenAI Chat Request In World」を右クリックして作成します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Options ノードを作成し、`Stream=true, Api Key="you api key from OpenAI"`を設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Messages を作成し、System Message と User Message をそれぞれ追加してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Delegate を作成し、モデルの出力情報を受け取り、画面に出力します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完璧な設計図は次のようになります。設計図を実行すると、ゲーム画面に大きなモデルが印刷されたメッセージが返されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###OpenAIを使用して、Blueprintは画像を作成します。

青写真で「Send OpenAI Image Request」ノードを右クリックして作成し、「In Prompt="a beautiful butterfly"」を設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Options ノードを作成し、`Api Key="OpenAIから提供されたAPIキー"` と設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

イメージにイベントをバインドして、画像をローカルディスクに保存します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

完全な設計図を見ると、そのように見えます。 設計図を実行すると、指定された場所に画像が保存されているのが見えます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###エディターはAzureを使用しています。

新しいチャットを開始し、ChatApiをAzureに変更してAzureのAPIパラメータを設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

チャットを開始します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###エディターを使って Azure で画像を作成します。

新しい画像チャットセッション（New Image Chat）を作成し、ChatApiをAzureに変更し、AzureのAPIパラメータを設定します。dall-e-2モデルの場合は、QualityとStypeパラメータをnot_useに設定する必要があります。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

チャットを開始し、Azureに画像を作成させます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Azure チャットで Blueprint を使用します。

以下の手順に従って、Azure オプションを設定してください。その後、実行ボタンをクリックすると、Azure から返されたチャット情報が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Azureで画像を作成するためにブループリントを使用します。

以下のブループリントを作成し、Azureのオプションを設定して、実行ボタンをクリックします。画像が正常に作成された場合、画面に「Create Image Done」というメッセージが表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

上記の設定にしたがって、画像はパス D:\Dwnloads\butterfly.png に保存されます。

## Claude

###エディターがClaudeを使用してチャットおよび画像を分析します。

新しいチャット（New Chat）を開始し、ChatApiをClaudeに変更して、ClaudeのAPIパラメータを設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

チャットを開始します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###青写真で Claude とチャットして画像を分析します。

設計図内で、ノード「Send Claude Chat Request」を右クリックで作成してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Options ノードを作成し、「Stream=true, Api Key="Clude から取得した API キー", Max Output Tokens=1024」と設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Messagesを作成し、ファイルからTexture2Dを作成し、Texture2DからAIChatPlusTextureを作成し、AIChatPlusTextureをMessageに追加します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

前述のチュートリアルに従って、イベントを作成し、情報をゲーム画面に表示します。

完全な設計図は以下のようになります。この設計図を実行すると、ゲーム画面に大きなモデルがプリントされたメッセージが表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Ollamaの取得

オラマガ公式サイトからインストールパッケージをダウンロードしてローカルにインストールすることができます：[ollama.com](https://ollama.com/)

他が提供するOllamaインタフェースを使用して、Ollamaを利用することができます。

###エディターはOllamaを使用してチャットや画像の分析を行います。

新しいチャットを作成し、ChatApiをOllamaに変更し、OllamaのAPIパラメータを設定します。テキストチャットの場合は、モデルをテキストモデル（たとえばllama3.1）に設定し、画像を処理する場合は、visionをサポートするモデル（例：moondream）に設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

チャットを開始します

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###ブループリントは、Ollamaを使用してチャットし、画像を分析します。

以下のブループリントを作成し、Ollama Optionsを設定した後、実行ボタンをクリックすれば、Ollamaから返されたチャット情報が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###エディターはジェミニを使用しています。

新規チャットを作成し、ChatApiをGeminiに変更してGeminiのAPIパラメータを設定してください。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

チャットを開始します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###設計図を使用してGeminiでチャットします。

以下の手順に従い、Gemini Optionsを設定し、実行ボタンをクリックすると、Geminiからのチャット情報が表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

## Deepseek

###エディターはDeepseekを使用しています。

新しいチャットを開始し、ChatApiをOpenAiに変更し、DeepseekのAPIパラメータを設定します。候補モデルをdeepseek-chatに追加し、モデルをdeepseek-chatに設定します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

チャットを開始します。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###ディープシークのチャットでのブループリントの使用

以下の手順に従い、Deepseekに関連するRequest Optionsを設定したブループリントを作成してください。これには、Model、Base Url、End Point Url、ApiKeyなどのパラメータを含めてください。実行をクリックすると、Geminiからのチャット情報が画面に表示されます。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##更新履歴

### v1.4.1 - 2025.01.04

####問題修復

チャットツールは画像だけを送信してメッセージを送信しないことをサポートしています。

OpenAI interfaceの画像送信の問題を修正できませんでした。

OpanAI、Azure チャットツールの設定で Quality、Style、ApiVersion パラメーターが抜けている問題を修正する。

### v1.4.0 - 2024.12.30

####新機能

（試験的機能）Cllama (llama.cpp) は多モードモデルをサポートし、画像を処理することができます。

すべての設計図のタイプパラメータには詳細なヒントが追加されました。

### v1.3.4 - 2024.12.05

####新機能

OpenAIはビジョンAPIをサポートしています。

####問題を修正

OpenAI ストリーム=false のエラーを修正します。

### v1.3.3 - 2024.11.25

####新機能

* Support UE-5.5
* UE-5.5をサポート

####問題の修正

一部分の設計図の不具合を修正します。

### v1.3.2 - 2024.10.10

####問題修復

手動停止リクエストの修正時に、`cllama`がクラッシュする問題を修正しました。

商城のダウンロード版Winパッケージでggml.dllやllama.dllファイルが見つからない問題を修正します。

ゲームスレッド内でCreateRequestを確認します。

### v1.3.1 - 2024.9.30

####新しい機能

SystemTemplateViewerを追加し、数百のsystem設定テンプレートを表示および使用できるようにしました。

####問題修復

商城からダウンロードしたプラグインを修正すると、llama.cpp でリンクライブラリが見つかりません。

LLAMACpp パスの長さの問題を修正

Windows パッケージング後のリンク llama.dll のエラーを修正します。

iOS/Android のファイルパス読み込みの問題を修正

Cllameの設定名の修正

### v1.3.0 - 2024.9.23

####重要な新機能

llama.cpp が統合され、大規模モデルのローカルオフライン実行をサポートします。

### v1.2.0 - 2024.08.20

####新機能

OpenAI Image Edit/Image Variationをサポートします。

Ollama APIに対応し、Ollamaサポートモデルのリストを自動的に取得する。

### v1.1.0 - 2024.08.07

####新機能

サポートプラン

### v1.0.0 - 2024.08.05

####新機能

基礎完整機能

OpenAI、Azure、Claude、Gemini を支持します。

組み込みの優れたエディター付きチャットツール

--8<-- "footer_ja.md"


> この投稿はChatGPTを使って翻訳されています。ご意見や[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。→ どのような見落としも指摘してください。 
