---
layout: post
title: Journal des versions
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
description: Journal des versions
---

<meta property="og:title" content="UE 插件 AIChatPlus 版本日志" />

#Journal des versions du plugin UE AIChatPlus

## v1.8.0 - 2025.11.03

Mettre à jour llama.cpp b6792

## v1.7.0 - 2025.07.06

Mettre à jour llama.cpp b5536

Prend en charge l'UE5.6.

Android发布后会导致崩溃，禁用llama.cpp。

## v1.6.2 - 2025.03.17

###Nouvelle fonctionnalité

Cllama a augmenté le paramètre KeepContext par défaut à false, le Contexte est automatiquement détruit à la fin du Chat.

The translation into French is:

* Cllama a ajouté le paramètre KeepAlive, ce qui peut réduire la lecture répétée du modèle.

## v1.6.1 - 2025.03.07

### Bug Fix

OpenAI Image Chat supporte l'entrée d'images selon le plan.

Outil d'édition Cllama mmproj permettant le modèle vide.

## v1.6.0 - 2025.03.02

###Nouvelle fonctionnalité

Mettre à jour llama.cpp vers la version b4604.

Cllama supporte les backends GPU : cuda et metal

L'outil de discussion Cllama prend en charge l'utilisation du GPU.

Prend en charge la lecture des fichiers de modèles empaquetés dans Pak.

### Bug Fix

Réparer le problème de plantage de Cllama lors du rechargement pendant le raisonnement.

Répare les erreurs de compilation iOS.

## v1.5.1 - 2025.01.30

###Nouvelle fonctionnalité

Autoriser uniquement les appareils Gemini à diffuser des fichiers audio.

Optimisez la méthode d'obtention des données PCM pour décompresser les données audio lors de la génération de B64.

Demander d'ajouter deux rappels OnMessageFinished et OnImagesFinished.

Optimiser la méthode Gemini, obtenir automatiquement le méthode en fonction de bStream.

Ajouter quelques fonctions de blueprint pour faciliter la conversion du Wrapper en type réel, ainsi que pour obtenir le message de réponse et l'erreur.

### Bug Fix

Réparer le problème d'appels multiples de la fin de la demande.

## v1.5.0 - 2025.01.29

###Nouvelle fonctionnalité

Soutenir l'envoi audio à Gemini.

Les outils de l'éditeur prennent en charge l'envoi d'audio et d'enregistrements.

### Bug Fix

Corriger le bug de l'échec de la copie de session.

## v1.4.1 - 2025.01.04

###Correction de problème

L'outil de messagerie prend en charge l'envoi d'images sans message.

Résolution de l'échec de la résolution du problème de l'envoi d'images de l'interface OpenAI.

Réparer les paramètres manquants Quality, Style et ApiVersion des outils de chat OpenAI et Azure.

## v1.4.0 - 2024.12.30

###Nouvelle fonctionnalité

* （機能試験中）Cllama (llama.cpp) prend en charge les modèles multimodaux et peut traiter les images

Tous les paramètres de type Blueprint ont été dotés de descriptions détaillées.

## v1.3.4 - 2024.12.05

###Nouvelle fonctionnalité.

OpenAI prend en charge l'API de vision.

###Résolution du problème

Réparer l'erreur lorsqu'OpenAI stream=false.

## v1.3.3 - 2024.11.25

###Nouvelle fonctionnalité

Prend en charge l'UE-5.5

###Résolution du problème

Réparer le problème de certaines Blueprints qui ne fonctionnent pas.

## v1.3.2 - 2024.10.10

###Réparation de problèmes

Réparer le plantage de cllama lors de l'arrêt manuel de la demande.

Résoudre le problème de non-localisation des fichiers ggml.dll llama.dll dans la version téléchargeable de Win d'une application de magasin.

Vérifier dans le GameThread lors de la création de la requête, CreateRequest.

## v1.3.1 - 2024.9.30

###Nouvelle fonctionnalité

Ajouter un SystemTemplateViewer pour visualiser et utiliser des centaines de modèles de paramètres système.

###Résolution de problèmes

Réparez le plugin téléchargé depuis le magasin, llama.cpp ne trouve pas la bibliothèque de liens.

Réparer le problème de chemin trop long dans LLAMACpp

Réparer l'erreur de lien llama.dll après l'emballage de Windows

Réparer le problème de chemin d'accès aux fichiers sur iOS/Android.

Réparer l'erreur de nom de configuration de Cllame

## v1.3.0 - 2024.9.23

###Nouvelle fonctionnalité majeure

Intégration de llama.cpp pour prendre en charge l'exécution hors ligne locale de modèles volumineux.

## v1.2.0 - 2024.08.20

###Nouvelle fonctionnalité

Soutenir OpenAI Image Edit/Image Variation.

Prend en charge l'API Ollama, permettant d'obtenir automatiquement la liste des modèles pris en charge par Ollama.

## v1.1.0 - 2024.08.07

###Nouvelle fonctionnalité

Soutenir le plan d'action

## v1.0.0 - 2024.08.05

###Nouvelle fonctionnalité

Fonctionnalité de base complète

Supporter OpenAI, Azure, Claude, Gemini

Apporter un outil de messagerie doté d'un éditeur complet intégré

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez donner votre [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Identifier tout oubli. 
