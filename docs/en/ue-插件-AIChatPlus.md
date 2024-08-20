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
description: UE Plugin AIChatPlus documentation
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE Plugin AIChatPlus Documentation

##Public warehouse

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Get plugin

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introduction to the Plugin

This plugin supports UE5.2+.

UE.AIChatPlus is a UnrealEngine plugin that enables communication with various GPT AI chat services. Currently supported services include OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, and Google Gemini. In the future, it will continue to support more service providers. Its implementation is based on asynchronous REST requests, ensuring high performance and making it convenient for UE developers to integrate these AI chat services.

UE.AIChatPlus also includes an editor tool that allows users to directly utilize these AI chat services in the editor to generate text and images, analyze images, and more.

##Instructions for use

###Editor chat tool

Menu bar: Tools -> AIChatPlus -> AIChat can open the editor chat tool provided by the plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chat, image generation, and image analysis.

The interface of the tool is roughly as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main Functions

Text Chat: Click the `New Chat` button in the bottom left corner to start a new text chat session.

Image Generation: Click on the `New Image Chat` button in the bottom left corner to start a new image generation session.

Image analysis: Some chat services of `New Chat` support sending images, such as Claude and Google Gemini. Simply click the 🖼️ or 🎨 button above the input box to load the image you want to send.

Support Blueprint: support Blueprint to create API requests, complete text chat, image generation, and other functions.

Set the current chat character: The dropdown box above the chat box can be used to set the current character for sending text, allowing you to simulate different characters to adjust AI chatting.

Clear chat: Clicking on the ❌ icon above the chat box clears the history of messages in the current conversation.

Global Settings: Click on the `Setting` button in the lower left corner to open the global settings window. You can configure default text chat, image generation API services, and specify parameters for each API service. The settings will be automatically saved in the project's directory `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversation Settings: Click on the settings button above the chat box to open the settings window for the current conversation. You can change the conversation name, modify the API service used for the conversation, and individually adjust specific parameters for each conversation's API. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Modify chat content: When hovering over the chat content, a settings button for that particular chat content will appear, supporting options to regenerate, edit, copy, delete, and regenerate below (for user role content).

* Image Browsing: For image generation, clicking on an image will open the image viewing window (ImageViewer), supporting saving images as PNG/UE Texture. Textures can be viewed directly in the Content Browser, making it convenient for images to be used within the editor. Additionally, it supports functions such as deleting images, regenerating images, and continuing to generate more images. For editors on Windows, copying images is also supported, allowing images to be copied directly to the clipboard for easy use. Images generated in the session are automatically saved in each session folder, typically located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Blueprint

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Global Settings:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Conversation settings:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Edit chat content:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Image Viewer:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

###Introduction to the core code

At present, the plugin is divided into two modules: AIChatPlusCommon (Runtime) and AIChatPlusEditor (Editor).

AIChatPlusCommon is responsible for handling sending requests and parsing reply content; AIChatPlusEditor is responsible for implementing an AI chat tool editor.

The UClass responsible for sending requests is FAIChatPlus_xxxChatRequest. Each API service has its own independent Request UClass. The replies to the requests are obtained through two UClass: UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase. You only need to register the corresponding callback delegate.

Before sending a request, you need to set up the parameters and the message to be sent for the API. This is done by setting up FAIChatPlus_xxxChatRequestBody. The specific content of the response is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving a callback, you can retrieve the ResponseBody through a specific interface.

More source code details can be obtained from the UE Marketplace: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)


###Release Notes

#### v1.2.0 - 2024.08.20

Support OpenAI Image Edit/Image Variation
Support Ollama API, support automatically getting the list of models supported by Ollama.

#### v1.1.0 - 2024.08.07

Support Blueprint

#### v1.0.0 - 2024.08.05

Complete basic functionality
Support OpenAI, Azure, Claude, Gemini
Built-in feature-rich editor chat tool

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
