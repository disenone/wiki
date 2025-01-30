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
description: UE Plugin AIChatPlus Documentation
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Document de description du plugin UE AIChatPlus

##Entrepôt public.

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtenir le plugin

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Présentation du module complémentaire

Ce plugin est compatible avec UE5.2 et les versions ultérieures.

UE.AIChatPlus is a plugin for UnrealEngine that enables communication with various GPT AI chat services. Currently, it supports services such as OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and local offline llama.cpp. More service providers will be supported in the future. Its implementation is based on asynchronous REST requests, providing high efficiency and convenient access to these AI chat services for UnrealEngine developers.

En même temps, UE.AIChatPlus comprend également un outil d'édition qui permet d'utiliser directement ces services de chat AI dans l'éditeur, de générer des textes et des images, d'analyser des images, etc.

##Instructions d'utilisation

###Outil de messagerie de l'éditeur

Le menu Outils -> AIChatPlus -> AIChat ouvre l'outil de chat de l'éditeur fourni par le plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


Le logiciel prend en charge la génération de texte, le chat textuel, la génération d'images et l'analyse d'images.

L'interface de l'outil est en gros :

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Fonctionnalités principales

Modèle hors ligne : Intégration de la bibliothèque llama.cpp pour prendre en charge l'exécution hors ligne locale des modèles volumineux.

* Chat textuel : Cliquez sur le bouton `New Chat` dans le coin inférieur gauche pour créer une nouvelle session de chat textuel.

Génération d'images : Appuyez sur le bouton `New Image Chat` situé en bas à gauche pour démarrer une nouvelle session de génération d'images.

Analyse d'image : Certaines fonctionnalités de chat de "New Chat" prennent en charge l'envoi d'images, telles que Claude, Google Gemini. Cliquez sur l'icône 🖼️ ou 🎨 au-dessus de la zone de texte pour charger l'image à envoyer.

Soutien aux plans (Blueprint) : Soutien à la création de plans pour API, réalisation de chat texte, génération d'images, etc.

Définissez le rôle de conversation actuel : Le menu déroulant en haut de la boîte de discussion permet de choisir le rôle depuis lequel les messages sont envoyés, ce qui permet de simuler différents rôles pour ajuster la conversation avec l'IA.

Vider la conversation : Le bouton ❌ en haut de la boîte de chat permet d'effacer l'historique des messages de la conversation en cours.

* Modèles de dialogue : des centaines de modèles de paramètres de dialogue intégrés, facilitant le traitement des questions courantes.

Paramètres globaux : En cliquant sur le bouton `Paramètres` en bas à gauche, vous pouvez ouvrir la fenêtre des paramètres globaux. Vous pouvez définir le chat texte par défaut, le service d'API de génération d'images, et configurer les paramètres spécifiques de chaque service API. Les paramètres seront automatiquement enregistrés dans le chemin du projet `$(DossierProjet)/Saved/AIChatPlusEditor`.

Paramètres de la conversation : en cliquant sur le bouton de paramètres en haut de la boîte de chat, vous pouvez ouvrir la fenêtre de paramètres de la conversation actuelle. Vous pouvez modifier le nom de la conversation, le service API utilisé pour la conversation, ainsi que les paramètres spécifiques de l'API utilisés pour chaque session individuelle. Les paramètres de la conversation sont automatiquement enregistrés dans `$(DossierDuProjet)/Saved/AIChatPlusEditor/Sessions`.

* Modification du contenu de chat : Survolez le contenu du chat avec la souris pour faire apparaître le bouton de réglage du contenu, qui permet de régénérer le contenu, de le modifier, de le copier, de le supprimer, ou de le régénérer en bas (pour le contenu dont le rôle est utilisateur).

