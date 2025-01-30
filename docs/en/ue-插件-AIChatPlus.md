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

##Plugin acquisition

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Plugin overview

This plugin supports UE5.2+.


UE.AIChatPlus is a plugin for Unreal Engine that facilitates communication with various GPT AI chat services. Currently supported services include OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and llama.cpp for local offline use. It will continue to support more service providers in the future. Its implementation is based on asynchronous REST requests, ensuring high performance and convenience for UE developers to integrate these AI chat services.

At the same time, UE.AIChatPlus also includes an editor tool that allows users to directly utilize these AI chat services within the editor to generate text and images, analyze images, and more.

##User Instructions

###Editor chat tool

The menu bar Tools -> AIChatPlus -> AIChat opens the chat tool editor provided by the plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chatting, image generation, and image analysis.

The interface of the tool is roughly as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main functions

* Offline large model: Integrates the llama.cpp library, supporting local offline execution of large models.

Text Messaging: Click the `New Chat` button in the lower left corner to start a new text messaging conversation.

* Image Generation: Click the `New Image Chat` button in the lower left corner to create a new image generation session.

* Image Analysis: The chat services in `New Chat` support sending images, such as Claude and Google Gemini. Click the 🖼️ or 🎨 button above the input box to load the image you want to send.

Support Blueprint: Support Blueprint for creating API requests, enabling features such as text chat and image generation.

Set the current chat role: The dropdown box above the chat box can be used to set the current role for sending text, allowing you to adjust the AI chat by simulating different roles.

* Clear conversation: The ❌ button at the top of the chat box can clear the history of the current conversation.

Dialogue Template: There are built-in hundreds of dialogue setting templates for easily handling common issues.

Global settings: Click the 'Setting' button in the bottom left corner to open the global settings window. You can configure default text chat, image generation API services, and specify parameters for each API service. The settings will be automatically saved in the project path '$(ProjectFolder)/Saved/AIChatPlusEditor'.

Conversation Settings: Click on the settings button at the top of the chat box to open the setting window for the current conversation. You can modify the conversation name, change the API service used for the conversation, and independently set specific parameters for each conversation's API. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

* Chat content modification: Hovering the mouse over the chat content will display a settings button for that specific chat content, which supports regenerating content, modifying content, copying content, deleting content, and regenerating content below (for content where the role is the user).

Image browsing: For image generation, clicking on an image will open the image viewing window (ImageViewer). It supports saving images as PNG/UE Texture, which can be viewed directly in the Content Browser for easy use in the editor. Additionally, it also supports functions such as deleting images, regenerating images, and generating more images. For editors on Windows, it also supports copying images, allowing images to be copied directly to the clipboard for convenient use. Images generated during sessions are automatically saved in each session folder, typically located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

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

Use offline large model

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Dialogue template

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introduction to Core Code

The plugin is currently divided into the following modules:

* AIChatPlusCommon: Runtime module, responsible for handling requests sent through various AI API interfaces and parsing the response content.

AIChatPlusEditor: Editor module, responsible for implementing the AI chat tool in the editor.

AIChatPlusCllama: Runtime module, responsible for encapsulating the interface and parameters of llama.cpp, achieving offline execution of large models.

Thirdparty/LLAMACpp: Runtime third-party module which integrates llama.cpp dynamic library and header files.

The specific UClass responsible for sending requests is FAIChatPlus_xxxChatRequest, and each API service has its own independent Request UClass. The responses to the requests are obtained through two UClasses: UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase, only requiring the registration of the corresponding callback delegate.

Before sending a request, you need to set the API parameters and the message to be sent. This is done through FAIChatPlus_xxxChatRequestBody. The specific content of the reply is also parsed into FAIChatPlus_xxxChatResponseBody, and when you receive a callback, you can obtain the ResponseBody through a specific interface.

More source code details are available on the UE Marketplace: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Use the offline model Cllama (llama.cpp) in the editor tool.

The following explains how to use the offline model llama.cpp in the AIChatPlus editor tool.

* First, download the offline model from the HuggingFace website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Place the model in a specific folder, such as under the game's project directory Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

* Open the AIChatPlus editor tool: Tools -> AIChatPlus -> AIChat, create a new chat session, and open the session settings page.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

