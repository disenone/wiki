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
description: UE Plugin AIChatPlus User Guide
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE Plugin AIChatPlus Documentation

##Public repository

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Plugin acquisition

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Plugin Introduction

This plugin supports UE5.2+.

UE.AIChatPlus is a plugin for UnrealEngine that enables communication with various GPT AI chat services. The supported services currently include OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini. In the future, it will continue to support more service providers. Its implementation is based on asynchronous REST requests, offering high performance and facilitating the integration of these AI chat services for UE developers.

At the same time, UE.AIChatPlus also includes an editor tool that allows direct use of these AI chat services in the editor to generate text and images, analyze images, and more.

##Instructions for Use

###Editor Chat Tool

Menu bar Tools -> AIChatPlus -> AIChat can open the editor chat tool provided by the plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chatting, image generation, and image analysis.

The interface of the tool is roughly:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main Functions

Text Chat: Click on the `New Chat` button in the bottom left corner to start a new text chat conversation. 

Image Generation: Click on the `New Image Chat` button in the bottom left corner to start a new image generation session.

Image analysis: Some chat services in "New Chat" support sending images, such as Claude, Google Gemini. You can click the 🖼️ or 🎨 button above the input box to load the image you want to send.

Support Blueprint: Support blueprint creation for API requests, text chat, image generation, and other functions.

Set the current chat character: The drop-down box at the top of the chat box can be used to set the current character for sending text, allowing you to adjust AI chat by simulating different characters.

Clear Chat: Clicking on the ❌ button on the top of the chat box can clear the history of the current conversation.

Global Settings: Click the `Setting` button in the bottom left corner to open the global settings window. You can set default text chat, image generation API services, and specific parameters for each API service. The settings will be automatically saved in the project path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversation Settings: Click on the settings button at the top of the chat box to open the settings window for the current conversation. You can change the conversation name, modify the API service used for the conversation, and specify specific parameters for each conversation's API independently. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Chat content editing: When hovering over the chat content, a setting button for that specific chat content will appear, supporting options such as regenerating content, modifying content, copying content, deleting content, and regenerating content below (for content from user roles).

* Image browser: For image generation, clicking on an image will open the image viewing window (ImageViewer), supporting saving images as PNG/UE Texture. Textures can be viewed directly in the Content Browser, making it easy to use images within the editor. Additionally, features include deleting images, regenerating images, and continuing to generate more images. For editors on Windows, image copying is also supported, allowing images to be copied directly to the clipboard for convenience. Images generated in a session will be automatically saved in each session folder, typically located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

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

###Introduction to core code

Currently, the plugin is divided into two modules: AIChatPlusCommon (Runtime) and AIChatPlusEditor (Editor).

AIChatPlusCommon is responsible for handling sending requests and parsing reply content; AIChatPlusEditor is responsible for implementing an editor AI chat tool.

The UClass responsible for sending requests is FAIChatPlus_xxxChatRequest, each API service has its own unique Request UClass. Replies to the requests are obtained through two UClass, UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase, and only require registering the corresponding callback delegate.

Before sending the request, you need to set the parameters of the API and the message to be sent. This is done by setting FAIChatPlus_xxxChatRequestBody. The specific content of the reply is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving the callback, you can retrieve the ResponseBody through a specific interface.

You can find more source code details on the UE marketplace: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)


###Change Log

#### v1.0.0 - 2024.08.07

Complete basic functions
Support OpenAI, Azure, Claude, Gemini
Support the blueprint.
Built-in feature-rich editor chat tool

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
