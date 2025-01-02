---
layout: post
title: UE Plug-in AIChatPlus Documentation
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

##Introduction to the plugin

This plugin supports UE5.2+.

UE.AIChatPlus is an UnrealEngine plugin that enables communication with various GPT AI chat services. The supported services currently include OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and local offline llama.cpp. In the future, more service providers will be supported. Its implementation is based on asynchronous REST requests, providing high performance and making it convenient for Unreal Engine developers to integrate these AI chat services.

At the same time, UE.AIChatPlus also includes an editor tool that allows you to use these AI chat services directly in the editor to generate text and images, analyze images, and more.

##Instructions for use

###Editor Chat Tool

Menu bar Tools -> AIChatPlus -> AIChat can open the editor chat tool provided by the plugin.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chatting, image generation, and image analysis.

The interface of the tool is roughly as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main Functions

Offline Big Model: Integrated the llama.cpp library, supporting local offline execution of big models

Text Chat: Click on the `New Chat` button in the bottom left corner to start a new text chat session.

Image Generation: Click the `New Image Chat` button in the bottom left corner to start a new image generation session.

Image Analysis: Some chat services of `New Chat` support image sending, such as Claude and Google Gemini. You can load the image you want to send by clicking the 🖼️ or 🎨 button above the input box.

Support Blueprint: Support blueprint creation API requests to complete functions such as text chat and image generation.

Set the current chat character: The dropdown menu above the chat box can be used to select the current character for sending text, allowing you to adjust the AI chat by simulating different characters.

Clear chat: Pressing the ❌ button at the top of the chat box can clear the history of the current conversation.

Dialogue Template: Built-in hundreds of dialogue setting templates, making it easy to handle common issues.

Global Settings: Click the `Setting` button in the lower left corner to open the global settings window. You can configure default text chat, image generation API services, and specific parameters for each API service. The settings will be automatically saved in the project's path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Conversation Settings: Click on the settings button above the chat box to open the settings window for the current conversation. You can change the name of the conversation, the API service used for the conversation, and specify specific parameters for each conversation API individually. The conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

Edit chat content: When hovering over a chat message, a settings button for that specific message will appear, allowing for options to regenerate, edit, copy, delete the content, and regenerate the content below (for content from user roles).

* Image Browsing: When it comes to image generation, clicking on an image will open the Image Viewer window, supporting saving images as PNG/UE Texture. Textures can be directly viewed in the Content Browser, making it convenient for images to be used within the editor. Additionally, there is support for deleting images, regenerating images, continuing to generate more images, and other functions. For editors on Windows, copying images is also supported, allowing images to be copied directly to the clipboard for ease of use. Images generated during sessions will also be automatically saved in each session folder, typically located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

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

Currently, the plugin is divided into the following modules:

AIChatPlusCommon: Runtime module, responsible for handling various AI API interface requests and parsing response content.

AIChatPlusEditor: Editor module, responsible for implementing the AI chat tool within the editor.

* AIChatPlusCllama: Runtime module, responsible for encapsulating the interface and parameters of llama.cpp, and achieving offline execution of large models

* Thirdparty/LLAMACpp: Runtime third-party module, integrating the dynamic library and header files of llama.cpp.

The UClass responsible for sending requests specifically is FAIChatPlus_xxxChatRequest, each API service has its own independent Request UClass. The response to the request is obtained through two UClass, UAIChatPlus_ChatHandlerBase and UAIChatPlus_ImageHandlerBase, only requiring the registration of the corresponding callback delegate.

Before sending a request, you need to set the parameters and the message to be sent for the API. This is done by setting up the FAIChatPlus_xxxChatRequestBody. The specific reply content is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving a callback, you can retrieve the ResponseBody through a specific interface.

More source code details can be obtained at the UE Marketplace: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Use offline model in the editor tool Cllama(llama.cpp)

The following explains how to use the offline model llama.cpp in the AIChatPlus editor tool.

First, download the offline model from the HuggingFace website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Put the model in a specific folder, such as placing it in the Content/LLAMA directory of the game project.

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

###Use the offline model Cllama (llama.cpp) in the editor tool to process images.

Download the offline model MobileVLM_V2-1.7B-GGUF from the HuggingFace website and place it in the directory Content/LLAMA as well: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)The [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)。

Set the model for the session:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Start chatting by sending pictures

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###The code utilizes the offline model Cllama (llama.cpp).

The following explains how to use the offline model llama.cpp in your code.

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

After recompiling, you can use commands in the Cmd editor to see the output of the large model in the OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Blueprint using offline model llama.cpp

The following explains how to use the offline model llama.cpp in the blueprint.

