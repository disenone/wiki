---
layout: post
title: 透過插件原始碼導入UE插件
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
description: 簡單記錄一下如何在擁有插件原始碼的情況下為 UE 添加插件。
figures: []
---

<meta property="og:title" content="UE 通过插件源码添加插件" />

#UE 透過插件原始碼新增插件

#添加外掛程式

> 簡單記錄一下如何在擁有插件原始碼的情況下添加插件。

使用插件 [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)為例

將原始碼放置在「插件」目錄下。
（這一步可以不執行）修改專案 .uproject 檔案，Plugins 欄位下增加：
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
右鍵 uproject 檔案，執行 "Generate Visual Studio Project Files"，更新 sln 專案檔案
打開sln檔案，編譯專案。

#設置多語言

請修改 `DefaultEditor.ini` 配置文件，新增以下路徑：

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```


--8<-- "footer_tc.md"


> 此貼文是由 ChatGPT 翻譯的，請在 [**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
