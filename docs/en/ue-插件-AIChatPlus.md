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

##Plugin introduction.

This plugin supports UE5.2+.

UE.AIChatPlus is a UnrealEngine plugin that enables communication with various GPT AI chat services. Currently, it supports services such as OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and local offline llama.cpp. In the future, more service providers will be supported. Its implementation is based on asynchronous REST requests, ensuring high performance and making it convenient for UnrealEngine developers to integrate these AI chat services.

UE.AIChatPlus also includes an editor tool that allows users to directly utilize these AI chat services in the editor, generating text and images, analyzing images, and more.

##Instructions for Use

###Editor chat tool

Menu bar Tools -> AIChatPlus -> AIChat can open the chat tool editor provided by the plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chatting, image generation, and image analysis.

The interface of the tool is roughly:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main Functions

Offline large-scale model: Integrated llama.cpp library, supporting local offline execution of large models.

Text Chat: Click on the `New Chat` button in the bottom left corner to start a new text chat session.

Image generation: Click on the 'New Image Chat' button in the bottom left corner to create a new image generation session.

Image Analysis: Some messaging services in "New Chat" support sending images, such as Claude, Google Gemini. Simply click on the 🖼️ or 🎨 button above the input box to load the image you want to send.

Support Blueprint: support Blueprint creation API requests, complete functions such as text chat, image generation, etc.

Set the current chat role: The drop-down box at the top of the chat box can be used to set the role for the text being sent, allowing you to adjust the AI chat by simulating different roles.

Clear chat: The ❌ button at the top of the chat box can be used to clear the history of the current conversation.

Dialogue Template: There are hundreds of built-in conversation setting templates available, making it easy to address common issues.

Global settings: Click on the `Settings` button in the bottom left corner to open the global settings window. You can adjust default text chat, image generation API services, and configure specific parameters for each API service. The settings will be automatically saved in the project's directory `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversation Settings: Click on the settings button at the top of the chat box to open the settings window for the current conversation. You can change the conversation name, the API service used for the conversation, and specify specific parameters for each conversation's API independently. The conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Modify chat content: When hovering over a chat message, a settings button will appear for that specific message, enabling options to regenerate, edit, copy, delete the message, and regenerate a new message below it (for user-generated content).

* Image browsing: For image generation, clicking on an image will open the Image Viewer window, supporting saving images as PNG/UE Texture. Textures can be viewed directly in the Content Browser, making it convenient for images to be used within the editor. Additionally, functions such as deleting images, regenerating images, and generating more images are supported. For editors on Windows, image copying is also supported, allowing images to be copied directly to the clipboard for easy use. Generated images are automatically saved in each session folder, typically located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Blueprint:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Global Settings:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Conversation settings:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Edit chat content:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Image viewer:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Use offline large models

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Dialogue template

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introduction to Core Code

The plugin is currently divided into the following modules:

AIChatPlusCommon: Runtime module responsible for handling various AI API interface requests and parsing response content.

AIChatPlusEditor: Editor module, responsible for implementing the AI chatting tool in the editor.

AIChatPlusCllama: Runtime module responsible for encapsulating the interface and parameters of llama.cpp to achieve offline execution of large models.

Thirdparty/LLAMACpp: Runtime third-party module, integrating llama.cpp dynamic library and header files.

The UClass responsible for sending requests is FAIChatPlus_xxxChatRequest. Each type of API service has its own separate Request UClass. The replies to the requests are obtained through two kinds of UClass, UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase, you just need to register the corresponding callback delegate.

Before sending a request, it is necessary to set the parameters and message to be sent for the API. This is done by setting up the FAIChatPlus_xxxChatRequestBody. The specific response content is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving a callback, the ResponseBody can be obtained through a specific interface.

More source code details can be found on the UE store: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Use offline model Cllama (llama.cpp) in the editor tool.

The following explains how to use the offline model llama.cpp in the AIChatPlus editor tool.

First, download the offline model from the HuggingFace website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Put the model in a specific folder, such as placing it under the game project directory Content/LLAMA.

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

###Using the offline model Cllama (llama.cpp) to process images in the editor tool.

Download the offline model MobileVLM_V2-1.7B-GGUF from the HuggingFace website and place it in the directory Content/LLAMA: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)Translate these text into English language:

和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but there seems to be no text to translate.

Set the session model:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Start chatting by sending a picture.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###The code uses the offline model Cllama (llama.cpp).

The following explains how to use the offline model llama.cpp in the code.

First, you also need to download the model file to Content/LLAMA.

Amend the code to include a new command and send a message to the offline model within the command.

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

After recompiling, by using the command in the Cmd editor, you can view the output results of the large model in the OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Blueprint uses offline model llama.cpp.

The following instructions explain how to use the offline model llama.cpp in the blueprint.