* Navigation d'images : Pour la génération d'images, cliquer sur une image ouvrira la fenêtre de visualisation d'images (ImageViewer), permettant d'enregistrer l'image sous PNG/UE Texture. La texture peut être directement visualisée dans le navigateur de contenu (Content Browser), facilitant son utilisation dans l'éditeur. De plus, il est possible de supprimer l'image, de la régénérer ou de générer davantage d'images. Pour l'éditeur sous Windows, la fonction de copier l'image est également disponible, permettant de la copier directement dans le presse-papiers pour une utilisation pratique. Les images générées pendant la session seront automatiquement enregistrées dans chaque dossier de session, avec un chemin généralement situé à `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Plan :

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Paramètres généraux :

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Paramètres de conversation :

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Change the chat content:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visionneuse d'images :

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Utiliser un modèle volumineux hors ligne

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Modèle de dialogue

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Présentation du code source principal

Actuellement, le plugin se divise en plusieurs modules :

* AIChatPlusCommon: Module d'exécution (Runtime) responsable du traitement des demandes envoyées par diverses interfaces API AI et de l'analyse des réponses.

AIChatPlusEditor: Module d'édition, responsable de la mise en œuvre de l'outil de discussion AI de l'éditeur.

AIChatPlusCllama: Module d'exécution (Runtime) chargé d'encapsuler les interfaces et les paramètres de llama.cpp, permettant ainsi d'exécuter de grands modèles hors ligne.

* Thirdparty/LLAMACpp : Module tiers à l'exécution (Runtime), intégrant la bibliothèque dynamique et les fichiers d'en-tête de llama.cpp.

La classe UClass responsable de l'envoi des requêtes est FAIChatPlus_xxxChatRequest, chaque service API dispose d'une UClass Request distincte. Les réponses aux requêtes peuvent être récupérées via deux UClass : UAIChatPlus_ChatHandlerBase et UAIChatPlus_ImageHandlerBase, il suffit de s'inscrire aux délégués de rappel correspondants.

Avant d'envoyer une requête, il est nécessaire de configurer les paramètres de l'API et le message à envoyer, ce qui se fait via FAIChatPlus_xxxChatRequestBody. Le contenu spécifique de la réponse est également analysé dans FAIChatPlus_xxxChatResponseBody, et lors de la réception du rappel, il est possible d'obtenir le ResponseBody via une interface spécifique.

Plus de détails sur le code source peuvent être obtenus dans le magasin UE : [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Utilisation de l'outil d'éditeur avec le modèle hors ligne Cllama (llama.cpp)

Voici comment utiliser le modèle hors ligne llama.cpp dans l'outil d'édition AIChatPlus.

* Tout d'abord, téléchargez le modèle hors ligne depuis le site HuggingFace : [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

* Placez le modèle dans un dossier, par exemple dans le répertoire du projet de jeu Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

* Ouvrir l'outil d'édition AIChatPlus : Outils -> AIChatPlus -> AIChat, créer une nouvelle session de chat et ouvrir la page de paramètres de session.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Définissez l'API sur Cllama, activez les paramètres d'API personnalisés, ajoutez un chemin de recherche de modèle et sélectionnez un modèle.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Commencer la conversation !!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###L'outil d'édition utilise le modèle hors ligne Cllama (llama.cpp) pour traiter les images.

Téléchargez le modèle hors ligne MobileVLM_V2-1.7B-GGUF depuis le site web de HuggingFace et placez-le dans le répertoire Content/LLAMA sous le nom [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)Translatez ce texte en langue française :

 和 [mmproj-modèle-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)。

Définir le modèle de la session :

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

* Envoyer une image pour commencer à discuter

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###Le code utilise le modèle hors ligne Cllama (llama.cpp).

Voici comment utiliser le modèle hors ligne llama.cpp dans le code.

Tout d'abord, il est également nécessaire de télécharger les fichiers de modèle dans Content/LLAMA.

* Modifier le code pour ajouter une commande et envoyer un message au modèle hors ligne dans cette commande.

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

* Après avoir recompilé, utilisez la commande dans l'éditeur Cmd pour voir les résultats de sortie du grand modèle dans le journal OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Le plan utilise le modèle hors ligne llama.cpp.

Explique comment utiliser le modèle hors ligne llama.cpp dans le blueprint.

* Dans le blueprint, faites un clic droit pour créer un nœud `Send Cllama Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

* Créez le nœud Options et définissez `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Créez des messages, ajoutez respectivement un message système et un message utilisateur.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Créer un délégué pour recevoir les sorties du modèle et les afficher à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

La version complète du blueprint ressemble à ceci, en exécutant le blueprint, vous pouvez voir le message renvoyé à l'écran de jeu imprimant le grand modèle.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###Le logiciel utilise OpenAI pour discuter.

Ouvrez l'outil de discussion Outils -> AIChatPlus -> AIChat, créez une nouvelle session de discussion Nouvelle discussion, définissez la session ChatApi sur OpenAI, définissez les paramètres de l'interface.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Commencer la conversation :

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Changer le modèle en gpt-4o / gpt-4o-mini permet d'utiliser la fonction d'analyse d'images d'OpenAI.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###Éditeur utilisant OpenAI pour traiter les images (créer/modifier/varier)

Créez une nouvelle discussion d'image dans l'outil de messagerie, nommez-la New Image Chat, ajustez les paramètres de la discussion à OpenAI et configurez-les.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Créer une image

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

* Modifiez l'image en changeant le type de conversation Image Chat en Edit, puis téléchargez deux images : l'une est l'image originale et l'autre est le masque, où les zones transparentes (canal alpha à 0) indiquent les endroits à modifier.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Modifier l'image en changeant le type d'image en "Variation", puis téléverser une image. OpenAI renverra une variation de l'image d'origine.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Utilisation du modèle de conversation OpenAI dans Blueprints

* Faites un clic droit dans le blueprint pour créer un nœud `Send OpenAI Chat Request In World`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Créez un nœud Options et définissez `Stream=true, Api Key="your api key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Créez des messages, ajoutez respectivement un message système et un message utilisateur.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Créer un Delegate pour recevoir les informations de sortie du modèle et les afficher à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Le texte en français est le suivant :

