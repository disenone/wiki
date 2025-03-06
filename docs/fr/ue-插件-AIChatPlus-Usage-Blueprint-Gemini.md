---
layout: post
title: Gemini
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
description: Gemini
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Gemini" />

#Chapitre des plans - Gémeaux

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_all.png)

###Chat texte

Créez un nœud "Options de discussion Gemini", définissez les paramètres "Modèle", "Clé API".

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_chat_1.png)

Créez un nœud "Demande de discussion Gemini", connectez-le aux nœuds "Options" et "Messages", puis cliquez sur Exécuter. Vous verrez s'afficher sur l'écran les informations de discussion renvoyées par Gemini, comme illustré :

![](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###Génération de texte à partir d'images

Créez également un nœud "Gemini Chat Options", puis configurez les paramètres "Model" et "Api Key".

Lire l'image flower.png depuis le fichier et la mettre en place dans "Messages".

![flower.png](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_vision_1.png)

Créez un nœud "Gemini Chat Request", cliquez sur Exécuter, et vous pourrez voir s'afficher sur l'écran les informations de chat renvoyées par Gemini, comme illustré ci-dessous :

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_vision_2.png)

###Transcription audio

Gemini soutient la conversion du son en texte.

Créez le schéma suivant, configurez le chargement audio, configurez les options Gemini, cliquez sur Exécuter, et vous verrez s'afficher sur l'écran les informations de chat renvoyées après le traitement audio par Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez [**fournir vos commentaires**](https://github.com/disenone/wiki_blog/issues/new)Indiquez tout oubli. 
