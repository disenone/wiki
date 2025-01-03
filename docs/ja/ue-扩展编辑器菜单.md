---
layout: post
title: UE 拡張エディタメニュー
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: 記録 UE 如何拡張エディターメニュー
---


<meta property="og:title" content="UE 扩展编辑器菜单" />

#UEの拡張編集メニュー

> UEでエディターメニューを拡張する方法を記録

## Hook

Hookは、メニューの拡張ポイントとして理解できます。新しいメニューコマンドをHookの前後に設定できます。UEが提供するエディタのメニューコマンドのほとんどはHookを持っています。UE5では、「Edit - Editor Preferences - General - Miscellaneous - Show UI Extension Points」を開くとすべてのメニューのHookを表示できます。

![](assets/img/2023-ue-extend_menu/show_hook.png)

![](assets/img/2023-ue-extend_menu/show_hook2.png)

##モジュールの依存関係

プロジェクトの .Build.cs ファイルに、依存モジュール LevelEditor、Slate、SlateCore、EditorStyle、EditorWidgets、UnrealEd、ToolMenus を追加する必要があります。

```c#
PrivateDependencyModuleNames.AddRange(
    new string[]
    {
        "Core",
        "Engine",
        "CoreUObject",
        "LevelEditor",
        "Slate",
        "SlateCore",
        "EditorStyle",
        "EditorWidgets",
        "UnrealEd",
        "ToolMenus",
    }
    );
```

##メニューバーを追加します。

直接上コード

```cpp
auto MenuExtender = MakeShared<FExtender>();

MenuExtender->AddMenuBarExtension(
    "Help", EExtensionHook::After,      // Create After Help
    nullptr,
    FMenuBarExtensionDelegate::CreateLambda([](FMenuBarBuilder& MenuBarBuilder)
    {
        MenuBarBuilder.AddPullDownMenu(
            TEXT("MenuTest"),       // Name
            TEXT("MenuTest"),       // Tips
            FNewMenuDelegate::CreateLambda([](FMenuBuilder& MenuBuilder)
            {
                // create sub menus
            }),
            TEXT("MenuText"));      // New Hook
    })
);
FModuleManager::LoadModuleChecked<FLevelEditorModule>("LevelEditor").GetMenuExtensibilityManager()->AddExtender(MenuExtender);
```

上記のコードを実行すると、"ヘルプ"の後に"MenuTest"というメニューバーが表示されます。

![](assets/img/2023-ue-extend_menu/bar.png)

##追加コマンド

使用するインターフェースは `MenuBuilder.AddMenuEntry` です。

```cpp
// Inside MenuTest Lambda
MenuBuilder.AddMenuEntry(
    FText::FromName("MenuTestAction"), FText::FromName("MenuTestAction"),
    FSlateIcon(), FUIAction(FExecuteAction::CreateLambda([]()
    {
        // do action
    })));
```

CreateLambdaに上記のコードを配置すると、メニューコマンドが生成されます。

![](assets/img/2023-ue-extend_menu/action.png)

##メニューをセクション別に表示します。

`MenuBuilder.BeginSection` と `MenuBuilder.EndSection` を使用してください：

```cpp
MenuBuilder.BeginSection(NAME_None, FText::FromName("MenuTestSection"));
// code to create action
MenuBuilder.EndSection();
```

##区切り記号

```cpp
MenuBuilder.AddMenuSeparator();
```

![](assets/img/2023-ue-extend_menu/section&sperator.png)

##子菜单

サブメニューは、メニューバーに類似しており、Lambda内で定義する必要があります。

```cpp
MenuBuilder.AddSubMenu(
    FText::FromName("MenuTestSub"),	
    FText::FromName("MenuTestSub"),	
    FNewMenuDelegate::CreateLambda([](FMenuBuilder& MenuBuilder)
    {
        MenuBuilder.AddMenuEntry(
            FText::FromName("MenuTestSubAction"), FText::FromName("MenuTestSubAction"),
            FSlateIcon(), FUIAction(FExecuteAction::CreateLambda([]()
            {
                // do action
            })));
    }));
```

![](assets/img/2023-ue-extend_menu/submenu.png)

#SlateUI コントロール

UI コンポーネントを追加することもできます：

