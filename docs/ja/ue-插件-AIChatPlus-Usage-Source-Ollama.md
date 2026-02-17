---
layout: post
title: Ollama
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
- Ollama
- Local LLM
description: Ollama
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Ollama" />

#C++ 編 - Ollama

このドキュメントでは、C++でOllamaのローカルAPIを利用してチャット、画像分析、およびTool Callingを行う方法について説明します。

Ollamaはローカルで大規模言語モデルを実行するツールで、デフォルトのアドレスは`http://localhost:11434`です。

##準備作業

使用前に以下の点を確認してください：

1. **Ollamaをインストールして実行する**：[ollama.com](https://ollama.com)Ollamaをダウンロードしてインストールした後、必要なモデル（例：`ollama pull llama3.2`）をダウンロードしてください。

2. プロジェクトの `.Build.cs` ファイルにモジュール依存関係を追加する：

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

3. 必要なヘッダーファイルを含める：

```cpp
#include "Common_Ollama/AIChatPlus_OllamaChatRequest.h"
```

##テキストチャット

###基本テキストチャット

```cpp
#include "Common_Ollama/AIChatPlus_OllamaChatRequest.h"

void UMyClass::SendOllamaChatRequest()
{
// 配置オプション
    FAIChatPlus_OllamaChatRequestOptions Options;
Options.Model = TEXT("llama3.2");  // ダウンロード済みのモデルを使用
Options.BaseUrl = TEXT("http://localhost:11434");  // デフォルトアドレス
Options.bStream = true;  // ストリーム出力を有効にする
    Options.Temperature = 0.8f;

// Ollama はAPIキーを必要としません（ローカルサービス）

// メッセージを作成（Systemメッセージを含む）
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is 2+2?"), EAIChatPlus_ChatRole::User});

// リクエストを作成する
    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// コールバックをバインド
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Ollama: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Token Usage: %s"), *Response.Usage.GetDescription());
        UE_LOG(LogTemp, Display, TEXT("Done Reason: %s"), *Response.DoneReason);
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_ResponseErrorBase>();
        UE_LOG(LogTemp, Error, TEXT("Request Failed: %s"), *Error.GetDescription());
    });

// リクエストを送信
    Request->SendRequest();
}
```

###マルチターン対話

```cpp
void UMyClass::MultiTurnOllamaChat()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

// 多轮対話履歴を構築する
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("My name is Charlie."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("Hello Charlie! Nice to meet you."), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my name?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###Generate APIを使用する（チャットモード非対応）

```cpp
void UMyClass::UseOllamaGenerateAPI()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;
オプション.IsChat = false; // /api/chat ではなく /api/generate を使用する
オプション.システム = TEXT("あなたは役立つアシスタントです。");  // Chatモード以外でのみ有効

// Chatモード以外はユーザーメッセージが1つだけ必要
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Write a haiku about programming."), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Generated: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##ビジョン（画像解析）

VisionをサポートするOllamaモデル（例えば `llava`、`llama3.2-vision`）は画像の内容を分析できます。

###ファイルから画像を読み込み分析する

```cpp
#include "Common_Ollama/AIChatPlus_OllamaChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithOllama()
{
// ファイルから画像をロードする
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image: %s"), *ImagePath);
        return;
    }

// プラグインで使用可能な Texture オブジェクトを作成
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

// 配置オプション
    FAIChatPlus_OllamaChatRequestOptions Options;
Options.Model = TEXT("llama3.2-vision");  // Vision をサポートするモデルを使用
    Options.bStream = true;

// 画像付きメッセージの作成
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("What do you see in this image?");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Ollama Vision: %s"), *Message);
    });

    Request->SendRequest();
}
```

##ツールコーリング（関数呼び出し）

一部のOllamaモデルはTool Calling機能をサポートしています。

###ツールを定義してリクエストを送信

```cpp
void UMyClass::SendOllamaToolCallRequest()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
Options.Model = TEXT("llama3.2");  // Tool Callingをサポートするモデルであることを確認
    Options.bStream = true;

// ツールの定義：天気を取得する
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");

// ツールパラメーターを定義
    FAIChatPlus_ChatRequestToolProperty LocationProp;
    LocationProp.Name = TEXT("location");
    LocationProp.Description = TEXT("The city name, e.g. Tokyo, Paris");
    LocationProp.Type = TEXT("string");
    LocationProp.Required = true;

    WeatherTool.Properties.Add(LocationProp);
    Options.Tools.Add(WeatherTool);

    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What's the weather in London?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
            for (const auto& ToolCall : ToolCalls)
            {
                UE_LOG(LogTemp, Display, TEXT("Tool Call - ID: %s, Function: %s, Args: %s"),
                    *ToolCall.Id, *ToolCall.FunctionName, *ToolCall.FunctionArguments);
            }
        }
        else
        {
            UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
        }
    });

    Request->SendRequest();
}
```

###ツールコール結果を処理

```cpp
void UMyClass::HandleOllamaToolCallResult()
{
    FString ToolCallId = TEXT("call_123");
    FString FunctionName = TEXT("get_weather");
    FString FunctionResult = TEXT("{\"temperature\": 15, \"unit\": \"celsius\", \"description\": \"Rainy\"}");

    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

// ツールの再定義
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");
    Options.Tools.Add(WeatherTool);

// メッセージ履歴を構築
    TArray<FAIChatPlus_ChatRequestMessage> Messages;

// 1. システム ニュース
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});

    // 2. ユーザーの元の質問
    Messages.Add({TEXT("What's the weather in London?"), EAIChatPlus_ChatRole::User});

// 3. アシスタントのツールコールリクエスト
    FAIChatPlus_ChatRequestMessage AssistantMessage;
    AssistantMessage.Role = EAIChatPlus_ChatRole::Assistant;
    AssistantMessage.Content = TEXT("");

    FAIChatPlus_ChatRequestToolCall ToolCallUse;
    ToolCallUse.Id = ToolCallId;
    ToolCallUse.Type = TEXT("function");
    ToolCallUse.FunctionName = FunctionName;
    ToolCallUse.FunctionArguments = TEXT("{\"location\": \"London\"}");
    AssistantMessage.ToolCallUses.Add(ToolCallUse);
    Messages.Add(AssistantMessage);

// 4. ツールの実行結果
    FAIChatPlus_ChatRequestMessage ToolResultMessage;
    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;

    FAIChatPlus_ChatRequestToolCallResult ToolResult;
    ToolResult.Id = ToolCallId;
    ToolResult.FunctionName = FunctionName;
    ToolResult.FunctionResult = FunctionResult;
    ToolResultMessage.ToolCallResults.Add(ToolResult);
    Messages.Add(ToolResultMessage);

// リクエストを送信する
    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###完全なTool Callのサイクル

```cpp
// 会話履歴の保存
TArray<FAIChatPlus_ChatRequestMessage> OllamaConversation;
FAIChatPlus_OllamaChatRequestOptions OllamaOptions;

void UMyClass::InitializeOllamaToolChat()
{
    OllamaOptions.Model = TEXT("llama3.2");
    OllamaOptions.bStream = true;

// ツールを定義する
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get weather for a location.");

    FAIChatPlus_ChatRequestToolProperty Prop;
    Prop.Name = TEXT("location");
    Prop.Type = TEXT("string");
    Prop.Required = true;
    WeatherTool.Properties.Add(Prop);

    OllamaOptions.Tools.Add(WeatherTool);

// ダイアログの初期化（Systemメッセージを追加する）
    OllamaConversation.Empty();
    OllamaConversation.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}

void UMyClass::SendOllamaUserMessage(const FString& UserMessage)
{
    OllamaConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(OllamaOptions, OllamaConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
            ProcessOllamaToolCalls(ToolCalls, Response.GetMessage());
        }
        else
        {
            FString AssistantMessage = Response.GetMessage();
            OllamaConversation.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});
            OnOllamaResponse(AssistantMessage);
        }
    });

    Request->SendRequest();
}

