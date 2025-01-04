---
layout: post
title: Documentation du plugin AIChatPlus de l'UE
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

#Document de présentation du plugin AIChatPlus de l'UE

##Entrepôt public

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtenir le plugin

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Présentation du plugin

Ce plugin prend en charge UE5.2+.

UE.AIChatPlus est un plugin pour UnrealEngine qui permet de communiquer avec divers services de chat GPT AI. Les services actuellement pris en charge sont OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama et llama.cpp en local hors ligne. À l'avenir, d'autres fournisseurs de services seront également pris en charge. Son implémentation repose sur des requêtes REST asynchrones, offrant des performances élevées et permettant aux développeurs d'UnrealEngine de facilement intégrer ces services de chat AI.

UE.AIChatPlus includes également un outil d'édition qui permet d'utiliser directement ces services de discussion AI dans l'éditeur pour générer du texte et des images, analyser des images, etc.

##Instructions d'utilisation.

###Outils de messagerie de l'éditeur

La section Tools -> AIChatPlus -> AIChat dans le menu ouvre l'outil de discussion de l'éditeur fourni par le plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


Le support de l'outil inclut la génération de texte, les chats textuels, la génération d'images, et l'analyse d'images.

L'interface de l'outil est approximativement la suivante :

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Fonctions principales

Modèle hors ligne : Intégration de la bibliothèque llama.cpp, prenant en charge l'exécution hors ligne locale des grands modèles

Créez une nouvelle conversation textuelle en cliquant sur le bouton `Nouveau Chat` situé en bas à gauche.

Génération d'images : Cliquez sur le bouton "Nouveau chat d'image" en bas à gauche pour démarrer une nouvelle session de génération d'images.

Analyse d'image : certaines fonctionnalités de chat de "Nouveau Chat" prennent en charge l'envoi d'images, comme Claude, Google Gemini. Cliquez sur les boutons 🖼️ ou 🎨 au-dessus de la zone de saisie pour charger l'image à envoyer.

Soutien des plans (Blueprint) : soutien à la création de plans pour les requêtes API, la messagerie texte, la génération d'images, etc.

Définir le rôle de discussion actuel : Le menu déroulant en haut de la fenêtre de discussion permet de choisir le rôle du personnage à partir duquel les messages sont envoyés, ce qui permet de régler les interactions avec l'IA en simulant différentes identités.

Vider la conversation : L'icône ❌ en haut de la fenêtre de discussion permet de supprimer l'historique des messages de la conversation actuelle.

Modèle de dialogue : des centaines de modèles de dialogues intégrés pour faciliter le traitement des problèmes courants.

Paramètres généraux : en cliquant sur le bouton "Paramètres" en bas à gauche, vous pouvez ouvrir la fenêtre des paramètres généraux. Vous pouvez définir le chat texte par défaut, le service API de génération d'images, et configurer les paramètres spécifiques de chaque service API. Les paramètres seront automatiquement enregistrés dans le chemin du projet "$(DossierProjet)/Saved/AIChatPlusEditor".

Paramètres de la conversation : en cliquant sur le bouton de paramètres en haut de la boîte de chat, vous pouvez ouvrir la fenêtre de paramètres de la conversation en cours. Cela permet de modifier le nom de la conversation, le service API utilisé pour la conversation, et de définir spécifiquement les paramètres de l'API pour chaque conversation individuelle. Les paramètres de la conversation sont automatiquement enregistrés dans `$(DossierProjet)/Saved/AIChatPlusEditor/Sessions`.

Modifier le contenu de la discussion : Lorsque vous survolez le contenu de la discussion avec la souris, un bouton de paramètres pour ce contenu apparaît, offrant la possibilité de régénérer, modifier, copier ou supprimer le contenu, ainsi que de régénérer le contenu en-dessous (pour les contenus appartenant à un utilisateur).

