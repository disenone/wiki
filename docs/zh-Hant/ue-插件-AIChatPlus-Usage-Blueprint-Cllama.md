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

#藍圖篇 - Cllama (llama.cpp)

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_all.png)

##離線模型

Cllama 是基於 llama.cpp 來實現的，支持離線使用 AI 推理模型。

由於是離線，因為我們需要先準備好模型檔案，譬如從 HuggingFace 網站下載離線模型：[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

將模型放置在特定資料夾中，例如放在遊戲專案的 Content/LLAMA 目錄下。

```shell
E:/UE/projects/FP_Test1/Content/LLAMA > ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

有了離線模型文件之後，我們就可以透過Cllama進行AI聊天。

##文字聊天

使用 Cllama 進行文字聊天

在藍圖中右鍵建立一個節點 `發送 Cllama 聊天請求`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

建立 Options節點，並設置 `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

建立 Messages，分別新增一條 System Message 和 User Message

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

建立 Delegate 接收模型輸出的資訊，並顯示在螢幕上。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

請將這些文字翻譯成繁體中文:

完整的藍圖看起來像這樣，運行藍圖，即可看到遊戲畫面中打印大型模型返回的訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##圖片生成文字 llava

Cllama 還實驗性支持了 llava 庫，提供了 Vision 的能力。

(https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-text-model-f16.gguf), [moondream2-mmproj-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-mmproj-f16.gguf)）或者 Qwen2-VL（[Qwen2-VL-7B-Instruct-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/Qwen2-VL-7B-Instruct-Q8_0.gguf), [mmproj-Qwen2-VL-7B-Instruct-f16.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-7B-Instruct-f16.gguf)）或其他被 llama.cpp 支援的多模式模型。

建立 Options 節點，分別設定參數 "Model Path" 和 "MMProject Model Path" 為對應的 Multimodal 模型檔案。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_1.png)

創建節點以讀取圖片文件 flower.png，並設置訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_3.png)

最後建立節點接受返回的資訊，並列印到螢幕上，完整的藍圖看起來是這樣的。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_4.png)

運行藍圖可看到返回的文字

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_5.png)

##llama.cpp 使用 GPU

「Cllama 聊天请求选项」增加了參數「Num Gpu Layer」，可設置 llama.cpp 的 GPU 載荷，以控制需要在 GPU 上計算的層數。請參考圖表。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

## KeepAlive

「Cllama Chat Request Options」新增參數「KeepAlive」，能夠讓已讀取的模型文件保留在記憶體中，方便下次直接使用，減少讀取模型的次數。KeepAlive 是模型保留的時間，0 表示不保留，使用後立即釋放；-1 表示永久保留。每次請求設定的 Options 都可以設定不同的 KeepAlive，新的 KeepAlive 會取代舊的數值，例如前幾次的請求可以設定 KeepAlive=-1，讓模型保留在記憶體中，直到最後一次的請求設定 KeepAlive=0，釋放模型文件。

##處理已打包在.Pak中的模型檔案

當 Pak 打包完成後，所有專案資源檔案都將存放在 .Pak 檔案中，當然也包含離線模型 gguf 檔案。

由於 llama.cpp 無法直接讀取 .Pak 文件，因此需要將 .Pak 文件中的離線模型檔案複製到檔案系統中。

AIChatPlus 提供了一個功能函數，可以自動將 .Pak 中的模型文件復制處理，並放在 Saved 文件夾中：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

你亦可自行處理.Pak中的模型文件，關鍵是需要將檔案複製出來，因為llama.cpp無法正確讀取.Pak。

##功能節點

Cllama 提供了一些功能節點方便獲取當前環境下的狀態。


"Cllama Is Valid"：判斷 Cllama llama.cpp 是否正確初始化

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu"：判斷 llama.cpp 在當前環境下是否支持 GPU backend

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

獲取當前 llama.cpp 支援的所有後端。


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama 在 Pak 中准备模型文件": 將 Pak 中的模型文件自動複製到檔案系統中

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)


--8<-- "footer_tc.md"


> 此帖文係透過 ChatGPT 翻譯完成，如有[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
