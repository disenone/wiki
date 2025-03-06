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

#UE 플러그인 AIChatPlus 버전 로그

## v1.6.0 - 2025.03.02

###새로운 기능

llama.cpp를 b4604 버전으로 업그레이드합니다.

Cllama는 GPU 백엔드인 cuda와 metal을 지원합니다.

채팅 도구 Cllama은 GPU 사용을 지원합니다.

패키지된 Pak 파일에서 모델 파일을 읽는 기능을 지원합니다.

### Bug Fix

추론 중에 Cllama가 리로드될 때 발생하는 충돌 문제를 수정했습니다.

iOS 빌드 오류 수정

## v1.5.1 - 2025.01.30

###새로운 기능

* Gemini만 오디오 송출 허용

PCMData를 가져오는 방법을 최적화하여 오디오 데이터를 B64로 인코딩할 때 데이터를 먼저 압축 해제합니다.

OnMessageFinished와 OnImagesFinished 두 개의 콜백을 추가해주세요.

* Gemini Method를 최적화하여 bStream을 기반으로 자동으로 Method를 가져옵니다.

일부 블루프린트 함수를 추가하여 Wrapper를 실제 유형으로 변환하고 응답 메시지와 오류를 가져올 수 있게 합니다.

### Bug Fix

요청 완료 호출 문제를 여러 번 실행하여 수정합니다.

## v1.5.0 - 2025.01.29

###새로운 기능

"지미니에게 음성 지원을 제공해주세요."

편집기 도구는 오디오 및 녹음을 전송하는 것을 지원합니다.

### Bug Fix

세션 복사 실패 버그 수정.

## v1.4.1 - 2025.01.04

###문제 해결

채팅 도구가 이미지만 보내고 메시지는 보내지 않는 기능을 지원합니다.

OpenAI 인터페이스로 사진 전송 문제를 해결하지 못했습니다.

OpanAI 및 Azure 채팅 도구 설정에서 누락된 매개변수 Quality, Style, ApiVersion 문제를 수정했습니다.

## v1.4.0 - 2024.12.30

###신 기능

* (실험 기능) Cllama(llama.cpp)는 다중 모드 모델을 지원하여 이미지를 처리할 수 있습니다.

* 모든 청사진 유형 매개변수에는 자세한 안내가 추가되었습니다.

## v1.3.4 - 2024.12.05

###신 기능

OpenAI는 Vision API를 지원합니다.

###문제 해결

OpenAI stream=false 오류 수정.

## v1.3.3 - 2024.11.25

###신기능

UE-5.5을 지원합니다.

###문제 해결

일부 블루프린트가 작동하지 않는 문제를 해결했습니다.

## v1.3.2 - 2024.10.10

###문제 해결

수동으로 중지 요청을 복구할 때 cllama가 충돌하는 문제를 수정하세요.

상점 다운로드 버전 win을 고치고 ggml.dll llama.dll 파일을 찾을 수 없는 문제

GameThread에서 CreateRequest를 확인합니다.

## v1.3.1 - 2024.9.30

###새로운 기능

SystemTemplateViewer를 추가하여 수백 개의 시스템 설정 템플릿을 볼 수 있고 사용할 수 있습니다.

###문제 해결

상점에서 다운로드한 플러그인을 수정하십시오. llama.cpp에서 링크 라이브러리를 찾을 수 없습니다.

LLAMACpp 경로 길이 문제 해결

Windows 패키징 후 llama.dll 링크 오류 수정

iOS/Android 파일 경로 문제 수정

Cllame 설정 이름 오류를 수정합니다.

## v1.3.0 - 2024.9.23

###중요한 새로운 기능

llama.cpp를 통합하여 대형 모델을 로컬 오프라인으로 실행할 수 있도록 지원합니다.

## v1.2.0 - 2024.08.20

###신 기능

OpenAI Image Edit/Image Variation을 지원합니다.

Ollama API를 지원하며, Ollama에서 지원하는 모델 목록을 자동으로 가져오는 기능을 지원합니다.

## v1.1.0 - 2024.08.07

###새로운 기능

지원 블루프린트

## v1.0.0 - 2024.08.05

###신기능

기반 완벽한 기능

오픈에이아이, 아주어, 클로드, 제미니를 지원합니다.

자체 편집기가 잘 갖춰진 채팅 도구

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT로 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 빠진 부분을 지적해 주세요. 
