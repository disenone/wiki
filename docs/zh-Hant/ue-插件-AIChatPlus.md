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

##插件獲取

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##插件簡介

此擴充套件支持 UE5.2+。

UE.AIChatPlus 是 UnrealEngine 的一個插件，可與多種 GPT AI 聊天服務進行通訊。目前支援的服務包括 OpenAI（ChatGPT、DALL-E）、Azure OpenAI（ChatGPT、DALL-E）、Claude、Google Gemini、以及本地離線的 Ollama 和 llama.cpp。未來將持續擴展支援更多服務提供者。這個插件基於異步 REST 請求實現，性能高效，方便 UnrealEngine 開發人員接入這些 AI 聊天服務。

UE.AIChatPlus 還包含了一個編輯器工具，可以直接在編輯器中使用這些 AI 聊天服務，生成文本和圖像，分析圖像等。

##使用說明

###編輯器聊天工具

菜单欄 Tools -> AIChatPlus -> AIChat 可以開啟插件提供的編輯器聊天工具

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


工具支援文件產生、文字對話、圖像生成，以及圖像分析。

工具的介面大致如下：

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####主要功能

離線大模型：整合了 llama.cpp 庫，支持本地離線執行大模型

文本聊天：點擊左下角的 `New Chat` 按鈕，創建新的文本聊天會話。

圖像生成：點擊左下角的 `New Image Chat` 按鈕，建立新的圖像生成會話。

圖像分析：`New Chat` 的部分聊天服務支援發送圖像，例如 Claude、Google Gemini。點擊輸入框上方的 🖼️ 或 🎨 按鈕即可載入需要發送的圖像。

支持藍圖（Blueprint）：支持藍圖建立 API 請求，實現文字聊天、圖像生成等功能。

設置當前聊天角色：聊天框上方的下拉式選單可讓您設置當前發送文字的角色，透過模擬不同的角色來調整 AI 聊天。

清空對話：點擊聊天框上方的 ❌ 圖示可以清除現在對話的歷史訊息。

對話範本：內建數百種對話設定模板，便於處理常見問題。

全局設置：點擊左下角的 `Setting` 按鈕，可以打開全局設置視窗。可以設置預設文本聊天，圖像生成的 API 服務，並設置每種 API 服務的具體參數。設置會自動保存在項目的路徑 `$(ProjectFolder)/Saved/AIChatPlusEditor` 下。

對話設置：點擊聊天框上方的設置按鈕，可以打開目前對話的設置視窗。支持修改對話名稱，修改對話使用的 API 服務，支持獨立設定每個對話使用 API 的具體參數。對話設置將自動保存在 `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`。

聊天內容修改：當滑鼠懸停在聊天內容上時，會出現一個設定按鈕，提供重新生成內容、修改內容、複製內容、刪除內容、以及在下方重新生成內容（針對角色是使用者的內容）。

圖像瀏覽：對於圖像生成，點擊圖像會打開圖像查看窗口（ImageViewer），支持圖片另存為PNG/UE Texture，Texture可以直接在內容瀏覽器（Content Browser）查看，方便圖片在編輯器內使用。另外還支持刪除圖片、重新生成圖片、繼續生成更多圖片等功能。對於Windows下的編輯器，還支持複製圖片，可以直接把圖片複製到剪貼板，方便使用。會話生成的圖片也會自動保存在每個會話文件夾下面，通常路徑是`$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`。

藍圖：

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

整體設定：

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

對話框設置:

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

* AIChatPlusCommon: Runtime 模組負責處理各種 AI API 介面的發送請求和解析回應內容。

AIChatPlusEditor：編輯器模組(Editor)，負責實現編輯器 AI 聊天工具。

AIChatPlusCllama：運行時模組（Runtime），負責封裝llama.cpp的介面和參數，實現離線執行大型模型

第三方/LLAMACpp: 這是一個運行時第三方模組（Runtime），整合了 llama.cpp 的動態庫和頭文件。

負責發送請求的 UClass 是 FAIChatPlus_xxxChatRequest，每種 API 服務都各自擁有獨立的 Request UClass。請求的回覆通過 UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase 兩種 UClass 來取得，僅需註冊相應的回調委派。

在發送請求之前，需要先設置好 API 的參數和要發送的訊息，這部分是透過FAIChatPlus_xxxChatRequestBody來設定。回覆的具體內容也會被解析到FAIChatPlus_xxxChatResponseBody中，當收到回調時可以通過特定介面獲取ResponseBody。

