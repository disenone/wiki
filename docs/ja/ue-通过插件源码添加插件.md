---
layout: post
title: UE は、プラグインのソースコードを追加してプラグインを追加します。
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
description: シンプルに、UEにプラグインを追加する方法をプラグインのソースコードを持っている場合に記録しておきます。
figures: []
---

<meta property="og:title" content="UE 通过插件源码添加插件" />

#UE プラグインの追加にプラグインのソースコードを使用します。

#プラグインを追加します。

> プラグインソースコードを持っている場合にプラグインを追加する方法を簡単に記録しておきます。

(https://github.com/disenone/UE.EditorPlus)例として

Pluginsディレクトリにソースコードを配置します。
- (このステップはスキップしても構いません) .uproject ファイルを編集し、Plugins フィールドに以下を追加します：
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
uprojectファイルを右クリックし、「Generate Visual Studio Project Files」を実行して、slnプロジェクトファイルを更新します。
slnファイルを開いて、プロジェクトをコンパイルします。

#複数言語の設定

「DefaultEditor.ini」という設定ファイルを編集して、新しいパスを追加してください。

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```


--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されましたので、[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
指摘してください。 
