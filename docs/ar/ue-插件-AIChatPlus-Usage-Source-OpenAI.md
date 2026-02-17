---
layout: post
title: OpenAI / Azure
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
description: OpenAI / Azure
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - OpenAI / Azure" />

#مقالة C++ - OpenAI / Azure

يصف هذا المستند كيفية استخدام OpenAI وواجهة برمجة تطبيقات Azure في لغة C++ لإجراء الدردشة وتحليل الصور والإدخال والإخراج الصوتي واستدعاء الأدوات.

> **ملاحظة**: إن Azure API متوافق مع OpenAI، وطريقة الاستخدام متشابهة إلى حد كبير، كل ما تحتاجه هو تعديل `BaseUrl` و `ApiKey`.

##الاستعدادات

قبل الاستخدام، يرجى التأكد من:

1. أضف تبعيات الوحدة النمطية في ملف `.Build.cs` للمشروع:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

2. تضمين ملفات الرأس الضرورية:

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"
#include "Common/AIChatPlus_Log.h"
```

##الدردشة النصية

###الدردشة النصية الأساسية

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"

void UMyClass::SendOpenAIChatRequest()
{
// خيارات التكوين
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-openai-api-key");
    Options.Model = TEXT("gpt-4o-mini");
الخيارات.بستريم = صحيح؛  // تفعيل الإخراج المتدفق
    Options.Temperature = 0.7f;
    Options.MaxOutputTokens = 1024;

// إنشاء رسالة
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is the capital of France?"), EAIChatPlus_ChatRole::User});

// إنشاء طلب
    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// ربط رد النداء
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Message: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Token Usage: %s"), *Response.Usage.GetDescription());
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_OpenAIChatResponseError>();
        UE_LOG(LogTemp, Error, TEXT("Request Failed: %s"), *Error.GetDescription());
    });

// إرسال الطلب
    Request->SendRequest();
}
```

###استخدم واجهة برمجة التطبيقات في Azure

واجهة برمجة التطبيقات من Azure متوافقة مع OpenAI، فقط تحتاج إلى تعديل عنوان URL وطريقة المصادقة:

```cpp
#include "Common_Azure/AIChatPlus_AzureChatRequest.h"

void UMyClass::SendAzureChatRequest()
{
    FAIChatPlus_AzureChatRequestOptions Options;
    Options.ApiKey = TEXT("your-azure-api-key");
Options.ResourceName = TEXT("اسم-مصدرك"); // اسم مورد Azure
Options.DeploymentName = TEXT("اسم-نشرك"); // اسم النشر
Options.ApiVersion = TEXT("2024-02-01"); // إصدار API
    Options.bStream = true;

    auto Request = UAIChatPlus_AzureChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System},
            {TEXT("Hello!"), EAIChatPlus_ChatRole::User}
        });

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Azure Message: %s"), *Message);
    });

    Request->SendRequest();
}
```

###حوار متعدد الجولات

```cpp
void UMyClass::MultiTurnConversation()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

// بناء تاريخ المحادثات متعددة الجولات
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("My name is Alice."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("Hello Alice! Nice to meet you. How can I help you today?"), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my name?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
// يجب أن يتذكر النموذج أن اسم المستخدم هو أليس
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##رؤية (تحليل الصور)

تسمح ميزة Vision من OpenAI للنموذج بتحليل محتوى الصور.

###تحميل الصورة من الملف وتحليلها

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageFromFile()
{
// تحميل الصورة من الملف
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image: %s"), *ImagePath);
        return;
    }

// إنشاء كائن Texture متاح للمكوّن الإضافي
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

// خيارات التكوين
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
 النموذج = نص("gpt-4o");  // يحتاج الرؤية إلى gpt-4o أو gpt-4-turbo
    Options.bStream = true;

// إنشاء رسالة مع صورة
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("What is in this image? Describe it in detail.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant that can analyze images."), EAIChatPlus_ChatRole::System},
            ImageMessage
        });

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Vision Analysis: %s"), *Message);
    });

    Request->SendRequest();
}
```

###من تحليل Texture2D (لقطة شاشة داخل اللعبة)

