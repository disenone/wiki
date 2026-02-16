---
layout: post
title: API Reference
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini, Ollama, llama.cpp]
description: API Reference
---
<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - API Reference" />

# C++ 篇 - API Reference

本文档提供 AIChatPlus 插件的 C++ API 参考，包含所有公开类、结构体、枚举和关键方法的说明。

## 目录

- [枚举类型](##枚举类型)
- [核心基类](##核心基类)
- [Handler 类](##handler-类)
- [Request 类](##request-类)
- [工具类](##工具类)
- [JSON 类](##json-类)

---

## 枚举类型

### EAIChatPlus_ChatApiProvider

AI 聊天 API 提供商枚举。

```cpp
enum class EAIChatPlus_ChatApiProvider : uint8
{
    OpenAI,         // OpenAI API
    Azure,          // Azure OpenAI API
    Claude,         // Anthropic Claude API
    Gemini,         // Google Gemini API
    Ollama,         // Ollama 本地服务
    Cllama,         // llama.cpp 直接调用（已废弃）
    CllamaServer    // llama.cpp 服务器模式
};
```

### EAIChatPlus_ImageApiProvider

图片生成 API 提供商枚举。

```cpp
enum class EAIChatPlus_ImageApiProvider : uint8
{
    OpenAI,   // OpenAI DALL-E
    Azure     // Azure OpenAI DALL-E
};
```

### EAIChatPlus_ChatRole

消息角色枚举。

```cpp
enum class EAIChatPlus_ChatRole : uint8
{
    System,     // 系统指令（旧模型）
    User,       // 用户消息
    Assistant,  // AI 回复
    Developer,  // 开发者指令（o1+ 模型）
    Tool        // 工具调用结果
};
```

### EAIChatPlus_ImageChatType

图片操作类型枚举。

```cpp
enum class EAIChatPlus_ImageChatType : uint8
{
    Generation,  // 图片生成
    Edit,        // 图片编辑
    Variation    // 图片变体
};
```

### EAIChatPlus_JsonValueType

JSON 值类型枚举。

```cpp
enum class EAIChatPlus_JsonValueType : uint8
{
    None,     // 无效
    Null,     // 空值
    String,   // 字符串
    Number,   // 数字
    Boolean,  // 布尔
    Array,    // 数组
    Object    // 对象
};
```

---

## 核心基类

### UAIChatPlus_RequestBase

所有请求的基类（抽象类）。

**关键方法：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `SendRequest()` | `bool` | 发送请求 |
| `StopRequest()` | `void` | 停止请求 |
| `Activate()` | `void` | 激活请求对象 |
| `IsActivated()` | `bool` | 检查是否已激活 |
| `SetIsAutoDestroy(bool)` | `void` | 设置完成后自动销毁 |

**委托：**

| 委托名 | 签名 | 描述 |
|--------|------|------|
| `OnStartedListeners` | `void()` | 请求开始 |
| `OnMessageListeners` | `void(const FString&)` | 收到流式消息 |
| `OnFinishedListeners` | `void(const FAIChatPlus_PointerWrapper&)` | 请求完成 |
| `OnFailedListeners` | `void(const FAIChatPlus_PointerWrapper&)` | 请求失败 |

---

### UAIChatPlus_ChatRequestBase

聊天请求基类，继承自 `UAIChatPlus_RequestBase`。

**静态工厂方法：**

```cpp
// 按 Provider 创建请求
static UAIChatPlus_ChatRequestBase* CreateByApi(EAIChatPlus_ChatApiProvider InApiProvider);
static UAIChatPlus_ChatRequestBase* CreateByApiInWorld(EAIChatPlus_ChatApiProvider InApiProvider, const UObject* InWorldContext);
```

**关键方法：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `SetMessages(const TArray<FAIChatPlus_ChatRequestMessage>&)` | `void` | 设置消息列表 |
| `GetFullUrl()` | `FString` | 获取完整请求 URL |
| `GetModelText()` | `FString` | 获取模型名称 |
| `GetTokenUsageText()` | `FString` | 获取 Token 用量描述 |
| `GetApiProvider()` | `EAIChatPlus_ChatApiProvider` | 获取 API Provider 类型 |

---

### UAIChatPlus_ImageRequestBase

图片请求基类，继承自 `UAIChatPlus_RequestBase`。

**静态工厂方法：**

```cpp
static UAIChatPlus_ImageRequestBase* CreateByApi(EAIChatPlus_ImageApiProvider InApiProvider);
static UAIChatPlus_ImageRequestBase* CreateByApiInWorld(EAIChatPlus_ImageApiProvider InApiProvider, const UObject* InWorldContext);
```

**关键方法：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `SetPrompt(const FString&)` | `void` | 设置图片生成提示词 |
| `SetImages(const TArray<UAIChatPlus_Texture*>&)` | `void` | 设置输入图片（编辑/变体） |
| `GetModelText()` | `FString` | 获取模型名称 |
| `GetStyleText()` | `FString` | 获取风格名称 |
| `GetRevisedPrompt()` | `FString` | 获取修正后的提示词 |
| `GetImageChatType()` | `FString` | 获取图片操作类型 |

---

### UAIChatPlus_ModelRequestBase

模型列表请求基类，继承自 `UAIChatPlus_RequestBase`。

**静态工厂方法：**

```cpp
static UAIChatPlus_ModelRequestBase* CreateByApi(EAIChatPlus_ChatApiProvider InApiProvider);
static UAIChatPlus_ModelRequestBase* CreateByApiInWorld(EAIChatPlus_ChatApiProvider InApiProvider, const UObject* InWorldContext);
```

---

## Handler 类

### UAIChatPlus_HandlerBase

所有 Handler 的基类。

**关键方法：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `SetIsAutoDestroy(bool)` | `void` | 设置自动销毁 |
| `AutoDestroy()` | `void` | 执行自动销毁 |
| `Destroy()` | `void` | 立即销毁 |

---

### UAIChatPlus_ChatHandlerBase

聊天请求 Handler，继承自 `UAIChatPlus_HandlerBase`。

**静态工厂方法：**

```cpp
static UAIChatPlus_ChatHandlerBase* New();
```

**绑定方法：**

| 方法 | 描述 |
|------|------|
| `BindChatRequest(UAIChatPlus_ChatRequestBase*)` | 绑定聊天请求 |
| `BindImageRequest(UAIChatPlus_ImageRequestBase*)` | 绑定图片请求 |
| `BindModelRequest(UAIChatPlus_ModelRequestBase*)` | 绑定模型请求 |
| `ClearDelegates()` | 清除所有委托绑定 |

**委托：**

| 委托名 | 签名 | 描述 |
|--------|------|------|
| `OnStarted` | `void()` | 请求开始 |
| `OnStopped` | `void()` | 请求停止 |
| `OnMessage` | `void(const FString&)` | 流式消息 |
| `OnMessageFinished` | `void(const FAIChatPlus_MessageFinishedPayload&)` | 消息完成 |
| `OnUpdated` | `void(const FAIChatPlus_PointerWrapper&)` | 请求更新 |
| `OnFinished` | `void(const FAIChatPlus_PointerWrapper&)` | 请求完成 |
| `OnFailed` | `void(const FAIChatPlus_PointerWrapper&)` | 请求失败 |
| `OnImages` | `void(const TArray<UTexture2D*>&, bool)` | 图片生成 |
| `OnModels` | `void(const TArray<FString>&)` | 模型列表 |

---

### UAIChatPlus_CllamaServerHandler

CllamaServer 专用 Handler。

**静态工厂方法：**

```cpp
static UAIChatPlus_CllamaServerHandler* CreateHandler();
```

**委托：**

| 委托名 | 签名 | 描述 |
|--------|------|------|
| `OnServerStarted` | `void(FGuid)` | 服务器启动 |
| `OnServerStopped` | `void(FGuid)` | 服务器停止 |
| `OnServerFailed` | `void(FGuid, const FString&)` | 服务器失败 |

---

## Request 类

所有 Provider 的 Request 类都遵循相同的工厂方法模式：

### 通用工厂方法模式

```cpp
// 以 OpenAI 为例，其他 Provider 类似
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

### 通用静态方法

所有 Request 类都提供 `CastWrapperToResponse` 方法用于类型转换：

```cpp
// 从 PointerWrapper 提取响应数据
static FAIChatPlus_XXXResponseBody& CastWrapperToResponse(const FAIChatPlus_PointerWrapper& InWrapper);
static FAIChatPlus_PointerWrapper CastResponseToWrapper(const FAIChatPlus_XXXResponseBody& InResponse);
```

---

### UAIChatPlus_OpenAIChatRequest

OpenAI 聊天请求。

**头文件：** `Common_OpenAI/AIChatPlus_OpenAIChatRequest.h`

**Options 类型：** `FAIChatPlus_OpenAIChatRequestOptions`

**Response 类型：** `FAIChatPlus_OpenAIChatResponseBody`

---

### UAIChatPlus_AzureChatRequest

Azure OpenAI 聊天请求。

**头文件：** `Common_Azure/AIChatPlus_AzureChatRequest.h`

**Options 类型：** `FAIChatPlus_AzureChatRequestOptions`

**Response 类型：** `FAIChatPlus_AzureChatResponseBody`

---

### UAIChatPlus_ClaudeChatRequest

Claude 聊天请求。

**头文件：** `Common_Claude/AIChatPlus_ClaudeChatRequest.h`

**Options 类型：** `FAIChatPlus_ClaudeChatRequestOptions`

**Response 类型：** `FAIChatPlus_ClaudeChatResponseBody`

---

### UAIChatPlus_GeminiChatRequest

Gemini 聊天请求。

**头文件：** `Common_Gemini/AIChatPlus_GeminiChatRequest.h`

**Options 类型：** `FAIChatPlus_GeminiChatRequestOptions`

**Response 类型：** `FAIChatPlus_GeminiChatResponseBody`

---

### UAIChatPlus_OllamaChatRequest

Ollama 聊天请求。

**头文件：** `Common_Ollama/AIChatPlus_OllamaChatRequest.h`

**Options 类型：** `FAIChatPlus_OllamaChatRequestOptions`

**Response 类型：** `FAIChatPlus_OllamaChatResponseBody`

---

### UAIChatPlus_OllamaModelRequest

Ollama 模型列表请求。

**头文件：** `Common_Ollama/AIChatPlus_OllamaModelRequest.h`

**Options 类型：** `FAIChatPlus_OllamaModelRequestOptions`

**Response 类型：** `FAIChatPlus_OllamaModelResponseBody`

**特有方法：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `GetModelNames()` | `TArray<FString>` | 获取模型名称列表 |

---

### UAIChatPlus_CllamaChatRequest（已废弃）

Cllama 离线聊天请求（已废弃，推荐使用 CllamaServer）。

**头文件：** `Common_Cllama/AIChatPlus_CllamaChatRequest.h`

**Options 类型：** `FAIChatPlus_CllamaChatRequestOptions`

**Response 类型：** `FAIChatPlus_CllamaChatResponseBody`

---

### UAIChatPlus_CllamaServerChatRequest

CllamaServer 聊天请求。

**头文件：** `Common_CllamaServer/AIChatPlus_CllamaServerChatRequest.h`

**Options 类型：** `FAIChatPlus_CllamaServerChatRequestOptions`

**Response 类型：** `FAIChatPlus_CllamaServerChatResponseBody`

---

### UAIChatPlus_OpenAIImageRequest

OpenAI 图片生成请求。

**头文件：** `Common_OpenAI/AIChatPlus_OpenAIImageRequest.h`

**Options 类型：** `FAIChatPlus_OpenAIImageRequestOptions`

**Response 类型：** `FAIChatPlus_OpenAIImageResponseBody`

---

### UAIChatPlus_AzureImageRequest

Azure 图片生成请求。

**头文件：** `Common_Azure/AIChatPlus_AzureImageRequest.h`

**Options 类型：** `FAIChatPlus_AzureImageRequestOptions`

**Response 类型：** `FAIChatPlus_AzureImageResponseBody`

---

### UAIChatPlus_CllamaServer

CllamaServer 服务器管理类。

**头文件：** `Common_CllamaServer/AIChatPlus_CllamaServer.h`

**静态工厂方法：**

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

**实例方法：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `Activate()` | `void` | 启动服务器 |
| `StopServer()` | `void` | 停止服务器 |
| `IsRunning()` | `bool` | 检查是否运行中 |
| `GetServerID()` | `FGuid` | 获取服务器 ID |
| `GetHost()` | `FString` | 获取主机地址 |
| `GetAddress()` | `FString` | 获取完整地址 |
| `GetServerInfo(FAIChatPlus_CllamaServerInfo&)` | `bool` | 获取服务器信息 |

**静态管理方法：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `IsServerValid(const FGuid&)` | `bool` | 检查服务器是否有效 |
| `IsServerRunning(const FGuid&)` | `bool` | 检查服务器是否运行中 |
| `StopServerByID(const FGuid&)` | `void` | 按 ID 停止服务器 |
| `StopAllServers()` | `void` | 停止所有服务器 |
| `GetServerByID(const FGuid&)` | `UAIChatPlus_CllamaServer*` | 按 ID 获取服务器 |
| `GetAllServerIDs()` | `TArray<FGuid>` | 获取所有服务器 ID |

---

## 工具类

### UAIChatPlus_Util

通用工具类，提供各种静态辅助方法。

**头文件：** `Common/AIChatPlus_Util.h`

#### 日志相关

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `SetInternalLogVerbosity(EAIChatPlus_LogVerbosityType)` | `void` | 设置内部日志级别 |

#### Wrapper 转换

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `CastWrapperToError(const FAIChatPlus_PointerWrapper&)` | `FAIChatPlus_ResponseErrorBase&` | 提取错误信息 |
| `CastWrapperToResponse(const FAIChatPlus_PointerWrapper&)` | `FAIChatPlus_ChatResponseBodyBase&` | 提取响应数据 |
| `GetErrorWrapperDescription(const FAIChatPlus_PointerWrapper&)` | `FString` | 获取错误描述 |
| `GetResponseWrapperMessage(const FAIChatPlus_PointerWrapper&)` | `FString` | 获取响应消息 |

#### 图片工具

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `LoadImage(const FString&, bool)` | `UTexture2D*` | 从文件加载图片 |
| `SaveImage(UTexture2D*, const FString&)` | `bool` | 保存图片到文件 |
| `ImageToB64(UTexture2D*, int32)` | `FString` | 图片转 Base64 |
| `CopyTexture2D(UTexture2D*, UObject*, FName, EObjectFlags)` | `UTexture2D*` | 复制纹理 |
| `FitImageSize(const FVector2D&, const FVector2D&)` | `FVector2D` | 计算适配尺寸 |
| `CopyTexture2DToClipboard(UTexture2D*)` | `void` | 复制到剪贴板 |
| `IsCanCopyTexture2DToClipboard()` | `bool` | 检查是否支持 |

#### 音频工具

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `LoadSoundWav(const FString&)` | `USoundWave*` | 从文件加载音频 |
| `SaveSoundWav(USoundWave*, const FString&)` | `bool` | 保存音频到文件 |
| `SoundToB64(USoundWave*)` | `FString` | 音频转 Base64 |
| `CopySoundWave(const USoundWave*, UObject*, FName)` | `USoundWave*` | 复制音频 |
| `WavDataToSoundWave(const TArray<uint8>&, bool, bool)` | `USoundWave*` | WAV 数据转音频 |
| `GetSoundWavePCMData(USoundWave*)` | `TArray<uint8>` | 获取 PCM 数据 |

#### JSON 工具

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `MergeJsonObjects(const FString&, const FString&)` | `FString` | 合并 JSON 字符串 |
| `LoadJsonString(const FString&)` | `TSharedPtr<FJsonObject>` | 解析 JSON 字符串 |
| `ToJsonString(const TSharedPtr<FJsonObject>&)` | `FString` | 转为 JSON 字符串 |

#### Cllama 工具

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `Cllama_IsValid()` | `bool` | 检查 Cllama 是否可用 |
| `Cllama_IsSupportGpu()` | `bool` | 检查是否支持 GPU |
| `Cllama_GetSupportBackends()` | `TArray<FString>` | 获取支持的后端 |
| `Cllama_PrepareModelPathFromPak(const FString&)` | `FString` | 从 Pak 准备模型路径 |

#### 模型信息

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `GetOpenAIChatDefaultModels()` | `const TArray<FName>&` | OpenAI 默认模型列表 |
| `GetOpenAIChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | 获取 OpenAI 模型信息 |
| `GetClaudeChatDefaultModels()` | `const TArray<FName>&` | Claude 默认模型列表 |
| `GetClaudeChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | 获取 Claude 模型信息 |
| `GetGeminiChatDefaultModels()` | `const TArray<FName>&` | Gemini 默认模型列表 |
| `GetGeminiChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | 获取 Gemini 模型信息 |

---

### UAIChatPlus_Texture

图片包装类，支持异步加载和 Base64 转换。

**头文件：** `Common/AIChatPlus_Texture.h`

**静态工厂方法：**

```cpp
static UAIChatPlus_Texture* New(UTexture2D* InTexture = nullptr, const FString& InSourcePath = "");
static UAIChatPlus_Texture* CreateInBlueprint(UObject* WorldContextObject, UTexture2D* InTexture);
```

**方法：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `LoadFromFile(const FString&)` | `bool` | 从文件加载（同步） |
| `LoadFromFileAsync(const FString&, Callback)` | `FLoadingTaskType*` | 从文件加载（异步） |
| `LoadFromAsset(UObject*, const FString&)` | `bool` | 从资产加载（同步） |
| `LoadFromAssetAsync(UObject*, Callback, const FString&)` | `FLoadingTaskType*` | 从资产加载（异步） |
| `ToB64()` | `const FString&` | 转为 Base64（同步） |
| `ToB64Async(Callback)` | `FLoadingTaskType*` | 转为 Base64（异步） |
| `GetBrush(bool)` | `const FSlateBrush*` | 获取 Slate 笔刷 |
| `GetBrushCopy(bool)` | `FSlateBrush` | 获取笔刷副本 |
| `GetSize()` | `FIntVector2` | 获取尺寸 |
| `GetSize2D()` | `FVector2D` | 获取尺寸（浮点） |
| `IsValid()` | `bool` | 检查是否有效 |
| `IsLoading()` | `bool` | 检查是否加载中 |
| `Reset()` | `void` | 重置 |
| `WaitLoadingComplete()` | `void` | 等待加载完成 |

---

### UAIChatPlus_Sound

音频包装类，支持异步加载和 Base64 转换。

**头文件：** `Common/AIChatPlus_Sound.h`

**静态工厂方法：**

```cpp
static UAIChatPlus_Sound* New(USoundWave* InSound = nullptr, const FString& InSourcePath = "");
static UAIChatPlus_Sound* CreateInBlueprint(UObject* WorldContextObject, USoundWave* InSound);
```

**方法：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `LoadFromFile(const FString&)` | `bool` | 从文件加载（同步） |
| `LoadFromFileAsync(const FString&, Callback)` | `FLoadingTaskType*` | 从文件加载（异步） |
| `LoadFromAsset(UObject*, const FString&)` | `bool` | 从资产加载（同步） |
| `LoadFromAssetAsync(UObject*, Callback, const FString&)` | `FLoadingTaskType*` | 从资产加载（异步） |
| `ToB64()` | `const FString&` | 转为 Base64（同步） |
| `ToB64Async(Callback)` | `FLoadingTaskType*` | 转为 Base64（异步） |
| `IsValid()` | `bool` | 检查是否有效 |
| `IsLoading()` | `bool` | 检查是否加载中 |
| `Reset()` | `void` | 重置 |
| `WaitLoadingComplete()` | `void` | 等待加载完成 |
| `PlayInEditor()` | `void` | 在编辑器中播放 |

---

## JSON 类

### UAIChatPlus_JsonObject

JSON 对象包装类。

**头文件：** `Common/Json/AIChatPlus_JsonObject.h`

**静态工厂方法：**

```cpp
static UAIChatPlus_JsonObject* Create();
static UAIChatPlus_JsonObject* Parse(const FString& JsonString, bool& bSuccess, FString& ErrorMessage);
static UAIChatPlus_JsonObject* FromStruct(const int32& Struct);  // CustomThunk
```

**设置字段方法（支持链式调用）：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `SetStringField(const FString&, const FString&)` | `UAIChatPlus_JsonObject*` | 设置字符串字段 |
| `SetNumberField(const FString&, float)` | `UAIChatPlus_JsonObject*` | 设置数字字段 |
| `SetIntegerField(const FString&, int32)` | `UAIChatPlus_JsonObject*` | 设置整数字段 |
| `SetBooleanField(const FString&, bool)` | `UAIChatPlus_JsonObject*` | 设置布尔字段 |
| `SetObjectField(const FString&, UAIChatPlus_JsonObject*)` | `UAIChatPlus_JsonObject*` | 设置对象字段 |
| `SetArrayField(const FString&, UAIChatPlus_JsonArray*)` | `UAIChatPlus_JsonObject*` | 设置数组字段 |
| `SetNullField(const FString&)` | `UAIChatPlus_JsonObject*` | 设置空字段 |

**获取字段方法：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `GetStringField(const FString&, const FString&, bool&)` | `FString` | 获取字符串 |
| `GetNumberField(const FString&, float, bool&)` | `float` | 获取数字 |
| `GetIntegerField(const FString&, int32, bool&)` | `int32` | 获取整数 |
| `GetBooleanField(const FString&, bool, bool&)` | `bool` | 获取布尔 |
| `GetObjectField(const FString&, bool&)` | `UAIChatPlus_JsonObject*` | 获取对象 |
| `GetArrayField(const FString&, bool&)` | `UAIChatPlus_JsonArray*` | 获取数组 |

**其他方法：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `HasField(const FString&)` | `bool` | 检查字段存在 |
| `GetFieldType(const FString&)` | `EAIChatPlus_JsonValueType` | 获取字段类型 |
| `RemoveField(const FString&)` | `UAIChatPlus_JsonObject*` | 移除字段 |
| `Clear()` | `UAIChatPlus_JsonObject*` | 清空所有字段 |
| `ToString(bool)` | `FString` | 转为字符串 |
| `ToStruct(int32&)` | `bool` | 转为结构体 |
| `Merge(UAIChatPlus_JsonObject*, bool)` | `UAIChatPlus_JsonObject*` | 合并对象 |
| `Duplicate()` | `UAIChatPlus_JsonObject*` | 复制对象 |
| `IsValid()` | `bool` | 检查有效性 |

**路径查询方法：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `SetStringByPath(const FString&, const FString&, const FAIChatPlus_JsonPathOptions&)` | `UAIChatPlus_JsonObject*` | 按路径设置字符串 |
| `GetStringByPath(const FString&, const FString&, FAIChatPlus_JsonQueryResult&)` | `FString` | 按路径获取字符串 |

---

### UAIChatPlus_JsonArray

JSON 数组包装类。

**头文件：** `Common/Json/AIChatPlus_JsonArray.h`

**静态工厂方法：**

```cpp
static UAIChatPlus_JsonArray* Create();
static UAIChatPlus_JsonArray* Parse(const FString& JsonString, bool& bSuccess, FString& ErrorMessage);
static UAIChatPlus_JsonArray* FromStringArray(const TArray<FString>& Values);
static UAIChatPlus_JsonArray* FromIntegerArray(const TArray<int32>& Values);
```

**添加元素方法（支持链式调用）：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `AddString(const FString&)` | `UAIChatPlus_JsonArray*` | 添加字符串 |
| `AddNumber(float)` | `UAIChatPlus_JsonArray*` | 添加数字 |
| `AddInteger(int32)` | `UAIChatPlus_JsonArray*` | 添加整数 |
| `AddBoolean(bool)` | `UAIChatPlus_JsonArray*` | 添加布尔 |
| `AddObject(UAIChatPlus_JsonObject*)` | `UAIChatPlus_JsonArray*` | 添加对象 |
| `AddArray(UAIChatPlus_JsonArray*)` | `UAIChatPlus_JsonArray*` | 添加数组 |
| `AddNull()` | `UAIChatPlus_JsonArray*` | 添加空值 |

**获取元素方法：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `GetString(int32, const FString&, bool&)` | `FString` | 获取字符串 |
| `GetNumber(int32, float, bool&)` | `float` | 获取数字 |
| `GetInteger(int32, int32, bool&)` | `int32` | 获取整数 |
| `GetBoolean(int32, bool, bool&)` | `bool` | 获取布尔 |
| `GetObject(int32, bool&)` | `UAIChatPlus_JsonObject*` | 获取对象 |
| `GetArray(int32, bool&)` | `UAIChatPlus_JsonArray*` | 获取数组 |

**其他方法：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `Length()` | `int32` | 获取长度 |
| `GetElementType(int32)` | `EAIChatPlus_JsonValueType` | 获取元素类型 |
| `SetString(int32, const FString&, bool&)` | `UAIChatPlus_JsonArray*` | 设置字符串 |
| `SetObject(int32, UAIChatPlus_JsonObject*, bool&)` | `UAIChatPlus_JsonArray*` | 设置对象 |
| `RemoveAt(int32, bool&)` | `UAIChatPlus_JsonArray*` | 移除元素 |
| `Clear()` | `UAIChatPlus_JsonArray*` | 清空数组 |
| `ToString(bool)` | `FString` | 转为字符串 |
| `Duplicate()` | `UAIChatPlus_JsonArray*` | 复制数组 |
| `IsValid()` | `bool` | 检查有效性 |

---

### UAIChatPlus_JsonLibrary

JSON 静态工具库。

**头文件：** `Common/Json/AIChatPlus_JsonLibrary.h`

**创建方法：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `MakeJsonObjectWithStringField(const FString&, const FString&)` | `UAIChatPlus_JsonObject*` | 创建单字段对象 |
| `MakeJsonObjectFromStringMap(const TMap<FString, FString>&)` | `UAIChatPlus_JsonObject*` | 从 Map 创建对象 |

**验证方法：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `ValidateJsonString(const FString&, FString&)` | `bool` | 验证 JSON 字符串 |
| `IsJsonObject(const FString&)` | `bool` | 检查是否为对象 |
| `IsJsonArray(const FString&)` | `bool` | 检查是否为数组 |

**格式化方法：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `PrettifyJson(const FString&)` | `FString` | 美化 JSON |
| `MinifyJson(const FString&)` | `FString` | 压缩 JSON |

**结构体转换（CustomThunk）：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `JsonStringToStruct(const FString&, int32&)` | `bool` | JSON 转结构体 |
| `StructToJsonString(const int32&, bool)` | `FString` | 结构体转 JSON |

**文件操作：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `LoadJsonObjectFromFile(const FString&, bool&, FString&)` | `UAIChatPlus_JsonObject*` | 从文件加载对象 |
| `SaveJsonObjectToFile(UAIChatPlus_JsonObject*, const FString&, bool, FString&)` | `bool` | 保存对象到文件 |
| `LoadJsonArrayFromFile(const FString&, bool&, FString&)` | `UAIChatPlus_JsonArray*` | 从文件加载数组 |
| `SaveJsonArrayToFile(UAIChatPlus_JsonArray*, const FString&, bool, FString&)` | `bool` | 保存数组到文件 |

**比较方法：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `EqualsJsonObject(UAIChatPlus_JsonObject*, UAIChatPlus_JsonObject*)` | `bool` | 比较对象 |
| `EqualsJsonArray(UAIChatPlus_JsonArray*, UAIChatPlus_JsonArray*)` | `bool` | 比较数组 |

**路径查询：**

| 方法 | 返回类型 | 描述 |
|------|---------|------|
| `QueryStringByPath(UAIChatPlus_JsonObject*, const FString&, const FString&, FAIChatPlus_JsonQueryResult&)` | `FString` | 按路径查询字符串 |
| `QueryObjectByPath(UAIChatPlus_JsonObject*, const FString&, FAIChatPlus_JsonQueryResult&)` | `UAIChatPlus_JsonObject*` | 按路径查询对象 |
| `QueryArrayByPath(UAIChatPlus_JsonObject*, const FString&, FAIChatPlus_JsonQueryResult&)` | `UAIChatPlus_JsonArray*` | 按路径查询数组 |

--8<-- "footer.md"
