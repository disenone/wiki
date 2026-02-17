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

#++C قسم - ابدأ الآن

##مقدمة الوحدة

ينقسم الملحق إلى الوحدات التالية:

* **AIChatPlusCommon**: وحدة وقت التشغيل (Runtime)، مسؤولة عن معالجة طلبات إرسال واجهات برمجة التطبيقات المختلفة للذكاء الاصطناعي وتحليل محتوى الردود.
* **AIChatPlusEditor**: وحدة المحرر (Editor)، المسؤولة عن تنفيذ أداة الدردشة بالذكاء الاصطناعي في المحرر.
* **AIChatPlusCllama**: وحدة وقت التشغيل (Runtime)، مسؤولة عن تغليف واجهة وخصائص llama.cpp، لتنفيذ نموذج ذكاء اصطناعي كبير بدون اتصال بالإنترنت.
* **طرف ثالث/إل إل إم أي سي بي بي**: وحدة وقت التشغيل (Runtime)، تجمع بين المكتبة الديناميكية وملفات الرأس الخاصة بـ llama.cpp.

##المفاهيم الأساسية

قبل استخدام الكود المصدري، يجب فهم بعض الفئات الرئيسية وعلاقاتها فيما بينها:

###طلب (طلب)

`UAIChatPlus_ChatRequestBase` هي الفئة الأساسية لجميع طلبات الدردشة. كل موفر API لديه فئة فرعية مقابلة:

* `UAIChatPlus_OpenAIChatRequest` - طلب دردشة OpenAI
* `UAIChatPlus_AzureChatRequest` - طلب دردشة Azure
* `UAIChatPlus_ClaudeChatRequest` - طلب دردشة كلود
* `UAIChatPlus_GeminiChatRequest` - طلب محادثة Gemini
* `UAIChatPlus_OllamaChatRequest` - طلب دردشة أولاما
* `UAIChatPlus_CllamaChatRequest` - طلب نموذج Cllama دون اتصال
* `UAIChatPlus_CllamaServerChatRequest` - طلب خادم CllamaServer المحلي

كائن Request مسؤول عن تكوين معلمات الطلب وإرسال الطلب واستقبال ردود النداء.

###المعَالِج

`UAIChatPlus_ChatHandlerBase` هي فئة مُعالج اختيارية تستخدم لإدارة موحدة لاستدعاءات الطلبات.

‏يقدم Handler التفويضات التالية:

* `OnStarted` - يتم تشغيله عند بدء الطلب
* `OnMessage` - يتم تشغيله عند استقبال رسالة تدفقية (إخراج تدفقي)
* `OnUpdated` - يتم تشغيله عند استلام تحديث
* `OnFinished` - يتم تشغيله عند اكتمال الطلب
* `OnFailed` - يتم تشغيله عند فشل الطلب

**متى نستخدم Handler؟**

* عند الحاجة إلى إدارة منطق الاستدعاءات المتعددة بشكل موحد
* عند الحاجة إلى مشاركة منطق رد الاتصال بين المخططات البرمجية (بلوبرينت) و++C
* يمكن أيضًا تحقيق استماع رد الاتصال باستخدام تفويض Request مباشرةً (مثل `OnStartedListeners`)

###خيارات

كل موفر API لديه بنية Options المقابلة، المستخدمة لتكوين معلمات API:

* `FAIChatPlus_OpenAIChatRequestOptions` - خيارات OpenAI (مفتاح API، النموذج، درجة الحرارة، إلخ)
* `FAIChatPlus_ClaudeChatRequestOptions` - خيارات كلود
* `FAIChatPlus_GeminiChatRequestOptions` - خيارات Gemini
* انتظر...

يشمل "Options" جميع التكوينات اللازمة لاتصال واجهة برمجة التطبيقات، مثل مفتاح API وعنوان URL للنقطة الطرفية واسم النموذج ومعلمات الإنشاء وغير ذلك.

###الرسائل

`FAIChatPlus_ChatRequestMessage` هو بنية الرسالة المرسلة إلى الذكاء الاصطناعي، وتحتوي على:

* `المحتوى` - نَصّ المُحْتَوَى
* `الدور` - دور الرسالة (النظام/المستخدم/المساعد/المطور/الأداة)
* `Images` - مصفوفة الصور (خاصية الرؤية)
* `Audios` - مجموعة الصوتيات (ميزة Audio)
* `ToolCallUses` - طلب استدعاء الأداة
* `ToolCallResults` - نتائج استدعاء الأداة

###الاستجابة

كل مزود لواجهة برمجة التطبيقات (API Provider) لديه هيكل ResponseBody خاص به:

* `FAIChatPlus_OpenAIChatResponseBody`
* `FAIChatPlus_ClaudeChatResponseBody`
* انتظر...

يتضمن ResponseBody جميع المعلومات التي تم إرجاعها من الذكاء الاصطناعي، بما في ذلك: نص الرسالة، واستهلاك الرموز المميزة (Token)، واستدعاء الأدوات، وإخراج الصوت، وما إلى ذلك.

