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

#UE plugin AIChatPlus documentation

##Public repository

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtain plugin

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introduction to the Plugin

This plugin supports UE5.2+.

UE.AIChatPlus is a UnrealEngine plugin that enables communication with various GPT AI chat services. Currently, it supports services such as OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini. In the future, it will continue to support more service providers. Its implementation is based on asynchronous REST requests, ensuring high performance and facilitating integration of these AI chat services by Unreal Engine developers.

At the same time, UE.AIChatPlus also includes an editor tool that allows you to directly use these AI chat services in the editor, generate text and images, and analyze images.

##Instructions for use

###Editor chat tool

Menu bar Tools -> AIChatPlus -> AIChat can open the editor chat tool provided by the plugin

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chatting, image generation, and image analysis.

The interface of the tool is roughly:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main Functions

Text Chat: Click the `New Chat` button in the bottom left corner to start a new text chat session.

Image Generation: Click the `New Image Chat` button in the bottom left corner to start a new image generation session.

Image Analysis: Some chat services in `New Chat` support sending images, such as Claude, Google Gemini. You can simply click on the 🖼️ or 🎨 button above the input box to load the image you want to send.

Support Blueprint: Supporting Blueprint to create API requests, complete text chat, image generation, and other functions.

Set the current chat role: The dropdown menu above the chat box can be used to set the current character for sending text, allowing you to simulate different roles to adjust AI chat.

Clear session: Tap the ❌ icon at the top of the chat box to clear the chat history of the current session.

**Global Settings:** Click on the `Settings` button in the lower left corner to open the global settings window. You can configure default text chat, image generation API services, and set specific parameters for each API service. The settings will be automatically saved in the project's path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversation Settings: Click on the settings button above the chat box to open the settings window for the current conversation. You can modify the conversation name, change the API service used for the conversation, and independently set specific parameters for each conversation's API. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Modify chat content: When hovering over the chat content, a settings button will appear for each chat content, supporting options to regenerate content, edit content, copy content, delete content, and regenerate content below (for content authored by users).

* Image browsing: For image generation, clicking on an image will open the image viewing window (ImageViewer), supporting saving images as PNG/UE Texture. Textures can be viewed directly in the content browser, making it convenient for images to be used within the editor. Additionally, functions such as deleting images, regenerating images, and generating more images are supported. For editors on Windows, image copying is also supported, allowing images to be copied directly to the clipboard for easy use. Images generated during the session will also be automatically saved in each session folder, typically located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Blueprint:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Global Settings: 

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Conversation Settings:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modify chat content:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Image Viewer:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

###Introduction to core code

At present, the plugin is divided into two modules: AIChatPlusCommon (Runtime) and AIChatPlusEditor (Editor).

AIChatPlusCommon is responsible for handling sending requests and parsing reply contents; AIChatPlusEditor is responsible for implementing the editor AI chat tool.

The UClass responsible for sending requests is FAIChatPlus_xxxChatRequest. Each type of API service has its own unique Request UClass. Responses to requests are obtained through two UClass, UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase, simply by registering the corresponding callback delegates.

Before sending a request, you need to set the parameters for the API and the message to be sent. This is done through FAIChatPlus_xxxChatRequestBody. The specific content of the reply is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving the callback, you can obtain the ResponseBody through a specific interface.

You can find more source code details on the UE Marketplace: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)


###Update Log

#### v1.2.0 - 2024.08.20

Support OpenAI Image Edit/Image Variation

Support Ollama API, support automatically getting the list of models supported by Ollama

#### v1.1.0 - 2024.08.07

Support blueprints

#### v1.0.0 - 2024.08.05

Basic complete function

Support OpenAI, Azure, Claude, Gemini.

Built-in feature-rich editor chat tool

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
