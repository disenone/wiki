---
layout: post
title: UE.EditorPlus Documentation
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: UE EditorPlus Instructions
---

<meta property="og:title" content="UE 编辑器插件 EditorPlus 说明文档" />

#UE EditorPlus Documentation

##Introduction Video

![type:video](assets/img/2024-ue-editorplus/market/video.mp4)

##Plugin Source Code

[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Project added source code plugin EU.EditorPlus

Reference Document:

- Chinese: [Adding plugins to UE through plugin source code](https://disenone.github.io/wiki/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)
- English: [UE adds plugins through the plugin source code](https://disenone.github.io/wiki/en/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)


##Plugin Details

UE.EditorPlus is a UE editor plugin that provides a convenient way to extend the editor menu and supports advanced methods of expansion, while also including some practical editor tools. This plugin supports UE5.3+.


##Expand Editor menu

![](assets/img/2024-ue-editorplus/menu.png)

###Explanation

Support for expanding the editor menu in multiple ways:

Path mode: `RegisterPathAction("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action")`
Instantiation method: `EP_NEW_MENU(FEditorPlusMenuBar)("Bar")`
Mixed mode: `RegisterPath("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",EP_NEW_MENU(FEditorPlusCommand)("Action")`

###Path Mode

You can register an editor menu command in the following way:

```cpp
FEditorPlusPath::RegisterPathAction(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",
    FExecuteAction::CreateLambda([]
        {
            // do action
        })
);
```

This way, you can add a menu bar Bar after the Help menu in the editor's menu bar. Inside Bar, you can add a submenu SubMenu, and inside SubMenu, you can add a command Action.

The complete path format will be like this: `/<Hook>HookName/<Type1>Name1/<Type2>Name2`, the first path must be `<Hook>`, currently supported types and limits are:

- `<Hook>`: There should not be any `<Hook>` in the subsequent path.
- `<MenuBar>`: The path behind cannot have `<Hook>, <MenuBar>`
- `<Section>`: The path following it cannot contain `<Hook>`, `<MenuBar>`, or `<Section>`.
- `<Separator>`: The path following it cannot include `<Hook>, <MenuBar>`
- `<SubMenu>`: The path following it should not include `<Hook>, <MenuBar>`
- `<Command>`: There should be no path specified after it.
- `<Widget>`: There should not be any path after it.

Simpler form of path: `/BarName/SubMenuName1/SubMenuName2/CommandName`. If the type is not specified, the first part of the path is `<MenuBar>`, the middle part is `<SubMenu>`, and the last part is `<Command>`.

If `<Hook>` is not specified, automatically prepend `<Hook>Help` to indicate adding a menu bar after the Help menu.

###Instantiation Method

The path mode automatically instantiates all nodes based on their type and default parameters. We can also control the instantiation ourselves to have more precise control over the extension's content.

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

When instantiating `MyBar`, you can pass the Hook name, localized name, and localized hint arguments (`"MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips")`). The code above is equivalent to the path-based approach `/<Hook>Help/<MenuBar>MyBar/<SubMenu>MySubMenu/<Command>MyAction`.

###Mixed Mode

Of course, you can also use a combination of both methods:

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

In this case, the plugin will automatically instantiate the nodes in the intermediate path, while the user's own instantiated nodes will be used for the final path.

###More use cases

Header File:

```cpp
#include <EditorPlusPath.h>
```

The path method specifies the localized language, `EP_FNAME_HOOK_AUTO` represents automatically using the path name as the `Hook` name:

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

Get nodes through paths and set localized text:

```cpp
FEditorPlusPath::GetNodeByPath("/MenuTest")
    ->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))
    ->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


Add a Slate UI control to the end of the path.

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Widget>Widget",
    EP_NEW_MENU(FEditorPlusWidget)("Widget", LOCTEXT("Widget", "Widget"))
        ->BindWidget(SNew(SHorizontalBox)));
);
```

Add new nodes in the built-in Hooks of UE

```cpp
FEditorPlusPath::RegisterPath("<Hook>EpicGamesHelp/<Separator>ExtendSeparator")
```

Declare the same path multiple times, and they will be recognized as the same path, allowing for continuous expansion of the same path.

```cpp
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path1", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path1", "Path1"), LOCTEXT("Path1Tips", "Path1Tips"));
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path2", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path2", "Path2"), LOCTEXT("Path2Tips", "Path2Tips"));
```

To continue expanding the path for a node

```cpp
auto node = FEditorPlusPath::GetNodeByPath("/MenuTest");
FEditorPlusPath::RegisterChildPath(node, "<SubMenu>Sub/<Separator>Sep");
```

Delete a path

```cpp
FEditorPlusPath::UnregisterPath("/MenuTest/SubMenu1/SubMenu1/Path1");
```

###Interface Description

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

- `RegisterPath`: Generate path menu.
- `RegisterPathAction`: Generate path menu and automatically bind actions to the terminal `<Command>` nodes.
- `RegisterChildPath`: Generate child paths for the specified node.
- `RegisterChildPathAction`: Generates child paths for the specified node and automatically binds actions.
- `UnregisterPath`: Remove the path. `Leaf` can be specified for strict matching when there are multiple nodes with the same name at the end. During the deletion process, it will backtrack to the intermediate nodes, and any intermediate node without any child nodes will also be deleted.
- `GetNodeByPath`: Get node by path


Node Type

```cpp
// base class of all node
class EDITORPLUS_API FEditorPlusMenuBase: public TSharedFromThis<FEditorPlusMenuBase> {}

class EDITORPLUS_API FEditorPlusHook: public TEditorPlusMenuBaseRoot {}

class EDITORPLUS_API FEditorPlusMenuBar: public TEditorPlusMenuBaseNode {}

class EDITORPLUS_API FEditorPlusSection: public TEditorPlusMenuBaseNode {}

class EDITORPLUS_API FEditorPlusSeparator: public TEditorPlusMenuBaseNode{}

class EDITORPLUS_API FEditorPlusSubMenu: public TEditorPlusMenuBaseNode {}

class EDITORPLUS_API FEditorPlusCommand: public TEditorPlusMenuBaseLeaf {}

class EDITORPLUS_API FEditorPlusWidget: public TEditorPlusMenuBaseLeaf {}
```

For more examples and interface explanations, please refer to the source code [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus), Test case [MenuTest.cpp](https://github.com/disenone/UE.EditorPlus/blob/ue5.3/Source/EditorPlusTools/Private/MenuTest/MenuTest.cpp)


###Modular Management

UE.EditorPlus also provides a framework for managing modular extension menus, supporting the automatic loading and unloading of extension menus when plugins are loaded and unloaded.

Let the menu class inherit from `IEditorPlusToolInterface` and override the `OnStartup` and `OnShutdown` functions. `OnStartup` is responsible for creating the menu, while `OnShutdown` is responsible for calling the node's `Destroy` function to clean up the menu. If the reference count of a single node is zero, automatic cleaning will be performed.

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

The menu management class inherits `IEditorPlusToolManagerInterface` and overrides the `AddTools` function to add menu classes in it.

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

When loading and unloading plugins, the `StartupTools` and `ShutdownTools` functions of the management class are called respectively.

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

Completing the above adaptation allows for the automatic loading and unloading of plugin menus when loading and unloading extensions.


##Editor Tools

UE.EditorPlus also provides some practical editor tools.

##Create Editor Window

Using EditorPlus, you can easily create a new editor window.

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

`SClassBrowserTab` is a custom UI control.

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

**ClassBrowser** is a UE Class viewer, which can be opened through the menu **EditorPlusTools -> ClassBrowser**.

![](assets/img/2024-ue-editorplus/classbrowser_menu.png)

![](assets/img/2024-ue-editorplus/classbrowser.png)

Based on UE reflection, it facilitates the easy viewing of various types of member information, including descriptions and prompts. It supports fuzzy searching and allows for jumping to open parent class information.

### MenuCollections

MenuCollections is a menu command quick search and collection tool that can help you quickly find the menu commands you need to execute and bookmark frequently used commands to improve efficiency.

![](assets/img/2024-ue-editorplus/menucollection_find.png)

![](assets/img/2024-ue-editorplus/menucollection_star.png)


--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