* Set the API to Cllama, enable Custom API Settings, add the model search path, and select the model.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

* Start chatting!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Use the offline model Cllama (llama.cpp) in the editor tool to process images.

* Download the offline model MobileVLM_V2-1.7B-GGUF from the HuggingFace website and place it in the directory Content/LLAMA: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)and [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)。

* Set the model for the session:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

* Send a picture to start a chat

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###The code uses the offline model Cllama(llama.cpp).

The following explains how to use the offline model llama.cpp in the code.

First, you'll also need to download the model files to Content/LLAMA.

* Modify the code to add a command and send a message to the offline model within that command.

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

After recompiling, you can use the command in the editor's Cmd to see the output results of the large model in the log OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###The blueprint uses the offline model llama.cpp.

The following explains how to use the offline model llama.cpp in Blueprints.

* Right-click in the blueprint to create a node `Send Cllama Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Create an Options node and set `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Create Messages, respectively adding a System Message and a User Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Create a delegate to receive the output information from the model and print it on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* The complete blueprint looks like this: run the blueprint, and you will see the game screen displaying the messages returned by the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###The editor uses OpenAI for chatting.

* Open the chat tool Tools -> AIChatPlus -> AIChat, create a new chat session New Chat, set the session ChatApi to OpenAI, and configure the interface parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Start chatting:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Switching the model to gpt-4o / gpt-4o-mini allows for utilizing OpenAI's visual capabilities to analyze images.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###The editor uses OpenAI to handle images (create/modify/variant).

Create a new Image Chat in the messaging tool, modify the conversation settings to OpenAI, and configure the parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

* Create Image

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Edit the image by changing the Image Chat Type to Edit, and upload two images. One image should be the original image, and the other should show the areas to be modified, with transparency (where the alpha channel is 0).

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Modify the image chat type to "Variation" and upload an image. OpenAI will generate a variant of the original image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Blueprint uses OpenAI model chat.

* Right-click in the blueprint to create a node `Send OpenAI Chat Request In World`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Create an Options node, and set `Stream=true, Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

* Create Messages, adding a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Create a Delegate to receive the model output information and print it on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, running the blueprint will show the message printed on the game screen when creating a large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Blueprint uses OpenAI to create images.

In the blueprint, right-click to create a node named "Send OpenAI Image Request" and set "In Prompt" to "a beautiful butterfly".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Create an Options node and set `Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Bind the On Images event and save the images to the local hard drive.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

* The complete blueprint looks like this. Run the blueprint to see the image saved in the specified location.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###The editor uses Azure.

Create a new chat session, change ChatApi to Azure, and configure Azure's API parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###The editor uses Azure to create images.

Create a new image chat session, change ChatApi to Azure, and configure Azure's API parameters. Note that if using the dall-e-2 model, Quality and Stype parameters should be set to not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

* Start chatting and let Azure create images.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Blueprint uses Azure chat.

Create the blueprint as outlined, configure the Azure Options, click on run, and you will see the chat information returned by Azure printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Use Azure to create images according to the blueprint.

Create the following blueprint, configure Azure Options, click Run, if the image creation is successful, you will see the message "Create Image Done" on the screen. 

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

According to the settings in the blueprint above, the image will be saved at the path D:\Downloads\butterfly.png.

## Claude

###The editor employs Claude for chatting and analyzing images.

Create a new chat session, change ChatApi to Claude, and configure Claude's API parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Start chatting.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Blueprint uses Claude for chatting and image analysis.

Create a node in the blueprint by right-clicking and naming it 'Send Claude Chat Request'.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

* Create an Options node, and set `Stream=true, Api Key="you api key from Clude", Max Output Tokens=1024`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Create Messages, create a Texture2D from a file, then create an AIChatPlusTexture from the Texture2D, and add the AIChatPlusTexture to the Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Just like the tutorial above, create an Event and print the information on the game screen.

The complete blueprint looks like this, run the blueprint, and you can see the message returned by the game screen when printing the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Acquire Ollama.

