---
layout: post
title: Cllama（廃止済み）
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
- Cllama
- llama.cpp
- Offline LLM
description: Cllama
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Cllama" />

#C++編 - Cllama（廃止済み）

##廃止済み

Cllamaは**廃止**としてマークされ、もはやメンテナンスされていません。

Cllamaの既存機能は[CllamaServer](ue-插件-AIChatPlus-Usage-Source-CllamaServer.md)来承载。

##オフラインモデル

この文書は、C++でCllama（llama.cppを統合）を使用してオフラインのローカル推論を行う方法について説明しています。

Cllamaは、大規模言語モデルをネットワーク接続なしで実行できるため、オフライン推論やプライバシー保護が求められるシナリオに最適です。

##準備作業

使用前に、以下の点を確認してください：

1. **GGUFモデルファイルをダウンロード**： [Hugging Face](https://huggingface.co)互換性のあるGGUF形式のモデルファイルをダウンロードする。

2. プロジェクトの `.Build.cs` ファイルにモジュール依存関係を追加する：

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

3. 必要なヘッダーファイルを含める：

```cpp
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"
```

##Cllamaの可用性を確認する

使用前に、Cllamaが利用可能かどうか、およびサポートされているバックエンドを確認できます：

```cpp
#include "Common/AIChatPlus_Util.h"

void UMyClass::CheckCllamaSupport()
{
// Cllamaが利用可能かチェックする
    if (UAIChatPlus_Util::Cllama_IsValid())
    {
        UE_LOG(LogTemp, Display, TEXT("Cllama is available"));

        // GPUサポートをチェック
        if (UAIChatPlus_Util::Cllama_IsSupportGpu())
        {
            UE_LOG(LogTemp, Display, TEXT("GPU acceleration is supported"));
        }

// サポートされているバックエンドリストを取得
        TArray<FString> Backends = UAIChatPlus_Util::Cllama_GetSupportBackends();
        for (const FString& Backend : Backends)
        {
            UE_LOG(LogTemp, Display, TEXT("Supported backend: %s"), *Backend);
        }
    }
    else
    {
        UE_LOG(LogTemp, Error, TEXT("Cllama is not available on this platform"));
    }
}
```

##テキストチャット

###基本的なテキストチャット

```cpp
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"

void UMyClass::SendCllamaChatRequest()
{
// 配置オプション
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
Options.bStream = true;  // ストリーム出力を有効にする
    Options.Temperature = 0.8f;
    Options.NumGpuLayers = 99;  // GPU アクセラレーションの層数（0 = CPUのみ）

// メッセージを作成
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is the meaning of life?"), EAIChatPlus_ChatRole::User});

// リクエストを作成
    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// コールバックをバインド
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Cllama: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Token Usage: %s"), *Response.Usage.GetDescription());
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_ResponseErrorBase>();
        UE_LOG(LogTemp, Error, TEXT("Request Failed: %s"), *Error.GetDescription());
    });

// リクエストを送信する
    Request->SendRequest();
}
```

###Content ディレクトリに対する相対パスを使用する

```cpp
void UMyClass::UseRelativeModelPath()
{
    FAIChatPlus_CllamaChatRequestOptions Options;

    // プロジェクトの Content ディレクトリに対する相対パス
    Options.ModelPath.FilePath = TEXT("Models/llama-3.2-1b-instruct-q4_k_m.gguf");

    Options.bStream = true;
    Options.NumGpuLayers = 99;

    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Hello!"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###Pakファイルからモデルをロード

```cpp
void UMyClass::LoadModelFromPak()
{
// Pakファイルにモデルがパッケージされている場合、モデルパスを準備する必要があります
    FString ModelPath = TEXT("Models/my_model.gguf");

// この関数はPak内のモデルを一時ディレクトリに解凍し、実際のパスを返します
    FString ActualPath = UAIChatPlus_Util::Cllama_PrepareModelPathFromPak(ModelPath);

    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = ActualPath;
    Options.bStream = true;

    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Hello from Pak!"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);
    Request->SendRequest();
}
```

###マルチターン対話

```cpp
void UMyClass::MultiTurnCllamaChat()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;

// マルチターン対話履歴を構築する
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("My favorite color is blue."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("That's a great choice! Blue is often associated with calmness."), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my favorite color?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###モデル保持ロード

```cpp
void UMyClass::KeepModelLoaded()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;

    // KeepAliveは、リクエスト後にモデルをロードした状態で保持する時間を制御します
// 0 = リクエスト後即時アンロード
    // -1 ＝ 永続的にロードを保持
    // >0 = 指定した秒数の間読み込みを維持する
Options.KeepAlive = -1;  // 永続的に読み込みを維持

    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Hello!"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);
    Request->SendRequest();
}
```

##ビジョン（画像解析）

CllamaはVision機能をサポートしており、マルチモーダルモデル（例：LLaVA）のサポートとMMProjectモデルファイルの提供が必要です。

> **注意**: Cllama Vision は最大1枚の画像をサポートしています（`FAIChatPlus_Constants::FCllama::MaxSendImageNum = 1`）。

###ファイルから画像を読み込んで解析する

```cpp
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithCllama()
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
    FAIChatPlus_CllamaChatRequestOptions Options;

// LLaVAモデルには2つのファイルが必要です：メインモデルとMMProjectモデル
    Options.ModelPath.FilePath = TEXT("D:/Models/llava-v1.6-mistral-7b.Q4_K_M.gguf");
    Options.MMProjectModelPath.FilePath = TEXT("D:/Models/mmproj-llava-v1.6-mistral-7b-f16.gguf");

    Options.bStream = true;
    Options.NumGpuLayers = 99;
    Options.MMProjectUseGpu = true;  // MMProject モデルもGPUを使用する

// 画像付きメッセージを作成
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("What do you see in this image?");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
ImageMessage.Images.Add(ChatTexture);  // 画像は1枚しか追加できません

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Cllama Vision: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###Texture2Dから画像を分析する

```cpp
void UMyClass::AnalyzeTextureWithCllama(UTexture2D* InTexture)
{
    if (!InTexture)
    {
        UE_LOG(LogTemp, Error, TEXT("Invalid texture"));
        return;
    }

    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(InTexture);

    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llava-v1.6-mistral-7b.Q4_K_M.gguf");
    Options.MMProjectModelPath.FilePath = TEXT("D:/Models/mmproj-llava-v1.6-mistral-7b-f16.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;
    Options.MMProjectUseGpu = true;

    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("Describe this image in detail.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Description: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##高度な設定

###サンプリングパラメータ設定

```cpp
void UMyClass::ConfigureCllamaSampling()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;

    // GPUアクセラレーション
オプション.NumGpuレイヤー = 99; // GPUにできるだけ多くのレイヤーを配置

// サンプリングパラメータ
    Options.Temperature = 0.7f;  // 温度
    Options.TopK = 40;           // Top-K サンプリング
Options.TopP = 0.95f;        // 核サンプリング
オプション.MinP = 0.05f;        // Min-Pサンプリング

    // Mirostatサンプリング（混乱度制御用）
    Options.Mirostat = 2;        // 0=無効, 1=Mirostat, 2=Mirostat 2.0
    Options.MirostatEta = 0.1f;
    Options.MirostatTau = 5.0f;

// コンテキストと生成制限
Options.NumCtx = 4096;       // コンテキストウィンドウのサイズ
Options.NumPredict = 256;    // 生成される最大トークン数（-1 = 無限）

// 繰り返しペナルティ
Options.RepeatLastN = 64;    // 最後にチェックするトークンの繰り返し数
    Options.RepeatPenalty = 1.1f;

// テールフリーサンプリング
Options.TfsZ = 1.0f;         // 1.0 = 無効

// 停止シーケンス
    Options.StopSequences.Add(TEXT("\n\n"));
    Options.StopSequences.Add(TEXT("User:"));

// ランダムシード（再現可能な生成のため）
    Options.Seed = 42;

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a short poem."), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###カスタムテンプレートを使用する

```cpp
void UMyClass::UseCustomTemplate()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/my_model.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;

// カスタムプロンプトテンプレート（モデル組み込みテンプレートを上書き）
    Options.Template = TEXT("<|im_start|>system\n{{system}}<|im_end|>\n<|im_start|>user\n{{prompt}}<|im_end|>\n<|im_start|>assistant\n");

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System},
            {TEXT("Hello!"), EAIChatPlus_ChatRole::User}
        });

    Request->SendRequest();
}
```

##エラー処理

```cpp
void UMyClass::RobustCllamaRequest()
{
// まずCllamaが利用可能かどうかをチェックします
    if (!UAIChatPlus_Util::Cllama_IsValid())
    {
        UE_LOG(LogTemp, Error, TEXT("Cllama is not available"));
        return;
    }

    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->OnStartedListeners.AddLambda([]()
    {
        UE_LOG(LogTemp, Display, TEXT("Cllama request started, loading model..."));
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.HasError())
        {
            UE_LOG(LogTemp, Error, TEXT("Response error: %s"), *Response.Error.GetDescription());
            return;
        }

        UE_LOG(LogTemp, Display, TEXT("Success: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Tokens: %s"), *Response.Usage.GetDescription());

// 性能指標
        UE_LOG(LogTemp, Display, TEXT("Total Duration: %lld ns"), Response.TotalDuration);
        UE_LOG(LogTemp, Display, TEXT("Load Duration: %lld ns"), Response.LoadDuration);
        UE_LOG(LogTemp, Display, TEXT("Prompt Eval Duration: %lld ns"), Response.PromptEvalDuration);
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
UAIChatPlus_CllamaChatRequest* CurrentCllamaRequest = nullptr;

void UMyClass::StartCllamaRequest()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;
オプション.予測数 = -1;  // 無限生成

    CurrentCllamaRequest = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a very long story about adventures."), EAIChatPlus_ChatRole::User}});

    CurrentCllamaRequest->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Generating: %s"), *Message);
    });

    CurrentCllamaRequest->SendRequest();
}

