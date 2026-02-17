---
layout: post
title: Cllama (obsolète)
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

#C++ Section - Cllama (obsolète)

##Abandonné

Cllama a été marqué comme **obsolète** et n'est plus maintenu.

Les fonctionnalités originales de Cllama sont assurées par [CllamaServer](ue-插件-AIChatPlus-Usage-Source-CllamaServer.md)Pour supporter.

##Modèle hors ligne

Ce document explique comment utiliser Cllama (intégrant llama.cpp) pour l'inférence locale hors ligne en C++.

Cllama permet d'exécuter des modèles de langage volumineux sans connexion Internet, idéal pour les scénarios nécessitant une inférence hors ligne ou la protection de la vie privée.

##Préparatifs

Avant utilisation, assurez-vous que :

1. **Téléchargez le fichier de modèle GGUF** : Depuis [Hugging Face](https://huggingface.co)Téléchargez le fichier de modèle au format GGUF compatible.

2. Dans le fichier `.Build.cs` du projet, ajoutez les dépendances de module :

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

3. Inclusion des fichiers d'en-tête nécessaires :

```cpp
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"
```

##Vérification de la disponibilité de Cllama

Avant de l'utiliser, vous pouvez vérifier si Cllama est disponible et quels sont les backends pris en charge :

```cpp
#include "Common/AIChatPlus_Util.h"

void UMyClass::CheckCllamaSupport()
{
// Vérifier si Cllama est disponible
    if (UAIChatPlus_Util::Cllama_IsValid())
    {
        UE_LOG(LogTemp, Display, TEXT("Cllama is available"));

// Vérifier si la prise en charge GPU est disponible
        if (UAIChatPlus_Util::Cllama_IsSupportGpu())
        {
            UE_LOG(LogTemp, Display, TEXT("GPU acceleration is supported"));
        }

        // Obtenir la liste des backends pris en charge
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

##Chat texte

###Chat de texte de base

```cpp
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"

void UMyClass::SendCllamaChatRequest()
{
// Configurer les Options
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
Options.bStream = true;  // Activer la sortie en flux
    Options.Temperature = 0.8f;
Options.NumGpuLayers = 99 ; // Nombre de couches accélérées par GPU (0 = CPU uniquement)

// Créer un message
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
    Messages.Add({TEXT("What is the meaning of life?"), EAIChatPlus_ChatRole::User});

// Créer une requête
    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// Liaison du rappel
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

// Envoyer la demande
    Request->SendRequest();
}
```

###Utiliser des chemins relatifs (par rapport au répertoire Content)

```cpp
void UMyClass::UseRelativeModelPath()
{
    FAIChatPlus_CllamaChatRequestOptions Options;

// Chemin relatif au répertoire Content du projet
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

###Chargement du modèle depuis un fichier Pak

```cpp
void UMyClass::LoadModelFromPak()
{
// Si le modèle est emballé dans un fichier Pak, il faut d'abord préparer le chemin du modèle
    FString ModelPath = TEXT("Models/my_model.gguf");

    // Cette fonction décompresse les modèles du Pak dans un répertoire temporaire et retourne le chemin réel
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

###Dialogue multi-tours

```cpp
void UMyClass::MultiTurnCllamaChat()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;

    // Construire l'historique de dialogue multi-tours
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

###Le modèle reste en cours de chargement

```cpp
void UMyClass::KeepModelLoaded()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;

    // KeepAlive contrôle la durée pendant laquelle le modèle reste chargé après une requête
// 0 = Décharger immédiatement après la demande
// -1 = Garde chargé en permanence
    // >0 = maintient le chargement pendant le nombre de secondes spécifié
Options.KeepAlive = -1;  // Maintenir le chargement de manière permanente

    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("Hello!"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(Options, Messages);
    Request->SendRequest();
}
```

##Vision (Analyse d'image)

Cllama prend en charge la fonction Vision, nécessitant l'utilisation d'un modèle multimodal (comme LLaVA) et la fourniture d'un fichier de modèle MMProject.

> **Remarque** : Cllama Vision prend en charge au maximum 1 image (`FAIChatPlus_Constants::FCllama::MaxSendImageNum = 1`).

###Charger une image à partir d'un fichier et l'analyser

```cpp
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithCllama()
{
// Chargement d'une image à partir d'un fichier
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image: %s"), *ImagePath);
        return;
    }

// Créer un objet Texture utilisable par le plugin
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

// Options de configuration
    FAIChatPlus_CllamaChatRequestOptions Options;

Le modèle LLaVA nécessite deux fichiers : le modèle principal et le modèle MMProject.
    Options.ModelPath.FilePath = TEXT("D:/Models/llava-v1.6-mistral-7b.Q4_K_M.gguf");
    Options.MMProjectModelPath.FilePath = TEXT("D:/Models/mmproj-llava-v1.6-mistral-7b-f16.gguf");

    Options.bStream = true;
    Options.NumGpuLayers = 99;
Options.MMProjectUseGpu = true;  // Le modèle MMProject utilise également le GPU

    // Créer un message avec image
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("What do you see in this image?");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
ImageMessage.Images.Add(ChatTexture);  // Ne peut ajouter qu'une seule image

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

###Analyse d'une image depuis Texture2D

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

##Configuration avancée

###Configuration des paramètres d'échantillonnage

```cpp
void UMyClass::ConfigureCllamaSampling()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;

// Accélération GPU
Options.NumGpuLayers = 99; // Placer autant de couches que possible sur le GPU

// Paramètres d'échantillonnage
Options.Temperature = 0.7f;  // Température
Options.TopK = 40;           // Échantillonnage Top-K
Options.TopP = 0.95f;        // Échantillonnage par noyau
Options.MinP = 0.05f;        // Échantillonnage Min-P

// Échantillonnage Mirostat (pour contrôler la perplexité)
Options.Mirostat = 2;        // 0=désactivé, 1=Mirostat, 2=Mirostat 2.0
    Options.MirostatEta = 0.1f;
    Options.MirostatTau = 5.0f;

// Contexte et limitations de génération
Options.NumCtx = 4096;       // Taille de la fenêtre contextuelle
Options.NumPredict = 256;    // Nombre maximum de tokens générés (-1 = infini)

// Répétition pénalisée
Options.RepeatLastN = 64;    // Vérifie les répétitions sur les N derniers tokens
    Options.RepeatPenalty = 1.1f;

    // échantillonnage libre en fin
Options.TfsZ = 1.0f;         // 1.0 = désactivé

    // Arrêter la séquence
    Options.StopSequences.Add(TEXT("\n\n"));
    Options.StopSequences.Add(TEXT("User:"));

// Graine aléatoire (pour une génération reproductible)
    Options.Seed = 42;

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a short poem."), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###Utiliser un modèle personnalisé

```cpp
void UMyClass::UseCustomTemplate()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/my_model.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;

    // Modèle de prompt personnalisé (remplace le modèle intégré du modèle)
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

##Gestion des erreurs

```cpp
void UMyClass::RobustCllamaRequest()
{
// Vérifier d'abord si Cllama est disponible
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

// Indicateurs de performance
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

##Demande d'arrêt

```cpp
UPROPERTY()
UAIChatPlus_CllamaChatRequest* CurrentCllamaRequest = nullptr;

void UMyClass::StartCllamaRequest()
{
    FAIChatPlus_CllamaChatRequestOptions Options;
    Options.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    Options.bStream = true;
    Options.NumGpuLayers = 99;
Options.NumPredict = -1;  // Génération infinie

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

##Exemple complet de gestion de dialogue

```cpp
// Variables de membre
TArray<FAIChatPlus_ChatRequestMessage> CllamaConversation;
FAIChatPlus_CllamaChatRequestOptions CllamaOptions;

void UMyClass::InitializeCllamaChat()
{
    CllamaOptions.ModelPath.FilePath = TEXT("D:/Models/llama-3.2-1b-instruct-q4_k_m.gguf");
    CllamaOptions.bStream = true;
    CllamaOptions.NumGpuLayers = 99;
    CllamaOptions.KeepAlive = -1;  // Garder le modèle chargé

// Initialisation de la conversation
    CllamaConversation.Empty();
    CllamaConversation.Add({TEXT("You are a helpful assistant."), EAIChatPlus_ChatRole::System});
}

void UMyClass::SendCllamaUserMessage(const FString& UserMessage)
{
    CllamaConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(CllamaOptions, CllamaConversation);

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
// Affichage en temps réel du contenu généré
        UE_LOG(LogTemp, Display, TEXT("Generating: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_CllamaChatRequest::CastWrapperToResponse(ResponseWrapper);

// Ajouter la réponse de l'Assistant à l'historique de la conversation
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

--8<-- "footer_fr.md"


> Ce message a été traduit à l'aide de ChatGPT, veuillez nous faire part de vos commentaires dans la section [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Souligner toute omission. 
