---
layout: post
title: Json 操作
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini, Ollama, Json, Blueprint]
description: Json 操作
---
<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Json 操作" />

# 蓝图篇 - Json 操作

<!-- 需要图片：展示 Json 相关的所有蓝图节点概览，包括 JsonObject、JsonArray、JsonLibrary 分类下的节点 -->
![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_all.png)

## 概述

AIChatPlus 提供了完整的 JSON 蓝图操作支持，方便在蓝图中处理 JSON 数据。主要包含三个类：

* **UAIChatPlus_JsonObject**: JSON 对象操作类，用于处理 `{}` 格式的 JSON
* **UAIChatPlus_JsonArray**: JSON 数组操作类，用于处理 `[]` 格式的 JSON
* **UAIChatPlus_JsonLibrary**: JSON 工具函数库，提供静态工具函数

这些类支持：
* 创建、解析、序列化 JSON
* 读取和设置字段值
* 嵌套路径查询
* JSON 与 USTRUCT 互转
* 文件读写
* 链式调用

## JsonObject 基础操作

### 创建 JsonObject

使用 `Create Json Object` 创建一个空的 JSON 对象：

<!-- 需要图片：展示在蓝图中右键搜索 "Create Json Object" 并创建节点的截图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_create_1.png)

### 从字符串解析

使用 `Parse Json Object` 从 JSON 字符串创建对象：

<!-- 需要图片：展示 Parse Json Object 节点，输入一个 JSON 字符串如 '{"name":"test","value":123}'，输出 JsonObject、bSuccess、ErrorMessage -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_parse_1.png)

### 设置字段值

JsonObject 提供了多种 Set 方法，支持链式调用：

| 函数 | 说明 |
|-----|------|
| `Set String Field` | 设置字符串字段 |
| `Set Number Field` | 设置浮点数字段 |
| `Set Integer Field` | 设置整数字段 |
| `Set Boolean Field` | 设置布尔字段 |
| `Set Object Field` | 设置嵌套对象字段 |
| `Set Array Field` | 设置数组字段 |
| `Set Null Field` | 设置 null 字段 |

<!-- 需要图片：展示链式调用设置多个字段的蓝图，如 Create Json Object -> Set String Field("name", "player1") -> Set Integer Field("level", 10) -> Set Boolean Field("active", true) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_set_1.png)

### 获取字段值

JsonObject 提供了多种 Get 方法：

| 函数 | 说明 |
|-----|------|
| `Get String Field` | 获取字符串字段 |
| `Get Number Field` | 获取浮点数字段 |
| `Get Integer Field` | 获取整数字段 |
| `Get Boolean Field` | 获取布尔字段 |
| `Get Object Field` | 获取嵌套对象字段 |
| `Get Array Field` | 获取数组字段 |

<!-- 需要图片：展示从 JsonObject 获取字段值的蓝图，使用 Get String Field 获取 "name" 字段，显示 DefaultValue 和 bSuccess 参数 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_get_1.png)

### 字段检查

| 函数 | 说明 |
|-----|------|
| `Has Field` | 检查字段是否存在 |
| `Get Field Type` | 获取字段类型 |
| `Get Field Names` | 获取所有字段名 |
| `Remove Field` | 删除字段 |
| `Clear` | 清空所有字段 |

<!-- 需要图片：展示使用 Has Field 检查字段是否存在，Get Field Type 获取字段类型的蓝图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_check_1.png)

### 序列化为字符串

使用 `To Json String` 将 JsonObject 转换为字符串：

<!-- 需要图片：展示 To Json String 节点，输入 JsonObject，bPrettyPrint 参数，输出格式化的 JSON 字符串 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_tostring_1.png)

## JsonArray 基础操作

### 创建 JsonArray

使用 `Create Json Array` 创建一个空的 JSON 数组：

<!-- 需要图片：展示在蓝图中创建 Create Json Array 节点的截图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_create_1.png)

### 添加元素

JsonArray 提供了多种 Add 方法，支持链式调用：

| 函数 | 说明 |
|-----|------|
| `Add String` | 添加字符串元素 |
| `Add Number` | 添加浮点数元素 |
| `Add Integer` | 添加整数元素 |
| `Add Boolean` | 添加布尔元素 |
| `Add Object` | 添加对象元素 |
| `Add Array` | 添加数组元素 |
| `Add Null` | 添加 null 元素 |

