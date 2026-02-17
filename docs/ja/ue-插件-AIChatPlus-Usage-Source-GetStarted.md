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

#C++ 編 - 始めよう

##モジュール紹介

プラグインは以下のモジュールに分かれています：

* **AIChatPlusCommon**: ランタイムモジュール（Runtime）。さまざまなAI APIインターフェースへのリクエスト送信と返信内容の解析を担当します。
* **AIChatPlusEditor**: エディタモジュール（Editor）、エディタ用AIチャットツールの実装を担当します。
* **AIChatPlusCllama**: ランタイムモジュール（Runtime）、llama.cppのインターフェースとパラメータをカプセル化し、オフラインでの巨大モデルの実行を実現する役割を担います。
* **Thirdparty/LLAMACpp**: ランタイムサードパーティモジュール (Runtime)、llama.cppの動的ライブラリとヘッダーファイルを統合しました。

##核心理念

ソースコードを使用する前に、いくつかのコアクラスとそれらの関係を理解する必要があります：

###Request（リクエスト）

`UAIChatPlus_ChatRequestBase` はすべてのチャットリクエストの基底クラスです。各APIプロバイダーには対応するサブクラスがあります：

* `UAIChatPlus_OpenAIChatRequest` - OpenAIチャットリクエスト
* `UAIChatPlus_AzureChatRequest` - Azureチャットリクエスト
* `UAIChatPlus_ClaudeChatRequest` - Claudeチャットリクエスト
* `UAIChatPlus_GeminiChatRequest` - Gemini チャットリクエスト
* `UAIChatPlus_OllamaChatRequest` - Ollama チャットリクエスト
* `UAIChatPlus_CllamaChatRequest` - Cllama オフラインモデルリクエスト
* `UAIChatPlus_CllamaServerChatRequest` - CllamaServer ローカルサーバーリクエスト

Requestオブジェクトは、リクエストパラメータの設定、リクエストの送信、コールバックの受信を担当します。

###ハンドラー（処理器）

`UAIChatPlus_ChatHandlerBase` は、リクエストのコールバックを統一管理するためのオプショナルなハンドラークラスです。

Handlerは以下の委譲を提供します：

* `OnStarted` - リクエスト開始時にトリガーされる
* `OnMessage` - ストリーミングメッセージを受信したときにトリガーされます（ストリーミング出力）
* `OnUpdated` - 更新を受信したときにトリガーされます
* `OnFinished` - リクエスト完了時にトリガーされます
* `OnFailed` - リクエストが失敗したときにトリガーされます

**ハンドラを使用するタイミングは？**

* 複数のリクエストのコールバックロジックを一元管理する必要がある場合
* ブループリントとC++間でコールバックロジックを共有する必要がある場合
* `OnStartedListeners` のような Request のデリゲートを直接使用しても、コールバックの監視を実現できます

###オプション（選択肢）

各APIプロバイダーには、対応するOptions構造体があり、APIパラメータを設定するために使用されます：

* `FAIChatPlus_OpenAIChatRequestOptions` - OpenAIオプション（ApiKey、Model、Temperatureなど）
* `FAIChatPlus_ClaudeChatRequestOptions` - Claudeオプション
* `FAIChatPlus_GeminiChatRequestOptions` - Gemini オプション
* などなど...

Optionsには、APIキー、エンドポイントURL、モデル名、生成パラメータなど、API接続に必要なすべての設定が含まれています。

###メッセージ（メッセージ）

`FAIChatPlus_ChatRequestMessage`はAIに送信されるメッセージ構造体であり、以下の内容を含みます：

* `コンテンツ` - テキスト内容
* `ロール` - メッセージの役割（System/User/Assistant/Developer/Tool）
* `Images` - 画像配列（Vision機能）
* `Audios` - オーディオ配列（Audio 機能）
* `ToolCallUses` - ツールコールリクエスト
* `ToolCallResults` - ツールコール結果

###レスポンス

各APIプロバイダーにはそれぞれ対応するResponseBody構造体があります：

* `FAIChatPlus_OpenAIChatResponseBody`
* `FAIChatPlus_ClaudeChatResponseBody`
* 待って...

ResponseBodyには、AIから返されるすべての情報が含まれています。これには、メッセージテキスト、トークン使用量、ツール呼び出し、オーディオ出力などが該当します。

##基本使用フロー（5ステップモデル）

AIChatPlusを使用してリクエストを送信する基本的な流れは以下の通りです：

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"

