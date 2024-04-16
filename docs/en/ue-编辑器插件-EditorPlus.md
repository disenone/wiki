---
layout: post
title: UE EditorPlus Documentation
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: UE EditorPlus Documentation
---

<meta property="og:title" content="UE 编辑器插件 EditorPlus 说明文档" />

#UE EditorPlus Documentation

##Introduction Video

![type:video](assets/img/2024-ue-editorplus/market/video.mp4)

##Plugin source code

[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Add source code plugin EU.EditorPlus

Reference documents:

- Chinese: [UE Adding Plugins via Plugin Source Code](https://wiki.disenone.site/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)
- English: [UE adds plugins through the plugin source code](https://wiki.disenone.site/en/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)


##Plugin Description

UE.EditorPlus is a UE editor plugin that provides a convenient way to extend the editor menu and supports advanced methods of extension, while also including some practical editor tools. This plugin supports UE5.3+.


##Extend editor menu

![](assets/img/2024-ue-editorplus/menu.png)

![](assets/img/2024-ue-editorplus/toolbar.png)

###Explanation

Support for multiple ways to extend the editor menu:

Path Method: `RegisterPathAction("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action")`
Instantiation method: `EP_NEW_MENU(FEditorPlusMenuBar)("Bar")`
- Mixed mode: `RegisterPath("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action", EP_NEW_MENU(FEditorPlusCommand)("Action")`

###Path mode

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

In this way, you can add a menu bar "Bar" after the "Help" menu in the editor's menu bar. Within the "Bar" menu, you can add a sub-menu "SubMenu", which in turn contains a command "Action".

The complete path format will look like this: `/<Hook>HookName/<Type1>Name1/<Type2>Name2`. The first path must be `<Hook>`, currently supported types and restrictions are:

- `<Hook>`: Represents the position where the menu needs to be generated in the Hook. The subsequent path should not contain `<Hook>`.
- `<MenuBar>`: Menu bar, the following path cannot contain `<Hook>, <MenuBar>, <ToolBar>`
- `<ToolBar>`: Toolbar, the following path cannot contain `<Hook>, <MenuBar>, <ToolBar>`
- `<Section>`: Menu section, the path behind cannot contain `<Hook>, <MenuBar>, <Section>`
- `<Separator>`: Menu separator, the following path cannot include `<Hook>, <MenuBar>`
- `<SubMenu>`: Submenu, the following paths should not include `<Hook>, <MenuBar>`
- `<Command>`: Menu command, there should be no path after it.
- `<Widget>`: More customizable Slate UI components for extension, no paths allowed afterwards.

Simpler path format: `/BarName/SubMenuName1/SubMenuName2/CommandName`. If no type is specified, the first part of the path is `<MenuBar>`, the middle part is `<SubMenu>`, and the last part is `<Command>`.

If `<Hook>` is not specified, automatically add `<Hook>Help` at the beginning to indicate adding a menu bar after the Help menu.

###Instantiation Method

The path method automatically instantiates all nodes according to their types and default parameters. We can also control the instantiation ourselves, allowing for more precise control over the extension's content.

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

When instantiating `MyBar`, you can pass in the Hook name, localized name, and the localized hint parameters (`"MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips")`). The code above is equivalent to the path-style `/<Hook>Help/<MenuBar>MyBar/<SubMenu>MySubMenu/<Command>MyAction`.

###Mixed mode

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

In this situation, the plugin will automatically instantiate the nodes of the intermediate paths, and the final path will use the nodes instantiated by the user themselves.

###More use cases

Header File:

```cpp
#include <EditorPlusPath.h>
```

Specify the localized language using the path mode. `EP_FNAME_HOOK_AUTO` indicates automatically using the path name as the `Hook` name:

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

Get the node by path and set localized text:

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

Add new nodes in the UE built-in Hook.

```cpp
FEditorPlusPath::RegisterPath("<Hook>EpicGamesHelp/<Separator>ExtendSeparator")
```

Multiple declarations of the same path are recognized as the same path, so the same path can be continuously expanded.

```cpp
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path1", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path1", "Path1"), LOCTEXT("Path1Tips", "Path1Tips"));
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path2", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path2", "Path2"), LOCTEXT("Path2Tips", "Path2Tips"));
```

To expand the path for a node

```cpp
auto node = FEditorPlusPath::GetNodeByPath("/MenuTest");
FEditorPlusPath::RegisterChildPath(node, "<SubMenu>Sub/<Separator>Sep");
```

Delete a path

```cpp
FEditorPlusPath::UnregisterPath("/MenuTest/SubMenu1/SubMenu1/Path1");
```

Expand Toolbar
```cpp
FEditorPlusPath::RegisterPath("/<Hook>ProjectSettings/<ToolBar>MenuTestToolBar")
->Content({
    EP_NEW_MENU(FEditorPlusCommand)("ToolBarCommand1")
    ->BindAction(...)
});
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

- `RegisterPath`: Generate path menu
- `RegisterPathAction`: Generate menu paths and automatically bind actions to the end `<Command>` nodes.
Translate these text into English language:

- `RegisterChildPath`: generate child paths for the specified node
- `RegisterChildPathAction`: Generate child paths for the specified node and automatically bind actions
- `UnregisterPath`: Delete a path. `Leaf` can be specified as an exact match when there are multiple nodes with the same name at the end. During the deletion process, intermediate nodes will be backtracked and deleted if they do not have any child nodes.
`GetNodeByPath`: Obtain a node by its path.


Node Type

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

For more examples and interface explanations, please refer to the source code [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus), Test case [MenuTest.cpp](https://github.com/disenone/UE.EditorPlus/blob/ue5.3/Source/EditorPlusTools/Private/MenuTest/MenuTest.cpp)


###Modular Management

UE.EditorPlus also provides a framework for modular management of extension menus, supporting the automatic loading and unloading of extension menus when plugins are loaded and unloaded.

Let the menu class inherit from `IEditorPlusToolInterface` and override the `OnStartup` and `OnShutdown` functions. `OnStartup` is responsible for creating the menu, and `OnShutdown` is responsible for calling the `Destroy` function of the node to clean up the menu. If the reference count of the single node is 0, automatic cleaning will be performed.

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

The menu management class inherits from `IEditorPlusToolManagerInterface` and overrides the `AddTools` function to add menu classes inside it.

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

When loading and unloading plugins, the `StartupTools` and `ShutdownTools` functions in the management class are called respectively.

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

If the above adaptation is completed, the menu for automatically loading and unloading extensions can be automatically loaded and unloaded when loading and unloading plugins.


##Editor Tools

UE.EditorPlus also provides some practical editor tools.

##Create the editor window.

With EditorPlus, you can easily create a new editor window.

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

ClassBrowser is a UE Class viewer, which can be opened through the menu EditorPlusTools -> ClassBrowser.

![](assets/img/2024-ue-editorplus/classbrowser_menu.png)

![](assets/img/2024-ue-editorplus/classbrowser.png)

Based on UE reflection, it is convenient to view various types of member information, instructions, prompts, and supports fuzzy search. It can also jump and open the information of the parent class.

### MenuCollections

**MenuCollections** is a tool for quickly searching and bookmarking menu commands. It can help you quickly find the menu commands you need to execute, and also allows you to bookmark commonly used commands, thereby enhancing efficiency.

![](assets/img/2024-ue-editorplus/menucollection_find.png)

![](assets/img/2024-ue-editorplus/menucollection_star.png)


### SlateResourceBrowser

[`SlateResourceBrowser`](https://github.com/ue4plugins/SlateResourceBrowser) is a tool that allows you to quickly view Slate UI resources. It can help you browse and locate the editor resources you need, making it easier to expand the editor.

![](assets/img/2024-ue-editorplus/slateresourcebrowser_color.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_icon.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_font.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_widgetstyle.png)

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