更多源碼細節可在 UE 商城取得：[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###編輯器工具使用離線模型 Cllama(llama.cpp)

這裡說明如何在 AIChatPlus 編輯器工具中使用離線模型 llama.cpp

請從 HuggingFace 網站下載離線模型：[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

將模型放置於特定文件夾中，例如放在遊戲項目的 Content/LLAMA 目錄下。

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

開啟 AIChatPlus 編輯器工具：工具 -> AIChatPlus -> AIChat，新建聊天會話，並打開會話設置頁面

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

將 Api 設定為 Cllama，開啟自訂 Api 設定，並新增模型搜尋路徑，然後選擇模型。

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

開始聊天！！

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###使用編輯器工具處理圖像的離線模型 Cllama(llama.cpp)。

從 HuggingFace 網站下載離線模型 MobileVLM_V2-1.7B-GGUF 同樣放到目錄 Content/LLAMA 下：[ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)與 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)抱歉，無法為您翻譯不包含任何文字內容的句子。如果您需要翻譯其他文字，請隨時告訴我。谢谢！

設置會話模式：

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

發送圖片開始聊天

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###代碼使用離線模型Cllama(llama.cpp)

這裡說明如何在程式碼中使用離線模型 llama.cpp。

首先，同樣需要將模型文件下載到 Content/LLAMA 目錄中。

修改程式碼以新增一個指令，在指令中向離線模型發送訊息。

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

重新編譯後，在編輯器 Cmd 中使用命令，便可在日誌 OutputLog 看到大型模型的輸出結果。

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###使用蓝圖文件 llama.cpp 中的離線模型。

以下說明如何在藍圖中使用離線模型 llama.cpp

在藍圖中右鍵創建一個節點 `Send Cllama Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

創建 Options 節點，並設置 `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

建立訊息，分別新增系統訊息和使用者訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

建立 Delegate 來接收模型輸出的資訊，並顯示於螢幕上。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完整的藍圖看起來是這樣的，運行藍圖，即可看到遊戲螢幕上列印大模型返回的訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###編輯器使用 OpenAI 聊天

打開聊天工具 工具 -> AIChatPlus -> AIChat，建立新的聊天對話 新對話，設定對話 ChatApi 為 OpenAI，設置接口參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

開始聊天：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

將模型切換為 gpt-4o / gpt-4o-mini 後，即可利用 OpenAI 的視覺功能來分析圖片。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###編輯器使用 OpenAI 處理圖片（建立/修改/變異）

在聊天工具中建立新的圖片對話 New Image Chat，修改對話設定為 OpenAI，並設置參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

建立圖片

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

修改圖片，將對話圖像類型修改為編輯，並上傳兩張圖片，一張是原始圖片，一張是具有透明位置（Alpha 通道為 0）的遮罩，這些位置表示需要修改的區域。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

將圖片變種，將對話圖片類型修改為變異，然後上傳一張圖片，OpenAI 將返回原圖片的變種。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###使用 OpenAI 模型進行藍圖交流

* 在藍圖中右鍵創建一個節點 `Send OpenAI Chat Request In World`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

建立 Options 节点，並設置 `Stream=true, Api Key="你從 OpenAI 獲取的 API 金鑰"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

建立"訊息"，分別新增一則"系統訊息"和"使用者訊息"。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

建立代理人以接收模型的輸出資訊並輸出至螢幕。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完善的藍圖看起來像這樣，執行藍圖，即可在遊戲畫面中看到返回的大型模型列印訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###使用 OpenAI 創建圖片的藍圖

在藍圖中右鍵創建一個節點 `Send OpenAI Image Request`，並設置 `In Prompt="a beautiful butterfly"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

建立 Options 節點，並設置 `Api Key="你從 OpenAI 獲取的 API 金鑰"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

為圖片添加 On Images 事件，並將圖片保存到本地硬碟上。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

完整的藍圖看起來會像這樣，執行藍圖後，您將能在指定位置看到圖片被儲存。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###編輯器使用 Azure

新增對話（New Chat），將 ChatApi 改為 Azure，並設置 Azure 的 API 參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

* 開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###編輯器使用 Azure 建立圖片

新建圖片會話（New Image Chat），將 ChatApi 改為Azure，並設定Azure的API參數，請注意，如果是dall-e-2模型，需要將 Quality 和 Stype 參數設置為 not_use。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

開始聊天，讓 Azure 創建圖片

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###請使用 Azure 聊天來製作藍圖。

建立以下藍圖，設定 Azure 選項，點擊運行，即可在螢幕上看到 Azure 返回的聊天訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###使用Azure建立圖像的藍圖。

建立以下藍圖，設定好 Azure 選項，點擊執行，如果圖片建立成功，將在螢幕上看到訊息 "Create Image Done"。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

根據上述藍圖設定，圖片將保存在路徑 D:\Dwnloads\butterfly.png

## Claude

###編輯器使用Claude聊天和分析圖片

建立新的對話（New Chat），將 ChatApi 修改為 Claude，並設置 Claude 的 Api 參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###使用Claude软件进行聊天和图像分析。

在藍圖中右鍵創建一個節點`Send Claude Chat Request`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

建立 Options 节点，並設置 `Stream=true, Api Key="you api key from Clude", Max Output Tokens=1024`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

創建 Messages，從檔案創建 Texture2D，並從 Texture2D 創建 AIChatPlusTexture，將 AIChatPlusTexture 添加到 Message 中

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

與上述教程相同，建立事件並將資訊列印在遊戲畫面上。

完整的藍圖看起來像這樣，運行藍圖，即可看到遊戲畫面在打印大型模型返回的訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###獲取 Ollama

您可以從 Ollama 官方網站獲取安裝程式，並進行本機安裝：[ollama.com](https://ollama.com/)

可以利用其他人提供的 Ollama 介面來使用 Ollama。

###編輯器使用 Ollama 聊天和分析圖片

新建會話（New Chat），將 ChatApi 改為 Ollama，並設置 Ollama 的 Api 參數。如果是文字聊天，則設置模型為文字模型，如 ll ama3.1；如果需要處理圖片，則設置模型為支援視覺的模型，例如 moondream。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

開始對話

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###藍圖使用 Ollama 聊天和分析圖片

建立以下藍圖，設定好Ollama選項，點擊執行，即可在屏幕上看到顯示Ollama返回的聊天資訊。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###請使用 Gemini 編輯器。

新建會話（New Chat），將 ChatApi 改為 Gemini，並設置 Gemini 的 Api 參數。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###請使用 Gemini 聊天藍圖。

建立以下藍圖，設置好 Gemini 選項，點擊運行，即可看到畫面上列印 Gemini 返回的聊天資訊。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)


##更新日誌

### v1.4.1 - 2025.01.04

####問題修復

聊天工具支援只傳送圖片不發送訊息。

修復 OpenAI 介面發送圖片問題失敗文件圖。

修復 OpanAI、Azure 聊天工具設置遺漏了參數 Quality、Style、ApiVersion 問題。

### v1.4.0 - 2024.12.30

####新功能

（實驗性功能）Cllama（llama.cpp）支援多模態模型，可處理圖片

所有的藍圖類型參數都加上了詳細提示

### v1.3.4 - 2024.12.05

####新功能

OpenAI 支援視覺 API。

####問題修復

修復 OpenAI stream=false 時的錯誤

### v1.3.3 - 2024.11.25

####新功能

* 支援 UE-5.5

####問題修復

修復部分藍圖不生效問題

### v1.3.2 - 2024.10.10

####問題修復

修復手動停止 request 的時候 cllama 崩潰

修復商城下載版本 win 打包找不到 ggml.dll llama.dll 文件的問題

在创建请求时，检查是否在游戏主线程中。

### v1.3.1 - 2024.9.30

####新功能

新增一個 SystemTemplateViewer，用於瀏覽和使用數百個系統設置模板。

####問題修復

修復從商城下載的插件，llama.cpp 找不到鏈接庫

修復 LLAMACpp 路徑過長問題

修復 Windows 打包後的連結 llama.dll 錯誤

修復 iOS/Android 讀取檔案路徑問題

修復 Cllame 設置名字錯誤

### v1.3.0 - 2024.9.23

####重要的新功能

整合了 llama.cpp，支援本地離線執行大型模型。

### v1.2.0 - 2024.08.20

####新功能

支持 OpenAI 圖像編輯/圖像變異

支援 Ollama API，以及自動取得 Ollama 支援的模型清單。

### v1.1.0 - 2024.08.07

####新功能

支持藍圖

### v1.0.0 - 2024.08.05

####新功能

基礎完整功能

支持 OpenAI, Azure, Claude, Gemini.

具備完善功能編輯器的聊天工具

--8<-- "footer_tc.md"


> 這篇文章是由 ChatGPT 翻譯的，如有任何[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
