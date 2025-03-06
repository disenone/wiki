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

#藍圖章節 - Cllama (llama.cpp)

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_all.png)

##離線模型

Cllama 是基於 llama.cpp 實現的，支援離線使用 AI 推論模型。

由於屬於離線情況，我們需要先準備好模型檔案，例如從 HuggingFace 網站下載離線模型：[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

將模型放在指定的檔案夾內，例如將其存放在遊戲專案目錄 Content/LLAMA 中。

```shell
E:/UE/projects/FP_Test1/Content/LLAMA > ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

有了離線模型文件之後，我們就可以透過 Cllama 來進行 AI 聊天。

##文字聊天

使用 Cllama 進行文字聊天

請在藍圖中按右鍵創建一個節點 `Send Cllama Chat Request`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

建立 Options 節點，並設定 `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

建立訊息，分別新增一條系統訊息和用戶訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

建立 Delegate 接收模型輸出的資訊，並顯示在螢幕上。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完整的藍圖看起來是這樣的，運行藍圖，即可看到遊戲屏幕在列印大型模型返回的訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##生成圖片文字 llava

Cllama 還實驗性支持了 llava 庫，提供了 Vision 的能力。

請準備好 Multimodal 離線模型檔案，例如 Moondream（[moondream2-text-model-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-text-model-f16.gguf), [moondream2-mmproj-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-mmproj-f16.gguf)）或者 Qwen2-VL（[Qwen2-VL-7B-Instruct-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/Qwen2-VL-7B-Instruct-Q8_0.gguf), [mmproj-Qwen2-VL-7B-Instruct-f16.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-7B-Instruct-f16.gguf)）或者其他 llama.cpp 支持的 Multimodal 模型。

建立「選項」節點，將「模型路徑」和「MMProject 模型路徑」參數分別設置為相對應的多模式模型檔案。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_1.png)

建立節點來讀取圖片檔案 flower.png，並設定訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_3.png)

最後建立節點接受返回的訊息，並列印到螢幕上，完整的藍圖看起來是這樣的。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_4.png)

運行藍圖可看到返回的文字

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_5.png)

##llama.cpp 使用 GPU

“Cllama Chat Request Options” 中新增一個參數 “Num Gpu Layer”，該參數可設置 llama.cpp 的 GPU 資料負載，進而控制需在 GPU 上計算的層數。示意如下圖。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

##處理打包後 .Pak 中的模型文件

啟動 Pak 打包後，專案中的所有資源檔案都會被放置在 .Pak 檔案中，當然也包括了離線模型 gguf 檔案。

因為 llama.cpp 無法直接讀取 .Pak 文件，所以需要將 .Pak 文件中的離線模型檔案複製到檔案系統中。

AIChatPlus 提供了一個功能函數，可以自動將 .Pak 中的模型檔案複製處理，並放在 Saved 資料夾中：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

您可以自行處理 .Pak 中的模型檔案，關鍵是要將檔案複製出來，因為 llama.cpp 無法正確讀取 .Pak。

##功能節點

Cllama 提供了一些功能節點，方便取得當前環境下的狀態。


"Cllama Is Valid"：檢查 Cllama llama.cpp 是否正確初始化

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu"：判斷 llama.cpp 在當前環境下是否支持 GPU backend

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"獲取支持的後端": 取得 llama.cpp 目前支援的所有後端。


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama Prepare ModelFile In Pak": 自動將 Pak 中的模型文件複製到檔案系統中

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)


--8<-- "footer_tc.md"


> 此貼文是由 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
