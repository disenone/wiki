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

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Get Started" />

#C++の部分 - スタートを切る

##コアコードの紹介

現在のプラグインは以下のモジュールに分かれています：

AIChatPlusCommon: ランタイムモジュールは、さまざまなAI APIインタフェースのリクエスト処理と応答内容の解析を担当しています。

AIChatPlusEditor: エディターモジュール（Editor），エディターAIチャットツールを実装する責任があります。

AIChatPlusCllama: ランタイムモジュール（Runtime）は、llama.cppのインターフェースとパラメータをカプセル化し、大規模モデルのオフライン実行を実現します。

Thirdparty/LLAMACpp: Runtimeサードパーティモジュールで、llama.cppのダイナミックライブラリとヘッダーファイルが統合されています。

具体責任を持つ UClass は FAIChatPlus_xxxChatRequest で、各種の API サービスにはそれぞれ独立した Request UClass があります。応答は UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase の２つの UClass を通じて取得し、適切なコールバックデリゲートを登録するだけです。

リクエストを送信する前に、APIのパラメータと送信するメッセージを設定する必要があります。これは、FAIChatPlus_xxxChatRequestBodyを使用して設定されます。応答の具体的な内容も、FAIChatPlus_xxxChatResponseBodyに解析され、コールバックを受信した時には、特定のインタフェースを使用してResponseBodyを取得できます。

##コードはオフラインモデルCllamaを使用します（llama.cpp）.

「llama.cpp」というオフラインモデルをコードで使用する方法についての説明が以下にあります。

ますます、Content/LLAMA にモデルファイルをダウンロードする必要があります。

コードを変更して、新しいコマンドを追加し、そのコマンドでオフラインモデルにメッセージを送信する。

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

再コンパイルした後、エディタのCmdでコマンドを使用すると、OutputLogで大規模モデルの出力結果を確認できます。

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

--8<-- "footer_ja.md"


> この投稿は ChatGPT によって翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)指摘された遺漏箇所を指摘してください。 
