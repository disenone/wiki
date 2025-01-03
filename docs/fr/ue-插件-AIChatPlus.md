---
layout: post
title: Document d'instructions du plug-in UE AIChatPlus
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
description: Documentation du plug-in AIChatPlus de l'UE
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documentation du plugin AIChatPlus de l'UE

##Entrepôt public

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtenir l'extension

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Présentation du module complémentaire

This plugin supports UE5.2+.


UE.AIChatPlus est un plug-in UnrealEngine qui permet la communication avec divers services de chat AI tels que OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama et llama.cpp en mode hors ligne local. À l'avenir, il prendra en charge davantage de fournisseurs de services. Son implémentation repose sur des requêtes REST asynchrones, offrant ainsi une haute performance et facilitant l'intégration de ces services de chat AI pour les développeurs UE.

UE.AIChatPlus includes a tool editor that allows you to use these AI chat services directly in the editor to generate text and images, analyze images, and more.

##Instructions d'utilisation

###Outil de discussion de l'éditeur

Dans la barre de menus, cliquez sur Tools -> AIChatPlus -> AIChat pour ouvrir l'éditeur de chat fourni par le plug-in.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


Le logiciel prend en charge la génération de texte, les conversations textuelles, la génération d'images et l'analyse d'images.

L'interface de l'outil est approximativement la suivante :

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Fonctions principales

Modèle hors ligne : Intégration de la bibliothèque llama.cpp, prenant en charge l'exécution hors ligne locale des grands modèles

Créez une nouvelle session de chat texte en appuyant sur le bouton `Nouveau Chat` situé en bas à gauche.

Génération d'images : appuyez sur le bouton `Nouveau Chat d'Images` dans le coin inférieur gauche pour démarrer une nouvelle session de génération d'images.

Analyse d'image : Certaines fonctionnalités de chat de "New Chat" prennent en charge l'envoi d'images, telles que Claude, Google Gemini. Cliquez sur l'icône 🖼️ ou 🎨 au-dessus de la zone de saisie pour charger l'image que vous souhaitez envoyer.

Soutenir les plans (Blueprint) : Soutenir la création de plans pour les demandes d'API, accomplir des tâches telles que le chat textuel et la génération d'images.

Définir le personnage de chat actuel : Vous pouvez choisir le personnage de chat en utilisant la liste déroulante située en haut de la boîte de chat, afin de simuler différentes identités et ajuster les échanges avec l'IA.

Vider la conversation : Le bouton ❌ en haut de la fenêtre de discussion permet de supprimer l'historique des messages de la conversation en cours.

Modèle de conversation : des centaines de modèles de conversation intégrés pour faciliter le traitement des problèmes courants.

Paramètres généraux : En cliquant sur le bouton `Paramètres` situé en bas à gauche, vous pouvez ouvrir la fenêtre des paramètres généraux. Vous pourrez définir le chat texte par défaut, le service API de génération d'images, ainsi que configurer les paramètres spécifiques de chaque service API. Les réglages seront automatiquement enregistrés dans le dossier du projet $(ProjectFolder)/Saved/AIChatPlusEditor.

Paramètres de conversation : en cliquant sur l'icône de paramètres en haut de la boîte de chat, vous pouvez ouvrir la fenêtre de paramètres de la conversation en cours. Vous pouvez modifier le nom de la conversation, le service API utilisé pour la conversation, et définir individuellement les paramètres spécifiques de l'API pour chaque conversation. Les paramètres de la conversation sont automatiquement enregistrés dans `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Modification du contenu du chat : lorsque vous survolez le contenu du chat avec la souris, un bouton de réglage du contenu apparaît pour chaque élément de discussion, permettant de régénérer le contenu, de le modifier, de le copier, de le supprimer, et de le régénérer en bas de l'écran (pour les contenus appartenant à des utilisateurs).