void UMyClass::ProcessOllamaToolCalls(const TArray<FAIChatPlus_ChatResponseToolCall>& ToolCalls, const FString& AssistantContent)
{
// AssistantのTool Callメッセージを追加する
    FAIChatPlus_ChatRequestMessage AssistantMsg;
    AssistantMsg.Role = EAIChatPlus_ChatRole::Assistant;
    AssistantMsg.Content = AssistantContent;

    for (const auto& ToolCall : ToolCalls)
    {
        FAIChatPlus_ChatRequestToolCall Use;
        Use.Id = ToolCall.Id;
        Use.Type = ToolCall.Type;
        Use.FunctionName = ToolCall.FunctionName;
        Use.FunctionArguments = ToolCall.FunctionArguments;
        AssistantMsg.ToolCallUses.Add(Use);
    }
    OllamaConversation.Add(AssistantMsg);

// ツールを実行し結果を追加する
    FAIChatPlus_ChatRequestMessage ToolResultMsg;
    ToolResultMsg.Role = EAIChatPlus_ChatRole::Tool;

    for (const auto& ToolCall : ToolCalls)
    {
        FString Result = ExecuteOllamaTool(ToolCall.FunctionName, ToolCall.FunctionArguments);

        FAIChatPlus_ChatRequestToolCallResult ToolResult;
        ToolResult.Id = ToolCall.Id;
        ToolResult.FunctionName = ToolCall.FunctionName;
        ToolResult.FunctionResult = Result;
        ToolResultMsg.ToolCallResults.Add(ToolResult);
    }
    OllamaConversation.Add(ToolResultMsg);

// 会話を続ける
    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(OllamaOptions, OllamaConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
            ProcessOllamaToolCalls(ToolCalls, Response.GetMessage());
        }
        else
        {
            FString FinalMessage = Response.GetMessage();
            OllamaConversation.Add({FinalMessage, EAIChatPlus_ChatRole::Assistant});
            OnOllamaResponse(FinalMessage);
        }
    });

    Request->SendRequest();
}

