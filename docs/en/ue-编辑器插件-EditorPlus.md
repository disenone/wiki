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
- Editor
- Editor Plus
- Editor Plugin
description: UE Editor Plugin UE.EditorPlus Documentation
---

<meta property="og:title" content="UE 编辑器插件 EditorPlus 说明文档" />

#UE EditorPlus Plugin Documentation

##Introduction video

![type:video](assets/img/2024-ue-editorplus/market/video.mp4)

##Plug-in source code

[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Download from the mall

[EditorPlus](https://www.unrealengine.com/marketplace/zh-CN/product/editorplus)

##Add the source code plugin EU.EditorPlus to the project.

Reference documents:

Chinese: [Add plugins with UE by plugin source code](https://wiki.disenone.site/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)
- English: [UE adds plugins through the plugin source code](https://wiki.disenone.site/en/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)


##Plugin Description

UE.EditorPlus is a UE editor plugin that provides a convenient way to extend the editor menu and supports advanced methods of extension, while also including some practical editor tools. This plugin supports UE5.3+.


##Expand editor menu

![](assets/img/2024-ue-editorplus/menu.png)

![](assets/img/2024-ue-editorplus/toolbar.png)

###Explanation

Support multiple ways to expand the editor menu:

Path method: `RegisterPathAction("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action")`
Instantiation method: `EP_NEW_MENU(FEditorPlusMenuBar)("Bar")`
- Mixed mode: `RegisterPath("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action", EP_NEW_MENU(FEditorPlusCommand)("Action")`

###Way of the path

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

This way, you can add a menu Bar behind the Help menu in the editor menu bar, with a submenu SubMenu inside Bar, and an Action command inside SubMenu.

The complete path format would be like this: `/<Hook>HookName/<Type1>Name1/<Type2>Name2`, the first path must be `<Hook>`, currently supported types and restrictions:

- `<Hook>`: indicates where to generate the menu, the subsequent path cannot contain `<Hook>`
Translate these text into English language:

- `<MenuBar>`: Menu Bar, the following paths cannot contain `<Hook>, <MenuBar>, <ToolBar>`
- `<ToolBar>`: Toolbar, the following path cannot contain `<Hook>, <MenuBar>, <ToolBar>`
- `<Section>`: Menu section, the following path cannot contain `<Hook>, <MenuBar>, <Section>`
- `<Separator>`: Menu separator, path cannot contain `<Hook>, <MenuBar>` afterwards
Translate these text into English language:

- `<SubMenu>`: Submenu, the following path cannot contain `<Hook>, <MenuBar>`
- `<Command>`: Menu command, no path should follow it
- `<Widget>`: More customizable Slate UI components for extendibility, with no paths following it.

A simpler path format: `/BarName/SubMenuName1/SubMenuName2/CommandName`, if the type is not specified, the first element of the path is `<MenuBar>`, the middle elements are `<SubMenu>`, and the last element is `<Command>`.

If `<Hook>` is not specified, automatically add `<Hook>Help` to the very beginning, indicating that the menu will be added after the Help menu.

###Way of instantiation

The route mode automatically instantiates all nodes based on type and default parameters, and we can also control instantiation ourselves to have a more detailed control over the content of the extension.

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

When instantiating `MyBar`, you can pass in the Hook name, localized name, and localized tooltip parameters (`"MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips")`). The above code is equivalent to the path way `/ <Hook>Help/ <MenuBar>MyBar/ <SubMenu>MySubMenu/ <Command>MyAction`.

###Mixed mode

Of course, you can also mix the two methods:

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

In this case, the plugin will automatically instantiate the nodes along the middle path, with the final node being instantiated by the user themselves.

###More use cases

Header file:

```cpp
#include <EditorPlusPath.h>
```

Specify the localization language by path, `EP_FNAME_HOOK_AUTO` means automatically using the path name as the Hook name:

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

Retrieve nodes by path and set localized text:

```cpp
FEditorPlusPath::GetNodeByPath("/MenuTest")
    ->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))
    ->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


Add a Slate UI widget to the end of the path

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Widget>Widget",
    EP_NEW_MENU(FEditorPlusWidget)("Widget", LOCTEXT("Widget", "Widget"))
        ->BindWidget(SNew(SHorizontalBox)));
);
```

Add new nodes in the Hook provided by UE.

```cpp
FEditorPlusPath::RegisterPath("<Hook>EpicGamesHelp/<Separator>ExtendSeparator")
```

Repeated declarations of the same path are recognized as the same path, so the same path can be continuously extended.

```cpp
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path1", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path1", "Path1"), LOCTEXT("Path1Tips", "Path1Tips"));
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path2", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path2", "Path2"), LOCTEXT("Path2Tips", "Path2Tips"));
```

Extend the path for a node

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

- `RegisterPath`: Generate Path Menu.
- `RegisterPathAction`: Generate path menu, and automatically bind operation to the end `<Command>` node
- `RegisterChildPath`: Generate child paths for the specified node.
- `RegisterChildPathAction`: Generate child paths for the specified node and automatically bind actions.
- `UnregisterPath`: Delete path, `Leaf` can specify strict matching when there are multiple end nodes with the same name. During the deletion process, the intermediate nodes will be traced back, and once an intermediate node has no child nodes, it will also be deleted.
- `GetNodeByPath`: Get node by path


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


###Modular management

UE.EditorPlus also provides a modular framework for managing extension menus, supporting automatic loading and unloading of extension menus when plugins are loaded and unloaded.

Let the menu class inherit `IEditorPlusToolInterface` and override the `OnStartup` and `OnShutdown` functions. `OnStartup` is responsible for creating the menu, while `OnShutdown` is responsible for calling the node's `Destroy` function to clean up the menu. When the reference count of a single node is 0, automatic cleanup will be triggered.

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

The **MenuManager** class inherits `IEditorPlusToolManagerInterface` and overrides the `AddTools` function to add menu classes inside it.

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

After completing the above adaptation, the extension menu can be automatically loaded and unloaded when loading and unloading plugins.


##Editor Tools

UE.EditorPlus also provides some practical editor tools.

##Create editor window

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

Based on UE's reflection, you can easily view various types of UE member information, descriptions, prompts, etc., support fuzzy search, and be able to jump to open parent class information.

### MenuCollections

MenuCollections is a tool for quickly searching for and collecting menu commands, which can help you quickly find the menu commands you need to execute, and can also collect frequently used commands to improve efficiency.

![](assets/img/2024-ue-editorplus/menucollection_find.png)

![](assets/img/2024-ue-editorplus/menucollection_star.png)


### SlateResourceBrowser

SlateResourceBrowser is a tool that allows you to quickly view Slate UI resources, helping you browse and find the editor resources you need, making it easy to expand the editor.

![](assets/img/2024-ue-editorplus/slateresourcebrowser_color.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_icon.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_font.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_widgetstyle.png)

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
