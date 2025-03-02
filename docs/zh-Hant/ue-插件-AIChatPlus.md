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

##插件取得

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##插件簡介

此外，此外，支援 UE5.2+。

UE.AIChatPlus 是一個 UnrealEngine 外掛程式，實現了與各種 GPT AI 聊天服務進行通訊，目前支持的服務有 OpenAI (ChatGPT, DALL-E)，Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, llama.cpp 本地離線。未來還會繼續支持更多服務提供商。它的實現基於異步 REST 請求，性能高效，方便 UE 開發人員接入這些 AI 聊天服務。

同時 UE.AIChatPlus 還包含了一個編輯器工具，可以直接在編輯器中使用這些 AI 聊天服務，生成文本和圖像，分析圖像等。

##Instructions for use.

###編輯器聊天工具

菜单欄 Tools -> AIChatPlus -> AIChat 可以開啟插件提供的編輯器聊天工具

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


工具支持文字生成、文字聊天、圖像生成，以及圖像分析。

工具的介面大致為：

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####主要功能

離線大模型：整合了 llama.cpp 庫，支持本地離線執行大模型

請點擊左下角的 `新聊天` 按鈕，以建立新的文本聊天對話。

圖像生成：點擊左下角的 `New Image Chat` 按鈕，建立新的圖像生成會話。

* 圖像分析: `New Chat` 的部分聊天服務支援發送圖像，例如 Claude、Google Gemini。點擊輸入框上方的 🖼️ 或 🎨 按鈕即可載入需要發送的圖像。

支持藍圖（Blueprint）：支持藍圖建立 API 要求，從而實現文字聊天、圖像生成等功能。

設置當前聊天角色：聊天框上方的下拉框可以設置當前發送文字的角色，可以透過模擬不同的角色來調整 AI 聊天。

清空會話：點擊聊天框上方的 ❌ 圖標可以清空當前會話的聊天記錄。

對話模板：內建數百種對話設定模板，方便處理常見問題。

全局設置：點擊左下角的 `Setting` 按鈕，可以打開全局設置視窗。可以設置默認文本聊天、圖像生成的 API 服務，並設置每種 API 服務的具體參數。設置會自動保存在項目的路徑 `$(ProjectFolder)/Saved/AIChatPlusEditor` 下。

會話設置：點擊聊天框上方的設定按鈕，可以開啟當前會話的設置視窗。支援修改會話名稱，修改會話使用的API服務，支援獨立設定每個會話使用API的具體參數。會話設置自動保存在`$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`。

聊天內容修改：當游標懸停在聊天內容上時，將出現該聊天內容的設定按鈕，支持重新生成內容、修改內容、複製內容、刪除內容、在下方重新生成內容（對於角色是用戶的內容）。

圖像瀏覽：針對圖像生成，點擊圖像將打開圖像查看視窗（ImageViewer），支持圖片另存為 PNG/UE Texture，Texture 可以直接在內容瀏覽器（Content Browser）查看，方便圖片在編輯器內使用。另外還支持刪除圖片、重新生成圖片、繼續生成更多圖片等功能。針對 Windows 下的編輯器，還支持複製圖片，可以直接將圖片複製到剪貼板，方便使用。會話生成的圖片也會自動保存在每個會話文件夾下面，通常路徑是 `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`。

藍圖：

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

全局設置：

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

對話框設定:

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

AIChatPlusCommon: Runtime，負責處理各種 AI API 介面的發送請求和解析回覆內容。

AIChatPlusEditor: 編輯器模組（Editor），負責實現編輯器 AI 聊天工具。

AIChatPlusCllama：運行時模組（Runtime），負責封裝 llama.cpp 的介面和參數，實現離線執行大型模型

Thirdparty/LLAMACpp: Runtime 第三方模組，整合了 llama.cpp 的動態庫和頭文件。

負責發送請求的 UClass 是 FAIChatPlus_xxxChatRequest，每個 API 服務都有專屬的 Request UClass。回覆請求則通過 UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase 兩種 UClass 進行處理，只需要註冊相應的回調委派即可。

在發送請求之前，需要先設置好 API 的參數和要發送的訊息，這部分是透過 FAIChatPlus_xxxChatRequestBody 來設定的。回復的具體內容也會被解析到 FAIChatPlus_xxxChatResponseBody 中，當收到回調時，可以通過特定介面獲取 ResponseBody。

