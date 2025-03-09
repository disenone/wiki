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
description: Journaux de version
---

<meta property="og:title" content="UE 插件 AIChatPlus 版本日志" />

#Journal des versions du plug-in UE AIChatPlus

## v1.6.1 - 2025.03.07

### Bug Fix

OpenAI Image Chat Blueprint prend en charge l'importation d'images.

Outil d'édition Cllama mmproj permettant un modèle vide.

## v1.6.0 - 2025.03.02

###Nouvelle fonctionnalité

Mettre à jour le fichier llama.cpp vers la version b4604.

Cllama supporte les GPU backends : cuda et metal

L'outil de discussion Cllama prend en charge l'utilisation de GPU.

Prend en charge la lecture des fichiers de modèle empaquetés dans un fichier Pak.

### Bug Fix

Réparer le problème de plantage de Cllama lors du rechargement pendant le raisonnement.

Réparer l'erreur de compilation ios

## v1.5.1 - 2025.01.30

###Nouvelle fonctionnalité

Seuls les Gémeaux sont autorisés à envoyer des messages audio.

Optimisez la méthode pour obtenir les données PCM afin de décompresser les données audio lors de la génération du B64.

Demande d'ajouter deux rappels OnMessageFinished et OnImagesFinished.

Optimiser la méthode Gemini, pour récupérer automatiquement la méthode en fonction de bStream.

Ajoutez quelques fonctions de blueprint pour faciliter la conversion du Wrapper en type réel, ainsi que pour obtenir le message de réponse et l'erreur.

### Bug Fix

Réparer le problème d'appels multiples de la fin de la requête.

## v1.5.0 - 2025.01.29

###Nouvelle fonctionnalité.

Soutenir l'audio pour Gemini.

Les outils de l'éditeur prennent en charge l'envoi de fichiers audio et d'enregistrements.

### Bug Fix

Réparer le bug d'échec de copie de session.

## v1.4.1 - 2025.01.04

###Résolution du problème

L'outil de messagerie prend en charge l'envoi d'images sans message.

Résolution de l'échec de l'envoi d'images via l'API OpenAItoBeInTheDocument.

Corrigez le problème de paramètres manquants Quality, Style et ApiVersion dans les paramètres de configuration des outils de discussion OpenAI et Azure.

## v1.4.0 - 2024.12.30

###Nouvelle fonctionnalité

（Fonctionnalité expérimentale）Cllama (llama.cpp) prend en charge les modèles multimodaux et peut traiter les images.

Tous les paramètres de type Blueprint ont désormais des indications détaillées.

## v1.3.4 - 2024.12.05

###Nouvelle fonctionnalité

OpenAI supporte l'API de vision.

###Résolution du problème

Réparer l'erreur lorsque OpenAI stream=false.

## v1.3.3 - 2024.11.25

###Nouvelle fonctionnalité

Prend en charge l'UE-5.5

###Réparation du problème

Résolution du problème de certaines blueprints qui ne fonctionnaient pas.

## v1.3.2 - 2024.10.10

###Résolution du problème

Réparer le crash de cllama lors de l'arrêt manuel de la requête.

Corriger le problème de l'incapacité de trouver les fichiers ggml.dll et llama.dll lors de l'empaquetage de la version de téléchargement Win du magasin.

Vérifiez si vous êtes sur le thread de jeu lors de la création de la requête.

## v1.3.1 - 2024.9.30

###Nouvelle fonctionnalité

Ajoutez un SystemTemplateViewer pour visualiser et utiliser des centaines de modèles de paramètres système.

###Réparation de problèmes

Réparer le plugin téléchargé depuis la boutique, llama.cpp ne trouve pas la bibliothèque de liens

Corriger le problème de chemin trop long dans LLAMACpp.

Réparer l'erreur de lien llama.dll après la compilation de Windows.

Corrige le problème de lecture du chemin des fichiers pour iOS/Android.

Corriger l'erreur de nom de réglage de Cllame

## v1.3.0 - 2024.9.23

###Nouvelle fonctionnalité majeure

Intégration de llama.cpp pour prendre en charge l'exécution hors ligne de grands modèles locaux.

## v1.2.0 - 2024.08.20

###Nouvelle fonctionnalité

Prend en charge OpenAI Image Edit/Image Variation.

Prend en charge l'API Ollama, prend en charge l'obtention automatique de la liste des modèles pris en charge par Ollama.

## v1.1.0 - 2024.08.07

###Nouvelles fonctionnalités

Soutenir le plan.

## v1.0.0 - 2024.08.05

###Nouvelle fonctionnalité

Fonctionnalité de base complète

Soutenir OpenAI, Azure, Claude, Gemini.

Fonction d'édition intégrée et outil de chat complet.

--8<-- "footer_fr.md"


> Ce message a été traduit en français à l'aide de ChatGPT. Merci de [**donner votre avis**](https://github.com/disenone/wiki_blog/issues/new)Signalez toute omission. 
