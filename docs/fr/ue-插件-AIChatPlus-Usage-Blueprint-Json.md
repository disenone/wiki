---
layout: post
title: Manipulation de Json
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
- Json
- Blueprint
description: Manipulation de Json
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Json 操作" />

#Chapitre Schéma directeur - Manipulation de JSON

<!-- Besoin d'une image : affichant une vue d'ensemble de tous les nœuds de blueprint liés à Json, incluant les catégories JsonObject, JsonArray et JsonLibrary -->
![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_all.png)

##Aperçu

AIChatPlus offre une prise en charge complète des opérations de schéma JSON, facilitant le traitement des données JSON dans les schémas. Il comprend principalement trois classes :

* **UAIChatPlus_JsonObject**: Classe de manipulation d'objet JSON, utilisée pour traiter les JSON au format `{}`
* **UAIChatPlus_JsonArray** : Classe de manipulation de tableaux JSON, utilisée pour traiter les JSON au format `[]`
* **UAIChatPlus_JsonLibrary**: Bibliothèque de fonctions utilitaires JSON, fournissant des fonctions utilitaires statiques

Ces classes prennent en charge :
* Création, analyse, sérialisation de JSON
* Lire et définir les valeurs des champs
* Requête de chemin imbriqué
* Conversion entre JSON et USTRUCT
* Lecture et écriture de fichiers
* Appel en chaîne

##Opérations de base sur JsonObject

###Créez JsonObject

Utilisez `Create Json Object` pour créer un objet JSON vide :

<!-- Besoin d'une image : capture d'écran montrant un clic droit sur le schéma pour rechercher "Create Json Object" et créer un nœud -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_create_1.png)

###Analyser à partir d'une chaîne de caractères

Utiliser `Parse Json Object` pour créer un objet à partir d'une chaîne JSON :

<!-- Image nécessaire : Nœud Parse Json Object avec comme entrée une chaîne JSON telle que '{"name":"test","value":123}', et comme sorties JsonObject, bSuccess, ErrorMessage -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_parse_1.png)

###Définir la valeur d'un champ

JsonObject propose plusieurs méthodes Set qui prennent en charge l'appel en chaîne :

| Fonction | Description |
|-----|------|
| `Définir le champ de chaîne` | Définir le champ de chaîne |
| `Set Number Field` | Définir un champ numérique à virgule flottante |
| `Définir Champ Entier` | Définir un champ entier |
| `Définir le champ booléen` | 设置布尔字段 |
| `Set Object Field` | Définir un champ d'objet imbriqué |
| `Set Array Field` | Définir le champ de tableau |
| `Champ Null Défini` | Définir un champ comme null |

<!-- Besoin d'une image : montrant un blueprint d'appels en chaîne définissant plusieurs champs, comme Créer Objet Json -> Définir Champ Chaîne("nom", "joueur1") -> Définir Champ Entier("niveau", 10) -> Définir Champ Booléen("actif", vrai) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_set_1.png)

###Obtenir la valeur du champ

JsonObject propose plusieurs méthodes Get :

| Fonction | Description |
|---|---|
|-----|------|
| `Get String Field` | Obtenir le champ chaîne |
| `Get Number Field` | Obtenir le champ numérique |
| `Get Integer Field` | Obtenir le champ entier |
| `Get Boolean Field` | Obtenir un champ booléen |
| `Obtenir Champ Objet` | Obtenir le champ d'un objet imbriqué |
| `Get Array Field` | Récupérer le champ de tableau |

<!-- Besoin d'une image : montrant un blueprint pour extraire une valeur de champ depuis un JsonObject, utilisant Get String Field pour obtenir le champ "name", affichant les paramètres DefaultValue et bSuccess -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_get_1.png)

### Vérification des champs

| Fonction | Description |
|-----|------|
| `Has Field` | Vérifie si le champ existe |
| `Get Field Type` | Obtenir le type de champ |
| `Get Field Names` | Obtenir tous les noms de champs |
| `Supprimer le champ` | Supprimer le champ |
| `Clear` | Effacer tous les champs |

