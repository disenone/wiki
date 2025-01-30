---
layout: post
title: UE 使用パス形式でメニューを拡張
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
---

<meta property="og:title" content="UE 使用路径形式扩展菜单" />

> UEでパス形式の拡張メニューを実装する方法を記録

UE拡張メニューに慣れていない場合は、まず簡単にこちらをご覧ください：[UE拡張エディタメニュー](ue-扩展编辑器菜单.md)

本文のコードは、プラグインに基づいています：[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##ノード管理

メニューをツリー構造で管理し、親ノードは子ノードを含むことができます：

```cpp
class EDITORPLUS_API FEditorPlusMenuBase: public TSharedFromThis<FEditorPlusMenuBase>
{
protected:
	// sub menus
	TArray<TSharedRef<FEditorPlusMenuBase>> Children;
}
```

親ノードを作成する際に子ノードも同時に作成する:

```cpp
void FEditorPlusMenuBase::Register(FMenuBuilder& MenuBuilder)
{
	for (const auto Menu: Children)
	{
		Menu->Register(MenuBuilder);
	}
}
```

各ノードの具体的な作成方法は、もちろん少し異なる場合があります。オーバーライド仮想関数を使用して実装します：

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

##パスを介してノードを生成します。

ツリー構造に基づいてメニューを整理し、パス形式でメニューのツリー構造を定義することができます：

```cpp
"/<Hook>Help/<MenuBar>BarTest/<SubMenu>SubTest/<Command>Action"
```

上記の手順に従うと、一連のメニューを作成できます：

- `<Hook>Help`：Hook 名称が Help のメニューの後に位置しています
- `<MenuBar>BarTest`：MenuBarタイプのメニューを作成し、名前をBarTestとします。
`<SubMenu>SubTest`：サブノードを作成し、タイプはサブメニューで名前は SubTest
- `<Command>Action`：最後にコマンドを作成します.

インターフェース呼び出しの形式は非常にシンプルです：

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

##カスタムフォーマットでノードを生成

私たちはまだ古くて非効率な方法でメニューを作成していますが、このやり方はより詳細な設定を可能にし、コードの構造はUEのSlateUIの構文に似ています：

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

もちろん、デフォルトのパス形式とカスタムメニューは同じです。両者を自由に組み合わせることができ、非常に柔軟性があります。

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

複数の場所で定義されたメニューは、同じツリー構造に統合され、名前が同じノードは同一のノードと見なされます。言い換えれば、パスは一意であり、同じパスはメニューのノードを一意に特定します。
そのため、ノードを見つけて、設定や変更を行うこともできます：

```cpp
// set Name and Tips
FEditorPlusPath::GetNodeByPath("/<MenuBar>BarTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。こちらで[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指摘任何漏れの部分。 
