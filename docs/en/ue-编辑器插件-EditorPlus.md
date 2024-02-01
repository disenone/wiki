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
description: 'UE 编辑器插件  UE.EditorPlus 说明文档

  UE Editor Plugin UE.EditorPlus Documentation'
---

<meta property="og:title" content="UE 编辑器插件 EditorPlus 说明文档" />

#**UE.EditorPlus Documentation**

This is the documentation for the UE.EditorPlus plugin.

##Introduction Video

![type:video](assets/img/2024-ue-editorplus/market/video.mp4)

##Plugin Source Code

[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Add source code plugin EU.EditorPlus to the project.

Reference Documents:

- 中文：[UE 通过插件源码添加插件]
- English: [UE adds plugins through plugin source code](https://disenone.github.io/wiki/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)
- English: [UE adds plugins through the plugin source code](https://disenone.github.io/wiki/en/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)


##Plugin Description

UE.EditorPlus is a plugin for UE editor that provides a convenient way to extend the editor menu and supports advanced methods of extension. It also includes some useful editor tools. This plugin supports UE5.3+.


##Expand Editor Menu

![](assets/img/2024-ue-editorplus/menu.png)

![](assets/img/2024-ue-editorplus/toolbar.png)

###Explanation

Support for multiple ways to expand the editor menu:

Path method: `RegisterPathAction("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action")`
Instantiation method: `EP_NEW_MENU(FEditorPlusMenuBar)("Bar")`
Mixed mode: `RegisterPath("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action", EP_NEW_MENU(FEditorPlusCommand)("Action")`.

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

This way, you can add a menu bar "Bar" behind the "Help" menu in the editor's menu bar. Inside "Bar", you can add a submenu "SubMenu", and inside "SubMenu", you can add a command "Action".

The complete path format will be like this: `/<Hook>HookName/<Type1>Name1/<Type2>Name2`, the first path must be `<Hook>`, currently supported types and limitations are:

- `<Hook>`: Indicates where the menu needs to be generated on which Hook position, the subsequent path should not contain `<Hook>`.
- `<MenuBar>`: Menu bar, the following path cannot include `<Hook>, <MenuBar>, <ToolBar>`
- `<ToolBar>`: Toolbar, the following path cannot include `<Hook>, <MenuBar>, <ToolBar>`
- `<Section>`: Menu section, the following path cannot contain `<Hook>, <MenuBar>, <Section>`
- `<Separator>`: Menu separator, the following path cannot have `<Hook>, <MenuBar>`
- `<SubMenu>`: Submenu, the path afterwards cannot contain `<Hook>, <MenuBar>`
- `<Command>`: Menu command, no paths allowed after it.
- `<Widget>`: More expandable and customizable Slate UI components, with no paths allowed afterwards.

Simpler path format: `/BarName/SubMenuName1/SubMenuName2/CommandName`. If no type is specified, the first part of the path is `<MenuBar>`, the middle part is `<SubMenu>`, and the last part is `<Command>`.

If `<Hook>` is not specified, automatically prepend `<Hook>Help` to indicate adding a menu bar after the Help menu.

###Instantiation method.

**Path mode** automatically instantiates all nodes based on their type and default parameters. We can also control instantiation ourselves, allowing for more precise control over the extension's content.

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

When instantiating `MyBar`, you can pass the hook name, localized name, and localized tooltip parameters (`"MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips")`). The above code is equivalent to the path-style `/ <Hook>Help / <MenuBar>MyBar / <SubMenu>MySubMenu/ <Command>MyAction`.

###Hybrid Mode

Of course, you can also use a combination of the two methods:

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

In this situation, the plugin will automatically instantiate nodes in the middle path, and the final path will use nodes instantiated by the user themselves.

###More Use Cases

Header file:

```cpp
#include <EditorPlusPath.h>
```

The localization language is specified by the path method. `EP_FNAME_HOOK_AUTO` means using the path name automatically as the hook name:

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

Get nodes by path and set localized text:

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

Add new nodes in the built-in Hooks of UE.

```cpp
FEditorPlusPath::RegisterPath("<Hook>EpicGamesHelp/<Separator>ExtendSeparator")
```

Multiple declarations of the same path are recognized as the same path, so the same path can be continuously expanded.

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
- `RegisterPathAction`: Generates a path menu and automatically binds the action to the end `<Command>` node.
- `RegisterChildPath`: Generate child paths for the specified node.
- `RegisterChildPathAction`: Generates child paths for the specified node and automatically binds the action.
- `UnregisterPath`: Deletes a path. `Leaf` can be used to specify strict matching when there are multiple endpoint nodes with the same name. During the deletion process, the intermediate nodes are backtrack and will also be deleted if they have no child nodes.
- `GetNodeByPath`: Get node by path


Node Types

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


###Module Management

UE.EditorPlus also provides a modular framework for managing extension menus, supporting the automatic loading and unloading of extensions' menus when plugins are loaded and unloaded.

Let the menu class inherit from `IEditorPlusToolInterface` and override the `OnStartup` and `OnShutdown` functions. `OnStartup` is responsible for creating the menu, while `OnShutdown` is responsible for calling the `Destroy` function of the node to clean up the menu. If the reference count of the single node becomes 0, automatic cleanup will be performed.

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

The menu management class inherits `IEditorPlusToolManagerInterface` and overrides the `AddTools` function to add menu classes inside it.

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

When the plugin is loaded and unloaded, respectively call the `StartupTools` and `ShutdownTools` functions of the management class.

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

To complete the above adaptation, the menu for loading and unloading extensions will be automatically loaded and unloaded when loading and unloading plugins.


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

`ClassBrowser` is a UE Class viewer, which can be opened through the menu `EditorPlusTools -> ClassBrowser`.

![](assets/img/2024-ue-editorplus/classbrowser_menu.png)

![](assets/img/2024-ue-editorplus/classbrowser.png)

Based on the reflection of UE, it can be very convenient to view various types of member information, explanatory tips, etc. It supports fuzzy search and can jump to open the information of the parent class.

### MenuCollections

MenuCollections is a tool for quickly finding and bookmarking menu commands. It can help you quickly find the menu commands you need to execute and bookmark frequently used commands to improve efficiency.

![](assets/img/2024-ue-editorplus/menucollection_find.png)

![](assets/img/2024-ue-editorplus/menucollection_star.png)


--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
