---
layout: post
title: UE Editor Plus Documentation
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: UE editor plugin UE.EditorPlus documentation
---

<meta property="og:title" content="UE 编辑器插件 EditorPlus 说明文档" />

#UE Editor Plugin UE.EditorPlus Documentation

##Plugin source code

[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Project add source code plugin EU.EditorPlus

Reference documents:

- Chinese: [UE adds plugins through plugin source code](https://disenone.github.io/wiki/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)
- English: [UE adds plugins through the plugin source code](https://disenone.github.io/wiki/en/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)


##Plugin Description

UE.EditorPlus is a UE editor plugin that provides a convenient way to expand editor menus and supports advanced methods for expansion. It also includes some practical editor tools. This plugin supports UE5.2+.


##Expand Editor Menu

###Explanation

Support for various ways to extend the editor menu:

- Path method: `RegisterPathAction("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action")`
Instantiation method: `EP_NEW_MENU(FEditorPlusMenuBar)("Bar")`
- Mixed mode: `RegisterPath("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",EP_NEW_MENU(FEditorPlusCommand)("Action")`

###Path mode

You can register an editor menu command in this way:

```cpp
FEditorPlusPath::RegisterPathAction(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",
    FExecuteAction::CreateLambda([]
        {
            // do action
        })
);
```

This way you can add a menu bar "Bar" behind the "Help" menu on the editor's menu bar. Inside "Bar", you can add a submenu "SubMenu", and inside "SubMenu" you can add a command "Action".

The complete path format will look like this: `/<Hook>HookName/<Type1>Name1/<Type2>Name2`, the first path must be `<Hook>`, the currently supported types and restrictions are:

- `<Hook>`: No `<Hook>` is allowed in the subsequent path
- `<MenuBar>`: The path behind cannot contain `<Hook>, <MenuBar>`
- `<Section>`: The path following cannot include `<Hook>, <MenuBar>, <Section>`
- `<Separator>`: The following path cannot contain `<Hook>, <MenuBar>`
- `<SubMenu>`: The following path cannot contain `<Hook>, <MenuBar>`
- `<Command>`: No path is allowed after it
- `<Widget>`: There can't be any path after it

More simplified path format: `/BarName/SubMenuName1/SubMenuName2/CommandName`, if no type is specified, the first in the path is `<MenuBar>`, the middle one is `<SubMenu>`, and the last one is `<Command>`.

If `<Hook>` is not specified, automatically prepend `<Hook>Help` to indicate adding the menu bar after the Help menu.

###Instantiation method

The path mode automatically instantiates all nodes based on type and default parameters, but we can also control instantiation ourselves to have more precise control over the expansion of content.

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

When instantiating `MyBar`, you can pass in the hook name, localized name, and localized tooltip parameters (`"MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips")`). The above code is equivalent to the path method `/<Hook>Help/<MenuBar>MyBar/<SubMenu>MySubMenu/<Command>MyAction`.

###Hybrid mode

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

In this situation, the plugin will automatically instantiate the nodes in the middle path, and the user's own instantiated nodes will be used for the final path.

###More use cases

Header file:

```cpp
#include <EditorPlusPath.h>
```

Specify the localization language through the path, `EP_FNAME_HOOK_AUTO` means automatically using the path name as the `Hook` name:

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

Retrieve nodes and set localized text through paths:

```cpp
FEditorPlusPath::GetNodeByPath("/MenuTest")
    ->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))
    ->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


Append a Slate UI control at the end of the path.

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Widget>Widget",
    EP_NEW_MENU(FEditorPlusWidget)("Widget", LOCTEXT("Widget", "Widget"))
        ->BindWidget(SNew(SHorizontalBox)));
);
```

Add a new node inside the built-in Hook of UE.

```cpp
FEditorPlusPath::RegisterPath("<Hook>EpicGamesHelp/<Separator>ExtendSeparator")
```

Repeatedly declaring the same path will be recognized as the same path, so you can continuously expand the same path.

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
- `RegisterPathAction`: Generate path menu, and automatically bind the operation to the end `<Command>` node
- `RegisterChildPath`: Generate child paths for the specified node.
`RegisterChildPathAction`: Generate child paths for the specified node and automatically bind the action.
- `UnregisterPath`: Delete path. `Leaf` can be used to specify strict matching when there are multiple nodes with the same name at the end. During the deletion process, it will backtrack to the middle nodes, and any middle nodes without any child nodes will also be deleted.
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


###Module Management

UE.EditorPlus also provides a modular framework for managing extension menus, supporting automatic loading and unloading of extension menus when plugins are loaded and unloaded.

Let the Menu class inherit `IEditorPlusToolInterface` and override the `OnStartup` and `OnShutdown` functions. `OnStartup` is responsible for creating the menu, and `OnShutdown` is responsible for calling the node's `Destroy` function to clean up the menu. When the reference count of a single node is 0, automatic cleanup will be performed.

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

Call the `StartupTools` and `ShutdownTools` functions of the management class when the plug-in is loaded and unloaded, respectively.

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

Once the above adaptation is completed, the extension menu will be automatically loaded and unloaded when the plugin is loaded and unloaded.


##Editor tools

UE.EditorPlus also provides some practical editor tools

##Create editor window

By using EditorPlus, you can easily create a new editor window.

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

![](assets/img/2024-ue-editorplus/menu.png)

![](assets/img/2024-ue-editorplus/classbrowser.png)

Based on the UE reflection, it is convenient to view various types of member information, explanations, and prompts for UE, supporting fuzzy search, and allowing for jumping to open parent class information.


--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
