---
layout: post
title: UE Plugin AIChatPlus Dokumentation
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
description: UE Plugin AIChatPlus Dokumentation
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE 插件 AIChatPlus Instructions Guide

##Öffentliches Lagerhaus

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Plug-in acquisition

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Plug-in Brief介Es ist eine Kurzbeschreibung eines Plug-ins.

This plugin supports UE5.2+.

UE.AIChatPlus ist ein UnrealEngine-Plugin, das die Kommunikation mit verschiedenen GPT AI-Chatdiensten ermöglicht. Derzeit unterstützte Dienste sind OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama und lokale Offline-Funktionalität mit llama.cpp. In Zukunft werden noch mehr Serviceanbieter unterstützt. Die Implementierung basiert auf asynchronen REST-Anfragen, die Leistung ist effizient und erleichtert es Entwicklern, diese AI-Chat-Services in ihre UnrealEngine-Projekte zu integrieren.

UE.AIChatPlus enthält auch ein Editor-Tool, mit dem Sie diese KI-Chat-Services direkt im Editor verwenden können, um Texte und Bilder zu generieren sowie Bilder zu analysieren.

##Benutzerhandbuch

###Editor Chat Tool

Im Menü "Tools" -> "AIChatPlus" -> "AIChat" können Sie das Chat-Tool des Plugins öffnen.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


Das Tool unterstützt die Generierung von Texten, Text-Chats, Bildgenerierung und Bildanalyse.

Das Interface des Tools ist ungefähr wie folgt:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Hauptfunktion

Offline large-scale models: Integrated the llama.cpp library, supporting local offline execution of large models

Textnachricht: Klicken Sie auf die Schaltfläche "Neuer Chat" in der linken unteren Ecke, um eine neue Textnachrichtenunterhaltung zu erstellen.

Bildgenerierung: Klicken Sie auf die Schaltfläche `New Image Chat` in der linken unteren Ecke, um eine neue Bildgenerierungssitzung zu erstellen.

Bildanalyse: Einige Chat-Dienste von `New Chat` unterstützen den Versand von Bildern, wie zum Beispiel Claude, Google Gemini. Klicken Sie einfach auf die Schaltfläche 🖼️ oder 🎨 über dem Eingabefeld, um das zu sendende Bild zu laden.

Unterstützung für Blaupausen (Blueprint): Unterstützung für das Erstellen von API-Anfragen über Blaupausen, um Funktionen wie Text-Chats, Bildgenerierung und mehr zu realisieren.

Wählen Sie die aktuelle Chat-Rolle: Das Dropdown-Menü über dem Chat-Feld kann die Chat-Rolle festlegen, von der aus die Texte gesendet werden. Indem Sie verschiedene Rollen simulieren, können Sie das KI-Chat anpassen.

Leeren Sie den Chat: Durch Klicken auf das ❌-Symbol oben im Chatfenster können Sie die Nachrichtenhistorie der aktuellen Sitzung löschen.

Gesprächsvorlagen: Hunderte von integrierten Gesprächseinstellungen, um häufige Probleme einfach zu behandeln.

Allgemeine Einstellungen: Durch Klicken auf die Schaltfläche "Einstellung" in der linken unteren Ecke können Sie das Fenster für allgemeine Einstellungen öffnen. Dort können Sie den Standardtextchat, den API-Dienst für die Bildgenerierung festlegen und die spezifischen Parameter für jeden API-Dienst einstellen. Die Einstellungen werden automatisch im Pfad des Projekts unter "$(ProjectFolder)/Saved/AIChatPlusEditor" gespeichert.

Konversationseinstellungen: Durch Klicken auf die Schaltfläche "Einstellungen" oben im Chat-Fenster können Sie das Einstellungsfenster der aktuellen Konversation öffnen. Sie können den Namen der Konversation ändern, den für die Konversation verwendeten API-Dienst ändern und spezifische Parameter für die API jeder Konversation separat festlegen. Die Konversationseinstellungen werden automatisch im Verzeichnis `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions` gespeichert.

