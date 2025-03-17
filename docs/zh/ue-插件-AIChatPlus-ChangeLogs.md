---
layout: post
title: 版本日志
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini, Ollama]
description: 版本日志
---
<meta property="og:title" content="UE 插件 AIChatPlus 版本日志" />

# UE 插件 AIChatPlus 版本日志

## v1.6.2 - 2025.03.17

### 新功能

* Cllama 增加 KeepContext 参数，默认 false，Context 在 Chat 结束后自动销毁

* Cllama 增加 KeepAlive 参数，可以减少 model 重复读取

## v1.6.1 - 2025.03.07

### Bug Fix

* OpenAI Image Chat 蓝图支持输入图片

* Editor Tool Cllama mmproj 模型允许空

## v1.6.0 - 2025.03.02

### 新功能

* llama.cpp 升级至 b4604 版本

* Cllama 支持 GPU backends: cuda 和 metal

* chat tool Cllama 支持使用 GPU

* 支持读取打包 Pak 中的模型文件

### Bug Fix

* 修复 Cllama 在推理的时候 reload 会崩溃的问题

* 修复 ios 编译报错

## v1.5.1 - 2025.01.30

### 新功能

* 只允许 Gemini 发音频

* 优化获取 PCMData 的方法，生成 B64 的时候再解压缩音频数据

* request 增加两个回调 OnMessageFinished OnImagesFinished

* 优化 Gemini Method，自动根据 bStream 获取 Method

* 增加一些蓝图函数，方便转换 Wrapper 到实际类型，并且获取 Response Message 和 Error

### Bug Fix

* 修复 Request Finish 多次调用问题

## v1.5.0 - 2025.01.29

### 新功能

* 支持给 Gemini 发音频

* 编辑器工具支持发送音频和录音

### Bug Fix

* 修复 Session copy 失败的 bug

## v1.4.1 - 2025.01.04

### 问题修复

* 聊天工具支持只发图片不发信息

* 修复 OpenAI 接口发送图片问题失败文图

* 修复 OpanAI、Azure 聊天工具设置遗漏了参数 Quality、Style、ApiVersion 问题=

## v1.4.0 - 2024.12.30

### 新功能

* （实验性功能）Cllama(llama.cpp) 支持多模态模型，可以处理图片

* 所有的蓝图类型参数都加上了详细提示

## v1.3.4 - 2024.12.05

### 新功能

* OpenAI 支持 vision api

### 问题修复

* 修复 OpenAI stream=false 时的错误

## v1.3.3 - 2024.11.25

### 新功能

* 支持 UE-5.5

### 问题修复

* 修复部分蓝图不生效问题

## v1.3.2 - 2024.10.10

### 问题修复

* 修复 手动停止 request 的时候 cllama 崩溃

* 修复商城下载版本 win 打包找不到 ggml.dll llama.dll 文件的问题

* 创建请求时检查是否在 GameThread 中，CreateRequest check in game thread

## v1.3.1 - 2024.9.30

### 新功能

* 增加一个 SystemTemplateViewer，可以查看和使用几百个 system 设置模版

### 问题修复

* 修复从商城下载的插件，llama.cpp 找不到链接库

* 修复 LLAMACpp 路径过长问题

* 修复 windows 打包后的链接 llama.dll 错误

* 修复 ios/android 读取文件路径问题

* 修复 Cllame 设置名字错误

## v1.3.0 - 2024.9.23

### 重大新功能

* 整合了 llama.cpp，支持本地离线执行大模型

## v1.2.0 - 2024.08.20

### 新功能

* 支持 OpenAI Image Edit/Image Variation

* 支持 Ollama API，支持自动获取 Ollama 支持的模型列表

## v1.1.0 - 2024.08.07

### 新功能

* 支持蓝图

## v1.0.0 - 2024.08.05

### 新功能

* 基础完整功能

* 支持 OpenAI， Azure，Claude，Gemini

* 自带功能完善编辑器聊天工具

--8<-- "footer.md"
