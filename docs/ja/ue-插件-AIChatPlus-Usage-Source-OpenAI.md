---
layout: post
title: OpenAI / Azure
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
description: OpenAI / Azure
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - OpenAI / Azure" />

#C++編 - OpenAI / Azure

このドキュメントでは、C++でOpenAIおよびAzure APIを使用して、チャット、画像分析、音声入出力、およびTool Callingを実行する方法について説明します。

> **注意**: Azure API は OpenAI と互換性があり、使い方はほぼ同じです。変更が必要なのは `BaseUrl` と `ApiKey` だけです。

##準備作業

使用前に、以下の点を確認してください：

1. プロジェクトの `.Build.cs` ファイルにモジュール依存関係を追加します：

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

2. 必要なヘッダーファイルを含める：

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"
#include "Common/AIChatPlus_Log.h"
```

##テキストチャット

###基本テキストチャット

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"

void UMyClass::SendOpenAIChatRequest()
{
// 配置オプション
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-openai-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;  // ストリーム出力を有効にする
    Options.Temperature = 0.7f;
    Options.MaxOutputTokens = 1024;

// メッセージを作成
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is the capital of France?"), EAIChatPlus_ChatRole::User});

// リクエストを作成
    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// コールバックをバインド
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Message: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Token Usage: %s"), *Response.Usage.GetDescription());
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_OpenAIChatResponseError>();
        UE_LOG(LogTemp, Error, TEXT("Request Failed: %s"), *Error.GetDescription());
    });

// リクエストを送信
    Request->SendRequest();
}
```

###Azure APIを使用する

Azure APIはOpenAIと互換性があり、URLと認証方法を変更するだけで利用できます：

```cpp
#include "Common_Azure/AIChatPlus_AzureChatRequest.h"

void UMyClass::SendAzureChatRequest()
{
    FAIChatPlus_AzureChatRequestOptions Options;
    Options.ApiKey = TEXT("your-azure-api-key");
Options.ResourceName = TEXT("あなたのリソース名");  // Azure リソース名
Options.DeploymentName = TEXT("あなたのデプロイ名");  // デプロイ名
    Options.ApiVersion = TEXT("2024-02-01");  // API バージョン
    Options.bStream = true;

    auto Request = UAIChatPlus_AzureChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System},
            {TEXT("Hello!"), EAIChatPlus_ChatRole::User}
        });

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Azure Message: %s"), *Message);
    });

    Request->SendRequest();
}
```

###マルチターン対話

```cpp
void UMyClass::MultiTurnConversation()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

// 複数ターンの対話履歴を構築する
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("My name is Alice."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("Hello Alice! Nice to meet you. How can I help you today?"), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my name?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
// モデルはユーザー名がAliceであることを覚えていられるべきです
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##ビジョン（画像分析）

OpenAIのVision機能により、モデルは画像の内容を分析することができます。

###ファイルから画像を読み込み解析する

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageFromFile()
{
// ファイルから画像を読み込む
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image: %s"), *ImagePath);
        return;
    }

// プラグインで使用可能な Texture オブジェクトを作成する
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

// オプションを配置する
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
Options.Model = TEXT("gpt-4o");  // Vision には gpt-4o または gpt-4-turbo が必要です
    Options.bStream = true;

// 画像付きのメッセージを作成
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("What is in this image? Describe it in detail.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant that can analyze images."), EAIChatPlus_ChatRole::System},
            ImageMessage
        });

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Vision Analysis: %s"), *Message);
    });

    Request->SendRequest();
}
```

###テクスチャ2Dから分析（ゲーム内スクリーンショット）

