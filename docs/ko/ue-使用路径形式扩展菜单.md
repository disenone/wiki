---
layout: post
title: UE 사용 경로 형식으로 메뉴 확장
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
---

<meta property="og:title" content="UE 使用路径形式扩展菜单" />

> UE에서 경로 형식으로 확장 메뉴를 구현하는 방법을 기록하세요.

UE 확장 메뉴얼을 잘 모르시면 먼저 간단히 확인해보세요: [UE 확장 편집기 메뉴](ue-扩展编辑器菜单.md)

본 코드는 플러그인 [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##노드 관리

메뉴를 나무 구조로 관리합니다. 부모 노드는 자식을 포함할 수 있습니다.

```cpp
class EDITORPLUS_API FEditorPlusMenuBase: public TSharedFromThis<FEditorPlusMenuBase>
{
protected:
	// sub menus
	TArray<TSharedRef<FEditorPlusMenuBase>> Children;
}
```

부모 노드를 만들 때 동시에 자식 노드를 만듭니다:

```cpp
void FEditorPlusMenuBase::Register(FMenuBuilder& MenuBuilder)
{
	for (const auto Menu: Children)
	{
		Menu->Register(MenuBuilder);
	}
}
```

당연히 각 노드의 구체적인 생성 동작은 약간 다를 것이며, 가상 함수를 재정의하여 구현합니다:

```cpp
// Menubar
void FEditorPlusMenuBar::Register(FMenuBarBuilder& MenuBarBuilder)
{
	MenuBarBuilder.AddPullDownMenu(
		GetFriendlyName(),
		GetFriendlyTips(),
        // Delegate to call Register
		FEditorPlusMenuManager::GetDelegate<FNewMenuDelegate>(GetUniqueId()),       
		Hook);
}

// Section
void FEditorPlusSection::Register(FMenuBuilder& MenuBuilder)
{
	MenuBuilder.BeginSection(Hook, GetFriendlyName());
	FEditorPlusMenuBase::Register(MenuBuilder);
	MenuBuilder.EndSection();
}

// Separator
void FEditorPlusSeparator::Register(FMenuBuilder& MenuBuilder)
{
	MenuBuilder.AddMenuSeparator(Hook);
	FEditorPlusMenuBase::Register(MenuBuilder);
}

// SubMenu
void FEditorPlusSubMenu::Register(FMenuBuilder& MenuBuilder)
{
	MenuBuilder.AddSubMenu(
		GetFriendlyName(),
		GetFriendlyTips(),
		FNewMenuDelegate::CreateSP(this, &FEditorPlusSubMenu::MakeSubMenu),
		false,
		FSlateIcon(),
		true,
		Hook
	);
}

// Command
void FEditorPlusCommand::Register(FMenuBuilder& MenuBuilder)
{
    MenuBuilder.AddMenuEntry(
        CommandInfo->Label, CommandInfo->Tips, CommandInfo->Icon,
        CommandInfo->ExecuteAction, CommandInfo->Hook, CommandInfo->Type);
}

// ......
```

##경로를 통해 노드를 생성합니다.

트리 구조로 메뉴를 구성하여 경로 형식을 통해 메뉴의 트리 구조를 정의할 수 있습니다.

```cpp
"/<Hook>Help/<MenuBar>BarTest/<SubMenu>SubTest/<Command>Action"
```

위 경로는 메뉴를 생성하는 일련의 단계를 정의할 수 있습니다:

- `<Hook>Help`：Help 메뉴 뒤에 위치한 Hook 이름입니다.
- `<MenuBar>BarTest`: MenuBar 유형의 메뉴를 만들어서 이름을 BarTest로 지정합니다.
- `<SubMenu>SubTest`: 하위 항목 생성, 종류는 SubMenu, 이름은 SubTest
- `<Command>Action` : 맨 마지막에 명령을 생성합니다.

인터페이스 호출 형식은 매우 간결할 수 있습니다:

```cpp
const FString Path = "/<Hook>Help/<MenuBar>BarTest/<SubMenu>SubTest/<Command>Action";
FEditorPlusPath::RegisterPathAction(
	Path, 
    FExecuteAction::CreateLambda([]
    {
        // do action
    })
);
```

##사용자 정의 양식으로 노드 생성

우리는 여전히 무겁고 복잡한 방식으로 메뉴를 만들고 있습니다. 이 무겁고 복잡한 방식은 더 자세한 설정을 허용할 수 있으며, 코드의 구성은 UE의 SlateUI 작성 방식과 비슷합니다.

```cpp
EP_NEW_MENU(FEditorPlusMenuBar)("BarTest")
->RegisterPath()
->Content({
    EP_NEW_MENU(FEditorPlusSubMenu)("SubTest")
    ->Content({
        EP_NEW_MENU(FEditorPlusCommand)("Action")
        ->BindAction(FExecuteAction::CreateLambda([]
            {
                // do action
            })),
    })
});
```

##혼합 형태

물론, 본래의 경로 방식과 사용자 정의로 생성된 메뉴는 동일하며 두 가지를 혼용할 수 있어 매우 유연합니다:

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>BarTest/<SubMenu>SubMenu/<Command>Action1", 
    EP_NEW_MENU(FEditorPlusCommand)("Action1")
    ->BindAction(FExecuteAction::CreateLambda([]
        {
            // do action
        })),
);

FEditorPlusPath::RegisterPath(
    "/<MenuBar>BarTest/<SubMenu>SubMenu/<Command>Action2", 
    EP_NEW_MENU(FEditorPlusCommand)("Action2")
    ->BindAction(FExecuteAction::CreateLambda([]
        {
            // do action
        })),
);
```

여러 곳에서 정의된 메뉴는 하나의 트리 구조로 병합되며, 동일한 이름을 가진 노드는 동일한 노드로 간주됩니다. 다시 말해, 경로는 유일하며 같은 경로는 메뉴 노드를 유일하게 식별할 수 있습니다.
따라서 우리는 노드를 찾아내서 다시 몇 가지 설정과 수정을 할 수 있습니다:

```cpp
// set Name and Tips
FEditorPlusPath::GetNodeByPath("/<MenuBar>BarTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떠한 빠진 부분도 지적하십시오. 
