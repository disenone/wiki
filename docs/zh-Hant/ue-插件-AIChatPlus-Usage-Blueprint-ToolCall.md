---
layout: post
title: Tool Call
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
- Tool Call
- Function Calling
description: Tool Call
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Tool Call" />

#藍圖篇 - 工具呼叫

工具調用（Tool Call）也稱為函式呼叫（Function Calling），意指大型模型能夠依據對話內容，判斷是否需要調用外部工具或函式來獲取資訊或執行操作。模型會返回需調用的函式名稱及參數，開發者實際執行調用後，將結果回傳給模型以繼續對話。

AIChatPlus 支援以下平台的 Tool Call 功能：

* OpenAI
* Claude
* Gemini
* Ollama
* Cllama伺服器（llama.cpp伺服器）

##核心概念

###工具定義

工具的定義包含以下關鍵欄位：

* **類型**：工具類型，目前僅支援 `Function`
* **名稱**：函數名稱，必須由 a-z、A-Z、0-9、底線或連字號組成，最大長度 64
* **描述**：函數描述，模型會根據此描述判斷何時調用該函數
* **屬性**：函數參數列表，每個參數包含名稱（Name）、描述（Description）、類型（Type）、是否必需（Required）等屬性

###工具呼叫流程

完整流程如下：工具呼叫

1. **發送請求**: 向模型發送包含工具定義的聊天請求
2. **模型判斷**: 模型根據對話內容判斷是否需要調用工具
3. **返回工具調用**：如果需要調用，模型返回要調用的函數名和參數
4. **執行函數**: 開發者根據返回資訊執行實際的函數調用
5. **返回結果**: 將函數執行結果作為新訊息發送給模型
6. **繼續對話**: 模型根據函數結果生成最終回覆

##OpenAI工具調用示例

以下以 OpenAI 為例，示範如何使用 Tool Call 功能。

###1. 定義 Tool

首先建立 Tool 的定義。本例中我們定義一個獲取快遞包裹送達時間的函數 `get_delivery_date`。

<!-- 需要圖片：展示創建 FAIChatPlus_ChatRequestTool 節點，設定 Type=Function, Name="get_current_weather", Description="取得指定地點的當前天氣" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_1.png)

###2. 定義工具參數

為 Tool 添加 Properties（參數）。本例中添加一個 `order_id` 參數，類型為 `string`，設置為必填。

<!-- 需要圖片：展示創建 FAIChatPlus_ChatRequestToolProperty 節點，設置 Name="location", Description="城市與州名，例如：San Francisco, CA", Type="string", Required=true，並透過 Make Array 連接到 Tool 的 Properties 欄位 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_2.png)

###3. 配置 Options

創建 `OpenAI Chat Request Options` 節點，設定 API Key 和 Model，並將 Tools 陣列連接到 Options。

<!-- 需要圖片：展示建立 OpenAI Chat Request Options 節點，設定 ApiKey，Model="gpt-4o-mini"，透過 Make Array 將上述的 Tool 連接到 Tools 欄位 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_3.png)

###4. 建立訊息

建立使用者訊息，詢問快遞包裹的相關問題。

<!-- 需要圖片：展示創建 Messages 陣列，添加一條 User Message，Content 設定為 "What's the weather like in Boston today?" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_4.png)

###5. 發送請求並處理Tool Call

建立 `Send OpenAI Chat Request In World` 節點，並將其綁定至 `On Message Finished` 事件。於事件回呼函式中，自 Payload 中擷取 ToolCalls 陣列。

當模型決定調用工具時，ToolCalls 陣列不為空。遍歷陣列以獲取每個 Tool Call 的資訊：

* **Id**：Tool Call 的唯一識別符
* **FunctionName**: 要呼叫的函式名稱
* **FunctionArguments**: 函數參數（JSON 字串格式）

<!-- 需要圖片：展示完整的發送請求藍圖，創建 Send OpenAI Chat Request In World 節點，連接 Options 和 Messages，綁定 On Message Finished 事件，在事件回呼中使用 Break 節點取得 Payload 中的 ToolCalls -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_5.png)

<!-- 需要圖片：展示遍歷 ToolCalls 陣列的藍圖，使用 For Each Loop 遍歷，對每個元素使用 Break 節點獲取 Id、FunctionName、FunctionArguments 欄位，並將其列印輸出 -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_6.png) -->

###6. 執行函數並返回結果

根據 FunctionName 執行對應的函數邏輯（本例中模擬獲取快遞包裹送達時間），然後將結果作為 ToolCallResult 類型的消息返回給模型。

創建新的 Message，需要設定：

* **角色**: 設定為 `工具`
* **內容**: 函數執行的結果
* **工具呼叫結果**：新增一個 `FAIChatPlus_ChatRequestToolCallResult`，設定 Id（使用先前的 Tool Call Id）、FunctionName 和 FunctionResult

<!-- 需要圖片：展示創建 Tool 角色訊息的藍圖，創建新的 Message，Role=Tool，Content 設定為模擬的天氣數據如 '{"temperature": "22", "unit": "celsius", "description": "Sunny"}'，並在 ToolCallResults 中加入對應的結果資訊 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_7.png)

###7. 繼續對話

將包含ToolCallResult結果的訊息加入到歷史訊息中，再次發送請求。模型會根據函數返回的結果生成最終的自然語言回覆。

<!-- 需要圖片：展示完整的第二次請求藍圖，將原始的 User Message、模型返回的 Assistant Message（包含 ToolCalls）、以及 Tool 結果 Message 組合成新的 Messages 陣列，再次調用 Send OpenAI Chat Request In World -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_8.png)

<!-- ### 9. 完整藍圖 -->

<!-- 完整的 Tool Call 藍圖看起來是這樣的： -->

<!-- 需要圖片：展示完整的 Tool Call 流程藍圖全貌，包含 Tool 定義、第一次請求、Tool Call 處理、第二次請求的完整流程 -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_9.png) -->

<!-- ### 10. 執行結果 -->

<!-- 運行藍圖，可以看到模型返回了包含天氣資訊的自然語言回覆。 -->

<!-- 需要圖片：展示運行結果截圖，螢幕上顯示模型的最終回覆，類似「波士頓目前的天氣為晴朗，氣溫22°C。」 -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_10.png) -->

##高階用法

###多個工具

可以同時定義多個Tools，模型會根據需要選擇呼叫哪個或哪些函式。

<!-- 需要圖片：展示定義多個工具的藍圖，例如同時定義取得當前天氣和取得股票價格兩個工具，並透過「建立陣列」功能組合成工具陣列 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_multi_tools.png)

###複雜參數類型

工具參數支援多種類型，可透過 `ExtraJsonString` 或 `ExtraJsonObject` 欄位添加更複雜的參數定義，例如列舉類型：

```json
{"enum": ["Beijing", "HongKong"]}
```

<!-- 需要圖片：展示使用 ExtraJsonString 設定列舉參數的藍圖，在 Property 節點的 ExtraJsonString 欄位中填入 '{"enum": ["celsius", "fahrenheit"]}' -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_extra_json.png)

###其他平台

Claude、Gemini、Ollama 和 CllamaServer 的 Tool Call 使用方式與 OpenAI 類似，只需替換對應的 Request 和 Options 節點即可。各平台的核心資料結構（`FAIChatPlus_ChatRequestTool`、`FAIChatPlus_ChatResponseToolCall` 等）是通用的。

--8<-- "footer_tc.md"


> 此貼文是使用ChatGPT翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遺漏之處。 
