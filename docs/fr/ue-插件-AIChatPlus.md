---
layout: post
title: Documentation sur le plugin UE AIChatPlus
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
description: UE Plugin AIChatPlus Document de présentation
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Document d'instruction du plugin UE AIChatPlus

##Entrepôt public

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtenir le plugin

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Présentation du plugin

Ce plugin prend en charge UE5.2 et plus.

UE.AIChatPlus est un plugin UnrealEngine qui permet de communiquer avec divers services de chat AI basés sur GPT. Les services actuellement pris en charge incluent OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, et llama.cpp en mode hors ligne local. À l'avenir, davantage de fournisseurs de services seront également supportés. Sa mise en œuvre repose sur des requêtes REST asynchrones, offrant une performance efficace et facilitant l'accès des développeurs UE à ces services de chat AI.

En même temps, UE.AIChatPlus comprend également un outil d'édition, permettant d'utiliser ces services de chat AI directement dans l'éditeur, de générer du texte et des images, d'analyser des images, etc.

##Mode d'emploi

###Outil de chat d'éditeur

Menu Outils -> AIChatPlus -> AIChat pour ouvrir l'outil de chat de l'éditeur fourni par le plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


Les outils prennent en charge la génération de texte, le chat textuel, la génération d'images et l'analyse d'images.

L'interface de l'outil est essentiellement la suivante :

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Principales fonctionnalités

* Modèle de grande taille hors ligne : intègre la bibliothèque llama.cpp, prend en charge l'exécution locale hors ligne de grands modèles.

* Chat textuel : Cliquez sur le bouton `Nouveau chat` en bas à gauche pour créer une nouvelle session de chat textuel.

* Génération d'images : cliquez sur le bouton `New Image Chat` en bas à gauche pour créer une nouvelle session de génération d'images.

* Analyse d'images : certaines fonctions de chat de `New Chat` prennent en charge l'envoi d'images, comme Claude, Google Gemini. Cliquez sur le bouton 🖼️ ou 🎨 au-dessus de la zone de saisie pour charger l'image à envoyer.

* Support des Blueprints : prend en charge la création de requêtes API avec des Blueprints, permettant des fonctionnalités telles que le chat textuel, la génération d'images, etc.

* Définir le rôle actuel du chat : Le menu déroulant en haut de la fenêtre de chat permet de définir le rôle de l'expéditeur du texte actuel, ce qui permet d'ajuster la conversation AI en simulant différents rôles.

* Effacer la conversation : Le bouton ❌ en haut de la zone de chat permet d'effacer l'historique des messages de la conversation en cours.

* Modèles de dialogue : plusieurs centaines de modèles de paramètres de dialogue intégrés, facilitant le traitement des questions courantes.

* Paramètres globaux : Cliquez sur le bouton `Setting` en bas à gauche pour ouvrir la fenêtre des paramètres globaux. Vous pouvez définir le chat texte par défaut, le service API de génération d'images et spécifier les paramètres concrets pour chaque service API. Les paramètres seront automatiquement enregistrés dans le chemin du projet `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Paramètres de la conversation : cliquez sur le bouton de paramètres en haut de la boîte de chat pour ouvrir la fenêtre des paramètres de la conversation actuelle. Il est possible de modifier le nom de la conversation, de changer le service API utilisé pour la conversation, et de configurer individuellement les paramètres spécifiques de l'API pour chaque conversation. Les paramètres de la conversation sont automatiquement enregistrés dans `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

* Modification du contenu de discussion : en survolant le contenu de la discussion, un bouton de réglage pour ce contenu apparaîtra, permettant de régénérer le contenu, de modifier le contenu, de copier le contenu, de supprimer le contenu, et de régénérer le contenu en bas (pour le contenu dont le rôle est l'utilisateur).

* Navigation d'images : Pour la génération d'images, cliquer sur une image ouvrira la fenêtre de visualisation d'image (ImageViewer), permettant d'enregistrer l'image sous PNG/UE Texture. La texture peut être directement visualisée dans le navigateur de contenu (Content Browser), rendant son utilisation dans l'éditeur plus pratique. De plus, il est possible de supprimer l'image, de régénérer l'image, ou de continuer à en générer davantage. Pour l'éditeur sous Windows, la fonction de copie d'image est également supportée, permettant de copier directement l'image dans le presse-papiers pour un usage facile. Les images générées lors des sessions seront également automatiquement sauvegardées dans chaque dossier de session, le chemin étant généralement `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Plan :

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Paramètres globaux :

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Paramètres de conversation :

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modifier le contenu de la discussion :

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visionneuse d'images :

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Utiliser un grand modèle hors ligne

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Modèle de dialogue

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introduction au code source

