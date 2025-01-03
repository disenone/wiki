---
layout: post
title: 透過插件原始碼來新增插件
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
description: 簡單記錄一下如何在擁有插件源碼的情況下為 UE 添加插件。
figures: []
---

<meta property="og:title" content="UE 通过插件源码添加插件" />

#透過插件原始碼在 UE 中新增插件。

#新增外掛程式

> 在擁有插件原始碼的情況下，簡單記錄如何添加插件。

使用外掛程式 [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)為例

將原始碼放置於Plugins目錄下。
- （這一步可跳過）修改專案 .uproject 檔案，新增以下內容到 Plugins 區段：
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
右鍵 uproject 檔案，執行 "Generate Visual Studio Project Files"，更新 sln 專案檔案。
請打開 sln 檔案，然後編譯專案。

#設置多語言

請修改專案的配置檔 `DefaultEditor.ini`，並新增以下路徑：

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```


--8<-- "footer_tc.md"


> 這篇文章是用 ChatGPT 翻譯的，詳情請參見[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
