---
layout: post
title: Json 操作
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
- Json
- Blueprint
description: JSON 操作
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Json 操作" />

#藍圖篇 - Json 操作

<!-- 需要圖片：展示 Json 相關的所有藍圖節點概覽，包括 JsonObject、JsonArray、JsonLibrary 分類下的節點 -->
![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_all.png)

##概述

AIChatPlus 提供完整的 JSON 藍圖操作支援，方便在藍圖中處理 JSON 數據。主要包含三個類：

* **UAIChatPlus_JsonObject**: JSON 物件操作類，用於處理 `{}` 格式的 JSON
* **UAIChatPlus_JsonArray**: JSON 陣列操作類，用於處理 `[]` 格式的 JSON
* **UAIChatPlus_JsonLibrary**: JSON 工具函式庫，提供靜態工具函式

這些類別支援：
* 創建、解析、序列化 JSON
* 讀取和設定欄位值
* 巢狀路徑查詢
* JSON 與 USTRUCT 互轉
* 檔案讀寫
* 鏈式呼叫

##JsonObject 基礎操作

###建立 JsonObject

使用 `Create Json Object` 建立一個空的 JSON 物件：

<!-- 需要圖片：展示在藍圖中右鍵搜尋「Create Json Object」並建立節點的截圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_create_1.png)

###從字串解析

使用 `Parse Json Object` 從 JSON 字串建立物件：

<!-- 需要圖片：展示 Parse Json Object 節點，輸入一個 JSON 字串如 '{"name":"test","value":123}'，輸出 JsonObject、bSuccess、ErrorMessage -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_parse_1.png)

###設定欄位值

JsonObject 提供了多種 Set 方法，支援鏈式呼叫：

| 函數 | 說明 |
|-----|------|
| `Set String Field` | 設定字串欄位 |
| `Set Number Field` | 設定浮點數字欄位 |
| `Set Integer Field` | 設定整數字段 |
| `Set Boolean Field` | 設定布林欄位 |
| `Set Object Field` | 設定嵌套物件欄位 |
| `Set Array Field` | 設置陣列欄位 |
| `Set Null Field` | 設定 null 欄位 |

<!-- 需要圖片：展示鏈式調用設置多個欄位的藍圖，例如 Create Json Object -> Set String Field("name", "player1") -> Set Integer Field("level", 10) -> Set Boolean Field("active", true) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_set_1.png)

###獲取欄位值

JsonObject 提供了多種 Get 方法：

| 函數 | 說明 |
|-----|------|
| `Get String Field` | 獲取字串欄位 |
| `Get Number Field` | 取得浮點數字欄位 |
| `Get Integer Field` | 獲取整數字段 |
| `Get Boolean Field` | 獲取布林欄位 |
| `Get Object Field` | 獲取嵌套物件欄位 |
| `取得陣列欄位` | 取得陣列欄位 |

<!-- 需要圖片：展示從 JsonObject 獲取欄位值的藍圖，使用 Get String Field 獲取 "name" 欄位，顯示 DefaultValue 和 bSuccess 參數 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_get_1.png)

###欄位檢查

| 函數 | 說明 |
|-----|------|
| `Has Field` | 檢查欄位是否存在 |
| `Get Field Type` | 獲取欄位型別 |
| `Get Field Names` | 獲取所有欄位名稱 |
| `Remove Field` | 刪除欄位 |
| `Clear` | 清空所有欄位 |

<!-- 需要圖片：展示使用 Has Field 檢查欄位是否存在，Get Field Type 獲取欄位類型的藍圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_check_1.png)

###序列化為字串

使用 `To Json String` 將 JsonObject 轉換為字串：

<!-- 需要圖片：展示 To Json String 節點，輸入 JsonObject，bPrettyPrint 參數，輸出格式化的 JSON 字串 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_tostring_1.png)

##JsonArray 基本操作

###建立 JsonArray

使用 `Create Json Array` 建立一個空的 JSON 陣列：

<!-- 需要圖片：展示在藍圖中創建 Create Json Array 節點的截圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_create_1.png)

###添加元素

JsonArray 提供了多種 Add 方法，支援鏈式呼叫：

| 函數 | 說明 |
|-----|------|
| `Add String` | 加入字串元素 |
| `Add Number` | 新增浮點數元素 |
| `Add Integer` | 添加整數元素 |
| `Add Boolean` | 添加布林元素 |
| `Add Object` | 添加物件元素 |
| `Add Array` | 新增陣列元素 |
| `Add Null` | 添加 null 元素 |

