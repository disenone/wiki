---
layout: post
title: UE Plugin AIChatPlus Benutzerhandbuch
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
description: UE Plugin AIChatPlus User Guide
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE-Plugin AIChatPlus User Guide

##Öffentliches Lagerhaus

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Plugin erhalten

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Plugin-Beschreibung

This plugin supports UE5.2+.

UE.AIChatPlus ist ein UnrealEngine-Plugin, das die Kommunikation mit verschiedenen GPT KI-Chat-Diensten ermöglicht. Derzeit werden Dienste von OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama und lokale Offline-Dienste von llama.cpp unterstützt. In Zukunft werden noch mehr Dienstanbieter integriert. Die Implementierung basiert auf asynchronen REST-Anfragen, was eine effiziente Leistung ermöglicht und es Entwicklern in UE erleichtert, auf diese KI-Chat-Dienste zuzugreifen.

UE.AIChatPlus enthält auch ein Editor-Tool, mit dem Sie diese KI-Chat-Services direkt im Editor verwenden können, um Texte und Bilder zu erstellen, Bilder zu analysieren usw.

##Bedienungsanleitung

###Editor-Chat-Tool

Das Menü Tools -> AIChatPlus -> AIChat öffnet den Editor für den Chat-Tool, der von dem Plugin bereitgestellt wird.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


Das Tool unterstützt Textgenerierung, Textchat, Bildgenerierung und Bildanalyse.

Die Benutzeroberfläche des Tools ist ungefähr wie folgt:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Main functions.

Offline Large Model: Integration of llama.cpp library, supporting local offline execution of large models.

Textchat: Klicke auf die Schaltfläche "Neuer Chat" unten links, um eine neue Textchat-Sitzung zu erstellen.

Bildgenerierung: Klicken Sie auf die Schaltfläche "Neues Bild-Chat" in der linken unteren Ecke, um eine neue Bildgenerierungssitzung zu erstellen.

Bildanalyse: Einige Chat-Dienste von `New Chat` unterstützen das Senden von Bildern, wie zum Beispiel Claude, Google Gemini. Klicken Sie einfach auf die Schaltfläche 🖼️ oder 🎨 über dem Eingabefeld, um das zu sendende Bild zu laden.

Unterstützung von Blueprints: Unterstützung bei der Erstellung von Blueprints für API-Anfragen zur Durchführung von Funktionen wie Text-Chat und Bildgenerierung.

Bitte diesen Text ins Deutsche übersetzen:

* Wählen Sie die aktuelle Chat-Rolle aus: Das Dropdown-Menü oben im Chatfenster ermöglicht es, die Rolle festzulegen, unter der der Text gesendet wird. Auf diese Weise kann die AI-Chat-Kommunikation durch das Simulieren verschiedener Rollen angepasst werden.

Leeren des Chats: Durch Klicken auf das ❌-Symbol oben im Chatfenster können Sie den Verlauf der aktuellen Unterhaltung leeren.

Dialogtemplate: Hunderte von integrierten Dialogvorlagen erleichtern die Bearbeitung häufiger Anliegen.

Global settings: By clicking the 'Settings' button in the bottom left corner, you can open the global settings window. Here, you can adjust default text chat, image generation API services, and specify parameters for each API service. The settings will be automatically saved in the project directory `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Konversations-Einstellungen: Durch Klicken auf die Schaltfläche "Einstellungen" oben im Chat-Feld können Sie das Einstellungsfenster für die aktuelle Konversation öffnen. Es ermöglicht das Ändern des Konversationsnamens, des verwendeten API-Dienstes und das eigenständige Festlegen spezifischer Parameter für die API-Nutzung in jeder Konversation. Die Konversations-Einstellungen werden automatisch im Ordner `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions` gespeichert.

Ändern des Chat-Inhalts: Wenn Sie mit der Maus über den Chat-Inhalt fahren, wird ein Einstellungsknopf für den jeweiligen Chat-Inhalt angezeigt. Sie können den Inhalt neu generieren, ändern, kopieren, löschen oder unterhalb des Inhalts neu generieren (für Benutzerinhalte).

Bildanzeige: Klicken Sie auf ein Bild, um das Bildbetrachtungsfenster (ImageViewer) zu öffnen. Unterstützt das Speichern von Bildern als PNG/UE Texture und das Anzeigen von Texturen im Inhaltsbrowser (Content Browser) für eine einfache Verwendung im Editor. Es bietet auch Funktionen wie das Löschen von Bildern, das Neuerstellen von Bildern und das Generieren weiterer Bilder. Für den Editor unter Windows wird auch das Kopieren von Bildern unterstützt, um sie direkt in die Zwischenablage zu kopieren und bequem zu verwenden. Die generierten Bilder werden automatisch im Ordner jeder Sitzung gespeichert, normalerweise unter dem Pfad `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Blueprint:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Globale Einstellungen:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Konversationsverlauf:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Bearbeite den Chatinhalt:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Bildbetrachter:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Verwendung von Offline-Modellen mit großer Kapazität.

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Dialogvorlage

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Einführung in den Kerncode

