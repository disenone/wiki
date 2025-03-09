---
layout: post
title: Document d'instructions
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

#Document d'instructions de l'extension AIChatPlus de l'UE

##Boutique de modules complémentaires

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##Entrepôt public.

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Présentation du module complémentaire

La dernière version v1.6.0.

Ce plugin est compatible avec UE5.2 - UE5.5.

UE.AIChatPlus est un plug-in pour UnrealEngine qui permet de communiquer avec divers services de discussion AI GPT. Les services actuellement pris en charge sont OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama et une version locale hors ligne de llama.cpp. À l'avenir, il prendra également en charge d'autres fournisseurs de services. Son implémentation repose sur des requêtes REST asynchrones, offrant ainsi des performances élevées et permettant aux développeurs d'Unreal Engine de se connecter facilement à ces services de discussion AI.

Le UE.AIChatPlus comprend également un outil d'édition qui permet d'utiliser directement ces services de discussion IA dans l'éditeur, pour générer du texte et des images, analyser des images, etc.

##Les caractéristiques principales

**Nouveau!** Le fichier AI llama.cpp hors ligne a été mis à jour vers la version b4604.

**Nouveau !** Prise en charge GPU Cuda et Metal pour AI llama.cpp hors ligne.

**Nouveau !** Prise en charge du service de transcription vocale en texte Gemini.

**API**：Prise en charge d'OpenAI, Azure OpenAI, Claude, Gemini, Ollama, llama.cpp, DeepSeek

**API en temps réel hors ligne** : prend en charge l'exécution hors ligne de l'IA avec llama.cpp, compatible avec les technologies GPU Cuda et Metal.

Traduisez ce texte en français :

**文本转文本** : Plusieurs API prennent en charge la génération de texte.

**Translation**: **Transformation de texte en image** : OpenAI Dall-E

**Conversion d'image en texte** : OpenAI Vision, Claude, Gemini, Ollama, llama.cpp

**Image to Image**: OpenAI Dall-E

**Transcription vocale** : Gemini

**Blueprint** : toutes les API et fonctionnalités prennent en charge le blueprint

Outil de discussion de l'éditeur : un outil de chat AI sophistiqué et riche en fonctionnalités, spécialement conçu.

**Appel asynchrone** : Toutes les API peuvent être appelées de manière asynchrone

**Outils pratiques** : divers outils d'image et audio

##API supportée :

**llama.cpp hors ligne**: Intégrez la bibliothèque llama.cpp pour exécuter hors ligne des modèles d'IA ! Prend également en charge les modèles multi-modaux (expérimental). Compatible avec Win64/Mac/Android/IOS. Prise en charge des GPU CUDA et METAL.

OpenAI: /chat/completions, /completions, /images/generations, /images/edits, /images/variations

Azure OpenAI : /chat/completions, /images/generations

Claude：/messages、/complete

**Gémeaux** : generateText, generateContent, streamGenerateContent

**Ollama**：/api/chat、/api/generate、/api/tags

**Ollama**：/api/chat、/api/generate、/api/tags

**DeepSeek**：/chat/completions

##Instructions d'utilisation

[**Instructions d'utilisation - chapitre sur la feuille de route**](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

(ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

(ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

(ue-插件-AIChatPlus-Usage-Package-GetStarted.md)

##Changer le journal

[**Changelog**](ue-插件-AIChatPlus-ChangeLogs.md)

##Support technique

**Commentaire** : N'hésitez pas à laisser un message dans la section des commentaires ci-dessous si vous avez des questions.

**Email**: Vous pouvez également m'envoyer un email à l'adresse suivante : disenonec@gmail.com

**discord**: Bientôt disponible

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez donner votre [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Identifier toute omission possible. 