Affichage d'images : Pour la génération d'images, cliquez sur une image pour ouvrir la fenêtre d'affichage d'images (ImageViewer), prenant en charge l'enregistrement des images au format PNG/UE Texture. Les textures peuvent être visualisées directement dans le navigateur de contenu (Content Browser), facilitant ainsi leur utilisation dans l'éditeur. De plus, vous pouvez supprimer, régénérer ou continuer à générer plus d'images. Pour les éditeurs sous Windows, il est également possible de copier les images pour les coller facilement. Les images générées au cours de la session seront automatiquement enregistrées dans le dossier de chaque session, généralement situé à l'emplacement suivant : `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Plan :

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Paramètres globaux :

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Paramètres de conversation :

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modifier le contenu de la conversation :

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visionneuse d'images :

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Utilisation de modèles de grande taille hors ligne

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Modèle de dialogue

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Présentation du code source principal

Actuellement, le plugin est divisé en plusieurs modules suivants :

AIChatPlusCommon : Module d'exécution, responsable du traitement des demandes envoyées aux différentes interfaces API de l'IA et de l'analyse du contenu des réponses.

AIChatPlusEditor: Module d'édition, responsable de la mise en œuvre de l'outil de chat AI de l'éditeur.

AIChatPlusCllama: Le module d'exécution (Runtime), responsable de l'encapsulation des interfaces et des paramètres de llama.cpp, permettant d'exécuter hors ligne de grands modèles.

Thirdparty/LLAMACpp: Un module tiers d'exécution (Runtime) qui intègre la bibliothèque dynamique et les fichiers d'en-tête llama.cpp.

Le UClass chargé spécifiquement d'envoyer les demandes est FAIChatPlus_xxxChatRequest. Chaque service API a son propre UClass de demande indépendant. Les réponses aux demandes sont obtenues via les UClass UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase, il suffit de s'inscrire aux délégués de rappel correspondants.

Avant d'envoyer une requête, il est nécessaire de configurer les paramètres de l'API et le message à envoyer, cela se fait en utilisant FAIChatPlus_xxxChatRequestBody. Les détails de la réponse sont également analysés dans FAIChatPlus_xxxChatResponseBody, et au moment de recevoir un retour d'appel, il est possible d'obtenir le ResponseBody via une interface spécifique.

Vous pouvez obtenir plus de détails sur le code source sur la boutique UE : [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Utilisation de l'outil d'édition avec le modèle hors ligne Cllama (llama.cpp)

Voici comment utiliser le modèle hors ligne llama.cpp dans l'outil d'édition AIChatPlus.

Tout d'abord, téléchargez le modèle hors ligne depuis le site de HuggingFace : [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Placez le modèle dans un dossier spécifique, par exemple dans le répertoire du projet de jeu Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Ouvrez l'outil éditeur AIChatPlus : Outils -> AIChatPlus -> AIChat, créez une nouvelle session de chat et ouvrez la page des paramètres de la session.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Configurer l'API sur Cllama, activer les paramètres API personnalisés, ajouter des chemins de recherche de modèles et sélectionner un modèle.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Commencez la conversation !!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Utilisation de l'outil de l'éditeur pour traiter les images à l'aide du modèle hors ligne Cllama (llama.cpp)

Téléchargez le modèle hors ligne MobileVLM_V2-1.7B-GGUF sur le site web de HuggingFace et placez-le également dans le répertoire Content/LLAMA : [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)Translatez ces textes en langue française :

 和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)。

Définir le modèle de la session :

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Envoyer une image pour commencer la conversation.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###Utilisation du modèle hors ligne Cllama (llama.cpp)

Voici comment utiliser le modèle hors ligne llama.cpp dans le code.

Tout d'abord, il est nécessaire de télécharger le fichier du modèle dans le dossier Content/LLAMA.

Veuillez ajouter une ligne de code pour inclure une commande permettant d'envoyer un message à un modèle hors ligne.

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

Après avoir recompilé, en utilisant la commande dans l'éditeur Cmd, vous pouvez voir les résultats de la sortie du grand modèle dans le journal OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Utiliser le modèle hors ligne llama.cpp dans le plan en question.

Les instructions suivantes expliquent comment utiliser le modèle hors ligne llama.cpp dans le script de blueprint.

Dans le plan, créez un nœud en faisant un clic droit et nommez-le "Envoyer une demande de discussion Cllama".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Créez un nœud Options et définissez `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Créez des messages, ajoutez un message système et un message utilisateur.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Créer un délégué pour recevoir les informations de sortie du modèle et les afficher à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Le texte traduit en français est le suivant :
"Le plan complet ressemble à ceci, en exécutant le plan, vous pouvez voir le message renvoyé à l'écran de jeu en imprimant un grand modèle."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###Le rédacteur utilise le chat OpenAI.