Änderung des Chat-Inhalts: Wenn Sie mit der Maus über den Chat-Inhalt fahren, wird eine Schaltfläche zur Konfiguration des jeweiligen Chat-Inhalts angezeigt. Sie können den Inhalt neu generieren, ändern, kopieren, löschen oder einen neuen Inhalt darunter generieren (für Inhalte, bei denen der Benutzer die Rolle hat).

Bildbetrachtung: Beim Generieren von Bildern wird durch Klicken auf ein Bild ein Bildbetrachtungsfenster (ImageViewer) geöffnet. Es unterstützt das Speichern von Bildern als PNG/UE-Textur, wobei die Textur direkt im Inhaltsbrowser (Content Browser) angezeigt werden kann, um die Verwendung von Bildern im Editor zu erleichtern. Darüber hinaus können Bilder gelöscht, neu generiert oder weitere Bilder generiert werden. Für den Editor unter Windows wird auch das Kopieren von Bildern unterstützt, um Bilder direkt in die Zwischenablage zu kopieren, was die Verwendung erleichtert. Die generierten Bilder werden automatisch im jeweiligen Sitzungsordner gespeichert, normalerweise unter dem Pfad `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.  

Plan:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Global settings:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Conversation settings:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Ändern Sie den Chat-Inhalt:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Bildbetrachter:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Verwendung von Offline-Großmodellen

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Dialogvorlage

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Erläuterung des Kerncodes

Derzeit ist das Plugin in die folgenden Module unterteilt:

AIChatPlusCommon: Das Runtime-Modul ist dafür zuständig, Anfragen von verschiedenen KI-API-Schnittstellen zu verarbeiten und die Antwortinhalte zu analysieren.

AIChatPlusEditor: Editor-Modul, das für die Implementierung des Editor AI-Chat-Tools zuständig ist.

AIChatPlusCllama: Das Laufzeitmodul, das die Schnittstelle und Parameter von llama.cpp kapselt und die Offline-Ausführung großer Modelle ermöglicht.

Drittanbieter/LLAMACpp: Enthält zur Laufzeit integrierte Drittanbietermodule (Runtime) mit den dynamischen Bibliotheken und Header-Dateien von llama.cpp.

Der UClass, der für das Senden von Anfragen verantwortlich ist, ist FAIChatPlus_xxxChatRequest. Jeder API-Dienst hat einen eigenen unabhängigen Request UClass. Die Antworten auf die Anfragen werden über die Klassen UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase erhalten, für die lediglich die entsprechenden Rückrufdelegaten registriert werden müssen.

Vor dem Senden einer Anfrage müssen die API-Parameter und die zu sendende Nachricht eingerichtet werden. Dies wird durch FAIChatPlus_xxxChatRequestBody festgelegt. Die spezifischen Inhalte der Antwort werden ebenfalls im FAIChatPlus_xxxChatResponseBody analysiert, und wenn eine Rückmeldung erfolgt, kann der ResponseBody über eine spezifische Schnittstelle abgerufen werden.

Weitere Details zum Quellcode sind im UE Store erhältlich: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Der Editor verwendet das Offline-Modell Cllama (llama.cpp).

The text has been translated into German:

Die folgenden Anweisungen zeigen, wie man das Offline-Modell llama.cpp im Editor-Tool AIChatPlus verwendet.

(https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Stellen Sie das Modell in einem bestimmten Ordner ab, z.B. im Verzeichnis Content/LLAMA des Spieleprojekts.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Öffnen Sie das AIChatPlus-Editor-Tool: Tools -> AIChatPlus -> AIChat, erstellen Sie eine neue Chat-Sitzung und öffnen Sie die Sitzungseinstellungen.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Legen Sie die API auf Cllama, aktivieren Sie die benutzerdefinierten API-Einstellungen und fügen Sie den Modelldateipfad hinzu. Wählen Sie dann das gewünschte Modell aus.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Beginnen wir mit dem Chat!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Verwenden Sie im Editor-Tool das Offline-Modell Cllama (llama.cpp), um Bilder zu verarbeiten.

Laden Sie das Offline-Modell MobileVLM_V2-1.7B-GGUF von der HuggingFace-Website herunter und speichern Sie es ebenfalls im Verzeichnis Content/LLAMA: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but there is no text provided for translation.

Setzen Sie das Modell der Sitzung:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Bitte senden Sie ein Bild, um das Gespräch zu beginnen.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###Der Code verwendet das Offline-Modell Cllama(llama.cpp).

Das folgende beschreibt, wie man das Offline-Modell llama.cpp im Code verwendet.

Zunächst müssen Sie die Modelldatei ebenfalls im Ordner Content/LLAMA herunterladen.

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

Nachdem Sie neu kompiliert haben, können Sie im Editor Cmd den Befehl verwenden, um die Ausgabenergebnisse des großen Modells im Protokoll OutputLog zu sehen.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Verwenden Sie das Offline-Modell blueprint.cpp.

Die folgenden Anweisungen zeigen, wie das Offline-Modell llama.cpp in der BluePrint verwendet werden kann.

Erstellen Sie im Blueprint einen Knoten mit der rechten Maustaste namens "Send Cllama Chat Request".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Erstellen Sie den Options-Knoten und legen Sie `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"` fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Erstellen Sie Nachrichten, fügen Sie jeweils eine Systemnachricht und eine Benutzernachricht hinzu.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Erstellen Sie eine Delegierte, die die Ausgabedaten des Modells empfängt und auf dem Bildschirm ausgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Eine vollständige Blaupause sieht so aus. Führen Sie die Blaupause aus, um die Nachrichten zu sehen, die das Spiel auf dem Bildschirm ausgibt, wenn ein großes Modell gedruckt wird.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###Der Editor verwendet OpenAI-Chat.

