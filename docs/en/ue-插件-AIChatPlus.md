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

This plugin supports UE5.2 and above.

UE.AIChatPlus is an Unreal Engine plugin that enables communication with various GPT AI chat services. Currently, it supports services such as OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, and local offline llama.cpp. In the future, it will support even more service providers. Its implementation is based on asynchronous REST requests, providing high performance and convenience for UE developers to integrate these AI chat services.

At the same time, UE.AIChatPlus also includes an editor tool that allows users to utilize these AI chat services directly within the editor to generate text and images, analyze images, and more.

##User Manual

###Editor Chat Tool

The menu bar Tools -> AIChatPlus -> AIChat opens the chat tool provided by the plugin's editor.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chatting, image generation, and image analysis.

The interface of the tool is generally as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main Features

* Offline large model: Integrates the llama.cpp library, supporting local offline execution of large models.

* Text chat: Click the `New Chat` button in the lower-left corner to start a new text chat session.

* Image Generation: Click the `New Image Chat` button in the lower left corner to start a new image generation session.

* Image Analysis: Some chat services in `New Chat` support sending images, such as Claude and Google Gemini. Click the 🖼️ or 🎨 button above the input box to load the image you want to send.

* Support Blueprint: Supports the creation of API requests for blueprints, enabling functionalities such as text chat and image generation.

* Set the current chat role: The dropdown menu at the top of the chat box allows you to specify the role for the text being sent, enabling you to adjust the AI chat by simulating different characters.

* Clear Conversation: The ❌ button at the top of the chat box can clear the history of the current conversation.

* Dialogue templates: Built-in hundreds of dialogue setting templates for convenient handling of common issues.

* Global Settings: Click the `Setting` button in the lower left corner to open the global settings window. You can set the default text chat, the API service for image generation, and configure specific parameters for each API service. The settings will be automatically saved in the project's path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* Conversation Settings: Click the settings button above the chat box to open the settings window for the current conversation. You can modify the conversation name, change the API service used for the conversation, and set specific parameters for each conversation’s API independently. The conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

* Chat Content Modification: Hovering over the chat content will display a settings button for that specific chat entry, allowing you to regenerate content, modify content, copy content, delete content, or regenerate content below (for content where the role is the user).

* Image Browsing: For image generation, clicking on an image will open the Image Viewer window, which supports saving the image as PNG/UE Texture. The texture can be viewed directly in the Content Browser, making it convenient for use within the editor. Additionally, it supports functionalities such as deleting images, regenerating images, and continuing to generate more images. For the editor on Windows, it also supports copying images, allowing you to copy the image directly to the clipboard for ease of use. Images generated during a session will also be automatically saved in each session's folder, typically located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

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

Using offline large models

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Dialogue Template

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Introduction to Core Code

The plugin is currently divided into the following modules:

* AIChatPlusCommon: Runtime module, responsible for handling requests sent to various AI API interfaces and parsing the response content.

* AIChatPlusEditor: Editor module, responsible for implementing the editor AI chat tool.

* AIChatPlusCllama: Runtime module, responsible for wrapping the interfaces and parameters of llama.cpp to achieve offline execution of large models.

* Thirdparty/LLAMACpp: Runtime third-party module, integrating the dynamic library and header files of llama.cpp.

The specific UClass responsible for sending requests is FAIChatPlus_xxxChatRequest, with each API service having its own independent Request UClass. The responses to the requests are obtained through the UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase UClasses, and you only need to register the corresponding callback delegates.

Before sending a request, you need to set up the API parameters and the message to be sent, which is done through FAIChatPlus_xxxChatRequestBody. The specific content of the reply is also parsed into FAIChatPlus_xxxChatResponseBody, and when a callback is received, you can obtain the ResponseBody through a specific interface.

More source code details can be found in the UE Store: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###The editor tool uses the offline model Cllama (llama.cpp).

The following explains how to use the offline model llama.cpp in the AIChatPlus editor tool.