* Le plan complet ressemble à ceci, en exécutant le plan, vous verrez le message renvoyé à l'écran de jeu pour imprimer le grand modèle.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Le plan utilise OpenAI pour créer des images.

* Faites un clic droit sur le blueprint pour créer un nœud `Send OpenAI Image Request` et définissez `In Prompt="a beautiful butterfly"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Créez un nœud Options et définissez `Api Key="votre clé API provenant d'OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

* Lier l'événement On Images et enregistrer les images sur le disque dur local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

Voici à quoi ressemble le plan complet : exécutez-le pour voir l'image sauvegardée à l'emplacement spécifié.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###Le logiciel utilise Azure.

Créez une nouvelle discussion (New Chat), remplacez ChatApi par Azure, et configurez les paramètres de l'API Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

* Commencer la conversation

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###Utilisateur du logiciel crée des images en utilisant Azure.

* Nouvelle session d'image (New Image Chat), changez ChatApi en Azure et configurez les paramètres de l'API Azure. Notez que si le modèle est dall-e-2, il faut régler les paramètres Quality et Stype sur not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

* Commencez à discuter, laissez Azure créer une image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Plan utilise le chat Azure

Créez le blueprint suivant, configurez les options Azure, puis cliquez sur Exécuter pour voir les messages de chat renvoyés par Azure s'afficher à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Créer une image avec Azure selon le plan.

Créez le schéma suivant, configurez les options Azure, puis appuyez sur Exécuter. Si la création de l'image est réussie, un message "Create Image Done" s'affichera à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

Selon les paramètres du plan ci-dessus, l'image sera enregistrée à l'emplacement D:\Dwnloads\butterfly.png.

## Claude

###Le rédacteur utilise Claude pour discuter et analyser des images.

Créez une nouvelle conversation (New Chat), remplacez ChatApi par Claude, et configurez les paramètres API de Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Commencer la discussion

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Utiliser Blueprint pour discuter et analyser des images avec Claude.

* Faites un clic droit sur le blueprint pour créer un nœud `Send Claude Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Créez un nœud Options et définissez `Stream=true, Api Key="votre clé API provenant de Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

* Créez des Messages, créez un Texture2D à partir d'un fichier, et créez un AIChatPlusTexture à partir du Texture2D, puis ajoutez l'AIChatPlusTexture au Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

* Comme dans le tutoriel ci-dessus, créez un événement et affichez les informations à l'écran du jeu.

* Le plan complet ressemble à ceci : en exécutant le plan, vous verrez l'écran de jeu afficher les messages renvoyés par le grand modèle.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Obtenir Ollama

