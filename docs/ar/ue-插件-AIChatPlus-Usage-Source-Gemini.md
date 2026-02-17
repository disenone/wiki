---
layout: post
title: Gemini
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
- Gemini
- Google
description: Gemini
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Gemini" />

#مقال C++ - جيميني

يشرح هذا المستند كيفية استخدام Google Gemini API في C++ لإجراء الدردشة وتحليل الصور واستدعاء الأدوات.

##الإعدادات الأولية

قبل الاستخدام، يرجى التأكد من:

1. إضافة تبعيات الوحدة في ملف `.Build.cs` الخاص بالمشروع:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

2. تضمين ملفات الرأس الضرورية:

```cpp
#include "Common_Gemini/AIChatPlus_GeminiChatRequest.h"
```

##الدردشة النصية

###الدردشة النصية الأساسية

```cpp
#include "Common_Gemini/AIChatPlus_GeminiChatRequest.h"

void UMyClass::SendGeminiChatRequest()
{
// خيارات التهيئة
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-google-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;  // تمكين الإخراج التدريجي
    Options.MaxOutputTokens = 1024;
    Options.Temperature = 0.7f;

يتم تعيين موجه النظام لـ Gemini عبر Options.System
    Options.System = TEXT("You are a helpful assistant.");

// إنشاء رسالة المستخدم
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("What is the capital of Japan?"), EAIChatPlus_ChatRole::User});

// إنشاء الطلب
    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// ربط الردود
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Gemini: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Token Usage: %s"), *Response.Usage.GetDescription());
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

###حوار متعدد الجولات

```cpp
void UMyClass::MultiTurnGeminiChat()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant with a good memory.");

    // بناء تاريخ الحوار متعدد الجولات
    // يستخدم جيميني "user" و"model" كأدوار
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("My name is Alice."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("Hello Alice! Nice to meet you. How can I help you today?"), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my name?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);
// يجب أن يتذكر النموذج أن اسم المستخدم هو أليس
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##الرؤية (تحليل الصور)

يُدعم نموذج جيميني (Gemini) ميزة الرؤية (Vision)، مما يمكنه من تحليل محتوى الصور.

> **ملاحظة**: تدعم Gemini Vision بحد أقصى 20 صورة (`FAIChatPlus_Constants::FGemini::MaxSendImageNum = 20`).

###تحميل الصورة من الملف وتحليلها

```cpp
#include "Common_Gemini/AIChatPlus_GeminiChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithGemini()
{
// تحميل الصورة من الملف
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
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
النموذج.الخيارات = نص("gemini-1.5-flash");  // أو gemini-1.5-pro
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant that can analyze images.");

// إنشاء رسالة مع صورة
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("Please describe this image in detail.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Gemini Vision: %s"), *Message);
    });

    Request->SendRequest();
}
```

###تحليل متعدد الصور

```cpp
void UMyClass::AnalyzeMultipleImagesWithGemini()
{
// تحميل عدة صور
    TArray<UAIChatPlus_Texture*> ChatTextures;

    TArray<FString> ImagePaths = {
        FPaths::ProjectContentDir() / TEXT("Images/before.png"),
        FPaths::ProjectContentDir() / TEXT("Images/after.png")
    };

    for (const FString& Path : ImagePaths)
    {
        if (UTexture2D* Texture = UAIChatPlus_Util::LoadImage(Path))
        {
            ChatTextures.Add(UAIChatPlus_Texture::CreateFromTexture2D(Texture));
        }
    }

    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;

// إنشاء رسالة متعددة الصور
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("Compare these two images and describe the differences.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images = ChatTextures;

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Comparison: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##استدعاء الأداة (استدعاء الوظيفة)

جيميني يدعم استدعاء الأدوات (استدعاء الوظائف)، مما يسمح للنموذج باستدعاء وظائف محددة مسبقاً.

###تعريف الأدوات وإرسال الطلب

```cpp
void UMyClass::SendGeminiToolCallRequest()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant. Use tools when needed.");

// تعريف الأداة: الحصول على الطقس
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");

// تعريف معلمات الأداة
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

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("What's the weather like in Tokyo?"), EAIChatPlus_ChatRole::User}});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);

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

