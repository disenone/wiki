---
layout: post
title: UE 编辑器插件 EditorPlus 说明文档
tags: [dev, game, UE, UnreanEngine, UE4, UE5]
description: UE 编辑器插件 EditorPlus 说明文档
---
<meta property="og:title" content="UE 编辑器插件 EditorPlus 说明文档" />

# UE 编辑器插件 EditorPlus 说明文档

## 插件源码

[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

## 项目添加源码插件 EditorPlus

参考文档：

- 中文：[UE 通过插件源码添加插件](https://disenone.github.io/wiki/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)
- English: [UE adds plugins through the plugin source code](https://disenone.github.io/wiki/en/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)


## 插件说明

EditorPlus 是一个 UE 编辑器插件，提供了一种方便的方式来扩展编辑器菜单，并支持高级方式来扩展，同时包含了一些实用的编辑器工具。本插件支持 UE5.2+。


## 扩展编辑器菜单

### 说明

支持多种方式扩展编辑器菜单：

- 路径方式：`RegisterPathAction("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action")`
- 实例化方式：`EP_NEW_MENU(FEditorPlusMenuBar)("Bar")`
- 混合方式：`RegisterPath("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",EP_NEW_MENU(FEditorPlusCommand)("Action")`

## 路径方式

可以通过这样的方式来注册一个编辑器菜单指令：

```cpp
FEditorPlusPath::RegisterPathAction(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",
    FExecuteAction::CreateLambda([]
        {
            // do action
        })
);
```

这样就可以在编辑器菜单栏 Help 后面增加一个菜单栏 Bar，Bar 里面增加一个子菜单 SubMenu， SubMenu 里面增加一个命令 Action。

完整的路径格式会是这样的：`/<Hook>HookName/<Type1>Name1/<Type2>Name2`，第一个路径必须是 `<Hook>`，目前支持的类型和限制：

- `<Hook>`：后续路径不能有 `<Hook>`
- `<MenuBar>`：后面路径不能有 `<Hook>, <MenuBar>`
- `<Section>`：后面路径不能有 `<Hook>, <MenuBar>, <Section>`
- `<Separator>`：后面路径不能有 `<Hook>, <MenuBar>`
- `<SubMenu>`：后面路径不能有 `<Hook>, <MenuBar>`
- `<Command>`：后面不能有任何路径
- `<Widget>`：后面不能有任何路径

更简易的路径形式：`/BarName/SubMenuName1/SubMenuName2/CommandName`，如果不指定类型，默认路径的第一个是 `<MenuBar>`，中间的是 `<SubMenu>`，最后的是 `<Command>`。

如果没有指定 `<Hook>` 则自动最前面加上 `<Hook>Help`，表示在 Help 菜单后面添加菜单栏。

## 实例化方式

路径方式是自动把所有节点根据类型和默认参数实例化出来，我们也可以自己控制实例化，可以更细致控制扩展的内容。

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
``

实例化 `MyBar` 的时候可以传入 Hook 名字，本地化名字，本地化提示参数（`"MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips")`）。上面代码就相当于路径方式 `/<Hook>Help/<MenuBar>MyBar/<SubMenu>MySubMenu/<Command>MyAction`。

## 混合方式

当然还可以两种方式混合使用：

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

这种情况下，插件会自动实例化中间路径的节点，最后的路径使用用户自己实例化的节点。

## 更多用例

头文件:

```cpp
#include <EditorPlusPath.h>
```

路径方式指定本地化语言，`EP_FNAME_HOOK_AUTO` 表示自动使用路径名字作为 `Hook` 名字：

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

通过路径获取节点并设置本地化文本：

```cpp
FEditorPlusPath::GetNodeByPath("/MenuTest")
    ->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))
    ->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


路径末端添加一个 Slate UI 控件

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Widget>Widget",
    EP_NEW_MENU(FEditorPlusWidget)("Widget", LOCTEXT("Widget", "Widget"))
        ->BindWidget(SNew(SHorizontalBox)));
);
```

在 UE 自带的 Hook 里面添加新的节点

```cpp
FEditorPlusPath::RegisterPath("<Hook>EpicGamesHelp/<Separator>ExtendSeparator")
```

多次声明相同的路径，都被识别成同一个路径，因此可以不断扩展相同的路径

```cpp
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path1", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path1", "Path1"), LOCTEXT("Path1Tips", "Path1Tips"));
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path2", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path2", "Path2"), LOCTEXT("Path2Tips", "Path2Tips"));
```

为一个节点继续扩展路径

```cpp
auto node = FEditorPlusPath::GetNodeByPath("/MenuTest");
FEditorPlusPath::RegisterChildPath(node, "<SubMenu>Sub/<Separator>Sep");
```

删除一个路径

```cpp
FEditorPlusPath::UnregisterPath("/MenuTest/SubMenu1/SubMenu1/Path1");
```

## 接口说明

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

- `RegisterPath`：生成路径菜单
- `RegisterPathAction`：生成路径菜单，并自动为末端 `<Command>` 节点绑定操作
- `RegisterChildPath`：为指定节点继续生成子路径
- `RegisterChildPathAction`：为指定节点继续生成子路径，并自动绑定操作
- `UnregisterPath`：删除路径，`Leaf` 在有多个同名的末端节点可以指定严格匹配。删除的过程中，会回溯中间节点，一旦中间节点没有任何子节点也会被删除
- `GetNodeByPath`：根据路径获取节点


节点类型

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

更多样例和接口说明请参考源码 [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)，测试用例 [MenuTest.cpp](https://github.com/disenone/UE.EditorPlus/blob/ue5.3/Source/EditorPlusTools/Private/MenuTest/MenuTest.cpp)


## 模块化管理

UE.EditorPlus 还提供了一个模块化管理扩展菜单的框架，支持插件加载和卸载的时候，自动加载和卸载扩展的菜单

让菜单类继承 `IEditorPlusToolInterface`，并覆写 `OnStartup` 和 `OnShutdown` 函数。`OnStartup` 负责创建菜单，`OnShutdown` 负责调用节点的 `Destroy` 函数清理菜单。单节点的引用数归0，则会执行自动清理。

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

菜单管理类继承 `IEditorPlusToolManagerInterface`，并覆写 `AddTools` 函数，在 `AddTools` 里面添加菜单类

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

插件加载和卸载的时候分别调用管理类的 `StartupTools` 和 `ShutdownTools` 函数

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

完成以上适配，则可以自动在加载和卸载插件的时候，自动加载和卸载扩展的菜单。

--8<-- "footer.md"
