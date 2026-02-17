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

#C++ Kapitel - OpenAI / Azure

Dieses Dokument erklärt, wie man in C++ die OpenAI- und Azure-API für Chatfunktionen, Bildanalyse, Spracheingabe/-ausgabe und Tool Calling nutzt.

> **Hinweis**: Die Azure-API ist mit OpenAI kompatibel und wird auf ähnliche Weise verwendet. Sie müssen lediglich die `BaseUrl` und den `ApiKey` anpassen.

##Vorbereitungen

Vor der Verwendung bitte sicherstellen, dass:

1. Fügen Sie im `.Build.cs`-File des Projekts die Modulabhängigkeit hinzu:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

2. Fügen Sie die erforderlichen Header-Dateien ein:

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"
#include "Common/AIChatPlus_Log.h"
```

##Text-Chat

###Grundlegender Text-Chat

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"

void UMyClass::SendOpenAIChatRequest()
{
// Optionen konfigurieren
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-openai-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;  // Aktiviert die Streaming-Ausgabe
    Options.Temperature = 0.7f;
    Options.MaxOutputTokens = 1024;

    // Nachricht erstellen
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is the capital of France?"), EAIChatPlus_ChatRole::User});

    // Anfrage erstellen
    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    // Rückruf binden
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

    // Anfrage senden
    Request->SendRequest();
}
```

###Verwenden der Azure-API

Azure API ist mit OpenAI kompatibel und erfordert lediglich eine Anpassung der URL und der Authentifizierungsmethode:

```cpp
#include "Common_Azure/AIChatPlus_AzureChatRequest.h"

void UMyClass::SendAzureChatRequest()
{
    FAIChatPlus_AzureChatRequestOptions Options;
    Options.ApiKey = TEXT("your-azure-api-key");
Options.ResourceName = TEXT("Ihr-Ressourcen-Name");  // Azure-Ressourcenname
Options.DeploymentName = TEXT("your-deployment-name");  // Bereitstellungsname
Options.ApiVersion = TEXT("2024-02-01");  // API-Version
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

###Mehrrunden-Dialog

```cpp
void UMyClass::MultiTurnConversation()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

    // Mehrfachdialogverlauf konstruieren
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("My name is Alice."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("Hello Alice! Nice to meet you. How can I help you today?"), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my name?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
// Das Modell sollte sich merken können, dass der Benutzername Alice ist
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##Vision (Bildanalyse)

Die Vision-Funktion von OpenAI ermöglicht es dem Modell, Bildinhalte zu analysieren.

###Bild aus einer Datei laden und analysieren

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageFromFile()
{
    // Bild aus einer Datei laden
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image: %s"), *ImagePath);
        return;
    }

    // Erstellt ein Texture-Objekt für die Verwendung durch Plugins
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

    // Optionen konfigurieren
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
Options.Model = TEXT("gpt-4o");  // Vision benötigt gpt-4o oder gpt-4-turbo
    Options.bStream = true;

// Erstellen einer Nachricht mit Bild
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

###Analyse der Texture2D (In-Game-Screenshot)

```cpp
void UMyClass::AnalyzeGameTexture(UTexture2D* GameTexture)
{
    if (!GameTexture)
    {
        UE_LOG(LogTemp, Error, TEXT("Invalid texture"));
        return;
    }

// In Plugin-Textur umwandeln
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

##Audio (Sprachaufnahme und -ausgabe)

OpenAI unterstützt Sprach- und Audiofunktionen (erfordert das Modell `gpt-4o-audio-preview`).

###Spracheingabe (Speech-to-Text)

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::SendAudioMessage()
{
// Audiodatei aus Datei laden
    FString AudioPath = FPaths::ProjectContentDir() / TEXT("Audio/question.wav");
    USoundWave* SoundWave = UAIChatPlus_Util::LoadSoundWav(AudioPath);

    if (!SoundWave)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load audio: %s"), *AudioPath);
        return;
    }

    // Sound-Objekt für die Plug-in-Verwendung erstellen
    UAIChatPlus_Sound* ChatSound = UAIChatPlus_Sound::CreateFromSoundWave(SoundWave);

// Optionen konfigurieren
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-audio-preview");  // Modell mit Audio-Unterstützung
Options.bStream = false;  // Audio-Ausgabe unterstützt kein Streaming

// Erstellen einer Nachricht mit Audio
    FAIChatPlus_ChatRequestMessage AudioMessage;
AudioMessage.Inhalt = TEXT(""); // Bei Audiomeldungen ist kein Text erforderlich
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

###Sprachausgabe (Text-to-Speech)

```cpp
void UMyClass::RequestAudioOutput()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-audio-preview");
    Options.bStream = false;  // Audio-Ausgabe unterstützt kein Streaming

    // Audioausgabe konfigurieren
    Options.Modalities.Add(EAIChatPlus_OpenAIChatModality::Text);
    Options.Modalities.Add(EAIChatPlus_OpenAIChatModality::Audio);
    Options.AudioConfig.Format = TEXT("wav");
Options.AudioConfig.Voice = TEXT("alloy");  // Optional: alloy, ash, ballad, coral, echo, sage, shimmer, verse

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System},
            {TEXT("Tell me a short joke."), EAIChatPlus_ChatRole::User}
        });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

        // Textantwort abrufen
        UE_LOG(LogTemp, Display, TEXT("Text Response: %s"), *Response.GetMessage());

