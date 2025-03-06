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

#Editorial Section - Get Started

##Editor chat tool.

Menu bar Tools -> AIChatPlus -> AIChat can open the editor chatting tool provided by the plugin

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


The tool supports text generation, text chat, image generation, and image analysis.

The interface of the tool is roughly as follows:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

##Main functions

* **Offline large models**: Integrated llama.cpp library, supporting local offline execution of large models

* **Text Chat**: Click on the `New Chat` button in the bottom left corner to start a new text chat session.

* **Image Generation**: Click the `New Image Chat` button in the bottom left corner to start a new image generation session.

**Image Analysis**: Some chat services of 'New Chat' support sending images, such as Claude, Google Gemini. You can simply click the 🖼️ or 🎨 button above the input box to load the image you want to send.

* **Audio Processing**: The tool allows reading audio files (.wav) and recording function, enabling communication with AI using the obtained audio.

*Set Current Chat Role*: The drop-down menu at the top of the chat box can be used to set the role of the character currently sending messages. This allows for simulating different roles to adjust the AI chat.

* **Clear Chat**: The ❌ button at the top of the chat box can clear the history of messages in the current conversation.

* **Dialogue Templates**: Hundreds of built-in dialogue templates are available to easily manage common issues.

**Global Settings**: Click on the `Setting` button in the lower left corner to open the global settings window. You can customize default text chat, image generation API services, and configure specific parameters for each API service. The settings will be automatically saved in the project path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

* **Conversation Settings**: Click the settings button above the chat box to open the settings window for the current conversation. You can change the conversation name, the API service used for the conversation, and customize specific parameters for each conversation's API. Conversation settings are automatically saved in `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`.

* **Chat Content Editing**: When hovering over a chat message, a settings button for that specific message will appear. It supports functions like regenerating content, editing content, copying content, deleting content, as well as regenerating content below (for messages where the user is the sender).

**Image browsing**: For image generation, clicking on an image will open the image viewing window (ImageViewer), supporting saving images as PNG/UE Texture. Textures can be viewed directly in the Content Browser, making it convenient for image use within the editor. Additionally, functionalities include deleting images, regenerating images, and continuing to generate more images. For editors on Windows, copying images is also supported, enabling direct copying to the clipboard for easy use. Images generated during sessions will automatically be saved in each session folder, typically located at `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Global Settings:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Conversation settings:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Edit Chat Content:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Image Viewer:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Using offline large models

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Dialogue Template

![system template](assets/img/2024-ue-aichatplus/system_template.png)

##Using offline model Cllama (llama.cpp) to edit tool.

The following instructions explain how to use the offline model llama.cpp in the AIChatPlus editor tool.

Firstly, download the offline model from the HuggingFace website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Place the model in a specific folder, such as within the Content/LLAMA directory of the game project.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Open the AIChatPlus editor tool: Tools -> AIChatPlus -> AIChat, create a new chat session, and open the session settings page.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Set the API to Cllama, enable Custom API Settings, add the model search path, and select the model.


![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Start chatting!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

##Use the offline model Cllama (llama.cpp) in the editor tool to process images.

Download the offline model MobileVLM_V2-1.7B-GGUF from the HuggingFace website and place it in the directory Content/LLAMA: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)Translate these text into English language:

和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but the text you provided is not meaningful or intelligible.

Set the session model:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)


Start chatting by sending a picture.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

##The editor uses OpenAI chat.

Open the chat tool, go to Tools -> AIChatPlus -> AIChat, create a new chat session, set the session to ChatApi as OpenAI, and configure the interface parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Start chatting:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Switching the model to GPT-4o / GPT-4o-mini enables the use of OpenAI's visual feature to analyze images.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

##The editor utilizes OpenAI to process images (create/modify/alter).

Create a new image chat session in the messaging tool, name it "New Image Chat," adjust session settings to OpenAI, and configure parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Create an image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Edit the image by changing the Image Chat Type to Edit, and upload two images. One should be the original image, and the other should be a masked image where the transparent areas (with an alpha value of 0) indicate the areas that need to be edited.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Modify the type of the image chat to "Variation" and upload an image. OpenAI will provide a variation of the original image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

##The editor uses Azure.

Create a new conversation (New Chat), change ChatApi to Azure, and configure Azure's API parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Start chatting.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

##The editor uses Azure to create images.

Create a new Image Chat session, switch from ChatApi to Azure, and configure the Azure API parameters. Please note that if using the dall-e-2 model, the Quality and Stype parameters should be set to not_use.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Start chatting to let Azure create an image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

##The editor utilizes Claude for chatting and analyzing images.

Create a new conversation (New Chat), change ChatApi to Claude, and configure Claude's Api parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

##The editor uses Ollama for chatting and analyzing images.

Create a new chat session, change ChatApi to Ollama, and configure Ollama's API parameters. If it's a text chat, set the model to a text model like llama3.1; if image processing is needed, set the model to one that supports vision, such as moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)


###The editor uses Gemini.

Create a new chat session, change ChatApi to Gemini, and configure Gemini's API parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

##The editor uses Gemini to send audio.

Choose to read audio from a file, from an asset, or record audio from the microphone to generate the audio to be sent.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

##The editor uses Deepseek.

Create a new chat session, change ChatApi to OpenAi, and configure the Deepseek API parameters. Add a new candidate model named deepseek-chat and set the model to deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

--8<-- "footer_en.md"


> This post has been translated using ChatGPT. Please provide your feedback in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
