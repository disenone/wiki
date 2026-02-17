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

#Partie C++ - CllamaServer

Ce document explique comment utiliser CllamaServer en C++ pour gérer un serveur d'IA local et envoyer des requêtes de chat.

CllamaServer fonctionne en mode serveur basé sur llama.cpp, offrant un service local compatible avec l'API OpenAI et prenant en charge les requêtes simultanées de plusieurs clients.

##Différences avec Cllama

| Fonctionnalité | Cllama | CllamaServer |
|------|--------|--------------|
| Mode | Inférence directe | Serveur HTTP |
| Multi-client | Non | Oui |
| Style d'API | Personnalisé | Compatible OpenAI |
| Accès réseau | Non | Optionnel |
| Appel d'Outil | Non | Oui |

##Préparation

Avant utilisation, assurez-vous que :

1. **Télécharger les fichiers de modèle GGUF** : Depuis [Hugging Face](https://huggingface.co)Téléchargez le fichier de modèle au format GGUF compatible.

2. Ajoutez les dépendances de modules dans le fichier `.Build.cs` du projet :

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

3. Inclure les fichiers d'en-tête nécessaires :

```cpp
#include "Common_CllamaServer/AIChatPlus_CllamaServer.h"
#include "Common_CllamaServer/AIChatPlus_CllamaServerChatRequest.h"
```

##Gestion des serveurs

###Démarrer le serveur (base)

```cpp
#include "Common_CllamaServer/AIChatPlus_CllamaServer.h"

UPROPERTY()
UAIChatPlus_CllamaServer* LocalServer = nullptr;

void UMyClass::StartCllamaServer()
{
// Configuration des paramètres du serveur
    FAIChatPlus_CllamaServerParam Params;
    Params.Model = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Params.NGpuLayers = -1;      // -1 = attribution automatique des couches GPU
Params.Port = 0;             // 0 = attribution automatique d'un port disponible
    Params.Host = TEXT("127.0.0.1");

// Créer et démarrer le serveur
    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params);

// Liaison du rappel de démarrage du serveur
    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnServerStarted);
    LocalServer->OnStoppedListeners.AddDynamic(this, &UMyClass::OnServerStopped);
    LocalServer->OnFailedListeners.AddDynamic(this, &UMyClass::OnServerFailed);

// Activation du serveur (début du processus de démarrage)
    LocalServer->Activate();
}

void UMyClass::OnServerStarted(FGuid ServerID)
{
// Obtenir les informations du serveur
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

###Utiliser Handler pour gérer le serveur

```cpp
#include "Common_CllamaServer/AIChatPlus_CllamaServer.h"
#include "Common_CllamaServer/AIChatPlus_CllamaServerHandler.h"

void UMyClass::StartServerWithHandler()
{
    FAIChatPlus_CllamaServerParam Params;
    Params.Model = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Params.NGpuLayers = 99;
    Params.Port = 8080;

// Créer un Handler
    auto ServerHandler = UAIChatPlus_CllamaServerHandler::CreateHandler();

// Liaison du rappel natif (non Dynamic)
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

// Utiliser Handler pour créer un serveur
    LocalServer = UAIChatPlus_CllamaServer::CreateServerWithHandler(Params, ServerHandler);
    LocalServer->Activate();
}
```

###Spécifier l'ID du serveur

```cpp
void UMyClass::StartServerWithCustomID()
{
    FAIChatPlus_CllamaServerParam Params;
    Params.Model = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Params.NGpuLayers = 99;

// Spécifier un ID de serveur personnalisé (pour faciliter la gestion ultérieure via l'ID)
    FGuid CustomServerID = FGuid::NewGuid();

    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params, CustomServerID);

    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnServerStarted);
    LocalServer->Activate();
}
```

###Arrêter le serveur

```cpp
void UMyClass::StopServer()
{
    if (LocalServer)
    {
        LocalServer->StopServer();
    }
}

// Arrêter le serveur par ID
void UMyClass::StopServerByID(const FGuid& ServerID)
{
    UAIChatPlus_CllamaServer::StopServerByID(ServerID);
}