Create a node `Send Cllama Chat Request` on the blueprint by right-clicking.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Create an Options node and set `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Create Messages, add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Create a delegate to accept the model's output information and print it on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, run the blueprint and you will see the message returned to the game screen printing the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###The file llama.cpp is using the GPU.

Add parameter "Num Gpu Layer" to "Cllama Chat Request Options" to set the gpu payload of llama.cpp, as shown in the figure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

You can use blueprint nodes to determine if the current environment supports GPU and to obtain the backends supported by the current environment.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_2.png)

###Handle the model files in the .Pak after packing.

After enabling Pak packaging, all project resources will be placed in the .Pak file, which naturally includes offline model .gguf files.

Due to the inability of llama.cpp to directly read .Pak files, it is necessary to extract the offline model files from the .Pak file and copy them to the file system.

AIChatPlus offers a feature that can automatically copy and process model files from .Pak and place them in the Saved folder:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

Alternatively, you can handle the model files in the .Pak yourself. The key is to copy and process the files, as llama.cpp cannot read .Pak correctly.

## OpenAI

###The editor utilizes OpenAI chat.

Open the chat tool, go to Tools -> AIChatPlus -> AIChat, create a new chat session named New Chat, and configure the session to use ChatApi with OpenAI as the interface parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Start chatting:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Switching the model to GPT-4o / GPT-4o-mini allows you to utilize OpenAI's visual capabilities for image analysis.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###The editor uses OpenAI to process images (create/modify/alter).

Create a new image chat in the messaging app, name it New Image Chat, adjust the conversation settings to OpenAI, and configure the parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Create image

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Edit the image by changing the Image Chat Type to Edit, and upload two images. One image should be the original picture, while the other should show the areas to be edited with transparency (where the alpha channel is 0).

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Modify the type of the image to "Variation" in the Image Chat, and upload an image. OpenAI will provide a variant of the original image in response.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###The blueprint uses OpenAI model chatting.

Create a node in the blueprint by right-clicking named `Send OpenAI Chat Request In World`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Create an Options node and set `Stream=true, Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Create Messages and add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Create a delegate to receive the output information from the model and print it on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this; when you run the blueprint, you can see the game screen printing the message returned by the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###The blueprint is created using OpenAI to generate images.

Create a node `Send OpenAI Image Request` by right-clicking in the blueprint and set `In Prompt="a beautiful butterfly"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Create an Options node and set `Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Bind the On Images event and save the image to the local hard drive.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

The complete blueprint looks like this, running the blueprint will show the image saved in the specified location.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###The editor uses Azure.

Create a new conversation (New Chat), change ChatApi to Azure, and configure the API parameters for Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###The editor uses Azure to create images.

Create a new image chat session, change ChatApi to Azure, and configure Azure's API parameters. Please note, if using the dall-e-2 model, set the Quality and Stype parameters to not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Start chatting and let Azure create an image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Blueprint using Azure Chat

Create the following blueprint, set up the Azure Options, click on Run, and you will see the chat information returned by Azure printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Create images using Azure blueprint.

Create the following blueprint, configure Azure Options, click Run, if the image creation is successful, you will see the message "Create Image Done" on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

According to the configuration in the blueprint above, the image will be saved at the path D:\Downloads\butterfly.png.

## Claude

###The editor uses Claude to chat and analyze pictures.

Create a new chat session, rename ChatApi to Claude, and configure Claude's API parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Use Blueprint to chat and analyze pictures with Claude.