##سير العمل الأساسي للاستخدام (نمط الخطوات الخمس)

الخطوات الأساسية لإرسال طلب باستخدام AIChatPlus هي كما يلي:

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"

void SendChatRequest()
{
// ===== الخطوة 1: إنشاء معالج (اختياري) =====
يستخدم Handler لإدارة ردود النداء بشكل موحد، ويمكن أيضًا استخدام تفويض Request مباشرةً
    TWeakObjectPtr<UAIChatPlus_ChatHandlerBase> Handler = UAIChatPlus_ChatHandlerBase::New();

    // ===== الخطوة 2: تهيئة الخيارات =====
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;  // تمكين الإخراج عبر التدفق

// ===== الخطوة 3: إنشاء الطلب =====
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("Hello, who are you?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// ===== الخطوة 4: ربط رد النداء =====
    // الطريقة أ: استخدام Handler
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

// الطريقة ب: الاستخدام المباشر لتفويض الطلب (بدون الحاجة إلى المُعالج)
    // Request->OnMessageListeners.AddDynamic(this, &UMyClass::OnMessageReceived);
    // Request->OnFinishedListeners.AddDynamic(this, &UMyClass::OnRequestFinished);

// ===== الخطوة 5: إرسال الطلب =====
    Request->SendRequest();
}
```

##الكتابة المبسَّطة

إذا لم تكن بحاجة إلى تحكم دقيق في الاستدعاء، يمكنك استخدام صيغة أكثر إيجازًا:

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

// ربط Lambda مباشرةً على Request
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

##إنشاء طلب عبر تعداد موفر واجهة برمجة التطبيقات (API)

إذا كنت تحتاج إلى تحديد موفر واجهة برمجة التطبيقات (API Provider) ديناميكيًا بناءً على التكوين، فيمكنك استخدام طريقة المصنع (Factory Method):

```cpp
void CreateRequestByProvider(EAIChatPlus_ChatApiProvider Provider)
{
// إنشاء Request المقابل وفقًا للتعداد
    auto Request = UAIChatPlus_ChatRequestBase::CreateByApi(Provider);

    // تعيين الخيارات بناءً على النوع الفعلي
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
    // ... مزودون آخرون
    }

// تعيين الرسالة وإرسالها
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Hello!"), EAIChatPlus_ChatRole::User});
    Request->SetMessages(Messages);
    Request->SendRequest();
}
```

##تعليمات الاسترجاع

###المندوبون الأساسيون للاستدعاء الخلفي (الراجع)

| التفويض | توقيت التشغيل | المعاملات |
|------|----------|------|
| `OnStarted` | عند بدء إرسال الطلب | لا شيء |
| `OnMessage` | عند استقبال رسالة متدفقة (كل رمز) | `const FString& Message` - المحتوى المتراكم للرسالة |
| `OnUpdated` | عند تلقي تحديث للاستجابة | `const FAIChatPlus_ResponseBodyBase& Response` |
| `OnFinished` | عند اكتمال الطلب بنجاح | `const FAIChatPlus_ResponseBodyBase& Response` |
| `OnFailed` | عند فشل الطلب | `const FAIChatPlus_ResponseErrorBase& Error` |
| `OnMessageFinished` | عند اكتمال استلام الرسالة | `const FAIChatPlus_MessageFinishedPayload& Payload` |

###الإخراج المتدفق مقابل الإخراج غير المتدفق

* **الإخراج المتدفق** (`bStream = true`): سيتم تشغيل `OnMessage` عدة مرات، حيث يُرجع في كل مرة المحتوى المتراكم للرسائل
* **الإخراج غير المتدفق** (`bStream = false`): يتم تشغيل `OnMessage` مرة واحدة فقط عند الانتهاء، ويعيد الرسالة كاملة.

##التالي

لمزيد من الاستخدامات التفصيلية، يُرجى الرجوع إلى الوثائق المتخصصة لمقدمي واجهة برمجة التطبيقات (API Providers):

* [استخدام OpenAI / Azure](ue-插件-AIChatPlus-Usage-Source-OpenAI.md)
* [استخدام كلود](ue-插件-AIChatPlus-Usage-Source-Claude.md)
* [استخدام جيميني](ue-插件-AIChatPlus-Usage-Source-Gemini.md)
* [استخدام أولاما](ue-插件-AIChatPlus-Usage-Source-Ollama.md)
* [نموذج Cllama دون اتصال](ue-插件-AIChatPlus-Usage-Source-Cllama.md)
* [خادم CllamaServer المحلي](ue-插件-AIChatPlus-Usage-Source-CllamaServer.md)
* [فئة الأدوات](ue-插件-AIChatPlus-Usage-Source-Utils.md)

--8<-- "footer_ar.md"

> هذا المنشور مترجم باستخدام ChatGPT، يُرجى تقديم الملاحظات في [**التغذية الراجعة**](https://github.com/disenone/wiki_blog/issues/new)أشر إلى أي نقص محتمل في النص. 
