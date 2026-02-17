---
layout: post
title: Tool Call
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
- Tool Call
- Function Calling
description: Tool Call
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Tool Call" />

#Chapitre des Plans Bleus - Appel d'Outils

L'appel d'outil (Tool Call), également connu sous le nom d'appel de fonction (Function Calling), fait référence à la capacité d'un grand modèle à déterminer, en fonction du contenu de la conversation, s'il est nécessaire de faire appel à des outils/fonctions externes pour obtenir des informations ou effectuer des opérations. Le modèle renverra le nom de la fonction à appeler ainsi que ses paramètres, et après que le développeur aura effectué l'appel réel, le résultat sera retourné au modèle pour poursuivre la conversation.

AIChatPlus prend en charge la fonction Tool Call pour les plateformes suivantes :

* OpenAI
* Claude
* Gemini
* Ollama
* CllamaServer (serveur llama.cpp)

##Concept clé

###Définition de l'outil

La définition d'un outil comprend les champs clés suivants :

* **Type**: Type d'outil, actuellement uniquement `Function` est pris en charge
* **Nom** : Nom de la fonction, doit être composé des caractères a-z, A-Z, 0-9, d’un tiret bas ou d’un trait d'union, longueur maximale de 64
* **Description**: Description de la fonction, le modèle utilisera cette description pour déterminer quand appeler cette fonction.
* **Propriétés** : Liste des paramètres de la fonction, chaque paramètre inclut des attributs tels que Nom, Description, Type, Obligatoire, etc.

###Fluxus d'Appel d'Outil

Le processus complet de Tool Call est le suivant :

1. **Envoyer une requête** : Envoyez une requête de chat incluant les définitions des Outils au modèle.
2. **Évaluation du modèle** : Le modèle détermine s'il est nécessaire d'utiliser un outil en fonction du contenu de la conversation
3. **Retour d'appels d'outils**: Si un appel est nécessaire, le modèle renvoie le nom de la fonction et les paramètres à appeler
4. **Exécution de la fonction** : Les développeurs effectuent l'appel réel de la fonction en fonction des informations retournées.
5. **Retour des résultats** : Envoyer les résultats de l'exécution de la fonction comme nouveau message au modèle
6. **Continuer la conversation** : Le modèle génère une réponse finale basée sur les résultats de la fonction.

##Exemple d'appel d'outil OpenAI

Voici un exemple avec OpenAI pour démontrer comment utiliser la fonctionnalité Tool Call.

###1. Définir Outil

Commencez par créer la définition de l'outil. Dans cet exemple, nous définissons une fonction `get_delivery_date` pour obtenir la date de livraison d'un colis.

<!-- Besoin d'une image : montrant la création du nœud FAIChatPlus_ChatRequestTool, avec la configuration Type=Fonction, Nom="get_current_weather", Description="Obtenir la météo actuelle pour un emplacement donné" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_1.png)

###2. Définir les paramètres de l'outil

Ajouter des Propriétés à Tool. Dans cet exemple, ajouter un paramètre `order_id`, de type `string`, défini comme obligatoire.

<!-- Besoin d'une image : montrant la création d'un nœud FAIChatPlus_ChatRequestToolProperty, avec Name="location", Description="La ville et l'état, par exemple San Francisco, CA", Type="string", Required=true, et connecté au champ Properties de Tool via Make Array -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_2.png)

###3. Configuration Options

Créer le nœud `OpenAI Chat Request Options`, configurer l'API Key et le Model, puis connecter le tableau Tools aux Options.

<!-- Besoin d'une image : montrant la création d'un nœud OpenAI Chat Request Options, avec la configuration de ApiKey, Model="gpt-4o-mini", et la connexion du Tool ci-dessus au champ Tools via Make Array -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_3.png)

###4. Créer des Messages

Créer un message utilisateur pour poser une question concernant un colis express.

<!-- Besoin d'une image : montrer la création d'un tableau Messages, ajouter un Message utilisateur avec le Contenu défini sur "Quel temps fait-il à Boston aujourd'hui ?" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_4.png)

###5. Envoyer une demande et traiter l'appel d'outil

Créez le nœud `Send OpenAI Chat Request In World` et liez-le à l'événement `On Message Finished`. Dans le rappel de l'événement, récupérez le tableau ToolCalls à partir de Payload.

Lorsque le modèle décide d'appeler un outil, le tableau ToolCalls n'est pas vide. Parcourez le tableau pour obtenir les informations de chaque appel d'outil (Tool Call) :

* **Id** : Identifiant unique de l'appel d'outil
* **FunctionName**: Nom de la fonction à appeler
* **FunctionArguments**: Arguments de la fonction (format chaîne JSON)

