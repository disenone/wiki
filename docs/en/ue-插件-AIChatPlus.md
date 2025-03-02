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
description: UE plugin AIChatPlus documentation
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE Plugin AIChatPlus Documentation

##Public warehouse

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Plugin acquisition

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Plugin Introduction

This plugin supports UE5.2+.

UE.AIChatPlus is a plugin for Unreal Engine that enables communication with various GPT AI chat services. It currently supports services such as OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and local offline llama.cpp. In the future, it will continue to support more service providers. Its implementation is based on asynchronous REST requests, ensuring high performance and facilitating UE developers to integrate these AI chat services.

UE.AIChatPlus also includes an editor tool that allows you to directly use these AI chat services in the editor to generate text and images, analyze images, and more.

##Instructions for use.

###Editor chat tool

Menu bar Tools -> AIChatPlus -> AIChat can open the plugin-provided editor chat tool.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chatting, image generation, and image analysis.

The interface of the tool is roughly as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main Functions

Offline Large Models: Integrated llama.cpp library, supporting local offline execution of large models.

Text Chat: Click the `New Chat` button in the bottom left corner to start a new text chat session.

Image generation: Click the 'New Image Chat' button in the bottom left corner to create a new image generation session.

Image Analysis: Some chat services in "New Chat" support sending images, such as Claude and Google Gemini. To send an image, simply click on the 🖼️ or 🎨 button above the input box.

Support Blueprint: Supporting Blueprint to create API requests, completing functions such as text chat and image generation.

Set the current chat character: The dropdown menu at the top of the chat box allows you to select the character for sending text and adjust AI chat by simulating different characters.

Clear chat: The ❌ button at the top of the chat box can clear the history messages of the current conversation.

Dialogue Template: Built-in with hundreds of dialogue templates for easy handling of common issues.

Global Settings: Click on the `Setting` button in the bottom left corner to open the global settings window. You can configure default text chat, image generation API services, and specify parameters for each API service. Settings will be automatically saved in the project path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversation settings: Clicking the settings button at the top of the chat box will open the settings window for the current conversation. You can change the conversation name, API service, and define specific parameters for each session. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Chat content editing: When hovering the mouse over a chat message, a settings button will appear for that specific message, allowing options to regenerate, edit, copy, delete, or regenerate below (for user-generated content).

* Image browsing: For image generation, clicking on the image will open the Image Viewer window, supporting saving the image as PNG/UE Texture. Textures can be viewed directly in the Content Browser, making it convenient to use images within the editor. Additionally, it supports functions like deleting images, regenerating images, and generating more images. For editors on Windows, it also allows copying images to the clipboard for easy use. Images generated during sessions are automatically saved in each session folder, typically located at `${ProjectFolder}/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

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

Use offline large-scale models.

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Dialogue Template

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introduction to Core Code

Currently, the plugin is divided into the following modules:

AIChatPlusCommon: Runtime module responsible for handling various AI API interface requests and parsing response content.

AIChatPlusEditor: Editor module responsible for implementing AI chat tools in the editor.

AIChatPlusCllama: Runtime module responsible for encapsulating the interface and parameters of llama.cpp, enabling offline execution of large models.

Thirdparty/LLAMACpp: Runtime third-party module integrating the dynamic library and header files of llama.cpp.

The UClass responsible for sending requests is FAIChatPlus_xxxChatRequest. Each API service has its own independent Request UClass. Responses to the requests are obtained through two UAIChatPlus classes, ChatHandlerBase and ImageHandlerBase, by simply registering the corresponding callback delegate.

Before sending a request, you need to set the parameters and messages for the API. This is done through FAIChatPlus_xxxChatRequestBody. The specific response is also parsed into FAIChatPlus_xxxChatResponseBody. You can obtain the ResponseBody through a specific interface when receiving a callback.

More source code details are available for purchase at the UE Store: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Using offline model Cllama(llama.cpp) in editor tool.

The following explains how to use the offline model llama.cpp in the AIChatPlus editor tool.

Firstly, download the offline model from the HuggingFace website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Place the model in a specific folder, for example, in the Content/LLAMA directory of the game project.

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

###Use the offline model Cllama (llama.cpp) in the editor tool to process images.

Download the offline model MobileVLM_V2-1.7B-GGUF from the HuggingFace website and place it in the Content/LLAMA directory as well: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)Translate these text into English language:

And [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)。

Set the model for the session:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Start chatting by sending a picture.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###The code utilizes the offline model Cllama (llama.cpp).

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

After recompiling, you can use commands in the Cmd editor to view the output results of large models in the OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Blueprint uses offline model llama.cpp.

The following instructions explain how to use the offline model llama.cpp in the blueprint.

Create a node `Send Cllama Chat Request` by right-clicking on the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Create an Options node and set `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Create messages, separately add a system message and a user message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Create a delegate that receives the model's output information and prints it on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, run the blueprint, and you will see the game screen printing the message returned by the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###llama.cpp uses GPU

