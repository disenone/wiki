---
layout: post
title: CllamaServer (llama.cpp server)
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini, Ollama, llama.cpp, CllamaServer]
description: CllamaServer (llama.cpp server)
---
<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - CllamaServer (llama.cpp server)" />

# 蓝图篇 - CllamaServer (llama.cpp server)

<!-- 需要图片：展示 CllamaServer 相关的所有蓝图节点概览，类似其他文档的 xxx_all.png -->
![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_all.png)

## 概述

CllamaServer 是基于 llama.cpp 的 Server 模式实现的，可以在本地启动一个兼容 OpenAI API 的服务器，支持多种功能：

* **本地推理服务**: 在本地启动 AI 推理服务器，无需依赖外部 API
* **兼容 OpenAI API**: 使用 OpenAI 兼容的 API 格式，方便迁移和集成
* **多会话支持**: 支持多个并发请求
* **Tool Calling**: 支持函数调用功能
* **语音转文字**: 支持 Speech-to-Text 功能
* **可视化管理**: 编辑器内置 Server 管理界面

与 Cllama 的区别：
* **Cllama**: 直接在进程内加载模型进行推理，单次只能处理一个请求
* **CllamaServer**: 启动独立的 HTTP 服务器，可以处理多个并发请求，API 兼容 OpenAI 格式

## 准备工作

由于是本地运行，需要先准备好离线模型文件，例如从 HuggingFace 下载：[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

把模型放在某个文件夹下面，譬如放在游戏项目的目录 `Content/LLAMA` 下。

## 创建 CllamaServer

### 使用蓝图创建 Server

在蓝图中右键创建节点 `Create Cllama Server In World`

<!-- 需要图片：展示在蓝图中右键搜索 "Create Cllama Server" 并创建节点的截图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_1.png)

### 配置 Server 参数

创建 `Cllama Server Param` 节点，并配置关键参数：

* **Model**: 模型文件路径（必填）
* **Port**: 服务器端口（0 表示自动分配）
* **Host**: 监听地址，默认 `127.0.0.1`
* **NGpuLayers**: GPU 层数（-1 表示全部使用 GPU）

<!-- 需要图片：展示创建 FAIChatPlus_CllamaServerParam 节点，设置 Model 路径、Port、NGpuLayers 等参数的截图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_2.png)

### 绑定回调事件

绑定 Server 的回调事件：

* **On Started**: Server 启动成功时触发
* **On Stopped**: Server 停止时触发
* **On Failed**: Server 启动失败时触发

<!-- 需要图片：展示绑定 OnStartedListeners、OnStoppedListeners、OnFailedListeners 事件的蓝图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_3.png)

### 完整的创建蓝图

完整的 Server 创建蓝图如下：

<!-- 需要图片：展示完整的 Server 创建蓝图全貌，包括参数设置、创建节点、回调绑定 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_4.png)

运行蓝图后，Server 启动成功会触发 `On Started` 事件。

<!-- 需要图片：展示 Server 启动成功后的运行结果，显示启动成功的日志或屏幕输出 -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_5.png) -->

## Server 参数详解

`FAIChatPlus_CllamaServerParam` 结构体包含以下参数：

### 常用参数

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|-------|------|
| Model | FString | - | 模型文件路径（必填） |
| Port | int32 | 0 | 监听端口，0 表示自动分配 |
| Host | FString | 127.0.0.1 | 监听地址 |
| NGpuLayers | int32 | -1 | GPU 层数，-1 表示全部 |
| bUseJinja | bool | false | 使用 Jinja 模板 |
| MMProj | FString | - | 多模态投影文件路径 |
| Temperature | float | 0.8 | 采样温度 |

### 推理参数

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|-------|------|
| CtxSize | int32 | 4096 | 上下文大小 |
| NPredict | int32 | -1 | 预测 Token 数，-1 表示无限 |
| Threads | int32 | -1 | CPU 线程数，-1 表示自动 |
| BatchSize | int32 | 2048 | 批处理大小 |

### 采样参数

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|-------|------|
| TopK | int32 | 40 | Top-K 采样 |
| TopP | float | 0.9 | Top-P 采样 |
| MinP | float | 0.1 | Min-P 采样 |
| RepeatPenalty | float | 1.0 | 重复惩罚 |

### 服务器参数

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|-------|------|
| ApiKey | FString | - | API 密钥（可选） |
| Timeout | int32 | 600 | 超时时间（秒） |
| Parallel | int32 | 1 | 并行序列数 |
| bNoWebUI | bool | false | 禁用 Web UI |
| bVerbose | bool | false | 详细日志 |

## 使用 CllamaServer 进行聊天

### 创建 Chat Request

Server 启动成功后，可以使用 `Send CllamaServer Chat Request` 节点发送聊天请求。

<!-- 需要图片：展示在蓝图中右键搜索 "CllamaServer Chat Request" 并创建节点的截图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_1.png)

### 配置 Chat Options

创建 `CllamaServer Chat Request Options` 节点，设置 BaseUrl 为 Server 地址。

可以通过 `Get Server Info By ID` 节点获取 Server 信息。

