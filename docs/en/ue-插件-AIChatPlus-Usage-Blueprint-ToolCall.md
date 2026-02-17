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

#Blueprint Chapter - Tool Call

Tool Calling, also known as Function Calling, refers to the capability of large models to determine whether they need to invoke external tools/functions based on the conversation content, in order to gather information or perform actions. The model will return the names of the functions to be called along with their parameters. Developers then execute the actual calls and feed the results back to the model for continuing the dialogue.

AIChatPlus supports the Tool Call feature on the following platforms:

* OpenAI
* Claude
* Gemini
* Ollama
* CllamaServer (llama.cpp server)

##Core Concepts

###Definition of Tool

The definition of a Tool includes the following key fields:

* **Type**: The type of tool; currently only `Function` is supported.
* **Name**: Function name, which must consist of a-z, A-Z, 0-9, underscores or hyphens, with a maximum length of 64
* **Description**: Function description, the model will determine when to call this function based on this description.
* **Properties**: The parameter list of a function, where each parameter includes attributes such as Name, Description, Type, Required, etc.

###Tool Call Process

The complete workflow of Tool Call is as follows:

1. **Send Request**: Dispatch a chat request to the model containing Tools definitions.
2. **Model Judgment**: The model determines whether tools need to be invoked based on the conversation content
3. **Return Tool Calls**: If invocation is required, the model returns the function name and parameters to be called.
4. **Execute Function**: Developers perform the actual function call based on the returned information.
5. **Return Result**: Send the function execution result as a new message to the model
6. **Continue Conversation**: The model generates the final reply based on the function results.

##OpenAI Tool Call Example

Below is an example using OpenAI to demonstrate how to use the Tool Call feature.

###1. Define Tool

First, create the Tool definition. In this example, we define a function `get_delivery_date` that retrieves the delivery time of a courier package.

<!-- Need image: Showing the creation of the FAIChatPlus_ChatRequestTool node, setting Type=Function, Name="get_current_weather", Description="Get the current weather in a given location" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_1.png)

###2. Defining Tool Parameters

Add Properties (parameters) to the Tool. In this example, add an `order_id` parameter with the type as `string` and set it as required.

<!-- Image required: Display the creation of a FAIChatPlus_ChatRequestToolProperty node, setting Name="location", Description="The city and state, e.g. San Francisco, CA", Type="string", Required=true, and connect it to the Tool's Properties field via Make Array -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_2.png)

###3. Configure Options

Create the `OpenAI Chat Request Options` node, configure the API Key and Model, and connect the Tools array to the Options.

**Image needed:** Showing the creation of an OpenAI Chat Request Options node, setting ApiKey and Model="gpt-4o-mini", and connecting the above Tool to the Tools field via Make Array.
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_3.png)

###4. Create Messages

Create a user message inquiring about courier package-related issues.

<!-- Image needed: Illustrate the creation of a Messages array, adding a User Message with Content set to "What's the weather like in Boston today?" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_4.png)

###5. Send the request and handle the Tool Call

Create the `Send OpenAI Chat Request In World` node and bind the `On Message Finished` event. In the event callback, retrieve the ToolCalls array from the Payload.

When the model decides to invoke a tool, the ToolCalls array is not empty. Traverse the array to retrieve information about each Tool Call:

* **Id**: Unique identifier for Tool Call
* **FunctionName**: The name of the function to be invoked
* **FunctionArguments**: Function parameters (in JSON string format)

<!-- Image needed: Display the complete request sending blueprint, create the Send OpenAI Chat Request In World node, connect Options and Messages, bind the On Message Finished event, and use the Break node in the event callback to retrieve ToolCalls from the Payload -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_5.png)

<!-- Image needed: A blueprint demonstrating iteration over the ToolCalls array, using a For Each Loop to traverse each element, utilizing a Break node to retrieve the Id, FunctionName, FunctionArguments fields, and printing them out. -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_6.png) -->

###6. Execute the function and return the result

Execute the corresponding function logic based on FunctionName (in this example, simulating the retrieval of a package delivery time), then return the result as a ToolCallResult-type message to the model.

Create a new Message, you need to set:

* **Role**: Set to `Tool`
* **Content**: The result of function execution
* **ToolCallResults**: Add a `FAIChatPlus_ChatRequestToolCallResult`, setting the Id (using the previous Tool Call Id), FunctionName, and FunctionResult.

<!-- Image needed: Display the blueprint for creating a Tool role message, create a new Message, Role=Tool, set Content to simulated weather data such as '{"temperature": "22", "unit": "celsius", "description": "Sunny"}', and add corresponding result information in ToolCallResults -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_7.png)

###7. Continue the conversation

Add the message containing the ToolCallResult to the conversation history and send the request again. The model will generate the final natural language response based on the returned function results.

<!-- Image needed: Show the complete blueprint for the second request, combining the original User Message, the Assistant Message returned by the model (including ToolCalls), and the Tool Result Message into a new Messages array, then calling Send OpenAI Chat Request In World again. -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_8.png)

<!-- ### 9. Complete Blueprint -->

The complete Tool Call blueprint looks like this:

<!-- Image required: Display the complete blueprint of the Tool Call process flow, encompassing Tool definition, the first request, Tool Call handling, and the second request in an end-to-end sequence -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_9.png) -->

### 10. Execution Results

Running the blueprint shows that the model returns natural language responses containing weather information.

<!-- Image needed: Screenshot of the execution result, displaying the model's final response on the screen, similar to "The current weather in Boston is sunny with a temperature of 22°C." -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_10.png) -->

##Advanced Usage

###Multiple Tools

You can define multiple Tools simultaneously, and the model will select which function or functions to invoke as needed.

<!-- Image needed: Shows a blueprint defining multiple Tools, such as defining both get_current_weather and get_stock_price Tools, combined into a Tools array via Make Array -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_multi_tools.png)

###Complex Parameter Types

Tool parameters support various types, and more complex parameter definitions such as enumeration types can be added through the `ExtraJsonString` or `ExtraJsonObject` fields. For example:

```json
{"enum": ["Beijing", "HongKong"]}
```

<!-- Need a picture: Showcase the blueprint for setting enumeration parameters using ExtraJsonString, filling in '{"enum": ["celsius", "fahrenheit"]}' within the ExtraJsonString field of the Property node -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_extra_json.png)

###Other Platforms

The usage of Tool Call in Claude, Gemini, Ollama, and CllamaServer is similar to OpenAI—simply replace the corresponding Request and Options nodes. The core data structures (`FAIChatPlus_ChatRequestTool`, `FAIChatPlus_ChatResponseToolCall`, etc.) are universal across these platforms.

--8<-- "footer_en.md"


> This post is translated using ChatGPT. Please provide [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Points out any omissions therein. 
