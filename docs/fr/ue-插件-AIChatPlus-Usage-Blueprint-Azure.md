---
layout: post
title: Azure
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
description: Azure
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Azure" />

#Chapitre des plans - Azure

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_all.png)

La façon dont Azure est utilisé est très similaire à OpenAI, donc voici une brève introduction.

##Discussion par texte

Créez le nœud "Azure Chat Options", en définissant les paramètres "Deployment Name", "Base URL" et "API Key".

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_chat_1.png)

Créez un nœud associé à "Messages" et connectez-le à "Azure Chat Request". Cliquez sur Exécuter pour afficher les informations de chat renvoyées par Azure à l'écran. Voir l'image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

##Créer une image

Créez un nœud "Options d'image Azure", configurez les paramètres "Nom du déploiement", "URL de base", "Clé d'API".

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_image_1.png)

Configurez les nœuds tels que "Azure Image Request", cliquez sur exécuter, et vous verrez s'afficher sur l'écran les informations de chat renvoyées par Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

Selon la configuration du schéma ci-dessus, l'image sera enregistrée dans le dossier D:\Dwnloads\butterfly.png.

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez donner votre [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Identifier toute omission. 
