---
layout: post
title: Emballez
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
description: Emballer
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - Package 篇 - Get Started" />

#Emballer

##Empaquetage du plugiciel

Lorsque vous compilez avec Unreal Engine, les fichiers de bibliothèque dynamique nécessaires aux plug-ins sont automatiquement inclus dans le package, il vous suffit simplement d'activer le plug-in.

Pour Windows, le processus de packaging placera automatiquement les fichiers llama.cpp et les DLL liés à CUDA dans le répertoire de destination. Il en va de même pour les autres plates-formes telles qu'Android, Mac et iOS.

Vous pouvez exécuter la commande "AIChatPlus.PrintCllamaInfo" dans le jeu en version Development après l'avoir packagé pour vérifier l'état actuel de l'environnement Cllama, confirmer si l'état est normal et s'il prend en charge le backend GPU.

##Emballage du modèle.

Supposons que les fichiers du modèle ajoutés au projet soient situés dans le dossier Content/LLAMA, alors vous pouvez inclure ce répertoire lors de l'emballage :

Ouvrez les "Paramètres du projet", sélectionnez l'onglet Packaging, ou recherchez directement "paquet d'actifs", repérez le paramètre "Répertoires supplémentaires à inclure dans le paquet" et ajoutez le dossier Content/LLAMA.

![](assets/img/2024-ue-aichatplus/usage/package/getstarted_1.png)

Une fois que le répertoire est ajouté, Unreal packagera automatiquement tous les fichiers du répertoire lors de la construction.

##Lire le fichier du modèle hors ligne après emballé.

Généralement, Uneal va regrouper tous les fichiers de projet dans un fichier .Pak. Si vous transmettez le chemin du fichier dans le .Pak au modèle hors ligne Cllam, cela échouera car llama.cpp ne peut pas lire directement le fichier de modèle regroupé dans le .Pak.

Il est donc nécessaire de copier les fichiers de modèle du fichier .Pak dans le système de fichiers, le plugin propose une fonction pratique pour copier directement les fichiers de modèle du fichier .Pak, et renvoie le chemin du fichier copié, ce qui permet à Cllama de les lire facilement.

Les nœuds de la feuille de route sont "Cllama Prepare ModelFile In Pak": ils copient automatiquement les fichiers de modèles du Pak dans le système de fichiers.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

Le code de la fonction en C++ est : 

```
#include <Cllama/AIChatPlusCllama_Util.h>

auto ModelPath = FAIChatPlusCllama_Util::PrepareModelFileInPak(InContentPath);
```

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez laisser vos [**commentaires**](https://github.com/disenone/wiki_blog/issues/new)Faites remarquer tout oubli. 