// Arrêter tous les serveurs
void UMyClass::StopAllServers()
{
    UAIChatPlus_CllamaServer::StopAllServers();
}
```

###Vérifier l'état du serveur

```cpp
void UMyClass::CheckServerStatus()
{
    // Vérifier l'instance actuelle du serveur
    if (LocalServer && LocalServer->IsRunning())
    {
        FString Host = LocalServer->GetHost();
        int32 Port = LocalServer->GetPort();
        FString Address = LocalServer->GetAddress();

        UE_LOG(LogTemp, Display, TEXT("Server running at: %s:%d"), *Host, Port);
    }

// Vérifier l'état du serveur par ID
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

##Chat textuel

###Chat de texte de base

```cpp
#include "Common_CllamaServer/AIChatPlus_CllamaServerChatRequest.h"

void UMyClass::SendCllamaServerChatRequest()
{
// Assurez-vous que le serveur est démarré
    if (!LocalServer || !LocalServer->IsRunning())
    {
        UE_LOG(LogTemp, Error, TEXT("Server is not running"));
        return;
    }

    // Configurer les options de requête (héritées du style OpenAI)
    FAIChatPlus_CllamaServerChatRequestOptions Options;
Options.BaseUrl = LocalServer->GetAddress();  // Par exemple "http://127.0.0.1:8080"
Options.Model = TEXT("modèle-local");          // Nom du modèle (personnalisable)
    Options.bStream = true;
    Options.Temperature = 0.8f;

// créer un message
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is the meaning of life?"), EAIChatPlus_ChatRole::User});

// Créer une requête
    auto Request = UAIChatPlus_CllamaServerChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    // Liaison du callback
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

    // Envoyer la requête
    Request->SendRequest();
}
```

###Dialogue multipartite

```cpp
// Variables membres
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

##Vision (Analyse d'image)

L'utilisation de Vision nécessite de spécifier le modèle MMProject lors du démarrage du serveur.

###Démarrer le serveur avec prise en charge de Vision

```cpp
void UMyClass::StartVisionServer()
{
    FAIChatPlus_CllamaServerParam Params;

// Modèle LLaVA
    Params.Model = TEXT("D:/Models/llava-v1.6-mistral-7b.Q4_K_M.gguf");
Params.MMProj = TEXT("D:/Models/mmproj-llava-v1.6-mistral-7b-f16.gguf");  // Clé : Modèle MMProject

    Params.NGpuLayers = 99;
    Params.Port = 8080;

    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params);
    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnVisionServerStarted);
    LocalServer->Activate();
}
```

###Envoyer une demande d'analyse d'image

```cpp
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithCllamaServer()
{
    if (!LocalServer || !LocalServer->IsRunning())
    {
        UE_LOG(LogTemp, Error, TEXT("Vision server is not running"));
        return;
    }

// Charger l'image
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image"));
        return;
    }

    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

// Configurer la requête
    FAIChatPlus_CllamaServerChatRequestOptions Options;
    Options.BaseUrl = LocalServer->GetAddress();
    Options.bStream = true;

// Créer un message avec une image
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

##Appel d'outil (fonction)

CllamaServer prend en charge les appels d'outils de style OpenAI (nécessite un modèle prenant en charge les appels de fonctions).

###Lancer le serveur avec prise en charge des Tool Calls

```cpp
void UMyClass::StartToolCallServer()
{
    FAIChatPlus_CllamaServerParam Params;
    Params.Model = TEXT("D:/Models/llama-3.1-8b-instruct-q4_k_m.gguf");
    Params.NGpuLayers = 99;
    Params.Port = 8080;
Params.bUseJinja = true;  // L'appel d'outil nécessite l'activation du modèle Jinja

    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params);
    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnToolCallServerStarted);
    LocalServer->Activate();
}
```

###Définir et utiliser des outils

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
Options.bStream = false;  // Appel d'outil - Recommandation de désactiver le streaming

    // Définir les outils
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

// Vérifier s'il y a un appel à un outil
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

// Exécuter l'appel d'outil et poursuivre la conversation
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

###Cycle d'appel d'outil complet