// Die Audioantwort abrufen
        TArray<FAIChatPlus_ChatResponseAudioOutput> AudioOutputs = Response.GetAudioOutputs();
        for (const auto& AudioOutput : AudioOutputs)
        {
            if (AudioOutput.Sound)
            {
// Audio abspielen
// AudioOutput.Sound ist ein UAIChatPlus_Sound*, aus dem man den USoundWave abrufen kann
                UE_LOG(LogTemp, Display, TEXT("Audio Transcript: %s"), *AudioOutput.Transcript);

                // Audio in Datei speichern
                FString SavePath = FPaths::ProjectSavedDir() / TEXT("Audio/response.wav");
                UAIChatPlus_Util::SaveSoundWav(AudioOutput.Sound->GetSoundWave(), SavePath);
            }
        }
    });

    Request->SendRequest();
}
```

##Tool Calling (Funktionsaufruf)

Tool Calling ermöglicht es dem Modell, vordefinierte Funktionen aufzurufen, um externe Daten zu beschaffen.

###Werkzeug definieren und Anfrage senden

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"

void UMyClass::SendToolCallRequest()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

// Werkzeug definieren: Wetter abrufen
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a location.");

// Definieren der Werkzeugparameter
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

// Überprüfen, ob ein Tool-Call vorhanden ist
        TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
        if (ToolCalls.Num() > 0)
        {
            for (const auto& ToolCall : ToolCalls)
            {
                UE_LOG(LogTemp, Display, TEXT("Tool Call - ID: %s, Function: %s, Args: %s"),
                    *ToolCall.Id, *ToolCall.FunctionName, *ToolCall.FunctionArguments);

// Hier wird der tatsächliche Funktionsaufruf durchgeführt, dann wird das Ergebnis zurück an das Modell gesendet
// Siehe das Beispiel "Tool Call Ergebnisse verarbeiten" unten
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

###Tool Call-Ergebnisse verarbeiten

Wenn das Modell einen Tool Call zurückgibt, müssen Sie die Funktion ausführen und das Ergebnis an das Modell zurücksenden:

```cpp
void UMyClass::HandleToolCallAndSendResult()
{
    // Angenommen, dies ist der zurückgegebene Tool-Aufruf des Modells
    FString ToolCallId = TEXT("call_abc123");
    FString FunctionName = TEXT("get_weather");
    FString FunctionResult = TEXT("{\"temperature\": 22, \"unit\": \"celsius\", \"description\": \"Sunny\"}");

    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
    Options.bStream = true;

// Das Werkzeug neu definieren (für Konsistenz sorgen)
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a location.");
    Options.Tools.Add(WeatherTool);

    // Nachrichtenverlauf mit Tool Call-Ergebnissen erstellen
    TArray<FAIChatPlus_ChatRequestMessage> Messages;

// 1. Systemnachrichten
    Messages.Add({TEXT("You are a helpful assistant. Use tools when needed."), EAIChatPlus_ChatRole::System});

    // 2. Ursprüngliche Frage des Benutzers
    Messages.Add({TEXT("What's the weather like in Tokyo?"), EAIChatPlus_ChatRole::User});

    // 3. Assistant-Anfrage für Tool-Aufruf
    FAIChatPlus_ChatRequestMessage AssistantMessage;
    AssistantMessage.Role = EAIChatPlus_ChatRole::Assistant;
    AssistantMessage.Content = TEXT("");  // Beim Tool Call gibt es möglicherweise keinen Textinhalt

    FAIChatPlus_ChatRequestToolCall ToolCallUse;
    ToolCallUse.Id = ToolCallId;
    ToolCallUse.Type = TEXT("function");
    ToolCallUse.FunctionName = FunctionName;
    ToolCallUse.FunctionArguments = TEXT("{\"location\": \"Tokyo\"}");
    AssistantMessage.ToolCallUses.Add(ToolCallUse);
    Messages.Add(AssistantMessage);

// 4. Werkzeug-Ausführungsergebnis
    FAIChatPlus_ChatRequestMessage ToolResultMessage;
    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;

    FAIChatPlus_ChatRequestToolCallResult ToolResult;
    ToolResult.Id = ToolCallId;
    ToolResult.FunctionName = FunctionName;
    ToolResult.FunctionResult = FunctionResult;
    ToolResultMessage.ToolCallResults.Add(ToolResult);
    Messages.Add(ToolResultMessage);

// Anfrage senden
    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);
