---
layout: post
title: UE 插件 AIChatPlus 說明文檔
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

本插件支持 UE5.2 以上版本。

UE.AIChatPlus 是一個 UnrealEngine 插件，該插件實現了與各種 GPT AI 聊天服務進行通信，目前支持的服務有 OpenAI (ChatGPT, DALL-E)、Azure OpenAI (ChatGPT, DALL-E)、Claude、Google Gemini、Ollama、llama.cpp 本地離線。未來還會繼續支持更多服務提供商。它的實現基於非同步 REST 請求，性能高效，方便 UE 開發人員接入這些 AI 聊天服務。

同時 UE.AIChatPlus 還包含了一個編輯器工具，可以直接在編輯器中使用這些 AI 聊天服務，生成文本和圖像，分析圖像等。

##使用說明

###編輯器聊天工具

菜單欄 Tools -> AIChatPlus -> AIChat 可打開插件提供的編輯器聊天工具

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


工具支持文本生成、文本聊天、圖像生成，圖像分析。

工具的界面大致為：

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####主要功能

* 離線大模型：整合了 llama.cpp 庫，支持本地離線執行大模型

* 文本聊天：點擊左下角的 `New Chat` 按鈕，創建新的文本聊天會話。

* 圖像生成：點擊左下角的 `New Image Chat` 按鈕，創建新的圖像生成會話。

* 圖像分析：`New Chat` 的部分聊天服務支持發送圖像，例如 Claude, Google Gemini。點擊輸入框上方的 🖼️ 或 🎨 按鈕即可加載需要發送的圖像。

* 支持藍圖 (Blueprint)：支持藍圖創建 API 請求，完成文本聊天，圖像生成等功能。

* 設定當前聊天角色：聊天框上方的下拉框可以設定當前發送文本的角色，可以通過模擬不同的角色來調整 AI 聊天。

* 清空會話：聊天框上方的 ❌ 按鈕可以清空當前會話的歷史消息。

對話模板：內建數百種對話設定模板，便於處理常見問題。

全局設置：點擊左下角的 `Setting` 按鈕，可以打開全局設置窗口。可以設置默認文本聊天，圖像生成的 API 服務，並設置每種 API 服務的具體參數。設置會自動保存在項目的路徑 `$(ProjectFolder)/Saved/AIChatPlusEditor` 下。

* 會話設定：點擊聊天框上方的設定按鈕，可以打開當前會話的設定窗口。支持修改會話名稱，修改會話使用的 API 服務，支持獨立設定每個會話使用 API 的具體參數。會話設定會自動保存在 `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions`

對話內容修改：當滑鼠懸停在對話內容上時，會出現一個設定按鈕，可以重新生成內容、修改內容、複製內容、刪除內容，以及在下方重新生成內容（針對使用者訊息的角色）。

* 圖像瀏覽：對於圖像生成，點擊圖像會打開圖像查看窗口 (ImageViewer)，支持圖片另存為 PNG/UE Texture，Texture 可以直接在內容瀏覽器 (Content Browser) 查看，方便圖片在編輯器內使用。另外還支持刪除圖片、重新生成圖片、繼續生成更多圖片等功能。對於 Windows 下的編輯器，還支持複製圖片，可以直接把圖片複製到剪貼板，方便使用。會話生成的圖片也會自動保存在每個會話文件夾下面，通常路徑是 `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`。

藍圖：

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

全局設定：

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

對話框設定：

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

修改聊天內容：

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

圖像查看器：

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

使用離線大模型

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

對話模板

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###核心程式碼介紹

目前插件分成以下幾個模組：

* AIChatPlusCommon: 運行時模塊（Runtime），負責處理各種 AI API 接口發送請求和解析回覆內容。

AIChatPlusEditor: 編輯器模組（Editor）， 負責實現編輯器 AI 聊天工具。

AIChatPlusCllama: 運行時模組（Runtime），負責封裝 llama.cpp 的介面和參數，實現離線執行大型模型

* Thirdparty/LLAMACpp: 運行時第三方模組 (Runtime)，整合了 llama.cpp 的動態庫和頭文件。

具體負責發送請求的 UClass 是 FAIChatPlus_xxxChatRequest，每種 API 服務都有獨立的 Request UClass。請求的回覆通過 UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase 兩種 UClass 來獲取，只需要註冊相應的回調委託。

在發送請求之前，需要先設定好 API 的參數和要發送的訊息，這部分是透過 FAIChatPlus_xxxChatRequestBody 來設定的。而具體的回覆內容則會被解析至 FAIChatPlus_xxxChatResponseBody 中，當接收到回調時，可以透過特定介面來取得 ResponseBody。

