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

#C++ - Pour Commencer

##Présentation du module

Le plugin est divisé en plusieurs modules :

* **AIChatPlusCommon** : Module d'exécution (Runtime), responsable de la gestion des requêtes envoyées via diverses interfaces API d'IA et de l'analyse des réponses.
* **AIChatPlusEditor** : Module éditeur (Editor), responsable de la mise en œuvre de l'outil de discussion IA de l'éditeur.
* **AIChatPlusCllama**: Module d'exécution (Runtime) chargé d'encapsuler les interfaces et paramètres de llama.cpp pour permettre l'exécution locale des grands modèles.
* **Thirdparty/LLAMACpp**: Module tiers pendant l'exécution (Runtime), intégrant la bibliothèque dynamique et les fichiers d'en-tête de llama.cpp.

##Concepts fondamentaux

Avant d'utiliser le code source, il est nécessaire de comprendre quelques classes principales et leurs relations :

###Demande

`UAIChatPlus_ChatRequestBase` est la classe de base pour toutes les requêtes de discussion. Chaque API Provider possède sa sous-classe correspondante :

* `UAIChatPlus_OpenAIChatRequest` - Requête de discussion OpenAI
* `UAIChatPlus_AzureChatRequest` - Demande de discussion Azure
* `UAIChatPlus_ClaudeChatRequest` - Demande de discussion Claude
* `UAIChatPlus_GeminiChatRequest` - Requête de chat Gemini
* `UAIChatPlus_OllamaChatRequest` - Requête de chat Ollama
* `UAIChatPlus_CllamaChatRequest` - Requête du modèle hors ligne Cllama
* `UAIChatPlus_CllamaServerChatRequest` - Requête du serveur local CllamaServer

L'objet Request est responsable de la configuration des paramètres de la requête, de l'envoi de la requête et de la réception des rappels.

###Gestionnaire

`UAIChatPlus_ChatHandlerBase` est une classe de gestionnaire facultative utilisée pour gérer uniformément les rappels des requêtes.

Handler fournit les délégations suivantes :

* `OnStarted` - Déclenché au démarrage de la requête
* `OnMessage` - Déclenché lors de la réception d'un message en continu (sortie en flux continu)
* `OnUpdated` - Déclenché lorsqu'une mise à jour est reçue
* `OnFinished` - Déclenché lorsque la demande est terminée
* `OnFailed` - Déclenché lorsque la requête échoue

**Quand utiliser un Handler ?**

* Lorsqu'il est nécessaire de gérer de manière unifiée la logique de rappel de plusieurs requêtes
* Lorsqu'il est nécessaire de partager une logique de rappel entre les Blueprints et le C++
* Il est également possible d'utiliser directement les délégués de Request (comme `OnStartedListeners`) pour implémenter l'écoute des rappels.

###Options（选项）

Chaque fournisseur d'API possède sa propre structure Options correspondante, utilisée pour configurer les paramètres de l'API :

* `FAIChatPlus_OpenAIChatRequestOptions` - Options OpenAI (ApiKey, Model, Température, etc.)
* `FAIChatPlus_ClaudeChatRequestOptions` - Options Claude
* `FAIChatPlus_GeminiChatRequestOptions` - Options Gemini
* Attends un peu...

Options contient toutes les configurations nécessaires à la connexion de l'API, comme la clé API, l'URL du point de terminaison, le nom du modèle, les paramètres de génération, etc.

###Messages

`FAIChatPlus_ChatRequestMessage` est une structure de message envoyée à l'IA, contenant :

* `Contenu` - Texte du contenu
* `Rôle` - Rôle du message (Système/Utilisateur/Assistant/Développeur/Outil)
* `Images` - Tableau d'images (fonctionnalité Vision)
* `Audios` - Tableau d'audios (Fonctionnalité Audio)
* `ToolCallUses` - Requête d'appel d'outil
* `ToolCallResults` - Résultats d'appel d'outil

###Réponse

Chaque fournisseur d'API possède sa propre structure ResponseBody correspondante :

* `FAIChatPlus_OpenAIChatResponseBody`
* `FAIChatPlus_ClaudeChatResponseBody`
* Attend...

ResponseBody contient toutes les informations renvoyées par l'IA, y compris : le texte du message, l'utilisation des tokens, les appels aux outils, les sorties audio, etc.

##Processus d'utilisation de base (modèle en 5 étapes)

Le processus de base pour envoyer une demande avec AIChatPlus est le suivant :

