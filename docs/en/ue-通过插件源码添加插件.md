---
layout: post
title: UE adds plugins through plugin source code.
date: 2023-12-01
categories:
- c++
- python
catalog: true
tags:
- dev
- game
- ue
- UnreanEngine
description: Simply note how to add a plugin to UE when you have the plugin source
  code.
figures: []
---

<meta property="og:title" content="UE 通过插件源码添加插件" />

Simple record on how to add a plugin when having the plugin source code.

Using the plugin [UE.EditorPlus] as an example

- Place the source code into the Plugins directory.
- (This step is optional) Modify the project's .uproject file, add the following under the Plugins field:
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