Öffnen Sie das Chat-Tool unter Tools -> AIChatPlus -> AIChat, erstellen Sie eine neue Chat-Sitzung unter New Chat, konfigurieren Sie die Sitzung unter ChatApi auf OpenAI und setzen Sie die Schnittstellenparameter.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Beginnen wir zu chatten:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Schalten Sie das Modell auf GPT-4o/GPT-4o-Mini um, um die Bildanalysefunktionen von OpenAI nutzen zu können.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###Der Editor nutzt OpenAI zur Bearbeitung von Bildern (Erstellung/Änderung/Varianten).

In einem Chat-Tool ein neues Bildgespräch erstellen, das Gespräch auf OpenAI ändern und die Parameter festlegen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Erstellen Sie ein Bild.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Ändern Sie das Bild, ändern Sie den Gesprächstyp von Bildchat auf "Bearbeiten" und laden Sie zwei Bilder hoch. Ein Bild ist das Originalbild und das andere ist die Maske, wobei die transparenten Stellen (Alpha-Kanal 0) die zu ändernden Bereiche anzeigen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Ändern Sie das Bild, ändern Sie den Chat-Typ des Bildes in "Variation" und laden Sie ein Bild hoch. OpenAI wird eine Variante des originalen Bildes zurückgeben.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Blueprint verwendet das OpenAI-Modell für Unterhaltungen.

In der Blaupause mit der rechten Maustaste einen Knoten namens `Send OpenAI Chat Request In World` erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Erstellen Sie ein Options-Knoten und legen Sie `Stream=true, Api Key="Ihren API-Schlüssel von OpenAI"` fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Erstellen Sie Nachrichten, fügen Sie jeweils eine Systemnachricht und eine Benutzernachricht hinzu.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Erstellen Sie einen Delegaten, der die Ausgabeinformationen des Modells annimmt und auf dem Bildschirm ausgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Die Übersetzung ins Deutsche lautet:

Die komplette Blaupause sieht so aus, führe die Blaupause aus, um die Nachrichten auf dem Bildschirm zu sehen, die das Drucken eines großen Modells bestätigen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Die Blaupause wurde mit OpenAI erstellt, um ein Bild zu erzeugen.

Erstellen Sie in der Blaupause einen Knoten mit der rechten Maustaste namens "Send OpenAI Image Request" und legen Sie "Im Prompt = 'einen schönen Schmetterling'" fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Erstellen Sie den Options-Knoten und legen Sie `Api Key="Ihren API-Schlüssel von OpenAI"` fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Binden Sie das Ereignis "On Images" und speichern Sie das Bild auf der lokalen Festplatte.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

