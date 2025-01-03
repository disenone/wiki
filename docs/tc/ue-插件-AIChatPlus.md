---
layout: post
title: UE 插件 AIChatPlus 說明文件
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
description: UE 插件 AIChatPlus 說明文件
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE 插件 AIChatPlus 說明文件

##公共倉庫

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##外掛取得

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##插件簡介

This plugin supports UE5.2+.

UE.AIChatPlus 是一個 UnrealEngine 外掛程式，實現了與各種 GPT AI 聊天服務進行通訊，目前支持的服務有 OpenAI (ChatGPT, DALL-E)，Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, llama.cpp 本地離線。未來還會繼續支持更多服務提供商。它的實現基於異步 REST 請求，性能高效，方便 UE 開發人員接入這些 AI 聊天服務。

同時 UE.AIChatPlus 還包含了一個編輯器工具，可以直接在編輯器中使用這些 AI 聊天服務，生成文本和圖像，分析圖像等。

##Instructions for use.

###編輯器聊天工具

菜單列 Tools -> AIChatPlus -> AIChat 可以開啟插件提供的編輯器聊天工具。

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


工具支援文字生成、文字聊天、圖像生成，以及圖像分析。

工具的界面大致為：

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####主要功能

離線大模型：整合了 llama.cpp 庫，支持本地離線執行大模型

進行文字聊天：點擊左下角的 `New Chat` 按鈕，建立新的文字聊天對話。

圖像生成：點擊左下角的 `New Image Chat` 按鈕，建立新的圖像生成會話。

圖像分析：`New Chat` 的部分聊天服務支援發送圖像，例如 Claude, Google Gemini。點擊輸入框上方的 🖼️ 或 🎨 按鈕即可載入需要發送的圖像。

支持藍圖（Blueprint）：支援藍圖建立 API 要求，完成文字聊天、圖像生成等功能。

設置當前聊天角色：聊天框上方的下拉選單可以設置當前發送文字的角色，可透過模擬不同的角色來調整 AI 聊天。

清空對話紀錄：在聊天框上方的 ❌ 按鈕上點選，可以清空現在對話的歷史訊息。

對話樣板：內建數百種對話設定樣板，方便處理常見問題。

全局設置：點擊左下角的 `Setting` 按鈕，可以打開全局設置視窗。可以設置預設文本聊天，圖像生成的 API 服務，並設置每種 API 服務的具體參數。設置會自動保存在專案的路徑 `$(ProjectFolder)/Saved/AIChatPlusEditor` 下。

會話設定：點擊聊天框上方的設定按鈕，可以打開當前會話的設定視窗。支持修改會話名稱，修改會話使用的 API 服務，支持獨立設定每個會話使用 API 的具體參數。會話設定自動保存在 `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`。

修改聊天內容：當滑鼠停留在聊天內容上方時，將顯示個別訊息的設置按鈕，可支援重新生成內容、修改內容、複製內容、刪除內容以及在底部重新生成內容（針對角色為用戶的內容）。

* 圖像瀏覽：對於圖像生成，點擊圖像會打開圖像查看視窗 (ImageViewer)，支持圖片另存為 PNG/UE 紋理，紋理可以直接在內容瀏覽器 (Content Browser) 查看，方便圖片在編輯器內使用。另外還支持刪除圖片、重新生成圖片、繼續生成更多圖片等功能。對於 Windows 下的編輯器，還支持複製圖片，可以直接將圖片複製到剪貼板，方便使用。會話生成的圖片也會自動保存在每個會話文件夾下面，通常路徑是 `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`。

藍圖：

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

整體設置：

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

對話框設定：

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

修改聊天內容：

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

影像檢視器：

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

使用離線大型模型

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

對話範本

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###核心程式碼介紹

目前插件分成以下幾個模組：

AIChatPlusCommon: 這是運行時模組（Runtime），負責處理各種 AI API 介面發送請求和解析回覆內容。

AIChatPlusEditor: 編輯器模組（Editor），負責實現編輯器 AI 聊天工具。

