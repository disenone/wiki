---
layout: post
title: Get Started
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
description: Get Started
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Get Started" />

#도면 섹션 - 시작하기

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

## Get Started

아래에서 OpenAI를 예로 들어 청사진의 기본 사용 방법을 소개합니다.

###텍스트 채팅

OpenAI를 사용하여 텍스트 채팅하기

블루프린트에서 'Send OpenAI Chat Request In World' 노드를 만들려면 마우스 오른쪽 버튼을 클릭하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Options 노드를 생성하고 `Stream=true, Api Key="OpenAI에서 받은 API 키"`로 설정하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

메시지를 생성하고 각각 시스템 메시지와 사용자 메시지를 추가하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Delegate를 생성하여 모델 출력 정보를 수신하고 화면에 출력합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

완전한 청사진은 다음과 같습니다. 청사진을 실행하면 게임 화면에서 대규모 모델을 출력한 메시지가 나타납니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###본문이미지생성

OpenAI를 사용하여 이미지를 만드세요.

블루프린트에서 'Send OpenAI Image Request' 노드를 만들려면 오른쪽 버튼을 클릭하고 `In Prompt="a beautiful butterfly"`로 설정하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

옵션 노드를 생성하고 `Api Key="OpenAI에서 받은 당신의 API 키"`를 설정합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

이미지에 바인딩하고 로컬 하드 드라이브에 이미지를 저장합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

완전한 청사진은 다음과 같습니다. 청사진 실행하면 이미지가 지정된 위치에 저장된 것을 볼 수 있습니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

###이 텍스트를 한국어로 번역해 주세요:

 이미지를 텍스트로 생성합니다

OpenAI Vision을 사용하여 이미지를 분석합니다.

블루프린트에서 'Send OpenAI Image Request' 노드를 마우스 오른쪽 클릭하여 생성하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_1.png)

Options 노드를 생성하고 `Api Key="OpenAI에서 받은 닥 키"`로 설정하고 모델을 `gpt-4o-mini`으로 설정하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_2.png)

메시지 만들기.
"Import File as Texture 2D" 노드를 만들어서 파일 시스템에서 이미지를 읽어옵니다.
* "Create AIChatPlus Texture From Texture2D" 노드를 통해 이미지를 플러그인에서 사용할 수 있는 객체로 변환합니다.
"Make Array" 노드를 사용하여 이미지를 "AIChatPlus_ChatRequestMessage" 노드의 "Images" 필드에 연결하십시오.
"Content" 필드 내용을 "이 이미지를 설명"으로 설정합니다.

그림과 같이:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_3.png)

전체 도면은 이렇습니다. 도면을 실행하면 결과가 화면에 표시됩니다.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_4.png)

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT로 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 누락된 부분을 발견하시면 제안해 주세요. 
