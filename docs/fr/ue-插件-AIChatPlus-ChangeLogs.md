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

#Journal des versions du plug-in AIChatPlus de l'UE

## v1.6.0 - 2025.03.02

###Nouvelle fonctionnalité

Mettre à jour llama.cpp vers la version b4604.

Cllama supports GPU backends: cuda and metal

L'outil de discussion Cllama supporte l'utilisation de GPU

Prend en charge la lecture des fichiers de modèle emballés dans Pak.

### Bug Fix

Réparer le problème de crash de Cllama lors du rechargement pendant le raisonnement.

Réparez l'erreur de compilation iOS.

## v1.5.1 - 2025.01.30

###Nouvelles fonctionnalités

Autoriser uniquement les Gémeaux à envoyer des messages vocaux.

Optimiser la méthode pour obtenir des données PCM, décompresser les données audio lors de la génération de B64.

Demande d'ajouter deux rappels OnMessageFinished et OnImagesFinished.

Optimisez la méthode Gemini pour automatiquement obtenir la méthode en fonction de bStream.

Ajoutez quelques fonctions de blueprint pour faciliter la conversion de Wrapper en types réels et obtenir le message de réponse et les erreurs.

### Bug Fix

Corriger le problème des appels multiples de la fin de la demande.

## v1.5.0 - 2025.01.29

###Nouvelle fonctionnalité

Soutenez l'envoi de fichiers audio à Gemini.

Les outils de l'éditeur prennent en charge l'envoi d'audio et d'enregistrements.

### Bug Fix

Corrige le bogue de copie de session qui échoue.

## v1.4.1 - 2025.01.04

###Résolution du problème

Les outils de messagerie prennent en charge l'envoi de photos sans message.

Réparer l'échec de l'envoi d'images via l'API OpenAI.

Rectifier les paramètres manquants Quality, Style et ApiVersion dans les paramètres de configuration des outils de discussion OpanAI et Azure.

## v1.4.0 - 2024.12.30

###Nouvelle fonctionnalité

（Fonctionnalité expérimentale）Cllama(llama.cpp) supporte les modèles multimodaux et peut traiter les images

Tous les paramètres de type "Blueprint" ont été dotés de conseils détaillés.

## v1.3.4 - 2024.12.05

###Nouvelle fonctionnalité

OpenAI supporte l'API vision.

###Résolution du problème

Réparer l'erreur de OpenAI stream=false.

## v1.3.3 - 2024.11.25

###Nouvelle fonctionnalité

Prend en charge l'UE-5.5.

###Résolution du problème

Réparer le problème de certaines blueprints qui ne fonctionnent pas.

## v1.3.2 - 2024.10.10

###Correction de problème

Réparer le crash de cllama lors de l'arrêt manuel de la requête.

Corriger le problème de l'impossibilité de trouver les fichiers ggml.dll et llama.dll lors de l'emballage de la version Win du téléchargement du magasin.

Vérifiez lors de la création de la demande si vous êtes dans le GameThread.

## v1.3.1 - 2024.9.30

###Nouvelle fonctionnalité

Ajouter un SystemTemplateViewer pour visualiser et utiliser des centaines de modèles de paramètres système.

###Résolution du problème

Réparez les plugins téléchargés depuis le magasin, llama.cpp ne trouve pas la bibliothèque de liens.

Réparer le problème de chemin trop long de LLAMACpp.

Réparez l'erreur de lien llama.dll après avoir empaqueté Windows.

Résolution du problème de lecture du chemin d'accès aux fichiers sur iOS/Android.

Réparer l'erreur de nom de réglage de Cllame

## v1.3.0 - 2024.9.23

###Nouvelle fonctionnalité majeure

Intégré llama.cpp, supportant l'exécution hors ligne de grands modèles locaux.

## v1.2.0 - 2024.08.20

###Nouvelle fonctionnalité

Soutenir OpenAI Image Edit / Image Variation.

Prend en charge l'API Ollama, prend en charge l'obtention automatique de la liste des modèles pris en charge par Ollama.

## v1.1.0 - 2024.08.07

###Nouvelle fonctionnalité

Soutenir le plan d'action

## v1.0.0 - 2024.08.05

###Nouvelle fonctionnalité

Fonctionnalité de base complète

Soutenir OpenAI, Azure, Claude, Gemini

Fournit un éditeur de chat doté de fonctionnalités avancées.

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT. Veuillez laisser vos [**retours**](https://github.com/disenone/wiki_blog/issues/new)Identifier et signaler tout élément manquant. 
