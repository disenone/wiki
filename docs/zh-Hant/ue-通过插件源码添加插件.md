---
layout: post
title: UE 透過插件源碼添加插件
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
description: 簡單記錄一下如何在擁有插件源碼的情況下為 UE 添加插件
figures: []
---

<meta property="og:title" content="UE 通过插件源码添加插件" />

#UE 透過插件原始碼添加外掛程式

#添加插件

> 簡單記錄一下如何在擁有插件源碼的情況下添加插件。

以插件 [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)為例

- 將源碼放到 Plugins 目錄下
- （這一步可以不執行）修改專案 .uproject 文件，Plugins 領域下增加：
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
右鍵 uproject 檔案，執行"Generate Visual Studio Project Files"，更新 sln 專案檔案
打開 sln 檔案，進行專案編譯。

#設定多語言

修改專案的配置檔案 `DefaultEditor.ini`，加入新路徑：

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```


--8<-- "footer_tc.md"


> 此帖子是使用 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