```cpp
TArray<FAIChatPlus_ChatRequestMessage> ToolCallConversation;
FAIChatPlus_CllamaServerChatRequestOptions ToolCallOptions;

void UMyClass::InitializeToolCallChat()
{
    ToolCallOptions.BaseUrl = LocalServer->GetAddress();
    ToolCallOptions.bStream = false;

// Définir l'outil
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
// 1. Ajouter la demande d'appel d'outil de l'Assistant à l'historique
                FAIChatPlus_ChatRequestMessage AssistantMessage;
                AssistantMessage.Role = EAIChatPlus_ChatRole::Assistant;
                AssistantMessage.ToolCallUses = ToolCalls;
                ToolCallConversation.Add(AssistantMessage);

// 2. Exécuter l'outil et ajouter les résultats
                for (const auto& ToolCall : ToolCalls)
                {
                    FString Result = ExecuteToolFunction(ToolCall.Function.Name, ToolCall.Function.Arguments);

                    FAIChatPlus_ChatRequestMessage ToolResultMessage;
                    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;
                    ToolResultMessage.Content = Result;
                    ToolResultMessage.ToolCallId = ToolCall.Id;
                    ToolCallConversation.Add(ToolResultMessage);
                }

// 3. Continuer la conversation pour que le modèle traite les résultats des outils
                ContinueToolCallConversation();
            }
            else
            {
// Réponse normale
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
// Analyser les paramètres et renvoyer le résultat
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

##Configuration avancée du serveur

###Exemple complet de configuration

```cpp
void UMyClass::StartAdvancedServer()
{
    FAIChatPlus_CllamaServerParam Params;

// ===== Configuration du modèle =====
    Params.Model = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
Params.Alias = TEXT("mon-modèle-local");    // Alias du modèle
    Params.MMProj = TEXT("");                 // Chemin du modèle Vision MMProject

// ===== Configuration matérielle =====
    Params.NGpuLayers = 99;      // Nombre de couches GPU (-1 = automatique)
    Params.Threads = -1;         // Nombre de threads CPU (-1 = automatique)
Params.ThreadsBatch = -1;    // Nombre de threads pour le traitement par lots

// ===== Configuration du contexte =====
Params.CtxSize = 4096;       // Taille de la fenêtre contextuelle
    Params.NPredict = -1;        // Nombre maximum de tokens générés (-1 = infini)
Params.BatchSize = 2048;     // Taille de lot logique
Params.UbatchSize = 512;     // Taille de lot physique
Params.Keep = 0;             // Nombre initial de jetons à conserver

// ===== Configuration d'échantillonnage =====
    Params.Temperature = 0.8f;
    Params.TopK = 40;
    Params.TopP = 0.9f;
    Params.MinP = 0.1f;
    Params.RepeatLastN = 64;
    Params.RepeatPenalty = 1.0f;
    Params.PresencePenalty = 0.0f;
    Params.FrequencyPenalty = 0.0f;
Params.Seed = 0xFFFFFFFF;    // Graine aléatoire (0xFFFFFFFF = aléatoire)

// ===== Configuration du serveur =====
    Params.Host = TEXT("127.0.0.1");
Params.Port = 8080;          // 0 = allocation automatique
Params.Timeout = 600;        // Délai d'attente (secondes)
Params.Parallel = 1;         // Nombre de requêtes parallèles
    Params.bContBatching = true; // Traitement par lots continu
Params.bSlots = true;        // Activer le monitoring des slots d'extrémité

// ===== Configuration des fonctionnalités =====
    Params.bUseJinja = true;     // Utiliser le modèle Jinja (nécessaire pour Tool Call)
Params.bNoWebUI = false;     // Désactiver l'interface Web
Params.ApiKey = TEXT("");    // Clé API pour l'authentification
Params.ChatTemplate = TEXT("");  // Modèle de chat personnalisé

// ===== Configuration du débogage =====
Params.bVerbose = true;      // Journal détaillé

    LocalServer = UAIChatPlus_CllamaServer::CreateServer(Params);
    LocalServer->OnStartedListeners.AddDynamic(this, &UMyClass::OnServerStarted);
    LocalServer->Activate();
}
```

##Gestion des erreurs

```cpp
void UMyClass::RobustCllamaServerRequest()
{
// Vérifier l'état du serveur
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

##Nettoyer les ressources

```cpp
void UMyClass::CleanupCllamaServer()
{
    // Arrêter toutes les requêtes
    // ...

// Arrêter le serveur
    if (LocalServer)
    {
        LocalServer->StopServer();
        LocalServer = nullptr;
    }

    // ou arrêter tous les serveurs
    UAIChatPlus_CllamaServer::StopAllServers();
}

// Nettoyage lors de la destruction de l'Actor
void AMyActor::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    CleanupCllamaServer();
    Super::EndPlay(EndPlayReason);
}
```

--8<-- "footer_fr.md"


> Ce message a été traduit avec ChatGPT, veuillez donner votre [**avis**](https://github.com/disenone/wiki_blog/issues/new)Pointer toute omission dans le texte. 
