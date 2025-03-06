---
layout: post
title: Ollama
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
description: Ollama
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Ollama" />

#블루프린트 부문 - 올라마

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_all.png)

##"획득 Ollama"

Ollama 공식 웹사이트에서 설치 파일을 다운로드하여 로컬에 설치할 수 있습니다: [ollama.com](https://ollama.com/)

Ollama를 사용하려면 다른 사람이 제공하는 Ollama API 인터페이스를 사용할 수 있습니다.

Ollama을 사용하여 로컬에서 모델을 다운로드하십시오:

```shell
> ollama run qwen:latest
> ollama run moondream:latest
```

##텍스트 채팅

"Ollama Options" 노드를 생성하고 "Model", "Base Url" 매개변수를 설정하십시오. Ollama가 로컬에서 실행 중이라면 "Base Url"은 일반적으로 "http://localhost:11434"입니다.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_chat_1.png)

"Ollama Request" 노드와 "Messages" 관련 노드를 연결하고 실행을 클릭하면 Ollama가 반환한 채팅 정보가 화면에 인쇄됩니다.如图

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

##이 텍스트를 한국어로 번역하시면 됩니다.

Ollama also supported the llava library, providing Vision capabilities.

첫 번째로 Multimodal 모델 파일을 다운로드하세요:

```shell
> ollama run moondream:latest
```

"Options" 노드를 설정하고, "Model"을 moondream:latest로 설정합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_1.png)

이미지 flower.png을 읽고 Message를 설정하세요.

![flower.png](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_3.png)

"Ollama Request" 노드를 연결하고 실행을 클릭하면 화면에 Ollama가 반환한 채팅 정보가 인쇄됩니다.

![](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_4.png)

![](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_5.png)

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. 피드백은 [**여기**](https://github.com/disenone/wiki_blog/issues/new)어떠한 누락된 사항도 지적해주세요. 
