---
layout: post
title: UE 插件 AIChatPlus 说明文档
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini]
description: UE 插件 AIChatPlus 说明文档
---
<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

# UE 插件 AIChatPlus 说明文档

## 公共仓库

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

## 插件获取

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## 插件简介

本插件支持 UE5.2+。

UE.AIChatPlus 是一个 UnrealEngine 插件，该插件实现了与各种 GPT AI 聊天服务进行通信，目前支持的服务有 OpenAI (ChatGPT, DALL-E)，Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini。未来还会继续支持更多服务提供商。它的实现基于异步 REST 请求，性能高效，方便 UE 开发人员接入这些 AI 聊天服务。

同时 UE.AIChatPlus 还包含了一个编辑器工具，可以直接在编辑器中使用这些 AI 聊天服务，生成文本和图像，分析图像等。

## 使用说明

### 编辑器聊天工具

菜单栏 Tools -> AIChatPlus -> AIChat 可打开插件提供的编辑器聊天工具

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


工具支持文本生成、文本聊天、图像生成，图像分析。

工具的界面大致为：

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

#### 主要功能

* 文本聊天：点击左下角的 `New Chat` 按钮，创建新的文本聊天会话。

* 图像生成：点击左下角的 `New Image Chat` 按钮，创建新的图像生成会话。

* 图像分析：`New Chat` 的部分聊天服务支持发送图像，例如 Claude, Google Gemini。点击输入框上方的 🖼️ 或 🎨 按钮即可加载需要发送的图像。

* 支持蓝图 (Blueprint)：支持蓝图创建 API 请求，完成文本聊天，图像生成等功能。

* 设置当前聊天角色：聊天框上方的下拉框可以设置当前发送文本的角色，可以通过模拟不同的角色来调节 AI 聊天。

* 清空会话：聊天框上方的 ❌ 按可以清空当前会话的历史消息。

* 全局设置：点击左下角的 `Setting` 按钮，可以打开全局设置窗口。可以设置默认文本聊天，图像生成的 API 服务，并设置每种 API 服务的具体参数。设置会自动保存在项目的路径 `$(ProjectFolder)/Saved/AIChatPlusEditor` 下。

* 会话设置：点击聊天框上方的设置按钮，可以打开当前会话的设置窗口。支持修改会话名字，修改会话使用的 API 服务，支持独立设置每个会话使用 API 的具体参数。会话设置自动保存在 `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

* 聊天内容修改：鼠标悬停在聊天内容上，会出现当个聊天内容的设置按钮，支持重新生成内容、修改内容、复制内容、删除内容、在下方重新生成内容（对于角色是用户的内容）

* 图像浏览：对于图像生成，点击图像会打开图像查看窗口 (ImageViewer) ，支持图片另存为 PNG/UE Texture，Texture 可以直接在内容浏览器 (Content Browser) 查看，方便图片在编辑器内使用。另外还支持删除图片、重新生成图片、继续生成更多图片等功能。对于 Windows 下的编辑器，还支持复制图片，可以直接把图片复制到剪贴板，方便使用。会话生成的图片也会自动保存在每个会话文件夹下面，通常路径是 `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`。

蓝图：

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

全局设置：

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

会话设置：

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

修改聊天内容：

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

图像查看器：

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

### 核心代码介绍

目前插件分成两个模块： AIChatPlusCommon (Runtime) 和 AIChatPlusEditor (Editor) 两个模块。

AIChatPlusCommon 负责处理发送请求和解析回复内容；AIChatPlusEditor 负责实现编辑器 AI 聊天工具。

具体负责发送请求的 UClass 是 FAIChatPlus_xxxChatRequest，每种 API 服务都分别有独立的 Request UClass。请求的回复通过 UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase 两种 UClass 来获取，只需要注册相应的回调委托。

发送请求之前需要先设置好 API 的参数和发送的消息，这块是通过 FAIChatPlus_xxxChatRequestBody 来设置。回复的具体内容也解析到 FAIChatPlus_xxxChatResponseBody 中，收到回调的时候可以通过特定接口获取 ResponseBody。

更多源码细节可在 UE 商城获取：[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)


### 更新日志

#### v1.2.0 - 2024.08.20

* 支持 OpenAI Image Edit/Image Variation
* 支持 Ollama API，支持自动获取 Ollama 支持的模型列表

#### v1.1.0 - 2024.08.07

* 支持蓝图

#### v1.0.0 - 2024.08.05

* 基础完整功能
* 支持 OpenAI， Azure，Claude，Gemini
* 自带功能完善编辑器聊天工具

--8<-- "footer.md"
