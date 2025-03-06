---
layout: post
title: Azure
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
description: Azure
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Azure" />

#Blueprint Section - Azure

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_all.png)

The usage of Azure is quite similar to OpenAI, so let me briefly introduce it here.

##Text chat

Create a node called "Azure Chat Options" and configure the parameters "Deployment Name," "Base Url," and "Api Key."

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_chat_1.png)

Create a "Messages" related node, and connect it to "Azure Chat Request". Click on Run, and you will be able to see the chat information returned by Azure printed on the screen. See the illustration below.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

##Create image

Create an "Azure Image Options" node, and configure the parameters "Deployment Name," "Base URL," and "API Key."

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_image_1.png)

Set up nodes like "Azure Image Request," click run, and you'll see the chat information returned by Azure printed on the screen. See the image for reference.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

According to the settings in the blueprint above, the image will be saved in the path D:\Downloads\butterfly.png.

--8<-- "footer_en.md"


> This post was translated using ChatGPT, please provide [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
