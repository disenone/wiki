---
layout: post
title: OpenAI
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
description: OpenAI
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - OpenAI" />

#Blueprint Section - OpenAI

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_all.png)

At [Get Started](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)The basic usage of OpenAI has been introduced in previous sections. Here, we provide a detailed explanation of its usage.

##Text chat

Use OpenAI for text chatting.

Create a node in the blueprint by right-clicking and selecting `Send OpenAI Chat Request In World`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Create the Options node and set `Stream=true, Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Create Messages, add a System Message and a User Message separately.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Create a delegate to receive the model's output information and print it on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this. Running the blueprint will show the message returned on the game screen printing large models.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

##Generate image based on the text

Create images using OpenAI.

In the blueprint, right-click to create a node named 'Send OpenAI Image Request', and set 'In Prompt="a beautiful butterfly"'.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Create an Options node and set `Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Bind the "On Images" event and save the images to the local hard drive.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

The complete blueprint looks like this. Run the blueprint to see the image saved at the specified location.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

##Generate Text from Image

Use OpenAI Vision to analyze images.

Create a node `Send OpenAI Image Request` by right-clicking on the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_1.png)

Create an Options node, and set `Api Key="your API key from OpenAI"`, and set the model to `gpt-4o-mini`.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_2.png)

Create Messages.
Create a node first: "Import File as Texture 2D" to load an image from the file system.
Convert the image into a format usable by the plugin through the node "Create AIChatPlus Texture From Texture2D".
Use the "Make Array" node to connect the image to the "Images" field of the "AIChatPlus_ChatRequestMessage" node.
Set the content of the "Content" field to "describe this image".

As shown in the figure:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_3.png)

The complete blueprint looks like this, run the blueprint, and you will see the results displayed on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_4.png)

##Edit image

OpenAI supports modifying regions marked on images.

First, prepare two images.

An image that needs to be edited, src.png

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_1.png)

One of the images is called mask.png, which marks the areas that need to be modified. By editing the original image, you can set the transparency of the modified areas to 0, that is, change the Alpha channel value to 0.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_2.png)

Separately read the two photos above and combine them into an array.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_3.png)

Create a "OpenAI Image Options" node, set ChatType = Edit, and change "End Point Url" to v1/images/edits.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_4.png)

Create an "OpenAI Image Request," set the "Prompt" to "change into two butterflies," connect the "Options" node to the image array, and save the generated images to the file system.

The complete blueprint looks like this:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_5.png)

Run the blueprint and save the generated image in the specified location.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_6.png)

##Image variants

OpenAI supports generating similar variations based on the input image.

First, prepare an image named src.png and then import it into the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_1.png)

Create a node called "OpenAI Image Options" and set ChatType to Variation, then update the "End Point Url" to v1/images/variations.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_2.png)

Create an "OpenAI Image Request", leave the "Prompt" blank, link to the "Options" node and the image, and save the generated image to the file system.

The complete blueprint looks like this:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_3.png)

Run the blueprint, and save the generated image at the specified location.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_4.png)

--8<-- "footer_en.md"


> (https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