```cpp
void UMyClass::AnalyzeGameTexture(UTexture2D* GameTexture)
{
    if (!GameTexture)
    {
        UE_LOG(LogTemp, Error, TEXT("Invalid texture"));
        return;
    }

// プラグインTextureに変換
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(GameTexture);

    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o");
    Options.bStream = true;

    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("Analyze this game screenshot and describe what you see.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options, {{TEXT("You are a game analyst."), EAIChatPlus_ChatRole::System}, ImageMessage});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Game Analysis: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##Audio（音声入力・出力）

OpenAIは音声入力と音声出力機能をサポートしています（`gpt-4o-audio-preview`モデルが必要です）。

###音声入力（スピーチ・トゥ・テキスト）

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::SendAudioMessage()
{
// ファイルから音声を読み込む
    FString AudioPath = FPaths::ProjectContentDir() / TEXT("Audio/question.wav");
    USoundWave* SoundWave = UAIChatPlus_Util::LoadSoundWav(AudioPath);

    if (!SoundWave)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load audio: %s"), *AudioPath);
        return;
    }

// プラグインで使用可能な Sound オブジェクトを作成する
    UAIChatPlus_Sound* ChatSound = UAIChatPlus_Sound::CreateFromSoundWave(SoundWave);

// 配置オプション
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
Options.Model = TEXT("gpt-4o-audio-preview");  // 音声対応モデル
Options.bStream = false;  // オーディオ出力はストリーミングをサポートしていません

// オーディオ付きメッセージを作成する
    FAIChatPlus_ChatRequestMessage AudioMessage;
AudioMessage.Content = TEXT("");  // オーディオメッセージにはテキストが不要な場合があります
    AudioMessage.Role = EAIChatPlus_ChatRole::User;
    AudioMessage.Audios.Add(ChatSound);

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant. Listen to the audio and respond."), EAIChatPlus_ChatRole::System},
            AudioMessage
        });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Response to audio: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###音声出力（テキスト読み上げ）

```cpp
void UMyClass::RequestAudioOutput()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-audio-preview");
    Options.bStream = false;  // オーディオ出力はストリーミングをサポートしていません

// オーディオ出力を設定
    Options.Modalities.Add(EAIChatPlus_OpenAIChatModality::Text);
    Options.Modalities.Add(EAIChatPlus_OpenAIChatModality::Audio);
    Options.AudioConfig.Format = TEXT("wav");
Options.AudioConfig.Voice = TEXT("alloy");  // オプション: alloy, ash, ballad, coral, echo, sage, shimmer, verse

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System},
            {TEXT("Tell me a short joke."), EAIChatPlus_ChatRole::User}
        });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

// テキスト応答を取得する
        UE_LOG(LogTemp, Display, TEXT("Text Response: %s"), *Response.GetMessage());

