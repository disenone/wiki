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

## v1.6.1 - 2025.03.07

### Bug Fix

OpenAI Image Chat blueprint supports input images.

편집 도구 Cllama mmproj 모델을 허용합니다.

## v1.6.0 - 2025.03.02

###신기능

llama.cpp를 b4604 버전으로 업데이트합니다.

Cllama supports GPU backends: cuda and metal.

채팅 도구 Cllama는 GPU 사용을 지원합니다.

Pak 파일에서 모델 파일을 읽는 기능을 지원합니다.

### Bug Fix

추론 중에 Cllama가 다시로드될 때 충돌하는 문제를 수정했습니다.

iOS 빌드 오류 수정

## v1.5.1 - 2025.01.30

###새로운 기능

Gemini 만 오디오 전송이 허용됩니다.

PCMData를 검색하는 방법을 최적화하여, 오디오 데이터를 압축 푸는 과정을 Base64로 변환할 때 실행합니다.

OnMessageFinished와 OnImagesFinished 두 개의 콜백을 추가해주세요.

Gemini Method를 최적화하여 bStream을 기반으로 Method를 자동으로 가져옵니다.

일부 블루프린트 함수를 추가하여 Wrapper를 실제 유형으로 변환하고 응답 메시지 및 오류를 가져오기 쉽게합니다.

### Bug Fix

* 요청 완료 다중 호출 문제 수정

## v1.5.0 - 2025.01.29

###신 기능

젬니니에게 오디오 받기 지원

편집 도구는 오디오 및 녹음을 전송하는 것을 지원합니다.

### Bug Fix

세션 복사 실패 버그 수정

## v1.4.1 - 2025.01.04

###문제 해결

채팅 도구에서는 사진만 보내고 메시지는 보내지 않는 기능을 지원합니다.

OpenAI 인터페이스 이미지 전송 문제 해결 실패 문서를 복구합니다.

OpenAI와 Azure 채팅 도구 설정에서 누락된 Quality, Style, ApiVersion 매개변수 문제를 수정했습니다.

## v1.4.0 - 2024.12.30

###신규 기능

* (실험적 기능) Cllama(llama.cpp)은 다중 모드 모델을 지원하여 이미지를 처리할 수 있습니다.

모든 청사진 유형 매개변수에는 상세 설명이 추가되었습니다.

## v1.3.4 - 2024.12.05

###새로운 기능

OpenAI는 Vision API를 지원합니다.

###문제 해결

OpenAI stream=false 오류 수정

## v1.3.3 - 2024.11.25

###신기능

* UE-5.5을 지원합니다.

###문제 해결

일부 블루프린트가 작동하지 않는 문제를 수정합니다.

## v1.3.2 - 2024.10.10

###문제 해결

수동 중단 요청 시 cllama가 충돌하는 문제 수정

* 상점 다운로드 버전 win 패키지에서 ggml.dll llama.dll 파일을 찾을 수 없는 문제를 해결하세요.

게임 스레드에서 CreateRequest를 확인합니다.

## v1.3.1 - 2024.9.30

###새로운 기능

SystemTemplateViewer 를 추가하여 수백 가지 시스템 설정 템플릿을 확인하고 사용할 수 있습니다.

###문제 해결

상점에서 다운로드한 플러그인을 수정합니다. llama.cpp에서 링크 라이브러리를 찾을 수 없습니다.

LLAMACpp 경로가 너무 길어지는 문제를 수정하였습니다.

windows로 패키징한 후에 발생한 llama.dll 링크 오류를 수정합니다.

iOS/Android 파일 경로 문제 수정

Cllame 설정 이름 오류 수정

## v1.3.0 - 2024.9.23

###주요 새로운 기능

llama.cpp가 통합되어 대규모 모델을 로컬에서 오프라인 실행할 수 있습니다.

## v1.2.0 - 2024.08.20

###새로운 기능

OpenAI Image Edit/Image Variation를 지원합니다.

Ollama API를 지원하며, Ollama가 지원하는 모델 목록을 자동으로 가져올 수 있습니다.

## v1.1.0 - 2024.08.07

###신기능

블루프린트를 지원합니다.

## v1.0.0 - 2024.08.05

###새로운 기능

기본 완전 기능

OpenAI, Azure, Claude, Gemini를 지원합니다.

자체 향상된 편집기와 채팅 도구 기능을 갖춘 툴입니다.

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT로 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 누락 사항이나 조사해주세요. 
