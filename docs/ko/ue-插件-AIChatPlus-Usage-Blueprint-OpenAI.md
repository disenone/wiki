---
layout: post
title: OpenAI
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
description: OpenAI
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - OpenAI" />

#청사진 - OpenAI

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_all.png)

[시작하기](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)이 절에서는 OpenAI의 기본 사용법을 이미 소개했으니, 여기서는 더 자세한 사용법을 설명하겠습니다.

##텍스트 채팅

OpenAI를 사용하여 텍스트 채팅을하다.

블루프린트에서 'Send OpenAI Chat Request In World' 노드를 우클릭하여 생성하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Options 노드를 만들고 `Stream=true, Api Key="OpenAI에서 받은 API 키"`로 설정하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Messages를 생성하고 System Message와 User Message를 각각 추가하십시오.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Delegate를 만들어서 모델의 출력 정보를 받고 화면에 출력합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

완벽한 청사진은 이렇습니다. 블루프린트를 실행하면 게임 화면에서 대형 모델이 출력된 메시지를 볼 수 있습니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

##이 텍스트를 한국어로 번역해 주세요: 

本文生成图片

OpenAI를 사용하여 이미지를 작성하십시오.

파란색 도면에서 'Send OpenAI Image Request' 노드를 만들고 마우스 오른쪽 클릭하여 'a beautiful butterfly'로 설정합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Options 노드를 생성하고 `Api Key="OpenAI에서 제공하는 닌 API 키"`로 설정합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

로 이미지에서 이벤트를 바인딩하고 이미지를 로컬 하드 드라이브에 저장합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

전체 도면은 이렇습니다. 도면을 실행하면 이미지가 지정된 위치에 저장됩니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

##이 텍스트를 한국어로 번역해주세요:

이미지를 텍스트로 변환

OpenAI Vision을 사용하여 이미지를 분석합니다.

블루프린트에서 'Send OpenAI Image Request' 노드를 만들려면 마우스 오른쪽 버튼을 클릭하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_1.png)

옵션 노드를 만들고 `Api Key="OpenAI에서 받은 자신의 API 키"`로 설정하고, 모델을 `gpt-4o-mini`으로 설정합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_2.png)

메시지 만들기.
파일 시스템에서 이미지를 읽어 "텍스처 2D로 파일 가져오기" 노드를 먼저 생성하세요.
"Create AIChatPlus Texture From Texture2D" 노드를 통해 이미지를 플러그인에서 사용할 수 있는 객체로 변환합니다.
"Make Array" 노드를 사용하여 이미지를 노드 "AIChatPlus_ChatRequestMessage"의 "Images" 필드에 연결합니다.
"Content" 필드 내용을 "이 이미지를 설명하세요"로 설정하십시오.

그림 참조:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_3.png)

모든 것이 갖춰진 도면은 다음과 같습니다. 도면을 실행하면 결과가 화면에 표시됩니다.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_4.png)

##이 텍스트를 한국어로 번역하십시오:

이미지 수정

OpenAI는 이미지에서의 지역을 편집할 수 있는 기능을 지원합니다.

먼저 두 장의 그림을 준비해주세요.

수정이 필요한 이미지는 src.png입니다.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_1.png)

필요한 수정 영역을 표시한 이미지인 mask.png을 사용합니다. 소스 이미지를 수정하여 수정 영역의 투명도를 0으로 설정하면 됩니다. 즉, 알파 채널 값이 0이 되도록 변경합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_2.png)

상기 두 장의 사진을 각각 읽어 배열로 구성합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_3.png)

"OpenAI Image Options" 노드를 생성하고 ChatType을 Edit로 설정하고 "End Point Url"을 v1/images/edits로 수정합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_4.png)

"OpenAI Image Request"를 만들고, "Prompt"를 "나비 두 마리로 변신하기"로 설정하여, "Options" 노드와 이미지 배열을 연결하고 생성된 이미지를 파일 시스템에 저장합니다.

전체 도면은 다음과 같습니다:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_5.png)

블루프린트를 실행하여 생성된 이미지가 지정된 위치에 저장됩니다.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_6.png)

##이 텍스트를 한국어로 번역하세요:  

이미지 변형

OpenAI는 입력된 이미지를 기반으로 유사한 변형(변형)을 생성하는 것을 지원합니다.

먼저 이미지 src.png을 준비하고 블루프린트에서 그것을 읽어 들입니다.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_1.png)

"OpenAI Image Options" 노드를 만들고 ChatType을 Variation으로 설정하고 "End Point Url"을 v1/images/variations으로 수정하십시오.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_2.png)

"OpenAI Image Request"를 만들어 "Prompt"를 비워둔 채로 "Options" 노드와 이미지를 연결하고 생성된 이미지를 파일 시스템에 저장합니다.

완벽한 청사진은 이렇게 보입니다:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_3.png)

블루프린트를 실행하여 생성된 이미지를 지정된 위치에 저장합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_4.png)

--8<-- "footer_ko.md"


> 이 글은 ChatGPT로 번역되었습니다. 피드백은 [**여기**](https://github.com/disenone/wiki_blog/issues/new)모든 누락된 사항을 지적하십시오. 
