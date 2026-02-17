---
layout: post
title: Changelog
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
description: Changelog
---

<meta property="og:title" content="UE 插件 AIChatPlus 版本日志" />

#UE Plugin AIChatPlus Version Log

## v2.0.0 - 2026.02.14

* **Multi-Platform Support for Tool Calling**: Added tool calling/function calling capabilities for five major platforms: OpenAI, Claude, Gemini, Ollama, and CllamaServer.
* **Cllama Server Integration**: Full support for local llama.cpp Server, including creation, management, and Speech-to-Text capabilities, with a visual management interface provided by the editor.
* **JSON Blueprint Library**: Added JsonObject/JsonArray blueprint operation classes, supporting JSON and USTRUCT interconversion.
* **OpenAI Audio**: Supports OpenAI audio input and output, allowing editors to preview audio responses.

## v1.8.0 - 2025.11.03

* Updated llama.cpp to b6792

## v1.7.0 - 2025.07.06

* Updated llama.cpp to b5536

* Supports UE5.6

* Android release shipping crashes, disable llama.cpp

## v1.6.2 - 2025.03.17

###New Feature

* Cllama adds the KeepContext parameter, defaulting to false, where Context is automatically destroyed after Chat ends

* Cllama adds KeepAlive parameter to reduce repeated model loading

## v1.6.1 - 2025.03.07

### Bug Fix

* The OpenAI Image Chat Blueprint supports image input.

* Editor Tool Cllama mmproj model allows empty

## v1.6.0 - 2025.03.02

###New Feature

* llama.cpp upgraded to version b4604

* Cllama supports GPU backends: cuda and metal

* Chat tool Cllama supports GPU usage

* Supports reading model files packaged in Pak archives

### Bug Fix

* Fixed an issue where Cllama would crash when reloading during inference.

* Fixed iOS compilation errors

## v1.5.1 - 2025.01.30

###New Features

* Only allow Gemini to send audio

* Optimize the method of obtaining PCMData by decompressing audio data only when generating Base64

* Request adding two callbacks: OnMessageFinished and OnImagesFinished.

* Optimize the Gemini Method to automatically retrieve methods based on bStream.

* Add some blueprint functions to facilitate the conversion from Wrapper to actual types, and to retrieve Response Message and Error.

### Bug Fix

* Fixed the issue of multiple calls to Request Finish

## v1.5.0 - 2025.01.29

###New Features

* Supports sending audio messages to Gemini

* The editor tool supports sending audio and recordings.

### Bug Fix

* Fixed the bug where Session copy failed

## v1.4.1 - 2025.01.04

###Bug fixes

* Chat tools support sending images without accompanying messages.

* Fixed the issue with images failing to send via the OpenAI API

* Fixed the issue where the OpenAI and Azure chat tools settings missed the parameters Quality, Style, and ApiVersion.

## v1.4.0 - 2024.12.30

###New Features

*(Experimental feature) Cllama (llama.cpp) supports multimodal models capable of handling images.*

* Detailed hints have been added to all blueprint parameter types.

## v1.3.4 - 2024.12.05

###New Feature

* OpenAI supports vision API

###Bug fixes

* Fixed the issue with OpenAI when stream=false

## v1.3.3 - 2024.11.25

###New Features

* Supports UE-5.5

###Bug fixes

* Fixed an issue where some blueprints were not taking effect

## v1.3.2 - 2024.10.10

###Bug fixes

* Fixed a crash in cllama when manually stopping requests

* Fixed issue where the Win-packaged download version from the store couldn't locate ggml.dll and llama.dll files.

* Check if in GameThread when creating a request, CreateRequest check in game thread

## v1.3.1 - 2024.9.30

###New Features

* Add a SystemTemplateViewer to browse and utilize hundreds of system configuration templates

###Bug Fixes

* Fixed issue where llama.cpp couldn't find the linked library for plugins downloaded from the store

* Fixed the issue of excessively long paths in LLAMACpp

* Fixed an error with the llama.dll link after Windows packaging

* Fixed file path reading issues on iOS/Android

* Fixed the incorrect name setting in Cllame

## v1.3.0 - 2024.9.23

###Major New Features

* Integrated llama.cpp to support local offline execution of large models

## v1.2.0 - 2024.08.20

###New features

* Support OpenAI Image Edit/Image Variation

* Supports Ollama API, automatically retrieves the list of models supported by Ollama

## v1.1.0 - 2024.08.07

###New Features

* Blueprint Support

## v1.0.0 - 2024.08.05

###New Feature

* Basic complete functionality

* Supports OpenAI, Azure, Claude, Gemini

* Built-in fully-featured chat tool with editor functionality

--8<-- "footer_en.md"


> This post was translated using ChatGPT. Please provide feedback **[here](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions herein. 
