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

플러그인은 몇 가지 편리한 블루프린트 기능 노드를 추가로 제공합니다.

##Cllama 관련

"Cllama Is Valid"：Cllama llama.cpp 파일이 올바르게 초기화되었는지 확인하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu"：llama.cpp 파일이 현재 환경에서 GPU 백엔드를 지원하는지 판단합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"llama.cpp에서 지원하는 모든 백엔드를 가져오기"


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Pak 안에서 모델 파일들을 파일 시스템에 자동으로 복사하도록 Cllama가 준비하십시오."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###이 텍스트를 한국어로 번역하면 "이미지 관련"입니다.

"UTexture2D를 Base64로 변환하기": UTexture2D 이미지를 png base64 형식으로 변환

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

"Save UTexture2D to .png file"을 한국어로 번역하면 "UTexture2D를 .png 파일로 저장합니다."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

".png 파일을 UTexture2D로 불러오기"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Duplicate UTexture2D": UTexture2D 복제

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###오디오 관련

"Load .wav file to USoundWave"을(를) 한국어로 번역하면 "USoundWave에 .wav 파일을 로드하세요"가 됩니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

".wav 데이터를 USoundWave로 변환하세요": wav 이진 데이터를 USoundWave로 변환하세요

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

"Save USoundWave to .wav file": USoundWave를 .wav 파일로 저장합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

"Get USoundWave Raw PCM Data": USoundWave를 이진 PCM 데이터로 변환합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"USoundWave를 Base64로 변환하세요." : "USoundWave를 Base64로 변환하세요."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicate USoundWave": USoundWave를 복사합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

"Convert Audio Capture Data to USoundWave": 오디오 캡처 데이터를 USoundWave로 변환하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT로 번역되었습니다. "[**피드백**](https://github.com/disenone/wiki_blog/issues/new)모든 생략된 부분을 지적하십시오. 
