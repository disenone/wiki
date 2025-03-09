---
layout: post
title: Get Started
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
description: Get Started
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 编辑器篇 - Get Started" />

#Text Editor Section - Get Started

##Editor chatting tool

Menu bar Tools -> AIChatPlus -> AIChat can open the chat tool provided by the plugin editor.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chatting, image generation, and image analysis.

The interface of the tool is roughly as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

##Main functions

Offline large-scale models: Integrated llama.cpp library, supporting local offline execution of large models

**Text Chat**: Click the `New Chat` button in the bottom left corner to start a new text chat session.

**Image Generation**: Click the `New Image Chat` button in the bottom left corner to start a new image generation session.

**Image Analysis**: Some chat services in `New Chat` support sending images, such as Claude, Google Gemini. Simply click the 🖼️ or 🎨 buttons above the input box to load the image you want to send.

**Audio Processing**: The tool enables reading audio files (.wav) and recording functions, allowing you to chat with AI using the acquired audio.

**Set Current Chat Role**: The dropdown menu at the top of the chat box allows you to set the current character for sending text. You can simulate different characters to adjust the AI chat.

**Clear Chat**: The ❌ button at the top of the chat box can be clicked to clear the history of messages in the current conversation.

**Dialogue Template**: Built-in hundreds of conversation setting templates, making it easy to handle common issues.

**Global Settings**: Click on the `Setting` button in the bottom left corner to open the global settings window. Here you can configure default text chat, image generation API services, and specify parameters for each API service. Settings will be automatically saved in the project path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

**Conversation Settings**: Click on the settings button above the chat box to open the settings window for the current conversation. You can change the conversation name, modify the API service used for the conversation, and independently set specific parameters for the API used in each conversation. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

**Chat Content Editing**: When hovering over a chat message, a settings button will appear for that specific message, allowing options to regenerate, edit, copy, delete the content, or generate new content below (for user-generated content).

**Image Browser**: For image generation, clicking on an image will open the image viewer window (ImageViewer), supporting saving images as PNG/UE Textures. Textures can be directly viewed in the Content Browser, facilitating their use within the editor. Additionally, functions such as deleting images, regenerating images, and continuing to generate more images are supported. For editors on Windows, image copying is also supported, allowing images to be copied directly to the clipboard for convenient use. Images generated during sessions will also be automatically saved under each session folder, typically located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Global settings:

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

##Use the offline model Cllama (llama.cpp) with the editor tool.

The following explains how to use the offline model llama.cpp in the AIChatPlus editor tool.

Firstly, download the offline model from the HuggingFace website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Place the model inside a specific folder, for example, in the directory Content/LLAMA of the game project.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Open the AIChatPlus editor tool: Tools -> AIChatPlus -> AIChat, create a new chat session, and open the session settings page.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Set the Api to Cllama, enable Custom Api Settings, and add a model search path, then select the model.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Start chatting now!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

##Use the offline model Cllama (llama.cpp) in the editor tool to process images.

Download the offline model MobileVLM_V2-1.7B-GGUF from the HuggingFace website and place it in the Content/LLAMA directory: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)Translate these text into English language:

And [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)。

Set the session model:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Start chatting by sending a picture.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

##The editor is using OpenAI chat.

Open the chat tool, go to Tools -> AIChatPlus -> AIChat, create a new chat session "New Chat", and set the session "ChatApi" to OpenAI with the interface parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Start chatting:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Switching the model to GPT-4o/GPT-4o-mini enables the use of OpenAI's visual capabilities to analyze images.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

##The editor utilizes OpenAI to process images (create/modify/variate).

Create a new image chat in the messaging tool, name it as "New Image Chat," change the chat settings to OpenAI, and configure the parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Create image

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Edit the image, change the Image Chat Type to Edit, and upload two pictures: one is the original image, and the other one is the mask where the transparent parts (with alpha channel 0) indicate the areas that need to be modified.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Modify the image by changing the Image Chat Type conversation to Variation, and upload the modified image. OpenAI will provide a variant of the original picture.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

##The editor uses Azure.

Create a new chat session (New Chat), change ChatApi to Azure, and configure Azure's API parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

##The editor uses Azure to create images.

Create a new image chat session (New Image Chat), change ChatApi to Azure, and configure Azure's API parameters. Note that if using the dall-e-2 model, set the Quality and Stype parameters to not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Start chatting, let Azure create an image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

##The editor uses Claude to chat and analyze images.

Create a new chat session, rename ChatApi to Claude, and configure Claude's API parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Start chatting.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

##The editor uses Ollama for chatting and analyzing images.

Create a new chat session, change ChatApi to Ollama, and configure Ollama's API parameters. If it's a text chat, set the model to a text model like llama3.1; if image processing is needed, set the model to a vision-enabled model like moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Editor using Gemini

Create a new conversation (New Chat), change ChatApi to Gemini, and configure Gemini's API parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Start chatting.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

##The editor uses Gemini to send audio.

Select to read audio from file / read audio from asset / record audio from microphone, generate the audio to be sent.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

Start chatting.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

##The editor uses Deepseek.

Create a new chat session, change ChatApi to OpenAi, and configure the API parameters of Deepseek. Add a new candidate model named deepseek-chat, and set the model as deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Start chatting.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

--8<-- "footer_en.md"


> This post has been translated using ChatGPT. Please provide feedback in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