// Das Modell generiert die endgültige Antwort basierend auf den Werkzeugen-Ergebnissen
        UE_LOG(LogTemp, Display, TEXT("Final Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###Voller Tool Call-Zyklus

Hier ist ein vollständiges Beispiel für eine Tool-Calling-Schleife:

```cpp
// Gesprächsverlauf speichern
TArray<FAIChatPlus_ChatRequestMessage> ConversationHistory;
FAIChatPlus_OpenAIChatRequestOptions CurrentOptions;

void UMyClass::InitializeToolChat()
{
    CurrentOptions.ApiKey = TEXT("your-api-key");
    CurrentOptions.Model = TEXT("gpt-4o-mini");
    CurrentOptions.bStream = true;

// Definition der Werkzeuge
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

// Initialisierung des Dialogs
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
// Tool Call verarbeiten
            ProcessToolCalls(ToolCalls, Response.GetMessage());
        }
        else
        {
// Normale Antwort
            FString AssistantMessage = Response.GetMessage();
            ConversationHistory.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});
            OnAssistantResponse(AssistantMessage);
        }
    });

    Request->SendRequest();
}

void UMyClass::ProcessToolCalls(const TArray<FAIChatPlus_ChatResponseToolCall>& ToolCalls, const FString& AssistantContent)
{
// Füge die Tool Call-Nachricht des Assistenten hinzu
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

    // Führe jedes Tool aus und füge die Ergebnisse hinzu
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

    // Anfrage mit Werkzeughinweisen senden
    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(CurrentOptions, ConversationHistory);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

        TArray<FAIChatPlus_ChatResponseToolCall> NewToolCalls = Response.GetToolCalls();
        if (NewToolCalls.Num() > 0)
        {
// Möglicherweise müssen weiterhin Tools aufgerufen werden
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
// Parse die Parameter und führe die eigentliche Wetterabfrage durch
// Hier werden die simulierten Daten zurückgegeben
        return TEXT("{\"temperature\": 22, \"unit\": \"celsius\", \"description\": \"Sunny\"}");
    }

    return TEXT("{\"error\": \"Unknown function\"}");
}

void UMyClass::OnAssistantResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Assistant: %s"), *Response);
}
```

##Bildgenerierung

Bilder mit dem DALL-E-Modell von OpenAI generieren:

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
// Bild speichern
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

##Erweiterte Konfiguration

###Verwenden der JSON-Erweiterungsoptionen

Durch `ExtraJsonString` oder `ExtraJsonObject` können Optionen hinzugefügt werden, die von der API nicht direkt unterstützt werden:

```cpp
void UMyClass::UseExtraJsonOptions()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");

// Hinzufügen zusätzlicher Optionen mit einem JSON-String
    Options.ExtraJsonString = TEXT("{\"store\": false, \"metadata\": {\"user_id\": \"12345\"}}");

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###Benutzerdefinierte Endpunkt-URL

Unterstützung für die Verwendung benutzerdefinierter API-Endpunkte (z.B. Proxyserver):

```cpp
void UMyClass::UseCustomEndpoint()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");

    // Methode 1: BaseUrl und EndPointUrl separat festlegen
    Options.BaseUrl = TEXT("https://your-proxy-server.com");
    Options.EndPointUrl = TEXT("v1/chat/completions");

    // Methode 2: Direktes Setzen der vollständigen URL (ignoriert BaseUrl und EndPointUrl)
    // Options.FullUrl = TEXT("https://your-proxy-server.com/v1/chat/completions");

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

##Fehlerbehandlung

###Komplettes Beispiel zur Fehlerbehandlung

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
// Streaming-Nachrichten
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_OpenAIChatRequest::CastWrapperToResponse(ResponseWrapper);

        // Überprüfen, ob die Antwort einen Fehler enthält
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

##Stoppanforderung

Laufende Anforderungen können gestoppt werden:

```cpp
// Anforderungsreferenz speichern
UPROPERTY()
UAIChatPlus_OpenAIChatRequest* CurrentRequest = nullptr;

void UMyClass::StartRequest()
{
    FAIChatPlus_OpenAIChatRequestOptions Options;
    // ... Konfigurationsoptionen

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

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte [**Feedback geben**](https://github.com/disenone/wiki_blog/issues/new)weisen auf etwaige Auslassungen hin. 