void UMyClass::CancelCllamaRequest()
{
    if (CurrentCllamaRequest && CurrentCllamaRequest->IsActivated())
    {
        CurrentCllamaRequest->StopRequest();
        UE_LOG(LogTemp, Display, TEXT("Cllama request cancelled"));
    }
}
```

##完全なダイアログ管理の例

```cpp
// メンバ変数
TArray<FAIChatPlus_ChatRequestMessage> CllamaConversation;
FAIChatPlus_CllamaChatRequestOptions CllamaOptions;

void UMyClass::InitializeCllamaChat()
{
    CllamaOptions.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    CllamaOptions.bStream = true;
    CllamaOptions.NumGpuLayers = 99;
CllamaOptions.KeepAlive = -1;  // モデルのロードを保持する

// ダイアログを初期化
    CllamaConversation.Empty();
    CllamaConversation.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}

void UMyClass::SendCllamaUserMessage(const FString& UserMessage)
{
    CllamaConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(CllamaOptions, CllamaConversation);

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
// 生成された内容をリアルタイムで表示
        UE_LOG(LogTemp, Display, TEXT("Generating: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);

// アシスタントの返答を会話履歴に追加
        FString AssistantMessage = Response.GetMessage();
        CllamaConversation.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});

        OnCllamaResponse(AssistantMessage);
    });

    Request->SendRequest();
}

void UMyClass::OnCllamaResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Cllama: %s"), *Response);
}

void UMyClass::ClearCllamaConversation()
{
    CllamaConversation.Empty();
    CllamaConversation.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}
```

--8<-- "footer_ja.md"


> この投稿はChatGPTによって翻訳されました。ご意見は[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)いかなる遺漏を指摘する。 
