---
layout: post
title: UE 編輯器插件 UE.EditorPlus 說明文檔
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
description: UE 編輯器插件  UE.EditorPlus 說明文件
---

<meta property="og:title" content="UE 编辑器插件 EditorPlus 说明文档" />

#UE 編輯器插件 UE.EditorPlus 說明文檔

##介紹視頻

![type:video](assets/img/2024-ue-editorplus/market/video.mp4)

##插件原始碼

[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##商城下載

[EditorPlus](https://www.unrealengine.com/marketplace/zh-CN/product/editorplus)

##將此文本翻譯為繁體中文：

增加專案源代插件 EU.EditorPlus

參考文件：

- Chinese Traditional: [透過進行UE插件原始碼的添加來新增插件](https://wiki.disenone.site/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)
- English: [UE adds plugins through the plugin source code](https://wiki.disenone.site/en/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)


##插件說明

UE.EditorPlus 是一個 UE 編輯器插件，提供了一種方便的方式來擴展編輯器菜單，並支持高級方式來擴展，同時包含了一些實用的編輯器工具。本插件支持 UE5.3+。


##擴展編輯器菜單

![](assets/img/2024-ue-editorplus/menu.png)

![](assets/img/2024-ue-editorplus/toolbar.png)

###說明

支援多種方式擴展編輯器選單：

- 路徑方式：`RegisterPathAction("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action")`
- 實例化方式：`EP_NEW_MENU(FEditorPlusMenuBar)("Bar")`
- 混合方式：`RegisterPath("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",EP_NEW_MENU(FEditorPlusCommand)("Action")`

###路徑方式

您可以透過以下方式註冊編輯器選單指令：

```cpp
FEditorPlusPath::RegisterPathAction(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",
    FExecuteAction::CreateLambda([]
        {
            // do action
        })
);
```

這樣就可以在編輯器菜單欄 Help 後面增加一個菜單欄 Bar，Bar 裡面增加一個子菜單 SubMenu，SubMenu 裡面增加一個命令 Action。

完整的路徑格式將會是這樣的：`/<Hook>HookName/<Type1>Name1/<Type2>Name2`，第一個路徑必須是 `<Hook>`，目前支持的類型和限制：

- `<Hook>`：表示需要在哪個 Hook 的位置上生成菜單，後續路徑不能有 `<Hook>`
- `<MenuBar>`：菜單列，後面路徑不能有 `<Hook>, <MenuBar>, <ToolBar>`
- `<ToolBar>`: 工具列，後面路徑不能有 `<Hook>、<MenuBar>、<ToolBar>`。
- `<Section>`：菜單分節，後面路徑不能有 `<Hook>、<MenuBar>、<Section>`
- `<Separator>`：菜單分隔符，後面路徑不能有 `<Hook>、<MenuBar>`
- `<SubMenu>`：子選單，後面路徑不能有 `<Hook>, <MenuBar>`
- `<Command>`：菜單命令，後面不能有任何路徑
- `<Widget>`：更多可擴展定制的 Slate UI 組件，後面不能有任何路徑

更簡易的路徑形式：`/BarName/SubMenuName1/SubMenuName2/CommandName`，如果不指定類型，默认路徑的第一個是 `<MenuBar>`，中間的是 `<SubMenu>`，最後的是 `<Command>`。

如果沒有指定 `<Hook>`，則自動最前面加上 `<Hook>Help`，表示在 Help 菜單後面添加菜單欄。

###實例化方式

路徑方式是自動把所有節點根據類型和默認參數實例化出來，我們也可以自己控制實例化，可以更細緻控制擴展的內容。

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

在實例化 `MyBar` 時，可以傳入 Hook 名稱、本地語系名稱和本地語系提示參數（`"MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips")`）。上述程式碼等同於路徑方式 `/<Hook>Help/<MenuBar>MyBar/<SubMenu>MySubMenu/<Command>MyAction`。

###混合方式

當然還可以兩種方式混合使用：

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

在這種情況下，插件會自動實例化中間路徑的節點，最終的路徑使用用戶自己實例化的節點。

###更多用例

標頭檔案:

```cpp
#include <EditorPlusPath.h>
```

路徑方式指定本地化語言，`EP_FNAME_HOOK_AUTO` 表示自動使用路徑名稱作為 `Hook` 名稱：

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

通過路徑獲取節點並設置本地化文本：

```cpp
FEditorPlusPath::GetNodeByPath("/MenuTest")
    ->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))
    ->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


在路径末端添加一個 Slate UI 控件

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Widget>Widget",
    EP_NEW_MENU(FEditorPlusWidget)("Widget", LOCTEXT("Widget", "Widget"))
        ->BindWidget(SNew(SHorizontalBox)));
);
```

在 UE 內建的 Hook 裡面添加新的節點

```cpp
FEditorPlusPath::RegisterPath("<Hook>EpicGamesHelp/<Separator>ExtendSeparator")
```

多次聲明相同的路徑，都被識別成同一個路徑，因此可以不斷擴展相同的路徑。

```cpp
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path1", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path1", "Path1"), LOCTEXT("Path1Tips", "Path1Tips"));
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path2", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path2", "Path2"), LOCTEXT("Path2Tips", "Path2Tips"));
```

為一個節點繼續擴展路徑

```cpp
auto node = FEditorPlusPath::GetNodeByPath("/MenuTest");
FEditorPlusPath::RegisterChildPath(node, "<SubMenu>Sub/<Separator>Sep");
```

刪除一個路徑

```cpp
FEditorPlusPath::UnregisterPath("/MenuTest/SubMenu1/SubMenu1/Path1");
```

擴展工具欄
```cpp
FEditorPlusPath::RegisterPath("/<Hook>ProjectSettings/<ToolBar>MenuTestToolBar")
->Content({
    EP_NEW_MENU(FEditorPlusCommand)("ToolBarCommand1")
    ->BindAction(...)
});
```

###介面說明

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

`RegisterPath`：生成路径菜单
- `RegisterPathAction`：生成路徑菜單，並自動為末端 `<Command>` 節點綁定操作
- `RegisterChildPath`：為指定節點繼續生成子路徑
- `RegisterChildPathAction`：為指定節點繼續生成子路徑，並自動綁定操作
- `UnregisterPath`：刪除路徑，`Leaf` 在有多個同名的末端節點可以指定嚴格匹配。刪除的過程中，會回溯中間節點，一旦中間節點沒有任何子節點也會被刪除。
- `GetNodeByPath`：根據路徑獲取節點


節點類型

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

請參閱源碼以獲取更多範例和界面說明 [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)，測試用例 [MenuTest.cpp](https://github.com/disenone/UE.EditorPlus/blob/ue5.3/Source/EditorPlusTools/Private/MenuTest/MenuTest.cpp)


###模組化管理

UE.EditorPlus 還提供了一個模塊化管理擴展功能表的框架，支持插件載入和卸載時，自動載入和卸載擴展的功能表

讓選單類別繼承 `IEditorPlusToolInterface`，並覆寫 `OnStartup` 和 `OnShutdown` 函數。`OnStartup` 負責創建選單，`OnShutdown` 負責調用節點的 `Destroy` 函數清理選單。單節點的引用數歸0時，則會執行自動清理。

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

菜單管理類應繼承 `IEditorPlusToolManagerInterface`，並覆寫 `AddTools` 函數，在 `AddTools` 內添加菜單類。

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

在插件加載和卸載時分別調用管理類的 `StartupTools` 和 `ShutdownTools` 函數。

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

完成以上適配後，則可以在加載和卸載插件時，自動加載和卸載擴展的菜單。


##編輯器工具

UE.EditorPlus 還提供了一些實用的編輯器工具

##建立編輯器視窗

使用 EditorPlus，可以很簡單地創建一個新的編輯器視窗。

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

`SClassBrowserTab` 是一個自訂的 UI 控件

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

ClassBrowser 是一個 UE Class 查看器，透過選單 EditorPlusTools -> ClassBrowser 來開啟。

![](assets/img/2024-ue-editorplus/classbrowser_menu.png)

![](assets/img/2024-ue-editorplus/classbrowser.png)

基於 UE 的反映來實現，可以很方便查看 UE 各種類型的成員資訊，說明提示等，支持模糊搜索，並能跳轉打開父類的資訊。

### MenuCollections

MenuCollections 是一個菜單命令快速查找和收藏工具，能夠幫助您快速找到需要執行的菜單命令，並可以收藏常用命令，提升效率。

![](assets/img/2024-ue-editorplus/menucollection_find.png)

![](assets/img/2024-ue-editorplus/menucollection_star.png)


### SlateResourceBrowser

SlateResourceBrowser 是一個可以快速查看 Slate UI 資源的工具，能夠幫助你瀏覽和查找需要的編輯器資源，方便擴展編輯器。

![](assets/img/2024-ue-editorplus/slateresourcebrowser_color.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_icon.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_font.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_widgetstyle.png)

--8<-- "footer_tc.md"


> 此帖子是使用 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遺漏之處。 