<!-- 需要圖片：展示鏈式呼叫添加多個元素的藍圖，如 Create Json Array -> Add String("a") -> Add String("b") -> Add Integer(123) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_add_1.png)

###獲取元素

JsonArray 提供了按索引獲取元素的方法：

| 函數 | 說明 |
|-----|------|
| `Get String` | 獲取字符串元素 |
| `Get Number` | 獲取浮點數元素 |
| `Get Integer` | 獲取整數元素 |
| `Get Boolean` | 獲取布林元素 |
| `Get Object` | 獲取物件元素 |
| `Get Array` | 獲取陣列元素 |

<!-- 需要圖片：展示使用 Get Object 按索引獲取陣列中物件元素的藍圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_get_1.png)

###陣列操作

| 函數 | 說明 |
|-----|------|
| `Length` | 取得陣列長度 |
| `Is Valid Index` | 檢查索引是否有效 |
| `Get Element Type` | 獲取元素類型 |
| `Remove At` | 刪除指定索引的元素 |
| `Clear` | 清空陣列 |

<!-- 需要圖片：展示使用 Length 取得陣列長度，配合 For Loop 遍歷陣列的藍圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_loop_1.png)

###批量轉換

JsonArray 支援與 UE 陣列的批次轉換：

| 函數 | 說明 |
|-----|------|
| `From String Array` | 從字串陣列建立 |
| `To String Array` | 轉換為字串陣列 |
| `From Integer Array` | 從整數陣列創建 |
| `To Integer Array` | 轉換為整數陣列 |

<!-- 需要圖片：展示 From String Array 和 To String Array 的使用範例 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_batch_1.png)

##路徑查詢

JsonObject 支援使用點分隔的路徑來存取巢狀資料，例如 `player.inventory.gold`。

###按路徑取得值

使用 `Get String By Path` 按路徑取得字串值：

```json
{
    "player": {
        "name": "Hero",
        "inventory": {
            "gold": 1000
        }
    }
}
```

<!-- 需要圖片：展示使用「透過路徑取得字串」節點，路徑設為「player.name」，取得巢狀結構數值的藍圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_get_1.png)

###依路徑設定值

使用 `Set String By Path` 依照路徑設定值：

<!-- 需要圖片：展示使用Set String By Path節點設定巢狀路徑值的藍圖，顯示FAIChatPlus_JsonPathOptions參數（bCaseSensitive、bCreateMissing） -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_set_1.png)

###查詢結果

路徑查詢返回 `FAIChatPlus_JsonQueryResult` 結構，包含：

* **bSuccess**：查詢是否成功
* **ValueType**: 返回值的類型
* **ErrorMessage**: 錯誤信息（如果失敗）

<!-- 需要圖片：展示 Break FAIChatPlus_JsonQueryResult 節點，顯示 bSuccess、ValueType、ErrorMessage 欄位 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_result_1.png)

##JSON 與 USTRUCT 轉換

AIChatPlus 支援 JSON 與 USTRUCT 之間的轉換，便於與藍圖結構體搭配使用。

###JSON 字串轉 USTRUCT

使用 `Json String To Struct` 將 JSON 字符串直接轉換為 USTRUCT：

<!-- 需要圖片：展示 Json String To Struct 節點，輸入 JSON 字串，輸出參數連接到一個自訂的 USTRUCT 變數（如 FAIChatPlus_OpenAIChatRequestOptions） -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_1.png)

###USTRUCT 轉 JSON 字串

使用 `Struct To Json String` 將 USTRUCT 轉換為 JSON 字串：

<!-- 需要圖片：展示 Struct To Json String 節點，輸入一個 USTRUCT 變數，bPrettyPrint 參數，輸出 JSON 字串 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_2.png)

###JsonObject 轉換為 USTRUCT

使用 JsonObject 的 `To Struct` 方法：

<!-- 需圖片：展示 JsonObject 的 To Struct 節點用法 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_3.png)

###USTRUCT 轉換為 JsonObject

使用 `From Struct` 靜態方法從 USTRUCT 建立 JsonObject：

<!-- 需要圖片：展示 From Struct 節點，輸入 USTRUCT，輸出 JsonObject -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_4.png)

##JsonLibrary 工具函數

`UAIChatPlus_JsonLibrary` 提供了一系列靜態工具函數。

###快速建立

| 函數 | 說明 |
|-----|------|
| `Make Json Object With String Field` | 快速建立帶單個欄位的 JsonObject |
| `Make Json Object From String Map` | 從 Map 創建 JsonObject |

