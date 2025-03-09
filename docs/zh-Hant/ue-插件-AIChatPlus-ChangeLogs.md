---
layout: post
title: 版本記錄
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

#UE 插件 AIChatPlus 版本日誌

## v1.6.1 - 2025.03.07

### Bug Fix

OpenAI Image Chat 藍圖支援圖片輸入

* 編輯工具 Cllama mmproj 模型允許空

## v1.6.0 - 2025.03.02

###新功能

將 llama.cpp 升級到 b4604 版本

Cllama支援GPU後端：cuda和metal

聊天工具 Cllama 支援 GPU。

支持讀取打包 Pak 中的模型文件

### Bug Fix

修復 Cllama 在推理時重新加載會崩潰的問題

修復 iOS 編譯錯誤

## v1.5.1 - 2025.01.30

###新功能

僅允許 Gemini 發送音訊。

優化取得 PCMData 的方式，生成 B64 時再解壓縮音頻數據

請求增加兩個回調 OnMessageFinished 和 OnImagesFinished

優化 Gemini Method，自動根據 bStream 獲取 Method

新增一些藍圖函數，以便將 Wrapper 轉換為實際類型，並獲取響應消息和錯誤。

### Bug Fix

修復 Request Finish 多次調用問題

## v1.5.0 - 2025.01.29

###新功能

支持給 Gemini 發音頻

編輯器工具支援傳送音訊和錄音。

### Bug Fix

修復 Session 複製失敗的 bug

## v1.4.1 - 2025.01.04

###問題修復

聊天工具支援僅發送圖片而不發送訊息。

修復 OpenAI 介面發送圖片問題失敗文件圖

修復了 OpanAI、Azure 聊天工具設定中遺漏了 Quality、Style、ApiVersion 參數的問題。

## v1.4.0 - 2024.12.30

###新功能

（實驗性功能）Cllama(llama.cpp) 支援多模態模型，能處理圖片

所有的藍圖類型參數都加上了詳細提示。

## v1.3.4 - 2024.12.05

###新功能

OpenAI supports vision API.

###問題修復

修復 OpenAI stream=false 時的錯誤

## v1.3.3 - 2024.11.25

###新功能

支援 UE-5.5

###問題修復

修復部分藍圖不生效問題

## v1.3.2 - 2024.10.10

###問題修復

修復手動停止 request 時 cllama 崩潰

修復商城下載版本 win 打包找不到 ggml.dll llama.dll 文件的問題。

當建立請求時，檢查是否在遊戲執行緒中。

## v1.3.1 - 2024.9.30

###新功能

新增一個 SystemTemplateViewer，可查看和使用數百個系統設置範本。

###問題修復

修復從商城下載的插件，llama.cpp 找不到鏈接庫

修復 LLAMACpp 路徑過長問題

修復 Windows 打包後的連結 llama.dll 錯誤

修復 iOS/Android 讀取檔案路徑問題

修復 Cllame 設置名稱錯誤

## v1.3.0 - 2024.9.23

###重要的新功能

整合了 llama.cpp，支援本地離線執行大型模型。

## v1.2.0 - 2024.08.20

###新功能

支持 OpenAI 圖像編輯/圖像變化

支持 Ollama API，並可自動獲取 Ollama 支持的模型列表。

## v1.1.0 - 2024.08.07

###新增功能

支持蓝图

## v1.0.0 - 2024.08.05

###新功能

基礎完整功能

支持 OpenAI，Azure，Claude，Gemini

具備全功能編輯器的聊天工具

--8<-- "footer_tc.md"


> 這篇文字是使用 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)請指出任何遺漏之處。 
