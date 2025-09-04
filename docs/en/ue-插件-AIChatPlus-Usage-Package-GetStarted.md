---
layout: post
title: Packaging
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
- Editor
- Editor Plus
- Editor Plugin
- AI Chat
- Chatbot
- Image Generation
- OpenAI
- Azure
- Claude
- Gemini
- Ollama
description: Packaging
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - Package 篇 - Get Started" />

#Packaging

##Plugin packaging

During the packaging process of Unreal, the necessary dynamic library files for the plugins will be automatically packaged, only requiring the activation of the plugin.

For instance, with Windows, packaging automatically places llama.cpp and the CUDA-related DLL files into the packaged directory. The same applies to other platforms such as Android, Mac, and iOS.

You can execute the command "AIChatPlus.PrintCllamaInfo" in the packaged Development version of the game to check the current Cllama environment status, confirm if the status is normal, and if it supports GPU backend.

##Model Packaging

Assuming that the model files for the project are located in the directory Content/LLAMA, you can include this directory when setting up the packaging process.

Open "Project Setting", select the Packaging tab, or simply search for "asset package". Locate the setting "Additional Non-Asset Directories to Package", and add the directory Content/LLAMA.

![](assets/img/2024-ue-aichatplus/usage/package/getstarted_1.png)

After adding a directory, Unreal will automatically package all files in the directory during the packaging process.

##Read the packaged offline model file.

Usually, Uneal will package project files into .Pak files. At this point, if you pass the file path in the .Pak to the Cllam offline model, it will fail to execute because llama.cpp cannot directly read the model files packaged in the .Pak.

Therefore, it is necessary to first copy the model files in the .Pak to the file system. The plugin provides a convenient function that can directly copy the model files from the .Pak and return the copied file path, allowing Cllama to read them easily.

Blueprint node "Cllama Prepare ModelFile In Pak" automatically copies model files from the Pak to the file system.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

The C++ code function is:

```
#include <Cllama/AIChatPlusCllama_Util.h>

auto ModelPath = FAIChatPlusCllama_Util::PrepareModelFileInPak(InContentPath);
```

--8<-- "footer_en.md"


> This post was translated using ChatGPT, please provide feedback in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
