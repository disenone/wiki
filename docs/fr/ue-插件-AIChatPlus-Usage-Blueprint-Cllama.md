---
layout: post
title: Cllama (llama.cpp)
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
- llama.cpp
description: Cllama (llama.cpp)
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Cllama (llama.cpp)" />

#Section Blueprint - Cllama (llama.cpp)

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_all.png)

##Modèle hors ligne

Cllama est basé sur llama.cpp et prend en charge l'utilisation hors ligne des modèles d'inférence en intelligence artificielle.

Étant donné qu'il s'agit d'une opération hors ligne, nous devons d'abord préparer les fichiers de modèle, tels que le téléchargement du modèle hors ligne depuis le site HuggingFace : [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Placez le modèle dans un dossier spécifique, par exemple dans le répertoire Content/LLAMA du projet de jeu.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA > ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Une fois que nous avons le fichier du modèle hors ligne, nous pouvons utiliser Cllama pour effectuer des discussions AI.

##Discussion par texte

Utiliser Cllama pour des discussions textuelles

Créez un nœud "Envoyer une Demande de Chat Cllama" en faisant un clic droit dans le diagramme.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Créez un nœud Options et définissez `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Créez des messages, ajoutez respectivement un message système et un message utilisateur.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Créez un délégué pour recevoir les informations de sortie du modèle et les afficher à l'écran

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Le texte en français est le suivant :

Le texte à traduire en français est le suivant : 

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##Créer un texte à partir de l'image llava

Cllama a également expérimentalement supporté la bibliothèque llava, offrant ainsi la capacité de Vision.

Tout d'abord, préparez le fichier du modèle hors ligne multimodal, comme Moondream ([moondream2-text-model-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-text-model-f16.gguf), [moondream2-mmproj-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-mmproj-f16.gguf)）或者 Qwen2-VL（[Qwen2-VL-7B-Instruct-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/Qwen2-VL-7B-Instruct-Q8_0.gguf), [mmproj-Qwen2-VL-7B-Instruct-f16.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-7B-Instruct-f16.gguf)Veuillez traduire ce texte en français :

）ou d'autres modèles multimodaux pris en charge par llama.cpp.

Créez un noeud Options, puis définissez les paramètres "Chemin du modèle" et "Chemin du modèle MMProject" avec les fichiers de modèle multimodal correspondants.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_1.png)

Crée un nœud pour lire le fichier d'image flower.png et configure les messages.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_3.png)

Crée en fin de compte un nœud qui recevra les informations renvoyées, puis les affichera à l'écran. Voici à quoi ressemblerait le schéma complet.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_4.png)

Exécutez le schéma pour afficher le texte renvoyé.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_5.png)

##Le fichier llama.cpp utilise le GPU.

Ajouter des options de demande de chat Cllama en ajoutant le paramètre "Num Gpu Layer", qui permet de définir la charge GPU de llama.cpp, permettant de contrôler le nombre de couches à calculer sur le GPU. Voir l'image pour plus de détails.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

##Traiter les fichiers de modèle dans le fichier .Pak après l'emballage.

Une fois que le Pak est activé, tous les fichiers de ressources du projet seront placés dans le fichier .Pak, y compris le fichier gguf du modèle hors ligne.

Étant donné que llama.cpp ne peut pas lire directement les fichiers .Pak, il est nécessaire de copier les fichiers de modèle hors ligne du fichier .Pak dans le système de fichiers.

AIChatPlus propose une fonctionnalité permettant de copier automatiquement les fichiers de modèle du fichier .Pak et de les placer dans le dossier Saved :

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

Ou bien vous pouvez traiter les fichiers de modèle vous-même dans le fichier .Pak. L'essentiel est de copier les fichiers, car llama.cpp ne peut pas lire correctement le fichier .Pak.

##Nœud de fonction

Cllama offre des nœuds de fonctionnalités permettant de récupérer l'état actuel de l'environnement.


"Cllama Is Valid"：Vérifiez si Cllama est correctement initialisé dans llama.cpp.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

Vérifie si le fichier llama.cpp prend en charge le backend GPU dans l'environnement actuel.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Obtenir les backends pris en charge par llama.cpp actuel"


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Prépare le fichier du modèle Cllama dans Pak": Automatically copies model files from Pak to the file system.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)


--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Signalez tout oubli. 
