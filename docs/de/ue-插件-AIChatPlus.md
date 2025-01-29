---
layout: post
title: UE Plugin AIChatPlus Beschreibung Dokument
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
description: UE Plugin AIChatPlus Anleitung
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE-Plugin AIChatPlus Handbuch

##Öffentliches Lager

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Plugin-Beschaffung

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Plugin-Beschreibung

Dieses Plugin unterstützt UE5.2+.

UE.AIChatPlus ist ein UnrealEngine-Plugin, das die Kommunikation mit verschiedenen GPT AI-Chatdiensten ermöglicht. Derzeit unterstützte Dienste sind OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama und llama.cpp für lokale Offline-Nutzung. In Zukunft werden weitere Dienstanbieter unterstützt. Die Implementierung basiert auf asynchronen REST-Anfragen, was eine hohe Effizienz bietet und es UE-Entwicklern erleichtert, diese AI-Chatdienste zu integrieren.

Gleichzeitig enthält UE.AIChatPlus ein Editor-Tool, mit dem man diese KI-Chatdienste direkt im Editor nutzen kann, um Texte und Bilder zu generieren, Bilder zu analysieren usw.

##Gebrauchsanweisung

###Editor-Chat-Tool

Menüleiste Tools -> AIChatPlus -> AIChat öffnet das von dem Plugin bereitgestellte Editor-Chat-Tool.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


Die Werkzeuge unterstützen die Textgenerierung, Textchats, die Bildgenerierung und die Bildanalyse.

Die Benutzeroberfläche des Werkzeugs ist im Großen und Ganzen wie folgt:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Hauptfunktionen

* Offline-Großmodell: Integriert die llama.cpp-Bibliothek und unterstützt die lokale Offline-Ausführung von Großmodellen.

* Text-Chat: Klicke auf die Schaltfläche `Neuen Chat` in der linken unteren Ecke, um eine neue Text-Chat-Sitzung zu erstellen.

* Bildgenerierung: Klicken Sie auf die Schaltfläche `Neuer Bild-Chat` in der linken unteren Ecke, um eine neue Bildgenerierungssitzung zu erstellen.

* Bildanalyse: Der Teil des Chatdienstes `New Chat` unterstützt das Senden von Bildern, wie zum Beispiel Claude, Google Gemini. Klicken Sie auf die 🖼️- oder 🎨-Schaltfläche über dem Eingabefeld, um das zu sendende Bild zu laden.

* Unterstützung von Blueprints: Unterstützung bei der Erstellung von API-Anfragen für Blueprints, um Text-Chats, Bildgenerierung und andere Funktionen zu ermöglichen.

* Aktuelle Chatrolle festlegen: Im Dropdown-Menü über dem Chatfenster kann die Rolle für den aktuellen Text eingestellt werden, um das AI-Chat zu steuern, indem verschiedene Rollen simuliert werden.

* Sitzung löschen: Oben im Chatfenster kann die ❌-Taste die Historie der aktuellen Sitzung löschen.

* Gesprächsvorlagen: EingebauteHunderte von Gesprächseinstellungs-Vorlagen, die die Bearbeitung häufiger Fragen erleichtern.

* Globale Einstellungen: Klicken Sie auf die Schaltfläche `Setting` in der linken unteren Ecke, um das Fenster für globale Einstellungen zu öffnen. Sie können den Standard-Textchat, die API-Dienste zur Bildgenerierung einstellen und die spezifischen Parameter jeder API-Dienstleistung festlegen. Die Einstellungen werden automatisch im Projektverzeichnis `$(ProjectFolder)/Saved/AIChatPlusEditor` gespeichert.

* Konversationseinstellungen: Klicken Sie auf die Schaltfläche "Einstellungen" über dem Chatfenster, um das Einstellungsfenster der aktuellen Konversation zu öffnen. Es ermöglicht die Änderung des Konversationsnamens, die Anpassung des verwendeten API-Dienstes sowie die individuelle Einstellung spezifischer Parameter für jede Konversation. Die Konversationseinstellungen werden automatisch unter `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions` gespeichert.