<!-- Image nécessaire : montrant l'utilisation de Has Field pour vérifier l'existence d'un champ et Get Field Type pour obtenir le type de champ dans le blueprint -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_check_1.png)

###Sérialisation en chaîne de caractères

Utiliser `To Json String` pour convertir un JsonObject en chaîne de caractères :

<!-- Besoin d'une image : montrant le nœud "To Json String", avec en entrée un JsonObject, le paramètre bPrettyPrint, et en sortie une chaîne JSON formatée -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_tostring_1.png)

##Opérations de base sur JsonArray

###Créer un JsonArray

Utiliser `Create Json Array` pour créer un tableau JSON vide :

<!-- Besoin d'une image : capture d'écran montrant la création du nœud Créer un tableau JSON dans Blueprint -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_create_1.png)

###Ajouter un élément

JsonArray propose plusieurs méthodes Add permettant un appel en chaîne :

| Fonction | Description |
|-----|------|
| `Add String` | Ajouter un élément chaîne |
| `Add Number` | Ajouter un élément nombre flottant |
| `Add Integer` | Ajouter un élément entier |
| `Add Boolean` | Ajouter un élément booléen |
| `Add Object` | Ajouter un objet |
| `Add Array` | Ajouter des éléments de tableau |
| `Add Null` | Ajouter un élément null |

<!-- Besoin d'une image : montrant un blueprint d'appel en chaîne pour ajouter plusieurs éléments, comme Créer un Tableau Json -> Ajouter une Chaîne("a") -> Ajouter une Chaîne("b") -> Ajouter un Entier(123) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_add_1.png)

###Obtenir l'élément

JsonArray fournit des méthodes pour accéder aux éléments par leur indice :

| Fonction | Description |
|------|-----------|
|-----|------|
| `Get String` | Obtenir un élément de chaîne |
| `Get Number` | Obtenir un élément à virgule flottante |
| `Get Integer` | Obtenir un élément entier |
| `Get Boolean` | Obtenir un élément booléen |
| `Get Object` | Obtenir l'élément objet |
| `Get Array` | Obtenir les éléments du tableau |

<!-- Image nécessaire : démontrant l'utilisation du blueprint "Get Object" pour récupérer un élément d'un tableau par son index -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_get_1.png)

###Manipulation de tableaux

| Fonction | Description |
|-----|------|
| `Length` | Obtenir la longueur du tableau |
| `Is Valid Index` | Vérifie si l'index est valide |
| `Obtenir le Type d'Élément` | Obtient le type d'élément |
| `Remove At` | Supprimer l'élément à l'index spécifié |
| `Clear` | Vider le tableau |

<!-- Besoin d'une image : montrant l'utilisation de Length pour obtenir la taille d'un tableau, en combinaison avec une boucle For pour parcourir le tableau -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_loop_1.png)

###Conversion par lots

JsonArray prend en charge la conversion par lots avec les tableaux UE :

| Fonction | Description |
|-----|------|
| `From String Array` | Créer à partir d'un tableau de chaînes |
| `Vers Tableau de Chaînes` | Convertit en tableau de chaînes |
| `Depuis un tableau d'entiers` | Création à partir d'un tableau d'entiers |
| `To Integer Array` | Convertir en tableau d'entiers |

<!-- Besoin d'une image : montrant des exemples d'utilisation de From String Array et To String Array -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_batch_1.png)

##Requête de chemin

JsonObject prend en charge l'accès aux données imbriquées en utilisant des chemins séparés par des points, comme `player.inventory.gold`.

###Obtenir la valeur par chemin

Utiliser `Get String By Path` pour obtenir une valeur de chaîne par chemin :

```json
{
    "player": {
        "name": "Hero",
        "inventory": {
            "gold": 1000
        }
    }
}
```

<!-- Image nécessaire : montrant l'utilisation du nœud Get String By Path avec le Path défini sur "player.name", illustrant la récupération d'une valeur imbriquée dans un blueprint -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_get_1.png)

