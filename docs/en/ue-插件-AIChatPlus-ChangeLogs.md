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
description: Release Notes
---

<meta property="og:title" content="UE 插件 AIChatPlus 版本日志" />

#UE plugin AIChatPlus version log

## v1.6.0 - 2025.03.02

###New feature.

Upgrade llama.cpp to version b4604

Cllama supports GPU backends: cuda and metal.

The chat tool Cllama supports the use of GPU.

Support reading model files packaged in Pak.

### Bug Fix

Fix the issue of Cllama crashing when reloading during reasoning.

Fix iOS compilation errors.

## v1.5.1 - 2025.01.30

###New feature

Only Gemini is allowed to send audio messages.

Optimize the method for obtaining PCMData, decompress the audio data when generating B64.

Add two callbacks: OnMessageFinished and OnImagesFinished to the request.

Optimize the Gemini Method to automatically fetch the Method based on bStream.

Add some blueprint functions to facilitate converting a Wrapper to the actual type, and fetching Response Message and Error.

### Bug Fix

Fix the issue of multiple calls to Request Finish.

## v1.5.0 - 2025.01.29

###New feature

Support sending audio to Gemini.

The editor tool supports sending audio and recordings.

### Bug Fix

Fix the bug causing Session copy to fail.

## v1.4.1 - 2025.01.04

###Problem fixing

The chat tool supports sending only images without messages.

Repair the failed image sending issue of the OpenAI interface.

Fix the issue of missing parameters Quality, Style, and ApiVersion in the settings of OpenAI and Azure chat tools.

## v1.4.0 - 2024.12.30

###New Feature

*(Experimental feature) Cllama(llama.cpp) supports multi-modal models and can handle images.*

All blueprint types parameters have been added with detailed prompts.

## v1.3.4 - 2024.12.05

###New feature.

OpenAI supports Vision API.

###Problem resolved

Fix the error when OpenAI stream=false.

## v1.3.3 - 2024.11.25

###New Feature.

Support UE-5.5

###Problem fixing

Fixing the issue of some blueprints not taking effect.

## v1.3.2 - 2024.10.10

###Troubleshooting

Fix the crash caused by cllama when manually stopping the request.

Fix the issue of not finding the ggml.dll and llama.dll files when packaging the win version for downloading in the shop.

Check if being called in the GameThread when creating a request.

## v1.3.1 - 2024.9.30

###New Feature

Add a SystemTemplateViewer to allow users to view and utilize hundreds of system setting templates.

###Issue fix

Fix the plugin downloaded from the store, llama.cpp cannot find the link library.

Fix LLAMACpp long path issue

Fixing the llama.dll error in Windows after packaging.

Fix ios/android file path reading issue

Fix Cllame settings name error

## v1.3.0 - 2024.9.23

###Major new feature

Integrated llama.cpp to support offline execution of large models locally.

## v1.2.0 - 2024.08.20

###New feature

Support OpenAI Image Edit/Image Variation.

Support Ollama API, support automatically obtaining the list of models supported by Ollama.

## v1.1.0 - 2024.08.07

###New feature

Support Blueprint

## v1.0.0 - 2024.08.05

###New feature

Complete basic functionality

Support OpenAI, Azure, Claude, Gemini.

Built-in feature-rich chat tool editor.

--8<-- "footer_en.md"


> This post was translated using ChatGPT. Please provide feedback in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
