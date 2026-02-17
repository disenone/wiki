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

#C++ Section - API Reference

This document provides the C++ API reference for the AIChatPlus plugin, including descriptions of all public classes, structures, enumerations, and key methods.

##Table of Contents

- [Enumeration Type](##枚举类型)
- [Core Base Classes](##核心基类)
- [Handler class](##handler-类)
- [Request Class](##request-类)
- [Utility Class](##工具类)
- [JSON Class](##json-类)

---

##Enumeration type

### EAIChatPlus_ChatApiProvider

Enumeration of AI Chat API Providers.

```cpp
enum class EAIChatPlus_ChatApiProvider : uint8
{
    OpenAI,         // OpenAI API
    Azure,          // Azure OpenAI API
    Claude,         // Anthropic Claude API
    Gemini,         // Google Gemini API
Ollama,         // Ollama local service
    Cllama,         // Direct call to llama.cpp (deprecated)
CllamaServer    // llama.cpp server mode
};
```

### EAIChatPlus_ImageApiProvider

Enumeration of Image Generation API Providers.

```cpp
enum class EAIChatPlus_ImageApiProvider : uint8
{
    OpenAI,   // OpenAI DALL-E
    Azure     // Azure OpenAI DALL-E
};
```

### EAIChatPlus_ChatRole

Message Role Enumeration.

```cpp
enum class EAIChatPlus_ChatRole : uint8
{
System,     // System commands (legacy model)
User,       // User message
Assistant, // AI response
Developer, // Developer command (o1+ model)
Tool        // Tool invocation result
};
```

### EAIChatPlus_ImageChatType

Image Operation Type Enumeration.

```cpp
enum class EAIChatPlus_ImageChatType : uint8
{
Generation,  // Image generation
Edit,        // Image editing
Variation    // Image variant
};
```

### EAIChatPlus_JsonValueType

Enumeration of JSON value types.

```cpp
enum class EAIChatPlus_JsonValueType : uint8
{
None,     // Invalid
Null,     // Null value
String,   // String
Number,   // Number
Boolean,  // Boolean
Array,    // Array
Object    // Object
};
```

---

##Core Base Class

### UAIChatPlus_RequestBase

Base class for all requests (abstract class).

**Key Methods:**

| Method | Return Type | Description |
|------|---------|------|
| `SendRequest()` | `bool` | Send Request |
| `StopRequest()` | `void` | Stop request |
| `Activate()` | `void` | Activates the request object |
| `IsActivated()` | `bool` | Checks if it has been activated |
| `SetIsAutoDestroy(bool)` | `void` | Automatically destroy upon completion |

**Authorization:**

| Delegation Name | Signature | Description |
|--------|------|------|
| `OnStartedListeners` | `void()` | Request started |
| `OnMessageListeners` | `void(const FString&)` | Receiving streaming messages |
| `OnFinishedListeners` | `void(const FAIChatPlus_PointerWrapper&)` | Request Completed |
| `OnFailedListeners` | `void(const FAIChatPlus_PointerWrapper&)` | Request failed |

---

### UAIChatPlus_ChatRequestBase

Chat request base class, inherited from `UAIChatPlus_RequestBase`.

**Static Factory Method:**

```cpp
// Create a request by Provider
static UAIChatPlus_ChatRequestBase* CreateByApi(EAIChatPlus_ChatApiProvider InApiProvider);
static UAIChatPlus_ChatRequestBase* CreateByApiInWorld(EAIChatPlus_ChatApiProvider InApiProvider, const UObject* InWorldContext);
```

**Key Methods:**

| Method | Return Type | Description |
|------|---------|------|
| `SetMessages(const TArray<FAIChatPlus_ChatRequestMessage>&)` | `void` | Sets the message list |
Here is the translation of the text into English:

| `GetFullUrl()` | `FString` | Retrieves the complete request URL |
| `GetModelText()` | `FString` | Retrieve the model name |
| `GetTokenUsageText()` | `FString` | Retrieves the description of Token usage |
| `GetApiProvider()` | `EAIChatPlus_ChatApiProvider` | Retrieves the API Provider type |

---

### UAIChatPlus_ImageRequestBase

Image request base class, inheriting from `UAIChatPlus_RequestBase`.

**Static Factory Methods:**

```cpp
static UAIChatPlus_ImageRequestBase* CreateByApi(EAIChatPlus_ImageApiProvider InApiProvider);
static UAIChatPlus_ImageRequestBase* CreateByApiInWorld(EAIChatPlus_ImageApiProvider InApiProvider, const UObject* InWorldContext);
```

**Key Methods:**

| Method | Return Type | Description |
|------|---------|------|
| `SetPrompt(const FString&)` | `void` | Sets the image generation prompt |
| `SetImages(const TArray<UAIChatPlus_Texture*>&)` | `void` | Set input images (edit/variant) |
| `GetModelText()` | `FString` | Get Model Name |
| `GetStyleText()` | `FString` | Retrieves the style name |
| `GetRevisedPrompt()` | `FString` | Retrieves the revised prompt |
| `GetImageChatType()` | `FString` | Retrieve image operation type |

---

### UAIChatPlus_ModelRequestBase

Model list request base class, inherits from `UAIChatPlus_RequestBase`.

**Static Factory Methods:**

```cpp
static UAIChatPlus_ModelRequestBase* CreateByApi(EAIChatPlus_ChatApiProvider InApiProvider);
static UAIChatPlus_ModelRequestBase* CreateByApiInWorld(EAIChatPlus_ChatApiProvider InApiProvider, const UObject* InWorldContext);
```

---

##Handler class

### UAIChatPlus_HandlerBase

Base class for all Handlers.

**Key Methods:**

| Method | Return Type | Description |
|------|---------|------|
| `SetIsAutoDestroy(bool)` | `void` | Sets auto-destruction |
| `AutoDestroy()` | `void` | Perform auto-destruction |
| `Destroy()` | `void` | Immediately destroys |

---

### UAIChatPlus_ChatHandlerBase

Chat Request Handler, inherits from `UAIChatPlus_HandlerBase`.

**Static Factory Methods:**

```cpp
static UAIChatPlus_ChatHandlerBase* New();
```

**Binding Method:**

| Method | Description |
|------|------|
| `BindChatRequest(UAIChatPlus_ChatRequestBase*)` | Bind Chat Request |
| `BindImageRequest(UAIChatPlus_ImageRequestBase*)` | Bind Image Request |
| `BindModelRequest(UAIChatPlus_ModelRequestBase*)` | Bind Model Request |
| `ClearDelegates()` | Clears all delegate bindings |

**Entrustment:**

| Delegated Name | Signature | Description |
|--------|------|------|
| `OnStarted` | `void()` | Request initiated |
| `OnStopped` | `void()` | Request Stop |
| `OnMessage` | `void(const FString&)` | Streaming Message |
| `OnMessageFinished` | `void(const FAIChatPlus_MessageFinishedPayload&)` | Message Completed |
| `OnUpdated` | `void(const FAIChatPlus_PointerWrapper&)` | Update Requested |
| `OnFinished` | `void(const FAIChatPlus_PointerWrapper&)` | Request completed |
| `OnFailed` | `void(const FAIChatPlus_PointerWrapper&)` | Request failed |
| `OnImages` | `void(const TArray<UTexture2D*>&, bool)` | Image Generation |
| `OnModels` | `void(const TArray<FString>&)` | List of Models |

---

### UAIChatPlus_CllamaServerHandler

Custom Handler for CllamaServer.

**Static Factory Method:**

```cpp
static UAIChatPlus_CllamaServerHandler* CreateHandler();
```

**Entrustment:**

| Delegation Name | Signature | Description |
|--------|------|------|
| `OnServerStarted` | `void(FGuid)` | Server Started |
| `OnServerStopped` | `void(FGuid)` | Server stopped |
| `OnServerFailed` | `void(FGuid, const FString&)` | Server Failure |

---

##Request Class

All Provider Request classes follow the same factory method pattern:

###Generic Factory Method Pattern

```cpp
// Taking OpenAI as an example, other Providers are similar
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

###Generic Static Methods

All Request classes provide the `CastWrapperToResponse` method for type conversion:

```cpp
// Extract response data from PointerWrapper
static FAIChatPlus_XXXResponseBody& CastWrapperToResponse(const FAIChatPlus_PointerWrapper& InWrapper);
static FAIChatPlus_PointerWrapper CastResponseToWrapper(const FAIChatPlus_XXXResponseBody& InResponse);
```

---

### UAIChatPlus_OpenAIChatRequest

OpenAI chat request.

**Header file:** `Common_OpenAI/AIChatPlus_OpenAIChatRequest.h`

**Options Type:** `FAIChatPlus_OpenAIChatRequestOptions`

**Response Type:** `FAIChatPlus_OpenAIChatResponseBody`

---

### UAIChatPlus_AzureChatRequest

Azure OpenAI chat request.

**Header File:** `Common_Azure/AIChatPlus_AzureChatRequest.h`

**Options Type:** `FAIChatPlus_AzureChatRequestOptions`

**Response Type:** `FAIChatPlus_AzureChatResponseBody`

---

### UAIChatPlus_ClaudeChatRequest

Claude chat request.

**Header File:** `Common_Claude/AIChatPlus_ClaudeChatRequest.h`

**Option Type:** `FAIChatPlus_ClaudeChatRequestOptions`

**Response Type:** `FAIChatPlus_ClaudeChatResponseBody`

---

### UAIChatPlus_GeminiChatRequest

Gemini chat request.

**Header File:** `Common_Gemini/AIChatPlus_GeminiChatRequest.h`

**Options Type:** `FAIChatPlus_GeminiChatRequestOptions`

**Response Type:** `FAIChatPlus_GeminiChatResponseBody`

---

### UAIChatPlus_OllamaChatRequest

Ollama chat request.

**Header File:** `Common_Ollama/AIChatPlus_OllamaChatRequest.h`

**Options Type:** `FAIChatPlus_OllamaChatRequestOptions`

**Response Type:** `FAIChatPlus_OllamaChatResponseBody`

---

### UAIChatPlus_OllamaModelRequest

Requesting Ollama model list.

**Header File:** `Common_Ollama/AIChatPlus_OllamaModelRequest.h`

**Options Type:** `FAIChatPlus_OllamaModelRequestOptions`

**Response Type:** `FAIChatPlus_OllamaModelResponseBody`

**Unique Methods：**

| Method | Return Type | Description |
|------|---------|------|
| `GetModelNames()` | `TArray<FString>` | Retrieves a list of model names |

---

###UAIChatPlus_CllamaChatRequest (Deprecated)

Cllama offline chat request (deprecated, CllamaServer recommended).

**Header File:** `Common_Cllama/AIChatPlus_CllamaChatRequest.h`

**Type of Options:** `FAIChatPlus_CllamaChatRequestOptions`

**Response Type:** `FAIChatPlus_CllamaChatResponseBody`

---

### UAIChatPlus_CllamaServerChatRequest

CllamaServer chat request.

**Header File:** `Common_CllamaServer/AIChatPlus_CllamaServerChatRequest.h`

**Options Type:** `FAIChatPlus_CllamaServerChatRequestOptions`

**Response Type:** `FAIChatPlus_CllamaServerChatResponseBody`

---

### UAIChatPlus_OpenAIImageRequest

OpenAI image generation request.

**Header File:** `Common_OpenAI/AIChatPlus_OpenAIImageRequest.h`

**Option Type:** `FAIChatPlus_OpenAIImageRequestOptions`

**Response Type:** `FAIChatPlus_OpenAIImageResponseBody`

---

### UAIChatPlus_AzureImageRequest

Azure image generation request.

**Header File:** `Common_Azure/AIChatPlus_AzureImageRequest.h`

**Options Type:** `FAIChatPlus_AzureImageRequestOptions`

**Response Type:** `FAIChatPlus_AzureImageResponseBody`

---

### UAIChatPlus_CllamaServer

CllamaServer Server Management Class.

**Header File:** `Common_CllamaServer/AIChatPlus_CllamaServer.h`

**Static Factory Method:**

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

**Instance Methods:**

| Method | Return Type | Description |
|------|---------|------|
| `Activate()` | `void` | Starts the server |
| `StopServer()` | `void` | Stop the server |
| `IsRunning()` | `bool` | Checks if it is currently running |
| `GetServerID()` | `FGuid` | Get Server ID |
| `GetHost()` | `FString` | Retrieves the host address |
| `GetAddress()` | `FString` | Get the complete address |
| `GetServerInfo(FAIChatPlus_CllamaServerInfo&)` | `bool` | Retrieves server information |

**Static Management Method:**

| Method | Return Type | Description |
|------|---------|------|
| `IsServerValid(const FGuid&)` | `bool` | Checks if the server is valid |
| `IsServerRunning(const FGuid&)` | `bool` | Checks if the server is currently running |
| `StopServerByID(const FGuid&)` | `void` | Stop the server by ID |
| `StopAllServers()` | `void` | Stops all servers |
| `GetServerByID(const FGuid&)` | `UAIChatPlus_CllamaServer*` | Get server by ID |
| `GetAllServerIDs()` | `TArray<FGuid>` | Get all server IDs |

---

##Utility Class

### UAIChatPlus_Util

General utility class providing various static helper methods.

**Header File:** `Common/AIChatPlus_Util.h`

####Log Related

| Method | Return Type | Description |
|------|---------|------|
| `SetInternalLogVerbosity(EAIChatPlus_LogVerbosityType)` | `void` | Sets the internal log verbosity level |

####Wrapper Conversion

| Method | Return Type | Description |
|------|---------|------|
| `CastWrapperToError(const FAIChatPlus_PointerWrapper&)` | `FAIChatPlus_ResponseErrorBase&` | Extract error information |
| `CastWrapperToResponse(const FAIChatPlus_PointerWrapper&)` | `FAIChatPlus_ChatResponseBodyBase&` | Extract response data |
| `GetErrorWrapperDescription(const FAIChatPlus_PointerWrapper&)` | `FString` | Gets the error description |
| `GetResponseWrapperMessage(const FAIChatPlus_PointerWrapper&)` | `FString` | Retrieve response message |

####Image Tool

| Method | Return Type | Description |
|------|---------|------|
| `LoadImage(const FString&, bool)` | `UTexture2D*` | Loads an image from a file |
| `SaveImage(UTexture2D*, const FString&)` | `bool` | Save image to file |
| `ImageToB64(UTexture2D*, int32)` | `FString` | Image to Base64 |
| `CopyTexture2D(UTexture2D*, UObject*, FName, EObjectFlags)` | `UTexture2D*` | Copy Texture |
| `FitImageSize(const FVector2D&, const FVector2D&)` | `FVector2D` | Calculate fitted size |
| `CopyTexture2DToClipboard(UTexture2D*)` | `void` | Copy to Clipboard |
| `IsCanCopyTexture2DToClipboard()` | `bool` | Checks if supported |

####Audio Tools

| Method | Return Type | Description |
|------|---------|------|
| `LoadSoundWav(const FString&)` | `USoundWave*` | Loads audio from file |
| `SaveSoundWav(USoundWave*, const FString&)` | `bool` | Save audio to file |
| `SoundToB64(USoundWave*)` | `FString` | Audio to Base64 |
| `CopySoundWave(const USoundWave*, UObject*, FName)` | `USoundWave*` | Copy Sound Wave |
| `WavDataToSoundWave(const TArray<uint8>&, bool, bool)` | `USoundWave*` | Convert WAV Data to Sound Wave |
Here's the translation of the text into English:

| `GetSoundWavePCMData(USoundWave*)` | `TArray<uint8>` | Retrieve PCM Data |

####JSON Tools

| Method | Return Type | Description |
|------|---------|------|
{
  "Translation": {
    "Function": "MergeJsonObjects(const FString&, const FString&)",
    "ReturnType": "FString",
    "Description": "Merge JSON strings"
  }
}
| `LoadJsonString(const FString&)` | `TSharedPtr<FJsonObject>` | Parses JSON string |
| `ToJsonString(const TSharedPtr<FJsonObject>&)` | `FString` | Convert to JSON string |

####Cllama Tool

| Method | Return Type | Description |
|------|---------|------|
| `Cllama_IsValid()` | `bool` | Check if Cllama is available |
| `Cllama_IsSupportGpu()` | `bool` | Check if GPU is supported |
| `Cllama_GetSupportBackends()` | `TArray<FString>` | Retrieve supported backends |
| `Cllama_PrepareModelPathFromPak(const FString&)` | `FString` | Prepare model path from Pak |

####Model Information

| Method | Return Type | Description |
|------|---------|------|
| `GetOpenAIChatDefaultModels()` | `const TArray<FName>&` | List of OpenAI's default models |
| `GetOpenAIChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | Fetch OpenAI model information |
| `GetClaudeChatDefaultModels()` | `const TArray<FName>&` | Claude Default Model List |
| `GetClaudeChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | Retrieve Claude Model Information |
| `GetGeminiChatDefaultModels()` | `const TArray<FName>&` | Gemini default model list |
| `GetGeminiChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | Retrieve Gemini model information |

---

### UAIChatPlus_Texture

Image packaging class, supports asynchronous loading and Base64 conversion.

**Header File:** `Common/AIChatPlus_Texture.h`

**Static Factory Method:**

```cpp
static UAIChatPlus_Texture* New(UTexture2D* InTexture = nullptr, const FString& InSourcePath = "");
static UAIChatPlus_Texture* CreateInBlueprint(UObject* WorldContextObject, UTexture2D* InTexture);
```

**Method:**

| Method | Return Type | Description |
|------|---------|------|
| `LoadFromFile(const FString&)` | `bool` | Load from file (synchronous) |
| `LoadFromFileAsync(const FString&, Callback)` | `FLoadingTaskType*` | Load from file (asynchronous) |
| `LoadFromAsset(UObject*, const FString&)` | `bool` | Load from asset (synchronous) |
| `LoadFromAssetAsync(UObject*, Callback, const FString&)` | `FLoadingTaskType*` | Load From Asset (Asynchronous) |
| `ToB64()` | `const FString&` | Convert to Base64 (synchronous) |
| `ToB64Async(Callback)` | `FLoadingTaskType*` | Convert to Base64 (Asynchronous) |
| `GetBrush(bool)` | `const FSlateBrush*` | Get Slate Brush |
| `GetBrushCopy(bool)` | `FSlateBrush` | Gets a brush copy |
| `GetSize()` | `FIntVector2` | Gets the size |
| `GetSize2D()` | `FVector2D` | Gets the size (floating-point) |
| `IsValid()` | `bool` | Checks if the object is valid |
| `IsLoading()` | `bool` | Checks if data is being loaded |
| `Reset()` | `void` | Reset |
| `WaitLoadingComplete()` | `void` | Wait for loading to complete |

---

### UAIChatPlus_Sound

Audio wrapper class, supporting asynchronous loading and Base64 conversion.

**Header File:** `Common/AIChatPlus_Sound.h`

**Static Factory Method:**

```cpp
static UAIChatPlus_Sound* New(USoundWave* InSound = nullptr, const FString& InSourcePath = "");
static UAIChatPlus_Sound* CreateInBlueprint(UObject* WorldContextObject, USoundWave* InSound);
```

**Method:**

| Method | Return Type | Description |
|------|---------|------|
| `LoadFromFile(const FString&)` | `bool` | Load from file (synchronous) |
| `LoadFromFileAsync(const FString&, Callback)` | `FLoadingTaskType*` | Load from file (asynchronous) |
| `LoadFromAsset(UObject*, const FString&)` | `bool` | Load from asset (synchronous) |
| `LoadFromAssetAsync(UObject*, Callback, const FString&)` | `FLoadingTaskType*` | Load from asset (asynchronous) |
| `ToB64()` | `const FString&` | Convert to Base64 (Synchronous) |
| `ToB64Async(Callback)` | `FLoadingTaskType*` | Convert to Base64 (Async) |
| `IsValid()` | `bool` | Checks if valid |
| `IsLoading()` | `bool` | Checks if it's loading |
| `Reset()` | `void` | Reset |
Here’s the translation:

| `WaitLoadingComplete()` | `void` | Waits for loading to complete |
| `PlayInEditor()` | `void` | Play in Editor |

---

##JSON Class

### UAIChatPlus_JsonObject

Wrapper class for JSON objects.

**Header File:** `Common/Json/AIChatPlus_JsonObject.h`

**Static Factory Method:**

```cpp
static UAIChatPlus_JsonObject* Create();
static UAIChatPlus_JsonObject* Parse(const FString& JsonString, bool& bSuccess, FString& ErrorMessage);
static UAIChatPlus_JsonObject* FromStruct(const int32& Struct);  // CustomThunk
```

**Set Field Method (Supports Method Chaining):**

| Method | Return Type | Description |
|------|---------|------|
| `SetStringField(const FString&, const FString&)` | `UAIChatPlus_JsonObject*` | Sets a string field |
| `SetNumberField(const FString&, float)` | `UAIChatPlus_JsonObject*` | Set number field |
| `SetIntegerField(const FString&, int32)` | `UAIChatPlus_JsonObject*` | Set integer field |
| `SetBooleanField(const FString&, bool)` | `UAIChatPlus_JsonObject*` | Set Boolean Field |
| `SetObjectField(const FString&, UAIChatPlus_JsonObject*)` | `UAIChatPlus_JsonObject*` | Set Object Field |
| `SetArrayField(const FString&, UAIChatPlus_JsonArray*)` | `UAIChatPlus_JsonObject*` | Sets an array field |
| `SetNullField(const FString&)` | `UAIChatPlus_JsonObject*` | Set null field |

**Method to Retrieve Fields:**

| Method | Return Type | Description |
|------|---------|------|
| `GetStringField(const FString&, const FString&, bool&)` | `FString` | Get String |
| `GetNumberField(const FString&, float, bool&)` | `float` | Get Number Field |
| `GetIntegerField(const FString&, int32, bool&)` | `int32` | Get integer |
| `GetBooleanField(const FString&, bool, bool&)` | `bool` | Get Boolean |
| `GetObjectField(const FString&, bool&)` | `UAIChatPlus_JsonObject*` | Get Object |
| `GetArrayField(const FString&, bool&)` | `UAIChatPlus_JsonArray*` | Get Array |

**Other Methods:**

| Method | Return Type | Description |
|------|---------|------|
| `HasField(const FString&)` | `bool` | Checks field existence |
| `GetFieldType(const FString&)` | `EAIChatPlus_JsonValueType` | Retrieves the field type |
| `RemoveField(const FString&)` | `UAIChatPlus_JsonObject*` | Remove Field |
| `Clear()` | `UAIChatPlus_JsonObject*` | Clear all fields |
| `ToString(bool)` | `FString` | Convert to string |
| `ToStruct(int32&)` | `bool` | Convert to struct |
| `Merge(UAIChatPlus_JsonObject*, bool)` | `UAIChatPlus_JsonObject*` | Merge Objects |
| `Duplicate()` | `UAIChatPlus_JsonObject*` | Clone Object |
| `IsValid()` | `bool` | Check validity |

**Route Query Method:**

| Method | Return Type | Description |
|------|---------|------|
| `SetStringByPath(const FString&, const FString&, const FAIChatPlus_JsonPathOptions&)` | `UAIChatPlus_JsonObject*` | Set string by path |
| `GetStringByPath(const FString&, const FString&, FAIChatPlus_JsonQueryResult&)` | `FString` | Retrieve string by path |

---

### UAIChatPlus_JsonArray

JSON Array Wrapper Class.

**Header File:** `Common/Json/AIChatPlus_JsonArray.h`

**Static Factory Methods:**

```cpp
static UAIChatPlus_JsonArray* Create();
static UAIChatPlus_JsonArray* Parse(const FString& JsonString, bool& bSuccess, FString& ErrorMessage);
static UAIChatPlus_JsonArray* FromStringArray(const TArray<FString>& Values);
static UAIChatPlus_JsonArray* FromIntegerArray(const TArray<int32>& Values);
```

**Methods for Adding Elements (Supporting Method Chaining):**

| Method | Return Type | Description |
|------|---------|------|
| `AddString(const FString&)` | `UAIChatPlus_JsonArray*` | Add a string |
| `AddNumber(float)` | `UAIChatPlus_JsonArray*` | Add Number |
| `AddInteger(int32)` | `UAIChatPlus_JsonArray*` | Add Integer |
| `AddBoolean(bool)` | `UAIChatPlus_JsonArray*` | Adds a boolean |
| `AddObject(UAIChatPlus_JsonObject*)` | `UAIChatPlus_JsonArray*` | Add Object |
| `AddArray(UAIChatPlus_JsonArray*)` | `UAIChatPlus_JsonArray*` | Add Array |
| `AddNull()` | `UAIChatPlus_JsonArray*` | Add null value |

**Methods for Obtaining Elements:**

| Method | Return Type | Description |
|------|---------|------|
| `GetString(int32, const FString&, bool&)` | `FString` | Get String |
| `GetNumber(int32, float, bool&)` | `float` | Get Number |
| `GetInteger(int32, int32, bool&)` | `int32` | Get Integer |
| `GetBoolean(int32, bool, bool&)` | `bool` | Gets Boolean |
| `GetObject(int32, bool&)` | `UAIChatPlus_JsonObject*` | Retrieve Object |
| `GetArray(int32, bool&)` | `UAIChatPlus_JsonArray*` | Retrieve Array |

**Other Methods:**

| Method | Return Type | Description |
|------|---------|------|
| `Length()` | `int32` | Get length |
| `GetElementType(int32)` | `EAIChatPlus_JsonValueType` | Get element type |
| `SetString(int32, const FString&, bool&)` | `UAIChatPlus_JsonArray*` | Set String |
| `SetObject(int32, UAIChatPlus_JsonObject*, bool&)` | `UAIChatPlus_JsonArray*` | Set Object |
| `RemoveAt(int32, bool&)` | `UAIChatPlus_JsonArray*` | Remove element |
| `Clear()` | `UAIChatPlus_JsonArray*` | Clear the array |
| `ToString(bool)` | `FString` | Convert to string |
| `Duplicate()` | `UAIChatPlus_JsonArray*` | Duplicate the array |
| `IsValid()` | `bool` | Validate |

---

### UAIChatPlus_JsonLibrary

JSON Static Utility Library.

**Header File:** `Common/Json/AIChatPlus_JsonLibrary.h`

**Creation Method:**

| Method | Return Type | Description |
|------|---------|------|
| `MakeJsonObjectWithStringField(const FString&, const FString&)` | `UAIChatPlus_JsonObject*` | Creates a single-field object |
| `MakeJsonObjectFromStringMap(const TMap<FString, FString>&)` | `UAIChatPlus_JsonObject*` | Creates an object from a Map |

**Verification Method:**

| Method | Return Type | Description |
|------|---------|------|
| `ValidateJsonString(const FString&, FString&)` | `bool` | Validate JSON string |
| `IsJsonObject(const FString&)` | `bool` | Checks if it is an object |
| `IsJsonArray(const FString&)` | `bool` | Checks if it is an array |

**Formatting Methods:**

| Method | Return Type | Description |
|------|---------|------|
| `PrettifyJson(const FString&)` | `FString` | Beautify JSON |
| `MinifyJson(const FString&)` | `FString` | Minify JSON |

**Structure Conversion (CustomThunk):**

| Method | Return Type | Description |
|------|---------|------|
| `JsonStringToStruct(const FString&, int32&)` | `bool` | JSON to Struct |
| `StructToJsonString(const int32&, bool)` | `FString` | Convert structure to JSON |

**File Operations:**

| Method | Return Type | Description |
|------|---------|------|
| `LoadJsonObjectFromFile(const FString&, bool&, FString&)` | `UAIChatPlus_JsonObject*` | Load object from file |
| `SaveJsonObjectToFile(UAIChatPlus_JsonObject*, const FString&, bool, FString&)` | `bool` | Save object to file |
| `LoadJsonArrayFromFile(const FString&, bool&, FString&)` | `UAIChatPlus_JsonArray*` | Load an array from a file |
| `SaveJsonArrayToFile(UAIChatPlus_JsonArray*, const FString&, bool, FString&)` | `bool` | Save array to file |

**Comparison Method:**

| Method | Return Type | Description |
|------|---------|------|
| `EqualsJsonObject(UAIChatPlus_JsonObject*, UAIChatPlus_JsonObject*)` | `bool` | Compare objects |
| `EqualsJsonArray(UAIChatPlus_JsonArray*, UAIChatPlus_JsonArray*)` | `bool` | Compare arrays |

**Path Query:**

| Method | Return Type | Description |
|------|---------|------|
| `QueryStringByPath(UAIChatPlus_JsonObject*, const FString&, const FString&, FAIChatPlus_JsonQueryResult&)` | `FString` | Query string by path |
| `QueryObjectByPath(UAIChatPlus_JsonObject*, const FString&, FAIChatPlus_JsonQueryResult&)` | `UAIChatPlus_JsonObject*` | Query Object by Path |
| `QueryArrayByPath(UAIChatPlus_JsonObject*, const FString&, FAIChatPlus_JsonQueryResult&)` | `UAIChatPlus_JsonArray*` | Query Array By Path |

--8<-- "footer_en.md"


> This post is translated using ChatGPT. Please leave your feedback in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions therein. 
