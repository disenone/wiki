---
layout: post
title: 說明文件
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
description: 說明文件
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE 插件 AIChatPlus 說明文件

##插件商城

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##公共倉庫

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##插件簡介

最新版本 v1.6.0。

該插件支援 UE5.2 - UE5.5。

UE.AIChatPlus 是一個 UnrealEngine 外掛程式，實現了與各種 GPT AI 聊天服務進行通訊，目前支援的服務有 OpenAI (ChatGPT, DALL-E)，Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, llama.cpp 本地離線。未來還會持續支援更多服務提供商。它的實現基於異步 REST 請求，性能高效，方便 UE 開發人員接入這些 AI 聊天服務。

UE.AIChatPlus 還包含了一個編輯器工具，可以直接在編輯器中使用這些 AI 聊天服務，生成文本和圖像，分析圖像等。

##主要功能

全新！離線 AI llama.cpp 升級至版本 b4604。

**全新！** 線下AI llama.cpp 支援GPU Cuda和Metal。

全新！支援雙子星語音轉文字。

**API**：支援 OpenAI、Azure OpenAI、Claude、Gemini、Ollama、llama.cpp、DeepSeek

**離線即時 API**：支援 llama.cpp 離線執行AI，支援 GPU Cuda 和 Metal。

**Text-to-Text Translation**: 各種 API 支援文本生成。

**文字轉圖像**：OpenAI Dall-E

**圖像轉文本**：OpenAI Vision、Claude、Gemini、Ollama、llama.cpp

**圖像轉圖像**：OpenAI Dall-E

語音轉文字：雙子座

**藍圖**：所有 API 和功能都支持藍圖

**編輯器聊天工具**：功能豐富、精心打造的編輯器 AI 聊天工具

**非同步呼叫**：所有的 API 都可進行非同步呼叫。

**實用工具**：各種圖像、音訊工具

##支援的 API：

**離線 llama.cpp**：與 llama.cpp 庫整合，可離線運行 AI 模型！還支援多模態模型（實驗性）。支援 Win64/Mac/Android/IOS。支援 GPU CUDA 和 METAL。

**OpenAI**：/chat/completions、/completions、/images/generations、/images/edits、/images/variations

Azure OpenAI：/chat/completions、/images/generations

**克勞德**：/訊息、/完成

**雙子座**：generateText、generateContent、streamGenerateContent

**Ollama**：/api/chat、/api/generate、/api/tags

**深度搜索**：/聊天/完成

##Instructions for use

[**Instructions for Use - Blueprint Section**](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

(ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

[**Instructions for Use - Editor Section**](ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

[**Instructions for Use - Packaging**](ue-插件-AIChatPlus-Usage-Package-GetStarted.md)

##修改紀錄

(ue-插件-AIChatPlus-ChangeLogs.md)

##技術支援

備註：如有任何問題，歡迎在下方留言區發表。

**郵件**：您也可以透過電子郵件向我發送郵件（disenonec@gmail.com）.

**discord**: 即將上線

--8<-- "footer_tc.md"


> 這篇文章是由 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出一切遺漏之處。 
