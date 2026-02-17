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

#UE 插件 AIChatPlus 版本更新記錄

## v2.0.0 - 2026.02.14

* **Tool Calling 多平台支援**：新增 OpenAI、Claude、Gemini、Ollama、CllamaServer 五大平台的工具調用／函式呼叫功能
* **Cllama 伺服器整合**：全面支援本地 llama.cpp 伺服器，涵蓋建立、管理、語音轉文字功能，並提供編輯器可視化管理介面
* **JSON 藍圖資料庫**：新增 JsonObject/JsonArray 藍圖操作類別，支援 JSON 與 USTRUCT 互相轉換
* **OpenAI 音訊**：支援 OpenAI 音訊的輸入與輸出，編輯器可預覽音訊回應

## v1.8.0 - 2025.11.03

* 升級 llama.cpp b6792

## v1.7.0 - 2025.07.06

* 升級 llama.cpp b5536

* 支援 UE5.6

* Android版本發布時會當機，需停用llama.cpp

## v1.6.2 - 2025.03.17

###新功能

* Cllama 新增了KeepContext參數，預設為false，當Chat結束時Context會自動清除

* Cllama 新增了 KeepAlive 參數，能有效降低模型重複載入的頻率

## v1.6.1 - 2025.03.07

### Bug Fix

* OpenAI 圖片聊天 藍圖支援圖片輸入

* 編輯工具 Cllama mmproj 模型允許空

## v1.6.0 - 2025.03.02

###新功能

* llama.cpp 升級至 b4604 版本

* Cllama 支援 GPU 後端：cuda 與 metal

* 聊天工具 Cllama 支援使用 GPU

* 支援讀取打包 Pak 中的模型檔案

### Bug Fix

* 修正 Cllama 在推理時重新載入會崩潰的問題

* 修復 iOS 編譯報錯

## v1.5.1 - 2025.01.30

###新功能

* 只允許 Gemini 發送音頻

* 優化取得 PCMData 的方法，於生成 B64 時再解壓縮音訊資料

* 請求新增兩個回調函數：OnMessageFinished 和 OnImagesFinished

* 最佳化 Gemini Method，自動根據 bStream 獲取 Method

* 新增一些藍圖函數，便於將 Wrapper 轉換為實際類型，以及獲取 Response Message 和 Error

### Bug Fix

* 修復 Request Finish 多次呼叫問題

## v1.5.0 - 2025.01.29

###新功能

* 支援向 Gemini 發送音頻功能

* 編輯器工具支援傳送音訊和錄音

### Bug Fix

* 修復 Session 複製失敗的錯誤

## v1.4.1 - 2025.01.04

###問題修復

* 聊天工具支援僅發送圖片不發送訊息

* 修復 OpenAI 介面傳送圖片問題失敗圖文

* 修復 OpanAI、Azure 聊天工具設置遺漏了參數 Quality、Style、ApiVersion 問題=

## v1.4.0 - 2024.12.30

###新功能

* （實驗性功能）Cllama(llama.cpp) 支援多模態模型，能夠處理圖片

* 所有的藍圖類型參數都加上了詳細提示

## v1.3.4 - 2024.12.05

###新功能

* OpenAI 支援視覺API

###問題修復

* 修復 OpenAI stream=false 時的錯誤

## v1.3.3 - 2024.11.25

###新功能

* 支援 UE-5.5

###問題修復

* 修復部分藍圖無效的問題

## v1.3.2 - 2024.10.10

###問題修復

* 修復 手動停止請求時 cllama 崩潰

* 修復商城下載版本 win 打包時找不到 ggml.dll llama.dll 檔案的問題

* 創建請求時檢查是否在 GameThread 中，CreateRequest 檢查遊戲執行緒

## v1.3.1 - 2024.9.30

###新功能

* 增加一個 SystemTemplateViewer，可以查看和使用數百個 system 設定模版

###問題修復

* 修復從商城下載的外掛程式，llama.cpp 找不到連結庫

* 修正 LLAMACpp 路徑過長的問題

* 修復 Windows 打包後連結 llama.dll 的錯誤

* 修復 iOS/Android 讀取檔案路徑問題

* 修復 Cllame 設定名稱錯誤

## v1.3.0 - 2024.9.23

###重大新功能

* 整合了 llama.cpp，支援本地離線執行大型模型

## v1.2.0 - 2024.08.20

###新功能

* 支援 OpenAI 圖片編輯/圖片變體

* 支援 Ollama API，支援自動取得 Ollama 所支援的模型列表

## v1.1.0 - 2024.08.07

###新功能

* 支援藍圖

## v1.0.0 - 2024.08.05

###新功能

* 基礎完整功能

* 支援 OpenAI、Azure、Claude、Gemini

* 自帶功能完善的編輯器聊天工具

--8<-- "footer_tc.md"


> 此貼文是使用 ChatGPT 翻譯的，請在[**回饋**](https://github.com/disenone/wiki_blog/issues/new)標註出任何遺漏之處。 
