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
description: UE Plugin AIChatPlus Documentation
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE Plugin AIChatPlus Documentation

##Public warehouse

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtain plugin

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introduction to Plugin

This plugin supports UE5.2+.

UE.AIChatPlus is an UnrealEngine plugin that enables communication with various GPT AI chat services. It currently supports services from OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini. In the future, it will continue to support more service providers. Its implementation is based on asynchronous REST requests, ensuring high performance and facilitating UE developers to integrate these AI chat services.

At the same time, UE.AIChatPlus also includes an editor tool that allows users to directly utilize these AI chat services within the editor, generating text and images, analyzing images, and more.

##Instructions for use

###Editor chat tool

Menu Bar Tools -> AIChatPlus -> AIChat can open the editor chat tool provided by the plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chatting, image generation, and image analysis.

The interface of the tool is approximately:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main Functions

Text Chat: Click the `New Chat` button in the bottom left corner to start a new text chat session.

Image Generation: Click on the `New Image Chat` button in the bottom left corner to create a new image generation session.

Image Analysis: Some chat services in `New Chat` support sending images, such as Claude, Google Gemini. Click the 🖼️ or 🎨 button above the input box to load the image you want to send.

Support Blueprint: Support the creation of Blueprint API requests to enable functionalities such as text chatting and image generation.

Set the current chat character: The dropdown box above the chat box can set the current character for sending text, allowing you to adjust AI chat by simulating different characters.

Empty Chat: The ❌ button above the chat box can clear the history messages of the current session.

Global Settings: Click on the `Setting` button in the bottom left corner to open the global settings window. You can configure default text chat, image generation API services, and specify parameters for each API service. The settings will be automatically saved in the project path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversational Settings: Click the settings button above the chat box to open the current conversation's settings window. You can change the conversation name, the API service used for the conversation, and independently set specific parameters for each conversation's API. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Modify Chat Content: Hovering over the chat content will display a settings button for that specific content, supporting options to regenerate, edit, copy, delete, or regenerate below (for content authored by the user role).

* Image browsing: For image generation, clicking on an image will open the image viewing window (ImageViewer), supporting saving images as PNG/UE Texture. Textures can be viewed directly in the Content Browser for easy use of images within the editor. Additionally, it supports functions such as deleting images, regenerating images, and continuing to generate more images. For editors on Windows, copying images is also supported, allowing images to be copied directly to the clipboard for easy use. Images generated during a session will also be automatically saved in each session folder, typically located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Blueprint:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Global Settings:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Conversation settings:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Edit chat content:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Image Viewer:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

###Introduction to Core Code

At present, the plugin is divided into two modules: AIChatPlusCommon (Runtime) and AIChatPlusEditor (Editor) modules.

AIChatPlusCommon is responsible for handling sending requests and parsing reply content; AIChatPlusEditor is responsible for implementing an editor AI chat tool.

The UClass responsible for sending requests is FAIChatPlus_xxxChatRequest. Each API service has its own separate Request UClass. The response to the requests is obtained through two UClass, UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase. It is only necessary to register the corresponding callback delegate.

Before sending a request, you need to first set the parameters of the API and the message to be sent. This part is configured using FAIChatPlus_xxxChatRequestBody. The specific reply is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving a callback, you can retrieve the ResponseBody through a specific interface.

More source code details can be obtained at UE Marketplace: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)


###Changelog

#### v1.0.0

Complete basic functions
Support OpenAI, Azure, Claude, Gemini
Support blueprint.
Built-in feature-rich editor chat tool


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