Add the parameter "Num Gpu Layer" to the "Cllama Chat Request Options", which can set the GPU payload of llama.cpp, as shown in the picture.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

You can use Blueprint nodes to determine if the current environment supports GPU and to get the backends supported by the current environment.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_2.png)

###Handle model files in the .Pak after packaging.

Once you enable the Pak packaging, all project resource files will be contained in the .Pak file, including the offline model gguf files.

Due to llama.cpp not being able to directly read .Pak files, it is necessary to copy the offline model files from the .Pak file to the file system.

AIChatPlus provides a feature that can automatically copy and process model files from .Pak and place them in the Saved folder:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

Alternatively, you can handle the model files in the .Pak by yourself. The key is to copy and process the files, as llama.cpp cannot read the .Pak correctly.

## OpenAI

###The editor uses OpenAI chat.

Open the chat tool, go to Tools -> AIChatPlus -> AIChat, create a new chat session New Chat, set the session to ChatApi as OpenAI, and configure the interface parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Start chatting:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Switching the model to GPT-4o/GPT-4o-mini enables the use of OpenAI's visual feature to analyze images.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###The editor utilizes OpenAI to handle images (creation/modification/variation).

Create a new Image Chat in the messaging tool, change the session settings to OpenAI, and configure the parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Create image

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Edit the image, change the Image Chat Type to Edit, and upload two images. One is the original image, and the other is a mask where the transparent areas (alpha channel is 0) indicate the parts that need to be edited.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Modify the image type from Image Chat Type to Variation, and upload an image. OpenAI will return a variant of the original image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Blueprint using OpenAI model chat

Create a node in the blueprint by right-clicking: `Send OpenAI Chat Request In World`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Create an "Options" node and set `Stream=true, Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Create Messages, respectively adding a System Message and a User Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Create a delegate to receive the output information from the model and print it on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, run the blueprint, and you will see the message returned on the game screen printing a large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Create images using OpenAI Blueprints

In the blueprint, right-click to create a node named "Send OpenAI Image Request", and set "In Prompt = 'a beautiful butterfly'".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Create the Options node, and set `Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Bind the On Images event and save the image to the local hard disk.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

The complete blueprint looks like this, running the blueprint will show the image saved in the specified location.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###The editor uses Azure.

Create a new chat session, change ChatApi to Azure, and configure the API parameters for Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Start chatting.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###The editor uses Azure to create images.

Create a new image chat session, change ChatApi to Azure, and set Azure's API parameters. Note that if the model is dall-e-2, the Quality and Style parameters need to be set to not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Start chatting, let Azure create images

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Blueprint using Azure Chat.

Create the following blueprint, configure the Azure Options, click Run, and you will see the chat information returned by Azure printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Create an image with Azure using Blueprint.

Create the following blueprint, configure the Azure Options, click Run, if the image creation is successful, you will see the message "Create Image Done" on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

According to the settings in the blueprint above, the image will be saved in the path D:\Downloads\butterfly.png.

## Claude

###The editor uses Claude to chat and analyze images.

Create a new chat session, rename ChatApi to Claude, and configure Claude's API parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Use the blueprint to chat with Claude and analyze images.

