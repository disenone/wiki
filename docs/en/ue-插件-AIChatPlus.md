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

#UE Plugin AIChatPlus User Manual

##Plugin Marketplace

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##Public warehouse

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Plugin Introduction

The latest version is v1.6.0.

This plugin supports UE5.2 - UE5.5.

UE.AIChatPlus is a plugin for UnrealEngine that enables communication with various GPT AI chat services. Currently, it supports services such as OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and local offline support for llama.cpp. In the future, it will continue to expand support for more service providers. Its implementation is based on asynchronous REST requests, ensuring high efficiency performance and making it convenient for Unreal Engine developers to integrate these AI chat services.

UE.AIChatPlus also includes an editor tool, which allows users to directly utilize these AI chat services within the editor to generate text and images, analyze images, and more.

##Main functions

**Brand new!** Offline AI llama.cpp upgraded to version b4604.

**Brand new!** Offline AI llama.cpp supports GPU Cuda and Metal.

**Brand new!** Support for Gemini speech-to-text.

**API**: Supports OpenAI, Azure OpenAI, Claude, Gemini, Ollama, llama.cpp, DeepSeek.

Offline Real-time API: Supports running AI offline with llama.cpp, and is compatible with GPU Cuda and Metal.

**Text-to-Text**: Various APIs support text generation.

Image-to-Text: OpenAI Dall-E

**Convert Image to Text**: OpenAI Vision, Claude, Gemini, Ollama, llama.cpp

**Image to Image Transformation**: OpenAI DALL-E

**Speech to Text**: Gemini

**Blueprint**: All APIs and features are supported by blueprints. 

Editor Chat Tool: A feature-rich, meticulously crafted editor AI chat tool.

Asynchronous calling: All APIs can be called asynchronously.

**Practical Tools**: Various image and audio tools

##Supported API:

**Offline llama.cpp**: Integrated with the llama.cpp library, it enables offline execution of AI models! Also, it supports multi-modal models (experimental). Compatible with Win64/Mac/Android/IOS. Supports GPU CUDA and METAL.

OpenAI: /chat/completions, /completions, /images/generations, /images/edits, /images/variations

**Azure OpenAI**: /chat/completions, /images/generations

**Claude**: /messages, /complete

**Gemini**: :generateText, :generateContent, :streamGenerateContent

**Ollama**: /api/chat, /api/generate, /api/tags

**DeepSeek**：/chat/completions

##Instructions for use

[**Instructions for use - Blueprint section**](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

[**Instructions for Use - C++ Section**](ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

[User Manual - Editor Section](ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

[**Instructions - Packaging**](ue-插件-AIChatPlus-Usage-Package-GetStarted.md)

##Change Log

[**Change Log**](ue-插件-AIChatPlus-ChangeLogs.md)

##Technical support

**Comment**: Feel free to leave a message in the comment section below if you have any questions.

**Email**: You can also email me at disenonec@gmail.com

**discord**: Coming soon

--8<-- "footer_en.md"


> This post was translated using ChatGPT. Please leave your [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
