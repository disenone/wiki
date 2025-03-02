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

## Cllama(llama.cpp)

### 编辑器工具使用离线模型 Cllama(llama.cpp)

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

### 编辑器工具使用离线模型 Cllama(llama.cpp) 处理图片

* 从 HuggingFace 网站下载离线模型 MobileVLM_V2-1.7B-GGUF 同样放到目录 Content/LLAMA 下：[ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf) 和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)。

* 设置会话的模型：

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

* 发送图片开始聊天

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

### 代码使用离线模型 Cllama(llama.cpp)

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

### llama.cpp 使用 GPU

"Cllama Chat Request Options" 增加参数 "Num Gpu Layer" ，可以设置 llama.cpp 的 gpu payload，如图

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

可以使用蓝图节点判断当前环境下是否支持 GPU 并获取当前环境支持的 backends：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_2.png)

### 处理打包后 .Pak 中的模型文件

开启 Pak 打包后，项目的所有资源文件都会放在 .Pak 文件中，当然也包含了离线模型 gguf 文件。

由于 llama.cpp 无法支持直接读取 .Pak 文件，因此需要把 .Pak 文件中的离线模型文件拷贝出来文件系统中。

AIChatPlus 提供了一个功能函数可以自动把 .Pak 中的模型文件拷贝处理，并放在 Saved 文件夹中：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

又或者你可以自己处理 .Pak 中的模型文件，关键就是需要把文件复制处理，llama.cpp 无法正确读取 .Pak。

## OpenAI

### 编辑器使用 OpenAI 聊天

* 打开聊天工具 Tools -> AIChatPlus -> AIChat，创建新的聊天会话 New Chat，设置会话 ChatApi 为 OpenAI, 设置接口参数

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

* 开始聊天：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

* 切换模型为 gpt-4o / gpt-4o-mini，可以使用 OpenAI 的视觉功能分析图片

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

### 编辑器使用 OpenAI 处理图片（创建/修改/变种）

* 在聊天工具中创建新的图片会话 New Image Chat，修改会话设置为 OpenAI，并设置参数

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

* 创建图片

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

* 修改图片，把会话 Image Chat Type 修改为 Edit，并上传两张图片，一张是原图片，一张是 mask 其中透明的位置（alpha 通道为 0）表示需要修改的地方

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

* 图片变种，把会话 Image Chat Type 修改为 Variation，并上传一张图片，OpenAI 会返回一张原图片的变种

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

### 蓝图使用 OpenAI 模型聊天

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

## Azure

### 编辑器使用 Azure

* 新建会话（New Chat），把 ChatApi 改为 Azure，并设置 Azure 的 Api 参数

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

* 开始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

### 编辑器使用 Azure 创建图片

* 新建图片会话（New Image Chat），把 ChatApi 改为Azure，并设置 Azure 的 Api 参数，注意，如果是 dall-e-2 模型，需要把参数 Quality 和 Stype 设置成 not_use

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

* 开始聊天，让 Azure 创建图片

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

### 蓝图使用 Azure 聊天

创建如下蓝图，设置好 Azure Options，点击运行，即可看到屏幕上打印 Azure 返回的聊天信息

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

### 蓝图使用 Azure 创建图片

创建如下蓝图，设置好 Azure Options，点击运行，如果创建图片成功，会在屏幕上看到信息 "Create Image Done"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

根据上面蓝图的设置，图片会保存在路径 D:\Dwnloads\butterfly.png

## Claude

### 编辑器使用 Claude 聊天和分析图片

* 新建会话（New Chat），把 ChatApi 改为 Claude，并设置 Claude 的 Api 参数

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

* 开始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

### 蓝图使用 Claude 聊天和分析图片

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

## Ollama

### 获取 Ollama

