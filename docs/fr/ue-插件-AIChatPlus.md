---
layout: post
title: Document d'explication du plugin AIChatPlus de l'UE
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
description: Documentation du plug-in AIChatPlus pour l'UE
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Document d'instructions du plug-in AIChatPlus de l'UE.

##Entrepôt public

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtenir le plugin

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Présentation du module complémentaire

Ce plugin est compatible avec UE5.2+.

UE.AIChatPlus est un plugin pour UnrealEngine qui permet de communiquer avec différents services de chat AI GPT. Actuellement, il prend en charge les services OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, et llama.cpp en local hors ligne. De nouveaux fournisseurs de services seront également pris en charge à l'avenir. Son implémentation repose sur des requêtes REST asynchrones, offrant des performances élevées et facilitant l'intégration de ces services de chat AI pour les développeurs d'UE.

UE.AIChatPlus comprend également un outil d'édition qui vous permet d'utiliser directement les services de chat AI dans l'éditeur pour générer du texte et des images, analyser des images, etc.

##Instructions d'utilisation

###Outil de messagerie de l'éditeur

La barre de menus Outils -> AIChatPlus -> AIChat permet d'ouvrir l'outil de messagerie de l'éditeur fourni par le plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


L'outil prend en charge la génération de texte, les chats par texte, la génération d'images et l'analyse d'images.

L'interface de l'outil est approximativement comme suit :

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Fonction principale

Modèle hors ligne : Intégration de la bibliothèque llama.cpp, permettant l'exécution hors ligne de gros modèles localement.

* Chat texte : Cliquez sur le bouton `Nouveau Chat` en bas à gauche pour créer une nouvelle conversation de chat texte.

Génération d'images : Cliquez sur le bouton `Nouveau Chat d'Images` dans le coin inférieur gauche pour créer une nouvelle session de génération d'images.

Analyse d'images : Certaines fonctions de chat de "Nouvelle discussion" permettent l'envoi d'images, telles que Claude, Google Gemini. Cliquez sur l'icône 🖼️ ou 🎨 au-dessus de la zone de saisie pour charger l'image à envoyer.

Soutien des plans : Soutien à la création de plans pour les demandes d'API, la messagerie texte, la génération d'images, etc.

Définir le rôle de discussion actuel : le menu déroulant en haut de la boîte de chat permet de choisir le rôle qui enverra les messages actuels, ce qui permet de simuler différents rôles pour ajuster la discussion avec l'IA.

Vider la conversation: En appuyant sur le ❌ en haut de la fenêtre de discussion, vous pouvez effacer l'historique des messages de la conversation actuelle.

Modèle de dialogue : Intégration de centaines de modèles de conversation préétablis pour faciliter le traitement des questions courantes.

Paramètres globaux : en cliquant sur le bouton `Paramétrage` en bas à gauche, vous pouvez ouvrir la fenêtre des paramètres globaux. Vous pouvez définir le chat textuel par défaut, les services d'API de génération d'images et configurer les paramètres spécifiques de chaque service d'API. Les paramètres seront automatiquement enregistrés dans le chemin du projet `$(DossierProjet)/Saved/AIChatPlusEditor`.

Paramètres de la conversation : en cliquant sur l'icône de réglages en haut de la fenêtre de discussion, vous pouvez ouvrir la fenêtre de réglages de la conversation en cours. Vous pouvez modifier le nom de la conversation, le service API utilisé pour la conversation, et définir des paramètres spécifiques pour chaque conversation. Les réglages de la conversation sont automatiquement enregistrés dans `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Modifier le contenu de la discussion : en survolant le contenu de la discussion avec la souris, un bouton de paramètres de ce contenu de discussion apparaîtra, permettant de régénérer le contenu, de le modifier, de le copier, de le supprimer, ou de régénérer le contenu en bas (pour le contenu appartenant à des utilisateurs).

Exploration d'images : En ce qui concerne la génération d'images, cliquer sur une image ouvrira une fenêtre de visualisation d'image (Visionneuse d'images), permettant d'enregistrer l'image au format PNG/UE Texture. Les textures peuvent être visualisées directement dans l'explorateur de contenu (Content Browser), facilitant ainsi leur utilisation dans l'éditeur. D'autres fonctionnalités sont également disponibles, telles que la suppression d'images, la régénération des images, la génération de nouvelles images, etc. Dans l'éditeur sous Windows, il est également possible de copier les images pour les coller directement dans le presse-papiers, facilitant ainsi leur utilisation. Les images générées pendant une session sont automatiquement enregistrées dans le dossier de chaque session, généralement situé dans `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

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

