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

#UEエディタープラグイン UE.EditorPlus 説明文書

##紹介ビデオ

![type:video](assets/img/2024-ue-editorplus/market/video.mp4)

##プラグインソースコード

[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##商城ダウンロード

[EditorPlus](https://www.unrealengine.com/marketplace/zh-CN/product/editorplus)

##プロジェクトにソースコードプラグイン「EU.EditorPlus」を追加します。

参考文献：

- 日本語：[UEがプラグインソースコードを通じてプラグインを追加](https://wiki.disenone.site/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)
- English: [UE adds plugins through the plugin source code](https://wiki.disenone.site/en/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)


##プラグインの説明

UE.EditorPlus は、UE エディタのプラグインであり、エディタメニューを拡張する便利な方法を提供し、高度な拡張方法もサポートしています。さらに、いくつかの便利なエディタツールも含まれています。このプラグインは、UE5.3以降をサポートしています。


##拡張エディターのメニュー

![](assets/img/2024-ue-editorplus/menu.png)

![](assets/img/2024-ue-editorplus/toolbar.png)

###説明

エディターメニューを拡張するためにさまざまな方法をサポートします：

- パス方式：`RegisterPathAction("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action")`
- インスタンス化方法：`EP_NEW_MENU(FEditorPlusMenuBar)("Bar")`
- RegisterPath関数: `/MenuBar/SubMenu/Action`を渡す。EP_NEW_MENU(FEditorPlusCommand)("Action")を使って新しいメニューアクションを作成する。

###路径方式  


このような方法を使って、エディターのメニューコマンドを登録することができます。

```cpp
FEditorPlusPath::RegisterPathAction(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",
    FExecuteAction::CreateLambda([]
        {
            // do action
        })
);
```

これにより、エディタのメニューバーの「ヘルプ」後にメニューバー「Bar」を追加し、「Bar」の中にサブメニュー「SubMenu」を追加し、「SubMenu」の中にコマンド「Action」を追加することができます。

完全なパス形式は次のようになります：`/<Hook>HookName/<Type1>Name1/<Type2>Name2`、最初のパスは `<Hook>` でなければなりません。現在サポートされているタイプと制限：

- `<Hook>`: メニューを生成するフックの位置を示します。その後には `<Hook>` を含めることはできません。
- `<MenuBar>`：メニューバー、その後のパスには `<Hook>, <MenuBar>, <ToolBar>` を含めることはできません。
- `<ToolBar>`: ツールバー、後続のパスに `<Hook>, <MenuBar>, <ToolBar>` は使用できません。
- `<Section>`：メニューのセクションで、その後のパスには `<Hook>, <MenuBar>, <Section>` を含めることはできません。
- `<Separator>`: メニューの区切り記号、後ろに `<Hook>, <MenuBar>` は指定できません。
- `<SubMenu>`：サブメニュー、後のパスには `<Hook>, <MenuBar>` を含めることはできません。
- `<Command>`：メニューコマンド、パスは含めないでください。
- `<Widget>`: さらなる拡張可能なカスタマイズが可能なSlate UIコンポーネントで、後ろには何もパスが付けることはできません。

より簡潔なパス形式：`/BarName/SubMenuName1/SubMenuName2/CommandName`。タイプを指定しない場合、デフォルトのパスの最初は `<MenuBar>`、中間は `<SubMenu>`、最後は `<Command>` です。

`<Hook>` が指定されていない場合、自動的に最初に `<Hook>Help` を追加してください。これは、ヘルプメニューの後にメニューバーを追加することを意味します。

###インスタンス化方式

パス方式は、すべてのノードをタイプとデフォルトパラメータに基づいて自動的にインスタンス化しますが、私たち自身でインスタンス化を制御することもでき、拡張内容をより細かく管理することができます。

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

`MyBar`のインスタンス化時には、フック名、ローカライズ名、およびローカライズヒント引数（`"MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips")`）を渡すことができます。上記のコードは、パス形式において `/ <Hook>Help/ <MenuBar>MyBar/ <SubMenu>MySubMenu/ <Command>MyAction` に相当します。

###ハイブリッド方式

当然、それらは両方の方法を組み合わせて使用することもできます：

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

この場合、プラグインは中間パスのノードを自動的にインスタンス化し、最終的なパスはユーザー自身がインスタンス化したノードを使用します。

###もっと例を挙げてください

ヘッダーファイル:

```cpp
#include <EditorPlusPath.h>
```

パス方式はローカライズされた言語を指定し、`EP_FNAME_HOOK_AUTO` は自動的にパス名を `Hook` 名称として使用します：

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

パスを通じてノードを取得し、ローカライズされたテキストを設定します：

```cpp
FEditorPlusPath::GetNodeByPath("/MenuTest")
    ->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))
    ->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


Slate UI コントロールをパスの末尾に追加します。

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Widget>Widget",
    EP_NEW_MENU(FEditorPlusWidget)("Widget", LOCTEXT("Widget", "Widget"))
        ->BindWidget(SNew(SHorizontalBox)));
);
```

UEに付属のHookに新しいノードを追加する

```cpp
FEditorPlusPath::RegisterPath("<Hook>EpicGamesHelp/<Separator>ExtendSeparator")
```

同じパスを何度も宣言すると、同じパスとして認識されるため、同じパスを継続して拡張することができます。

```cpp
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path1", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path1", "Path1"), LOCTEXT("Path1Tips", "Path1Tips"));
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path2", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path2", "Path2"), LOCTEXT("Path2Tips", "Path2Tips"));
```

1つのノードのパスを拡張し続ける

```cpp
auto node = FEditorPlusPath::GetNodeByPath("/MenuTest");
FEditorPlusPath::RegisterChildPath(node, "<SubMenu>Sub/<Separator>Sep");
```

1つのパスを削除します。

```cpp
FEditorPlusPath::UnregisterPath("/MenuTest/SubMenu1/SubMenu1/Path1");
```

拡張ツールバー
```cpp
FEditorPlusPath::RegisterPath("/<Hook>ProjectSettings/<ToolBar>MenuTestToolBar")
->Content({
    EP_NEW_MENU(FEditorPlusCommand)("ToolBarCommand1")
    ->BindAction(...)
});
```

###インターフェイス説明

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

- `RegisterPath`：生成パスメニュー
- `RegisterPathAction`：パスメニューを生成し、末端の `<Command>` ノードに自動的に操作をバインドします。
「RegisterChildPath」：指定ノードに子パスを生成するように登録します。
- `RegisterChildPathAction`：指定されたノードに対して子パスを生成し、操作を自動的にバインドします。
- `UnregisterPath`：パスを削除します。`Leaf` は同名の末端ノードが複数ある場合、厳密な一致を指定できます。削除の過程で、中間ノードを遡り、もし中間ノードに子ノードがない場合は、それも削除されます。
「GetNodeByPath」：指定されたパスからノードを取得します。


ノードタイプ

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

より多くの例やインターフェースの説明については、ソースコード [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)，テストケース [MenuTest.cpp](https://github.com/disenone/UE.EditorPlus/blob/ue5.3/Source/EditorPlusTools/Private/MenuTest/MenuTest.cpp)


###モジュラーマネジメント

UE.EditorPlusは、拡張メニューをモジュラーに管理するフレームワークも提供しており、プラグインの読み込みおよびアンロード時に拡張メニューを自動的に読み込みおよびアンロードするサポートがされています。

メニュークラスは `IEditorPlusToolInterface` を継承し、`OnStartup` と `OnShutdown` 関数をオーバーライドします。`OnStartup` はメニューの作成を担当し、`OnShutdown` はノードの `Destroy` 関数を呼び出してメニューをクリーンアップします。単一ノードの参照数が0になると、自動クリーンアップが実行されます。

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

メニュー管理クラスは `IEditorPlusToolManagerInterface` を継承し、`AddTools` 関数をオーバーライドし、その中でメニュークラスを追加します。

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

プラグインの読み込みおよびアンロード時には、それぞれ `StartupTools` および `ShutdownTools` 関数を管理クラスから呼び出します。

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

完成以上の適合ができれば、プラグインの読み込みとアンロードの際に、拡張メニューを自動で読み込みおよびアンロードすることができます。


##エディタツール

UE.EditorPlusは便利なエディターツールも提供しています。

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

`SClassBrowserTab` はカスタム UI コントロールです。

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

ClassBrowser は、UE Class のブラウザであり、EditorPlusTools -> ClassBrowser メニューから開くことができます。

![](assets/img/2024-ue-editorplus/classbrowser_menu.png)

![](assets/img/2024-ue-editorplus/classbrowser.png)

UEの反映を利用して実現され、UEのさまざまなタイプのメンバー情報や説明のヒントなどを簡単に表示でき、あいまいな検索が可能であり、親クラスの情報に移動して開くことができます。

### MenuCollections

MenuCollections は、メニューコマンドを素早く検索して保存するツールで、必要なメニューコマンドを素早く見つけるのに役立ち、よく使うコマンドを保存して効率を向上させることができます。

![](assets/img/2024-ue-editorplus/menucollection_find.png)

![](assets/img/2024-ue-editorplus/menucollection_star.png)


### SlateResourceBrowser

SlateResourceBrowser は、Slate UI リソースを素早く閲覧できるツールであり、エディターのリソースを簡単にブラウズして必要なものを見つけるのに役立ちます。エディターの拡張が簡単になります。

![](assets/img/2024-ue-editorplus/slateresourcebrowser_color.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_icon.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_font.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_widgetstyle.png)

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。ご意見は[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)何か不足している点があれば指摘してください。 
