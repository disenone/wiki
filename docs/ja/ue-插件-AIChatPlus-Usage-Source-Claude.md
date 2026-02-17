---
layout: post
title: Claude
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
- Claude
- Anthropic
description: Claude
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Claude" />

#C++編 - Claude

本ドキュメントでは、C++でAnthropic Claude APIを使用してチャット、画像分析、Tool Callingを行う方法について説明します。

##準備作業

ご使用前に以下のことを確認してください：

1. プロジェクトの`.Build.cs`ファイルにモジュール依存関係を追加：

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

2. 必要なヘッダーファイルを含める：

```cpp
#include "Common_Claude/AIChatPlus_ClaudeChatRequest.h"
```

##テキストチャット

###基本テキストチャット

```cpp
#include "Common_Claude/AIChatPlus_ClaudeChatRequest.h"

void UMyClass::SendClaudeChatRequest()
{
// 配置オプション
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-anthropic-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;  // ストリーム出力を有効にする
    Options.MaxOutputTokens = 1024;
    Options.Temperature = 0.7f;

// Claude のシステムプロンプトは Options.System で設定されます
    Options.System = TEXT("You are a helpful assistant.");

// ユーザーメッセージを作成
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("What is the capital of France?"), EAIChatPlus_ChatRole::User});

// リクエストを作成
    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    // コールバックのバインド
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Claude: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Token Usage: %s"), *Response.Usage.GetDescription());
        UE_LOG(LogTemp, Display, TEXT("Stop Reason: %s"), *Response.StopReason);
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

###マルチターン会話

```cpp
void UMyClass::MultiTurnClaudeChat()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant with a good memory.");

// 複数ターンの対話履歴を構築（Systemを含まず、ClaudeのSystemはOptions内にある）
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("My name is Bob."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("Hello Bob! Nice to meet you. How can I assist you today?"), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my name?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);
// モデルはユーザー名がBobであることを覚えておくべき
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##Vision（画像分析）

Claude 3シリーズのモデルはVision機能をサポートしており、画像の内容を分析できます。

> **注意**: Claude Visionは最大20枚の画像をサポートします（`FAIChatPlus_Constants::FClaude::MaxSendImageNum = 20`）。

###ファイルから画像を読み込んで解析

```cpp
#include "Common_Claude/AIChatPlus_ClaudeChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithClaude()
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

// オプションの配置
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
オプション.モデル = テキスト("claude-3-5-sonnet-20240620");  // Claude 3 シリーズを使用
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant that can analyze images.");

// 画像付きメッセージを作成する
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("Please describe this image in detail.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Claude Vision: %s"), *Message);
    });

    Request->SendRequest();
}
```

###マルチイメージ解析

```cpp
void UMyClass::AnalyzeMultipleImages()
{
// 複数画像を読み込む
    TArray<UAIChatPlus_Texture*> ChatTextures;

    TArray<FString> ImagePaths = {
        FPaths::ProjectContentDir() / TEXT("Images/image1.png"),
        FPaths::ProjectContentDir() / TEXT("Images/image2.png"),
        FPaths::ProjectContentDir() / TEXT("Images/image3.png")
    };

    for (const FString& Path : ImagePaths)
    {
        if (UTexture2D* Texture = UAIChatPlus_Util::LoadImage(Path))
        {
            ChatTextures.Add(UAIChatPlus_Texture::CreateFromTexture2D(Texture));
        }
    }

    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant.");

// 複数の画像を含むメッセージを作成する
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("Compare these images and describe the differences.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images = ChatTextures;

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Comparison: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##ツールコーリング（関数呼び出し）

Claude は Tool Calling をサポートしており、モデルが事前定義された関数を呼び出すことができます。

###ツールを定義し、リクエストを送信する

```cpp
void UMyClass::SendClaudeToolCallRequest()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant. Use tools when needed.");

// ツール定義：天気を取得する
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");

