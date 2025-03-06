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

#편집기 섹션 - 시작하기

##편집기 채팅 도구

메뉴 바 Tools -> AIChatPlus -> AIChat을 클릭하여 플러그인에서 제공하는 편집기 채팅 도구를 열 수 있습니다.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


도구는 텍스트 생성, 텍스트 대화, 이미지 생성 및 이미지 분석을 지원합니다.

도구의 인터페이스는 대체로 다음과 같습니다:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

##주요 기능

**오프라인 대규모 모델**: llama.cpp 라이브러리를 통합하여 로컬 오프라인에서 대규모 모델 실행을 지원합니다.

텍스트 채팅: `New Chat` 버튼을 클릭하여 왼쪽 아래 코너에 새로운 텍스트 채팅 세션을 생성하십시오.

**이미지 생성** : 왼쪽 아래의 `New Image Chat` 버튼을 클릭하여 새 이미지 생성 세션을 만듭니다.

* **이미지 분석** : `New Chat`의 일부 채팅 서비스는 이미지를 보낼 수 있도록 지원하며, 예를 들어 Claude, Google Gemini 같은. 보내려는 이미지를 로드하려면 입력란 위의 🖼️ 또는 🎨 버튼을 클릭하십시오.

**오디오 처리**: 도구는 오디오 파일 (.wav)을 읽고 녹음 기능을 제공하여 획득한 오디오를 AI와 대화에 활용할 수 있습니다.

현재 대화 캐릭터 설정: 대화 상자 상단의 드롭다운 메뉴를 사용하여 텍스트를 보낼 현재 캐릭터를 설정할 수 있습니다. AI 대화를 조정하기 위해 다양한 캐릭터를 모방할 수 있습니다.

**대화 지우기**: 채팅 상자 위쪽의 ❌ 버튼을 누르면 현재 대화의 이전 메시지들을 모두 지울 수 있어.

**대화 템플릿**: 수백 가지의 대화 설정 템플릿이 통합되어 있어서 일상적으로 발생하는 문제를 손쉽게 처리할 수 있습니다.

* **전체 설정** : 왼쪽 아래의 `Setting` 버튼을 클릭하면 전체 설정 창이 열립니다. 기본 텍스트 채팅, 이미지 생성 API 서비스를 설정하고 각 API 서비스의 구체적인 매개변수를 설정할 수 있습니다. 설정은 프로젝트 경로인 `$(ProjectFolder)/Saved/AIChatPlusEditor`에 자동으로 저장됩니다.

* **대화 설정**: 채팅 상자 상단의 설정 버튼을 클릭하면 현재 대화의 설정 창이 열립니다. 대화 이름 변경, 사용 중인 API 서비스 수정, 각 대화에 대한 API 구체적 매개변수 지원을 할 수 있습니다. 대화 설정은 자동으로 `$(프로젝트 폴더)/Saved/AIChatPlusEditor/Sessions`에 저장됩니다.

* **채팅 내용 수정** : 채팅 내용 위에 마우스를 올리면 해당 채팅 내용의 설정 버튼이 나타납니다. 컨텐츠를 다시 생성하거나 수정하거나 복사하거나 삭제하거나, 아래에 있는 새로운 컨텐츠를 생성할 수 있습니다 (유저 캐릭터의 경우).

* **이미지 미리 보기**: 이미지 생성에 대해, 이미지를 클릭하면 이미지 뷰어(ImageViewer)가 열리며, 이미지를 PNG/UE 텍스처로 저장할 수 있습니다. 텍스처는 콘텐츠 브라우저(Content Browser)에서 직접 확인할 수 있어 편리하게 이미지를 편집기 내에서 사용할 수 있습니다. 또한 이미지 삭제, 이미지 재생성, 추가 이미지 생성 등의 기능도 지원합니다. Windows에서의 편집기에서 이미지 복사도 지원되어 클립 보드로 바로 복사할 수 있어 사용이 용이합니다. 생성된 이미지는 각 세션 폴더에 자동으로 저장되며 일반적으로 경로는 `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`입니다.

전체 설정:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

대화 설정:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

대화 내용 수정:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

이 텍스트를 한국어로 번역하면 "이미지 뷰어:" 가 됩니다.

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

오프라인 대형 모델 사용

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

대화 템플릿

![system template](assets/img/2024-ue-aichatplus/system_template.png)

##편집기 도구는 오프라인 모델 Cllama(llama.cpp)을 사용합니다.

AIChatPlus 편집기 도구에서 오프라인 모델 llama.cpp를 사용하는 방법에 대한 설명은 다음과 같습니다:

