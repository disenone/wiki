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

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 编辑器篇 - Get Started" />

#Article de l'éditeur - Commencer

##Outil de messagerie de l'éditeur

Dans la barre de menu, allez sur Outils -> AIChatPlus -> AIChat pour ouvrir l'éditeur de discussion proposé par le plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


Le logiciel prend en charge la génération de texte, les discussions textuelles, la génération d'images et l'analyse d'images.

L'interface de l'outil est approximativement comme suit:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

##Les caractères chinois "主要功能" se traduisent en français par "fonction principale".

* **Modèle hors ligne**: Intégration de la bibliothèque llama.cpp, prenant en charge l'exécution hors ligne locale des grands modèles.

* **Chat textuel** : Cliquez sur le bouton `Nouvelle discussion` en bas à gauche pour créer une nouvelle session de chat textuel.

* **Image generation**: Cliquez sur le bouton `New Image Chat` en bas à gauche pour créer une nouvelle session de génération d'images.

* **Analyse d'images**: Certaines fonctions de chat de "Nouveau Chat" prennent en charge l'envoi d'images, par exemple Claude, Google Gemini. Cliquez sur les icônes 🖼️ ou 🎨 au-dessus de la zone de saisie pour charger l'image à envoyer.

* **Traitement audio** : L'outil permet de lire des fichiers audio (.wav) et d'enregistrer des sons, afin de pouvoir discuter avec une intelligence artificielle en utilisant l'audio obtenu.

* **Définir le rôle de discussion actuel** : La liste déroulante en haut de la fenêtre de discussion permet de choisir le rôle depuis lequel vous envoyez des messages, vous permettant de simuler différents rôles pour ajuster la conversation avec l'IA.

* **Effacer la conversation** : Le bouton ❌ en haut de la fenêtre de chat permet de supprimer l'historique des messages de la conversation en cours.

*Modèle de conversation* : Intègre des centaines de modèles de configurations de conversation pour faciliter la gestion des problèmes courants.

**Paramètres globaux** : En cliquant sur le bouton `Paramètres` en bas à gauche, vous pouvez ouvrir la fenêtre des paramètres globaux. Vous pourrez y définir le chat textuel par défaut, le service API de génération d'images, et configurer les paramètres spécifiques à chaque service API. Les paramètres seront automatiquement enregistrés dans le répertoire du projet `$(ProjectFolder)/Saved/AIChatPlusEditor`.

**Paramètres de la conversation** : En cliquant sur l'icône de paramètres située en haut de la fenêtre de chat, vous pouvez ouvrir la fenêtre des paramètres de la conversation en cours. Vous pouvez y modifier le nom de la conversation, le service API utilisé et personnaliser les paramètres spécifiques de l'API pour chaque conversation. Les paramètres de la conversation sont automatiquement enregistrés dans `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Modifier le contenu de la conversation : Lorsque vous survolez le contenu de la conversation avec la souris, un bouton de paramétrage du contenu individuel de la conversation apparaît, ce qui permet de régénérer le contenu, le modifier, le copier, le supprimer, le régénérer en bas (pour les contenus avec des utilisateurs en tant que personnages).

* **Visionneuse d'images** : Pour la génération d'images, en cliquant sur une image, une fenêtre de visualisation d'images (Visionneuse) s'ouvrira, prenant en charge l'enregistrement d'images au format PNG/Texture UE, permettant de visualiser directement le Texture dans le navigateur de contenu pour une utilisation facile des images dans l'éditeur. Il est également possible de supprimer des images, de les regénérer, de continuer à générer plus d'images, entre autres fonctionnalités. Pour les éditeurs sous Windows, la copie d'images est également prise en charge, permettant de copier directement une image dans le presse-papiers pour une utilisation aisée. Les images générées lors d'une session sont automatiquement enregistrées dans le dossier de chaque session, généralement à l'emplacement suivant : `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.





Paramètres généraux :

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Paramètres de conversation :

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modifier le contenu de la discussion :

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visualiseur d'images :

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Utilisation de modèles de grande taille hors ligne

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Modèle de conversation

![system template](assets/img/2024-ue-aichatplus/system_template.png)

