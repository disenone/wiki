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

#Blueprint Chapter - CllamaServer (llama.cpp server)

<!-- Image required: An overview of all blueprint nodes related to CllamaServer, similar to xxx_all.png in other documentation -->
![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_all.png)

##Overview

CllamaServer is implemented based on the Server mode of llama.cpp. It allows you to locally spin up a server compatible with the OpenAI API, offering support for multiple features:

* **Local Inference Service**: Launch an AI inference server locally without relying on external APIs.
* **OpenAI API Compatible**: Supports OpenAI-compatible API formats for easier migration and integration
* **Multi-session Support**: Supports multiple concurrent requests
* **Tool Calling**: Supports function calling capabilities
* **Speech-to-Text**: Supports Speech-to-Text functionality
* **Visual Management**: Built-in Server management interface in the editor

Differences from Cllama:
* **Cllama**: Directly loads the model within the process for inference, capable of handling only one request at a time.
* **CllamaServer**: Launches a standalone HTTP server capable of handling multiple concurrent requests, with API compatibility in OpenAI format.

##Preparation work

Since it's running locally, you'll need to prepare the offline model files first, such as downloading [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Place the model in a certain folder, for example, under the game project directory `Content/LLAMA`.

##Create CllamaServer

###Creating a Server Using Blueprints

Right-click in the blueprint to create the node `Create Cllama Server In World`

<!-- Image needed: Screenshot showing right-click search "Create Cllama Server" and node creation in the blueprint -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_1.png)

###Configure Server Parameters

Create the `Cllama Server Param` node and configure essential parameters:

* **Model**: Path to the model file (required)
* **Port**: Server port (0 indicates automatic allocation)
* **Host**: Listening address, defaults to `127.0.0.1`
* **NGpuLayers**: Number of GPU layers (-1 means to use all GPUs)

<!-- Need image: Screenshot demonstrating the creation of FAIChatPlus_CllamaServerParam node, setting parameters such as Model path, Port, NGpuLayers, etc. -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_2.png)

###Bind callback events

Binding callback events for Server:

* **On Started**: Triggered when the server starts successfully
* **On Stopped**: Triggered when the server stops
* **On Failed**: Triggered when Server startup fails

<!-- Need image: Blueprint showcasing the binding of OnStartedListeners, OnStoppedListeners, OnFailedListeners events -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_3.png)

###Complete Creation Blueprint

The complete Server creation blueprint is as follows:

<!-- Image needed: Display the complete Server creation blueprint overview, including parameter settings, node creation, callback binding -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_4.png)

After running the blueprint, the Server will trigger the `On Started` event upon successful startup.

<!-- Image needed: Showing the running result after Server successfully starts, displaying the startup success log or screen output -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_5.png) -->

##Detailed Explanation of Server Parameters

The `FAIChatPlus_CllamaServerParam` struct contains the following parameters:

###Common Parameters

| Parameter | Type | Default Value | Description |
|-----|------|-------|------|
| Model | FString | - | Model file path (required) |
| Port | int32 | 0 | Listening port, 0 indicates automatic allocation |
| Host | FString | 127.0.0.1 | Listening Address |
| NGpuLayers | int32 | -1 | Number of GPU layers, -1 means all |
| bUseJinja | bool | false | Use Jinja template |
| MMProj | FString | - | Multimodal projection file path |
| Temperature | float | 0.8 | Sampling temperature |

###Reasoning Argument

| Parameter | Type | Default Value | Description |
|-----|------|-------|------|
| CtxSize | int32 | 4096 | Context Size |
| NPredict | int32 | -1 | Number of tokens to predict, -1 denotes unlimited |
| Threads | int32 | -1 | CPU thread count, -1 denotes automatic |
| BatchSize | int32 | 2048 | Batch size |

###Sampling Parameters

| Parameter | Type | Default Value | Description |
|-----|------|-------|------|
| TopK | int32 | 40 | Top-K sampling |
| TopP | float | 0.9 | Top-P Sampling |
| MinP | float | 0.1 | Min-P sampling |
| RepeatPenalty | float | 1.0 | Repetition penalty |

###Server Parameters

| Parameter | Type | Default Value | Description |
|-----|------|-------|------|
| ApiKey | FString | - | API Key (optional) |
| Timeout | int32 | 600 | Timeout duration (seconds) |
| Parallel | int32 | 1 | Number of parallel sequences |
| bNoWebUI | bool | false | Disable Web UI |
| bVerbose | bool | false | Verbose Logging |

##Chat using CllamaServer

###Create Chat Request

Once the server starts successfully, you can use the `Send CllamaServer Chat Request` node to send chat requests.

<!-- Image needed: A screenshot showing how to right-click and search for "CllamaServer Chat Request" in the blueprint to create a node. -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_1.png)

###Configure Chat Options

Create a `CllamaServer Chat Request Options` node and set the BaseUrl to the Server address.

You can obtain Server information through the `Get Server Info By ID` node.

