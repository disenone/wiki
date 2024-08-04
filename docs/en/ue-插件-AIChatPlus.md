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

##Plugin acquisition

[AIChatPlus]()

##Introduction to the plugin

This plugin supports UE5.2+.

UE.AIChatPlus is a UnrealEngine plugin that enables communication with various GPT AI chat services. Currently supported services include OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, and Google Gemini. More service providers will be supported in the future. Its implementation is based on asynchronous REST requests, offering high performance and making it convenient for Unreal Engine developers to integrate these AI chat services.

The UE.AIChatPlus also includes an editor tool, which allows you to directly use these AI chat services in the editor to generate text and images, analyze images, and so on.

##Instructions for use

###Editor chat tools

Menu bar: Tools -> AIChatPlus -> AIChat can open the editor chat tool provided by the plugin

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chatting, image generation, and image analysis.

The interface of the tool is roughly as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

The main functions include:

Text Chat: Click the `New Chat` button in the bottom left corner to start a new text chat session.

Image Generation: Click on the `New Image Chat` button in the bottom left corner to start a new image generation session.

Image Analysis: Some chat services in `New Chat` support sending images, such as Claude and Google Gemini. Click the 🖼️ or 🎨 button above the input box to load the image you want to send.

Set the current chat role: The drop-down box at the top of the chat box can be used to set the current role for sending text, allowing you to simulate different roles to adjust the AI chat.

Clear conversation: The ❌ button at the top of the chat box can clear the history of the current conversation.

Global Settings: Click on the `Setting` button in the bottom left corner to open the global settings window. You can configure default text chat, image generation API services, and specify parameters for each API service. The settings will be automatically saved in the project path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversation settings: Click the settings button at the top of the chat box to open the settings window for the current conversation. Support modifying the conversation name, changing the API service used in the conversation, and independently setting specific parameters for each conversation's API usage. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Edit Chat Message: When hovering over a chat message, a settings button for that specific message will appear, allowing you to regenerate, edit, copy, or delete the message, as well as regenerate it below (for messages from user roles).

* Image browsing: For image generation, clicking on the image will open the image viewing window (ImageViewer), supporting saving images as PNG/UE Texture. Textures can be viewed directly in the Content Browser, making it convenient to use images within the editor. Additionally, functions such as deleting images, regenerating images, and continuing to generate more images are supported. For editors on Windows, image copying is also supported, allowing images to be directly copied to the clipboard for easy use. Images generated during sessions will automatically be saved under each session folder, typically located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Global Settings:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Conversation settings:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Edit chat content:
![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Image Viewer:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

###Introduction to Core Code

Currently, the plugin is divided into two modules: AIChatPlusCommon (Runtime) and AIChatPlusEditor (Editor).

AIChatPlusCommon is responsible for handling sending requests and parsing reply content; AIChatPlusEditor is responsible for implementing an editor AI chat tool.

The UClass responsible for sending requests is FAIChatPlus_xxxChatRequest. Each API service has its own independent Request UClass. The replies to the requests are received through two UAIChatPlus_ClassHandlerBase / UAIChatPlus_ImageHandlerBase UClass, it is only necessary to register the corresponding callback delegate.

Before sending a request, you need to set the parameters of the API and the message to be sent. This is done by setting FAIChatPlus_xxxChatRequestBody. The specific content of the response is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving a callback, you can obtain the ResponseBody through a specific interface.

More details of the source code can be obtained at the UE Marketplace: [AIChatPlus]()


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