Utilisation de modèles haute capacité hors ligne

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Modèle de conversation

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Présentation du code source principal

Actuellement, le plugin est divisé en plusieurs modules suivants :

AIChatPlusCommon : Le module d'exécution, responsable du traitement des demandes envoyées aux diverses interfaces API d'IA et de l'analyse des réponses reçues.

AIChatPlusEditor: Module d'édition, responsable de la mise en œuvre de l'outil de chat AI de l'éditeur.

AIChatPlusCllama: Module d'exécution (Runtime) chargé d'encapsuler les interfaces et les paramètres de llama.cpp, permettant ainsi l'exécution hors ligne des grands modèles.

Thirdparty/LLAMACpp: Un module tiers d'exécution (Runtime) intégrant la bibliothèque dynamique et les fichiers d'en-tête de llama.cpp.

Le UClass responsable spécifique de l'envoi de la demande est FAIChatPlus_xxxChatRequest. Chaque service API a son propre UClass de demande indépendant. Les réponses aux demandes sont obtenues via deux types de UClass : UAIChatPlus_ChatHandlerBase et UAIChatPlus_ImageHandlerBase. Il suffit de s'inscrire avec les délégués de rappel correspondants.

Avant d'envoyer une requête, vous devez d'abord configurer les paramètres de l'API et le message à envoyer. Ceci est fait en utilisant FAIChatPlus_xxxChatRequestBody. Les détails de la réponse sont également analysés dans FAIChatPlus_xxxChatResponseBody, afin de récupérer le ResponseBody via une interface spécifique lors de la réception de l'appel.