###معالجة نتيجة استدعاء الأداة

```cpp
void UMyClass::HandleGeminiToolCallResult()
{
// لنفترض أن هذا هو معلومات استدعاء الأداة التي تم إرجاعها بواسطة النموذج
    FString ToolCallId = TEXT("call_abc123");
    FString FunctionName = TEXT("get_weather");
    FString FunctionResult = TEXT("{\"temperature\": 25, \"unit\": \"celsius\", \"description\": \"Sunny\"}");

    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;

// إعادة تعريف الأدوات
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");
    Options.Tools.Add(WeatherTool);

// بناء تاريخ الرسالة
    TArray<FAIChatPlus_ChatRequestMessage> Messages;

// ١. سؤال المستخدم الأصلي
    Messages.Add({TEXT("What's the weather like in Tokyo?"), EAIChatPlus_ChatRole::User});

// 2. طلب استدعاء أداة المساعد
    FAIChatPlus_ChatRequestMessage AssistantMessage;
    AssistantMessage.Role = EAIChatPlus_ChatRole::Assistant;
    AssistantMessage.Content = TEXT("");

    FAIChatPlus_ChatRequestToolCall ToolCallUse;
    ToolCallUse.Id = ToolCallId;
    ToolCallUse.Type = TEXT("function");
    ToolCallUse.FunctionName = FunctionName;
    ToolCallUse.FunctionArguments = TEXT("{\"location\": \"Tokyo\"}");
    AssistantMessage.ToolCallUses.Add(ToolCallUse);
    Messages.Add(AssistantMessage);

// 3. نتائج تنفيذ الأداة
    FAIChatPlus_ChatRequestMessage ToolResultMessage;
    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;

    FAIChatPlus_ChatRequestToolCallResult ToolResult;
    ToolResult.Id = ToolCallId;
    ToolResult.FunctionName = FunctionName;
    ToolResult.FunctionResult = FunctionResult;
    ToolResultMessage.ToolCallResults.Add(ToolResult);
    Messages.Add(ToolResultMessage);

// إرسال الطلب
    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###دورة Tool Call الكاملة

```cpp
// تخزين تاريخ المحادثة
TArray<FAIChatPlus_ChatRequestMessage> GeminiConversation;
FAIChatPlus_GeminiChatRequestOptions GeminiOptions;

void UMyClass::InitializeGeminiToolChat()
{
    GeminiOptions.ApiKey = TEXT("your-api-key");
    GeminiOptions.Model = TEXT("gemini-1.5-flash");
    GeminiOptions.bStream = true;
    GeminiOptions.System = TEXT("You are a helpful assistant. Use tools when needed.");

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

    GeminiOptions.Tools.Add(WeatherTool);

مسح سجل المحادثة
    GeminiConversation.Empty();
}

void UMyClass::SendGeminiUserMessage(const FString& UserMessage)
{
    GeminiConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(GeminiOptions, GeminiConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
            ProcessGeminiToolCalls(ToolCalls, Response.GetMessage());
        }
        else
        {
            FString AssistantMessage = Response.GetMessage();
            GeminiConversation.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});
            OnGeminiResponse(AssistantMessage);
        }
    });

    Request->SendRequest();
}

void UMyClass::ProcessGeminiToolCalls(const TArray<FAIChatPlus_ChatResponseToolCall>& ToolCalls, const FString& AssistantContent)
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
    GeminiConversation.Add(AssistantMsg);

// تنفيذ الأداة وإضافة النتائج
    FAIChatPlus_ChatRequestMessage ToolResultMsg;
    ToolResultMsg.Role = EAIChatPlus_ChatRole::Tool;

    for (const auto& ToolCall : ToolCalls)
    {
        FString Result = ExecuteGeminiTool(ToolCall.FunctionName, ToolCall.FunctionArguments);

        FAIChatPlus_ChatRequestToolCallResult ToolResult;
        ToolResult.Id = ToolCall.Id;
        ToolResult.FunctionName = ToolCall.FunctionName;
        ToolResult.FunctionResult = Result;
        ToolResultMsg.ToolCallResults.Add(ToolResult);
    }
    GeminiConversation.Add(ToolResultMsg);