FString UMyClass::ExecuteOllamaTool(const FString& FunctionName, const FString& Arguments)
{
    if (FunctionName == TEXT("get_weather"))
    {
        return TEXT("{\"temperature\": 15, \"unit\": \"celsius\", \"description\": \"Rainy\"}");
    }
    return TEXT("{\"error\": \"Unknown tool\"}");
}

void UMyClass::OnOllamaResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Ollama: %s"), *Response);
}
```

##モデルリストを取得

`UAIChatPlus_OllamaModelRequest` を使用すると、Ollama サーバーで利用可能なモデルのリストを取得できます。

```cpp
#include "Common_Ollama/AIChatPlus_OllamaModelRequest.h"

void UMyClass::GetOllamaModels()
{
    FAIChatPlus_OllamaModelRequestOptions Options;
オプション.ベースURL = テキスト("http://localhost:11434");  // デフォルトアドレス

    auto Request = UAIChatPlus_OllamaModelRequest::CreateWithOptions(Options);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaModelRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FString> ModelNames = Response.GetModelNames();
        for (const FString& ModelName : ModelNames)
        {
            UE_LOG(LogTemp, Display, TEXT("Available Model: %s"), *ModelName);
        }

// 詳細情報を取得
        for (const auto& Model : Response.Models)
        {
            UE_LOG(LogTemp, Display, TEXT("Model: %s, Size: %lld, Family: %s"),
                *Model.Name, Model.Size, *Model.Details.Family);
        }
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_ResponseErrorBase>();
        UE_LOG(LogTemp, Error, TEXT("Failed to get models: %s"), *Error.GetDescription());
    });

    Request->SendRequest();
}
```

##高度な設定

###Ollama固有パラメータ

```cpp
void UMyClass::ConfigureOllamaAdvanced()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