Visualisation d'images : Pour la génération d'images, en cliquant sur une image, une fenêtre de visualisation d'images (Visionneuse d'images) s'ouvrira, prenant en charge l'enregistrement d'images en tant que PNG/Texture UE, les textures pouvant être visualisées directement dans le navigateur de contenu (Explorateur de contenu), facilitant ainsi leur utilisation dans l'éditeur. De plus, il est possible de supprimer des images, de les régénérer, et de continuer à en générer davantage. Pour les utilisateurs de l'éditeur sous Windows, la copie d'images est également prise en charge, permettant de les copier directement dans le presse-papiers pour une utilisation aisée. Les images générées lors des sessions sont automatiquement enregistrées dans le dossier de chaque session, le chemin habituel étant `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Plan :

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Paramètres généraux :

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Paramètres de conversation :

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modifier le contenu de la conversation :

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visionneuse d'images :

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Utilisation de modèles volumineux hors ligne

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Modèle de dialogue

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Présentation du code source principal.

Actuellement, le plugin est divisé en plusieurs modules suivants :

AIChatPlusCommon: Runtime module, responsible for handling various AI API interface requests and parsing response content.

AIChatPlusEditor: Module d'édition, responsable de la mise en œuvre de l'outil de chat AI de l'éditeur.

AIChatPlusCllama: Module d'exécution responsable de l'encapsulation des interfaces et des paramètres de llama.cpp, permettant l'exécution hors ligne de modèles volumineux.

Thirdparty/LLAMACpp: Un module tiers pour l'exécution (Runtime), intégrant la bibliothèque dynamique et les fichiers d'en-tête de llama.cpp.

Le UClass responsable d'envoyer la requête est FAIChatPlus_xxxChatRequest. Chaque service API a son propre UClass de requête indépendant. Les réponses aux requêtes sont obtenues via les UClass UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase ; il suffit de s'inscrire aux délégués de retour appropriés.

Avant d'envoyer la demande, il est nécessaire de configurer préalablement les paramètres de l'API et le message à envoyer, cette partie se fait en définissant FAIChatPlus_xxxChatRequestBody. Les détails de la réponse sont également analysés dans FAIChatPLus_xxxChatResponseBody, et lors de la réception de l'appel, il est possible d'obtenir le ResponseBody via une interface spécifique.

Pour obtenir plus de détails sur le code source, vous pouvez consulter l'UE Marketplace : [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Utilisation de l'outil d'édition avec le modèle hors ligne Cllama (llama.cpp)

Les instructions suivantes détaillent l'utilisation du modèle hors ligne llama.cpp dans l'outil d'édition AIChatPlus.

Tout d'abord, téléchargez le modèle hors ligne à partir du site Web de HuggingFace : [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Placez le modèle dans un dossier spécifique, par exemple, dans le répertoire Content/LLAMA du projet de jeu.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Ouvrez l'outil d'édition AIChatPlus : Outils -> AIChatPlus -> AIChat, créez une nouvelle conversation et ouvrez la page de paramètres de la session

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Configurez l'API en tant que Cllama, activez les paramètres d'API personnalisés, ajoutez des chemins de recherche de modèle et sélectionnez un modèle.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Commencez la discussion !!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Utilisation de l'outil de l'éditeur pour traiter les images avec le modèle hors ligne Cllama (llama.cpp)

Téléchargez le modèle hors ligne MobileVLM_V2-1.7B-GGUF depuis le site web de HuggingFace et placez-le également dans le dossier Content/LLAMA sous le nom [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)Translate these text into French language:

和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but the text provided is incomplete and does not contain any content to be translated.

Définir le modèle de session :

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Commencer la discussion en envoyant des images.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###Utilisation du modèle hors ligne Cllama (llama.cpp)

Voici comment utiliser le modèle hors ligne llama.cpp dans votre code.

Tout d'abord, il est nécessaire de télécharger les fichiers de modèle dans Content/LLAMA.

Ajouter une commande au code, et envoyer un message au modèle hors ligne à l'intérieur de cette commande.

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

Après avoir recompilé, utilisez la commande dans l'éditeur Cmd pour voir les résultats de la sortie du grand modèle dans le journal OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Utilisez le modèle hors ligne llama.cpp dans le blueprint.

Les instructions suivantes expliquent comment utiliser le modèle hors ligne llama.cpp dans le blueprint.

Créez un nœud "Envoyer une demande de discussion Cllama" en faisant clic droit dans le schéma.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Créez un nœud Options et définissez `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Créez des messages, ajoutez respectivement un message système et un message utilisateur.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Créez un délégué pour recevoir les informations en sortie du modèle et les afficher à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Voici à quoi ressemble le blueprint complet. Exécutez-le pour voir le message renvoyé par l'écran de jeu lors de l'impression du grand modèle.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###Le rédacteur utilise OpenAI Chat.

