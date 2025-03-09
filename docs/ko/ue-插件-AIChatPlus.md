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

##확장 기능 상점

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##공공 창고

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##플러그인 소개

최신 버전 v1.6.0.

이 플러그인은 UE5.2 - UE5.5를 지원합니다.

UE.AIChatPlus는 UnrealEngine 플러그인으로, 다양한 GPT AI 채팅 서비스와 통신을 구현합니다. 현재 지원되는 서비스로는 OpenAI(ChatGPT, DALL-E), Azure OpenAI(ChatGPT, DALL-E), Claude, Google Gemini, Ollama, llama.cpp 로컬 오프라인이 있습니다. 미래에는 더 많은 서비스 제공 업체를 지원할 예정입니다. 이 구현은 비동기 REST 요청을 기반으로 하며, 성능이 효율적이며 UE 개발자가 이러한 AI 채팅 서비스에 쉽게 접근할 수 있도록 합니다.

UE.AIChatPlus에는 편집기 도구가 포함되어 있어 편집기에서 직접 AI 채팅 서비스를 사용하여 텍스트 및 이미지를 생성하고 이미지를 분석할 수 있습니다.

##주요 기능

**최신 소식!** 오프라인 AI llama.cpp가 b4604 버전으로 업그레이드되었습니다.

**브랜드 뉴!** 오프라인 AI llama.cpp가 GPU Cuda와 Metal을 지원합니다.

**신제품!** Gemini 음성을 텍스트로 변환하는 기능을 지원합니다.

**API** : OpenAI, Azure OpenAI, Claude, Gemini, Ollama, llama.cpp, DeepSeek를 지원합니다.

**오프라인 실시간 API**: llama.cpp를 지원하여 AI를 오프라인으로 실행하며, GPU Cuda와 Metal을 지원합니다.

이 텍스트를 한국어로 번역해주세요:

**텍스트를 텍스트로 변환** : 다양한 API가 텍스트 생성을 지원합니다.

**텍스트를 그림으로 만들기**: OpenAI DALL-E

**이미지를 텍스트로 전환** : OpenAI Vision, Claude, Gemini, Ollama, llama.cpp

**이미지에서 이미지로** : OpenAI Dall-E

**음성 인식**: Gemini

**블루프린트**: 모든 API와 기능은 블루프린트를 지원합니다.

**편집기 채팅 도구**: 기능이 풍부하고 정성으로 만들어진 편집기 AI 채팅 도구

**비동기 호출**: 모든 API는 비동기적으로 호출할 수 있습니다.

**실용 도구**: 다양한 이미지, 오디오 도구

##지원되는 API:

**오프라인 llama.cpp**: llama.cpp 라이브러리와 통합되어 AI 모델을 오프라인에서 실행할 수 있습니다! 실험적으로 다중 모달 모델도 지원합니다. Win64/Mac/Android/IOS를 지원하며 GPU CUDA와 METAL도 지원합니다.

오픈에이 아이：/챗/완성품, /완성품, /이미지/생성, /이미지/편집, /이미지/변형

**Azure OpenAI**: /chat/completions, /images/generations

**Claude**: /메시지, /완료

**쌍둥이자리**: generateText, generateContent, streamGenerateContent

**Ollama** : /api/chat, /api/generate, /api/tags

**DeepSeek**：/chat/completions

##사용 설명서

[**사용설명서 - 블루프린트 편**](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

[C++ 섹션 사용 설명서](ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

[**사용 설명서 - 편집기 편**](ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

[**사용 설명 - 포장**](ue-插件-AIChatPlus-Usage-Package-GetStarted.md)

##변경 로그

[**업데이트 내역**](ue-插件-AIChatPlus-ChangeLogs.md)

##기술 지원

**의견**: 아무 문제가 있으면 아래 의견란에 남겨주세요.

**이메일**: 이메일로도 연락 가능합니다 (disenonec@gmail.com)

디스코드: 곧 출시되오니 기대해 주세요.

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 빠뜨린 부분도 지적하십시오. 