<!-- Image nécessaire : montrant le schéma complet d'envoi de requête, création du nœud "Send OpenAI Chat Request In World", connexion des options et des messages, liaison de l'événement "On Message Finished", utilisation d'un nœud "Break" dans le rappel d'événement pour récupérer les ToolCalls dans le Payload -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_5.png)

<!-- Image nécessaire : Un diagramme de flux montrant la traversée d'un tableau ToolCalls à l'aide d'une boucle For Each Loop, avec l'utilisation d'un nœud Break pour extraire les champs Id, FunctionName, FunctionArguments pour chaque élément, puis leur affichage en sortie -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_6.png) -->

###6. Exécuter la fonction et retourner le résultat

Selon FunctionName, exécuter la logique de fonction correspondante (dans cet exemple, simuler l'obtention du délai de livraison d'un colis postal), puis renvoyer le résultat au modèle sous forme de message de type ToolCallResult.

Pour créer un nouveau Message, vous devez configurer :

* **Rôle**: Défini sur `Outil`
* **Contenu** : Résultat de l'exécution de la fonction
* **ToolCallResults** : Ajoutez un `FAIChatPlus_ChatRequestToolCallResult`, configurez Id (en utilisant l'Id précédent de Tool Call), FunctionName et FunctionResult

<!-- Besoin d'une image : montrant le blueprint pour créer un message du rôle Tool, créer un nouveau Message, Role=Tool, Content défini sur des données météorologiques simulées comme '{"temperature": "22", "unit": "celsius", "description": "Ensoleillé"}', et ajouter les informations de résultat correspondantes dans ToolCallResults -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_7.png)

###7. Continuer la conversation

Ajoutez le message contenant le résultat de ToolCallResult à l'historique des messages, puis renvoyez la requête. Le modèle générera une réponse finale en langage naturel en fonction des résultats retournés par la fonction.

<!-- Image nécessaire : montrant la structure complète d'une deuxième requête Blueprint, combinant le User Message original, le Assistant Message retourné par le modèle (contenant des ToolCalls), ainsi que les résultats Tool Message pour former un nouveau tableau Messages, puis rappelant Send OpenAI Chat Request In World -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_8.png)

<!-- ### 9. Plan complet -->

Le schéma complet de l'appel d'outil ressemble à ceci :

<!-- Besoin d'image : Présenter un schéma complet du processus Tool Call, incluant la définition de l'outil, la première requête, le traitement de l'appel d'outil, et la séquence complète de la deuxième requête. -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_9.png) -->

### 10. Résultats d'exécution

<!-- En exécutant le schéma directeur, vous pouvez voir que le modèle retourne une réponse en langage naturel incluant les informations météorologiques. -->

<!-- Nécessite une image : capture d'écran montrant le résultat de l'exécution, avec la réponse finale du modèle affichée à l'écran, comme par exemple "La météo actuelle à Boston est ensoleillée avec une température de 22°C." -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_10.png) -->

##Utilisation avancée

###Plusieurs outils

Vous pouvez définir plusieurs outils simultanément, et le modèle choisira quelle(s) fonction(s) appeler selon ses besoins.

<!-- Besoin d'une image : montrant une esquisse définissant plusieurs Outils, par exemple définir simultanément deux Outils comme get_current_weather et get_stock_price, combinés en un tableau d'Outils via Make Array -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_multi_tools.png)

###Types de paramètres complexes

Les paramètres d'outil prennent en charge plusieurs types. Il est possible d'ajouter des définitions de paramètres plus complexes, comme des types énumération, via les champs `ExtraJsonString` ou `ExtraJsonObject` :

```json
{"enum": ["Beijing", "HongKong"]}
```

<!-- Image nécessaire : montrant un blueprint utilisant ExtraJsonString pour définir des paramètres d'énumération, avec '{"enum": ["celsius", "fahrenheit"]}' saisi dans le champ ExtraJsonString du nœud Property -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_extra_json.png)

###Autres plateformes

L'utilisation des appels d'outils (Tool Call) pour Claude, Gemini, Ollama et CllamaServer est similaire à celle d'OpenAI. Il suffit de remplacer les nœuds Request et Options correspondants. Les structures de données clés (`FAIChatPlus_ChatRequestTool`, `FAIChatPlus_ChatResponseToolCall`, etc.) sont communes à toutes ces plateformes.

--8<-- "footer_fr.md"


> Ce message a été traduit avec ChatGPT, veuillez laisser votre [**feedback**](https://github.com/disenone/wiki_blog/issues/new)signaler toute omission constatée. 
