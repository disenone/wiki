---
layout: post
title: Claude
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
description: Claude
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Claude" />

#Chapitre du plan - Claude

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/claude_all.png)

##Discussion textuelle

Créez un nœud "Options", définissez les paramètres "Modèle", "Clé API", "Version Anthropic".

![](assets/img/2024-ue-aichatplus/usage/blueprint/claude_chat_1.png)

Rassemblez le nœud "Demande de Claude" avec le nœud associé "Messages", cliquez sur exécuter, et vous verrez s'afficher sur l'écran les informations de chat renvoyées par Claude.

![](assets/img/2024-ue-aichatplus/usage/blueprint/claude_chat_2.png)

##Créer du texte à partir d'une image

Claude soutient également la fonction Vision.

Créez un noeud "Envoyer une demande de discussion à Claude" en cliquant droit dans le plan.

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Créez un nœud "Options" et définissez `Stream=true, Api Key="votre clé API de Clude", Max Output Tokens=1024`.

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Créez des messages, créez une Texture2D à partir d'un fichier, puis créez un AIChatPlusTexture à partir de la Texture2D, et ajoutez ce AIChatPlusTexture au message.

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Événement et afficher les informations sur l'écran du jeu.

Le blueprint complet ressemble à ceci, en exécutant le blueprint, vous pourrez voir l'écran du jeu afficher le message renvoyé par le grand modèle d'impression.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)


--8<-- "footer_fr.md"


> Ce message a été traduit en français en utilisant ChatGPT. Veuillez donner votre [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Veuillez signaler tout oubli. 
