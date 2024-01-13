---
layout: post
title: UE Editor Plugin UE.EditorPlus Documentation
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: UE EditorPlus Plugin User Manual
---

<meta property="og:title" content="UE 编辑器插件 EditorPlus 说明文档" />

#UE Editor Plugin UE.EditorPlus Documentation

##Plugin source code

[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Add the source code plugin EU.EditorPlus to the project.

Reference Document:

- Chinese: [UE add plugins through plugin source code](https://disenone.github.io/wiki/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)
- English: [UE adds plugins through the plugin source code](https://disenone.github.io/wiki/en/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)


##Plugin description

UE.EditorPlus is a UE editor plugin that provides a convenient way to extend the editor menu and supports advanced methods for extension, while also including some practical editor tools. This plugin supports UE5.2+.


##Expand the editor menu

###Explanation

Support for expanding the editor menu in multiple ways:

- Path method: `RegisterPathAction("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action")`
Instantiation method: `EP_NEW_MENU(FEditorPlusMenuBar)("Bar")`
- Mixed mode: `RegisterPath("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",EP_NEW_MENU(FEditorPlusCommand)("Action")`

###Pathway Method

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

This way, you can add a menu bar "Bar" behind the "Help" in the editor menu bar. Within "Bar," you can add a submenu called "SubMenu," and within "SubMenu," you can add a command called "Action."

The complete format of the path will be like this: `/<Hook>HookName/<Type1>Name1/<Type2>Name2`, the first path must be `<Hook>`, the currently supported types and restrictions are:

- `<Hook>`: The subsequent path cannot contain `<Hook>`
- `<MenuBar>`: The following path cannot contain `<Hook>, <MenuBar>`
Translate these text into English language:

- `<Section>`: The following path cannot contain `<Hook>, <MenuBar>, <Section>`
- `<Separator>`: There should be no `<Hook>` or `<MenuBar>` after this path.
- `<SubMenu>`: The following path cannot contain `<Hook>, <MenuBar>`
- `<Command>`: There should be no path after it
- `<Widget>`: There should be no additional path after it.

A simpler form of the path is: `/BarName/SubMenuName1/SubMenuName2/CommandName`. If no type is specified, the first part of the path is `<MenuBar>`, the middle part is `<SubMenu>`, and the last part is `<Command>`.

If `<Hook>` is not specified, automatically prepend `<Hook>Help` at the beginning to indicate adding a menu bar after the Help menu.

###Instantiation Method

The path mode automatically instantiates all nodes based on type and default parameters. We can also control instantiation ourselves, allowing for more fine-grained control over the content of the extension.

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

When you instantiate `MyBar`, you can pass in the hook name, localized name, and localized tooltip parameters (`"MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips")`). The above code is equivalent to the path-based approach `/<Hook>Help/<MenuBar>MyBar/<SubMenu>MySubMenu/<Command>MyAction`.

##Mixed mode

Of course, you can also mix and match the two methods:

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

In this scenario, the plug-in will automatically instantiate the nodes in the middle path, and the user's own instantiated nodes will be used for the final path.

##### More Use Cases

Header File:

```cpp
#include <EditorPlusPath.h>
```

Specify the localization language using the path method, `EP_FNAME_HOOK_AUTO` indicates automatic use of the path name as the `Hook` name:

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

Get nodes and set localized text through paths:

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

Add new nodes in the UE built-in Hook.

```cpp
FEditorPlusPath::RegisterPath("<Hook>EpicGamesHelp/<Separator>ExtendSeparator")
```

Repeatedly stating the same path will be recognized as a single path, so the same path can be continuously expanded.

```cpp
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path1", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path1", "Path1"), LOCTEXT("Path1Tips", "Path1Tips"));
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path2", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path2", "Path2"), LOCTEXT("Path2Tips", "Path2Tips"));
```

Continue to expand the path for a node

```cpp
auto node = FEditorPlusPath::GetNodeByPath("/MenuTest");
FEditorPlusPath::RegisterChildPath(node, "<SubMenu>Sub/<Separator>Sep");
```

Remove a path

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

- `RegisterPath`: Generate Path Menu
- `RegisterPathAction`: Generate a path menu and automatically bind operations to the end `<Command>` node
- `RegisterChildPath`: Generate child paths for the specified node.
- `RegisterChildPathAction`: Automatically generates child paths for the specified node and binds the action
- `UnregisterPath`: Delete the path. `Leaf` can be specified for strict matching when there are multiple end nodes with the same name. During the deletion process, it will backtrack through the intermediate nodes, and any intermediate node without any child nodes will also be deleted.
- `GetNodeByPath`: Obtain node by path


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

Please refer to the source code for more examples and interface explanations [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)，test case [MenuTest.cpp](https://github.com/disenone/UE.EditorPlus/blob/ue5.3/Source/EditorPlusTools/Private/MenuTest/MenuTest.cpp)


###Module management

UE.EditorPlus also provides a modular framework for managing extension menus, supporting automatic loading and unloading of extension menus when plugins are loaded and unloaded.

Let the menu class inherit from `IEditorPlusToolInterface`, and override the `OnStartup` and `OnShutdown` functions. `OnStartup` is responsible for creating the menu, and `OnShutdown` is responsible for calling the `Destroy` function of the node to clean up the menu. When the reference count of a single node becomes 0, automatic cleanup will be triggered.

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

The menu management class inherits `IEditorPlusToolManagerInterface` and overrides the `AddTools` function to add menu items inside `AddTools`.

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

Call the `StartupTools` and `ShutdownTools` functions of the management class respectively when loading and unloading the plugin.

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

Once the above adaptation is completed, the extension's menu will be automatically loaded and unloaded when the plugin is loaded and unloaded.


##Editor Tools

UE.EditorPlus also provides some practical editor tools.

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

ClassBrowser is a UE class viewer, which can be opened via the menu EditorPlusTools -> ClassBrowser

![](assets/img/2024-ue-editorplus/menu.png)

![](assets/img/2024-ue-editorplus/classbrowser.png)

Based on UE reflection, it's convenient to view various types of UE member information, descriptions and prompts, support fuzzy search, and can jump to open parent class information.


--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
