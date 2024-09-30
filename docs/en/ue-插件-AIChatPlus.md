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
description: UE Plugin AIChatPlus Documentation
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE Plugin AIChatPlus Documentation

##Public Repository

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtain Plugin

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introduction to the Plugin

This plugin supports UE5.2+.

UE.AIChatPlus is a plugin for Unreal Engine that enables communication with various GPT AI chat services. Currently, it supports services such as OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and local offline llama.cpp. In the future, it will continue to support more service providers. Its implementation is based on asynchronous REST requests, ensuring high efficiency and making it convenient for UE developers to integrate these AI chat services.

At the same time, UE.AIChatPlus also includes an editor tool that allows you to use these AI chat services directly in the editor to generate text and images, analyze images, and more.

##Instructions for use

###Editor Chat Tool

Menu bar Tools -> AIChatPlus -> AIChat can open the editor chat tool provided by the plugin

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chatting, image generation, and image analysis.

The interface of the tool is roughly as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main Functions

Offline Large Model: Integrated llama.cpp library, supporting local offline execution of large models

Text chat: Click on the `New Chat` button in the bottom left corner to start a new text chat session.

Image Generation: Click the `New Image Chat` button in the lower left corner to create a new image generation session.

Image Analysis: Some chat services in `New Chat` support sending images, such as Claude, Google Gemini. You can simply click the 🖼️ or 🎨 button above the input box to load the image you want to send.

Support Blueprint: Support blueprint to create API requests, complete text chatting, image generation, and other functions.

Set the current chat character: The dropdown menu above the chat box allows you to select the current character for sending text. You can simulate different characters to adjust AI chat.

Clear Chat: Clicking the ❌ button at the top of the chat box can clear the history of the current conversation.

Global Settings: Click the `Setting` button in the lower left corner to open the global settings window. You can configure default text chat, image generation API services, and specify parameters for each API service. The settings will be automatically saved in the project directory `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversation Settings: Click on the settings button above the chat box to open the settings window for the current conversation. You can modify the conversation name, change the API service used in the conversation, and independently adjust specific parameters for each session's API. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Edit Chat Content: When hovering over a chat message, a settings button for that message will appear. It supports options like regenerating content, editing, copying, deleting, and regenerating content below (for messages from user role).

* Image browsing: For image generation, clicking on an image will open the image viewer window (ImageViewer), supporting saving images as PNG/UE Texture. Textures can be viewed directly in the Content Browser, making it convenient to use images within the editor. Additionally, there is support for deleting images, regenerating images, and continuing to generate more images. For the editor on Windows, there is also the option to copy images, allowing them to be copied directly to the clipboard for easy use. Images generated during a session will also be automatically saved in each session folder, usually located at ` $(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Blueprint:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Global Settings:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Conversation settings:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Edit Chat Content:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Image Viewer:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

###Introduction to Core Code

The plugins are currently divided into the following modules:

AIChatPlusCommon: Runtime module, responsible for processing various AI API interface requests and parsing reply content.

* AIChatPlusEditor: Editor module, responsible for implementing the AI chat tool editor.

* AIChatPlusCllama: Runtime module responsible for encapsulating the interface and parameters of llama.cpp to achieve offline execution of large models

Thirdparty/LLAMACpp: Third-party module at runtime, integrating llama.cpp dynamic library and header files.

The specific UClass responsible for sending requests is FAIChatPlus_xxxChatRequest. Each API service has its own independent Request UClass. The replies to the requests are obtained through two types of UClass: UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase. You only need to register the corresponding callback delegate.

Before sending a request, you need to set the parameters and messages for the API. This is done by setting up the FAIChatPlus_xxxChatRequestBody. The specific response content is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving a callback, you can retrieve the ResponseBody through a specific interface.

More source code details can be found on UE Marketplace: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)


###Release Notes

#### v1.3.0 - 2024.9.23

Heavy update

Integrated llama.cpp, supporting local offline execution of large models.

#### v1.2.0 - 2024.08.20

Support OpenAI Image Edit/Image Variation.

Support Ollama API, support automatically fetching the list of models supported by Ollama.

#### v1.1.0 - 2024.08.07

Support blueprint.

#### v1.0.0 - 2024.08.05

Complete basic functionality

Support OpenAI, Azure, Claude, Gemini

Built-in feature-rich chat tool editor

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
