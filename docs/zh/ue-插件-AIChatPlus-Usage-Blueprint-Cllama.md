---
layout: post
title: Cllama (llama.cpp)
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini, Ollama, llama.cpp]
description: Cllama (llama.cpp)
---
<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Cllama (llama.cpp)" />

# 蓝图篇 - Cllama (llama.cpp)

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_all.png)

## 离线模型

Cllama 是基于 llama.cpp 来实现的，支持离线使用 AI 推理模型。

由于是离线，因为我们需要先准备好模型文件，譬如从 HuggingFace 网站下载离线模型：[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

把模型放在某个文件夹下面，譬如放在游戏项目的目录 Content/LLAMA 下

```shell
E:/UE/projects/FP_Test1/Content/LLAMA > ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

有了离线模型文件之后，我们就可以通过 Cllama 来进行 AI 聊天

## 文本聊天

使用 Cllama 进行文本聊天

在蓝图中右键创建一个节点 `Send Cllama Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

创建 Options 节点，并设置 `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

创建 Messages，分别添加一条 System Message 和 User Message

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

创建 Delegate 接受模型输出的信息，并打印在屏幕上

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完整的蓝图看起来是这样的，运行蓝图，即可看到游戏屏幕在打印大模型返回的消息

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## 图片生成文字 llava

Cllama 还实验性支持了 llava 库，提供了 Vision 的能力

首先准备好 Multimodal 离线模型文件，例如 Moondream （[moondream2-text-model-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-text-model-f16.gguf), [moondream2-mmproj-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-mmproj-f16.gguf)）或者 Qwen2-VL（[Qwen2-VL-7B-Instruct-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/Qwen2-VL-7B-Instruct-Q8_0.gguf), [mmproj-Qwen2-VL-7B-Instruct-f16.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-7B-Instruct-f16.gguf)）或者其他 llama.cpp 支持的 Multimodal 模型。

创建 Options 节点，分别设置参数 "Model Path" 和 "MMProject Model Path" 为对应的 Multimodal 模型文件。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_1.png)

创建节点读取图片文件 flower.png，并设置 Messages

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_3.png)

最后创建节点接受返回的信息，并打印到屏幕上，完整的蓝图看起来是这样的

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_4.png)

运行蓝图可看到返回的文字

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_5.png)

## llama.cpp 使用 GPU

"Cllama Chat Request Options" 增加参数 "Num Gpu Layer" ，可以设置 llama.cpp 的 gpu payload，可以控制需要在 GPU 上计算的层数。如图

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

## 处理打包后 .Pak 中的模型文件

开启 Pak 打包后，项目的所有资源文件都会放在 .Pak 文件中，当然也包含了离线模型 gguf 文件。

由于 llama.cpp 无法支持直接读取 .Pak 文件，因此需要把 .Pak 文件中的离线模型文件拷贝出来文件系统中。

AIChatPlus 提供了一个功能函数可以自动把 .Pak 中的模型文件拷贝处理，并放在 Saved 文件夹中：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

又或者你可以自己处理 .Pak 中的模型文件，关键就是需要把文件复制出来，因为 llama.cpp 无法正确读取 .Pak。

## 功能节点

Cllama 提供了一些功能节点方便获取当前环境下状态


"Cllama Is Valid"：判断 Cllama llama.cpp 是否正常初始化

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu"：判断 llama.cpp 在当前环境下是否支持 GPU backend

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Cllama Get Support Backends": 获取当前 llama.cpp 支持的所有 backends


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama Prepare ModelFile In Pak": 自动把 Pak 中的模型文件复制到文件系统中

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)


--8<-- "footer.md"
