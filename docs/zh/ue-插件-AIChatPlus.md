---
layout: post
title: UE 插件 AIChatPlus 说明文档
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini, Ollama]
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

UE.AIChatPlus 是一个 UnrealEngine 插件，该插件实现了与各种 GPT AI 聊天服务进行通信，目前支持的服务有 OpenAI (ChatGPT, DALL-E)，Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, llama.cpp 本地离线。未来还会继续支持更多服务提供商。它的实现基于异步 REST 请求，性能高效，方便 UE 开发人员接入这些 AI 聊天服务。

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

* 离线大模型：整合了 llama.cpp 库，支持本地离线执行大模型

* 文本聊天：点击左下角的 `New Chat` 按钮，创建新的文本聊天会话。

* 图像生成：点击左下角的 `New Image Chat` 按钮，创建新的图像生成会话。

* 图像分析：`New Chat` 的部分聊天服务支持发送图像，例如 Claude, Google Gemini。点击输入框上方的 🖼️ 或 🎨 按钮即可加载需要发送的图像。

* 支持蓝图 (Blueprint)：支持蓝图创建 API 请求，完成文本聊天，图像生成等功能。

* 设置当前聊天角色：聊天框上方的下拉框可以设置当前发送文本的角色，可以通过模拟不同的角色来调节 AI 聊天。

* 清空会话：聊天框上方的 ❌ 按可以清空当前会话的历史消息。

* 对话模版：内置几百种对话设置模版，方便处理常用的问题。

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

使用离线大模型

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

对话模版

![system template](assets/img/2024-ue-aichatplus/system_template.png)

### 核心代码介绍

目前插件分成以下几个模块：

* AIChatPlusCommon: 运行时模块 (Runtime)，负责处理各种 AI API 接口发送请求和解析回复内容。

* AIChatPlusEditor: 编辑器模块 (Editor)， 负责实现编辑器 AI 聊天工具。

* AIChatPlusCllama: 运行时模块 (Runtime)，负责封装 llama.cpp 的接口和参数，实现离线执行大模型

* Thirdparty/LLAMACpp: 运行时第三方模块 (Runtime)，整合了 llama.cpp 的动态库和头文件。

具体负责发送请求的 UClass 是 FAIChatPlus_xxxChatRequest，每种 API 服务都分别有独立的 Request UClass。请求的回复通过 UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase 两种 UClass 来获取，只需要注册相应的回调委托。

发送请求之前需要先设置好 API 的参数和发送的消息，这块是通过 FAIChatPlus_xxxChatRequestBody 来设置。回复的具体内容也解析到 FAIChatPlus_xxxChatResponseBody 中，收到回调的时候可以通过特定接口获取 ResponseBody。

