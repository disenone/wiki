---
layout: post
title: UE 外掛 AIChatPlus 說明文件
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

##外掛簡介

This plugin supports UE5.2+.

UE.AIChatPlus 是一個 UnrealEngine 外掛程式，能夠與各種 GPT AI 聊天服務進行溝通。目前支持的服務包括 OpenAI（ChatGPT、DALL-E）、Azure OpenAI（ChatGPT、DALL-E）、Claude、Google Gemini、Ollama，以及 llama.cpp 本地離線。未來還將持續擴展更多服務提供商。該外掛程式基於異步 REST 請求實現，性能高效，方便 UnrealEngine 開發人員接入這些 AI 聊天服務。

UE.AIChatPlus 還包含了一個編輯器工具，可以直接在編輯器中使用這些 AI 聊天服務，生成文本和圖像，分析圖像等。

##使用說明

###編輯器聊天工具

菜單欄 Tools -> AIChatPlus -> AIChat 可以啟用此插件提供的編輯聊天工具。

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


工具支持文本生成、文本聊天、圖像生成，圖像分析。

工具的界面大致為：

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####主要功能

離線大模型：整合了 llama.cpp 庫，支援本地離線執行大模型

在文字聊天時：請按左下角的 `新增聊天` 按鈕，建立新的文字聊天對話。

圖像生成：點擊左下角的 `New Image Chat` 按鈕，創建新的圖像生成會話。

圖像分析: `New Chat` 的部分聊天服務支援發送圖像，例如 Claude, Google Gemini。點擊輸入框上方的 🖼️ 或 🎨 按鈕即可載入需要發送的圖像。

支持藍圖（Blueprint）：支持藍圖建立 API 要求，完成文字聊天、圖像生成等功能。

設定當前聊天角色：在聊天框上方的下拉選單中，可以選擇當前發送訊息的角色，透過模擬不同角色來調整 AI 聊天。

清空對話：在聊天框上方的 ❌ 按鈕可以清空當前對話的歷史消息。

對話模板：內建數百種對話設定模板，便於處理常見問題。

全局設置：點擊左下角的 `Setting` 按鈕，可以打開全局設置視窗。可以設置預設文本聊天，圖像生成的 API 服務，並設置每種 API 服務的具體參數。設置會自動保存在專案的路徑 `$(ProjectFolder)/Saved/AIChatPlusEditor` 下。

會話設定：點擊聊天框上方的設定按鈕，可以打開當前會話的設定視窗。支援修改會話名稱，修改會話使用的 API 服務，支援獨立設定每個會話使用 API 的具體參數。會話設定自動保存在 `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`。

聊天內容修改: 當滑鼠懸停在聊天內容上時，將顯示該聊天內容的設置按鈕，支援重新生成內容、修改內容、複製內容、刪除內容、重新生成下方內容（對於角色是使用者的內容）。

圖像瀏覽：對於圖像生成，點擊圖像會開啟圖像檢視視窗（ImageViewer），支援圖片另存為 PNG/UE Texture，Texture 可以直接在內容瀏覽器（Content Browser）查看，方便圖片在編輯器內使用。另外還支援刪除圖片、重新生成圖片、繼續生成更多圖片等功能。對於 Windows 下的編輯器，還支援複製圖片，可以直接將圖片複製到剪貼簿，方便使用。會話生成的圖片也會自動保存在每個會話資料夾下，通常路徑為 `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`。

藍圖：

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

全局設置：

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

對話設置：

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

修改聊天內容：

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

圖像檢視器：

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

使用離線大型模型

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

對話範本

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###核心程式碼介紹

目前插件分成以下幾個模組：

AIChatPlusCommon: Runtime，專責處理各種 AI API 介面發出的請求和解析回覆內容。

AIChatPlusEditor: 編輯器模組 (Editor)，負責實現編輯器 AI 聊天工具。

AIChatPlusCllama：執行時模組（Runtime），負責封裝llama.cpp的介面和參數，實現離線執行大型模型

* Thirdparty/LLAMACpp: 包含了 llama.cpp 的動態庫和標頭檔的運行時第三方模組（Runtime）。

負責發送請求的具體 UClass 是 FAIChatPlus_xxxChatRequest，每種 API 服務都有專屬的 Request UClass。回應請求則是透過 UAIChatPlus_ChatHandlerBase/UAIChatPlus_ImageHandlerBase 兩種 UClass 來獲取，只需註冊相應的回調委託。

在發送請求之前，需要先設置好 API 的參數和發送的消息。這部分是透過 FAIChatPlus_xxxChatRequestBody 來設定。回覆的具體內容也被解析到 FAIChatPlus_xxxChatResponseBody 中，當收到回調時，可以通過特定接口獲取 ResponseBody。

