---
layout: post
title: Azure
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
description: Azure
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Azure" />

#블루프린트 - 아즈어

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_all.png)

Azure의 사용법은 OpenAI와 매우 유사하기 때문에 여기서 간략히 소개하겠습니다.

##텍스트 채팅

"Azure Chat Options" 노드를 생성하고, "Deployment Name", "Base Url", "Api Key" 매개변수를 설정하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_chat_1.png)

"Messages" 관련 노드를 생성하고 "Azure Chat Request"를 연결합니다. 실행을 클릭하면 화면에 Azure가 반환한 채팅 정보가 출력됩니다.如图

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

##이 텍스트를 한국어로 번역하십시오:

이미지 만들기

"Azure Image Options" 노드를 생성하고 "Deployment Name", "Base Url", "Api Key" 매개변수를 설정합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_image_1.png)

"Azure Image Request" 노드를 설정하고 실행을 클릭하면 화면에 Azure에서 반환한 대화 정보가 출력됩니다. 아래 그림을 참조하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

위에 있는 도면에 따라, 이미지는 D:\Dwnloads\butterfly.png 경로에 저장됩니다.

--8<-- "footer_ko.md"


> 본 게시물은 ChatGPT를 사용하여 번역되었습니다. 피드백은 [**여기**](https://github.com/disenone/wiki_blog/issues/new)모든 빠진 부분을 지적하십시오. 
