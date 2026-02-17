---
layout: post
title: CllamaServer (llama.cpp server)
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
- CllamaServer
description: CllamaServer (llama.cpp server)
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - CllamaServer (llama.cpp server)" />

#藍圖篇 - CllamaServer (llama.cpp 伺服器)

<!-- 需要圖片：展示與 CllamaServer 相關的所有藍圖節點概覽，類似其他文件的 xxx_all.png -->
![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_all.png)

##概覽

CllamaServer 是基於 llama.cpp 的 Server 模式所實現的，能夠在本地啟動一個與 OpenAI API 相容的伺服器，並支援多項功能：

* **本地推理服務**: 在本地啟動 AI 推理伺服器，無需依賴外部 API
* **兼容 OpenAI API**：採用與 OpenAI 相容的 API 格式，便於遷移與整合
* **多會話支援**: 支援多個並行請求
* **工具呼叫**：支援函式呼叫功能
* **語音轉文字**: 支援 Speech-to-Text 功能
* **可視化管理**：編輯器內建 Server 管理介面

與 Cllama 的區別：
* **Cllama**：直接在進程內加載模型進行推理，單次只能處理一個請求
* **CllamaServer**：啟動獨立的 HTTP 伺服器，能夠處理多個並行請求，API 相容於 OpenAI 格式

##準備工作

由於是本地運行，需要先準備好離線模型文件，例如從HuggingFace下載：[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

將模型放置於某個資料夾內，例如放在遊戲專案的目錄 `Content/LLAMA` 下。

##創建 CllamaServer

###使用藍圖創建 Server

在藍圖中點擊右鍵創建節點 `Create Cllama Server In World`

<!-- 需要圖片：展示在藍圖中右鍵搜尋「Create Cllama Server」並建立節點的截圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_1.png)

###設定 Server 參數

建立 `Cllama Server Param` 節點，並設定關鍵參數：

* **模組**: 模型檔案路徑（必填）
* **連接埠**: 伺服器埠（0 表示自動分配）
* **主機**: 監聽地址，預設為 `127.0.0.1`
* **NGpuLayers**: GPU 層數（-1 表示全部使用 GPU）

<!-- 需提供圖片：展示建立 FAIChatPlus_CllamaServerParam 節點，設定 Model 路徑、Port、NGpuLayers 等參數的畫面截圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_2.png)

###綁定回調事件

綁定 Server 的回調事件：

* **On Started**：當伺服器啟動成功時觸發
* **On Stopped**: 伺服器停止時觸發
* **失敗時（On Failed）**：伺服器啟動失敗時觸發

<!-- 需要圖片：展示綁定 OnStartedListeners、OnStoppedListeners、OnFailedListeners 事件的藍圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_3.png)

###完整的創建藍圖

完整的 Server 建立藍圖如下：

<!-- 需要圖片：展示完整的 Server 創建藍圖全貌，包括參數設置、創建節點、回調綁定 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_4.png)

執行藍圖後，Server啟動成功會觸發`On Started`事件。

<!-- 需要圖片：展示 Server 啟動成功後的運行結果，顯示啟動成功的日誌或畫面輸出 -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_5.png) -->

##伺服器參數詳解

`FAIChatPlus_CllamaServerParam` 結構體包含以下參數：

###常用參數

| 參數 | 類型 | 預設值 | 說明 |
|-----|------|-------|------|
| 模型 | FString | - | 模型檔案路徑（必填） |
| 埠號 | int32 | 0 | 監聽埠，0 表示自動分配 |
| 主機 | FString | 127.0.0.1 | 監聽地址 |
| NGpuLayers | int32 | -1 | GPU層數，-1表示全部 |
| bUseJinja | bool | false | 使用 Jinja 模板 |
| MMProj | FString | - | 多模態投影檔案路徑 |
| 溫度 | float | 0.8 | 採樣溫度 |

###推理參數

| 參數 | 類型 | 預設值 | 說明 |
|-----|------|-------|------|
| CtxSize | int32 | 4096 | 上下文大小 |
| NPredict | int32 | -1 | 預測 Token 數，-1 表示無限 |
| 執行緒數 | int32 | -1 | CPU 執行緒數量，-1 表示自動設定 |
| BatchSize | int32 | 2048 | 批次處理大小 |

###採樣參數

| 參數 | 類型 | 預設值 | 說明 |
|-----|------|-------|------|
| TopK | int32 | 40 | Top-K 取樣 |
| TopP | 浮點數 | 0.9 | Top-P 取樣 |
| MinP | 浮點數 | 0.1 | 最小概率採樣 |
| RepeatPenalty | float | 1.0 | 重複懲罰 |

###伺服器參數

| 參數 | 類型 | 預設值 | 說明 |
|-----|------|-------|------|
| ApiKey | FString | - | API 金鑰（可選） |
| Timeout | int32 | 600 | 逾時時間（秒） |
| Parallel | int32 | 1 | 並行序列數 |
| bNoWebUI | 布林值 | 否 | 停用 Web 使用者介面 |
| bVerbose | 布林值 | 否 | 詳細日誌 |

##使用 CllamaServer 進行聊天

###創建聊天請求

當 Server 成功啟動後，便可使用 `Send CllamaServer Chat Request` 節點發送聊天請求。

<!-- 需要圖片：展示在藍圖中右鍵搜尋「CllamaServer Chat Request」並建立節點的截圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_1.png)

###設定聊天選項

創建 `CllamaServer Chat Request Options` 節點，設置 BaseUrl 為 Server 地址。

