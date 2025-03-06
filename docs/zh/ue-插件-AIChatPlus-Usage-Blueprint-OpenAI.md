---
layout: post
title: OpenAI
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini, Ollama]
description: OpenAI
---
<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - OpenAI" />

# 蓝图篇 - OpenAI

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_all.png)

在 [Get Started](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md) 章节已经介绍过 OpenAI 的基本用法，我们在这里再给出详细的用法。

## 文本聊天

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

## 本文生成图片

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

## 图片生成文字

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

## 修改图片

OpenAI 支持对图片标记的区域进行修改

首先准备两张图片

一张是需要修改的图片 src.png

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_1.png)

一张是把需要修改的区域标记出来的图片 mask.png，可以通过修改源图片，把修改区域的透明度设置成 0，即 Alpha 通道数值改成 0

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_2.png)

分别读取以上两张照片，组合成数组

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_3.png)

创建 "OpenAI Image Options" 节点，设置 ChatType = Edit，并修改 "End Point Url" = v1/images/edits

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_4.png)

创建 "OpenAI Image Request"，设置 "Prompt" 为 "change into two butterfly"，连接 "Options" 节点 和 图片数组，并把生成的图片保存到文件系统中。

完整的蓝图看起来是这样的：

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_5.png)

运行蓝图，生成的图片保存在指定的位置上

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_6.png)

## 图片变种

OpenAI 支持根据输入的图片生成类似的变种 (Variation)

首先还是准备一张图片 src.png，并在蓝图中读取进来

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_1.png)

创建 "OpenAI Image Options" 节点，设置 ChatType = Variation，并修改 "End Point Url" = v1/images/variations

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_2.png)

创建 "OpenAI Image Request"，保留 "Prompt" 为空，连接 "Options" 节点 和 图片，并把生成的图片保存到文件系统中。

完整的蓝图看起来是这样的：

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_3.png)

运行蓝图，生成的图片保存在指定的位置上

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_4.png)

--8<-- "footer.md"
