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

#C++ فصل - مرجع API

يوفر هذا المستند مرجعًا لـ C++ API لـ ملحق AIChatPlus، متضمنًا شرحًا لكل الفئات والهياكل والتعدادات والطرق الرئيسية المتاحة.

##فهرس

- [نوع التعداد](##枚举类型)
- [الفئات الأساسية](##核心基类)
- [فئة معالج](##handler-类)
- [فئة Request](##request-类)
- [أدوات](##工具类)
-[فئة JSON](##json-类)

---

##أنواع التعداد

### EAIChatPlus_ChatApiProvider

مزودو واجهات برمجة التطبيقات (API) للدردشة الذكاء الاصطناعي مدرجون.

```cpp
enum class EAIChatPlus_ChatApiProvider : uint8
{
    OpenAI,         // OpenAI API
    Azure,          // Azure OpenAI API
    Claude,         // Anthropic Claude API
    Gemini,         // Google Gemini API
Ollama،         // خدمة Ollama المحلية
كلاما،         // استدعاء مباشر لـllama.cpp (مهمل)
CllamaServer    // وضع خادم llama.cpp
};
```

### EAIChatPlus_ImageApiProvider

مزودو واجهات برمجة التطبيقات لإنشاء الصور المدرجون.

```cpp
enum class EAIChatPlus_ImageApiProvider : uint8
{
    OpenAI,   // OpenAI DALL-E
    Azure     // Azure OpenAI DALL-E
};
```

### EAIChatPlus_ChatRole

تعداد أدوار الرسائل.

```cpp
enum class EAIChatPlus_ChatRole : uint8
{
    System,     // تعليمات النظام (النموذج القديم)
المستخدم،       // رسالة المستخدم
مساعد،   // رد الذكاء الاصطناعي
المطور،
أداة        // نتيجة استدعاء الأداة
};
```

### EAIChatPlus_ImageChatType

تعداد أنواع عمليات الصور.

```cpp
enum class EAIChatPlus_ImageChatType : uint8
{
الجيل،  // توليد الصور
تعديل،        // تعديل الصورة
التغير    // متغير الصورة
};
```

### EAIChatPlus_JsonValueType

تعداد أنواع قيم JSON.

```cpp
enum class EAIChatPlus_JsonValueType : uint8
{
لا شيء،     // غير صالح
    فارغ,     // قيمة خالية
String,   // سلسلة نصية
رقم،
Boolean, // منطقي
Array,    // مصفوفة
الكائن    // الكائن
};
```

---

##الصف الأساسي المركزي

### UAIChatPlus_RequestBase

الفئة الأساسية لجميع الطلبات (فئة مجردة).

**الطرق الرئيسية:**

| طريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `SendRequest()` | `bool` | إرسال الطلب |
| `StopRequest()` | `void` | إيقاف الطلب |
| `Activate()` | `void` | تفعيل كائن الطلب |
| `IsActivated()` | `bool` | التحقق مما إذا كان قد تم التفعيل |
| `SetIsAutoDestroy(bool)` | `void` | تعيين التدمير التلقائي بعد الانتهاء |

**التكليف:**

| اسم الوكالة | التوقيع | الوصف |
|--------|------|------|
| `OnStartedListeners` | `void()` | بدء الطلب |
| `OnMessageListeners` | `void(const FString&)` | استلام رسالة متدفقة |
| `OnFinishedListeners` | `void(const FAIChatPlus_PointerWrapper&)` | اكتمال الطلب |
| `OnFailedListeners` | `void(const FAIChatPlus_PointerWrapper&)` | فشل في الطلب |

---

### UAIChatPlus_ChatRequestBase

الفئة الأساسية لطلب الدردشة، مُوروثة من `UAIChatPlus_RequestBase`.

**طريقة المصنع الساكنة:**

```cpp
// إنشاء طلب حسب Provider
static UAIChatPlus_ChatRequestBase* CreateByApi(EAIChatPlus_ChatApiProvider InApiProvider);
static UAIChatPlus_ChatRequestBase* CreateByApiInWorld(EAIChatPlus_ChatApiProvider InApiProvider, const UObject* InWorldContext);
```

**الأساليب الرئيسية:**

| الطريقة | نوع الإرجاع | الوصف |
|---|---|---|
Note: Arabic is written right-to-left (RTL), so the table columns will appear reversed compared to the original left-to-right (LTR) English version while maintaining proper RTL formatting. The headers flow from right to left as الطريقة (Method), نوع الإرجاع (Return Type), الوصف (Description).
|------|---------|------|
| `SetMessages(const TArray<FAIChatPlus_ChatRequestMessage>&)` | `void` | تحديد قائمة الرسائل |
| `GetFullUrl()` | `FString` | الحصول على رابط الطلب الكامل |
| `GetModelText()` | `FString` | جلب اسم النموذج |
| `GetTokenUsageText()` | `FString` | الحصول على وصف استخدام التوكين |
| `GetApiProvider()` | `EAIChatPlus_ChatApiProvider` | الحصول على نوع موفر واجهة برمجة التطبيقات (API) |

---

### UAIChatPlus_ImageRequestBase

الصف الأساسي لطلب الصور، موروث من `UAIChatPlus_RequestBase`.

**طريقة المصنع الثابتة:**

```cpp
static UAIChatPlus_ImageRequestBase* CreateByApi(EAIChatPlus_ImageApiProvider InApiProvider);
static UAIChatPlus_ImageRequestBase* CreateByApiInWorld(EAIChatPlus_ImageApiProvider InApiProvider, const UObject* InWorldContext);
```

**المناهج الرئيسية:**

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `SetPrompt(const FString&)` | `void` | تعيين كلمات التلميح لتوليد الصورة |
| `SetImages(const TArray<UAIChatPlus_Texture*>&)` | `void` | تعيين الصور المدخلة (تحرير/تنويع) |
| `GetModelText()` | `FString` | الحصول على اسم النموذج |
| `GetStyleText()` | `FString` | الحصول على اسم النمط |
| `GetRevisedPrompt()` | `FString` | الحصول على التلميح المعدّل |
| `GetImageChatType()` | `FString` | الحصول على نوع عملية الصورة |

---

### UAIChatPlus_ModelRequestBase

قائمة الطرازات الأساسية للطلب، ترث من `UAIChatPlus_RequestBase`.

**طُرُق المصنع الساكنة:**

```cpp
static UAIChatPlus_ModelRequestBase* CreateByApi(EAIChatPlus_ChatApiProvider InApiProvider);
static UAIChatPlus_ModelRequestBase* CreateByApiInWorld(EAIChatPlus_ChatApiProvider InApiProvider, const UObject* InWorldContext);
```

---

##فئة المُعَالِج

### UAIChatPlus_HandlerBase

الفئة الأساسية لكل المعالجات (Handler).

**الأساليب الرئيسية:**

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `SetIsAutoDestroy(bool)` | `void` | تعيين التدمير التلقائي |
| `التدمير التلقائي()` | `باطل` | تنفيذ التدمير التلقائي |
| `Destroy()` | `void` | التدمير الفوري |

---

### UAIChatPlus_ChatHandlerBase

معالج طلب الدردشة، مُورَّث من `UAIChatPlus_HandlerBase`.

**طريقة المصنع الساكنة:**

```cpp
static UAIChatPlus_ChatHandlerBase* New();
```

**طريقة الربط:**

| الطريقة | الوصف |
|------|------|
| `BindChatRequest(UAIChatPlus_ChatRequestBase*)` | ربط طلب المحادثة |
| `BindImageRequest(UAIChatPlus_ImageRequestBase*)` | ربط طلب الصورة |
| `BindModelRequest(UAIChatPlus_ModelRequestBase*)` | طلب ربط النموذج |
| `ClearDelegates()` | مسح جميع ارتباطات المفوضين |

**التفويض:**

| الاسم المفوض   | التوقيع | الوصف |
|--------|------|------|
| `OnStarted` | `void()` | بداية الطلب |
| `OnStopped` | `void()` | طلب التوقف |
| `OnMessage` | `void(const FString&)` | رسائل دفقيه (ستريم) |
| `OnMessageFinished` | `void(const FAIChatPlus_MessageFinishedPayload&)` | اكتمال الرسالة |
| `OnUpdated` | `void(const FAIChatPlus_PointerWrapper&)` | طلب التحديث |
| `OnFinished` | `void(const FAIChatPlus_PointerWrapper&)` | طلب مكتمل |
| `OnFailed` | `void(const FAIChatPlus_PointerWrapper&)` | فشل الطلب |
| `OnImages` | `void(const TArray<UTexture2D*>&, bool)` | توليد الصور |
| `OnModels` | `void(const TArray<FString>&)` | قائمة النماذج |

---

### UAIChatPlus_CllamaServerHandler

معالج مخصص لـ CllamaServer.

**طريقة المصنع الثابتة:**

```cpp
static UAIChatPlus_CllamaServerHandler* CreateHandler();
```

**التوكيل:**

| اسم التفويض | التوقيع | الوصف |
|--------|------|------|
| `OnServerStarted` | `void(FGuid)` | بدء تشغيل الخادم |
| `OnServerStopped` | `void(FGuid)` | توقف الخادم |
| `OnServerFailed` | `void(FGuid, const FString&)` | فشل الخادم |

---

##فئة الطلب

تتبع جميع فئات Request في Provider نفس نمط طريقة المصنع:

###نمط طريقة المصنع العامة

```cpp
// على سبيل المثال OpenAI، ومعظم مزودي الخدمات الآخرين مشابهون
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

###الطرق العامة الثابتة

توفر جميع فئات Request طريقة `CastWrapperToResponse` للتحويل بين الأنواع:

```cpp
// استخراج بيانات الاستجابة من PointerWrapper
static FAIChatPlus_XXXResponseBody& CastWrapperToResponse(const FAIChatPlus_PointerWrapper& InWrapper);
static FAIChatPlus_PointerWrapper CastResponseToWrapper(const FAIChatPlus_XXXResponseBody& InResponse);
```

---

### UAIChatPlus_OpenAIChatRequest

طلب محادثة OpenAI.

**ملف الرأس:** `Common_OpenAI/AIChatPlus_OpenAIChatRequest.h`

**نوع الخيارات:** `FAIChatPlus_OpenAIChatRequestOptions`

**نوع الرد:** `FAIChatPlus_OpenAIChatResponseBody`

---

### UAIChatPlus_AzureChatRequest

طلبات الدردشة Azure OpenAI.

**ملف الرأس:** `Common_Azure/AIChatPlus_AzureChatRequest.h`

**نوع الخيارات:** `FAIChatPlus_AzureChatRequestOptions`

**نوع الاستجابة:** `FAIChatPlus_AzureChatResponseBody`

---

### UAIChatPlus_ClaudeChatRequest

طلب محادثة مع كلود.

**ملف الرأس:** `Common_Claude/AIChatPlus_ClaudeChatRequest.h`

**نوع الخيارات:** `FAIChatPlus_ClaudeChatRequestOptions`

**نوع الاستجابة:** `FAIChatPlus_ClaudeChatResponseBody`

---

### UAIChatPlus_GeminiChatRequest

طلبات الدردشة على جيميني.

**ملف الرأس:** `Common_Gemini/AIChatPlus_GeminiChatRequest.h`

**نوع الخيارات:** `FAIChatPlus_GeminiChatRequestOptions`

**نوع الاستجابة:** `FAIChatPlus_GeminiChatResponseBody`

---

### UAIChatPlus_OllamaChatRequest

طلب محادثة Ollama.

**ملف الرأس:** `Common_Ollama/AIChatPlus_OllamaChatRequest.h`

**نوع الخيارات:** `FAIChatPlus_OllamaChatRequestOptions`

**نوع الاستجابة:** `FAIChatPlus_OllamaChatResponseBody`

---

### UAIChatPlus_OllamaModelRequest

طلب قائمة نماذج Ollama.

**ملفات الرأس:** `Common_Ollama/AIChatPlus_OllamaModelRequest.h`

**نوع Options:** `FAIChatPlus_OllamaModelRequestOptions`

**نوع الاستجابة:** `FAIChatPlus_OllamaModelResponseBody`

**الأساليب المميزة:**

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `GetModelNames()` | `TArray<FString>` | جلب قائمة أسماء النماذج |

---

###UAIChatPlus_CllamaChatRequest (مهمَل)

طلبات الدردشة غير المتصلة بـ Cllama (مهجورة، يُوصى باستخدام CllamaServer بدلاً منها).

**رأس الملف:** `Common_Cllama/AIChatPlus_CllamaChatRequest.h`

**نوع الخيارات:** `FAIChatPlus_CllamaChatRequestOptions`

**نوع الرد:** `FAIChatPlus_CllamaChatResponseBody`

---

### UAIChatPlus_CllamaServerChatRequest

طلب دردشة CllamaServer.

**رأس الملف:** `Common_CllamaServer/AIChatPlus_CllamaServerChatRequest.h`

**نوع الخيارات:** `FAIChatPlus_CllamaServerChatRequestOptions`

**نوع الاستجابة:** `FAIChatPlus_CllamaServerChatResponseBody`

---

### UAIChatPlus_OpenAIImageRequest

طلب توليد صور من OpenAI.

**ملف الرأس:** `Common_OpenAI/AIChatPlus_OpenAIImageRequest.h`

**نوع الخيارات:** `FAIChatPlus_OpenAIImageRequestOptions`

**نوع الاستجابة:** `FAIChatPlus_OpenAIImageResponseBody`

---

### UAIChatPlus_AzureImageRequest

طلب إنشاء صورة في أزور.

**رأس الملف:** `Common_Azure/AIChatPlus_AzureImageRequest.h`

**نوع الخيارات:** `FAIChatPlus_AzureImageRequestOptions`

**نوع الرد:** `FAIChatPlus_AzureImageResponseBody`

---

### UAIChatPlus_CllamaServer

CllamaServer فئة إدارة الخادم.

**ملف الرأس:** `Common_CllamaServer/AIChatPlus_CllamaServer.h`

**طريقة المصنع الساكن:**

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

**الطرق العينية:**

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `Activate()` | `void` | تشغيل الخادم |
| `StopServer()` | `void` | إيقاف الخادم |
| `IsRunning()` | `bool` | التحقق مما إذا كان قيد التشغيل |
| `GetServerID()` | `FGuid` | الحصول على معرف الخادم |
| `GetHost()` | `FString` | الحصول على عنوان المضيف |
| `GetAddress()` | `FString` | الحصول على العنوان الكامل |
| `GetServerInfo(FAIChatPlus_CllamaServerInfo&)` | `bool` | الحصول على معلومات الخادم |

**طرق الإدارة الثابتة:**

| الطريقة  | نوع الإرجاع  | الوصف        |
|------|---------|------|
|
| `IsServerValid(const FGuid&)` | `bool` | التحقق مما إذا كان الخادم صالحًا |
| `IsServerRunning(const FGuid&)` | `bool` | التحقق مما إذا كان الخادم قيد التشغيل |
| `StopServerByID(const FGuid&)` | `void` | إيقاف الخادم حسب المعرف |
| `StopAllServers()` | `void` | إيقاف جميع الخوادم |
| `GetServerByID(const FGuid&)` | `UAIChatPlus_CllamaServer*` | الحصول على الخادم حسب الهوية |
| `GetAllServerIDs()` | `TArray<FGuid>` | الحصول على جميع معرفات الخوادم |

---

##فئة الأدوات

### UAIChatPlus_Util

فئة الأدوات العامة، توفر طرقًا مساعدة ثابتة متنوعة.

**ملف الرأس:** `Common/AIChatPlus_Util.h`

####التي تتعلق بالسجلات

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `SetInternalLogVerbosity(EAIChatPlus_LogVerbosityType)` | `void` | تعيين مستوى السجل الداخلي |

####مُحَوِّل الغلاف

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `CastWrapperToError(const FAIChatPlus_PointerWrapper&)` | `FAIChatPlus_ResponseErrorBase&` | استخراج معلومات الخطأ |
| `CastWrapperToResponse(const FAIChatPlus_PointerWrapper&)` | `FAIChatPlus_ChatResponseBodyBase&` | استخراج بيانات الاستجابة |
| `GetErrorWrapperDescription(const FAIChatPlus_PointerWrapper&)` | `FString` | الحصول على وصف الخطأ |
| `GetResponseWrapperMessage(const FAIChatPlus_PointerWrapper&)` | `FString` | الحصول على رسالة الاستجابة |

####أدوات الصور

| الطريقة | نوع الإرجاع | الوصف |
|-------|----------|--------|
|------|---------|------|
| `LoadImage(const FString&, bool)` | `UTexture2D*` | تحميل الصورة من ملف |
| `SaveImage(UTexture2D*, const FString&)` | `bool` | حفظ الصورة في ملف |
| `ImageToB64(UTexture2D*, int32)` | `FString` | تحويل الصورة إلى Base64 |
| `CopyTexture2D(UTexture2D*, UObject*, FName, EObjectFlags)` | `UTexture2D*` | نسخ النسيج |
| `FitImageSize(const FVector2D&, const FVector2D&)` | `FVector2D` | حساب حجم التكيف |
| `CopyTexture2DToClipboard(UTexture2D*)` | `void` | نسخ إلى الحافظة |
| `IsCanCopyTexture2DToClipboard()` | `bool` | التحقق مما إذا كان مدعومًا |

####أدوات الصوت

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `LoadSoundWav(const FString&)` | `USoundWave*` | تحميل الصوت من ملف |
| `SaveSoundWav(USoundWave*, const FString&)` | `bool` | حفظ الصوت في ملف |
| `SoundToB64(USoundWave*)` | `FString` | الصوت إلى Base64 |
| `CopySoundWave(const USoundWave*, UObject*, FName)` | `موجة صوتية أمريكية*` | نسخ الصوت |
| `WavDataToSoundWave(const TArray<uint8>&, bool, bool)` | `USoundWave*` | تحويل بيانات WAV إلى موجة صوتية |
| `GetSoundWavePCMData(USoundWave*)` | `TArray<uint8>` | الحصول على بيانات PCM |

####أدوات JSON

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `MergeJsonObjects(const FString&, const FString&)` | `FString` | دمج نصوص JSON |
| `LoadJsonString(const FString&)` | `TSharedPtr<FJsonObject>` | تحليل سلسلة JSON |
| `ToJsonString(const TSharedPtr<FJsonObject>&)` | `FString` | تحويل إلى سلسلة JSON |

####أداة Cllama

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `Cllama_IsValid()` | `bool` | التحقق مما إذا كان Cllama متاحًا للاستخدام |
| `Cllama_IsSupportGpu()` | `منطقي` | التحقق من دعم وحدة معالجة الرسومات |
| `Cllama_IsSupportGpu()` | `منطقي` | التحقق مما إذا كان يدعم وحدة معالجة الرسومات |
| `Cllama_GetSupportBackends()` | `TArray<FString>` | الحصول على الواجهات الخلفية المدعومة |
| `Cllama_PrepareModelPathFromPak(const FString&)` | `FString` | إعداد مسار النموذج من حزمة Pak |

####معلومات النموذج

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `GetOpenAIChatDefaultModels()` | `const TArray<FName>&` | قائمة نماذج OpenAI الافتراضية |
| `GetOpenAIChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | الحصول على معلومات نموذج OpenAI |
| `GetClaudeChatDefaultModels()` | `const TArray<FName>&` | قائمة نماذج كلود الافتراضية |
| `GetClaudeChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | الحصول على معلومات نموذج كلود |
| `GetGeminiChatDefaultModels()` | `const TArray<FName>&` | قائمة نماذج جيميني الافتراضية |
| `GetGeminiChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | الحصول على معلومات نموذج جيميني |

---

### UAIChatPlus_Texture

فئة تغليف الصور، تدعم التحميل غير المتزامن والتحويل إلى Base64.

**ملف الرأس:** `Common/AIChatPlus_Texture.h`

**طرق المصنع الساكنة:**

```cpp
static UAIChatPlus_Texture* New(UTexture2D* InTexture = nullptr, const FString& InSourcePath = "");
static UAIChatPlus_Texture* CreateInBlueprint(UObject* WorldContextObject, UTexture2D* InTexture);
```

**الطريقة:**

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `LoadFromFile(const FString&)` | `bool` | تحميل من الملف (متزامن) |
| `LoadFromFileAsync(const FString&, Callback)` | `FLoadingTaskType*` | تحميل من ملف (غير متزامن) |
| `LoadFromAsset(UObject*, const FString&)` | `bool` | تحميل من الأصل (متزامن) |
| `LoadFromAssetAsync(UObject*, Callback, const FString&)` | `FLoadingTaskType*` | التحميل من الأصل (غير متزامن) |
| `ToB64()` | `const FString&` | تحويل إلى Base64 (متزامن) |
| `ToB64Async(Callback)` | `FLoadingTaskType*` | التحويل إلى Base64 (غير متزامن) |
| `GetBrush(bool)` | `const FSlateBrush*` | الحصول على فرشاة Slate |
| `GetBrushCopy(bool)` | `FSlateBrush` | الحصول على نسخة من الفرشاة |
| `GetSize()` | `FIntVector2` | الحصول على الأبعاد |
| `GetSize2D()` | `FVector2D` | الحصول على الحجم (نقطة عائمة) |
| `IsValid()` | `منطقي` | التحقق مما إذا كان صالحًا |
| `IsLoading()` | `bool` | التحقق مما إذا كان التحميل قيد التقدم |
| `Reset()` | `void` | إعادة تعيين |
| `انتظراكتمالالتحميل()` | `باطل` | انتظر اكتمال التحميل |

---

### UAIChatPlus_Sound

فئة تغليف الصوتيات، تدعم التحميل غير المتزامن وتحويل Base64.

**ملفات الرأس:** `Common/AIChatPlus_Sound.h`

**طُرُق المصنع الثابتة:**

```cpp
static UAIChatPlus_Sound* New(USoundWave* InSound = nullptr, const FString& InSourcePath = "");
static UAIChatPlus_Sound* CreateInBlueprint(UObject* WorldContextObject, USoundWave* InSound);
```

**الطريقة:**

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `LoadFromFile(const FString&)` | `bool` | تحميل من ملف (متزامن) |
| `LoadFromFileAsync(const FString&, Callback)` | `FLoadingTaskType*` | التحميل من ملف (غير متزامن) |
| `LoadFromAsset(UObject*, const FString&)` | `bool` | التحميل من الأصل (متزامن) |
| `LoadFromAssetAsync(UObject*, Callback, const FString&)` | `FLoadingTaskType*` | التحميل من الأصل (غير متزامن) |
| `ToB64()` | `const FString&` | تحويل إلى Base64 (متزامن) |
| `ToB64Async(Callback)` | `FLoadingTaskType*` | التحويل إلى Base64 (غير متزامن) |
| `IsValid()` | `bool` | التحقق مما إذا كان صالحًا |
| `هل التحميل جارٍ()` | `منطقي` | التحقق مما إذا كان التحميل قيد الإجراء |
| `Reset()` | `void` | إعادة تعيين |
| `WaitLoadingComplete()` | `void` | انتظر اكتمال التحميل |
| `PlayInEditor()` | `void` | التشغيل في المُحرِّر |

---

##فئة JSON

### UAIChatPlus_JsonObject

فئة تغليف كائن JSON.

**ملف الرأس:** `Common/Json/AIChatPlus_JsonObject.h`

**طرق المصنع الثابتة:**

```cpp
static UAIChatPlus_JsonObject* Create();
static UAIChatPlus_JsonObject* Parse(const FString& JsonString, bool& bSuccess, FString& ErrorMessage);
static UAIChatPlus_JsonObject* FromStruct(const int32& Struct);  // CustomThunk
```

**طرق تعيين الحقول (مدعومة بالاستدعاء التسلسلي):**

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `SetStringField(const FString&, const FString&)` | `UAIChatPlus_JsonObject*` | تعيين حقل السلسلة النصية |
| `SetNumberField(const FString&, float)` | `UAIChatPlus_JsonObject*` | تعيين حقل رقمي |
| `SetIntegerField(const FString&, int32)` | `UAIChatPlus_JsonObject*` | تعيين حقل رقمي صحيح |
| `SetBooleanField(const FString&, bool)` | `UAIChatPlus_JsonObject*` | تعيين حقل منطقي |
| `SetObjectField(const FString&, UAIChatPlus_JsonObject*)` | `UAIChatPlus_JsonObject*` | تعيين حقل الكائن |
| `SetArrayField(const FString&, UAIChatPlus_JsonArray*)` | `UAIChatPlus_JsonObject*` | تعيين حقل مصفوفة |
| `SetNullField(const FString&)` | `UAIChatPlus_JsonObject* ` | تعيين حقل فارغ |

**طرق الحصول على الحقول:**

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `GetStringField(const FString&, const FString&, bool&)` | `FString` | الحصول على سلسلة نصية |
| `GetNumberField(const FString&, float, bool&)` | `float` | الحصول على رقم |
| `GetIntegerField(const FString&, int32, bool&)` | `int32` | الحصول على عدد صحيح |
| `GetBooleanField(const FString&, bool, bool&)` | `bool` | جلب قيمة منطقية |
| `GetObjectField(const FString&, bool&)` | `UAIChatPlus_JsonObject*` | الحصول على كائن |
| `GetArrayField(const FString&, bool&)` | `UAIChatPlus_JsonArray*` | الحصول على مصفوفة |

**طرق أخرى:**

| الطريقة | نوع الإرجاع | الوصف |
|---|---|---|
|------|---------|------|
| `HasField(const FString&)` | `bool` | التحقق من وجود الحقل |
| `GetFieldType(const FString&)` | `EAIChatPlus_JsonValueType` | الحصول على نوع الحقل |
| `RemoveField(const FString&)` | `UAIChatPlus_JsonObject*` | إزالة الحقل |
| `Clear()` | `UAIChatPlus_JsonObject*` | إفراغ جميع الحقول |
| `ToString(bool)` | `FString` | التحويل إلى سلسلة نصية |
| `ToStruct(int32&)` | `bool` | تحويل إلى بنية |
| `Merge(UAIChatPlus_JsonObject*, bool)` | `UAIChatPlus_JsonObject*` | دمج الكائنات |
| `Duplicate()` | `UAIChatPlus_JsonObject*` | استنساخ الكائن |
| `IsValid()` | `bool` | التحقق من الصحة |

**طريقة استعلام المسار:**

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `SetStringByPath(const FString&, const FString&, const FAIChatPlus_JsonPathOptions&)` | `UAIChatPlus_JsonObject*` | تعيين سلسلة نصية حسب المسار |
| `GetStringByPath(const FString&, const FString&, FAIChatPlus_JsonQueryResult&)` | `FString` | الحصول على سلسلة نصية حسب المسار |

---

### UAIChatPlus_JsonArray

فئة تغليف مصفوفة JSON.

**ملفات الرأس:** `Common/Json/AIChatPlus_JsonArray.h`

**طريقة المصنع الثابتة:**

```cpp
static UAIChatPlus_JsonArray* Create();
static UAIChatPlus_JsonArray* Parse(const FString& JsonString, bool& bSuccess, FString& ErrorMessage);
static UAIChatPlus_JsonArray* FromStringArray(const TArray<FString>& Values);
static UAIChatPlus_JsonArray* FromIntegerArray(const TArray<int32>& Values);
```

**طريقة إضافة العناصر (تدعم الاستدعاء التسلسلي):**

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `AddString(const FString&)` | `UAIChatPlus_JsonArray*` | إضافة سلسلة نصية |
| `AddNumber(float)` | `UAIChatPlus_JsonArray*` | إضافة رقم |
| `AddInteger(int32)` | `UAIChatPlus_JsonArray*` | إضافة عدد صحيح |
| `AddBoolean(bool)` | `UAIChatPlus_JsonArray*` | إضافة قيمة منطقية |
| `AddObject(UAIChatPlus_JsonObject*)` | `UAIChatPlus_JsonArray*` | إضافة كائن |
| `AddArray(UAIChatPlus_JsonArray*)` | `UAIChatPlus_JsonArray*` | إضافة مصفوفة |
| `AddNull()` | `UAIChatPlus_JsonArray*` | إضافة قيمة فارغة |

**طرق الحصول على العناصر:**

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `GetString(int32, const FString&, bool&)` | `FString` | استرداد سلسلة نصية |
| `GetNumber(int32، float، bool&)` | `float` | احصل على الرقم |
| `GetInteger(int32, int32, bool&)` | `int32` | الحصول على عدد صحيح |
| `GetBoolean(int32, bool, bool&)` | `bool` | الحصول على قيمة منطقية |
| `GetObject(int32, bool&)` | `UAIChatPlus_JsonObject*` | الحصول على الكائن |
| `GetArray(int32, bool&)` | `UAIChatPlus_JsonArray*` | الحصول على مصفوفة |

**طرق أخرى:**

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `Length()` | `int32` | الحصول على الطول |
| `GetElementType(int32)` | `EAIChatPlus_JsonValueType` | الحصول على نوع العنصر |
| `SetString(int32, const FString&, bool&)` | `UAIChatPlus_JsonArray*` | تعيين السلسلة النصية |
| `SetObject(int32, UAIChatPlus_JsonObject*, bool&)` | `UAIChatPlus_JsonArray*` | تعيين الكائن |
| `RemoveAt(int32, bool&)` | `UAIChatPlus_JsonArray*` | إزالة عنصر |
| `Clear()` | `UAIChatPlus_JsonArray*` | إفراغ المصفوفة |
إليك الترجمة:

| `ToString(bool)` | `FString` | تحويل إلى سلسلة نصية |
| `Duplicate()` | `UAIChatPlus_JsonArray*` | نسخ المصفوفة |
| `IsValid()` | `منطقي` | التحقق من الصحة |

---

### UAIChatPlus_JsonLibrary

مكتبة أدوات JSON الثابتة.

**ملف الرأس:** `Common/Json/AIChatPlus_JsonLibrary.h`

**طريقة الإنشاء:**

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `MakeJsonObjectWithStringField(const FString&, const FString&)` | `UAIChatPlus_JsonObject*` | إنشاء كائن بحقل واحد |
| `MakeJsonObjectFromStringMap(const TMap<FString, FString>&)` | `UAIChatPlus_JsonObject*` | إنشاء كائن من خريطة |

**طريقة التحقق:**

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `ValidateJsonString(const FString&, FString&)` | `bool` | التحقق من صحة سلسلة JSON |
| `IsJsonObject(const FString&)` | `bool` | التحقق مما إذا كان كائنًا |
| `IsJsonArray(const FString&)` | `bool` | التحقق مما إذا كان مصفوفة أم لا |

**طرق التنسيق:**

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `PrettifyJson(const FString&)` | `FString` | تجميل JSON |
| `MinifyJson(const FString&)` | `FString` | ضغط JSON |

**تحويل الهياكل (CustomThunk):**

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `JsonStringToStruct(const FString&, int32&)` | `bool` | تحويل JSON إلى بنية |
| `StructToJsonString(const int32&, bool)` | `FString` | تحويل البنية إلى JSON |

**معالجة الملفات:**

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `تحميل_كائن_جسون_من_الملف(const FString&، bool&، FString&)` | `*UAIChatPlus_JsonObject` | تحميل الكائن من الملف |
SaveJsonObjectToFile(UAIChatPlus_JsonObject*, const FString&, bool, FString&) | bool | حفظ الكائن إلى ملف
| `تحميلJsonArrayمنالملف(const FString&, bool&, FString&)` | `UAIChatPlus_JsonArray*` | تحميل مصفوفة من ملف |
| `SaveJsonArrayToFile(UAIChatPlus_JsonArray*, const FString&, bool, FString&)` | `bool` | حفظ المصفوفة في ملف |

**طريقة المقارنة:**

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `EqualsJsonObject(UAIChatPlus_JsonObject*, UAIChatPlus_JsonObject*)` | `bool` | مقارنة الكائنات |
| `EqualsJsonArray(UAIChatPlus_JsonArray*, UAIChatPlus_JsonArray*)` | `bool` | مقارنة المصفوفات |

**استعلام عن المسار:**

| الطريقة | نوع الإرجاع | الوصف |
|------|---------|------|
| `QueryStringByPath(UAIChatPlus_JsonObject*, const FString&, const FString&, FAIChatPlus_JsonQueryResult&)` | `FString` | الاستعلام عن سلسلة نصية حسب المسار |
| `QueryObjectByPath(UAIChatPlus_JsonObject*, const FString&, FAIChatPlus_JsonQueryResult&)` | `UAIChatPlus_JsonObject*` | الاستعلام عن كائن حسب المسار |
| `QueryArrayByPath(UAIChatPlus_JsonObject*, const FString&, FAIChatPlus_JsonQueryResult&)` | `UAIChatPlus_JsonArray*` | استعلام عن المصفوفة حسب المسار |

--8<-- "footer_ar.md"


> هذا المنشور مترجم باستخدام ChatGPT، يُرجى تقديم ملاحظات في [**التغذية الراجعة**](https://github.com/disenone/wiki_blog/issues/new)أشر إلى أي نقص في ذلك. 