* First, download the offline model from the HuggingFace website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Place the model in a specific folder, for example, in the game project directory Content/LLAMA.

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

###The editor tool uses the offline model Cllama (llama.cpp) to process images.

* Download the offline model MobileVLM_V2-1.7B-GGUF from the HuggingFace website and place it in the directory Content/LLAMA: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)and [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf).

* Set the model for the session:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

* Send a picture to start chatting.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###The code uses the offline model Cllama (llama.cpp)

The following explains how to use the offline model llama.cpp in the code.

* First, you also need to download the model files to Content/LLAMA.

* Modify the code to add a command and send a message to the offline model within the command.

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

* After recompiling, you can use the command in the editor Cmd to see the output results of the large model in the log OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###The blueprint uses the offline model llama.cpp.

The following explains how to use the offline model llama.cpp in Blueprints.

* Right-click in the blueprint to create a node `Send Cllama Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

* Create the Options node and set `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

* Create Messages, adding a System Message and a User Message separately.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Create a Delegate to accept the model output and print it on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* The complete blueprint looks like this; run the blueprint to see the game screen displaying the messages returned by the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###The editor uses OpenAI chat.

* Open the chat tool Tools -> AIChatPlus -> AIChat, create a new chat session New Chat, set the session ChatApi to OpenAI, and configure the interface parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

* Start chatting:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

* Switch the model to gpt-4o / gpt-4o-mini to utilize OpenAI's visual capabilities for analyzing images.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###The editor uses OpenAI to process images (create/modify/variant).

* Create a new image chat in the chat tool, set the chat settings to OpenAI, and configure the parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

* Create image

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

* Modify the image, change the conversation Image Chat Type to Edit, and upload two images: one is the original image, and the other is the mask where the transparent areas (alpha channel set to 0) indicate the parts that need to be modified.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

* Image variation, change the conversation Image Chat Type to Variation, and upload an image. OpenAI will return a variant of the original image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Blueprint uses OpenAI model chat.

* Right-click in the blueprint to create a node `Send OpenAI Chat Request In World`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

* Create an Options node and set `Stream=true, Api Key="your api key from OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

* Create Messages, adding a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Create a Delegate to accept the model output information and print it on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* The complete blueprint looks like this. Run the blueprint to see the game screen displaying the messages returned by the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Blueprint uses OpenAI to create images.

* Right-click to create a node `Send OpenAI Image Request` in the blueprint, and set `In Prompt="a beautiful butterfly"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

* Create an Options node and set `Api Key="your api key from OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

* Bind the On Images event and save the images to the local hard drive.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

The complete blueprint looks like this; by running the blueprint, you can see the images saved in the specified location.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###The editor uses Azure.

* Create a new chat (New Chat), change ChatApi to Azure, and set the Azure API parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

* Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###The editor uses Azure to create images.

* Create a new image chat session (New Image Chat), change ChatApi to Azure, and set the Azure API parameters. Note that if you are using the dall-e-2 model, you need to set the parameters Quality and Stype to not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

* Start chatting and let Azure create images.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Blueprint uses Azure chat.

Create the blueprint as follows, set the Azure Options, click run, and you will see the chat information returned by Azure printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Blueprint uses Azure to create images.

Create the blueprint as follows, set the Azure Options, and click Run. If the image is created successfully, you will see the message "Create Image Done" on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

According to the settings in the blueprint above, the image will be saved at the path D:\Dwnloads\butterfly.png.

## Claude

###The editor uses Claude to chat and analyze images.

* Start a new conversation (New Chat), change ChatApi to Claude, and set Claude's API parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

* Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Blueprint uses Claude for chatting and image analysis.

* Right-click in the blueprint to create a node `Send Claude Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

* Create an Options node and set `Stream=true, Api Key="your api key from Clude", Max Output Tokens=1024`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

* Create Messages, create Texture2D from a file, create AIChatPlusTexture from Texture2D, and add AIChatPlusTexture to the Message.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

