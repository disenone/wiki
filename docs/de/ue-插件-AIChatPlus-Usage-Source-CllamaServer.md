---
layout: post
title: CllamaServer
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
- llama.cpp
- Local Server
description: CllamaServer
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - CllamaServer" />

#C++ Abschnitt - CllamaServer

Dieses Dokument beschreibt, wie Sie mit CllamaServer in C++ einen lokalen KI-Server verwalten und Chat-Anfragen senden können.

CllamaServer läuft im Servermodus von llama.cpp und stellt einen lokalen Dienst bereit, der mit der OpenAI-API kompatibel ist und gleichzeitige Anfragen mehrerer Clients unterstützt.

##Unterschiede zu Cllama

| Funktion | Cllama | CllamaServer |
|------|--------|--------------|
| Modus | Direkte Schlussfolgerung | HTTP-Server |
| Mehrere Clients | Nein | Ja |
| API-Stil | Benutzerdefiniert | OpenAI-kompatibel |
| Netzwerkzugriff | Nein | Optional |
| Tool Call | Nein | Ja |

##Vorbereitungen

Bitte stellen Sie vor der Verwendung sicher, dass:

1. **GGUF-Modelldatei herunterladen**: Von [Hugging Face](https://huggingface.co)Laden Sie die kompatible GGUF-Modell-Datei herunter.

2. Fügen Sie die Modulabhängigkeiten in der `.Build.cs`-Datei des Projekts hinzu:

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

3. Einbinden der notwendigen Header-Dateien:

```cpp
#include "Common_CllamaServer/AIChatPlus_CllamaServer.h"
#include "Common_CllamaServer/AIChatPlus_CllamaServerChatRequest.h"
```

##Serververwaltung

###Server starten (Grundlagen)

```cpp
#include "Common_CllamaServer/AIChatPlus_CllamaServer.h"

UPROPERTY()
UAIChatPlus_CllamaServer* LocalServer = nullptr;

void UMyClass::StartCllamaServer()
{
    // Serverparameter konfigurieren
    FAIChatPlus_CllamaServerParam Params;
    Params.Model = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
Params.NGpuLayers = -1;      // -1 = Automatische Zuweisung der GPU-Schichten
Params.Port = 0;             // 0 = automatisch verfügbaren Port zuweisen
    Params.Host = TEXT("127.0.0.1");

    // Erstelle und starte den Server
    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params);

    // Bindung des Serverstart-Rückrufs
    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnServerStarted);
    LocalServer->OnStoppedListeners.AddDynamic(this, &UMyClass::OnServerStopped);
    LocalServer->OnFailedListeners.AddDynamic(this, &UMyClass::OnServerFailed);

// Server aktivieren (Startprozess einleiten)
    LocalServer->Activate();
}

void UMyClass::OnServerStarted(FGuid ServerID)
{
    // Serverinformationen abrufen
    FAIChatPlus_CllamaServerInfo Info;
    if (LocalServer->GetServerInfo(Info))
    {
        UE_LOG(LogTemp, Display, TEXT("Server started at: %s"), *Info.HttpAddress);
        UE_LOG(LogTemp, Display, TEXT("Port: %d"), Info.Port);
    }
}

void UMyClass::OnServerStopped(FGuid ServerID)
{
    UE_LOG(LogTemp, Display, TEXT("Server stopped: %s"), *ServerID.ToString());
}

void UMyClass::OnServerFailed(FGuid ServerID, const FString& ErrorMessage)
{
    UE_LOG(LogTemp, Error, TEXT("Server failed: %s"), *ErrorMessage);
}
```

###Verwendung von Handler zur Verwaltung des Servers

```cpp
#include "Common_CllamaServer/AIChatPlus_CllamaServer.h"
#include "Common_CllamaServer/AIChatPlus_CllamaServerHandler.h"

void UMyClass::StartServerWithHandler()
{
    FAIChatPlus_CllamaServerParam Params;
    Params.Model = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Params.NGpuLayers = 99;
    Params.Port = 8080;

// Handler erstellen
    auto ServerHandler = UAIChatPlus_CllamaServerHandler::CreateHandler();

// Native Callback binden (nicht Dynamic)
    ServerHandler->OnStarted.AddLambda([](FGuid ServerID)
    {
        UE_LOG(LogTemp, Display, TEXT("Server started: %s"), *ServerID.ToString());
    });

    ServerHandler->OnStopped.AddLambda([](FGuid ServerID)
    {
        UE_LOG(LogTemp, Display, TEXT("Server stopped: %s"), *ServerID.ToString());
    });

    ServerHandler->OnFailed.AddLambda([](FGuid ServerID, const FString& Error)
    {
        UE_LOG(LogTemp, Error, TEXT("Server failed: %s - %s"), *ServerID.ToString(), *Error);
    });

    // Server mit Handler erstellen
    LocalServer = UAIChatPlus_CllamaServer::CreateServerWithHandler(Params, ServerHandler);
    LocalServer->Activate();
}
```

###Angegebene Server-ID

```cpp
void UMyClass::StartServerWithCustomID()
{
    FAIChatPlus_CllamaServerParam Params;
    Params.Model = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Params.NGpuLayers = 99;

    // Benutzerdefinierte Server-ID angeben (für spätere Verwaltung über die ID)
    FGuid CustomServerID = FGuid::NewGuid();

    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params, CustomServerID);

    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnServerStarted);
    LocalServer->Activate();
}
```

###Server beenden

```cpp
void UMyClass::StopServer()
{
    if (LocalServer)
    {
        LocalServer->StopServer();
    }
}

// Server anhand der ID stoppen
void UMyClass::StopServerByID(const FGuid& ServerID)
{
    UAIChatPlus_CllamaServer::StopServerByID(ServerID);
}

// Alle Server stoppen
void UMyClass::StopAllServers()
{
    UAIChatPlus_CllamaServer::StopAllServers();
}
```

###Serverstatus abfragen

```cpp
void UMyClass::CheckServerStatus()
{
    // Aktuelle Serverinstanz überprüfen
    if (LocalServer && LocalServer->IsRunning())
    {
        FString Host = LocalServer->GetHost();
        int32 Port = LocalServer->GetPort();
        FString Address = LocalServer->GetAddress();

        UE_LOG(LogTemp, Display, TEXT("Server running at: %s:%d"), *Host, Port);
    }

// Serverstatus anhand der ID überprüfen
    FGuid ServerID = LocalServer->GetServerID();
    if (UAIChatPlus_CllamaServer::IsServerRunning(ServerID))
    {
        FAIChatPlus_CllamaServerInfo Info = UAIChatPlus_CllamaServer::GetServerInfoByID(ServerID);
        UE_LOG(LogTemp, Display, TEXT("Server info: %s"), *Info.HttpAddress);
    }
}

void UMyClass::ListAllServers()
{
    TArray<FGuid> AllServerIDs = UAIChatPlus_CllamaServer::GetAllServerIDs();

    for (const FGuid& ServerID : AllServerIDs)
    {
        FAIChatPlus_CllamaServerInfo Info = UAIChatPlus_CllamaServer::GetServerInfoByID(ServerID);
        UE_LOG(LogTemp, Display, TEXT("Server: %s - Running: %s"),
            *ServerID.ToString(),
            Info.bIsRunning ? TEXT("Yes") : TEXT("No"));
    }
}
```

##Text-Chat

###Grundlegender Textchat

```cpp
#include "Common_CllamaServer/AIChatPlus_CllamaServerChatRequest.h"

void UMyClass::SendCllamaServerChatRequest()
{
// Stelle sicher, dass der Server gestartet ist
    if (!LocalServer || !LocalServer->IsRunning())
    {
        UE_LOG(LogTemp, Error, TEXT("Server is not running"));
        return;
    }

    // Konfiguriere die Anfrageoptionen (geerbt vom OpenAI-Stil)
    FAIChatPlus_CllamaServerChatRequestOptions Options;
    Options.BaseUrl = LocalServer->GetAddress();  // Beispielsweise "http://127.0.0.1:8080"
Options.Model = TEXT("local-model");          // Modellname (kann benutzerdefiniert werden)
    Options.bStream = true;
    Options.Temperature = 0.8f;

// Nachricht erstellen
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is the meaning of life?"), EAIChatPlus_ChatRole::User});

// Anfrage erstellen
    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    // Rückruf binden
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("CllamaServer: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);
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

###Mehrrunden-Dialog

```cpp
// Mitgliedsvariablen
TArray<FAIChatPlus_ChatRequestMessage> CllamaServerConversation;

void UMyClass::InitializeCllamaServerChat()
{
    CllamaServerConversation.Empty();
    CllamaServerConversation.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}

void UMyClass::SendMessage(const FString& UserMessage)
{
    CllamaServerConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    FAIChatPlus_CllamaServerChatRequestOptions Options;
    Options.BaseUrl = LocalServer->GetAddress();
    Options.bStream = true;

    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(
        Options, CllamaServerConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);
        FString AssistantMessage = Response.GetMessage();
        CllamaServerConversation.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});

        UE_LOG(LogTemp, Display, TEXT("Assistant: %s"), *AssistantMessage);
    });

    Request->SendRequest();
}
```

##Vision (Bildanalyse)

Die Verwendung von Vision erfordert die Angabe des MMProject-Modells beim Starten des Servers.

###Vision-fähigen Server starten

```cpp
void UMyClass::StartVisionServer()
{
    FAIChatPlus_CllamaServerParam Params;

// LLaVA-Modell
    Params.Model = TEXT("D:/Models/llava-v1.6-mistral-7b.Q4_K_M.gguf");
Params.MMProj = TEXT("D:/Models/mmproj-llava-v1.6-mistral-7b-f16.gguf");  // Wichtig: MMProj-Modell

    Params.NGpuLayers = 99;
    Params.Port = 8080;

    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params);
    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnVisionServerStarted);
    LocalServer->Activate();
}
```

###Bildanalyseanfrage senden

```cpp
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithCllamaServer()
{
    if (!LocalServer || !LocalServer->IsRunning())
    {
        UE_LOG(LogTemp, Error, TEXT("Vision server is not running"));
        return;
    }

    // Bild laden
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image"));
        return;
    }

    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

