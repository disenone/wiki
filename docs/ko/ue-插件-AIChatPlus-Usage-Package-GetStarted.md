---
layout: post
title: 포장
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
- AI Chat
- Chatbot
- Image Generation
- OpenAI
- Azure
- Claude
- Gemini
- Ollama
description: 포장
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - Package 篇 - Get Started" />

#포장

##플러그인 패키징

Unreal Engine을 패키징할 때, 필요한 플러그인 동적 라이브러리 파일이 자동으로 패키징되어 플러그인을 활성화하기만 하면 됩니다.

Windows를 예로들면, 패키지가 llama.cpp, CUDA 관련 dll 파일을 자동으로 패키지 후 디렉터리에 넣습니다. Android/Mac/IOS와 같은 다른 플랫폼에 대해서도 마찬가지입니다.

Development 버전으로 묶인 게임 내에서 "AIChatPlus.PrintCllamaInfo" 명령을 실행하여 현재 Cllama 환경 상태를 확인하고 상태가 정상인지, GPU 백엔드를 지원하는지 확인할 수 있습니다.

##모델 포장

프로젝트에 추가된 모델 파일은 Content/LLAMA 디렉토리에 저장되어 있습니다. 따라서 패키징할 때 이 디렉토리를 포함시킬 수 있습니다.

"Project Setting"을 열고 Packaging 탭을 선택하거나 "asset package"를 직접 검색하여 "Additional Non-Asset Directories to Package" 설정을 찾아서 Content/LLAMA 디렉토리를 추가하면 됩니다.

![](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_6.png)

폴더를 추가한 후에 Unreal이 빌드할 때 자동으로 폴더 내 모든 파일을 함께 묶어서 빌드합니다.


##패키지된 오프라인 모델 파일을 읽기

일반적으로 프로젝트 파일은 .Pak 파일에 포장되는데, 이때 .Pak 내의 파일 경로를 Cllam 오프라인 모델에 전달하면 실패할 것입니다. 이는 llama.cpp가 .Pak에 포장된 모델 파일을 직접 읽을 수 없기 때문입니다.

따라서 .Pak 파일 안의 모델 파일을 파일 시스템으로 먼저 복사해야 합니다. 플러그인은 .Pak 파일 안의 모델 파일을 직접 복사하고 복사한 파일 경로를 반환해주는 편리한 함수를 제공합니다. 이렇게 하면 Cllama가 쉽게 읽을 수 있습니다.

블루프린트 노드는 "Cllama Prepare ModelFile In Pak"입니다: Pak 내의 모델 파일을 자동으로 파일 시스템으로 복사합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

C++ 코드 함수는:

```
#include <Cllama/AIChatPlusCllama_Util.h>

auto ModelPath = FAIChatPlusCllama_Util::PrepareModelFileInPak(InContentPath);
```

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 빠진 부분도 지적하십시오. 