<!-- Image needed: Demonstrating the creation of an FAIChatPlus_CllamaServerChatRequestOptions node, using Get Http Address to retrieve the Server address and setting it to BaseUrl in Blueprints -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_2.png)

###Create Messages

Create Messages array, add System Message and User Message.

<!-- Image needed: Shows the blueprint for creating a Messages array, including System Message (setting assistant role) and User Message (user question). -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_3.png)

###Bind callback handlers to process responses

Bind the `On Message` or `On Message Finished` events to receive model responses.

<!-- Image needed: Blueprint demonstrating the binding of OnMessageListeners events and printing messages to the screen within the callback -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_4.png)

###Complete Chat Blueprint

The complete chat blueprint is as follows:

<!-- Need image: Display the complete overview of the chat blueprint, including the entire process of creating a Server, waiting for startup, sending chat requests, and handling responses. -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_5.png)

###Execution Result

Run the blueprint, and you'll see the message returned by the model displayed on the screen.

<!-- Image required: Showing a chat operation result with the model's response displayed on the screen -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_6.png) -->

##Server Management

###Get Server Information

Use the `Get Server Info` node to fetch detailed information about the Server.

<!-- Image needed: Showcase the blueprint of using a Get Server Info node to retrieve FAIChatPlus_CllamaServerInfo and Break to display each field -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_info_1.png)

Server Info includes the following information:
* **ServerID**: Unique server identifier
* **Host**: Listening Address
* **Port**: Listening Port
* **Address**: Complete address (host:port)
* **HttpAddress**: HTTP Address (http://host:port)
* **bIsRunning**: Whether it is running
* **Param**: Server parameter

###Stop Server

Use the `Stop Server By ID` node to stop the current Server.

<!-- Requires image: Blueprint showcasing the calling of Stop Cllama Server node -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_stop_1.png)

###Static Management Functions

AIChatPlus provides a set of static functions for managing all Servers.

| Function | Description |
|-----|------|
| `Is Server Valid (Static)` | Check if the Server is Valid |
| `Is Server Running (Static)` | Check if the server is running |
| `Stop Server By ID` | Stop the specified Server by ID |
| `Stop All Servers` | Stop All Servers |
| `Get Server Info By ID` | Get Server Info By ID |
| `Get All Server IDs` | Retrieve All Server IDs |
| `Get Server By ID` | Retrieve Server instance by ID |

<!-- Image needed: Example blueprint showing the usage of static management functions like GetAllServerIDs and StopAllServers -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_static_1.png)

##Multimodal Support

CllamaServer supports multimodal models (such as Moondream, Qwen2-VL, etc.).

###Configure Multimodal Parameters

Set `MMProj` (multimodal projection file path) in the Server parameters:

<!-- Requires image: Blueprint displaying the paths for setting Model and MMProj in Server Param -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_1.png)

###Send image message

Add images in Messages:

<!-- Image needed: Demonstrating reading an image file, creating a Message containing the image, and sending a request via CllamaServer's blueprint -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_2.png)

### Execution Results

<!-- Image needed: Displaying the result of image recognition, with the screen showing the model's description of the picture's content -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_3.png) -->

## Tool Calling

CllamaServer supports Tool Calling (function calling) functionality, with usage similar to OpenAI.

For detailed usage, please refer to [Tool Call](ue-插件-AIChatPlus-Usage-Blueprint-ToolCall.md)Document.

When using CllamaServer for Tool Call, the following are required:
1. Set `bUseJinja = true` in the Server parameters
2. Define tools in the Tools field of Chat Options

<!-- An image is required: displaying the complete blueprint of CllamaServer Tool Call, including the setup with bUseJinja=true and Tools definitions -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_tool_1.png)

##Editor Server Management

AIChatPlus offers a visual CllamaServer management interface within the editor tool, simplifying the creation, monitoring, and administration of multiple Servers.

Open the editor tool by navigating to: `Tools -> AIChatPlus -> AIChat`, then open the Cllama Server Manager tab.

<!-- Need image: Screenshot of the CllamaServer management interface in the editor, showing Server list, Create button, status information, etc. -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_editor_1.png)

In the editor, you can:
* Create a new Server
* Check the status of the running Server
* Stop the specified Server
* Configure Server Parameters
* Server configurations are automatically saved.

<!-- Image needed: Interface of creating a new Server in the editor, showcasing the parameter configuration panel -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_editor_2.png)

##Relationship to Other APIs

Since CllamaServer is compatible with the OpenAI API format, you can also use OpenAI’s Chat Request node to communicate with CllamaServer—just set the `BaseUrl` to the address of CllamaServer.

<!-- Requires image: Showcasing a blueprint example of using the OpenAI Chat Request node with the BaseUrl set to the CllamaServer address -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_openai_1.png) -->

--8<-- "footer_en.md"


> This post was translated using ChatGPT; please provide feedback at [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions therein. 
