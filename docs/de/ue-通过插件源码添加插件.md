---
layout: post
title: UE fügt Plugins durch Hinzufügen des Plugin-Quellcodes hinzu.
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
description: Einfach festhalten, wie man Plugins zu UE hinzufügt, wenn man den Quellcode
  des Plugins hat.
figures: []
---

<meta property="og:title" content="UE 通过插件源码添加插件" />

#UE fügt Plugins über den Quellcode des Plugins hinzu.

#Fügen Sie Plugins hinzu.

> Einfach festhalten, wie man Plugins hinzufügt, wenn man den Quellcode für das Plugin hat.

Mit dem Plugin [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)Für Beispiel.

Legen Sie den Quellcode in das Verzeichnis "Plugins".
- Ändern Sie die Datei .uproject des Projekts, fügen Sie im Abschnitt "Plugins" folgendes hinzu:
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
Rechtsklick auf die uproject-Datei, wählen Sie "Generate Visual Studio Project Files" aus, um die sln-Projektdatei zu aktualisieren.
Öffnen Sie die sln-Datei und kompilieren Sie das Projekt.

#Stellen Sie mehrere Sprachen ein.

Bearbeiten Sie die Konfigurationsdatei des Projekts "DefaultEditor.ini" und fügen Sie den neuen Pfad hinzu:

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```


--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte geben Sie Ihr Feedback im[**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte weisen Sie auf etwaige Auslassungen hin. 
