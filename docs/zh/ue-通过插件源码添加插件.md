---
layout: post
title: UE 通过插件源码添加插件
date: 2023-12-01
categories: [c++, ue]
catalog: true
tags: [dev, game, UE, UnreanEngine, UE4, UE5]
description: |
    简单记录一下如何在拥有插件源码的情况下为 UE 添加插件
figures: []
---
<meta property="og:title" content="UE 通过插件源码添加插件" />

> 简单记录一下如何在拥有插件源码的情况下添加插件.

以插件 [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus) 为例

- 把源码放到 Plugins 目录下
- （这一步可以不执行）修改项目 .uproject 文件，Plugins 字段下增加：
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
- 右键 uproject 文件，执行 "Generate Visual Studio Project Files"，更新 sln 项目文件
- 打开 sln 文件，编译项目
