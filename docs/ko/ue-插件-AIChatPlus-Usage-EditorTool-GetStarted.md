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

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 编辑器篇 - Get Started" />

#편집기 - 시작하기

##에디터 채팅 도구

메뉴 바에서 Tools -> AIChatPlus -> AIChat를 선택하면 플러그인에서 제공하는 편집기 채팅 도구가 열립니다.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


도구는 텍스트 생성, 텍스트 채팅, 이미지 생성, 이미지 분석을 지원합니다.

도구의 인터페이스는 대략적으로 다음과 같습니다:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

##주요 기능

**오프라인 대규모 모델**: llama.cpp 라이브러리를 통합하여 로컬에서 대규모 모델을 실행할 수 있습니다.

**문자 대화**: 왼쪽 아래의 `새 대화` 버튼을 클릭하여 새 텍스트 채팅 세션을 생성합니다.

**이미지 생성**: 왼쪽 아래의 '새 이미지 대화' 버튼을 클릭하여 새 이미지 생성 세션을 만듭니다.

**이미지 분석** : 'New Chat'의 일부 채팅 서비스는 이미지를 보낼 수 있도록 지원하며, 예를 들어 Claude, Google Gemini가 있습니다. 전송하려는 이미지를로드하려면 입력 상자 위의 🖼️ 또는 🎨 버튼을 클릭하십시오.

**오디오 처리**: 이 도구는 오디오 파일(.wav)을 읽거나 녹음하여 얻은 오디오로 AI와 대화할 수 있게 해줍니다.

**현재 대화 캐릭터 설정**: 채팅 상자 상단의 드롭다운 메뉴를 통해 현재 텍스트를 전송하는 캐릭터를 설정할 수 있으며, 다양한 캐릭터를 모방하여 AI 대화를 조정할 수 있습니다.

**세션 지우기**: 채팅 상자 위쪽의 ❌ 버튼을 눌러 현재 세션의 대화 기록을 지울 수 있습니다.

**대화 템플릿**: 수백 가지의 대화 설정 템플릿이 내장되어 있어서 일상적인 문제를 쉽게 처리할 수 있습니다.

**전체 설정** : `설정` 버튼을 클릭하여 왼쪽 아래에 전체 설정 창을 열 수 있습니다. 기본 텍스트 채팅, 이미지 생성 API 서비스를 설정하고 각 API 서비스의 구체적인 매개변수를 설정할 수 있습니다. 설정은 자동으로 프로젝트 경로 `$(ProjectFolder)/Saved/AIChatPlusEditor`에 저장됩니다.

**대화 설정**: 채팅 상자 상단의 설정 버튼을 클릭하면 현재 대화의 설정 창을 열 수 있습니다. 대화 이름을 변경하거나 사용 중인 API 서비스를 변경할 수 있으며, 각 대화별로 API에 대한 구체적인 매개변수를 독립적으로 설정할 수 있습니다. 대화 설정은 `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`에 자동으로 저장됩니다.

**채팅 내용 수정**: 채팅 내용 위로 마우스를 올리면 해당 채팅 내용에 대한 설정 버튼이 나타납니다. 내용을 다시 생성하거나 수정하거나 복사하거나 삭제하거나 아래에서 새로운 내용을 생성하는 기능을 지원합니다(캐릭터가 사용자인 경우).

**이미지 브라우징**: 이미지 생성에 대해, 이미지를 클릭하면 이미지 뷰어 팝업이 열립니다. PNG 또는 UE 텍스처로 이미지 저장을 지원하며, 텍스처는 콘텐츠 브라우저에서 바로 확인할 수 있어 편리하게 편집기 내에서 이미지를 사용할 수 있습니다. 또한 이미지 삭제, 이미지 재생성, 추가 이미지 생성 등의 기능을 지원합니다. Windows에서 에디터를 사용할 경우, 이미지 복사도 지원되어 이미지를 바로 클립보드로 복사하여 편리하게 사용할 수 있습니다. 생성된 이미지는 각 세션 폴더에 자동으로 저장되며 일반적으로 경로는 `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images` 입니다.

전체 설정:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

대화 설정:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

채팅 내용 수정:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

이 텍스트를 한국어로 번역합니다: 

이미지 뷰어:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

오프라인 대형 모델 사용

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

대화 템플릿

![system template](assets/img/2024-ue-aichatplus/system_template.png)

##편집기 도구는 오프라인 모델 Cllama(llama.cpp)을 사용합니다.

AIChatPlus 편집기 도구에서 오프라인 모델 llama.cpp을 사용하는 방법에 대한 설명은 다음과 같습니다:

먼저, HuggingFace 웹사이트에서 오프라인 모델을 다운로드하십시오: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

모델을 특정 폴더에 넣으세요. 예를 들어 게임 프로젝트의 Content/LLAMA 디렉토리에 넣으세요.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

AIChatPlus 편집기 도구를 엽니다: 도구 -> AIChatPlus -> AIChat으로 이동하여 새 채팅 세션을 생성하고 세션 설정 페이지를 엽니다.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Api를 Cllama로 설정하고 사용자 지정 Api 설정을 활성화하고 모델 검색 경로를 추가하고 모델을 선택하십시오.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

채팅을 시작하자!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

##에디터 도구는 오프라인 모델 Cllama(llama.cpp)을 사용하여 이미지를 처리합니다.

HuggingFace 웹사이트에서 오프라인 모델 MobileVLM_V2-1.7B-GGUF을 다운로드하여 Content/LLAMA 폴더에 넣으십시오: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)"和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)"."

회의 모델 설정:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

이미지를 보내고 대화를 시작하세요.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

##편집기가 OpenAI 채팅을 사용 중입니다.

채팅 도구를 열어 Tools -> AIChatPlus -> AIChat로 이동하여 새 채팅 세션을 만듭니다. 새로운 채팅을 시작하고, 세션을 ChatApi로 설정하여 OpenAI를 연결하고 인터페이스 매개변수를 설정하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

채팅 시작:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

gpt-4o / gpt-4o-mini 모델로 변경하여 OpenAI의 이미지 분석 기능을 활용할 수 있습니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

##편집기가 OpenAI를 사용하여 이미지를 처리합니다(생성/수정/변형).

채팅 도구에서 새로운 이미지 채팅을 만들고, 채팅 설정을 OpenAI로 변경하고 매개변수를 설정하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

이 텍스트를 한국어로 번역하면 "이미지 만들기"가 됩니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

이미지를 수정하여 Image Chat Type을 "Edit"로 변경하고 원본 이미지와 투명한 부분을 나타내는 마스크 이미지 두 장을 업로드해주세요. 투명한 부분은 수정이 필요한 부분을 나타냅니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

이미지를 변형하여 Image Chat Type를 Variation으로 수정하고 이미지를 업로드하세요. OpenAI는 원본 이미지의 변형 이미지를 반환할 것입니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

##에디터가 Azure를 사용 중입니다.

"새 채팅을 시작하세요(New Chat), ChatApi를 Azure로 변경하고 Azure의 API 매개변수를 설정하세요."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

채팅을 시작하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

##편집기 사용 Azure로 이미지 생성

새 이미지 채팅 세션을 만들어 ChatApi를 Azure로 변경하고 Azure의 API 매개변수를 설정합니다. 만약 dall-e-2 모델을 사용하는 경우, Quality와 Stype 매개변수를 not_use로 설정해야 합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

대화를 시작하고 Azure가 이미지를 생성하도록합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

##"편집기를 사용하여 Claude와 채팅하고 사진을 분석합니다."

새 대화(새 채팅)를 만들고 ChatApi를 Claude로 변경하고 Claude의 API 매개변수를 설정하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

대화를 시작하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

##에디터가 Ollama를 사용하여 채팅하고 이미지를 분석합니다.

새 대화를 시작하세요(New Chat), ChatApi를 Ollama로 변경하고 Ollama의 API 매개변수를 설정하세요. 텍스트 채팅인 경우 텍스트 모델인 llama3.1로 설정하고 이미지 처리가 필요한 경우 vision을 지원하는 moondream과 같은 모델로 설정하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

채팅 시작

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Gemini를 사용한 에디터.

"새 대화 생성(New Chat), ChatApi를 Gemini으로 변경하고 Gemini의 Api 매개변수를 설정하십시오."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

대화를 시작합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

##편집기가 Gemini를 사용하여 오디오를 전송합니다.

파일에서 오디오 읽기 / 에셋에서 오디오 읽기 / 마이크로 오디오 녹음하여 전송해야 하는 오디오 생성

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

채팅을 시작하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

##편집기는 Deepseek를 사용합니다.

새 대화(New Chat) 세션을 시작하고 ChatApi를 OpenAi로 변경하고 Deepseek의 Api 매개변수를 설정하십시오. Candidate Models에 deepseek-chat을 추가하고 해당 모델을 deepseek-chat으로 설정하십시오.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

채팅을 시작하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT로 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 누락된 것도 지적하십시오. 
