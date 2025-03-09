---
layout: post
title: Get Started
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini, Ollama]
description: Get Started
---
<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 编辑器篇 - Get Started" />

# 编辑器篇 - Get Started

## 编辑器聊天工具

菜单栏 Tools -> AIChatPlus -> AIChat 可打开插件提供的编辑器聊天工具

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


工具支持文本生成、文本聊天、图像生成，图像分析。

工具的界面大致为：

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

## 主要功能

**离线大模型**：整合了 llama.cpp 库，支持本地离线执行大模型

**文本聊天**：点击左下角的 `New Chat` 按钮，创建新的文本聊天会话。

**图像生成**：点击左下角的 `New Image Chat` 按钮，创建新的图像生成会话。

**图像分析**：`New Chat` 的部分聊天服务支持发送图像，例如 Claude, Google Gemini。点击输入框上方的 🖼️ 或 🎨 按钮即可加载需要发送的图像。

**音频处理**：工具提供读取音频文件 (.wav) 和 录音功能，可以使用获得的音频跟 AI 聊天。

**设置当前聊天角色**：聊天框上方的下拉框可以设置当前发送文本的角色，可以通过模拟不同的角色来调节 AI 聊天。

**清空会话**：聊天框上方的 ❌ 按可以清空当前会话的历史消息。

**对话模版**：内置几百种对话设置模版，方便处理常用的问题。

**全局设置**：点击左下角的 `Setting` 按钮，可以打开全局设置窗口。可以设置默认文本聊天，图像生成的 API 服务，并设置每种 API 服务的具体参数。设置会自动保存在项目的路径 `$(ProjectFolder)/Saved/AIChatPlusEditor` 下。

**会话设置**：点击聊天框上方的设置按钮，可以打开当前会话的设置窗口。支持修改会话名字，修改会话使用的 API 服务，支持独立设置每个会话使用 API 的具体参数。会话设置自动保存在 `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

**聊天内容修改**：鼠标悬停在聊天内容上，会出现当个聊天内容的设置按钮，支持重新生成内容、修改内容、复制内容、删除内容、在下方重新生成内容（对于角色是用户的内容）

**图像浏览**：对于图像生成，点击图像会打开图像查看窗口 (ImageViewer) ，支持图片另存为 PNG/UE Texture，Texture 可以直接在内容浏览器 (Content Browser) 查看，方便图片在编辑器内使用。另外还支持删除图片、重新生成图片、继续生成更多图片等功能。对于 Windows 下的编辑器，还支持复制图片，可以直接把图片复制到剪贴板，方便使用。会话生成的图片也会自动保存在每个会话文件夹下面，通常路径是 `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`。

全局设置：

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

会话设置：

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

修改聊天内容：

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

图像查看器：

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

使用离线大模型

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

对话模版

![system template](assets/img/2024-ue-aichatplus/system_template.png)

## 编辑器工具使用离线模型 Cllama(llama.cpp)

以下说明如何在 AIChatPlus 编辑器工具中使用离线模型 llama.cpp

 首先，从 HuggingFace 网站下载离线模型：[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

把模型放在某个文件夹下面，譬如放在游戏项目的目录 Content/LLAMA 下

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

打开 AIChatPlus 编辑器工具：Tools -> AIChatPlus -> AIChat，新建聊天会话，并打开会话设置页面

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

设置 Api 为 Cllama，开启 Custom Api Settings， 并添加模型搜索路径，并选择模型

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

开始聊天！！

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

## 编辑器工具使用离线模型 Cllama(llama.cpp) 处理图片

从 HuggingFace 网站下载离线模型 MobileVLM_V2-1.7B-GGUF 同样放到目录 Content/LLAMA 下：[ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf) 和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)。

设置会话的模型：

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

发送图片开始聊天

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

## 编辑器使用 OpenAI 聊天

打开聊天工具 Tools -> AIChatPlus -> AIChat，创建新的聊天会话 New Chat，设置会话 ChatApi 为 OpenAI, 设置接口参数

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

开始聊天：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

切换模型为 gpt-4o / gpt-4o-mini，可以使用 OpenAI 的视觉功能分析图片

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

## 编辑器使用 OpenAI 处理图片（创建/修改/变种）

在聊天工具中创建新的图片会话 New Image Chat，修改会话设置为 OpenAI，并设置参数

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

创建图片

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

修改图片，把会话 Image Chat Type 修改为 Edit，并上传两张图片，一张是原图片，一张是 mask 其中透明的位置（alpha 通道为 0）表示需要修改的地方

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

图片变种，把会话 Image Chat Type 修改为 Variation，并上传一张图片，OpenAI 会返回一张原图片的变种

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

## 编辑器使用 Azure

新建会话（New Chat），把 ChatApi 改为 Azure，并设置 Azure 的 Api 参数

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

开始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

## 编辑器使用 Azure 创建图片

新建图片会话（New Image Chat），把 ChatApi 改为Azure，并设置 Azure 的 Api 参数，注意，如果是 dall-e-2 模型，需要把参数 Quality 和 Stype 设置成 not_use

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

开始聊天，让 Azure 创建图片

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

## 编辑器使用 Claude 聊天和分析图片

新建会话（New Chat），把 ChatApi 改为 Claude，并设置 Claude 的 Api 参数

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

开始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

## 编辑器使用 Ollama 聊天和分析图片

新建会话（New Chat），把 ChatApi 改为 Ollama，并设置 Ollama 的 Api 参数。如果是文本聊天，则设置模型为文本模型，如 llama3.1；如果需要处理图片，则设置模型为支持 vision 的模型，例如 moondream。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

开始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

### 编辑器使用 Gemini

新建会话（New Chat），把 ChatApi 改为 Gemini，并设置 Gemini 的 Api 参数。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

开始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

## 编辑器使用 Gemini 发送音频

选择 从文件读取音频 / 从 Asset 读取音频 / 从麦克风录取音频，生成需要发送的音频

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

开始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

## 編輯器使用 Deepseek

新建会话（New Chat），把 ChatApi 改为 OpenAi，并设置 Deepseek 的 Api 参数。新增 Candidate Models 叫做 deepseek-chat，并把 Model 设置为 deepseek-chat

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

开始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

--8<-- "footer.md"
