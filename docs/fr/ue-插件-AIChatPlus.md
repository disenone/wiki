---
layout: post
title: Document d'explication
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
description: Document d'explication
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documentation du plug-in UE AIChatPlus

##Magasin d'extensions

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##Entrepôt public

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Présentation du plug-in

La dernière version v1.6.0.

Ce plug-in prend en charge UE5.2 - UE5.5.

UE.AIChatPlus est un plugin Unreal Engine qui permet de communiquer avec divers services de discussion GPT AI. Les services actuellement pris en charge incluent OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, ainsi qu'une version locale hors ligne llama.cpp. À l'avenir, davantage de fournisseurs de services seront pris en charge. Son implémentation repose sur des requêtes REST asynchrones, offrant une performance efficace et permettant aux développeurs d'Unreal Engine d'intégrer facilement ces services de discussion AI.

Le UE.AIChatPlus comprend également un outil d'édition qui permet d'utiliser directement ces services de chat AI dans l'éditeur pour générer du texte et des images, analyser des images, etc.

##Fonctions principales

**Nouveau !** La mise à jour de l'IA hors ligne llama.cpp est passée à la version b4604.

**Nouveau !** Le fichier AI llama.cpp prend désormais en charge les GPU Cuda et Metal hors ligne.

Nouveau ! Prend en charge la transcription vocale en texte pour Gemini.

**API** : Supporte OpenAI, Azure OpenAI, Claude, Gemini, Ollama, llama.cpp, DeepSeek.

**API temps réel hors ligne** : prend en charge l'exécution hors ligne de l'IA avec llama.cpp, avec prise en charge de CUDA GPU et Metal.

Traduisez ce texte en français :

**文本转文本** : Prise en charge de diverses API pour la génération de texte.

**Text-to-Image** : OpenAI Dall-E

**Transcription d'image** : OpenAI Vision, Claude, Gemini, Ollama, llama.cpp

**Image to Image**: OpenAI Dall-E

**Texte traduit** : Gemini

**Blueprint** : Tous les API et fonctionnalités supportent le blueprint.

Outil de messagerie de l'éditeur : un outil de messagerie AI riche en fonctionnalités et soigneusement conçu.

**Appel asynchrone** : Toutes les API peuvent être appelées de manière asynchrone.

Outils pratiques : divers outils d'images et de son.

##API supportée :

**Offline llama.cpp**: Intégré à la bibliothèque llama.cpp, permet d'exécuter hors ligne des modèles d'IA ! Prend aussi en charge les modèles multimodaux (expérimental). Compatible avec Win64/Mac/Android/IOS. Prend en charge CUDA et METAL GPU.

OpenAI: /chat/completions, /completions, /images/generations, /images/edits, /images/variations

Azure OpenAI : /chat/completions, /images/generations

**Claude**：/messages、/complete

**Gemini**：:générerTexte、:générerContenu、:générerContenuEnStreaming

**Ollama**：/api/chat、/api/generate、/api/tags

**DeepSeek**：/chat/completions

##Instructions d'utilisation

[**Instructions d'utilisation - Chapitre sur les plans**](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

Veuillez traduire ce texte en français : 

[**Guide d'utilisation - Partie C++**](ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

[**Instructions d'utilisation - Section éditeur**](ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

##Changer les journaux

(ue-插件-AIChatPlus-ChangeLogs.md)

##Assistance technique

**Commentaire** : N'hésitez pas à poser vos questions dans la section des commentaires ci-dessous.

**Email**: Vous pouvez également m'envoyer un email à l'adresse suivante : disenonec@gmail.com

**discord** : Bientôt disponible

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Identifiez toute omission éventuelle. 
