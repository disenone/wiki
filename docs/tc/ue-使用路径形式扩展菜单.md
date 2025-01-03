---
layout: post
title: UE 使用路徑形式擴展選單
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
---

<meta property="og:title" content="UE 使用路径形式扩展菜单" />

> 紀錄如何在 UE 中實現路徑形式擴展選單

如果對於UE擴展菜單不熟悉，建議先簡單查看一下：[UE擴展編輯器菜單](ue-扩展编辑器菜单.md)

本文代碼基於插件：[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##節點管理

按照樹狀結構管理菜單，父節點可以包含子節點：

```cpp
class EDITORPLUS_API FEditorPlusMenuBase: public TSharedFromThis<FEditorPlusMenuBase>
{
protected:
	// sub menus
	TArray<TSharedRef<FEditorPlusMenuBase>> Children;
}
```

在創建父節點的同時創建子節點：

```cpp
void FEditorPlusMenuBase::Register(FMenuBuilder& MenuBuilder)
{
	for (const auto Menu: Children)
	{
		Menu->Register(MenuBuilder);
	}
}
```

當然每個節點的具體創建行為會有點不同，覆寫虛函數來實現：

```cpp
// Menubar
void FEditorPlusMenuBar::Register(FMenuBarBuilder& MenuBarBuilder)
{
	MenuBarBuilder.AddPullDownMenu(
		GetFriendlyName(),
		GetFriendlyTips(),
        // Delegate to call Register
		FEditorPlusMenuManager::GetDelegate<FNewMenuDelegate>(GetUniqueId()),       
		Hook);
}

// Section
void FEditorPlusSection::Register(FMenuBuilder& MenuBuilder)
{
	MenuBuilder.BeginSection(Hook, GetFriendlyName());
	FEditorPlusMenuBase::Register(MenuBuilder);
	MenuBuilder.EndSection();
}

// Separator
void FEditorPlusSeparator::Register(FMenuBuilder& MenuBuilder)
{
	MenuBuilder.AddMenuSeparator(Hook);
	FEditorPlusMenuBase::Register(MenuBuilder);
}

// SubMenu
void FEditorPlusSubMenu::Register(FMenuBuilder& MenuBuilder)
{
	MenuBuilder.AddSubMenu(
		GetFriendlyName(),
		GetFriendlyTips(),
		FNewMenuDelegate::CreateSP(this, &FEditorPlusSubMenu::MakeSubMenu),
		false,
		FSlateIcon(),
		true,
		Hook
	);
}

// Command
void FEditorPlusCommand::Register(FMenuBuilder& MenuBuilder)
{
    MenuBuilder.AddMenuEntry(
        CommandInfo->Label, CommandInfo->Tips, CommandInfo->Icon,
        CommandInfo->ExecuteAction, CommandInfo->Hook, CommandInfo->Type);
}

// ......
```

##透過路徑生成節點

根據樹狀結構組織菜單，路徑格式可以定義菜單的樹狀結構：

```cpp
"/<Hook>Help/<MenuBar>BarTest/<SubMenu>SubTest/<Command>Action"
```

以上路徑即可定義一系列選單的建立：

- `<Hook>Help`：位置在 Hook 名字為 Help 的選單後
- `MenuBar`菜單：建立名為 BarTest 的 MenuBar 類型菜單
- `<SubMenu>SubTest`：建立子節點，類型為 SubMenu，名稱為 SubTest
`<Command>Action`：最後建立一個指令

接口調用形式可以很簡潔：

```cpp
const FString Path = "/<Hook>Help/<MenuBar>BarTest/<SubMenu>SubTest/<Command>Action";
FEditorPlusPath::RegisterPathAction(
	Path, 
    FExecuteAction::CreateLambda([]
    {
        // do action
    })
);
```

##自訂表單生成節點

我們依然保留了笨重的方式來創建菜單，這種方式可以允許更詳細的設置，程式碼的組織形式與 UE 的 SlateUI 寫法有些相似：

```cpp
EP_NEW_MENU(FEditorPlusMenuBar)("BarTest")
->RegisterPath()
->Content({
    EP_NEW_MENU(FEditorPlusSubMenu)("SubTest")
    ->Content({
        EP_NEW_MENU(FEditorPlusCommand)("Action")
        ->BindAction(FExecuteAction::CreateLambda([]
            {
                // do action
            })),
    })
});
```

##混合形式

當然，本身路徑形式和自定義生成的菜單，都是相同的，它們之間可以混用，有很大的靈活性：

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>BarTest/<SubMenu>SubMenu/<Command>Action1", 
    EP_NEW_MENU(FEditorPlusCommand)("Action1")
    ->BindAction(FExecuteAction::CreateLambda([]
        {
            // do action
        })),
);

FEditorPlusPath::RegisterPath(
    "/<MenuBar>BarTest/<SubMenu>SubMenu/<Command>Action2", 
    EP_NEW_MENU(FEditorPlusCommand)("Action2")
    ->BindAction(FExecuteAction::CreateLambda([]
        {
            // do action
        })),
);
```

多個地方定義的選單，會合併到同一個樹狀結構中，名字相同的節點會認為是同一個節點。換言之，路徑是唯一的，同一個路徑可以唯一確定一個選單節點。
因此，我們也可以找出節點，重新進行一些設置和修改：

```cpp
// set Name and Tips
FEditorPlusPath::GetNodeByPath("/<MenuBar>BarTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


--8<-- "footer_tc.md"


> This post is translated using ChatGPT. Please provide [**feedback**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
