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

#UE 插件 AIChatPlus 使用說明

##插件商場

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##公共倉庫

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##插件簡介

最新版本 v2.0.0。

本插件支援 UE5.2 至 UE5.7 版本。

UE.AIChatPlus 是一個 UnrealEngine 插件，該插件實現了與各種 GPT AI 聊天服務進行通信，目前支援的服務有 OpenAI (ChatGPT, DALL-E)、Azure OpenAI (ChatGPT, DALL-E)、Claude、Google Gemini、Ollama、llama.cpp 本地離線。未來還會繼續支援更多服務提供商。它的實現基於非同步 REST 請求，性能高效，方便 UE 開發人員接入這些 AI 聊天服務。

同時，UE.AIChatPlus 還包含了一個編輯器工具，能夠讓您直接在編輯器中使用這些AI聊天服務，不僅能生成文字和圖像，還能進行圖像分析等功能。

##主要功能

**全新！**所有 API 皆支援 ToolCall。

**全新！**OpenAI/Azure 支援語音轉文字和文字轉語音。

**全新！**藍圖支援 Json。

**全新！**離線 AI llama.cpp 升級至版本 b6792。

**全新！**離線 AI llama.cpp 支援 GPU Cuda 與 Metal。

**全新功能！**支援Gemini語音轉文字。

**API**：支援 OpenAI、Azure OpenAI、Claude、Gemini、Ollama、llama.cpp、DeepSeek

**離線即時 API**：支援 llama.cpp 離線執行 AI，兼容 GPU Cuda 與 Metal。

**文字轉文字**：各種API支援文字生成。

**文字轉圖像**：OpenAI Dall-E

**影像轉文字**：OpenAI Vision、Claude、Gemini、Ollama、llama.cpp

**圖像轉圖像**：OpenAI Dall-E

**語音轉文字**：Gemini

**藍圖**：所有 API 和功能都支援藍圖

**編輯器聊天工具**：功能豐富、精心打造的編輯器 AI 聊天工具

**非同步呼叫**：所有的 API 都能以非同步方式呼叫

**實用工具**：各種圖像、音訊工具

##支援的 API：

**離線 llama.cpp**：整合 llama.cpp 函式庫，能夠離線運行 AI 模型！還支援多模態模型（實驗性）。相容 Win64/Mac/Android/IOS 平台。支援 GPU CUDA 和 METAL 架構。

**OpenAI**：/chat/completions、/completions、/images/generations、/images/edits、/images/variations

**Azure OpenAI**：/chat/completions、/images/generations

**Claude**：/訊息、/完成

**雙子座**：:generateText、:generateContent、:streamGenerateContent

**Ollama**：/api/聊天、/api/生成、/api/標籤

**DeepSeek**：/chat/completions

##使用說明

[**使用說明 - 藍圖篇**](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

[**使用說明 - C++ 篇**](ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

[**使用說明 - 編輯器篇**](ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

[**使用說明 - 打包**](ue-插件-AIChatPlus-Usage-Package-GetStarted.md)

##更新日誌

[**變更日誌**](ue-插件-AIChatPlus-ChangeLogs.md)

##技術支援

**評論**：有任何問題歡迎在下面評論區留言

**郵件**：也可以透過信箱給我發郵件 ( disenonec@gmail.com )

**discord**: 即將上線

--8<-- "footer_tc.md"


> 此貼子是使用 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
