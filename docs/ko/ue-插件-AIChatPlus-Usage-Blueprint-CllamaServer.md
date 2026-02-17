---
layout: post
title: CllamaServer (llama.cpp server)
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
- CllamaServer
description: CllamaServer (llama.cpp server)
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - CllamaServer (llama.cpp server)" />

#청사진 편 - CllamaServer (llama.cpp 서버)

<!-- 이미지 필요: CllamaServer 관련 모든 블루프린트 노드 개요를 보여주는 그림, 다른 문서의 xxx_all.png와 유사한 -->
![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_all.png)

##개요

CllamaServer는 llama.cpp의 서버 모드를 기반으로 구현되었으며, 로컬에서 OpenAI API와 호환되는 서버를 시작할 수 있고, 다양한 기능을 지원합니다:

* **로컬 추론 서비스**: 외부 API에 의존하지 않고 로컬에서 AI 추론 서버를 시작합니다
* **OpenAI API 호환**: OpenAI와 호환되는 API 형식을 사용하여 이전과 통합이 용이합니다
* **다중 세션 지원**: 여러 동시 요청을 지원합니다
* **도구 호출(Tool Calling)**: 함수 호출 기능을 지원합니다
* **음성 텍스트 변환**: Speech-to-Text 기능 지원
* **시각화 관리**: 편집기 내장 서버 관리 인터페이스

Cllama와의 차이점:
* **Cllama**: 모델을 프로세스 내에 직접 로드하여 추론을 수행하며, 한 번에 하나의 요청만 처리할 수 있습니다.
* **CllamaServer**: 독립적인 HTTP 서버를 시작하여 여러 동시 요청을 처리할 수 있으며, OpenAI 형식과 호환되는 API를 제공합니다.

##준비 작업

로컬에서 실행되므로 오프라인 모델 파일을 먼저 준비해야 합니다. 예를 들어 HuggingFace에서 [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

모델을 특정 폴더 아래에 놓으세요. 예를 들어 게임 프로젝트 디렉터리의 `Content/LLAMA` 아래에 위치시킬 수 있습니다.

##CllamaServer 생성하기

###블루프린트를 사용하여 서버 생성하기

블루프린트에서 우클릭하여 노드 생성 `Create Cllama Server In World`

<!-- 필요 이미지: 블루프린트에서 마우스 오른쪽 버튼으로 "Create Cllama Server"를 검색하고 노드를 생성하는 화면 캡처 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_1.png)

###서버 매개변수 구성

`Cllama Server Param` 노드를 생성하고, 주요 매개변수를 구성합니다:

* **모델**: 모델 파일 경로(필수)
* **포트**: 서버 포트(0은 자동 할당을 의미함)
* **호스트**: 청취 주소, 기본값 `127.0.0.1`
* **NGpuLayers**: GPU 레이어 수 (-1은 모든 GPU 사용을 의미함)

<!-- 이미지 필요: FAIChatPlus_CllamaServerParam 노드를 생성하고, Model 경로, Port, NGpuLayers 등의 매개변수를 설정하는 화면 캡처 표시 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_2.png)

###바인딩 콜백 이벤트

서버의 콜백 이벤트 바인딩:

* **시작 시**: 서버가 성공적으로 시작되었을 때 트리거됨
* **중지 시**: 서버가 중지될 때 트리거됩니다.
* **실패 시**: 서버 시작이 실패했을 때 트리거됩니다.

<!-- 이미지 필요: OnStartedListeners, OnStoppedListeners, OnFailedListeners 이벤트를 바인딩한 블루프린트 예시 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_3.png)

###완벽한 생성 설계도

서버 생성 전체 로드맵은 다음과 같습니다:

<!-- 이미지 필요: 매개변수 설정, 생성 노드, 콜백 바인딩을 포함한 완전한 Server 생성 블루프린트의 전체 모습을 보여줌 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_4.png)

블루프린트 실행 후, 서버가 성공적으로 시작되면 `On Started` 이벤트가 트리거됩니다.

<!-- 그림 필요: Server 시작 성공 후의 실행 결과를 보여주는 이미지, 성공적으로 시작되었음을 알리는 로그 또는 화면 출력을 표시 -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_5.png) -->

##서버 매개변수 상세 설명

`FAIChatPlus_CllamaServerParam` 구조체에는 다음 매개변수가 포함됩니다:

###일반 매개변수

