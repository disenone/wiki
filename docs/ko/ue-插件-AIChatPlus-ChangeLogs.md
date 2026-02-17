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

#UE 플러그인 AIChatPlus 버전 변경 로그

## v2.0.0 - 2026.02.14

* **Tool Calling 다중 플랫폼 지원**: OpenAI, Claude, Gemini, Ollama, CllamaServer 총 5개 주요 플랫폼의 도구 호출/함수 호출 기능이 새롭게 추가되었습니다.
* **Cllama 서버 통합**: 로컬 llama.cpp 서버를 완벽하게 지원하며, 생성, 관리, Speech-to-Text 기능을 포함하고 있으며, 편집기 시각적 관리 인터페이스를 제공합니다.
* **JSON 블루프린트 라이브러리**: 새롭게 추가된 JsonObject/JsonArray 블루프린트 작업 클래스로 JSON과 USTRUCT 간 상호 변환을 지원합니다.
* **OpenAI 오디오**: OpenAI 오디오 입출력 지원, 편집기에서 오디오 응답 미리보기 가능

## v1.8.0 - 2025.11.03

* llama.cpp b6792로 업그레이드

## v1.7.0 - 2025.07.06

* llama.cpp b5536으로 업그레이드

* UE5.6 지원

* Android 출시 시 shipping 버전에서 충돌(crash)이 발생하므로, llama.cpp를 비활성화하세요.

## v1.6.2 - 2025.03.17

###새로운 기능

* Cllama에 KeepContext 매개변수 추가, 기본값은 false로 설정되며 채팅 종료 시 Context가 자동으로 파기됩니다

* Cllama에 KeepAlive 매개변수를 추가하여 모델의 반복적 읽기를 줄일 수 있습니다.

## v1.6.1 - 2025.03.07

### Bug Fix

* OpenAI 이미지 채팅 블루프린트는 이미지 입력을 지원합니다

* 에디터 도구 Cllama mmproj 모델은 공백을 허용합니다

## v1.6.0 - 2025.03.02

###새로운 기능

* llama.cpp를 b4604 버전으로 업그레이드했습니다

* Cllama는 GPU 백엔드를 지원합니다: cuda와 metal

* 채팅 도구 Cllama는 GPU 사용을 지원합니다

* 패키지된 Pak 파일 내부의 모델 파일 읽기 지원

### Bug Fix

* Cllama에서 추론 중 reload 시 발생하는 충돌 문제 수정

* iOS 컴파일 오류 수정

## v1.5.1 - 2025.01.30

###새로운 기능

* 오직 Gemini만 오디오 전송이 허용됩니다

* PCMData 획득 방법 최적화, B64 생성 시 오디오 데이터 압축 해제

* 요청 추가 콜백 두 개: OnMessageFinished OnImagesFinished

* Gemini Method 최적화, 자동으로 bStream에 따라 Method 획득

* 몇 가지 블루프린트 함수를 추가하여 Wrapper를 실제 유형으로 쉽게 변환하고 Response Message와 Error를 얻을 수 있도록 합니다

### Bug Fix

* Request Finish의 다중 호출 문제 수정

## v1.5.0 - 2025.01.29

###새로운 기능

* Gemini에 오디오 보내기 지원

* 편집기 도구는 오디오 및 녹음 발송을 지원합니다.

### Bug Fix

* Session 복사 실패 버그 수정

## v1.4.1 - 2025.01.04

###문제 해결

* 채팅 도구는 이미지만 보내고 메시지는 보내지 않는 기능을 지원합니다.

* OpenAI 인터페이스의 이미지 전송 문제 수정 실패 문서

* OpenAI 및 Azure 채팅 도구 설정에서 Quality, Style, ApiVersion 매개변수 누락 문제 수정

## v1.4.0 - 2024.12.30

###신기능

* (실험적 기능) Cllama(llama.cpp)는 멀티모달 모델을 지원하며 이미지를 처리할 수 있습니다.

* 모든 블루프린트 유형 매개변수에 상세한 힌트가 추가되었습니다.

## v1.3.4 - 2024.12.05

###새로운 기능

* OpenAI는 비전 API를 지원합니다

###문제 수정

* OpenAI stream=false일 때의 오류 수정

## v1.3.3 - 2024.11.25

###새로운 기능

* UE-5.5 지원

###문제 수정

* 일부 블루프린트가 작동하지 않는 문제 수정

## v1.3.2 - 2024.10.10

###문제 수정

* 수동으로 요청을 중지할 때 cllama가 충돌하는 문제 수정

* 쇼핑몰 다운로드 버전에서 win 패키징 시 ggml.dll 및 llama.dll 파일을 찾지 못하는 문제 수정

* 요청 생성 시 GameThread에서 확인하기, CreateRequest 게임 스레드 확인

## v1.3.1 - 2024.9.30

###새로운 기능

* SystemTemplateViewer를 추가하여 수백 개의 시스템 설정 템플릿을 확인하고 사용할 수 있습니다

###문제 수정

* 마켓플레이스에서 다운로드한 플러그인에서 발생한 문제 해결: llama.cpp 연결 라이브러리를 찾을 수 없음

* LLAMACpp 경로 길이 문제 수정

* Windows 패키징 후 발생하는 llama.dll 링크 오류 수정

* ios/android 파일 경로 읽기 문제 수정

* Cllame 설정 이름 오류 수정

## v1.3.0 - 2024.9.23

###주요 신기능

* llama.cpp를 통합하여 로컬 오프라인에서 대형 모델 실행을 지원합니다

## v1.2.0 - 2024.08.20

###새로운 기능

* OpenAI 이미지 편집/이미지 변이 지원

* Ollama API를 지원하며, Ollama가 지원하는 모델 목록을 자동으로 가져오는 기능을 포함합니다

## v1.1.0 - 2024.08.07

###새로운 기능

* 블루프린트 지원

## v1.0.0 - 2024.08.05

###새로운 기능

* 기본 완전한 기능

* OpenAI, Azure, Claude, Gemini 지원

* 자체 기능이 완벽한 편집기 채팅 도구

--8<-- "footer_ko.md"


> 이 글은 ChatGPT를 사용하여 번역되었습니다. [**의견 보내기**](https://github.com/disenone/wiki_blog/issues/new)누락된 부분을 지적해 주세요. 