// Anfrage konfigurieren
    FAIChatPlus_CllamaServerChatRequestOptions Options;
    Options.BaseUrl = LocalServer->GetAddress();
    Options.bStream = true;

    // Erstellen einer Nachricht mit Bild
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("What do you see in this image?");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(
        Options, {ImageMessage});

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Vision: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##Tool-Aufruf (Funktionsaufruf)

CllamaServer unterstützt OpenAI-ähnliche Tool Calls (erfordert ein Modell mit Funktion-calling-Unterstützung).

###Starten Sie einen Server mit Tool-Call-Unterstützung

```cpp
void UMyClass::StartToolCallServer()
{
    FAIChatPlus_CllamaServerParam Params;
    Params.Model = TEXT("D:/Models/llama-3.1-8b-instruct-q4_k_m.gguf");
    Params.NGpuLayers = 99;
    Params.Port = 8080;
Params.bUseJinja = true;  // Für Tool Call muss die Jinja-Vorlage aktiviert sein

    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params);
    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnToolCallServerStarted);
    LocalServer->Activate();
}
```

###Definition und Nutzung von Werkzeugen

```cpp
void UMyClass::SendToolCallRequest()
{
    if (!LocalServer || !LocalServer->IsRunning())
    {
        UE_LOG(LogTemp, Error, TEXT("Tool call server is not running"));
        return;
    }

    FAIChatPlus_CllamaServerChatRequestOptions Options;
    Options.BaseUrl = LocalServer->GetAddress();
    Options.bStream = false;  // Tool Call empfiehlt die Deaktivierung des Streamings

// Werkzeuge definieren
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = TEXT("function");
    WeatherTool.Function.Name = TEXT("get_weather");
    WeatherTool.Function.Description = TEXT("Get the current weather for a location");
    WeatherTool.Function.Parameters = TEXT(R"({
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit"
            }
        },
        "required": ["location"]
    })");

    Options.Tools.Add(WeatherTool);

    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is the weather like in Tokyo?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);

// Prüfen, ob ein Werkzeug aufgerufen wurde
        if (Response.Choices.Num() > 0)
        {
            const auto& Choice = Response.Choices[0];
            const auto& ToolCalls = Choice.Message.ToolCalls;

            if (ToolCalls.Num() > 0)
            {
                for (const auto& ToolCall : ToolCalls)
                {
                    UE_LOG(LogTemp, Display, TEXT("Tool Call: %s(%s)"),
                        *ToolCall.Function.Name, *ToolCall.Function.Arguments);

// Führe den Werkzeugaufruf aus und setze die Unterhaltung fort
                    ExecuteToolCall(ToolCall);
                }
            }
            else
            {
                UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
            }
        }
    });

    Request->SendRequest();
}
```

