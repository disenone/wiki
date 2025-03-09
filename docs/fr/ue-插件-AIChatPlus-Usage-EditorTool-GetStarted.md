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

#Traduction en français : 

Article de l'éditeur - Pour commencer

##Outil de messagerie de l'éditeur

La barre de menus Outils -> AIChatPlus -> AIChat permet d'ouvrir l'éditeur de chat fourni par le plug-in.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


Le logiciel propose des fonctionnalités de génération de texte, de messagerie textuelle, de création d'images et d'analyse d'images.

L'interface de l'outil est approximativement la suivante :

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

##Fonction principale

**Modèle en ligne hors connexion** : Intégration de la bibliothèque llama.cpp pour prendre en charge l'exécution hors ligne de grands modèles locaux

**Chat textuel** : Cliquez sur le bouton `Nouveau Chat` en bas à gauche pour créer une nouvelle conversation de chat textuel.

**Génération d'image** : Cliquez sur le bouton `Nouvelle conversation d'image` en bas à gauche pour créer une nouvelle session de génération d'image.

**Analyse d'images**: Certaines fonctions de messagerie de `New Chat` prennent en charge l'envoi d'images, telles que Claude, Google Gemini. Cliquez sur l'icône 🖼️ ou 🎨 au-dessus de la zone de texte pour charger l'image à envoyer.

**Traitement audio** : L'outil permet de lire des fichiers audio (.wav) et d'enregistrer des sons, afin de pouvoir discuter avec une Intelligence Artificielle en utilisant l'audio obtenu.

**Définir le rôle du personnage de discussion actuel** : le menu déroulant en haut de la fenêtre de discussion peut être utilisé pour définir le personnage qui envoie actuellement du texte, permettant de simuler différents rôles pour ajuster la discussion de l'IA.

**Effacer la conversation** : Le bouton ❌ en haut de la fenêtre de discussion permet d'effacer l'historique des messages actuel de la conversation.

**Modèle de dialogue** : Intègre des centaines de modèles de dialogues prédéfinis pour faciliter le traitement des problèmes courants.

**Paramètres globaux** : En cliquant sur le bouton `Paramètres` en bas à gauche, vous pouvez ouvrir la fenêtre des paramètres globaux. Vous pouvez définir les paramètres par défaut pour le chat textuel, le service API de génération d'images, et spécifier les paramètres précis pour chaque service API. Les réglages seront automatiquement sauvegardés dans le chemin du projet `$(ProjectFolder)/Saved/AIChatPlusEditor`.

**Paramètres de conversation** : En cliquant sur l'icône des paramètres en haut de la fenêtre de discussion, vous pouvez ouvrir la fenêtre de paramètres de la conversation en cours. Vous pouvez modifier le nom de la conversation, le service API utilisé pour la conversation, et spécifier des paramètres spécifiques à chaque conversation pour l'utilisation de l'API. Les paramètres de la conversation sont automatiquement enregistrés dans `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Modifier le contenu de la conversation : lorsque vous survolez le contenu de la conversation avec la souris, un bouton de réglage pour ce contenu s'affiche. Vous pouvez générer à nouveau, modifier, copier, supprimer le contenu ou générer un nouveau contenu en dessous (pour les contenus des utilisateurs).

**Visualisation des images** : Pour la génération d'images, cliquer sur une image ouvrira la fenêtre de visionnage d'images (ImageViewer), qui prend en charge l'enregistrement d'images au format PNG/Texture UE, lesquelles peuvent être visualisées directement dans le navigateur de contenu (Content Browser), facilitant ainsi leur utilisation dans l'éditeur. De plus, il est possible de supprimer des images, de regénérer des images, et de continuer à en générer davantage. Pour les utilisateurs de l'éditeur sous Windows, il est également possible de copier des images pour les coller directement dans le presse-papiers, facilitant ainsi leur utilisation. Les images générées lors de la session seront automatiquement sauvegardées dans le dossier de chaque session, généralement situé à l'adresse suivante : $(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images.

Paramètres globaux :

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Paramètres de la conversation :

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modifier le contenu de la conversation :

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Visionneuse d'images :

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Utilisation de modèles hors ligne à grande échelle

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Modèle de conversation

![system template](assets/img/2024-ue-aichatplus/system_template.png)

