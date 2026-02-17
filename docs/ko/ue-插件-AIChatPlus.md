---
layout: post
title: 설명 문서
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
description: 설명 문서
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE 플러그인 AIChatPlus 설명 문서

##플러그인 스토어

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##공개 창고

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##플러그인 소개

최신 버전 v2.0.0.

본 플러그인은 UE5.2부터 UE5.7까지 지원합니다.

UE.AIChatPlus는 언리얼엔진 플러그인으로, 다양한 GPT AI 채팅 서비스와의 통신을 구현하였습니다. 현재 지원하는 서비스는 OpenAI(ChatGPT, DALL-E), Azure OpenAI(ChatGPT, DALL-E), Claude, Google Gemini, Ollama, llama.cpp 로컬 오프라인 버전 등이며, 앞으로도 더 많은 서비스 제공업체를 지원할 예정입니다. 이 플러그인은 비동기 REST 요청을 기반으로 구현되어 있어 고성능을 자랑하며, UE 개발자들이 이러한 AI 채팅 서비스에 쉽게 접근할 수 있도록 도와줍니다.

동시에 UE.AIChatPlus는 편집기 도구도 포함하고 있어, 편집기 내에서 바로 이러한 AI 채팅 서비스를 사용해 텍스트와 이미지를 생성하고, 이미지를 분석하는 등의 작업을 할 수 있습니다.

##주요 기능

**신규!** 모든 API가 ToolCall을 지원합니다.

**새로움!** OpenAI/Azure가 음성 텍스트 변환과 텍스트 음성 변환을 지원합니다.

**새로워요!** 청사진이 Json을 지원합니다.

**새롭게!** 오프라인 AI llama.cpp가 버전 b6792로 업그레이드되었습니다.

**새로워요!** 오프라인 AI llama.cpp가 GPU Cuda와 Metal을 지원합니다.

**새롭게!** Gemini 음성 텍스트 변환을 지원합니다.

**API**: OpenAI, Azure OpenAI, Claude, Gemini, Ollama, llama.cpp, DeepSeek 지원

**오프라인 실시간 API**: llama.cpp를 통해 오프라인에서 AI를 실행할 수 있으며, GPU Cuda 및 Metal을 지원합니다.

**텍스트 대 텍스트**: 다양한 API가 텍스트 생성을 지원합니다.

**텍스트를 이미지로**：OpenAI Dall-E

**이미지에서 텍스트 추출**: OpenAI Vision, Claude, Gemini, Ollama, llama.cpp

**이미지에서 이미지로**: OpenAI Dall-E

**음성 텍스트 변환**: Gemini

**청사진**: 모든 API와 기능이 청사진을 지원합니다.

**에디터 채팅 도구**：기능이 풍부하고 세심하게 제작된 에디터 AI 채팅 도구

**비동기 호출**: 모든 API는 비동기로 호출할 수 있습니다.

**실용적인 도구**: 다양한 이미지 및 오디오 도구

##지원하는 API：

**오프라인 llama.cpp**：llama.cpp 라이브러리와 통합되어 AI 모델을 오프라인에서 실행할 수 있습니다! 또한 멀티모달 모델(실험적 기능)도 지원합니다. Win64/Mac/Android/IOS를 지원하며, GPU CUDA와 METAL도 사용 가능합니다.

**OpenAI**: /chat/completions, /completions, /images/generations, /images/edits, /images/variations

**Azure OpenAI**: /chat/completions, /images/generations

**Claude**：/메시지, /완료

**제미니**: :generateText, :generateContent, :streamGenerateContent

**Ollama**: /api/chat, /api/generate, /api/tags

**DeepSeek**：/채팅/완성

##사용 설명서

[**사용 설명서 - 청사진 편**](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

[**사용 설명서 - C++ 편**](ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

[**사용 설명서 - 편집기 편**](ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

[**사용 설명 - 포장**](ue-插件-AIChatPlus-Usage-Package-GetStarted.md)

##변경 로그

[**변경 로그**](ue-插件-AIChatPlus-ChangeLogs.md)

##기술 지원

**댓글**: 궁금한 점이 있으면 아래 댓글란에 글 남겨주세요

**이메일**：이메일로도 연락주세요 ( disenonec@gmail.com )

**디스코드**: 출시 예정

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. 의견이 있으시면 [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 누락된 부분도 지적한다. 
