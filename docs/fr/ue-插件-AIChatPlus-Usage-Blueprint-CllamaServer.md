---
layout: post
title: CllamaServer (llama.cpp server)
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
- CllamaServer
description: CllamaServer (llama.cpp server)
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - CllamaServer (llama.cpp server)" />

#Plan directeur - CllamaServer (serveur llama.cpp)

<!-- Image requise : Présentation de tous les nœuds de blueprint liés à CllamaServer, similaire aux xxx_all.png des autres documentations -->
![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_all.png)

##Aperçu

CllamaServer est une implémentation basée sur le mode Serveur de llama.cpp, permettant de démarrer localement un serveur compatible avec l'API OpenAI et prenant en charge diverses fonctionnalités :

* **Service d'inférence locale** : Lancez un serveur d'inférence IA en local, sans dépendre d'API externes
* **Compatibilité avec l'API OpenAI** : Utilisation d'un format d'API compatible avec OpenAI pour faciliter la migration et l'intégration
* **Prise en charge multi-session** : Prise en charge de plusieurs requêtes simultanées
* **Appel d'outil** : Prend en charge la fonction d'appel de fonction
* **Reconnaissance vocale**: Prend en charge la fonctionnalité Speech-to-Text
* **Gestion visuelle**: L'éditeur intègre une interface de gestion du serveur.

Différences avec Cllama :
* **Cllama** : Charge directement le modèle dans le processus pour l'inférence, ne peut traiter qu'une seule requête à la fois.
* **CllamaServer** : Démarrer un serveur HTTP autonome capable de gérer plusieurs requêtes simultanées, avec une API compatible au format OpenAI

##Préparatifs

Puisqu'il s'agit d'une exécution locale, il faut d'abord préparer le fichier de modèle hors ligne, par exemple en le téléchargeant depuis HuggingFace : [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Placez le modèle dans un dossier spécifique, par exemple dans le répertoire du projet de jeu `Content/LLAMA`.

##Création de CllamaServer

###Créer un serveur à l'aide d'un blueprint

Cliquez avec le bouton droit dans le blueprint pour créer un nœud `Create Cllama Server In World`.

<!-- Besoin d'une image : capture d'écran montrant la recherche par clic droit dans le blueprint "Create Cllama Server" et la création d'un nœud -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_1.png)

###Configurer les paramètres du serveur

Créer le nœud `Cllama Server Param` et configurer les paramètres clés :

* **Modèle** : Chemin du fichier modèle (requis)
* **Port** : Port du serveur (0 signifie une allocation automatique)
* **Hôte** : adresse d'écoute, par défaut `127.0.0.1`
* **NGpuLayers** : Nombre de couches GPU (-1 signifie utiliser toutes les GPU)

<!-- Image nécessaire : capture d'écran montrant la création du nœud FAIChatPlus_CllamaServerParam, avec la configuration des paramètres tels que le chemin du Model, Port, NGpuLayers, etc. -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_2.png)

###Associer les événements de rappel

Liaison des événements de rappel du serveur :

* **On Started** : Déclenché lorsque le serveur démarre avec succès
* **On Stopped** : Déclenché lorsque le serveur s'arrête
* **On Failed** : Se déclenche lorsque le démarrage du serveur échoue

<!-- Image nécessaire : montrant les événements de liaison OnStartedListeners, OnStoppedListeners, OnFailedListeners dans un blueprint -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_3.png)

###Plan complet de création

Le plan complet de création du serveur est le suivant :

<!-- Besoin d'une image : Montrer une vue complète du schéma de création de Server, incluant la configuration des paramètres, la création des nœuds et la liaison des rappels -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_4.png)

Après avoir exécuté le plan directeur, le démarrage réussi du serveur déclenchera l'événement `On Started`.

<!-- Besoin d'une image : montrer les résultats après le démarrage réussi du serveur, affichant les logs ou la sortie écran confirmant le succès du lancement -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_5.png) -->

##Détails des paramètres du serveur

`FAIChatPlus_CllamaServerParam` est une structure qui contient les paramètres suivants :

###Paramètres courants

| Paramètre | Type | Valeur par défaut | Description |
|-----|------|-------|------|
| Modèle | FString | - | Chemin du fichier modèle (obligatoire) |
| Port | int32 | 0 | Port d'écoute, 0 signifie allocation automatique |
| Hôte | ChaîneF | 127.0.0.1 | Adresse d'écoute |
| NGpuLayers | int32 | -1 | Nombre de couches GPU, -1 signifie toutes |
| bUseJinja | bool | false | Utiliser le modèle Jinja |
| MMProj | FString | - | Chemin du fichier de projection multimodale |
| Température | float | 0.8 | Température d'échantillonnage |

