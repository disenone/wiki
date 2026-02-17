---
layout: post
title: Documentation
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
description: Documentation
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE Plugin AIChatPlus Documentation

##Plugin Store

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##Public Repository

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Plugin Introduction

Latest version v2.0.0.

This plugin supports UE5.2 - UE5.7.

UE.AIChatPlus is an UnrealEngine plugin that enables communication with various GPT AI chat services. Currently supported services include OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and llama.cpp for local offline use. Support for additional service providers will be added in the future. Built on asynchronous REST requests, it delivers high performance and offers UnrealEngine developers seamless integration with these AI chat services.

Meanwhile, UE.AIChatPlus also includes an editor tool, allowing users to utilize these AI chat services directly within the editor—generating text and images, analyzing images, and more.

##Main Features

**Brand new!** All APIs now support ToolCall.

**New!** OpenAI/Azure supports speech-to-text and text-to-speech.

**New!** Blueprint now supports Json.

**New!** Offline AI llama.cpp upgraded to version b6792.

**New!** Offline AI llama.cpp supports GPU Cuda and Metal.

**New!** Supports Gemini Speech-to-Text.

**APIs**: Supports OpenAI, Azure OpenAI, Claude, Gemini, Ollama, llama.cpp, DeepSeek

**Offline Real-time API**: Supports offline operation of AI with llama.cpp, compatible with GPU Cuda and Metal.

**Text-to-Text**: Various APIs support text generation.

**Text-to-Image**: OpenAI Dall-E

**Image to Text**: OpenAI Vision, Claude, Gemini, Ollama, llama.cpp

**Image-to-Image**: OpenAI Dall-E

**Speech-to-Text**: Gemini

**Blueprint**: All APIs and functionalities support blueprints

**Editor Chat Tool**: A feature-rich, meticulously crafted editor AI chat tool

**Asynchronous Invocation**: All APIs can be called asynchronously.

**Practical Tools**: Various image and audio utilities

##Supported APIs:

**Offline llama.cpp**: Integrates with the llama.cpp library to run AI models offline! Also supports multimodal models (experimental). Compatible with Win64/Mac/Android/iOS. Features GPU CUDA and METAL support.

**OpenAI**: /chat/completions, /completions, /images/generations, /images/edits, /images/variations

**Azure OpenAI**: /chat/completions, /images/generations

**Claude**: /messages, /complete

**Gemini**: :generateText、:generateContent、:streamGenerateContent

**Ollama**: /api/chat, /api/generate, /api/tags

**DeepSeek**: /chat/completions

##Instructions for Use

[**Instructions - Blueprint Edition**](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

[**Usage Instructions - C++ Edition**](ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

[**User Guide - Editor Section**](ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

[**Instructions - Packaging**](ue-插件-AIChatPlus-Usage-Package-GetStarted.md)

##Changelog

[**Changelog**](ue-插件-AIChatPlus-ChangeLogs.md)

##Technical Support

**Comment**: Feel free to leave any questions in the comment section below.

**Email**: You can also send me an email at disenonec@gmail.com

**discord**: Coming soon

--8<-- "footer_en.md"


> This post was translated using ChatGPT. Please provide feedback at [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions therein. 
