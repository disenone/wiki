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

#Journal des versions du plugin AIChatPlus de l'UE

## v1.6.2 - 2025.03.17

###Nouvelle fonctionnalité

Cllama a augmenté le paramètre KeepContext par défaut à false, le contexte est automatiquement détruit après la fin du chat.

Cllama a ajouté le paramètre KeepAlive, ce qui peut réduire la lecture répétée du modèle.

## v1.6.1 - 2025.03.07

### Bug Fix

Le plan OpenAI Image Chat prend désormais en charge l'entrée d'images.

Outil d'édition Cllama mmproj modèle autorise vide

## v1.6.0 - 2025.03.02

###Nouvelle fonctionnalité

Mettre à jour llama.cpp vers la version b4604.

Cllama supporte les GPU backends : cuda et metal

L'outil de discussion Cllama prend en charge l'utilisation du GPU.

Prend en charge la lecture des fichiers de modèle emballés dans un Pak.

### Bug Fix

Réparation du problème de plantage de Cllama lors du rechargement lors de l'inférence

Réparer l'erreur de compilation iOS

## v1.5.1 - 2025.01.30

###Nouvelle fonctionnalité

Seuls les Gémeaux peuvent envoyer des fichiers audio.

Optimisation de la méthode d'extraction des données PCM pour décompresser les données audio lors de la génération du B64.

Demande d'ajouter deux rappels OnMessageFinished et OnImagesFinished.

Optimisez la méthode Gemini pour automatiquement obtenir la méthode en fonction de bStream.

Ajoutez quelques fonctions de blueprint pour faciliter la conversion du Wrapper en type réel, et obtenir le message de réponse et l'erreur.

### Bug Fix

Corriger le problème des appels répétés à la fin de la requête.

## v1.5.0 - 2025.01.29

###Nouvelle fonctionnalité

S'il vous plaît supporter l'audio pour Gemini.

Les outils de l'éditeur prennent en charge l'envoi d'audio et d'enregistrements.

### Bug Fix

Corrige le bug qui empêche la copie de session.

## v1.4.1 - 2025.01.04

###Correction de problème

L'outil de messagerie prend en charge l'envoi d'images sans message.

Réparer l'échec de l'envoi d'images à l'API OpenAI.

Réparez les paramètres manquants Quality, Style et ApiVersion dans les configurations des outils de messagerie OpanAI et Azure.

## v1.4.0 - 2024.12.30

###Nouvelle fonctionnalité

Fonction expérimentale Cllama (llama.cpp) prenant en charge des modèles multimodaux pour le traitement d'images.

Tous les paramètres de type blueprint ont été accompagnés de directives détaillées.

## v1.3.4 - 2024.12.05

###Nouvelle fonctionnalité

OpenAI supporte l'API de vision.

###Résolution du Problème

Réparer l'erreur lorsqu'OpenAI stream=false.

## v1.3.3 - 2024.11.25

###Nouvelle fonctionnalité

Prend en charge UE-5.5

###Correction de problèmes

Réparer le problème de certains plans qui ne fonctionnent pas.

## v1.3.2 - 2024.10.10

###Réparation du problème

Réparer le crash de cllama lors de l'arrêt manuel de la demande.

Réparer le problème de l'impossibilité de trouver les fichiers ggml.dll et llama.dll lors de l'emballage de la version de téléchargement de la boutique Win.

Vérifiez lors de la création de la requête si vous êtes dans GameThread.

## v1.3.1 - 2024.9.30

###Nouvelle fonctionnalité

Ajouter un SystemTemplateViewer permettant de visualiser et d'utiliser des centaines de modèles de paramètres système.

###Correction de problème

Réparez le plug-in téléchargé depuis le magasin, llama.cpp ne trouve pas la bibliothèque de liens.

Réparer le problème de chemin trop long de LLAMACpp.

Réparez l'erreur de lien llama.dll après avoir empaqueté Windows.

Répare le problème de lecture du chemin du fichier sur iOS/Android.

Réparer le nom incorrect des paramètres de Cllame

## v1.3.0 - 2024.9.23

###Nouvelle fonctionnalité majeure

Intégré llama.cpp, pris en charge de l'exécution hors ligne de grands modèles locaux.

## v1.2.0 - 2024.08.20

###Nouvelle fonctionnalité.

Soutenir la fonction OpenAI Image Edit/Image Variation.

Prend en charge l'API Ollama, permet d'obtenir automatiquement la liste des modèles pris en charge par Ollama.

## v1.1.0 - 2024.08.07

###Nouvelle fonctionnalité

Soutenir le plan d'action.

## v1.0.0 - 2024.08.05

###Nouvelles fonctionnalités

Fonctionnalité de base complète

Soutenir OpenAI, Azure, Claude, Gemini.

Un outil de messagerie avec un éditeur intégré complet.

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT. Veuillez laisser vos [**commentaires**](https://github.com/disenone/wiki_blog/issues/new)Veuillez identifier tout élément omis. 
