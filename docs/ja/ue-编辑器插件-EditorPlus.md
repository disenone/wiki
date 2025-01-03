---
layout: post
title: UE エディタープラグイン UE.EditorPlus 説明書
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
- Editor
- Editor Plus
- Editor Plugin
description: UE エディタープラグイン UE.EditorPlus 説明書
---

<meta property="og:title" content="UE 编辑器插件 EditorPlus 说明文档" />

#UE.EditorPlusの説明書

##紹介ビデオ

![type:video](assets/img/2024-ue-editorplus/market/video.mp4)

##プラグインのソースコード

[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##商城下载

[EditorPlus](https://www.unrealengine.com/marketplace/zh-CN/product/editorplus)

##プロジェクトにソースコードプラグイン EU.EditorPlus を追加します。

参考文献：

日本語に翻訳すると下記の通りです：

- 中国語：[UE 通过插件源码添加插件](https://wiki.disenone.site/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)
- English: [UE adds plugins through the plugin source code](https://wiki.disenone.site/en/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)


##プラグイン説明

UE.EditorPlus は、UE エディタのプラグインであり、エディタメニューを拡張する便利な方法を提供し、高度な拡張機能をサポートし、さまざまな実用的なエディタツールを含んでいます。このプラグインは UE5.3+ をサポートしています。


##エディタのメニューを拡張

![](assets/img/2024-ue-editorplus/menu.png)

![](assets/img/2024-ue-editorplus/toolbar.png)

###説明

エディターメニューの拡張をサポートするさまざまな方法：

パスの指定方法：`RegisterPathAction("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action")`
インスタンス化方法：`EP_NEW_MENU(FEditorPlusMenuBar)("Bar")`
- RegisterPath ("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action", EP_NEW_MENU (FEditorPlusCommand)("Action") のような混合方式：

###経路方式

エディターメニューコマンドを登録する方法は次のとおりです：

```cpp
FEditorPlusPath::RegisterPathAction(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",
    FExecuteAction::CreateLambda([]
        {
            // do action
        })
);
```

このようにして、エディターのメニューバーのHelpの後ろにBarというメニューバーを追加し、BarにSubMenuというサブメニューを追加し、SubMenuにActionという命令を追加することができます。

完整なパスの形式は次のようになります：`/<Hook>HookName/<Type1>Name1/<Type2>Name2`。最初のパスは `<Hook>` である必要があり、現時点でサポートされているタイプと制限：

＜Hook＞：メニューを生成する Hook の位置を示す。後続のパスに＜Hook＞は含まれていてはいけない。
- `<MenuBar>`: メニューバー、パスには `<Hook>, <MenuBar>, <ToolBar>` を含めないでください。
- `<ToolBar>`: ツールバー：`<Hook>`、`<MenuBar>`、`<ToolBar>`の後にはパスを記述できません。
- `<Section>`: メニューをセクションに分けます。その後のパスには `<Hook>、<MenuBar>、<Section>` が含まれてはいけません。
- `<Separator>`：メニューの区切り記号で、後続のパスには `<Hook>`、 `<MenuBar>` は使用できません。
- `<SubMenu>`: サブメニュー、後続のパスには `<Hook>`、 `<MenuBar>` が含まれてはいけません。
- `<Command>`：メニューコマンドで、後ろには任意のパスを指定しないでください。
- `<Widget>`：追加可能なカスタマイズ可能な Slate UI コンポーネント。後続にはパスを含めないでください。

より簡潔なパス形式：`/BarName/SubMenuName1/SubMenuName2/CommandName` 、タイプが指定されていない場合、デフォルトのパスは最初が `<MenuBar>` 、その次が `<SubMenu>` 、最後が `<Command>` となります。

指定がない場合、自動的に `<Hook> ` の前に `<Hook>Help` を追加して、Helpメニューの後にメニューバーを追加する。

###インスタンス化方法

ルート方法は、すべてのノードをタイプとデフォルトパラメータに基づいて自動的にインスタンス化することですが、インスタンス化を自分で制御することもでき、拡張内容をより詳細に制御することができます。

```cpp
EP_NEW_MENU(FEditorPlusMenuBar)("MyBar", "MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips"))
->RegisterPath()
->Content({
    EP_NEW_MENU(FEditorPlusSubMenu)("MySubMenu")
    ->Content({
        EP_NEW_MENU(FEditorPlusCommand)("MyAction")
        ->BindAction(FExecuteAction::CreateLambda([]
            {
                // do action
            })),
    })
});
```

`MyBar`をインスタンス化する際には、Hook名、ローカライズ名、ローカライズヒント引数（`"MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips")`）を渡すことができます。上記のコードは、パス方式で言えば `/<Hook>Help/<MenuBar>MyBar/<SubMenu>MySubMenu/<Command>MyAction`に相当します。

###混合方式

自然に、両方の方法を組み合わせて使用することも可能です：

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",
    EP_NEW_MENU(FEditorPlusCommand)("Action")
    ->BindAction(FExecuteAction::CreateLambda([]
        {
            // do action
        })),
);
```

この場合、プラグインは中間パスのノードを自動的にインスタンス化し、最終パスではユーザー自身がインスタンス化したノードが使用されます。

###さらなる使用例

ヘッダーファイル:

```cpp
#include <EditorPlusPath.h>
```

パス方式はローカライズされた言語を指定します。`EP_FNAME_HOOK_AUTO` は、パス名を自動的に`Hook`名として使用することを示します。

```cpp
FEditorPlusPath::RegisterPathAction(
        "/Bar/Action",
        FExecuteAction::CreateLambda([]
        {
            // do action
        }),
        EP_FNAME_HOOK_AUTO,
        LOCTEXT("Action", "Action"),
        LOCTEXT("ActionTips", "ActionTips"));
```

ノードを取得してローカライズテキストを設定するためのパスを使用する:

```cpp
FEditorPlusPath::GetNodeByPath("/MenuTest")
    ->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))
    ->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


パスの末尾に Slate UI コントロールを追加します。

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Widget>Widget",
    EP_NEW_MENU(FEditorPlusWidget)("Widget", LOCTEXT("Widget", "Widget"))
        ->BindWidget(SNew(SHorizontalBox)));
);
```

UEの組み込みのHookに新しいノードを追加します。

```cpp
FEditorPlusPath::RegisterPath("<Hook>EpicGamesHelp/<Separator>ExtendSeparator")
```

同じパスを複数回宣言すると、同じパスとして認識され、同じパスを継続的に拡張することができるため、

```cpp
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path1", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path1", "Path1"), LOCTEXT("Path1Tips", "Path1Tips"));
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path2", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path2", "Path2"), LOCTEXT("Path2Tips", "Path2Tips"));
```

1つのノードのパスを拡張し続ける

```cpp
auto node = FEditorPlusPath::GetNodeByPath("/MenuTest");
FEditorPlusPath::RegisterChildPath(node, "<SubMenu>Sub/<Separator>Sep");
```

パスを削除します。

```cpp
FEditorPlusPath::UnregisterPath("/MenuTest/SubMenu1/SubMenu1/Path1");
```

ツールバーを拡張
```cpp
FEditorPlusPath::RegisterPath("/<Hook>ProjectSettings/<ToolBar>MenuTestToolBar")
->Content({
    EP_NEW_MENU(FEditorPlusCommand)("ToolBarCommand1")
    ->BindAction(...)
});
```

###インターフェース説明

```cpp
class EDITORPLUS_API FEditorPlusPath
{
public:

