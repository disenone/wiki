---
layout: post
title: UE plugin AIChatPlus documentation
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

##Public repository

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Obtain plugin.

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Introduction to the plugin

This plugin supports UE5.2+.

UE.AIChatPlus is a UnrealEngine plugin that enables communication with various GPT AI chat services. Currently, it supports services such as OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and llama.cpp for local offline processing. In the future, more service providers will be supported. Its implementation is based on asynchronous REST requests, ensuring high performance and making it convenient for UE developers to integrate these AI chat services.

At the same time, UE.AIChatPlus also includes an editor tool that allows you to directly use these AI chat services in the editor to generate text and images, analyze images, and more.

##Instructions for use

###Editor chat tool

Menu bar Tools -> AIChatPlus -> AIChat can open the chat tool editor provided by the plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chatting, image generation, and image analysis.

The interface of the tool is roughly as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main Functions

Offline Large Model: Integrated llama.cpp library, supporting local offline execution of large models

Text Chat: Click the `New Chat` button in the bottom left corner to create a new text chat session.

Image Generation: Click the `New Image Chat` button in the bottom left corner to create a new image generation session.

Image Analysis: Some chat services in `New Chat` support sending images, such as Claude, Google Gemini. You can click the 🖼️ or 🎨 button above the input box to load the image you want to send.

Support Blueprint: Support Blueprint for creating API requests, completing text chatting, image generation, and other functions.

Set the current chat role: The dropdown menu at the top of the chat box can set the current role for sending text. You can simulate different roles to adjust the AI chat.

Clear the conversation: Clicking the ❌ icon above the chat box clears the history of the current conversation.

Dialogue Template: Built-in hundreds of dialogue setting templates, making it convenient to handle common issues.

Global Settings: Click on the `Setting` button in the bottom left corner to open the global settings window. You can configure default text chat, image generation API services, and specify parameters for each API service. The settings will be automatically saved in the project path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversation Settings: Click the settings button at the top of the chat box to open the settings window for the current conversation. You can modify the conversation name, change the API service used for the conversation, and independently adjust the specific parameters for each conversation's API usage. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Chat Content Editing: When hovering over the chat content, a settings button for that specific content will appear, supporting options to regenerate, edit, copy, or delete the content. Additionally, there is an option to regenerate the content below (for content created by users).

* Image browsing: For image generation, clicking on an image will open the image viewing window (ImageViewer). It supports saving images as PNG/UE Texture. Textures can be directly viewed in the Content Browser, making it convenient to use images within the editor. Additionally, it supports functions like deleting images, regenerating images, and generating more images. For editors on Windows, copying images is also supported, allowing images to be copied directly to the clipboard for convenient use. Images generated during sessions will be automatically saved in each session folder, usually located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Blueprint:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Global Settings:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Conversation Settings:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Edit chat content:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Image viewer:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Use offline large-scale models.

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Dialogue Template

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introduction to the Core Code

The plugins are currently divided into the following modules:

AIChatPlusCommon: Runtime module, responsible for handling various AI API interface requests and parsing reply content.

AIChatPlusEditor: Editor module, responsible for implementing the AI chat tool in the editor.

AIChatPlusCllama: Runtime module, responsible for encapsulating the interface and parameters of llama.cpp, achieving offline execution of large models

* Thirdparty/LLAMACpp: Runtime third-party module integrating the dynamic library and header files of llama.cpp.

The UClass specifically responsible for sending requests is FAIChatPlus_xxxChatRequest. Each API service has its own independent Request UClass. The responses to the requests are obtained through two types of UClass - UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase; it is only necessary to register the corresponding callback delegate.

Before sending a request, you need to set up the parameters and the message to be sent for the API, which is done through FAIChatPlus_xxxChatRequestBody. The specific reply is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving a callback, you can retrieve the ResponseBody through a specific interface.

More source code details can be obtained from the UE store: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Use offline model Cllama (llama.cpp) in the editor tool.

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

Start chatting!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Use the offline model editor tool Cllama(llama.cpp) to process images.

Download the offline model MobileVLM_V2-1.7B-GGUF from the HuggingFace website and place it in the directory Content/LLAMA as well: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)Translate these text into English language:

和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf).

Set the session model:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Start chatting by sending a picture.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###Code uses offline model Cllama(llama.cpp)

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

After recompiling, you can see the output results of the large model in the log OutputLog by using commands in the editor Cmd.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###The blueprint utilizes the offline model llama.cpp.

The following instructions explain how to use the offline model llama.cpp in the blueprint.

