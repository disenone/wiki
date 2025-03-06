---
layout: post
title: UE 에디터 플러스 플러그인 UE.EditorPlus 설명 문서
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
description: UE 편집기 플러그인 UE.EditorPlus 설명서
---

<meta property="og:title" content="UE 编辑器插件 EditorPlus 说明文档" />

#UE.EditorPlus 플러그인 설명서

##비디오 소개

![type:video](assets/img/2024-ue-editorplus/market/video.mp4)

##확장 프로그램 소스 코드

[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##상점 다운로드

[EditorPlus](https://www.unrealengine.com/marketplace/zh-CN/product/editorplus)

##EU.EditorPlus 플러그인을 포함하는 프로젝트입니다.

참고 문서:

한국어: [UE 플러그인 소스 코드를 통해 플러그인 추가](https://wiki.disenone.site/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)
- English: [UE adds plugins through the plugin source code](https://wiki.disenone.site/en/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)


##플러그인 설명

UE.EditorPlus는 UE 에디터 플러그인으로, 에디터 메뉴를 확장하는 간편한 방법을 제공하며, 고급 방식으로 확장하고 일부 유용한 에디터 도구를 포함하고 있습니다. 이 플러그인은 UE5.3 이상을 지원합니다.


##확장 편집기 메뉴

![](assets/img/2024-ue-editorplus/menu.png)

![](assets/img/2024-ue-editorplus/toolbar.png)

###설명

편집기 메뉴를 확장하는 다양한 방법을 지원합니다:

- 경로 방식: `RegisterPathAction("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action")`
- 인스턴스화 방법: `EP_NEW_MENU(FEditorPlusMenuBar)("Bar")`
- 혼합 방식: `RegisterPath("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",EP_NEW_MENU(FEditorPlusCommand)("Action")`

###경로 방식

한국어로 번역하면 다음과 같습니다:

편집기 메뉴 명령을 등록하는 방법은 다음과 같습니다:

```cpp
FEditorPlusPath::RegisterPathAction(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",
    FExecuteAction::CreateLambda([]
        {
            // do action
        })
);
```

이렇게 하면 편집기 메뉴 막대의 도움 메뉴 뒤에 메뉴 막대 바를 추가할 수 있습니다. 바 안에 하위 메뉴 서브메뉴를 추가하고, 서브메뉴 안에는 명령 액션을 추가할 수 있습니다.

완전한 경로 형식은 다음과 같을 것이다: `/<Hook>HookName/<Type1>Name1/<Type2>Name2`, 첫 번째 경로는 반드시 `<Hook>`여야 하며, 현재 지원되는 유형과 제한은:

- `<Hook>`: 메뉴를 생성해야 하는 Hook 위치를 나타내며, 후속 경로에 `<Hook>`가 없어야 합니다.
`<MenuBar>`은 메뉴 바입니다. 뒤에 `<Hook>`, `<MenuBar>`, `<ToolBar>` 경로가 포함되어서는 안 됩니다.
- `<ToolBar>`: 툴바, 뒤에 `<Hook>, <MenuBar>, <ToolBar>` 경로는 허용되지 않습니다.
- `<Section>`：메뉴를 구분하며, 뒤에 경로에는 `<Hook>, <MenuBar>, <Section>`이 포함되면 안 됩니다.
- `<Separator>`은 메뉴 구분자입니다. 뒤에 `<Hook>, <MenuBar>` 경로가 없어야 합니다.
- `<SubMenu>`: 서브메뉴, 뒤에는 `<Hook>, <MenuBar>`와 같은 경로가 없어야 합니다.
- `<Command>`: 메뉴 명령어, 뒤에 어떤 경로도 없어야 함
- `<Widget>` : 더 많은 확장 가능한 사용자 지정 Slate UI 구성 요소로, 뒤에는 경로가 없어야 합니다.

더 간단한 경로 형식은 `/BarName/SubMenuName1/SubMenuName2/CommandName`입니다. 종류를 지정하지 않으면 기본 경로는 첫 번째가 `<MenuBar>`, 중간이 `<SubMenu>`, 마지막이 `<Command>`입니다.

만약 `<Hook>`가 지정되지 않았다면 `<Hook>Help`를 자동으로 앞부분에 추가하여 Help 메뉴 뒤에 메뉴바를 추가합니다.

###인스턴스화 방식

경로 방식은 모든 노드를 자동으로 유형 및 기본 매개변수에 따라 인스턴스화하는 것이며, 우리는 인스턴스화를 직접 제어할 수도 있습니다. 확장 내용을 더 세밀하게 제어할 수 있습니다.

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

`MyBar`를 인스턴스화할 때 Hook 이름, 로컬라이즈된 이름, 로컬라이즈된 힌트 매개변수(`"MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips")`)를 전달할 수 있습니다. 위의 코드는 다음과 같은 경로 방식과 같습니다 `/<Hook>Help/<MenuBar>MyBar/<SubMenu>MySubMenu/<Command>MyAction`.

###혼합 방식

당연히 두 가지 방법을 혼합해서 사용할 수도 있습니다:

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

이 상황에서 플러그인은 중간 경로의 노드를 자동으로 인스턴스화하고 최종 경로에는 사용자가 직접 인스턴스화한 노드를 사용합니다.

###더 많은 사용 예시

헤더 파일:

```cpp
#include <EditorPlusPath.h>
```

경로 방식으로 로컬라이즈 언어를 지정하며, `EP_FNAME_HOOK_AUTO`는 훅 이름으로 경로명을 자동으로 사용함을 나타냅니다:

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

노드를 경로를 통해 가져와서 로컬라이즈된 텍스트를 설정하세요.

```cpp
FEditorPlusPath::GetNodeByPath("/MenuTest")
    ->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))
    ->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


경로 끝에 Slate UI 위젯을 추가합니다.

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Widget>Widget",
    EP_NEW_MENU(FEditorPlusWidget)("Widget", LOCTEXT("Widget", "Widget"))
        ->BindWidget(SNew(SHorizontalBox)));
);
```

UE의 기본 Hook에 새 노드 추가하기

```cpp
FEditorPlusPath::RegisterPath("<Hook>EpicGamesHelp/<Separator>ExtendSeparator")
```

동일한 경로를 반복 선언하면 동일한 경로로 인식되어 계속해서 동일한 경로를 확장할 수 있습니다.

```cpp
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path1", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path1", "Path1"), LOCTEXT("Path1Tips", "Path1Tips"));
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path2", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path2", "Path2"), LOCTEXT("Path2Tips", "Path2Tips"));
```

하나의 노드를 계속 확장하는 경로

```cpp
auto node = FEditorPlusPath::GetNodeByPath("/MenuTest");
FEditorPlusPath::RegisterChildPath(node, "<SubMenu>Sub/<Separator>Sep");
```

한 경로를 삭제합니다.

```cpp
FEditorPlusPath::UnregisterPath("/MenuTest/SubMenu1/SubMenu1/Path1");
```

확장 도구 모음
```cpp
FEditorPlusPath::RegisterPath("/<Hook>ProjectSettings/<ToolBar>MenuTestToolBar")
->Content({
    EP_NEW_MENU(FEditorPlusCommand)("ToolBarCommand1")
    ->BindAction(...)
});
```

###인터페이스 설명

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

- `RegisterPath`: 경로 메뉴 생성
`RegisterPathAction`：Create a path menu and automatically bind the action to the terminal `<Command>` node.
`RegisterChildPath`: 지정된 노드에 대한 하위 경로를 계속 생성합니다.
`RegisterChildPathAction`: 특정 노드에 대한 하위 경로를 계속 생성하고 자동으로 작업을 바인딩합니다.
- `UnregisterPath`: 경로 삭제, `Leaf` 에서 여러 개의 동일한 이름을 가진 끝 노드가있는 경우 엄격하게 일치하도록 지정할 수 있습니다. 삭제 과정 중에는 중간 노드를 되돌아가며, 중간 노드에 하위 노드가 없는 경우 중간 노드도 삭제됩니다.
`GetNodeByPath`：경로에 따라 노드를 가져옵니다.


노드 유형

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

더 많은 예제와 인터페이스 설명은 소스 코드 [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)"，测试用例 [MenuTest.cpp](https://github.com/disenone/UE.EditorPlus/blob/ue5.3/Source/EditorPlusTools/Private/MenuTest/MenuTest.cpp)


###모듈화 관리

UE.EditorPlus는 확장 메뉴를 모듈화하여 관리하는 프레임워크를 제공합니다. 플러그인을 로드하거나 언로드할 때 자동으로 확장 메뉴를 로드하거나 언로드할 수 있습니다.

`IEditorPlusToolInterface`를 상속하여 메뉴 클래스를 만들고 `OnStartup` 및 `OnShutdown` 함수를 오버라이드합니다. `OnStartup`은 메뉴를 생성하고, `OnShutdown`은 노드의 `Destroy` 함수를 호출하여 메뉴를 정리합니다. 노드의 참조 수가 0이 되면 자동으로 정리가 실행됩니다.

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

메뉴 관리 클래스는 `IEditorPlusToolManagerInterface`를 상속하고 `AddTools` 함수를 오버라이드하여 `AddTools` 함수 내에서 메뉴 클래스를 추가합니다.

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

플러그인이 로드되거나 언로드될 때 각각 `StartupTools` 및 `ShutdownTools` 함수를 호출하도록 관리 클래스를 사용합니다.

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

위의 적응 작업을 완료하면 플러그인을 로드 및 언로드할 때 자동으로 확장 메뉴를 로드 및 언로드할 수 있습니다.


##편집기 도구

UE.EditorPlus는 몇 가지 유용한 편집 도구도 제공합니다.

##편집기 창 생성

EditorPlus를 사용하면 새로운 편집기 창을 쉽게 만들 수 있습니다.

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

`SClassBrowserTab` 는 사용자 지정 UI 컨트롤입니다.

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

ClassBrowser 는 UE 클래스 브라우저로, EditorPlusTools -> ClassBrowser 메뉴를 통해 열 수 있습니다.

![](assets/img/2024-ue-editorplus/classbrowser_menu.png)

![](assets/img/2024-ue-editorplus/classbrowser.png)

UE의 반사를 기반으로 구현되어서 UE의 다양한 유형의 멤버 정보, 설명 및 안내를 쉽게 확인할 수 있으며, 흐릿한 검색을 지원하고 상위 클래스 정보로 이동하여 열람할 수 있습니다.

### MenuCollections

MenuCollections 는 메뉴 명령을 빠르게 찾고 저장할 수 있는 도구로, 필요한 메뉴 명령을 빠르게 찾아주고 자주 사용하는 명령을 저장하여 효율성을 향상시켜 줍니다.

![](assets/img/2024-ue-editorplus/menucollection_find.png)

![](assets/img/2024-ue-editorplus/menucollection_star.png)


### SlateResourceBrowser

SlateResourceBrowser는 Slate UI 자원을 빠르게 확인할 수 있는 도구로, 필요한 편집기 자원을 찾아 볼 수 있도록 도와주며 편집기를 편리하게 확장하는 데 도움을 줍니다.

![](assets/img/2024-ue-editorplus/slateresourcebrowser_color.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_icon.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_font.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_widgetstyle.png)

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 누락된 부분도 지적하십시오. 
