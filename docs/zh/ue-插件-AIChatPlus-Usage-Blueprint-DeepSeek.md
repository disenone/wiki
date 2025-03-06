---
layout: post
title: DeepSeek
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini, Ollama]
description: DeepSeek
---
<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - DeepSeek" />

# 蓝图篇 - DeepSeek

因为 DeepSeek 兼容了 OpenAI 的 API 接口格式，所以我们可以很简单的使用 OpenAI 相关的节点来访问 DeepSeek，只要把相关的 url 修改成 DeepSeek 的 url 即可

# 文本聊天

创建 "OpenAI Chat Options" 节点，设置好 Model, Url, Api Key 参数

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/deepseek_chat_1.png)

其他设置跟 OpenAI 相同，完整的蓝图看起来像这样：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

运行即可在屏幕看看到 DeepSeek 的返回：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

--8<-- "footer.md"
