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

#La section Blueprint - Cllama (llama.cpp)

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_all.png)

##Modèle hors ligne

Cllama est implémenté sur la base de llama.cpp, prenant en charge l'utilisation hors ligne de modèles d'inférence en IA.

En raison de son caractère hors ligne, nous devons d'abord préparer les fichiers modèle, tels que télécharger le modèle hors ligne depuis le site web de HuggingFace : [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Placez le modèle dans un dossier spécifique, par exemple dans le répertoire Content/LLAMA du projet de jeu.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA > ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Une fois que nous avons le fichier du modèle hors ligne, nous pouvons utiliser Cllama pour faire des conversations d'IA.

##Discussion par texte

Utilisez Cllama pour des conversations textuelles.

Créez un noeud "Send Llama Chat Request" en faisant un clic droit dans le blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Créez un noeud Options et définissez `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Créez des messages, ajoutez respectivement un message système et un message utilisateur.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Créez un délégué pour recevoir les informations de sortie du modèle et les afficher à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Le plan complet ressemble à ceci, en exécutant le plan, vous pouvez voir le message renvoyé sur l'écran de jeu en train d'imprimer le grand modèle.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##Convertissez ce texte en français :

图片生成文字 llava

Cllama a également soutenu llava de manière expérimentale, offrant la capacité de Vision.

Tout d'abord, préparez le fichier du modèle hors ligne multimodal, tel que Moondream ([moondream2-text-model-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-text-model-f16.gguf), [moondream2-mmproj-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-mmproj-f16.gguf)）或者 Qwen2-VL（[Qwen2-VL-7B-Instruct-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/Qwen2-VL-7B-Instruct-Q8_0.gguf), [mmproj-Qwen2-VL-7B-Instruct-f16.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-7B-Instruct-f16.gguf)Veuillez traduire ce texte en français :

）ou un autre modèle multimodal pris en charge par llama.cpp.

Créez un nœud Options et définissez les paramètres "Chemin du modèle" et "Chemin du modèle du projet multimodal" avec les fichiers de modèle multimodal correspondants.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_1.png)

Créer un nœud pour lire le fichier image flower.png et définir les messages.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_3.png)

Créez enfin un nœud pour recevoir les informations renvoyées et les afficher à l'écran. Voici à quoi ressemble le plan complet.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_4.png)

Exécuter le schéma peut afficher le texte renvoyé.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_5.png)

##llama.cpp utilise le GPU

Ajouter l'option "Num Gpu Layer" aux "Paramètres de demande de discussion du Cllama" pour configurer la charge gpu de llama.cpp, permettant de contrôler le nombre de couches à calculer sur le GPU. Voir l'image ci-dessous.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

## KeepAlive

Les "Options de demande de chat Cllama" ajoutent le paramètre "KeepAlive", qui permet de conserver le fichier modèle en mémoire après sa lecture, facilitant ainsi son utilisation directe la prochaine fois et réduisant le nombre de lectures du modèle. KeepAlive spécifie la durée de conservation du modèle en mémoire : 0 pour aucune conservation, sera libéré immédiatement après utilisation ; -1 pour une conservation permanente. Chaque demande peut configurer un KeepAlive différent dans les Options, le nouveau KeepAlive remplaçant l'ancienne valeur. Par exemple, les premières demandes peuvent définir KeepAlive=-1 pour conserver le modèle en mémoire jusqu'à ce que la dernière demande le définisse à KeepAlive=0 pour libérer le fichier modèle.

##Traiter les fichiers de modèle dans le fichier .Pak après l'emballage.

Une fois que le Pak est activé, tous les fichiers resources du projet seront regroupés dans le fichier .Pak, incluant bien sûr les fichiers gguf des modèles hors ligne.

Étant donné que llama.cpp ne prend pas en charge la lecture directe des fichiers .Pak, il est nécessaire de copier les fichiers de modèles hors ligne du fichier .Pak dans le système de fichiers.

AIChatPlus propose une fonctionnalité qui permet de copier automatiquement les fichiers de modèle du fichier .Pak et de les placer dans le dossier Saved.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

Ou bien, vous pouvez gérer les fichiers de modèle dans le fichier .Pak vous-même, l'élément clé est de copier les fichiers car llama.cpp ne peut pas lire correctement le fichier .Pak.

##Nœud de fonctionnalité

Cllama propose des nœuds de fonction pour faciliter l'obtention de l'état actuel dans l'environnement.


"Cllama Is Valid"：Vérifier si Cllama llama.cpp est correctement initialisé

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

Évaluer si llama.cpp prend en charge le backend GPU dans l'environnement actuel.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Obtenir les backends pris en charge par llama.cpp actuel"


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Préparer le fichier modèle dans Pak": Automatically copy model files from Pak to the file system.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)


--8<-- "footer_fr.md"


> Ce message a été traduit à l'aide de ChatGPT. Veuillez envoyer vos [**commentaires**](https://github.com/disenone/wiki_blog/issues/new)Indiquez toute omission. 
