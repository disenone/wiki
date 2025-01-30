---
layout: post
title: UE プラグインのソースコードを追加してプラグインを作成する
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
description: 拥有プラグインのソースコードを持っている場合に、UE にプラグインを追加する方法を簡単に記録しておきます。
figures: []
---

<meta property="og:title" content="UE 通过插件源码添加插件" />

#UE は、拡張機能のソースコードを使用して拡張機能を追加します。

#プラグインを追加する

> プラグインのソースコードを持っている場合に、プラグインを追加する方法を簡単に記録します。

プラグイン [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)例えば

Pluginsディレクトリにソースコードを配置してください。
- （このステップは実行しなくてもよい）プロジェクト .uproject ファイルを修正し、Plugins フィールドの下に追加します：
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
uprojectファイルを右クリックし、「Generate Visual Studio Project Files」を実行して、.slnプロジェクトファイルを更新してください。
slnファイルを開いて、プロジェクトをコンパイルしてください。

#多言語設定

プロジェクトの設定ファイルである `DefaultEditor.ini` に新しいパスを追加してください：

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```


--8<-- "footer_ja.md"


> この投稿は ChatGPT を使用して翻訳されました。フィードバックは[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)指摘された箇所を特定してください。 