* Vous pouvez obtenir le package d'installation pour une installation locale sur le site officiel d'Ollama : [ollama.com](https://ollama.com/)

* Ollama peut être utilisé via l'interface Ollama fournie par d'autres personnes.

###L'éditeur utilise Ollama pour discuter et analyser des images.

* Nouvelle conversation (New Chat), changez ChatApi en Ollama et définissez les paramètres de l'Api d'Ollama. S'il s'agit d'un chat textuel, définissez le modèle sur un modèle textuel, comme llama3.1 ; si vous devez traiter des images, définissez le modèle sur un modèle compatible avec la vision, comme moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

* Commencer à discuter

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Utilisez Ollama pour discuter et analyser des images.

Créez le plan suivant, configurez les options d'Ollama, cliquez sur "Exécuter" et vous verrez les messages de chat retournés par Ollama s'afficher à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###L'éditeur utilise Gemini.

* Nouvelle conversation (New Chat), changez ChatApi en Gemini et paramétrez les paramètres de l'API de Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

* Commencer la conversation

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###L'éditeur utilise Gemini pour envoyer des audio.

Lire l'audio depuis un fichier / lire l'audio depuis des ressources / enregistrer l'audio depuis un microphone, et générer l'audio à envoyer.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

Commencer la conversation

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###Utilisez Gemini pour discuter des plans avec les Blueprints.

Créez le plan suivant, configurez bien les options Gemini, cliquez sur exécuter et vous pourrez voir les informations de chat retournées par Gemini affichées à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###Le plan utilise Gemini pour envoyer de l'audio.

Créez le blueprint suivant, configurez le chargement de l'audio, paramétrez correctement les options Gemini, cliquez sur exécuter, et vous verrez les informations de chat retournées par Gemini après le traitement de l'audio s'afficher à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###L'éditeur utilise Deepseek.

Créez une nouvelle conversation (New Chat), remplacez ChatApi par OpenAi, et configurez les paramètres Api de Deepseek. Ajoutez un nouveau modèle de candidat appelé deepseek-chat, et définissez le modèle comme deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Commencer la discussion

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Utilisez Deepseek pour discuter des plans.

Créez le plan suivant, configurez les options de requête liées à Deepseek, y compris le modèle, l'URL de base, l'URL du point de terminaison, la clé API et d'autres paramètres. Cliquez sur Exécuter pour voir les informations de chat renvoyées par Gemini s'afficher à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##Journal des mises à jour

### v1.5.1 - 2025.01.30

####Nouvelle fonctionnalité

* Seul Gemini est autorisé à émettre des audio.

* Optimiser la méthode d'obtention des PCMData, décompresser les données audio au moment de générer le B64.

Ajouter deux rappels OnMessageFinished et OnImagesFinished à la demande

Optimisez la méthode Gemini pour obtenir automatiquement la méthode en fonction de bStream.

Ajoutez quelques fonctions de blueprint pour faciliter la conversion du Wrapper en type réel, et pour obtenir le message de réponse et les erreurs.

#### Bug Fix

* Corriger le problème d'appels multiples de Request Finish

### v1.5.0 - 2025.01.29

####Nouvelle fonctionnalité

Soutenir l'envoi audio à Gemini.

* Les outils de l'éditeur prennent en charge l'envoi audio et d'enregistrements.

#### Bug Fix

Corriger le bug de copie de session en échec

### v1.4.1 - 2025.01.04

####Correction de problèmes

* Les outils de chat prennent en charge l'envoi uniquement d'images sans message.

Réparer le problème d'envoi d'images de l'interface OpenAI a échoué.

* Correction des paramètres Quality, Style, ApiVersion manquants dans les paramètres de l'outil de chat OpanAI et Azure=

### v1.4.0 - 2024.12.30

####Nouveau fonctionnement

* (Fonctionnalité expérimentale) Cllama (llama.cpp) prend en charge les modèles multimodaux, capables de traiter des images.

Tous les paramètres de type "Blueprint" ont maintenant des descriptions détaillées.

### v1.3.4 - 2024.12.05

####Nouvelle fonctionnalité

* OpenAI prend en charge l'API de vision

####Correction de problèmes

Réparer l'erreur lors du paramétrage de stream=false d'OpenAI.

### v1.3.3 - 2024.11.25

####Nouvelle fonctionnalité

* Supporte UE-5.5

####Correction de problèmes

* Réparation de certains problèmes de non-application des plans.

### v1.3.2 - 2024.10.10

####Réparation de problèmes

* Correction de l'effondrement de cllama lors de l'arrêt manuel de la demande.

Résoudre le problème de l'absence des fichiers ggml.dll et llama.dll lors de la création du package pour la version Windows du magasin en ligne.

Vérifiez lors de la création de la demande si vous êtes dans le GameThread.

### v1.3.1 - 2024.9.30

####Nouvelle fonctionnalité

* Ajouter un SystemTemplateViewer, permettant de consulter et d'utiliser des centaines de modèles de paramètres système.

####Réparation du problème

Réparez le plugin téléchargé depuis la boutique, llama.cpp ne trouve pas la bibliothèque de liens

* Correction du problème de chemin trop long de LLAMACpp

Réparez l'erreur de lien llama.dll après avoir emballé Windows.

* Corriger le problème de lecture des chemins de fichiers sur ios/android

Réparer l'erreur de nom de configuration de Cllame

### v1.3.0 - 2024.9.23

####Nouvelle fonctionnalité majeure

* Intégré avec llama.cpp, prend en charge l'exécution hors ligne locale de grands modèles.

### v1.2.0 - 2024.08.20

####Nouvelle fonction

* Prise en charge de l'édition d'images OpenAI / Variation d'images

* Prise en charge de l'API Ollama, prise en charge de l'obtention automatique de la liste des modèles pris en charge par Ollama.

### v1.1.0 - 2024.08.07

####Nouveau fonctionnalité

Soutien au plan d'action

### v1.0.0 - 2024.08.05

####Nouveau fonction

* Fonctionnalités de base complètes

Soutenir OpenAI, Azure, Claude, Gemini.

* Éditeur de chat intégré avec des fonctionnalités complètes.

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez donner votre [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Identifier tout manquement. 