更多源码细节可在 UE 商城获取：[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## 使用指南

### 编辑器工具使用离线模型 llama.cpp

以下说明如何在 AIChatPlus 编辑器工具中使用离线模型 llama.cpp

* 首先，从 HuggingFace 网站下载离线模型：[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

* 把模型放在某个文件夹下面，譬如放在游戏项目的目录 Content/LLAMA 下

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

* 打开 AIChatPlus 编辑器工具：Tools -> AIChatPlus -> AIChat，新建聊天会话，并打开会话设置页面

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

* 设置 Api 为 Cllama，开启 Custom Api Settings， 并添加模型搜索路径，并选择模型

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

* 开始聊天！！

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

### 代码使用离线模型 llama.cpp

以下说明如何在代码中使用离线模型 llama.cpp

* 首先，同样需要下载模型文件到 Content/LLAMA 下

* 修改代码添加一条命令，并在命令里面给离线模型发送消息

```c++
#include "Common/AIChatPlus_Log.h"
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"

void AddTestCommand()
{
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("AIChatPlus.TestChat"),
		TEXT("Test Chat."),
		FConsoleCommandDelegate::CreateLambda([]()
		{
			if (!FModuleManager::GetModulePtr<FAIChatPlusCommon>(TEXT("AIChatPlusCommon"))) return;

			TWeakObjectPtr<UAIChatPlus_ChatHandlerBase> HandlerObject = UAIChatPlus_ChatHandlerBase::New();
			// Cllama
			FAIChatPlus_CllamaChatRequestOptions Options;
			Options.ModelPath.FilePath = FPaths::ProjectContentDir() / "LLAMA" / "qwen1.5-1_8b-chat-q8_0.gguf";
			Options.NumPredict = 400;
			Options.bStream = true;
			// Options.StopSequences.Emplace(TEXT("json"));
			auto RequestPtr = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(
				Options,
				{
					{"You are a chat bot", EAIChatPlus_ChatRole::System},
					{"who are you", EAIChatPlus_ChatRole::User}
				});

			HandlerObject->BindChatRequest(RequestPtr);
			const FName ApiName = TEnumTraits<EAIChatPlus_ChatApiProvider>::ToName(RequestPtr->GetApiProvider());

			HandlerObject->OnMessage.AddLambda([ApiName](const FString& Message)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] Message: [%s]"), *ApiName.ToString(), *Message);
			});
			HandlerObject->OnStarted.AddLambda([ApiName]()
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestStarted"), *ApiName.ToString());
			});
			HandlerObject->OnFailed.AddLambda([ApiName](const FAIChatPlus_ResponseErrorBase& InError)
			{
				UE_LOG(AIChatPlus_Internal, Error, TEXT("TestChat[%s] RequestFailed: %s "), *ApiName.ToString(), *InError.GetDescription());
			});
			HandlerObject->OnUpdated.AddLambda([ApiName](const FAIChatPlus_ResponseBodyBase& ResponseBody)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestUpdated"), *ApiName.ToString());
			});
			HandlerObject->OnFinished.AddLambda([ApiName](const FAIChatPlus_ResponseBodyBase& ResponseBody)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestFinished"), *ApiName.ToString());
			});

			RequestPtr->SendRequest();
		}),
		ECVF_Default
	);
}
```

* 重新编译后，在编辑器 Cmd 中使用命令，便可在日志 OutputLog 看到大模型的输出结果

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

### 蓝图使用离线模型 llama.cpp

以下说明如何在蓝图中使用离线模型 llama.cpp

* 在蓝图中右键创建一个节点 `Send Cllama Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

* 创建 Options 节点，并设置 `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

* 创建 Messages，分别添加一条 System Message 和 User Message

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* 创建 Delegate 接受模型输出的信息，并打印在屏幕上

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* 完整的蓝图看起来是这样的，运行蓝图，即可看到游戏屏幕在打印大模型返回的消息

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

### 蓝图使用 OpenAI 模型

* 在蓝图中右键创建一个节点 `Send OpenAI Chat Request In World`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

* 创建 Options 节点，并设置 `Stream=true, Api Key="you api key from OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

* 创建 Messages，分别添加一条 System Message 和 User Message

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* 创建 Delegate 接受模型输出的信息，并打印在屏幕上

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* 完整的蓝图看起来是这样的，运行蓝图，即可看到游戏屏幕在打印大模型返回的消息

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

### 蓝图使用 Claude 分析图片

* 在蓝图中右键创建一个节点 `Send Claude Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

* 创建 Options 节点，并设置 `Stream=true, Api Key="you api key from Clude", Max Output Tokens=1024`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

* 创建 Messages，从文件创建 Texture2D，并从 Texture2D 创建 AIChatPlusTexture，把 AIChatPlusTexture 添加到 Message 中

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

* 跟上述教程一样，创建 Event 并把信息打印到游戏屏幕上

* 完整的蓝图看起来是这样的，运行蓝图，即可看到游戏屏幕在打印大模型返回的消息

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

### 蓝图使用 OpenAI 创建图片

* 在蓝图中右键创建一个节点 `Send OpenAI Image Request`，并设置 `In Prompt="a beautiful butterfly"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

* 创建 Options 节点，并设置 `Api Key="you api key from OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

* 绑定 On Images 事件，并把图片保存到本地硬盘上

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

* 完整的蓝图看起来是这样的，运行蓝图，即可看到图片保存在指定的位置上

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## 更新日志

### v1.3.3 - 2024.11.25

#### 新功能

* 支持 UE-5.5

#### 问题修复

* 修复部分蓝图不生效问题

### v1.3.2 - 2024.10.10

#### 新功能

* 修复 手动停止 request 的时候 cllama 崩溃

* 修复商城下载版本 win 打包找不到 ggml.dll llama.dll 文件的问题

* 创建请求时检查是否在 GameThread 中，CreateRequest check in game thread

### v1.3.1 - 2024.9.30

#### 新功能

* 增加一个 SystemTemplateViewer，可以查看和使用几百个 system 设置模版

#### 问题修复

* 修复从商城下载的插件，llama.cpp 找不到链接库

* 修复 LLAMACpp 路径过长问题

* 修复 windows 打包后的链接 llama.dll 错误

* 修复 ios/android 读取文件路径问题

* 修复 Cllame 设置名字错误

### v1.3.0 - 2024.9.23

#### 重大新功能

* 整合了 llama.cpp，支持本地离线执行大模型

### v1.2.0 - 2024.08.20

#### 新功能

* 支持 OpenAI Image Edit/Image Variation

* 支持 Ollama API，支持自动获取 Ollama 支持的模型列表

### v1.1.0 - 2024.08.07

#### 新功能

* 支持蓝图

### v1.0.0 - 2024.08.05

#### 新功能

* 基础完整功能

* 支持 OpenAI， Azure，Claude，Gemini

* 自带功能完善编辑器聊天工具

--8<-- "footer.md"