You can download the installation package for local installation from the Ollama official website: [ollama.com](https://ollama.com/)

You can use Ollama through the Ollama interface provided by others.

###The editor uses Ollama for chatting and analyzing images.

* Start a new chat, change ChatApi to Ollama, and set the API parameters for Ollama. If it's a text chat, set the model to a text model, like llama3.1; if you need to process images, set the model to one that supports vision, such as moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

* Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Use Ollama blueprint for chatting and analyzing images.

Create the following blueprint, configure the Ollama Options, click Run, and you will see the chat information returned by Ollama printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###Editor uses Gemini

* Start a new session (New Chat), change ChatApi to Gemini, and set the Gemini API parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###The editor uses Gemini to send audio.

Choose to read audio from a file, from an asset, or record audio from a microphone to generate the audio that needs to be sent.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

* Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###Blueprint uses Gemini chat.

Create the following blueprint, configure the Gemini Options, click on Run, and you will see the chat information returned by Gemini printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###The blueprint uses Gemini to send audio.

Create the following blueprint, set up the audio loading, configure the Gemini Options, click run, and you will see the chat information returned by Gemini after processing the audio printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###The editor utilizes Deepseek.

* Create a new chat, change ChatApi to OpenAi, and set the Deepseek API parameters. Add a Candidate Model named deepseek-chat and set the Model to deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Start chatting.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Blueprint uses Deepseek chat.

Create the following blueprint, set up the Request Options related to Deepseek, including parameters such as Model, Base Url, End Point Url, ApiKey, etc. Click on run, and you will be able to see the chat information returned by Gemini printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##Release Notes

### v1.5.1 - 2025.01.30

####New feature

* Only Gemini is allowed to pronounce audio.

* Optimize the method for obtaining PCMData by decompressing the audio data when generating B64.

Please increase two callbacks OnMessageFinished and OnImagesFinished.

Optimize the Gemini Method to automatically retrieve the Method based on bStream.

Add some blueprint functions to easily convert Wrapper to actual types, and retrieve Response Message and Error.

#### Bug Fix

* Fix the issue of multiple calls to Request Finish.

### v1.5.0 - 2025.01.29

####New Feature

Support sending audio to Gemini.

The editor tool supports sending audio and recordings.

#### Bug Fix

Fix the bug that causes Session copy to fail.

### v1.4.1 - 2025.01.04

####Problem fixing

* The chat tool supports sending only images without text.

Repair failed documentation image for OpenAI interface picture sending issue

* Fix the issue where the parameters Quality, Style, and ApiVersion were omitted in the settings for OpanAI and Azure chat tools.

### v1.4.0 - 2024.12.30

####New feature

*(Experimental feature) Cllama (llama.cpp) supports multimodal models and can handle images.

* All blueprint type parameters have detailed hints added.

### v1.3.4 - 2024.12.05

####New features

* OpenAI supports vision API

####Problem Fixing

Fix the error when OpenAI stream=false.

### v1.3.3 - 2024.11.25

####New feature

* Supports UE-5.5

####Issue resolution

Fix the issue where some blueprints are not taking effect.

### v1.3.2 - 2024.10.10

####Issue Resolution

* Fix the crash of cllama when manually stopping the request.

Fix the issue where the download version of the win package in the mall cannot find the ggml.dll llama.dll files.

Check if you are on the GameThread when creating a request.

### v1.3.1 - 2024.9.30

####New features

Add a SystemTemplateViewer, where users can view and utilize hundreds of system setting templates.

####Problem resolved

* Fix the plugin downloaded from the mall, llama.cpp cannot find the link library.

Fix the issue of LLAMACpp path being too long

Fix the llama.dll error in the Windows package after compilation.

Fix the issue with reading file paths on iOS/Android.

Fix Cllame setting name error

### v1.3.0 - 2024.9.23

####Major New Feature

* Integrated with llama.cpp, supporting local offline execution of large models.

### v1.2.0 - 2024.08.20

####New feature

Support OpenAI Image Edit/Image Variation

* Supports Ollama API, allows for automatic retrieval of the list of models supported by Ollama.

### v1.1.0 - 2024.08.07

####New feature.

Support blueprints.

### v1.0.0 - 2024.08.05

####New Features

* Complete basic functionality

* Supports OpenAI, Azure, Claude, Gemini

Built-in feature-rich chat tool editor

--8<-- "footer_en.md"


> This post has been translated using ChatGPT. Please provide [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Please point out any omissions. 
