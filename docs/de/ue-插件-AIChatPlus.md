---
layout: post
title: UE Plugin AIChatPlus User Guide
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
description: UE Plugin AIChatPlus Documentation
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE 插件 AIChatPlus User Guide

##Öffentliches Lagerhaus

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Erweiterung erhalten

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Plugin-Einführung

Dieses Plugin unterstützt UE5.2+.

UE.AIChatPlus ist ein UnrealEngine-Plugin, das die Kommunikation mit verschiedenen GPT KI-Chat-Services ermöglicht. Aktuell werden Dienste wie OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama und llama.cpp lokal offline unterstützt. In Zukunft werden noch mehr Serviceanbieter hinzukommen. Die Implementierung basiert auf asynchronen REST-Anfragen, um eine effiziente Leistung zu gewährleisten und es Entwicklern in der UnrealEngine leicht zu machen, diese KI-Chat-Services zu integrieren.

UE.AIChatPlus enthält auch ein Editor-Tool, mit dem Sie direkt in dem Editor auf diese AI-Chat-Services zugreifen können, um Texte und Bilder zu erstellen, Bilder zu analysieren usw.

##Gebrauchsanweisung

###Editor Chat-Tool

Das Menü "Tools" -> "AIChatPlus" -> "AIChat" öffnet das Chat-Tool des Plugins.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


Das Tool unterstützt die Erstellung von Texten, Textchats, Bildgenerierung und Bildanalyse.

Die Benutzeroberfläche des Tools ist ungefähr wie folgt:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Hauptfunktion

Offline Big Model: Integration of the llama.cpp library to support local offline execution of big models.

Textnachricht: Klicken Sie auf die Schaltfläche `Neuer Chat` in der linken unteren Ecke, um eine neue Textnachricht zu erstellen.

Bildgenerierung: Klicken Sie auf die Schaltfläche "New Image Chat" unten links, um eine neue Bildgenerierungssitzung zu erstellen.

Bildanalyse: Einige Chat-Dienste in "New Chat" unterstützen das Senden von Bildern, wie z.B. Claude, Google Gemini. Klicken Sie einfach auf die Schaltfläche 🖼️ oder 🎨 über dem Eingabefeld, um das zu sendende Bild zu laden.

Unterstützung für Blaupausen (Blueprint): Unterstützung für die Erstellung von API-Anfragen über Blaupausen für Textchats, Bildgenerierung und andere Funktionen.

Legen Sie die aktuelle Chatrolle fest: Das Dropdown-Menü oben im Chat kann die Rolle festlegen, aus der der Text gesendet wird. Durch das Simulieren verschiedener Rollen kann der KI-Chat angepasst werden.

Leeren Sie den Chat: Klicken Sie auf das ❌-Symbol oben im Chatfenster, um den Verlauf des aktuellen Chats zu löschen.

Gesprächsvorlage: Hunderte von integrierten Gesprächsvorlagen erleichtern die Bearbeitung häufiger Probleme.

Global Settings: By clicking on the `Setting` button in the bottom left corner, you can open the global settings window. Here, you can configure default text chat, image generation API services, and specify parameters for each API service. The settings will be automatically saved in the project's path `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Konversations-Einstellungen: Klicke auf die Schaltfläche "Einstellungen" oben im Chatfenster, um das Einstellungsfenster der aktuellen Konversation zu öffnen. Hier kannst du den Konversationsnamen ändern, den für die Konversation verwendeten API-Dienst modifizieren und spezifische Parameter für jede Konversation festlegen. Die Konversations-Einstellungen werden automatisch unter `$(Projektordner)/Saved/AIChatPlusEditor/Sessions` gespeichert.

Ändern der Chat-Nachricht: Wenn Sie mit der Maus über den Chat-Inhalt fahren, wird eine Schaltfläche zur Nachrichteneinstellung angezeigt, die das Neugenerieren, Bearbeiten, Kopieren, Löschen und das Neuerzeugen des Inhalts unten (für benutzerbezogene Inhalte) unterstützt.

