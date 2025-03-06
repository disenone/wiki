---
layout: post
title: Cllama (llama.cpp)
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
- llama.cpp
description: Cllama (llama.cpp)
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Cllama (llama.cpp)" />

#도면 부분 - Cllama(llama.cpp)

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_all.png)

##오프라인 모델

Cllama는 llama.cpp를 기반으로 만들어졌으며 오프라인에서 AI 추론 모델을 지원합니다.

오프라인이므로 모델 파일을 준비해야 합니다. 예를 들어 HuggingFace 웹사이트에서 오프라인 모델을 다운로드할 수 있습니다: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

어떤 폴더에 모델을 넣으세요. 예를 들어 게임 프로젝트의 Content/LLAMA 디렉토리에 넣으세요.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA > ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

오프라인 모델 파일이 있으면 Cllama를 통해 AI 채팅을 할 수 있습니다.

##문자 메시지 대화

Cllama를 사용하여 텍스트 채팅을 진행합니다.

블루프린트에서 마우스 오른쪽 버튼을 클릭하여 `Send Cllama Chat Request` 노드를 만드세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Options 노드를 생성하고 `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`을 설정하십시오.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

메시지를 만들고, 시스템 메시지 하나와 사용자 메시지 하나를 추가하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Delegate를 생성하여 모델 출력 정보를 수신하고 화면에 출력하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

완성된 청사진은 이렇게 보입니다. 청사진을 실행하면 게임 화면에 대형 모델을 출력한 메시지가 나타납니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##이 텍스트를 한국어로 번역해주세요:

이미지 생성 텍스트 llava

Cllama는 llava 라이브러리의 실험적인 지원을 제공하여 Vision 기능을 제공합니다.

먼저 Multimodal 오프라인 모델 파일을 준비하세요, 예를 들어 Moondream([moondream2-text-model-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-text-model-f16.gguf), [moondream2-mmproj-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-mmproj-f16.gguf)）또는 Qwen2-VL（[Qwen2-VL-7B-Instruct-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/Qwen2-VL-7B-Instruct-Q8_0.gguf), [mmproj-Qwen2-VL-7B-Instruct-f16.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-7B-Instruct-f16.gguf)）또는 llama.cpp가 지원하는 다중 모델 모드를 지원합니다.

Options 노드를 생성하고 "Model Path" 및 "MMProject Model Path" 매개변수를 해당하는 멀티모달 모델 파일로 설정합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_1.png)

flower.png 이미지 파일을 읽고 Messages를 설정하는 노드를 생성합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_3.png)

마지막으로 노드를 생성하고 반환된 정보를 받아 화면에 출력합니다. 전체 청사진은 다음과 같습니다.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_4.png)

운영 청사진을 확인하면 반환된 텍스트를 볼 수 있습니다.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_5.png)

##llama.cpp은 GPU를 사용합니다.

"Llama Chat Request Options"에 대한 옵션에 "Num Gpu Layer" 매개변수를 추가하여, llama.cpp 파일의 GPU 작업 부하를 설정할 수 있고, GPU에서 계산해야 하는 레이어 수를 제어할 수 있습니다. 아래 그림 참조.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

##.Pak 파일 내에 포장된 모델 파일 처리하기

Pak 파일을 활성화하면 프로젝트의 모든 리소스 파일이 .Pak 파일에 저장되며, 오프라인 모델 gguf 파일도 포함됩니다.

llama.cpp가 .Pak 파일을 직접 읽을 수 없기 때문에 오프라인 모델 파일을 .Pak 파일에서 파일 시스템으로 복사해야 합니다.

AIChatPlus는 .Pak 파일에서 모델 파일을 자동으로 복사하고 처리하여 Saved 폴더에 넣는 기능 함수를 제공합니다:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

모델 파일을 .Pak에서 직접 다루실 수도 있습니다. 중요한 점은 파일을 복사해서 붙여넣어야 합니다. llama.cpp에서 .Pak을 올바르게 읽을 수 없기 때문입니다.

##기능 노드

Cllama는 현재 환경 상태를 손쉽게 얻기 위해 몇 가지 기능 노드를 제공합니다.


"Cllama Is Valid"을(를) 번역하면 "Cllama llama.cpp" 파일이 올바르게 초기화되었는지 확인합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"현재 환경에서 llama.cpp가 GPU 백엔드를 지원하는지 확인합니다."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"얻기 지원 뒷단": llama.cpp가 지원하는 모든 백엔드 얻기


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Pak에 있는 모델 파일을 파일 시스템으로 자동으로 복사합니다."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)


--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)모든 빠진 부분을 지적하십시오. 
