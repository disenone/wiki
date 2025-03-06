---
layout: post
title: Gemini
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
description: Gemini
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Gemini" />

#청사진 - 쌍둥이자리

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_all.png)

###텍스트 채팅

"젬니 챗 옵션" 노드를 생성하고, "모델", "API 키" 매개변수를 설정하세요.

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_chat_1.png)

"젬니미 채팅 요청" 노드를 만들어서 "옵션"과 "메시지" 노드에 연결한 후 실행을 클릭하면 화면에 젬니미가 반환한 채팅 정보가 출력됩니다. 아래 그림 참조:

![](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###이 텍스트를 한국어로 번역해주세요:

이미지 생성 텍스트

"젬니니 채팅 옵션" 노드를 만들어서 "모델", "API 키" 매개변수를 설정하십시오.

파일에서 이미지 flower.png을 읽어와 "Messages"에 설정합니다.

![flower.png](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_vision_1.png)

"젬니미 챗 요청" 노드를 생성하고 실행을 클릭하면 화면에 출력된 젬니미가 반환한 채팅 정보를 볼 수 있습니다. 아래 그림 참조:

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_vision_2.png)

###오디오를 텍스트로 변환합니다.

젬니는 오디오를 텍스트로 변환하는 기능을 지원합니다.

아래 블루프린트를 만들고 오디오를 로드하고 Gemini 옵션을 설정한 후 실행을 클릭하면 화면에 Gemini가 오디오를 처리한 후 반환하는 채팅 정보가 인쇄됩니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)어떠한 빠뜨림도 지적해주세요. 