*Durchsuchen von Bildern: Wenn Sie ein Bild generieren, klicken Sie darauf, um das Bildanzeigefenster (ImageViewer) zu öffnen. Sie können das Bild im PNG/UE-Texturformat speichern, die Textur kann direkt im Inhaltsbrowser (Content Browser) angesehen werden, um Bilder bequem im Editor zu verwenden. Es gibt auch Funktionen zum Löschen von Bildern, Neugenerieren von Bildern und Fortfahren mit der Generierung weiterer Bilder. Für Editoren unter Windows wird auch das Kopieren von Bildern unterstützt, damit können Bilder direkt in die Zwischenablage kopiert werden, um sie bequem zu verwenden. Die generierten Bilder werden automatisch im Ordner jeder Sitzung gespeichert, normalerweise unter dem Pfad `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.*

Der Text lautet: "Die Blaupause:"

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Global Settings:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Gesprächseinstellungen:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Ändern Sie den Chatinhalt:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Bildbetrachter:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Verwendung von Offline-Großmodellen

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Dialogvorlage

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Einführung in den Kerncode

Derzeit unterteilt sich das Plugin in folgende Module:

AIChatPlusCommon: Das Runtime-Modul, das dafür zuständig ist, verschiedene AI-API-Anfragen zu verarbeiten und die Antwortinhalte zu analysieren.

AIChatPlusEditor: Editor-Modul, das die Implementierung des Editor-KI-Chat-Tools steuert.

AIChatPlusCllama: Runtime-Modul, das die Schnittstelle und Parameter von llama.cpp kapselt und die Offline-Ausführung großer Modelle ermöglicht.

Drittanbieter/LLAMACpp: Laufzeit-Drittanbietermodul (Runtime), das die dynamische Bibliothek und Header-Datei von llama.cpp integriert.

Der `UClass`, der für das Senden von Anfragen verantwortlich ist, ist `FAIChatPlus_xxxChatRequest`. Jeder API-Dienst hat seine eigene separate `Request UClass`. Die Antwort auf die Anfrage wird über `UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase` `UClass` erhalten, es ist nur erforderlich, die entsprechenden Rückruf-Delegaten zu registrieren.

Before sending a request, you need to set the parameters of the API and the message to be sent. This is done by using FAIChatPlus_xxxChatRequestBody. The specific content of the response is also parsed into FAIChatPlus_xxxChatResponseBody, and when receiving a callback, you can retrieve the ResponseBody through a specific interface.

Weitere Quelldetails sind im UE Store erhältlich: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Die Editor-Tools verwenden das Offline-Modell Cllama(llama.cpp).

The text translates into German as:

"Die folgende Anleitung zeigt, wie man das Offline-Modell llama.cpp im Editor-Tool AIChatPlus verwendet."

Zunächst einmal, laden Sie das Offline-Modell von der HuggingFace-Website herunter: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Legen Sie das Modell in einen bestimmten Ordner, beispielsweise im Verzeichnis Content/LLAMA des Spiels.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Öffnen Sie das AIChatPlus-Editor-Tool: Tools -> AIChatPlus -> AIChat, erstellen Sie eine neue Chat-Sitzung und öffnen Sie die Sitzungseinstellungen Seite.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Setzen Sie die API auf Cllama, aktivieren Sie die benutzerdefinierten API-Einstellungen, fügen Sie den Modell-Suchpfad hinzu und wählen Sie ein Modell aus.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Beginnen Sie mit der Unterhaltung!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Verwenden Sie das Offline-Modell Cllama (llama.cpp) im Editor-Tool zur Bildverarbeitung.

Laden Sie das Offline-Modell MobileVLM_V2-1.7B-GGUF von der HuggingFace-Website herunter und speichern Sie es im Verzeichnis Content/LLAMA als [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but I cannot provide a translation for non-textual content.

Setzen Sie das Modell der Sitzung:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Send a picture to start chatting.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###Der Code verwendet das Offline-Modell Cllama (llama.cpp).

Die folgende Erklärung zeigt, wie man das Offline-Modell llama.cpp im Code verwendet.

Zunächst müssen Sie die Modelldateien auch in den Ordner "Content/LLAMA" herunterladen.

Ändern Sie den Code, fügen Sie einen Befehl hinzu und senden Sie eine Nachricht an das Offline-Modell innerhalb des Befehls.

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

Nachdem Sie neu kompiliert haben, können Sie im Editor Cmd Befehle verwenden, um die Ausgabenergebnisse des großen Modells im Protokoll OutputLog zu sehen.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Bitte benutzen Sie das Offline-Modell Blueprint llama.cpp.

The following explains how to use the offline model llama.cpp in a blueprint.

In der Blaupause mit der rechten Maustaste einen Knoten namens `Send Cllama Chat Request` erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Erstellen Sie den Knoten "Options" und legen Sie `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"` fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Erstellen Sie Nachrichten, fügen Sie jeweils eine Systemnachricht und eine Benutzernachricht hinzu.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Erstellen Sie einen Delegaten, der Informationen aus dem Modell entgegennimmt und auf dem Bildschirm ausgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Eine vollständige Blaupause sieht so aus, führen Sie die Blaupause aus und Sie sehen die Nachricht, die auf dem Bildschirm erscheint, wenn das große Modell gedruckt wird. 

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###Die Datei llama.cpp nutzt die GPU.

