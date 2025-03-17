---
layout: post
title: 版本日誌
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
description: 版本日誌
---

<meta property="og:title" content="UE 插件 AIChatPlus 版本日志" />

#以下是 UE 插件 AIChatPlus 的版本紀錄。

## v1.6.2 - 2025.03.17

###新功能

將 Cllama 增加 KeepContext 參數，預設為 false，Context 在 Chat 結束後自動銷毀。

Cllama增加KeepAlive參數，可以減少model重複讀取。

## v1.6.1 - 2025.03.07

### Bug Fix

OpenAI Image Chat 藍圖支援輸入圖片

* 編輯器工具 Cllama mmproj 模型允許空

## v1.6.0 - 2025.03.02

###新功能

將 llama.cpp 升級至 b4604 版本

Cllama支援GPU後端：cuda和metal

聊天工具 Cllama 支援 GPU 使用

支援讀取打包 Pak 中的模型檔案

### Bug Fix

修復 Cllama 在推理時重新加載時崩潰的問題

修復 iOS 編譯錯誤

## v1.5.1 - 2025.01.30

###新功能

只允許 Gemini 發音頻

優化獲取 PCMData 的方法，生成 B64 的時候再解壓縮音頻數據

要求增加兩個回調 OnMessageFinished 和 OnImagesFinished。

優化 Gemini 方法，自動根據 bStream 獲取 Method

增加一些藍圖函數，方便轉換 Wrapper 到實際類型，並且獲取 Response Message 和 Error。

### Bug Fix

修復 Request Finish 多次呼叫問題

## v1.5.0 - 2025.01.29

###新功能

支持給Gemini發送音頻。

編輯器工具支援傳送音訊和錄音。

### Bug Fix

修復 Session copy 失敗的 bug

## v1.4.1 - 2025.01.04

###問題修復

聊天工具支援僅傳送圖片而不發送訊息。

修復 OpenAI 介面發送圖片問題失敗文件圖。

修復 OpanAI、Azure 聊天工具設置遺漏了參數 Quality、Style、ApiVersion 問題。

## v1.4.0 - 2024.12.30

###新功能

（實驗性功能）Cllama（llama.cpp）支持多模態模型，可以處理圖片

所有的藍圖類型參數都加上了詳細提示。

## v1.3.4 - 2024.12.05

###新功能

OpenAI 支援視覺 API。

###問題修復

修復 OpenAI stream=false 時的錯誤

## v1.3.3 - 2024.11.25

###新功能

支援 UE-5.5

###問題修復

修復部分藍圖不生效問題

## v1.3.2 - 2024.10.10

###問題修復

修復手動停止 request 的時候 cllama 崩潰

修復商城下載版本 win 打包找不到 ggml.dll llama.dll 檔案的問題

在创建请求时检查是否在游戏线程中。

## v1.3.1 - 2024.9.30

###新功能

新增一個 SystemTemplateViewer，可查看和使用數百個系統設定模板。

###問題修復

修復從商城下載的插件，llama.cpp 找不到鏈接庫。

修復 LLAMACpp 路徑過長問題

修復 Windows 打包後的連結 llama.dll 錯誤

修復 iOS / Android 讀取文件路徑問題

修復 Cllame 設置名字錯誤

## v1.3.0 - 2024.9.23

###重要的新功能

整合了 llama.cpp，支援本地離線執行大型模型。

## v1.2.0 - 2024.08.20

###新功能

支援 OpenAI 圖片編輯/圖片變化

支援Ollama API，可自動獲取Ollama支援的模型清單。

## v1.1.0 - 2024.08.07

###新功能

支持藍圖

## v1.0.0 - 2024.08.05

###新功能

基礎完整功能

支持 OpenAI，Azure，Claude，Gemini

* 具備完善編輯功能的聊天工具

--8<-- "footer_tc.md"


> 此帖文係由 ChatGPT 翻譯嘅，如果有任何[**反饋**](https://github.com/disenone/wiki_blog/issues/new)請指出任何遺漏之處。 
