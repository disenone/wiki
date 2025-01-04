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

##Plugin acquisition

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Plugin Introduction

This plugin supports UE5.2+.

UE.AIChatPlus is a plugin for Unreal Engine that allows communication with various GPT AI chat services. Currently supported services include OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and local offline support for llama.cpp. More service providers will be supported in the future. It is implemented based on asynchronous REST requests, offering high performance and making it easy for Unreal Engine developers to integrate these AI chat services.

UE.AIChatPlus also includes an editor tool that allows you to use these AI chat services directly within the editor, generating text and images, analyzing images, and more.

##Instructions for use

###Editor chatting tool

Menu Bar: Tools -> AIChatPlus -> AIChat can open the editor chat tool provided by the plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chat, image generation, and image analysis.

The interface of the tool is roughly as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main functions

Offline large-scale model: Integrated llama.cpp library, supports local offline execution of large models.

Text chat: Click the `New Chat` button in the bottom left corner to start a new text chat conversation.

Image Generation: Click the 'New Image Chat' button in the bottom left corner to start a new image generation session.

Image analysis: Part of the chat service in `New Chat` supports sending images, such as Claude, Google Gemini. Click the 🖼️ or 🎨 button above the input box to load the image you want to send.

Support blueprint: support blueprint creation for API requests, enabling functions such as text chat and image generation.

Set the current chat character: The dropdown menu at the top of the chat box can be used to select the current character for sending text, allowing you to adjust the AI chat by simulating different characters.

Clear Chat: Clicking on the ❌ icon above the chat box clears the history of the current conversation.

Dialogue Template: Built-in hundreds of dialogue setting templates, making it easy to handle common issues.

Global Settings: Click on the 'Setting' button in the bottom left corner to open the global settings window. You can configure default text chat, image generation API services, and customize parameters for each API service. The settings will be automatically saved in the project directory `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Conversation Settings: Click the settings button at the top of the chat box to open the settings window for the current conversation. You can change the conversation name, modify the API service used in the conversation, and independently set specific parameters for each conversation. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Edit Chat Content: Hovering over a chat message will display individual message settings, supporting options to regenerate, edit, copy, delete, regenerate below (for messages authored by users).

* Image browsing: For image generation, clicking on an image will open an image viewing window (ImageViewer), supporting saving images as PNG/UE Texture. Textures can be directly viewed in the Content Browser, facilitating image usage within the editor. Additionally, functions such as deleting images, regenerating images, and continuing to generate more images are supported. For editors on Windows, image copying is also supported, allowing images to be copied directly to the clipboard for ease of use. Images generated during sessions will automatically be saved under each session folder, typically located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Blueprint:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Global settings:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Conversation settings:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Edit chat content:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Image Viewer:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Using offline large models

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Dialogue template

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introduction to the core code

The plugins are currently divided into the following modules:

AIChatPlusCommon: Runtime module, responsible for handling various AI API interface requests and parsing response content.

AIChatPlusEditor: Editor module responsible for implementing AI chat tools in the editor.

AIChatPlusCllama: Runtime module, responsible for encapsulating the interface and parameters of llama.cpp, achieving offline execution of large models.

Thirdparty/LLAMACpp: Runtime third-party module that integrates llama.cpp dynamic library and header files.

The UClass responsible for sending requests is FAIChatPlus_xxxChatRequest. Each API service has its own independent Request UClass. Replies to requests are obtained through two UClass, UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase, by registering the corresponding callback delegate.

Before sending a request, you need to set up the API parameters and the message to be sent. This is done by setting up the FAIChatPlus_xxxChatRequestBody. The specific content of the reply is also parsed into FAIChatPlus_xxxChatResponseBody. When you receive the callback, you can obtain the ResponseBody through a specific interface.

More source code details can be obtained from the UE Marketplace: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###The editor tool uses the offline model Cllama (llama.cpp).

The following explains how to use the offline model llama.cpp in the AIChatPlus editor tool.

First, download the offline model from the HuggingFace website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Place the model in a specific folder, for example, put it in the Content/LLAMA directory of the game project.

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

###The editing tool uses the offline model Cllama(llama.cpp) to process images.

Download the offline model MobileVLM_V2-1.7B-GGUF from the HuggingFace website and place it in the directory Content/LLAMA: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)Translate these text into English language:

And [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)。

Set the session model:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Start chatting by sending a picture.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###The code uses the offline model Cllama (llama.cpp).

The following instructions explain how to use the offline model llama.cpp in the code.

First, you also need to download the model file to Content/LLAMA.

Update the code to include a new command, and send a message to the offline model within the command.

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

After recompiling, you can use the command in the Cmd editor to see the output results of the large model in the OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Blueprint uses the offline model llama.cpp.

The following instructions explain how to use the offline model llama.cpp in the blueprint.

Create a node `Send Cllama Chat Request` with a right-click on the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Create an Options node and set `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Create Messages, add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Create a delegate to receive the model's output information and print it on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, run the blueprint, and you will see the message returned on the game screen printing large models.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###The editor uses OpenAI chat.

Open the chat tool, go to Tools -> AIChatPlus -> AIChat, create a new chat session, set the session to ChatApi as OpenAI, and configure the interface parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Start chatting:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Switching the model to GPT-4o / GPT-4o-mini allows for the use of OpenAI's visual feature to analyze images.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###The editor uses OpenAI to process images (create/modify/alter).

