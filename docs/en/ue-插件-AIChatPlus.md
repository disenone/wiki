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
description: UE Plugin AIChatPlus User Manual
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE Plugin AIChatPlus Documentation

##Public warehouse

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtain Plugin

[AIChatPlus]()

##Introduction to the Plugin

This plugin supports UE5.2+.


UE.AIChatPlus is a plugin for Unreal Engine that enables communication with various GPT AI chat services. Currently, it supports services such as OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, and Google Gemini. In the future, it will continue to support more service providers. Its implementation is based on asynchronous REST requests, offering high performance and making it convenient for Unreal Engine developers to integrate these AI chat services.

At the same time, UE.AIChatPlus also includes an editor tool, which allows you to use these AI chat services directly in the editor to generate text and images, analyze images, and so on.

##Instructions for use

###Editor chat tool

Menu Bar Tools -> AIChatPlus -> AIChat can open the editor chat tool provided by the plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chat, image generation, and image analysis.

The interface of the tool is roughly as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

The main functions include:

Text Chat: Click the `New Chat` button in the bottom left corner to create a new text chat session.
Image Generation: Click the `New Image Chat` button in the bottom left corner to create a new image generation session.
Image Analysis: Some chat services within `New Chat` support image sending, such as Claude, Google Gemini. Simply click on the 🖼️ or 🎨 buttons above the input box to load the image you want to send.
Set the current chat character: The dropdown menu above the chat box can be used to select the current character for sending text, allowing you to adjust AI chat by simulating different characters.
Clear chat: The ❌ button above the chat box can be clicked to clear the history of the current chat session.
Global Settings: Click the `Setting` button in the bottom left corner to open the global settings window. You can configure default text chat, image generation API services, and specify parameters for each API service. The settings will be automatically saved in the project's path `$(ProjectFolder)/Saved/AIChatPlusEditor`.
Conversation Settings: Click the settings button at the top of the chat box to open the settings window for the current conversation. You can change the conversation name, modify the API service used for the conversation, and independently set specific parameters for each conversation's API usage. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.
Modification of Chat Content: When hovering over a chat message, a settings button will appear for that specific message. It supports options such as regenerating content, editing content, copying content, deleting content, and regenerating content below (for user-generated messages).
* Image browsing: For image generation, clicking on an image will open the Image Viewer window, supporting saving images as PNG/UE Texture. Textures can be viewed directly in the Content Browser, facilitating their use within the editor. Additionally, it supports functions like deleting images, regenerating images, and generating more images. For editors on Windows, it also supports copying images, allowing them to be copied directly to the clipboard for easy usage. Images generated during a session will also be automatically saved in each session folder, typically located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Global Settings:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Conversation settings:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Edit chat content:
![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Image Viewer:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

###Introduction to Core Code

The plugins are currently divided into two modules: AIChatPlusCommon (Runtime) and AIChatPlusEditor (Editor).

AIChatPlusCommon is responsible for handling sending requests and parsing reply contents; AIChatPlusEditor is responsible for implementing an AI chat tool editor.

The UClass responsible for sending requests is FAIChatPlus_xxxChatRequest, each API service has its own independent Request UClass. The replies to the requests are obtained through two types of UClass - UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase. You just need to register the corresponding callback delegate.

Before sending a request, you need to set the parameters and the message to be sent for the API. This is done by setting up with FAIChatPlus_xxxChatRequestBody. The specific reply content is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving a callback, you can obtain the ResponseBody through a specific interface.

More source code details can be found on the UE Marketplace: [AIChatPlus]()


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
