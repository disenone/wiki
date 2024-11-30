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
description: UE plugin AIChatPlus user manual
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE Plugin AIChatPlus Documentation

##Public warehouse

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Get Plugin

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Plugin Introduction

This plugin supports UE5.2+.

UE.AIChatPlus is a plugin for UnrealEngine that enables communication with various GPT AI chat services. Currently supported services include OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and local offline llama.cpp. More service providers will be supported in the future. Its implementation is based on asynchronous REST requests, efficient in performance, making it convenient for Unreal Engine developers to integrate these AI chat services.

At the same time, UE.AIChatPlus also includes an editor tool that allows you to use these AI chat services directly in the editor to generate text and images, analyze images, and so on.

##Instructions for use

###Editor chat tool

Menu bar Tools -> AIChatPlus -> AIChat can open the editor chat tool provided by the plugin

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chat, image generation, and image analysis.

The interface of the tool is roughly as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main Functions

Offline large-scale model: Integrated llama.cpp library, supporting local offline execution of large models

Text Chat: Click on the `New Chat` button in the bottom left corner to create a new text chat session.

Image Generation: Click on the `New Image Chat` button in the bottom left corner to start a new image generation session.

Image Analysis: Some chat services in `New Chat` support sending images, such as Claude, Google Gemini. Click the 🖼️ or 🎨 button above the input box to load the image you want to send.

Support Blueprint: Support Blueprint to create API requests, complete text chatting, image generation, and other functions.

Set the current chat role: The dropdown menu at the top of the chat box can be used to set the current role for sending text, allowing you to adjust AI chat by simulating different roles.

Clear the conversation: Clicking the ❌ icon on the top of the chat box can clear the history messages of the current conversation.

Dialogue Template: Built-in hundreds of dialogue setting templates, making it easy to handle common issues.

Global Settings: Click the `Setting` button at the bottom left corner to open the global settings window. You can set default text chat, API services for image generation, and specify parameters for each API service. The settings will be saved automatically in the project's path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversation Settings: Click on the Settings button above the chat box to open the settings window for the current conversation. You can edit the conversation name, change the API service used for the conversation, and customize specific parameters for each conversation independently. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Edit chat content: When hovering over a chat message, a settings button for that individual message will appear, enabling options to regenerate, edit, copy, delete, or regenerate below (for user-generated content).

* Image browsing: For image generation, clicking on the image will open the image viewing window (ImageViewer), supporting saving images as PNG/UE Texture. Textures can be viewed directly in the Content Browser for easy use within the editor. Additionally, it supports functions such as deleting images, regenerating images, and continuing to generate more images. For editors on Windows, it also supports copying images, allowing you to directly copy images to the clipboard for easy use. Images generated during the session will be automatically saved in each session folder, typically located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

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

Use offline large models

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Dialogue Template

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introduction to the core code

The plugin is currently divided into the following modules:

AIChatPlusCommon: Runtime module, responsible for handling various AI API interface requests and parsing response content.

* AIChatPlusEditor: Editor module, responsible for implementing the editor AI chat tool.

AIChatPlusCllama: Runtime module responsible for encapsulating the interface and parameters of llama.cpp, enabling offline execution of large models

* Thirdparty/LLAMACpp: Runtime third-party module, integrating llama.cpp dynamic library and header files.

The UClass responsible for sending requests is FAIChatPlus_xxxChatRequest specifically. Each API service has its own independent Request UClass. Responses to requests are obtained through two UClass: UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase, just need to register the corresponding callback delegate.

Before sending a request, you need to set the parameters of the API and the message to be sent. This is done by setting up FAIChatPlus_xxxChatRequestBody. The specific content of the response is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving a callback, you can obtain the ResponseBody through a specific interface.

More source code details can be obtained from the UE Marketplace: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##User Guide

###Use the offline model llama.cpp with the editor tool.

The following explains how to use the offline model llama.cpp in the AIChatPlus editor tool.

First, download the offline model from the HuggingFace website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Put the model in a specific folder, such as placing it in the directory Content/LLAMA of the game project.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Open the AIChatPlus editor tool: Tools -> AIChatPlus -> AIChat, create a new chat session, and open the session settings page.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Set the API to Cllama, enable Custom API Settings, add model search paths, and select a model.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Start chatting!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###The code uses the offline model llama.cpp.

The following explains how to use the offline model llama.cpp in the code.

First of all, you also need to download the model files to Content/LLAMA.

Add a command in the code to send a message to the offline model within the command.

