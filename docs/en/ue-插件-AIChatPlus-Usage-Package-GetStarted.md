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

During Unreal packaging, the necessary dynamic library files for the plugins are automatically packaged, so you just need to enable the plugin.

For example, when it comes to Windows, packaging will automatically place the llama.cpp, CUDA-related DLL files into the packaged directory. The same applies to other platforms like Android, Mac, and IOS.

In the packaged Development version of the game, you can execute the command "AIChatPlus.PrintCllamaInfo" to check the current Cllama environment status, confirm if the state is normal, and verify GPU backend support.

##Model packaging

The model files for the project are placed in the directory Content/LLAMA. You can then include this directory when setting up the packaging process.

Open "Project Settings", select the Packaging tab, or simply search for "asset package". Once you see the setting "Additional Non-Asset Directories to Package", add the directory Content/LLAMA.

![](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_6.png)

After adding a content directory, Unreal will automatically package all the files in the directory when packaging.


##Read the packaged offline model file.

Normally, Uneal packages project files into .Pak files. If the file path from the .Pak is passed to the Cllam offline model, it will fail to execute. This is because llama.cpp cannot directly read the packaged model file from the .Pak.

Therefore, it is necessary to first copy the model files from the .Pak to the file system. The plugin provides a convenient function that can directly copy the model files from the .Pak and return the path of the copied files, enabling Cllama to read them easily.

The blueprint node is "Cllama Prepare ModelFile In Pak": it automatically copies model files from the Pak to the file system.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

The C++ code function is:

```
#include <Cllama/AIChatPlusCllama_Util.h>

auto ModelPath = FAIChatPlusCllama_Util::PrepareModelFileInPak(InContentPath);
```

--8<-- "footer_en.md"


> This post was translated using ChatGPT. Please provide feedback [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
