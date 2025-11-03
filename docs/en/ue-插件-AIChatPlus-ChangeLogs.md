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

#UE plugin AIChatPlus version log

## v1.8.0 - 2025.11.03

Upgrade llama.cpp to version b6792

## v1.7.0 - 2025.07.06

Upgrade llama.cpp to version b5536

Support UE5.6

The Android release is crashing during shipping, disable llama.cpp.

## v1.6.2 - 2025.03.17

###New feature

Cllama increases the KeepContext parameter by default to false, where the context is automatically destroyed after the chat ends.

Cllama increased the KeepAlive parameter to reduce redundant model reads.

## v1.6.1 - 2025.03.07

### Bug Fix

OpenAI Image Chat blueprint supports inputting images.

The Editor Tool Cllama mmproj model allows space.

## v1.6.0 - 2025.03.02

###New feature

Upgrade llama.cpp to version b4604.

Cllama supports GPU backends: cuda and metal.

The chat tool Cllama supports GPU utilization.

Support reading model files packaged in a Pak.

### Bug Fix

Fix the issue of Cllama crashing when reloading during reasoning.

Fix iOS compilation error

## v1.5.1 - 2025.01.30

###New feature.

Only Gemini is allowed to send voice messages.

Optimize the method for obtaining PCMData, decompress the audio data when generating B64.

* request to add two callbacks OnMessageFinished and OnImagesFinished

Optimize the Gemini Method to automatically retrieve the Method based on bStream.

Add some blueprint functions to facilitate the conversion of the Wrapper to actual types, as well as to retrieve Response Message and Error.

### Bug Fix

Fix the issue of multiple calls to "Request Finish."

## v1.5.0 - 2025.01.29

###New feature

Support sending audio to Gemini.

The editing tools support sending audio and recordings.

### Bug Fix

Fix the bug causing Session copy failure.

## v1.4.1 - 2025.01.04

###Problem solving

Chat tool supports sending only pictures without text messages.

Fix OpenAI interface failed to send image issue and document the picture.

Fix the issue where parameters Quality, Style, and ApiVersion were missing in OpanAI and Azure chat tool settings.

## v1.4.0 - 2024.12.30

###New features

*(Experimental feature) Cllama(llama.cpp) supports multi-modal models, capable of processing images.

All blueprint type parameters have been added with detailed hints.

## v1.3.4 - 2024.12.05

###New feature.

OpenAI supports Vision API.

###Problem fixed.

Fix the error when OpenAI stream=false.

## v1.3.3 - 2024.11.25

###New feature

Supports UE-5.5

###Problem resolved.

Fixing an issue where some blueprints were not working as intended.

## v1.3.2 - 2024.10.10

###Problem fixed

Repair the crash when cllama crashes during manual stop request.

Fix the issue of not finding the ggml.dll and llama.dll files when packaging the Win download version of the mall.

Verify whether the request is being created on the GameThread.

## v1.3.1 - 2024.9.30

###New feature

Add a SystemTemplateViewer for viewing and using hundreds of system setting templates.

###Problem resolution

Fix the plugin downloaded from the store. Llama.cpp cannot find the link library.

Fix LLAMACpp long path issue.

Fix the llama.dll error in the Windows package.

Fixing the file path reading issue on iOS/Android.

Fix Cllame setting name error

## v1.3.0 - 2024.9.23

###Significant new feature

Integrated llama.cpp, supporting local offline execution of large models.

## v1.2.0 - 2024.08.20

###New Feature

Support OpenAI Image Edit/Image Variation

Support Ollama API, support automatically obtaining the list of models supported by Ollama.

## v1.1.0 - 2024.08.07

###New Feature

Support blueprint

## v1.0.0 - 2024.08.05

###New Feature

Comprehensive foundational features

Support OpenAI, Azure, Claude, Gemini

Comes with a well-equipped editor chat tool.

--8<-- "footer_en.md"


> This post was translated using ChatGPT, please provide [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
