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

#UE Plugin AIChatPlus Instruction Manual

##Public warehouse

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtain plug-in

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Plugin Introduction

This plugin supports UE5.2+.

UE.AIChatPlus is a UnrealEngine plugin that enables communication with various GPT AI chat services. The plugin currently supports services such as OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and local offline llama.cpp. In the future, it will continue to support more service providers. Its implementation is based on asynchronous REST requests, providing high performance and making it convenient for UE developers to integrate these AI chat services.

At the same time, UE.AIChatPlus also includes an editor tool that allows direct use of these AI chat services in the editor to generate text and images, analyze images, and more.

##Instructions for use

###Editor chat tool

Menu bar Tools -> AIChatPlus -> AIChat can open the editor chat tool provided by the plugin

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chat, image generation, and image analysis.

The interface of the tool is roughly as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main Functions

Offline Large Model: Integrated llama.cpp library, supporting local offline execution of large models

Text chat: Click the `New Chat` button in the lower-left corner to start a new text chat session.

Image Generation: Click on the `New Image Chat` button in the bottom left corner to create a new image generation session.

Image Analysis: Some chat services in `New Chat` support sending images, such as Claude, Google Gemini. Click the 🖼️ or 🎨 button above the input box to load the image you want to send.

Support Blueprint: Support the creation of Blueprint API requests to achieve functions such as text chat and image generation.

Set the current chat character: The dropdown box above the chat box can be used to set the current character for sending text, allowing you to adjust the AI chat by simulating different characters.

Clear chat: The ❌ button above the chat box can clear the chat history of the current session.

Dialogue Template: Hundreds of built-in dialogue templates are available to easily handle common issues.

Global settings: Click the `Setting` button in the lower-left corner to open the global settings window. You can configure default text chat, image generation API services, and specify parameters for each API service. The settings will be automatically saved in the project directory `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversation Settings: Click on the settings button above the chat box to open the settings window for the current conversation. You can change the conversation name, modify the API service used for the conversation, and independently set specific parameters for each conversation's API. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Chat content editing: When hovering over a chat content, a settings button for that specific content will appear, supporting options to regenerate, modify, copy, delete, and regenerate below (for content owned by a user role).

* Image browsing: For image generation, clicking on an image will open the image viewing window (ImageViewer), supporting saving images as PNG/UE Texture. Textures can be viewed directly in the Content Browser, making it easy to use images within the editor. Additionally, it supports functions like deleting images, regenerating images, and continuing to generate more images. For editors on Windows, image copying is also supported, allowing images to be copied directly to the clipboard for easy use. Images generated during a session will also be automatically saved under each session folder, usually located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Blueprint:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Global Settings:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Conversation Settings:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Edit Chat Content:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Image Viewer:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Use offline large models

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Dialogue Template

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introduction to Core Code

Currently, the plugin is divided into the following modules:

* **AIChatPlusCommon:** Runtime module responsible for handling various AI API interface requests and parsing response content.

* AIChatPlusEditor: Editor module, responsible for implementing the AI chat tool within the editor.

AIChatPlusCllama: Runtime module, responsible for encapsulating the interface and parameters of llama.cpp, implementing offline execution of large models

* Thirdparty/LLAMACpp: Third-party runtime module, integrating the dynamic library and header files of llama.cpp.

The UClass responsible for sending requests specifically is FAIChatPlus_xxxChatRequest. Each type of API service has its own independent Request UClass. Replies to the requests are obtained through two types of UClass, UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase, simply by registering the corresponding callback delegate.

Before sending a request, you need to set the parameters of the API and the message to be sent. This is done by setting up the FAIChatPlus_xxxChatRequestBody. The specific content of the reply is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving a callback, you can obtain the ResponseBody through a specific interface.

More source code details can be found on UE Marketplace: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)


###Update Log

#### v1.3.1 - 2024.9.30

Add a System Template Viewer that allows you to view and utilize hundreds of system setting templates.

##### Bugfix

Fix the plugin downloaded from the mall, llama.cpp cannot find the linked library.
Fix the issue of LLAMACpp path being too long
Fix the llama.dll error in the windows packaged build
Fix iOS/Android file path reading issue
Fix Cllame setting name error

#### v1.3.0 - 2024.9.23

Major Update

Integrated llama.cpp to support local offline execution of large models.

#### v1.2.0 - 2024.08.20

Support for OpenAI Image Edit/Image Variation

Support Ollama API, support automatically fetching the list of models supported by Ollama.

#### v1.1.0 - 2024.08.07

Support blueprint.

#### v1.0.0 - 2024.08.05

Complete Basic Functionality

Support OpenAI, Azure, Claude, Gemini.

Built-in feature-rich editor for chatting tool

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