AIChatPlusCllama: 用來封裝 llama.cpp 的介面和參數，實現執行大型模型的運行時模組。

Thirdparty/LLAMACpp: 在運行時整合了 llama.cpp 的動態庫和頭文件的第三方模塊(Runtime)。

負責發送請求的 UClass 是 FAIChatPlus_xxxChatRequest，每個 API 服務都有對應的獨立 Request UClass。請求的回覆將透過 UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase 這兩個 UClass 來接收，只需註冊相應的回調函數即可。

在發送請求之前，需要先設置好 API 的參數和要發送的訊息。這部分是透過 FAIChatPlus_xxxChatRequestBody 來設定的。回覆的具體內容也被解析到 FAIChatPlus_xxxChatResponseBody 中，在收到回調時，可以透過特定接口獲取 ResponseBody。

可於UE商城購買以獲取更多程式碼細節：[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###編輯器工具使用離線模型 Cllama(llama.cpp)

以下說明如何在 AIChatPlus 編輯器工具中使用離線模型 llama.cpp

請從 HuggingFace 網站下載離線模型：[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

將模型放在某個資料夾裡，例如放在遊戲項目的目錄 Content/LLAMA 下。

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

打開 AIChatPlus 編輯器工具：Tools -> AIChatPlus -> AIChat，新建聊天會話，並開啟會話設置頁面

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

將 Api 設置為 Cllama，啟用自定義 Api 設置，添加模型搜索路徑並選擇模型。

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

開始聊天！

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###使用選擇內建編輯器工具來處理圖片時，會使用離線模型Cllama(llama.cpp)。

從 HuggingFace 網站下載離線模型 MobileVLM_V2-1.7B-GGUF 同樣放到目錄 Content/LLAMA 下：[ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)與 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)抱歉，您提供的文本是一债没有任何内容的句号。

設置對話框架：

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

發送圖片開始聊天

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###使用離線模型代碼 Cllama(llama.cpp)

這裡將說明如何在程式碼中使用離線模型 llama.cpp。

首先，同樣需要將模型檔案下載至 Content/LLAMA 目錄中。

修改程式碼以新增一條指令，在指令中向離線模型發送訊息。

```c++
#include "Common/AIChatPlus_Log.h"
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"

void AddTestCommand()
{
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("AIChatPlus.TestChat"),
		TEXT("Test Chat."),
		FConsoleCommandDelegate::CreateLambda([]()
		{
			if (!FModuleManager::GetModulePtr<FAIChatPlusCommon>(TEXT("AIChatPlusCommon"))) return;

			TWeakObjectPtr<UAIChatPlus_ChatHandlerBase> HandlerObject = UAIChatPlus_ChatHandlerBase::New();
			// Cllama
			FAIChatPlus_CllamaChatRequestOptions Options;
			Options.ModelPath.FilePath = FPaths::ProjectContentDir() / "LLAMA" / "qwen1.5-1_8b-chat-q8_0.gguf";
			Options.NumPredict = 400;
			Options.bStream = true;
			// Options.StopSequences.Emplace(TEXT("json"));
			auto RequestPtr = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(
				Options,
				{
					{"You are a chat bot", EAIChatPlus_ChatRole::System},
					{"who are you", EAIChatPlus_ChatRole::User}
				});

			HandlerObject->BindChatRequest(RequestPtr);
			const FName ApiName = TEnumTraits<EAIChatPlus_ChatApiProvider>::ToName(RequestPtr->GetApiProvider());

			HandlerObject->OnMessage.AddLambda([ApiName](const FString& Message)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] Message: [%s]"), *ApiName.ToString(), *Message);
			});
			HandlerObject->OnStarted.AddLambda([ApiName]()
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestStarted"), *ApiName.ToString());
			});
			HandlerObject->OnFailed.AddLambda([ApiName](const FAIChatPlus_ResponseErrorBase& InError)
			{
				UE_LOG(AIChatPlus_Internal, Error, TEXT("TestChat[%s] RequestFailed: %s "), *ApiName.ToString(), *InError.GetDescription());
			});
			HandlerObject->OnUpdated.AddLambda([ApiName](const FAIChatPlus_ResponseBodyBase& ResponseBody)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestUpdated"), *ApiName.ToString());
			});
			HandlerObject->OnFinished.AddLambda([ApiName](const FAIChatPlus_ResponseBodyBase& ResponseBody)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestFinished"), *ApiName.ToString());
			});

			RequestPtr->SendRequest();
		}),
		ECVF_Default
	);
}
```

重新編譯後，在編輯器 Cmd 中使用命令，便可在日誌 OutputLog 看到大模型的輸出結果。

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###使用離線模型 llama.cpp 的藍圖。

以下是如何在藍圖中使用離線模型 llama.cpp 的說明。

在藍圖中右鍵建立一個節點 `Send Cllama Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

建立 Options 節點，並設定 `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

建立訊息，分別新增一條系統訊息和使用者訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

建立代表委派接收模型輸出資訊並顯示在螢幕上。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完整的藍圖看起來像這樣，運行藍圖，即可看到遊戲螢幕上顯示的大型模型的消息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###編輯器使用 OpenAI 聊天

打開聊天工具 Tools -> AIChatPlus -> AIChat，創建新的聊天會話 New Chat，設置會話 ChatApi 為 OpenAI，設置接口參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

開始聊天：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

將模型切換為 GPT-4o / GPT-4o-mini，可以利用 OpenAI 的視覺功能分析圖片。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###編輯器使用 OpenAI 處理圖片（創建/修改/變種）

在聊天工具中創建新的圖片對話 New Image Chat，修改對話設定為 OpenAI，並設置參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

建立圖片

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

修改圖片，將對話圖像類型修改為編輯，然後上傳兩張圖片。一張是原始圖片，另一張是帶有透明部分（alpha通道為0）的遮罩圖片，用來標記需要修改的區域。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

將圖片變種，將聊天圖片類型修改為變種並上傳一張圖片，OpenAI 將返回原始圖片的變種。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###藍圖使用 OpenAI 模型聊天

在藍圖中右鍵創建一個節點 `Send OpenAI Chat Request In World`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

建立選項節點，並設置 `Stream=true, Api Key="您從 OpenAI 獲取的 API 金鑰"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

建立訊息，分別新增一條系統訊息和使用者訊息

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

建立 Delegate 接收模型輸出的資訊並顯示在螢幕上

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完整的藍圖看起來是這樣的，運行藍圖，即可看到遊戲螢幕在列印大型模型返回的訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###藍圖使用 OpenAI 創建圖片

在藍圖中右鍵創建一個節點 `Send OpenAI Image Request`，並設定 `In Prompt="a beautiful butterfly"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

建立 Options 节点，並設置 `Api Key="您從 OpenAI 獲得的 API 金鑰"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

綁定圖片事件，並將圖片保存到本地硬碟上。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

完整的藍圖看起來就像這樣，運行藍圖，你就可以看到圖片保存在指定的位置上。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###編輯器使用 Azure

新建對話（New Chat），將 ChatApi 改為 Azure，並設置 Azure 的 Api 參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###使用 Azure 建立圖片的編輯器

建立新的圖像對話（New Image Chat），將ChatApi改為Azure，並設置Azure的API參數，請注意，如果是dall-e-2模型，需要將品質（Quality）和風格（Stype）參數設置為not_use。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

開始聊天，請 Azure 創建圖片。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###請使用 Azure 聊天蓝图。

建立以下藍圖，設定好 Azure 選項，點擊執行，即可在螢幕上看到 Azure 回傳的聊天訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###使用Azure創建圖片的藍圖

建立以下的藍圖，設定好 Azure 選項，點擊執行。若建立圖片成功，將在螢幕上看到訊息 "Create Image Done"。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

根據上述藍圖設置，圖片將保存在路徑 D:\Dwnloads\butterfly.png。

## Claude

###編輯器使用Claude聊天和分析圖片。

新建對話（New Chat），將 ChatApi 修改為 Claude，並設置 Claude 的 Api 參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###使用Claude藍圖進行聊天和圖片分析。

在藍圖中右鍵創建一個節點 `Send Claude Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

建立 Options 节点，並設置 `Stream=true, Api Key="來自Clude的API金鑰", Max Output Tokens=1024`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

建立 Messages，從檔案建立 Texture2D，並從 Texture2D 創建 AIChatPlusTexture，將 AIChatPlusTexture 加入到 Message 中。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

與上述教程相同，創建事件並將信息列印在遊戲屏幕上。

完整的藍圖看起來是這樣的，運行藍圖，即可看到遊戲螢幕在列印大模型返回的訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###獲取 Ollama

您可以透過 Ollama 官方網站下載安裝檔進行本機安裝：[ollama.com](https://ollama.com/)

可以使用其他人提供的 Ollama 介面來使用 Ollama。

###編輯器使用 Ollama 聊天和分析圖片

* 新建會話（New Chat），將 ChatApi 改為 Ollama，並設置 Ollama 的 API 參數。如果是文本聊天，則設置模型為文本模型，如 llama3.1；如果需要處理圖片，則設置模型為支援 vision 的模型，例如 moondream。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###使用Ollama藍圖聊天和分析圖片。

建立以下藍圖，設置好 Ollama 選項，點擊執行，即可看到屏幕上打印 Ollama 返回的聊天信息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###編輯器使用 Gemini

新建會話（New Chat），將 ChatApi 改為 Gemini，並設置 Gemini 的 Api 參數。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###請使用 Gemini Messenger 查看藍圖。

建立以下藍圖，設置好 Gemini 選項，點擊運行，即可在螢幕上看到 Gemini 回傳的聊天訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)


##更新紀錄

### v1.4.1 - 2025.01.04

####問題修復

聊天工具支援僅發送圖片而不發送訊息

修復 OpenAI 介面傳送圖片問題失敗文件图

修復 OpanAI、Azure 聊天工具設置遺漏了參數 Quality、Style、ApiVersion 問題。

### v1.4.0 - 2024.12.30

####新功能

* （實驗性功能）Cllama(llama.cpp) 支援多模態模型，可以處理圖片

所有的藍圖類型參數都加上了詳細提示。

### v1.3.4 - 2024.12.05

####新功能

OpenAI 支援視覺 API。

####問題修復

修復 OpenAI stream=false 時的錯誤

### v1.3.3 - 2024.11.25

####新功能

支援 UE-5.5

####問題修復

修復部分藍圖不生效問題。

### v1.3.2 - 2024.10.10

####問題修復

當手動停止 request 時修復 cllama 崩潰。

修復商城下載版本 win 打包找不到 ggml.dll llama.dll 文件的問題

在创建请求时检查是否在游戏线程中。

### v1.3.1 - 2024.9.30

####新功能

新增一個 SystemTemplateViewer，可查看並使用數百個系統設定模版。

####問題修復

修復商城下載的插件時，出現 llama.cpp 無法找到連結庫的問題。

修復 LLAMACpp 路徑過長問題

修復 Windows 打包後的連結 llama.dll 錯誤

修復 iOS/Android 讀取檔案路徑問題

修復 Cllame 設置名字錯誤

### v1.3.0 - 2024.9.23

####重要的新功能

將 llama.cpp 整合，支援在本機離線執行大型模型。

### v1.2.0 - 2024.08.20

####新功能

支援 OpenAI 影像編輯/圖像變異

支持 Ollama API，支持自動獲取 Ollama 支持的模型列表

### v1.1.0 - 2024.08.07

####新功能

支持藍圖

### v1.0.0 - 2024.08.05

####新功能

基礎完整功能

支持 OpenAI，Azure，Claude，Gemini

具有完善編輯器的內建聊天工具

--8<-- "footer_tc.md"


> 此帖文是透過 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)請指出任何遺漏之處。 