Actuellement, le plugin est divisé en plusieurs modules :

* AIChatPlusCommon : Module d'exécution (Runtime), responsable du traitement des requêtes envoyées par diverses API d'IA et de l'analyse des réponses.

* AIChatPlusEditor : module d'édition (Editor), chargé de mettre en œuvre l'outil de chat AI pour l'édition.

* AIChatPlusCllama : Module d'exécution (Runtime), responsable de l'encapsulation des interfaces et des paramètres de llama.cpp, permettant l'exécution hors ligne de grands modèles.

* Thirdparty/LLAMACpp : Module tiers à l'exécution (Runtime), intégrant la bibliothèque dynamique et les fichiers d'en-tête de llama.cpp.

La classe UClass spécifiquement responsable de l'envoi des requêtes est FAIChatPlus_xxxChatRequest, et chaque service API possède une classe Request UClass indépendante. Les réponses aux requêtes sont obtenues via deux UClass, UAIChatPlus_ChatHandlerBase et UAIChatPlus_ImageHandlerBase, et il suffit d'enregistrer les délégués de rappel appropriés.

Avant d'envoyer une requête, il est nécessaire de configurer les paramètres de l'API et le message à envoyer. Cela se fait via FAIChatPlus_xxxChatRequestBody. Le contenu spécifique de la réponse est également analysé dans FAIChatPlus_xxxChatResponseBody, et lors de la réception du rappel, il est possible d'obtenir le ResponseBody via une interface spécifique.

