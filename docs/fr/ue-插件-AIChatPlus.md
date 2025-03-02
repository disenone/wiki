---
layout: post
title: Document d'instructions du plugin AIChatPlus de l'UE
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
description: Documentation des directives AIChatPlus de l'UE
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documentation de l'extension AIChatPlus de l'UE

##Entrepôt public

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtenir le plugin

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Présentation du plugin

Ce plug-in prend en charge UE5.2+.

UE.AIChatPlus est un plugin pour UnrealEngine qui permet de communiquer avec divers services de chat basés sur l'intelligence artificielle GPT. Les services actuellement pris en charge incluent OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, et un mode local pour llama.cpp en mode hors ligne. De nouveaux fournisseurs de services seront également pris en charge à l'avenir. Son implémentation repose sur des requêtes REST asynchrones, offrant des performances optimales et facilitant l'intégration de ces services de chat IA par les développeurs UE.

UE.AIChatPlus comprend également un outil d'édition qui permet d'utiliser directement ces services de discussion par intelligence artificielle dans l'éditeur, pour générer du texte et des images, et analyser des images, entre autres fonctionnalités.

##Instructions d'utilisation

###Outil de messagerie de l'éditeur.

Le menu Outils -> AIChatPlus -> AIChat ouvre l'éditeur de chat fourni par le plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


L'outil prend en charge la génération de texte, la messagerie textuelle, la génération d'images et l'analyse d'images.

L'interface de l'outil est approximativement la suivante :

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Fonctions principales

Modèle hors ligne : intégration de la bibliothèque llama.cpp pour prendre en charge l'exécution hors ligne de grands modèles en local.

Messagerie texte : Appuyez sur le bouton `Nouvelle discussion` en bas à gauche pour créer une nouvelle conversation de messagerie texte.

Génération d'image : Appuyez sur le bouton `Nouveau Chat d'Image` dans le coin inférieur gauche pour démarrer une nouvelle session de génération d'image.

Analyse d'images : Certaines fonctionnalités de discussion de `New Chat` permettent d'envoyer des images, telles que Claude et Google Gemini. Il suffit de cliquer sur les boutons 🖼️ ou 🎨 au-dessus de la zone de texte pour charger l'image à envoyer.

Soutien aux plans (Blueprint) : pour la création de demandes API à partir de plans, permettant de réaliser des fonctions telles que le chat textuel et la génération d'images.

Définissez le rôle de discussion actuel : le menu déroulant en haut de la boîte de discussion permet de définir le rôle actuel pour l'envoi de messages, ce qui permet de simuler différents rôles pour ajuster les conversations avec l'IA.

Vider la conversation : en appuyant sur la croix en haut de la fenêtre de discussion, vous pouvez effacer l'historique des messages de la conversation en cours.

Modèle de conversation : intégration de centaines de modèles de paramètres de conversation pour faciliter le traitement des problèmes courants.

Paramètres généraux : cliquez sur le bouton "Paramètres" en bas à gauche pour ouvrir la fenêtre des paramètres généraux. Vous pouvez définir les paramètres par défaut du chat texte, le service API pour la génération d'images, et configurer les paramètres spécifiques de chaque service API. Les paramètres seront automatiquement enregistrés dans le chemin du projet `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Paramètres de conversation : en cliquant sur le bouton de réglages en haut de la fenêtre de discussion, vous pouvez ouvrir la fenêtre de paramétrage de la conversation en cours. Vous pouvez modifier le nom de la conversation, le service API utilisé pour la conversation, et définir les paramètres spécifiques de l'API pour chaque conversation. Les paramètres de la conversation sont automatiquement enregistrés dans `$(DossierProjet)/Saved/AIChatPlusEditor/Sessions`.

Modifier le contenu du chat : Lorsque vous survolez le contenu du chat avec la souris, un bouton de réglage du contenu s'affiche pour prendre en charge la régénération, la modification, la copie ou la suppression du contenu, ainsi que la régénération du contenu en bas (pour le contenu appartenant aux utilisateurs).

