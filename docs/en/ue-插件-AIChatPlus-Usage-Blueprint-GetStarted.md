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

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Get Started" />

#Blueprint Section - Get Started

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

## Get Started

Below, let's take OpenAI as an example to introduce the basic usage of blueprints.

###Text chat

Using OpenAI for text chatting.

Create a node in the blueprint by right-clicking, named `Send OpenAI Chat Request In World`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Create an Options node, and set `Stream=true, Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Create Messages, add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Create a Delegate to receive the output information from the model and print it on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, run the blueprint, and you will see the game screen displaying the message returned by printing the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Generate image from text.

Create an image using OpenAI.

In the blueprint, right-click to create a node named "Send OpenAI Image Request", and set "In Prompt" to "a beautiful butterfly".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Create an Options node, and set `Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Bind the "On Images" event and save the images to the local hard drive.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

The complete blueprint looks like this, run the blueprint, and you will see the image saved in the specified location.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

###Generate text from image.

Use OpenAI Vision to analyze images.

Create a node called `Send OpenAI Image Request` by right-clicking on the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_1.png)

Create an Options node and set `Api Key="your API key from OpenAI"`, then set the model to `gpt-4o-mini`.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_2.png)

Create Messages.
Create a node "Import File as Texture 2D" first, and read an image from the file system.
Convert the image into a format that the plugin can utilize through the node "Create AIChatPlus Texture From Texture2D".
Connect the image to the "Images" field of the "AIChatPlus_ChatRequestMessage" node using the "Make Array" node.
Set the "Content" field content to "describe this image".

As shown in the figure:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_3.png)

The complete blueprint looks like this, run the blueprint, and you will see the results displayed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_4.png)

--8<-- "footer_en.md"


> This post was translated using ChatGPT, please provide feedback in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
