---
layout: post
title: DeepSeek
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
description: DeepSeek
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - DeepSeek" />

#Blueprint Section - DeepSeek

Because DeepSeek is compatible with OpenAI's API interface format, we can easily use OpenAI's related nodes to access DeepSeek. Just modify the relevant URL to DeepSeek's URL.

#Text chatting

Create an "OpenAI Chat Options" node, and configure the Model, Url, and Api Key parameters.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/deepseek_chat_1.png)

The rest of the settings are the same as OpenAI's, the complete blueprint looks like this:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

Upon execution, you will see DeepSeek's output on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

--8<-- "footer_en.md"


> This post was translated using ChatGPT, please provide feedback in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
