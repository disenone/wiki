---
layout: post
title: Gemini
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini, Ollama]
description: Gemini
---
<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Gemini" />

# 蓝图篇 - Gemini

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_all.png)

### 文本聊天

创建 "Gemini Chat Options" 节点，设置参数 "Model", "Api Key"

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_chat_1.png)

创建 "Gemini Chat Request" 节点，并连接 "Options" 和 "Messages" 节点，点击运行，即可看到屏幕上打印 Gemini 返回的聊天信息，如图：

![](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

### 图片生成文字

同样创建 "Gemini Chat Options" 节点，设置参数 "Model", "Api Key"

从文件读取图片 flower.png，并设置到 "Messages" 上

![flower.png](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_vision_1.png)

创建 "Gemini Chat Request" 节点，点击运行，即可看到屏幕上打印 Gemini 返回的聊天信息，如图：

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_vision_2.png)

### 音频生成文字

Gemini 支持把音频转成文字

创建如下蓝图，设置加载音频，设置好 Gemini Options，点击运行，即可看到屏幕上打印 Gemini 处理音频后返回的聊天信息

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

--8<-- "footer.md"
