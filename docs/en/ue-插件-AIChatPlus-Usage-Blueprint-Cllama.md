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

Cllama is implemented based on llama.cpp and supports offline AI inference model usage.

Since it is offline, we need to first prepare the model files, such as downloading the offline model from the HuggingFace website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Place the model in a specific folder, for example, in the game project directory Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA > ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Once we have the offline model file, we can then use Cllama for AI chatting.

##Text chat

Use Cllama for text chatting.

In the blueprint, right-click to create a node `Send Cllama Chat Request`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Create an 'Options' node and set `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Create Messages, add a System Message and a User Message respectively.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Create a Delegate to receive the model's output information and print it on the screen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, running the blueprint will display the message returned on the game screen when printing the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##生成文字图片 llava

Cllama also experimentally supports the llava library, providing the capability of Vision.

First, prepare the Multimodal offline model file, such as Moondream ([moondream2-text-model-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-text-model-f16.gguf), [moondream2-mmproj-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-mmproj-f16.gguf)）或者 Qwen2-VL（[Qwen2-VL-7B-Instruct-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/Qwen2-VL-7B-Instruct-Q8_0.gguf), [mmproj-Qwen2-VL-7B-Instruct-f16.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-7B-Instruct-f16.gguf)Or other multimodal models supported by llama.cpp.

Create the Options node and set the parameters "Model Path" and "MMProject Model Path" to the corresponding Multimodal model files.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_1.png)

Create a node to read the image file flower.png and configure the messages.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_3.png)

Finally, create a node to receive the returned information and print it on the screen. The complete blueprint looks like this:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_4.png)

Running the blueprint will display the returned text.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_5.png)

##llama.cpp uses GPU

"Add parameter 'Num Gpu Layer' to 'Cllama Chat Request Options', which can set the gpu payload of llama.cpp and control the number of layers to be computed on the GPU. See the image below."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

##Handle model files in the .Pak after packaging.

After enabling "Pak" packaging, all project resources will be placed in a .Pak file, which naturally includes offline model gguf files.

Due to the incapacity of llama.cpp to directly read .Pak files, it is necessary to extract the offline model files from the .Pak file and copy them into the file system.

AIChatPlus provides a feature that can automatically copy and process model files from .Pak and place them in the Saved folder.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

Alternatively, you can handle the model files in the .Pak yourself. The key is to make sure to copy the files out because llama.cpp is unable to read .Pak files correctly.

##Function node

Cllama provides some functional nodes to easily access the status under the current environment.


Check if "Cllama Is Valid"：judges if Cllama llama.cpp is initialized correctly.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

Check if llama.cpp supports GPU backend in the current environment.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

Retrieve all the backends supported by the current llama.cpp.


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

Automatically copies the model files from Pak to the file system.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)


--8<-- "footer_en.md"


> This post was translated using ChatGPT, please provide feedback in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
