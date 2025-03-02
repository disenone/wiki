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

##擴充功能取得

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##插件簡介

該插件支援 UE5.2+。

UE.AIChatPlus 是一個 UnrealEngine 外掛程式，實現與各種 GPT AI 聊天服務通訊的功能。目前支援的服務有 OpenAI (ChatGPT, DALL-E)、Azure OpenAI (ChatGPT, DALL-E)、Claude、Google Gemini、Ollama、以及本地離線的 llama.cpp。未來將持續支援更多服務提供商。它採用異步REST請求實現，性能高效，方便UE開發人員接入這些AI聊天服務。

UE.AIChatPlus 同時還包含了一個編輯器工具，可以直接在編輯器中使用這些 AI 聊天服務，生成文本和圖像，分析圖像等。

##使用說明

###編輯器聊天工具

菜單列 Tools -> AIChatPlus -> AIChat 可以打開插件提供的編輯器聊天工具

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


工具支援文本生成、文本聊天、圖像生成，以及圖像分析。

工具的界面大致為：

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####主要功能

離線大模型：整合了 llama.cpp 庫，支持本地離線執行大模型

點擊左下角的 `New Chat` 按鈕，建立新的文字聊天對話。

圖像生成：點擊左下角的 `New Image Chat` 按鈕，創建新的圖像生成會話。

圖像分析：`New Chat` 的部分聊天服務支援發送圖像，例如 Claude、Google Gemini。點擊輸入框上方的 🖼️ 或 🎨 按鈕即可加載需要發送的圖像。

支持藍圖（Blueprint）：支持藍圖創建 API 請求，完成文本聊天、圖像生成等功能。

設置當前聊天角色：聊天框上方的下拉框可以設定當前發送文本的角色，可以透過模擬不同的角色來調整 AI 聊天。

清空對話: 在聊天框頂部的 ❌ 按鈕，可以清除目前對話的歷史訊息。

對話模板：內建數百種對話設定模板，方便處理常見問題。

全局设置：點擊左下角的 `Setting` 按鈕，可以打開全局設置視窗。可以設置預設文本聊天，圖像生成的 API 服務，並設置每種 API 服務的具體參數。設置會自動保存在項目的路徑 `$(ProjectFolder)/Saved/AIChatPlusEditor` 下。

對話設定：點擊聊天框上方的設定按鈕，可以打開當前對話的設定視窗。支持修改對話名稱，修改對話使用的 API 服務，支持獨立設定每個對話使用 API 的具體參數。對話設定會自動保存在 `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`當中。

聊天內容修改：當把滑鼠懸停在聊天內容上時，會出現個別聊天內容的設定按鈕，可支持重新生成內容、修改內容、複製內容、刪除內容、在下方重新生成內容（針對角色為使用者的內容）。

* 圖像瀏覽：對於圖像生成，點擊圖像將開啟圖像查看窗口 (ImageViewer)，支持圖片另存為 PNG/UE 紋理，紋理可直接在內容瀏覽器 (Content Browser) 中查看，方便圖片在編輯器內使用。另外還支持刪除圖片、重新生成圖片、繼續生成更多圖片等功能。對於 Windows 下的編輯器，還支持複製圖片，可以直接將圖片複製到剪貼板，方便使用。會話生成的圖片也會自動保存在每個會話資料夾下，通常路徑是 `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`。

藍圖：

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

全局設置：

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

對話設定：

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

修改聊天內容：

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

圖像檢視器：

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

使用離線大型模型

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

對話範本

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###核心代碼介紹

目前插件分成以下幾個模組：

AIChatPlusCommon: Runtime是一個運行時模組，負責處理各種人工智慧API介面的請求和解析回覆內容。

AIChatPlusEditor: 編輯器模組 (Editor)， 負責實現編輯器 AI 聊天工具。

AIChatPlusCllama: 運行時模塊（Runtime），負責封裝 llama.cpp 的介面和參數，實現離線執行大型模型

Thirdparty/LLAMACpp: 在運行時，整合了 llama.cpp 的動態庫和頭文件的第三方模塊。

負責發送請求的 UClass 是 FAIChatPlus_xxxChatRequest，每種 API 服務都分別有獨立的 Request UClass。請求的回覆透過 UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase 兩種 UClass 來獲取，只需要註冊相應的回調委託。

