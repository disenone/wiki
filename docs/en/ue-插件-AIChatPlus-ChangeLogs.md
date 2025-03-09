---
layout: post
title: Version Log
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
description: Version Log
---

<meta property="og:title" content="UE 插件 AIChatPlus 版本日志" />

#UE Plugin AIChatPlus Version Log

## v1.6.1 - 2025.03.07

### Bug Fix

OpenAI Image Chat blueprint supports input images.

Editor Tool Cllama mmproj model allows empty.

## v1.6.0 - 2025.03.02

###New Feature

Upgrade llama.cpp to version b4604.

Cllama supports GPU backends: cuda and metal

The chat tool Cllama supports using GPU.

Support reading model files packed in Pak.

### Bug Fix

Fix the issue where Cllama crashes when reloading during deduction.

Fix iOS compilation error.

## v1.5.1 - 2025.01.30

###New Feature

Only Gemini is allowed to send voice messages.

Optimize the method for obtaining PCMData, decompress the audio data when generating B64.

Please add two callbacks: OnMessageFinished and OnImagesFinished.

Optimize the Gemini Method to automatically retrieve the Method based on bStream.

Add some blueprint functions to easily convert the Wrapper to actual types, and to retrieve the Response Message and Error.

### Bug Fix

Fix the issue of multiple calls to "Request Finish."

## v1.5.0 - 2025.01.29

###New Feature

Support sending audio to Gemini

The editor tool supports sending audio and recordings.

### Bug Fix

Fix the bug of session copy failure.

## v1.4.1 - 2025.01.04

###Problem fixed

Chat tool supports sending only pictures without text messages.

Repair OpenAI interface failed to send image document.

Fix the missing parameters Quality, Style, and ApiVersion settings in OpanAI and Azure chat tool configurations.

## v1.4.0 - 2024.12.30

###New feature

*(Experimental Feature) Cllama (llama.cpp) supports multimodal models and can handle images.*

All blueprint type parameters have been provided with detailed descriptions.

## v1.3.4 - 2024.12.05

###New feature

OpenAI supports the Vision API.

###Problem Fix

Fix the error when OpenAI stream=false.

## v1.3.3 - 2024.11.25

###New feature

Support UE-5.5.

###Issue resolution

Fix the issue where some blueprints are not working.

## v1.3.2 - 2024.10.10

###Problem fix.

Repair the crash when cllama collapses if you manually stop the request.

Fix the issue of not finding the ggml.dll and llama.dll files when packaging the win download version of the store.

Ensure to verify if in the GameThread when creating a request.

## v1.3.1 - 2024.9.30

###New feature

Add a SystemTemplateViewer that allows users to view and utilize hundreds of system setting templates.

###Problem Fix.

Fix the plugin downloaded from the app store, llama.cpp cannot find the link library.

Fix LLAMACpp path too long issue

Fix the llama.dll error in the Windows packaged build.

Fixing the file path reading issue on iOS/Android.

Fix Cllame setting name error.

## v1.3.0 - 2024.9.23

###Significant new features

Integrated llama.cpp, supporting local offline execution of large models.

## v1.2.0 - 2024.08.20

###New feature

Support OpenAI Image Edit/Image Variation.

Support Ollama API, support automatically obtaining the list of models supported by Ollama.

## v1.1.0 - 2024.08.07

###New Feature

Support Blueprint

## v1.0.0 - 2024.08.05

###New feature

Complete basic functionality.

Support OpenAI, Azure, Claude, Gemini

Built-in feature-rich editor chat tool.

--8<-- "footer_en.md"


> This post was translated using ChatGPT, please provide [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
