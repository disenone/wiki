---
layout: post
title: Gemini
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
description: Gemini
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Gemini" />

#Blueprint Chapter - Gemini

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_all.png)

###Text chat

Create a node called "Gemini Chat Options" and configure the parameters "Model" and "API Key."

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_chat_1.png)

Create a "Gemini Chat Request" node, and connect it to the "Options" and "Messages" nodes. Click on run, and you will see Gemini chat information printed on the screen, as shown in the image:

![](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###Generate text from image.

Create a "Gemini Chat Options" node as well, and configure the parameters "Model" and "Api Key".

Read the image file flower.png and set it to "Messages".

![flower.png](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_vision_1.png)

Create a "Gemini Chat Request" node, click on Run, and you will see the chat messages returned by Gemini printed on the screen, as shown below:

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_vision_2.png)

###Convert audio into text

Gemini supports converting audio into text.

Create the following blueprint, set up audio loading, configure the Gemini Options, click Run, and you will see the chat messages returned by Gemini after processing the audio on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

--8<-- "footer_en.md"


> This post was translated using ChatGPT, please provide feedback in [**反馈**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
