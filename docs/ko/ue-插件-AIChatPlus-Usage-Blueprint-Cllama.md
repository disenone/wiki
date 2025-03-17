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

#블루프린트 섹션 - Cllama (llama.cpp)

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_all.png)

##오프라인 모델

Cllama는 llama.cpp를 기반으로 구현되어 있으며 오프라인에서 AI 추론 모델을 지원합니다.

오프라인이라 준비해야 할 모델 파일이 필요합니다. HuggingFace 웹사이트에서 오프라인 모델을 다운로드할 수 있습니다: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

어떤 파일에 모델을 넣어 놓으세요. 예를 들어, 게임 프로젝트 폴더 내 Content/LLAMA에 넣어 두시면 됩니다.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA > ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

오프라인 모델 파일이 있으면 Cllama를 이용하여 AI 채팅을 할 수 있습니다.

##텍스트 채팅

Cllama를 사용하여 텍스트 채팅을 합니다.

블루프린트에서 'Send Cllama Chat Request' 노드를 만들려면 마우스 오른쪽 버튼을 클릭하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Options 노드를 생성하고 `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`로 설정하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

메시지를 만들고 시스템 메시지와 사용자 메시지를 각각 추가하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Delegate를 생성하여 모델 출력 정보를 받아 화면에 출력합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

전체 블루프린트는 다음과 같습니다. 블루프린트를 실행하면 게임 화면에 대형 모델이 인쇄된 메시지가 표시됩니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##"이미지 생성 텍스트 llava"

Cllama는 llava 라이브러리를 실험적으로 지원하여 Vision 기능을 제공합니다.

우선 Multimodal 오프라인 모델 파일을 준비하세요, 예를 들어 Moondream ([moondream2-text-model-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-text-model-f16.gguf), [moondream2-mmproj-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-mmproj-f16.gguf)）또는 Qwen2-VL([Qwen2-VL-7B-Instruct-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/Qwen2-VL-7B-Instruct-Q8_0.gguf), [mmproj-Qwen2-VL-7B-Instruct-f16.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-7B-Instruct-f16.gguf)）또는 다른 llama.cpp에서 지원하는 다중 모달 모델.

Options 노드를 생성하고 "Model Path" 및 "MMProject Model Path" 매개변수를 각각 해당하는 다중모달 모델 파일로 설정합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_1.png)

이 텍스트를 한국어로 번역해주세요:

노드를 생성하여 이미지 파일 flower.png을 읽고, 메시지 설정하기

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_3.png)

최종적으로 노드를 생성하고 반환된 정보를 받아 화면에 출력합니다. 전체적인 청사진은 다음과 같습니다.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_4.png)

운영 블루프린트에서는 반환된 텍스트를 볼 수 있습니다.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_5.png)

##llama.cpp은 GPU를 사용합니다.

"Cllama Chat Request Options"에 추가 매개변수 "Num Gpu Layer"를 도입하였습니다. 이를 통해 llama.cpp의 GPU 페이로드를 설정할 수 있게 되었고, GPU에서 계산해야 하는 레이어 수를 제어할 수 있습니다. 아래 이미지를 참고하세요.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

## KeepAlive

"Cllama Chat Request Options" 추가 매개변수 "KeepAlive"은 모델 파일을 읽은 뒤 메모리에 유지하여 다음에 바로 사용할 수 있도록 해 주어 모델을 다시 읽는 횟수를 줄일 수 있습니다. KeepAlive는 모델이 유지되는 시간을 나타내며, 0은 유지하지 않고 즉시 해제하는 것을 의미하며, -1은 영구적인 유지를 나타냅니다. 각 요청마다 설정된 Options은 서로 다른 KeepAlive를 설정할 수 있으며, 새로운 KeepAlive는 이전 값 대신 적용되며, 예를 들어 처음 몇 번의 요청은 KeepAlive=-1로 설정하여 모델을 메모리에 유지하고, 마지막 요청에서 KeepAlive=0으로 설정하여 모델 파일을 해제할 수 있습니다.

##.Pak 파일에 포함된 모델 파일을 처리하십시오.

Pak 파일을 생성하면 프로젝트의 모든 리소스 파일이 .Pak 파일에 저장되며 이는 오프라인 모델 gguf 파일도 포함됩니다.

llama.cpp가 .Pak 파일을 직접 읽을 수 없기 때문에 오프라인 모델 파일을 .Pak 파일에서 파일 시스템으로 복사해야 합니다.

AIChatPlus는 .Pak 파일에서 모델 파일을 자동으로 복사하고 Saved 폴더에 저장하는 기능 함수를 제공합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

.Pak 파일에서 모델 파일을 직접 처리할 수도 있습니다. 중요한 점은 파일을 복사하여야 하는데, llama.cpp가 .Pak을 올바르게 읽지 못하기 때문입니다.

##기능 노드

Cllama는 현재 환경에서 상태를 쉽게 얻을 수 있도록 일부 기능 노드를 제공합니다.


"Cllama Is Valid"은 Cllama llama.cpp이 올바르게 초기화되었는지 확인합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu"：llama.cpp이 현재 환경에서 GPU 백엔드를 지원하는지 확인합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"현재 llama.cpp가 지원하는 모든 백엔드를 가져옵니다."


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

팹에 있는 모델 파일을 파일 시스템으로 자동으로 복사합니다.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)


--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 빠진 부분도 지적해 주세요. 
