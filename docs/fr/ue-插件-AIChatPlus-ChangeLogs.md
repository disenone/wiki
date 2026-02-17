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

#Journal des modifications de l'extension UE AIChatPlus

## v2.0.0 - 2026.02.14

* **Prise en charge multi-plateformes de Tool Calling** : Ajout des fonctionnalités d'appel d'outils/appel de fonctions pour cinq grandes plateformes : OpenAI, Claude, Gemini, Ollama et CllamaServer.
* **Intégration de Cllama Server**: Prise en charge complète du serveur local llama.cpp, incluant la création, la gestion, la fonction Speech-to-Text et une interface de gestion visuelle dans l'éditeur.
* **Bibliothèque de plans JSON**: Ajoute des classes d'opérations de plans JsonObject/JsonArray, prenant en charge la conversion mutuelle entre JSON et USTRUCT.
* **Audio OpenAI** : Prend en charge l'entrée et la sortie audio d'OpenAI, l'éditeur permet de prévisualiser les réponses audio

## v1.8.0 - 2025.11.03

* Mise à niveau de llama.cpp b6792

## v1.7.0 - 2025.07.06

* Mise à jour de llama.cpp vers la version b5536

* Prise en charge d'UE5.6

* Android publie un problème où le shipping provoque un crash, désactivez llama.cpp

## v1.6.2 - 2025.03.17

###Nouvelles fonctionnalités

* Cllama ajoute le paramètre KeepContext, par défaut false, le Context est automatiquement détruit à la fin du Chat

* Cllama ajoute le paramètre KeepAlive pour réduire la lecture répétée du modèle

## v1.6.1 - 2025.03.07

### Bug Fix

* Le modèle OpenAI Image Chat prend en charge la saisie d'images

* L'outil Editor Tool Cllama mmproj modèle autorise le vide

## v1.6.0 - 2025.03.02

###Nouvelle fonctionnalité

* llama.cpp mis à jour vers la version b4604

* Cllama prend en charge les backends GPU : cuda et metal

* L'outil de discussion Cllama prend en charge l'utilisation du GPU

* Prise en charge de la lecture des fichiers de modèles dans les packs Pak

### Bug Fix

* Correction du problème de crash lors du rechargement pendant l'inférence avec Cllama

* Correction des erreurs de compilation sous iOS

## v1.5.1 - 2025.01.30

###Nouvelle fonctionnalité

* Seul Gemini est autorisé à envoyer des fichiers audio

* Optimiser la méthode d'obtention des données PCM, décompresser les données audio lors de la génération du B64

* demande ajouter deux rappels OnMessageFinished OnImagesFinished

* Optimiser la méthode Gemini pour obtenir automatiquement la méthode en fonction du bStream

* Ajouter quelques fonctions de blueprint pour faciliter la conversion des Wrapper en types réels, ainsi que pour récupérer les Response Message et Error.

### Bug Fix

* Correction du problème d'appels multiples de Request Finish

## v1.5.0 - 2025.01.29

###Nouvelle fonctionnalité

* Prise en charge de l'envoi d'audio à Gemini

* L'outil éditeur prend en charge l'envoi d'audio et d'enregistrements

### Bug Fix

* Correction du bug d'échec de copie de Session

## v1.4.1 - 2025.01.04

###Correction des problèmes

* L'outil de chat permet d'envoyer uniquement des images sans message

* Correction de l'échec de l'envoi d'images via l'interface OpenAI

* Correction du problème où les paramètres Quality, Style et ApiVersion étaient omis dans les paramètres des outils de chat OpanAI et Azure=

## v1.4.0 - 2024.12.30

###Nouvelle fonctionnalité

* (Fonction expérimentale) Cllama(llama.cpp) prend en charge les modèles multimodaux et peut traiter des images

* Des conseils détaillés ont été ajoutés à tous les paramètres des types de plans.

## v1.3.4 - 2024.12.05

###Nouvelle fonctionnalité

* OpenAI prend en charge l'API vision

###Correction de problème

* Correction de l'erreur lorsque OpenAI stream=false

## v1.3.3 - 2024.11.25

###Nouvelle fonctionnalité

* Prise en charge d'UE-5.5

###Correction de problèmes

* Correction du problème où certains schémas ne prenaient pas effet

## v1.3.2 - 2024.10.10

###Correction de problèmes

* Correction d'un plantage de cllama lors de l'arrêt manuel d'une requête

* Correction du problème lors de l'empaquetage de la version téléchargée sur la boutique Windows où les fichiers ggml.dll et llama.dll étaient introuvables.

* Vérifier si c'est dans le GameThread lors de la création de la requête, CréerRequête vérifie dans le fil de jeu

## v1.3.1 - 2024.9.30

###Nouvelle fonctionnalité

* Ajouter un SystemTemplateViewer permettant de consulter et d'utiliser des centaines de modèles de paramètres système

###Correction des problèmes

* Correction d'un problème où les plugins téléchargés depuis la boutique ne trouvaient pas la bibliothèque de liens llama.cpp

* Correction du problème de chemin trop long avec LLAMACpp

* Correction des erreurs de liaison de llama.dll après l'empaquetage sous Windows

* Correction des problèmes de lecture des chemins de fichiers sur iOS/Android

* Correction de l'erreur de configuration du nom dans Cllame

## v1.3.0 - 2024.9.23

###Nouvelles fonctionnalités majeures

* Intégré llama.cpp, prenant en charge l'exécution locale hors ligne de grands modèles

## v1.2.0 - 2024.08.20

###Nouvelle fonctionnalité

* Prise en charge de OpenAI Édition d'image/Variation d'image

* Prise en charge de l'API Ollama, avec récupération automatique de la liste des modèles pris en charge par Ollama

## v1.1.0 - 2024.08.07

###Nouvelle fonctionnalité

* Prise en charge des plans directeurs

## v1.0.0 - 2024.08.05

###Nouvelle fonctionnalité

* Fonctions de base complètes

* Compatible avec OpenAI, Azure, Claude, Gemini

* Outil de chat avec éditeur intégré complet

--8<-- "footer_fr.md"


> Ce message a été traduit avec ChatGPT, veuillez envoyer vos commentaires sur [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Signaler toute omission dans le texte. 