Create a node in the blueprint by right-clicking called `Send Claude Chat Request`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Create an Options node, and set `Stream=true, Api Key="your API key from Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Create Messages, create a Texture2D from a file, create AIChatPlusTexture from Texture2D, and add AIChatPlusTexture to the Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Create an Event like in the tutorial above, and print the information on the game screen.

The complete blueprint looks like this, run the blueprint, and you will see the message returned on the game screen when printing a large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Acquire Ollama

You can download the installation package locally from the Ollama official website: [ollama.com](https://ollama.com/)

You can use Ollama through the Ollama interface provided by others.

###The editor uses Ollama for chatting and analyzing images.

Create a new chat session, change ChatApi to Ollama, and configure Ollama's API parameters. If it's a text chat, set the model to a text model, such as llama3.1; if image processing is required, set the model to a vision-supporting model, like moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Use Ollama to chat and analyze images on the blueprint.

Create the following blueprint, configure the Ollama Options, click on Run, and you will see the chat messages returned by Ollama printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###Gemini used in the editor

Create a new chat session, change ChatApi to Gemini, and configure Gemini's API parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Start chatting.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###The text translates to:

The editor uses Gemini to send audio.

Select to read audio from file / read audio from asset / record audio from microphone, generate the audio to be sent.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

Start chatting.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###Blueprint uses Gemini chat

Create the blueprint as shown, set up the Gemini Options, click run, and you will see the chat information returned by Gemini printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###Blueprint uses Gemini to send audio.

Create the following blueprint, set up audio loading, configure the Gemini Options, click Run, and you will see the chat information returned after Gemini processes the audio displayed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###The editor utilizes Deepseek.

Create a new chat session, change ChatApi to OpenAi, and set the Api parameters of Deepseek. Add a new candidate model called deepseek-chat and set the model to deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Start chatting.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Use Deepseek chat for the blueprint.

Create the following blueprint, set up the Request Options related to Deepseek, including parameters such as Model, Base Url, End Point Url, and ApiKey. Click to run, and you will see Gemini's chat information printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##Extra provided blueprint feature nodes.

###Cllama related.

Verify if "Cllama" is valid: judge if Cllama llama.cpp is properly initialized.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

Determine if llama.cpp supports GPU backend in the current environment.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

Retrieve all backends supported by the current llama.cpp

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

Automatically copy model files from Pak to the file system: "Cllama Prepare ModelFile In Pak"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###Image-related

Translate the text into English language:

"Convert UTexture2D to Base64": Convert the image of UTexture2D to PNG base64 format

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

Save the UTexture2D as a .png file.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

Load the .png file into UTexture2D.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Duplicate UTexture2D" means copying UTexture2D.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###Audio related

Load the .wav file as USoundWave.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

Transform the WAV binary data into a USoundWave.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

Save USoundWave as a .wav file.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

Convert USoundWave to binary audio data

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

Convert the USoundWave to Base64 data.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

Duplicate USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

Transfer the audio capture recording data to USoundWave.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

##Release Notes

### v1.6.0 - 2025.03.02

####New feature

Upgrade llama.cpp to version b4604.
Cllama supports GPU backends: cuda and metal
The chat tool Cllama supports GPU usage.
Support reading model files packaged in Pak.

#### Bug Fix

Fix the issue where Cllama crashes when reloading during inference.

Fix iOS compilation errors.

### v1.5.1 - 2025.01.30

####New Feature

Only Gemini is allowed to send audio messages.

Optimize the method for obtaining PCMData by decompressing the audio data when generating B64.

* request to add two callbacks: OnMessageFinished and OnImagesFinished

Optimize the Gemini Method to automatically retrieve the Method based on bStream.

Add some blueprint functions to facilitate converting the Wrapper to actual types, and to retrieve Response Message and Error.

#### Bug Fix

Fix the issue of multiple Request Finish calls.

### v1.5.0 - 2025.01.29

####New feature

Support sending audio to Gemini.

The editor tool supports sending audio and recordings.

#### Bug Fix

Fix the bug causing Session copy failure.

### v1.4.1 - 2025.01.04

####Problem fixed

The chat tool supports sending only pictures without any text.

Fix the failure to send images through the OpenAI interface.

Repair the issues with the missing parameters Quality, Style, and ApiVersion in the settings of OpenAI and Azure chat tools.

### v1.4.0 - 2024.12.30

####New Feature

*(Experimental feature) Cllama (llama.cpp) supports multimodal models and can process images.

All blueprint type parameters have been accompanied by detailed prompts.

### v1.3.4 - 2024.12.05

####New feature

OpenAI supports the Vision API.

####Problem fixed

Fix the error in OpenAI stream=false.

### v1.3.3 - 2024.11.25

####New Feature

Support UE-5.5.

####Problem resolution.

Fixing the issue where some blueprints are not taking effect.

### v1.3.2 - 2024.10.10

####Problem fixed

Fix cllama crashing when manually stopping request.

Fix the issue of not being able to find the ggml.dll and llama.dll files when packaging the win download version of the mall.

When creating a request, check if it is in the GameThread.

### v1.3.1 - 2024.9.30

####New feature

Add a SystemTemplateViewer that allows you to view and utilize hundreds of system setting templates.

####Problem fixed

Fix the plug-in downloaded from the mall, llama.cpp could not find the link library

Fix the issue of LLAMACpp path being too long.

Fix the llama.dll link error after packaging Windows.

Fixing the file path reading issue on iOS/Android.

Fix the error in setting name for ClIame.

### v1.3.0 - 2024.9.23

####Significant new feature

Integrated llama.cpp to support local offline execution of large models.

### v1.2.0 - 2024.08.20

####New feature

Support OpenAI Image Edit/Image Variation.

Support Ollama API, support automatically obtaining the list of models supported by Ollama.

### v1.1.0 - 2024.08.07

####New Feature

Support the blueprint.

### v1.0.0 - 2024.08.05

####New feature

Complete basic functionalities

Support OpenAI, Azure, Claude, Gemini

Built-in feature-rich chat tool with a comprehensive editor.

--8<-- "footer_en.md"


> This post was translated using ChatGPT, please provide feedback in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