Parcourir les images : pour créer des images, cliquez dessus pour ouvrir la fenêtre de visualisation d'images (ImageViewer), prenant en charge l'enregistrement des images au format PNG/UE Texture. Les textures peuvent être visualisées directement dans le navigateur de contenu (Content Browser), facilitant ainsi leur utilisation dans l'éditeur. De plus, vous pouvez également supprimer des images, en générer de nouvelles, ou encore créer davantage d'images. Dans l'éditeur sous Windows, vous avez également la possibilité de copier des images pour les coller directement dans le presse-papiers, facilitant leur utilisation. Les images générées durant une session seront automatiquement enregistrées dans le dossier de chaque session, généralement situé dans le chemin suivant : `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Plan :

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Paramètres généraux :

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Paramètres de conversation :

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modifier le contenu de la discussion :

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visualiseur d'image :

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Utilisation de modèles à grande échelle hors ligne

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Modèle de conversation

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Présentation du code source principal

Actuellement, le plug-in est divisé en plusieurs modules suivants :

* AIChatPlusCommon: Le module d'exécution (Runtime) est chargé de traiter les demandes d'envoi d'interface API pour l'IA et d'analyser le contenu des réponses.

AIChatPlusEditor : Module éditeur, chargé de mettre en œuvre l'outil de chat AI de l'éditeur.

AIChatPlusCllama: Le module d'exécution (Runtime), responsable de l'encapsulation des interfaces et des paramètres de llama.cpp, permettant l'exécution hors ligne de grands modèles.

Thirdparty/LLAMACpp: Un module tiers d'exécution (Runtime) intégrant les fichiers de bibliothèque dynamique et les fichiers d'en-tête de llama.cpp.

Le UClass spécifiquement chargé d'envoyer la requête est FAIChatPlus_xxxChatRequest, chaque service API ayant son propre UClass de requête indépendant. Les réponses aux requêtes sont obtenues via les UClass UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase, il suffit de s'inscrire au délégué de rappel correspondant.

Avant d'envoyer une demande, il est nécessaire de configurer les paramètres de l'API et le message à envoyer. Cela se fait en utilisant FAIChatPlus_xxxChatRequestBody. Les détails de la réponse sont également analysés dans FAIChatPlus_xxxChatResponseBody, et peuvent être récupérés via une interface spécifique lors de la réception de l'appel de retour.

