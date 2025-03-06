---
layout: post
title: UE에서 플러그인 소스 코드를 사용하여 플러그인을 추가합니다.
date: 2023-12-01
categories:
- c++
- ue
catalog: true
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: 단순히 어떻게 UE에 플러그인을 추가하는지 소스 코드가 있는 상황에서 기록해 봅니다.
figures: []
---

<meta property="og:title" content="UE 通过插件源码添加插件" />

#UE 플러그인 소스 코드를 통해 플러그인을 추가합니다.

#플러그인 추가

> 플러그인 소스 코드를 보유한 상황에서 플러그인을 추가하는 방법을 간단히 기록합니다.

플러그인인 [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)예를 들어

Placing the source code under the Plugins directory.
- 이 단계를 건너뛰어도 괜찮습니다. .uproject 파일을 수정하여 Plugins 필드에 다음을 추가하십시오:
    ```json
        "Plugins": [
        {
            "Name": "EditorPlus",
            "Enabled": true,
            "TargetAllowList": [
                "Editor"
            ]
        }
    ```
- uproject 파일을 마우스 오른쪽 버튼으로 클릭하여 "Generate Visual Studio Project Files"를 실행하여 sln 프로젝트 파일을 업데이트하십시오.
sln 파일을 열고 프로젝트를 컴파일하세요.

#여러 언어 설정

프로젝트의 설정 파일 'DefaultEditor.ini'을 수정하여 새 경로를 추가하십시오:

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```


--8<-- "footer_ko.md"


> 이 포스트는 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)모든 빠뜨린 부분을 지적하십시오. 