Eine vollständige Blaupause siehst du hier, führe sie aus und du kannst sehen, wie das Bild an der angegebenen Stelle gespeichert wird.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###Der Editor verwendet Azure.

Erstellen Sie eine neue Unterhaltung (New Chat), ändern Sie ChatApi zu Azure und konfigurieren Sie die Azure-API-Parameter.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Beginnen Sie zu chatten.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###Der Editor verwendet Azure, um Bilder zu erstellen.

Erstellen Sie eine neue Bild-Chat-Sitzung (New Image Chat), ändern Sie ChatApi auf Azure und legen Sie die Azure-API-Parameter fest. Bitte beachten Sie, bei Verwendung des dall-e-2-Modells müssen die Parameter Quality und Stype auf not_use gesetzt werden.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Beginnen Sie mit dem Chat und lassen Sie Azure das Bild erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Blueprint verwenden Azure Chat

Erstellen Sie das folgende Blueprint, konfigurieren Sie die Azure-Optionen, klicken Sie auf Ausführen und sehen Sie die Chat-Nachrichten, die von Azure zurückgegeben werden, auf dem Bildschirm.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Entwurf mit Azure erstellen Bild.

Erstellen Sie das folgende Blueprint, konfigurieren Sie die Azure-Optionen, klicken Sie auf "Ausführen". Wenn das Bild erfolgreich erstellt wurde, erscheint die Meldung "Bild erstellen abgeschlossen".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

Gemäß den Einstellungen des obigen Bauplans wird das Bild im Pfad D:\Downloads\butterfly.png gespeichert.

## Claude

###Der Editor verwendet Claude, um zu chatten und Bilder zu analysieren.

Erstellen Sie einen neuen Chat, ändern Sie ChatApi zu Claude und konfigurieren Sie Claudes Api-Parameter.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Beginnen Sie mit dem Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Verwenden Sie die Blaupause, um mit Claude zu chatten und Bilder zu analysieren.

In der Blaupause rechtsklicken und einen Knoten namens `Send Claude Chat Request` erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Erstellen Sie einen Options-Knoten und legen Sie `Stream=true, Api Key="Ihr API-Schlüssel von Clude", Max Output Tokens=1024` fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Erstellen Sie Nachrichten, erstellen Sie aus der Datei Texture2D und aus Texture2D AIChatPlusTexture, fügen Sie AIChatPlusTexture zur Nachricht hinzu.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Wie im obigen Tutorial, erstelle ein Ereignis und drucke die Informationen auf den Bildschirm des Spiels.

Eine vollständige Blaupause sieht so aus, wenn du die Blaupause ausführst, siehst du die Nachricht auf dem Bildschirm, die das Drucken des großen Modells bestätigt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Erhalten Sie Ollama

