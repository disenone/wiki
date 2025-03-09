---
layout: post
title: 기능 노드
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
description: 기능 노드
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - 功能节点" />

#블루프린트 섹션 - 기능 노드

플러그인은 일부 편리한 블루프린트 기능 노드를 추가로 제공합니다.

##Cllama 관련

"Cllama Is Valid"를 해석합니다: Cllama llama.cpp 파일이 제대로 초기화되었는지 판단합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu"을(를) 현재 환경에서 GPU 백엔드를 지원하는지 판별합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"현재 llama.cpp에서 지원하는 모든 백엔드를 가져옵니다"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

파일 준비 모델 파일을 Pak에 복사합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

##이 텍스트를 한국어로 번역하십시오:

이미지 관련

"UTexture2D를 Base64로 변환하기": UTexture2D를 png base64 형식으로 변환합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

"Save UTexture2D to .png file"을(를) .png 파일로 저장합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

".png 파일을 UTexture2D로 불러오기"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Duplicate UTexture2D": UTexture2D 복제

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

##오디오 관련

"USoundWave로 .wav 파일을 불러오기"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

".wav 데이터를 USoundWave로 변환하십시오": wav 이진 데이터를 USoundWave로 변환하십시오.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

"USoundWave를 .wav 파일로 저장하세요"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

"Get USoundWave Raw PCM Data": USoundWave를 원시 PCM 데이터로 가져오기

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"Convert USoundWave to Base64": USoundWave를 Base64로 변환하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicate USoundWave": USoundWave를 복제합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

"Convert Audio Capture Data to USoundWave": 오디오 캡처 데이터를 USoundWave로 변환하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT로 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)모든 누락된 부분을 지적하십시오. 
