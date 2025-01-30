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
description: A simple note on how to add a plugin to UE when you have the plugin source
  code.
figures: []
---

<meta property="og:title" content="UE 通过插件源码添加插件" />

#Add plugins via plugin source code in UE.

#Add Plugin

> A brief record of how to add a plugin when you have the plugin's source code.

Using the plugin [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)For example.

Put the source code into the Plugins directory.
- (This step can be skipped) Modify the .uproject file and add under the Plugins field:
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
Right-click on the uproject file, select "Generate Visual Studio Project Files", and update the sln project file.
Open the .sln file and compile the project.

#Set up multiple languages.

Modify the project's configuration file `DefaultEditor.ini` to add the new path:

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```


--8<-- "footer_en.md"


> This post was translated using ChatGPT. Please provide feedback in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
