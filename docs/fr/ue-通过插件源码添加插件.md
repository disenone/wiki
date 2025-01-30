---
layout: post
title: UE ajoute des plugins via le code source du plugin.
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
description: Enregistrement simple sur la façon d'ajouter un plugin à UE lorsqu'on
  possède le code source du plugin.
figures: []
---

<meta property="og:title" content="UE 通过插件源码添加插件" />

#L'UE ajoute des plugins en ajoutant du code source de plugins.

#Ajouter un plugin

> Enregistrer simplement comment ajouter un plugin lorsque l'on dispose du code source du plugin.

avec le plugin [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)"为例" translates to "pour exemple" in French.

- Placez le code source dans le répertoire Plugins.
- (Cette étape peut ne pas être exécutée) Modifiez le fichier .uproject du projet et ajoutez sous le champ Plugins :
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
Cliquez avec le bouton droit sur le fichier uproject, exécutez "Générer les fichiers de projet Visual Studio", puis mettez à jour le fichier de projet sln.
Ouvrez le fichier sln, puis compilez le projet.

#Configurer le multilingue

Modifier le fichier de configuration du projet `DefaultEditor.ini`, en ajoutant le nouveau chemin :

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```


--8<-- "footer_fr.md"


> Ce message a été traduit avec ChatGPT, veuillez laisser vos [**retours**](https://github.com/disenone/wiki_blog/issues/new)Veuillez indiquer toute omission. 
