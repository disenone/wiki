---
layout: post
title: Cllama (llama.cpp)
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

#Blueprint Section - Cllama (llama.cpp)

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_all.png)

##Offline model

Cllama is implemented based on llama.cpp, supporting offline use of AI inference models.

As it is offline, we need to first prepare the model files, such as downloading the offline model from the HuggingFace website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Place the model in a specific folder, for example, in the directory Content/LLAMA of the game project.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA > ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Once we have the offline model files, we can use Cllama for AI chatting.

##Text chat

Use Cllama for text chatting

Create a node called `Send Cllama Chat Request` by right-clicking on the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Create an Options node and set `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Create Messages, then add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Create a delegate to receive the model's output information and print it on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, run the blueprint to see the message returned on the game screen when printing the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##Generate text from images	llava

Cllama also experimentally supports the llava library, providing the capability of Vision.

First, prepare the Multimodal offline model file, such as Moondream ([moondream2-text-model-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-text-model-f16.gguf), [moondream2-mmproj-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-mmproj-f16.gguf)）or Qwen2-VL ([Qwen2-VL-7B-Instruct-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/Qwen2-VL-7B-Instruct-Q8_0.gguf), [mmproj-Qwen2-VL-7B-Instruct-f16.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-7B-Instruct-f16.gguf)Or any other Multimodal model supported by llama.cpp.

Create an Options node, and set the parameters "Model Path" and "MMProject Model Path" to the corresponding Multimodal model files.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_1.png)

Create a node to read the image file named flower.png and configure Messages.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_3.png)

Finally, create a node to receive the returned information and print it on the screen. The complete blueprint looks like this:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_4.png)

You can view the returned text by running the blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_5.png)

##llama.cpp uses GPU

Add a parameter "Num Gpu Layer" to the "Cllama Chat Request Options," which can configure the GPU payload in llama.cpp to control the number of layers that need to be computed on the GPU. See the illustration below.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

## KeepAlive

Add the parameter "KeepAlive" to the "Cllama Chat Request Options", which allows the loaded model file to be retained in memory for easy direct use, reducing the number of times the model is read. KeepAlive is the duration for which the model is kept in memory, where 0 means no retention and is released immediately after use, while -1 means permanent retention. Each request can set different KeepAlive values in the Options, with the new KeepAlive replacing the old value. For example, initial requests can set KeepAlive=-1 to keep the model in memory until the final request sets KeepAlive=0 to release the model file.

##Handle model files in the .Pak after being packaged.

After enabling Pak packaging, all project resources will be placed in a .Pak file, which also includes offline model GGUF files.

Due to the inability of llama.cpp to directly read .Pak files, it is necessary to copy the offline model files from the .Pak file to the file system.

AIChatPlus provides a functionality function that automatically copies and processes model files from .Pak, placing them in the Saved folder:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

Alternatively, you can handle the model files in .Pak yourself. The key is to copy the files out because llama.cpp cannot read .Pak correctly.

##Function Node

Cllama provides some functional nodes to easily access the current state in the environment.


"Verify if Cllama Is Valid": Determine if Cllama llama.cpp is properly initialized.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

Determine if llama.cpp supports GPU backend in the current environment.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

Retrieve all backend support that is currently supported by llama.cpp


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

“Cllama Prepare ModelFile In Pak”: Automatically copies model files from the Pak to the file system.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)


--8<-- "footer_en.md"


> This post was translated using ChatGPT, please provide feedback in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