// متابعة المحادثة
    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(GeminiOptions, GeminiConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
            ProcessGeminiToolCalls(ToolCalls, Response.GetMessage());
        }
        else
        {
            FString FinalMessage = Response.GetMessage();
            GeminiConversation.Add({FinalMessage, EAIChatPlus_ChatRole::Assistant});
            OnGeminiResponse(FinalMessage);
        }
    });

    Request->SendRequest();
}

FString UMyClass::ExecuteGeminiTool(const FString& FunctionName, const FString& Arguments)
{
    if (FunctionName == TEXT("get_weather"))
    {
// الاستعلام الفعلي عن حالة الطقس
        return TEXT("{\"temperature\": 25, \"unit\": \"celsius\", \"description\": \"Sunny\"}");
    }

    return TEXT("{\"error\": \"Unknown tool\"}");
}

void UMyClass::OnGeminiResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Gemini: %s"), *Response);
}
```

##إعدادات متقدمة

###استخدام خيارات توسعة JSON

```cpp
void UMyClass::UseGeminiExtraOptions()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");

// إضافة خيارات JSON إضافية
    Options.ExtraJsonString = TEXT("{\"safetySettings\": [{\"category\": \"HARM_CATEGORY_HARASSMENT\", \"threshold\": \"BLOCK_NONE\"}]}");

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###URL نقطة النهاية المخصصة

```cpp
void UMyClass::UseCustomGeminiEndpoint()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");

// استخدام نقاط نهاية مخصصة (مثل خوادم الوكلاء)
    Options.BaseUrl = TEXT("https://your-proxy-server.com/v1beta/models");
الخيارات.الطريقة = نص("إنشاء المحتوى")؛ // أو دفق إنشاء المحتوى

// أو قم بتعيين عنوان URL الكامل مباشرة
    // Options.FullUrl = TEXT("https://your-proxy-server.com/v1beta/models/gemini-1.5-flash:generateContent?key=xxx");

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###إعدادات معلمات أخذ العينات

```cpp
void UMyClass::ConfigureGeminiSampling()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-pro");

// معايير العينة
Options.Temperature = 0.3f; // درجة حرارة منخفضة، نتائج أكثر تحديدًا
Options.TopK = 40;           // أخذ العينات من أعلى K
Options.TopP = 0.95f;        // أخذ العينات بالنواة
    Options.MaxOutputTokens = 2048;

    // تسلسل التوقف
    Options.StopSequences.Add(TEXT("\n\n"));
    Options.StopSequences.Add(TEXT("END"));

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a short story."), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

##معالجة الأخطاء

```cpp
void UMyClass::RobustGeminiRequest()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->OnStartedListeners.AddLambda([]()
    {
        UE_LOG(LogTemp, Display, TEXT("Gemini request started..."));
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.HasError())
        {
            UE_LOG(LogTemp, Error, TEXT("Response error: %s"), *Response.Error.GetDescription());
            return;
        }

// التحقق من FinishReason
        if (!Response.Messages.IsEmpty())
        {
            FString FinishReason = Response.Messages[0].FinishReason;
            UE_LOG(LogTemp, Display, TEXT("Finish Reason: %s"), *FinishReason);
        }

        UE_LOG(LogTemp, Display, TEXT("Success: %s"), *Response.GetMessage());
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

##طلب الإيقاف

```cpp
UPROPERTY()
UAIChatPlus_GeminiChatRequest* CurrentGeminiRequest = nullptr;

void UMyClass::StartGeminiRequest()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;

    CurrentGeminiRequest = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a very long essay about technology."), EAIChatPlus_ChatRole::User}});

    CurrentGeminiRequest->SendRequest();
}

void UMyClass::CancelGeminiRequest()
{
    if (CurrentGeminiRequest && CurrentGeminiRequest->IsActivated())
    {
        CurrentGeminiRequest->StopRequest();
        UE_LOG(LogTemp, Display, TEXT("Gemini request cancelled"));
    }
}
```

--8<-- "footer_ar.md"


> هذه المشاركة مترجمة باستخدام ChatGPT، يرجى تقديم [**تعليقاتكم**](https://github.com/disenone/wiki_blog/issues/new)أشر إلى أي نقص أو إغفال ممّا ذُكر. 
