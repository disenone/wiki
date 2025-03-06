---
layout: post
title: UE 설정 지역화 다국어
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: UE에서 로컬라이즈된 다국어를 구현하는 방법 기록
---

<meta property="og:title" content="UE 设置本地化多语言" />

#UE 설정 로컬라이제이션 다국어

> UE 내에서 로컬라이즈된 다국어를 구현하는 방법을 기록하세요.

UE 확장 메뉴를 잘 모르는 경우, 먼저 간단히 [UE 확장 편집기 메뉴](ue-扩展编辑器菜单.md)，[사용 경로 형식으로 확장 메뉴](ue-使用路径形式扩展菜单.md)

이 문서의 코드는 플러그인을 기반으로 합니다: [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##기능 소개

UE comes with tools that allow for localizing multiple languages, for example, we can localize the editor menus:

중국어 메뉴:

![](assets/img/2023-ue-localization/chinese.png)

영어 메뉴:

![](assets/img/2023-ue-localization/english.png)

##코드 선언

메뉴 로컬라이제이션을 실현하기 위해 코드에서 UE가 처리해야 하는 문자열을 명시적으로 선언해야 합니다. UE에서 정의된 `LOCTEXT` 및 `NSLOCTEXT` 매크로를 사용하세요.

- 파일 전역 정의 방식에서, `LOCTEXT_NAMESPACE`라는 매크로를 먼저 정의하고, 여기에는 현재 다국어 텍스트가 있는 네임스페이스의 이름이 들어간다. 그 이후 파일 내에서 텍스트를 정의할 때 `LOCTEXT`를 사용할 수 있으며, 파일 끝에서 `LOCTEXT_NAMESPACE` 매크로를 취소한다:

```cpp
// #define LOCTEXT(InKey, InTextLiteral)

#define LOCTEXT_NAMESPACE "EditorPlusTools"
LOCTEXT("Key", "Content");
#undef LOCTEXT_NAMESPACE

```

`NSLOCTEXT`을 사용하여 지역 정의 방식을 사용하십시오. 텍스트를 정의할 때 이름 공간 매개변수를 포함하십시오.

```cpp
// #define NSLOCTEXT(InNamespace, InKey, InTextLiteral)

NSLOCTEXT("EditorPlusTools", "Key", "Content");
```

UE 툴은 'LOCTEXT' 및 'NSLOCTEXT' 매크로의 등장을 통해 번역해야 할 모든 텍스트를 수집합니다.

##텍스트를 한국어로 번역하세요.

주어진 텍스트를 다음과 같이 코드로 정의해 보겠습니다:

```cpp
#define LOCTEXT_NAMESPACE "EditorPlusTools"
// register path node loctext
FEditorPlusPath::GetNodeByPath("/MenuTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/<Hook>Help/<MenuBar>MenuTest/<SubMenu>SubMenu1/<Section>Section1")->SetFriendlyName(LOCTEXT("Section1", "Section1"))->SetFriendlyTips(LOCTEXT("Section1Tips", "Section1Tips"));
#undef LOCTEXT_NAMESPACE
```

먼저 번역 도구를 열고 편집기 설정을 엽니다. "편집 - 편집기 기본 설정"을 선택하여 "일반 - 실험 기능 - 도구 - 번역 선택기"를 체크합니다.

![](assets/img/2023-ue-localization/editor_enable_tool.png)


번역 도구를 여세요 `도구 - 로컬라이제이션 콘트롤판`:

![](assets/img/2023-ue-localization/editor_open_tool.png)

기존 Game 하위에 새로운 대상을 생성하거나 (기본 Game에서도 가능합니다. 새로 생성하는 것은 번역 텍스트를 쉽게 관리하고 이동하기 위함입니다)

![](assets/img/2023-ue-localization/tool_new_target.png)

목표 매개변수를 구성하고, 여기 이름을 `EditorPlusTools`로 변경하고 로드 정책은 `편집기`로 설정하며 텍스트 수집 및 플러그인 디렉토리를 추가하고, 대상 종속성은 `Engine, 편집기`로 유지하고 다른 구성은 변경하지 않습니다:

![](assets/img/2023-ue-localization/tool_target_config.png)

한국어로 번역하면:

언어 옵션을 추가하여 중국어(간체)와 영어 두 가지 언어가 보장되도록 하고, 언어 이름 위에 마우스를 올리면 각각 `zh-Hans`와 `en`이 표시되도록 확인하고, 영어를 선택합니다(코드에서 텍스트를 영어로 정의했으므로 영어 텍스트를 수집해야 합니다).

![](assets/img/2023-ue-localization/tool_target_lang.png)

클릭하여 텍스트를 수집하십시오:

![](assets/img/2023-ue-localization/tool_target_collect.png)

수집 진행 상자가 표시되고 수집이 성공할 때까지 기다리면 초록색 체크 마크가 표시됩니다.

![](assets/img/2023-ue-localization/tool_target_collected.png)

수집 진행 상자를 닫고 번역 도구로 돌아가면 영어 줄에 수집된 수량이 표시됩니다. 영어 자체는 번역할 필요가 없으며 중국어 줄의 번역 단추를 클릭하십시오:

![](assets/img/2023-ue-localization/tool_go_trans.png)

해당 텍스트를 한국어로 번역해보겠습니다. 

열려면 번역되지 않은 칼럼에 내용이 표시됩니다. 영어 텍스트 오른쪽에 번역된 내용을 입력하고 번역을 완료한 후에는 저장하고 창을 닫으세요.

![](assets/img/2023-ue-localization/tool_trans.png)

글자 수를 클릭하여 통계를 보세요. 작업을 마치면 번역된 양을 중국어 열에서 확인할 수 있습니다:

![](assets/img/2023-ue-localization/tool_count.png)

최종 컴파일 텍스트:

![](assets/img/2023-ue-localization/tool_build.png)

번역된 데이터는 `Content\Localization\EditorPlusTools` 폴더에 저장됩니다. 각 언어별로 한 개의 폴더가 있고, zh-Hans 폴더 내에서 두 개의 파일을 볼 수 있습니다. `.archive` 파일은 수집하고 번역한 텍스트이며, `.locres` 파일은 컴파일된 데이터입니다.

![](assets/img/2023-ue-localization/tool_ret.png)

![](assets/img/2023-ue-localization/tool_ret2.png)

##번역된 텍스트를 플러그인 디렉토리에 넣으세요.

우리는 플러그인에서 생성된 번역 텍스트를 프로젝트 디렉토리에 넣었는데, 이제 이 텍스트들을 플러그인으로 옮겨야 해. 플러그인과 함께 쉽게 배포할 수 있도록.

`Content\Localization\EditorPlusTools` 디렉토리를 플러그인 디렉토리 아래의 Content로 이동하십시오. 제 경우에는 `Plugins\UE.EditorPlus\Content\Localization\EditorPlusTools`입니다.

프로젝트의 설정 파일 `DefaultEditor.ini`을 수정하여 새 경로를 추가하십시오.

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```

이렇게 하면 다른 프로젝트가 플러그인을 받은 후, `DefaultEditor.ini`를 수정하기만 하면 번역 텍스트를 바로 사용할 수 있어서 번역을 다시 구성할 필요가 없습니다.

##주의사항

번역 데이터를 생성하는 과정에서 몇 가지 문제가 발생했는데, 다음은 주의해야 할 사항들을 요약한 것이다:

코드 안에서 텍스트를 정의할 때는 매크로 'LOCTEXT'와 'NSLOCTEXT'을 사용해야 합니다. 텍스트는 문자열 상수이어야 하며, 이렇게 해야 UE에서 수집할 수 있습니다.
번역 대상 이름에 `.`와 같은 기호가 있으면 안 되고, `Content\Localization\` 하위 디렉토리의 이름에 `.`이 있으면 안 됩니다. UE는 `.` 이전의 이름만 가져갑니다. 번역 텍스트를 읽는 중에 UE가 이름을 잘못 인식하여 읽기 실패할 수 있습니다.
- 에디터 플러그인의 경우, 명령행 모드인 경우 `IsRunningCommandlet()`을 확인하여 SlateUI 및 메뉴를 생성하지 않아야 합니다. 왜냐하면 명령행 모드에서는 Slate 모듈이 없기 때문에 텍스트 수집 시 'Assertion failed: CurrentApplication.IsValid()' 에러가 발생할 수 있습니다. 이와 같은 오류를 겪고 있다면 이 확인을 추가해 보세요. 구체적인 오류 메시지:

    > Assertion failed: CurrentApplication.IsValid() [File:E:\UE\ue5.3_git\Engine\Source\Runtime\Slate\Public\Framework\Application\SlateApplication.h] [Line: 255] 

    ![](assets/img/2023-ue-localization/tool_error.png)

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT로 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)모든 빠진 부분을 찾으십시오. 
