---
layout: post
title: 版本紀錄
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

## v1.8.0 - 2025.11.03

更新 llama.cpp 至版本 b6792

## v1.7.0 - 2025.07.06

升級 llama.cpp 到版本 b5536

支援 UE5.6

Android 發布 shipping 會 crash，禁用掉 llama.cpp

## v1.6.2 - 2025.03.17

###新功能

Cllama 增加 KeepContext 參數，預設為 false，Context 在 Chat 結束後自動銷毀。

Cllama 增加 KeepAlive 參數，可以減少 model 重複讀取

## v1.6.1 - 2025.03.07

### Bug Fix

OpenAI Image Chat 的藍圖支援輸入圖片。

編輯工具 Cllama mmproj 模型允許空

## v1.6.0 - 2025.03.02

###新功能

將 llama.cpp 升級至 b4604 版本

Cllama 支援 GPU 後端: cuda 和 metal

聊天工具 Cllama 支援 GPU 使用

支援讀取打包在 Pak 中的模型檔案

### Bug Fix

修復 Cllama 在推理時重新加載會崩潰的問題

修復 iOS 編譯錯誤

## v1.5.1 - 2025.01.30

###新功能

僅允許雙子座發送音频。

優化獲取 PCMData 的方法，生成 B64 的時候再解壓縮音頻數據

請求添加兩個回調函數 OnMessageFinished 和 OnImagesFinished

優化 Gemini Method，自動根據 bStream 獲取 Method

新增一些藍圖函數，便於將 Wrapper 轉換為實際類型，並獲取回應訊息和錯誤。

### Bug Fix

修復請求完成時多次調用的問題

## v1.5.0 - 2025.01.29

###新功能

支援傳送音訊給 Gemini

編輯器工具支援傳送音頻和錄音。

### Bug Fix

修復 Session copy 失敗的 bug

## v1.4.1 - 2025.01.04

###問題修復

聊天工具支援只發圖片不發訊息。

修復 OpenAI 介面傳送圖片問題失敗文件。

修復 OpanAI、Azure 聊天工具設定遺漏了參數 Quality、Style、ApiVersion 問題=

## v1.4.0 - 2024.12.30

###新功能

（實驗性功能）Cllama（llama.cpp）支持多模態模型，可以處理圖片

所有藍圖類型參數都添加了詳細提示。

## v1.3.4 - 2024.12.05

###新功能

* OpenAI 支援影像 API

###問題修復

修復OpenAI stream=false時的錯誤

## v1.3.3 - 2024.11.25

###新功能

支援 UE-5.5

###問題修復

修復部分藍圖無效問題

## v1.3.2 - 2024.10.10

###問題修復

修復手動停止 request 的時候 cllama 崩潰

修復商城下載版本 win 打包找不到 ggml.dll llama.dll 檔案的問題

* 在建立請求時，檢查是否在遊戲執行緒中，CreateRequest check in game thread

## v1.3.1 - 2024.9.30

###新功能

新增一個 SystemTemplateViewer，可查看和使用數百個系統設定模板。

###問題修復

修復自商城下載的插件，llama.cpp 找不到連結庫

修復 LLAMACpp 路徑過長問題

修復 Windows 打包後的連結 llama.dll 錯誤

修復 iOS/Android 讀取檔案路徑問題

修復 Cllame 設置名字錯誤

## v1.3.0 - 2024.9.23

###重大新功能

集成了 llama.cpp 檔案，支援本機離線執行大型模型。

## v1.2.0 - 2024.08.20

###新功能

支持 OpenAI Image Edit/Image Variation

支援 Ollama API，可自動獲取 Ollama 支援的模型列表。

## v1.1.0 - 2024.08.07

###新功能

支持藍圖

## v1.0.0 - 2024.08.05

###新功能

基礎完整功能

支持 OpenAI，Azure，Claude，Gemini

* 具備自家優良編輯器的聊天工具

--8<-- "footer_tc.md"


> 此貼文是由 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