Ouvrez l'outil de chat Outils -> AIChatPlus -> AIChat, créez une nouvelle session de chat New Chat, configurez la session ChatApi sur OpenAI, configurez les paramètres de l'interface.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Commencer la discussion :

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Changer le modèle en gpt-4o / gpt-4o-mini permet d'utiliser la fonction d'analyse visuelle d'OpenAI pour les images.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###Le rédacteur utilise OpenAI pour traiter les images (créer/modifier/transformer).

Créer une nouvelle conversation d'image dans l'outil de messagerie, nommée "New Image Chat", modifier les paramètres de la conversation en OpenAI, et définir les paramètres.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Créer une image

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Modifier l'image en remplaçant l'intitulé "Image Chat Type" par "Edit", puis téléverser deux images : une de l'image originale et l'autre avec le masque montrant les zones à modifier (où le canal alpha est à 0).

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Modifier l'image en modifiant le type de discussion de l'image en Variation, puis télécharger une image. OpenAI renverra une variation de l'image initiale.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Utilisation du modèle de chat OpenAI dans le cadre du plan stratégique.

Créez un nœud "Envoyer une demande de discussion OpenAI dans le monde" en faisant un clic droit dans le schéma.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Créez un nœud Options et définissez `Stream=true, Api Key="votre clé API d'OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Créer des messages, ajouter respectivement un message système et un message utilisateur.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Créer un délégué qui reçoit les informations en sortie du modèle et les affiche à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Le texte en français est le suivant :

"Le plan complet ressemble à ceci, en exécutant le plan, vous pouvez voir le message renvoyé par l'écran de jeu lors de l'impression du grand modèle."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Utilisation de la technologie OpenAI pour générer des images.

Dans le schéma, faites un clic droit pour créer un nœud "Send OpenAI Image Request", puis définissez "In Prompt='un beau papillon'".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Créez un nœud Options et définissez `Api Key="votre clé API provenant d'OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Associez l'événement "On Images" et enregistrez les images sur le disque dur local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

Le texte est traduit en français.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###L'éditeur utilise Azure.

Créez une nouvelle conversation (New Chat), remplacez ChatApi par Azure et configurez les paramètres d'API d'Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Commencer la conversation

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###Le rédacteur utilise Azure pour créer des images.

Créez une nouvelle session d'image (New Image Chat), remplacez ChatApi par Azure et configurez les paramètres de l'API Azure. Notez que si le modèle est dall-e-2, les paramètres Quality et Stype doivent être définis sur not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Commencez la conversation pour demander à Azure de créer une image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Utiliser Azure Chat dans Blueprints.


Élaborez le plan suivant, configurez les options Azure, appuyez sur Exécuter, et vous verrez s'afficher sur l'écran les informations de chat renvoyées par Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Utilisation d'Azure pour créer des images selon les directives.

Élaborez le schéma ci-dessous, configurez les options Azure, puis cliquez sur Exécuter. Si l'image est créée avec succès, le message "Create Image Done" s'affichera à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

Selon le paramétrage du plan ci-dessus, l'image sera enregistrée dans le dossier D:\Dwnloads\butterfly.png

## Claude

###Le rédacteur utilise Claude pour discuter et analyser des images.

Créez une nouvelle discussion (New Chat), remplacez ChatApi par Claude, et configurez les paramètres d'API de Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Commencer la discussion

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Utiliser le blueprint pour discuter avec Claude et analyser les images.

