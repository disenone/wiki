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

## v1.8.0 - 2025.11.03

* 빠져 나온 llama.cpp b6792를 업그레이드하세요.

## v1.7.0 - 2025.07.06

llama.cpp의 b5536를 업그레이드하세요.

UE5.6를 지원합니다.

Android 출시 시 충돌이 발생할 수 있는 `llama.cpp`를 비활성화하십시오.

## v1.6.2 - 2025.03.17

###신기능

Cllama가 KeepContext 매개변수를 추가하여 기본값을 false로 지정했습니다. 채팅이 종료된 후에 Context가 자동으로 삭제됩니다.

Cllama는 KeepAlive 매개변수를 추가하여 모델 반복 로드를 줄일 수 있습니다.

## v1.6.1 - 2025.03.07

### Bug Fix

OpenAI Image Chat blueprint supports input images.

편집 도구 Cllama mmproj 모델이 비어 있는 것을 허용합니다.

## v1.6.0 - 2025.03.02

###새로운 기능

llama.cpp를 b4604 버전으로 업그레이드합니다.

Cllama는 GPU 백엔드 cuda와 metal을 지원합니다.

채팅 도구 Cllama은 GPU를 사용하도록 지원합니다.

Pak 파일에서 모델 파일을 읽어오는 기능 지원

### Bug Fix

추론 중에 Cllama가 다시로드되면 충돌하는 문제를 수정하였습니다.

iOS 빌드 오류를 수정하세요.

## v1.5.1 - 2025.01.30

###신기능

* Gemini만 오디오 발음 허용

PCMData를 얻는 방법을 최적화하여, 오디오 데이터를 B64로 인코딩할 때 압축을 해제합니다.

OnMessageFinished와 OnImagesFinished 두 개의 콜백을 추가해 주세요.

Gemini Method를 최적화하여 bStream을 기반으로 한 Method를 자동으로 가져옵니다.

일부 블루프린트 함수를 추가하여 Wrapper를 실제 유형으로 변환하고 응답 메시지 및 오류를 얻기 쉽게 만듭니다.

### Bug Fix

수리 요청 완료 다중 호출 문제 해결

## v1.5.0 - 2025.01.29

###새로운 기능

저희 문장은 다음과 같이 번역됩니다: "Gemini에 오디오를 제공하는 것을 지원합니다."

편집기 도구는 오디오 및 녹음을 보내는 기능을 지원합니다.

### Bug Fix

Session 복사 실패 버그를 수정하였습니다.

## v1.4.1 - 2025.01.04

###문제 해결

채팅 도구가 사진만 보내고 글을 보내지 않도록 지원합니다.

OpenAI 인터페이스 이미지 전송 문제 해결 실패 문서 병원

OpanAI 및 Azure 채팅 도구 설정에서 Quality, Style, ApiVersion 매개변수가 누락된 문제를 해결함=

## v1.4.0 - 2024.12.30

###신 기능

（실험 기능）Cllama(llama.cpp)은 다중 모드 모델을 지원하여 이미지를 처리할 수 있습니다.

* 모든 설계도 유형 매개변수에 세부 설명이 추가되었습니다.

## v1.3.4 - 2024.12.05

###새로운 기능

OpenAI는 Vision API를 지원합니다.

###문제 해결

OpenAI stream=false 시 발생하는 오류 수정

## v1.3.3 - 2024.11.25

###새로운 기능

* UE-5.5를 지원합니다.

###문제 해결

일부 청사진 작동 안 되는 문제를 수정하세요.

## v1.3.2 - 2024.10.10

###고치기 문제

수동 중지 요청 시 cllama 충돌 수정

* 상점 다운로드 버전 win 패키지로 ggml.dll llama.dll 파일을 찾을 수 없는 문제 해결

* 요청을 생성할 때 GameThread에서 확인합니다.

## v1.3.1 - 2024.9.30

###신 기능

수백 개의 시스템 설정 템플릿을 확인하고 사용할 수 있는 SystemTemplateViewer를 추가했습니다.

###문제 해결

상점에서 다운로드한 플러그인을 수정하십시오. llama.cpp에서 링크 라이브러리를 찾을 수 없습니다.

LLAMACpp 경로가 너무 길어 발생하는 문제 수정

Windows 패키지 빌드 후 llama.dll 링크 오류를 수정하세요.

iOS/Android 파일 경로 문제 수정

Cllame 설정 이름 오류 수정

## v1.3.0 - 2024.9.23

###중대한 새로운 기능

llama.cpp 파일을 통합하여 대형 모델의 로컬 오프라인 실행을 지원합니다.

## v1.2.0 - 2024.08.20

###신기능

OpenAI Image Edit/Image Variation을 지원합니다.

Ollama API를 지원하며 Ollama가 지원하는 모델 목록을 자동으로 얻는 것을 지원합니다.

## v1.1.0 - 2024.08.07

###새로운 기능

지원 도표

## v1.0.0 - 2024.08.05

###신 기능

기본 완전한 기능

OpenAI, Azure, Claude, Gemini를 지원합니다.

사용자 정의 편집기를 갖고 있는 대화 도구.

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었으니 [**피드백**](https://github.com/disenone/wiki_blog/issues/new)모든 빈틈을 지적해 주세요. 