"Cllama Chat Request Options" hat einen neuen Parameter "Num Gpu Layer" hinzugefügt, mit dem das GPU-Payload in llama.cpp konfiguriert werden kann, wie im Bild gezeigt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

Sie können mit Blueprints-Nodes überprüfen, ob die aktuelle Umgebung GPU unterstützt und die unterstützten Backends abrufen:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_2.png)

###Verarbeitung der Modelldateien in der .Pak-Datei.

Nach dem Aktivieren von Pak werden alle Ressourcendateien des Projekts in der .Pak-Datei gespeichert, einschließlich der Offline-Modell-GGUF-Datei.

Da llama.cpp kann keine direkte Unterstützung zum Lesen von .Pak-Dateien bieten, ist es notwendig, die Offline-Modelldateien aus der .Pak-Datei ins Dateisystem zu kopieren.

AIChatPlus bietet eine Funktion, die automatisch Modelldateien aus .Pak kopiert und in den Ordner "Saved" verschiebt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

Oder Sie können die Modelldateien in der .Pak-Datei selbst verarbeiten, das Hauptproblem liegt darin, dass die Dateien kopiert werden müssen, da llama.cpp die .Pak-Datei nicht korrekt lesen kann.

## OpenAI

###Der Editor verwendet OpenAI Chat.

Öffnen Sie das Chat-Tool Tools -> AIChatPlus -> AIChat, erstellen Sie eine neue Chat-Sitzung New Chat, setzen Sie die Sitzung ChatApi auf OpenAI, setzen Sie die Schnittstellenparameter.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Begin chatting:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Ändern Sie das Modell auf gpt-4o / gpt-4o-mini, um die Bildanalysefunktionen von OpenAI zu nutzen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###Der Editor verwendet OpenAI, um Bilder zu verarbeiten (erstellen/modifizieren/variieren).

Erstellen Sie in der Chat-App einen neuen Bild-Chat, ändern Sie die Chat-Einstellungen auf OpenAI und konfigurieren Sie die Parameter.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Erstellen von Bildern

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Ändern Sie das Bild, ändern Sie den Bild Chat Typ in "Bearbeiten" und laden Sie zwei Bilder hoch, eines ist das Originalbild und das andere ist das maskierte Bild, bei dem die transparenten Stellen (Alpha-Kanal 0) die zu bearbeitenden Bereiche anzeigen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Ändern Sie das Bildformat, ändern Sie den Bild-Chat-Typ in "[Variation]" und laden Sie ein Bild hoch. OpenAI wird eine Variante des Originalbildes zurückgeben.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Use OpenAI models to chat with Blueprint.

In der Blueprint einen Knoten mit der rechten Maustaste erstellen: `Send OpenAI Chat Request In World`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Erstellen Sie den Options-Knoten und legen Sie `Stream=true, Api Key="Ihr API-Schlüssel von OpenAI"` fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Erstellen Sie Nachrichten, fügen Sie jeweils eine Systemnachricht und eine Benutzernachricht hinzu.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Erstellen Sie einen Delegierten, der die Ausgabeinformationen des Modells annimmt und auf dem Bildschirm ausgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Eine vollständige Blaupause sieht so aus, führe die Blaupause aus und du wirst die Nachricht sehen, die auf dem Bildschirm erscheint, wenn das Spiel das große Modell druckt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Die Blaupause wurde mit OpenAI erstellt, um ein Bild zu erstellen.