```cpp
void UMyClass::AnalyzeGameTexture(UTexture2D* GameTexture)
{
    if (!GameTexture)
    {
        UE_LOG(LogTemp, Error, TEXT("Invalid texture"));
        return;
    }

// التحويل إلى المكون الإضافي Texture
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(GameTexture);

    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o");
    Options.bStream = true;

    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("Analyze this game screenshot and describe what you see.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options, {{TEXT("You are a game analyst."), EAIChatPlus_ChatRole::System}, ImageMessage});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Game Analysis: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##Audio (إدخال وإخراج الصوت)

أوبن أيه آي تدعم ميزة إدخال وإخراج الصوت (يتطلب نموذج `gpt-4o-audio-preview`).

###إدخال الصوت (التعرف على الكلام)

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::SendAudioMessage()
{
// تحميل الصوت من الملف
    FString AudioPath = FPaths::ProjectContentDir() / TEXT("Audio/question.wav");
    USoundWave* SoundWave = UAIChatPlus_Util::LoadSoundWav(AudioPath);

    if (!SoundWave)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load audio: %s"), *AudioPath);
        return;
    }

إنشاء كائن Sound متاح للمكونات الإضافية
    UAIChatPlus_Sound* ChatSound = UAIChatPlus_Sound::CreateFromSoundWave(SoundWave);

// خيارات التكوين
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
الخيارات.النموذج = نص("gpt-4o-audio-preview");  // نموذج يدعم الصوت
الخيارات.bStream = false;  // إخراج الصوت لا يدعم البث المتدفق

    // إنشاء رسالة تحتوي على صوت
    FAIChatPlus_ChatRequestMessage AudioMessage;
AudioMessage.Content = TEXT("");  // الرسالة الصوتية قد لا تحتاج إلى نص
    AudioMessage.Role = EAIChatPlus_ChatRole::User;
    AudioMessage.Audios.Add(ChatSound);

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant. Listen to the audio and respond."), EAIChatPlus_ChatRole::System},
            AudioMessage
        });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Response to audio: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###الإخراج الصوتي (تحويل النص إلى كلام)

```cpp
void UMyClass::RequestAudioOutput()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-audio-preview");
    الخيارات.بستريم = خطأ؛  // مخرجات الصوت لا تدعم البث المتدفق

// تكوين إخراج الصوت
    Options.Modalities.Add(EAIChatPlus_OpenAIChatModality::Text);
    Options.Modalities.Add(EAIChatPlus_OpenAIChatModality::Audio);
    Options.AudioConfig.Format = TEXT("wav");
    الخيارات.إعدادات_الصوت.الصوت = TEXT("alloy");  // اختياري: alloy، ash، ballad، coral، echo، sage، shimmer، verse

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System},
            {TEXT("Tell me a short joke."), EAIChatPlus_ChatRole::User}
        });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

// الحصول على استجابة نصية
        UE_LOG(LogTemp, Display, TEXT("Text Response: %s"), *Response.GetMessage());

