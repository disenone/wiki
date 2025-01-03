---
layout: post
title: UE peut ajouter des plugins en utilisant le code source du plugin.
date: 2023-12-01
categories:
- c++
- ue
catalog: true
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: Simple record of how to add plugins to UE with plugin source code.
figures: []
---

<meta property="og:title" content="UE 通过插件源码添加插件" />

#L'UE ajoute des plugins en intégrant le code source du plugin.

#Ajouter des extensions

> Je vais noter brièvement comment ajouter un plugin lorsque vous avez accès au code source du plugin.

Avec le plug-in [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)Pour exemple

Placez le code source dans le répertoire Plugins.
- Modifier le fichier .uproject du projet (cette étape peut être ignorée), ajouter ce qui suit sous le champ Plugins :
    ```json
        "Plugins": [
        {
            "Name": "EditorPlus",
            "Enabled": true,
            "TargetAllowList": [
                "Editor"
            ]
        }
    ```
Cliquez avec le bouton droit sur le fichier uproject, exécutez "Générer les fichiers de projet Visual Studio", et mettez à jour le fichier de projet sln.
Ouvrez le fichier sln, compilez le projet.

#Configurer plusieurs langues.

Modifier le fichier de configuration du projet `DefaultEditor.ini`, en ajoutant le nouveau chemin :

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```


--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez [**donner votre avis**](https://github.com/disenone/wiki_blog/issues/new)Identifier toute omission. 
