---
layout: post
title: UE 使用パス形式でメニューを拡張します
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
---

<meta property="og:title" content="UE 使用路径形式扩展菜单" />

> UE内でパス形式の拡張メニューを実装する方法を記録する

UEの拡張メニューに慣れていない場合は、まずこれをチェックすることをお勧めします：[UE拡張エディターメニュー](ue-扩展编辑器菜单.md)

本文のコードはプラグインに基づいている：[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##ノード管理

メニューを木構造で管理してください。親ノードに子ノードを含めることができます。

```cpp
class EDITORPLUS_API FEditorPlusMenuBase: public TSharedFromThis<FEditorPlusMenuBase>
{
protected:
	// sub menus
	TArray<TSharedRef<FEditorPlusMenuBase>> Children;
}
```

親ノードを作成する際に、同時に子ノードも作成してください：

```cpp
void FEditorPlusMenuBase::Register(FMenuBuilder& MenuBuilder)
{
	for (const auto Menu: Children)
	{
		Menu->Register(MenuBuilder);
	}
}
```

各ノードの具体的な作成動作は、少し異なる場合があります。オーバーライド仮想関数を使用して実装します：

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

##パスを通じてノードを生成します。

ツリー構造でメニューを整理し、パス形式でメニューのツリー構造を定義できます：

```cpp
"/<Hook>Help/<MenuBar>BarTest/<SubMenu>SubTest/<Command>Action"
```

上記の手順に従うことで、メニューの作成手順を定義できます:

- `<Hook>Help`は、メニュー名が Help の Hook の後ろに位置します。
- `<MenuBar>BarTest`: メニュータイプのMenuBarを作成し、名前をBarTestにします。
- `<SubMenu>SubTest`：サブメニューを作成し、タイプは SubMenu、名前は SubTest
- `<Command>Action`：最後にコマンドを作成します。

インターフェースの呼び出し形式は非常に簡潔になる可能性があります：

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

##カスタムフォーマットでノードを生成します。

私たちはまだ古くて複雑な方法でメニューを作っています。この複雑な方法によって、より詳細な設定が可能になります。コードの構造はUEのSlateUIの書き方に少し似ています：

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

##ハイブリッド形式

当然、通常、固定されたパス形式とカスタムメニュー生成は同様であり、両者を混在させることができ、非常に柔軟性があります。

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

複数の場所で定義されたメニューは、同じ名前のノードは同じノードと見なされ、同じパスはメニューノードを一意に決定します。つまり、パスは一意であり、同じパスはメニューノードを一意に識別します。
それにより、私たちはノードを見つけて、設定や修正を行うことができます。

```cpp
// set Name and Tips
FEditorPlusPath::GetNodeByPath("/<MenuBar>BarTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指すべての欠落箇所を示してください。 
