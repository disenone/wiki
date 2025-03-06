---
layout: post
title: Get Started
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
description: Get Started
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 编辑器篇 - Get Started" />

#編輯器篇 - 開始吧

##編輯器聊天工具

菜單欄 工具 -> AIChatPlus -> AIChat 可以使用這個插件提供的編輯器聊天工具。

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


工具支援文件生成、文字聊天、圖像生成，以及圖像分析。

工具的界面大致為：

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

##主要功能

* **離線大模型**：整合了 llama.cpp 庫，支持本地離線執行大型模型

* **文本聊天**：點擊左下角的 `New Chat` 按鈕，創建新的文本聊天會話。

圖像生成：點擊左下角的 `New Image Chat` 按鈕，創建新的圖像生成會話。

**圖像分析**：`New Chat` 的部分聊天服務支援發送圖像，例如 Claude、Google Gemini。點擊輸入框上方的 🖼️ 或 🎨 按鈕即可載入需要發送的圖像。

音頻處理：工具提供讀取音頻文件 (.wav) 和 錄音功能，可以使用獲得的音頻跟 AI 聊天。

* **設置當前聊天角色**：聊天框上方的下拉選單可設置當前發送文字的角色，可以透過模擬不同的角色來調整 AI 聊天。

**清空對話：** 在聊天框上方的 ❌ 按鈕能夠清除當前對話的歷史訊息。

**對話模板**：內建數百種對話設置模板，便於處理常見問題。

* **全局设置**：點擊左下角的 `Setting` 按鈕，可以打開全局設置視窗。可以設置預設文本聊天、圖像生成的 API 服務，以及設置每種 API 服務的具體參數。設置將自動保存在專案路徑 `$(ProjectFolder)/Saved/AIChatPlusEditor` 下。

**會話設置**：點擊聊天框上方的設置按鈕，可以打開當前會話的設置視窗。支援修改會話名稱，修改會話使用的 API 服務，支援獨立設置每個會話使用 API 的具體參數。會話設置自動保存在 `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

* **聊天内容修改**：當滑鼠懸停於聊天內容上時，將會出現個別聊天內容的設定按鈕，支援重新生成功能、修改內容、複製內容、刪除內容、以及在下方重新生成內容（針對角色是使用者的內容）。

* **圖像瀏覽**：對於圖像生成，點擊圖像會開啟圖像檢視視窗（ImageViewer），支援將圖片另存為 PNG/UE 紋理，紋理可直接在內容瀏覽器（Content Browser）中查看，方便圖片於編輯器內使用。此外還支援刪除圖片、重新生成圖片、繼續生成更多圖片等功能。對於 Windows 下的編輯器，還支援複製圖片，可以直接將圖片複製到剪貼板，方便使用。會話生成的圖片也會自動保存在每個會話檔案夾下，通常路徑是 `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`。

全局设置：

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

對話設置：

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

修改聊天內容：

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

影像檢視器：

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

使用離線大型模型

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

對話範本

![system template](assets/img/2024-ue-aichatplus/system_template.png)

##編輯器工具使用離線模型 Cllama(llama.cpp)

以下是如何在 AIChatPlus 編輯器工具中使用離線模型 llama.cpp。

首先，從 HuggingFace 網站下載離線模型：[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

將模型放在特定的資料夾裡，例如放在遊戲專案的 Content/LLAMA 資料夾中。

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

打開 AIChatPlus 編輯器工具：工具 -> AIChatPlus -> AIChat，新建聊天會話，並打開會話設置頁面

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

將 Api 設定為 Cllama，開啟自訂 Api 設定，加入模型搜尋路徑，並選擇模型。


![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

開始聊天！

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

##使用離線模型 Cllama(llama.cpp) 來處理圖片的編輯器工具。

從HuggingFace網站下載離線模型MobileVLM_V2-1.7B-GGUF，同樣將其放在Content/LLAMA目錄下：[ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)Translate these text into Traditional Chinese language:

。

* 設置會談的模型：

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)


* 發送圖片開始聊天

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

##編輯器使用 OpenAI 聊天

打開聊天工具 Tools -> AIChatPlus -> AIChat，創建新的聊天會話 New Chat，設置會話 ChatApi 為 OpenAI，設定接口參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

開始聊天：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

將模型切換為 gpt-4o / gpt-4o-mini，即可使用 OpenAI 的視覺功能分析圖片。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

##編輯器使用 OpenAI 處理圖片（創建/修改/變種）

在聊天工具中建立新的圖片聊天，將會話名稱修改為OpenAI，並設置參數。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

製作圖片

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

* 修改圖片，將對話圖像類型改為「編輯」，然後上傳兩張圖片，一張是原始圖片，另一張是透明位置的遮罩（Alpha 通道為 0），表示需要修改的部分。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

將圖片變種，將對話圖片類型修改為變異，並上傳一張圖片，OpenAI 將返回原圖片的一個變種。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

##編輯器使用 Azure

新建對話（New Chat），將ChatApi更改為Azure，並設置Azure的API參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

##使用 Azure 創建圖片的編輯器

新建圖片會話（New Image Chat），將ChatApi改為Azure，並設置Azure的Api參數，注意，如果是dall-e-2模型，需要將參數Quality和Stype設置為not_use。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

開始聊天，讓 Azure 創建圖片

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

##編輯器使用 Claude 聊天和分析圖片

建立新的對話（New Chat），將 ChatAPI 更改為 Claude，並設定 Claude 的 API 參數。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

##編輯器使用 Ollama 聊天和分析圖片

新建會話（New Chat），將 ChatApi 改為 Ollama，並設置 Ollama 的 API 參數。如果是文本聊天，則設置模型為文本模型，如 llama3.1；如果需要處理圖片，則設置模型為支持 vision 的模型，例如 moondream。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

* Start chatting

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)


###編輯器使用 Gemini

* 建立新對話（New Chat），將 ChatApi 改為 Gemini，並設置 Gemini 的 Api 參數。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

##編輯器使用 Gemini 發送音頻

從文件讀取音訊 / 從資產讀取音訊 / 從麥克風錄取音訊，生成需發送的音訊。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

##編輯器使用 Deepseek

創建新對話（New Chat），將 ChatApi 改為 OpenAi，並設置Deepseek的API參數。新增候選模型名為 deepseek-chat，並將模型設置為 deepseek-chat。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

--8<-- "footer_tc.md"


> 這篇文章是使用 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
