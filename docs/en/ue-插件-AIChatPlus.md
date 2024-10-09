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
description: UE Plugin AIChatPlus User Manual
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE Plugin AIChatPlus Documentation

##Public repository

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Plugin Acquisition

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introduction to the Plugin

This plugin supports UE5.2+.

UE.AIChatPlus is a UnrealEngine plugin that enables communication with various GPT AI chat services. Currently supported services include OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and local offline llama.cpp. In the future, more service providers will continue to be supported. Its implementation is based on asynchronous REST requests, ensuring high performance and facilitating access to these AI chat services for Unreal Engine developers.

At the same time, UE.AIChatPlus also includes an editor tool that allows you to use these AI chat services directly in the editor to generate text and images, analyze images, and more.

##Instructions for use

###Chat tool for text editors

Menu bar Tools -> AIChatPlus -> AIChat can open the editor chat tool provided by the plugin

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chatting, image generation, and image analysis.

The interface of the tool is roughly:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main Functions

Offline Large Model: Integrated the llama.cpp library, supporting local offline execution of large models.

Text Chat: Click the `New Chat` button in the bottom left corner to start a new text chat session.

Image Generation: Click on the `New Image Chat` button in the bottom left corner to start a new image generation session.

Image Analysis: Some chat services in `New Chat` support sending images, such as Claude, Google Gemini. Click the 🖼️ or 🎨 button above the input box to load the image you want to send.

Support Blueprint: Support Blueprint to create API requests, complete text chatting, image generation, and other functions.

Set the current chat character: The dropdown box at the top of the chat box can be used to set the current character for sending text, allowing you to adjust AI chat by simulating different characters.

Clear chat: Clicking on the ❌ above the chat box clears the history of the current conversation.

Dialogue Template: Built-in hundreds of dialogue setting templates, making it convenient to handle common issues.

Global Settings: Click the `Setting` button in the bottom left corner to open the global settings window. You can configure default text chat, image generation API services, and specific parameters for each API service. The settings will be automatically saved in the project's path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversation Settings: Click on the settings button at the top of the chat box to open the settings window for the current conversation. You can modify the conversation's name, change the API service used in the conversation, and independently adjust specific parameters for each API used in the conversation. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Modify chat content: When hovering the mouse over the chat content, a settings button for each chat content will appear, supporting options like regenerating content, modifying content, copying content, deleting content, and regenerating content below (for content authored by users).

* Image Browsing: For image generation, clicking on an image will open the Image Viewer window, supporting saving images as PNG/UE Texture. Textures can be directly viewed in the Content Browser, facilitating their use within the editor. Additionally, it supports functions such as deleting images, regenerating images, and continuing to generate more images. For editors on Windows, image copying is also supported, allowing images to be copied directly to the clipboard for convenient use. Images generated during sessions will also be automatically saved in each session folder, usually located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Blueprint:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Global Settings:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Conversation Settings:

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

Currently, the plugin is divided into the following modules:

* AIChatPlusCommon: Runtime module, responsible for handling various AI API interface request sending and response content parsing.

AIChatPlusEditor: The editor module is responsible for implementing the AI chatting tool editor.

* AIChatPlusCllama: Runtime module responsible for encapsulating the interface and parameters of llama.cpp, achieving offline execution of large models

* Thirdparty/LLAMACpp: Runtime third-party module, integrating llama.cpp dynamic library and header files.

The UClass responsible for sending requests specifically is FAIChatPlus_xxxChatRequest, each type of API service has its own independent Request UClass. The response to the request is obtained through two UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase UClass, you only need to register the corresponding callback delegate.

Before sending a request, you need to set the parameters of the API and the message to be sent. This is done by setting FAIChatPlus_xxxChatRequestBody. The specific reply is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving a callback, you can obtain the ResponseBody through a specific interface.

More source code details are available on the UE Marketplace: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##User Manual

###Use the offline model llama.cpp in the editor tool.

The following explains how to use the offline model llama.cpp in the AIChatPlus editor tool.

First, download the offline model from the HuggingFace website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Put the model in a certain folder, such as placing it in the Content/LLAMA directory of the game project.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Open the AIChatPlus editor tool: Tools -> AIChatPlus -> AIChat, create a new chat session, and open the session settings page.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Set the API to Cllama, enable Custom API Settings, add model search paths, and select the model.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Start chatting!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###The code uses the offline model llama.cpp.

The following explains how to use the offline model llama.cpp in the code.

First, you also need to download the model file to Content/LLAMA.

Modify the code to add a new command and send a message to the offline model within the command.

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

After recompiling, you can use commands in the Cmd editor to see the output results of large models in the OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Use the offline model llama.cpp in the blueprint.

The following explains how to use the offline model llama.cpp in the blueprint.

Right-click in the blueprint to create a node called `Send Cllama Chat Request`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Create an Options node, and set `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Create Messages, add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Create a Delegate to receive the model's output information and print it on the screen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, run the blueprint, and you will see the message returned to the game screen when printing the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##Release Notes

### v1.3.1 - 2024.9.30

Add a SystemTemplateViewer that allows you to view and utilize hundreds of system setting templates.

#### Bugfix

Fix the plugin downloaded from the mall, llama.cpp can't find the link library
Fix LLAMACpp long path issue
Fix the llama.dll error after packaging Windows.
Fix iOS/Android file path reading issue
Fix Cllame setting name error

### v1.3.0 - 2024.9.23

Major Update

Integrated llama.cpp, supporting local offline execution of large models

### v1.2.0 - 2024.08.20

Support OpenAI Image Edit/Image Variation.

Support Ollama API, support automatically obtaining the list of models supported by Ollama.

### v1.1.0 - 2024.08.07

Support the blueprint

### v1.0.0 - 2024.08.05

Basic Complete Features

Support OpenAI, Azure, Claude, Gemini.

Built-in feature-rich editor chat tool

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
