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

#編輯器專題 - 開始入門

##編輯器聊天工具

按照菜单列選 Tools -> AIChatPlus -> AIChat 可以啟動插件提供的聊天編輯工具。

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


工具支援文字產生、文字對話、圖像生成，以及圖像分析。

工具的界面大致為：

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

##主要功能

**離線大型模型**：整合了 llama.cpp 庫，支持本地離線執行大型模型

**文字聊天**：點擊左下角的 `新對話` 按鈕，建立新的文字聊天對話。

**圖像生成**：點擊左下角的 `New Image Chat` 按鈕，創建新的圖像生成會話。

**圖像分析**：`New Chat` 的一些聊天服務支援發送圖像，如 Claude、Google Gemini。只需點擊輸入框上方的 🖼️ 或 🎨 按鈕，就可以載入要發送的圖像。

音頻處理：此工具可讀取音頻文件（.wav）和進行錄音，從而讓您可以與 AI 利用所獲得的音頻進行對話。

**設定當前聊天角色**：聊天視窗上方的下拉式選單可以設定當前發送文字的角色，可以透過模擬不同的角色來調整 AI 聊天。

**清空對話**：聊天視窗頂部的 ❌ 按鈕可以清空當前對話的歷史訊息。

**對話範本**：內建數百種設定好的對話範本，便於處理常見問題。

**全局設定**：點擊左下角的 `Setting` 按鈕，可以打開全局設定視窗。可以設定預設文本聊天，圖像生成的 API 服務，並設定每種 API 服務的具體參數。設定會自動保存在專案的路徑 `$(ProjectFolder)/Saved/AIChatPlusEditor` 下。

**對話設置**：點擊聊天框上方的設置按鈕，即可開啟當前對話的設置窗口。支援修改對話名稱，修改對話使用的 API 服務，並支援獨立設定每個對話使用 API 的具體參數。對話設置將自動保存在`$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`。

**聊天內容修改**：當滑鼠停留在聊天內容上時，會顯示個別聊天內容的設置按鈕，支援重新生成內容、修改內容、複製內容、刪除內容、在下方重新生成內容（針對角色為用戶的內容）。

**圖像瀏覽**：針對圖像生成，點擊圖像將開啟圖像查看窗口（ImageViewer），支援圖片另存為 PNG/UE 紋理，紋理可直接在內容瀏覽器（Content Browser）中檢視，方便圖片在編輯器內使用。另外還支援刪除圖片、重新生成圖片、繼續生成更多圖片等功能。針對 Windows 下的編輯器，還支援複製圖片，可直接將圖片複製到剪貼板，方便使用。會話生成的圖片也會自動保存在每個會話檔案夾下，通常路徑是 `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`。

全局設定：

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

對話框設置：

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

修改對話內容：

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

圖像檢視器：

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

使用離線大型模型

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

對話模板

![system template](assets/img/2024-ue-aichatplus/system_template.png)

##編輯器工具使用離線模型Cllama(llama.cpp)

以下說明如何在 AIChatPlus 編輯器工具中使用離線模型 llama.cpp

首先，從 HuggingFace 網站下載離線模型：[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

將模型存放在指定的資料夾中，例如放在遊戲專案的 Content/LLAMA 目錄下。

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

打開 AIChatPlus 編輯器工具：工具 -> AIChatPlus -> AIChat，新建聊天會話，並打開會話設置頁面

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

將 Api 設置為Cllama，開啟自訂 Api 設置，並新增模型搜索路徑，然後選擇模型。

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

開始聊天！！

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

##使用離線模型 Cllama (llama.cpp) 在編輯器工具中處理圖片。

從 HuggingFace 網站下載離線模型 MobileVLM_V2-1.7B-GGUF 同樣放到目錄 Content/LLAMA 下：[ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)與 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)。

設置對話模型：

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

請發送圖片來啟動聊天。

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

##使用 OpenAI 聊天的編輯器

打開聊天工具 Tools -> AIChatPlus -> AIChat，創建新的聊天會話 New Chat，設置會話 ChatApi 為 OpenAI，設置介面參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

開始聊天：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

將模型切換為 gpt-4o / gpt-4o-mini，您就能夠利用 OpenAI 的視覺功能來分析圖片。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

##編輯器使用 OpenAI 處理圖片（創建/修改/變種）

在聊天工具中建立新的圖片對話New Image Chat，將對話設置更改為 OpenAI，並設定參數。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

建立圖片

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

修改圖片，將對話圖片類型修改為「編輯」，並上傳兩張圖片，一張是原圖，另一張是遮罩，其中透明位置（alpha 通道為 0）表示需要修改的部分。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

請將圖片設定更改為「變種」，將會話圖片類型修改為「變異」，並上傳一張圖片，OpenAI將返回原始圖片的一個變種。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

##編輯器使用 Azure

新增對話（New Chat），將 ChatApi 改為 Azure，並設置 Azure 的 API 參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

##使用 Azure 建立圖片的編輯器

建立新的圖片聊天（New Image Chat），將 ChatApi 改為Azure，並設置Azure的API參數，請注意，如果是dall-e-2模型，需要將參數Quality和Stype設置為not_use

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

開始對話，請 Azure 創建圖片。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

##編輯器使用 Claude 聊天和分析圖片

建立一個新的對話（New Chat），將 ChatApi 修改為 Claude，並調整 Claude 的 API 參數。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

##編輯器使用 Ollama 聊天和分析圖片。

建立新的對話框（New Chat），將 ChatApi 改為 Ollama，並設定 Ollama 的 API 參數。若為文字對話，則設定模型為文字模型，例如 llama3.1；若需處理圖片，則設定模型為支援視覺的模型，例如 moondream。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###編輯器使用 Gemini

建立新的對話（New Chat），將 ChatApi 改為 Gemini，並設置 Gemini 的 API 參數。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

##編輯器使用 Gemini 發送音頻

從檔案讀取音頻 / 從資產讀取音頻 / 從麥克風錄取音頻，生成需要發送的音頻

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

##編輯器使用Deepseek

新增對話（New Chat），將 ChatApi 改為 OpenAi，並設置 Deepseek 的 Api 參數。新增候選模型名稱為 deepseek-chat，並將模型設置為 deepseek-chat。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

--8<-- "footer_tc.md"


> 這篇文章是使用 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