void SendChatRequest()
{
    // ===== ステップ 1: ハンドラの作成（オプション） =====
    // Handlerはコールバックを一元管理するために使用され、Requestのデリゲートを直接使用することもできます
    TWeakObjectPtr<UAIChatPlus_ChatHandlerBase> Handler = UAIChatPlus_ChatHandlerBase::New();

// ===== ステップ 2: Optionsの設定 =====
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
Options.bStream = true;  // ストリーミング出力を有効にする

// ===== ステップ 3: リクエストの作成 =====
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("Hello, who are you?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// ===== ステップ 4: コールバックのバインド =====
// 方法 A: Handlerを使用する
    Handler->BindChatRequest(Request);
    Handler->OnMessage.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Stream Message: %s"), *Message);
    });
    Handler->OnFinished.AddLambda([](const FAIChatPlus_ChatResponseBodyBase& Response)
    {
        UE_LOG(LogTemp, Display, TEXT("Request Finished"));
    });
    Handler->OnFailed.AddLambda([](const FAIChatPlus_ResponseErrorBase& Error)
    {
        UE_LOG(LogTemp, Error, TEXT("Request Failed: %s"), *Error.GetDescription());
    });

// 方式 B: リクエストの委譲を直接使用（ハンドラーは不要）
    // Request->OnMessageListeners.AddDynamic(this, &UMyClass::OnMessageReceived);
    // Request->OnFinishedListeners.AddDynamic(this, &UMyClass::OnRequestFinished);

    // ===== 手順 5: リクエストを送信する =====
    Request->SendRequest();
}
```

##簡略表記

精度の高いコールバック制御が必要なければ、より簡潔な記述が可能です：

```cpp
void SendSimpleChatRequest()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System},
            {TEXT("Hello!"), EAIChatPlus_ChatRole::User}
        });

    // Request に直接 Lambda をバインド
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Message: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final Message: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##APIプロバイダーの列挙を使用してリクエストを作成する

設定に基づいてAPIプロバイダーを動的に選択する必要がある場合、ファクトリメソッドを使用できます：

```cpp
void CreateRequestByProvider(EAIChatPlus_ChatApiProvider Provider)
{
// 列挙型に基づいて対応するリクエストを作成する
    auto Request = UAIChatPlus_ChatRequestBase::CreateByApi(Provider);

// 実際のタイプに基づいてOptionsを設定する
    switch (Provider)
    {
    case EAIChatPlus_ChatApiProvider::OpenAI:
        {
            auto OpenAIRequest = Cast<UAIChatPlus_OpenAIChatRequest>(Request);
            FAIChatPlus_OpenAIChatRequestOptions Options;
            Options.ApiKey = TEXT("your-api-key");
            OpenAIRequest->SetOptions(Options);
        }
        break;

    case EAIChatPlus_ChatApiProvider::Claude:
        {
            auto ClaudeRequest = Cast<UAIChatPlus_ClaudeChatRequest>(Request);
            FAIChatPlus_ClaudeChatRequestOptions Options;
            Options.ApiKey = TEXT("your-api-key");
            ClaudeRequest->SetOptions(Options);
        }
        break;
    // ... その他の Provider
    }

// メッセージを設定して送信
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Hello!"), EAIChatPlus_ChatRole::User});
    Request->SetMessages(Messages);
    Request->SendRequest();
}
```

##コールバック説明

###主なコールバック委託

| 委託 | トリガータイミング | パラメーター |
|------|----------|------|
| `OnStarted` | リクエストの送信開始時 | なし |
| `OnMessage` | ストリーミングメッセージを受信した時（各トークンごと） | `const FString& Message` - 累積されたメッセージ内容 |
| `OnUpdated` | レスポンスの更新を受け取った時 | `const FAIChatPlus_ResponseBodyBase& Response` |
| `OnFinished` | リクエストが正常に完了した時 | `const FAIChatPlus_ResponseBodyBase& Response` |
| `OnFailed` | リクエストが失敗した時 | `const FAIChatPlus_ResponseErrorBase& Error` |
| `OnMessageFinished` | メッセージ受信完了時 | `const FAIChatPlus_MessageFinishedPayload& Payload` |

###ストリーミング出力 vs 非ストリーミング出力

* **ストリーミング出力** (`bStream = true`): `OnMessage` が複数回トリガーされ、毎回蓄積されたメッセージ内容を返します
* **非ストリーミング出力** (`bStream = false`)：`OnMessage` は完了時に一度だけトリガーされ、完全なメッセージを返します

##次へ

各APIプロバイダーの詳細なドキュメントを参照してください：

* [OpenAI / Azure 利用](ue-插件-AIChatPlus-Usage-Source-OpenAI.md)
* [Claude 使用](ue-插件-AIChatPlus-Usage-Source-Claude.md)
* [ジェミニ 使用](ue-插件-AIChatPlus-Usage-Source-Gemini.md)
* [Ollama 使用](ue-插件-AIChatPlus-Usage-Source-Ollama.md)
* [Cllama オフラインモデル](ue-插件-AIChatPlus-Usage-Source-Cllama.md)
* [CllamaServer ローカルサーバー](ue-插件-AIChatPlus-Usage-Source-CllamaServer.md)
* [ツール類](ue-插件-AIChatPlus-Usage-Source-Utils.md)

--8<-- "footer_ja.md"

> (https://github.com/disenone/wiki_blog/issues/new)どこか抜けている箇所を指摘してください。 