在發送請求之前，需要先設定好 API 的參數和要發送的訊息，這部分是透過 FAIChatPlus_xxxChatRequestBody 來設定的。回覆的具體內容也會解析到 FAIChatPlus_xxxChatResponseBody 中，收到回調時可以透過特定接口獲取 ResponseBody。

您可以在UE商城獲取更多的源碼細節：[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###使用離線模型編輯器工具 Cllama(llama.cpp)

以下說明如何在 AIChatPlus 編輯器工具中使用離線模型 llama.cpp

首先，從 HuggingFace 網站下載離線模型：[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

將模型放在特定資料夾中，例如將其放在遊戲項目的目錄 Content/LLAMA 中。

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

打開 AIChatPlus 編輯器工具：工具 -> AIChatPlus -> AIChat，新建聊天會話，並打開會話設置頁面

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

將 API 設定為 Cllama，啟用自定義 API 設定，新增模型搜尋路徑並選擇模型。

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

開始聊天！！

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###使用編輯器工具來處理圖片時，請使用離線模型 Cllama(llama.cpp)。

從 HuggingFace 網站下載離線模型 MobileVLM_V2-1.7B-GGUF 同樣放到目錄 Content/LLAMA 下：[ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)與 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)抱歉，我無法翻譯這個內容。

設置會話的模型：

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

傳送圖片開始聊天

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###代碼使用離線模型 Cllama(llama.cpp)

以下是在程式碼中使用離線模型 llama.cpp 的說明。

首先，同樣需要將模型文件下載至 Content/LLAMA 目錄中。

修改程式碼以新增一條指令，並在該指令中向離線模型發送訊息。

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

經重新編譯後，在編輯器 Cmd 中使用命令，在日誌 OutputLog 中即可查看大型模型的輸出結果。

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###請使用離線模型llama.cpp來繪製藍圖。 

以下說明了如何在藍圖中使用離線模型 llama.cpp。

請在藍圖中按右鍵創建一個節點 `Send Cllama Chat Request`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

建立 Options 节点，並設定 `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

創建 Messages，分別添加一條系統訊息和用戶訊息

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

建立 Delegate 接受模型輸出的信息，並在屏幕上列印出來。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完整的藍圖看起來像這樣，運行藍圖，即可看到遊戲螢幕打印大型模型的回應訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###llama.cpp 使用 GPU

" Cllama Chat Request Options" 增加參數 "Num Gpu Layer" ，可以設定 llama.cpp 的 gpu payload，如圖。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

您可以使用藍圖節點來判斷當前環境是否支援 GPU，並獲取當前環境支持的後端。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_2.png)

###處理打包後 .Pak 中的模型檔案

在 Pak 打包完成後，專案中所有的資源檔案都會被放入 .Pak 檔案中，當然也包括離線模型的 gguf 檔案。

因為 llama.cpp 無法直接讀取 .Pak 文件，所以需要將 .Pak 文件中的離線模型文件複製到檔案系統中。

AIChatPlus 提供了一個功能函數可以自動將 .Pak 中的模型檔案複製處理，並放在 Saved 資料夾中：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

你也可以自行處理.Pak中的模型檔案，關鍵是需要將檔案複製處理，llama.cpp無法正確讀取.Pak。

## OpenAI

###編輯器使用 OpenAI 聊天

打開即時通訊工具 Tools -> AIChatPlus -> AIChat，創建新的聊天會話 New Chat，將會話 ChatApi 設置為 OpenAI，並設置接口參數。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

開始聊天：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

將模型切換為gpt-4o / gpt-4o-mini後，即可利用OpenAI的視覺功能分析圖片。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###編輯器使用 OpenAI 處理圖片（創建/修改/變種）

在聊天工具中建立新的圖像對話「New Image Chat」，將對話設置為 OpenAI，並設置參數。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

建立圖片

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

修改圖片，將對話圖片類型修改為編輯，然後上傳兩張圖片，一張是原始圖片，另一張是遮罩，其中透明的部分（alpha 通道為 0）表示需要修改的區域。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

將圖像變種，將圖片對話類型修改為變種，並上傳一張圖片，OpenAI 將返回原始圖片的一個變種。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###藍圖使用 OpenAI 模型聊天

在蓝图中右键创建一个节点 `在世界中发送 OpenAI 聊天请求`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

建立 Options 節點，並設置 `Stream=true, Api Key="你從 OpenAI 獲取的 API 金鑰"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

建立「訊息」，分別添加一則「系統訊息」和「使用者訊息」。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

建立 Delegate 接收模型輸出的資訊，並顯示在螢幕上。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完整的藍圖看起來像這樣，執行藍圖，即可看到遊戲畫面在列印大型模型返回的訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###藍圖使用 OpenAI 創建圖片

在藍圖中右鍵創建一個節點 `發送 OpenAI 圖片請求`，並設置 `輸入提示="一隻美麗的蝴蝶"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

建立選項節點，並設置 `Api Key="您從 OpenAI 獲得的 API 金鑰"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

綁定圖片上的事件，並將圖片保存到本地硬碟。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

完整的藍圖看起來是這樣的，運行藍圖，即可看到圖片保存在指定的位置上。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###編輯器使用 Azure

新建會話（New Chat），將 ChatApi 改為 Azure，並設置 Azure 的 API 參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###使用 Azure 建立圖片的編輯器

新建圖片對話（New Image Chat），將ChatApi改為Azure，並設置Azure的Api參數，注意，如果是dall-e-2模型，需要將參數Quality和Stype設置為not_use。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

開始聊天，請 Azure 創建圖片。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###請使用 Azure 聊天藍圖。

建立以下藍圖，設定好 Azure 選項，點擊執行，即可在螢幕上看到列印出來的 Azure 回傳聊天資訊。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###使用 Azure 建立藍圖图片。

建立以下藍圖，設定 Azure 選項，然後點擊運行。如果成功創建圖片，將在屏幕上看到 "Create Image Done" 的訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

根據上述藍圖設置，圖片將保存在路徑 D:\Dwnloads\butterfly.png

## Claude

###使用 Claude 聊天和分析圖片的編輯器

新建對話（New Chat），將 ChatApi 更改為 Claude，並設置 Claude 的 API 參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###使用 Claude 藍圖進行聊天與圖片分析。

在藍圖中右鍵建立一個節點 `Send Claude Chat Request`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

建立 Options 節點，並設置 `Stream=true, Api Key="來自 Clude 的您的 API 金鑰", Max Output Tokens=1024`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

建立 Messages，從檔案建立 Texture2D，再從 Texture2D 創建 AIChatPlusTexture，將 AIChatPlusTexture 加入到 Message 中。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

與上述教程相同，創建事件並將資訊印刷到遊戲螢幕上。

* 完整的藍圖看起來是這樣的，運行藍圖，即可看到遊戲屏幕在列印大型模型返回的訊息

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###獲取 Ollama

您可以透過 Ollama 官網取得安裝檔案，進行本地安裝：[ollama.com](https://ollama.com/)

可以使用其他人提供的Ollama API來使用Ollama。

###編輯器使用 Ollama 聊天和分析圖片

* 新增對話（New Chat），將 ChatApi 改為 Ollama，並設置 Ollama 的 API 參數。如果是文本聊天，則將模型設置為文字模型，如 llama3.1；如果需要處理圖片，則將模型設置為支援視覺的模型，例如 moondream。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###藍圖使用Ollama聊天和分析圖片。

建立以下藍圖，設定好 Ollama 選項，點擊執行，即可在螢幕上看到 Ollama 回傳的聊天資訊。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###編輯器使用 Gemini

新建會話（New Chat），將 ChatApi 修改為 Gemini，並設置 Gemini 的 Api 參數。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###使用Gemini編輯器發送音頻。

從檔案讀取音訊 / 從資產讀取音訊 / 從麥克風錄取音訊，生成需要傳送的音訊。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###使用 Gemini 聊天的藍圖

建立以下藍圖，設定好 Gemini 選項，點擊運行，即可在螢幕上看到 Gemini 返回的聊天信息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###使用Gemini发送音频的蓝图

建立以下藍圖，設置載入音訊，設定好 Gemini 選項，點擊執行，即可看到螢幕上列印 Gemini 處理音訊後返回的聊天資訊。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###編輯器使用 Deepseek

新建會話（New Chat），將 ChatApi 改為 OpenAi，並設置 Deepseek 的 Api 參數。新增 Candidate Models 叫做 deepseek-chat，並將 Model 設置為 deepseek-chat。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###使用 Deepseek 聊天藍圖

建立以下藍圖，設定 Deepseek 相關的 Request Options，包括 Model、Base Url、End Point Url、ApiKey 等參數。點擊執行，即可在螢幕上看到 Gemini 返回的聊天訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##額外提供的藍圖功能節點

###Cllama相關

"Cllama Is Valid"：判斷 Cllama llama.cpp 是否正確初始化

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu"：判斷 llama.cpp 在當前環境下是否支持 GPU backend

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"獲取支援 llama.cpp 的所有後端"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama Prepare ModelFile In Pak": 將 Pak 中的模型檔案準備好並複製到系統檔案中

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###圖像相關

將 UTexture2D 轉換為 Base64：將 UTexture2D 的圖像轉換為 PNG Base64 格式

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

將 UTexture2D 儲存為 .png 檔案

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

將 .png 檔案加載到 UTexture2D：讀取 png 檔案為 UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

複製 UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###音頻相關

將.wav檔案加載到USoundWave：將.wav檔案加載到USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

將.wav數據轉換為USoundWave：將wav二進制數據轉換為USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

將 USoundWave 儲存為 .wav 檔案

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

將 USoundWave 轉換為原始 PCM 資料

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

將USoundWave轉換為Base64格式。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicate USoundWave": 複製 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

將音訊擷取資料轉換為 USoundWave: 將音訊擷取資料轉換為 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

##更新日誌

### v1.6.0 - 2025.03.02

####新功能

將 llama.cpp 升級至 b4604 版本

Cllama支援GPU後端：cuda和metal

聊天工具 Cllama 支援 GPU 使用

支援讀取打包 Pak 中的模型檔案

#### Bug Fix

修復 Cllama 在推理時重新載入時會崩潰的問題

修復 iOS 編譯錯誤

### v1.5.1 - 2025.01.30

####新功能

僅允許 Gemini 發送音頻

優化獲取 PCMData 的方法，生成 B64 的時候再解壓縮音頻數據

要求增加兩個回呼 OnMessageFinished 和 OnImagesFinished。

優化 Gemini 方法，根據 bStream 自動獲取方法。

增加一些藍圖函數，方便將 Wrapper 轉換為實際類型，並獲取響應訊息和錯誤。

#### Bug Fix

修正要求完成多次調用的問題。

### v1.5.0 - 2025.01.29

####新功能

支援給 Gemini 送出音頻

編輯器工具支援發送音頻和錄音

#### Bug Fix

修復 Session copy 失敗的 bug

### v1.4.1 - 2025.01.04

####問題修復

聊天工具支援僅傳送圖片而不發送訊息。

修復 OpenAI 介面發送圖片問題失敗文件。

修補 OpanAI、Azure 聊天工具設置遺漏了參數 Quality、Style、ApiVersion 問題。

### v1.4.0 - 2024.12.30

####新功能

Cllama（llama.cpp）支援多模態模型，能處理圖片。

所有藍圖類型參數都有詳細提示。

### v1.3.4 - 2024.12.05

####新功能

OpenAI 支援視覺 API。

####問題修復

修復 OpenAI stream=false 時的錯誤

### v1.3.3 - 2024.11.25

####新功能

支持 UE-5.5

####問題修復

修復部分藍圖不生效問題

### v1.3.2 - 2024.10.10

####問題修復

修復手動停止 request 的時候 cllama 崩潰

修復商城下載版本win打包時找不到ggml.dll和llama.dll檔案的問題。

在創建請求時檢查是否在主線程中。

### v1.3.1 - 2024.9.30

####新功能

新增一個 SystemTemplateViewer，可查看和使用數百個系統設置模板。

####問題修復

修復從商城下載的插件，llama.cpp 找不到鏈接庫

修復 LLAMACpp 路徑過長問題

修復 Windows 打包後的連結 llama.dll 錯誤

修復 iOS/Android 讀取檔案路徑問題

修復 Cllame 設置名字錯誤

### v1.3.0 - 2024.9.23

####重大新功能

整合了 llama.cpp，支持本地離線執行大型模型。

### v1.2.0 - 2024.08.20

####新功能

支援 OpenAI 圖像編輯/圖像變化。

支援 Ollama API，並可自動取得 Ollama 支援的模型列表。

### v1.1.0 - 2024.08.07

####新增功能

支持藍圖

### v1.0.0 - 2024.08.05

####新功能

基礎完整功能

支持 OpenAI，Azure，Claude，Gemini

具備完善編輯功能的聊天工具

--8<-- "footer_tc.md"


> 此篇文章由 ChatGPT 翻譯完成，請在 [**反饋**](https://github.com/disenone/wiki_blog/issues/new)請指出任何遺漏之處。 