// الحصول على استجابة الصوت
        TArray<FAIChatPlus_ChatResponseAudioOutput> AudioOutputs = Response.GetAudioOutputs();
        for (const auto& AudioOutput : AudioOutputs)
        {
            if (AudioOutput.Sound)
            {
// تشغيل الصوت
// AudioOutput.Sound هو UAIChatPlus_Sound*، يمكن الحصول على USoundWave منه
                UE_LOG(LogTemp, Display, TEXT("Audio Transcript: %s"), *AudioOutput.Transcript);

// حفظ الصوت في ملف
                FString SavePath = FPaths::ProjectSavedDir() / TEXT("Audio/response.wav");
                UAIChatPlus_Util::SaveSoundWav(AudioOutput.Sound->GetSoundWave(), SavePath);
            }
        }
    });

    Request->SendRequest();
}
```

##استدعاء الأداة (استدعاء الدالة)

يسمح "استدعاء الأداة" للنموذج باستدعاء وظائف محددة مسبقًا للحصول على بيانات خارجية.

###تحديد الأداة وإرسال الطلب

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"

void UMyClass::SendToolCallRequest()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

// تعريف الأداة: الحصول على الطقس
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a location.");

// تعريف معلمات الأدوات
    FAIChatPlus_ChatRequestToolProperty LocationProp;
    LocationProp.Name = TEXT("location");
    LocationProp.Description = TEXT("The city name, e.g. Beijing, Tokyo, New York");
    LocationProp.Type = TEXT("string");
    LocationProp.Required = true;

    FAIChatPlus_ChatRequestToolProperty UnitProp;
    UnitProp.Name = TEXT("unit");
    UnitProp.Description = TEXT("The temperature unit");
    UnitProp.Type = TEXT("string");
    UnitProp.Required = false;
    UnitProp.ExtraJsonString = TEXT("{\"enum\": [\"celsius\", \"fahrenheit\"]}");

    WeatherTool.Properties.Add(LocationProp);
    WeatherTool.Properties.Add(UnitProp);

    Options.Tools.Add(WeatherTool);

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant. Use tools when needed."), EAIChatPlus_ChatRole::System},
            {TEXT("What's the weather like in Tokyo?"), EAIChatPlus_ChatRole::User}
        });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

// التحقق من وجود نداء للأداة
        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
            for (const auto& ToolCall : ToolCalls)
            {
                UE_LOG(LogTemp, Display, TEXT("Tool Call - ID: %s, Function: %s, Args: %s"),
                    *ToolCall.Id, *ToolCall.FunctionName, *ToolCall.FunctionArguments);

// هنا نقوم بتنفيذ الاستدعاء الفعلي للدالة، ثم نرسل النتيجة إلى النموذج
// انظر إلى مثال "معالجة نتيجة نداء الأداة" أدناه
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

عندما يُعيد النموذج استدعاء الأداة (Tool Call)، يجب تنفيذ الوظيفة وإرسال النتيجة مرة أخرى إلى النموذج:

```cpp
void UMyClass::HandleToolCallAndSendResult()
{
    // لنفترض أن هذا هو استدعاء الأداة الذي تم إرجاعه من النموذج
    FString ToolCallId = TEXT("call_abc123");
    FString FunctionName = TEXT("get_weather");
    FString FunctionResult = TEXT("{\"temperature\": 22, \"unit\": \"celsius\", \"description\": \"Sunny\"}");

    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

// إعادة تعريف الأداة (الحفاظ على الاتساق)
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a location.");
    Options.Tools.Add(WeatherTool);

// بناء سجل الرسائل الذي يتضمن نتائج استدعاء الأداة
    TArray<FAIChatPlus_ChatRequestMessage> Messages;

// 1. رسائل النظام
    Messages.Add({TEXT("You are a helpful assistant. Use tools when needed."), EAIChatPlus_ChatRole::System});

// 2. السؤال الأصلي للمستخدم
    Messages.Add({TEXT("What's the weather like in Tokyo?"), EAIChatPlus_ChatRole::User});

// 3. طلب استدعاء أداة المساعد
    FAIChatPlus_ChatRequestMessage AssistantMessage;
    AssistantMessage.Role = EAIChatPlus_ChatRole::Assistant;
المساعدMessage.Content = TEXT("");  // قد لا يكون هناك محتوى نصي عند استدعاء الأداة

    FAIChatPlus_ChatRequestToolCall ToolCallUse;
    ToolCallUse.Id = ToolCallId;
    ToolCallUse.Type = TEXT("function");
    ToolCallUse.FunctionName = FunctionName;
    ToolCallUse.FunctionArguments = TEXT("{\"location\": \"Tokyo\"}");
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
    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
// سيقوم النموذج بإنشاء الرد النهائي بناءً على نتائج الأداة
        UE_LOG(LogTemp, Display, TEXT("Final Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###دورة كاملة لـ Tool Call

فيما يلي مثال كامل لدورة اتصال الأدوات:

```cpp
// تخزين سجل المحادثة
TArray<FAIChatPlus_ChatRequestMessage> ConversationHistory;
FAIChatPlus_OpenAIChatRequestOptions CurrentOptions;

void UMyClass::InitializeToolChat()
{
    CurrentOptions.ApiKey = TEXT("your-api-key");
    CurrentOptions.Model = TEXT("gpt-4o-mini");
    CurrentOptions.bStream = true;

// تعريف الأدوات
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a location.");

    FAIChatPlus_ChatRequestToolProperty LocationProp;
    LocationProp.Name = TEXT("location");
    LocationProp.Type = TEXT("string");
    LocationProp.Required = true;
    WeatherTool.Properties.Add(LocationProp);

    CurrentOptions.Tools.Add(WeatherTool);

// تهيئة المحادثة
    ConversationHistory.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}

void UMyClass::SendUserMessage(const FString& UserMessage)
{
    ConversationHistory.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(CurrentOptions, ConversationHistory);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
// التعامل مع استدعاء الأداة
            ProcessToolCalls(ToolCalls, Response.GetMessage());
        }
        else
        {
// رد عادي
            FString AssistantMessage = Response.GetMessage();
            ConversationHistory.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});
            OnAssistantResponse(AssistantMessage);
        }
    });

    Request->SendRequest();
}

void UMyClass::ProcessToolCalls(const TArray<FAIChatPlus_ChatResponseToolCall>& ToolCalls, const FString& AssistantContent)
{
// إضافة رسالة نداء أداة Assistant
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
    ConversationHistory.Add(AssistantMsg);

// تنفيذ كل أداة وإضافة النتائج
    FAIChatPlus_ChatRequestMessage ToolResultMsg;
    ToolResultMsg.Role = EAIChatPlus_ChatRole::Tool;

    for (const auto& ToolCall : ToolCalls)
    {
        FString Result = ExecuteTool(ToolCall.FunctionName, ToolCall.FunctionArguments);

        FAIChatPlus_ChatRequestToolCallResult ToolResult;
        ToolResult.Id = ToolCall.Id;
        ToolResult.FunctionName = ToolCall.FunctionName;
        ToolResult.FunctionResult = Result;
        ToolResultMsg.ToolCallResults.Add(ToolResult);
    }
    ConversationHistory.Add(ToolResultMsg);

// إرسال الطلب مع نتائج الأداة
    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(CurrentOptions, ConversationHistory);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> NewToolCalls = Response.GetToolCalls();
        if (NewToolCalls.Num() > 0)
        {
// قد يكون هناك حاجة لمواصلة استدعاء الأدوات
            ProcessToolCalls(NewToolCalls, Response.GetMessage());
        }
        else
        {
            FString FinalMessage = Response.GetMessage();
            ConversationHistory.Add({FinalMessage, EAIChatPlus_ChatRole::Assistant});
            OnAssistantResponse(FinalMessage);
        }
    });

    Request->SendRequest();
}

FString UMyClass::ExecuteTool(const FString& FunctionName, const FString& Arguments)
{
    if (FunctionName == TEXT("get_weather"))
    {
        // تحليل المعلمات وتنفيذ استعلام الطقس الفعلي
// هنا يتم إرجاع بيانات وهمية
        return TEXT("{\"temperature\": 22, \"unit\": \"celsius\", \"description\": \"Sunny\"}");
    }

    return TEXT("{\"error\": \"Unknown function\"}");
}

void UMyClass::OnAssistantResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Assistant: %s"), *Response);
}
```

##إنشاء الصور

استخدم نموذج DALL-E من OpenAI لتوليد الصور:

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIImageRequest.h"

void UMyClass::GenerateImage()
{
    FAIChatPlus_OpenAIImageRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("dall-e-3");
    Options.ChatType = EAIChatPlus_ImageChatType::Generation;
    Options.Size = TEXT("1024x1024");
    Options.Quality = EAIChatPlus_OpenAIImageQuality::Standard;
    Options.ResponseFormat = EAIChatPlus_OpenAIImageResponseFormat::Url;

    auto Request = UAIChatPlus_OpenAIImageRequest::CreateWithOptions(Options);
    Request->SetPrompt(TEXT("A beautiful sunset over mountains, digital art style"));

    Request->OnImagesListeners.AddLambda([](const TArray<UTexture2D*>& Images, bool bFinished)
    {
        for (int32 i = 0; i < Images.Num(); ++i)
        {
            if (Images[i])
            {
// حفظ الصورة
                FString SavePath = FString::Printf(TEXT("%s/GeneratedImages/image_%d.png"),
                    *FPaths::ProjectSavedDir(), i);
                UAIChatPlus_Util::SaveImage(Images[i], SavePath);
                UE_LOG(LogTemp, Display, TEXT("Image saved to: %s"), *SavePath);
            }
        }
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_OpenAIChatResponseError>();
        UE_LOG(LogTemp, Error, TEXT("Image generation failed: %s"), *Error.GetDescription());
    });

    Request->SendRequest();
}
```

##الإعدادات المتقدمة

###استخدم خيار تمديد JSON

من خلال `ExtraJsonString` أو `ExtraJsonObject` لإضافة خيارات غير مدعومة مباشرةً بواسطة API:

```cpp
void UMyClass::UseExtraJsonOptions()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");

// استخدام سلسلة JSON لإضافة خيارات إضافية
    Options.ExtraJsonString = TEXT("{\"store\": false, \"metadata\": {\"user_id\": \"12345\"}}");

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###رابط نقطة النهاية المخصص

يدعم استخدام نقاط نهاية API مخصصة (مثل خوادم الوكيل):

```cpp
void UMyClass::UseCustomEndpoint()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");

    // الطريقة 1: تعيين BaseUrl وEndPointUrl بشكل منفصل
    Options.BaseUrl = TEXT("https://your-proxy-server.com");
    Options.EndPointUrl = TEXT("v1/chat/completions");

    // الطريقة 2: تعيين عنوان URL كامل مباشرة (سيتم تجاهل BaseUrl و EndPointUrl)
    // Options.FullUrl = TEXT("https://your-proxy-server.com/v1/chat/completions");

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

##معالجة الأخطاء

###مثال كامل لمعالجة الأخطاء

```cpp
void UMyClass::RobustChatRequest()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->OnStartedListeners.AddLambda([]()
    {
        UE_LOG(LogTemp, Display, TEXT("Request started..."));
    });

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
// رسائل البث
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

        // التحقق مما إذا كان هناك خطأ في الاستجابة
        if (Response.HasError())
        {
            UE_LOG(LogTemp, Error, TEXT("Response error: %s"), *Response.Error.GetDescription());
            return;
        }

        UE_LOG(LogTemp, Display, TEXT("Success: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Tokens used: %s"), *Response.Usage.GetDescription());
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_OpenAIChatResponseError>();
        UE_LOG(LogTemp, Error, TEXT("Request failed!"));
        UE_LOG(LogTemp, Error, TEXT("  Code: %s"), *Error.Code);
        UE_LOG(LogTemp, Error, TEXT("  Type: %s"), *Error.Type);
        UE_LOG(LogTemp, Error, TEXT("  Message: %s"), *Error.Message);
        UE_LOG(LogTemp, Error, TEXT("  Param: %s"), *Error.Param);
    });

    Request->SendRequest();
}
```

##طلب الإيقاف

يمكن إيقاف الطلبات الجارية:

```cpp
// تخزين مرجع الطلب
UPROPERTY()
UAIChatPlus_OpenAIChatRequest* CurrentRequest = nullptr;

void UMyClass::StartRequest()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
// ... خيارات التكوين

    CurrentRequest = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a very long story."), EAIChatPlus_ChatRole::User}});

    CurrentRequest->SendRequest();
}

void UMyClass::CancelRequest()
{
    if (CurrentRequest && CurrentRequest->IsActivated())
    {
        CurrentRequest->StopRequest();
        UE_LOG(LogTemp, Display, TEXT("Request cancelled"));
    }
}
```

--8<-- "footer_ar.md"


> هذا المنشور مترجم باستخدام ChatGPT، يُرجى تقديم [**تغذية راجعة**](https://github.com/disenone/wiki_blog/issues/new)أشر إلى أيّ إغفال في ذلك. 
