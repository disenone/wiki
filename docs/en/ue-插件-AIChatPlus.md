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

##Obtain Plugin

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introduction to the plugin

This plugin supports UE5.2+.

UE.AIChatPlus is a UnrealEngine plugin that allows communication with various GPT AI chat services. Currently, it supports services like OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and local offline llama.cpp. In the future, more service providers will be supported. Its implementation is based on asynchronous REST requests, providing high efficiency performance, making it convenient for UE developers to integrate these AI chat services.

At the same time, UE.AIChatPlus also includes an editor tool that allows you to use these AI chat services directly in the editor to generate text and images, analyze images, and so on.

##Instructions for use

###Editor Chat Tool

Menu bar Tools -> AIChatPlus -> AIChat can open the editor chat tool provided by the plugin

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chat, image generation, and image analysis.

The interface of the tool is roughly:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main Features

Offline Large Models: Integrated llama.cpp library, supporting local offline execution of large models

Text Chat: Click the `New Chat` button in the lower left corner to create a new text chat session.

Image Generation: Click the `New Image Chat` button in the bottom left corner to start a new image generation session.

Image Analysis: Some chat services in "New Chat" support sending images, such as Claude and Google Gemini. Simply click on the 🖼️ or 🎨 button above the input box to load the image you want to send.

Support Blueprint: Support Blueprint to create API requests, complete text chatting, image generation, and other functions.

Set the current chat character: The dropdown menu above the chat box can set the role for the currently sending text, allowing you to adjust the AI chat by simulating different characters.

Clear chat: Clicking the ❌ icon at the top of the chat box will clear the history of the current conversation.

Dialogue Template: There are hundreds of built-in dialogue setting templates available to facilitate the handling of common issues.

Global Settings: Click on the `Setting` button in the lower left corner to open the global settings window. You can set default text chat, image generation API services, and specify parameters for each API service. The settings will be automatically saved in the project's path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversation Settings: Click on the settings button above the chat box to open the settings window for the current conversation. You can modify the conversation name, change the API service used for the conversation, and independently set specific parameters for each conversation's API usage. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Chat content editing: When hovering over a chat message, a settings button for that particular message will appear, allowing you to regenerate, edit, copy, or delete the content, as well as regenerate the content below (for messages authored by users).

* Image Browser: For image generation, clicking on an image will open the Image Viewer, supporting saving images as PNG/UE Texture. Textures can be directly viewed in the Content Browser, making it convenient to use images within the editor. Additionally, functions such as deleting images, regenerating images, and generating more images are supported. For editors on Windows, image copying is also supported, enabling images to be copied to the clipboard for easy use. Images generated during sessions will automatically be saved in each session folder, typically located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

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

Using offline large models

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Dialogue Template

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introduction to Core Code

The plugins are currently divided into the following modules:

* AIChatPlusCommon: Runtime module, responsible for handling various AI API interface requests and parsing response content.

* AIChatPlusEditor: Editor module, responsible for implementing the AI chat tool in the editor.

AIChatPlusCllama: Runtime module responsible for encapsulating the interface and parameters of llama.cpp, implementing offline execution of large models.

* Thirdparty/LLAMACpp: Runtime third-party module, integrating the dynamic library and header files of llama.cpp.

The UClass responsible for sending requests specifically is FAIChatPlus_xxxChatRequest, and each API service has its own independent Request UClass. The replies to the requests are obtained through two types of UClass, UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase, simply requiring the registration of the corresponding callback delegate.

Before sending a request, you need to set up the API parameters and the message to be sent. This is done through the FAIChatPlus_xxxChatRequestBody. The specific reply content is also parsed into the FAIChatPlus_xxxChatResponseBody. When receiving a callback, you can retrieve the ResponseBody through a specific interface.

More details of the source code can be obtained at the UE Marketplace: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##User Guide

###Use the offline model llama.cpp in the editor tool.

The following explains how to use the offline model llama.cpp in the AIChatPlus editor tool.

First, download the offline model from the HuggingFace website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Put the model in a specific folder, like placing it in the Content/LLAMA directory of the game project.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Open the AIChatPlus editor tool: Tools -> AIChatPlus -> AIChat, create a new chat session, and open the session settings page.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Set the API to Cllama, enable Custom API Settings, add model search paths, and select models.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Start chatting!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Use the offline model code llama.cpp.

The following explains how to use the offline model llama.cpp in the code.

First, you also need to download the model file to Content/LLAMA.

Modify the code to add a command and send a message to the offline model within the command.

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

After recompiling, use the command in the editor's Cmd to see the output results of large models in the log OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Use the offline model blueprint llama.cpp.

The following explains how to use the offline model llama.cpp in the blueprint.

Create a node `Send Cllama Chat Request` by right-clicking in the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Create an Options node and set `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Create Messages, add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Create a delegate to receive the model's output information and print it on the screen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this. When you run the blueprint, you will see the message returned on the game screen printing a large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##Changelog

### v1.3.3 - 2024.11.25

Support UE-5.5.

### v1.3.2 - 2024.10.10

#### Bugfix

Fix crash when manual stopping request in cllama.
Fix the issue where the win package of the mall download version cannot find the ggml.dll and llama.dll files.
When creating a request, check if it is in the GameThread.

### v1.3.1 - 2024.9.30

Add a SystemTemplateViewer that allows you to view and use hundreds of system setting templates.

#### Bugfix

Fix the plugin downloaded from the store, llama.cpp can't find the link library.
Fix LLAMACpp long path issue
Fix the llama.dll error in the Windows build.
Fix iOS/Android file reading path issue
Fix the Cllame setting name error

### v1.3.0 - 2024.9.23

Major Update

Integrated llama.cpp, supports local offline execution of large models.

### v1.2.0 - 2024.08.20

Support OpenAI Image Edit/Image Variation.

Support Ollama API, support automatically fetching the list of models supported by Ollama.

### v1.1.0 - 2024.08.07

Support Blueprint

### v1.0.0 - 2024.08.05

Basic complete functionality

Support OpenAI, Azure, Claude, Gemini.

Built-in feature-rich editor chat tool

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
