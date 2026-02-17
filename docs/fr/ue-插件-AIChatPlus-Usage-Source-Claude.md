---
layout: post
title: Claude
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
- Claude
- Anthropic
description: Claude
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Claude" />

#C++ Section - Claude

Ce document explique comment utiliser l'API Claude d'Anthropic en C++ pour discuter, analyser des images et effectuer des appels d'outils.

##Préparatifs

Avant utilisation, assurez-vous que :

1. Ajouter les dépendances du module dans le fichier `.Build.cs` du projet :

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "AIChatPlusCommon"
});
```

2. Inclure les fichiers d'en-tête nécessaires :

```cpp
#include "Common_Claude/AIChatPlus_ClaudeChatRequest.h"
```

##Chat texte

###Chat de texte de base

```cpp
#include "Common_Claude/AIChatPlus_ClaudeChatRequest.h"

void UMyClass::SendClaudeChatRequest()
{
// Options de configuration
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-anthropic-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;  // Active la sortie en flux
    Options.MaxOutputTokens = 1024;
    Options.Temperature = 0.7f;

// Le prompt système de Claude est défini via Options.System
    Options.System = TEXT("You are a helpful assistant.");

// Créer un message utilisateur
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("What is the capital of France?"), EAIChatPlus_ChatRole::User});

// Création de la requête
    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, Messages);

// Liaison des rappels
    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Claude: %s"), *Message);
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Token Usage: %s"), *Response.Usage.GetDescription());
        UE_LOG(LogTemp, Display, TEXT("Stop Reason: %s"), *Response.StopReason);
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

###Conversation multi-tours

```cpp
void UMyClass::MultiTurnClaudeChat()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant with a good memory.");

// Construire l'historique du dialogue multi-tours (sans inclure System, le System de Claude se trouve dans Options)
    TArray<FAIChatPlus_ChatRequestMessage> Messages;
    Messages.Add({TEXT("My name is Bob."), EAIChatPlus_ChatRole::User});
    Messages.Add({TEXT("Hello Bob! Nice to meet you. How can I assist you today?"), EAIChatPlus_ChatRole::Assistant});
    Messages.Add({TEXT("What is my name?"), EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);
// Le modèle doit se souvenir que le nom de l'utilisateur est Bob
        UE_LOG(LogTemp, Display, TEXT("Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

##Vision (analyse d'image)

La série Claude 3 des modèles prend en charge la fonction Vision, permettant d'analyser le contenu des images.

> **Note** : Claude Vision prend en charge jusqu'à 20 images (`FAIChatPlus_Constants::FClaude::MaxSendImageNum = 20`).

###Charger une image depuis un fichier et l'analyser

```cpp
#include "Common_Claude/AIChatPlus_ClaudeChatRequest.h"
#include "Common/AIChatPlus_Util.h"

