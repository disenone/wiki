---
layout: post
title: 버전 로그
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
description: 버전 로그
---

<meta property="og:title" content="UE 插件 AIChatPlus 版本日志" />

#UE 플러그인 AIChatPlus의 버전 로그

## v1.6.2 - 2025.03.17

###새로운 기능

Cllama는 KeepContext 매개변수를 추가하여 기본값을 false로 설정했으며, 채팅이 종료된 후에 자동으로 Context를 제거합니다.

Cllama는 KeepAlive 매개변수를 추가하여 모델 중복로드를 줄일 수 있습니다.

## v1.6.1 - 2025.03.07

### Bug Fix

OpenAI Image Chat blueprint supports uploading images.

편집 도구 Cllama mmproj 모델이 비어 있도록 허용합니다.

## v1.6.0 - 2025.03.02

###새로운 기능

llama.cpp를 b4604 버전으로 업그레이드합니다.

Cllama는 GPU 백엔드 cuda와 metal을 지원합니다.

채팅 도구 Cllama은 GPU를 지원합니다.

* Pak에 포장된 모델 파일을 읽는 기능을 지원합니다.

### Bug Fix

추론 중에 Cllama가 다시로드될 때 뻗는 문제 수정

iOS 빌드 오류 수정.

## v1.5.1 - 2025.01.30

###신기능

Gemini만 오디오를 전송할 수 있습니다.

PCMData를 얻는 방법을 최적화하여, 오디오 데이터를 B64로 생성할 때에 해제 압축합니다.

OnMessageFinished와 OnImagesFinished 두 개의 콜백을 추가해 주세요.

Gemini Method을 최적화하여 bStream을 기반으로 Method를 자동으로 획득합니다.

일부 블루프린트 기능을 추가하여 Wrapper를 실제 유형으로 변환하고 응답 메시지와 오류를 가져올 수 있도록 합니다.

### Bug Fix

요청 완료 다중 호출 문제 수정

## v1.5.0 - 2025.01.29

###새로운 기능

젬니니에게 오디오를 전달해줘.

편집기 도구는 오디오 및 녹음을 전송하는 기능을 지원합니다.

### Bug Fix

Session 복사 실패 버그를 수정하세요.

## v1.4.1 - 2025.01.04

###문제 해결

채팅 도구가 이미지만 보내고 텍스트를 보내지 않도록 지원합니다.

OpenAI 인터페이스 이미지 전송 문제 해결 실패 문구를 한국어로 번역해주세요.

오픈AI 및 Azure 채팅 도구 설정에서 누락된 매개변수 Quality, Style, ApiVersion 문제를 수정했습니다.

## v1.4.0 - 2024.12.30

###새로운 기능

* (Experimental feature) Cllama (llama.cpp) supports multi-modal model, able to handle images.

* 모든 도면 유형 매개변수에 자세한 안내가 추가되었습니다.

## v1.3.4 - 2024.12.05

###새로운 기능

OpenAI는 Vision API를 지원합니다.

###문제 해결

OpenAI 스트림=false 일 때의 오류 수정

## v1.3.3 - 2024.11.25

###새로운 기능

UE-5.5을 지원합니다.

###문제 해결

특정 청사진이 작동되지 않는 문제를 수정했습니다.

## v1.3.2 - 2024.10.10

###문제 해결

수동 중지 요청 시 cllama 충돌 수정

다음 텍스트를 한국어로 번역하십시오:

* 상점 다운로드 버전 win 패키징시 ggml.dll llama.dll 파일을 찾을 수 없는 문제 수정

* 创建 요청 시 게임 스레드에서 확인합니다.

## v1.3.1 - 2024.9.30

###신기능

수백 가지 시스템 설정 템플릿을 확인하고 사용할 수 있는 SystemTemplateViewer를 추가했습니다.

###문제 해결

상점에서 다운로드한 플러그인을 수정하실 때, llama.cpp에서 링크 라이브러리를 찾을 수 없습니다.

LLAMACpp 경로가 너무 길어서 발생하는 문제를 해결했습니다.

Windows 패키징 후 llama.dll 링크 오류를 수정합니다.

iOS/Android 파일 경로 문제 수정

Cllame 설정 이름 오류 수정

## v1.3.0 - 2024.9.23

###주요 새로운 기능

llama.cpp를 통합하여 대규모 모델의 로컬 오프라인 실행을 지원합니다.

## v1.2.0 - 2024.08.20

###새로운 기능

OpenAI Image Edit/Image Variation을 지원합니다.

Ollama API를 지원하며, Ollama에서 지원하는 모델 목록을 자동으로 가져올 수 있습니다.

## v1.1.0 - 2024.08.07

###새로운 기능

지원 계획

## v1.0.0 - 2024.08.05

###신기능

기초 완벽한 기능

오픈에이아이, 애저, 클로드, 제미니를 지원합니다.

자체 기능이 완벽한 편집기 채팅 도구

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 빠뜨린 부분도 지적하십시오. 