먼저, HuggingFace 웹사이트에서 오프라인 모델 [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

일부 파일을 폴더에 넣어두세요. 예를 들어 게임 프로젝트 폴더 Content/LLAMA에 넣어두시면 됩니다.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

AIChatPlus 에디터 도구를 열어주세요: 도구 -> AIChatPlus -> AIChat을 찾아 새 채팅 세션을 생성하고, 세션 설정 페이지를 열어주세요.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Cllama로 API를 설정하고 사용자 정의 API 설정을 활성화하고 모델 검색 경로를 추가하고 모델을 선택합니다.


![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

대화를 시작하세요!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

##편집기 도구가 오프라인 모델 Cllama(llama.cpp)을 사용하여 이미지를 처리합니다.

HuggingFace 웹사이트에서 오프라인 모델 MobileVLM_V2-1.7B-GGUF를 다운로드하여 Content/LLAMA 디렉터리에 똑같이 넣으세요: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)텍스트를 한국어로 번역해 주세요:

和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)"。" 문자를 한국어로 번역합니다.

세션 모델 설정:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)


이 텍스트를 한국어로 번역해주세요:

* 사진을 보내면 채팅을 시작할 수 있습니다.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

##OpenAI 챗봇을 사용한 편집기.

"대화 도구를 열어주세요. 도구 -> AIChatPlus -> AIChat로 이동해서 새 대화 세션을 만들어주세요. 세션을 ChatApi로 설정하고 OpenAI로 인터페이스 매개변수를 설정해주세요."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

채팅 시작:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

gpt-4o / gpt-4o-mini 모델로 전환하면 OpenAI의 시각 기능을 사용하여 이미지를 분석할 수 있습니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

##편집기가 OpenAI를 사용하여 이미지를 처리합니다(생성/수정/변형)

채팅 도구에서 새 이미지 채팅을 만들고, 채팅 설정을 OpenAI로 변경하고 매개변수를 설정하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

이 텍스트를 한국어로 번역해주세요:

* 이미지 생성

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

이미지를 수정하고, 채팅 이미지 유형을 수정으로 변경한 후에 원본 이미지와 수정이 필요한 부분을 나타내는 마스크 이미지(알파 채널이 0인 투명 위치) 두 장을 업로드해주세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

이미지를 변형하고 Image Chat Type 대화를 Variation으로 수정한 후 이미지를 업로드하면 OpenAI가 원본 이미지의 변형 이미지를 반환합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

##편집기가 Azure를 사용합니다.

"새 대화 만들기(New Chat), ChatApi를 Azure로 변경하고 Azure의 Api 매개변수를 설정하십시오."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

채팅을 시작하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

##에디터가 Azure를 사용하여 이미지를 만든다.

새 이미지 채팅 세션을 생성하고 ChatApi를 Azure로 변경하고 Azure의 API 매개변수를 설정합니다. dall-e-2 모델인 경우 Quality와 Style 매개변수를 not_use로 설정해야 합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

채팅을 시작하고, Azure가 이미지를 생성하도록 하십시오.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

##편집기를 사용하여 Claude와 채팅하고 이미지를 분석합니다.

새 채팅(New Chat)을 만들고, ChatApi를 Claude로 변경하고 Claude의 API 매개변수를 설정합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

채팅을 시작합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

##편집기를 사용하여 Ollama와 채팅하고 이미지를 분석합니다.

* 새 대화(新建会话)를 시작하세요, ChatApi를 Ollama로 변경하고 Ollama의 Api 매개변수를 설정하세요. 텍스트 채팅인 경우 텍스트 모델을 llama3.1과 같이 설정하고 이미지를 처리해야하는 경우 vision을 지원하는 모델인 moondream으로 설정하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

채팅을 시작하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)


###편집기 Gemini 사용

* 새 대화 생성(New Chat), ChatApi를 Gemini으로 변경하고 Gemini의 API 매개변수를 설정하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

대화를 시작하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

##에디터가 Gemini를 사용하여 오디오를 전송합니다.

파일에서 오디오를 읽기/자산에서 오디오를 읽기/마이크로폰으로 오디오를 녹음하여 전송해야 할 오디오 생성

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

채팅 시작

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

##편집기는 Deepseek를 사용합니다.

* 새 대화(새로운 채팅)를 만들고, ChatApi를 OpenAi로 변경하고 Deepseek의 Api 매개변수를 설정하세요. 'Candidate Models'를 deepseek-chat으로 추가하고, 모델을 deepseek-chat로 설정하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

대화 시작하기

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT로 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 누락된 부분도 지적해주세요. 
