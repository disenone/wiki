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

#C++ Einführung - Erste Schritte

##Modulvorstellung

Das Plugin ist in die folgenden Module unterteilt:

* **AIChatPlusCommon**: Laufzeitmodul (Runtime), zuständig für die Bearbeitung von Anfragen an verschiedene KI-API-Schnittstellen und die Analyse der Antwortinhalte.
* **AIChatPlusEditor**: Das Editormodul (Editor), verantwortlich für die Implementierung des Editor-AI-Chat-Tools.
* **AIChatPlusCllama**: Laufzeitmodul (Runtime), verantwortlich für die Kapselung der llama.cpp-Schnittstelle und Parameter, ermöglicht die Offline-Ausführung des großen Modells.
* **Thirdparty/LLAMACpp**: Laufzeit-Drittanbietermodul (Runtime), das die dynamischen Bibliotheken und Header-Dateien von llama.cpp integriert.

##Kerngedanke

Bevor Sie den Quellcode verwenden, müssen Sie einige Kernklassen und deren Beziehungen verstehen:

###Anfrage（请求）

`UAIChatPlus_ChatRequestBase` ist die Basisklasse für alle Chat-Anfragen. Jeder API-Provider hat entsprechende Unterklassen:

* `UAIChatPlus_OpenAIChatRequest` - OpenAI Chat-Anfrage
* `UAIChatPlus_AzureChatRequest` - Azure Chat-Anfrage
* `UAIChatPlus_ClaudeChatRequest` - Claude-Chat-Anfrage
* `UAIChatPlus_GeminiChatRequest` - Gemini-Chatanfrage
* `UAIChatPlus_OllamaChatRequest` - Ollama-Chat-Anfrage
* `UAIChatPlus_CllamaChatRequest` - Cllama Offline-Modellanfrage
* `UAIChatPlus_CllamaServerChatRequest` - CllamaServer Lokaler Server-Anfrage

Das Request-Objekt ist verantwortlich für die Konfiguration der Anfrageparameter, das Absenden der Anfrage und den Empfang von Rückrufen.

###Handler (Handler)

`UAIChatPlus_ChatHandlerBase` ist eine optionale Handler-Klasse zur einheitlichen Verwaltung von Anforderungsrückrufen.

Der Handler bietet die folgenden Delegaten an:

* `OnStarted` - Wird ausgelöst, wenn die Anforderung beginnt
* `OnMessage` - Wird ausgelöst, wenn eine Streaming-Nachricht empfangen wird (Streaming-Ausgabe)
* `OnUpdated` - Wird ausgelöst, wenn ein Update empfangen wird
* `OnFinished` – Wird ausgelöst, wenn die Anfrage abgeschlossen ist
* `OnFailed` - Wird ausgelöst, wenn die Anfrage fehlschlägt

**Wann sollte man Handler verwenden?**

* Wenn mehrere Rückruflogiken für Anfragen einheitlich verwaltet werden müssen
* Wenn Callback-Logik zwischen Blueprint und C++ gemeinsam genutzt werden muss
* Direkte Verwendung von Delegaten wie `OnStartedListeners` mit Request ermöglicht ebenfalls die Implementierung von Callback-Überwachung

###Optionen (选项)

Jeder API-Provider hat eine entsprechende Options-Struktur zur Konfiguration der API-Parameter:

* `FAIChatPlus_OpenAIChatRequestOptions` - OpenAI-Optionen (ApiKey, Model, Temperature usw.)
* `FAIChatPlus_ClaudeChatRequestOptions` - Claude-Optionen
* `FAIChatPlus_GeminiChatRequestOptions` - Gemini-Optionen
* Warte mal...

Options enthält alle für die API-Verbindung erforderlichen Konfigurationen wie API-Schlüssel, Endpunkt-URL, Modellname und Erzeugungsparameter.

###Nachrichten

`FAIChatPlus_ChatRequestMessage` ist die Nachrichtenstruktur, die an die KI gesendet wird, und enthält:

* `Inhalt` - Textinhalt
* `Rolle` - Nachrichtenrolle (System/Benutzer/Assistent/Entwickler/Werkzeug)
* `Bilder` - Bilderarray (Vision-Funktion)
* `Audios` - Audiodateien-Array (Audio-Funktion)
* `ToolCallUses` - Werkzeugaufrufanfrage
* `ToolCallResults` - Werkzeugaufrufergebnisse

###Antwort

Für jeden API-Anbieter gibt es eine entsprechende ResponseBody-Struktur:

* `FAIChatPlus_OpenAIChatResponseBody`
* `FAIChatPlus_ClaudeChatResponseBody`
* Warte mal...

Die ResponseBody enthält alle vom KI zurückgegebenen Informationen, einschließlich: Nachrichtentext, Token-Verbrauch, Werkzeugaufrufe, Audioausgabe usw.

