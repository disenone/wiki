---
layout: post
title: Tool Call
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini, Ollama, Tool Call, Function Calling]
description: Tool Call
---
<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Tool Call" />

# 蓝图篇 - Tool Call

Tool Call（工具调用）也被称为 Function Calling（函数调用），是指大模型可以根据对话内容，判断是否需要调用外部工具/函数来获取信息或执行操作。模型会返回需要调用的函数名称和参数，由开发者执行实际调用后，将结果返回给模型继续对话。

AIChatPlus 支持以下平台的 Tool Call 功能：

* OpenAI
* Claude
* Gemini
* Ollama
* CllamaServer（llama.cpp server）

## 核心概念

### Tool 定义

Tool 的定义包含以下关键字段：

* **Type**: 工具类型，目前仅支持 `Function`
* **Name**: 函数名称，必须由 a-z、A-Z、0-9、下划线或连字符组成，最大长度 64
* **Description**: 函数描述，模型会根据此描述判断何时调用该函数
* **Properties**: 函数参数列表，每个参数包含 Name、Description、Type、Required 等属性

### Tool Call 流程

Tool Call 的完整流程如下：

1. **发送请求**: 向模型发送包含 Tools 定义的聊天请求
2. **模型判断**: 模型根据对话内容判断是否需要调用工具
3. **返回 Tool Calls**: 如果需要调用，模型返回要调用的函数名和参数
4. **执行函数**: 开发者根据返回信息执行实际的函数调用
5. **返回结果**: 将函数执行结果作为新消息发送给模型
6. **继续对话**: 模型根据函数结果生成最终回复

## OpenAI Tool Call 示例

下面以 OpenAI 为例，演示如何使用 Tool Call 功能。

### 1. 定义 Tool

首先创建 Tool 定义。本例中我们定义一个获取快递包裹送达时间的函数 `get_delivery_date`。

<!-- 需要图片：展示创建 FAIChatPlus_ChatRequestTool 节点，设置 Type=Function, Name="get_current_weather", Description="Get the current weather in a given location" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_1.png)

### 2. 定义 Tool 参数

为 Tool 添加 Properties（参数）。本例中添加一个 `order_id` 参数，类型为 `string`，设置为必填。

<!-- 需要图片：展示创建 FAIChatPlus_ChatRequestToolProperty 节点，设置 Name="location", Description="The city and state, e.g. San Francisco, CA", Type="string", Required=true，并通过 Make Array 连接到 Tool 的 Properties 字段 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_2.png)

### 3. 配置 Options

创建 `OpenAI Chat Request Options` 节点，设置 API Key 和 Model，并将 Tools 数组连接到 Options。

<!-- 需要图片：展示创建 OpenAI Chat Request Options 节点，设置 ApiKey, Model="gpt-4o-mini", 通过 Make Array 将上面的 Tool 连接到 Tools 字段 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_3.png)

### 4. 创建 Messages

创建用户消息，询问快递包裹相关的问题。

<!-- 需要图片：展示创建 Messages 数组，添加一条 User Message，Content 设置为 "What's the weather like in Boston today?" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_4.png)

### 5. 发送请求并处理 Tool Call

创建 `Send OpenAI Chat Request In World` 节点，绑定 `On Message Finished` 事件。在事件回调中，从 Payload 获取 ToolCalls 数组。

当模型决定调用工具时，ToolCalls 数组不为空。遍历数组获取每个 Tool Call 的信息：

* **Id**: Tool Call 的唯一标识符
* **FunctionName**: 要调用的函数名
* **FunctionArguments**: 函数参数（JSON 字符串格式）

<!-- 需要图片：展示完整的发送请求蓝图，创建 Send OpenAI Chat Request In World 节点，连接 Options 和 Messages，绑定 On Message Finished 事件，在事件回调中使用 Break 节点获取 Payload 中的 ToolCalls -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_5.png)

<!-- 需要图片：展示遍历 ToolCalls 数组的蓝图，使用 For Each Loop 遍历，对每个元素使用 Break 节点获取 Id, FunctionName, FunctionArguments 字段，并将其打印输出 -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_6.png) -->

### 6. 执行函数并返回结果

根据 FunctionName 执行对应的函数逻辑（本例中模拟获取快递包裹送达时间），然后将结果作为 ToolCallResult 类型的消息返回给模型。

创建新的 Message，需要设置：

* **Role**: 设置为 `Tool`
* **Content**: 函数执行的结果
* **ToolCallResults**: 添加一个 `FAIChatPlus_ChatRequestToolCallResult`，设置 Id（使用之前的 Tool Call Id）、FunctionName 和 FunctionResult

<!-- 需要图片：展示创建 Tool 角色消息的蓝图，创建新的 Message，Role=Tool，Content 设置为模拟的天气数据如 '{"temperature": "22", "unit": "celsius", "description": "Sunny"}'，并在 ToolCallResults 中添加对应的结果信息 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_7.png)

### 7. 继续对话

将包含 ToolCallResult 结果的消息添加到历史消息中，再次发送请求。模型会根据函数返回的结果生成最终的自然语言回复。

<!-- 需要图片：展示完整的第二次请求蓝图，将原始的 User Message、模型返回的 Assistant Message（包含 ToolCalls）、以及 Tool 结果 Message 组合成新的 Messages 数组，再次调用 Send OpenAI Chat Request In World -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_8.png)

<!-- ### 9. 完整蓝图 -->

<!-- 完整的 Tool Call 蓝图看起来是这样的： -->

<!-- 需要图片：展示完整的 Tool Call 流程蓝图全貌，包含 Tool 定义、第一次请求、Tool Call 处理、第二次请求的完整流程 -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_9.png) -->

<!-- ### 10. 运行结果 -->

<!-- 运行蓝图，可以看到模型返回了包含天气信息的自然语言回复。 -->

<!-- 需要图片：展示运行结果截图，屏幕上显示模型的最终回复，类似 "The current weather in Boston is sunny with a temperature of 22°C." -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_10.png) -->

## 高级用法

### 多个 Tools

可以同时定义多个 Tools，模型会根据需要选择调用哪个或哪些函数。

<!-- 需要图片：展示定义多个 Tools 的蓝图，例如同时定义 get_current_weather 和 get_stock_price 两个 Tool，通过 Make Array 组合成 Tools 数组 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_multi_tools.png)

### 复杂参数类型

Tool 参数支持多种类型，可以通过 `ExtraJsonString` 或 `ExtraJsonObject` 字段添加更复杂的参数定义，例如枚举类型：

```json
{"enum": ["Beijing", "HongKong"]}
```

<!-- 需要图片：展示使用 ExtraJsonString 设置枚举参数的蓝图，在 Property 节点的 ExtraJsonString 字段中填入 '{"enum": ["celsius", "fahrenheit"]}' -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_extra_json.png)

### 其他平台

Claude、Gemini、Ollama 和 CllamaServer 的 Tool Call 用法与 OpenAI 类似，只需替换相应的 Request 和 Options 节点即可。各平台的核心数据结构（`FAIChatPlus_ChatRequestTool`、`FAIChatPlus_ChatResponseToolCall` 等）是通用的。

--8<-- "footer.md"