<!-- 需要图片：展示创建 FAIChatPlus_CllamaServerChatRequestOptions 节点，使用 Get Http Address 获取 Server 地址并设置到 BaseUrl 的蓝图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_2.png)

### 创建 Messages

创建 Messages 数组，添加 System Message 和 User Message。

<!-- 需要图片：展示创建 Messages 数组，包含 System Message（设置助手角色）和 User Message（用户问题）的蓝图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_3.png)

### 绑定回调处理响应

绑定 `On Message` 或 `On Message Finished` 事件来接收模型响应。

<!-- 需要图片：展示绑定 OnMessageListeners 事件，并在回调中打印消息到屏幕的蓝图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_4.png)

### 完整的聊天蓝图

完整的聊天蓝图如下：

<!-- 需要图片：展示完整的聊天蓝图全貌，包括创建 Server、等待启动、发送聊天请求、处理响应的完整流程 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_5.png)

### 运行结果

运行蓝图，可以看到模型返回的消息显示在屏幕上。

<!-- 需要图片：展示聊天运行结果，屏幕上显示模型返回的回复内容 -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_6.png) -->

## Server 管理

### 获取 Server 信息

使用 `Get Server Info` 节点获取 Server 的详细信息。

<!-- 需要图片：展示使用 Get Server Info 节点获取 FAIChatPlus_CllamaServerInfo 的蓝图，并 Break 显示各字段 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_info_1.png)

Server Info 包含以下信息：
* **ServerID**: 服务器唯一 ID
* **Host**: 监听地址
* **Port**: 监听端口
* **Address**: 完整地址（host:port）
* **HttpAddress**: HTTP 地址（http://host:port）
* **bIsRunning**: 是否正在运行
* **Param**: 服务器参数

### 停止 Server

使用 `Stop Server By ID` 节点停止当前 Server。

<!-- 需要图片：展示调用 Stop Cllama Server 节点的蓝图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_stop_1.png)

### 静态管理函数

AIChatPlus 提供了一系列静态函数用于管理所有 Server：

| 函数 | 说明 |
|-----|------|
| `Is Server Valid (Static)` | 检查 Server 是否有效 |
| `Is Server Running (Static)` | 检查 Server 是否运行中 |
| `Stop Server By ID` | 通过 ID 停止指定 Server |
| `Stop All Servers` | 停止所有 Server |
| `Get Server Info By ID` | 通过 ID 获取 Server 信息 |
| `Get All Server IDs` | 获取所有 Server ID |
| `Get Server By ID` | 通过 ID 获取 Server 实例 |

<!-- 需要图片：展示使用 Get All Server IDs 和 Stop All Servers 等静态管理函数的蓝图示例 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_static_1.png)

## 多模态支持

CllamaServer 支持多模态模型（如 Moondream、Qwen2-VL 等）。

### 配置多模态参数

在 Server 参数中设置 `MMProj`（多模态投影文件路径）：

<!-- 需要图片：展示在 Server Param 中设置 Model 和 MMProj 两个路径的蓝图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_1.png)

### 发送图片消息

在 Messages 中添加图片：

<!-- 需要图片：展示读取图片文件，创建包含图片的 Message，通过 CllamaServer 发送请求的蓝图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_2.png)

<!-- ### 运行结果 -->

<!-- 需要图片：展示图片识别的运行结果，屏幕显示模型对图片内容的描述 -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_3.png) -->

## Tool Calling

CllamaServer 支持 Tool Calling（函数调用）功能，用法与 OpenAI 类似。

详细用法请参考 [Tool Call](ue-插件-AIChatPlus-Usage-Blueprint-ToolCall.md) 文档。

使用 CllamaServer 进行 Tool Call 时，需要：
1. 在 Server 参数中设置 `bUseJinja = true`
2. 在 Chat Options 的 Tools 字段中定义工具

<!-- 需要图片：展示 CllamaServer Tool Call 的完整蓝图，包括 bUseJinja=true 的设置和 Tools 定义 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_tool_1.png)

## 编辑器 Server 管理

AIChatPlus 在编辑器工具中提供了可视化的 CllamaServer 管理界面，方便创建、监控和管理多个 Server。

打开编辑器工具：`Tools -> AIChatPlus -> AIChat`，打开 Cllama Server Manager 标签页。

<!-- 需要图片：展示编辑器中 CllamaServer 管理界面的截图，显示 Server 列表、创建按钮、状态信息等 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_editor_1.png)

在编辑器中可以：
* 创建新的 Server
* 查看运行中的 Server 状态
* 停止指定的 Server
* 配置 Server 参数
* Server 配置会自动保存

<!-- 需要图片：展示编辑器中创建新 Server 的界面，显示参数配置面板 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_editor_2.png)

## 与其他 API 的关系

由于 CllamaServer 兼容 OpenAI API 格式，你也可以使用 OpenAI 的 Chat Request 节点来与 CllamaServer 通信，只需将 `BaseUrl` 设置为 CllamaServer 的地址即可。

<!-- 需要图片：展示使用 OpenAI Chat Request 节点，但 BaseUrl 设置为 CllamaServer 地址的蓝图示例 -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_openai_1.png) -->

--8<-- "footer.md"