	static TSharedPtr<FEditorPlusMenuBase> RegisterPath(const FString& Path, const TSharedPtr<FEditorPlusMenuBase>& Menu=nullptr);
	static TSharedPtr<FEditorPlusMenuBase> RegisterPath(const FString& Path, const FText& FriendlyName, const FText& FriendlyTips);
	static TSharedPtr<FEditorPlusMenuBase> RegisterPathAction(
		const FString& Path, const FExecuteAction& ExecuteAction, const FName& Hook=EP_FNAME_HOOK_AUTO,
		const FText& FriendlyName=FText::GetEmpty(), const FText& FriendlyTips=FText::GetEmpty());

	static TSharedPtr<FEditorPlusMenuBase> RegisterChildPath(
		const TSharedRef<FEditorPlusMenuBase>& InParent, const FString& Path, const TSharedPtr<FEditorPlusMenuBase>& Menu=nullptr);
	static TSharedPtr<FEditorPlusMenuBase> RegisterChildPath(
		const TSharedRef<FEditorPlusMenuBase>& InParent, const FString& Path, const FText& FriendlyName, const FText& FriendlyTips);
	static TSharedPtr<FEditorPlusMenuBase> RegisterChildPathAction(
		const TSharedRef<FEditorPlusMenuBase>& InParent, const FString& Path, const FExecuteAction& ExecuteAction,
		const FName& Hook=EP_FNAME_HOOK_AUTO, const FText& FriendlyName=FText::GetEmpty(), const FText& FriendlyTips=FText::GetEmpty());

