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

##Public warehouse

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Plugin Acquisition

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introduction to the plugin

This plugin supports UE5.2+.

UE.AIChatPlus is a UnrealEngine plugin that enables communication with various GPT AI chat services. Currently supported services include OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and local offline llama.cpp. More service providers will be supported in the future. Its implementation is based on asynchronous REST requests, ensuring high efficiency performance, making it convenient for Unreal Engine developers to integrate these AI chat services.

At the same time, UE.AIChatPlus also includes an editor tool that allows you to directly utilize these AI chat services in the editor to generate text and images, analyze images, and more.

##Instructions for use

###Chat tool for editors

Menu bar Tools -> AIChatPlus -> AIChat can open the editor chat tool provided by the plugin

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chat, image generation, and image analysis.

The interface of the tool is roughly as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main Functions

Offline large models: Integrated llama.cpp library to support local offline execution of large models

Text Chat: Click the `New Chat` button in the bottom left corner to create a new text chat session.

Image Generation: Click on the `New Image Chat` button in the bottom left corner to create a new image generation session.

Image analysis: Some chat services in 'New Chat' support sending images, such as Claude and Google Gemini. You can click on the 🖼️ or 🎨 button above the input box to load the image you want to send.

Support blueprint: Support blueprint to create API requests, complete text chat, image generation, and other functions.

Set the current chat role: The dropdown box above the chat box can be used to set the current role for sending text, allowing the simulation of different roles to adjust AI chat.

Clear chat: Clicking on the ❌ icon at the top of the chat box can clear the chat history of the current session.

Dialogue Template: Built-in hundreds of conversation setting templates, making it easy to handle common issues.

Global Settings: Click the `Setting` button in the lower left corner to open the global settings window. You can set default text chat, image generation API services, and specific parameters for each API service. The settings will be automatically saved in the project path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversation Settings: Click on the settings button above the chat box to open the settings window for the current conversation. You can modify the conversation name, change the API service used for the conversation, and independently set specific parameters for each conversation's API usage. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Chat content editing: When hovering over a chat message, an individual message settings button will appear, supporting options to regenerate content, edit content, copy content, delete content, and regenerate content below (for content created by the user role).

* Image browsing: For image generation, clicking on an image will open the Image Viewer window, supporting saving images as PNG/UE Texture. Textures can be viewed directly in the Content Browser, making it convenient to use images within the editor. Additionally, it supports functions such as deleting images, regenerating images, and continuing to generate more images. For editors on Windows, it also supports copying images to the clipboard for easy use. The generated images will be automatically saved in each session folder, usually located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

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

*AIChatPlusCommon: Runtime module responsible for handling various AI API interface requests and parsing response content.*

**AIChatPlusEditor:** The Editor module is responsible for implementing the AI chat tool in the editor.

* AIChatPlusCllama: Runtime module, responsible for encapsulating the interface and parameters of llama.cpp, implementing offline execution of large models

* Thirdparty/LLAMACpp: A third-party runtime module that integrates the dynamic library and header files of llama.cpp.

The `UClass` responsible for sending the request is `FAIChatPlus_xxxChatRequest`, each API service has its own independent `Request UClass`. The response to the request is received through two `UClass` types: `UAIChatPlus_ChatHandlerBase` and `UAIChatPlus_ImageHandlerBase`, and only need to register the corresponding callback delegate.

Before sending a request, you need to set up the parameters and the message to be sent for the API. This is done by setting up the FAIChatPlus_xxxChatRequestBody. The specific content of the reply is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving a callback, you can obtain the ResponseBody through a specific interface.

More source code details can be obtained from the UE mall: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

###User Guide

####Use the offline model llama.cpp with the text editor tool.

The following explains how to use the offline model llama.cpp in the AIChatPlus editor tool.

First, download the offline model from the HuggingFace website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Put the model in a specific folder, for example, place it in the Content/LLAMA directory of the game project.

	```shell
	E:/UE/projects/FP_Test1/Content/LLAMA
	> ls
	qwen1.5-1_8b-chat-q8_0.gguf*
	```

Open the AIChatPlus editor tool: Tools -> AIChatPlus -> AIChat, create a new chat session, and open the session settings page

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Set the API to Cllama, enable Custom API Settings, add the model search path, and select the model.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Start chatting!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

####The code uses the offline model llama.cpp.

The following explains how to use the offline model llama.cpp in the code.

First, you also need to download the model file to Content/LLAMA.

Modify the code to add a command, and send a message to the offline model within the command.

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

####Blueprint uses offline model llama.cpp

todo

###Release Notes

#### v1.3.1 - 2024.9.30

Add a SystemTemplateViewer that allows viewing and using hundreds of system setting templates.

##### Bugfix

Fix the plugin downloaded from the mall, llama.cpp cannot find the link library.
Fix LLAMACpp long path issue
Fix the llama.dll error in the Windows build links.
Fix the issue of reading file paths in iOS/Android.
Fix Cllame setting name error

#### v1.3.0 - 2024.9.23

Major Update

Integrated llama.cpp to support local offline execution of large models.

#### v1.2.0 - 2024.08.20

Support OpenAI Image Edit/Image Variation.

Support Ollama API, support automatically retrieving the list of models supported by Ollama.

#### v1.1.0 - 2024.08.07

Support blueprint

#### v1.0.0 - 2024.08.05

Complete Basic Functionality

Support OpenAI, Azure, Claude, Gemini.

Built-in feature-rich editor chat tool

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
