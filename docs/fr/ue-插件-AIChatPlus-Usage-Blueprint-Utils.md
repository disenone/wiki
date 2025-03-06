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

#Chapitre des plans - Noeuds de fonction

Le plugin propose des noeuds de fonctionnalités pratiques supplémentaires pour les blueprints.

##Cllama lié

"Vérifiez si Cllama est valide"：判断 Cllama llama.cpp 是否正常初始化.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

Vérifie si llama.cpp prend en charge le backend GPU dans l'environnement actuel.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Obtenir les backends pris en charge actuellement par llama.cpp"


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama Prepare ModelFile In Pak": Copie automatique des fichiers de modèle dans Pak vers le système de fichiers

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###Images associées

Convertir UTexture2D en Base64: Convertissez l'image UTexture2D au format Base64 PNG

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

Enregistrer UTexture2D sous forme de fichier .png.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

"Charger le fichier .png dans UTexture2D"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Dupliquer UTexture2D"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###Audio-related

"Charger le fichier .wav dans USoundWave"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

Convertir les données .wav en USoundWave : Convertir les données binaires wav en USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

Enregistrez USoundWave sous format .wav.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

"Obtenir les données brutes PCM de USoundWave": Convertir USoundWave en données audio binaire

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"Convert USoundWave to Base64" : Convertir USoundWave en données Base64

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Dupliquer USoundWave": Duplicate USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

Convertir les données de capture audio en USoundWave.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez [**Données de retour**](https://github.com/disenone/wiki_blog/issues/new)Identifier toute omission éventuelle. 