* Chat-Inhalt bearbeiten: Wenn Sie mit der Maus über den Chat-Inhalt fahren, erscheint ein Einstellungsbutton für den einzelnen Chat-Inhalt, der das erneute Generieren von Inhalten, das Bearbeiten von Inhalten, das Kopieren von Inhalten, das Löschen von Inhalten und das erneute Generieren von Inhalten unten (für Inhalte, bei denen die Rolle der Benutzer ist) unterstützt.

* Bildbrowser: Zum Generieren von Bildern öffnet ein Klick auf das Bild das Bildanzeigefenster (ImageViewer), das das Speichern von Bildern im PNG/UE-Texture-Format unterstützt. Die Texturen können direkt im Inhaltsbrowser (Content Browser) angezeigt werden, was die Verwendung der Bilder im Editor erleichtert. Zudem unterstützen wir Funktionen wie das Löschen von Bildern, das erneute Generieren von Bildern und das Fortsetzen der Generierung weiterer Bilder. Für den Editor unter Windows wird außerdem das Kopieren von Bildern unterstützt, sodass Bilder direkt in die Zwischenablage kopiert werden können, was die Nutzung erleichtert. Die während der Sitzung generierten Bilder werden auch automatisch in jedem Sitzungsordner gespeichert, der normalerweise den Pfad `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images` hat.

Bauplan:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Globale Einstellungen:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Konversationseinstellungen:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Ändern Sie den Chatinhalt:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Bildbetrachter:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Verwendung des Offline-Großmodells

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Dialogvorlage

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Kerncode Einführung

Derzeit ist das Plugin in folgende Module unterteilt:

* AIChatPlusCommon: Laufzeitmodul, verantwortlich für die Verarbeitung von Anfragen, die von verschiedenen AI-API-Schnittstellen gesendet werden, und für die Analyse der Antwortinhalte.

* AIChatPlusEditor: Editor-Modul, verantwortlich für die Implementierung des AI-Chat-Tools im Editor.

* AIChatPlusCllama: Laufzeitmodul, das die Schnittstelle und Parameter von llama.cpp kapselt und die Offline-Ausführung großer Modelle ermöglicht.

* Thirdparty/LLAMACpp: Laufzeit-Drittanbieter-Modul, das die dynamischen Bibliotheken und Header-Dateien von llama.cpp integriert.

Die spezifisch zuständige UClass für das Senden von Anfragen ist FAIChatPlus_xxxChatRequest, wobei jeder API-Dienst über eine eigene, unabhängige Request UClass verfügt. Die Antworten auf die Anfragen werden über die beiden UClass UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase abgerufen, wobei lediglich die entsprechenden Callback-Delegaten registriert werden müssen.

Vor dem Senden einer Anfrage müssen die API-Parameter und die zu sendende Nachricht festgelegt werden, dies erfolgt über FAIChatPlus_xxxChatRequestBody. Die genauen Inhalte der Antwort werden im FAIChatPlus_xxxChatResponseBody analysiert, und bei Erhalt des Rückrufs kann das ResponseBody über eine spezielle Schnittstelle abgerufen werden.

Weitere Quellcodedetails sind im UE Marketplace erhältlich: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Editor-Tool verwendet Offline-Modell Cllama(llama.cpp)

Die folgende Anleitung beschreibt, wie Sie das Offline-Modell llama.cpp im AIChatPlus-Editor-Tool verwenden können.

* Zuerst das Offline-Modell von der HuggingFace-Website herunterladen: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

* Legen Sie das Modell in einen bestimmten Ordner, zum Beispiel im Verzeichnis Content/LLAMA des Spieleprojekts ab.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

* Öffnen Sie das AIChatPlus-Bearbeitungstool: Werkzeuge -> AIChatPlus -> AIChat, erstellen Sie eine neue Chatsitzung und öffnen Sie die Sitzungssteuerungsseite.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

* Setze die API auf Cllama, aktiviere die benutzerdefinierten API-Einstellungen, füge den Modell-Suchpfad hinzu und wähle das Modell aus.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

* Lass uns chatten!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Der Editor-Tool verwendet das Offline-Modell Cllama (llama.cpp) zur Verarbeitung von Bildern.

