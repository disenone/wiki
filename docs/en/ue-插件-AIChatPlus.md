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

#Documentation for UE plugin AIChatPlus

##Public warehouse

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Plugin acquisition

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introduction to the plugin

This plugin supports UE5.2+.

UE.AIChatPlus is a plugin for UnrealEngine that enables communication with various GPT AI chat services. Currently, it supports services such as OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and llama.cpp for local offline processing. In the future, it will continue to support more service providers. Its implementation is based on asynchronous REST requests, ensuring high performance and making it convenient for UE developers to integrate these AI chat services.

At the same time, UE.AIChatPlus also includes an editor tool that allows you to directly use these AI chat services in the editor to generate text and images, analyze images, and so on.

##Instructions for use

###Chat tool for editors

Menu bar: Tools -> AIChatPlus -> AIChat can open the editor chat tool provided by the plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chat, image generation, and image analysis.

The interface of the tool is roughly as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main Functions

Offline large-scale model: integrated llama.cpp library, supporting local offline execution of large models

Text chat: Click the `New Chat` button in the lower left corner to start a new text chat session.

Image Generation: Click on the `New Image Chat` button in the bottom left corner to start a new image generation session.

Image Analysis: Some chat services in `New Chat` support sending images, such as Claude, Google Gemini. You can click on the 🖼️ or 🎨 button above the input box to load the image you want to send.

Support Blueprint: Support blueprint creation API requests, complete text chat, image generation, and other functions.

Set the current chat role: The dropdown box above the chat box can be used to set the current character for sending text, allowing you to simulate different characters to adjust the AI chat.

Clear chat: Use the ❌ button at the top of the chat box to delete the history of the current conversation.

Dialogue Template: Built-in hundreds of dialogue setting templates, making it easy to handle common issues.

Global Settings: Click the `Setting` button in the lower-left corner to open the global settings window. You can set default text chat, image generation API services, and specify parameters for each API service. The settings will be automatically saved in the project's path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversation settings: Click on the settings button above the chat box to open the settings window for the current conversation. You can modify the conversation name, change the API service used for the conversation, and independently specify specific parameters for each conversation's API usage. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Modify chat content: When hovering over a chat message, a settings button for that message will appear. It supports options to regenerate, edit, copy, delete, or regenerate below (for messages authored by users).

* Image browsing: For image generation, clicking on the image will open the image viewer (ImageViewer), supporting saving images as PNG/UE Texture. Textures can be directly viewed in the Content Browser, facilitating image usage within the editor. Additionally, it supports functions such as deleting images, regenerating images, and continuing to generate more images. For editors on Windows, it also supports copying images, allowing images to be copied directly to the clipboard for easy use. Images generated in the session will also be automatically saved under each session folder, typically located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

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

###Introduction to Core Code

The plugins are currently divided into the following modules:

AIChatPlusCommon: Runtime module, responsible for handling various AI API interface requests and parsing reply content.

AIChatPlusEditor: Editor module, responsible for implementing the AI chat tool in the editor.

AIChatPlusCllama: Runtime module, responsible for encapsulating the interface and parameters of llama.cpp to achieve offline execution of large models

* Thirdparty/LLAMACpp: Runtime third-party module, integrating llama.cpp dynamic library and header files.

The UClass responsible for sending requests is FAIChatPlus_xxxChatRequest. Each API service has its own independent Request UClass. The response to the request is obtained through two types of UClass, UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase, simply by registering the corresponding callback delegate.

Before sending the request, you need to set the parameters and message to be sent for the API. This is done by setting the FAIChatPlus_xxxChatRequestBody. The specific reply is also parsed into the FAIChatPlus_xxxChatResponseBody, which can be obtained through a specific interface when receiving the callback.

More source code details can be obtained at the UE Marketplace: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##User Guide

###Use the offline model llama.cpp in the editor tool.

The following instructions explain how to use the offline model llama.cpp in the AIChatPlus editor tool.

First, download the offline model from the HuggingFace website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Put the model in a specific folder, for example, place it in the directory Content/LLAMA of the game project.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Open the AIChatPlus editor tool: Tools -> AIChatPlus -> AIChat, create a new chat session, and open the session settings page.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Set the API to Cllama, enable Custom API Settings, add model search paths, and choose a model.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Start chatting!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###The code uses the offline model llama.cpp

The following explains how to use the offline model llama.cpp in the code.

First, you also need to download the model files to Content/LLAMA.

Insert a command in the code to send a message to the offline model within the command.

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

After recompiling, you can use commands in the editor Cmd to see the output results of the large model in the OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Use the offline model llama.cpp in the blueprint.

The following explains how to use the offline model llama.cpp in the blueprint.

In the blueprint, right-click to create a node called `Send Cllama Chat Request`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Create an Options node, and set `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Create Messages, add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Create a delegate to receive model output information and print it on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, running the blueprint, you can see the message on the game screen printing the large model returned.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###Blueprint using OpenAI model

Create a node `Send OpenAI Chat Request In World` by right-clicking in the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Create an Options node, and set `Stream=true, Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Create Messages, add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Create a delegate that accepts the model's output information and prints it on the screen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, running the blueprint, you can see the message returned by the game screen when printing large models.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

##Release Notes

### v1.3.3 - 2024.11.25

Support UE-5.5

* **Bugfix**: Fixed an issue where some blueprints were not taking effect.

### v1.3.2 - 2024.10.10

#### Bugfix

Fix cllama crash when manually stopping the request

Fix the issue of not being able to find the ggml.dll and llama.dll files when packaging the win version for the store download.

When creating a request, check if it is in the GameThread.

### v1.3.1 - 2024.9.30

Add a **SystemTemplateViewer** to view and utilize hundreds of system setting templates.

#### Bugfix

Repair the plugin downloaded from the marketplace, llama.cpp cannot find the linked library.

Fix the issue of LLAMACpp path being too long

Fix the llama.dll error in Windows after packaging.

Fix the issue of reading file paths on iOS/Android.

Fix Cllame setting name error

### v1.3.0 - 2024.9.23

Heavy update

Integrated llama.cpp to support offline execution of large models locally

### v1.2.0 - 2024.08.20

Support OpenAI Image Edit/Image Variation.

Support Ollama API, support automatically retrieving the list of models supported by Ollama.

### v1.1.0 - 2024.08.07

Support blueprint

### v1.0.0 - 2024.08.05

Complete basic functionality

Support OpenAI, Azure, Claude, Gemini

Built-in feature-rich editor chat tool

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
