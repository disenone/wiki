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

#C++ Chapitre - Gemini

Ce document explique comment utiliser l'API Google Gemini en C++ pour discuter, analyser des images et effectuer des appels d'outils.

##Préparation

Avant utilisation, assurez-vous que :

1. Ajoutez les dépendances de module dans le fichier `.Build.cs` du projet :

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

2. Inclure les fichiers d'en-tête nécessaires :

```cpp
#include "Common_Gemini/AIChatPlus_GeminiChatRequest.h"
```

##Chat textuel

###Chat de base en texte

```cpp
#include "Common_Gemini/AIChatPlus_GeminiChatRequest.h"

void UMyClass::SendGeminiChatRequest()
{
// Configuration des Options
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-google-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;  // Activer la sortie en flux
    Options.MaxOutputTokens = 1024;
    Options.Temperature = 0.7f;

    // Le System Prompt de Gemini est configuré via Options.System
    Options.System = TEXT("You are a helpful assistant.");

// Créer un message utilisateur
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("What is the capital of Japan?"), EAIChatPlus_ChatRole::User});

// Créer une requête
    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    // Liaison du rappel
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

// Envoyer la requête
    Request->SendRequest();
}
```

###Dialogues multiphases

```cpp
void UMyClass::MultiTurnGeminiChat()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant with a good memory.");

// Construire l'historique du dialogue multi-tour
// Gemini utilise "user" et "model" comme rôles
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("My name is Alice."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("Hello Alice! Nice to meet you. How can I help you today?"), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my name?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);
// Le modèle devrait se souvenir que le nom de l'utilisateur est Alice
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##Vision (Analyse d'image)

Le modèle Gemini prend en charge la fonction Vision, qui permet d'analyser le contenu des images.

> **Remarque** : Gemini Vision prend en charge jusqu'à 20 images (`FAIChatPlus_Constants::FGemini::MaxSendImageNum = 20`).

###Charger et analyser une image à partir d'un fichier

```cpp
#include "Common_Gemini/AIChatPlus_GeminiChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithGemini()
{
// Charger une image à partir d'un fichier
    FString ImagePath = FPaths::ProjectContentDir() / TEXT("Images/sample.png");
    UTexture2D* Texture = UAIChatPlus_Util::LoadImage(ImagePath);

    if (!Texture)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load image: %s"), *ImagePath);
        return;
    }

// Créer un objet Texture utilisable par le plugin
    UAIChatPlus_Texture* ChatTexture = UAIChatPlus_Texture::CreateFromTexture2D(Texture);

    // Configurer les Options
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
Options.Model = TEXTE("gemini-1.5-flash");  // ou gemini-1.5-pro
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant that can analyze images.");

// Créer un message avec une image
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

###Analyse d'images multiples

```cpp
void UMyClass::AnalyzeMultipleImagesWithGemini()
{
// Charger plusieurs images
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

// Créer un message avec plusieurs images
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

##Appel d'outil (appel de fonction)

Gemini prend en charge l'appel d'outils (Function Calling), ce qui permet au modèle d'invoquer des fonctions prédéfinies.

###Définir l'outil et envoyer la requête

```cpp
void UMyClass::SendGeminiToolCallRequest()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant. Use tools when needed.");

// Définir l'outil : obtenir la météo
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");

// Définition des paramètres de l'outil
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

###Traitement des résultats de l'appel d'outil