可以在UE商城獲取更多源碼細節：[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###編輯器工具使用離線模型 Cllama(llama.cpp)

以下說明如何在 AIChatPlus 編輯器工具中使用離線模型 llama.cpp

首先，從 HuggingFace 網站下載離線模型：[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

將模型放在特定資料夾中，例如將其放在遊戲項目目錄 Content/LLAMA 下。

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

打開 AIChatPlus 編輯器工具：工具 -> AIChatPlus -> AIChat, 新建聊天會話，並開啟會話設定頁面

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

將 Api 設置為 Cllama，啟用自定義 Api 設置，並新增模型搜索路徑，然後選擇模型。

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

開始聊天!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###使用離線模型 Cllama（llama.cpp）來處理圖片的編輯器工具。

從 HuggingFace 網站下載離線模型 MobileVLM_V2-1.7B-GGUF 同樣放到目錄 Content/LLAMA 下：[ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)與 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)。

設置對話模型：

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

傳送圖片開始聊天

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###程式碼使用離線模型 Cllama(llama.cpp)

以下是在程式碼中使用離線模型 llama.cpp 的說明。

首先，您也需要將模型檔案下載到 Content/LLAMA 資料夾中。

修改程式碼以新增一條指令，在該指令中向離線模型發送訊息。

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

經重新編譯後，在編輯器 Cmd 中使用指令，即可在日誌 OutputLog 中看到大型模型的輸出結果。

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###使用離線模型 llama.cpp 的藍圖

以下說明如何在藍圖中使用離線模型 llama.cpp

在藍圖中右鍵創建一個節點 `Send Cllama Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

建立 Options 節點，並設置 `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

建立消息，分別新增一則系統消息和用戶消息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

建立 Delegate 接收模型輸出的資訊，並在螢幕上列印出來。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完整的藍圖看起來就像這樣，執行藍圖後，你會看到遊戲畫面印出大型模型返回的訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###llama.cpp 使用 GPU

"Cllama Chat Request Options" 增加參數 "Num Gpu Layer" ，可以設置 llama.cpp 的 gpu payload，如圖

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

您可以使用藍圖節點來判斷當前環境是否支持 GPU，並獲取當前環境支持的後端：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_2.png)

###處理打包後 .Pak 中的模型文件

啟動 Pak 打包後，專案中的所有資源檔案都會被放在 .Pak 檔案中，當然也包含了離線模型 gguf 檔案。

由於 llama.cpp 無法直接讀取 .Pak 文件，因此需要將 .Pak 文件中的離線模型檔案複製到檔案系統中。

AIChatPlus 提供了一項功能，可以自動將 .Pak 中的模型檔案複製處理，並放在 Saved 資料夾中：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

或者您可以自行處理 .Pak 中的模型檔案，關鍵是需要將檔案複製處理，llama.cpp 無法正確讀取 .Pak。

## OpenAI

###編輯器使用 OpenAI 聊天

點開聊天工具 工具 -> AIChatPlus -> AIChat，建立新的聊天對話 New Chat，設置對話 ChatApi 為 OpenAI，設置介面參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

開始對話：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

將模型切換為GPT-4o/GPT-4o-mini後，可利用OpenAI的視覺功能進行圖片分析。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###編輯器使用 OpenAI 處理圖片（建立/修改/變更）

在聊天工具中建立新的圖片聊天，修改對話框設定為 OpenAI，並設定參數。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

建立圖片

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

修改圖片，將對話框 Image Chat Type 改為編輯，然後上傳兩張圖片，一張是原始圖片，另一張是其中透明位置的遮罩（alpha 通道為 0），表示需要進行修改的區域。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

將圖片變異，將Image Chat Type變更為Variation，並上傳一張圖片，OpenAI會回傳原圖片的一個變異。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###藍圖使用 OpenAI 模型聊天

在藍圖中右鍵創建一個節點 `Send OpenAI Chat Request In World`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

建立 Options 節點，並設置 `Stream=true, Api Key="您從 OpenAI 獲得的 API 金鑰"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

建立訊息，分別新增一則系統訊息和使用者訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

建立委託，接收模型輸出的資訊並顯示在螢幕上。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完整的藍圖看起來像這樣，運行藍圖，即可看到遊戲螢幕上打印大型模型返回的訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###使用OpenAI創建圖片的藍圖

在藍圖中右鍵創建一個節點 `Send OpenAI Image Request`，並設置 `In Prompt="a beautiful butterfly"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

