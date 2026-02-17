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

#C++ - Ollama

يقدم هذا المستند شرحًا لكيفية استخدام واجهة برمجة تطبيقات Ollama المحلية في لغة C++ لإجراء المحادثات وتحليل الصور واستدعاء الأدوات.

أولاما هي أداة لتشغيل نماذج اللغة الكبيرة محلياً، والعنوان الافتراضي هو `http://localhost:11434`.

##الاستعدادات

قبل الاستخدام، يرجى التأكد من:

1. **تثبيت وتشغيل Ollama**: من [ollama.com](https://ollama.com)قم بتنزيل وتثبيت Ollama، ثم انزل النموذج المطلوب (مثل `ollama pull llama3.2`).

2. في ملف `.Build.cs` الخاص بالمشروع، أضف تبعيات الوحدات:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

3. تضمين ملفات الرأس الضرورية:

```cpp
#include "Common_Ollama/AIChatPlus_OllamaChatRequest.h"
```

## الدردشة النصية

###الدردشة النصية الأساسية

```cpp
#include "Common_Ollama/AIChatPlus_OllamaChatRequest.h"

void UMyClass::SendOllamaChatRequest()
{
// خيارات التهيئة
    FAIChatPlus_OllamaChatRequestOptions Options;
النموذج.الخيار = نص("لاما3.2")؛ // استخدام النموذج الذي تم تنزيله
    Options.BaseUrl = TEXT("http://localhost:11434");  // عنوان افتراضي
الخيارات.بستريم = صحيح؛ // تمكين الإخراج المتدفق
    Options.Temperature = 0.8f;

// Ollama لا يحتاج إلى مفتاح واجهة برمجة التطبيقات (خدمة محلية)

// إنشاء رسالة (تشمل رسالة النظام)
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is 2+2?"), EAIChatPlus_ChatRole::User});

// إنشاء طلب
    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    // ربط رد النداء
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

// إرسال الطلب
    Request->SendRequest();
}
```

###محادثة متعددة الجولات

```cpp
void UMyClass::MultiTurnOllamaChat()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

//بناء تاريخ الحوار متعدد الجولات
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

###استخدم Generate API (وضع غير Chat)

```cpp
void UMyClass::UseOllamaGenerateAPI()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;
خيارات.IsChat = خطأ؛ // يستخدم /api/generate بدلاً من /api/chat
الخيارات.النظام = TEXT("أنت مساعد مفيد.");  // يعمل فقط في الوضع غير الدردشة

// وضع غير المحادثة يحتاج فقط إلى رسالة واحدة من المستخدم
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

##الرؤية (تحليل الصور)

نماذج أولاما التي تدعم الرؤية (مثل `llava` أو `llama3.2-vision`) قادرة على تحليل محتوى الصور.

###تحميل الصورة من الملف وتحليلها

```cpp
#include "Common_Ollama/AIChatPlus_OllamaChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithOllama()
{
// تحميل الصور من الملف
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image: %s"), *ImagePath);
        return;
    }

// إنشاء كائن Texture متاح للإضافات
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

// خيارات التكوين
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2-vision");  // استخدام نموذج يدعم الرؤية
    Options.bStream = true;

// إنشاء رسالة تحتوي على صورة
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

##استدعاء الأداة (استدعاء الدالة)

بعض نماذج Ollama تدعم وظيفة "Tool Calling".

###تحديد الأداة وإرسال الطلب

```cpp
void UMyClass::SendOllamaToolCallRequest()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
الخيارات.النموذج = نص("لاما3.2"); // تأكد من أن النموذج يدعم استدعاء الأدوات
    Options.bStream = true;

// تعريف الأداة: الحصول على الطقس
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");

// تعريف معلمات الأدوات
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

###معالجة نتائج استدعاء الأداة

```cpp
void UMyClass::HandleOllamaToolCallResult()
{
    FString ToolCallId = TEXT("call_123");
    FString FunctionName = TEXT("get_weather");
    FString FunctionResult = TEXT("{\"temperature\": 15, \"unit\": \"celsius\", \"description\": \"Rainy\"}");

    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

// إعادة تعريف الأداة
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");
    Options.Tools.Add(WeatherTool);

// بناء سجل الرسائل
    TArray<FAIChatPlus_ChatRequestMessage> Messages;

// 1. رسائل النظام
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});

    // 2. السؤال الأصلي للمستخدم
    Messages.Add({TEXT("What's the weather in London?"), EAIChatPlus_ChatRole::User});

// 3. طلب استدعاء أداة المساعد
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

    // 4. نتائج تنفيذ الأداة
    FAIChatPlus_ChatRequestMessage ToolResultMessage;
    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;

    FAIChatPlus_ChatRequestToolCallResult ToolResult;
    ToolResult.Id = ToolCallId;
    ToolResult.FunctionName = FunctionName;
    ToolResult.FunctionResult = FunctionResult;
    ToolResultMessage.ToolCallResults.Add(ToolResult);
    Messages.Add(ToolResultMessage);

// إرسال الطلب
    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###حلقة اتصال الأداة الكاملة

```cpp
// تخزين سجل المحادثة
TArray<FAIChatPlus_ChatRequestMessage> OllamaConversation;
FAIChatPlus_OllamaChatRequestOptions OllamaOptions;

void UMyClass::InitializeOllamaToolChat()
{
    OllamaOptions.Model = TEXT("llama3.2");
    OllamaOptions.bStream = true;

// تعريف الأدوات
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

// تهيئة الحوار (إضافة رسالة النظام)
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
// إضافة رسالة استدعاء أداة Assistant
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

// تنفيذ الأداة وإضافة النتائج
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

// متابعة المحادثة
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

##الحصول على قائمة النماذج

استخدام `UAIChatPlus_OllamaModelRequest` يتيح لك الحصول على قائمة النماذج المتاحة على خادم Ollama.

```cpp
#include "Common_Ollama/AIChatPlus_OllamaModelRequest.h"

void UMyClass::GetOllamaModels()
{
    FAIChatPlus_OllamaModelRequestOptions Options;
Options.BaseUrl = TEXT("http://localhost:11434");  // العنوان الافتراضي

    auto Request = UAIChatPlus_OllamaModelRequest::CreateWithOptions(Options);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OllamaModelRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FString> ModelNames = Response.GetModelNames();
        for (const FString& ModelName : ModelNames)
        {
            UE_LOG(LogTemp, Display, TEXT("Available Model: %s"), *ModelName);
        }

// الحصول على التفاصيل
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

##إعدادات متقدمة

###معلمات خاصة بـ Ollama

```cpp
void UMyClass::ConfigureOllamaAdvanced()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

// معلمات العينة
    Options.Temperature = 0.7f;
    الخيارات.الرؤوسك = 40؛           // أخذ العينات من الأعلى ك
Options.TopP = 0.9f;         // العينة النووية
الخيارات.MinP = 0.05f;        // أخذ عينات Min-P

// عينة Mirostat (تُستخدم للتحكم بمستوى الحيرة)

    Options.Mirostat = 2;        // 0=معطل، 1=Mirostat، 2=Mirostat 2.0
    Options.MirostatEta = 0.1f;
    Options.MirostatTau = 5.0f;

// السياق والقيود على التوليد
    الخيارات.عددالسياق = 4096;       // حجم نافذة السياق
    Options.NumPredict = 256;    // الحد الأقصى لعدد الرموز المولدة

// عقوبة التكرار
    Options.RepeatLastN = 64;
    Options.RepeatPenalty = 1.1f;

// تسلسل التوقف
    Options.StopSequences.Add(TEXT("\n\n"));

// وقت تحميل النموذج الثابت
الخيارات.ابقَ نشيطًا = 300؛     // ثانية

// بذرة عشوائية (تُستخدم من أجل إنشاء يمكن تكراره)
    Options.Seed = 42;

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###استخدم مفتاح API (Ollama عن بُعد)

```cpp
void UMyClass::ConnectToRemoteOllama()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.BaseUrl = TEXT("https://your-ollama-server.com");
    Options.ApiKey = TEXT("مفتاح-واجهة-البرمجة-التطبيقية-الخاص-بك");  // إذا كان الخادم يتطلب المصادقة
    Options.bStream = true;

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello from remote!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###استخدام خيارات تمديد JSON

```cpp
void UMyClass::UseOllamaExtraOptions()
{
    FAIChatPlus_OllamaChatRequestOptions Options;
    Options.Model = TEXT("llama3.2");
    Options.bStream = true;

// إضافة خيارات JSON إضافية
    Options.ExtraJsonString = TEXT("{\"format\": \"json\"}");

    auto Request = UAIChatPlus_OllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Return a JSON with name and age fields."), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

##معالجة الأخطاء

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

// مؤشرات الأداء المميزة في أولاما
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

##إيقاف الطلب

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

--8<-- "footer_ar.md"


> هذا المنشور مترجم باستخدام ChatGPT، يُرجى تقديم [**ملاحظاتكم**](https://github.com/disenone/wiki_blog/issues/new)أشر إلى أي نقص في ذلك. 