##Utilise un modèle hors ligne Cllama avec l'outil de l'éditeur (llama.cpp).

Voici comment utiliser le modèle hors ligne llama.cpp dans l'outil d'édition AIChatPlus.

Téléchargez d'abord le modèle hors ligne depuis le site web de HuggingFace : [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Placez le modèle dans un dossier spécifique, par exemple dans le répertoire du projet de jeu Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Ouvrez l'outil d'édition AIChatPlus: Outils -> AIChatPlus -> AIChat, créez une nouvelle session de discussion et ouvrez la page des paramètres de la session.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Définissez l'API sur Cllama, activez les paramètres d'API personnalisés, ajoutez un chemin de recherche de modèle et sélectionnez le modèle.


![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Commencer à discuter!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

##Utiliser l'outil d'éditeur pour traiter les images avec le modèle hors ligne Cllama (llama.cpp).

Téléchargez le modèle hors ligne MobileVLM_V2-1.7B-GGUF depuis le site Web de HuggingFace et placez-le également dans le répertoire Content/LLAMA : [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)Translate these text into French language:

和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but there is no text to translate.

Définir le modèle de la session :

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)


Envoyer une image pour commencer la discussion

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

##Le rédacteur utilise OpenAI pour discuter.

Ouvrez l'outil de discussion Outils -> AIChatPlus -> AIChat, créez une nouvelle conversation New Chat, et configurez la session ChatApi sur OpenAI, en définissant les paramètres de l'interface.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Commencer la discussion :

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Changer le modèle en gpt-4o / gpt-4o-mini permet d'utiliser la fonctionnalité de vision par ordinateur d'OpenAI pour analyser les images.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

##Utilisation par l'éditeur d'OpenAI pour traiter les images (création/modification/variation)

Créez une nouvelle conversation d'image New Image Chat dans l'outil de messagerie, modifiez les paramètres de la conversation en OpenAI et configurez les paramètres.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Créer une image

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Please translate the following text into French:

* Edit the image by changing the "Image Chat Type" to "Edit", and upload two pictures. One should be the original image, and the other should be a mask with transparent areas (where the alpha channel is 0) indicating the areas that need to be edited.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Modifier l'image en changeant le type de conversation de "Image Chat Type" en "Variation", puis télécharger une image. OpenAI renverra une variante de l'image originale.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

##L'éditeur utilise Azure.

Créer une nouvelle conversation (New Chat), remplacer ChatApi par Azure, et configurer les paramètres de l'API Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Commencer la conversation

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

##Le rédacteur utilise Azure pour créer des images.

Créer une nouvelle session d'image (New Image Chat), changer ChatApi en Azure, et configurer les paramètres d'API d'Azure. Remarque : si le modèle est dall-e-2, il faut définir les paramètres Quality et Stype sur not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Commencez la conversation pour que Azure crée une image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

##Le rédacteur utilise Claude pour discuter et analyser des images.

Créer une nouvelle discussion (New Chat), changer ChatApi en Claude, et configurer les paramètres Api de Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Commencer la conversation

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

##Le logiciel utilise Ollama pour discuter et analyser des images.

Créer une nouvelle discussion (New Chat), changer ChatApi en Ollama et configurer les paramètres Api d'Ollama. Pour une conversation textuelle, définir le modèle en tant que modèle textuel, comme llama3.1 ; pour le traitement des images, choisir un modèle prenant en charge la vision, par exemple moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Commencer la discussion

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)


###Utilisons Gemini comme éditeur.

Créez une nouvelle discussion (New Chat), remplacez ChatApi par Gemini, et configurez les paramètres d'Api de Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Commencer la conversation

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

##L'éditeur utilise Gemini pour envoyer de l'audio.

Choisissez de lire l'audio à partir du fichier / de l'actif / de l'enregistrement du microphone pour générer l'audio à envoyer.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

Commencer la conversation

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

##Le logiciel utilise Deepseek.

Créer une nouvelle session (New Chat), remplacer ChatApi par OpenAi, et configurer les paramètres Api de Deepseek. Ajouter un nouveau modèle de candidat appelé deepseek-chat, et définir le modèle comme deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Commencer la conversation

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez donner votre [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Signalez tout oubli. 
