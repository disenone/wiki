---
layout: post
title: Nœud de fonction
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
description: Nœud de fonction
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - 功能节点" />

#Chapitre des plans - Nœuds de fonction

Le plugin propose des noeuds de fonctionnalités pratiques supplémentaires pour les blueprints.

##Cllama related

"Cllama Is Valid"：Vérifier si Cllama llama.cpp est initialisé correctement

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Vérifie si le fichier llama.cpp est compatible avec le backend GPU dans l'environnement actuel."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Obtenir les backends pris en charge par llama.cpp actuel."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Prépare le fichier modèle Cllama dans Pak": Automatically copies model files from Pak to the file system.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

##Images associées.

"Convert UTexture2D to Base64": Convertir une image UTexture2D en format base64 png

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

Enregistrer UTexture2D sous forme de fichier .png.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

Charger le fichier .png dans UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Dupliquer UTexture2D"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

##Audio related.

Charger le fichier .wav dans USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

Convertir les données .wav en USoundWave: Convertir les données binaires .wav en USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

Enregistrez USoundWave sous forme de fichier .wav.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

"Obtenez les données brutes PCM de USoundWave": Convertir USoundWave en données audio binaires

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"Convert USoundWave to Base64" : Convertir USoundWave en données Base64

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Dupliquer USoundWave"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

Transformer les données de capture audio en USoundWave.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT. Veuillez [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Indiquer tout oubli. 
