---
layout: post
title: Claude
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
description: Claude
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Claude" />

#藍圖篇 - Claude

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/claude_all.png)

##文本聊天

建立「選項」節點，設定參數「模型」、「API 金鑰」、「Anthropic 版本」

![](assets/img/2024-ue-aichatplus/usage/blueprint/claude_chat_1.png)

連接 "Claude Request" 節點和 "Messages" 相關節點，點擊運行，即可看到屏幕上打印 Claude 返回的聊天信息。如圖。

![](assets/img/2024-ue-aichatplus/usage/blueprint/claude_chat_2.png)

##圖片轉換文字

Claude 同樣支持 Vision 功能

在藍圖中右鍵建立一個節點 `發送克勞德聊天請求`

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

建立 Options 節點，並設置`Stream=true, Api Key="你從 Clude 取得的 API 金鑰", Max Output Tokens=1024`

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

建立 Messages，從檔案建立 Texture2D，然後由 Texture2D 創建 AIChatPlusTexture，將 AIChatPlusTexture 加入到 Message 中。

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

將事件監聽並將資訊輸出到遊戲畫面上

完整的藍圖看起來是這樣的，運行藍圖，即可看到遊戲畫面在打印大模型返回的訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)


--8<-- "footer_tc.md"


> 這篇文章是由 ChatGPT 翻譯的，如有任何[**反饋**](https://github.com/disenone/wiki_blog/issues/new)請指出任何遺漏之處。 