您可以在UE商城获取更多源码细节：[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###編輯器工具使用離線模型 Cllama(llama.cpp)

請參考以下方式在 AIChatPlus 編輯器工具中使用離線模型 llama.cpp。

* 首先，從 HuggingFace 網站下載離線模型：[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

將模型放置在特定的資料夾中，例如將其放置在遊戲專案目錄 Content/LLAMA 下。

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

打開 AIChatPlus 編輯器工具：工具 -> AIChatPlus -> AIChat，新建聊天會話，並打開會話設置頁面。

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

將 API 設置為 Cllama，開啟自定義 API 設置，加入模型搜索路徑並選擇模型。

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

* 開始聊天！！

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###編輯器工具使用離線模型 Cllama(llama.cpp) 處理圖片

* 從 HuggingFace 網站下載離線模型 MobileVLM_V2-1.7B-GGUF，同樣放到目錄 Content/LLAMA 下：[ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)。

設置會話的模型:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

傳送圖片開始聊天

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###代碼使用離線模型 Cllama(llama.cpp)

以下說明如何在程式碼中使用離線模型 llama.cpp

首先，同樣需要將模型文件下載至Content/LLAMA中。

* 修改程式碼新增一條命令，並在命令內給離線模型發送消息

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

重新編譯後，在編輯器 Cmd 中使用命令，便可在日誌 OutputLog 中看到大模型的輸出結果。

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###藍圖使用離線模型 llama.cpp

以下是如何在藍圖中使用離線模型 llama.cpp。

* 在藍圖中右鍵建立一個節點 `Send Cllama Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

建立 Options 节点，並設定 `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

建立訊息，分別新增系統訊息和使用者訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

建立委派以接收模型輸出的信息，並在螢幕上顯示。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* 完整的藍圖看起來是這樣的，運行藍圖，即可看到遊戲螢幕在打印大模型返回的消息

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###編輯器使用 OpenAI 聊天

打開聊天工具 工具 -> AIChatPlus -> AIChat，創建新的聊天會話 新聊天，設置會話 ChatApi 為 OpenAI，設置接口參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

開始聊天：

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

* 切換模型為 gpt-4o / gpt-4o-mini，可以使用 OpenAI 的視覺功能分析圖片

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###編輯器使用 OpenAI 處理圖片（創建/修改/變種）

在聊天工具中建立新的圖像對話 New Image Chat，修改對話設定為 OpenAI，並設定參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

建立圖片

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

* 修改圖片，把會話 Image Chat Type 修改為 Edit，並上傳兩張圖片，一張是原圖片，一張是 mask 其中透明的位置（alpha 通道為 0）表示需要修改的地方。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

將圖片變體中的「Image Chat Type」修改為「變異」，然後上傳一張圖片，OpenAI 會回傳原圖片的一個變體。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###使用 OpenAI 模型進行對話。

* 在藍圖中右鍵創建一個節點 `Send OpenAI Chat Request In World`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

* 創建 Options 節點，並設置 `Stream=true, Api Key="你從 OpenAI 獲得的 API 金鑰"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

* 創建 Messages，分別添加一條 System Message 和 User Message

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* 創建 Delegate 以接收模型輸出的資訊，並在螢幕上列印。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

完整的藍圖看起來是這樣的，運行藍圖，即可看到遊戲螢幕在列印大模型返回的訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###藍圖使用 OpenAI 創建圖片

在藍圖中右鍵創建一個節點 `Send OpenAI Image Request`，並設置 `In Prompt="a beautiful butterfly"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

建立 Options 节点，並設定 `Api Key="you api key from OpenAI"`。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

* 綁定圖像事件，並將圖片保存到本地硬盤上

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

完整的藍圖看起來是這樣的，運行藍圖，即可看到圖片保存在指定的位置上。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###編輯器使用 Azure

* 新建會話（New Chat），將 ChatApi 改為 Azure，並設置 Azure 的 Api 參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###使用 Azure 建立圖片的編輯器

* 新建圖片會話（New Image Chat），將 ChatApi 改為 Azure，並設定 Azure 的 Api 參數，注意，如果是 dall-e-2 模型，需要將參數 Quality 和 Stype 設定為 not_use。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

* 開始聊天，讓 Azure 創建圖片

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###使用Azure Chat的藍圖

創建如下藍圖，設置好 Azure 選項，點擊運行，即可看到屏幕上打印 Azure 返回的聊天信息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###使用 Azure 建立圖像的藍圖

建立以下藍圖，設定好 Azure 選項，點擊運行，如果成功建立圖片，將在螢幕上看到訊息「建立圖片完成」。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

根據上面的藍圖設定，圖片會保存在路徑 D:\Dwnloads\butterfly.png

## Claude

###編輯器使用 Claude 聊天和分析圖片

* 新建會話（New Chat），把 ChatApi 改為 Claude，並設置 Claude 的 Api 參數

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

* 開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###藍圖使用 Claude 聊天和分析圖片

* 在藍圖中右鍵創建一個節點 `Send Claude Chat Request`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

* 創建 Options 節點，並設置 `Stream=true, Api Key="your api key from Clude", Max Output Tokens=1024`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

建立 Messages，從檔案建立 Texture2D，然後從 Texture2D 創建 AIChatPlusTexture，將 AIChatPlusTexture 加入到訊息中。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

* 跟上述教程一樣，創建 Event 並把信息印出到遊戲畫面上

完整的藍圖看起來是這樣的，運行藍圖，即可看到遊戲屏幕在打印大模型返回的消息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###獲取 Ollama

* 可以通过 Ollama 官方网站获取安装包进行本地安装：[ollama.com](https://ollama.com/)

你可以使用其他人提供的 Ollama 接口來使用 Ollama。

###編輯器使用 Ollama 聊天和分析圖片

* 新建會話（New Chat），將 ChatApi 改為 Ollama，並設置 Ollama 的 Api 參數。如果是文本聊天，則設置模型為文本模型，如 llama3.1；如果需要處理圖片，則設置模型為支持視覺的模型，例如 moondream。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###藍圖使用 Ollama 聊天和分析圖片

建立以下藍圖，設置好Ollama選項，點擊運行，即可看到螢幕上打印Ollama返回的聊天訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###編輯器使用 Gemini

新增對話（New Chat），將ChatApi改為Gemini，並設置Gemini的Api參數。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

* 開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###編輯器使用 Gemini 發送音頻

* 選擇 從檔案讀取音訊 / 從資產讀取音訊 / 從麥克風錄製音訊，生成需要發送的音訊

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

* 開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###藍圖運用 Gemini 聊天

創建如下藍圖，設置好 Gemini Options，點擊運行，即可看到屏幕上打印 Gemini 返回的聊天信息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###使用Gemini藍圖傳送音訊。

創建如下藍圖，設置加載音頻，設置好 Gemini Options，點擊運行，即可看到螢幕上打印 Gemini 處理音頻後返回的聊天信息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###編輯器使用 Deepseek

新建會話（New Chat），將 ChatApi 改為 OpenAi，並設置 Deepseek 的 Api 參數。新增 Candidate Models 叫做 deepseek-chat，並將 Model 設置為 deepseek-chat。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

開始聊天

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###藍圖使用 Deepseek 聊天

建立以下藍圖，設定Deepseek相關的Request選項，包括Model、Base Url、End Point Url、ApiKey等參數。點擊運行，即可看到螢幕上顯示Gemini回傳的聊天訊息。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##更新日誌

### v1.5.1 - 2025.01.30

####新功能

* 只允許 Gemini 發音頻

* 優化獲取 PCMData 的方法，生成 B64 的時候再解壓縮音頻數據

請求增加兩個回調 OnMessageFinished 和 OnImagesFinished

* 優化 Gemini 方法，自動根據 bStream 獲取方法

增加一些藍圖函式，方便將 Wrapper 轉換為實際類型，並取得回應訊息和錯誤。

#### Bug Fix

修復 Request Finish 多次調用問題

### v1.5.0 - 2025.01.29

####新功能

支援 Gemini 的音頻发放。

編輯器工具支援發送音訊和錄音。

#### Bug Fix

修復 Session copy 失敗的 bug

### v1.4.1 - 2025.01.04

####問題修復

聊天工具支持只發圖片不發信息

* 修復 OpenAI 接口發送圖片問題失敗文圖

* 修復 OpanAI、Azure 聊天工具設置漏掉了參數 Quality、Style、ApiVersion 的問題=

### v1.4.0 - 2024.12.30

####新功能

（實驗性功能）Cllama（llama.cpp）支援多模態模型，可以處理圖片

* 所有的藍圖類型參數都加上了詳細提示

### v1.3.4 - 2024.12.05

####新功能

OpenAI 支持視覺 API。

####問題修復

修復 OpenAI stream=false 時的錯誤

### v1.3.3 - 2024.11.25

####新功能

* 支援 UE-5.5

####問題修復

* 修復部分藍圖不生效問題

### v1.3.2 - 2024.10.10

####問題修復

* 修復手動停止請求時的 cllama 崩潰問題

* 修復商城下載版本 win 打包找不到 ggml.dll llama.dll 檔案的問題

* 創建請求時檢查是否在遊戲線程中，CreateRequest 需在遊戲線程中檢查

### v1.3.1 - 2024.9.30

####新功能

新增一個 SystemTemplateViewer，可供查看和使用數百個系統設定範本。

####問題修復

* 修復從商城下載的插件，llama.cpp 找不到連結庫

* 修復 LLAMACpp 路徑過長問題

* 修復 windows 打包後的連結 llama.dll 錯誤

* 修復 ios/android 讀取檔案路徑問題

修復 Cllame 設定名稱錯誤

### v1.3.0 - 2024.9.23

####重要新功能

* 整合了 llama.cpp，支持本地離線執行大模型

### v1.2.0 - 2024.08.20

####新功能

支援 OpenAI 圖像編輯/圖像變化

* 支援 Ollama API，支持自動獲取 Ollama 支援的模型列表

### v1.1.0 - 2024.08.07

####新功能

支持藍圖

### v1.0.0 - 2024.08.05

####新功能

基礎完整功能

支持 OpenAI，Azure，Claude，Gemini

* 自帶功能完善的編輯器聊天工具

--8<-- "footer_tc.md"


> 此帖子是使用 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)請指出任何遺漏之處。 