	static bool UnregisterPath(
		const FString& Path, const TSharedPtr<FEditorPlusMenuBase>& Leaf=nullptr);

	static TSharedPtr<FEditorPlusMenuBase> GetNodeByPath(const FString& Path);
};
```

「RegisterPath」：パス登録メニュー
「RegisterPathAction」：パスメニューを生成し、末端の `<Command>` ノードに自動的にアクションをバインドします。
`RegisterChildPath`: 指定ノードに子パスを生成するために登録します。
`RegisterChildPathAction`：指定ノードに対して子パスを作成し、自動的にアクションをバインドします。
- `UnregisterPath`：パスを削除する、`Leaf` は複数の同名の末端ノードがある場合、厳密に一致することができます。削除プロセス中には、中間ノードがバックトラックされ、中間ノードに子ノードがない場合は削除されます。
「GetNodeByPath」：GetNodeByPathにより、ノードをパスで取得します。


ノードの種類

```cpp
// base class of all node
class EDITORPLUS_API FEditorPlusMenuBase: public TSharedFromThis<FEditorPlusMenuBase> {}

class EDITORPLUS_API FEditorPlusHook: public TEditorPlusMenuBaseRoot {}

class EDITORPLUS_API FEditorPlusMenuBar: public TEditorPlusMenuBaseNode {}

class EDITORPLUS_API FEditorPlusToolBar: public TEditorPlusMenuBaseNode {}

class EDITORPLUS_API FEditorPlusSection: public TEditorPlusMenuBaseNode {}

class EDITORPLUS_API FEditorPlusSeparator: public TEditorPlusMenuBaseNode{}

class EDITORPLUS_API FEditorPlusSubMenu: public TEditorPlusMenuBaseNode {}

class EDITORPLUS_API FEditorPlusCommand: public TEditorPlusMenuBaseLeaf {}

class EDITORPLUS_API FEditorPlusWidget: public TEditorPlusMenuBaseLeaf {}
```

より多くのサンプルおよびインターフェースの説明については、ソースコード[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)，テストケース [MenuTest.cpp](https://github.com/disenone/UE.EditorPlus/blob/ue5.3/Source/EditorPlusTools/Private/MenuTest/MenuTest.cpp)


###モジュール化管理

UE.EditorPlusは、拡張メニューをモジュール化管理するフレームワークを提供しています。プラグインの読み込みとアンロード時に、拡張メニューを自動的に読み込んだりアンロードする機能をサポートしています。

`IEditorPlusToolInterface`を継承した`Menu`クラスを作成し、`OnStartup`と`OnShutdown`関数をオーバーライドします。`OnStartup`はメニューを作成し、`OnShutdown`はノードの`Destroy`関数を呼び出してメニューを片付けます。ノードの参照数が0になると、自動的にクリーンアップが実行されます。

```cpp
class FMenuTest: public IEditorPlusToolInterface
{
public:
	virtual void OnStartup() override;
	virtual void OnShutdown() override;
}