* Laden Sie das Offline-Modell MobileVLM_V2-1.7B-GGUF von der HuggingFace-Website herunter und legen Sie es ebenfalls im Verzeichnis Content/LLAMA ab: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)。

* Modell der Sitzung festlegen:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

* Bild senden, um den Chat zu beginnen

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###Der Code verwendet das Offline-Modell Cllama(llama.cpp)

Die folgende Anleitung beschreibt, wie man das Offline-Modell llama.cpp im Code verwendet.

Zuerst müssen auch die Modell-Dateien in den Ordner Content/LLAMA heruntergeladen werden.

* Ändern Sie den Code, um einen Befehl hinzuzufügen, und senden Sie eine Nachricht an das Offline-Modell in diesem Befehl.

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

* Nach der Neakomplilierung können Sie im Editor Cmd den Befehl verwenden, um die Ausgabe des großen Modells im Protokoll OutputLog zu sehen.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Der Blueprint verwendet das Offline-Modell llama.cpp.

Folgende Informationen erklären, wie man Offline-Modelle mit llama.cpp in Blueprint verwendet.

* Klicken Sie mit der rechten Maustaste im Blueprint, um einen Knoten `Send Cllama Chat Request` zu erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

* Erstellen Sie einen Optionsknoten und setzen Sie `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

* Erstellen Sie Nachrichten, indem Sie eine Systemnachricht und eine Benutzernachricht hinzufügen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Erstellen Sie einen Delegate, der die Informationen der Modellausgabe empfängt und auf dem Bildschirm druckt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* Der vollständige Plan sieht so aus, führen Sie den Plan aus und Sie werden die Spieloberfläche sehen, die die vom großen Modell zurückgegebenen Nachrichten druckt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###Editor verwendet OpenAI-Chat

* Öffnen Sie das Chat-Tool Tools -> AIChatPlus -> AIChat, erstellen Sie eine neue Chatsitzung New Chat, setzen Sie die Sitzung ChatApi auf OpenAI und passen Sie die Schnittstellenparameter an.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

* Chat beginnen:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

* Wechseln Sie das Modell zu gpt-4o / gpt-4o-mini, um die visuellen Funktionen von OpenAI zur Analyse von Bildern zu nutzen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###Der Editor verwendet OpenAI zur Verarbeitung von Bildern (Erstellen/Ändern/Variieren)

* Erstelle im Chat-Tool einen neuen Bildchat New Image Chat, ändere die Sitzungs Einstellungen auf OpenAI und setze die Parameter.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

* Bilder erstellen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

* Ändern Sie das Bild, ändern Sie den Konversationstyp Image Chat in Edit und laden Sie zwei Bilder hoch, eines ist das Originalbild, das andere ist die Maske, wobei die transparenten Bereiche (Alpha-Kanal 0) die zu ändernden Stellen darstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

* Bildvarianten, ändern Sie den Gesprächs Image Chat Type in Variation und laden Sie ein Bild hoch. OpenAI wird eine Variante des ursprünglichen Bildes zurückgeben.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Blueprint verwendet OpenAI-Modell Chat

* Klicken Sie mit der rechten Maustaste auf das Blueprint, um einen Knoten `Send OpenAI Chat Request In World` zu erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

* Erstellen Sie den Options-Knoten und setzen Sie `Stream=true, Api Key="Ihr API-Schlüssel von OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

* Erstelle Nachrichten und füge jeweils eine Systemnachricht und eine Benutzernachricht hinzu.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

* Erstellen Sie einen Delegate, um die Informationen aus dem Modelloutput zu empfangen und auf dem Bildschirm anzuzeigen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* Der vollständige Blueprint sieht so aus, und wenn Sie den Blueprint ausführen, können Sie sehen, dass der Spielbildschirm die Nachrichten des großen Modells ausgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Blueprint verwendet OpenAI zur Erstellung von Bildern.

* Klicken Sie mit der rechten Maustaste in die Blaupause, um einen Knoten `Send OpenAI Image Request` zu erstellen, und setzen Sie `In Prompt="a beautiful butterfly"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

* Erstellen Sie den Options-Knoten und setzen Sie `Api Key="Ihr API-Schlüssel von OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

