---
layout: post
title: Get Started
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
description: Get Started
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Get Started" />

#Chapitre du Plan - Commencez

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

## Get Started

Voici un exemple avec OpenAI pour illustrer les méthodes d'utilisation de la feuille de route.

###Chat texte

Utiliser OpenAI pour la discussion textuelle

Créez un nœud `Envoyer une demande de chat OpenAI dans le monde` en cliquant droit dans le blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Créez un nœud Options et définissez `Stream=true, Api Key="votre clé API d'OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Créez des messages en ajoutant respectivement un message système et un message utilisateur.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Créez un délégué pour recevoir les informations du modèle et les afficher à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Le plan complet ressemble à ceci ; en exécutant le plan, vous verrez un message imprimé à l'écran du jeu avec le retour du grand modèle.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Ce texte génère une image.

Utiliser OpenAI pour créer des images

Dans le blueprint, faites un clic droit pour créer un nœud appelé « Envoyer une requête d'image à OpenAI » et définissez « In Prompt="un beau papillon" ».

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Créez un nœud Options et définissez `Api Key="votre clé d'API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Attacher l'événement On Images et enregistrer les images sur le disque dur local

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

Le texte traduit en français est le suivant:

Le plan complet ressemble à cela, une fois le plan exécuté, vous pourrez voir l'image enregistrée à l'emplacement spécifié.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

###Génération de texte à partir d'une image

Utiliser OpenAI Vision pour analyser les images

Créez un nœud "Envoyer une demande d'image OpenAI" en cliquant avec le bouton droit dans le schéma.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_1.png)

Créez un noeud Options, et définissez `Api Key="votre clé API d'OpenAI"`, en définissant le modèle comme `gpt-4o-mini`.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_2.png)

Créer des messages.
Créez d'abord un nœud "Importer un fichier en tant que texture 2D" pour charger une image à partir du système de fichiers.
Convertir l'image en un objet utilisable par le plugin via le nœud "Create AIChatPlus Texture From Texture2D".
Utilisez le nœud "Créer un tableau" pour connecter les images au champ "Images" du nœud "AIChatPlus_ChatRequestMessage".
Définissez le contenu du champ "Content" comme étant "décrire cette image".

Comme indiqué ci-dessus :

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_3.png)

Le plan complet ressemble à ceci, exécutez-le, vous verrez les résultats s'afficher à l'écran.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_4.png)

--8<-- "footer_fr.md"


> Ce message a été traduit en français à l'aide de ChatGPT. Veuillez laisser vos [**commentaires**](https://github.com/disenone/wiki_blog/issues/new)Identifier tout manquement. 