void UMyClass::AnalyzeImageWithClaude()
{
// Charger une image depuis un fichier
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
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
Options.Model = TEXT("claude-3-5-sonnet-20240620");  // Utilisation de la série Claude 3
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant that can analyze images.");

// Créer un message avec image
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("Please describe this image in detail.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images.Add(ChatTexture);

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnMessageListeners.AddLambda([](const FString& Message)
    {
        UE_LOG(LogTemp, Display, TEXT("Claude Vision: %s"), *Message);
    });

    Request->SendRequest();
}
```

###Analyse multi-images

```cpp
void UMyClass::AnalyzeMultipleImages()
{
// Charger plusieurs images
    TArray<UAIChatPlus_Texture*> ChatTextures;

    TArray<FString> ImagePaths = {
        FPaths::ProjectContentDir() / TEXT("Images/image1.png"),
        FPaths::ProjectContentDir() / TEXT("Images/image2.png"),
        FPaths::ProjectContentDir() / TEXT("Images/image3.png")
    };

    for (const FString& Path : ImagePaths)
    {
        if (UTexture2D* Texture = UAIChatPlus_Util::LoadImage(Path))
        {
            ChatTextures.Add(UAIChatPlus_Texture::CreateFromTexture2D(Texture));
        }
    }

    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant.");

// Créer un message avec plusieurs images
    FAIChatPlus_ChatRequestMessage ImageMessage;
    ImageMessage.Content = TEXT("Compare these images and describe the differences.");
    ImageMessage.Role = EAIChatPlus_ChatRole::User;
    ImageMessage.Images = ChatTextures;

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, {ImageMessage});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Comparison: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

## Appel d'outil (fonction d'appel)

Claude prend en charge l'appel d'outils (Tool Calling), permettant au modèle d'invoquer des fonctions prédéfinies.

###Définir l'outil et envoyer la requête

```cpp
void UMyClass::SendClaudeToolCallRequest()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant. Use tools when needed.");

// Définition de l'outil : Obtenir la météo
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");

// Définir les paramètres de l'outil
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

// Optionnel : définir ToolChoice
    // Options.ToolChoice.Type = TEXT("auto");  // auto, any, or tool
    // Options.ToolChoice.Name = TEXT("get_weather");  // À utiliser uniquement lorsque Type == "tool"

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("What's the weather like in Paris?"), EAIChatPlus_ChatRole::User}});

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);

// Vérifie si la raison de l'arrêt est tool_use
        if (Response.StopReason == TEXT("tool_use"))
        {
            TArray<FAIChatPlus_ChatResponseToolCall> ToolCalls = Response.GetToolCalls();
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

###Traiter les résultats de l'appel d'outil

```cpp
void UMyClass::HandleClaudeToolCallResult()
{
    // Supposons que ce sont les informations de Tool Call renvoyées par le modèle
    FString ToolCallId = TEXT("toolu_01abc123");
    FString FunctionName = TEXT("get_weather");
    FString FunctionResult = TEXT("{\"temperature\": 18, \"unit\": \"celsius\", \"description\": \"Cloudy\"}");

    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;
    Options.System = TEXT("You are a helpful assistant. Use tools when needed.");

// Redéfinir les outils
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get the current weather for a specific location.");
    Options.Tools.Add(WeatherTool);

// Construire l'historique des messages
    TArray<FAIChatPlus_ChatRequestMessage> Messages;

// 1. Question originale de l'utilisateur
    Messages.Add({TEXT("What's the weather like in Paris?"), EAIChatPlus_ChatRole::User});

// 2. Requête d'utilisation d'outil par l'Assistant
    FAIChatPlus_ChatRequestMessage AssistantMessage;
    AssistantMessage.Role = EAIChatPlus_ChatRole::Assistant;
    AssistantMessage.Content = TEXT("");

    FAIChatPlus_ChatRequestToolCall ToolCallUse;
    ToolCallUse.Id = ToolCallId;
    ToolCallUse.Type = TEXT("function");
    ToolCallUse.FunctionName = FunctionName;
    ToolCallUse.FunctionArguments = TEXT("{\"location\": \"Paris\"}");
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
    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(Options, Messages);

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);
        UE_LOG(LogTemp, Display, TEXT("Final Response: %s"), *Response.GetMessage());
    });

    Request->SendRequest();
}
```

###Cycle complet d'appel d'outil

```cpp
// Stocker l'historique de la conversation
TArray<FAIChatPlus_ChatRequestMessage> ClaudeConversation;
FAIChatPlus_ClaudeChatRequestOptions ClaudeOptions;

void UMyClass::InitializeClaudeToolChat()
{
    ClaudeOptions.ApiKey = TEXT("your-api-key");
    ClaudeOptions.Model = TEXT("claude-3-5-sonnet-20240620");
    ClaudeOptions.bStream = true;
    ClaudeOptions.System = TEXT("You are a helpful assistant. Use tools to get real-time information.");

// Définir l'outil
    FAIChatPlus_ChatRequestTool WeatherTool;
    WeatherTool.Type = EAIChatPlus_ChatToolType::Function;
    WeatherTool.Name = TEXT("get_weather");
    WeatherTool.Description = TEXT("Get weather for a location.");

    FAIChatPlus_ChatRequestToolProperty Prop;
    Prop.Name = TEXT("location");
    Prop.Type = TEXT("string");
    Prop.Required = true;
    WeatherTool.Properties.Add(Prop);

    ClaudeOptions.Tools.Add(WeatherTool);

// Effacer l'historique des conversations
    ClaudeConversation.Empty();
}

void UMyClass::SendClaudeUserMessage(const FString& UserMessage)
{
    ClaudeConversation.Add({UserMessage, EAIChatPlus_ChatRole::User});

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(ClaudeOptions, ClaudeConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.StopReason == TEXT("tool_use"))
        {
            ProcessClaudeToolCalls(Response.GetToolCalls(), Response.GetMessage());
        }
        else
        {
            FString AssistantMessage = Response.GetMessage();
            ClaudeConversation.Add({AssistantMessage, EAIChatPlus_ChatRole::Assistant});
            OnClaudeResponse(AssistantMessage);
        }
    });

    Request->SendRequest();
}

