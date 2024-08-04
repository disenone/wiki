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

##Public repository

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtain Plug-in

[AIChatPlus]()

##Introduction to the plugin

This plugin supports UE5.2+.

UE.AIChatPlus is a plugin for UnrealEngine that enables communication with various GPT AI chat services. Currently supported services include OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, and Google Gemini. In the future, more service providers will be supported. Its implementation is based on asynchronous REST requests, resulting in high performance, making it convenient for UE developers to integrate these AI chat services.

UE.AIChatPlus also includes an editor tool that allows you to directly use these AI chat services in the editor to generate text and images, analyze images, and more.

##Instructions for Use

###Editor chat tool

Menu bar Tools -> AIChatPlus -> AIChat can open the chat tool editor provided by the plugin

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chatting, image generation, and image analysis.

The interface of the tool is roughly as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main functions

Text Chat: Click on the `New Chat` button in the bottom left corner to create a new text chat session.

Image Generation: Click the `New Image Chat` button in the bottom left corner to start a new image generation session.

Image Analysis: Some chat services in `New Chat` support sending images, such as Claude and Google Gemini. You can simply click on the 🖼️ or 🎨 button above the input box to upload the image you want to send.

Set the current chat character: The dropdown box at the top of the chat box can set the current role for sending text, allowing you to adjust the AI chat by simulating different characters.

Clear chat: The ❌ button at the top of the chat box can clear the history of the current conversation.

Global Settings: Click on the `Setting` button in the bottom left corner to open the global settings window. You can configure default text chat, image generation API services, and specify parameters for each API service. The settings will be automatically saved in the project path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Conversation Settings: Click the settings button at the top of the chat box to open the settings window for the current conversation. You can modify the conversation name, the API service used for the conversation, and customize specific parameters for each conversation. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Chat Content Editing: When hovering over a chat message, a settings button for that specific message will appear, allowing for options such as regenerating, editing, copying, or deleting the content. Additionally, there is an option to regenerate the content below (for messages from user roles).

* Image browsing: For image generation, clicking on an image will open the image viewing window (ImageViewer), supporting saving images as PNG/UE Texture. Textures can be viewed directly in the Content Browser, facilitating image usage within the editor. Additionally, it supports functions such as deleting images, regenerating images, and generating more images. For editors on Windows, it also supports copying images, allowing images to be copied to the clipboard for easy use. Images generated during a session are automatically saved under each session folder, typically located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

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

AIChatPlusCommon is responsible for handling sending requests and parsing reply contents; AIChatPlusEditor is responsible for implementing an AI chat tool editor.

The UClass responsible for sending requests is FAIChatPlus_xxxChatRequest. Each API service has its own independent Request UClass. The replies to the requests are obtained through two UClass: UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase. You only need to register the corresponding callback delegate.

Before sending a request, you need to set up the API parameters and the message to be sent. This is done by setting up the FAIChatPlus_xxxChatRequestBody. The specific response content is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving a callback, you can use a specific interface to retrieve the ResponseBody.

More source code details can be obtained from the UE Marketplace: [AIChatPlus]()


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
