---
layout: post
title: Cllama (veraltet)
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
- Cllama
- llama.cpp
- Offline LLM
description: Cllama
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Cllama" />

#C++ Kapitel - Cllama (veraltet)

##Verworfen

Cllama wurde als **veraltet** markiert und wird nicht mehr gewartet.

Die ursprünglichen Funktionen von Cllama werden von [CllamaServer](ue-插件-AIChatPlus-Usage-Source-CllamaServer.md)zu tragen.

##Offline-Modell

Dieses Dokument erklärt, wie Cllama (integriert mit llama.cpp) für lokale Offline-Inferenz in C++ verwendet wird.

Cllama ermöglicht die Ausführung großer Sprachmodelle ohne Internetverbindung, was ideal für Szenarien mit Bedarf an Offline-Inferenz oder Datenschutz ist.

##Vorbereitungen

Vor Gebrauch bitte sicherstellen:

1. **GGUF-Modelldatei herunterladen**: Von [Hugging Face](https://huggingface.co)Laden Sie die kompatible GGUF-Modell-Datei herunter.

2. Fügen Sie im `.Build.cs`-File des Projekts die Modulabhängigkeiten hinzu:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

3. Notwendige Header-Dateien einbinden:

```cpp
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"
```

##Überprüfung der Verfügbarkeit von Cllama

Vor der Verwendung können Sie prüfen, ob Cllama verfügbar ist und welche Backends unterstützt werden:

```cpp
#include "Common/AIChatPlus_Util.h"

void UMyClass::CheckCllamaSupport()
{
    // Prüfen, ob Cllama verfügbar ist
    if (UAIChatPlus_Util::Cllama_IsValid())
    {
        UE_LOG(LogTemp, Display, TEXT("Cllama is available"));

        // Überprüfen, ob GPU unterstützt wird
        if (UAIChatPlus_Util::Cllama_IsSupportGpu())
        {
            UE_LOG(LogTemp, Display, TEXT("GPU acceleration is supported"));
        }

// Abrufen der Liste unterstützter Backends
        TArray<FString> Backends = UAIChatPlus_Util::Cllama_GetSupportBackends();
        for (const FString& Backend : Backends)
        {
            UE_LOG(LogTemp, Display, TEXT("Supported backend: %s"), *Backend);
        }
    }
    else
    {
        UE_LOG(LogTemp, Error, TEXT("Cllama is not available on this platform"));
    }
}
```

##Text-Chat

###Grunder Text-Chat

```cpp
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"

void UMyClass::SendCllamaChatRequest()
{
// Optionen konfigurieren
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
Options.bStream = true;  // Aktiviert die Streaming-Ausgabe
    Options.Temperature = 0.8f;
    Options.NumGpuLayers = 99;  // Anzahl der GPU-Beschleunigungsschichten (0 = nur CPU)

// Nachricht erstellen
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is the meaning of life?"), EAIChatPlus_ChatRole::User});

// Anfrage erstellen
    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    // Rückruf binden
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Cllama: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Token Usage: %s"), *Response.Usage.GetDescription());
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_ResponseErrorBase>();
        UE_LOG(LogTemp, Error, TEXT("Request Failed: %s"), *Error.GetDescription());
    });

// Anfrage senden
    Request->SendRequest();
}
```

###Verwenden Sie einen relativen Pfad (relativ zum Content-Verzeichnis)

```cpp
void UMyClass::UseRelativeModelPath()
{
    FAIChatPlus_CllamaChatRequestOptions Options;

„// Relativer Pfad zum Content-Verzeichnis des Projekts“
    Options.ModelPath.FilePath = TEXT("Models/llama-3.2-1b-instruct-q4_k_m.gguf");

    Options.bStream = true;
    Options.NumGpuLayers = 99;

    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Hello!"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###Modell aus einer Pak-Datei laden

```cpp
void UMyClass::LoadModelFromPak()
{
// Wenn Modelle in Pak-Dateien verpackt sind, muss der Modellpfad zunächst vorbereitet werden
    FString ModelPath = TEXT("Models/my_model.gguf");

// Diese Funktion entpackt das Modell aus dem Pak in ein temporäres Verzeichnis und gibt den tatsächlichen Pfad zurück
    FString ActualPath = UAIChatPlus_Util::Cllama_PrepareModelPathFromPak(ModelPath);

    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = ActualPath;
    Options.bStream = true;

    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Hello from Pak!"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);
    Request->SendRequest();
}
```

###Mehr-Runden-Dialog

```cpp
void UMyClass::MultiTurnCllamaChat()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;

// Mehrrunden-Dialogverlauf erstellen
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("My favorite color is blue."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("That's a great choice! Blue is often associated with calmness."), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my favorite color?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###Modell wird geladen

```cpp
void UMyClass::KeepModelLoaded()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;

    // KeepAlive steuert, wie lange das Modell nach einer Anfrage im Speicher bleibt
    // 0 = Sofort nach der Anforderung entladen
    // -1 = Lädt dauerhaft
    // >0 = Hält die Ladung für die angegebene Anzahl von Sekunden
Options.KeepAlive = -1;  // Dauerhaft geladen halten

    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Hello!"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);
    Request->SendRequest();
}
```

##Vision (Bildanalyse)

Cllama unterstützt die Vision-Funktion, dafür wird ein multimodales Modell (z.B. LLaVA) benötigt sowie eine MMProject-Modelldatei bereitgestellt.

> **Hinweis**: Cllama Vision unterstützt maximal 1 Bild (`FAIChatPlus_Constants::FCllama::MaxSendImageNum = 1`).

###Bild aus Datei laden und analysieren

```cpp
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithCllama()
{
// Bild aus einer Datei laden
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image: %s"), *ImagePath);
        return;
    }

// Erstelle ein Texture-Objekt für die Verwendung durch das Plugin
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

    // Optionen konfigurieren
    FAIChatPlus_CllamaChatRequestOptions Options;

    // Das LLaVA-Modell benötigt zwei Dateien: das Hauptmodell und das MMProject-Modell
    Options.ModelPath.FilePath = TEXT("D:/Models/llava-v1.6-mistral-7b.Q4_K_M.gguf");
    Options.MMProjectModelPath.FilePath = TEXT("D:/Models/mmproj-llava-v1.6-mistral-7b-f16.gguf");

    Options.bStream = true;
    Options.NumGpuLayers = 99;
Options.MMProjectUseGpu = true;  // MMProject-Modell verwendet ebenfalls die GPU

// Erstellen einer Nachricht mit Bildern
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("What do you see in this image?");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
ImageMessage.Images.Add(ChatTexture);  // Kann nur 1 Bild hinzufügen

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Cllama Vision: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###Aus Texture2D ein Bild analysieren

```cpp
void UMyClass::AnalyzeTextureWithCllama(UTexture2D* InTexture)
{
    if (!InTexture)
    {
        UE_LOG(LogTemp, Error, TEXT("Invalid texture"));
        return;
    }

    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(InTexture);

    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llava-v1.6-mistral-7b.Q4_K_M.gguf");
    Options.MMProjectModelPath.FilePath = TEXT("D:/Models/mmproj-llava-v1.6-mistral-7b-f16.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;
    Options.MMProjectUseGpu = true;

    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("Describe this image in detail.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Description: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##Erweiterte Konfiguration

###Abtastparameterkonfiguration

```cpp
void UMyClass::ConfigureCllamaSampling()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;

    // GPU-Beschleunigung
    Options.NumGpuLayers = 99;  // So viele Schichten wie möglich auf die GPU legen

// Abtastparameter
    Optionen.Temperatur = 0.7f;  // Temperatur
Optionen.TopK = 40;          // Top-K-Sampling
    Options.TopP = 0.95f;        // Nucleus-Sampling
Options.MinP = 0.05f;        // Min-P-Sampling

    // Mirostat-Sampling (zur Steuerung der Perplexität)
Optionen.Mirostat = 2;        // 0=Deaktiviert, 1=Mirostat, 2=Mirostat 2.0
    Options.MirostatEta = 0.1f;
    Options.MirostatTau = 5.0f;

// Kontext und Generierungsbeschränkungen
Options.NumCtx = 4096;       // Größe des Kontextfensters
Options.NumPredict = 256;    // Maximale Anzahl der generierten Tokens (-1 = unendlich)

    // Wiederholungsbestrafung
Options.RepeatLastN = 64;    // Überprüft, wie viele der letzten Token sich wiederholen
    Options.RepeatPenalty = 1.1f;

// Freiheitsgradsampling am Ende
    Options.TfsZ = 1.0f;         // 1.0 = deaktiviert

    // Sequenz stoppen
    Options.StopSequences.Add(TEXT("\n\n"));
    Options.StopSequences.Add(TEXT("User:"));

// Zufälliger Seed (zur wiederholbaren Generierung)
    Options.Seed = 42;

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a short poem."), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###Benutzerdefinierte Vorlagen verwenden

```cpp
void UMyClass::UseCustomTemplate()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/my_model.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;

    // Benutzerdefinierte Prompt-Vorlage (überschreibt die integrierte Modellvorlage)
    Options.Template = TEXT("<|im_start|>system\n{{system}}<|im_end|>\n<|im_start|>user\n{{prompt}}<|im_end|>\n<|im_start|>assistant\n");

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {
            {TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System},
            {TEXT("Hello!"), EAIChatPlus_ChatRole::User}
        });

    Request->SendRequest();
}
```

##Fehlerbehandlung

```cpp
void UMyClass::RobustCllamaRequest()
{
    // Zuerst prüfen, ob Cllama verfügbar ist
    if (!UAIChatPlus_Util::Cllama_IsValid())
    {
        UE_LOG(LogTemp, Error, TEXT("Cllama is not available"));
        return;
    }

    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->OnStartedListeners.AddLambda([]()
    {
        UE_LOG(LogTemp, Display, TEXT("Cllama request started, loading model..."));
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.HasError())
        {
            UE_LOG(LogTemp, Error, TEXT("Response error: %s"), *Response.Error.GetDescription());
            return;
        }

        UE_LOG(LogTemp, Display, TEXT("Success: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Tokens: %s"), *Response.Usage.GetDescription());

// Leistungskennzahlen
        UE_LOG(LogTemp, Display, TEXT("Total Duration: %lld ns"), Response.TotalDuration);
        UE_LOG(LogTemp, Display, TEXT("Load Duration: %lld ns"), Response.LoadDuration);
        UE_LOG(LogTemp, Display, TEXT("Prompt Eval Duration: %lld ns"), Response.PromptEvalDuration);
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

##Stopp-Anfrage

```cpp
UPROPERTY()
UAIChatPlus_CllamaChatRequest* CurrentCllamaRequest = nullptr;

void UMyClass::StartCllamaRequest()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;
    Options.NumPredict = -1;  // Unbegrenzte Generierung

    CurrentCllamaRequest = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a very long story about adventures."), EAIChatPlus_ChatRole::User}});

    CurrentCllamaRequest->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Generating: %s"), *Message);
    });

    CurrentCllamaRequest->SendRequest();
}

void UMyClass::CancelCllamaRequest()
{
    if (CurrentCllamaRequest && CurrentCllamaRequest->IsActivated())
    {
        CurrentCllamaRequest->StopRequest();
        UE_LOG(LogTemp, Display, TEXT("Cllama request cancelled"));
    }
}
```

##Komplettes Beispiel zur Dialogverwaltung

```cpp
// Mitgliedsvariablen
TArray<FAIChatPlus_ChatRequestMessage> CllamaConversation;
FAIChatPlus_CllamaChatRequestOptions CllamaOptions;

void UMyClass::InitializeCllamaChat()
{
    CllamaOptions.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    CllamaOptions.bStream = true;
    CllamaOptions.NumGpuLayers = 99;
CllamaOptions.KeepAlive = -1;  // Das Modell geladen halten

    // Initialisierung des Dialogs
    CllamaConversation.Empty();
    CllamaConversation.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}

void UMyClass::SendCllamaUserMessage(const FString& UserMessage)
{
    CllamaConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(CllamaOptions, CllamaConversation);

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
// Echtzeit-Anzeige der generierten Inhalte
        UE_LOG(LogTemp, Display, TEXT("Generating: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);

// Antwort des Assistenten zum Gesprächsverlauf hinzufügen
        FString AssistantMessage = Response.GetMessage();
        CllamaConversation.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});

        OnCllamaResponse(AssistantMessage);
    });

    Request->SendRequest();
}

void UMyClass::OnCllamaResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Cllama: %s"), *Response);
}

void UMyClass::ClearCllamaConversation()
{
    CllamaConversation.Empty();
    CllamaConversation.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}
```

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte geben Sie Ihr Feedback **[hier](https://github.com/disenone/wiki_blog/issues/new)weisen auf etwaige Auslassungen hin. 
