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
description: UE plugin AIChatPlus documentation
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE Plugin AIChatPlus Documentation

##Public repository

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Plugin acquisition

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introduction to the plugin

This plugin supports UE5.2+.

UE.AIChatPlus is a UnrealEngine plugin that enables communication with various GPT AI chat services. Currently supported services include OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and local offline llama.cpp. In the future, more service providers will be supported. Its implementation is based on asynchronous REST requests, ensuring high efficiency performance, making it convenient for UE developers to integrate these AI chat services.

At the same time, UE.AIChatPlus also includes an editor tool that allows you to use these AI chat services directly in the editor to generate text and images, analyze images, and more.

##Instructions for use

###Editor Chat Tool

Menu bar Tools -> AIChatPlus -> AIChat can open the editing chat tool provided by the plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chatting, image generation, and image analysis.

The interface of the tool is roughly as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main Functions

Offline Large Models: Integrated llama.cpp library, supporting local offline execution of large models.

Text Chat: Click the `New Chat` button in the bottom left corner to start a new text chat session.

Image Generation: Click the `New Image Chat` button in the bottom left corner to start a new image generation session.

Image Analysis: Some chat services in `New Chat` support sending images, such as Claude and Google Gemini. You can click on the 🖼️ or 🎨 button above the input box to upload the image you want to send.

Support Blueprint: Support Blueprint to create API requests, complete text chat, image generation, and other functions.

Set the current chat role: The dropdown box above the chat box can set the current character for sending text, allowing you to adjust AI chat by simulating different characters.

Clear chat: Clicking on the ❌ icon at the top of the chat box will clear the history of the current session.

**Global Settings**: Click on the `Setting` button in the bottom left corner to open the global settings window. You can adjust default text chat, image generation API services, and configure specific parameters for each API service. The settings will be automatically saved in the project's path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversation Settings: Click the settings button above the chat box to open the settings window for the current conversation. You can modify the conversation name, change the API service used for the conversation, and independently set specific parameters for each session's API usage. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Modify chat content: Hover over the chat content, a settings button will appear for that specific chat content, supporting options like regenerating content, modifying content, copying content, deleting content, and regenerating content below (for content owned by the user role).

* Image Browsing: For image generation, clicking on the image will open the image viewing window (ImageViewer), supporting saving the image as PNG/UE Texture. Textures can be directly viewed in the Content Browser, making it convenient to use images within the editor. Additionally, it supports functions such as deleting images, regenerating images, and generating more images. For editors on Windows, there is also support for copying images, allowing you to copy images directly to the clipboard for easy use. The images generated during the session will be automatically saved in each session folder, usually located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Blueprint:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Global settings:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Conversation settings:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Edit chat content:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Image Viewer:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

###Introduction to the core code

Currently, the plugin is divided into the following modules:

*AIChatPlusCommon: Runtime module, responsible for handling various AI API interface requests and parsing response content.*

* AIChatPlusEditor: Editor module, responsible for implementing the AI chat tool within the editor.

AIChatPlusCllama: Runtime module responsible for encapsulating the interface and parameters of llama.cpp to achieve offline execution of large models

* Thirdparty/LLAMACpp: Third-party module at runtime, integrating dynamic library and header files of llama.cpp.

The UClass responsible for sending requests is FAIChatPlus_xxxChatRequest specifically. Each API service has its own independent Request UClass. The replies to the requests are obtained through two types of UClass, UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase, and only require registering the corresponding callback delegate.

Before sending a request, you need to set the parameters and the message to be sent for the API. This part is set using FAIChatPlus_xxxChatRequestBody. The specific response content is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving a callback, you can obtain the ResponseBody through a specific interface.

More source code details can be obtained on the UE marketplace: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)


###Release Notes

### v1.3.0 - 2024.9.23

Major Update

Integrated llama.cpp to support local offline execution of large models.

#### v1.2.0 - 2024.08.20

Support OpenAI Image Edit/Image Variation

Support the Ollama API, support automatically obtaining the list of models supported by Ollama

#### v1.1.0 - 2024.08.07

Support blueprint

#### v1.0.0 - 2024.08.05

Complete basic functionality

Support OpenAI, Azure, Claude, Gemini

Integrated feature-rich editor chat tool

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