* Similar to the tutorial above, create an Event and print the information on the game screen.

* The complete blueprint looks like this; when you run the blueprint, you will see the game screen displaying the messages returned by the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Get Ollama

You can download the installation package for local installation from the official Ollama website: [ollama.com](https://ollama.com/)

You can use Ollama through the interface provided by others.

###The editor uses Ollama for chatting and analyzing images.

* Create a new chat, change ChatApi to Ollama, and set the Api parameters for Ollama. If it's a text chat, set the model to a text model, such as llama3.1; if image processing is required, set the model to a vision-enabled model, such as moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

* Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Blueprint uses Ollama for chatting and analyzing images.

Create the blueprint as follows, set the Ollama Options, click run, and you will see the chat information returned by Ollama printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###The editor uses Gemini.

* Start a new chat, change ChatApi to Gemini, and set the Gemini API parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

* Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###Blueprint uses Gemini chat.

Create the following blueprint, set up Gemini Options, click run, and you will see the chat information returned by Gemini printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

## Deepseek

###The editor uses Deepseek.

* Create a new conversation (New Chat), change ChatApi to OpenAi, and set the Api parameters for Deepseek. Add a Candidate Model called deepseek-chat and set the Model to deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

* Start chat

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Blueprint uses Deepseek chat.

Create the following blueprint and set the relevant Request Options for Deepseek, including parameters such as Model, Base Url, End Point Url, ApiKey, etc. Click run, and you will see the chat information returned by Gemini printed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##Update log

### v1.5.0 - 2025.01.29

####New Features

* Support sending audio to Gemini

* The editor tool supports sending audio and recordings.

#### Bug Fix

* Fix the bug related to Session copy failure.

### v1.4.1 - 2025.01.04

####Issue Resolution

* The chat tool supports sending only images without messages.

* Fix the issue of sending images through the OpenAI interface failure.

* Fix the issue where the parameters Quality, Style, and ApiVersion were omitted in the OpanAI and Azure chat tool settings.

### v1.4.0 - 2024.12.30

####New Features

* (Experimental feature) Cllama (llama.cpp) supports multi-modal models and can process images.

* All blueprint type parameters have detailed prompts added.

### v1.3.4 - 2024.12.05

####New Features

* OpenAI supports vision API

####Issue Fixing

* Fix the error when OpenAI stream=false

### v1.3.3 - 2024.11.25

####New Feature

* Supports UE-5.5

####Issue Fixing

* Fix issues with some blueprints not being effective.

### v1.3.2 - 2024.10.10

####Issue fix

* Fix the crash of cllama when manually stopping requests.

* Fix the issue where the ggml.dll and llama.dll files cannot be found in the packaged download version for Windows in the mall.

* Check if in GameThread when creating a request, CreateRequest check in game thread

### v1.3.1 - 2024.9.30

####New features

* Add a SystemTemplateViewer to view and use hundreds of system setting templates.

####Issue resolution

* Fix the plugin downloaded from the store; llama.cpp cannot find the link library.

* Fix the issue of LLAMACpp with excessively long paths.

* Fix the llama.dll error after packaging Windows

* Fix the issue with ios/android reading file paths.

* Fix the incorrect name in Cllame settings.

### v1.3.0 - 2024.9.23

####Significant New Features

* Integrated llama.cpp, supporting local offline execution of large models.

### v1.2.0 - 2024.08.20

####New features

* Support OpenAI Image Edit/Image Variation

* Supports the Ollama API, enabling automatic retrieval of the list of models supported by Ollama.

### v1.1.0 - 2024.08.07

####New features

* Support Blueprint

### v1.0.0 - 2024.08.05

####New Features

* Complete basic functionality

* Supports OpenAI, Azure, Claude, Gemini

* Built-in comprehensive editor chat tool

--8<-- "footer_en.md"


> This post was translated using ChatGPT, please provide feedback in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Please point out any omissions. 
