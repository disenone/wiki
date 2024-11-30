---
layout: post
title: UE Plugin AIChatPlus User Manual
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

#UE plugin AIChatPlus documentation

##Public Repository

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Get plugin

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introduction to the plugin.

This plugin supports UE5.2+.

UE.AIChatPlus is a plugin for UnrealEngine that allows communication with various GPT AI chat services. Currently supported services include OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and local offline llama.cpp. More service providers will be supported in the future. Its implementation is based on asynchronous REST requests, providing high performance and convenience for UE developers to integrate these AI chat services.

At the same time, UE.AIChatPlus also includes an editor tool, which allows you to use these AI chat services directly in the editor to generate text and images, analyze images, and more.

##Instructions for use

###Chat tool for editors

Menu bar Tools -> AIChatPlus -> AIChat can open the editor chat tool provided by the plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chat, image generation, and image analysis.

The interface of the tool is roughly:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main Functions

Offline Big Model: Integrated llama.cpp library, supporting local offline execution of big models

Text Chat: Click the `New Chat` button in the bottom left corner to start a new text chat session.

Image Generation: Click the `New Image Chat` button in the bottom left corner to start a new image generation session.

Image Analysis: Some chat services in `New Chat` support sending images, such as Claude, Google Gemini. Click the 🖼️ or 🎨 button above the input box to load the images you want to send.

Support Blueprint: Support blueprint creation of API requests, completing functions such as text chat and image generation.

Set the current chat role: The drop-down box at the top of the chat box can be used to set the current character for sending text. You can adjust AI chat by simulating different characters.

Clear chat: The ❌ button above the chat box can clear the history of the current conversation.

Dialogue template: Built-in hundreds of dialogue settings templates, making it easy to handle common issues.

* Global Settings: Click on the `Setting` button in the lower left corner to open the global settings window. You can set default text chat, image generation API services, and specify parameters for each API service. The settings will be automatically saved in the project path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversation Settings: Click the settings button above the chat box to open the settings window for the current conversation. You can change the conversation name, modify the API service used for the conversation, and independently set specific parameters for each conversation's API. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Edit chat content: When hovering over a chat message, a setting button for that specific message will appear, allowing options to regenerate, edit, copy, delete, or regenerate below (for user-generated content).

* Image browsing: For image generation, clicking on the image will open the image viewing window (ImageViewer), supporting saving images as PNG/UE Texture. Textures can be viewed directly in the Content Browser, facilitating image usage within the editor. Additionally, support for deleting images, regenerating images, continuing to generate more images, and other functions is available. For editors on Windows, copying images is also supported, allowing images to be directly copied to the clipboard for convenient use. Images generated during the session will also be automatically saved in each session folder, typically located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Blueprint:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Global settings:

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

###Introduction to the core code

Currently, the plug-in is divided into the following modules:

* AIChatPlusCommon: Runtime module responsible for handling various AI API interface requests and parsing response content.

AIChatPlusEditor: Editor module, responsible for implementing the AI chat tool editor.

* AIChatPlusCllama: Runtime module, responsible for encapsulating the interface and parameters of llama.cpp, achieving offline execution of large models

* Thirdparty/LLAMACpp: A third-party module at runtime, integrating the dynamic library and header files of llama.cpp.

The UClass responsible for sending requests is FAIChatPlus_xxxChatRequest, each API service has its own independent Request UClass. The responses to the requests are obtained through two different UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase UClass; it is only necessary to register the corresponding callback delegate.

Before sending the request, you need to set up the parameters and the message to be sent for the API. This is done through FAIChatPlus_xxxChatRequestBody. The specific response content is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving the callback, you can obtain the ResponseBody through a specific interface.

More source code details can be obtained from the UE Marketplace: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##User Guide

###Use the offline model llama.cpp for the editor tool.

The following instructions explain how to use the offline model llama.cpp in the AIChatPlus editor tool.

First, download the offline model from the HuggingFace website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Put the model in a specific folder, for example in the project directory Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Open the AIChatPlus editor tool: Tools -> AIChatPlus -> AIChat, create a new chat session, and open the session settings page.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Set the API to Cllama, enable Custom API Settings, add a model search path, and select a model.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Start chatting!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###The code uses the offline model llama.cpp.

The following explains how to use the offline model llama.cpp in the code.

First, you also need to download the model file to Content/LLAMA.

* Add a command in the code to send a message to the offline model within the command.

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

###Use the offline model blueprint llama.cpp.

The following explains how to use the offline model llama.cpp in the blueprint.

Create a node in the blueprint by right-clicking `Send Cllama Chat Request`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Create an Options node, and set `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Create Messages, add a System Message and a User Message separately.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Create a Delegate to receive the model's output information and print it on the screen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, run the blueprint, and you will see the message returned on the game screen when printing a large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###Blueprint uses OpenAI model

Create a node "Send OpenAI Chat Request In World" by right-clicking in the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Create an Options node and set `Stream=true, Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Create Messages, add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Create a `Delegate` to receive the model's output information and print it on the screen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, running the blueprint, you can see the message returned by the game screen printing the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Use Claude to analyze the blueprint.

Create a node `Send Claude Chat Request` by right-clicking in the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Create an Options node, and set `Stream=true, Api Key="your API key from Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Create Messages, create Texture2D from file, and create AIChatPlusTexture from Texture2D, then add AIChatPlusTexture to Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Just like the tutorial above, create an Event and print the information on the game screen.

The complete blueprint looks like this, run the blueprint, and you will see a message on the game screen printing the large model returned

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

###Blueprint using OpenAI to generate images

Create a node `Send OpenAI Image Request` by right-clicking in the blueprint, and set `In Prompt="a beautiful butterfly"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Create an Options node and set `Api Key="your api key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Bind the On Images event and save the images to the local hard disk.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

The complete blueprint looks like this, run the blueprint, and you will see the image saved at the specified location.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

##Release Notes

### v1.3.3 - 2024.11.25

####New feature

Support UE-5.5

####Problem fixing

Fix issues where some blueprints are not working.

### v1.3.2 - 2024.10.10

####Issue Fix

Fix crash when manually stopping request in cllama.

Repair the issue of not being able to find the ggml.dll and llama.dll files when packaging the Windows download version of the store.

When creating a request, check if it is in the GameThread.

### v1.3.1 - 2024.9.30

####New Feature

Add a SystemTemplateViewer to view and utilize hundreds of system setting templates.

####Problem fixed

Repair the plug-in downloaded from the mall, llama.cpp cannot find the linking library.

Fix LLAMACpp long path issue

Fix the llama.dll error after packaging Windows.

Fix the issue of reading file paths on ios/android.

Fix Cllame setting name error

### v1.3.0 - 2024.9.23

####A significant new feature

Integrated llama.cpp, supporting offline execution of large models locally

### v1.2.0 - 2024.08.20

####New feature

Support OpenAI Image Edit/Image Variation

Support Ollama API, support automatically obtaining the list of models supported by Ollama.

### v1.1.0 - 2024.08.07

####New feature

Support blueprint

### v1.0.0 - 2024.08.05

####New feature

Complete basic functionality

Support OpenAI, Azure, Claude, Gemini

Built-in feature-rich editor chat tool

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
