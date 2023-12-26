---
layout: post
title: UE adds plugins through the plugin source code.
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
description: Simply record how to add plugins to UE when you have the plugin source
  code.
figures: []
---

<meta property="og:title" content="UE 通过插件源码添加插件" />

Just a quick note on how to add a plugin when you have the plugin source code.

Plugin [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)For example

- Put the source code into the Plugins directory.
- (This step can be skipped) Modify the project's .uproject file and add the following under the Plugins field:
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
- Right-click on the uproject file, execute "Generate Visual Studio Project Files," update the sln project file.
- Open the sln file, compile the project.

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
