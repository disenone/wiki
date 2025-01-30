---
layout: post
title: UE は地域化された多言語を設定します。
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: UEにおけるローカライズされた多言語の実装方法を記録する
---

<meta property="og:title" content="UE 设置本地化多语言" />

#UEのローカライズ多言語設定

> UE内での多言語ローカライズの実装方法を記録

UEの拡張メニューに慣れていない場合は、まず[UE拡張エディターメニュー](ue-扩展编辑器菜单.md)，[ue-使用パス形式の拡張メニュー](ue-使用路径形式扩展菜单.md)

本文のコードはプラグインに基づいています：[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##機能紹介

UEが提供するツールを使用すれば、ローカライズされた多言語環境を実現できます。たとえば、エディタのメニューをローカライズすることができます。

中国語メニュー：

![](assets/img/2023-ue-localization/chinese.png)

英文メニュー：

![](assets/img/2023-ue-localization/english.png)

##コード宣言

メニューのローカライズを実現するために、コード内で UE が処理する必要がある文字列を明示的に宣言し、UE が定義したマクロ `LOCTEXT` と `NSLOCTEXT` を使用する必要があります。

- ファイルの全体的な定義方式では、まず `LOCTEXT_NAMESPACE` という名前のマクロを定義します。その内容は、現在の多言語テキストが存在する名前空間です。その後、ファイル内のテキストは `LOCTEXT` を使用して定義できます。ファイルの最後でマクロ `LOCTEXT_NAMESPACE` をキャンセルします。

```cpp
// #define LOCTEXT(InKey, InTextLiteral)

#define LOCTEXT_NAMESPACE "EditorPlusTools"
LOCTEXT("Key", "Content");
#undef LOCTEXT_NAMESPACE

```

- 局部定義方式、`NSLOCTEXT`を使用し、テキストを定義する際に名前空間パラメータを付加します：

```cpp
// #define NSLOCTEXT(InNamespace, InKey, InTextLiteral)

NSLOCTEXT("EditorPlusTools", "Key", "Content");
```

UEツールは、翻訳が必要なすべてのテキストを収集するために、マクロ `LOCTEXT` と `NSLOCTEXT` の出現を検索します。

##日本語に翻訳してください：使用工具翻译文本

仮に私たちが次のようなコードでテキストを定義するとします：

```cpp
#define LOCTEXT_NAMESPACE "EditorPlusTools"
// register path node loctext
FEditorPlusPath::GetNodeByPath("/MenuTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/<Hook>Help/<MenuBar>MenuTest/<SubMenu>SubMenu1/<Section>Section1")->SetFriendlyName(LOCTEXT("Section1", "Section1"))->SetFriendlyTips(LOCTEXT("Section1Tips", "Section1Tips"));
#undef LOCTEXT_NAMESPACE
```

最初に翻訳ツールを開き、エディター設定を開きます。`編集 - エディターの環境設定`に進み、`一般 - 実験機能 - ツール - 翻訳選択器`にチェックを入れます。

![](assets/img/2023-ue-localization/editor_enable_tool.png)


次に翻訳ツールを開きます `ツール - ローカライズコントロールパネル`：

![](assets/img/2023-ue-localization/editor_open_tool.png)

新しいターゲットを作成します（デフォルトのゲーム下に作成しても構いませんが、新しく作成することで、翻訳テキストの管理や移動が容易になります）

![](assets/img/2023-ue-localization/tool_new_target.png)

設定目標參數，這裡將名稱改為 `EditorPlusTools`，載入策略為 `編輯器`，從文字收集，並添加插件目錄，目標依賴性為 `Engine, Editor`，其他配置保持不變：

![](assets/img/2023-ue-localization/tool_target_config.png)

言語設定を追加し、中国語（簡体字）と英語の2つの言語設定を確保してください。言語名をマウスでポイントすると、「zh-Hans」と「en」が表示されることを確認し、英語が選択されていることを確認してください（なぜならば、私たちのコードでは英語でテキストが定義されているため、この英語テキストを収集する必要があるためです）。

![](assets/img/2023-ue-localization/tool_target_lang.png)

テキストを収集するにはクリックしてください：

![](assets/img/2023-ue-localization/tool_target_collect.png)

収集進捗のポップアップが表示され、収集が成功するまで待ちます。成功すると緑色のチェックマークが表示されます。

![](assets/img/2023-ue-localization/tool_target_collected.png)

収集進捗ボックスを閉じて、翻訳ツールに戻ると、英語の行に収集された数量が表示されています。英語自体は翻訳する必要はなく、中国語の行の翻訳ボタンをクリックしてください：

![](assets/img/2023-ue-localization/tool_go_trans.png)

訳すと、次のようになります。

開いた後、未翻訳の欄に内容が表示されます。英文テキストの右側の欄に翻訳した内容を入力し、翻訳が全て完了したら、保存してウィンドウを閉じてください。

![](assets/img/2023-ue-localization/tool_trans.png)

テキストを日本語に翻訳してください：

クリックして文字数をカウントし、終了後には翻訳された数が中国語の列に表示されます。

![](assets/img/2023-ue-localization/tool_count.png)

最終コンパイルされたテキスト：

![](assets/img/2023-ue-localization/tool_build.png)

翻訳データは `Content\Localization\EditorPlusTools` フォルダに格納されます。各言語ごとに1つのフォルダがあり、zh-Hans内には2つのファイルがあります。`.archive`は収集および翻訳されたテキストを含み、`.locres`はコンパイルされたデータです。

![](assets/img/2023-ue-localization/tool_ret.png)

![](assets/img/2023-ue-localization/tool_ret2.png)

##翻訳されたテキストをプラグインディレクトリに保存してください。

私たちは生成されたプラグインの翻訳テキストをプロジェクトディレクトリに配置しましたが、これらのテキストをプラグイン内に移動して、プラグインと一緒に簡単に配布できるようにしたいです。

`Content\Localization\EditorPlusTools` ディレクトリをプラグインディレクトリの Content 下面に移動してください。こちらでは `Plugins\UE.EditorPlus\Content\Localization\EditorPlusTools` になります。

"DefaultEditor.ini"ファイルの設定を変更し、新しいパスを追加してください。

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```

こうして、他のプロジェクトがプラグインを取得した後は、`DefaultEditor.ini` を変更するだけで翻訳テキストを直接使用でき、再度翻訳の設定を行う必要はありません。

##注意事項

翻訳データ生成の過程でいくつかの問題に直面したため、以下に注意事項をまとめました。

コード内で定義されたテキストは、マクロ `LOCTEXT` と `NSLOCTEXT` を使用する必要があり、テキストは文字列定数でなければなりません。そうでないと、UEはそれを収集することができません。
翻訳の対象名には `.`、`Content\Localiztion\` フォルダ以下のディレクトリ名には `.` を含めないでください。UE は `.` の前の部分しか読み取りません。名前の間違いがあると、UE は翻訳テキストを読み取る際に読み取りエラーが発生する可能性があります。
- エディタプラグインに関して、コマンドラインモード `IsRunningCommandlet()` であれば、メニューや SlateUI を生成しないように判断する必要があります。コマンドラインモードでは Slate モジュールがないため、テキストを収集する際に `Assertion failed: CurrentApplication.IsValid()` というエラーが発生します。同様のエラーに遭遇した場合は、この判断を追加してみてください。具体的なエラー情報：

    > Assertion failed: CurrentApplication.IsValid() [File:E:\UE\ue5.3_git\Engine\Source\Runtime\Slate\Public\Framework\Application\SlateApplication.h] [Line: 255] 

    ![](assets/img/2023-ue-localization/tool_error.png)

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました、[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