Derzeit ist das Plugin in folgende Module unterteilt:

AIChatPlusCommon: Runtime-Modul, zuständig für die Verarbeitung verschiedener AI-API-Anfragen und die Analyse der Antwortinhalte.

AIChatPlusEditor: Editor-Modul, das für die Implementierung des Editor AI-Chat-Tools verantwortlich ist.

AIChatPlusCllama: Laufzeitmodul, das die Schnittstelle und Parameter von llama.cpp kapselt und die Offline-Ausführung großer Modelle ermöglicht.

Drittanbieter/LLAMACpp: Ein Laufzeit-Drittanbietermodul, das die dynamische Bibliothek und Headerdateien von llama.cpp integriert.

Die UClass, die für das Senden von Anfragen verantwortlich ist, ist FAIChatPlus_xxxChatRequest. Jeder API-Dienst hat seine eigene unabhängige Request UClass. Die Antworten auf die Anfragen werden über die UClass UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase erhalten, wobei nur die entsprechenden Callback-Delegaten registriert werden müssen.

Before sending the request, you need to set up the API parameters and the message to be sent. This is done by setting up FAIChatPlus_xxxChatRequestBody. The specific content of the response is also parsed into FAIChatPlus_xxxChatResponseBody. When receiving the callback, you can obtain the ResponseBody through a specific interface.

Weitere Details zum Quellcode finden Sie im UE Store: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Verwenden Sie das Offline-Modell Cllama (llama.cpp) im Editor-Tool.

The following explains how to use the offline model llama.cpp in the AIChatPlus editor tool.

Zunächst einmal, lade das Offline-Modell von der HuggingFace-Website herunter: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Legen Sie das Modell in einem bestimmten Ordner ab, beispielsweise im Verzeichnis Content/LLAMA des Spielprojekts.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Öffnen Sie das AIChatPlus-Editor-Tool: Tools -> AIChatPlus -> AIChat. Erstellen Sie eine neue Chat-Sitzung und öffnen Sie die Sitzungseinstellungsseite.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Setzen Sie die API auf Cllama, aktivieren Sie die benutzerdefinierten API-Einstellungen, fügen Sie den Modellsuchpfad hinzu und wählen Sie ein Modell aus.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Beginnen wir zu plaudern!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Die Editor-Tool verwendet das Offline-Modell Cllama (llama.cpp), um Bilder zu verarbeiten.

Bitte laden Sie das Offline-Modell MobileVLM_V2-1.7B-GGUF von der HuggingFace-Website herunter und legen Sie es auch im Verzeichnis "Content/LLAMA" ab: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)Translate these text into German language:

和 [mmproj-model-f16.gguf] 

"和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but there is nothing to translate in the text provided.

Definieren Sie das Modell der Sitzung:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Send pictures to start chatting.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###Der Code verwendet das Offline-Modell Cllama (llama.cpp).

The following explains how to use the offline model llama.cpp in your code.

Zunächst müssen Sie die Modelldatei auch unter Content/LLAMA herunterladen.

Ändern Sie den Code, um einen Befehl hinzuzufügen und innerhalb des Befehls eine Nachricht an das Offline-Modell zu senden.

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

Nach dem erneuten Kompilieren können Sie im Editor Cmd Befehle verwenden, um die Ausgabenergebnisse des großen Modells im Protokoll OutputLog zu sehen.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Das Dokument verwendet das Offline-Modell llama.cpp.

Hier sind die Anweisungen zur Verwendung des Offline-Modells llama.cpp in der Blaupause.

In der Blaupause mit der rechten Maustaste einen Knoten namens `Send Cllama Chat Request` erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Erstellen Sie den Options-Knoten und legen Sie `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"` fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Erstellen Sie Nachrichten, fügen Sie eine Systemnachricht und eine Benutzernachricht hinzu.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Erstellen Sie einen Delegaten, der die Ausgabeinformationen des Modells empfängt und auf dem Bildschirm ausgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Die vollständige Blaupause sieht so aus. Wenn Sie die Blaupause ausführen, können Sie auf dem Bildschirm die Meldung sehen, die das Drucken des großen Modells bestätigt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###Der Editor verwendet das OpenAI-Chat.

