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

#C++ Chapter - Get Started

##Présentation du code source principal

Actuellement, le plugin est divisé en plusieurs modules suivants :

AIChatPlusCommon: Le module d'exécution (Runtime) est chargé de gérer l'envoi des requêtes aux différentes interfaces API d'IA et d'analyser les réponses renvoyées.

AIChatPlusEditor: Module d'édition, responsable de la mise en œuvre de l'outil de chat AI de l'éditeur.

AIChatPlusCllama: Module d'exécution, responsable d'encapsuler les interfaces et les paramètres de llama.cpp, permettant d'exécuter hors ligne de grands modèles.

Thirdparty/LLAMACpp: un module tiers en temps d'exécution, intégrant la bibliothèque dynamique et les fichiers d'en-tête de llama.cpp.

Le UClass responsable spécifique de l'envoi des demandes est FAIChatPlus_xxxChatRequest, chaque service API ayant son propre UClass de demande distinct. Les réponses des demandes sont obtenues via les UClass UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase, il suffit de s'inscrire aux délégués de rappel correspondants.

Avant d'envoyer une demande, il est nécessaire de configurer les paramètres de l'API et le message à envoyer, ceci est réalisé en utilisant FAIChatPlus_xxxChatRequestBody. Les détails de la réponse sont également analysés dans FAIChatPlus_xxxChatResponseBody, où vous pouvez obtenir le ResponseBody via une interface spécifique lors de la réception de l'appel de retour.

##Utilisation du code modèle hors ligne Cllama (llama.cpp)

Voici comment utiliser le modèle hors ligne llama.cpp dans le code.

Tout d'abord, il est nécessaire de télécharger le fichier du modèle dans Content/LLAMA.

Ajouter une instruction au code pour envoyer un message au modèle hors ligne à l'intérieur de cette instruction.

```c++
#include "Common/AIChatPlus_Log.h"
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"

void AddTestCommand()
{
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("AIChatPlus.TestChat"),
		TEXT("Test Chat."),
		FConsoleCommandDelegate::CreateLambda([]()
		{
			if (!FModuleManager::GetModulePtr<FAIChatPlusCommon>(TEXT("AIChatPlusCommon"))) return;

			TWeakObjectPtr<UAIChatPlus_ChatHandlerBase> HandlerObject = UAIChatPlus_ChatHandlerBase::New();
			// Cllama

			FAIChatPlus_CllamaChatRequestOptions Options;

			Options.ModelPath.FilePath = FPaths::ProjectContentDir() / "LLAMA" / "qwen1.5-1_8b-chat-q8_0.gguf";
			Options.NumPredict = 400;
			Options.bStream = true;
			// Options.StopSequences.Emplace(TEXT("json"));
			auto RequestPtr = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(

				Options,
				{
					{"You are a chat bot", EAIChatPlus_ChatRole::System},
					{"who are you", EAIChatPlus_ChatRole::User}
				});

			HandlerObject->BindChatRequest(RequestPtr);
			const FName ApiName = TEnumTraits<EAIChatPlus_ChatApiProvider>::ToName(RequestPtr->GetApiProvider());

			HandlerObject->OnMessage.AddLambda([ApiName](const FString& Message)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] Message: [%s]"), *ApiName.ToString(), *Message);
			});
			HandlerObject->OnStarted.AddLambda([ApiName]()
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestStarted"), *ApiName.ToString());
			});
			HandlerObject->OnFailed.AddLambda([ApiName](const FAIChatPlus_ResponseErrorBase& InError)
			{
				UE_LOG(AIChatPlus_Internal, Error, TEXT("TestChat[%s] RequestFailed: %s "), *ApiName.ToString(), *InError.GetDescription());
			});
			HandlerObject->OnUpdated.AddLambda([ApiName](const FAIChatPlus_ResponseBodyBase& ResponseBody)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestUpdated"), *ApiName.ToString());
			});
			HandlerObject->OnFinished.AddLambda([ApiName](const FAIChatPlus_ResponseBodyBase& ResponseBody)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestFinished"), *ApiName.ToString());
			});

			RequestPtr->SendRequest();
		}),
		ECVF_Default
	);
}
```

Une fois que vous avez recompilé, vous pouvez utiliser la commande dans l'éditeur Cmd pour afficher les résultats de sortie du grand modèle dans le journal OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez fournir votre [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Veuillez signaler tout oubli éventuel. 
