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

Unreal Engine이 패키징될 때, 필요한 플러그인 동적 라이브러리 파일이 자동으로 포함되어 패키징되어 플러그인을 활성화하기만 하면 됩니다.

Windows의 경우, 묶을 때 llama.cpp 및 CUDA 관련 dll 파일이 자동으로 묶여진 디렉토리에 들어갑니다. Android/Mac/IOS 같은 다른 플랫폼도 마찬가지입니다.

개발된 게임의 패키지된 버전에서 "AIChatPlus.PrintCllamaInfo" 명령을 실행하여 현재 Cllama 환경 상태를 확인하고, 상태가 정상인지 및 GPU 백엔드를 지원하는지 확인할 수 있습니다.

##모델 패키징

만약 프로젝트 모델 파일을 'Content/LLAMA' 디렉토리에 넣는다고 가정하면, 패키징할 때 이 디렉토리를 포함시킬 수 있습니다:

"프로젝트 설정"을 열고 Packaging 탭을 선택하거나 "asset package"를 직접 검색하여 "추가 패키지할 비 에셋 디렉터리" 설정을 찾아 Content/LLAMA 디렉터리를 추가하면 됩니다:

![](assets/img/2024-ue-aichatplus/usage/package/getstarted_1.png)

목차를 추가한 후에, 언리얼이 빌드할 때 자동으로 해당 폴더의 모든 파일을 포장합니다.

##패키지된 오프라인 모델 파일을 읽기

일반적으로 프로젝트 파일은 .Pak 파일에 패키징됩니다. 이 때, .Pak 파일 내의 파일 경로를 Cllam 오프라인 모델에 전달하면 실행이 실패합니다. 왜냐하면 llama.cpp는 .Pak에 패키징된 모델 파일을 직접 읽을 수 없기 때문입니다.

따라서 먼저 .Pak 파일 내의 모델 파일을 파일 시스템으로 복사해야 합니다. 플러그인은 .Pak의 모델 파일을 복사하고 복사된 파일 경로를 반환하는 편리한 함수를 제공하여 Cllama가 쉽게 읽을 수 있도록 합니다.

블루프린트 노드인 "Cllama Prepare ModelFile In Pak"는 Pak 파일에서 모델 파일을 자동으로 파일 시스템으로 복사합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

C++ 코드 함수는:

```
#include <Cllama/AIChatPlusCllama_Util.h>

auto ModelPath = FAIChatPlusCllama_Util::PrepareModelFileInPak(InContentPath);
```

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT로 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 빠진 부분이 있으면 가리키세요. 