###Vollständiger Tool Call-Zyklus

```cpp
TArray<FAIChatPlus_ChatRequestMessage> ToolCallConversation;
FAIChatPlus_CllamaServerChatRequestOptions ToolCallOptions;

void UMyClass::InitializeToolCallChat()
{
    ToolCallOptions.BaseUrl = LocalServer->GetAddress();
    ToolCallOptions.bStream = false;

// Werkzeuge definieren
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = TEXT("function");
    WeatherTool.Function.Name = TEXT("get_weather");
    WeatherTool.Function.Description = TEXT("Get the current weather");
    WeatherTool.Function.Parameters = TEXT(R"({
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City name"}
        },
        "required": ["location"]
    })");
    ToolCallOptions.Tools.Add(WeatherTool);

    ToolCallConversation.Empty();
    ToolCallConversation.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}

void UMyClass::SendToolCallMessage(const FString& UserMessage)
{
    ToolCallConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(
        ToolCallOptions, ToolCallConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.Choices.Num() > 0)
        {
            const auto& Choice = Response.Choices[0];
            const auto& ToolCalls = Choice.Message.ToolCalls;

            if (ToolCalls.Num() > 0)
            {
// 1. Füge die Anfrage zur Tool-Nutzung des Assistenten zur Historie hinzu
                FAIChatPlus_ChatRequestMessage AssistantMessage;
                AssistantMessage.Role = EAIChatPlus_ChatRole::Assistant;
                AssistantMessage.ToolCallUses = ToolCalls;
                ToolCallConversation.Add(AssistantMessage);

// 2. Werkzeug ausführen und Ergebnis hinzufügen
                for (const auto& ToolCall : ToolCalls)
                {
                    FString Result = ExecuteToolFunction(ToolCall.Function.Name, ToolCall.Function.Arguments);

                    FAIChatPlus_ChatRequestMessage ToolResultMessage;
                    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;
                    ToolResultMessage.Content = Result;
                    ToolResultMessage.ToolCallId = ToolCall.Id;
                    ToolCallConversation.Add(ToolResultMessage);
                }

                // 3. Setze das Gespräch fort und lasse das Modell die Werkzeugegebnisse verarbeiten
                ContinueToolCallConversation();
            }
            else
            {
// Normale Antwort
                FString AssistantResponse = Response.GetMessage();
                ToolCallConversation.Add({AssistantResponse, EAIChatPlus_ChatRole::Assistant});
                UE_LOG(LogTemp, Display, TEXT("Final: %s"), *AssistantResponse);
            }
        }
    });

    Request->SendRequest();
}

FString UMyClass::ExecuteToolFunction(const FString& FunctionName, const FString& Arguments)
{
    if (FunctionName == TEXT("get_weather"))
    {
// Parameter analysieren und das Ergebnis zurückgeben
        return TEXT("{\"temperature\": \"22\", \"condition\": \"sunny\", \"unit\": \"celsius\"}");
    }
    return TEXT("{\"error\": \"Unknown function\"}");
}

void UMyClass::ContinueToolCallConversation()
{
    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(
        ToolCallOptions, ToolCallConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);
        FString FinalResponse = Response.GetMessage();
        ToolCallConversation.Add({FinalResponse, EAIChatPlus_ChatRole::Assistant});

        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *FinalResponse);
    });

    Request->SendRequest();
}
```