Plus de détails sur le code source peuvent être obtenus sur la boutique UE : [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###L'outil d'édition utilise le modèle hors ligne Cllama (llama.cpp)

Voici comment utiliser le modèle hors ligne llama.cpp dans l'outil d'édition AIChatPlus.

* Tout d'abord, téléchargez le modèle hors ligne depuis le site HuggingFace : [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

* Placez le modèle dans un dossier, par exemple dans le répertoire du projet de jeu Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

* Ouvrez l'outil d'édition AIChatPlus : Outils -> AIChatPlus -> AIChat, créez une nouvelle session de chat et ouvrez la page des paramètres de session.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

* Définissez l'Api sur Cllama, activez les paramètres d'Api personnalisés, ajoutez le chemin de recherche du modèle et choisissez le modèle.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

* Commencer la discussion !!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###L'outil de l'éditeur utilise le modèle hors ligne Cllama (llama.cpp) pour traiter les images.

* Téléchargez le modèle hors ligne MobileVLM_V2-1.7B-GGUF depuis le site HuggingFace et placez-le également dans le répertoire Content/LLAMA : [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)。

* Configurer le modèle de la session :

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

* Envoyer une image pour commencer la conversation

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###Le code utilise le modèle hors ligne Cllama (llama.cpp)

Voici comment utiliser le modèle hors ligne llama.cpp dans le code.

* Tout d'abord, il est également nécessaire de télécharger le fichier modèle dans le dossier Content/LLAMA.

* Modifiez le code pour ajouter une commande et envoyez un message au modèle hors ligne dans cette commande.

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

* Après recompilation, utilisez la commande dans l'éditeur Cmd pour voir les résultats du grand modèle dans le journal OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Le plan utilise le modèle hors ligne llama.cpp.

Voici comment utiliser le modèle hors ligne llama.cpp dans les planches.

* Faites un clic droit dans le blueprint pour créer un nœud `Send Cllama Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

* Créez le nœud Options et définissez `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

* Créez des Messages, en ajoutant respectivement un Message Système et un Message Utilisateur.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Créez un délégué pour recevoir les informations de sortie du modèle et les afficher à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* Le plan complet ressemble à cela. Exécutez le plan pour voir l'écran de jeu afficher le message renvoyé par le grand modèle.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###L'éditeur utilise OpenAI Chat.

* Ouvrez l'outil de chat Outils -> AIChatPlus -> AIChat, créez une nouvelle session de chat Nouvelle discussion, définissez la session ChatApi sur OpenAI, définissez les paramètres de l'interface.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

* Commencer à discuter :

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

* Changez le modèle en gpt-4o / gpt-4o-mini, vous pouvez utiliser les fonctionnalités visuelles d'OpenAI pour analyser les images.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###L'éditeur utilise OpenAI pour traiter des images (création/modification/variation)

* Créez une nouvelle conversation d'image dans l'outil de chat New Image Chat, modifiez les paramètres de la conversation en OpenAI et réglez les paramètres.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

* Créer une image

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

* Modifiez l'image, changez le type de conversation Image Chat en Éditer et téléversez deux images, l'une étant l'image originale et l'autre étant le masque où les zones transparentes (canal alpha à 0) indiquent les endroits à modifier.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

* Modifiez le type de conversation Image Chat en Variation et téléchargez une image. OpenAI renverra une variante de l'image originale.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Le plan utilise les modèles de chat d'OpenAI.

* Dans le blueprint, faites un clic droit pour créer un nœud `Send OpenAI Chat Request In World`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

* Créez un nœud Options et définissez `Stream=true, Api Key="votre clé API d'OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

* Créer des Messages, en ajoutant respectivement un Message Système et un Message Utilisateur.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Créer un Delegate pour recevoir les informations de sortie du modèle et les afficher à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* Le blueprint complet ressemble à ceci. En exécutant le blueprint, vous pourrez voir l'écran de jeu affichant les messages retournés par le grand modèle.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Le plan utilise OpenAI pour créer des images.

* Dans le plan, faites un clic droit pour créer un nœud `Send OpenAI Image Request` et définissez `In Prompt="a beautiful butterfly"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

* Créez un nœud Options et définissez `Api Key="votre clé API d'OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

* Lier l'événement On Images et enregistrer les images sur le disque dur local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

* Le blueprint complet ressemble à cela, exécutez le blueprint pour voir l'image enregistrée à l'emplacement spécifié.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###Éditeur utilisant Azure

* Nouvelle conversation (New Chat), changez ChatApi en Azure et configurez les paramètres Api d'Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

* Commencer à discuter

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###L'éditeur utilise Azure pour créer des images.

* Nouvelle session d'image (New Image Chat), changez ChatApi en Azure et configurez les paramètres de l'API Azure. Remarque : si c'est le modèle dall-e-2, il faut régler les paramètres Quality et Stype sur not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

* Commencez à discuter, laissez Azure créer des images.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Plan utiliser Azure Chat

Créez le plan suivant, configurez les options Azure, puis cliquez sur exécuter pour voir les messages de chat renvoyés par Azure s'afficher à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Créer des images avec Azure dans le plan directeur

Créez le blueprint suivant, configurez les options Azure, puis cliquez sur exécuter. Si la création de l'image est réussie, un message "Création de l'image terminée" s'affichera à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

Selon la configuration du plan ci-dessus, l'image sera enregistrée à l'emplacement D:\Dwnloads\butterfly.png.

## Claude

###L'éditeur utilise Claude pour discuter et analyser des images.

* Nouvelle conversation, remplacez ChatApi par Claude et définissez les paramètres de l'API de Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

* commencer à discuter

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Le plan utilise Claude pour discuter et analyser des images.

* Faites un clic droit dans le blueprint pour créer un nœud `Send Claude Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

* Créez un nœud Options et définissez `Stream=true, Api Key="votre clé API de Clude", Max Output Tokens=1024`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

* Créer des Messages, créer Texture2D à partir d'un fichier, et créer AIChatPlusTexture à partir de Texture2D, puis ajouter AIChatPlusTexture au Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

* Comme dans le tutoriel ci-dessus, créez un événement et imprimez les informations à l'écran du jeu.

* Le plan complet ressemble à ceci. En exécutant le plan, vous pourrez voir l'écran de jeu afficher les messages renvoyés par le grand modèle.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Obtenir Ollama

* Vous pouvez obtenir le package d'installation pour une installation localement sur le site officiel d'Ollama : [ollama.com](https://ollama.com/)

* Il est possible d'utiliser Ollama via l'interface fournie par d'autres.

###L'éditeur utilise Ollama pour discuter et analyser des images.

* Nouveau chat (New Chat), changez ChatApi en Ollama et définissez les paramètres de l'API Ollama. Si c'est un chat textuel, définissez le modèle sur un modèle textuel, comme llama3.1 ; si vous devez traiter des images, définissez le modèle sur un modèle prenant en charge la vision, tel que moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

* Commencer à discuter

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Le plan utilise Ollama pour discuter et analyser des images.

Créez le schéma suivant, configurez les options Ollama, puis cliquez sur exécuter pour voir l'information de chat renvoyée par Ollama s'afficher sur l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###Éditeur utilisant Gemini

* Nouvelle conversation (New Chat), changez le ChatApi en Gemini et définissez les paramètres de l'Api de Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

* Commencer la discussion

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###Le plan utilise le chat Gemini.

Créez le blueprint suivant, configurez les options Gemini, cliquez sur exécuter, et vous verrez s'afficher sur l'écran les messages de chat renvoyés par Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

## Deepseek

###L'éditeur utilise Deepseek

* Nouvelle conversation (New Chat), changer ChatApi en OpenAi et paramétrer les paramètres Api de Deepseek. Ajoutez des modèles candidats appelés deepseek-chat et définissez le modèle sur deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

* Commencer le chat

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Plan d'utilisation de Deepseek Chat

Créez le plan suivant et configurez les options de requête liées à Deepseek, y compris les paramètres Model, Base Url, End Point Url et ApiKey. Cliquez sur exécuter pour voir les informations de chat retournées par Gemini s'afficher à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##Journal des mises à jour

### v1.5.0 - 2025.01.29

####Nouveau fonctionnalité

* Soutenir l’envoi de fichiers audio à Gemini

* Les outils de l'éditeur prennent en charge l'envoi de l'audio et des enregistrements.

#### Bug Fix

* Correction du bug d'échec de copie de session

### v1.4.1 - 2025.01.04

####Correction de problèmes

* L'outil de chat prend en charge l'envoi d'images sans messages.

* Correction de l'échec de l'envoi d'images par l'interface OpenAI.

* Correction du problème où les paramètres Quality, Style, ApiVersion étaient omis dans les paramètres de l'outil de chat OpanAI et Azure.

### v1.4.0 - 2024.12.30

####Nouveau fonctionnalités

* (Fonctionnalité expérimentale) Cllama (llama.cpp) prend en charge les modèles multimodaux et peut traiter des images.

* Tous les paramètres de type blueprint sont accompagnés d'instructions détaillées.

### v1.3.4 - 2024.12.05

####Nouveau fonction

* OpenAI prend en charge l'API de vision

####Correction de problèmes

* Correction de l'erreur lorsque OpenAI stream=false

### v1.3.3 - 2024.11.25

####Nouvelle fonctionnalité

* Supporte UE-5.5

####Correction de problèmes

* Correction de certains problèmes d'inefficacité des plans.

### v1.3.2 - 2024.10.10

####Correction de problèmes

* Correction d'un crash de cllama lors de l'arrêt manuel de la requête.

* Résoudre le problème de non-trouvabilité des fichiers ggml.dll et llama.dll dans la version téléchargée de la boutique pour Windows.

* Vérifiez si vous êtes dans le GameThread lors de la création de la demande, vérification de CreateRequest dans le fil de jeu.

### v1.3.1 - 2024.9.30

####Nouvelle fonctionnalité

* Ajouter un SystemTemplateViewer, permettant de consulter et d'utiliser des centaines de modèles de paramètres système.

####Correction de problèmes

* Réparer le plugin téléchargé depuis la boutique, la bibliothèque llama.cpp est introuvable.

* Correction du problème de chemin trop long dans LLAMACpp

* Correction de l'erreur de lien llama.dll après le packaging de Windows.

* Correction du problème de lecture du chemin de fichier sur iOS/Android.

* Corriger l'erreur de nom dans les paramètres Cllame

### v1.3.0 - 2024.9.23

####Nouvelles fonctionnalités majeures

* Intègre llama.cpp, prend en charge l'exécution locale hors ligne de grands modèles.

### v1.2.0 - 2024.08.20

####Nouveau Fonctionnalité

* Support pour l'édition d'images OpenAI / Variation d'images

* Prise en charge de l'API Ollama, prise en charge de l'obtention automatique de la liste des modèles pris en charge par Ollama.

### v1.1.0 - 2024.08.07

####Nouveau fonctionnement

* Soutien aux plans

### v1.0.0 - 2024.08.05

####Nouveau Fonctionnalité

* Fonctionnalités complètes de base

* Support pour OpenAI, Azure, Claude, Gemini

* Outil de chat avec éditeur de fonctionnalités complètes intégré

--8<-- "footer_fr.md"


> Ce post a été traduit à l'aide de ChatGPT, veuillez laisser vos [**retours**](https://github.com/disenone/wiki_blog/issues/new)Veuillez indiquer toute omission. 