* Binden Sie die On Images-Ereignisse und speichern Sie die Bilder auf der lokalen Festplatte.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

* Der vollständige Plan sieht so aus, führen Sie den Plan aus, um das Bild am vorgesehenen Speicherort zu sehen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###Editor verwendet Azure

* Neue Sitzung (New Chat), ändern Sie ChatApi in Azure und setzen Sie die API-Parameter von Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

* Das Gespräch beginnen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###Editor verwendet Azure zur Erstellung von Bildern

* Neue Bild-Chat-Sitzung (New Image Chat), ändere ChatApi in Azure und setze die API-Parameter von Azure. Beachte, dass für das Modell dall-e-2 die Parameter Quality und Stype auf not_use gesetzt werden müssen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

* Chat beginnen, lassen Sie Azure Bilder erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Blaupause verwendet Azure Chat

Erstellen Sie die folgende Blaupause, stellen Sie die Azure-Optionen ein, und klicken Sie auf Ausführen, um die von Azure zurückgegebenen Chatinformationen auf dem Bildschirm anzuzeigen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Blueprints verwenden Azure zur Erstellung von Bildern

Erstellen Sie folgendes Blueprint, stellen Sie die Azure-Optionen ein und klicken Sie auf Ausführen. Wenn das Erstellen des Bildes erfolgreich ist, wird die Meldung "Create Image Done" auf dem Bildschirm angezeigt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

Gemäß den oben genannten Einstellungen wird das Bild unter dem Pfad D:\Dwnloads\butterfly.png gespeichert.

## Claude

###Der Editor verwendet Claude für Chat und Bildanalyse.

* Neue Unterhaltung (New Chat), ändere ChatApi in Claude und setze die Api-Parameter von Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

* Chat starten

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Bauplan verwendet Claude zum Chatten und Analysieren von Bildern.

* Erstellen Sie einen Knoten `Send Claude Chat Request` im Blueprint mit der rechten Maustaste.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

* Erstellen Sie den Options-Knoten und setzen Sie `Stream=true, Api Key="Ihr API-Schlüssel von Clude", Max Output Tokens=1024`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

* Erstellen von Nachrichten, Texture2D aus einer Datei erstellen und AIChatPlusTexture aus Texture2D erstellen, AIChatPlusTexture zu Nachricht hinzufügen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

* Erstellen Sie ein Event und drucken Sie die Informationen wie im obigen Tutorial auf den Spielbildschirm.

* Der vollständige Blueprint sieht so aus, und wenn Sie den Blueprint ausführen, können Sie auf dem Spielbildschirm die von dem großen Modell zurückgegebenen Nachrichten sehen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Ollama erhalten

