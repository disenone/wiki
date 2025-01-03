---
layout: post
title: UE 设置本地化多语言
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: UEでローカライズされた多言語を実装する方法を記録します。
---

<meta property="og:title" content="UE 设置本地化多语言" />

#UE ローカライズ多言語設定

> UEでのローカライゼーション多言語の実装方法を記録

UE拡張メニューに慣れていない場合は、まず簡単に[UE拡張エディタメニュー](ue-扩展编辑器菜单.md)，[Navigated to Menu by Expanding Path Format](ue-使用路径形式扩展菜单.md)

テキストを日本語に翻訳します： 

本文のコードは、[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##機能紹介

UE 自带のツールを使用して、多言語のローカライズを実現できます。たとえば、エディターのメニューをローカライズすることができます。

中国語メニュー：

![](assets/img/2023-ue-localization/chinese.png)

英文菜单：　English menu:

![](assets/img/2023-ue-localization/english.png)

##コードの宣言

メニューのローカライズを実現するために、UE で処理する必要がある文字列をコードで明示的に宣言する必要があります。`LOCTEXT` と `NSLOCTEXT` という UE が定義したマクロを使用してください。

- File-wide definition method, first define a macro called `LOCTEXT_NAMESPACE`, which contains the namespace where the current multilingual text is located. After that, texts in the file can be defined using `LOCTEXT`, and finally remove the `LOCTEXT_NAMESPACE` macro at the end of the file: 

- ファイル全体での定義方法は、まず `LOCTEXT_NAMESPACE` というマクロを定義します。これには、現在の多言語テキストが存在する名前空間が含まれています。その後、ファイル内のテキストは`LOCTEXT`を使用して定義できます。最後にファイルの末尾で`LOCTEXT_NAMESPACE`マクロを削除します。

```cpp
// #define LOCTEXT(InKey, InTextLiteral)

#define LOCTEXT_NAMESPACE "EditorPlusTools"
LOCTEXT("Key", "Content");
#undef LOCTEXT_NAMESPACE

```

局部定义方式，使用 `NSLOCTEXT`，定义文本的时候带上名字空间参数：

```cpp
// #define NSLOCTEXT(InNamespace, InKey, InTextLiteral)

NSLOCTEXT("EditorPlusTools", "Key", "Content");
```

UE工具は、`LOCTEXT`および`NSLOCTEXT`マクロの出現を検索して、翻訳が必要なすべてのテキストを収集します。

##日本語に翻訳してください：使用工具翻訳テキスト

以下のテキストを日本語に翻訳してください：

```cpp
#define LOCTEXT_NAMESPACE "EditorPlusTools"
// register path node loctext
FEditorPlusPath::GetNodeByPath("/MenuTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/<Hook>Help/<MenuBar>MenuTest/<SubMenu>SubMenu1/<Section>Section1")->SetFriendlyName(LOCTEXT("Section1", "Section1"))->SetFriendlyTips(LOCTEXT("Section1Tips", "Section1Tips"));
#undef LOCTEXT_NAMESPACE
```

まずは翻訳ツールを起動して、エディターの設定を開いてください。「編集 - エディターの設定」を選択し、「一般 - 実験的機能 - Tools - 選択したテキストの翻訳」をチェックしてください。

![](assets/img/2023-ue-localization/editor_enable_tool.png)


そのテキストを日本語に翻訳します：  
そのテキストは日本語に翻訳されます：

![](assets/img/2023-ue-localization/editor_open_tool.png)

新しいターゲットを作成してください（デフォルトのゲームの下でもかまいませんが、これらの翻訳テキストを管理および移動しやすくするために新しいターゲットを作成してください）。

![](assets/img/2023-ue-localization/tool_new_target.png)

配置されたパラメーターは、こちらで `EditorPlusTools` という名前に変更され、読み込みポリシーは `エディター`、テキストから収集され、プラグインディレクトリが追加されます。目標依存関係は `Engine, Editor` です。他の設定は変更されません：

![](assets/img/2023-ue-localization/tool_target_config.png)

言語の追加を確認し、中国語（簡体字）と英語の2つの言語があることを確実にする。言語名にマウスを置くとそれぞれ `zh-Hans` および `en` が表示されることを確認する。そして英語が選択されていることを確認する（当社のコードではテキストが英語で定義されているため、これらの英語テキストを収集する必要があります）。

![](assets/img/2023-ue-localization/tool_target_lang.png)

テキストを日本語に翻訳しています。

![](assets/img/2023-ue-localization/tool_target_collect.png)

収集の進行状況ウィンドウが表示され、収集が成功するのを待って、緑色のチェックマークが表示されます：

![](assets/img/2023-ue-localization/tool_target_collected.png)

収集進捗ウィンドウを閉じて、翻訳ツールに戻ると、英文の行に収集した数量が表示されます。英文自体は翻訳不要です。中国語の行の翻訳ボタンをクリックしてください：

![](assets/img/2023-ue-localization/tool_go_trans.png)

開いたら、翻訳されていない欄に内容が表示されます。英文テキストの右側に翻訳内容を入力し、すべての翻訳が完了したら保存してウィンドウを閉じます。

![](assets/img/2023-ue-localization/tool_trans.png)

文字をクリックして、文字数をカウントすると、完了後に翻訳された量が中国語の列に表示されます。

![](assets/img/2023-ue-localization/tool_count.png)

最後の編集テキスト：

![](assets/img/2023-ue-localization/tool_build.png)

翻訳されたデータは、`Content\Localization\EditorPlusTools` ディレクトリに格納されます。各言語ごとに1つのフォルダがあり、`zh-Hans` フォルダ内には2つのファイルが表示されます。`.archive` は収集された翻訳テキストであり、`.locres` はコンパイル後のデータです。

![](assets/img/2023-ue-localization/tool_ret.png)

![](assets/img/2023-ue-localization/tool_ret2.png)

##翻訳されたテキストをプラグインディレクトリに配置してください。

私たちはプラグインが生成した翻訳テキストをプロジェクトディレクトリに置いていますが、これらのテキストをプラグイン内に移動して、プラグインと一緒に簡単に配布できるようにしたいです。

`Content\Localization\EditorPlusTools` のディレクトリを、プラグインディレクトリの Content の下に移動してください。私の場所は `Plugins\UE.EditorPlus\Content\Localization\EditorPlusTools` です。

「DefaultEditor.ini」という設定ファイルでプロジェクトのパスを更新してください。

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```

他のプロジェクトがプラグインを取得した場合、`DefaultEditor.ini` を変更するだけで、翻訳テキストを直接使用できるため、翻訳を再構成する必要はありません。

##注意事項

翻訳データを作成する過程で、いくつかの問題に遭遇しました。以下に、注意すべき点をまとめました：

コード内でテキストを定義する場合は、`LOCTEXT`や`NSLOCTEXT`などのマクロを使用する必要があります。テキストは文字列定数である必要があり、そのようにしないとUEが収集できません。
翻訳の対象名に `.` は使えません。`Content\Localiztion\` ディレクトリ配下の名前にも `.` は使えません。UE は `.` の前の部分しか取得しませんので、翻訳テキストの読み取りに失敗します。
- エディタープラグインにおいて、コマンドラインモードであるかを判別する必要があります。`IsRunningCommandlet()`が `true` の場合、メニューやSlateUIを生成しないように制御する必要があります。なぜならコマンドラインモードではSlateモジュールが存在しないため、テキストの収集時に `Assertion failed: CurrentApplication.IsValid()` のエラーが発生する可能性があります。同様のエラーに遭遇した場合は、この条件分岐を追加してみてください。具体的なエラーメッセージ：

    > Assertion failed: CurrentApplication.IsValid() [File:E:\UE\ue5.3_git\Engine\Source\Runtime\Slate\Public\Framework\Application\SlateApplication.h] [Line: 255] 

    ![](assets/img/2023-ue-localization/tool_error.png)

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