void FMenuTest::OnStartup()
{
	BuildPathMenu();
	BuildCustomMenu();
	BuildMixMenu();
	BuildExtendMenu();
}

void FMenuTest::OnShutdown()
{
	for(auto Menu: Menus)
	{
		if(Menu.IsValid()) Menu->Destroy();
	}
	Menus.Empty();
}
```

メニュー管理クラスは`IEditorPlusToolManagerInterface`を継承し、`AddTools`関数をオーバーライドして、`AddTools`内でメニュークラスを追加します。

```cpp
class FEditorPlusToolsImpl: public IEditorPlusToolManagerInterface
{
public:
	virtual void AddTools() override;
}

void FEditorPlusToolsImpl::AddTools()
{
	if (!Tools.Num())
	{
		Tools.Emplace(MakeShared<FMenuTest>());
	}

}
```

プラグインの読み込みと削除時には、`StartupTools` および `ShutdownTools` 関数をそれぞれ管理クラスで呼び出します。

```cpp
void FEditorPlusToolsModule::StartupModule()
{
	Impl = FEditorPlusToolsImpl::Get();
	Impl->StartupTools();

}
void FEditorPlusToolsModule::ShutdownModule()
{
	Impl->ShutdownTools();
}
```

達成以上的配對後，在載入或卸載外掛程式時，將自動載入或卸載擴充選單。


##エディターツール

UE. EditorPlus は便利なエディターツールも提供しています。

##エディターウィンドウを作成する

EditorPlusを使用すると、新しいエディターウィンドウを簡単に作成できます。

```cpp
// register spawn tab
Tab = MakeShared<FEditorPlusTab>(LOCTEXT("ClassBrowser", "ClassBrowser"), LOCTEXT("ClassBrowserTip", "Open the ClassBrowser"));
Tab->Register<SClassBrowserTab>();

// register menu action to spawn tab
FEditorPlusPath::RegisterPathAction(
    "/EditorPlusTools/ClassBrowser",
    FExecuteAction::CreateSP(Tab.ToSharedRef(), &FEditorPlusTab::TryInvokeTab),
);
```

`SClassBrowserTab` はカスタムの UI コントロールです。

```cpp
class SClassBrowserTab final : public SCompoundWidget
{
	SLATE_BEGIN_ARGS(SClassBrowserTab)
	{}
	SLATE_END_ARGS()
    // ...
}
```

### ClassBrowser

ClassBrowserは、UEクラスビューアーで、EditorPlusTools -> ClassBrowser メニューから開くことができます。

![](assets/img/2024-ue-editorplus/classbrowser_menu.png)

![](assets/img/2024-ue-editorplus/classbrowser.png)

UEに基づいて反映され、UEのさまざまなタイプのメンバー情報や説明を簡単に表示できるようになります。曖昧な検索をサポートし、親クラスの情報に移動できます。

### MenuCollections

MenuCollections は、メニューコマンドを迅速に検索してお気に入り機能を保存するツールで、必要なメニューコマンドを素早く見つけてお気に入りを保存して効率を向上させることができます。

![](assets/img/2024-ue-editorplus/menucollection_find.png)

![](assets/img/2024-ue-editorplus/menucollection_star.png)


### SlateResourceBrowser

SlateResourceBrowser は、Slate UI リソースを迅速に閲覧できるツールであり、必要なエディタリソースをブラウズおよび検索し、エディタの拡張を容易にします。

![](assets/img/2024-ue-editorplus/slateresourcebrowser_color.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_icon.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_font.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_widgetstyle.png)

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されましたので、[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 -> どこか見落としていない点があれば指摘してください。 
