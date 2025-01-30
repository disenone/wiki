---
layout: post
title: UE configure la localisation multilingue
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: Enregistrer comment réaliser une localisation multilingue dans l'UE.
---

<meta property="og:title" content="UE 设置本地化多语言" />

#UE configure la localisation multilingue

> Comment implémenter la localisation multilingue dans l'UE.

Si vous n'êtes pas familiarisé avec le menu d'extension UE, il est conseillé de jeter un œil rapide sur : [Menu de l'éditeur d'extension UE](ue-扩展编辑器菜单.md)，[ue- utilisation du chemin pour étendre le menu](ue-使用路径形式扩展菜单.md)

Le code de cet article est basé sur le plugin : [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Présentation des fonctionnalités

Les outils intégrés de l'UE permettent de réaliser la localisation multilingue, par exemple, nous pouvons localiser les menus de l'éditeur :

Menu en chinois :

![](assets/img/2023-ue-localization/chinese.png)

Menu en anglais :

![](assets/img/2023-ue-localization/english.png)

##Déclaration de code

Pour réaliser la localisation du menu, nous devons déclarer explicitement dans le code les chaînes à traiter par UE, en utilisant les macros définies par UE `LOCTEXT` et `NSLOCTEXT` :

Définir au préalable le nom de l'espace de noms global du fichier en créant une macro appelée `LOCTEXT_NAMESPACE`, qui contiendra le nom de l'espace de noms actuel des textes multilingues. Ensuite, les textes du fichier pourront être définis en utilisant `LOCTEXT`, et enfin, retirer la macro `LOCTEXT_NAMESPACE` à la fin du fichier.

```cpp
// #define LOCTEXT(InKey, InTextLiteral)

#define LOCTEXT_NAMESPACE "EditorPlusTools"
LOCTEXT("Key", "Content");
#undef LOCTEXT_NAMESPACE

```

- Méthode de définition partielle, en utilisant `NSLOCTEXT`, définir le texte en incluant le paramètre de l'espace de noms :

```cpp
// #define NSLOCTEXT(InNamespace, InKey, InTextLiteral)

NSLOCTEXT("EditorPlusTools", "Key", "Content");
```

Le plug-in UE collecte tous les textes à traduire en recherchant les occurrences des macros `LOCTEXT` et `NSLOCTEXT`.

##Utilisez un outil de traduction pour convertir ce texte en français.

Supposons que nous ayons le code suivant définissant le texte :

```cpp
#define LOCTEXT_NAMESPACE "EditorPlusTools"
// register path node loctext
FEditorPlusPath::GetNodeByPath("/MenuTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/<Hook>Help/<MenuBar>MenuTest/<SubMenu>SubMenu1/<Section>Section1")->SetFriendlyName(LOCTEXT("Section1", "Section1"))->SetFriendlyTips(LOCTEXT("Section1Tips", "Section1Tips"));
#undef LOCTEXT_NAMESPACE
```

Ouvrez d'abord l'outil de traduction en ouvrant les préférences de l'éditeur `Edit - Preferences Editor`, cochez `General - Experimental features - Tools - Translate selector`:

![](assets/img/2023-ue-localization/editor_enable_tool.png)


Ensuite, ouvrez l'outil de traduction `Outils - Panneau de contrôle de localisation` :

![](assets/img/2023-ue-localization/editor_open_tool.png)

Créer un nouvel objectif (cela peut également se faire sous le Game par défaut, créer un nouvel objectif permet de faciliter la gestion et le déplacement de ces textes traduits)

![](assets/img/2023-ue-localization/tool_new_target.png)

Configurer les paramètres de l'objectif, je renomme cela en `EditorPlusTools`, la politique de chargement est `Éditeur`, collecté à partir du texte, et ajouté le répertoire des plugins, la dépendance cible est `Engine, Editor`, les autres configurations demeurent inchangées :

![](assets/img/2023-ue-localization/tool_target_config.png)

Ajouter des langues, en veillant à inclure le chinois simplifié (中文（简体）) et l'anglais, confirmer que lorsque le curseur est placé sur le nom de la langue, `zh-Hans` et `en` s'affichent respectivement, et sélectionner l'anglais (car les textes dans notre code sont définis en anglais, nous devons ici collecter ces textes anglais) :

![](assets/img/2023-ue-localization/tool_target_lang.png)

Cliquez pour collecter le texte :

![](assets/img/2023-ue-localization/tool_target_collect.png)

Affichera une boîte de dialogue de collecte, attendre la réussite de la collecte, affichera une coche verte :

![](assets/img/2023-ue-localization/tool_target_collected.png)

Fermez la boîte de dialogue de collecte, retournez à l'outil de traduction où vous pouvez voir le nombre d'éléments collectés affiché pour la ligne en anglais. Nous n'avons pas besoin de traduire l'anglais en lui-même. Cliquez sur le bouton de traduction pour la ligne en chinois.

![](assets/img/2023-ue-localization/tool_go_trans.png)

Une fois ouvert, nous pouvons voir qu'il y a du contenu dans la colonne des traductions manquantes. Dans la colonne à droite du texte en anglais, saisissez le contenu traduit. Une fois toutes les traductions terminées, enregistrez et fermez la fenêtre.

![](assets/img/2023-ue-localization/tool_trans.png)

Cliquez sur le compteur de mots pour voir le nombre de caractères chinois traduits une fois terminé :

![](assets/img/2023-ue-localization/tool_count.png)

Veuillez traduire ce texte en langue française :

最后编译文本：

![](assets/img/2023-ue-localization/tool_build.png)

Les données traduites seront placées dans `Content\Localization\EditorPlusTools`, avec un dossier pour chaque langue. Dans le dossier zh-Hans, vous pourrez voir deux fichiers : `.archive` pour le texte collecté et traduit, et `.locres` pour les données après compilation :

![](assets/img/2023-ue-localization/tool_ret.png)

![](assets/img/2023-ue-localization/tool_ret2.png)

##Mettez le texte traduit dans le répertoire du plugin.

Nous avons placé les textes traduits générés par le plugin dans le répertoire du projet, nous devons les déplacer dans le plugin pour les publier avec celui-ci.

Déplacez le répertoire `Content\Localization\EditorPlusTools` dans le répertoire des plugins Content, ici c'est `Plugins\UE.EditorPlus\Content\Localization\EditorPlusTools`.

Modifier le fichier de configuration du projet `DefaultEditor.ini` en ajoutant le nouveau chemin :

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```

Ainsi, une fois que les autres projets ont obtenu le plugin, il leur suffit de modifier le `DefaultEditor.ini` pour pouvoir utiliser directement le texte traduit, sans avoir à reconfigurer la traduction.

##Instructions.

Au cours du processus de génération des données de traduction, certaines problématiques ont été rencontrées. Voici un résumé des points à prendre en compte :

Dans le code, les textes doivent être définis en utilisant les macros `LOCTEXT` et `NSLOCTEXT`, les textes doivent être des constantes de chaînes de caractères pour que UE puisse les collecter.
Veuillez traduire ce texte en français :

- Les noms de cible à traduire ne doivent pas contenir les symboles `.`. Les noms de répertoires sous `Content\Localiztion\` ne doivent pas contenir `.`. UE coupera seulement le nom avant le `.`. Cela peut entraîner un échec de lecture des textes traduits par UE en raison d'un nom incorrect.
- Pour le plugin de l'éditeur, il est nécessaire de déterminer si c'est en mode ligne de commande `IsRunningCommandlet()`, alors il ne faut pas générer de menu ni de SlateUI, car en mode ligne de commande, il n'y a pas de module Slate, ce qui peut entraîner une erreur lors de la collecte de texte `Assertion failed: CurrentApplication.IsValid()`. Si vous rencontrez également une erreur similaire, vous pouvez essayer d'ajouter cette vérification. Détails de l'erreur :

    > Assertion failed: CurrentApplication.IsValid() [File:E:\UE\ue5.3_git\Engine\Source\Runtime\Slate\Public\Framework\Application\SlateApplication.h] [Line: 255] 

    ![](assets/img/2023-ue-localization/tool_error.png)

--8<-- "footer_fr.md"


> Ce post a été traduit à l'aide de ChatGPT, veuillez laisser vos [**retours**](https://github.com/disenone/wiki_blog/issues/new)Veuillez indiquer toute omission. 