Create a node `Send Cllama Chat Request` by right-clicking in the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Create an Options node, and set `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Create Messages, respectively add a System Message and a User Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Create a Delegate to receive model output information and print it on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, run the blueprint, and you will see the message returned on the game screen when printing large models.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###The editor is using OpenAI chat.

Open the chat tool. Go to Tools -> AIChatPlus -> AIChat, create a new chat session named New Chat, and configure the session ChatApi as OpenAI. Set the interface parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

* Start chatting:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Switching the model to gpt-4o / gpt-4o-mini enables the use of OpenAI's visual functionality to analyze images.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###The editor uses OpenAI to process images (create/modify/variate).

Create a new Image Chat in the messaging app, modify the session settings to OpenAI, and configure the parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Create an image

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

* Edit the image, change the Image Chat Type to Edit, and upload two images: one original image and one where the transparent areas (with an alpha channel of 0) indicate the parts that need to be modified.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Modify the image prompt by changing the "Image Chat Type" to "Variation," then upload a new image. OpenAI will provide a variant of the original image in response.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###The blueprint uses OpenAI model chatting

Create a node `Send OpenAI Chat Request In World` by right-clicking in the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Create an Options node, and set `Stream=true, Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Create Messages, add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Create a Delegate to receive model output information and print it on the screen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this. Run the blueprint, and you'll see the game screen printing a message confirming the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Create images using OpenAI blueprint.

Create a node `Send OpenAI Image Request` on the blueprint by right-clicking, and set `In Prompt="a beautiful butterfly"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Create an Options node, and set `Api Key="your API key from OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Bind On Images event, and save the images to the local hard drive.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

The complete blueprint looks like this, run the blueprint, and you can see the picture saved in the specified location.

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

Let's start chatting and have Azure create an image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Use Azure Chat for blueprints

Create the following blueprint, set up Azure Options, click Run, and you will see the chat messages returned by Azure printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Create images using Azure Blueprints

Create the following blueprint, set up Azure Options, click Run. If the image creation is successful, you will see the message "Create Image Done" on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

According to the settings in the blueprint above, the image will be saved to the path D:\Downloads\butterfly.png.

## Claude

###The editor uses Claude to chat and analyze pictures.

Create a new conversation (New Chat), change `ChatApi` to `Claude`, and configure the Api parameters of `Claude`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Start chatting.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###The blueprint uses Claude to chat and analyze images.

Create a node `Send Claude Chat Request` in the blueprint by right-clicking.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Create an Options node and set `Stream=true, Api Key="your API key from Clude", Max Output Tokens=1024`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Create Messages, create Texture2D from file, and create AIChatPlusTexture from Texture2D, then add AIChatPlusTexture to the Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Just like the tutorial above, create an Event and print the information on the game screen.

The complete blueprint looks like this, run the blueprint, and you will see the game screen printing the message returned by the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Obtain Ollama

You can obtain the installation package locally through the Ollama official website: [ollama.com](https://ollama.com/)

You can use Ollama through the Ollama interface provided by others.

###The editor uses Ollama to chat and analyze images.

Create a new chat session, change ChatApi to Ollama, and set Ollama's API parameters. If it's a text chat, set the model to a text model, like llama3.1; if image processing is needed, set the model to a vision-supported model, such as moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###The blueprint uses Ollama to chat and analyze images.

Create the following blueprint, set up Ollama Options, click Run, and you will see the chat information returned by Ollama printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###The editor uses Gemini.

Create a new chat session (New Chat), change ChatApi to Gemini, and configure Gemini's Api parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

* Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###Use Gemini chat for the blueprint.

Create the following blueprint, set up Gemini Options, click Run, and you will see the chat information returned by Gemini printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)


##Update Log

### v1.4.1 - 2025.01.04

####Issue Fix

Chat tools support sending only pictures without text messages.

Fix OpenAI interface failed to send image issue picture.

Fix missing parameters Quality, Style, ApiVersion in OpanAI and Azure chat tool settings.

### v1.4.0 - 2024.12.30

####New feature

* (Experimental feature) Cllama(llama.cpp) supports multimodal models, capable of processing images

All blueprint type parameters have detailed hints added.

### v1.3.4 - 2024.12.05

####New Function

OpenAI supports Vision API.

####Problem resolved

Fix the error in OpenAI stream=false.

### v1.3.3 - 2024.11.25

####New features

Supporting UE-5.5

####Troubleshooting

Fix some blueprints not taking effect issue

### v1.3.2 - 2024.10.10

####Issue Resolution

Fix crash when manually stopping the request in cllama.

Fix the issue of not finding ggml.dll and llama.dll files when packaging the Win download version of the mall.

When creating a request, make sure to check if it is in the GameThread.

### v1.3.1 - 2024.9.30

####New Feature

Add a SystemTemplateViewer, where you can view and use hundreds of system setting templates.

####Issue fixed

Fix the plugin downloaded from the mall, llama.cpp cannot find the link library.

Fix LLAMACpp long path issue

Fix the llama.dll error in Windows after packaging.

Fix the issue of reading file paths on iOS/Android.

Fix Cllame setting name error

### v1.3.0 - 2024.9.23

####Significant new feature

Integrated llama.cpp to support local offline execution of large models.

### v1.2.0 - 2024.08.20

####New Feature

Support OpenAI Image Edit/Image Variation

Support Ollama API, support automatically fetching the list of models supported by Ollama

### v1.1.0 - 2024.08.07

####New Feature

Support Blueprint

### v1.0.0 - 2024.08.05

####New Feature

Complete basic features

Support OpenAI, Azure, Claude, Gemini.

Built-in feature-rich editor chat tool.

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
