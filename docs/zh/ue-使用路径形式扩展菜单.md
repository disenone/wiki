---
layout: post
title: UE 使用路径形式扩展菜单
tags: [dev, game, UE, UnreanEngine, UE4, UE5]
---
<meta property="og:title" content="UE 使用路径形式扩展菜单" />

> 记录如何在 UE 中实现路径形式扩展菜单

如果不熟悉 UE 扩展菜单，建议先简单看下：[UE 扩展编辑器菜单](ue-扩展编辑器菜单.md)

本文代码基于插件：[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

## 节点管理

把菜单按照树的结构来管理，父节点可以包含孩子：

```cpp
class EDITORPLUS_API FEditorPlusMenuBase: public TSharedFromThis<FEditorPlusMenuBase>
{
protected:
	// sub menus
	TArray<TSharedRef<FEditorPlusMenuBase>> Children;
}
```

在创建父节点的同时创建子节点：

```cpp
void FEditorPlusMenuBase::Register(FMenuBuilder& MenuBuilder)
{
	for (const auto Menu: Children)
	{
		Menu->Register(MenuBuilder);
	}
}
```

当然每个节点的具体创建行为会有点不同，覆写虚函数来实现：

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

## 通过路径生成节点

按照树形结构组织好菜单，路径格式就可以定义一条菜单的树形结构：

```cpp
"/<Hook>Help/<MenuBar>BarTest/<SubMenu>SubTest/<Command>Action"
```

以上路径即可以定义一系列菜单的创建：

- `<Hook>Help`：位置在 Hook 名字为 Help 的菜单后
- `<MenuBar>BarTest`：创建类型 MenuBar 的菜单，名字为 BarTest
- `<SubMenu>SubTest`：创建子节点，类型 SubMenu, 名字 SubTest
- `<Command>Action`：最后创建一个命令

接口调用形式可以很简洁：

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

## 自定义形式生成节点

我们依然保留了笨重的方式来创建菜单，笨重的方式可以允许有更详细的设置，代码的组织形式跟 UE 的 SlateUI 写法有些像：

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

## 混合形式

当然，本身路径形式和自定义生成的菜单，都是相同的，它们之间可以混用，有很大的灵活性：

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

多个地方定义的菜单，会合并到同一个树形结构中，名字相同的节点会认为是同一个节点。换言之，路径是唯一的，同一个路径可以唯一确定一个菜单节点。
于是我们也可以把节点找出来，重新做一些设置和修改：

```cpp
// set Name and Tips
FEditorPlusPath::GetNodeByPath("/<MenuBar>BarTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


--8<-- "footer.md"