Öffnen Sie das Chat-Tool Tools -> AIChatPlus -> AIChat, erstellen Sie eine neue Chat-Sitzung New Chat, setzen Sie die Sitzung ChatApi auf OpenAI und konfigurieren Sie die Schnittstellenparameter.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Beginne zu chatten:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Schalten Sie das Modell auf GPT-4o / GPT-4o-Mini um, um die Bildanalysefunktion von OpenAI zu nutzen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###Der Editor nutzt OpenAI zur Bearbeitung von Bildern (Erstellung/Modifikation/Variation).

In Chat-Tools eine neue Bild-Chat-Sitzung erstellen, die Sitzungseinstellungen auf OpenAI ändern und Parameter festlegen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Bild erstellen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Ändern Sie das Bild, ändern Sie den Chat-Typ des Bildes in "Bearbeiten" und laden Sie zwei Bilder hoch. Eines ist das Originalbild, das andere zeigt den Bereich, der bearbeitet werden soll, wobei die transparenten Stellen (Alpha-Kanal = 0) markiert sind.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Ändern Sie das Bild, indem Sie den Gesprächstyp von "Bild-Chat" in "Variation" ändern und laden Sie ein Bild hoch. OpenAI wird eine Variante des Originalbildes zurückgeben.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Blueprint verwenden OpenAI Modell Chatten

Erstellen Sie einen Knoten mit der rechten Maustaste im Blueprint mit dem Namen `Send OpenAI Chat Request In World`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Erstellen Sie einen Options-Knoten und setzen Sie `Stream=true, Api Key="your API key from OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Erstellen Sie Nachrichten, fügen Sie jeweils eine Systemnachricht und eine Benutzernachricht hinzu.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Erstellen Sie einen Delegaten, der die Ausgabedaten des Modells annimmt und auf dem Bildschirm ausgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Eine vollständige Blaupause sieht so aus, führe die Blaupause aus und du wirst die Nachricht sehen, die auf dem Bildschirm erscheint, wenn das große Modell gedruckt wird.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Verwenden von OpenAI, um Bilder zu erstellen.

Erstellen Sie in der Blaupause durch Rechtsklick einen Knoten namens "Send OpenAI Image Request" und legen Sie "In Prompt='ein schöner Schmetterling'" fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Erstellen Sie einen Options-Knoten und setzen Sie `Api Key="Ihren API-Schlüssel von OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Binden Sie das "On Images" Ereignis und speichern Sie das Bild auf der lokalen Festplatte.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

Ein vollständiger Bauplan sieht so aus, führen Sie den Bauplan aus, um zu sehen, wie das Bild an der angegebenen Stelle gespeichert wird.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###Der Editor verwendet Azure.

Erstellen Sie einen neuen Chat und ändern Sie ChatApi auf Azure. Konfigurieren Sie die API-Parameter für Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Beginnen wir mit dem Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###Der Editor verwendet Azure, um Bilder zu erstellen.

Erstellen Sie eine neue Bild-Chat-Sitzung (New Image Chat), ändern Sie ChatApi zu Azure und konfigurieren Sie die Azure-API-Parameter. Beachten Sie, dass bei Verwendung des dall-e-2-Modells die Parameter Qualität und Stil auf not_use gesetzt werden müssen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Beginnen Sie mit dem Chat und lassen Sie Azure das Bild erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Blueprint verwenden Azure Chat

Erstellen Sie das folgende Schema, konfigurieren Sie die Azure-Optionen, klicken Sie auf "Ausführen" und Sie werden die Chat-Nachrichten sehen, die von Azure auf dem Bildschirm ausgegeben werden.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Erstellen Sie ein Bild mit Azure mithilfe von Blueprints.

Erstellen Sie das folgende Schaubild, konfigurieren Sie die Azure-Optionen, klicken Sie auf Ausführen. Wenn das Erstellen des Bildes erfolgreich ist, wird die Meldung "Create Image Done" auf dem Bildschirm angezeigt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

Gemäß den Einstellungen im obigen Plan werden die Bilder im Pfad D:\Downloads\butterfly.png gespeichert.

## Claude

###Der Editor verwendet Claude zum Chatten und Analysieren von Bildern.

Erstellen Sie einen neuen Chat, ändern Sie ChatApi in Claude und legen Sie die Api-Parameter für Claude fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Beginnen Sie mit dem Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Verwenden von Claude, um Bilder zu chatten und analysieren.

Im Blueprint mit der rechten Maustaste einen Knoten namens "Send Claude Chat Request" erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Erstellen Sie den Options-Knoten und legen Sie `Stream=true, Api Key="Ihr API-Schlüssel von Clude", Max Output Tokens=1024` fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Erstellen Sie Nachrichten, erstellen Sie eine Texture2D aus einer Datei und erstellen Sie AiChatPlusTexture aus der Texture2D. Fügen Sie AiChatPlusTexture der Nachricht hinzu.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Entsprechend dem obigen Tutorial, erstellen wir ein Ereignis und drucken die Informationen auf dem Bildschirm des Spiels aus.