// ツールパラメータを定義
    FAIChatPlus_ChatRequestToolProperty LocationProp;
    LocationProp.Name = TEXT("location");
    LocationProp.Description = TEXT("The city name, e.g. Tokyo, Paris, New York");
    LocationProp.Type = TEXT("string");
    LocationProp.Required = true;

    FAIChatPlus_ChatRequestToolProperty UnitProp;
    UnitProp.Name = TEXT("unit");
    UnitProp.Description = TEXT("The temperature unit: celsius or fahrenheit");
    UnitProp.Type = TEXT("string");
    UnitProp.Required = false;

    WeatherTool.Properties.Add(LocationProp);
    WeatherTool.Properties.Add(UnitProp);

    Options.Tools.Add(WeatherTool);

// オプション：ToolChoiceの設定
    // Options.ToolChoice.Type = TEXT("auto");  // auto, any, or tool
    // Options.ToolChoice.Name = TEXT("get_weather");  // Type == "tool" の場合のみ使用

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("What's the weather like in Paris?"), EAIChatPlus_ChatRole::User}});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);

// 停止理由が tool_use かどうかを確認する
        if (Response.StopReason == TEXT("tool_use"))
        {
            TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
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

###Tool Call 結果の処理

```cpp
void UMyClass::HandleClaudeToolCallResult()
{
// これはモデルが返したTool Call情報だと仮定します
    FString ToolCallId = TEXT("toolu_01abc123");
    FString FunctionName = TEXT("get_weather");
    FString FunctionResult = TEXT("{\"temperature\": 18, \"unit\": \"celsius\", \"description\": \"Cloudy\"}");

    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant. Use tools when needed.");

// ツールを再定義する
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");
    Options.Tools.Add(WeatherTool);

// メッセージ履歴の構築
    TArray<FAIChatPlus_ChatRequestMessage> Messages;

    // 1. ユーザーのオリジナルの質問
    Messages.Add({TEXT("What's the weather like in Paris?"), EAIChatPlus_ChatRole::User});

// 2. AssistantのTool使用リクエスト
    FAIChatPlus_ChatRequestMessage AssistantMessage;
    AssistantMessage.Role = EAIChatPlus_ChatRole::Assistant;
    AssistantMessage.Content = TEXT("");

    FAIChatPlus_ChatRequestToolCall ToolCallUse;
    ToolCallUse.Id = ToolCallId;
    ToolCallUse.Type = TEXT("function");
    ToolCallUse.FunctionName = FunctionName;
    ToolCallUse.FunctionArguments = TEXT("{\"location\": \"Paris\"}");
    AssistantMessage.ToolCallUses.Add(ToolCallUse);
    Messages.Add(AssistantMessage);

// 3. ツールの実行結果
    FAIChatPlus_ChatRequestMessage ToolResultMessage;
    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;

    FAIChatPlus_ChatRequestToolCallResult ToolResult;
    ToolResult.Id = ToolCallId;
    ToolResult.FunctionName = FunctionName;
    ToolResult.FunctionResult = FunctionResult;
    ToolResultMessage.ToolCallResults.Add(ToolResult);
    Messages.Add(ToolResultMessage);

// リクエストを送信する
    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###完全なTool Callサイクル

```cpp
// 会話履歴の保存
TArray<FAIChatPlus_ChatRequestMessage> ClaudeConversation;
FAIChatPlus_ClaudeChatRequestOptions ClaudeOptions;

void UMyClass::InitializeClaudeToolChat()
{
    ClaudeOptions.ApiKey = TEXT("your-api-key");
    ClaudeOptions.Model = TEXT("claude-3-5-sonnet-20240620");
    ClaudeOptions.bStream = true;
    ClaudeOptions.System = TEXT("You are a helpful assistant. Use tools to get real-time information.");

// ツールを定義
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get weather for a location.");

    FAIChatPlus_ChatRequestToolProperty Prop;
    Prop.Name = TEXT("location");
    Prop.Type = TEXT("string");
    Prop.Required = true;
    WeatherTool.Properties.Add(Prop);

    ClaudeOptions.Tools.Add(WeatherTool);

// 会話履歴をクリア
    ClaudeConversation.Empty();
}

void UMyClass::SendClaudeUserMessage(const FString& UserMessage)
{
    ClaudeConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(ClaudeOptions, ClaudeConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.StopReason == TEXT("tool_use"))
        {
            ProcessClaudeToolCalls(Response.GetToolCalls(), Response.GetMessage());
        }
        else
        {
            FString AssistantMessage = Response.GetMessage();
            ClaudeConversation.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});
            OnClaudeResponse(AssistantMessage);
        }
    });

    Request->SendRequest();
}