void UMyClass::ProcessClaudeToolCalls(const TArray<FAIChatPlus_ChatResponseToolCall>& ToolCalls, const FString& AssistantContent)
{
// Ajouter un message d'appel d'outil Assistant
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
    ClaudeConversation.Add(AssistantMsg);

// Exécuter l'outil et ajouter les résultats
    FAIChatPlus_ChatRequestMessage ToolResultMsg;
    ToolResultMsg.Role = EAIChatPlus_ChatRole::Tool;

    for (const auto& ToolCall : ToolCalls)
    {
        FString Result = ExecuteClaudeTool(ToolCall.FunctionName, ToolCall.FunctionArguments);

        FAIChatPlus_ChatRequestToolCallResult ToolResult;
        ToolResult.Id = ToolCall.Id;
        ToolResult.FunctionName = ToolCall.FunctionName;
        ToolResult.FunctionResult = Result;
        ToolResultMsg.ToolCallResults.Add(ToolResult);
    }
    ClaudeConversation.Add(ToolResultMsg);

// Continuer la conversation
    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(ClaudeOptions, ClaudeConversation);

    Request->OnFinishedListeners.AddLambda([this](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.StopReason == TEXT("tool_use"))
        {
            ProcessClaudeToolCalls(Response.GetToolCalls(), Response.GetMessage());
        }
        else
        {
            FString FinalMessage = Response.GetMessage();
            ClaudeConversation.Add({FinalMessage, EAIChatPlus_ChatRole::Assistant});
            OnClaudeResponse(FinalMessage);
        }
    });

    Request->SendRequest();
}

FString UMyClass::ExecuteClaudeTool(const FString& FunctionName, const FString& Arguments)
{
    if (FunctionName == TEXT("get_weather"))
    {
// Exécution réelle de la requête météo
        return TEXT("{\"temperature\": 18, \"unit\": \"celsius\", \"description\": \"Cloudy\"}");
    }

    return TEXT("{\"error\": \"Unknown tool\"}");
}

void UMyClass::OnClaudeResponse(const FString& Response)
{
    UE_LOG(LogTemp, Display, TEXT("Claude: %s"), *Response);
}
```

##Configuration avancée

###Utiliser les options d'extension JSON

```cpp
void UMyClass::UseClaudeExtraOptions()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");

// Ajouter des options JSON supplémentaires
    Options.ExtraJsonString = TEXT("{\"metadata\": {\"user_id\": \"12345\"}}");

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###URL de point de terminaison personnalisée

```cpp
void UMyClass::UseCustomClaudeEndpoint()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");

    // Utilisation de points de terminaison personnalisés (comme un serveur proxy)
    Options.BaseUrl = TEXT("https://your-proxy-server.com");
    Options.EndPointUrl = TEXT("v1/messages");

    // ou définissez directement l'URL complète
    // Options.FullUrl = TEXT("https://your-proxy-server.com/v1/messages");

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

###Configurer la version Anthropic

```cpp
void UMyClass::SetAnthropicVersion()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");

// Définir la version de l'API
    Options.AnthropicVersion = TEXT("2023-06-01");

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->SendRequest();
}
```

##Gestion des erreurs

```cpp
void UMyClass::RobustClaudeRequest()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;

    auto Request = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Hello!"), EAIChatPlus_ChatRole::User}});

    Request->OnStartedListeners.AddLambda([]()
    {
        UE_LOG(LogTemp, Display, TEXT("Claude request started..."));
    });

    Request->OnFinishedListeners.AddLambda([](const FAIChatPlus_PointerWrapper& ResponseWrapper)
    {
        auto& Response = UAIChatPlus_ClaudeChatRequest::CastWrapperToResponse(ResponseWrapper);

        if (Response.HasError())
        {
            UE_LOG(LogTemp, Error, TEXT("Response error: %s"), *Response.Error.GetDescription());
            return;
        }

        UE_LOG(LogTemp, Display, TEXT("Success: %s"), *Response.GetMessage());
        UE_LOG(LogTemp, Display, TEXT("Stop Reason: %s"), *Response.StopReason);
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
UAIChatPlus_ClaudeChatRequest* CurrentClaudeRequest = nullptr;

void UMyClass::StartClaudeRequest()
{
    FAIChatPlus_ClaudeChatRequestOptions Options;
    Options.ApiKey = TEXT("your-api-key");
    Options.Model = TEXT("claude-3-5-sonnet-20240620");
    Options.bStream = true;

    CurrentClaudeRequest = UAIChatPlus_ClaudeChatRequest::CreateWithOptionsAndMessages(
        Options,
        {{TEXT("Write a very long essay about AI."), EAIChatPlus_ChatRole::User}});

    CurrentClaudeRequest->SendRequest();
}

void UMyClass::CancelClaudeRequest()
{
    if (CurrentClaudeRequest && CurrentClaudeRequest->IsActivated())
    {
        CurrentClaudeRequest->StopRequest();
        UE_LOG(LogTemp, Display, TEXT("Claude request cancelled"));
    }
}
```

--8<-- "footer_fr.md"


> Ce message a été traduit à l'aide de ChatGPT, veuillez nous faire part de vos commentaires dans la section [**Retour d'information**](https://github.com/disenone/wiki_blog/issues/new)Signaler toute omission constatée. 
