---
layout: post
title: Ollama
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
description: Ollama
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Ollama" />

#Blueprint Chapter - Ollama

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_all.png)

##Obtain Ollama

You can obtain the installation package for local installation through the Ollama official website: [ollama.com](https://ollama.com/)

You can use Ollama through the Ollama API interface provided by others.

Download the model using Ollama locally.

```shell
> ollama run qwen:latest
> ollama run moondream:latest
```

##Text chat

Create a "Ollama Options" node, set the parameters "Model" and "Base Url". If Ollama is running locally, the "Base Url" is usually "http://localhost:11434".

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_chat_1.png)

Connect the "Ollama Request" node with the relevant "Messages" node, click on run, and you will be able to see the chat messages returned by Ollama printed on the screen. Refer to the image for details.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

##Generate Text from Image

Ollama also supports the llava library, providing the capability of Vision.

First obtain the Multimodal model file:

```shell
> ollama run moondream:latest
```

Set the "Options" node, and set "Model" to moondream:latest.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_1.png)

Read the image flower.png and set the message.

![flower.png](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_3.png)

Connect to the "Ollama Request" node, click run, and you will see the chat messages returned by Ollama printed on the screen.

![](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_4.png)

![](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_5.png)

--8<-- "footer_en.md"


> This post was translated using ChatGPT. Please provide [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