建立 Options 節點，並設置 `Api Key="你從 OpenAI 獲取的 API 金鑰"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

綁定圖片點擊事件，並將圖片保存至本地硬碟上。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

完整的藍圖看起來像這樣，執行藍圖後，您可以看到圖片保存在指定的位置上。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###編輯器使用 Azure

新建會話（New Chat），將ChatApi改為Azure，並設置Azure的Api參數。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###使用 Azure 建立圖片的編輯器

建立新的圖片對話（New Image Chat），將 ChatApi 更改為 Azure，並設置 Azure 的 API 參數，請注意，如果使用 dall-e-2 模型，請將參數 Quality 和 Stype 設置為 not_use。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

開始聊天，請 Azure 創建圖片。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###使用 Azure 聊天中的藍圖

建立以下藍圖，設定好 Azure 選項，點擊運行，即可看到螢幕上列印出 Azure 回傳的聊天資訊。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###使用 Azure 建立圖片的藍圖

建立以下藍圖，設定 Azure 選項，點擊執行。若成功建立圖片，螢幕上將顯示「Create Image Done」訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

根據上面藍圖的設定，圖片將會保存在路徑 D:\Dwnloads\butterfly.png

## Claude

###使用Claude編輯器進行聊天和分析圖片。

建立新對話（New Chat），將ChatApi改為Claude，並設置Claude的API參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###使用Claude進行對話和圖片分析。

在藍圖中右鍵建立一個節點 `Send Claude Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

建立 Options 节点，並設置 `Stream=true, Api Key="you api key from Clude", Max Output Tokens=1024`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

建立 Messages，從檔案建立 Texture2D，並從 Texture2D 創建 AIChatPlusTexture，將 AIChatPlusTexture 加入訊息中。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

與上述教程相同，建立事件並將訊息輸出至遊戲畫面。

完整的藍圖看起來像這樣，執行藍圖，即可看到遊戲畫面打印出大模型返回的訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###獲取 Ollama