// サンプリングパラメータ
    Options.Temperature = 0.7f;
    Options.TopK = 40;           // Top-K サンプリング
オプション.トップP = 0.9f;         // ニュークリアス・サンプリング
オプション.MinP = 0.05f;        // Min-P サンプリング

    // Mirostat サンプリング（パープレキシティ制御用）
Options.Mirostat = 2;        // 0=無効, 1=Mirostat, 2=Mirostat 2.0
    Options.MirostatEta = 0.1f;
    Options.MirostatTau = 5.0f;

// コンテキストと生成制限
    Options.NumCtx = 4096;       // コンテキストウィンドウサイズ
    Options.NumPredict = 256;    // 最大生成トークン数

// 繰り返しペナルティ
    Options.RepeatLastN = 64;
    Options.RepeatPenalty = 1.1f;

// 停止シーケンス
    Options.StopSequences.Add(TEXT("\n\n"));

// モデル保持ロード時間
オプション.KeepAlive = 300;     // 秒

    // ランダムシード（再現性のある生成のために）
    Options.Seed = 42;

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###APIキーを使用（リモートOllama）

```cpp
void UMyClass::ConnectToRemoteOllama()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.BaseUrl = TEXT("https://your-ollama-server.com");
Options.ApiKey = TEXT("your-api-key");  // サーバー認証が必要な場合
    Options.bStream = true;

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello from remote!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###JSON拡張オプションを使用する

```cpp
void UMyClass::UseOllamaExtraOptions()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

// 追加のJSONオプションを追加する
    Options.ExtraJsonString = TEXT("{\"format\": \"json\"}");

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Return a JSON with name and age fields."), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

##エラー処理

```cpp
void UMyClass::RobustOllamaRequest()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->OnStartedListeners.AddLambda([]()
    {
        UE_LOG(LogTemp, Display, TEXT("Ollama request started..."));
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.HasError())
        {
            UE_LOG(LogTemp, Error, TEXT("Response error: %s"), *Response.Error.GetDescription());
            return;
        }

        UE_LOG(LogTemp, Display, TEXT("Success: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Done Reason: %s"), *Response.DoneReason);
        UE_LOG(LogTemp, Display, TEXT("Tokens: %s"), *Response.Usage.GetDescription());

// Ollama特有のパフォーマンスメトリクス
        UE_LOG(LogTemp, Display, TEXT("Total Duration: %lld ns"), Response.TotalDuration);
        UE_LOG(LogTemp, Display, TEXT("Load Duration: %lld ns"), Response.LoadDuration);
        UE_LOG(LogTemp, Display, TEXT("Eval Duration: %lld ns"), Response.EvalDuration);
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_ResponseErrorBase>();
        UE_LOG(LogTemp, Error, TEXT("Request failed: %s"), *Error.GetDescription());
    });

    Request->SendRequest();
}
```

##停止要求

```cpp
UPROPERTY()
UAIChatPlus_OllamaChatRequest* CurrentOllamaRequest = nullptr;

void UMyClass::StartOllamaRequest()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

    CurrentOllamaRequest = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a very long story."), EAIChatPlus_ChatRole::User}});

    CurrentOllamaRequest->SendRequest();
}

void UMyClass::CancelOllamaRequest()
{
    if (CurrentOllamaRequest && CurrentOllamaRequest->IsActivated())
    {
        CurrentOllamaRequest->StopRequest();
        UE_LOG(LogTemp, Display, TEXT("Ollama request cancelled"));
    }
}
```

--8<-- "footer_ja.md"


> この投稿はChatGPTによって翻訳されています。ご意見・ご感想は[**こちら**](https://github.com/disenone/wiki_blog/issues/new)以下の点で見落とした箇所があれば指摘してください。 