###Argument de raisonnement

| Paramètre | Type | Valeur par défaut | Description |
|-----|------|-------|------|
| CtxSize | int32 | 4096 | Taille du contexte |
| NPredict | int32 | -1 | Nombre de Tokens à prédire, -1 signifie illimité |
| Threads | int32 | -1 | Nombre de threads CPU, -1 signifie automatique |
| BatchSize | int32 | 2048 | Taille du lot (batch) |

###Paramètres d'échantillonnage

| Paramètre | Type | Valeur par défaut | Description |
|-----|------|-------|------|
| TopK | int32 | 40 | Échantillonnage Top-K |
| TopP | float | 0.9 | Échantillonnage Top-P |
| MinP | float | 0.1 | Échantillonnage Min-P |
| RepeatPenalty | float | 1.0 | Pénalité de répétition |

###Paramètres du serveur

| Paramètre | Type | Valeur par défaut | Description |
|-----|------|-------|------|
| ApiKey | FString | - | Clé API (optionnelle) |
| Timeout | int32 | 600 | Durée d'expiration (secondes) |
| Parallèle | int32 | 1 | Nombre de séquences parallèles |
| bNoWebUI | bool | false | Désactiver l'interface Web |
| bVerbose | bool | false | Journal détaillé |

##Utiliser CllamaServer pour discuter

###Créer une demande de chat

Une fois le serveur démarré avec succès, vous pouvez utiliser le nœud `Send CllamaServer Chat Request` pour envoyer une demande de chat.

<!-- Besoin d'une image : capture d'écran montrant la recherche par clic droit dans le blueprint de "CllamaServer Chat Request" et la création d'un nœud -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_1.png)

###Configurer les Options de Chat

Créer le nœud `CllamaServer Chat Request Options`, définissez BaseUrl comme l'adresse du serveur.

Vous pouvez obtenir les informations du serveur via le nœud `Get Server Info By ID`.

<!-- Besoin d'une image : montrant la création du nœud FAIChatPlus_CllamaServerChatRequestOptions, utilisant Get Http Address pour récupérer l'adresse du serveur et la définir sur BaseUrl dans le blueprint -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_2.png)

###Créer des Messages

Créez un tableau Messages, ajoutez un Message Système et un Message Utilisateur.

<!-- Besoin d'une image : montrant la création d'un tableau Messages, contenant un Message Système (définissant le rôle de l'assistant) et un Message Utilisateur (question de l'utilisateur) en schéma -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_3.png)

###Associer des rappels pour traiter les réponses

Lieez l'événement `On Message` ou `On Message Finished` pour recevoir les réponses du modèle.

<!-- Image nécessaire : une capture d'écran d'un blueprint illustrant la liaison d'événements OnMessageListeners et l'affichage des messages dans un callback à l'écran -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_4.png)

###Plan complet de discussion

Le plan complet de conversation est le suivant :

<!-- Besoin d'une image : montrant une vue d'ensemble complète du schéma de discussion, incluant la création du serveur, l'attente du démarrage, l'envoi de la requête de discussion et le traitement de la réponse -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_5.png)

###Résultat de l'exécution

Exécutez le modèle et vous verrez le message renvoyé par le modèle s'afficher à l'écran.

<!-- Besoin d'une image : montrer le résultat de la conversation en cours d'exécution, avec le contenu de la réponse du modèle affiché à l'écran -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_6.png) -->

##Gestion des serveurs

###Obtenir les informations du Serveur

Utilisez le nœud `Get Server Info` pour obtenir les détails du serveur.

<!-- Besoin d'une image : montrant l'utilisation du nœud Get Server Info pour récupérer FAIChatPlus_CllamaServerInfo dans le blueprint, puis Break pour afficher chaque champ -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_info_1.png)

Les informations sur le serveur contiennent les éléments suivants :
* **ServerID** : ID unique du serveur
* **Hôte** : Adresse d'écoute
* **Port**: Port d'écoute
* **Adresse** : Adresse complète (hôte:port)
* **HttpAddress**: Adresse HTTP (http://host:port)
* **bIsRunning**: Est-ce en cours d'exécution
* **Param**: Paramètre du serveur

###Arrêter le serveur

Utilisez le nœud `Stop Server By ID` pour arrêter le serveur actuel.

<!-- Besoin d'une image : montrant le blueprint pour l'appel du nœud Stop Cllama Server -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_stop_1.png)