您可以透過 Ollama 官方網站取得安裝檔進行本機安裝：[ollama.com](https://ollama.com/)

可以使用他人提供的 Ollama 介面來使用 Ollama。

###編輯器使用 Ollama 聊天和分析圖片

創建新對話（New Chat），將 ChatApi 改為 Ollama，並設置 Ollama 的 API 參數。如果是文字聊天，則將模型設置為文字模型，例如 llama3.1；如果需要處理圖片，則將模型設置為支持視覺的模型，例如 moondream。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###使用 Ollama 平臺進行聊天和圖片分析。

建立以下藍圖，設定好 Ollama 選項，點擊執行，即可在螢幕上看到 Ollama 返回的聊天資訊。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###編輯器使用 Gemini

創建新對話（New Chat），將 ChatApi 改為 Gemini，並設置 Gemini 的 Api 參數。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###使用編輯器透過Gemini發送音頻。

從檔案讀取音訊 / 從資產讀取音訊 / 從麥克風錄取音訊，生成需要傳送的音訊。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###使用 Gemini 聊天藍圖

建立如下藍圖，設定好 Gemini Options，點擊運行，即可看到螢幕上列印 Gemini 返回的聊天訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###使用 Gemini 來發送音訊蓝图

請創建以下藍圖，設置載入音頻，設置好 Gemini 選項，點擊運行，即可看到屏幕上列印 Gemini 處理音頻後返回的聊天信息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###編輯器使用 Deepseek

建立新聊天室，將 ChatApi 修改為 OpenAi，並設置 Deepseek 的 Api 參數。新增候選模型名為 deepseek-chat，並將模型設置為 deepseek-chat。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###藍圖使用 Deepseek 聊天

建立以下藍圖，設定好 Deepseek 相關的 Request Options，包括 Model、Base Url、End Point Url、ApiKey 等參數。點擊執行，即可在螢幕上看到 Gemini 返回的聊天訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##額外提供的藍圖功能節點

###Cllama相關

"Cllama Is Valid"：判斷 Cllama llama.cpp 是否正常初始化

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

「Cllama Is Support Gpu」：判斷 llama.cpp 在當前環境下是否支持 GPU 後端。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

獲取 llma.cpp 支援的所有後端。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama Prepare ModelFile In Pak": 將 Pak 中的模型檔準備至檔案系統中。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###圖像相關

將 UTexture2D 轉換為 Base64：將 UTexture2D 圖像轉換為 png base64 格式

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

將 UTexture2D 儲存為 .png 檔案

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

將 .png 檔案加載到 UTexture2D：讀取 png 檔案為 UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

複製 UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###聲音相關

將 .wav 檔案載入至 USoundWave：讀取 wav 檔案為 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

將 .wav 數據轉換為 USoundWave：把 wav 二進制數據轉換為 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

將 USoundWave 儲存為 .wav 檔案

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

將 USoundWave 轉換為原始 PCM 數據

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

將 USoundWave 轉換為 Base64：將 USoundWave 轉換為 Base64 資料

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicate USoundWave": 複製 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

將音頻捕捉數據轉換為 USoundWave：將音頻捕捉數據轉換為 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

##更新日誌

### v1.6.0 - 2025.03.02

####新功能

將 llama.cpp 升級至 b4604 版本。
Cllama支援 GPU 後端：cuda 和 metal
聊天工具 Cllama 支持 GPU 使用
支援讀取打包 Pak 中的模型檔案

#### Bug Fix

修復 Cllama 在推理時重新載入時會崩潰的問題。

修復 iOS 編譯錯誤

### v1.5.1 - 2025.01.30

####新功能

僅允許雙子座發送音頻。

優化獲取 PCMData 的方法，生成 B64 的時候再解壓縮音頻數據

* 要求新增兩個回調函數 OnMessageFinished 和 OnImagesFinished

優化 Gemini Method，自動根據 bStream 獲取 Method

增加一些藍圖函數，方便轉換 Wrapper 到實際類型，並且獲取 Response Message 和 Error。

#### Bug Fix

修正 Request Finish 多次呼叫的問題

### v1.5.0 - 2025.01.29

####新功能

支援推送音頻到Gemini。

編輯器工具支持發送音頻和錄音

#### Bug Fix

修復會話複製失敗的臭蟲

### v1.4.1 - 2025.01.04

####問題修復

聊天工具支援僅發送圖片而不發送訊息。

修復 OpenAI 介面發送圖片問題失敗文件。

修復 OpanAI、Azure 聊天工具設定遺漏了參數 Quality、Style、ApiVersion 問題。

### v1.4.0 - 2024.12.30

####新功能

（實驗性功能）Cllama（llama.cpp）支持多模態模型，可以處理圖片

所有的藍圖類型參數都添加了詳細提示。

### v1.3.4 - 2024.12.05

####新功能

OpenAI 支援的視覺 API。

####問題修復

修復 OpenAI stream=false 時的錯誤

### v1.3.3 - 2024.11.25

####新功能

支援 UE-5.5

####問題修復

修復部分藍圖不生效問題。

### v1.3.2 - 2024.10.10

####問題修復

修復在手動停止 request 時 cllama 崩潰的問題。

修復商城下載版本 win 打包找不到 ggml.dll llama.dll 文件的問題

在创建请求時檢查是否在遊戲線程中。

### v1.3.1 - 2024.9.30

####新功能

新增一個 SystemTemplateViewer，可查看並使用數百個系統設定範本。

####問題修復

修 復 從 商 城 下 載 的 插 件，llama.cpp 找 不 到 連 結 庫

修復LLAMACpp路徑過長問題

修复 Windows 打包後的連結 llama.dll 錯誤

修復 iOS/Android 讀取檔案路徑問題

修正 Cllame 設定名稱錯誤

### v1.3.0 - 2024.9.23

####重大新功能

整合了 llama.cpp，支援本機離線執行大型模型。

### v1.2.0 - 2024.08.20

####新功能

支持 OpenAI 圖像編輯/圖像變換

支持 Ollama API，支持自動獲取 Ollama 支持的模型列表 

### v1.1.0 - 2024.08.07

####新功能

支持藍圖

### v1.0.0 - 2024.08.05

####新功能

基礎完整功能

支持 OpenAI，Azure，Claude，Gemini

* 具備完善編輯功能的聊天工具

--8<-- "footer_tc.md"


> 此貼文是由 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
