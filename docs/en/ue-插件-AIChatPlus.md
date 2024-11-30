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

#UE Plugin AIChatPlus Documentation

##Public Warehouse

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Get plugin

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introduction to Plugins

This plugin supports UE5.2+.

UE.AIChatPlus is a plugin for UnrealEngine that enables communication with various GPT AI chat services. Currently supported services include OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and llama.cpp for local offline usage. More service providers will be supported in the future. Its implementation is based on asynchronous REST requests, offering high performance and making it convenient for UE developers to integrate these AI chat services.

The UE.AIChatPlus also includes an editor tool, which allows users to directly utilize these AI chat services in the editor to generate text and images, analyze images, and so on.

##Instructions for Use

###Chat tool for editors

Menu bar Tools -> AIChatPlus -> AIChat can open the editor chat tool provided by the plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chat, image generation, and image analysis.

The interface of the tool is roughly:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main functions

Offline large model: Integrated the llama.cpp library, supporting local offline execution of large models.

Text Chat: Click the `New Chat` button at the bottom left corner to create a new text chat session.

Image Generation: Click the `New Image Chat` button in the bottom left corner to start a new image generation session.

Image Analysis: Some chat services in `New Chat` support sending images, such as Claude and Google Gemini. You can simply click on the 🖼️ or 🎨 button above the input box to load the image you want to send.

Support Blueprint: support Blueprint to create API requests, complete tasks such as text chatting, image generation, etc.

Set the current chat role: The drop-down box above the chat box can be used to set the current role for sending text. You can simulate different roles to adjust AI chat.

Empty Chat: Clicking on the ❌ icon at the top of the chat box can clear the history of the current conversation.

Dialogue Template: Built-in hundreds of dialogue setting templates, convenient for handling common issues.

Global Settings: Click the `Setting` button in the bottom left corner to open the global settings window. You can configure default text chat, image generation API services, and specify parameters for each API service. The settings will be automatically saved in the project path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversation Settings: Click the settings button at the top of the chat box to open the settings window for the current conversation. You can modify the conversation name, change the API service used for the conversation, and independently set specific parameters for each conversation's API usage. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Edit Chat Message: Hover over the chat message to display a settings button for that individual message. Options include regenerating content, editing, copying, deleting, and regenerating content below (for messages authored by users).

* Image browsing: For image generation, clicking on an image will open the image viewing window (ImageViewer), which supports saving images as PNG/UE Texture. Textures can be viewed directly in the Content Browser, making it easy to use images within the editor. Additionally, functionalities such as deleting images, regenerating images, and continuing to generate more images are supported. For editors on Windows, image copying is also supported, allowing images to be copied directly to the clipboard for convenient usage. Images generated during a session will automatically be saved in each session folder, generally located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

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

Dialogue template

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Core Code Introduction

The plugins are currently divided into the following modules:

* AIChatPlusCommon: Runtime module responsible for handling various AI API interface requests and parsing response content.

AIChatPlusEditor: Editor module, responsible for implementing the AI chat tool in the editor.

* AIChatPlusCllama: Runtime module responsible for encapsulating the interface and parameters of llama.cpp, enabling offline execution of large models

* Thirdparty/LLAMACpp: Runtime third-party module, integrating the dynamic library and header files of llama.cpp.

The UClass responsible for sending requests specifically is FAIChatPlus_xxxChatRequest. Each type of API service has its own independent Request UClass. The response to the request is obtained through two types of UClass, UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase, by simply registering the corresponding callback delegate.

Before sending a request, you need to set up the parameters and the message to be sent for the API. This part is configured using FAIChatPlus_xxxChatRequestBody. The specific content of the reply is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving the callback, you can obtain the ResponseBody through a specific interface.

You can find more source code details on the UE Marketplace: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##User Guide

###Use the offline model llama.cpp in the text editor tool.

Below is an explanation of how to use the offline model llama.cpp in the AIChatPlus editor tool.

First, download the offline model from the HuggingFace website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Put the model in a certain folder, such as placing it in the Content/LLAMA directory of the game project.

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

###The code uses the offline model llama.cpp

The following explains how to use the offline model llama.cpp in the code.

Firstly, you also need to download the model files to Content/LLAMA.

Modify the code to add a command, and send a message to the offline model inside the command.

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

After recompilation, you can use the command in the Cmd editor to see the output results of the large model in the OutputLog log.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Use the offline model blueprint llama.cpp.

The following instructions explain how to use the offline model llama.cpp in the blueprint.

In the blueprint, right-click to create a node `Send Cllama Chat Request`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

* Create an Options node, and set `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Create Messages, respectively add a System Message and a User Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Create a Delegate to receive the model's output information and print it on the screen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, running the blueprint, you will see the message returned on the game screen as it prints the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###Use OpenAI model for blueprint.

Create a node `Send OpenAI Chat Request In World` by right-clicking in the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Create an Options node, and set `Stream=true, Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

* Create Messages, add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Create a Delegate to receive output information from the model and print it on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this; running the blueprint will display a message on the game screen printing the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Blueprint uses Claude to analyze images

* Right-click in the blueprint to create a node `Send Claude Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Create the Options node and set `Stream=true, Api Key="your API key from Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

* Create Messages, create Texture2D from file, and create AIChatPlusTexture from Texture2D, then add AIChatPlusTexture to Message

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Just like the tutorial above, create an Event and print the information on the game screen.

The complete blueprint looks like this. Run the blueprint, and you will see the message returned from printing the large model on the game screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

###Create images using OpenAI Blueprints

In the blueprint, right-click to create a node `Send OpenAI Image Request`, and set `In Prompt="a beautiful butterfly"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Create an Options node, and set `Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Bind the On Images event and save the image to the local hard disk.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

The complete blueprint looks like this, run the blueprint, and you will see the image saved in the specified location.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

##Release Notes

### v1.3.3 - 2024.11.25

####New Feature

Support UE-5.5.

###Problem Fix

Fix some blueprints not taking effect issue

### v1.3.2 - 2024.10.10

####New Feature

Fix the crash when manually stopping the request in cllama.

Fix the issue of not being able to find ggml.dll and llama.dll files in the win packaging of the mall download version.

When creating a request, check if it is in the GameThread.

### v1.3.1 - 2024.9.30

####New feature

Add a SystemTemplateViewer that allows you to view and use hundreds of system setting templates.

####Problem Fix

Fix the plugin downloaded from the store, llama.cpp cannot find the linking library.

Fix LLAMACpp path too long issue

Fix the llama.dll error in Windows packaging after linking.

Fix the issue of reading file paths on iOS/Android.

Fix Cllame setting name error.

### v1.3.0 - 2024.9.23

####Major New Feature

Integrated llama.cpp to support local offline execution of large models

### v1.2.0 - 2024.08.20

####New Feature

Support OpenAI Image Edit/Image Variation

Support Ollama API, support automatically fetching the list of models supported by Ollama.

### v1.1.0 - 2024.08.07

####New features

Support blueprint

### v1.0.0 - 2024.08.05

####New feature

Complete basic functionality

Support OpenAI, Azure, Claude, Gemini.

Built-in feature-rich editor chat tool

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
