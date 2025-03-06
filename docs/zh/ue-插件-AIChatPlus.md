---
layout: post
title: 说明文档
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini, Ollama]
description: 说明文档
---
<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

# UE 插件 AIChatPlus 说明文档

## 插件商城

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

## 公共仓库

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

## 插件简介

最新版本 v1.6.0。

本插件支持 UE5.2 - UE5.5。

UE.AIChatPlus 是一个 UnrealEngine 插件，该插件实现了与各种 GPT AI 聊天服务进行通信，目前支持的服务有 OpenAI (ChatGPT, DALL-E)，Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, llama.cpp 本地离线。未来还会继续支持更多服务提供商。它的实现基于异步 REST 请求，性能高效，方便 UE 开发人员接入这些 AI 聊天服务。

同时 UE.AIChatPlus 还包含了一个编辑器工具，可以直接在编辑器中使用这些 AI 聊天服务，生成文本和图像，分析图像等。

## 主要功能

**全新！**离线 AI llama.cpp 升级至版本 b4604。

**全新！**离线 AI llama.cpp 支持 GPU Cuda 和 Metal。

**全新！**支持 Gemini 语音转文字。

**API**：支持 OpenAI、Azure OpenAI、Claude、Gemini、Ollama、llama.cpp、DeepSeek

**离线实时 API**：支持 llama.cpp 离线运行 AI，支持 GPU Cuda 和 Metal。

**文本转文本**：各种 API 支持文本生成。

**文本转图像**：OpenAI Dall-E

**图像转文本**：OpenAI Vision、Claude、Gemini、Ollama、llama.cpp

**图像转图像**：OpenAI Dall-E

**语音转文本**：Gemini

**蓝图**：所有 API 和功能都支持蓝图

**编辑器聊天工具**：功能丰富、精心打造的编辑器 AI 聊天工具

**异步调用**：所有的 API 都可以异步调用

**实用工具**：各种图像、音频工具

## 支持的 API：

**离线 llama.cpp**：与 llama.cpp 库集成，可以离线运行 AI 模型！还支持多模态模型（实验性）。支持 Win64/Mac/Android/IOS。支持 GPU CUDA 和 METAL。

**OpenAI**：/chat/completions、/completions、/images/generations、/images/edits、/images/variations

**Azure OpenAI**：/chat/completions、/images/generations

**Claude**：/messages、/complete

**Gemini**：:generateText、:generateContent、:streamGenerateContent

**Ollama**：/api/chat、/api/generate、/api/tags

**DeepSeek**：/chat/completions

## 使用说明

[**使用说明 - 蓝图篇**](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

[**使用说明 - C++ 篇**](ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

[**使用说明 - 编辑器篇**](ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

## 更改日志

[**更改日志**](ue-插件-AIChatPlus-ChangeLogs.md)

## 技术支持

**评论**：有任何问题欢迎在下面评论区留言

**邮件**：也可以通过邮箱给我发邮件 ( disenonec@gmail.com )

**discord**: 即将上线

--8<-- "footer.md"
