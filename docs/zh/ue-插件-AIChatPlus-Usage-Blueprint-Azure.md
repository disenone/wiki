---
layout: post
title: Azure
tags: [dev, game, UE, UnreanEngine, UE4, UE5, Editor, Editor Plus, Editor Plugin, AI Chat, Chatbot, Image Generation, OpenAI, Azure, Claude, Gemini, Ollama]
description: Azure
---
<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Azure" />

# 蓝图篇 - Azure

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_all.png)

Azure 的用法跟 OpenAI 也很相似，所以这里简略介绍

## 文本聊天

创建 "Azure Chat Options" 节点，设置参数 "Deployment Name", "Base Url", "Api Key"

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_chat_1.png)

创建 "Messages" 相关节点，并连接 "Azure Chat Request"，点击运行，即可看到屏幕上打印 Azure 返回的聊天信息。如图

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

## 创建图片

创建 "Azure Image Options" 节点，设置参数 "Deployment Name", "Base Url", "Api Key"

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_image_1.png)

设置好 "Azure Image Request" 等节点，点击运行，即可看到屏幕上打印 Azure 返回的聊天信息。如图

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

根据上面蓝图的设置，图片会保存在路径 D:\Dwnloads\butterfly.png

--8<-- "footer.md"