Right-click in the blueprint to create a node `Send Cllama Chat Request`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Create an Options node, and set `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

* Create Messages and add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Create a Delegate that accepts the model's output information and prints it on the screen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, run the blueprint, and you will see the message returning on the game screen as it prints a large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###The editor uses OpenAI chat.

Open the chat tool Tools -> AIChatPlus -> AIChat, create a new chat session New Chat, set the session ChatApi to OpenAI, set <api_key>.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

* Start chatting:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Switch the model to gpt-4o / gpt-4o-mini, you can use OpenAI's visual feature to analyze images.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###The editor uses OpenAI to process images (create/modify/variate).

Create a new image conversation New Image Chat in chat creation fear, modify session settings to OpenAI, and set <api_key>.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

* Create Image

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

* Edit the image, change the Image Chat Type to Edit, and upload two images. One image is the original image, and the other image is the mask where the transparent areas (with an alpha channel of 0) indicate the parts that need to be modified.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Convert the image variant by changing the Image Chat Type to Edit, and upload an image. OpenAI will provide a variant of the original image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Use OpenAI models to chat about blueprints

Create a node in the blueprint with the title `Send OpenAI Chat Request In World` by right-clicking.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Create an Options node, and set `Stream=true, Api Key="your api key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Create Messages, add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Create a Delegate that accepts the model's output information and prints it on the screen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, run the blueprint, and you will see the game screen printing a message returning a large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###The plan uses OpenAI to create images.

Create a node `Send OpenAI Image Request` in the blueprint by right-clicking, and set `In Prompt="a beautiful butterfly"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Create an Options node, and set `Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Bind the "On Images" event and save the images to the local hard drive.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

The complete blueprint looks like this. Run the blueprint and you will see the image saved at the specified location.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_5.png)

## Azure

###The editor uses Azure.

Create a new session (New Chat), change ChatApi to Azure, and configure Azure's API parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###The editor uses Azure to create images.  

Create a new image chat session, change ChatApi to Azure, and set Azure's API parameters. Please note, if using the dall-e-2 model, make sure to set the Quality and Style parameters to not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Start chatting, let Azure create an image

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Use Azure Chat for the blueprint concept

Create the following blueprint, configure the Azure Options, click run, and you will see the chat information returned by Azure printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Create an image using Azure Blueprint.

Create the following blueprint, set up the Azure Options, click Run, and if the image creation is successful, you will see the message "Create Image Done" on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

According to the settings in the blueprint above, the image will be saved in the path D:\Downloads\butterfly.png.

## Claude

###The editor uses Claude to chat and analyze images.

Create a new conversation (New Chat), change ChatApi to Claude, and configure Claude's API parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Blueprint uses Claude to chat and analyze images

Create a node `Send Claude Chat Request` in the blueprint by right-clicking.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Create an Options node and set `Stream=true, Api Key="your API key from Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

* Create Messages, create Texture2D from file, and create AIChatPlusTexture from Texture2D, then add AIChatPlusTexture to Message

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Just like in the tutorial above, create an Event and print the information on the game screen.

The complete blueprint looks like this, run the blueprint, and you will see the game screen printing the message returned by the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Obtain Ollama

You can download the installation package locally from the Ollama official website: [ollama.com](https://ollama.com/)

You can use Ollama through the Ollama API provided by others.

###The editor uses Ollama for chatting and analyzing images.

Create a new chat session, change ChatApi to Ollama, and set Ollama's API parameters. If it's text chat, set the model to a text model like llama3.1; if you need to handle images, set the model to a vision-supporting model, for example, moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Blueprint uses Ollama to chat and analyze images

Create the blueprint as follows, set the Ollama Options, click Run, and you will see the chat information returned by Ollama printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###The editor uses Gemini.

Create a new chat session (New Chat), change ChatApi to Gemini, and configure Gemini's Api parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Use Gemini chat for blueprint collaboration.

Create the following blueprint, set up the Gemini Options, click Run, and you will see the chat information returned by Gemini printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)


##Release Notes

### v1.4.0 - 2024.12.30

####New Feature

*(Experimental Feature)* Cllama (llama.cpp) supports multi-modal models and can handle images.

All the blueprint type parameters have been given detailed hints.

### v1.3.4 - 2024.12.05

####New Features

OpenAI supports the vision API.

####Problem fixing

Fix the error when OpenAI stream=false

### v1.3.3 - 2024.11.25

####New Feature

Support UE-5.5

####Issue fixing

Fix the issue of some blueprints not taking effect.

### v1.3.2 - 2024.10.10

####Problem fixed

Fix crash in cllama when stopping the request manually

Fix the issue where the win deployment of the mall cannot find the ggml.dll and llama.dll files.

Check whether it is in the GameThread when creating a request.

### v1.3.1 - 2024.9.30

####New feature

Add a SystemTemplateViewer that allows users to view and utilize hundreds of system setting templates.

####Issue resolution

Repair plug-ins downloaded from the mall, llama.cpp cannot find the linked library.

Fix the issue of LLAMACpp path being too long

Fix the Link Error of llama.dll After Packaging Windows

Fix the issue of reading file paths on iOS/Android.

Fix Cllame setting name error

### v1.3.0 - 2024.9.23

####Major New Feature

Integrated llama.cpp to support local offline execution of large models.

### v1.2.0 - 2024.08.20

####New feature

Support OpenAI Image Edit/Image Variation

Support Ollama API, support automatically fetching the list of models supported by Ollama.

### v1.1.0 - 2024.08.07

####New Feature

Support blueprint

### v1.0.0 - 2024.08.05

####New feature

Complete Basic Features

Support OpenAI, Azure, Claude, Gemini

A self-contained feature-rich editor chat tool.

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
