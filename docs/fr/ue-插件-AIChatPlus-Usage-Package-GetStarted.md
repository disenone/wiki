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
description: Emballez
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - Package 篇 - Get Started" />

#Emballer

##Emballage de plug-ins

Lorsque vous effectuez le packaging dans Unreal Engine, les fichiers de bibliothèques dynamiques requis par les plugins sont automatiquement inclus dans le package, il vous suffit simplement d'activer le plugin.

Pour Windows, lors du packaging, les fichiers llama.cpp, ainsi que les fichiers DLL liés à CUDA, seront automatiquement placés dans le répertoire de destination. Il en va de même pour les autres plateformes telles qu'Android, Mac et iOS.

Vous pouvez exécuter la commande "AIChatPlus.PrintCllamaInfo" dans le jeu version Development après l'avoir packagé, pour vérifier l'état actuel de l'environnement Cllama, confirmer si l'état est normal et s'il prend en charge le backend GPU.

##Emballage du modèle

Les fichiers de modèle pour le projet sont situés dans le répertoire Content/LLAMA. Ainsi, vous pouvez définir d'inclure ce répertoire lors de l'emballage.

Ouvrez les "Paramètres du projet", sélectionnez l'onglet Packaging, ou recherchez directement "asset package", puis repérez l'option "Répertoires supplémentaires à inclure dans le package" et ajoutez le répertoire Content/LLAMA.

![](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_6.png)

Après avoir ajouté la table des matières, Unreal va automatiquement empaqueter tous les fichiers du répertoire lors du processus de compilation.


##Lire le fichier du modèle hors ligne empaqueté.

En général, Uneal packagera tous les fichiers de projet dans un fichier .Pak. Si vous transmettez le chemin du fichier dans le .Pak au modèle hors ligne Cllam, l'exécution échouera car le fichier empaqueté du modèle ne peut pas être lu directement par llama.cpp.

Il est donc nécessaire de copier les fichiers de modèle du .Pak dans le système de fichiers avant tout, le plugin offre une fonction pratique qui permet de copier directement les fichiers de modèle du .Pak et de renvoyer le chemin du fichier copié, pour que Cllama puisse les lire facilement.

Les Blueprints Nodes sont "Cllama Prepare ModelFile In Pak": ils copient automatiquement les fichiers de modèle du Pak dans le système de fichiers.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

Le code de la fonction C++ est :

```
#include <Cllama/AIChatPlusCllama_Util.h>

auto ModelPath = FAIChatPlusCllama_Util::PrepareModelFileInPak(InContentPath);
```

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez donner votre [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Identifier toute omission. 