* 可以通过 Ollama 官网获取安装包本地安装：[ollama.com](https://ollama.com/)

* 可以通过其他人提供的 Ollama 接口使用 Ollama。

### 编辑器使用 Ollama 聊天和分析图片

* 新建会话（New Chat），把 ChatApi 改为 Ollama，并设置 Ollama 的 Api 参数。如果是文本聊天，则设置模型为文本模型，如 llama3.1；如果需要处理图片，则设置模型为支持 vision 的模型，例如 moondream。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

* 开始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

### 蓝图使用 Ollama 聊天和分析图片

创建如下蓝图，设置好 Ollama Options，点击运行，即可看到屏幕上打印 Ollama 返回的聊天信息

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

### 编辑器使用 Gemini

* 新建会话（New Chat），把 ChatApi 改为 Gemini，并设置 Gemini 的 Api 参数。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

* 开始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

### 编辑器使用 Gemini 发送音频

* 选择 从文件读取音频 / 从 Asset 读取音频 / 从麦克风录取音频，生成需要发送的音频

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

* 开始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

### 蓝图使用 Gemini 聊天

创建如下蓝图，设置好 Gemini Options，点击运行，即可看到屏幕上打印 Gemini 返回的聊天信息

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

### 蓝图使用 Gemini 发送音频

创建如下蓝图，设置加载音频，设置好 Gemini Options，点击运行，即可看到屏幕上打印 Gemini 处理音频后返回的聊天信息

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

### 編輯器使用 Deepseek

* 新建会话（New Chat），把 ChatApi 改为 OpenAi，并设置 Deepseek 的 Api 参数。新增 Candidate Models 叫做 deepseek-chat，并把 Model 设置为 deepseek-chat

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

* 开始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

### 蓝图使用 Deepseek 聊天

创建如下蓝图，设置好 Deepseek 相关的 Request Options，包括 Model、Base Url、End Point Url、ApiKey 等参数。点击运行，即可看到屏幕上打印 Gemini 返回的聊天信息

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

## 额外提供的蓝图功能节点

### Cllama 相关

"Cllama Is Valid"：判断 Cllama llama.cpp 是否正常初始化

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu"：判断 llama.cpp 在当前环境下是否支持 GPU backend

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Cllama Get Support Backends": 获取当前 llama.cpp 支持的所有 backends

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama Prepare ModelFile In Pak": 自动把 Pak 中的模型文件复制到文件系统中

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

### 图像相关

"Convert UTexture2D to Base64": 把 UTexture2D 的图像转成 png base64 格式

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

"Save UTexture2D to .png file": 把 UTexture2D 保存成 png 文件

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

"Load .png file to UTexture2D": 读取 png 文件为 UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Duplicate UTexture2D": 复制 UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

### 音频相关

"Load .wav file to USoundWave": 读取 wav 文件为 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

"Convert .wav data to USoundWave": 把 wav 二进制数据转成 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

"Save USoundWave to .wav file": 把 USoundWave 保存为 .wav 文件

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

"Get USoundWave Raw PCM Data": 把 USoundWave 转成二进制音频数据

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"Convert USoundWave to Base64": 把 USoundWave 转成 Base64 数据

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicate USoundWave": 复制 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

"Convert Audio Capture Data to USoundWave": 把 Audio Capture 录音数据转成 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

## 更新日志

### v1.6.0 - 2025.03.02

#### 新功能

* llama.cpp 升级至 b4604 版本

* Cllama 支持 GPU backends: cuda 和 metal

* chat tool Cllama 支持使用 GPU

* 支持读取打包 Pak 中的模型文件

#### Bug Fix

* 修复 Cllama 在推理的时候 reload 会崩溃的问题

* 修复 ios 编译报错

### v1.5.1 - 2025.01.30

#### 新功能

* 只允许 Gemini 发音频

* 优化获取 PCMData 的方法，生成 B64 的时候再解压缩音频数据

* request 增加两个回调 OnMessageFinished OnImagesFinished

* 优化 Gemini Method，自动根据 bStream 获取 Method

* 增加一些蓝图函数，方便转换 Wrapper 到实际类型，并且获取 Response Message 和 Error

#### Bug Fix

* 修复 Request Finish 多次调用问题

### v1.5.0 - 2025.01.29

#### 新功能

* 支持给 Gemini 发音频

* 编辑器工具支持发送音频和录音

#### Bug Fix

* 修复 Session copy 失败的 bug

### v1.4.1 - 2025.01.04

#### 问题修复

* 聊天工具支持只发图片不发信息

* 修复 OpenAI 接口发送图片问题失败文图

* 修复 OpanAI、Azure 聊天工具设置遗漏了参数 Quality、Style、ApiVersion 问题=

### v1.4.0 - 2024.12.30

#### 新功能

* （实验性功能）Cllama(llama.cpp) 支持多模态模型，可以处理图片

* 所有的蓝图类型参数都加上了详细提示

### v1.3.4 - 2024.12.05

#### 新功能

* OpenAI 支持 vision api

#### 问题修复

* 修复 OpenAI stream=false 时的错误

### v1.3.3 - 2024.11.25

#### 新功能

* 支持 UE-5.5

#### 问题修复

* 修复部分蓝图不生效问题

### v1.3.2 - 2024.10.10

#### 问题修复

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