##Server Erweiterte Konfiguration

###Vollständiges Konfigurationsbeispiel

```cpp
void UMyClass::StartAdvancedServer()
{
    FAIChatPlus_CllamaServerParam Params;

// ===== Modellkonfiguration =====
    Params.Model = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
Params.Alias = TEXT("my-local-model");    // Modellalias
Params.MMProj = TEXT("");                 // Pfad zum Vision MMProject-Modell

// ===== Hardware-Konfiguration =====
Params.NGpuLayers = 99;      // Anzahl der GPU-Schichten (-1 = automatisch)
    Params.Threads = -1;         // Anzahl der CPU-Threads (-1 = automatisch)
Params.ThreadsBatch = -1;    // Stapelverarbeitungs-Threadanzahl

// ===== Kontextkonfiguration =====
    Params.CtxSize = 4096;       // Größe des Kontextfensters
    Params.NPredict = -1;        // Maximale Anzahl generierter Tokens (-1 = unbegrenzt)
Params.BatchSize = 2048;     // Logische Batch-Größe
Params.UbatchSize = 512;     // Physikalische Batch-Größe
Params.Keep = 0;             // Anzahl der beizubehaltenden initialen Tokens

    // ===== Abtastkonfiguration =====
    Params.Temperature = 0.8f;
    Params.TopK = 40;
    Params.TopP = 0.9f;
    Params.MinP = 0.1f;
    Params.RepeatLastN = 64;
    Params.RepeatPenalty = 1.0f;
    Params.PresencePenalty = 0.0f;
    Params.FrequencyPenalty = 0.0f;
    Params.Seed = 0xFFFFFFFF;    // Zufälliger Seed (0xFFFFFFFF = zufällig)

// ===== Serverkonfiguration =====
    Params.Host = TEXT("127.0.0.1");
Params.Port = 8080;          // 0 = automatische Zuweisung
Params.Timeout = 600;        // Timeout (Sekunden)
    Params.Parallel = 1;         // Anzahl paralleler Anfragen
    Params.bContBatching = true; // Kontinuierliche Stapelverarbeitung
    Params.bSlots = true;        // Aktiviert den Slots-Überwachungsendpunkt

// ===== Funktionskonfiguration =====
Params.bUseJinja = true;     // Jinja-Vorlage verwenden (für Tool Call erforderlich)
    Params.bNoWebUI = false;     // Web-UI deaktivieren
Params.ApiKey = TEXT("");    // API-Schlüssel Authentifizierung
    Params.ChatTemplate = TEXT("");  // Benutzerdefinierte Chatvorlage

    // ===== Debug-Konfiguration =====
Params.bVerbose = true;      // Detaillierte Protokollierung

    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params);
    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnServerStarted);
    LocalServer->Activate();
}
```

