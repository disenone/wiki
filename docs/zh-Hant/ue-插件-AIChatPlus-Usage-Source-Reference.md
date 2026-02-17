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

#C++ 篇 - API 參考手冊

本文檔提供 AIChatPlus 插件的 C++ API 參考，涵蓋所有公開類別、結構體、列舉及關鍵方法的說明。

##目錄

- [列舉類型](##枚举类型)
- [核心基類](##核心基类)
[處理器類別](##handler-类)
- [Request 類](##request-类)
- [工具類](##工具类)
- [JSON 類](##json-类)

---

##枚舉類型

### EAIChatPlus_ChatApiProvider

AI 聊天 API 提供商列舉。

```cpp
enum class EAIChatPlus_ChatApiProvider : uint8
{
    OpenAI,         // OpenAI API
    Azure,          // Azure OpenAI API
    Claude,         // Anthropic Claude API
    Gemini,         // Google Gemini API
Ollama,         // Ollama 本機服務
Cllama,         // llama.cpp 直接調用（已廢棄）
CllamaServer    // llama.cpp 伺服器模式
};
```

### EAIChatPlus_ImageApiProvider

圖片生成 API 提供商列表。

```cpp
enum class EAIChatPlus_ImageApiProvider : uint8
{
    OpenAI,   // OpenAI DALL-E
    Azure     // Azure OpenAI DALL-E
};
```

### EAIChatPlus_ChatRole

消息角色枚舉。

```cpp
enum class EAIChatPlus_ChatRole : uint8
{
系統,     // 系統指令（舊模型）
使用者，       // 使用者訊息
助手，  // AI 回覆
    開發者,  // 開發者指令（o1+ 模型）
工具        // 工具調用結果
};
```

### EAIChatPlus_ImageChatType

圖片操作類型枚舉。

```cpp
enum class EAIChatPlus_ImageChatType : uint8
{
生成,  // 圖片生成
編輯,        // 圖片編輯
變體    // 圖片變體
};
```

### EAIChatPlus_JsonValueType

JSON 值類型枚舉。

```cpp
enum class EAIChatPlus_JsonValueType : uint8
{
無效,     // 無效
Null，     // 空值
字串,   // 字串
數字,   // 數字
布林,  // 布爾
    Array,    // 陣列
物件    // 對象
};
```

---

##核心基類

### UAIChatPlus_RequestBase

所有請求的基類（抽象類）。

**關鍵方法：**

| 方法 | 返回類型 | 描述 |
|------|---------|------|
| `SendRequest()` | `bool` | 發送請求 |
| `StopRequest()` | `void` | 停止請求 |
| `Activate()` | `void` | 啟用請求物件 |
| `IsActivated()` | `bool` | 檢查是否已啟用 |
| `SetIsAutoDestroy(bool)` | `void` | 設置完成後自動銷毀 |

**委託：**

| 委託名 | 簽名 | 描述 |
|--------|------|------|
| `OnStartedListeners` | `void()` | 請求開始 |
| `OnMessageListeners` | `void(const FString&)` | 接收串流訊息 |
| `OnFinishedListeners` | `void(const FAIChatPlus_PointerWrapper&)` | 請求完成 |
| `OnFailedListeners` | `void(const FAIChatPlus_PointerWrapper&)` | 請求失敗 |

---

### UAIChatPlus_ChatRequestBase

聊天請求基類，繼承自 `UAIChatPlus_RequestBase`。

**靜態工廠方法：**

```cpp
// 依 Provider 建立請求
static UAIChatPlus_ChatRequestBase* CreateByApi(EAIChatPlus_ChatApiProvider InApiProvider);
static UAIChatPlus_ChatRequestBase* CreateByApiInWorld(EAIChatPlus_ChatApiProvider InApiProvider, const UObject* InWorldContext);
```

**關鍵方法：**

| 方法 | 回傳型別 | 說明 |
|------|---------|------|
| `SetMessages(const TArray<FAIChatPlus_ChatRequestMessage>&)` | `void` | 設定訊息列表 |
| `GetFullUrl()` | `FString` | 獲取完整請求 URL |
| `GetModelText()` | `FString` | 取得模型名稱 |
| `GetTokenUsageText()` | `FString` | 取得 Token 用量描述 |
| `GetApiProvider()` | `EAIChatPlus_ChatApiProvider` | 取得 API 提供者類型 |

---

### UAIChatPlus_ImageRequestBase

圖片請求基類，繼承自 `UAIChatPlus_RequestBase`。

**靜態工廠方法：**

```cpp
static UAIChatPlus_ImageRequestBase* CreateByApi(EAIChatPlus_ImageApiProvider InApiProvider);
static UAIChatPlus_ImageRequestBase* CreateByApiInWorld(EAIChatPlus_ImageApiProvider InApiProvider, const UObject* InWorldContext);
```

**關鍵方法：**

| 方法     | 返回型別 | 描述     |
|------|---------|------|
| `SetPrompt(const FString&)` | `void` | 設定圖片生成提示詞 |
| `SetImages(const TArray<UAIChatPlus_Texture*>&)` | `void` | 設定輸入圖片（編輯/變體） |
| `GetModelText()` | `FString` | 取得模型名稱 |
| `GetStyleText()` | `FString` | 獲取風格名稱 |
| `GetRevisedPrompt()` | `FString` | 取得修正後的提示詞 |
| `GetImageChatType()` | `FString` | 獲取圖片操作類型 |

---

### UAIChatPlus_ModelRequestBase

模型列表請求基類，繼承自 `UAIChatPlus_RequestBase`。

**靜態工廠方法：**

```cpp
static UAIChatPlus_ModelRequestBase* CreateByApi(EAIChatPlus_ChatApiProvider InApiProvider);
static UAIChatPlus_ModelRequestBase* CreateByApiInWorld(EAIChatPlus_ChatApiProvider InApiProvider, const UObject* InWorldContext);
```

---

##處理器類別

### UAIChatPlus_HandlerBase

所有 Handler 的基類。

**關鍵方法：**

| 方法 | 返回類型 | 描述 |
|------|---------|------|
| `SetIsAutoDestroy(bool)` | `void` | 設定自動銷毀 |
| `AutoDestroy()` | `void` | 執行自動銷毀 |
| `Destroy()` | `void` | 立即销毁 |

---

### UAIChatPlus_ChatHandlerBase

聊天請求 Handler，繼承自 `UAIChatPlus_HandlerBase`。

**靜態工廠方法：**

```cpp
static UAIChatPlus_ChatHandlerBase* New();
```

**綁定方法：**

| 方法 | 描述 |
|------|------|
| `BindChatRequest(UAIChatPlus_ChatRequestBase*)` | 綁定聊天請求 |
| `BindImageRequest(UAIChatPlus_ImageRequestBase*)` | 綁定圖片請求 |
| `BindModelRequest(UAIChatPlus_ModelRequestBase*)` | 綁定模型請求 |
| `ClearDelegates()` | 清除所有委託綁定 |

**委託：**

| 委託名 | 簽名 | 描述 |
|--------|------|------|
| `OnStarted` | `void()` | 請求開始 |
| `OnStopped` | `void()` | 請求停止 |
| `OnMessage` | `void(const FString&)` | 流式訊息 |
| `OnMessageFinished` | `void(const FAIChatPlus_MessageFinishedPayload&)` | 訊息完成 |
| `OnUpdated` | `void(const FAIChatPlus_PointerWrapper&)` | 請求更新 |
| `OnFinished` | `void(const FAIChatPlus_PointerWrapper&)` | 請求完成 |
| `OnFailed` | `void(const FAIChatPlus_PointerWrapper&)` | 請求失敗 |
| `OnImages` | `void(const TArray<UTexture2D*>&, bool)` | 圖片生成 |
| `OnModels` | `void(const TArray<FString>&)` | 模型清單 |

---

### UAIChatPlus_CllamaServerHandler

CllamaServer 專用 Handler。

**靜態工廠方法：**

```cpp
static UAIChatPlus_CllamaServerHandler* CreateHandler();
```

**委託：**

| 委託名 | 簽名 | 描述 |
|--------|------|------|
| `OnServerStarted` | `void(FGuid)` | 伺服器啟動 |
| `OnServerStopped` | `void(FGuid)` | 伺服器停止 |
| `OnServerFailed` | `void(FGuid, const FString&)` | 伺服器失敗 |

---

##請求類別

所有 Provider 的 Request 類別都遵循相同的工廠方法模式：

###通用工廠方法模式

```cpp
// 以 OpenAI 為例，其他 Provider 類似
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

###通用靜態方法

所有 Request 類別都提供了 `CastWrapperToResponse` 方法用於類型轉換：

```cpp
// 從 PointerWrapper 提取響應數據
static FAIChatPlus_XXXResponseBody& CastWrapperToResponse(const FAIChatPlus_PointerWrapper& InWrapper);
static FAIChatPlus_PointerWrapper CastResponseToWrapper(const FAIChatPlus_XXXResponseBody& InResponse);
```

---

### UAIChatPlus_OpenAIChatRequest

OpenAI 聊天請求。

**標頭檔：** `Common_OpenAI/AIChatPlus_OpenAIChatRequest.h`

**選項類型：** `FAIChatPlus_OpenAIChatRequestOptions`

**回應類型：** `FAIChatPlus_OpenAIChatResponseBody`

---

### UAIChatPlus_AzureChatRequest

Azure OpenAI 聊天請求。

**標頭檔：** `Common_Azure/AIChatPlus_AzureChatRequest.h`

**選項類型：** `FAIChatPlus_AzureChatRequestOptions`

**回應類型：** `FAIChatPlus_AzureChatResponseBody`

---

### UAIChatPlus_ClaudeChatRequest

Claude 聊天請求。

**標頭檔案：** `Common_Claude/AIChatPlus_ClaudeChatRequest.h`

**選項 類型：** `FAIChatPlus_ClaudeChatRequestOptions`

**回應類型：** `FAIChatPlus_ClaudeChatResponseBody`

---

### UAIChatPlus_GeminiChatRequest

雙子座聊天請求。

**標頭檔：** `Common_Gemini/AIChatPlus_GeminiChatRequest.h`

**選項 類型：** `FAIChatPlus_GeminiChatRequestOptions`

**回應類型：** `FAIChatPlus_GeminiChatResponseBody`

---

### UAIChatPlus_OllamaChatRequest

Ollama 聊天請求。

**標頭檔案：** `Common_Ollama/AIChatPlus_OllamaChatRequest.h`

**選項 類型：** `FAIChatPlus_OllamaChatRequestOptions`

**回應類型：** `FAIChatPlus_OllamaChatResponseBody`

---

### UAIChatPlus_OllamaModelRequest

Ollama 模型清單請求。

**標頭檔：** `Common_Ollama/AIChatPlus_OllamaModelRequest.h`

**選項類型：** `FAIChatPlus_OllamaModelRequestOptions`

**回應類別：** `FAIChatPlus_OllamaModelResponseBody`

**特有方法：**

| 方法 | 回傳型別 | 描述 |
|------|---------|------|
| `GetModelNames()` | `TArray<FString>` | 獲取模型名稱列表 |

---

###UAIChatPlus_CllamaChatRequest（已廢棄）

Cllama 離線聊天請求（已廢棄，推薦使用 CllamaServer）。

**標頭檔：** `Common_Cllama/AIChatPlus_CllamaChatRequest.h`

**選項類型：** `FAIChatPlus_CllamaChatRequestOptions`

**回應類型：** `FAIChatPlus_CllamaChatResponseBody`

---

### UAIChatPlus_CllamaServerChatRequest

CllamaServer 聊天請求。

**標頭檔：** `Common_CllamaServer/AIChatPlus_CllamaServerChatRequest.h`

**選項類型：** `FAIChatPlus_CllamaServerChatRequestOptions`

**回應類型：** `FAIChatPlus_CllamaServerChatResponseBody`

---

### UAIChatPlus_OpenAIImageRequest

OpenAI 圖片生成請求。

**標頭檔：** `Common_OpenAI/AIChatPlus_OpenAIImageRequest.h`

**選項類型：** `FAIChatPlus_OpenAIImageRequestOptions`

**回應類型：** `FAIChatPlus_OpenAIImageResponseBody`

---

### UAIChatPlus_AzureImageRequest

Azure 圖片生成請求。

**標頭檔：** `Common_Azure/AIChatPlus_AzureImageRequest.h`

**選項類型：** `FAIChatPlus_AzureImageRequestOptions`

**回應類型：** `FAIChatPlus_AzureImageResponseBody`

---

### UAIChatPlus_CllamaServer

CllamaServer 伺服器管理類別。

**標頭檔：** `Common_CllamaServer/AIChatPlus_CllamaServer.h`

**靜態工廠方法：**

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

**實例方法：**

| 方法 | 返回類型 | 描述 |
|------|---------|------|
| `Activate()` | `void` | 啟動伺服器 |
| `StopServer()` | `void` | 停止伺服器 |
| `IsRunning()` | `bool` | 檢查是否運行中 |
| `GetServerID()` | `FGuid` | 取得伺服器 ID |
| `GetHost()` | `FString` | 取得主機位址 |
| `GetAddress()` | `FString` | 取得完整地址 |
| `GetServerInfo(FAIChatPlus_CllamaServerInfo&)` | `bool` | 獲取伺服器資訊 |

**靜態管理方法：**

| 方法 | 返回類型 | 描述 |
|------|---------|------|
| `IsServerValid(const FGuid&)` | `bool` | 檢查伺服器是否有效 |
| `IsServerRunning(const FGuid&)` | `bool` | 檢查伺服器是否運行中 |
| `StopServerByID(const FGuid&)` | `void` | 依ID停止伺服器 |
| `StopAllServers()` | `void` | 停止所有伺服器 |
| `GetServerByID(const FGuid&)` | `UAIChatPlus_CllamaServer*` | 按 ID 取得伺服器 |
| `GetAllServerIDs()` | `TArray<FGuid>` | 取得所有伺服器 ID |

---

##工具類

### UAIChatPlus_Util

通用工具類，提供各種靜態輔助方法。

**標頭檔：** `Common/AIChatPlus_Util.h`

####日誌相關

| 方法 | 回傳型別 | 描述 |
|------|---------|------|
| `SetInternalLogVerbosity(EAIChatPlus_LogVerbosityType)` | `void` | 設定內部日誌級別 |

####包裝轉換

| 方法      | 回傳類型   | 描述       |
|------|---------|------|
| `CastWrapperToError(const FAIChatPlus_PointerWrapper&)` | `FAIChatPlus_ResponseErrorBase&` | 提取錯誤資訊 |
| `CastWrapperToResponse(const FAIChatPlus_PointerWrapper&)` | `FAIChatPlus_ChatResponseBodyBase&` | 提取響應數據 |
| `GetErrorWrapperDescription(const FAIChatPlus_PointerWrapper&)` | `FString` | 獲取錯誤描述 |
| `GetResponseWrapperMessage(const FAIChatPlus_PointerWrapper&)` | `FString` | 獲取響應訊息 |

####圖片工具

| 方法 | 返回類型 | 描述 |
|------|---------|------|
以下是翻譯成繁體中文的文本：

| `LoadImage(const FString&, bool)` | `UTexture2D*` | 從文件載入圖片 |
| `SaveImage(UTexture2D*, const FString&)` | `bool` | 保存圖片到檔案 |
| `ImageToB64(UTexture2D*, int32)` | `FString` | 圖片轉 Base64 |
| `CopyTexture2D(UTexture2D*, UObject*, FName, EObjectFlags)` | `UTexture2D*` | 複製紋理 |
| `FitImageSize(const FVector2D&, const FVector2D&)` | `FVector2D` | 計算適配尺寸 |
| `CopyTexture2DToClipboard(UTexture2D*)` | `void` | 複製到剪貼簿 |
| `IsCanCopyTexture2DToClipboard()` | `bool` | 檢查是否支援 |

####音频工具

| 方法 | 回傳型別 | 描述 |
|------|---------|------|
| `LoadSoundWav(const FString&)` | `USoundWave*` | 從檔案載入音訊 |
| `SaveSoundWav(USoundWave*, const FString&)` | `bool` | 儲存音訊至檔案 |
| `SoundToB64(USoundWave*)` | `FString` | 音訊轉 Base64 |
| `CopySoundWave(const USoundWave*, UObject*, FName)` | `USoundWave*` | 複製音波 |
| `WavDataToSoundWave(const TArray<uint8>&, bool, bool)` | `USoundWave*` | WAV 數據轉音頻 |
| `GetSoundWavePCMData(USoundWave*)` | `TArray<uint8>` | 獲取 PCM 數據 |

####JSON 工具

| 方法 | 返回類型 | 描述 |
|------|---------|------|
| `MergeJsonObjects(const FString&, const FString&)` | `FString` | 合併 JSON 字串 |
| `LoadJsonString(const FString&)` | `TSharedPtr<FJsonObject>` | 解析 JSON 字串 |
| `ToJsonString(const TSharedPtr<FJsonObject>&)` | `FString` | 轉為 JSON 字串 |

####Cllama 工具

| 方法 | 回傳型別 | 描述 |
|------|---------|------|
| `Cllama_IsValid()` | `bool` | 檢查 Cllama 是否可用 |
| `Cllama_IsSupportGpu()` | `bool` | 檢查是否支援 GPU |
| `Cllama_GetSupportBackends()` | `TArray<FString>` | 取得支援的後端 |
| `Cllama_PrepareModelPathFromPak(const FString&)` | `FString` | 從 Pak 準備模型路徑 |

####模型資訊

| 方法 | 回傳型別 | 描述 |
|------|---------|------|
| `GetOpenAIChatDefaultModels()` | `const TArray<FName>&` | OpenAI 預設模型列表 |
| `GetOpenAIChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | 取得 OpenAI 模型資訊 |
| `GetClaudeChatDefaultModels()` | `const TArray<FName>&` | Claude 預設模型列表 |
| `GetClaudeChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | 獲取 Claude 模型資訊 |
| `GetGeminiChatDefaultModels()` | `const TArray<FName>&` | Gemini 預設模型列表 |
| `GetGeminiChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | 取得 Gemini 模型資訊 |

---

### UAIChatPlus_Texture

圖片包裝類，支援非同步載入與Base64轉換。

**標頭檔：** `Common/AIChatPlus_Texture.h`

**靜態工廠方法：**

```cpp
static UAIChatPlus_Texture* New(UTexture2D* InTexture = nullptr, const FString& InSourcePath = "");
static UAIChatPlus_Texture* CreateInBlueprint(UObject* WorldContextObject, UTexture2D* InTexture);
```

**方法：**

| 方法 | 返回類型 | 描述 |
|------|---------|------|
| `LoadFromFile(const FString&)` | `bool` | 從檔案載入（同步） |
`LoadFromFileAsync(const FString&, Callback)` | `FLoadingTaskType*` | 從檔案載入（非同步） |
| `LoadFromAsset(UObject*, const FString&)` | `bool` | 從資產載入（同步） |
| `LoadFromAssetAsync(UObject*, Callback, const FString&)` | `FLoadingTaskType*` | 從資產載入（非同步） |
| `ToB64()` | `const FString&` | 轉為 Base64（同步） |
| `ToB64Async(Callback)` | `FLoadingTaskType*` | 轉為 Base64（非同步） |
| `GetBrush(bool)` | `const FSlateBrush*` | 獲取 Slate 筆刷 |
| `GetBrushCopy(bool)` | `FSlateBrush` | 取得筆刷副本 |
| `GetSize()` | `FIntVector2` | 獲取尺寸 |
| `GetSize2D()` | `FVector2D` | 獲取尺寸（浮點） |
| `IsValid()` | `bool` | 檢查是否有效 |
| `IsLoading()` | `bool` | 檢查是否加載中 |
| `Reset()` | `void` | 重置 |
| `WaitLoadingComplete()` | `void` | 等待載入完成 |

---

### UAIChatPlus_Sound

音頻包裝類，支援非同步載入與Base64轉換。

**標頭檔案：** `Common/AIChatPlus_Sound.h`

**靜態工廠方法：**

```cpp
static UAIChatPlus_Sound* New(USoundWave* InSound = nullptr, const FString& InSourcePath = "");
static UAIChatPlus_Sound* CreateInBlueprint(UObject* WorldContextObject, USoundWave* InSound);
```

**方法：**

| 方法 | 返回型別 | 描述 |
|------|---------|------|
| `LoadFromFile(const FString&)` | `bool` | 從檔案載入（同步） |
| `LoadFromFileAsync(const FString&, Callback)` | `FLoadingTaskType*` | 從檔案載入（非同步） |
| `LoadFromAsset(UObject*, const FString&)` | `bool` | 從資產載入（同步） |
| `LoadFromAssetAsync(UObject*, Callback, const FString&)` | `FLoadingTaskType*` | 從資產載入（非同步） |
| `ToB64()` | `const FString&` | 轉為 Base64（同步） |
| `ToB64Async(Callback)` | `FLoadingTaskType*` | 轉為 Base64（非同步） |
| `IsValid()` | `bool` | 檢查是否有效 |
| `IsLoading()` | `bool` | 檢查是否加載中 |
| `Reset()` | `void` | 重置 |
| `WaitLoadingComplete()` | `void` | 等待載入完成 |
| `PlayInEditor()` | `void` | 在編輯器中播放 |

---

##JSON 類別

### UAIChatPlus_JsonObject

JSON 物件包裝類別。

**頭文件：** `Common/Json/AIChatPlus_JsonObject.h`

**靜態工廠方法：**

```cpp
static UAIChatPlus_JsonObject* Create();
static UAIChatPlus_JsonObject* Parse(const FString& JsonString, bool& bSuccess, FString& ErrorMessage);
static UAIChatPlus_JsonObject* FromStruct(const int32& Struct);  // CustomThunk
```

**設置欄位方法（支援鏈式調用）：**

| 方法 | 返回型別 | 描述 |
|-------|----------|-------|
|------|---------|------|
| `SetStringField(const FString&, const FString&)` | `UAIChatPlus_JsonObject*` | 設定字串欄位 |
| `SetNumberField(const FString&, float)` | `UAIChatPlus_JsonObject*` | 設定數字欄位 |
| `SetIntegerField(const FString&, int32)` | `UAIChatPlus_JsonObject*` | 設定整數字段 |
| `SetBooleanField(const FString&, bool)` | `UAIChatPlus_JsonObject*` | 設置布爾字段 |
| `SetObjectField(const FString&, UAIChatPlus_JsonObject*)` | `UAIChatPlus_JsonObject*` | 設置物件欄位 |
| `SetArrayField(const FString&, UAIChatPlus_JsonArray*)` | `UAIChatPlus_JsonObject*` | 設定陣列欄位 |
| `SetNullField(const FString&)` | `UAIChatPlus_JsonObject*` | 設定空字段 |

**獲取字段方法：**

| 方法     | 返回類型  | 描述     |
|------|---------|------|
| `GetStringField(const FString&, const FString&, bool&)` | `FString` | 獲取字串 |
| `GetNumberField(const FString&, float, bool&)` | `float` | 獲取數字 |
| `GetIntegerField(const FString&, int32, bool&)` | `int32` | 獲取整數 |
| `GetBooleanField(const FString&, bool, bool&)` | `bool` | 獲取布爾值 |
| `GetObjectField(const FString&, bool&)` | `UAIChatPlus_JsonObject*` | 獲取物件 |
| `GetArrayField(const FString&, bool&)` | `UAIChatPlus_JsonArray*` | 獲取陣列 |

**其他方法：**

| 方法     | 返回類型   | 描述         |
|------|---------|------|
| `HasField(const FString&)` | `bool` | 檢查欄位存在 |
| `GetFieldType(const FString&)` | `EAIChatPlus_JsonValueType` | 獲取欄位類型 |
| `RemoveField(const FString&)` | `UAIChatPlus_JsonObject*` | 移除欄位 |
| `Clear()` | `UAIChatPlus_JsonObject*` | 清空所有欄位 |
| `ToString(bool)` | `FString` | 轉為字串 |
| `ToStruct(int32&)` | `bool` | 轉為結構體 |
| `Merge(UAIChatPlus_JsonObject*, bool)` | `UAIChatPlus_JsonObject*` | 合併物件 |
| `Duplicate()` | `UAIChatPlus_JsonObject*` | 複製物件 |
| `IsValid()` | `bool` | 檢查有效性 |

**路徑查詢方法：**

| 方法 | 返回類型 | 描述 |
|------|---------|------|
| `SetStringByPath(const FString&, const FString&, const FAIChatPlus_JsonPathOptions&)` | `UAIChatPlus_JsonObject*` | 依路徑設定字串 |
| `GetStringByPath(const FString&, const FString&, FAIChatPlus_JsonQueryResult&)` | `FString` | 按路徑獲取字符串 |

---

### UAIChatPlus_JsonArray

JSON 陣列包裝類。

**標頭檔：** `Common/Json/AIChatPlus_JsonArray.h`

**靜態工廠方法：**

```cpp
static UAIChatPlus_JsonArray* Create();
static UAIChatPlus_JsonArray* Parse(const FString& JsonString, bool& bSuccess, FString& ErrorMessage);
static UAIChatPlus_JsonArray* FromStringArray(const TArray<FString>& Values);
static UAIChatPlus_JsonArray* FromIntegerArray(const TArray<int32>& Values);
```

**添加元素方法（支援鏈式呼叫）：**

| 方法         | 返回類型     | 描述         |
|------|---------|------|
| `AddString(const FString&)` | `UAIChatPlus_JsonArray*` | 新增字串 |
| `AddNumber(float)` | `UAIChatPlus_JsonArray*` | 添加數字 |
| `AddInteger(int32)` | `UAIChatPlus_JsonArray*` | 添加整數 |
| `AddBoolean(bool)` | `UAIChatPlus_JsonArray*` | 添加布林值 |
| `AddObject(UAIChatPlus_JsonObject*)` | `UAIChatPlus_JsonArray*` | 添加物件 |
| `AddArray(UAIChatPlus_JsonArray*)` | `UAIChatPlus_JsonArray*` | 新增陣列 |
| `AddNull()` | `UAIChatPlus_JsonArray*` | 添加空值 |

**獲取元素方法：**

| 方法 | 返回類型 | 描述 |
|------|---------|------|
| `GetString(int32, const FString&, bool&)` | `FString` | 獲取字串 |
| `GetNumber(int32, float, bool&)` | `float` | 獲取數字 |
| `GetInteger(int32, int32, bool&)` | `int32` | 取得整數 |
| `GetBoolean(int32, bool, bool&)` | `bool` | 獲取布林 |
| `GetObject(int32, bool&)` | `UAIChatPlus_JsonObject*` | 取得對象 |
| `GetArray(int32, bool&)` | `UAIChatPlus_JsonArray*` | 獲取陣列 |

**其他方法：**

| 方法 | 回傳型別 | 描述 |
|------|---------|------|
| `Length()` | `int32` | 取得長度 |
| `GetElementType(int32)` | `EAIChatPlus_JsonValueType` | 獲取元素類型 |
| `SetString(int32, const FString&, bool&)` | `UAIChatPlus_JsonArray*` | 設定字串 |
| `SetObject(int32, UAIChatPlus_JsonObject*, bool&)` | `UAIChatPlus_JsonArray*` | 設定物件 |
| `RemoveAt(int32, bool&)` | `UAIChatPlus_JsonArray*` | 移除元素 |
| `Clear()` | `UAIChatPlus_JsonArray*` | 清空陣列 |
以下是翻譯後的文本：

| `ToString(bool)` | `FString` | 轉為字串 |
| `Duplicate()` | `UAIChatPlus_JsonArray*` | 複製陣列 |
| `IsValid()` | `bool` | 檢查有效性 |

---

### UAIChatPlus_JsonLibrary

JSON 靜態工具庫。

**標頭檔：** `Common/Json/AIChatPlus_JsonLibrary.h`

**創建方法：**

| 方法 | 返回類型 | 描述 |
|------|---------|------|
| `MakeJsonObjectWithStringField(const FString&, const FString&)` | `UAIChatPlus_JsonObject*` | 建立單字段物件 |
| `MakeJsonObjectFromStringMap(const TMap<FString, FString>&)` | `UAIChatPlus_JsonObject*` | 從 Map 建立物件 |

**驗證方法：**

| 方法 | 返回類型 | 描述 |
|------|---------|------|
| `ValidateJsonString(const FString&, FString&)` | `bool` | 驗證 JSON 字串 |
| `IsJsonObject(const FString&)` | `bool` | 檢查是否為物件 |
| `IsJsonArray(const FString&)` | `bool` | 檢查是否為陣列 |

**格式化方法：**

| 方法 | 回傳型別 | 描述 |
|------|---------|------|
| `PrettifyJson(const FString&)` | `FString` | 美化 JSON |
| `MinifyJson(const FString&)` | `FString` | 壓縮 JSON |

**結構體轉換（CustomThunk）：**

| 方法 | 回傳型別 | 描述 |
|------|---------|------|
| `JsonStringToStruct(const FString&, int32&)` | `bool` | JSON 轉結構體 |
| `StructToJsonString(const int32&, bool)` | `FString` | 結構體轉 JSON |

**檔案操作：**

| 方法 | 返回類型 | 描述 |
|------|---------|------|
| `LoadJsonObjectFromFile(const FString&, bool&, FString&)` | `UAIChatPlus_JsonObject*` | 從檔案載入物件 |
| `SaveJsonObjectToFile(UAIChatPlus_JsonObject*, const FString&, bool, FString&)` | `bool` | 將物件儲存至檔案 |
| `LoadJsonArrayFromFile(const FString&, bool&, FString&)` | `UAIChatPlus_JsonArray*` | 從檔案載入陣列 |
| `SaveJsonArrayToFile(UAIChatPlus_JsonArray*, const FString&, bool, FString&)` | `bool` | 將陣列儲存至檔案 |

**比較方法：**

| 方法 | 回傳型別 | 描述 |
|------|---------|------|
| `EqualsJsonObject(UAIChatPlus_JsonObject*, UAIChatPlus_JsonObject*)` | `bool` | 比較物件 |
| `EqualsJsonArray(UAIChatPlus_JsonArray*, UAIChatPlus_JsonArray*)` | `bool` | 比較陣列 |

**路徑查詢：**

| 方法 | 回傳類型 | 描述 |
|------|---------|------|
| `QueryStringByPath(UAIChatPlus_JsonObject*, const FString&, const FString&, FAIChatPlus_JsonQueryResult&)` | `FString` | 按路徑查詢字串 |
| `QueryObjectByPath(UAIChatPlus_JsonObject*, const FString&, FAIChatPlus_JsonQueryResult&)` | `UAIChatPlus_JsonObject*` | 依路徑查詢物件 |
| `QueryArrayByPath(UAIChatPlus_JsonObject*, const FString&, FAIChatPlus_JsonQueryResult&)` | `UAIChatPlus_JsonArray*` | 按路徑查詢陣列 |

--8<-- "footer_tc.md"


> 此貼文是使用 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
