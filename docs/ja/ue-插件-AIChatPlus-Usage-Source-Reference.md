---
layout: post
title: API Reference
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
- llama.cpp
description: API Reference
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - API Reference" />

#C++編 - API リファレンス

このドキュメントは、AIChatPlusプラグインのC++ APIリファレンスを提供し、公開されているすべてのクラス、構造体、列挙型および主要なメソッドの説明を含みます。

##目次

- [列挙型](##枚举类型)
[コア基本クラス](##核心基类)
- [Handler クラス](##handler-类)
- [Request クラス](##request-类)
- [ツール類](##工具类)
- [JSONクラス](##json-类)

---

##列挙型

### EAIChatPlus_ChatApiProvider

AIチャットAPIプロバイダーの列挙。

```cpp
enum class EAIChatPlus_ChatApiProvider : uint8
{
    OpenAI,         // OpenAI API
    Azure,          // Azure OpenAI API
    Claude,         // Anthropic Claude API
    Gemini,         // Google Gemini API
オラマ,         // Ollama ローカルサービス
Clama,         // llama.cpp ダイレクトコール（廃止済み）
CllamaServer    // llama.cpp サーバーモード
};
```

### EAIChatPlus_ImageApiProvider

画像生成 APIプロバイダ一覧。

```cpp
enum class EAIChatPlus_ImageApiProvider : uint8
{
    OpenAI,   // OpenAI DALL-E
    Azure     // Azure OpenAI DALL-E
};
```

### EAIChatPlus_ChatRole

メッセージキャラクター列挙型。

```cpp
enum class EAIChatPlus_ChatRole : uint8
{
システム,     // システムコマンド（旧モデル）
ユーザー,       // ユーザーメッセージ
アシスタント,  // AI 返答
開発者,  // 開発者指令（o1+ モデル）
ツール        // ツール呼び出し結果
};
```

### EAIChatPlus_ImageChatType

画像操作タイプの列挙型。

```cpp
enum class EAIChatPlus_ImageChatType : uint8
{
世代,  // 画像生成
編集,        // 画像編集
バリエーション    // 图片变体
};
```

### EAIChatPlus_JsonValueType

JSON値タイプの列挙型。

```cpp
enum class EAIChatPlus_JsonValueType : uint8
{
なし,     // 無効
    Null,     // 空値
String,   // 文字列
数字,   // Number
ブール,  // ブール
配列,    // 配列
オブジェクト    // 対象
};
```

---

##コアベースクラス

### UAIChatPlus_RequestBase

すべてのリクエストの基底クラス（抽象クラス）。

**主な方法：**

| 方法 | 戻り値の型 | 説明 |
|------|---------|------|
| `SendRequest()` | `bool` | リクエストを送信 |
| `StopRequest()` | `void` | 停止要求 |
| `Activate()` | `void` | リクエストオブジェクトをアクティベートする |
| `IsActivated()` | `bool` | アクティベートされているかどうかをチェック |
| `SetIsAutoDestroy(bool)` | `void` | 設定完了後、自動的に破棄 |

**依頼：**

| 委託名 | 署名 | 説明文 |
|--------|------|------|
| `OnStartedListeners` | `void()` | リクエスト開始 |
| `OnMessageListeners` | `void(const FString&)` | ストリーミングメッセージを受信 |
`OnFinishedListeners` | `void(const FAIChatPlus_PointerWrapper&)` | リクエスト完了
| `OnFailedListeners` | `void(const FAIChatPlus_PointerWrapper&)` | リクエスト失敗 |

---

### UAIChatPlus_ChatRequestBase

チャットリクエストの基底クラスで、`UAIChatPlus_RequestBase` から継承されています。

**静的ファクトリメソッド：**

```cpp
// プロバイダーごとにリクエストを作成
static UAIChatPlus_ChatRequestBase* CreateByApi(EAIChatPlus_ChatApiProvider InApiProvider);
static UAIChatPlus_ChatRequestBase* CreateByApiInWorld(EAIChatPlus_ChatApiProvider InApiProvider, const UObject* InWorldContext);
```

**主要な方法：**

| 方法 | 戻り型 | 説明 |
|------|---------|------|
| `SetMessages(const TArray<FAIChatPlus_ChatRequestMessage>&)` | `void` | メッセージリストを設定 |
| `GetFullUrl()` | `FString` | 完全なリクエストURLを取得 |
| `GetModelText()` | `FString` | モデル名を取得する |
| `GetTokenUsageText()` | `FString` | Tokenの使用状況を説明する文字列を取得 |
| `GetApiProvider()` | `EAIChatPlus_ChatApiProvider` | APIプロバイダタイプを取得 |

---

### UAIChatPlus_ImageRequestBase

画像リクエスト基底クラス、`UAIChatPlus_RequestBase`から継承。

**静的ファクトリメソッド：**

```cpp
static UAIChatPlus_ImageRequestBase* CreateByApi(EAIChatPlus_ImageApiProvider InApiProvider);
static UAIChatPlus_ImageRequestBase* CreateByApiInWorld(EAIChatPlus_ImageApiProvider InApiProvider, const UObject* InWorldContext);
```

**重要手法：**

｜方法｜戻り値の型｜説明｜
|------|---------|------|
| `SetPrompt(const FString&)` | `void` | 画像生成のプロンプトを設定 |
| `SetImages(const TArray<UAIChatPlus_Texture*>&)` | `void` | 入力画像を設定（編集/バリエーション） |
| `GetModelText()` | `FString` | モデル名を取得 |
以下是将给定文本翻译成日语的结果：

| `GetStyleText()` | `FString` | スタイル名を取得 |
| `GetRevisedPrompt()` | `FString` | 修正後のプロンプトを取得する |
| `GetImageChatType()` | `FString` | 画像操作タイプを取得 |

---

### UAIChatPlus_ModelRequestBase

モデルリストリクエストの基底クラスで、`UAIChatPlus_RequestBase`を継承しています。

**静的ファクトリメソッド：**

```cpp
static UAIChatPlus_ModelRequestBase* CreateByApi(EAIChatPlus_ChatApiProvider InApiProvider);
static UAIChatPlus_ModelRequestBase* CreateByApiInWorld(EAIChatPlus_ChatApiProvider InApiProvider, const UObject* InWorldContext);
```

---

##Handler クラス

### UAIChatPlus_HandlerBase

すべての Handler の基底クラス。

**重要な方法：**

| 方法 | 戻り値の型 | 説明 |
|------|---------|------|
| `SetIsAutoDestroy(bool)` | `void` | 自動破壊を設定 |
| `AutoDestroy()` | `void` | 自動破棄を実行します |
| `Destroy()` | `void` | 即時破棄 |

---

### UAIChatPlus_ChatHandlerBase

チャットリクエストハンドラー、`UAIChatPlus_HandlerBase`を継承。

**静的ファクトリーメソッド：**

```cpp
static UAIChatPlus_ChatHandlerBase* New();
```

**バインド方法：**

| 方法 | 説明 |
|------|------|
| `BindChatRequest(UAIChatPlus_ChatRequestBase*)` | チャットリクエストをバインド |
| `BindImageRequest(UAIChatPlus_ImageRequestBase*)` | 画像リクエストをバインド |
`BindModelRequest(UAIChatPlus_ModelRequestBase*)` | モデルリクエストのバインド
| `ClearDelegates()` | すべてのデリゲートバインディングをクリアする |

**依頼：**

| 委託名 | 署名 | 説明 |
|--------|------|------|
| `OnStarted` | `void()` | リクエスト開始 |
| `OnStopped` | `void()` | 停止要求 |
| `OnMessage` | `void(const FString&)` | ストリーミングメッセージ |
| `OnMessageFinished` | `void(const FAIChatPlus_MessageFinishedPayload&)` | メッセージ完了 |
| `OnUpdated` | `void(const FAIChatPlus_PointerWrapper&)` | 更新要求 |
| `OnFinished` | `void(const FAIChatPlus_PointerWrapper&)` | リクエスト完了 |
| `OnFailed` | `void(const FAIChatPlus_PointerWrapper&)` | リクエスト失敗 |
| `OnImages` | `void(const TArray<UTexture2D*>&, bool)` | 画像生成 |
| `OnModels` | `void(const TArray<FString>&)` | モデルリスト |

---

### UAIChatPlus_CllamaServerHandler

CllamaServer専用ハンドラー。

**静的ファクトリメソッド：**

```cpp
static UAIChatPlus_CllamaServerHandler* CreateHandler();
```

**委託：**

| 委託名 | 署名 | 説明 |
|--------|------|------|
| `OnServerStarted` | `void(FGuid)` | サーバー起動 |
| `OnServerStopped` | `void(FGuid)` | サーバー停止 |
| `OnServerFailed` | `void(FGuid, const FString&)` | サーバーの失敗 |

---

##リクエストクラス

すべてのProviderのRequestクラスは同じファクトリメソッドパターンに従います：

###汎用工場メソッドパターン

```cpp
// OpenAIを例として、他のプロバイダも同様です
static UAIChatPlus_OpenAIChatRequest* Create();
static UAIChatPlus_OpenAIChatRequest* CreateWithOptions(const FAIChatPlus_OpenAIChatRequestOptions& InOptions);
static UAIChatPlus_OpenAIChatRequest* CreateWithOptionsAndMessages(
    const FAIChatPlus_OpenAIChatRequestOptions& InOptions,
    const TArray<FAIChatPlus_ChatRequestMessage>& InMessages);
static UAIChatPlus_OpenAIChatRequest* CreateInWorld(const UObject* InWorldContext);
static UAIChatPlus_OpenAIChatRequest* CreateInWorldWithOptions(
    const UObject* InWorldContext,
    const FAIChatPlus_OpenAIChatRequestOptions& InOptions);
static UAIChatPlus_OpenAIChatRequest* CreateInWorldWithOptionsAndMessages(
    const UObject* InWorldContext,
    const FAIChatPlus_OpenAIChatRequestOptions& InOptions,
    const TArray<FAIChatPlus_ChatRequestMessage>& InMessages);
```

###汎用的な静的メソッド

すべてのRequestクラスは、型変換のために`CastWrapperToResponse`メソッドを提供します：

```cpp
// PointerWrapperから応答データを抽出する
static FAIChatPlus_XXXResponseBody& CastWrapperToResponse(const FAIChatPlus_PointerWrapper& InWrapper);
static FAIChatPlus_PointerWrapper CastResponseToWrapper(const FAIChatPlus_XXXResponseBody& InResponse);
```

---

### UAIChatPlus_OpenAIChatRequest

OpenAI チャットリクエスト。

**ヘッダーファイル：** `Common_OpenAI/AIChatPlus_OpenAIChatRequest.h`

**オプションタイプ:** `FAIChatPlus_OpenAIChatRequestOptions`

**応答タイプ：** `FAIChatPlus_OpenAIChatResponseBody`

---

### UAIChatPlus_AzureChatRequest

Azure OpenAI チャットリクエスト。

**ヘッダーファイル：** `Common_Azure/AIChatPlus_AzureChatRequest.h`

**オプションの種類：** `FAIChatPlus_AzureChatRequestOptions`

**応答タイプ：** `FAIChatPlus_AzureChatResponseBody`

---

### UAIChatPlus_ClaudeChatRequest

クロードとのチャットリクエスト。

**ヘッダーファイル：** `Common_Claude/AIChatPlus_ClaudeChatRequest.h`

**オプション タイプ：** `FAIChatPlus_ClaudeChatRequestOptions`

**レスポンスタイプ：** `FAIChatPlus_ClaudeChatResponseBody`

---

### UAIChatPlus_GeminiChatRequest

ジェミニ チャットリクエスト。

**ヘッダーファイル：** `Common_Gemini/AIChatPlus_GeminiChatRequest.h`

**オプションタイプ:** `FAIChatPlus_GeminiChatRequestOptions`

**レスポンス タイプ：** `FAIChatPlus_GeminiChatResponseBody`

---

### UAIChatPlus_OllamaChatRequest

Ollama チャットリクエスト。

**ヘッダーファイル：** `Common_Ollama/AIChatPlus_OllamaChatRequest.h`

**オプション タイプ：** `FAIChatPlus_OllamaChatRequestOptions`

**レスポンスタイプ:** `FAIChatPlus_OllamaChatResponseBody`

---

### UAIChatPlus_OllamaModelRequest

Ollamaモデルリストリクエスト。

**ヘッダーファイル：** `Common_Ollama/AIChatPlus_OllamaModelRequest.h`

**オプション タイプ：** `FAIChatPlus_OllamaModelRequestOptions`

**レスポンス タイプ:** `FAIChatPlus_OllamaModelResponseBody`

**特有方法：**
**特有の方法：**

| 方法       | 戻り値の型   | 説明         |
|------|---------|------|
| `GetModelNames()` | `TArray<FString>` | モデル名リストを取得 |

---

###UAIChatPlus_CllamaChatRequest（非推奨）

Cllama オフラインチャットリクエスト（廃止済み、CllamaServerの使用を推奨）。

**ヘッダーファイル：** `Common_Cllama/AIChatPlus_CllamaChatRequest.h`

**オプションタイプ：** `FAIChatPlus_CllamaChatRequestOptions`

**応答タイプ：** `FAIChatPlus_CllamaChatResponseBody`

---

### UAIChatPlus_CllamaServerChatRequest

CllamaServer チャットリクエスト。

**ヘッダーファイル：** `Common_CllamaServer/AIChatPlus_CllamaServerChatRequest.h`

**オプション タイプ：** `FAIChatPlus_CllamaServerChatRequestOptions`

**レスポンス タイプ：** `FAIChatPlus_CllamaServerChatResponseBody`

---

### UAIChatPlus_OpenAIImageRequest

OpenAI 画像生成リクエスト。

**ヘッダーファイル：** `Common_OpenAI/AIChatPlus_OpenAIImageRequest.h`

**Options タイプ：** `FAIChatPlus_OpenAIImageRequestOptions`

**応答タイプ：** `FAIChatPlus_OpenAIImageResponseBody`

---

### UAIChatPlus_AzureImageRequest

Azure 画像生成リクエスト。

**ヘッダーファイル：** `Common_Azure/AIChatPlus_AzureImageRequest.h`

**オプション タイプ：** `FAIChatPlus_AzureImageRequestOptions`

**応答タイプ:** `FAIChatPlus_AzureImageResponseBody`

---

### UAIChatPlus_CllamaServer

CllamaServer サーバー管理クラス。

**ヘッダーファイル：** `Common_CllamaServer/AIChatPlus_CllamaServer.h`

**静的ファクトリメソッド：**

```cpp
static UAIChatPlus_CllamaServer* CreateServer(
    const FAIChatPlus_CllamaServerParam& InParams,
    FGuid InServerID = FGuid());
static UAIChatPlus_CllamaServer* CreateServerInWorld(
    const UObject* InWorldContext,
    const FAIChatPlus_CllamaServerParam& InParams,
    FGuid InServerID = FGuid());
static UAIChatPlus_CllamaServer* CreateServerWithHandler(
    const FAIChatPlus_CllamaServerParam& InParams,
    UAIChatPlus_CllamaServerHandler* InHandler,
    FGuid InServerID = FGuid());
```

**インスタンスメソッド：**

| 方法 | 戻り値の型 | 説明 |
|------|---------|------|
| `Activate()` | `void` | サーバーを起動する |
| `StopServer()` | `void` | サーバーを停止する |
| `IsRunning()` | `bool` | 実行中かどうかをチェックします |
| `GetServerID()` | `FGuid` | サーバーIDを取得 |
| `GetHost()` | `FString` | ホストアドレスを取得 |
| `GetAddress()` | `FString` | 完全なアドレスを取得 |
| `GetServerInfo(FAIChatPlus_CllamaServerInfo&)` | `bool` | サーバー情報を取得する |

**静的マネジメント手法：**

| 方法          | 戻り値の型       | 説明             |
|------|---------|------|
| `IsServerValid(const FGuid&)` | `bool` | サーバーが有効かどうかをチェックします |
| `IsServerRunning(const FGuid&)` | `bool` | サーバーが実行中かどうかをチェックします |
| `StopServerByID(const FGuid&)` | `void` | ID でサーバーを停止する |
| `StopAllServers()` | `void` | 全てのサーバーを停止する |
| `GetServerByID(const FGuid&)` | `UAIChatPlus_CllamaServer*` | IDによるサーバーの取得 |
| `GetAllServerIDs()` | `TArray<FGuid>` | 全てのサーバーIDを取得 |

---

##ツール類

### UAIChatPlus_Util

汎用ユーティリティクラスで、さまざまな静的ヘルパーメソッドを提供します。

**ヘッダーファイル：** `Common/AIChatPlus_Util.h`

####ログ関連

| メソッド | 戻り型 | 説明 |
|------|---------|------|
| `SetInternalLogVerbosity(EAIChatPlus_LogVerbosityType)` | `void` | 内部ログレベルを設定する |

####ラッパー変換

| 方法 | 戻り値の型 | 説明 |
|------|---------|------|
| `CastWrapperToError(const FAIChatPlus_PointerWrapper&)` | `FAIChatPlus_ResponseErrorBase&` | エラー情報の抽出 |
| `CastWrapperToResponse(const FAIChatPlus_PointerWrapper&)` | `FAIChatPlus_ChatResponseBodyBase&` | 応答データを抽出 |
| `GetErrorWrapperDescription(const FAIChatPlus_PointerWrapper&)` | `FString` | エラー説明を取得する |
| `GetResponseWrapperMessage(const FAIChatPlus_PointerWrapper&)` | `FString` | レスポンスメッセージを取得 |

####画像ツール

| 方法 | 戻り値の型 | 説明 |
|------|---------|------|
| `LoadImage(const FString&, bool)` | `UTexture2D*` | ファイルから画像を読み込む |
| `SaveImage(UTexture2D*, const FString&)` | `bool` | 画像をファイルに保存 |
| `ImageToB64(UTexture2D*, int32)` | `FString` | イメージからBase64へ変換 |
| `CopyTexture2D(UTexture2D*, UObject*, FName, EObjectFlags)` | `UTexture2D*` | テクスチャのコピー |
| `FitImageSize(const FVector2D&, const FVector2D&)` | `FVector2D` | 適合サイズを計算 |
| `CopyTexture2DToClipboard(UTexture2D*)` | `void` | クリップボードにコピー |
| `IsCanCopyTexture2DToClipboard()` | `bool` | サポートされているかどうかを確認 |

####オーディオツール

| メソッド | 戻り値の型 | 説明 |
|------|---------|------|
| `LoadSoundWav(const FString&)` | `USoundWave*` | ファイルから音声をロード |
以下是将给定文本翻译成日语的版本：

| `SaveSoundWav(USoundWave*, const FString&)` | `bool` | 音声ファイルへの保存 |
| `SoundToB64(USoundWave*)` | `FString` | オーディオをBase64に変換 |
| `CopySoundWave(const USoundWave*, UObject*, FName)` | `USoundWave*` | サウンドウェーブのコピー |
| `WavDataToSoundWave(const TArray<uint8>&, bool, bool)` | `USoundWave*` | WAVデータからサウンドウェーブへ変換 |
| `GetSoundWavePCMData(USoundWave*)` | `TArray<uint8>` | PCM データを取得 |

####JSONツール

| 方法 | 戻り値の型 | 説明 |
|------|---------|------|
| `MergeJsonObjects(const FString&, const FString&)` | `FString` | JSON文字列の結合 |
| `LoadJsonString(const FString&)` | `TSharedPtr<FJsonObject>` | JSON文字列の解析 |
| `ToJsonString(const TSharedPtr<FJsonObject>&)` | `FString` | JSON文字列に変換 |

####Cllama ツール

| 方法 | 戻り値の型 | 説明 |
|------|---------|------|
| `Cllama_IsValid()` | `bool` | Cllamaが利用可能かどうかをチェックします |
| `Cllama_IsSupportGpu()` | `bool` | GPUサポートの有無を確認 |
| `Cllama_GetSupportBackends()` | `TArray<FString>` | サポートされているバックエンドを取得 |
| `Cllama_PrepareModelPathFromPak(const FString&)` | `FString` | Pakからモデルパスを準備 |

####モデル情報

| メソッド | 戻り型 | 説明 |
|------|---------|------|
| `GetOpenAIChatDefaultModels()` | `const TArray<FName>&` | OpenAIデフォルトモデルリスト |
| `GetOpenAIChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | OpenAIのモデル情報を取得する |
| `GetClaudeChatDefaultModels()` | `const TArray<FName>&` | Claude デフォルトモデルリスト |
| `GetClaudeChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | Claudeモデル情報を取得 |
| `GetGeminiChatDefaultModels()` | `const TArray<FName>&` | Gemini デフォルトモデル一覧 |
| `GetGeminiChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | Geminiモデル情報を取得 |

---

### UAIChatPlus_Texture

画像ラッパークラス、非同期読み込みとBase64変換をサポート。

**ヘッダーファイル：** `Common/AIChatPlus_Texture.h`

**静的ファクトリメソッド：**

```cpp
static UAIChatPlus_Texture* New(UTexture2D* InTexture = nullptr, const FString& InSourcePath = "");
static UAIChatPlus_Texture* CreateInBlueprint(UObject* WorldContextObject, UTexture2D* InTexture);
```

**方法：**

| 方法 | 戻り値の型 | 説明 |
|------|---------|------|
| `LoadFromFile(const FString&)` | `bool` | ファイルからの読み込み（同期） |
| `LoadFromFileAsync(const FString&, Callback)` | `FLoadingTaskType*` | ファイルからの読み込み（非同期） |
| `LoadFromAsset(UObject*, const FString&)` | `bool` | アセットからの読み込み（同期） |
| `LoadFromAssetAsync(UObject*, Callback, const FString&)` | `FLoadingTaskType*` | アセットからロード（非同期） |
| `ToB64()` | `const FString&` | Base64に変換（同期） |
以下是将提供的文本翻译成日语的结果：

| `ToB64Async(Callback)` | `FLoadingTaskType*` | Base64に変換（非同期） |
| `GetBrush(bool)` | `const FSlateBrush*` | Slateブラシを取得 |
| `GetBrushCopy(bool)` | `FSlateBrush` | ブラシのコピーを取得 |
| `GetSize()` | `FIntVector2` | サイズを取得 |
`GetSize2D()` | `FVector2D` | サイズを取得する（浮動小数点）
| `IsValid()` | `bool` | 有効かどうかをチェック |
| `IsLoading()` | `bool` | 読み込み中かどうかをチェック |
| `Reset()` | `void` | リセット |
| `WaitLoadingComplete()` | `void` | ロード完了を待つ |

---

### UAIChatPlus_Sound

オーディオラッピングクラス、非同期読み込みとBase64変換をサポート。

**ヘッダーファイル：** `Common/AIChatPlus_Sound.h`

**静的ファクトリメソッド：**

```cpp
static UAIChatPlus_Sound* New(USoundWave* InSound = nullptr, const FString& InSourcePath = "");
static UAIChatPlus_Sound* CreateInBlueprint(UObject* WorldContextObject, USoundWave* InSound);
```

**方法：**

| 方法 | 戻り値の型 | 説明 |
|------|---------|------|
| `LoadFromFile(const FString&)` | `bool` | ファイルからの読み込み（同期） |
| `LoadFromFileAsync(const FString&, Callback)` | `FLoadingTaskType*` | ファイルから非同期でロードする |
| `LoadFromAsset(UObject*, const FString&)` | `bool` | アセットからの読み込み（同期） |
| `LoadFromAssetAsync(UObject*, Callback, const FString&)` | `FLoadingTaskType*` | アセットから非同期でロードする |
| `ToB64()` | `const FString&` | Base64に変換（同期） |
| `ToB64Async(コールバック)` | `FLoadingTaskType*` | Base64に変換（非同期） |
| `IsValid()` | `bool` | 有効かどうかを確認する |
| `IsLoading()` | `bool` | ロード中かどうかをチェック |
`Reset()` | `void` | リセット
| `WaitLoadingComplete()` | `void` | ロード完了を待機 |
| `PlayInEditor()` | `void` | エディタで再生する |

---

##JSON クラス

### UAIChatPlus_JsonObject

JSONオブジェクトのラッパークラス。

**ヘッダーファイル：** `Common/Json/AIChatPlus_JsonObject.h`

**静的ファクトリメソッド：**

```cpp
static UAIChatPlus_JsonObject* Create();
static UAIChatPlus_JsonObject* Parse(const FString& JsonString, bool& bSuccess, FString& ErrorMessage);
static UAIChatPlus_JsonObject* FromStruct(const int32& Struct);  // CustomThunk
```

**フィールド設定メソッド（チェーンメソッド呼び出しに対応）：**

| 方法 | 戻り値の型 | 説明 |

|------|---------|------|
| `SetStringField(const FString&, const FString&)` | `UAIChatPlus_JsonObject*` | 文字列フィールドの設定 |
| `SetNumberField(const FString&, float)` | `UAIChatPlus_JsonObject*` | 数字フィールドを設定 |
| `SetIntegerField(const FString&, int32)` | `UAIChatPlus_JsonObject*` | 整数フィールドの設定 |
| `SetBooleanField(const FString&, bool)` | `UAIChatPlus_JsonObject*` | ブールフィールドを設定 |
| `SetObjectField(const FString&, UAIChatPlus_JsonObject*)` | `UAIChatPlus_JsonObject*` | オブジェクトフィールドの設定 |
| `SetArrayField(const FString&, UAIChatPlus_JsonArray*)` | `UAIChatPlus_JsonObject*` | 配列フィールドを設定 |
| `SetNullField(const FString&)` | `UAIChatPlus_JsonObject*` | 空フィールドを設定 |

**フィールド取得方法：**

| 方法 | 戻り値の型 | 説明 |
|------|---------|------|
| `GetStringField(const FString&, const FString&, bool&)` | `FString` | 文字列を取得する |
| `GetNumberField(const FString&, float, bool&)` | `float` | 数値取得 |
| `GetIntegerField(const FString&, int32, bool&)` | `int32` | 整数を取得 |
| `GetBooleanField(const FString&, bool, bool&)` | `bool` | ブール値を取得 |
| `GetObjectField(const FString&, bool&)` | `UAIChatPlus_JsonObject*` | オブジェクトを取得 |
| `GetArrayField(const FString&, bool&)` | `UAIChatPlus_JsonArray*` | 配列を取得 |

**その他の方法：**

| メソッド | 戻り値の型 | 説明 |
|------|---------|------|
| `HasField(const FString&)` | `bool` | フィールドの存在をチェック |
| `GetFieldType(const FString&)` | `EAIChatPlus_JsonValueType` | フィールドタイプを取得 |
| `RemoveField(const FString&)` | `UAIChatPlus_JsonObject*` | フィールドを削除 |
| `Clear()` | `UAIChatPlus_JsonObject*` | 全てのフィールドをクリア |
以下是将这些文本翻译成日语的结果：

| `ToString(bool)` | `FString` | 文字列に変換 |
| `ToStruct(int32&)` | `bool` | 構造体に変換 |
| `Merge(UAIChatPlus_JsonObject*, bool)` | `UAIChatPlus_JsonObject*` | オブジェクトのマージ |
| `Duplicate()` | `UAIChatPlus_JsonObject*` | オブジェクトの複製 |
| `IsValid()` | `bool` | 有効性をチェック |

**経路照会方法：**

| メソッド | 戻り型 | 説明 |
|------|---------|------|
| `SetStringByPath(const FString&, const FString&, const FAIChatPlus_JsonPathOptions&)` | `UAIChatPlus_JsonObject*` | パスごとに文字列を設定 |
| `GetStringByPath(const FString&, const FString&, FAIChatPlus_JsonQueryResult&)` | `FString` | パスで文字列を取得 |

---

### UAIChatPlus_JsonArray

JSON配列ラッパークラス。

**ヘッダーファイル：** `Common/Json/AIChatPlus_JsonArray.h`

**静的ファクトリメソッド：**

```cpp
static UAIChatPlus_JsonArray* Create();
static UAIChatPlus_JsonArray* Parse(const FString& JsonString, bool& bSuccess, FString& ErrorMessage);
static UAIChatPlus_JsonArray* FromStringArray(const TArray<FString>& Values);
static UAIChatPlus_JsonArray* FromIntegerArray(const TArray<int32>& Values);
```

**要素の追加方法（チェーン呼び出しをサポート）：**

| 方法 | 戻り値の型 | 説明 |
|------|---------|------|
| `AddString(const FString&)` | `UAIChatPlus_JsonArray*` | 文字列を追加 |
| `AddNumber(float)` | `UAIChatPlus_JsonArray*` | 数字を追加 |
| `AddInteger(int32)` | `UAIChatPlus_JsonArray*` | 整数を追加 |
| `AddBoolean(bool)` | `UAIChatPlus_JsonArray*` | ブール値を追加 |
| `AddObject(UAIChatPlus_JsonObject*)` | `UAIChatPlus_JsonArray*` | オブジェクトを追加 |
| `AddArray(UAIChatPlus_JsonArray*)` | `UAIChatPlus_JsonArray*` | 配列を追加 |
| `AddNull()` | `UAIChatPlus_JsonArray*` | 空の値を追加 |

**要素の取得方法：**

| 方法 | 戻り値の型 | 説明 |
|------|---------|------|
| `GetString(int32, const FString&, bool&)` | `FString` | 文字列を取得 |
| `GetNumber(int32, float, bool&)` | `float` | 数値を取得する |
| `GetInteger(int32, int32, bool&)` | `int32` | 整数を取得 |
| `GetBoolean(int32, bool, bool&)` | `bool` | ブール値を取得 |
| `GetObject(int32, bool&)` | `UAIChatPlus_JsonObject*` | オブジェクトを取得 |
| `GetArray(int32, bool&)` | `UAIChatPlus_JsonArray*` | 配列を取得 |

**その他の方法：**

| 方法 | 戻り値の型 | 説明 |
|------|---------|------|
| `Length()` | `int32` | 長さを取得 |
| `GetElementType(int32)` | `EAIChatPlus_JsonValueType` | 要素タイプを取得 |
| `SetString(int32, const FString&, bool&)` | `UAIChatPlus_JsonArray*` | 文字列を設定 |
| `SetObject(int32, UAIChatPlus_JsonObject*, bool&)` | `UAIChatPlus_JsonArray*` | オブジェクトの設定 |
| `RemoveAt(int32, bool&)` | `UAIChatPlus_JsonArray*` | 要素を削除 |
| `Clear()` | `UAIChatPlus_JsonArray*` | 配列を空にする |
| `ToString(bool)` | `FString` | 文字列に変換 |
| `Duplicate()` | `UAIChatPlus_JsonArray*` | 配列を複製 |
| `IsValid()` | `bool` | 有効性をチェック |

---

### UAIChatPlus_JsonLibrary

JSON静的ユーティリティライブラリ。

**ヘッダーファイル：** `Common/Json/AIChatPlus_JsonLibrary.h`

**作成方法：**

| メソッド | 戻り値の型 | 説明 |
|------|---------|------|
| `MakeJsonObjectWithStringField(const FString&, const FString&)` | `UAIChatPlus_JsonObject*` | 単一フィールドオブジェクトの作成 |
| `MakeJsonObjectFromStringMap(const TMap<FString, FString>&)` | `UAIChatPlus_JsonObject*` | Mapからオブジェクトを作成 |

**検証方法：**

| 方法 | 戻り値の型 | 説明 |
|------|---------|------|
| `ValidateJsonString(const FString&, FString&)` | `bool` | JSON文字列の検証 |
以下是将给定文本翻译成日语的结果：

| `IsJsonObject(const FString&)` | `bool` | オブジェクトかどうかをチェックする |
`IsJsonArray(const FString&)` | `bool` | 配列であるかを確認します |

**書式設定方法：**

| 方法 | 戻り値の型 | 説明 |
|------|---------|------|
| `PrettifyJson(const FString&)` | `FString` | JSONの美化 |
| `MinifyJson(const FString&)` | `FString` | JSONの圧縮 |

**構造体変換（CustomThunk）：**

| 方法 | 戻り値の型 | 説明 |
|------|---------|------|
| `JsonStringToStruct(const FString&, int32&)` | `bool` | JSONを構造体に変換 |
| `StructToJsonString(const int32&, bool)` | `FString` | 構造体をJSONに変換 |

**ファイル操作：**

| 方法 | 戻り値の型 | 説明 |
|------|---------|------|
| `LoadJsonObjectFromFile(const FString&, bool&, FString&)` | `UAIChatPlus_JsonObject*` | ファイルからオブジェクトをロード |
以下是将给定的文本翻译成日语的结果：

| `SaveJsonObjectToFile(UAIChatPlus_JsonObject*, const FString&, bool, FString&)` | `bool` | オブジェクトをファイルに保存する |
`LoadJsonArrayFromFile(const FString&, bool&, FString&)` | `UAIChatPlus_JsonArray*` | ファイルから配列を読み込む
| `SaveJsonArrayToFile(UAIChatPlus_JsonArray*, const FString&, bool, FString&)` | `bool` | 配列をファイルに保存 |

**比較方法：**

| 方法 | 戻り値の型 | 説明 |
|------|---------|------|
| `EqualsJsonObject(UAIChatPlus_JsonObject*, UAIChatPlus_JsonObject*)` | `bool` | オブジェクトの比較 |
| `EqualsJsonArray(UAIChatPlus_JsonArray*, UAIChatPlus_JsonArray*)` | `bool` | 配列の比較 |

**ルート検索：**

| 方法 | 戻り値の型 | 説明 |
|------|---------|------|
| `QueryStringByPath(UAIChatPlus_JsonObject*, const FString&, const FString&, FAIChatPlus_JsonQueryResult&)` | `FString` | パスによる文字列のクエリ |
| `QueryObjectByPath(UAIChatPlus_JsonObject*, const FString&, FAIChatPlus_JsonQueryResult&)` | `UAIChatPlus_JsonObject*` | パスによるオブジェクトのクエリ |
| `QueryArrayByPath(UAIChatPlus_JsonObject*, const FString&, FAIChatPlus_JsonQueryResult&)` | `UAIChatPlus_JsonArray*` | パスで配列を検索 |

--8<-- "footer_ja.md"


> この投稿はChatGPTで翻訳されたものです。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指摘された箇所を補足してください。 