###Définir la valeur par chemin

Utilisation de `Set String By Path` pour définir une valeur par chemin :

<!-- Image requise : montrant un blueprint utilisant le nœud Set String By Path pour définir une valeur avec un chemin imbriqué, affichant les paramètres FAIChatPlus_JsonPathOptions (bCaseSensitive, bCreateMissing) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_set_1.png)

###Résultats de la recherche

La requête de chemin renvoie la structure `FAIChatPlus_JsonQueryResult` qui contient :

* **bSuccess** : Indique si la requête a réussi
* **ValueType**: Le type de la valeur renvoyée
* **ErrorMessage**: Message d'erreur (en cas d'échec)

<!-- Image nécessaire : Montrant le nœud Break FAIChatPlus_JsonQueryResult, avec les champs bSuccess, ValueType, ErrorMessage visibles -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_result_1.png)

##Conversion entre JSON et USTRUCT

AIChatPlus prend en charge la conversion entre JSON et USTRUCT, facilitant son utilisation avec les structures de Blueprint.

###Chaîne JSON vers USTRUCT

Utiliser `Json String To Struct` pour convertir directement une chaîne JSON en USTRUCT :

<!-- Image requise : illustrant le nœud Json String To Struct, avec en entrée une chaîne JSON et en sortie des paramètres connectés à une variable USTRUCT personnalisée (par exemple FAIChatPlus_OpenAIChatRequestOptions) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_1.png)

###Conversion de USTRUCT en chaîne JSON

Utiliser `Struct To Json String` pour convertir une USTRUCT en chaîne JSON :

<!-- Besoin d'une image : montrant le nœud Struct To Json String, avec en entrée une variable USTRUCT, le paramètre bPrettyPrint, et en sortie une chaîne JSON -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_2.png)

###Conversion de JsonObject vers USTRUCT

Utilisation de la méthode `To Struct` avec JsonObject :

<!-- Besoin d'une image : montrant l'utilisation du nœud To Struct avec JsonObject -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_3.png)

###USTRUCT en JsonObject

Utilisez la méthode statique `From Struct` pour créer un JsonObject à partir d'une USTRUCT :

<!-- Besoin d'une image : montrant le nœud From Struct, entrée USTRUCT, sortie JsonObject -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_4.png)

##Fonctions utilitaires JsonLibrary

La bibliothèque `UAIChatPlus_JsonLibrary` offre une série de fonctions utilitaires statiques.

###Création rapide

| Fonction | Description |
|-----|------|
| `Make Json Object With String Field` | Créer rapidement un JsonObject avec un seul champ |
| `Make Json Object From String Map` | Créer un JsonObject à partir d'une Map |

<!-- Besoin d'une image : montrant l'utilisation de Make Json Object From String Map, avec une entrée TMap<FString, FString> et une sortie JsonObject en blueprint -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_make_1.png)

###Vérification

| Fonction | Description |
|-----|------|
| `Valider la Chaîne Json` | Vérifier si la chaîne JSON est valide |
| `Is Json Object` | Vérifie si c'est un objet JSON |
| `Is Json Array` | Vérifie si c'est un tableau JSON |

<!-- Image nécessaire : Visualisation d'un blueprint utilisant Validate Json String pour valider une chaîne JSON -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_validate_1.png)

###Formatage

| Fonction | Description |
|-----|------|
| `Prettify Json` | Formater JSON (avec indentation et sauts de ligne) |
| `Minify Json` | Minifier JSON (supprimer les espaces) |

<!-- Image nécessaire : illustrant l'utilisation de Prettify Json pour formater une chaîne JSON, montrant l'entrée JSON compressée et la sortie JSON formatée -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_format_1.png)

###Opération de fichiers

| Fonction | Description |
|-----|------|
| `Charger l'objet Json depuis un fichier` | Charger un JsonObject à partir d'un fichier |
| `Enregistrer l'objet Json dans un fichier` | Sauvegarder JsonObject dans un fichier |
| `Load Json Array From File` | Charger un JsonArray depuis un fichier |
| `Enregistrer un tableau Json dans un fichier` | Sauvegarder JsonArray dans un fichier |

