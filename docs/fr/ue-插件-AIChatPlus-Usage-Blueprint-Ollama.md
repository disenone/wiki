---
layout: post
title: Ollama
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
description: Ollama
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Ollama" />

#Chapitre des plans - Ollama

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_all.png)

##Obtenir Ollama

Vous pouvez télécharger le package d'installation en local sur le site officiel d'Ollama : [ollama.com](https://ollama.com/)

Vous pouvez utiliser Ollama via l'API fournie par d'autres personnes.

Utilisez localement Ollama pour télécharger le modèle :

```shell
> ollama run qwen:latest
> ollama run moondream:latest
```

##Discussion par texte

Créez un nœud "Ollama Options", configurez les paramètres "Model" et "Base Url". Si Ollama est exécuté localement, "Base Url" est généralement "http://localhost:11434".

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_chat_1.png)

Connectez le nœud "Ollama Request" au nœud associé "Messages", cliquez sur Exécuter, et vous pourrez voir s'afficher à l'écran les messages de chat renvoyés par Ollama. Voir l'image pour plus de détails.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

##Générer du texte à partir d'une image llava

Ollama a également soutenu la bibliothèque llava, offrant ainsi la capacité de Vision.

Tout d'abord, obtenir le fichier du modèle multimodal :

```shell
> ollama run moondream:latest
```

Configurez le nœud "Options", définissez "Model" sur moondream:latest.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_1.png)

Charger l'image flower.png et définir le Message.

![flower.png](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_3.png)

Se connecter au nœud "Ollama Request", cliquer sur Exécuter, permettra d'afficher les messages de chat renvoyés par Ollama à l'écran.

![](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_4.png)

![](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_5.png)

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez laisser vos [**commentaires**](https://github.com/disenone/wiki_blog/issues/new)Indiquer tout élément manquant. 
