---
layout: post
title: DeepSeek
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
description: DeepSeek
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - DeepSeek" />

#Blueprint Chapter - DeepSeek

DeepSeek는 OpenAI의 API 인터페이스 형식을 호환하기 때문에 DeepSeek에 액세스하기 위해 OpenAI 관련 노드를 간단히 사용할 수 있습니다. 관련 URL을 DeepSeek의 URL로 변경하기만 하면 됩니다.

#텍스트 채팅

"OpenAI Chat Options" 노드를 만들어 Model, Url, Api Key 매개변수를 설정하십시오.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/deepseek_chat_1.png)

기타 설정은 OpenAI와 동일하며, 완전한 청사진은 다음과 같이 보입니다:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

화면에서 DeepSeek의 반환을 볼 수 있습니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

--8<-- "footer_ko.md"


> 이 글은 ChatGPT로 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 빠뜨림도 감지하십시오. 