In der Blaupause mit der rechten Maustaste einen Knoten mit dem Namen `Send OpenAI Image Request` erstellen und `In Prompt="a beautiful butterfly"` festlegen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Erstellen Sie den Options-Knoten und legen Sie `Api Key="Ihr API-Schlüssel von OpenAI"` fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Binden Sie das Ereignis "On Images" und speichern Sie das Bild auf der lokalen Festplatte.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

Eine vollständige Blaupause sieht so aus, wenn Sie die Blaupause ausführen, können Sie sehen, dass das Bild an einem festgelegten Ort gespeichert wird.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###Der Editor nutzt Azure.

Erstellen Sie einen neuen Chat, ändern Sie ChatApi auf Azure und konfigurieren Sie die Azure API-Parameter.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Beginnen wir mit der Unterhaltung.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###Der Editor erstellt Bilder mit Azure.

Erstellen Sie eine neue Bildunterhaltung (New Image Chat), tauschen Sie ChatApi gegen Azure aus und konfigurieren Sie die Azure API-Parameter. Beachten Sie, wenn das Modell dall-e-2 verwendet wird, müssen die Parameter Quality und Stype auf not_use eingestellt werden.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Beginnen Sie mit dem Chat und lassen Sie Azure ein Bild erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Blueprint verwenden Azure Chat

Erstellen Sie das folgende Schema, konfigurieren Sie die Azure Optionen, klicken Sie auf Ausführen und Sie werden die Chatnachrichten von Azure auf dem Bildschirm sehen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Erstellen Sie ein Bild mit Azure-Blueprints.

Erstellen Sie das folgende Blueprint, konfigurieren Sie die Azure-Optionen, klicken Sie auf Ausführen. Wenn das Bild erfolgreich erstellt wurde, wird die Meldung "Bild erstellt" auf dem Bildschirm angezeigt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

Basierend auf den Einstellungen des obigen   Entwurfs wird das Bild im Pfad D:\Downloads\butterfly.png gespeichert.

## Claude

###Der Editor verwendet Claude, um Bilder zu chatten und zu analysieren.

Erstellen Sie einen neuen Chat, ändern Sie ChatApi in Claude und konfigurieren Sie die API-Parameter von Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Beginnen Sie mit dem Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Translate these text into German language:

Der Plan verwendet Claude zum Chatten und Analysieren von Bildern.

In der Baupläne rechte Maustaste klicken und einen Knoten "Send Claude Chat Request" erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Erstellen Sie den Options-Knoten und legen Sie `Stream=true, Api Key="Ihr API-Schlüssel von Clude", Max Output Tokens=1024` fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Erstellen von Nachrichten, Erstellen von Texture2D aus einer Datei und Erstellen von AIChatPlusTexture aus Texture2D, um AIChatPlusTexture zur Nachricht hinzuzufügen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Wie im obigen Tutorial, erstellen Sie ein Ereignis und drucken Sie die Informationen auf den Bildschirm des Spiels.

Eine vollständige Blaupause sieht so aus. Wenn du die Blaupause ausführst, siehst du die Nachricht, die auf dem Bildschirm angezeigt wird, wenn das große Modell gedruckt wird.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Erhalten Sie Ollama.