<!-- 需要圖片：展示使用「從字串映射建立JSON物件」，輸入TMap<FString, FString>，輸出JsonObject的藍圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_make_1.png)

###驗證

| 函數 | 說明 |
|-----|------|
| `Validate Json String` | 驗證 JSON 字符串是否有效 |
| `Is Json Object` | 檢查是否為 JSON 物件 |
| `Is Json Array` | 檢查是否為 JSON 陣列 |

<!-- 需要圖片：展示使用 Validate Json String 驗證 JSON 字串的藍圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_validate_1.png)

###格式化

| 函數 | 說明 |
|-----|------|
| `Prettify Json` | 格式化 JSON（新增縮排換行） |
| `Minify Json` | 壓縮 JSON（移除空白） |

<!-- 需要圖片：展示使用 Prettify Json 格式化 JSON 字串，顯示輸入的壓縮 JSON 和輸出的格式化 JSON -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_format_1.png)

###檔案操作

| 函數 | 說明 |
|-----|------|
| `Load Json Object From File` | 從檔案載入 JsonObject |
| `Save Json Object To File` | 將 JsonObject 存入檔案 |
| `從檔案載入 JsonArray` | 從檔案載入 JsonArray |
| `Save Json Array To File` | 將 Json 陣列儲存至檔案 |

<!-- 需要圖片：展示 Save Json Object To File 和 Load Json Object From File 的使用範例 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_file_1.png)

###比較

| 函數 | 說明 |
|-----|------|
| `Equals Json Object` | 比較兩個 JsonObject 是否相等 |
| `Equals Json Array` | 比較兩個 JsonArray 是否相等 |

<!-- 需要圖片：展示使用 Equals Json Object 比較兩個 JsonObject 的藍圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_compare_1.png)

###高級路徑查詢

| 函數 | 說明 |
|-----|------|
| `Query String By Path` | 按路徑查詢字符串（支援陣列索引，如 `items[0].name`） |
| `Query Object By Path` | 按路徑查詢物件 |
| `Query Array By Path` | 按路徑查詢陣列 |

<!-- 需要圖片：展示使用 Query String By Path 查詢帶有陣列索引的路徑，如 "data.items[0].name" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_query_1.png)

###批量操作

| 函數 | 說明 |
|-----|------|
| `從映射設置字符串字段` | 批量設置字符串字段 |
| `Get String Fields To Map` | 批量獲取字串欄位 |

<!-- 需要圖片：展示使用 Set String Fields From Map 批次設定欄位的藍圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_batch_1.png)

##其他操作

###合併 JsonObject

使用 `Merge` 方法合併兩個 JsonObject：

<!-- 需要圖片：展示 Merge 節點，將兩個 JsonObject 合併，顯示 bOverwrite 參數 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_merge_1.png)

###複製 JsonObject

使用 `Duplicate` 方法深複製 JsonObject：

<!-- 需要圖片：展示 Duplicate 節點複製 JsonObject 的藍圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_dup_1.png)

##實際應用示例

###解析API回應

從 AI 聊天回應中提取工具呼叫（Tool Call）的參數：

<!-- 需要圖片：展示完整的解析範例藍圖：從 FunctionArguments 字串 Parse 成 JsonObject，接著使用 Get String Field 取得參數值 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_1.png)

###構建請求參數

使用 JsonObject 構建複雜的請求參數：

<!-- 需要圖片：展示構建嵌套JSON結構的藍圖，建立JsonObject設定多個欄位，包含嵌套的JsonObject與JsonArray -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_2.png)

###配置文件讀寫

從 JSON 檔案載入配置，修改後儲存：

<!-- 需要圖片：展示完整的配置讀寫流程：從檔案載入Json物件 -> 修改欄位 -> 將Json物件儲存至檔案 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_3.png)

##類型枚舉

`EAIChatPlus_JsonValueType` 枚舉定義了 JSON 值的類型：

| 列舉值 | 說明 |
|-------|------|
| `None` | 未知類型 |
| `Null` | 空值 |
| `String` | 字串 |
| `Number` | 數字 |
| `Boolean` | 布林值 |
| `Array` | 陣列 |
| `Object` | 對象 |

<!-- 需要圖片：展示使用 Switch 節點根據 JsonValueType 進行不同處理的藍圖 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_type_1.png)

--8<-- "footer_tc.md"


> 此貼文由 ChatGPT 翻譯，請至[**回饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
