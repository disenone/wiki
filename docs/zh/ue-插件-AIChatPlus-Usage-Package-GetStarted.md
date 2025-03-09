---
layout: post
title: 打包
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini, Ollama]
description: 打包
---
<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - Package 篇 - Get Started" />

# 打包

## 插件打包

Unreal 打包的时候，会自动把插件需要的动态库文件都打包好，只需要启用插件即可。

譬如对于 Windows，打包会自动把 llama.cpp, CUDA 相关的 dll 文件都放到打包后的目录中。对于其他平台 Android / Mac / IOS 也是同样的。

可以在打包后的 Development 版本游戏里面执行指令 "AIChatPlus.PrintCllamaInfo"，查看当前的 Cllama 环境状态，确认是否状态是否正常，是否支持 GPU backend。

## 模型打包

加入项目的模型文件放在了目录 Content/LLAMA 下面，那么可以设置打包的时候包含此目录：

打开 "Project Setting"，选择 Packaging 页签，或者直接搜索 "asset package"，看到设置 "Additional Non-Asset Directories to Package"，添加目录 Content/LLAMA 即可：

![](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_6.png)

添加目录之后，Unreal 在打包的时候就会自动把目录的所有文件都打包好。


## 读取打包后的离线模型文件

一般 Uneal 会把项目文件都打包到 .Pak 文件中，此时如果把 .Pak 中的文件路径传递给 Cllam 离线模型，是会执行失败的，因为 llama.cpp 无法直接读取 .Pak 中打包后的模型文件。

因此需要先把 .Pak 中的模型文件复制出来文件系统中，插件提供了一个方便的函数可以直接把 .Pak 的模型文件复制出来，并返回复制后的文件路径，让 Cllama 可以方便读取。

蓝图节点是 "Cllama Prepare ModelFile In Pak": 自动把 Pak 中的模型文件复制到文件系统中

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

C++ 代码函数是：

```
#include <Cllama/AIChatPlusCllama_Util.h>

auto ModelPath = FAIChatPlusCllama_Util::PrepareModelFileInPak(InContentPath);
```

--8<-- "footer.md"