可在UE商城获取更多源码细节：[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###使用編輯器工具編輯離線模型 Cllama (llama.cpp)

如何在 AIChatPlus 編輯器工具中運用離線模型 llama.cpp 的方法如下：

首先，從 HuggingFace 網站下載離線模型：[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

將模型放置在特定資料夾中，例如將其放在遊戲專案目錄 Content/LLAMA 中。

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

打開 AIChatPlus 編輯器工具：工具 -> AIChatPlus -> AIChat，新建聊天會話，並打開會話設定頁面。

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

將 Api 設置為 Cllama，開啟自定義 Api 設置，添加模型搜索路徑，並選擇模型。

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

開始聊天！！

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###使用編輯器工具處理圖片，使用離線模型 Cllama(llama.cpp)。

從 HuggingFace 網站下載離線模型 MobileVLM_V2-1.7B-GGUF 同樣放到目錄 Content/LLAMA 下：[ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)與 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)抱歉，我無法將您提供的文字進行翻譯。

設置對話模型：

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

傳送圖片開始聊天

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###代碼使用離線模型 Cllama(llama.cpp)

以下說明了如何在程式碼中使用離線模型 llama.cpp

首先，同樣需要下載模型文件到 Content/LLAMA 下。

更改程式碼以新增一個指令，在該指令中向離線模型發送訊息。

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

重新編譯後，在編輯器 Cmd 中使用命令，便可在日誌 OutputLog 看到大型模型的輸出結果

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###蓝图使用離線模型 llama.cpp

請參考以下說明以在藍圖中使用離線模型 llama.cpp。

在藍圖中右鍵建立一個節點 `Send Cllama Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

建立 Options 節點，並設定 `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

建立訊息，分別新增系統訊息和使用者訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

建立 Delegate 接收模型輸出的資訊，並顯示在螢幕上。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完整的藍圖看起來會是這樣，運行藍圖後，您將在遊戲畫面上看到返回的大型模型打印消息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###使用 OpenAI 進行編輯器聊天。

請打開聊天工具，選擇「工具」->「AIChatPlus」->「AIChat」，然後創建一個新的聊天對話。將對話設定為「ChatApi」，並設置接口參數。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

開始聊天：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

將模型切換至 gpt-4o / gpt-4o-mini，即可利用 OpenAI 的視覺功能來分析圖片。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###編輯器使用 OpenAI 處理圖片（創建/修改/變種）

在聊天工具中建立新的圖片聊天，將會話設置更改為 OpenAI，並設定參數。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

建立圖片

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

修改圖片，將對話的圖片類型修改為「編輯」，然後上傳兩張圖片：一張是原始圖片，另一張是 mask 圖像，其中透明的部分（alpha 通道為 0）表示需要進行修改的區域。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

將圖片變種，將對話圖像類型修改為變種，並上傳一張圖片，OpenAI 將返回一張原始圖片的變種。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###使用OpenAI模型進行對話設計

在藍圖中點擊滑鼠右鍵建立一個節點 `發送 OpenAI 聊天請求在世界中`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

建立 Options節點，並設置 `Stream=true, Api Key="你從 OpenAI 獲取的 API 金鑰"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

建立訊息，分別新增一則系統訊息和使用者訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

建立 Delegate 接受模型輸出的資訊，並在螢幕上列印出來

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完整的藍圖看起來就是這樣的，執行藍圖，即可看到遊戲螢幕上打印出大型模型返回的訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###藍圖使用 OpenAI 建立圖片

在藍圖中右鍵創建一個節點 `Send OpenAI Image Request`，並設置 `In Prompt="a beautiful butterfly"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

建立 Options 節點，並設置 `Api Key="你從性從 OpenAI 獲取的 API 金鑰"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

為圖像綁定事件，並將圖片保存到本地硬碟上。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

完整的藍圖看起來是這樣的，運行藍圖，即可看到圖片保存在指定的位置上。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###編輯器使用 Azure

建立新對話（New Chat），將 ChatApi 改為 Azure，並設置 Azure 的 API 參數。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###使用 Azure 建立圖片的編輯器

創建新的圖片對話（New Image Chat），將 ChatApi 改爲Azure，並設置Azure的API參數，請注意，如果使用dall-e-2模型，請將品質（Quality）和風格（Stype）參數設置為not_use。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

開始聊天，讓 Azure 創建圖片

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###藍圖使用 Azure 聊天

建立以下藍圖，設定好 Azure 選項，點擊執行，即可在螢幕上看到 Azure 返回的聊天訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###使用 Azure 建立圖片的藍圖

建立如下藍圖，設定好 Azure Options，點擊執行，如果建立圖片成功，會在螢幕上看到訊息 "Create Image Done"。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

根據上述藍圖設置，圖片將保存在路徑 D:\Dwnloads\butterfly.png。

## Claude

###使用編輯器與 Claude 進行聊天和分析圖片。

新建對話（New Chat），將 ChatApi 改為 Claude，並設置 Claude 的 Api 參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###使用Claude藉由聊天和圖片進行藍圖分析。

在藍圖中按右鍵建立一個節點 `發送克勞德聊天請求`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

創建 Options 節點，並設置 `Stream=true, Api Key="you api key from Clude", Max Output Tokens=1024`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

創建 Messages，從檔案建立 Texture2D，並從 Texture2D 創建 AIChatPlusTexture，將 AIChatPlusTexture 添加到 Message 中。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

* 就像前述的教學一樣，建立事件並將訊息列印到遊戲螢幕上。

完整的藍圖看起來是這樣的，運行藍圖，即可看到遊戲畫面在列印大型模型返回的訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###獲取 Ollama

您可以透過 Ollama 官方網站取得安裝檔案進行本地安裝：[ollama.com](https://ollama.com/)

可以使用其他人提供的 Ollama 介面來使用 Ollama。

###編輯器使用 Ollama 聊天和分析圖片

* 新增對話（New Chat），將 ChatApi 改為 Ollama，並設定 Ollama 的 API 參數。若為文字聊天，則設置模型為文字模型，如 llama3.1；若需處理圖片，則設置模型為支援視覺的模型，例如 moondream。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###論文使用Ollama進行聊天和分析圖片。

建立這個藍圖，設定好 Ollama 選項，點選運行，就能夠在螢幕上看到 Ollama 回傳的聊天訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###編輯器：Gemini

* 新增聊天（New Chat），將 ChatApi 改為 Gemini，並設置 Gemini 的 API 參數。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###使用Gemini聊天的藍圖

建立以下藍圖，設定好 Gemini 選項，點擊執行，即可看到螢幕上列印 Gemini 返回的聊天訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

## Deepseek

###編輯器使用Deepseek

* 新增對話（New Chat），將 ChatApi 改為 OpenAi，並設定 Deepseek 的 API 參數。新增候選模型名稱為 deepseek-chat，並將模型設定為 deepseek-chat。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###藍圖使用 Deepseek 聊天

建立以下藍圖，設置好 Deepseek 相關的 Request Options，包括 Model、Base Url、End Point Url、ApiKey 等參數。點擊運行，即可看到螢幕上列印出 Gemini 返回的聊天信息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##更新紀錄

### v1.4.1 - 2025.01.04

####問題修復

聊天工具支援僅發送圖片而不發送訊息。

修復 OpenAI 介面發送圖片問題失敗文字

修復 OpanAI、Azure 聊天工具設定遺漏了參數 Quality、Style、ApiVersion 問題=

### v1.4.0 - 2024.12.30

####新功能

（實驗性功能）Cllama(llama.cpp)支援多模式模型，可以處理圖片

所有的藍圖類型參數都已添加詳細提示。

### v1.3.4 - 2024.12.05

####新功能

OpenAI 支援的視覺 API。

####問題修復

修復 OpenAI stream=false 時的錯誤

### v1.3.3 - 2024.11.25

####新功能

支援 UE-5.5

####問題修復

修復部分藍圖不生效問題

### v1.3.2 - 2024.10.10

####問題修復

修復手動停止 request 的時候 cllama 崩潰

修復商城下載版本Win打包時找不到ggml.dll和llama.dll文件的問題。

在创建请求时检查是否在游戏线程中。

### v1.3.1 - 2024.9.30

####新功能

新增一個SystemTemplateViewer，可以查看和使用幾百個system設置模板。

####問題修復

修復從商城下載的插件，llama.cpp 找不到鏈接庫。

修復 LLAMACpp 路徑過長問題

修復 Windows 打包後的連結 llama.dll 錯誤

修復 iOS/Android 讀取檔案路徑問題

修正Cllame設定名稱錯誤

### v1.3.0 - 2024.9.23

####重要的新功能

將 llama.cpp 整合，支援本地離線執行大型模型。

### v1.2.0 - 2024.08.20

####新功能

支援 OpenAI 圖像編輯/圖像變化

支持 Ollama API，支持自動獲取 Ollama 支持的模型列表

### v1.1.0 - 2024.08.07

####新功能

支持藍圖

### v1.0.0 - 2024.08.05

####新功能

基礎完整功能

Support OpenAI，Azure，Claude，Gemini

具備完善功能的編輯器聊天工具

--8<-- "footer_tc.md"


> 這篇文章是由 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
