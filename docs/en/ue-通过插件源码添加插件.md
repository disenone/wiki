---
layout: post
title: UE adds plugins through plugin source code.
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
description: Simple record of how to add plugins to UE with the source code.
figures: []
---

<meta property="og:title" content="UE 通过插件源码添加插件" />

#Add plugins by adding plugin source code in UE.

#Add plugin

> Simple record of how to add a plugin when you have the plugin source code.

Plugin [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)For example

Put the source code into the Plugins directory.
- (This step can be skipped) Modify the .uproject file of the project, add the following under the Plugins field:
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
- Right-click on the uproject file, execute "Generate Visual Studio Project Files", and update the sln project file.
Open the .sln file and compile the project.

#Set up multiple languages

Edit the project's configuration file `DefaultEditor.ini` to add the new path:

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```


--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
