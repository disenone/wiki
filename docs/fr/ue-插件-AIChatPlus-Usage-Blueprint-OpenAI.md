---
layout: post
title: OpenAI
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
description: OpenAI
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - OpenAI" />

#Chapitre Blueprint - OpenAI

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_all.png)

Dans [Commencer](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)Le chapitre a déjà couvert les bases d'OpenAI, nous fournirons ici des instructions détaillées sur son utilisation.

##Chat text

Utilisation d'OpenAI pour des discussions textuelles

Créez un nœud "Envoyer une demande de discussion OpenAI dans le monde" en cliquant droit dans le blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Créez un nœud Options et définissez `Stream=true, Api Key="votre clé API provenant d'OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Créez des messages en ajoutant respectivement un message système et un message utilisateur.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Créez un délégué pour recevoir les informations en sortie du modèle et les afficher à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Le blueprint complet ressemble à ceci, en exécutant le blueprint, vous verrez le message renvoyé par l'écran de jeu lors de l'impression du grand modèle.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

##Ce document génère une image.

Créez des images en utilisant OpenAI.

Dans le blueprint, créez un noeud "Send OpenAI Image Request" en cliquant avec le bouton droit, et configurez "In Prompt = 'a beautiful butterfly'".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Créez un nœud Options et définissez `Api Key="votre clé API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Lier l'événement "On Images" et enregistrer les images sur le disque dur local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

Le blueprint complet ressemble à ceci, en exécutant le blueprint, vous pouvez voir que l'image est enregistrée à l'emplacement spécifié.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

##Génération de texte à partir d'une image

Utiliser OpenAI Vision pour analyser des images

Créez un nœud "Envoyer une demande d'image OpenAI" en cliquant droit sur le blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_1.png)

Créez un nœud Options et définissez `Api Key="votre clé d'API provenant d'OpenAI"`, en définissant le modèle comme `gpt-4o-mini`.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_2.png)

Créer des messages.
Créez d'abord un noeud "Importer un fichier en tant que texture 2D" pour charger une image à partir du système de fichiers.
Convertissez l'image en un objet utilisable par le plugin en utilisant le nœud "Create AIChatPlus Texture From Texture2D".
Utilisez le nœud "Make Array" pour connecter les images au champ "Images" du nœud "AIChatPlus_ChatRequestMessage".
Définir le contenu du champ "Content" comme "décrire cette image".

Comme indiqué sur l'image :

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_3.png)

Le plan complet ressemble à ceci, exécutez-le pour voir les résultats s'afficher à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_4.png)

##Modifier l'image

OpenAI soutient la modification des régions marquées sur les images.

Tout d'abord, préparez deux images.

Une image à modifier nommé src.png

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_1.png)

Un des fichiers est une image mask.png sur laquelle les zones à modifier sont marquées. Vous pouvez modifier l'image source en réglant la transparence des zones modifiées à 0, en changeant tout simplement la valeur du canal alpha en 0.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_2.png)

Lire respectivement les deux photos ci-dessus, les combiner en un tableau.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_3.png)

Créez un nœud "Options d'images OpenAI", définissez ChatType sur Edit, et modifiez "End Point Url" en v1/images/edits.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_4.png)

Créez une "Demande d'image OpenAI", définissez "Prompt" comme "changer en deux papillons", connectez le nœud "Options" et le tableau d'images, puis enregistrez l'image générée dans le système de fichiers.

Le plan complet ressemble à ceci :

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_5.png)

Exécuter le plan, enregistrer l'image générée à l'emplacement spécifié.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_6.png)

##Les images mutants

OpenAI soutient la création de variations similaires d'une image en fonction de l'entrée fournie.

Tout d'abord, préparez une image nommée src.png et importez-la dans le blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_1.png)

Créez un nœud "OpenAI Image Options", définissez ChatType = Variation, et modifiez "End Point Url" en v1/images/variations.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_2.png)

Créez une "Demande d'image OpenAI", en laissant la "Incitation" vide, en reliant les nœuds "Options" et les images, et en enregistrant l'image générée dans le système de fichiers.

Le plan complet ressemble à ceci :

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_3.png)

Exécuter le plan, enregistrer l'image générée à l'emplacement spécifié.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_4.png)

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez [**donner votre avis**](https://github.com/disenone/wiki_blog/issues/new)Signalez toute omission. 