Vous pouvez trouver plus de détails sur le code source sur la boutique UE : [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Utiliser l'outil d'édition avec le modèle hors ligne Cllama(llama.cpp)

Les instructions suivantes expliquent comment utiliser le modèle hors ligne llama.cpp dans l'outil éditeur AIChatPlus.

Tout d'abord, téléchargez le modèle hors ligne à partir du site HuggingFace : [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Placez le modèle dans un dossier spécifique, par exemple dans le répertoire du projet de jeu Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Ouvrez l'outil d'édition AIChatPlus : Outils -> AIChatPlus -> AIChat, créez une nouvelle session de chat et ouvrez la page de paramètres de la session.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Configurez l'API sur Cllama, activez les paramètres d'API personnalisés, ajoutez des chemins de recherche de modèles et sélectionnez le modèle.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Commencez la conversation !!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Utilisation de l'outil éditeur pour traiter les images avec le modèle hors ligne Cllama(llama.cpp)

Téléchargez le modèle hors ligne MobileVLM_V2-1.7B-GGUF depuis le site web de HuggingFace et placez-le dans le répertoire Content/LLAMA : [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but the text you provided is not readable and seems to be a punctuation mark. Could you please provide a valid text for translation?

Définir le modèle de la session :

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Commencez la discussion en envoyant des photos.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###Utilisation du modèle hors ligne Cllama (llama.cpp)

Voici comment utiliser le modèle hors ligne llama.cpp dans le code.

Tout d'abord, il est nécessaire de télécharger le fichier du modèle dans le dossier Content/LLAMA.

Modifier le code pour ajouter une commande, puis envoyer un message au modèle hors ligne à l'intérieur de cette commande.

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

Une fois que vous avez recompilé, utilisez la commande dans l'éditeur Cmd pour visualiser les résultats de sortie du grand modèle dans le journal OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Utiliser le modèle hors ligne llama.cpp pour le plan en cours.

Voici comment utiliser le modèle hors ligne llama.cpp dans le blueprint.

Créez un nœud 'Demander le chat de Cllama' en cliquant droit dans le schéma.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Créez un nœud Options et définissez `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Créez des Messages, ajoutez respectivement un Message Système et un Message Utilisateur.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Créer un délégué qui reçoit les informations en sortie du modèle et les affiche à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Le texte traduit en français est le suivant :

* L'architecture complète ressemble à ceci, exécutez l'architecture et vous verrez le message renvoyé à l'écran du jeu lors de l'impression du grand modèle.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###Le fichier llama.cpp utilise le GPU.

Ajouter l'option "Num Gpu Layer" aux paramètres de demande de chat Cllama, permettant de définir la charge GPU pour llama.cpp, comme illustré dans l'image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

Vous pouvez utiliser les nœuds Blueprint pour déterminer si le GPU est pris en charge dans l'environnement actuel et obtenir les backends pris en charge par cet environnement.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_2.png)

###Traitement des fichiers de modèle dans le fichier .Pak après l'empaquetage.

Une fois que le Pak est activé, tous les fichiers de ressources du projet seront placés dans le fichier .Pak, y compris les fichiers de modèle hors ligne gguf.

Étant donné que llama.cpp ne prend pas en charge la lecture directe des fichiers .Pak, il est nécessaire de copier les fichiers de modèle hors ligne du fichier .Pak dans le système de fichiers.

AIChatPlus propose une fonctionnalité qui permet de copier automatiquement les fichiers de modèle dans le fichier .Pak et de les placer dans le dossier Saved.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

Vous pouvez également manipuler les fichiers de modèle dans .Pak vous-même, l'essentiel est de copier et de traiter les fichiers, car llama.cpp ne peut pas lire correctement .Pak.

## OpenAI

###Le logiciel utilise OpenAI pour la conversation.

Ouvrez l'outil de chat Outils -> AIChatPlus -> AIChat, créez une nouvelle session de chat Nouveau Chat, configurez la session ChatApi sur OpenAI, configurez les paramètres de l'interface.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Commencer la conversation :

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Changer le modèle en gpt-4o / gpt-4o-mini permet d'utiliser la fonction d'analyse d'images d'OpenAI.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###Le logiciel utilise OpenAI pour traiter les images (créer/modifier/altérer).

Créez une nouvelle conversation d'image dans l'outil de messagerie, nommée "New Image Chat", modifiez les paramètres de la conversation en OpenAI et configurez les paramètres.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Créer une image

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Modifier l'image en remplaçant l'élément "Image Chat Type" par "Edit". Ensuite, télécharger deux images : une image originale et une image avec des zones transparentes indiquant les modifications à apporter (la canal alpha étant égal à 0).

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Modifiez l'image en changeant le type de discussion de l'image en Variation, puis téléchargez une image. OpenAI générera une variante de l'image originale.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Utilisation du modèle de chat OpenAI dans le cadre de la discussion sur le plan.

Dans la feuille de plan, faites un clic droit pour créer un nœud `Send OpenAI Chat Request In World`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Créez un nœud Options et définissez `Stream=true, Api Key="votre clé API OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Créez des messages en ajoutant respectivement un message système et un message utilisateur.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Créez un délégué qui reçoit les informations de sortie du modèle et les affiche à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Le texte traduit en français est le suivant :

* Le blueprint complet ressemble à ceci, en exécutant le blueprint, vous pouvez voir le message renvoyé à l'écran de jeu lors de l'impression du grand modèle.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Utilisation de OpenAI pour créer des images.

Créez un noeud `Send OpenAI Image Request` en faisant un clic droit dans le schéma, et définissez `In Prompt="a beautiful butterfly"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Créez un nœud Options et définissez `Api Key="your api key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Attacher l'événement *On Images* et enregistrer les images sur le disque dur local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

Le blueprint complet ressemble à ceci. En exécutant le blueprint, vous pouvez voir l'image enregistrée à l'emplacement spécifié.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###Utilisation d'Azure par l'éditeur

Créer une nouvelle discussion (New Chat), changer ChatApi en Azure, et configurer les paramètres de l'API Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Commencer la conversation

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###Utilisation d'Azure par l'éditeur pour créer des images

Crée une nouvelle session d'image (New Image Chat), remplace ChatApi par Azure, et configure les paramètres de l'API Azure. Note que si le modèle est dall-e-2, les paramètres Quality et Stype doivent être définis sur not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Commencez la discussion pour demander à Azure de créer une image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Utiliser Azure Chat pour Blueprint

Élaborez le plan suivant, configurez les options Azure, appuyez sur Exécuter, et vous verrez s'afficher sur l'écran les informations de chat renvoyées par Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Utilisez Azure pour créer des images selon le plan.

Créez le schéma ci-dessous, configurez les options Azure, puis cliquez sur Exécuter. Si la création de l'image est réussie, vous verrez s'afficher sur l'écran le message "Création de l'image terminée".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

Selon le paramétrage du plan ci-dessus, l'image sera sauvegardée dans le chemin D:\Dwnloads\butterfly.png.

## Claude

###Le rédacteur utilise Claude pour discuter et analyser les images.

Créez une nouvelle discussion (New Chat), remplacez ChatApi par Claude, et configurez les paramètres d'API de Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Commencer la conversation

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Utilisez Claude pour discuter et analyser des images dans Blueprint.

Créez un nœud "Envoyer une demande de chat à Claude" en cliquant droit dans le schéma.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Créez un nœud Options et définissez `Stream=true, Api Key="votre clé d'API de Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Créez des messages, créez un Texture2D à partir du fichier, puis créez un AIChatPlusTexture à partir du Texture2D et ajoutez-le au message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Suivez le tutoriel ci-dessus pour créer un événement et afficher les informations sur l'écran du jeu.

Le texte en français serait :

* Voici à quoi ressemble un blueprint complet. En exécutant le blueprint, vous pourrez voir le message renvoyé affiché sur l'écran de jeu.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Obtenir Ollama

Vous pouvez obtenir le package d'installation localement sur le site officiel d'Ollama : [ollama.com](https://ollama.com/)

Vous pouvez utiliser Ollama via l'interface Ollama fournie par d'autres utilisateurs.

###Le rédacteur utilise Ollama pour discuter et analyser des images.

Créer une nouvelle conversation (Nouveau Chat), remplacer ChatApi par Ollama et configurer les paramètres de l'API d'Ollama. Pour les discussions textuelles, définir le modèle comme un modèle textuel, tel que llama3.1 ; pour le traitement des images, choisir un modèle prenant en charge la vision comme moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Commencer la discussion

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Utiliser Ollama pour discuter et analyser des images dans les plans.

Élaborez le schéma suivant, configurez les options d'Ollama, appuyez sur Exécuter, et vous verrez s'afficher sur l'écran les informations de chat renvoyées par Ollama.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###Le logiciel utilise Gemini.

Créer une nouvelle conversation (New Chat), changer ChatApi en Gemini, et configurer les paramètres Api de Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Commencer la discussion

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###Le rédacteur utilise Gemini pour envoyer de l'audio.

Sélectionnez la lecture de fichiers audio / la lecture d'actifs audio / l'enregistrement audio du microphone pour générer l'audio à envoyer.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

Commencer la conversation

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###Utilisez Gemini pour discuter des plans.

Créez le plan suivant, configurez les options Gemini, appuyez sur Exécuter, et vous verrez s'afficher sur l'écran les messages de chat renvoyés par Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###Utilisez Gemini pour envoyer des fichiers audio via Blueprint.

Créez le schéma suivant, configurez le chargement audio, paramétrez les options Gemini, cliquez sur Exécuter et vous verrez s'afficher à l'écran les informations de discussion renvoyées par Gemini après traitement audio.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###L'éditeur utilise Deepseek

Créer une nouvelle discussion (New Chat), remplacer ChatApi par OpenAi, et configurer les paramètres de l'API Deepseek. Ajouter un modèle de candidat appelé deepseek-chat, et définir le modèle sur deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Commencer la discussion

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Utiliser Deepseek Chat dans Blueprint

Créez le schéma suivant et configurez les options de demande associées à Deepseek, telles que le modèle, l'URL de base, l'URL de point final, la clé API, etc. Cliquez sur Exécuter pour afficher les informations de chat renvoyées par Gemini à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##Fonctionnalités supplémentaires des nœuds de fonction ajoutés

###Cllama related

"Cllama Is Valid"：Vérifier si Cllama llama.cpp est correctement initialisé.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

Vérifier si le fichier llama.cpp prend en charge le backend GPU dans l'environnement actuel.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Obtenir les backends pris en charge par llama.cpp actuel"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Prépare le fichier modèle Cllama dans Pak": Automatically copies model files from Pak to the file system

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###Images connexes

"Convertir UTexture2D en Base64": Convertir l'image de UTexture2D en format base64 png

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

Enregistrer UTexture2D sous forme de fichier .png

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

Charger le fichier .png dans UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Duplicate UTexture2D": Dupliquer UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###Les textes sont traduits en français: "Audio associé".

"Charger le fichier .wav dans USoundWave"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

Convertir les données .wav en USoundWave: Convertir les données binaires wav en USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

Enregistrez USoundWave sous format de fichier .wav.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

"Obtenir les données brutes PCM de l'USoundWave": Convertir l'USoundWave en données audio brutes binaires

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

Convertir USoundWave en Base64

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Dupliquer USoundWave": Dupliquer USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

Convertir les données de capture audio en USoundWave.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

##Journal de mises à jour

### v1.6.0 - 2025.03.02

####Nouvelle fonctionnalité

Mettre à jour le fichier llama.cpp vers la version b4604.

Cllama supporte les GPU backends : cuda et metal.

L'outil de chat Cllama prend en charge l'utilisation du GPU.

Prise en charge de la lecture des fichiers de modèle dans le package Pak

#### Bug Fix

Réparer le problème de plantage de Cllama lors du rechargement pendant le raisonnement.

Réparer l'erreur de compilation sur iOS.

### v1.5.1 - 2025.01.30

####Nouvelle fonctionnalité

Autoriser uniquement Gemini à envoyer des fichiers audio.

Optimisez la méthode d'obtention des données PCM afin de décompresser les données audio lors de la génération de B64.

Demande d'ajouter deux rappels OnMessageFinished et OnImagesFinished

Optimise la méthode Gemini, et automatise l'acquisition de la méthode selon bStream.

Ajoutez quelques fonctions de plan pour faciliter la conversion de l'enveloppe en types réels, ainsi que pour obtenir le message de réponse et l'erreur.

#### Bug Fix

Corriger le problème des appels multiples à la fin de la demande.

### v1.5.0 - 2025.01.29

####Nouvelle fonctionnalité

Soutenir l'envoi d'audio à Gemini

Les outils de l'éditeur prennent en charge l'envoi d'audio et d'enregistrements.

#### Bug Fix

Corriger le bug causant l'échec de la copie de session.

### v1.4.1 - 2025.01.04

####Réparation de problèmes

L'outil de messagerie prend en charge l'envoi uniquement d'images sans texte.

Réparer l'échec de l'envoi d'images via l'interface OpenAI.

Réparer les paramètres manquants Quality, Style et ApiVersion dans les configurations des outils de chat OpanAI et Azure.

### v1.4.0 - 2024.12.30

####Nouvelle fonctionnalité

* Fonction expérimentale Cllama (llama.cpp) prend en charge les modèles multimodaux et peut traiter les images

Tous les paramètres de type Blueprint ont été pourvus de conseils détaillés.

### v1.3.4 - 2024.12.05

####Nouvelle fonctionnalité

OpenAI prend en charge l'API de vision.

####Réparation des problèmes

Réparer l'erreur lors de OpenAI stream=false

### v1.3.3 - 2024.11.25

####Nouvelle fonctionnalité

Prise en charge de l'UE-5.5.

####Correction du problème

Réparer le problème de certaines blueprints ne fonctionnant pas.

### v1.3.2 - 2024.10.10

####Correction de problèmes

Réparer le crash de cllama lors de l'arrêt manuel de la requête.

Réparer le problème de l'absence des fichiers ggml.dll et llama.dll lors de la création du package win pour le téléchargement de la version dans la boutique.

Vérifier dans le GameThread lors de la création de la requête.

### v1.3.1 - 2024.9.30

####Nouvelle fonctionnalité.

Ajouter un SystemTemplateViewer pour visualiser et utiliser des centaines de modèles de paramètres système.

####Réparation du problème

Réparez le plugin téléchargé depuis le magasin, llama.cpp ne trouve pas la bibliothèque de lien.

Corriger le problème des trop longs chemins dans LLAMACpp.

Réparez l'erreur de lien llama.dll après avoir empaqueté Windows.

Résoudre le problème de lecture du chemin du fichier sur iOS/Android

Corriger le nom d'erreur du Cllame de paramètres

### v1.3.0 - 2024.9.23

####Nouvelle fonctionnalité majeure

Intégré llama.cpp pour prendre en charge l'exécution hors ligne de gros modèles locaux.

### v1.2.0 - 2024.08.20

####Nouvelle fonctionnalité

Soutenir OpenAI Image Edit/Image Variation

Prend en charge l'API Ollama, prend en charge la récupération automatique de la liste des modèles pris en charge par Ollama.

### v1.1.0 - 2024.08.07

####Nouvelle fonctionnalité

Soutenir le plan / la feuille de route.

### v1.0.0 - 2024.08.05

####Nouvelle fonctionnalité

Fonctionnalité de base complète

Soutenir OpenAI, Azure, Claude, Gemini

Propre éditeur de chat avec des fonctionnalités intégrées.

--8<-- "footer_fr.md"


> (https://github.com/disenone/wiki_blog/issues/new)Veuillez signaler tout oubli. 