Dans la feuille de route, créez un nœud en cliquant droit et nommez-le `Envoyer une demande de discussion à Claude`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Créez un nœud Options et définissez `Stream=true, Api Key="votre clé API provenant de Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Créez des messages, créez une Texture2D à partir d'un fichier, puis créez un AIChatPlusTexture à partir de cette Texture2D et ajoutez-le au message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Suivez le tutoriel ci-dessus pour créer un événement et afficher les informations à l'écran du jeu.

Le texte traduit en français est le suivant : "Le schéma complet ressemble à ceci, exécutez le schéma et vous verrez un message renvoyé à l'écran de jeu pour imprimer un modèle 3D."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Obtenir Ollama

Vous pouvez obtenir le package d'installation localement via le site officiel d'Ollama : [ollama.com](https://ollama.com/)

Vous pouvez utiliser Ollama via l'interface fournie par d'autres utilisateurs d'Ollama.

###L'éditeur utilise Ollama pour discuter et analyser les images.

Créez une nouvelle discussion (New Chat), remplacez ChatApi par Ollama, et configurez les paramètres Api d'Ollama. Pour une conversation textuelle, définissez le modèle comme modèle textuel, tel que llama3.1; pour le traitement d'images, utilisez un modèle prenant en charge la vision, comme moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Commencer la discussion

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Utiliser Ollama pour discuter et analyser des images dans Blueprint.

Créez le schéma suivant, configurez les options d'Ollama, cliquez sur Exécuter, et vous verrez s'afficher les messages de chat renvoyés par Ollama à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###Utilisation de Gemini par l'éditeur

Créer une nouvelle discussion (New Chat), remplacer ChatApi par Gemini et configurer les paramètres d'API de Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Commencer la conversation

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###Utilisation de Gemini pour les discussions sur les blueprints.

Élaborez le schéma ci-dessous, configurez les Options Gemini, cliquez sur Exécuter et vous verrez s'afficher sur l'écran les messages de chat renvoyés par Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)


##Journal des mises à jour

### v1.4.1 - 2025.01.04

####Résolution du problème

Le support de la messagerie pour l'envoi uniquement d'images sans texte.

Répare l'échec d'envoi d'image à l'interface OpenAI.

Réparez le problème de paramètres manquants Quality, Style et ApiVersion dans les configurations d'OpanAI et Azure chattools.

### v1.4.0 - 2024.12.30

####Nouvelles fonctionnalités

* (Fonction expérimentale) Cllama (llama.cpp) prend en charge les modèles multi-modaux et peut traiter les images.

Tous les paramètres de type de plan ont été accompagnés de conseils détaillés.

### v1.3.4 - 2024.12.05

####Nouvelle fonctionnalité

OpenAI supporte l'API de vision.

####Réparation du problème

Réparer l'erreur lors du paramètre stream=false d'OpenAI.

### v1.3.3 - 2024.11.25

####Nouvelle fonctionnalité

Prend en charge l'UE-5.5.

####Réparation du problème

Réparer les problèmes dus à des schémas qui ne fonctionnent pas.

### v1.3.2 - 2024.10.10

####Réparation de problèmes

Réparer le crash de cllama lors de l'arrêt manuel de la demande.

Résolution du problème de l'absence des fichiers ggml.dll et llama.dll lors de l'empaquetage de la version Windows du magasin de téléchargement.

Vérifiez lors de la création de la demande si vous êtes dans le GameThread.

### v1.3.1 - 2024.9.30

####Nouvelle fonctionnalité

Ajouter un SystemTemplateViewer qui permet de visualiser et d'utiliser des centaines de modèles de paramètres système.

####Résolution du problème

Réparez le plugin téléchargé depuis le magasin, llama.cpp ne trouve pas la bibliothèque de liens

Corriger le problème de chemin trop long de LLAMACpp.

Corrigez l'erreur de lien llama.dll après l'empaquetage de Windows.

Réparer le problème de lecture du chemin du fichier sur iOS/Android

Réparer l'erreur de nom dans les réglages de Cllame

### v1.3.0 - 2024.9.23

####Nouvelle fonctionnalité majeure

Intégré llama.cpp pour prendre en charge l'exécution hors ligne de grands modèles locaux.

### v1.2.0 - 2024.08.20

####Nouvelle fonctionnalité

Soutien de la fonctionnalité OpenAI Image Edit/Image Variation

Prend en charge l'API Ollama, permet l'obtention automatique de la liste des modèles pris en charge par Ollama.

### v1.1.0 - 2024.08.07

####Nouvelle fonctionnalité.

Soutenir le plan.

### v1.0.0 - 2024.08.05

####Nouvelle fonctionnalité

Fonctionnalité de base complète

Soutenir OpenAI, Azure, Claude, Gemini

Appliqué avec éditeur de chat intégré.

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Signaler tout oubli. 