Vous pouvez obtenir plus de détails sur le code source sur la boutique UE : [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Utilisation de l'outil d'édition avec le modèle hors ligne Cllama (llama.cpp)

Voici comment utiliser le modèle hors ligne llama.cpp dans l'outil d'édition AIChatPlus.

Tout d'abord, téléchargez le modèle hors ligne à partir du site Web de HuggingFace : [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Placez le modèle dans un dossier spécifique, par exemple dans le répertoire Content/LLAMA du projet de jeu.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Ouvrez l'outil de l'éditeur AIChatPlus : Outils -> AIChatPlus -> AIChat, créez une nouvelle session de chat et ouvrez la page de paramètres de la session.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Définissez l'API sur Cllama, activez les Paramètres d'API personnalisés, ajoutez un chemin de recherche de modèle et sélectionnez le modèle.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Commencez la discussion !!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Utilisation de l'outil d'édition avec le modèle hors ligne Cllama (llama.cpp) pour traiter les images.

Téléchargez le modèle hors ligne MobileVLM_V2-1.7B-GGUF depuis le site web de HuggingFace et placez-le également dans le répertoire Content/LLAMA : [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but the text you provided does not contain any content to be translated.

Définir le modèle de la session :

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Commencez la discussion en envoyant une photo.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###Utilise le modèle hors ligne Cllama (llama.cpp) dans le code.

Voici comment utiliser le modèle hors ligne llama.cpp dans le code.

Tout d'abord, assurez-vous de télécharger les fichiers de modèle dans le dossier Content/LLAMA.

Ajouter une commande au code et envoyer un message au modèle hors ligne à l'intérieur de cette commande.

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

Après la recompilation, en utilisant la commande dans l'éditeur Cmd, vous pourrez voir les résultats de la sortie du grand modèle dans le journal OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Utilisez le modèle hors ligne llama.cpp pour la conception du projet.

Le texte est traduit en français comme suit :

Le texte décrit comment utiliser le modèle hors ligne llama.cpp dans le blueprint.

Dans la feuille de route, cliquez avec le bouton droit pour créer un nœud `Envoyer une demande de discussion Cllama`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Créez un nœud Options et définissez `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Créez des messages, ajoutez respectivement un message système et un message utilisateur.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Créez un délégué pour recevoir les informations en sortie du modèle et les afficher à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Le texte traduit en français est le suivant :

* Le plan complet ressemble à ceci, en exécutant le plan, vous pouvez voir le message renvoyé à l'écran de jeu imprimant un grand modèle.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###Le fichier llama.cpp utilise le GPU.

Ajout des options de demande de chat Cllama" avec le paramètre "Num Gpu Layer" permettant de définir la charge GPU de llama.cpp, comme illustré dans l'image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

Vous pouvez utiliser un nœud Blueprint pour déterminer si le GPU est pris en charge dans l'environnement actuel et obtenir les backends pris en charge par cet environnement.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_2.png)

###Traiter les fichiers de modèles dans le fichier .Pak après l'emballage.

Une fois que le package Pak est activé, tous les fichiers de ressources du projet seront regroupés dans le fichier .Pak, y compris les fichiers gguf du modèle hors ligne.

Étant donné que llama.cpp ne peut pas lire directement les fichiers .Pak, il est nécessaire de copier les fichiers de modèle hors ligne du fichier .Pak dans le système de fichiers.

AIChatPlus offre une fonctionnalité qui permet de copier automatiquement les fichiers de modèle du fichier .Pak et de les placer dans le dossier Saved :

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

Ou bien, vous pouvez gérer les fichiers de modèle dans le fichier .Pak vous-même, l'essentiel est de copier et traiter les fichiers, car llama.cpp ne peut pas lire correctement le fichier .Pak.

## OpenAI

###Le programme utilise OpenAI pour la conversation.

Ouvrez l'outil de messagerie Tools -> AIChatPlus -> AIChat, créez une nouvelle session de chat New Chat, configurez la session ChatApi sur OpenAI, configurez les paramètres de l'interface.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Commencer la conversation :

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Changer le modèle en gpt-4o / gpt-4o-mini, vous permet d'utiliser la fonction d'analyse d'image OpenAI.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###Le logiciel utilise OpenAI pour traiter les images (créer / modifier / altérer).

Créer une nouvelle session de chat image appelée New Image Chat dans l'outil de messagerie, modifier les paramètres de la session en OpenAI et définir les paramètres.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Créer une image

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Modifier l'image en changeant "Image Chat Type" par "Edit", puis télécharger deux images : une de l'image originale et une autre montrant les zones à modifier, avec une transparence partielle (canal alpha à 0).

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Transformer ces textes en français :

* Modification de la variante d'image par type de chat d'image en type de variation et téléchargement d'une image, OpenAI renverra une variante de l'image d'origine.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Utilisation du modèle de chat OpenAI avec des blueprints

Créez un nœud "Envoyer une demande de chat OpenAI dans le monde" en cliquant droit dans le plan.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Créez un nœud Options et définissez `Stream=true, Api Key="votre clé API provenant d'OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Créer des messages, ajouter respectivement un message système et un message utilisateur.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Créez un délégué qui reçoit les informations de sortie du modèle et les affiche à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Voici comment se présente le blueprint complet. Lancez le blueprint pour voir le message renvoyé sur l'écran du jeu lors de l'impression du grand modèle.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Utilisez OpenAI pour créer des images de la plan.

Dans le plan, faites un clic droit pour créer un nœud appelé "Envoyer une requête d'image à OpenAI" et définissez l'entrée comme "un beau papillon".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Créez un nœud Options et définissez `Api Key="your api key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Attacher l'événement On Images et enregistrer les images sur le disque dur local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

Le document finalisé ressemble à ceci, en exécutant le plan, vous pourrez voir l'image enregistrée à l'emplacement spécifié.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###L'éditeur utilise Azure.

Créer une nouvelle conversation (New Chat), passer de ChatApi à Azure, et configurer les paramètres d'API d'Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Commencer la conversation

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###Le logiciel utilise Azure pour créer des images.

Créez une nouvelle session d'image (Nouvelle discussion d'image), remplacez ChatApi par Azure et configurez les paramètres de l'API Azure. Veuillez noter que si vous utilisez le modèle dall-e-2, les paramètres Quality et Stype doivent être définis sur not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Commencez la conversation et demandez à Azure de créer une image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Utilisez Azure Chat dans le cadre du plan Azure.

Créez le schéma suivant, configurez les options Azure, appuyez sur exécuter et vous verrez s'afficher sur l'écran les informations de chat renvoyées par Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Utiliser Azure pour créer des images.

Élaborez le schéma suivant, configurez les options Azure, puis appuyez sur Exécuter. Si la création de l'image est réussie, vous verrez s'afficher sur l'écran le message "Create Image Done".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

Selon le paramétrage du schéma ci-dessus, l'image sera enregistrée dans le chemin D:\Téléchargements\papillon.png

## Claude

###Le rédacteur utilise Claude pour discuter et analyser des images.

Créer un nouveau chat (New Chat), renommer ChatApi en Claude et configurer les paramètres de l'API de Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Commencer la conversation

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Utilisation des plans bleus pour discuter et analyser les images avec Claude.

Dans le plan, créez un nœud en cliquant avec le bouton droit sur "Envoyer une demande de chat à Claude".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Créez un nœud Options et définissez `Stream=true, Api Key="your api key from Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Créez des messages, créez une Texture2D à partir d'un fichier, puis créez AIChatPlusTexture à partir de Texture2D et ajoutez AIChatPlusTexture au message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Suivez le tutoriel ci-dessus pour créer un événement et afficher les informations à l'écran du jeu.

Voici comment le plan complet ressemble. Lancer le plan pour afficher le message renvoyé sur l'écran de jeu pendant l'impression du grand modèle.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Obtenir Ollama

Vous pouvez obtenir le package d'installation en local via le site officiel d'Ollama : [ollama.com](https://ollama.com/)

Vous pouvez utiliser Ollama via l'interface Ollama fournie par d'autres personnes.

###Le logiciel utilise Ollama pour discuter et analyser des images.

Créer une nouvelle discussion (New Chat), remplacer ChatApi par Ollama et configurer les paramètres d'API d'Ollama. Si c'est une discussion texte, définir le modèle comme modèle texte, tel que llama3.1 ; si vous avez besoin de traiter des images, définir le modèle comme un modèle prenant en charge la vision, par exemple moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Commencez la discussion

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Utiliser Ollama pour discuter et analyser des images sur Blueprint.

Élaborez le schéma suivant, configurez les options Ollama, cliquez sur Exécuter, et vous verrez s'afficher sur l'écran les informations de chat renvoyées par Ollama.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###Utilisez Gemini comme éditeur.

Créez une nouvelle conversation (New Chat), remplacez ChatApi par Gemini et configurez les paramètres d'API de Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Commencer la discussion

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###Le rédacteur utilise Gemini pour envoyer de l'audio.

Sélectionnez la lecture audio à partir d'un fichier / d'un asset ou enregistrez depuis le microphone pour créer l'audio à envoyer.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

Commencer la discussion

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###Utilisation de Gemini pour les discussions sur le projet Blueprint.

Créez le blueprint suivant, configurez les options de Gemini, cliquez sur exécuter, et vous verrez s'afficher sur l'écran les messages de chat renvoyés par Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###Utiliser Gemini pour envoyer des fichiers audio via Blueprint.

Créez le schéma suivant, configurez le chargement audio, configurez les options Gemini, cliquez sur Exécuter, et vous verrez s'afficher sur l'écran les messages de chat renvoyés par Gemini après le traitement audio.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###Utilisez Deepseek dans l'éditeur.

Créez une nouvelle conversation (New Chat), remplacez ChatApi par OpenAi et configurez les paramètres de l'API Deepseek. Ajoutez un modèle de candidat appelé deepseek-chat et définissez le modèle comme deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Commencer la discussion

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Utilisation de Deepseek pour le chat Blueprint

Créez le schéma suivant en configurant les options de requête liées à Deepseek, telles que le modèle, l'URL de base, l'URL de point final, la clé API, etc. Cliquez sur Exécuter pour visualiser les informations de discussion renvoyées par Gemini imprimées à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##Les fonctionnalités supplémentaires du nœud de fonctionnalités fourni

###Cllama 相关 --> Cllama associé

"Cllama Is Valid": Vérifier si Cllama llama.cpp est correctement initialisé.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Vérifie si llama.cpp prend en charge le backend GPU dans l'environnement actuel."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Obtenez les backends pris en charge par llama.cpp actuel"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Préparer le fichier modèle dans Pak": Automatically copying model files from Pak to the file system.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###Images associées

Convertissez UTexture2D en Base64 : convertissez l'image de UTexture2D en format base64 PNG.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

"Enregistrer UTexture2D au format .png"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

Charger le fichier .png dans UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Dupliquer UTexture2D"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###Audio associé

Charger le fichier .wav dans USoundWave.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

Convertir les données .wav en USoundWave: Convertir les données binaires .wav en USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

Sauvegardez USoundWave dans un fichier .wav

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

"Obtenir les données brutes PCM de USoundWave": Convertir USoundWave en données audio binaires.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"Convert USoundWave to Base64" se traduit en français par : "Convertir un USoundWave en Base64".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Dupliquer USoundWave"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

Convertir les données de capture audio en USoundWave: Convertir les données de capture audio en USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

##Journal des mises à jour

### v1.6.0 - 2025.03.02

####Nouvelle fonctionnalité

Mettre à jour llama.cpp vers la version b4604.
Cllama supporte les GPU backends : cuda et metal.
L'outil de discussion Cllama prend en charge l'utilisation du GPU.
Prend en charge la lecture des fichiers de modèle emballés dans Pak.

#### Bug Fix

Résoudre le problème de plantage de Cllama lors du rechargement pendant le raisonnement.

Réparez les erreurs de compilation iOS.

### v1.5.1 - 2025.01.30

####Nouvelle fonctionnalité

Seuls les Gémeaux sont autorisés à partager des fichiers audio.

Optimiser la méthode pour obtenir les données PCM, décompresser les données audio lors de la génération du B64.

Demander d'ajouter deux callbacks OnMessageFinished et OnImagesFinished.

Optimisez la méthode Gemini pour obtenir automatiquement la méthode en fonction de bStream.

Ajoutez quelques fonctions de blueprint pour faciliter la conversion du Wrapper en type réel et obtenir le message de réponse et les erreurs.

#### Bug Fix

Réparer le problème des appels multiples de la fin de la demande.

### v1.5.0 - 2025.01.29

####Nouvelle fonctionnalité.

Soutenir l'envoi de fichiers audio à Gemini.

Les outils de l'éditeur prennent en charge l'envoi de fichiers audio et d'enregistrements.

#### Bug Fix

Réparer le bug de copie de session qui échoue.

### v1.4.1 - 2025.01.04

####Correction de problème

Les outils de messagerie prennent en charge l'envoi d'images sans message.

Réparer le problème d'envoi d'images de l'API OpenAI a échoué document graphique

Veuillez traduire ce texte en français :

* Correction du problème de paramètres manquants Quality, Style et ApiVersion dans les réglages des outils de chat OpanAI et Azure.

### v1.4.0 - 2024.12.30

####Nouvelles fonctionnalités

* (Feature under experimentation) Cllama (llama.cpp) supports multi-modal models, capable of processing images

Tous les paramètres de type blueprint ont été complétés avec des instructions détaillées.

### v1.3.4 - 2024.12.05

####Nouvelle fonctionnalité

OpenAI supporte l'API de vision.

####Correction de problèmes

Réparer l'erreur lorsqu'OpenAI stream=false.

### v1.3.3 - 2024.11.25

####Nouvelles fonctionnalités

Prend en charge l'UE-5.5.

####Réparation du problème

Réparer les problèmes de certains blueprints qui ne fonctionnent pas.

### v1.3.2 - 2024.10.10

####Résolution du problème

Réparer le crash de cllama lorsque vous arrêtez manuellement la demande.

Résoudre le problème de l'absence des fichiers ggml.dll et llama.dll dans le package de téléchargement de la version Win du magasin.

Vérifiez lors de la création de la requête si vous vous trouvez dans le thread de jeu.

### v1.3.1 - 2024.9.30

####Nouvelle fonctionnalité

Ajoutez un SystemTemplateViewer pour visualiser et utiliser des centaines de modèles de paramètres système.

####Résolution du problème

Réparez le plugin téléchargé depuis le magasin, llama.cpp ne peut pas trouver la bibliothèque de liens.

Corriger le problème de chemin trop long de LLAMACpp.

Réparer l'erreur de lien llama.dll après l'emballage de Windows.

Réparer le problème de chemin d'accès aux fichiers pour ios/android.

Réparer l'erreur de nom dans Cllame Setting

### v1.3.0 - 2024.9.23

####Nouvelle fonctionnalité majeure

Intégré llama.cpp pour prendre en charge l'exécution hors ligne de gros modèles locaux.

### v1.2.0 - 2024.08.20

####Nouvelle fonctionnalité

Soutenir OpenAI Image Edit/Image Variation

Prend en charge l'API Ollama, permet d'obtenir automatiquement la liste des modèles pris en charge par Ollama.

### v1.1.0 - 2024.08.07

####Nouvelle fonctionnalité

Soutenir le plan.

### v1.0.0 - 2024.08.05

####Nouvelle fonctionnalité

Fonctionnalité de base complète

Soutien à OpenAI, Azure, Claude et Gemini.

Fournit un outil de messagerie avec un éditeur intégré de qualité.

--8<-- "footer_fr.md"


> Ce message a été traduit en français en utilisant ChatGPT, veuillez donner votre [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Veillez à signaler tout oubli. 
