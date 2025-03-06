---
layout: post
title: Get Started
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
description: Get Started
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Get Started" />

#C++ - Einleitung

##Einführung in den Kerncode

Derzeit ist das Plugin in folgende Module unterteilt:

AIChatPlusCommon: The runtime module, responsible for handling various AI API interface requests and parsing reply content.

AIChatPlusEditor: Editor-Modul (Editor), das für die Implementierung des AI-Chat-Tools des Editors verantwortlich ist.

AIChatPlusCllama: Run-time module (Runtime), responsible for encapsulating the interface and parameters of llama.cpp, enabling offline execution of large models.

Drittanbieter/LLAMACpp: Eine Laufzeitumgebung für Drittanbietermodule, die die dynamischen Bibliotheken und Header-Dateien von llama.cpp integriert.

Der `UClass`, der für den Versand von Anfragen zuständig ist, heißt `FAIChatPlus_xxxChatRequest`. Für jeden API-Dienst gibt es jeweils eine separate `Request UClass`. Die Antworten auf die Anfragen können über die `UAIChatPlus_ChatHandlerBase` / `UAIChatPlus_ImageHandlerBase` UClass abgerufen werden, indem die entsprechenden Rückruf-Delegaten registriert werden.

Vor dem Senden einer Anfrage müssen die Parameter und Nachrichten für die API konfiguriert werden. Dies wird durch die Verwendung von FAIChatPlus_xxxChatRequestBody festgelegt. Die spezifischen Informationen der Antwort werden ebenfalls im FAIChatPlus_xxxChatResponseBody analysiert und können über eine spezifische Schnittstelle abgerufen werden, wenn die Rückmeldung empfangen wird.

##Der Code verwendet das Offline-Modell Cllama (llama.cpp).

Die folgende Erklärung zeigt, wie man das Offline-Modell llama.cpp im Code verwendet.

Zunächst müssen Sie die Modelldatei auch im Ordner Content/LLAMA herunterladen.

Fügen Sie eine Befehlszeile im Code hinzu und senden Sie eine Nachricht an das Offline-Modell innerhalb des Befehls.

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

Nach dem Neukompilieren können Sie im Editor Cmd Befehle verwenden, um die Ausgabenergebnisse des großen Modells im Protokoll OutputLog zu sehen.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

--8<-- "footer_de.md"


> Dieser Beitrag wurde mithilfe von ChatGPT übersetzt. Bitte melden Sie sich unter [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Zeigen Sie alle Übersehenen. 
