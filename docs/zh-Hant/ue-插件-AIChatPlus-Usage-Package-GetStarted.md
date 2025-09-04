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

#包裝

##插件打包

在 Unreal 打包的過程中，系統會自動將插件所需的動態庫檔案一併打包好，只需啟用插件即可。

例如對於 Windows，打包程序會自動將 llama.cpp 和 CUDA 相關的 dll 檔案都放入打包後的目錄中。而對於其他平台 Android / Mac / IOS 也是同樣的方式。

你可以在打包後的 Development 版本遊戲裡執行指令 "AIChatPlus.PrintCllamaInfo"，查看目前的 Cllama 環境狀態，確認狀態是否正常，以及是否支援 GPU 後端。

##模型打包

假設加入專案的模型文件放在了目錄 Content/LLAMA 下面，那麼可以設定打包的時候包含此目錄：

打開 "專案設定"，選擇封裝頁籤，或直接搜尋 " asset package"，找到 "要封裝的其他非資產目錄" 設定，加入目錄 Content/LLAMA 即可：

![](assets/img/2024-ue-aichatplus/usage/package/getstarted_1.png)

在添加目錄後，Unreal 在打包的時候就會自動將目錄中的所有檔案一併打包。

##讀取打包後的離線模型文件

通常 Uneal 會將專案檔案打包成 .Pak 檔案，若將 .Pak 中的檔案路徑傳遞給 Cllam 離線模型，將會執行失敗，因為 llama.cpp 無法直接讀取 .Pak 中打包後的模型檔案。

因此需要先將 .Pak 中的模型文件複製到文件系統中，插件提供了一個方便的函數，可以直接將 .Pak 的模型文件複製出來並返回複製後的文件路徑，以方便Cllama進行讀取。

藍圖節點是 "Cllama Prepare ModelFile In Pak": 自動將 Pak 中的模型文件複製到檔案系統中。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

C++ code function is:

```
#include <Cllama/AIChatPlusCllama_Util.h>

auto ModelPath = FAIChatPlusCllama_Util::PrepareModelFileInPak(InContentPath);
```

--8<-- "footer_tc.md"


> 此貼文是由 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)請指出任何遺漏之處。 