* Kann über die offizielle Ollama-Website das Installationspaket für die lokale Installation erhalten werden: [ollama.com](https://ollama.com/)

* Ollama kann über die von anderen bereitgestellte Ollama-Schnittstelle genutzt werden.

###Editor verwendet Ollama zum Chatten und Analysieren von Bildern.

* Neue Unterhaltung (New Chat), ändern Sie ChatApi in Ollama und setzen Sie die API-Parameter von Ollama. Wenn es sich um einen textbasierten Chat handelt, setzen Sie das Modell auf ein Textmodell, wie llama3.1; wenn Bilder verarbeitet werden müssen, setzen Sie das Modell auf ein visionfähiges Modell, wie moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

* Beginne zu chatten

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Bauplan verwendet Ollama für Chats und Bildanalyse.

Erstellen Sie das folgende Blueprint, stellen Sie die Ollama-Optionen ein und klicken Sie auf Ausführen, dann sehen Sie die vom Ollama zurückgegebenen Chatinformationen auf dem Bildschirm angezeigt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###Editor verwendet Gemini

* Neue Sitzung (New Chat), ändern Sie ChatApi in Gemini und setzen Sie die Api-Parameter von Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

* Chat beginnen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###Bauplan verwendet Gemini-Chat

Erstellen Sie die folgende Vorlage, konfigurieren Sie die Gemini-Optionen und klicken Sie auf Ausführen, um die von Gemini zurückgegebenen Chat-Nachrichten auf dem Bildschirm anzuzeigen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

## Deepseek

###Der Editor verwendet Deepseek.

* Neue Unterhaltung (New Chat), ändere ChatApi zu OpenAi und setze die Api-Parameter von Deepseek. Füge die neuen Kandidatenmodelle mit dem Namen deepseek-chat hinzu und stelle das Modell auf deepseek-chat ein.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

* Gespräch beginnen

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Blaupause verwendet Deepseek-Chat

Erstellen Sie den folgenden Blueprint und konfigurieren Sie die entsprechenden Request-Optionen für Deepseek, einschließlich Model, Base Url, End Point Url, ApiKey und weiterer Parameter. Klicken Sie auf Ausführen, um die vom Gemini zurückgegebenen Chatinformationen auf dem Bildschirm anzuzeigen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##Änderungsprotokoll

### v1.5.0 - 2025.01.29

####Neue Funktionen

* Unterstützung für Gemini bei der Audioübertragung

* Der Editor-Tool unterstützt das Senden von Audio und Aufnahmen.

#### Bug Fix

* Behebung des Fehlers beim Kopieren der Sitzung

### v1.4.1 - 2025.01.04

####Problemlösung

* Das Chat-Tool unterstützt nur das Versenden von Bildern, nicht von Nachrichten.

* Behebung des Problems mit dem Senden von Bildern über die OpenAI-Schnittstelle fehlgeschlagen.

* Behebung des Problems, dass in den Einstellungen des OpanAI- und Azure-Chattools die Parameter Quality, Style und ApiVersion fehlen.

### v1.4.0 - 2024.12.30

####Neue Funktion

* (Experimentelle Funktion) Cllama (llama.cpp) unterstützt multimodale Modelle und kann Bilder verarbeiten.

* Alle Typparameter der Blueprint wurden mit detaillierten Hinweisen versehen.

### v1.3.4 - 2024.12.05

####Neue Funktionen

* OpenAI unterstützt die Vision-API

####Fehlerbehebung

* Beheben des Fehlers, wenn OpenAI stream=false ist

### v1.3.3 - 2024.11.25

####Neue Funktionen

* Unterstützung für UE-5.5

####Problembehebung

* Behebung des Problems, dass einige Blueprint nicht wirksam sind.

### v1.3.2 - 2024.10.10

####Problembeseitigung

* Beheben des Absturzes von cllama beim manuellen Stoppen der Anfrage.

* Behebung des Problems, dass die ggml.dll und llama.dll Dateien in der Win-Version des Download-Shops nicht gefunden werden können.

* Überprüfen, ob beim Erstellen der Anfrage im GameThread, CreateRequest-Überprüfung im Spiel-Thread

### v1.3.1 - 2024.9.30

####Neue Funktion

* Fügen Sie einen SystemTemplateViewer hinzu, mit dem Hunderte von System-Einstellungs-Templates angesehen und verwendet werden können.

####Problembehebung

* Beheben Sie das Problem, dass die vom Marktplatz heruntergeladenen Plugins die Bibliothek llama.cpp nicht finden können.

* Behebung des Problems mit zu langen LLAMACpp-Pfaden

* Behebung des Fehlers bei der Verknüpfung mit llama.dll nach dem Windows-Paketieren

* Behebung des Problems mit dem Lesen von Dateipfaden auf iOS/Android

* Behebung des Namensfehlers in den Cllame-Einstellungen

### v1.3.0 - 2024.9.23

####Wichtige neue Funktionen

* Integriert llama.cpp, unterstützt die lokale Offline-Ausführung großer Modelle.

### v1.2.0 - 2024.08.20

####Neue Funktion

* Unterstützung für OpenAI Bildbearbeitung/Bildvariation

* Unterstützung der Ollama API, automatische Abruf der von Ollama unterstützten Modellliste

### v1.1.0 - 2024.08.07

####Neue Funktionen

* Unterstützung von Blaupausen

### v1.0.0 - 2024.08.05

####Neue Funktionen

* Vollständige Grundfunktionen

* Unterstützt OpenAI, Azure, Claude, Gemini

* Integriertes, vollständig funktionsfähiges Editor-Chat-Tool

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte weisen Sie auf etwaige Auslassungen hin. 
