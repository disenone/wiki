---
layout: post
title: 打包
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
description: 打包
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - Package 篇 - Get Started" />

#打包

##插件打包

在 Unreal 打包的過程中，將自動打包所需插件的動態庫文件，只需啟用插件即可。

對於 Windows 而言，打包程序會自動將 llama.cpp 和相關的 CUDA dll 檔案都放入打包後的資料夾中。對於其他平台 Android / Mac / IOS 也是同樣的。

在已經打包好的開發版本遊戲中，執行指令 "AIChatPlus.PrintCllamaInfo"，檢視目前的 Cllama 環境狀態，確認其運作是否正常，以及是否支援 GPU 後端。

##模型打包

將加入專案的模型檔案放置在 Content/LLAMA 目錄下，您可以在打包時設定包含此目錄：

打開「專案設置」，選擇「打包」頁籤，或直接搜尋「資產套件」，找到「要打包的其他非資產目錄」設置，新增目錄「Content/LLAMA」即可：

![](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_6.png)

添加目录後，Unreal 在打包的時候就會自動將該目錄中的所有檔案一併打包。


##讀取打包後的離線模型文件

一般情況下，Uneal 會將專案檔案打包成 .Pak 檔案。若此時將 .Pak 檔案的路徑傳遞給 Cllam 離線模型，執行將失敗，因為 llama.cpp 無法直接讀取打包後的模型檔案。

因此需要先將 .Pak 中的模型文件複製出來到文件系統中，插件提供了一個方便的函數可以直接將 .Pak 的模型文件複製出來，並返回複製後的文件路徑，讓 Cllama 可以方便讀取。

藍圖節點是"Cllama Prepare ModelFile In Pak"：自動將 Pak 中的模型文件複製到檔案系統中

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

C++ 代碼函數是：

```
#include <Cllama/AIChatPlusCllama_Util.h>

auto ModelPath = FAIChatPlusCllama_Util::PrepareModelFileInPak(InContentPath);
```

--8<-- "footer_tc.md"


> 此貼文是用ChatGPT翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
