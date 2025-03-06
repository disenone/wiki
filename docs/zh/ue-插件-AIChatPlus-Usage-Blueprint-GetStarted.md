---
layout: post
title: Get Started
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini, Ollama]
description: Get Started
---
<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Get Started" />

# 蓝图篇 - Get Started

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

## Get Started

下面以 OpenAI 为例，介绍蓝图的基本使用方法

### 文本聊天

使用 OpenAI 进行文本聊天

在蓝图中右键创建一个节点 `Send OpenAI Chat Request In World`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

创建 Options 节点，并设置 `Stream=true, Api Key="you api key from OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

创建 Messages，分别添加一条 System Message 和 User Message

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

创建 Delegate 接受模型输出的信息，并打印在屏幕上

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完整的蓝图看起来是这样的，运行蓝图，即可看到游戏屏幕在打印大模型返回的消息

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

### 本文生成图片

使用 OpenAI 创建图片

在蓝图中右键创建一个节点 `Send OpenAI Image Request`，并设置 `In Prompt="a beautiful butterfly"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

创建 Options 节点，并设置 `Api Key="you api key from OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

绑定 On Images 事件，并把图片保存到本地硬盘上

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

完整的蓝图看起来是这样的，运行蓝图，即可看到图片保存在指定的位置上

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

### 图片生成文字

使用 OpenAI Vision 分析图片

在蓝图中右键创建一个节点 `Send OpenAI Image Request`

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_1.png)

创建 Options 节点，并设置 `Api Key="you api key from OpenAI"`，设置模型为 `gpt-4o-mini`

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_2.png)

创建 Messages。
* 先创建节点 "Import File as Texture 2D" 从文件系统读取一张图片；
* 通过节点 "Create AIChatPlus Texture From Texture2D" 把图片转换成插件可用的对象；
* 通过 "Make Array" 节点把图片连接到节点 "AIChatPlus_ChatRequestMessage" 的 "Images" 字段上；
* 设置 "Content" 字段内容为 "describe this image"。

如图：

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_3.png)

完整的蓝图看起来是这样的，运行蓝图，即可看到结果显示在屏幕上

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_4.png)

--8<-- "footer.md"