```cpp
void UMyClass::HandleGeminiToolCallResult()
{
    // Supposons que ce soit les informations d'appel d'outil renvoyées par le modèle
    FString ToolCallId = TEXT("call_abc123");
    FString FunctionName = TEXT("get_weather");
    FString FunctionResult = TEXT("{\"temperature\": 25, \"unit\": \"celsius\", \"description\": \"Sunny\"}");

    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");
    Options.bStream = true;

// Redéfinir les outils
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");
    Options.Tools.Add(WeatherTool);

// Construire l'historique des messages
    TArray<FAIChatPlus_ChatRequestMessage> Messages;

    // 1. Question originale de l'utilisateur
    Messages.Add({TEXT("What's the weather like in Tokyo?"), EAIChatPlus_ChatRole::User});

// 2. Requête d'appel d'outil de l'Assistant
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

// 3. Résultats d'exécution de l'outil
    FAIChatPlus_ChatRequestMessage ToolResultMessage;
    ToolResultMessage.Role = EAIChatPlus_ChatRole::Tool;

    FAIChatPlus_ChatRequestToolCallResult ToolResult;
    ToolResult.Id = ToolCallId;
    ToolResult.FunctionName = FunctionName;
    ToolResult.FunctionResult = FunctionResult;
    ToolResultMessage.ToolCallResults.Add(ToolResult);
    Messages.Add(ToolResultMessage);

// Envoyer la requête
    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_GeminiChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###Le cycle complet d'appel d'outil

```cpp
// Stocker l'historique des conversations
TArray<FAIChatPlus_ChatRequestMessage> GeminiConversation;
FAIChatPlus_GeminiChatRequestOptions GeminiOptions;

void UMyClass::InitializeGeminiToolChat()
{
    GeminiOptions.ApiKey = TEXT("your-api-key");
    GeminiOptions.Model = TEXT("gemini-1.5-flash");
    GeminiOptions.bStream = true;
    GeminiOptions.System = TEXT("You are a helpful assistant. Use tools when needed.");

// Définition des outils
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

    // Effacer l'historique de la conversation
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
// Ajouter un message d'appel d'outil pour l'Assistant
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

// Exécuter l'outil et ajouter les résultats
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

// Continuer la conversation
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
        // Exécution réelle de la requête météo
        return TEXT("{\"temperature\": 25, \"unit\": \"celsius\", \"description\": \"Sunny\"}");
    }

    return TEXT("{\"error\": \"Unknown tool\"}");
}

void UMyClass::OnGeminiResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Gemini: %s"), *Response);
}
```

##Configuration avancée

###Utiliser les options d'extension JSON

```cpp
void UMyClass::UseGeminiExtraOptions()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");

// Ajouter des options JSON supplémentaires
    Options.ExtraJsonString = TEXT("{\"safetySettings\": [{\"category\": \"HARM_CATEGORY_HARASSMENT\", \"threshold\": \"BLOCK_NONE\"}]}");

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###URL de point de terminaison personnalisée

```cpp
void UMyClass::UseCustomGeminiEndpoint()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-flash");

// Utiliser un point de terminaison personnalisé (tel qu'un serveur proxy)
    Options.BaseUrl = TEXT("https://your-proxy-server.com/v1beta/models");
Options.Method = TEXT("generateContent");  // Ou streamGenerateContent

    // Ou définissez directement l'URL complète
    // Options.FullUrl = TEXT("https://your-proxy-server.com/v1beta/models/gemini-1.5-flash:generateContent?key=xxx");

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###Configuration des paramètres d'échantillonnage

```cpp
void UMyClass::ConfigureGeminiSampling()
{
    FAIChatPlus_GeminiChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("gemini-1.5-pro");

    // Paramètres d'échantillonnage
    Options.Temperature = 0.3f;  // Température basse pour une sortie plus déterministe
Options.TopK = 40;           // Échantillonnage Top-K
Options.TopP = 0.95f;        // Échantillonnage Nucléus
    Options.MaxOutputTokens = 2048;

    // Séquence d'arrêt
    Options.StopSequences.Add(TEXT("\n\n"));
    Options.StopSequences.Add(TEXT("END"));

    auto Request = UAIChatPlus_GeminiChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a short story."), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

##Gestion des erreurs

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

// Vérifier le FinishReason
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

##Demande d'arrêt

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

--8<-- "footer_fr.md"


> Ce poste est traduit par ChatGPT, veuillez nous faire part de vos commentaires sur [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)signaler toute omission relevée. 