Create a node named 'Send Claude Chat Request' by right-clicking on the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Create an Options node and set `Stream=true, Api Key="your API key from Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Create Messages, create a Texture2D from a file, and create AIChatPlusTexture from Texture2D, then add AIChatPlusTexture to Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Create an Event as mentioned above and print the information on the game screen, just like in the tutorial.

The complete blueprint looks like this, running the blueprint will show the message returned by the game screen printing the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Acquiring Ollama

You can download the installation package from the official Ollama website for local installation: [ollama.com](https://ollama.com/)

You can use Ollama through the Ollama interface provided by others.

###The editor uses Ollama for chatting and analyzing images.

Create a new chat session, change ChatApi to Ollama, and configure Ollama's API parameters. If it's a text chat, set the model to a text model, such as llama3.1; if image processing is needed, set the model to one that supports vision, for example, moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Start chatting.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Use Ollama to chat and analyze images with the blueprint.

Create the following blueprint, configure the Ollama Options, click on run, and you will see the chat information returned by Ollama printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###The editor uses Gemini.

Create a new conversation (New Chat), change ChatApi to Gemini, and set Gemini's API parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###The editor uses Gemini to send audio.

Select reading audio from file / reading audio from Asset / recording audio from microphone, and generate the audio to be sent.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###Blueprint using Gemini chat

Create the following blueprint, configure the Gemini Options, click run, and you will see the chat information returned by Gemini printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###The blueprint uses Gemini to send audio.

Create the following blueprint, set up loading audio, configure the Gemini Options, click on Run, and you will see the chat information returned after Gemini processes the audio on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###The editor utilizes Deepseek.

Create a new chat session, change ChatApi to OpenAi, and set the Api parameters for Deepseek. Add a new candidate model named deepseek-chat, and set the model to deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Blueprint using Deepseek chat

Create the blueprint as follows, set up the Request Options related to Deepseek, including Model, Base Url, End Point Url, ApiKey, and other parameters. Click 'run' to display the chat information returned by Gemini on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##Extra provided blueprint feature node

###Cllama related

"Cllama Is Valid": Check if Cllama llama.cpp is properly initialized.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Determine if llama.cpp supports GPU backend in the current environment."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

Retrieve all backends supported by the current llama.cpp.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Prepare ModelFile In Pak": Automatically copies model files from Pak to the file system.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###Image-related

Convert the image of UTexture2D to PNG base64 format.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

Save the UTexture2D as a .png file

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

Load a .png file into UTexture2D.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

Duplicate UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###Audio-related.

Read the .wav file as USoundWave.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

"Convert .wav data to USoundWave": Convert binary data from .wav to USoundWave.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

Save USoundWave as a .wav file.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

Convert USoundWave to binary audio data

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

Convert USoundWave to Base64 data.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

Duplicate USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

"Convert Audio Capture Data to USoundWave" translates to "将音频采集数据转换为 USoundWave".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

##Changelog

### v1.6.0 - 2025.03.02

####New Feature

Upgrade llama.cpp to version b4604.

Cllama supports GPU backends: cuda and metal

The chat tool Cllama supports the use of GPU.

Support reading model files packed in a Pak.

#### Bug Fix

Fix the issue where Cllama crashes when reloading during deduction.

Fixing iOS compilation errors

### v1.5.1 - 2025.01.30

####New Feature

Only Gemini is allowed to send audio messages.

Optimize the method to acquire PCMData, decompress audio data when generating B64.

Add two callbacks OnMessageFinished and OnImagesFinished to the request.

Optimize the Gemini Method to automatically fetch the Method based on bStream.

Add some blueprint functions to facilitate converting Wrapper to actual types, and getting Response Message and Error.

#### Bug Fix

Fix issue of multiple requests being finished.

### v1.5.0 - 2025.01.29

####New feature

Support sending audio to Gemini.

The editing tool supports sending audio and recordings.

#### Bug Fix

Fix the bug causing Session copy failure.

### v1.4.1 - 2025.01.04

####Problem fixed

Chat tool support sending only images without text messages.

Fix OpenAI API image sending issue failed document图

Fix the missing parameters Quality, Style, and ApiVersion in the settings of OpanAI and Azure chat tools.

### v1.4.0 - 2024.12.30

####New feature

*(Experimental feature)* Cllama (llama.cpp) supports multi-modal models and is able to process images.

All blueprint type parameters have been added with detailed hints.

### v1.3.4 - 2024.12.05

####New feature

OpenAI supports a vision API.

####Issue Resolution

Fix the error when OpenAI stream=false.

### v1.3.3 - 2024.11.25

####New feature

Support UE-5.5.

####Problem fixed

Fix the issue where some blueprints are not working.

### v1.3.2 - 2024.10.10

####Troubleshooting

Fix crash when manually stopping request in cllama

Fix the issue of not being able to find the ggml.dll and llama.dll files when packaging the download version of the Win store.

Check if in GameThread when creating a request.

### v1.3.1 - 2024.9.30

####New feature

Add a SystemTemplateViewer that allows you to view and use hundreds of system setting templates.

####Problem fixed

Repair the plugin downloaded from the store, llama.cpp cannot find the link library.

Fix the issue of LLAMACpp path being too long.

Fix the llama.dll error in Windows packaging.

Fixing the file path reading issue on iOS/Android.

Fix Cllame's name setting error.

### v1.3.0 - 2024.9.23

####Significant new feature

Integrated llama.cpp, supporting local offline execution of large models.

### v1.2.0 - 2024.08.20

####New feature

Support for OpenAI Image Edit/Image Variation.

Support Ollama API, support automatically obtaining the list of models supported by Ollama.

### v1.1.0 - 2024.08.07

####New feature

Support Blueprint

### v1.0.0 - 2024.08.05

####New feature

Complete basic functionality

Support OpenAI, Azure, Claude, and Gemini.

Built-in feature-rich chat tool with an advanced editor.

--8<-- "footer_en.md"


> This post was translated using ChatGPT. Please provide [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
