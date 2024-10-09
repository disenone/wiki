---
layout: post
title: UE Plugin AIChatPlus Documentation
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
description: UE Plugin AIChatPlus User Manual
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE Plugin AIChatPlus Documentation

##Public repository

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Get plugin

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introduction to the Plugin

This plugin supports UE5.2+.

UE.AIChatPlus is a plugin for UnrealEngine that enables communication with various GPT AI chat services. Currently supported services include OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and local offline llama.cpp. In the future, more service providers will be supported. Its implementation is based on asynchronous REST requests, ensuring high performance and making it convenient for Unreal Engine developers to integrate these AI chat services.

At the same time, UE.AIChatPlus also includes an editor tool, which allows you to directly use these AI chat services in the editor, generating text and images, analyzing images, and more.

##Instructions for use

###Editor chat tool

Menu bar Tools -> AIChatPlus -> AIChat can open the editor chat tool provided by the plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chat, image generation, and image analysis.

The interface of the tool is roughly as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main Features

Offline Large-scale Models: Integrated llama.cpp library, supporting local offline execution of large models

* Text chat: Click on the `New Chat` button in the bottom left corner to start a new text chat session.

Image generation: Click the `New Image Chat` button in the bottom left corner to start a new image generation session.

Image Analysis: Some chat services of `New Chat` support sending images, such as Claude and Google Gemini. You can simply click the 🖼️ or 🎨 button above the input box to upload the image you want to send.

Support Blueprint: Support blueprint creation API requests, complete text chat, image generation, and other functions.

Set the current chat character: The dropdown box at the top of the chat box can be used to set the current character for sending text, allowing you to adjust AI chat by simulating different characters.

Clear Chat: Clicking on the ❌ icon at the top of the chat box can clear the history messages of the current conversation.

Dialogue template: Built-in hundreds of dialogue setting templates, making it easy to handle common issues.

Global Settings: Click on the `Setting` button in the bottom left corner to open the global settings window. You can configure default text chat, image generation API services, and specify parameters for each API service. The settings will be automatically saved in the project's path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversation Settings: Click on the settings button at the top of the chat box to open the settings window for the current conversation. You can modify the conversation name, change the API service used for the conversation, and independently set specific parameters for each conversation's API. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Edit Chat Content: When hovering over the chat content, a settings button for that specific chat content will appear. It supports options like regenerating content, editing content, copying content, deleting content, and regenerating content below (for content created by user roles).

* Image Browser: For image generation, clicking on an image will open the image viewing window (ImageViewer), supporting saving images as PNG/UE Texture. Textures can be viewed directly in the Content Browser, making it convenient to use images within the editor. Additionally, it supports functions such as deleting images, regenerating images, and generating more images. For editors on Windows, it also supports copying images, allowing them to be copied directly to the clipboard for easy use. Images generated during sessions will automatically be saved in each session folder, typically located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Blueprint:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Global Settings:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Conversation Settings:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Edit chat content:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Image Viewer:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Use offline large models

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Dialogue template

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introduction to the core code

Currently, the plugin is divided into the following modules:

AIChatPlusCommon: Runtime module, responsible for processing various AI API interface requests and parsing response content.

AIChatPlusEditor: Editor module, responsible for implementing the AI chat tool editor.

* AIChatPlusCllama: Runtime module responsible for encapsulating the interface and parameters of llama.cpp, implementing offline execution of large models

* Thirdparty/LLAMACpp: A third-party runtime module that integrates the dynamic library and header files of llama.cpp.

The UClass responsible for sending requests specifically is FAIChatPlus_xxxChatRequest. Each API service has its own independent Request UClass. The responses to the requests are obtained through two types of UClass: UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase. It is only necessary to register the corresponding callback delegate.

Before sending a request, you need to set the parameters of the API and the message to be sent. This is done by setting up FAIChatPlus_xxxChatRequestBody. The specific response content is also parsed into FAIChatPlus_xxxChatResponseBody. When you receive a callback, you can obtain the ResponseBody through a specific interface.

More source code details can be obtained from the UE Marketplace: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)


###User Guide

####Use the editor tool in offline mode llama.cpp

The following describes how to use the offline model llama.cpp in the AIChatPlus editor tool.

First, download the offline model from the HuggingFace website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Put the model in a specific folder, for example, place it in the directory Content/LLAMA of the game project.

	```shell
	E:/UE/projects/FP_Test1/Content/LLAMA
	> ls
	qwen1.5-1_8b-chat-q8_0.gguf*
	```

Open the AIChatPlus editor tool: Tools -> AIChatPlus -> AIChat, create a new chat session, and open the session settings page.

	![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Set the Api to Cllama, enable Custom Api Settings, add model search paths, and select models

	![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Start chatting!!

	![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

####The code uses the offline model llama.cpp.

todo

####Use the offline model llama.cpp in the blueprint.

todo

###Release Notes

#### v1.3.1 - 2024.9.30

Add a SystemTemplateViewer that allows you to view and use hundreds of system setting templates.

##### Bugfix

Fix the plugin downloaded from the mall, llama.cpp cannot find the link library.
Fix the issue of LLAMACpp path being too long
Fix the "llama.dll" error in Windows packaging.
Fix iOS/Android file path reading issue
Fix Cllame setting name error

#### v1.3.0 - 2024.9.23

Heavy Update

Integrated llama.cpp, supporting local offline execution of large models.

#### v1.2.0 - 2024.08.20

Support OpenAI Image Edit/Image Variation.

Support Ollama API, support automatically fetching the list of models supported by Ollama.

#### v1.1.0 - 2024.08.07

Support blueprint

#### v1.0.0 - 2024.08.05

Complete basic functionality

Support OpenAI, Azure, Claude, Gemini

Built-in feature-rich editor chat tool

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
