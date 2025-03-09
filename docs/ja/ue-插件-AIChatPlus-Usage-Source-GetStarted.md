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

#C++ の部 - はじめに

##コアコードの説明

現在、プラグインは以下のモジュールに分かれています：

**AIChatPlusCommon**: ランタイムモジュール（Runtime）は、さまざまなAI APIインターフェースのリクエスト送信と応答コンテンツの解析を担当しています。

AIChatPlusEditor: エディターモジュール（Editor）、エディターAIチャットツールの実装を担当しています。

AIChatPlusCllama：ランタイムモジュール（Runtime）は、llama.cppのインターフェースとパラメータをカプセル化し、大規模モデルのオフライン実行を実現します。

* **Thirdparty/LLAMACpp**: ランタイムにおけるサードパーティモジュールで、llama.cpp のダイナミックライブラリとヘッダーファイルが統合されています。

UClass でリクエストを送信する責任を持つのは、FAIChatPlus_xxxChatRequest です。各種 API サービスごとに独立したリクエスト UClass があります。応答は UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase の 2 種類の UClass を通じて取得され、対応するコールバックデリゲートを登録する必要があります。

API のパラメータと送信メッセージを設定する必要があります。FAIChatPlus_xxxChatRequestBody を使用して設定します。応答の具体的な内容はFAIChatPlus_xxxChatResponseBody に解析され、コールバックを受け取った際には、特定のインターフェースを介して ResponseBody を取得できます。

##コードはオフラインモデルCllama(llama.cpp)を使用しています。

こちらは、コード内でオフラインモデル llama.cpp を使用する方法についての説明です。

最初に、Content/LLAMA フォルダにモデルファイルをダウンロードする必要があります。

コードを修正して、1つのコマンドを追加し、そのコマンドでオフラインモデルにメッセージを送信します。

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

再コンパイル後、Cmdエディターでコマンドを使用すると、OutputLogで大規模モデルの出力結果を確認できます。

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されています。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)指摘された＠場云🈲なエリアを示してください。 
