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

#C++ Artikel - Erste Schritte

##Einführung in den Kerncode

Derzeit ist das Plugin in die folgenden Module unterteilt:

* **AIChatPlusCommon**: Runtime-Modul, das für die Verarbeitung von verschiedenen AI-API-Anfragen und die Analyse von Antwortinhalten zuständig ist.

* **AIChatPlusEditor**: Editor-Modul, das verantwortlich ist für die Implementierung des AI-Chat-Tools im Editor.

* **AIChatPlusCllama**: Laufzeitmodul, das die Schnittstelle und Parameter von llama.cpp kapselt und die Offline-Ausführung großer Modelle ermöglicht.

* **Thirdparty/LLAMACpp**: Ein Laufzeit-Drittanbietermodul (Runtime), das die dynamische Bibliothek und Header-Dateien von llama.cpp integriert.

Der UClass, der für das Senden von Anfragen verantwortlich ist, ist FAIChatPlus_xxxChatRequest. Jeder API-Dienst hat seinen eigenen separaten Request-UClass. Die Antworten auf Anfragen werden über die UClass UAIChatPlus_ChatHandlerBase/UAIChatPlus_ImageHandlerBase abgerufen. Es ist lediglich erforderlich, den entsprechenden Rückruf-Delegaten zu registrieren.

Bevor Sie eine Anfrage senden, müssen Sie zunächst die Parameter der API und die zu sendende Nachricht einstellen. Dies wird durch FAIChatPlus_xxxChatRequestBody festgelegt. Die spezifischen Inhalte der Antwort werden ebenfalls in FAIChatPlus_xxxChatResponseBody analysiert. Wenn Sie Rückmeldungen erhalten, können Sie über eine spezifische Schnittstelle auf den ResponseBody zugreifen.

##Der Code nutzt das Offline-Modell Cllama (llama.cpp).

Bitte verwende das Offline-Modell llama.cpp gemäß den folgenden Anweisungen im Code.

Zunächst müssen Sie die Modelldatei auch in den Ordner Content/LLAMA herunterladen.

Bearbeiten Sie den Code, fügen Sie einen Befehl hinzu und senden Sie eine Nachricht an das Offline-Modell im Befehl.

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


> Dieser Beitrag wurde von ChatGPT übersetzt. Bitte gib dein Feedback unter [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte zeigen Sie alle Auslassungen an. 
