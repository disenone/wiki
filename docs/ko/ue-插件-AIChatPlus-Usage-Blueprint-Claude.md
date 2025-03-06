---
layout: post
title: Claude
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
description: Claude
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Claude" />

#청사진 부분 - 클로드

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/claude_all.png)

##텍스트 채팅

옵션 노드를 만들고 "Model", "Api Key", "Anthropic Version" 매개변수를 설정하십시오.

![](assets/img/2024-ue-aichatplus/usage/blueprint/claude_chat_1.png)

"Claude Request" 노드와 "Messages" 관련 노드를 연결하고 실행을 클릭하면 화면에 Claude가 반환한 채팅 정보가 출력됩니다.

![](assets/img/2024-ue-aichatplus/usage/blueprint/claude_chat_2.png)

##이 텍스트를 한국어로 번역하면 "이미지 생성 텍스트"가 됩니다.

Claude also supports the Vision feature.

블루프린트에서 오른쪽 클릭하여 노드 'Send Claude Chat Request'를 만듭니다.

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Options 노드를 생성하고 `Stream=true, Api Key="Clude에서 제공하는 API 키", Max Output Tokens=1024`로 설정하십시오.

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Messages를 만들고, 파일에서 Texture2D를 만들어 AIChatPlusTexture를 만들고, AIChatPlusTexture를 Messages에 추가합니다.

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

이벤트를 생성하고 정보를 게임 화면에 출력합니다.

전문 번역 엔진으로서 텍스트 내용을 자연스럽고 전문적이며 우아하게 번역해 주세요. 기계 번역 스타일을 사용하지 마십시오.글 내용을 번역 할 뿐이며 해석하지 마십시오. 번역할 수없는 모든 문자를 유지하십시오. 아무것도 말하지 마십시오. 아무것도 설명하지 마십시오.


![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)


--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)모든 빠짐없는 것을 지적해 주십시오. 