Create a new image chat session in the messaging tool, name it "New Image Chat," adjust the session settings to OpenAI, and configure the parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Create image

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Edit the image by changing the Image Chat Type to Edit, and upload two images: one original image and another with the areas to be modified highlighted in a mask where transparency (with alpha channel set to 0).

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Alter the image variant by changing the Image Chat Type to Variation, and upload an image. OpenAI will provide a variant of the original image in return.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Use OpenAI models to chat with blueprints.

Create a node `Send OpenAI Chat Request In World` by right-clicking on the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Create an Options node and set `Stream=true, Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Create Messages, and add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Create a delegate to receive the model's output information and print it on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, run the blueprint, and you will see the message printed on the game screen returning a large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Blueprint using OpenAI to create images

Create a node called `Send OpenAI Image Request` in the blueprint by right-clicking, and set `In Prompt="a beautiful butterfly"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Create an Options node and set `Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Bind the On Images event and save the image to the local hard drive.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

The complete blueprint looks like this, run the blueprint, and you will see the image saved in the specified location.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###The editor uses Azure.

Create a new chat session, change ChatApi to Azure, and configure Azure's API parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###The editor uses Azure to create images.

Create a new image chat session, change ChatApi to Azure, and configure Azure's API parameters. Please note that if using the dall-e-2 model, set the Quality and Stype parameters to not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Start chatting to let Azure create an image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Use Azure Chat for blueprint.

Create the following blueprint, set up the Azure Options, click on run, and you will see the chat information returned by Azure printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Create images with Azure Blueprint.

Create the following blueprint, configure the Azure Options, click on Run. If the image creation is successful, you will see the message "Create Image Done" on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

According to the settings in the blueprint above, the image will be saved at the path D:\Downloads\butterfly.png.

## Claude

###The editor uses Claude to chat and analyze images.

Create a new chat session, change ChatApi to Claude, and configure Claude's API parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Use Claude to chat and analyze images in the blueprint.

Create a node `Send Claude Chat Request` by right-clicking in the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Create an Options node, and set `Stream=true, Api Key="you api key from Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Create Messages, create a Texture2D from a file, and create AIChatPlusTexture from Texture2D, then add AIChatPlusTexture to Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Create an Event just like the tutorial above and print the information on the game screen.

The complete blueprint looks like this, run the blueprint, and you will see the message printed on the game screen for the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Obtain Ollama

You can download the installation package locally from the Ollama official website: [ollama.com](https://ollama.com/)

You can use Ollama through the Ollama interface provided by others.

###The editor uses Ollama for chatting and analyzing images.

Create a new chat session, change ChatApi to Ollama, and configure Ollama's Api parameters. If it's a text chat, set the model to a text model, such as llama3.1; if you need to handle images, set the model to a vision-enabled model, such as moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###The blueprint uses Ollama for chatting and analyzing images.

Create the following blueprint, set up the Ollama Options, click on Run, and you will see the chat information returned by Ollama printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###Editor uses Gemini

Create a new chat session, change ChatApi to Gemini, and configure Gemini's API parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###Blueprint using Gemini chat

Create the following blueprint, configure the Gemini Options, click run, and you will see the chat information returned by Gemini printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

## Deepseek

###The editor utilizes Deepseek.

Create a new chat session, change ChatApi to OpenAi, and configure the API parameters for Deepseek. Add a new candidate model named deepseek-chat, and set the model to deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Blueprint using Deepseek chat

Create the following blueprint, set up the Request Options related to Deepseek, including Model, Base Url, End Point Url, ApiKey, and other parameters. Click on run, and you will see the chat information returned by Gemini printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##Change log

### v1.4.1 - 2025.01.04

####Problem fixed

The chat tool supports sending only pictures without messages.

Repair OpenAI interface failed to send image documents.

Fix the missing parameters Quality, Style, and ApiVersion in the OpanAI and Azure chat tool settings.

### v1.4.0 - 2024.12.30

####New Feature

* (Experimental Feature) Cllama (llama.cpp) supports multi-modal models and can handle images.

All blueprint type parameters have been provided with detailed prompts.

### v1.3.4 - 2024.12.05

####New Feature

OpenAI supports vision API.

####Issue resolution

Fix the error when OpenAI stream=false.

### v1.3.3 - 2024.11.25

####New feature

Support UE-5.5

####Problem fixing

Fix the issue of some blueprints not taking effect.

### v1.3.2 - 2024.10.10

####Problem Fixing

Fix crash when manually stopping cllama request.

Fix the issue of missing ggml.dll and llama.dll files when packaging the win version of the mall download.

Ensure the request is created within the GameThread.

### v1.3.1 - 2024.9.30

####New feature

Add a SystemTemplateViewer, which allows you to view and use hundreds of system setting templates.

####Problem fixed

Fix the plugin downloaded from the store, llama.cpp cannot find the link library.

Fix LLAMACpp path too long issue

Fix the llama.dll error after packaging Windows.

Fixing the file path reading issue on iOS/Android.

Fix Cllame setting name error.

### v1.3.0 - 2024.9.23

####Significant new feature

Integrated llama.cpp to support local offline execution of large models.

### v1.2.0 - 2024.08.20

####New feature

Support OpenAI Image Edit/Image Variation.

Support the Ollama API and automatically retrieve the list of models supported by Ollama.

### v1.1.0 - 2024.08.07

####New feature

Support blueprint

### v1.0.0 - 2024.08.05

####New feature

Complete foundational functionality

Support OpenAI, Azure, Claude, Gemini.

Built-in feature-rich editor chat tool

--8<-- "footer_en.md"


> This post has been translated using ChatGPT. Please provide feedback in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