| 매개변수 | 유형 | 기본값 | 설명 |
|-----|------|-------|------|
| 모델 | FString | - | 모델 파일 경로 (필수 입력) |
| 포트 | int32 | 0 | 감시 포트, 0은 자동 할당을 의미합니다 |
| 호스트 | FString | 127.0.0.1 | 리슨 주소 |
| NGpuLayers | int32 | -1 | GPU 레이어 수, -1은 모두를 의미함 |
| bUseJinja | bool | false | Jinja 템플릿 사용 여부 |
| MMProj | FString | - | 멀티모달 프로젝션 파일 경로 |
| 온도 | 실수형 | 0.8 | 샘플링 온도 |

###추론 매개변수

| 매개변수 | 유형 | 기본값 | 설명 |
|-----|------|-------|------|
| CtxSize | int32 | 4096 | 컨텍스트 크기 |
| NPredict | int32 | -1 | 예측할 토큰 수, -1은 무제한을 의미 |
| 스레드 | int32 | -1 | CPU 스레드 수, -1은 자동을 의미 |
| 배치사이즈 | int32 | 2048 | 배치 처리 크기 |

###샘플링 매개변수

| 매개변수 | 유형 | 기본값 | 설명 |
|-----|------|-------|------|
| TopK | int32 | 40 | 탑 K 샘플링 |
| TopP | float | 0.9 | Top-P 샘플링 |
| MinP | float | 0.1 | 최소 확률 샘플링 |
| RepeatPenalty | float | 1.0 | 반복 패널티 |

###서버 파라미터

| 매개변수 | 유형 | 기본값 | 설명 |
|-----|------|-------|------|
| ApiKey | FString | - | API 키 (선택 사항) |
| 타임아웃 | int32 | 600 | 타임아웃 시간(초) |
| 병렬 | int32 | 1 | 병렬 시퀀스 수 |
| bNoWebUI | bool | false | 웹 UI 비활성화 |
| bVerbose | bool | false | 상세 로그 |

##CllamaServer를 사용하여 채팅하기

###채팅 요청 생성

서버가 성공적으로 시작되면 `Send CllamaServer Chat Request` 노드를 사용하여 채팅 요청을 보낼 수 있습니다.

<!-- 이미지 필요: 블루프린트에서 우클릭으로 "CllamaServer Chat Request"를 검색하여 노드를 생성하는 화면 캡처 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_1.png)

###채팅 옵션 설정

`CllamaServer Chat Request Options` 노드를 생성하고, BaseUrl을 서버 주소로 설정하세요.

`Get Server Info By ID` 노드를 통해 서버 정보를 얻을 수 있습니다.

<!-- 이미지 필요: FAIChatPlus_CllamaServerChatRequestOptions 노드 생성, Get Http Address를 사용하여 서버 주소를 가져와 BaseUrl에 설정하는 블루프린트 표시 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_2.png)

###메시지 생성

Messages 배열을 생성하고 System Message와 User Message를 추가합니다.

<!-- 이미지 필요: Messages 배열 생성 예시, System Message(어시스턴트 역할 설정)와 User Message(사용자 질문)가 포함된 블루프린트를 보여주는 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_3.png)

###콜백 바인딩으로 응답 처리

`On Message` 또는 `On Message Finished` 이벤트를 바인딩하여 모델 응답을 수신합니다.

<!-- 이미지 필요: OnMessageListeners 이벤트를 바인딩하고, 콜백에서 메시지를 화면에 출력하는 블루프린트를 보여주는 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_4.png)

###완벽한 채팅 청사진

완전한 채팅 설계도는 다음과 같습니다:

<!-- 이미지 필요: 전체 채팅 블루프린트 그림을 보여주는 것으로, 서버 생성, 시작 대기, 채팅 요청 전송, 응답 처리의 전체 흐름을 포함해야 함 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_5.png)

###실행 결과

청사진을 실행하면 모델이 반환한 메시지가 화면에 표시됩니다.

<!-- 필요한 이미지: 채팅 실행 결과를 보여주며, 화면에 모델이 반환한 응답 내용이 표시된 모습 -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_6.png) -->

##서버 관리

###서버 정보 가져오기

`Get Server Info` 노드를 사용하여 서버의 상세 정보를 가져옵니다.

<!-- 이미지 필요: Get Server Info 노드를 사용하여 FAIChatPlus_CllamaServerInfo를 가져오는 블루프린트와 각 필드를 Break로 표시하는 것을 보여주는 예시 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_info_1.png)