Sie können die Installationsdatei direkt von der Ollama-Website herunterladen und lokal installieren: [ollama.com](https://ollama.com/)

Sie können Ollama über die von anderen bereitgestellte Ollama-Schnittstelle nutzen.

###Der Editor verwendet Ollama zum Chatten und Analysieren von Bildern.

Erstellen Sie ein neues Chatfenster, ändern Sie ChatApi in Ollama und konfigurieren Sie die Api-Parameter von Ollama. Wenn es sich um einen Text-Chat handelt, setzen Sie das Modell auf ein Textmodell wie llama3.1. Wenn Bilder verarbeitet werden müssen, wählen Sie ein Modell aus, das Bildverarbeitung unterstützt, beispielsweise moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Beginnen Sie mit dem Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Das bedeutet "Blueprints verwenden Ollama zum Chatten und Analysieren von Bildern"

Erstellen Sie die folgende Blaupause, konfigurieren Sie die Ollama-Optionen, klicken Sie auf Ausführen, um die Chat-Nachrichten zu sehen, die Ollama auf dem Bildschirm ausgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###Der Editor verwendet Gemini.

Erstellen Sie einen neuen Chat, ändern Sie ChatApi in Gemini und konfigurieren Sie die API-Parameter von Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Beginne den Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###Der Editor nutzt Gemini, um Audiodateien zu versenden.

Wählen Sie aus, ob Sie Audio aus einer Datei lesen, aus einer Ressource lesen oder über ein Mikrofon aufnehmen möchten, um das benötigte Audio für den Versand zu erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

Beginne den Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###Verwenden Sie in der Blaupause die Gemini-Chatfunktion.

Erstellen Sie das folgende Schema, konfigurieren Sie die Gemini-Optionen, klicken Sie auf Ausführen und Sie werden die Chat-Informationen sehen, die Gemini auf dem Bildschirm ausgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###Blueprint verwendet Gemini, um Audio zu senden.

Erstellen Sie die folgende Blaupause, konfigurieren Sie das Laden von Audio, konfigurieren Sie die Gemini-Optionen, klicken Sie auf Ausführen und Sie sehen die Chat-Nachrichten von Gemini nach der Audiobearbeitung auf dem Bildschirm gedruckt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###Der Editor verwendet Deepseek.

Erstellen Sie einen neuen Chat, ersetzen Sie ChatApi durch OpenAi und konfigurieren Sie die API-Parameter von Deepseek. Fügen Sie das Kandidatenmodell mit dem Namen deepseek-chat hinzu und setzen Sie das Modell auf deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Beginnen Sie zu chatten

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Please provide the text you would like me to translate.

Erstellen Sie das folgende Schema und konfigurieren Sie die Deepseek-bezogenen Anforderungsoptionen, einschließlich Modell, Basis-URL, Endpunkt-URL, ApiKey und andere Parameter. Klicken Sie auf Ausführen, um die Chatnachrichten von Gemini auf dem Bildschirm angezeigt zu bekommen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##Zusätzlich bereitgestellte Blaupausen-Funktionsknoten

###Cllama related

"Cllama Is Valid": Überprüfen, ob Cllama llama.cpp ordnungsgemäß initialisiert ist.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu" wird übersetzt zu "Entscheiden Sie, ob llama.cpp die GPU-Backend in der aktuellen Umgebung unterstützt".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Holen Sie sich Support-Backends von Cllama": Fetch alle Backends, die von llama.cpp unterstützt werden.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama Prepare ModelFile In Pak": Automatische Kopie von Modelldateien aus Pak in das Dateisystem.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###Bildbezogen

"Konvertieren Sie UTexture2D in Base64": Konvertieren Sie das Bild von UTexture2D in das PNG-Base64-Format.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

"Speichern Sie UTexture2D als .png-Datei": Speichern Sie UTexture2D als .png-Datei

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

"Lade die .png-Datei in UTexture2D"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Duplicate UTexture2D": Dupliziere UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###Audio related

"Laden Sie die .wav-Datei in USoundWave."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

Konvertiere die .wav-Daten in USoundWave: Convert .wav data to USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

"Speichern Sie USoundWave als .wav-Datei"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

"Holen Sie sich USoundWave Raw PCM-Daten": Convert USoundWave into binary audio data.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"USoundWave in Base64 umwandeln": "Convertiere USoundWave in Base64"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Dupliziere USoundWave": Dupliziere USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

Konvertieren Sie die Audioaufzeichnungsdaten in einen USoundWave.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

##Aktualisierungsprotokoll

### v1.6.0 - 2025.03.02

####Neue Funktion

llama.cpp upgraded to version b4604.
Cllama supports GPU backends: cuda and metal.
Das Chat-Tool Cllama unterstützt die Verwendung von GPUs.
Unterstützung zum Lesen von Modelldateien im Paket Pak.

#### Bug Fix

Fix the problem of Cllama crashing when reloading during reasoning.

Fix iOS compilation error.

### v1.5.1 - 2025.01.30

####Neue Funktion

Erlauben Sie nur Gemini, Audio abzuspielen.

Optimieren Sie die Methode zum Abrufen von PCM-Daten, und dekomprimieren Sie die Audiodaten beim Generieren von B64.

Bitte fügen Sie zwei Callbacks hinzu: OnMessageFinished und OnImagesFinished.

Optimiere die Gemini-Methode, um automatisch die Methode über bStream zu erhalten. 

Fügen Sie einige Blueprint-Funktionen hinzu, um Wrapper in tatsächliche Typen umzuwandeln und Response Message und Error abzurufen.

#### Bug Fix

Beheben Sie das Problem mit mehrfachen Aufrufen von Request Finish.

### v1.5.0 - 2025.01.29

####Neue Funktion.

Unterstützung für die Bereitstellung von Audio für Gemini.

Die Editor-Tools unterstützen den Versand von Audio und Aufnahmen.

#### Bug Fix

Beheben Sie den Fehler beim Kopieren der Sitzung.

### v1.4.1 - 2025.01.04

####Problembehebung

Die Chat-App unterstützt das Senden von Bildern ohne Text.

Behebung des Problems beim Senden von Bildern über die OpenAI-Schnittstelle fehlgeschlagen.

Fix für das Problem, dass beim Einrichten der OpanAI- und Azure-Chat-Tools die Parameter Qualität, Stil und API-Version fehlen.

### v1.4.0 - 2024.12.30

####Neue Funktion

（Experimental feature）Cllama (llama.cpp) supports multimodal models and can process images.

Alle Blaupausen-Typenparameter wurden mit ausführlichen Hinweisen versehen.

### v1.3.4 - 2024.12.05

####Neue Funktion

OpenAI unterstützt die Vision API.

####Problembehebung

Beheben Sie den Fehler bei OpenAI stream=false.

### v1.3.3 - 2024.11.25

####Neue Funktion

Unterstützt UE-5.5.

####Fehlerbehebung

Fixing the issue where some blueprints are not working.

### v1.3.2 - 2024.10.10

####Problembehebung

Reparatur: Absturz von cllama beim manuellen Stoppen des Requests.

Fix das Problem beim Packen des Win-Downloads im Shop, bei dem die ggml.dll- und llama.dll-Dateien nicht gefunden werden konnten.

Überprüfen Sie beim Erstellen der Anfrage, ob sich der GameThread befindet.

### v1.3.1 - 2024.9.30

####Neue Funktion

Erstellen Sie einen SystemTemplateViewer, um Hunderte von Systemeinstellungs-Vorlagen anzuzeigen und zu verwenden.

####Problembehebung

Beheben Sie das Problem mit dem Plugin, das aus dem App Store heruntergeladen wurde. Llama.cpp konnte die Verbindungsbibliothek nicht finden.

Behebung des Problems mit zu langen Pfaden in LLAMACpp.

Beheben Sie den Fehler der Verknüpfung llama.dll nach dem Windows-Paketieren.

Behebung des Problems bei der Dateipfad-Lesevorgänge auf iOS/Android.

* Beheben Sie den Fehler beim Einstellen des Namens Cllame

### v1.3.0 - 2024.9.23

####Wichtige neue Funktion

Integriert llama.cpp für die lokale Offline-Ausführung großer Modelle.

### v1.2.0 - 2024.08.20

####Neue Funktion

Unterstützung für OpenAI Image Edit/Image Variation.

Unterstützt die Ollama API und ermöglicht das automatische Abrufen der Liste der von Ollama unterstützten Modelle.

### v1.1.0 - 2024.08.07

####Neue Funktion

Unterstützung der Blaupause

### v1.0.0 - 2024.08.05

####Neue Funktion

Grundlegende Vollfunktion

Unterstützung für OpenAI, Azure, Claude, Gemini.

Integriertes Tool für umfassende Editor-Chat-Funktionen

--8<-- "footer_de.md"


> (https://github.com/disenone/wiki_blog/issues/new)Bitte weisen Sie auf alle ausgelassenen Stellen hin. 