```cpp
#include "Common_OpenAI/AIChatPlus_OpenAIChatRequest.h"

void SendChatRequest()
{
// ===== Étape 1 : Créer un Handler (facultatif) =====
    // Handler est utilisé pour gérer de manière unifiée les rappels, on peut aussi utiliser directement les délégués de Request
    TWeakObjectPtr<UAIChatPlus_ChatHandlerBase> Handler = UAIChatPlus_ChatHandlerBase::New();

// ===== Étape 2 : Configurer les options =====
    FAIChatPlus_OpenAIChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gpt-4o-mini");
Options.bStream = true;  // Activer la sortie en flux

// ===== Étape 3 : Créer une requête =====
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("Hello, who are you?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_OpenAIChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// ===== Étape 4: Liaison des rappels =====
    // Méthode A : Utilisation d'un Handler
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

// Méthode B : Utilisation directe du délégué de Request (pas besoin de Handler)
    // Request->OnMessageListeners.AddDynamic(this, &UMyClass::OnMessageReceived);
    // Request->OnFinishedListeners.AddDynamic(this, &UMyClass::OnRequestFinished);

// ===== Étape 5 : Envoi de la requête =====
    Request->SendRequest();
}
```

##Écriture simplifiée

Si vous n'avez pas besoin d'un contrôle fin des rappels, vous pouvez utiliser une écriture plus concise :

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

    // Lier directement une Lambda à la Request
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

##Créer une requête via l'énumération API Provider

S'il est nécessaire de sélectionner dynamiquement un fournisseur d'API en fonction de la configuration, vous pouvez utiliser une méthode d'usine :

```cpp
void CreateRequestByProvider(EAIChatPlus_ChatApiProvider Provider)
{
    // Créer une demande correspondante selon l'énumération
    auto Request = UAIChatPlus_ChatRequestBase::CreateByApi(Provider);

    // Définir les Options selon le type réel
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
    // ... Autres Providers
    }

// Définir le message et l'envoyer
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Hello!"), EAIChatPlus_ChatRole::User});
    Request->SetMessages(Messages);
    Request->SendRequest();
}
```

##Note de rappel

###Principaux rappels délégués

| Délégation | Moment de déclenchement | Paramètres |
|------|----------|------|
| `OnStarted` | Lorsque l'envoi de la requête commence | Aucun |
| `OnMessage` | Lors de la réception d'un message en continu (pour chaque jeton) | `const FString& Message` - Contenu accumulé du message |
| `OnUpdated` | Lors de la réception d'une mise à jour de réponse | `const FAIChatPlus_ResponseBodyBase& Response` |
| `OnFinished` | Lorsque la requête est terminée avec succès | `const FAIChatPlus_ResponseBodyBase& Response` |
| `OnFailed` | Lorsque la demande échoue | `const FAIChatPlus_ResponseErrorBase& Error` |
| `OnMessageFinished` | Lorsque la réception du message est terminée | `const FAIChatPlus_MessageFinishedPayload& Payload` |

###Sortie en flux vs Sortie non en flux

* **Flux de sortie** (`bStream = true`) : `OnMessage` se déclenche plusieurs fois, renvoyant à chaque fois le contenu cumulé des messages
* **Sortie non fluxée** (`bStream = false`) : `OnMessage` ne se déclenche qu'une seule fois à la fin, renvoyant le message complet.

##Suivant

Pour plus de détails sur l'utilisation, veuillez consulter les documents spécifiques de chaque fournisseur d'API :

* [Utilisation d'OpenAI / Azure](ue-插件-AIChatPlus-Usage-Source-OpenAI.md)
* [Utilisation de Claude](ue-插件-AIChatPlus-Usage-Source-Claude.md)
* [Utilisation de Gemini](ue-插件-AIChatPlus-Usage-Source-Gemini.md)
* [Utilisation d'Ollama](ue-插件-AIChatPlus-Usage-Source-Ollama.md)
* [Modèle hors ligne Cllama](ue-插件-AIChatPlus-Usage-Source-Cllama.md)
* [Serveur local CllamaServer](ue-插件-AIChatPlus-Usage-Source-CllamaServer.md)
* [Outils](ue-插件-AIChatPlus-Usage-Source-Utils.md)

--8<-- "footer_fr.md"

> Ce message a été traduit à l'aide de ChatGPT. Veuillez donner votre [**retour**](https://github.com/disenone/wiki_blog/issues/new)signaler toute omission constatée. 