void UMyClass::ProcessClaudeToolCalls(const TArray<FAIChatPlus_ChatResponseToolCall>& ToolCalls, const FString& AssistantContent)
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
    ClaudeConversation.Add(AssistantMsg);

    // ツールを実行して結果を追加する
    FAIChatPlus_ChatRequestMessage ToolResultMsg;
    ToolResultMsg.Role = EAIChatPlus_ChatRole::Tool;

    for (const auto& ToolCall : ToolCalls)
    {
        FString Result = ExecuteClaudeTool(ToolCall.FunctionName, ToolCall.FunctionArguments);

        FAIChatPlus_ChatRequestToolCallResult ToolResult;
        ToolResult.Id = ToolCall.Id;
        ToolResult.FunctionName = ToolCall.FunctionName;
        ToolResult.FunctionResult = Result;
        ToolResultMsg.ToolCallResults.Add(ToolResult);
    }
    ClaudeConversation.Add(ToolResultMsg);

    // 会話を続ける
    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(ClaudeOptions, ClaudeConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.StopReason == TEXT("tool_use"))
        {
            ProcessClaudeToolCalls(Response.GetToolCalls(), Response.GetMessage());
        }
        else
        {
            FString FinalMessage = Response.GetMessage();
            ClaudeConversation.Add({FinalMessage, EAIChatPlus_ChatRole::Assistant});
            OnClaudeResponse(FinalMessage);
        }
    });

    Request->SendRequest();
}

FString UMyClass::ExecuteClaudeTool(const FString& FunctionName, const FString& Arguments)
{
    if (FunctionName == TEXT("get_weather"))
    {
// 実際に天気のクエリを実行する
        return TEXT("{\"temperature\": 18, \"unit\": \"celsius\", \"description\": \"Cloudy\"}");
    }

    return TEXT("{\"error\": \"Unknown tool\"}");
}

void UMyClass::OnClaudeResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Claude: %s"), *Response);
}
```

##高度な設定

###JSON 拡張オプションを使用する

```cpp
void UMyClass::UseClaudeExtraOptions()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");

// 追加のJSONオプションを追加
    Options.ExtraJsonString = TEXT("{\"metadata\": {\"user_id\": \"12345\"}}");

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###カスタムエンドポイントURL

```cpp
void UMyClass::UseCustomClaudeEndpoint()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");

// カスタムエンドポイント（プロキシサーバーなど）を使用する
    Options.BaseUrl = TEXT("https://your-proxy-server.com");
    Options.EndPointUrl = TEXT("v1/messages");

// または完全な URL を直接設定する
    // Options.FullUrl = TEXT("https://your-proxy-server.com/v1/messages");

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###Anthropicバージョンの設定

```cpp
void UMyClass::SetAnthropicVersion()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");

// APIバージョンを設定
    Options.AnthropicVersion = TEXT("2023-06-01");

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

##エラー処理

```cpp
void UMyClass::RobustClaudeRequest()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->OnStartedListeners.AddLambda([]()
    {
        UE_LOG(LogTemp, Display, TEXT("Claude request started..."));
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.HasError())
        {
            UE_LOG(LogTemp, Error, TEXT("Response error: %s"), *Response.Error.GetDescription());
            return;
        }

        UE_LOG(LogTemp, Display, TEXT("Success: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Stop Reason: %s"), *Response.StopReason);
        UE_LOG(LogTemp, Display, TEXT("Tokens: %s"), *Response.Usage.GetDescription());
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
UAIChatPlus_ClaudeChatRequest* CurrentClaudeRequest = nullptr;

void UMyClass::StartClaudeRequest()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;

    CurrentClaudeRequest = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a very long essay about AI."), EAIChatPlus_ChatRole::User}});

    CurrentClaudeRequest->SendRequest();
}

void UMyClass::CancelClaudeRequest()
{
    if (CurrentClaudeRequest && CurrentClaudeRequest->IsActivated())
    {
        CurrentClaudeRequest->StopRequest();
        UE_LOG(LogTemp, Display, TEXT("Claude request cancelled"));
    }
}
```

--8<-- "footer_ja.md"


> この投稿はChatGPTによって翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指摘すべき抜け目があればご指摘ください。 
