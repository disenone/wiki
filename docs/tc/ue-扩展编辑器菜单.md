---
layout: post
title: 擴展UE編輯器選單
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: 記錄 UE 如何擴展編輯器菜單
---


<meta property="og:title" content="UE 扩展编辑器菜单" />

#UE 擴展編輯器選單

> 記錄 UE 如何擴展編輯器功能表

## Hook

Hook 可以理解為擴展功能表的錨點，我們可以設置新添加的功能表命令在 Hook 的前面或者後面，UE 自帶的編輯器功能表命令基本都帶有 Hook，UE5 下打開 `編輯 - 編輯器偏好設置 - 通用 - 其他 - 顯示 UI 擴展點` 來顯示所有功能表的 Hook：

![](assets/img/2023-ue-extend_menu/show_hook.png)

![](assets/img/2023-ue-extend_menu/show_hook2.png)

##模塊依賴

請在專案的.Build.cs檔中加入所需的模組LevelEditor、Slate、SlateCore、EditorStyle、EditorWidgets、UnrealEd、ToolMenus：

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

##新增選單列

請直接撰寫程式碼。

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

執行以上程式碼可以看到在「幫助」後面加上了一個菜單欄 MenuTest:

![](assets/img/2023-ue-extend_menu/bar.png)

##新增指令

使用 `MenuBuilder.AddMenuEntry` 方法：

```cpp
// Inside MenuTest Lambda
MenuBuilder.AddMenuEntry(
    FText::FromName("MenuTestAction"), FText::FromName("MenuTestAction"),
    FSlateIcon(), FUIAction(FExecuteAction::CreateLambda([]()
    {
        // do action
    })));
```

將上述程式碼放入 CreateLambda 內，即可生成選單命令：

![](assets/img/2023-ue-extend_menu/action.png)

##菜單分節

使用 `MenuBuilder.BeginSection` 和 `MenuBuilder.EndSection`：

```cpp
MenuBuilder.BeginSection(NAME_None, FText::FromName("MenuTestSection"));
// code to create action
MenuBuilder.EndSection();
```

##分隔符

```cpp
MenuBuilder.AddMenuSeparator();
```

![](assets/img/2023-ue-extend_menu/section&sperator.png)

##子選單

子選單類似選單欄，需要在 Lambda 內定義：

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

#SlateUI 控制項

仍可加入 UI 元件：

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

這裡不會詳細展開有關Slate UI的內容，如果有興趣可以去找其他文章來看。

#增加選單

在「工具 - 編程」中新增一個指令，就像是在程式碼中加入了一行代碼一樣。

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

您可以考慮加入其他種類的菜單。

#完整代碼

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

--8<-- "footer_tc.md"



> 此帖文乃透過 ChatGPT 翻譯，如有[**回饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