```cpp
MenuBuilder.AddWidget(
    SNew(SHorizontalBox)
        + SHorizontalBox::Slot()
        .AutoWidth()
        [
            SNew(SEditableTextBox)
            .MinDesiredWidth(50)
            .Text(FText::FromName("MenuTestWidget"))
        ]
        
        + SHorizontalBox::Slot()
        .AutoWidth()
        .Padding(5, 0, 0, 0)
        [
        SNew(SButton)
        .Text(FText::FromName("ExtendWidget"))
        .OnClicked(FOnClicked::CreateLambda([]()
        {
            // do action
            return FReply::Handled();
        }))
        ],
    FText::GetEmpty()
);
```

![](assets/img/2023-ue-extend_menu/widget.png)

Slate UIの関連コンテンツについてはここでは詳しく述べませんが、興味のある方は別の記事を探してご覧ください。

#フック増加メニュー

「例えば、`ツール - プログラミング` にコマンドを追加する場合：」

```cpp
MenuExtender->AddMenuExtension(
    "Programming", EExtensionHook::After,
    nullptr,
    FMenuExtensionDelegate::CreateLambda([](FMenuBuilder& MenuBuilder)
    {
        MenuBuilder.AddMenuEntry(
        FText::FromName("MenuTestAction"), FText::FromName("MenuTestAction"),
        FSlateIcon(), FUIAction(FExecuteAction::CreateLambda([]()
        {
            // do action
        })));
    })
);
```

![](assets/img/2023-ue-extend_menu/other_hook.png)

同様に、他のメニュータイプを追加することもできます。

#完整なコード

```cpp
void BuildTestMenu()
{
	auto MenuExtender = MakeShared<FExtender>();

	MenuExtender->AddMenuBarExtension(
		"Help", EExtensionHook::After,
		nullptr,
		FMenuBarExtensionDelegate::CreateLambda([](FMenuBarBuilder& MenuBarBuilder)
		{
			MenuBarBuilder.AddPullDownMenu(
				FText::FromName("MenuTest"),
				FText::FromName("MenuTest"),
				FNewMenuDelegate::CreateLambda([](FMenuBuilder& MenuBuilder)
				{
					MenuBuilder.BeginSection(NAME_None, FText::FromName("MenuTestSection"));
					MenuBuilder.AddMenuSeparator();
					MenuBuilder.AddMenuEntry(
						FText::FromName("MenuTestAction"), FText::FromName("MenuTestAction"),
						FSlateIcon(), FUIAction(FExecuteAction::CreateLambda([]()
						{
                            // do action
						})));

					MenuBuilder.AddSubMenu(
						FText::FromName("MenuTestSubb"),
						FText::FromName("MenuTestSubb"),
						FNewMenuDelegate::CreateLambda([](FMenuBuilder& MenuBuilder)
						{
							MenuBuilder.AddMenuEntry(
								FText::FromName("MenuTestSubAction"), FText::FromName("MenuTestSubAction"),
								FSlateIcon(), FUIAction(FExecuteAction::CreateLambda([]()
								{
                                    // do action
								})));
						}));
					MenuBuilder.EndSection();

					MenuBuilder.AddWidget(
					SNew(SHorizontalBox)
						 + SHorizontalBox::Slot()
						 .AutoWidth()
						 [
							 SNew(SEditableTextBox)
							 .MinDesiredWidth(50)
							 .Text(FText::FromName("MenuTestWidget"))
						 ]
						 + SHorizontalBox::Slot()
						 .AutoWidth()
						 .Padding(5, 0, 0, 0)
						 [
							SNew(SButton)
							.Text(FText::FromName("ExtendWidget"))
							.OnClicked(FOnClicked::CreateLambda([]()
							{
								// do action
								return FReply::Handled();
							}))
						 ],
					 FText::GetEmpty()
					);
				}),
				"MenuTest");
		})
	);

	MenuExtender->AddMenuExtension(
		"Programming", EExtensionHook::After,
		nullptr,
		FMenuExtensionDelegate::CreateLambda([](FMenuBuilder& MenuBuilder)
		{
			MenuBuilder.AddMenuEntry(
			FText::FromName("MenuTestAction"), FText::FromName("MenuTestAction"),
			FSlateIcon(), FUIAction(FExecuteAction::CreateLambda([]()
			{
                // do action
			})));
		})
	);

	FModuleManager::LoadModuleChecked<FLevelEditorModule>("LevelEditor").GetMenuExtensibilityManager()->AddExtender(MenuExtender);
}
```

![](assets/img/2023-ue-extend_menu/overall.png)

--8<-- "footer_ja.md"



> この投稿はChatGPTを使用して翻訳されましたので、[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指は遺漏箇所を指摘してください。 
