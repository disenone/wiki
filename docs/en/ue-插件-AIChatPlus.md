---
layout: post
title: Document Explanation
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

##Public warehouse

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Plugin introduction

The latest version is v1.6.0.

This plugin supports UE5.2 - UE5.5.

UE.AIChatPlus is a UnrealEngine plugin that enables communication with various GPT AI chat services. Currently supported services include OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and local offline llama.cpp. Future updates will continue to add support for more service providers. Its implementation is based on asynchronous REST requests, ensuring high efficiency performance, making it convenient for Unreal Engine developers to integrate these AI chat services.

Furthermore, UE.AIChatPlus also includes an editor tool that allows you to directly utilize these AI chat services within the editor, generating text and images, analyzing images, and more.

##Primary functions

**Brand new!** Offline AI llama.cpp upgraded to version b4604.

**Brand new!** Offline AI llama.cpp now supports GPU Cuda and Metal.

**Brand new!** Supports Gemini voice-to-text.

**API**: Support OpenAI, Azure OpenAI, Claude, Gemini, Ollama, llama.cpp, DeepSeek.

**Offline Real-time API**: Support offline execution of AI in llama.cpp, compatible with GPU Cuda and Metal.

**Text translation**: Various APIs support text generation.

Text-to-Image: OpenAI DALL-E

**Image-to-Text**: OpenAI Vision, Claude, Gemini, Ollama, llama.cpp

**Image-to-Image**: OpenAI DALL-E

**Speech-to-Text**: Gemini

**Blueprint**: All APIs and features support blueprints.

**Editor Chat Tool**: An editor AI chat tool with rich features, carefully crafted.

Asynchronous calling: All APIs can be called asynchronously.

**Practical Tools**: Various image and audio tools.

##Supported APIs:

**Offline llama.cpp**: Integrated with the llama.cpp library, it can run AI models offline! It also supports multimodal models (experimental). Compatible with Win64/Mac/Android/IOS. Supports GPU CUDA and METAL.

**OpenAI**: /chat/completions, /completions, /images/generations, /images/edits, /images/variations

**Azure OpenAI**: /chat/completions, /images/generations

**Claude**: /messages, /complete

**Gemini**：generateText, generateContent, streamGenerateContent

**Ollama**: /api/chat, /api/generate, /api/tags

**DeepSeek**: /chat/completions

##Instructions for use

[**Instructions for Use - Blueprint Section**](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

[**User Manual - C++ Edition**](ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

[**Instructions for Use - Editor Section**](ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

##Change log

[**Change Log**](ue-插件-AIChatPlus-ChangeLogs.md)

##Technical support

**Comment**: Feel free to leave a message in the comment section below if you have any questions.

Email: You can also email me at disenonec@gmail.com.

**discord**: Coming soon

--8<-- "footer_en.md"


> This post has been translated using ChatGPT. Please provide feedback in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
