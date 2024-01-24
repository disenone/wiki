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

##Plug-in Source Code

[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Add source code plugin EU.EditorPlus to the project.

Reference Documents:

Chinese: ![UE 通过插件源码添加插件]

English: ![UE Adding Plugins through Plugin Source Code](https://disenone.github.io/wiki/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)
- English: [UE adds plugins through the plugin source code](https://disenone.github.io/wiki/en/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)


##Plugin Description

UE.EditorPlus is a UE editor plugin that provides a convenient way to extend editor menus and supports advanced ways to extend them, as well as including some useful editor tools. This plugin supports UE5.3+.


##Expand the editor menu.

###Explanation

Support multiple ways to extend the editor menu:

Path method: `RegisterPathAction("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action")`
Instantiation method: `EP_NEW_MENU(FEditorPlusMenuBar)("Bar")`
Mixed mode: `RegisterPath("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",EP_NEW_MENU(FEditorPlusCommand)("Action")`

###Path mode

You can register an editor menu command using this approach:

```cpp
FEditorPlusPath::RegisterPathAction(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",
    FExecuteAction::CreateLambda([]
        {
            // do action
        })
);
```

This way, you can add a menu bar "Bar" behind the "Help" menu bar in the editor. Inside "Bar", you can add a submenu called "SubMenu", and inside "SubMenu", you can add a command called "Action".

The complete format for the path will be like this: `/<Hook>HookName/<Type1>Name1/<Type2>Name2`, the first path must be `<Hook>`, and currently supported types and restrictions are:

- `<Hook>`: There can be no `<Hook>` in the following path.
- `<MenuBar>`: The path following cannot contain `<Hook>, <MenuBar>`
- `<Section>`: The following path cannot contain `<Hook>, <MenuBar>, <Section>`
- `<Separator>`: The following path cannot contain `<Hook>, <MenuBar>`
- `<SubMenu>`: The subsequent path should not include `<Hook>, <MenuBar>`
- `<Command>`: There should be no paths following it.
- `<Widget>`: There should be no path after it.

Easier path format: `/BarName/SubMenuName1/SubMenuName2/CommandName`. If no type is specified, the first part of the path is `<MenuBar>`, the middle part is `<SubMenu>`, and the last part is `<Command>`.

If `<Hook>` is not specified, `<Hook>Help` will be automatically added at the beginning to indicate appending the menu bar after the Help menu.

###Instantiation Method

The path mode automatically instantiates all nodes based on their types and default parameters. We can also control the instantiation ourselves, allowing for more precise control over the extension's content.

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

When instantiating `MyBar`, you can pass the Hook name, localized name, and localized prompt parameters (`"MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips")`). The above code is equivalent to the path format `/<Hook>Help/<MenuBar>MyBar/<SubMenu>MySubMenu/<Command>MyAction`.

###Mixed Mode

Of course, you can also use a combination of two methods:

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

In this case, the plugin will automatically instantiate the nodes in the intermediate paths, while the last path will use the nodes instantiated by the user.

###More use cases

Header File:

```cpp
#include <EditorPlusPath.h>
```

The localization language is specified through the path method. `EP_FNAME_HOOK_AUTO` indicates that the path name will be automatically used as the name for the `Hook`.

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

Get node by path and set localized text:

```cpp
FEditorPlusPath::GetNodeByPath("/MenuTest")
    ->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))
    ->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


Add a Slate UI control at the end of the path.

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Widget>Widget",
    EP_NEW_MENU(FEditorPlusWidget)("Widget", LOCTEXT("Widget", "Widget"))
        ->BindWidget(SNew(SHorizontalBox)));
);
```

Add new node in UE's built-in Hook.

```cpp
FEditorPlusPath::RegisterPath("<Hook>EpicGamesHelp/<Separator>ExtendSeparator")
```

Declare the same path multiple times, it will be recognized as the same path, so you can continuously expand the same path.

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

- `RegisterPath`: Generate path menu
- `RegisterPathAction`: Generate path menu and automatically bind actions to terminal `<Command>` nodes.
`RegisterChildPath`: Generate child paths for the specified node.
- `RegisterChildPathAction`: Generate child paths for the specified node and automatically bind actions
- `UnregisterPath`: Delete a path. Specify `Leaf` to strictly match one of the multiple nodes with the same name at the end. During the deletion process, it will backtrack on intermediate nodes. If an intermediate node has no child nodes, it will also be deleted.
- `GetNodeByPath`: Get the node by its path.


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

For more examples and interface explanations, please refer to the source code [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus), Test Case [MenuTest.cpp](https://github.com/disenone/UE.EditorPlus/blob/ue5.3/Source/EditorPlusTools/Private/MenuTest/MenuTest.cpp)


###Modular management

UE.EditorPlus also provides a framework for modularly managing extension menus, supporting automatic loading and unloading of extension menus when plugins are loaded and unloaded.

Let the menu class inherit `IEditorPlusToolInterface` and override the `OnStartup` and `OnShutdown` functions. `OnStartup` is responsible for creating the menu, and `OnShutdown` is responsible for calling the `Destroy` function of the node to clean up the menu. If the reference count of the single node is 0, automatic cleanup will be performed.

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

The menu management class inherits `IEditorPlusToolManagerInterface` and overrides the `AddTools` function to add the menu class inside it.

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

When loading and unloading plugins, the `StartupTools` and `ShutdownTools` functions of the management class are called, respectively.

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

If the above adaptation is completed, the menu for automatically loading and unloading extensions will be automatically loaded and unloaded when loading and unloading plugins.


##Editor Tools

UE.EditorPlus also provides some practical editor tools.

##Create editor window

By using EditorPlus, it is very easy to create a new editor window.

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

ClassBrowser is a UE Class viewer that can be opened through the menu EditorPlusTools -> ClassBrowser.

![](assets/img/2024-ue-editorplus/classbrowser_menu.png)

![](assets/img/2024-ue-editorplus/classbrowser.png)

Based on UE's reflection, it is convenient to view various types of member information, including descriptions and prompts. It supports fuzzy searching and can jump to open the parent class information.

### MenuCollections

**MenuCollections** is a tool for quickly searching and bookmarking menu commands. It helps you find the menu commands you need to execute quickly and allows you to bookmark commonly used commands, thereby improving efficiency.

![](assets/img/2024-ue-editorplus/menucollection_find.png)

![](assets/img/2024-ue-editorplus/menucollection_star.png)


--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
