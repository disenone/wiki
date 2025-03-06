---
layout: post
title: DeepSeek
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
description: DeepSeek
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - DeepSeek" />

#藍圖篇 - DeepSeek

由於 DeepSeek 兼容了 OpenAI 的 API 接口格式，所以我們可以輕鬆地使用 OpenAI 相關的節點來訪問 DeepSeek，只需將相關的 URL 修改成 DeepSeek 的 URL 即可。

#文字聊天

建立 "OpenAI Chat Options" 節點，設置好 Model、Url、Api Key 參數。

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/deepseek_chat_1.png)

其他設置與 OpenAI 相同，完整的藍圖看起來像這樣：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

運行後，您可以在屏幕上看到 DeepSeek 的返回結果：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

--8<-- "footer_tc.md"


> 此篇文章是由 ChatGPT 翻譯而成的，請留言在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