```c++
#include "Common/AIChatPlus_Log.h"
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"

void AddTestCommand()
{
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("AIChatPlus.TestChat"),
		TEXT("Test Chat."),
		FConsoleCommandDelegate::CreateLambda([]()
		{
			if (!FModuleManager::GetModulePtr<FAIChatPlusCommon>(TEXT("AIChatPlusCommon"))) return;

			TWeakObjectPtr<UAIChatPlus_ChatHandlerBase> HandlerObject = UAIChatPlus_ChatHandlerBase::New();
			// Cllama
			FAIChatPlus_CllamaChatRequestOptions Options;
			Options.ModelPath.FilePath = FPaths::ProjectContentDir() / "LLAMA" / "qwen1.5-1_8b-chat-q8_0.gguf";
			Options.NumPredict = 400;
			Options.bStream = true;
			// Options.StopSequences.Emplace(TEXT("json"));
			auto RequestPtr = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(
				Options,
				{
					{"You are a chat bot", EAIChatPlus_ChatRole::System},
					{"who are you", EAIChatPlus_ChatRole::User}
				});

			HandlerObject->BindChatRequest(RequestPtr);
			const FName ApiName = TEnumTraits<EAIChatPlus_ChatApiProvider>::ToName(RequestPtr->GetApiProvider());

			HandlerObject->OnMessage.AddLambda([ApiName](const FString& Message)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] Message: [%s]"), *ApiName.ToString(), *Message);
			});
			HandlerObject->OnStarted.AddLambda([ApiName]()
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestStarted"), *ApiName.ToString());
			});
			HandlerObject->OnFailed.AddLambda([ApiName](const FAIChatPlus_ResponseErrorBase& InError)
			{
				UE_LOG(AIChatPlus_Internal, Error, TEXT("TestChat[%s] RequestFailed: %s "), *ApiName.ToString(), *InError.GetDescription());
			});
			HandlerObject->OnUpdated.AddLambda([ApiName](const FAIChatPlus_ResponseBodyBase& ResponseBody)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestUpdated"), *ApiName.ToString());
			});
			HandlerObject->OnFinished.AddLambda([ApiName](const FAIChatPlus_ResponseBodyBase& ResponseBody)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestFinished"), *ApiName.ToString());
			});

			RequestPtr->SendRequest();
		}),
		ECVF_Default
	);
}
```

After recompiling, you can use commands in the editor Cmd to see the output results of the large model in the log OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Use the offline model llama.cpp in the blueprint.

The following explains how to use the offline model llama.cpp in the blueprint.

Create a node `Send Cllama Chat Request` by right-clicking in the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Create an Options node, and set `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

* Create Messages, add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Create a delegate to receive model output information and print it on the screen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, run the blueprint, and you will see the message returned on the game screen when printing the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###Blueprint uses OpenAI models

Create a node `Send OpenAI Chat Request In World` by right-clicking in the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Create the Options node and set `Stream=true, Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Create Messages, and add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Create a `Delegate` to receive model output information and print it on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, run the blueprint, and you will see the game screen printing the message returned by the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###The blueprint employs Claude to analyze images.

Create a node `Send Claude Chat Request` by right-clicking in the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Create an Options node, and set `Stream=true, Api Key="your API key from Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Create Messages, create a Texture2D from a file, and create AIChatPlusTexture from Texture2D, then add AIChatPlusTexture to Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Just like the tutorial above, create an Event and print the information on the game screen.

The complete blueprint looks like this. Running the blueprint will show the message returned by the game screen when printing the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

###Blueprint using OpenAI to create images

In the blueprint, right-click to create a node `Send OpenAI Image Request`, and set `In Prompt="a beautiful butterfly"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Create an Options node and set `Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Bind the On Images event and save the image to the local hard disk.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

The complete blueprint looks like this, run the blueprint, and you will see the image saved in the specified location.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

##Release Notes

### v1.3.3 - 2024.11.25

####New Feature

Supports UE-5.5

####Problem Fix

Repair some blueprints not taking effect issue

### v1.3.2 - 2024.10.10

####New feature

Fix cllama crash when manually stopping request.

Fix the issue of not being able to find ggml.dll and llama.dll files when packaging the Win version of the mall for download.

Ensure to check if it is in the GameThread when creating a request.

### v1.3.1 - 2024.9.30

####New Features

Add a SystemTemplateViewer that allows you to view and use hundreds of system setting templates.

####Issue resolved

Repair the plugin downloaded from the mall, llama.cpp cannot find the linking library.

Fix the issue of LLAMACpp path being too long.

Repair the llama.dll error in the Windows packaged link.

Fix iOS/Android file path reading issue

Fix Cllame setting name error

### v1.3.0 - 2024.9.23

####Significant new feature

Integrated llama.cpp to support local offline execution of large models.

### v1.2.0 - 2024.08.20

####New Feature

Support OpenAI Image Edit/Image Variation.

Support Ollama API, support automatically obtaining the list of models supported by Ollama.

### v1.1.0 - 2024.08.07

####New feature

Support Blueprint

### v1.0.0 - 2024.08.05

####New Feature

Basic complete functionality

Support OpenAI, Azure, Claude, Gemini

An editor with built-in chat tool.

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
