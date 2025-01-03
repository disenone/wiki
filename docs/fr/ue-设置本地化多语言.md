---
layout: post
title: UE met en place une localisation multilingue
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: Enregistrer comment réaliser la localisation multilingue dans l'UE
---

<meta property="og:title" content="UE 设置本地化多语言" />

#Configurer la localisation multilingue de l'UE.

> Enregistrer comment mettre en œuvre la localisation multilingue dans l'UE.

Si vous n'êtes pas familier avec le menu de l'extension UE, je vous suggère de jeter un coup d'œil rapide à : [UE Extension Editor Menu](ue-扩展编辑器菜单.md)(ue-使用路径形式扩展菜单.md)

Ce texte est basé sur le plugin : [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Description des fonctionnalités

Les outils intégrés de l'UE permettent de mettre en place une localisation multilingue, par exemple pour localiser les menus de l'éditeur :

Traduisez ce texte en langue française :

Menu en chinois :

![](assets/img/2023-ue-localization/chinese.png)

Menu en anglais :

![](assets/img/2023-ue-localization/english.png)

##Déclaration du code

Pour localiser le menu, nous devons explicitement déclarer les chaînes à traiter par l'UE dans le code en utilisant les macros prédéfinies `LOCTEXT` et `NSLOCTEXT`.

Définir tout d'abord un macro appelé `LOCTEXT_NAMESPACE` pour définir globalement le nom de l'espace de noms des textes multilingues. Ensuite, les textes du fichier peuvent être définis en utilisant `LOCTEXT`, et enfin il convient de supprimer le macro `LOCTEXT_NAMESPACE` en fin de fichier.

```cpp
// #define LOCTEXT(InKey, InTextLiteral)

#define LOCTEXT_NAMESPACE "EditorPlusTools"
LOCTEXT("Key", "Content");
#undef LOCTEXT_NAMESPACE

```

Définissez localement en utilisant `NSLOCTEXT` en incluant le paramètre de l'espace de noms lors de la définition du texte :

```cpp
// #define NSLOCTEXT(InNamespace, InKey, InTextLiteral)

NSLOCTEXT("EditorPlusTools", "Key", "Content");
```

L'outil de l'UE collecte tous les textes à traduire en recherchant les occurrences des macros `LOCTEXT` et `NSLOCTEXT`.

##Utilisez un logiciel de traduction pour convertir le texte.

Suppose we have the following code defining text:

```cpp
#define LOCTEXT_NAMESPACE "EditorPlusTools"
// register path node loctext
FEditorPlusPath::GetNodeByPath("/MenuTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/<Hook>Help/<MenuBar>MenuTest/<SubMenu>SubMenu1/<Section>Section1")->SetFriendlyName(LOCTEXT("Section1", "Section1"))->SetFriendlyTips(LOCTEXT("Section1Tips", "Section1Tips"));
#undef LOCTEXT_NAMESPACE
```

Tout d'abord, ouvrez l'outil de traduction, accédez aux préférences de l'éditeur en sélectionnant `Édition - Préférences de l'éditeur`, puis cochez `Général - Fonctionnalités expérimentales - Outils - Sélecteur de traduction` :

![](assets/img/2023-ue-localization/editor_enable_tool.png)


Ouvrez ensuite l'outil de traduction `Outils - Panneau de localisation` :

![](assets/img/2023-ue-localization/editor_open_tool.png)

Créez un nouvel objectif (cela peut également se faire sous le jeu par défaut, la création d'un nouveau objectif facilite la gestion et le déplacement de ces textes traduits).

![](assets/img/2023-ue-localization/tool_new_target.png)

Configurer les paramètres de la cible, je renomme ici le nom en `EditorPlusTools`, le type de chargement est `éditeur`, récupérer à partir du texte et ajouter le répertoire des plugins, les dépendances de la cible sont `Engine, Editor`, les autres configurations restent inchangées :

![](assets/img/2023-ue-localization/tool_target_config.png)

Veuillez ajouter des langues pour inclure le chinois simplifié (zh-Hans) et l'anglais. Assurez-vous que lorsque vous survolez un nom de langue, les codes `zh-Hans` et `en` s'affichent. Sélectionnez l'anglais car notre code utilise des textes en anglais et nous devons collecter ces textes en anglais.

![](assets/img/2023-ue-localization/tool_target_lang.png)

Cliquez pour collecter le texte:

![](assets/img/2023-ue-localization/tool_target_collect.png)

Il affichera une boîte de dialogue de collecte de progression, attendez que la collecte réussisse, puis un coche vert s'affichera.

![](assets/img/2023-ue-localization/tool_target_collected.png)

Fermez la boîte de dialogue de collecte, et revenez à l'outil de traduction où vous verrez le nombre de collecte affiché sur une ligne en anglais. Nous n'avons pas besoin de traduire l'anglais lui-même. Cliquez sur le bouton de traduction de la ligne chinoise.

![](assets/img/2023-ue-localization/tool_go_trans.png)

Ouvrez la page, vous verrez une colonne non traduite. Entrez la traduction à droite du texte anglais. Une fois la traduction terminée, enregistrez et fermez la fenêtre.

![](assets/img/2023-ue-localization/tool_trans.png)

Cliquez sur "compter les mots" pour voir le nombre de caractères traduits en chinois une fois terminé :

![](assets/img/2023-ue-localization/tool_count.png)

Veuillez traduire ce texte en langue française :

"Le texte compilé final : "

![](assets/img/2023-ue-localization/tool_build.png)

Les données traduites seront placées dans le dossier `Content\Localization\EditorPlusTools`, avec un dossier pour chaque langue. Dans le dossier zh-Hans, vous verrez deux fichiers, `.archive` contient les textes collectés et traduits, tandis que`.locres` contient les données compilées après traduction.

![](assets/img/2023-ue-localization/tool_ret.png)

![](assets/img/2023-ue-localization/tool_ret2.png)

##Placer le texte traduit dans le répertoire du plugin.

Nous avons placé les textes de traduction générés par le plugin dans le répertoire du projet. Nous devons déplacer ces textes dans le plugin pour faciliter leur publication avec le plugin.

Déplacez le répertoire `Content\Localization\EditorPlusTools` dans le répertoire du plugin Content, ici `Plugins\UE.EditorPlus\Content\Localization\EditorPlusTools`.

Veuillez modifier le fichier de configuration du projet `DefaultEditor.ini` en y ajoutant le nouveau chemin :

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```

Ainsi, une fois que d'autres projets ont obtenu le plugin, ils peuvent simplement modifier le fichier `DefaultEditor.ini` pour utiliser directement le texte traduit, sans avoir besoin de reconfigurer la traduction.

##Instructions.

Dans le processus de création de données de traduction, quelques problèmes ont été rencontrés, voici les points à noter :

Dans le code, les textes doivent être définis à l'aide des macros `LOCTEXT` et `NSLOCTEXT`. Les textes doivent être des constantes de chaîne de caractères pour qu'Unreal Engine puisse les collecter.
Veuillez traduire ce texte en langue française :
- Les noms de cible de traduction ne doivent pas contenir les symboles `.`. Les noms des répertoires sous `Content\Localiztion\` ne doivent pas contenir `.`. UE ne prendra en compte que le nom qui précède le `.`. Cela pourrait entraîner un échec de la lecture des traductions par UE en raison d'erreurs de nommage.
Pour les plugins de l'éditeur, il est nécessaire de vérifier si le mode commande est activé avec `IsRunningCommandlet()`, afin de ne pas générer de menu ni d'interface SlateUI. En effet, le module Slate n'est pas disponible en mode commande, ce qui entraîne une erreur lors de la collecte de texte avec l'énoncé `Assertion failed: CurrentApplication.IsValid()`. Si vous rencontrez une erreur similaire, vous pouvez essayer d'ajouter cette vérification. Voici le message d'erreur spécifique :

    > Assertion failed: CurrentApplication.IsValid() [File:E:\UE\ue5.3_git\Engine\Source\Runtime\Slate\Public\Framework\Application\SlateApplication.h] [Line: 255] 

    ![](assets/img/2023-ue-localization/tool_error.png)

--8<-- "footer_fr.md"


> Ce message a été traduit à l'aide de ChatGPT. Veuillez laisser vos [**commentaires**](https://github.com/disenone/wiki_blog/issues/new)Indiquez toute omission. 
