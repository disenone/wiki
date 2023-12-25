---
layout: post
title: Use the plugin source code to add a plugin in UE.
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
description: Just a simple note on how to add plugins to Unreal Engine with the source
  code.
figures: []
---

<meta property="og:title" content="UE 通过插件源码添加插件" />

Just a simple note on how to add a plugin when you have the plugin source code.

Using the plugin [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus) as an example

- Place the source code in the Plugins directory
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
- Right-click on the uproject file, execute "Generate Visual Studio Project Files", update the sln project file
- Open the sln file, compile the project


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
