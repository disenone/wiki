---
layout: post
title: Cllama (llama.cpp)(Deprecated)
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
- llama.cpp
description: Cllama (llama.cpp)
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Cllama (llama.cpp)" />

#Blueprints Chapter - Cllama (llama.cpp) (Deprecated)

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_all.png)

##Obsolete

Cllama has been marked as **deprecated** and is no longer maintained.

The original functionalities of Cllama are provided by [CllamaServer](ue-插件-AIChatPlus-Usage-Blueprint-CllamaServer.md)To carry.

##Offline Model

Cllama is built upon llama.cpp and supports offline usage of AI inference models.

Since it's offline, we need to prepare the model files beforehand, such as downloading the offline model from the HuggingFace website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Place the model under a certain folder, for example, within your game project directory at Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA > ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

With the offline model files in place, we can now engage in AI chat using Cllama.

##Text Chat

Text Chat Using Cllama

Right-click in the blueprint to create a node `Send Cllama Chat Request`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Create an Options node and set `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Create Messages, add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Create a Delegate to receive the model's output and print it on the screen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this: Run the blueprint, and you'll see the game screen printing messages returned by the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##Image captioning llava

Cllama also experimentally supports the llava library, offering Vision capabilities.

First, prepare the Multimodal offline model files, such as Moondream ([moondream2-text-model-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-text-model-f16.gguf), [moondream2-mmproj-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-mmproj-f16.gguf)or Qwen2-VL ([Qwen2-VL-7B-Instruct-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/Qwen2-VL-7B-Instruct-Q8_0.gguf), [mmproj-Qwen2-VL-7B-Instruct-f16.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-7B-Instruct-f16.gguf)or other Multimodal models supported by llama.cpp.

Create an Options node and set the parameters "Model Path" and "MMProject Model Path" to the corresponding Multimodal model files respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_1.png)

Create a node to read the image file flower.png and configure Messages.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_3.png)

Finally, the node that accepts the returned information is created and printed to the screen. The complete blueprint will look like this:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_4.png)

Run the blueprint to see the returned text

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_5.png)

##llama.cpp with GPU support

"ClLama Chat Request Options" Added parameter "Num Gpu Layer," allows setting llama.cpp's GPU payload to control the number of layers computed on the GPU. As shown in the figure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

## KeepAlive

"Cllama Chat Request Options" adds a parameter "KeepAlive" that allows the loaded model file to remain in memory after use, enabling direct utilization for subsequent requests and reducing the frequency of model loads. KeepAlive specifies the duration for which the model is retained; 0 means it is not retained and gets released immediately after use, while -1 indicates permanent retention. Each request's Options can assign a different KeepAlive value, with new settings overriding previous ones. For example, initial requests might set KeepAlive=-1 to keep the model in memory, then the final request could set KeepAlive=0 to release the model file.

##Handling model files within the packed .Pak

After enabling Pak packaging, all the project's resource files will be placed in the .Pak file, including the offline model gguf files as well.

Since llama.cpp cannot directly read .Pak files, it is necessary to extract the offline model files from the .Pak files and place them into the file system.

AIChatPlus provides a utility function that automatically copies and processes model files from .Pak archives, placing them in the Saved folder:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

Alternatively, you can handle the model files within the .Pak yourself. The key is to extract the files, as llama.cpp cannot properly read the .Pak format.

##Functional Nodes

Cllama provides several functional nodes for easily retrieving the current environment status.


"Cllama Is Valid": Determine if Cllama llama.cpp is properly initialized

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu": Determines whether llama.cpp supports GPU backend in the current environment

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Cllama Get Support Backends": Retrieves all currently supported backends by llama.cpp


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama Prepare ModelFile In Pak": Automatically copies model files from Pak to the file system.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)


--8<-- "footer_en.md"


> This post is translated using ChatGPT. Please provide feedback [**here**](https://github.com/disenone/wiki_blog/issues/new)Pointing out any omissions therein. 