##Grundlegende Nutzungsablauf (5-Schritte-Modell)

Der grundlegende Ablauf zum Senden einer Anfrage mit AIChatPlus ist wie folgt:

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"

void SendChatRequest()
{
    // ===== Schritt 1: Handler erstellen (optional) =====
    // Handler dient der einheitlichen Verwaltung von Rückrufen, oder es können auch direkt die Delegierten von Request verwendet werden
    TWeakObjectPtr<UAIChatPlus_ChatHandlerBase> Handler = UAIChatPlus_ChatHandlerBase::New();

    // ===== Schritt 2: Optionen konfigurieren =====
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
Options.bStream = true;  // Streamausgabe aktivieren

// ===== Schritt 3: Request erstellen =====
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("Hello, who are you?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// ===== Schritt 4: Rückruf binden =====
// Methode A: Mit einem Handler arbeiten
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

// Methode B: Direkte Verwendung der Delegation des Requests (ohne Handler notwendig)
    // Request->OnMessageListeners.AddDynamic(this, &UMyClass::OnMessageReceived);
    // Request->OnFinishedListeners.AddDynamic(this, &UMyClass::OnRequestFinished);

// ===== Schritt 5: Anfrage senden =====
    Request->SendRequest();
}
```

##Vereinfachte Schreibweise

Falls keine fein abgestimmte Rückruffunktion benötigt wird, kann folgende kompaktere Schreibweise verwendet werden:

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

// Lambda direkt an Request binden
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

##Erstellen einer Anfrage über die API-Provider-Aufzählung

Wenn Sie den API-Anbieter dynamisch basierend auf der Konfiguration auswählen müssen, können Sie die Fabrikmethode verwenden:

```cpp
void CreateRequestByProvider(EAIChatPlus_ChatApiProvider Provider)
{
// Erstelle entsprechenden Request basierend auf der Enumeration
    auto Request = UAIChatPlus_ChatRequestBase::CreateByApi(Provider);

    // Optionen entsprechend des tatsächlichen Typs festlegen
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
// ... andere Provider
    }

// Nachricht einstellen und senden
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Hello!"), EAIChatPlus_ChatRole::User});
    Request->SetMessages(Messages);
    Request->SendRequest();
}
```

##Rückrufanweisung

###Haupt-Rückrufdelegat

| Delegat | Auslösezeitpunkt | Parameter |
|------|----------|------|
| `OnStarted` | Wird ausgelöst, wenn der Versand der Anfrage beginnt | Keine |
| `OnMessage` | Wird bei Empfang einer Stream-Nachricht (jedes Token) aufgerufen | `const FString& Message` - Der akkumulierte Nachrichteninhalt |
| `OnUpdated` | Empfangen bei der Aktualisierung der Antwort | `const FAIChatPlus_ResponseBodyBase& Response` |
| `OnFinished` | Wenn die Anfrage erfolgreich abgeschlossen wurde | `const FAIChatPlus_ResponseBodyBase& Response` |
| `OnFailed` | Bei fehlgeschlagener Anfrage | `const FAIChatPlus_ResponseErrorBase& Error` |
| `OnMessageFinished` | Nachrichtenempfang abgeschlossen | `const FAIChatPlus_MessageFinishedPayload& Payload` |

###Streaming-Ausgabe vs. Nicht-Streaming-Ausgabe

* **Streaming-Ausgabe** (`bStream = true`): `OnMessage` wird mehrfach ausgelöst und gibt jedes Mal die kumulierten Nachrichteninhalte zurück
* **Nicht-Streaming-Ausgabe** (`bStream = false`): `OnMessage` wird nur einmal bei Fertigstellung ausgelöst und gibt die vollständige Nachricht zurück

##Weiter

Weitere detaillierte Verwendungsmöglichkeiten finden Sie in den speziellen Dokumentationen der jeweiligen API-Anbieter:

* [Nutzen von OpenAI / Azure](ue-插件-AIChatPlus-Usage-Source-OpenAI.md)
* [Claude-Nutzung](ue-插件-AIChatPlus-Usage-Source-Claude.md)
* [Verwendung von Gemini](ue-插件-AIChatPlus-Usage-Source-Gemini.md)
* [Ollama Nutzung](ue-插件-AIChatPlus-Usage-Source-Ollama.md)
* [Cllama Offline-Modell](ue-插件-AIChatPlus-Usage-Source-Cllama.md)
* [CllamaServer lokaler Server](ue-插件-AIChatPlus-Usage-Source-CllamaServer.md)
* [Werkzeugklasse](ue-插件-AIChatPlus-Usage-Source-Utils.md)

--8<-- "footer_de.md"

> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte geben Sie Ihr Feedback unter [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Weist auf etwaige Auslassungen hin. 