서버 정보는 다음과 같은 정보를 포함합니다:
* **ServerID**: 서버 고유 ID
* **호스트**: 수신 주소
* **포트**: 리스닝 포트
* **주소**: 전체 주소(host:port)
* **HttpAddress**: HTTP 주소 (http://host:port)
* **bIsRunning**: 실행 중인지 여부
* **Param**: 서버 파라미터

###서버 중지

현재 서버를 중지하려면 `Stop Server By ID` 노드를 사용하십시오.

<!-- 이미지 필요: Stop Cllama Server 노드 호출을 보여주는 블루프린트 예시 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_stop_1.png)

###정적 관리 함수

AIChatPlus는 모든 서버 관리를 위한 일련의 정적 함수를 제공합니다:

| 함수 | 설명 |
|-----|------|
| `서버 유효 확인 (정적)` | 서버가 유효한지 확인합니다 |
| `서버 실행 중 확인 (정적)` | 서버가 실행 중인지 확인합니다 |
| `Stop Server By ID` | ID로 지정된 서버 정지 |
| `모든 서버 중지` | 모든 서버를 중지합니다 |
| `Get Server Info By ID` | ID로 서버 정보 가져오기 |
| `모든 서버 ID 가져오기` | 모든 Server ID 획득 |
| `Get Server By ID` | ID로 서버 인스턴스 가져오기 |

<!-- 필요 이미지: GetAllServerIDs 및 StopAllServers와 같은 정적 관리 함수를 사용하는 블루프린트 예시를 보여주는 것 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_static_1.png)

##다중모드 지원

CllamaServer는 다중 모달 모델(Moondream, Qwen2-VL 등)을 지원합니다.

###멀티모달 파라미터 구성

Server 매개변수에서 `MMProj`(다중 모드 프로젝션 파일 경로)를 설정합니다:

<!-- 필요 이미지: Server Param에서 Model과 MMProj 두 경로를 설정하는 블루프린트를 보여주는 사진 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_1.png)

###이미지 메시지 보내기

Messages에 사진 추가하기:

<!-- 이미지 필요: 이미지 파일을 읽고, 이미지가 포함된 메시지를 생성하여 CllamaServer로 요청을 보내는 것을 보여주는 블루프린트 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_2.png)

<!-- ### 실행 결과 -->

<!-- 이미지 필요: 이미지 인식 실행 결과를 보여주며, 화면에는 모델이 이미지 내용을 설명하는 내용이 표시된다 -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_3.png) -->

## Tool Calling

CllamaServer는 Tool Calling(함수 호출) 기능을 지원하며, 사용법은 OpenAI와 유사합니다.

자세한 사용법은 [Tool Call](ue-插件-AIChatPlus-Usage-Blueprint-ToolCall.md)문서.

CllamaServer를 사용하여 Tool Call을 할 때에는 다음과 같은 사항이 필요합니다:
1. Server 파라미터에서 `bUseJinja = true`로 설정하세요.
2. Chat Options의 Tools 필드에서 도구 정의하기

<!-- 이미지 필요: CllamaServer Tool Call의 전체 블루프린트를 보여주는 이미지로, bUseJinja=true 설정 및 Tools 정의가 포함된 모습 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_tool_1.png)

##편집기 Server 관리

AIChatPlus는 편집기 도구 내에서 시각적인 CllamaServer 관리 인터페이스를 제공하여 여러 서버의 생성, 모니터링 및 관리를 용이하게 합니다.

편집기 도구 열기: `도구 -> AIChatPlus -> AIChat`, Cllama 서버 관리자 탭을 엽니다.

<!-- 이미지 필요: 에디터 내 CllamaServer 관리 인터페이스 스크린샷 표시, 서버 목록, 생성 버튼, 상태 정보 등이 보이는 화면 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_editor_1.png)

에디터에서 할 수 있는 작업은 다음과 같습니다:
* 새로운 서버 생성
* 실행 중인 Server 상태 확인하기
* 지정된 서버 정지
* 서버 파라미터 구성하기
* 서버 구성은 자동으로 저장됩니다

<!-- 이미지 필요: 편집기에서 새 Server를 만드는 화면을 보여주고, 매개변수 설정 패널이 표시되도록 함 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_editor_2.png)

##다른 API와의 관계

CllamaServer가 OpenAI API 형식과 호환되기 때문에, OpenAI의 Chat Request 노드를 사용하여 CllamaServer와 통신할 수도 있습니다. `BaseUrl`을 CllamaServer의 주소로 설정하기만 하면 됩니다.

<!-- 필요 이미지: OpenAI Chat Request 노드를 사용하지만 BaseUrl을 CllamaServer 주소로 설정한 블루프린트 예시 보여주기 -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_openai_1.png) -->

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT로 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 누락된 부분도 지적하지 않는다. 
