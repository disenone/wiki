---
layout: post
title: UE EditorPlus plugin documentation
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
description: UE EditorPlus Documentation
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE Plug-in AIChatPlus Documentation


##Introduction Video

![type:video]()

##Public Repository

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtain Plugin

[AIChatPlus]()

##Introduction to the Plugin

This plugin supports UE5.2+.

UE.AIChatPlus is a plugin for UnrealEngine that enables communication with various GPT AI chat services. Currently supported services include OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, and Google Gemini. In the future, more service providers will be supported. Its implementation is based on asynchronous REST requests, ensuring high efficiency performance, making it convenient for Unreal Engine developers to integrate these AI chat services.

At the same time, UE.AIChatPlus also includes an editor tool that allows you to directly use these AI chat services in the editor to generate text and images, analyze images, and more.

##Instructions for use

###Editor Chat Tool

Menu bar: Tools -> AIChatPlus -> AIChat can open the chat tool provided by the plugin editor.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chat, image generation, and image analysis.

The interface of the tool is roughly as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

The main functions include:

Text Chat: Click the `New Chat` button in the bottom left corner to start a new text chat session.
Image Generation: Click on the `New Image Chat` button in the bottom left corner to create a new image generation session.
Image Analysis: Some chat services in "New Chat" support sending images, such as Claude and Google Gemini. By clicking on the 🖼️ or 🎨 button above the input box, you can easily load the images you want to send.
Set the current chat character: The dropdown menu at the top of the chat box can be used to set the current character for sending text. By simulating different characters, you can adjust the AI chat.
Clear conversation: Tap the ❌ icon at the top of the chat box to clear the history of the current conversation.
**Global Settings:** Click the `Setting` button in the bottom left corner to open the global settings window. You can configure default text chat, image generation API services, and define parameters for each API service. The settings will be automatically saved in the project's path `$(ProjectFolder)/Saved/AIChatPlusEditor`.
Conversation Settings: Click the settings button above the chat box to open the settings window for the current conversation. You can change the conversation name, the API service used for the conversation, and independently configure specific parameters for each conversation's API. The conversation settings will be automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.
Edit Chat Content: When you hover the mouse over the chat content, a settings button for that specific chat will appear, allowing you to regenerate, edit, copy, or delete the content. Additionally, you can regenerate content below (for user-generated content).
* Image browsing: For image generation, clicking on an image will open the image viewing window (ImageViewer), supporting saving images as PNG/UE Texture. Textures can be directly viewed in the Content Browser for easy use in the editor. Additionally, it supports functions such as deleting images, regenerating images, and generating more images. For editors on Windows, copying images is also supported, allowing images to be copied directly to the clipboard for convenient use. Images generated in each session are automatically saved in the respective session folder, usually located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

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

AIChatPlusCommon is responsible for handling sending requests and parsing reply contents; AIChatPlusEditor is responsible for implementing an AI chat tool editor.

The UClass responsible for sending requests is FAIChatPlus_xxxChatRequest. Each API service has its own independent Request UClass. The replies to the requests are obtained through two UClass, UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase. You just need to register the corresponding callback delegate.

Before sending a request, you need to set the parameters of the API and the message to be sent. This is done by setting up the FAIChatPlus_xxxChatRequestBody. The specific content of the reply is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving a callback, you can retrieve the ResponseBody through a specific interface.

More source code details can be obtained from the UE Marketplace: [AIChatPlus]()


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