Die vollständige Blaupause sieht so aus, führen Sie die Blaupause aus und Sie werden die Meldung auf dem Bildschirm sehen, die das Drucken des großen Modells bestätigt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Erhalten Sie Ollama.

Sie können die Installationsdatei lokal über die Ollama-Website beziehen: [ollama.com](https://ollama.com/)

Sie können Ollama über die von anderen bereitgestellte Ollama-Schnittstelle verwenden.

###Der Editor verwendet Ollama zum Chatten und Analysieren von Bildern.

Erstellen Sie einen neuen Chat und ändern Sie ChatApi in Ollama um. Legen Sie die Api-Parameter für Ollama fest. Wenn es sich um einen Text-Chat handelt, setzen Sie das Modell auf Textmodell, wie zum Beispiel llama3.1. Wenn Bilder verarbeitet werden müssen, wählen Sie ein Modell aus, das Vision unterstützt, zum Beispiel moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Beginnen wir mit dem Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Blueprints werden mit Ollama zum Chatten und Analysieren von Bildern verwendet.

Erstellen Sie das folgende Schema, konfigurieren Sie die Ollama-Optionen, klicken Sie auf Ausführen, um die Chat-Nachrichten zu sehen, die von Ollama auf dem Bildschirm ausgegeben werden.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###Der Editor verwendet Gemini.

Erstellen Sie einen neuen Chat und ändern Sie ChatApi in Gemini. Konfigurieren Sie die Api-Parameter von Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Beginnen Sie mit dem Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###Verwendet Gemini-Chat für Blaupausen.

Erstellen Sie das folgende Schema, konfigurieren Sie die Gemini-Optionen, klicken Sie auf Ausführen und Sie werden die Chat-Nachrichten sehen, die Gemini zurückgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)


##Aktualisierungsprotokoll

### v1.4.1 - 2025.01.04

####Problembehebung

Die Chat-Plattform ermöglicht das Versenden von Bildern ohne Text.

Reparieren Sie das Problem beim Senden von Bildern über die OpenAI-Schnittstelle fehlgeschlagenen Text.

Behebung des Problems mit fehlenden Parametern Quality, Style und ApiVersion in den Einstellungen von OpanAI und Azure-Chattools.

### v1.4.0 - 2024.12.30

####Neue Funktion

*(Experimental feature) Cllama (llama.cpp) supports multimodal models and can process images.*

Alle Arten von Bauplan-Parametern wurden mit ausführlichen Hinweisen versehen.

### v1.3.4 - 2024.12.05

####Neue Funktion

OpenAI unterstützt eine Vision API.

####Problembehebung

Fixing the error when OpenAI stream=false.

### v1.3.3 - 2024.11.25

####New feature

Unterstützt UE-5.5.

####Fehlerbehebung

Das Problem mit den nicht funktionierenden Teilen der Baupläne wurde behoben.

### v1.3.2 - 2024.10.10

####Problembehebung

Beheben Sie den Absturz von cllama beim manuellen Stoppen einer Anfrage.

Repairing the issue of not finding the ggml.dll and llama.dll files when packaging the Win version of the mall download.

Prüf beim Erstellen der Anfrage, ob sich der Thread im GameThread befindet.

### v1.3.1 - 2024.9.30

####Neue Funktion

Fügen Sie einen SystemTemplateViewer hinzu, um Hunderte von Systemeinstellungs-Templates anzuzeigen und zu nutzen.

####Reparatur des Problems

Fix the plug-in downloaded from the store, llama.cpp cannot find the link library.

Reparatur des Problems mit zu langen Pfaden in LLAMACpp.

Beheben Sie den Linkfehler von llama.dll nach dem Verpacken von Windows.

Beheben Sie das Problem mit dem Lesen von Dateipfaden auf iOS/Android.

Fixing the Cllame setting name error.

### v1.3.0 - 2024.9.23

####Bedauerlicherweise kann ich keinen konkreten Text finden um es zu übersetzen.

Integriert llama.cpp, unterstützt die lokale Offline-Ausführung großer Modelle.

### v1.2.0 - 2024.08.20

####Neue Funktion

Unterstützung für OpenAI Image Edit/Image Variation.

Unterstützt die Ollama API, unterstützt das automatische Abrufen der Liste der von Ollama unterstützten Modelle.

### v1.1.0 - 2024.08.07

####Neue Funktion

Unterstützung der Blaupause

### v1.0.0 - 2024.08.05

####Neue Funktion

Grundlegende vollständige Funktion.

Unterstützung für OpenAI, Azure, Claude, Gemini.

Mit integriertem voll ausgestattetem Editor-Chat-Tool.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte im [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte weisen Sie auf etwaige Auslassungen hin. 