可以通過 `Get Server Info By ID` 節點獲取 Server 資訊。

<!-- 需要圖片：展示創建 FAIChatPlus_CllamaServerChatRequestOptions 節點，使用 Get Http Address 獲取 Server 位址並設定到 BaseUrl 的藍圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_2.png)

###建立訊息

創建 Messages 陣列，新增 System Message 和 User Message。

<!-- 需要圖片：展示創建 Messages 陣列，包含 System Message（設定助手角色）和 User Message（用戶問題）的藍圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_3.png)

###綁定回調處理回應

綁定 `On Message` 或 `On Message Finished` 事件來接收模型回應。

<!-- 需要圖片：展示綁定 OnMessageListeners 事件，並在回調中打印訊息到螢幕的藍圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_4.png)

###完整的聊天藍圖

完整的聊天藍圖如下：

<!-- 需要圖片：展示完整的聊天藍圖全貌，包括創建 Server、等待啟動、發送聊天請求、處理回應的完整流程 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_5.png)

###執行結果

執行藍圖後，螢幕上將顯示模型返回的訊息。

<!-- 需要圖片：展示聊天運行結果，螢幕上顯示模型回覆的內容 -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_6.png) -->

##伺服器管理

###取得 Server 資訊

使用 `Get Server Info` 節點取得 Server 的詳細資訊。

<!-- 需要圖片：展示使用 Get Server Info 節點取得 FAIChatPlus_CllamaServerInfo 的藍圖，並 Break 顯示各欄位 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_info_1.png)

伺服器資訊 包含以下資訊：
* **ServerID**: 伺服器唯一 ID
* **主機**: 監聽位址
* **連接埠**：監聽埠號
* **地址**: 完整地址（host:port）
* **HttpAddress**: HTTP 位址（http://host:port）
* **bIsRunning**: 是否正在執行
* **參數**：伺服器參數

###停止伺服器

使用 `Stop Server By ID` 節點停止當前 Server。

<!-- 需要圖片：展示調用 Stop Cllama Server 節點的藍圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_stop_1.png)

###靜態管理函數

AIChatPlus 提供了一系列靜態函數用於管理所有 Server：

| 函數 | 說明 |
|-----|------|
| `Is Server Valid (Static)` | 檢查 Server 是否有效 |
| `Is Server Running (Static)` | 檢查 Server 是否運行中 |
| `Stop Server By ID` | 透過 ID 停止指定 Server |
| `Stop All Servers` | 停止所有伺服器 |
| `Get Server Info By ID` | 通過 ID 獲取伺服器資訊 |
| `Get All Server IDs` | 獲取所有伺服器 ID |
| `Get Server By ID` | 通過 ID 取得 Server 實例 |

<!-- 需要圖片：展示使用「取得所有伺服器ID」和「停止所有伺服器」等靜態管理函式的藍圖範例 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_static_1.png)

##多模態支援

CllamaServer 支援多模態模型（如 Moondream、Qwen2-VL 等）。

###配置多模態參數

在 Server 參數中設定 `MMProj`（多模態投影檔案路徑）：

<!-- 需要圖片：展示在 Server Param 中設置 Model 和 MMProj 兩個路徑的藍圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_1.png)

###發送圖片訊息

在 Messages 中加入圖片：

<!-- 需要圖片：展示讀取圖片檔案，建立包含圖片的 Message，透過 CllamaServer 發送請求的藍圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_2.png)

<!-- ### 執行結果 -->

<!-- 需要圖片：展示圖片識別的運行結果，螢幕顯示模型對圖片內容的描述 -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_3.png) -->

## Tool Calling

CllamaServer 支援 Tool Calling（函數呼叫）功能，其使用方式與 OpenAI 相似。

詳細用法請參考 [Tool Call](ue-插件-AIChatPlus-Usage-Blueprint-ToolCall.md)文件。

使用 CllamaServer 進行 Tool Call 時，需要：
1. 在 Server 參數中設定 `bUseJinja = true`
2. 在 Chat Options 的 Tools 欄位中定義工具

<!-- 需要圖片：展示 CllamaServer Tool Call 的完整藍圖，包括 bUseJinja=true 的設定和 Tools 定義 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_tool_1.png)

##編輯器 Server 管理

AIChatPlus 在編輯器工具中提供了可視化的 CllamaServer 管理介面，方便創建、監控和管理多個 Server。

開啟編輯器工具：`工具 -> AIChatPlus -> AIChat`，打開 Cllama Server Manager 標籤頁。

<!-- 需提供圖片：展示編輯器中 CllamaServer 管理介面的截圖，顯示 Server 列表、創建按鈕、狀態資訊等 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_editor_1.png)

在編輯器中可以：
* 建立新的伺服器
* 檢視運行中的伺服器狀態
* 停止指定的伺服器
* 配置伺服器參數
* Server 配置會自動儲存

<!-- 需要圖片：展示編輯器中創建新 Server 的介面，顯示參數配置面板 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_editor_2.png)

##與其他API的關係

由於 CllamaServer 能兼容 OpenAI API 格式，您同樣可使用 OpenAI 的 Chat Request 節點來與 CllamaServer 進行通訊，只需將 `BaseUrl` 設定為 CllamaServer 的地址即可。

<!-- 需要圖片：展示使用 OpenAI Chat Request 節點，但 BaseUrl 設定為 CllamaServer 位址的藍圖範例 -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_openai_1.png) -->

--8<-- "footer_tc.md"


> 這篇文章是由ChatGPT翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遺漏之處。 