// 音声応答を取得する
        TArray<FAIChatPlus_ChatResponseAudioOutput> AudioOutputs = Response.GetAudioOutputs();
        for (const auto& AudioOutput : AudioOutputs)
        {
            if (AudioOutput.Sound)
            {
// オーディオを再生する
// AudioOutput.Sound は UAIChatPlus_Sound* であり、その中の USoundWave を取得できます
                UE_LOG(LogTemp, Display, TEXT("Audio Transcript: %s"), *AudioOutput.Transcript);

// オーディオをファイルに保存
                FString SavePath = FPaths::ProjectSavedDir() / TEXT("Audio/response.wav");
                UAIChatPlus_Util::SaveSoundWav(AudioOutput.Sound->GetSoundWave(), SavePath);
            }
        }
    });

    Request->SendRequest();
}
```

##ツールコーリング（関数呼び出し）

Tool Callingにより、モデルは事前定義された関数を呼び出して外部データを取得できます。

###ツールを定義してリクエストを送信

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"

void UMyClass::SendToolCallRequest()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

// ツールの定義：天気を取得
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a location.");

// ツールパラメータを定義
    FAIChatPlus_ChatRequestToolProperty LocationProp;
    LocationProp.Name = TEXT("location");
    LocationProp.Description = TEXT("The city name, e.g. Beijing, Tokyo, New York");
    LocationProp.Type = TEXT("string");
    LocationProp.Required = true;

    FAIChatPlus_ChatRequestToolProperty UnitProp;
    UnitProp.Name = TEXT("unit");
    UnitProp.Description = TEXT("The temperature unit");
    UnitProp.Type = TEXT("string");
    UnitProp.Required = false;
    UnitProp.ExtraJsonString = TEXT("{\"enum\": [\"celsius\", \"fahrenheit\"]}");

    WeatherTool.Properties.Add(LocationProp);
    WeatherTool.Properties.Add(UnitProp);

    Options.Tools.Add(WeatherTool);

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant. Use tools when needed."), EAIChatPlus_ChatRole::System},
            {TEXT("What's the weather like in Tokyo?"), EAIChatPlus_ChatRole::User}
        });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

// Tool Callがあるかどうかをチェック
        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
            for (const auto& ToolCall : ToolCalls)
            {
                UE_LOG(LogTemp, Display, TEXT("Tool Call - ID: %s, Function: %s, Args: %s"),
                    *ToolCall.Id, *ToolCall.FunctionName, *ToolCall.FunctionArguments);

// ここで実際の関数呼び出しを実行し、結果をモデルに送り返します
// 下記の「Tool Call 結果の処理」例を参照
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

###ツールコール結果の処理

このモデルがツールコールを返した場合、関数を実行し結果をモデルに送り返す必要があります：

```cpp
void UMyClass::HandleToolCallAndSendResult()
{
// これはモデルが返した Tool Call だと仮定します
    FString ToolCallId = TEXT("call_abc123");
    FString FunctionName = TEXT("get_weather");
    FString FunctionResult = TEXT("{\"temperature\": 22, \"unit\": \"celsius\", \"description\": \"Sunny\"}");

    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

// ツールを再定義（整合性を維持）
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a location.");
    Options.Tools.Add(WeatherTool);

// Tool Call の結果を含むメッセージ履歴を構築する
    TArray<FAIChatPlus_ChatRequestMessage> Messages;

// 1. システム メッセージ
    Messages.Add({TEXT("You are a helpful assistant. Use tools when needed."), EAIChatPlus_ChatRole::System});

    // 2. ユーザーのオリジナルの質問
    Messages.Add({TEXT("What's the weather like in Tokyo?"), EAIChatPlus_ChatRole::User});

// 3. AssistantのTool Callリクエスト
    FAIChatPlus_ChatRequestMessage AssistantMessage;
    AssistantMessage.Role = EAIChatPlus_ChatRole::Assistant;
アシスタントメッセージ.コンテンツ = TEXT("");  // ツールコール時はテキスト内容がない場合があります

    FAIChatPlus_ChatRequestToolCall ToolCallUse;
    ToolCallUse.Id = ToolCallId;
    ToolCallUse.Type = TEXT("function");
    ToolCallUse.FunctionName = FunctionName;
    ToolCallUse.FunctionArguments = TEXT("{\"location\": \"Tokyo\"}");
    AssistantMessage.ToolCallUses.Add(ToolCallUse);
    Messages.Add(AssistantMessage);

// 4. ツール実行結果
    FAIChatPlus_ChatRequestMessage ToolResultMessage;
    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;

    FAIChatPlus_ChatRequestToolCallResult ToolResult;
    ToolResult.Id = ToolCallId;
    ToolResult.FunctionName = FunctionName;
    ToolResult.FunctionResult = FunctionResult;
    ToolResultMessage.ToolCallResults.Add(ToolResult);
    Messages.Add(ToolResultMessage);

    // リクエストを送信する
    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
// モデルはツールの結果に基づいて最終的な返答を生成します
        UE_LOG(LogTemp, Display, TEXT("Final Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###完全なTool Callサイクル

以下は完全なTool Callingのループ例です：

```cpp
// 会話履歴の保存
TArray<FAIChatPlus_ChatRequestMessage> ConversationHistory;
FAIChatPlus_OpenAIChatRequestOptions CurrentOptions;

void UMyClass::InitializeToolChat()
{
    CurrentOptions.ApiKey = TEXT("your-api-key");
    CurrentOptions.Model = TEXT("gpt-4o-mini");
    CurrentOptions.bStream = true;

// ツールを定義
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a location.");

    FAIChatPlus_ChatRequestToolProperty LocationProp;
    LocationProp.Name = TEXT("location");
    LocationProp.Type = TEXT("string");
    LocationProp.Required = true;
    WeatherTool.Properties.Add(LocationProp);

    CurrentOptions.Tools.Add(WeatherTool);

// ダイアログの初期化
    ConversationHistory.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}

void UMyClass::SendUserMessage(const FString& UserMessage)
{
    ConversationHistory.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(CurrentOptions, ConversationHistory);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
// ツールコールの処理
            ProcessToolCalls(ToolCalls, Response.GetMessage());
        }
        else
        {
// 通常の返信
            FString AssistantMessage = Response.GetMessage();
            ConversationHistory.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});
            OnAssistantResponse(AssistantMessage);
        }
    });

    Request->SendRequest();
}

void UMyClass::ProcessToolCalls(const TArray<FAIChatPlus_ChatResponseToolCall>& ToolCalls, const FString& AssistantContent)
{
// Assistant の Tool Call メッセージを追加
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
    ConversationHistory.Add(AssistantMsg);

// 各ツールを実行して結果を追加する
    FAIChatPlus_ChatRequestMessage ToolResultMsg;
    ToolResultMsg.Role = EAIChatPlus_ChatRole::Tool;

    for (const auto& ToolCall : ToolCalls)
    {
        FString Result = ExecuteTool(ToolCall.FunctionName, ToolCall.FunctionArguments);

        FAIChatPlus_ChatRequestToolCallResult ToolResult;
        ToolResult.Id = ToolCall.Id;
        ToolResult.FunctionName = ToolCall.FunctionName;
        ToolResult.FunctionResult = Result;
        ToolResultMsg.ToolCallResults.Add(ToolResult);
    }
    ConversationHistory.Add(ToolResultMsg);

    // ツール結果を含むリクエストを送信する
    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(CurrentOptions, ConversationHistory);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> NewToolCalls = Response.GetToolCalls();
        if (NewToolCalls.Num() > 0)
        {
// ツールの呼び出しを続ける必要があるかもしれません
            ProcessToolCalls(NewToolCalls, Response.GetMessage());
        }
        else
        {
            FString FinalMessage = Response.GetMessage();
            ConversationHistory.Add({FinalMessage, EAIChatPlus_ChatRole::Assistant});
            OnAssistantResponse(FinalMessage);
        }
    });

    Request->SendRequest();
}

FString UMyClass::ExecuteTool(const FString& FunctionName, const FString& Arguments)
{
    if (FunctionName == TEXT("get_weather"))
    {
// パラメータを解析し、実際の天気クエリを実行する
// ここでは模擬データを返します
        return TEXT("{\"temperature\": 22, \"unit\": \"celsius\", \"description\": \"Sunny\"}");
    }

    return TEXT("{\"error\": \"Unknown function\"}");
}

void UMyClass::OnAssistantResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Assistant: %s"), *Response);
}
```

##画像生成

OpenAIのDALL-Eモデルを使用して画像を生成：

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIImageRequest.h"

void UMyClass::GenerateImage()
{
    FAIChatPlus_OpenAIImageRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("dall-e-3");
    Options.ChatType = EAIChatPlus_ImageChatType::Generation;
    Options.Size = TEXT("1024x1024");
    Options.Quality = EAIChatPlus_OpenAIImageQuality::Standard;
    Options.ResponseFormat = EAIChatPlus_OpenAIImageResponseFormat::Url;

    auto Request = UAIChatPlus_OpenAIImageRequest::CreateWithOptions(Options);
    Request->SetPrompt(TEXT("A beautiful sunset over mountains, digital art style"));

    Request->OnImagesListeners.AddLambda([](const TArray<UTexture2D*>& Images, bool bFinished)
    {
        for (int32 i = 0; i < Images.Num(); ++i)
        {
            if (Images[i])
            {
// 画像を保存
                FString SavePath = FString::Printf(TEXT("%s/GeneratedImages/image_%d.png"),
                    *FPaths::ProjectSavedDir(), i);
                UAIChatPlus_Util::SaveImage(Images[i], SavePath);
                UE_LOG(LogTemp, Display, TEXT("Image saved to: %s"), *SavePath);
            }
        }
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_OpenAIChatResponseError>();
        UE_LOG(LogTemp, Error, TEXT("Image generation failed: %s"), *Error.GetDescription());
    });

    Request->SendRequest();
}
```

##高級設定

###JSON拡張オプションを使用する

`ExtraJsonString`または`ExtraJsonObject`を使用して、APIで直接サポートされていないオプションを追加します：

```cpp
void UMyClass::UseExtraJsonOptions()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");

    // JSON文字列を使用して追加オプションを追加する
    Options.ExtraJsonString = TEXT("{\"store\": false, \"metadata\": {\"user_id\": \"12345\"}}");

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###カスタムエンドポイント URL

カスタムAPIエンドポイント（例：プロキシサーバー）の使用をサポート：

```cpp
void UMyClass::UseCustomEndpoint()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");

// 方式1: BaseUrlとEndPointUrlを個別に設定する
    Options.BaseUrl = TEXT("https://your-proxy-server.com");
    Options.EndPointUrl = TEXT("v1/chat/completions");

// 方法 2: 完全なURLを直接設定する（BaseUrlとEndPointUrlは無視されます）
    // Options.FullUrl = TEXT("https://your-proxy-server.com/v1/chat/completions");

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

##エラー処理

###完全なエラー処理の例

```cpp
void UMyClass::RobustChatRequest()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->OnStartedListeners.AddLambda([]()
    {
        UE_LOG(LogTemp, Display, TEXT("Request started..."));
    });

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
// ストリーミングメッセージ
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

// レスポンスにエラーがあるかどうかをチェックする
        if (Response.HasError())
        {
            UE_LOG(LogTemp, Error, TEXT("Response error: %s"), *Response.Error.GetDescription());
            return;
        }

        UE_LOG(LogTemp, Display, TEXT("Success: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Tokens used: %s"), *Response.Usage.GetDescription());
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_OpenAIChatResponseError>();
        UE_LOG(LogTemp, Error, TEXT("Request failed!"));
        UE_LOG(LogTemp, Error, TEXT("  Code: %s"), *Error.Code);
        UE_LOG(LogTemp, Error, TEXT("  Type: %s"), *Error.Type);
        UE_LOG(LogTemp, Error, TEXT("  Message: %s"), *Error.Message);
        UE_LOG(LogTemp, Error, TEXT("  Param: %s"), *Error.Param);
    });

    Request->SendRequest();
}
```

##停止要求

実行中のリクエストは停止できます：

```cpp
// リクエストの参照を格納する
UPROPERTY()
UAIChatPlus_OpenAIChatRequest* CurrentRequest = nullptr;

void UMyClass::StartRequest()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    // ... 配置オプション

    CurrentRequest = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a very long story."), EAIChatPlus_ChatRole::User}});

    CurrentRequest->SendRequest();
}

void UMyClass::CancelRequest()
{
    if (CurrentRequest && CurrentRequest->IsActivated())
    {
        CurrentRequest->StopRequest();
        UE_LOG(LogTemp, Display, TEXT("Request cancelled"));
    }
}
```

--8<-- "footer_ja.md"


> この投稿はChatGPTで翻訳されたものです。ご意見・ご感想は[**こちら**](https://github.com/disenone/wiki_blog/issues/new)以下の抜けている点があれば指摘してください。 
