---
layout: post
title: UE fügt Plugins über den Plugin-Quellcode hinzu.
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
description: Einfach aufzeichnen, wie man ein Plugin zu UE hinzufügt, wenn man den
  Quellcode des Plugins hat.
figures: []
---

<meta property="og:title" content="UE 通过插件源码添加插件" />

#UE fügt Plugins durch das Hinzufügen von Plug-in-Quellcode hinzu.

#Plugin hinzufügen

> Einfach festhalten, wie man ein Plugin hinzufügt, wenn man den Quellcode des Plugins hat.

Mit dem Plugin [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)als Beispiel

Legen Sie den Quellcode im Plugins-Verzeichnis ab.
- (Dieser Schritt kann unterlassen werden) Modifizieren Sie die .uproject-Datei des Projekts und fügen Sie im Feld Plugins hinzu:
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
Klicken Sie mit der rechten Maustaste auf die Uproject-Datei, wählen Sie "Visual Studio-Projektdateien generieren" und aktualisieren Sie die sln-Projektdatei.
- Öffnen Sie die sln-Datei und kompilieren Sie das Projekt.

#Legen Sie die Sprache fest.

Ändern Sie die Konfigurationsdatei `DefaultEditor.ini` und fügen Sie den neuen Pfad hinzu:

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```


--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte bei [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte weisen Sie auf eventuelle Auslassungen hin. 