<!-- Besoin d'une image : montrant des exemples d'utilisation de Sauvegarder Objet Json Dans Fichier et Charger Objet Json Depuis Fichier -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_file_1.png)

###Comparaison

| Fonction | Description |
|-----|------|
| `Equals Json Object` | Compare si deux JsonObject sont égaux |
| `Égale au Tableau Json` | Compare si deux JsonArray sont égaux |

<!-- Image nécessaire : montrant un plan d'utilisation de Equals Json Object pour comparer deux JsonObject -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_compare_1.png)

###Requête de chemin avancée

| Fonction | Description |
|-----|------|
| `Query String By Path` | Recherche de chaîne par chemin (prend en charge les index de tableau, comme `items[0].name`) |
| `Query Object By Path` | Rechercher un objet par chemin |
| `Query Array By Path` | Interroger un tableau par chemin |

<!-- Besoin d'une image : montrer l'utilisation de Query String By Path pour interroger un chemin avec un index de tableau, comme "data.items[0].name" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_query_1.png)

###Opération par lots

| Fonction | Description |
|-----|------|
| `Définir les champs de chaîne à partir d'une carte` | Définir en masse les champs de chaîne |
| `Get String Fields To Map` | Récupérer les champs de chaîne en masse |

<!-- Image nécessaire : illustration du Schéma de configuration en masse des champs avec Set String Fields From Map -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_batch_1.png)

##Autres opérations

###Fusionner JsonObject

Utiliser la méthode `Merge` pour fusionner deux JsonObject :

<!-- Besoin d'une image : montrant le nœud Merge, fusionnant deux JsonObject, avec affichage du paramètre bOverwrite -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_merge_1.png)

###Copier JsonObject

Utiliser la méthode `Duplicate` pour effectuer une copie profonde de JsonObject :

<!-- Besoin d'une image : montrant le blueprint d'un nœud Duplicate copiant un JsonObject -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_dup_1.png)

##Exemple d'application pratique

###Analyser la réponse de l'API

Extraire les paramètres d'appel d'outil à partir des réponses de chat IA :

<!-- Besoin d'une image : montrant un exemple complet de schéma d'analyse : de la chaîne FunctionArguments à l'analyse en JsonObject, puis utilisation de Get String Field pour récupérer la valeur du paramètre -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_1.png)

###Construire les paramètres de requête

Utilisation de JsonObject pour construire des paramètres de requête complexes :

<!-- Besoin d'une image : montrant un schéma pour construire une structure JSON imbriquée, créant un JsonObject avec plusieurs champs, incluant des JsonObject et JsonArray imbriqués -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_2.png)

###Lecture et écriture des fichiers de configuration

Charger la configuration depuis un fichier JSON, la modifier puis l'enregistrer :

<!-- Besoin d'une image illustrant le processus complet de lecture-écriture de configuration : Charger un Objet Json Depuis un Fichier -> Modifier un Champ -> Enregistrer l'Objet Json Dans un Fichier -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_3.png)

##Énumération de types

L'énumération `EAIChatPlus_JsonValueType` définit le type de valeur JSON :

| Valeur énumérée | Description |
|-------|------|
| `None` | Type inconnu |
| `Null` | valeur nulle |
| `String` | Chaîne de caractères |
| `Number` | Nombre |
| `Boolean` | Valeur booléenne |
| `Array` | Tableau |
| `Object` | Objet |

<!-- Image nécessaire : démontrant un blueprint utilisant un nœud Switch pour traiter différemment selon le JsonValueType -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_type_1.png)

--8<-- "footer_fr.md"


> Ce post a été traduit à l'aide de ChatGPT. Veuillez donner votre avis dans la section [**commentaires**](https://github.com/disenone/wiki_blog/issues/new)Pointer toute omission constatée. 