##Utilisation de l'outil d'édition avec le modèle hors ligne Cllama (llama.cpp)

Voici comment utiliser le modèle hors ligne llama.cpp dans l'outil éditeur AIChatPlus.

Tout d'abord, téléchargez le modèle hors ligne depuis le site de HuggingFace : [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Placez le modèle dans un dossier spécifique, par exemple dans le répertoire Content/LLAMA du projet de jeu.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Ouvrez l'outil d'édition AIChatPlus : Outils -> AIChatPlus -> AIChat, créez une nouvelle session de chat et ouvrez la page de paramètres de la session.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Configurer l'API sur Cllama, activer les Paramètres d'API Personnalisés, ajouter un chemin de recherche de modèle et sélectionner un modèle.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Commencez la conversation !!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

##Utilisation de l'outil d'édition avec le modèle hors ligne Cllama (llama.cpp) pour traiter les images.

Téléchargez le modèle hors ligne MobileVLM_V2-1.7B-GGUF depuis le site web de HuggingFace et mettez-le également dans le répertoire Content/LLAMA : [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but there is no text to translate.

Définir le modèle de la session :

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Commencez la conversation en envoyant une photo.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

##L'éditeur utilise OpenAI pour discuter.

Ouvrez l'outil de messagerie Tools -> AIChatPlus -> AIChat, créez une nouvelle discussion New Chat, configurez la session ChatApi avec OpenAI, définissez les paramètres de l'interface.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Commencer la conversation :

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Changer le modèle en gpt-4o / gpt-4o-mini, vous permet d'utiliser les fonctionnalités de vision artificielle d'OpenAI pour analyser des images.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

##Le logiciel utilise OpenAI pour traiter les images (créer/modifier/altérer).

Créer une nouvelle conversation avec images sur l'outil de messagerie, nommée New Image Chat, configurer la conversation en tant que OpenAI, et définir les paramètres.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Créer une image

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Modifier l'image en remplaçant "Type d'image de chat" par "Edit", puis télécharger deux images : une originale et une autre avec les zones transparentes (canal alpha à 0) indiquant les emplacements à modifier.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Modifier l'image en changeant le type de conversation de "Image Chat" à "Variation" et télécharger une image. OpenAI renverra une variante de l'image d'origine.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

##Utiliser Azure dans l'éditeur.

Créer une nouvelle conversation (New Chat), changer ChatApi pour Azure et configurer les paramètres d'API d'Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Commencer la discussion

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

##Le logiciel utilise Azure pour créer des images.

Créer une nouvelle session d'image (New Image Chat), changer ChatApi en Azure, et configurer les paramètres de l'API Azure. Notez que si le modèle est dall-e-2, les paramètres Quality et Stype doivent être définis sur not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Commencez la discussion pour que Azure crée une image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

##Le logiciel utilise Claude pour discuter et analyser les images.

Créer une nouvelle conversation, changer ChatApi en Claude, et configurer les paramètres de l'API de Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Commencer la discussion

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

##Le rédacteur utilise Ollama pour discuter et analyser les images.

Créer une nouvelle conversation (New Chat), changer ChatApi en Ollama, et configurer les paramètres Api d'Ollama. Si c'est une conversation textuelle, définir le modèle comme modèle de texte, tel que llama3.1 ; s'il est nécessaire de traiter des images, définir le modèle comme un modèle prenant en charge la vision, comme moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Commencer la discussion

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Utiliser Gemini dans l'éditeur.

Créer une nouvelle conversation (New Chat), renommer ChatApi en Gemini, et configurer les paramètres Api de Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Commencer la discussion

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

##Le logiciel utilise Gemini pour envoyer des fichiers audio.

Lire l'audio à partir du fichier / lire l'audio à partir de l'Asset / enregistrer l'audio depuis le microphone, pour générer l'audio à envoyer.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

Commencez la conversation.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

##L'éditeur utilise Deepseek.

Créer une nouvelle conversation (New Chat), changer ChatApi par OpenAi et configurer les paramètres de l'API Deepseek. Ajouter un modèle de candidat appelé deepseek-chat et définir le modèle comme deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Commencer la discussion

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez laisser vos commentaires dans la section [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Signalez tout oubli. 