Ouvrez l'outil de chat Outils -> AIChatPlus -> AIChat, créez une nouvelle session de chat Nouveau Chat, configurez la session ChatApi sur OpenAI, configurez les paramètres de l'interface.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Commencer la discussion :

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Changer le modèle en gpt-4o/gpt-4o-mini permet d'utiliser la fonction d'analyse d'images d'OpenAI.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###Le logiciel utilise OpenAI pour traiter les images (créer/modifier/transformer).

Créer une nouvelle discussion avec image sur l'outil de messagerie, nommée New Image Chat, puis modifier les paramètres de la discussion en OpenAI et configurer les paramètres.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Créer une image

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Modifier l'image en changeant le type d'image de chat en "Modifier", puis télécharger deux images : une est l'image d'origine et l'autre est le masque où les zones transparentes (canal alpha 0) indiquent les endroits à modifier.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Modifier l'image en changeant le type de chat de l'image en Variation, puis télécharger une nouvelle image. OpenAI générera une variation de l'image initiale.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Utilisation de la modélisation de chat OpenAI dans le blueprint

Créez un nœud "Envoyer une demande de chat OpenAI dans le monde" en cliquant droit dans le plan.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Créez un nœud Options et définissez `Stream=true, Api Key="votre clé d'API provenant d'OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Créez des messages, ajoutez respectivement un message système et un message utilisateur.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Crée un délégué pour recevoir les informations produites par le modèle et les afficher à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Voici à quoi ressemble le plan complet. Exécutez-le et vous verrez le message renvoyé à l'écran de jeu lors de l'impression du grand modèle.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Utiliser OpenAI pour créer des images selon le plan.

Dans le schéma, créez un nœud en cliquant avec le bouton droit de la souris sur "Send OpenAI Image Request", puis définissez "In Prompt = 'a beautiful butterfly'"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Créez un nœud Options et définissez "Api Key="votre clé d'API provenant d'OpenAI"".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Attacher l'événement On Images et enregistrer les images sur le disque dur local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

Voici à quoi ressemble le blueprint complet. En exécutant le blueprint, vous pourrez voir l'image enregistrée à l'endroit spécifié.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###Le rédacteur utilise Azure.

Créer une nouvelle discussion (New Chat), changer ChatApi en Azure, et configurer les paramètres d'API Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Commencer la conversation.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###Utiliser Azure pour créer des images dans l'éditeur.

Créer une nouvelle session d'image (New Image Chat), changer ChatApi en Azure, et configurer les paramètres de l'API Azure. Remarque, si le modèle est dall-e-2, il est nécessaire de définir les paramètres Qualité et Style sur not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Commencez la discussion pour permettre à Azure de créer l'image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Utilisation de Chat Azure avec Azure Blueprint.

Créez le plan suivant, configurez les options Azure, cliquez sur Exécuter, et vous verrez s'afficher sur l'écran les informations de chat renvoyées par Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Utilisez Azure pour créer des images avec la blueprit.

Élaborez le plan suivant, configurez les options Azure, puis appuyez sur Exécuter. Si l'image est créée avec succès, vous verrez s'afficher le message "Create Image Done" à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

Selon le paramétrage du schéma ci-dessus, l'image sera enregistrée dans le chemin D:\Dwnloads\butterfly.png

## Claude

###Le rédacteur utilise Claude pour discuter et analyser les images.

Créer une nouvelle discussion (Nouveau Chat), remplacer ChatApi par Claude, et configurer les paramètres d'API de Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Commencer la discussion

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Utilisation des plans pour discuter et analyser les images avec Claude.

Dans la feuille de route, faites un clic droit pour créer un nœud `Envoyer une demande de chat à Claude`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Créez un nœud Options et définissez `Stream=true, Api Key="votre clé API de Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Créez des messages, créez une Texture2D à partir d'un fichier, puis créez AIChatPlusTexture à partir de cette Texture2D et ajoutez AIChatPlusTexture au message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Suivez le guide ci-dessus pour créer un Événement et afficher les informations à l'écran du jeu.

Le texte traduit en français est le suivant : 
"Le plan complet ressemble à ceci, en exécutant le plan, vous pouvez voir un message renvoyé à l'écran du jeu impressionnant le grand modèle."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Obtenir Ollama

