---
layout: post
title: 설명서
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
description: 설명서
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE 플러그인 AIChatPlus 설명서

##플러그인 상점

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##공공 창고

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##플러그인 소개

최신 버전 v1.6.0.

이 플러그인은 UE5.2 - UE5.5를 지원합니다.

UE.AIChatPlus는 UnrealEngine 플러그인으로, 다양한 GPT AI 채팅 서비스와 통신할 수 있습니다. 현재 지원되는 서비스로는 OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, llama.cpp 로컬 오프라인이 있습니다. 향후 더 많은 서비스 제공업체를 지원할 예정입니다. 이 플러그인은 비동기 REST 요청을 기반으로 구현되어 있어 성능이 우수하며 UE 개발자가 이러한 AI 채팅 서비스에 접속하기가 편리합니다.

UE.AIChatPlus에는 편집기 도구가 포함되어 있어 편집기에서 이 AI 채팅 서비스를 직접 사용하여 텍스트와 이미지를 생성하고 이미지를 분석할 수 있습니다.

##주요 기능

**새로운 소식!** 오프라인 AI llama.cpp가 b4604 버전으로 업그레이드되었습니다.

**전세계 최신 소식!** 오프라인 AI llama.cpp가 GPU Cuda와 Metal을 지원합니다.

**Brand new!** Gemini language support for speech-to-text.

**API** : OpenAI, Azure OpenAI, Claude, Gemini, Ollama, llama.cpp, DeepSeek를 지원합니다.

**오프라인 실시간 API**: llama.cpp의 오프라인 AI 실행을 지원하며 GPU Cuda와 Metal을 지원합니다.

이 텍스트를 한국어로 번역해주세요:

**文本转文本**：다양한 API가 텍스트 생성을 지원합니다.

**텍스트를 그림으로 변환하기**: OpenAI Dall-E

**이미지를 텍스트로 변환** : OpenAI Vision, Claude, Gemini, Ollama, llama.cpp

**이미지를 이미지로 변환하기** : OpenAI DALL-E

**음성 인식** : 제미니

**블루프린트**: 모든 API 및 기능이 블루프린트를 지원합니다.

**에디터 채팅 도구**: 기능이 풍부하고 정성들여 만든 에디터 AI 채팅 도구

"비동기 호출": 모든 API는 비동기 호출이 가능합니다.

**실용 도구**: 다양한 이미지, 오디오 도구

##지원하는 API:

**오프라인 llama.cpp** : llama.cpp 라이브러리와 통합되어 AI 모델을 오프라인으로 실행할 수 있습니다! 더불어 실험적으로 다중 모달 모델을 지원하며, Win64/Mac/Android/IOS를 지원합니다. GPU CUDA와 METAL을 지원합니다.

**OpenAI**：/chat/completions、/completions、/images/generations、/images/edits、/images/variations

**Azure OpenAI**：/chat/completions、/images/generations

**클로드**: /메시지, /완료

**쌍둥이**：generateText、generateContent、streamGenerateContent

**Ollama**: /api/chat, /api/generate, /api/tags

**DeepSeek**：/chat/completions

##사용 설명

[사용 설명서 - 블루프린트 편](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

[C++ 설명서 - 사용법](ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

[Korean translation](ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

##변경 로그

[**변경 로그**](ue-插件-AIChatPlus-ChangeLogs.md)

##기술 지원

**댓글**: 어떤 질문이든 아래 댓글란에 남겨주시면 환영합니다.

**이메일**: disenonec@gmail.com 으로 이메일을 보내도 됩니다.

"Discord: Coming soon" into Korean is "디스코드: 곧 출시 예정".

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)중요한 부분을 빠짐없이 지적하십시오. 
