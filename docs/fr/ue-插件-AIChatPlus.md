---
layout: post
title: Documentation d'utilisation
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
description: Documentation d'utilisation
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documentation du plugin UE AIChatPlus

##Boutique d'extensions

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##Entrepôt public

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Présentation du plugin

Dernière version v2.0.0.

Ce plugin prend en charge les versions UE5.2 à UE5.7.

UE.AIChatPlus est un plugin UnrealEngine qui permet de communiquer avec divers services de chat GPT AI. Les services actuellement pris en charge incluent OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, et llama.cpp en mode local hors ligne. À l'avenir, davantage de fournisseurs de services seront ajoutés. Son implémentation repose sur des requêtes REST asynchrones, offrant des performances élevées et facilitant l'intégration de ces services de chat AI pour les développeurs UE.

En outre, UE.AIChatPlus inclut également un outil éditeur qui permet d'utiliser directement ces services de chat IA dans l'éditeur pour générer du texte et des images, analyser des images, etc.

##Fonctionnalités principales

**Nouveau !** Toutes les API prennent en charge ToolCall.

**Nouveau !** OpenAI/Azure prend en charge la reconnaissance vocale et la synthèse vocale.

**Nouveau !** Les schémas prennent désormais en charge Json.

**Nouveau !** La mise à jour hors ligne de AI llama.cpp est maintenant disponible en version b6792.

**Nouveau !** Prise en charge hors ligne de l'IA llama.cpp avec GPU Cuda et Metal.

**Nouveau !** Prise en charge de la synthèse vocale Gemini.

**API** : Prend en charge OpenAI, Azure OpenAI, Claude, Gemini, Ollama, llama.cpp, DeepSeek

**API en temps réel hors ligne** : Prend en charge l'exécution hors ligne de l'IA avec llama.cpp, compatible avec GPU Cuda et Metal.

**Texte vers texte** : Diverses API prennent en charge la génération de texte.

**Texte en image** : OpenAI Dall-E

**Conversion d'image en texte** : OpenAI Vision, Claude, Gemini, Ollama, llama.cpp

**Image à Image** : OpenAI Dall-E

**Reconnaissance vocale** : Gemini

**Blueprint** : Toutes les API et fonctionnalités prennent en charge les blueprints

**Éditeur ChatTool** : Un outil de chat AI éditeur riche en fonctionnalités et soigneusement conçu

**Appel asynchrone** : Toutes les API peuvent être appelées de manière asynchrone.

**Outils pratiques** : Divers outils pour les images et l'audio

##API pris en charge :

**llama.cpp hors ligne** : Intégré avec la bibliothèque llama.cpp, permet d'exécuter des modèles d'IA hors ligne ! Prend également en charge les modèles multimodaux (expérimental). Compatible avec Win64/Mac/Android/iOS. Supporte CUDA pour GPU et METAL.

**OpenAI** : /chat/completions, /completions, /images/generations, /images/edits, /images/variations  

*Note: The original text consists of API endpoint paths which remain the same in French, hence the unchanged translation.*

**Azure OpenAI** : /chat/completions, /images/generations

**Claude**：/messages、/complete

**Gemini** : :generateText、:generateContent、:streamGenerateContent  

Remarque : Les termes techniques comme ":generateText", ":generateContent", et ":streamGenerateContent" sont conservés tels quels, car ils font probablement référence à des méthodes ou fonctions spécifiques dans un contexte de programmation et n'ont pas d'équivalent standard en français.

**Ollama** : /api/chat, /api/generate, /api/tags

**DeepSeek** : /chat/complétions

##Mode d'emploi

[**Mode d'emploi - Plans techniques**](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

[**Mode d'emploi - C++**](ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

[**Mode d'emploi - Éditeur**](ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

[**Mode d'emploi - Emballage**](ue-插件-AIChatPlus-Usage-Package-GetStarted.md)

##Journal des modifications

[**Journal des modifications**](ue-插件-AIChatPlus-ChangeLogs.md)

##Assistance technique

**Commentaire** : N'hésitez pas à poser vos questions dans la section des commentaires ci-dessous.

**Courriel** : Vous pouvez également m'envoyer un email à cette adresse ( disenonec@gmail.com )

**discord**: Bientôt disponible

--8<-- "footer_fr.md"


> Ce message a été traduit à l'aide de ChatGPT. Veuillez laisser vos commentaires [**ici**](https://github.com/disenone/wiki_blog/issues/new)Signaler toute omission. 