<!-- 需要图片：展示链式调用添加多个元素的蓝图，如 Create Json Array -> Add String("a") -> Add String("b") -> Add Integer(123) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_add_1.png)

### 获取元素

JsonArray 提供了按索引获取元素的方法：

| 函数 | 说明 |
|-----|------|
| `Get String` | 获取字符串元素 |
| `Get Number` | 获取浮点数元素 |
| `Get Integer` | 获取整数元素 |
| `Get Boolean` | 获取布尔元素 |
| `Get Object` | 获取对象元素 |
| `Get Array` | 获取数组元素 |

<!-- 需要图片：展示使用 Get Object 按索引获取数组中的对象元素的蓝图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_get_1.png)

### 数组操作

| 函数 | 说明 |
|-----|------|
| `Length` | 获取数组长度 |
| `Is Valid Index` | 检查索引是否有效 |
| `Get Element Type` | 获取元素类型 |
| `Remove At` | 删除指定索引的元素 |
| `Clear` | 清空数组 |

<!-- 需要图片：展示使用 Length 获取数组长度，配合 For Loop 遍历数组的蓝图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_loop_1.png)

### 批量转换

JsonArray 支持与 UE 数组的批量转换：

| 函数 | 说明 |
|-----|------|
| `From String Array` | 从字符串数组创建 |
| `To String Array` | 转换为字符串数组 |
| `From Integer Array` | 从整数数组创建 |
| `To Integer Array` | 转换为整数数组 |

<!-- 需要图片：展示 From String Array 和 To String Array 的使用示例 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_batch_1.png)

## 路径查询

JsonObject 支持使用点分隔的路径访问嵌套数据，如 `player.inventory.gold`。

### 按路径获取值

使用 `Get String By Path` 按路径获取字符串值：

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

<!-- 需要图片：展示使用 Get String By Path 节点，Path 设置为 "player.name"，获取嵌套值的蓝图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_get_1.png)

### 按路径设置值

使用 `Set String By Path` 按路径设置值：

<!-- 需要图片：展示使用 Set String By Path 节点设置嵌套路径值的蓝图，显示 FAIChatPlus_JsonPathOptions 参数（bCaseSensitive、bCreateMissing） -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_set_1.png)

### 查询结果

路径查询返回 `FAIChatPlus_JsonQueryResult` 结构，包含：

* **bSuccess**: 查询是否成功
* **ValueType**: 返回值的类型
* **ErrorMessage**: 错误信息（如果失败）

<!-- 需要图片：展示 Break FAIChatPlus_JsonQueryResult 节点，显示 bSuccess、ValueType、ErrorMessage 字段 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_result_1.png)

## JSON 与 USTRUCT 转换

AIChatPlus 支持 JSON 与 USTRUCT 之间的转换，方便与蓝图结构体配合使用。

### JSON 字符串转 USTRUCT

使用 `Json String To Struct` 将 JSON 字符串直接转换为 USTRUCT：

<!-- 需要图片：展示 Json String To Struct 节点，输入 JSON 字符串，输出参数连接到一个自定义的 USTRUCT 变量（如 FAIChatPlus_OpenAIChatRequestOptions） -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_1.png)

### USTRUCT 转 JSON 字符串

使用 `Struct To Json String` 将 USTRUCT 转换为 JSON 字符串：

<!-- 需要图片：展示 Struct To Json String 节点，输入一个 USTRUCT 变量，bPrettyPrint 参数，输出 JSON 字符串 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_2.png)

### JsonObject 转 USTRUCT

使用 JsonObject 的 `To Struct` 方法：

<!-- 需要图片：展示 JsonObject 的 To Struct 节点用法 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_3.png)

### USTRUCT 转 JsonObject

使用 `From Struct` 静态方法从 USTRUCT 创建 JsonObject：

<!-- 需要图片：展示 From Struct 节点，输入 USTRUCT，输出 JsonObject -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_4.png)

## JsonLibrary 工具函数

`UAIChatPlus_JsonLibrary` 提供了一系列静态工具函数。

### 快速创建

| 函数 | 说明 |
|-----|------|
| `Make Json Object With String Field` | 快速创建带单个字段的 JsonObject |
| `Make Json Object From String Map` | 从 Map 创建 JsonObject |

