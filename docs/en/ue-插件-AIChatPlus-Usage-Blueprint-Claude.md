---
layout: post
title: Claude
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
description: Claude
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Claude" />

#Blueprint Chapter - Claude

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/claude_all.png)

##Text chat

Create an "Options" node and set the parameters "Model", "API Key", "Anthropic Version".

![](assets/img/2024-ue-aichatplus/usage/blueprint/claude_chat_1.png)

Connect the "Claude Request" node to the associated "Messages" node, click run, and you will see Claude's chat messages printed on the screen. See image for reference.

![](assets/img/2024-ue-aichatplus/usage/blueprint/claude_chat_2.png)

##Generate text from images.

Claude also supports the Vision feature.

Create a node 'Send Claude Chat Request' in the blueprint by right-clicking.

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Create an Options node and set `Stream=true, Api Key="your API key from Clude", Max Output Tokens=1024`.

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Create Messages, create a Texture2D from a file, and then create AIChatPlusTexture from the Texture2D. Finally, add the AIChatPlusTexture to the Message.

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Event and print the information on the game screen.

The complete blueprint looks like this, run the blueprint, and you will see the message returned from printing the large model on the game screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)


--8<-- "footer_en.md"


> This post has been translated using ChatGPT. Please provide feedback in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