###Fonctions de gestion statique

AIChatPlus offre une série de fonctions statiques pour gérer tous les serveurs :

| Fonction | Description |
|-----|------|
| `Is Server Valid (Static)` | Vérifie si le serveur est valide |
| `Is Server Running (Statique)` | Vérifie si le Serveur est en cours d'exécution |
| `Arrêter le Serveur Par ID` | Arrête le serveur spécifié par ID |
| `Stop All Servers` | Arrêter tous les serveurs |
| `Get Server Info By ID` | Obtenir les informations du serveur par ID |
| `Obtenir tous les ID des serveurs` | Récupérer tous les ID des serveurs |
| `Get Server By ID` | Obtenir une instance de Serveur par ID |

<!-- Besoin d'une image : exemple de blueprint illustrant l'utilisation de fonctions de gestion statiques comme Get All Server IDs et Stop All Servers -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_static_1.png)

##Support multilingue

CllamaServer prend en charge les modèles multimodaux (comme Moondream, Qwen2-VL, etc.).

###Configurer les paramètres multimodaux

Dans le paramètre Server, définissez `MMProj` (chemin du fichier de projection multimodale) :

<!-- Image nécessaire : une capture d'écran illustrant la configuration dans Server Param des chemins d'accès pour Model et MMProj dans l'éditeur de blueprint -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_1.png)

###Envoyer un message avec une image

Ajouter des images dans Messages :

<!-- Image requise : schéma illustrant la lecture d'un fichier image, la création d'un Message contenant l'image, et l'envoi de la requête via CllamaServer -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_2.png)

<!-- ### Résultats d'exécution -->

<!-- Image requise : montrer les résultats de l'exécution de la reconnaissance d'image, avec l'affichage à l'écran de la description du contenu de l'image par le modèle -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_3.png) -->

## Tool Calling

CllamaServer prend en charge la fonction Tool Calling (appel de fonction), dont l'utilisation est similaire à celle d'OpenAI.

Pour une utilisation détaillée, veuillez consulter [Tool Call](ue-插件-AIChatPlus-Usage-Blueprint-ToolCall.md)Document.

Pour utiliser CllamaServer pour les appels d'outil (Tool Call), il est nécessaire de :
1. Dans les paramètres du Serveur, définissez `bUseJinja = true`
2. Définir les outils dans le champ Tools des Chat Options

<!-- Image requise : montrant le plan complet de CllamaServer Tool Call, incluant le paramètre bUseJinja=true et la définition des Tools -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_tool_1.png)

##Éditeur Gestion du Serveur

AIChatPlus propose dans ses outils d'édition une interface visuelle de gestion pour CllamaServer, facilitant ainsi la création, la surveillance et la gestion de plusieurs serveurs.

Ouvrez l'outil d'édition : `Outils -> AIChatPlus -> AIChat`, puis ouvrez l'onglet Cllama Server Manager.

<!-- Besoin d'une image : capture d'écran de l'interface de gestion de CllamaServer dans l'éditeur, montrant la liste des serveurs, le bouton de création, les informations d'état, etc. -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_editor_1.png)

Dans l'éditeur, vous pouvez :
* Créer un nouveau serveur
* Vérifier l'état du serveur en cours d'exécution
* Arrêter le serveur spécifié
* Configuration des paramètres du serveur
* La configuration du serveur est automatiquement sauvegardée.

<!-- Besoin d'une image : montrant l'interface de création d'un nouveau Serveur dans l'éditeur, affichant le panneau de configuration des paramètres -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_editor_2.png)

##Relations avec les autres API

Puisque CllamaServer est compatible avec le format API d'OpenAI, vous pouvez également utiliser le nœud Chat Request d'OpenAI pour communiquer avec CllamaServer. Il suffit de définir le `BaseUrl` sur l'adresse de CllamaServer.

<!-- Besoin d'une image : Exemple de blueprint montrant l'utilisation du nœud OpenAI Chat Request, mais avec BaseUrl configurée sur l'adresse de CllamaServer -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_openai_1.png) -->

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, merci de nous faire part de vos [**retours**](https://github.com/disenone/wiki_blog/issues/new)Signaler toute omission. 
