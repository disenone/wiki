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

#UE plugin AIChatPlus version log.

## v1.6.2 - 2025.03.17

###New feature

Increase the KeepContext parameter to "true" by default in Cllama. Context will be automatically destroyed after the Chat ends.

Cllama has added the KeepAlive parameter, which can reduce redundancy in model re-reading.

## v1.6.1 - 2025.03.07

### Bug Fix

OpenAI Image Chat blueprint supports input images.

The Editor Tool Cllama mmproj model allows empty.

## v1.6.0 - 2025.03.02

###New Feature

Upgrade llama.cpp to version b4604.

Cllama supports GPU backends: cuda and metal.

The chat tool Cllama supports the use of GPU.

Support reading model files packaged in Pak.

### Bug Fix

Fix the issue where Cllama crashes when reloading during reasoning.

Fix iOS compilation error.

## v1.5.1 - 2025.01.30

###New feature

Only Gemini is allowed to send audio messages.

Optimize the method of obtaining PCMData, decompress the audio data when generating B64.

Please add two callbacks: OnMessageFinished and OnImagesFinished.

Optimize the Gemini Method to automatically retrieve Method based on bStream.

Add some blueprint functions to facilitate converting the Wrapper to actual types, and extracting the Response Message and Error.

### Bug Fix

Fix the issue of multiple Request Finish calls.

## v1.5.0 - 2025.01.29

###New feature

Support audio for Gemini.

The editor tool supports sending audio and recordings.

### Bug Fix

Fix the bug causing the failure in copying sessions.

## v1.4.1 - 2025.01.04

###Problem fixing

The chat tool supports sending only pictures without text messages.

Fix the failed image sending issue of the OpenAI interface.

Fix the issue of missing parameters Quality, Style, and ApiVersion in the OpanAI and Azure chat tool settings.

## v1.4.0 - 2024.12.30

###New feature

*(Experimental feature) Cllama (llama.cpp) supports multimodal models and can handle images.

All blueprint type parameters have been provided with detailed instructions.

## v1.3.4 - 2024.12.05

###New Feature

OpenAI supports vision API.

###Problem fixed

Fix the error when OpenAI stream=false.

## v1.3.3 - 2024.11.25

###New feature

Support UE-5.5

###Problem fixed

Fix the issue of some blueprints not taking effect.

## v1.3.2 - 2024.10.10

###Problem Fix

Fix the crash when cllama crashes when manually stopping the request.

Fix the issue of not being able to find the ggml.dll and llama.dll files when packaging the Win version of the store download.

Verify whether the request is made in the GameThread when creating it.

## v1.3.1 - 2024.9.30

###New Feature

Add a SystemTemplateViewer that allows users to view and utilize hundreds of system setting templates.

###Problem fixing

Fix the plugin downloaded from the store, llama.cpp cannot find the link library.

Fix the issue of LLAMACpp path being too long.

Fixing the llama.dll error in the Windows bundle after packaging.

Fix the issue of reading file paths on iOS/Android

Fix Cllame setting name error

## v1.3.0 - 2024.9.23

###Significant new feature

Integrated llama.cpp, supporting local offline execution of large models.

## v1.2.0 - 2024.08.20

###New feature

Support OpenAI Image Edit/Image Variation.

Support Ollama API, support automatically obtaining the list of models supported by Ollama.

## v1.1.0 - 2024.08.07

###New feature

Support blueprint.

## v1.0.0 - 2024.08.05

###New feature

Complete Basic Functions

Support OpenAI, Azure, Claude, and Gemini.

Comes with a well-equipped chat tool editor.

--8<-- "footer_en.md"


> This post has been translated using ChatGPT. Please provide some [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
