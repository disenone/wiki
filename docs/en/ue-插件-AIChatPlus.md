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

##Public warehouse

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Plugin acquisition

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introduction to the plugin

This plugin supports UE5.2+.

UE.AIChatPlus is a plugin for UnrealEngine that enables communication with various GPT AI chat services. Currently supported services include OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and local offline llama.cpp. Future updates will continue to support more service providers. Its implementation is based on asynchronous REST requests, ensuring high efficiency performance, and facilitating UE developers to integrate these AI chat services.

At the same time, UE.AIChatPlus also includes an editor tool that allows you to directly use these AI chat services in the editor to generate text and images, analyze images, and more.

##Instructions for Use

###Editor Chat Tool

Menu bar Tools -> AIChatPlus -> AIChat can open the editing chat tool provided by the plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chat, image generation, and image analysis.

The interface of the tool is roughly as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main Functions

Offline large-scale models: integrated llama.cpp library, supporting local offline execution of large-scale models

Text Chat: Click the `New Chat` button in the bottom left corner to start a new text chat session.

Image Generation: Click the `New Image Chat` button in the bottom left corner to start a new image generation session.

Image Analysis: Some messaging services in `New Chat` support sending images, such as Claude, Google Gemini. Click the 🖼️ or 🎨 button above the input box to load the image you want to send.

Support Blueprint: Support Blueprint to create API requests, complete text chat, image generation, and other functions.

Set the current chat role: The dropdown box above the chat box can be used to set the current role for sending text, allowing you to adjust AI chat by simulating different roles.

Clear chat: The ❌ button on the top of the chat box can clear the history of the current conversation.

Dialogue Template: With hundreds of built-in dialogue templates, it facilitates handling common issues.

**Global Settings:** Click the `Setting` button in the bottom left corner to open the global settings window. You can set default text chat, image generation API services, and configure specific parameters for each API service. The settings will be automatically saved in the project path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversation settings: Click on the settings button at the top of the chat box to open the settings window for the current conversation. You can modify the conversation name, the API service used for the conversation, and independently set specific parameters for each conversation's API. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Edit Chat Message: When hovering over a chat message, a settings button for that specific message will appear, allowing you to regenerate, edit, copy, or delete the content, as well as regenerate new content below (for content authored by users).

* Image browsing: For image generation, clicking on an image will open the image viewing window (ImageViewer), supporting saving images as PNG/UE Texture. Textures can be viewed directly in the Content Browser for easy use within the editor. Additionally, functionalities such as deleting images, regenerating images, and continuing to generate more images are supported. For editors on Windows, image copying is also supported, allowing images to be copied to the clipboard for easy use. Images generated during a session will also be automatically saved under each session folder, usually located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Blueprint:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Global Settings:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Conversation settings:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Modify chat content:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Image Viewer:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Use offline large models.

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Dialogue template

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introduction to Core Code

Currently, the plugin is divided into the following modules:

AIChatPlusCommon: Runtime module, responsible for handling various AI API interface requests and parsing reply contents.

* AIChatPlusEditor: Editor module, responsible for implementing the AI chat tool editor.

* AIChatPlusCllama: Runtime module responsible for encapsulating the interface and parameters of llama.cpp, enabling offline execution of large models

* Thirdparty/LLAMACpp: Runtime third-party module, integrating llama.cpp dynamic library and header files.

The `UClass` responsible for sending requests is `FAIChatPlus_xxxChatRequest`, each API service has its own independent `Request UClass`. The response to the request is obtained through two `UClass`: `UAIChatPlus_ChatHandlerBase` and `UAIChatPlus_ImageHandlerBase`, you just need to register the corresponding callback delegate.

Before sending a request, you need to set up the API parameters and the message to be sent. This is done by setting up the FAIChatPlus_xxxChatRequestBody. The specific content of the reply is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving a callback, you can obtain the ResponseBody through a specific interface.

More source code details can be found on the UE Marketplace: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##User Guide

###Use the offline model llama.cpp with the editor tool.

The following explains how to use the offline model llama.cpp in the AIChatPlus editor tool.

First, download the offline model from the HuggingFace website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Put the model in a specific folder, for example, place it in the Content/LLAMA directory of the game project.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Open the AIChatPlus editor tool: Tools -> AIChatPlus -> AIChat, create a new chat session, and open the session settings page.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Set the API to Cllama, enable Custom API Settings, add model search paths, and select a model.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Let's start chatting!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###The code uses the offline model llama.cpp.

The following explains how to use the offline model llama.cpp in the code.

First, you also need to download the model files to Content/LLAMA.

Add a command to the code and send a message to the offline model inside the command.

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

Create an Options node and set `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Create Messages, add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Create a delegate to receive the model's output information and print it on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, run the blueprint, and you will see the message returned on the game screen printing a large model

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###Use OpenAI model for blueprint

Create a node `Send OpenAI Chat Request In World` by right-clicking in the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Create an Options node and set `Stream=true, Api Key="your API key from OpenAI"` as the values.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Create Messages, and add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Create a Delegate to receive the output information from the model and print it on the screen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this. When you run the blueprint, you can see the message returned by the game screen printing the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Use Claude to analyze images in the blueprint.

Create a node `Send Claude Chat Request` by right-clicking in the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Create an Options node, and set `Stream=true, Api Key="your api key from Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

* Create Messages, create a Texture2D from a file, and create AIChatPlusTexture from Texture2D, then add AIChatPlusTexture to Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Just like the tutorial above, create an Event and print the information on the game screen.

The complete blueprint looks like this, run the blueprint, and you will see the message returned on the game screen when printing a large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

###Use OpenAI to create images.

Create a node `Send OpenAI Image Request` by right-clicking in the blueprint, and set `In Prompt="a beautiful butterfly"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Create an Options node, and set `Api Key="your api key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Bind the *On Images* event and save the image to the local hard drive.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

The complete blueprint looks like this. Run the blueprint, and you will see the image saved in the specified location.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

##Update Log

### v1.3.3 - 2024.11.25

Support UE-5.5

* **Bugfix**: Fixed an issue where some blueprints were not taking effect

### v1.3.2 - 2024.10.10

#### Bugfix

Fix crash when manually stopping request in cllama

Fix the issue of not finding the ggml.dll and llama.dll files when packaging the Win download version of the mall.

Check whether it is in the GameThread when creating a request.

### v1.3.1 - 2024.9.30

Create a SystemTemplateViewer to view and use hundreds of system setting templates.

#### Bugfix

Fix the plugin downloaded from the store, llamacpp cannot find the linked library.

Fix the issue of LLAMACpp path being too long

Repair the llama.dll error in Windows packaging.

Fix iOS/Android file path reading issue.

Fix Cllame setting name error

### v1.3.0 - 2024.9.23

Major Update

Integrated llama.cpp to support local offline execution of large models.

### v1.2.0 - 2024.08.20

Support OpenAI Image Edit/Image Variation

Support Ollama API, support automatically getting the list of models supported by Ollama.

### v1.1.0 - 2024.08.07

Support the blueprint.

### v1.0.0 - 2024.08.05

Full functionality.

Support OpenAI, Azure, Claude, and Gemini.

Built-in feature-rich editor chat tool.

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
