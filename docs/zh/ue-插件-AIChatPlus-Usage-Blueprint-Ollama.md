---
layout: post
title: Ollama
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini, Ollama]
description: Ollama
---
<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Ollama" />

# 蓝图篇 - Ollama

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_all.png)

## 获取 Ollama

可以通过 Ollama 官网获取安装包本地安装：[ollama.com](https://ollama.com/)

可以通过其他人提供的 Ollama API 接口使用 Ollama。

本地使用 Ollama 下载模型：

```shell
> ollama run qwen:latest
> ollama run moondream:latest
```

## 文本聊天

创建 "Ollama Options" 节点，设置参数 "Model", "Base Url"，如果是本地运行的 Ollama，则 "Base Url" 一般是 "http://localhost:11434"

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_chat_1.png)

连接 "Ollama Request" 节点 和 "Messages" 相关节点，点击运行，即可看到屏幕上打印 Ollama 返回的聊天信息。如图

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## 图片生成文字 llava

Ollama 同样支持了 llava 库，提供了 Vision 的能力

首先获取 Multimodal 模型文件：

```shell
> ollama run moondream:latest
```

设置 "Options" 节点，"Model" 设置为 moondream:latest

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_1.png)

读取图片 flower.png，并设置 Message

![flower.png](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_3.png)

连接 "Ollama Request" 节点，点击运行，即可看到屏幕上打印 Ollama 返回的聊天信息。如图

![](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_4.png)

![](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_5.png)

--8<-- "footer.md"