Vous pouvez obtenir le package d'installation sur le site officiel d'Ollama pour une installation locale : [ollama.com](https://ollama.com/)

Vous pouvez utiliser Ollama via l'interface Ollama fournie par d'autres.

###Le gestionnaire utilise Ollama pour discuter et analyser des images.

Créer une nouvelle conversation (New Chat), changer ChatApi en Ollama, et configurer les paramètres Api d'Ollama. Pour une conversation textuelle, définir le modèle comme le modèle textuel, tel que llama3.1 ; pour le traitement d'images, choisir un modèle compatible avec la vision, par exemple moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Commencer la discussion.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Utiliser le plan Ollama pour discuter et analyser des images.

Élaborez le schéma suivant, configurez les options d'Ollama, appuyez sur Exécuter, et vous verrez s'afficher sur l'écran les informations de discussion renvoyées par Ollama.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###Utiliser Gemini dans l'éditeur.

Créer une nouvelle discussion (New Chat), remplacer ChatApi par Gemini, et configurer les paramètres d'API de Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Commencer la discussion

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###Utilisation de Gemini Chat dans les plans.

Élaborez le plan suivant, configurez les options Gemini, appuyez sur exécuter, et vous verrez s'afficher à l'écran les informations de chat renvoyées par Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

## Deepseek

###Le logiciel utilise Deepseek.

Créer une nouvelle discussion (New Chat), changer ChatApi en OpenAi, et configurer les paramètres de l'API de Deepseek. Ajouter un modèle de candidat appelé "deepseek-chat" et définir le modèle sur "deepseek-chat".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Commencer la conversation

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Utiliser Deepseek pour la discussion sur le blueprint

Élaborez le schéma suivant et configurez les options de requête relatives à Deepseek, y compris le modèle, l'URL de base, l'URL de point final, la clé API, etc. Cliquez sur Exécuter pour afficher les informations de chat renvoyées par Gemini à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##Journal des mises à jour

### v1.4.1 - 2025.01.04

####Résolution du problème

Le support de discussion permet d'envoyer uniquement des images sans message.

Réparer l'échec de l'envoi d'images à l'interface OpenAI.

Rectifiez les paramètres manquants Quality, Style et ApiVersion dans les paramètres de configuration des outils de chat OpanAI et Azure.

### v1.4.0 - 2024.12.30

####Nouvelle fonctionnalité

（Function expérimentale）Cllama (llama.cpp) prend en charge les modèles multimodaux et peut traiter des images.

Tous les paramètres des types de plans ont été assortis de conseils détaillés.

### v1.3.4 - 2024.12.05

####Nouvelle fonctionnalité

OpenAI supporte l'API de vision.

####Résolution du problème

Réparez l'erreur lorsqu'OpenAI stream=false.

### v1.3.3 - 2024.11.25

####Nouvelles fonctionnalités

Prend en charge l'UE-5.5.

####Résolution du Problème

Réparer le problème de certaines plans qui ne fonctionnent pas.

### v1.3.2 - 2024.10.10

####Résolution du problème.

Réparer le crash de cllama lors de l'arrêt manuel de la demande.

Résoudre le problème de la version de téléchargement win de la boutique où les fichiers ggml.dll et llama.dll ne peuvent pas être trouvés lors de l'emballage.

Vérifiez lors de la création de la requête si vous êtes dans le GameThread.

### v1.3.1 - 2024.9.30

####Nouvelle fonctionnalité

Ajouter un SystemTemplateViewer pour afficher et utiliser des centaines de modèles de paramètres système.

####Résolution du problème

Réparez le plugin téléchargé depuis le magasin, llama.cpp ne peut pas trouver la bibliothèque de liens

Corriger le problème de chemin trop long de LLAMACpp

Réparer l'erreur de lien llama.dll après avoir packagé Windows

Réparer le problème de chemin d'accès aux fichiers pour iOS/Android.

Réparer l'erreur de nom de réglage de Cllame

### v1.3.0 - 2024.9.23

####Nouvelle fonctionnalité majeure.

Intégré llama.cpp pour prendre en charge l'exécution hors ligne des grands modèles locaux.

### v1.2.0 - 2024.08.20

####Nouvelle fonctionnalité

Soutenir OpenAI Image Edit / Image Variation.

Prend en charge l'API Ollama, prend en charge l'obtention automatique de la liste des modèles pris en charge par Ollama.

### v1.1.0 - 2024.08.07

####Nouvelle fonctionnalité

Soutenir le plan.

### v1.0.0 - 2024.08.05

####Nouvelle fonctionnalité

Fonctionnalités de base complètes

Soutenir OpenAI, Azure, Claude, Gemini

Un outil de messagerie intégré avec un éditeur complet.

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez [**反馈**](https://github.com/disenone/wiki_blog/issues/new)Indiquez tout manquement. 