Sie können die Installationsdatei direkt von der Ollama-Website herunterladen und lokal installieren: [ollama.com](https://ollama.com/)

Sie können Ollama über die von anderen bereitgestellte Ollama-Schnittstelle verwenden.

###Der Editor verwendet Ollama zum Chatten und Analysieren von Bildern.

Erstellen Sie eine neue Unterhaltung (New Chat), ändern Sie ChatApi in Ollama und konfigurieren Sie die API-Parameter von Ollama. Wenn es sich um einen Text-Chat handelt, setzen Sie das Modell auf ein Textmodell wie llama3.1; wenn Bilder verarbeitet werden müssen, wählen Sie ein Modell aus, das die Bilderkennung unterstützt, wie beispielsweise moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Beginnen Sie mit dem Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Verwenden Sie Ollama, um Bilder zu chatten und zu analysieren.

Erstellen Sie das folgende Schema, konfigurieren Sie die Ollama-Optionen, klicken Sie auf Ausführen, um die Chat-Informationen zu sehen, die Ollama auf dem Bildschirm zurückgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###Der Editor verwendet Gemini.

* Erstellen Sie einen neuen Chat, ändern Sie ChatApi zu Gemini und konfigurieren Sie die Api-Parameter von Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Beginnen Sie mit dem Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###Verwenden Sie Gemini-Chat in Ihrem Blueprint.

Erstellen Sie die folgende Blaupause, konfigurieren Sie die Gemini-Optionen, klicken Sie auf Ausführen und Sie werden die Chatnachrichten sehen, die Gemini zurückgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

## Deepseek

###The text is: "Editor uses Deepseek."

Erstellen Sie eine neue Chat-Sitzung, ändern Sie ChatApi auf OpenAi und konfigurieren Sie die Deepseek-Api-Parameter. Fügen Sie ein neues Kandidatenmodell namens deepseek-chat hinzu und setzen Sie das Modell auf deepseek-chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Beginnen Sie mit dem Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Blueprint verwenden Deepseek Chat

Erstellen Sie das folgende Schema und konfigurieren Sie die Deepseek-spezifischen Anforderungsoptionen, einschließlich Modell, Basis-URL, Endpunkt-URL, API-Schlüssel usw. Klicken Sie auf "Ausführen", um die Chatnachrichten zurückzubekommen, die Gemini ausgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##Änderungsprotokoll

### v1.4.1 - 2025.01.04

####Problem behoben

Die Messaging-App unterstützt das Senden von nur Bildern ohne Text.

Repariere das Problem mit dem Versenden von Bildern über die OpenAI-Schnittstelle.

Repariere das Problem im OpanAI- und Azure-Chat-Tool-Einstellungen, das die Parameter Quality, Style und ApiVersion ausgelassen hat.

### v1.4.0 - 2024.12.30

####Neue Funktion

*(Experimental feature) Cllama (llama.cpp) supports multi-modal models and can handle images.*

Alle Blueprint-Typ-Parameter wurden mit detaillierten Hinweisen versehen.

### v1.3.4 - 2024.12.05

####Neue Funktion

OpenAI unterstützt Vision-API.

####Problembehebung

Fixing the error when OpenAI stream=false.

### v1.3.3 - 2024.11.25

####Neue Funktion

Unterstützt UE-5.5.

####Problembehebung

Behebung des Problems, bei dem einige Baupläne nicht funktionieren.

### v1.3.2 - 2024.10.10

####Fehlerbehebung

Behebung des Absturzes von cllama beim manuellen Stoppen der Anfrage.

Fix the issue of missing ggml.dll and llama.dll files when packaging the downloaded version of win in the store.

Beim Erstellen einer Anfrage wird überprüft, ob sich der Thread im Spiel befindet.

### v1.3.1 - 2024.9.30

####Neue Funktion

Fügen Sie einen SystemTemplateViewer hinzu, um Hunderte von Systemeinstellungsvorlagen anzuzeigen und zu nutzen.

####Problembehebung.

Reparieren Sie das heruntergeladene Plugin aus dem Store, llama.cpp kann die Linksbibliothek nicht finden.

Fix LLAMACpp long path issue

Beheben Sie den Link-Fehler von llama.dll nach dem Windows-Build.

Beheben Sie das Problem mit dem Lesen des Dateipfads auf iOS/Android.

Reparatur des Fehler bei der Einstellung des Namens von Cllame

### v1.3.0 - 2024.9.23

####Wichtige neue Funktion

Integrierte llama.cpp, unterstützt die lokale Offline-Ausführung großer Modelle.

### v1.2.0 - 2024.08.20

####Neue Funktion.

Unterstützung für OpenAI Image Edit/Image Variation.

Unterstützung der Ollama API, Unterstützung beim automatischen Abrufen der Liste der von Ollama unterstützten Modelle.

### v1.1.0 - 2024.08.07

####Neue Funktion

Unterstützung des Entwurfs

### v1.0.0 - 2024.08.05

####Neue Funktion

Grundlegende vollständige Funktion.

Unterstützt OpenAI, Azure, Claude, Gemini.

Mit einem integrierten Chat-Tool mit umfangreichen Funktionen.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte gib dein [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte weisen Sie auf etwaige Auslassungen hin. 