##Fehlerbehandlung

```cpp
void UMyClass::RobustCllamaServerRequest()
{
// Überprüfen des Serverstatus
    if (!LocalServer)
    {
        UE_LOG(LogTemp, Error, TEXT("Server instance is null"));
        return;
    }

    if (!LocalServer->IsRunning())
    {
        UE_LOG(LogTemp, Error, TEXT("Server is not running"));
        return;
    }

    FAIChatPlus_CllamaServerChatRequestOptions Options;
    Options.BaseUrl = LocalServer->GetAddress();
    Options.bStream = true;

    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->OnStartedListeners.AddLambda([]()
    {
        UE_LOG(LogTemp, Display, TEXT("Request started"));
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaServerChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.HasError())
        {
            UE_LOG(LogTemp, Error, TEXT("Response error: %s"), *Response.Error.GetDescription());
            return;
        }

        UE_LOG(LogTemp, Display, TEXT("Success: %s"), *Response.GetMessage());
    });

    Request->OnFailedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ErrorWrapper)
    {
        auto& Error = *ErrorWrapper.CastTo<FAIChatPlus_ResponseErrorBase>();
        UE_LOG(LogTemp, Error, TEXT("Request failed: %s"), *Error.GetDescription());
    });

    Request->SendRequest();
}
```

##Bereinigung von Ressourcen

```cpp
void UMyClass::CleanupCllamaServer()
{
// Alle Anfragen stoppen
    // ...

// Server stoppen
    if (LocalServer)
    {
        LocalServer->StopServer();
        LocalServer = nullptr;
    }

    // Oder stoppen Sie alle Server
    UAIChatPlus_CllamaServer::StopAllServers();
}

// Bereinigung bei der Zerstörung des Actors
void AMyActor::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    CleanupCllamaServer();
    Super::EndPlay(EndPlayReason);
}
```

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte nutzen Sie [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Auf etwaige Auslassungen hinweisen. 