<!-- 需要图片：展示使用 Make Json Object From String Map，输入 TMap<FString, FString>，输出 JsonObject 的蓝图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_make_1.png)

### 验证

| 函数 | 说明 |
|-----|------|
| `Validate Json String` | 验证 JSON 字符串是否有效 |
| `Is Json Object` | 检查是否为 JSON 对象 |
| `Is Json Array` | 检查是否为 JSON 数组 |

<!-- 需要图片：展示使用 Validate Json String 验证 JSON 字符串的蓝图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_validate_1.png)

### 格式化

| 函数 | 说明 |
|-----|------|
| `Prettify Json` | 格式化 JSON（添加缩进换行） |
| `Minify Json` | 压缩 JSON（移除空白） |

<!-- 需要图片：展示使用 Prettify Json 格式化 JSON 字符串，显示输入的压缩 JSON 和输出的格式化 JSON -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_format_1.png)

### 文件操作

| 函数 | 说明 |
|-----|------|
| `Load Json Object From File` | 从文件加载 JsonObject |
| `Save Json Object To File` | 保存 JsonObject 到文件 |
| `Load Json Array From File` | 从文件加载 JsonArray |
| `Save Json Array To File` | 保存 JsonArray 到文件 |

<!-- 需要图片：展示 Save Json Object To File 和 Load Json Object From File 的使用示例 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_file_1.png)

### 比较

| 函数 | 说明 |
|-----|------|
| `Equals Json Object` | 比较两个 JsonObject 是否相等 |
| `Equals Json Array` | 比较两个 JsonArray 是否相等 |

<!-- 需要图片：展示使用 Equals Json Object 比较两个 JsonObject 的蓝图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_compare_1.png)

### 高级路径查询

| 函数 | 说明 |
|-----|------|
| `Query String By Path` | 按路径查询字符串（支持数组索引，如 `items[0].name`） |
| `Query Object By Path` | 按路径查询对象 |
| `Query Array By Path` | 按路径查询数组 |

<!-- 需要图片：展示使用 Query String By Path 查询带数组索引的路径，如 "data.items[0].name" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_query_1.png)

### 批量操作

| 函数 | 说明 |
|-----|------|
| `Set String Fields From Map` | 批量设置字符串字段 |
| `Get String Fields To Map` | 批量获取字符串字段 |

<!-- 需要图片：展示使用 Set String Fields From Map 批量设置字段的蓝图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_batch_1.png)

## 其他操作

### 合并 JsonObject

使用 `Merge` 方法合并两个 JsonObject：

<!-- 需要图片：展示 Merge 节点，将两个 JsonObject 合并，显示 bOverwrite 参数 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_merge_1.png)

### 复制 JsonObject

使用 `Duplicate` 方法深拷贝 JsonObject：

<!-- 需要图片：展示 Duplicate 节点复制 JsonObject 的蓝图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_dup_1.png)

## 实际应用示例

### 解析 API 响应

从 AI 聊天响应中提取 Tool Call 的参数：

<!-- 需要图片：展示完整的解析示例蓝图：从 FunctionArguments 字符串 Parse 成 JsonObject，然后使用 Get String Field 获取参数值 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_1.png)

### 构建请求参数

使用 JsonObject 构建复杂的请求参数：

<!-- 需要图片：展示构建嵌套 JSON 结构的蓝图，创建 JsonObject 设置多个字段，包含嵌套的 JsonObject 和 JsonArray -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_2.png)

### 配置文件读写

从 JSON 文件加载配置，修改后保存：

<!-- 需要图片：展示完整的配置读写流程：Load Json Object From File -> 修改字段 -> Save Json Object To File -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_3.png)

## 类型枚举

`EAIChatPlus_JsonValueType` 枚举定义了 JSON 值的类型：

| 枚举值 | 说明 |
|-------|------|
| `None` | 未知类型 |
| `Null` | null 值 |
| `String` | 字符串 |
| `Number` | 数字 |
| `Boolean` | 布尔值 |
| `Array` | 数组 |
| `Object` | 对象 |

<!-- 需要图片：展示使用 Switch 节点根据 JsonValueType 进行不同处理的蓝图 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_type_1.png)

--8<-- "footer.md"
