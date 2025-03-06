---
layout: post
title: Claude
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini, Ollama]
description: Claude
---
<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Claude" />

# 蓝图篇 - Claude

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/claude_all.png)

## 文本聊天

创建 "Options" 节点，设置参数 "Model", "Api Key", "Anthropic Version"

![](assets/img/2024-ue-aichatplus/usage/blueprint/claude_chat_1.png)

连接 "Claude Request" 节点 和 "Messages" 相关节点，点击运行，即可看到屏幕上打印 Claude 返回的聊天信息。如图

![](assets/img/2024-ue-aichatplus/usage/blueprint/claude_chat_2.png)

## 图片生成文字

Claude 同样支持 Vision 功能

在蓝图中右键创建一个节点 `Send Claude Chat Request`

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

创建 Options 节点，并设置 `Stream=true, Api Key="you api key from Clude", Max Output Tokens=1024`

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

创建 Messages，从文件创建 Texture2D，并从 Texture2D 创建 AIChatPlusTexture，把 AIChatPlusTexture 添加到 Message 中

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Event 并把信息打印到游戏屏幕上

完整的蓝图看起来是这样的，运行蓝图，即可看到游戏屏幕在打印大模型返回的消息

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)


--8<-- "footer.md"
