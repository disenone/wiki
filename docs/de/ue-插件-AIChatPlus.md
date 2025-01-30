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
description: UE Plugin AIChatPlus Anleitung
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE 插件 AIChatPlus User Manual

##Öffentliches Lagerhaus

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Plugin erhalten.

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Plugin-Beschreibung

Dieses Plugin unterstützt UE5.2+.

UE.AIChatPlus ist ein UnrealEngine-Plugin, das die Kommunikation mit verschiedenen GPT AI-Chat-Diensten ermöglicht. Derzeit unterstützte Dienste sind OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama und llama.cpp lokal im Offline-Modus. In Zukunft werden weiterhin weitere Dienstanbieter unterstützt. Die Implementierung basiert auf asynchronen REST-Anfragen, ist leistungsfähig und erleichtert es UE-Entwicklern, diese AI-Chat-Dienste zu integrieren.

Gleichzeitig enthält UE.AIChatPlus ein Editor-Tool, mit dem man diese KI-Chat-Dienste direkt im Editor nutzen kann, um Texte und Bilder zu generieren, Bilder zu analysieren usw.

##Gebrauchsanweisung

###Editor-Chat-Tool

Menüleiste Werkzeuge -> AIChatPlus -> AIChat öffnet das von dem Plugin bereitgestellte Editor-Chat-Tool.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


Das Tool unterstützt die Textgenerierung, Textchat, die Bilderzeugung und Bildanalyse.

Die Benutzeroberfläche des Werkzeugs sieht ungefähr so aus:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Hauptfunktionen

Offline Large Model: Integration of the llama.cpp library, supporting local offline execution of large models.

* Text-Chat: Klicken Sie auf die Schaltfläche `Neuen Chat` in der linken unteren Ecke, um eine neue Text-Chat-Sitzung zu erstellen.

* Bildgenerierung: Klicken Sie auf die Schaltfläche `Neues Bild-Chat` in der linken unteren Ecke, um eine neue Bildgenerierungssitzung zu erstellen.

Bildanalyse: Einige Chat-Dienste von 'New Chat' unterstützen das Senden von Bildern, wie zum Beispiel Claude, Google Gemini. Klicken Sie einfach auf die Schaltfläche 🖼️ oder 🎨 oben im Eingabefeld, um das zu sendende Bild zu laden.

* Unterstützte Blaupausen (Blueprint): Unterstützung für die Erstellung von API-Anfragen für Textchats, Bildgenerierung und weitere Funktionen.

Festlegen des aktuellen Chat-Charakters: Das Dropdown-Menü über dem Chat-Fenster ermöglicht die Auswahl des aktuellen Charakters, von dem die Texte gesendet werden. Dies ermöglicht die Simulation verschiedener Charaktere zur Anpassung des KI-Chats.

Leeren der Konversation: Das X-Symbol oben im Chatfenster kann verwendet werden, um den Verlaufsnachrichten der aktuellen Konversation zu löschen.

Gesprächsvorlage: Hunderte von integrierten Gesprächssettings stehen zur Verfügung, um häufig auftretende Probleme einfach zu behandeln.

Globale Einstellungen: Klicken Sie auf die Schaltfläche "Einstellungen" unten links, um das Fenster für die globalen Einstellungen zu öffnen. Hier können Sie den Standard-Text-Chat, den API-Dienst für die Bildgenerierung und die spezifischen Parameter für jeden API-Dienst festlegen. Die Einstellungen werden automatisch im Projektverzeichnis `$(ProjectFolder)/Saved/AIChatPlusEditor` gespeichert.

* Gesprächseinstellungen: Klicken Sie auf die Schaltfläche "Einstellungen" oberhalb des Chatfensters, um das Einstellungsfenster des aktuellen Gesprächs zu öffnen. Es wird unterstützt, den Gesprächsnamen zu ändern, den verwendeten API-Dienst anzupassen und spezifische Parameter für die API jeder Sitzung unabhängig festzulegen. Die Gesprächst Einstellungen werden automatisch im `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions` gespeichert.

Ändern des Chat-Inhalts: Wenn Sie mit der Maus über einen Chat-Inhalt fahren, wird eine Schaltfläche zur Inhaltssteuerung für diesen einzelnen Chat-Inhalt angezeigt. Zu den Optionen gehören das Neugenerieren des Inhalts, das Bearbeiten, Kopieren, Löschen sowie das erneute Generieren von Inhalten unten (für Inhalte, bei denen der Benutzer die Rolle des Absenders hat).

* Bildanzeige: Bei der Bilderzeugung öffnet ein Klick auf das Bild das Bildansichtsfenster (ImageViewer), das das Speichern des Bildes als PNG/UE-Textur unterstützt. Die Textur kann direkt im Inhaltsbrowser (Content Browser) angezeigt werden, was die Verwendung von Bildern im Editor erleichtert. Außerdem werden Funktionen wie das Löschen von Bildern, das erneute Generieren von Bildern und das Fortsetzen der Generierung weiterer Bilder unterstützt. Für den Editor unter Windows wird zusätzlich das Kopieren von Bildern unterstützt, sodass Bilder direkt in die Zwischenablage kopiert werden können, was die Benutzung erleichtert. Die Bilder, die während der Sitzung generiert werden, werden automatisch in jedem Sitzungsordner gespeichert, normalerweise unter dem Pfad `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Bauplan:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Allgemeine Einstellungen:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Konversationseinstellungen:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Bearbeiten Sie den Chat-Inhalt:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Bildbetrachter:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Verwendung von Offline-Großmodellen

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Dialogvorlage

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Kerncode Einführung

Derzeit ist das Plugin in folgende Module unterteilt:

AIChatPlusCommon: Runtime-Modul, das für die Verarbeitung von verschiedenen AI-API-Anfragen und die Analyse von Antwortinhalten zuständig ist.

AIChatPlusEditor: Editor-Modul, verantwortlich für die Implementierung des Editor-KI-Chat-Tools.

AIChatPlusCllama: Laufzeitmodul (Runtime), das die Schnittstelle und Parameter von llama.cpp kapselt und die Offline-Ausführung großer Modelle ermöglicht.

* Thirdparty/LLAMACpp: Laufzeit-Drittanbieter-Modul, das die dynamischen Bibliotheken und Header-Dateien von llama.cpp integriert.

Der UClass, der für das Senden von Anfragen zuständig ist, ist FAIChatPlus_xxxChatRequest. Jeder API-Dienst hat sein eigenes unabhängiges Request UClass. Die Antworten auf die Anfragen werden durch die UClass UAIChatPlus_ChatHandlerBase/UAIChatPlus_ImageHandlerBase erhalten, es ist nur erforderlich, die entsprechenden Rückruffunktionen zu registrieren.

Bevor eine Anfrage gesendet wird, müssen die API-Parameter und die Nachricht festgelegt werden. Dies geschieht über FAIChatPlus_xxxChatRequestBody. Der spezifische Inhalt der Antwort wird im FAIChatPlus_xxxChatResponseBody analysiert, und beim Empfang des Rückrufs kann das ResponseBody über eine spezielle Schnittstelle abgerufen werden.

Weitere Quellcodedetails sind im UE Shop erhältlich: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Verwenden Sie das Offline-Modell Cllama (llama.cpp) mit dem Editor-Tool.

Dieser Text lautet auf Deutsch:

Hier sind Anweisungen zur Verwendung des Offline-Modells llama.cpp im AIChatPlus-Editor-Tool.

* Zuerst das Offline-Modell von der HuggingFace-Website herunterladen: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Legen Sie das Modell in einen bestimmten Ordner, zum Beispiel im Verzeichnis Content/LLAMA des Spielprojekts.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

* Öffnen Sie das AIChatPlus-Bearbeitungswerkzeug: Tools -> AIChatPlus -> AIChat, erstellen Sie eine neue Chatsitzung und öffnen Sie die Konfigurationsseite der Sitzung.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Stellen Sie die API auf Cllama ein, aktivieren Sie die benutzerdefinierten API-Einstellungen, fügen Sie den Modellsuchpfad hinzu und wählen Sie ein Modell aus.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

* Lass uns chatten!!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Der Editor verwendet das Offline-Modell Cllama (llama.cpp) zur Bearbeitung von Bildern.

Laden Sie das Offline-Modell MobileVLM_V2-1.7B-GGUF von der HuggingFace-Website herunter und legen Sie es ebenfalls im Verzeichnis Content/LLAMA ab: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I am sorry, but there is nothing to translate in the text you provided.

* Modell für die Sitzung festlegen:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

* Bild senden, um den Chat zu starten

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###Der Code verwendet das Offline-Modell Cllama (llama.cpp).

Die folgende Anleitung beschreibt, wie man das Offline-Modell llama.cpp im Code verwendet.

Zuerst müssen die Modell-Dateien ebenfalls in den Ordner Content/LLAMA heruntergeladen werden.

Ändern Sie den Code, um einen Befehl hinzuzufügen und über diesen Befehl eine Nachricht an das Offline-Modell zu senden.

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

* Nach der erneuten Kompilierung können Sie im Editor Cmd den Befehl verwenden, um die Ausgaberesultate des großen Modells im Protokoll OutputLog zu sehen.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Blueprint verwendet das Offline-Modell llama.cpp

Die folgende Anleitung erläutert, wie man Offline-Modelle wie llama.cpp in Blueprints verwendet.

* Klicken Sie mit der rechten Maustaste im Blueprint und erstellen Sie einen Knoten `Send Cllama Chat Request`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

* Erstellen Sie den Options-Knoten und setzen Sie `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Erstellen Sie Nachrichten, fügen Sie jeweils eine Systemnachricht und eine Benutzernachricht hinzu.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Erstellen Sie einen Delegaten, der die Ausgaben des Modells annimmt und auf dem Bildschirm ausgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Eine vollständige Blaupause sieht so aus, führen Sie die Blaupause aus und Sie werden die Nachricht sehen, die auf dem Bildschirm erscheint, die das Drucken eines großen Modells bestätigt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

## OpenAI

###Editor verwendet OpenAI-Chat

* Öffnen Sie das Chat-Tool Tools -> AIChatPlus -> AIChat, erstellen Sie eine neue Chatsitzung New Chat, setzen Sie die Sitzung ChatApi auf OpenAI, setzen Sie die Schnittstellenparameter.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

* Chat starten:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Wechseln Sie das Modell auf gpt-4o / gpt-4o-mini, um die Bildanalysefunktionen von OpenAI zu nutzen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###Der Editor verwendet OpenAI, um Bilder zu bearbeiten (erstellen/ändern/variieren).

* Erstellen Sie im Chat-Tool eine neue Bildunterhaltung New Image Chat, ändern Sie die Sitzungseinstellungen auf OpenAI und passen Sie die Parameter an.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Erstellen von Bildern

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

* Ändern Sie das Bild, ändern Sie den Bild-Chattyp in Bearbeiten und laden Sie zwei Bilder hoch, eines ist das Originalbild und das andere ist die Maske, wobei die transparenten Bereiche (Alpha-Kanal = 0) die Stellen darstellen, die geändert werden müssen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

* Ändern Sie den Konversationstyp von Image Chat in Variation und laden Sie ein Bild hoch. OpenAI wird eine Variation des originalen Bildes zurückgeben.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Blueprint nutzt OpenAI Model Chats.

In der Blaupause mit der rechten Maustaste einen Knoten `Send OpenAI Chat Request In World` erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

* Erstellen Sie einen Options-Knoten und setzen Sie `Stream=true, Api Key="Ihr API-Schlüssel von OpenAI"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

* Erstellen Sie Nachrichten und fügen Sie jeweils eine Systemnachricht und eine Benutzernachricht hinzu.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Erstellen Sie einen Delegaten, der die Ausgabeinformationen des Modells empfängt und auf dem Bildschirm ausgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

* Der vollständige Blueprint sieht so aus, wenn Sie den Blueprint ausführen, können Sie den Spielbildschirm sehen, der die Nachrichten des zurückgegebenen großen Modells anzeigt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Entwurf mit OpenAI erstelltes Bild.

In der Blaupause mit der rechten Maustaste einen Knoten namens "Send OpenAI Image Request" erstellen und "In Prompt="a beautiful butterfly"" einstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Erstellen Sie den Options-Knoten und legen Sie `Api Key="Ihr API-Schlüssel von OpenAI"` fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

* Binde das On Images-Ereignis und speichere die Bilder auf der lokalen Festplatte.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

* Der vollständige Plan sieht so aus, indem Sie den Plan ausführen, können Sie die Bilder am angegebenen Speicherort sehen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###Der Editor verwendet Azure.

Erstellen einer neuen Unterhaltung (New Chat), indem Sie ChatApi auf Azure umstellen und die Api-Parameter von Azure einrichten.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Beginnen Sie zu plaudern.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###Editor verwendet Azure, um Bilder zu erstellen.

Erstellen Sie ein neues Bild-Chat-Gespräch (*New Image Chat*), ändern Sie *ChatApi* auf *Azure* und konfigurieren Sie die Azure-API-Parameter. Beachten Sie, dass bei Verwendung des *dall-e-2*-Modells die Parameter *Quality* und *Stype* auf *not_use* gesetzt werden müssen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

* Beginnen Sie den Chat und lassen Sie Azure Bilder erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Blueprint verwenden Azure Chat.

Erstellen Sie das folgende Blueprint, richten Sie die Azure-Optionen ein, und klicken Sie auf Ausführen, um die von Azure zurückgegebenen Chatnachrichten auf dem Bildschirm zu sehen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Blueprint verwendet Azure zur Erstellung von Bildern.

Erstelle das folgende Schema, konfiguriere die Azure-Optionen, klicke auf "Ausführen". Wenn das Erstellen des Bildes erfolgreich ist, wird die Meldung "Bild erstellen erfolgreich" auf dem Bildschirm angezeigt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

Gemäß den oben genannten Einstellungen wird das Bild im Pfad D:\Dwnloads\butterfly.png gespeichert.

## Claude

###Der Editor verwendet Claude für Chat und Bildanalyse.

* Neue Unterhaltung erstellen (New Chat), ändern Sie ChatApi in Claude und stellen Sie die Api-Parameter für Claude ein.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

* Chat starten

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Blueprint verwenden Claude zum Chatten und Analysieren von Bildern.

In der Blaupause mit der rechten Maustaste einen Knoten namens "Send Claude Chat Request" erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

* Erstellen Sie einen Options-Knoten und setzen Sie `Stream=true, Api Key="Ihr API-Schlüssel von Clude", Max Output Tokens=1024`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Erstellen von Nachrichten, Erstellen eines Texture2D aus einer Datei und Erstellen von AIChatPlusTexture aus dem Texture2D, dann Hinzufügen des AIChatPlusTexture zur Nachricht.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

* Erstelle ein Event wie im obigen Tutorial und drucke die Informationen auf den Spielbildschirm.

Die vollständige Blaupause sieht so aus, führe die Blaupause aus und du wirst auf dem Spielschirm die Nachricht sehen, die das gedruckte große Modell zurückgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Ollama abrufen

* Die Installationspakete können über die offizielle Ollama-Website heruntergeladen werden: [ollama.com](https://ollama.com/)

Sie können Ollama über die von anderen bereitgestellte Ollama-Schnittstelle verwenden.

###Editor verwendet Ollama, um zu chatten und Bilder zu analysieren.

Erstellen Sie einen neuen Chat und ändern Sie ChatApi in Ollama. Legen Sie die Api-Parameter für Ollama fest. Wenn es sich um einen Text-Chat handelt, setzen Sie das Modell auf den Text-Modus, wie z.B. llama3.1; Wenn Bilder verarbeitet werden müssen, wählen Sie ein Modell aus, das die Bildverarbeitung unterstützt, z.B. moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Beginnen Sie mit dem Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Blueprint verwenden Ollama zum Chatten und Analysieren von Bildern.

Erstellen Sie das folgende Schema, konfigurieren Sie die Ollama-Optionen, klicken Sie auf Ausführen und Sie werden die Chat-Nachrichten sehen, die von Ollama auf dem Bildschirm ausgegeben werden.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###Der Editor verwendet Gemini.

* Neue Sitzung (New Chat), ändern Sie ChatApi zu Gemini und setzen Sie die Api-Parameter von Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Bitte übersetzen Sie den folgenden Text ins Deutsche: 

"Beginne den Chat."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###Der Editor verwendet Gemini, um Audio zu senden.

* Wählen Sie Audio aus Datei lesen / Audio aus Asset lesen / Audio vom Mikrofon aufnehmen, um die zu sendende Audio zu generieren.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

Beginnen Sie mit dem Chatten.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###Verwenden Sie den Blueprint für Chats mit Gemini.

Erstellen Sie folgendes Blueprint, stellen Sie die Gemini Options ein, klicken Sie auf Ausführen, und Sie können die von Gemini zurückgegebenen Chatnachrichten auf dem Bildschirm sehen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###Blueprint verwendet Gemini zum Senden von Audio.

Erstellen Sie das folgende Blueprint, laden Sie die Audio-Datei, konfigurieren Sie die Gemini-Optionen und klicken Sie auf Ausführen. Dann können Sie die im Bildschirm ausgegebenen Chat-Nachrichten sehen, die von Gemini nach der Verarbeitung der Audiodatei zurückgegeben werden.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###Der Editor verwendet Deepseek.

Erstellen Sie einen neuen Chat, ändern Sie ChatApi in OpenAi und konfigurieren Sie die API-Parameter von Deepseek. Fügen Sie ein neues Kandidatenmodell namens Deepseek-Chat hinzu und setzen Sie das Modell auf Deepseek-Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Beginnen Sie mit dem Gespräch.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Blaupause verwendet Deepseek-Chat

Erstellen Sie das folgende Blueprint und richten Sie die entsprechenden Request-Optionen für Deepseek ein, einschließlich Model, Base Url, End Point Url, ApiKey und weiteren Parametern. Klicken Sie auf Ausführen, um die von Gemini zurückgegebenen Chatinformationen auf dem Bildschirm anzuzeigen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##Änderungsprotokoll

### v1.5.1 - 2025.01.30

####Neue Funktion

* Nur Gemini darf Audio abspielen.

* Optimierung der Methode zur Erfassung von PCMData, um die Audiodaten erst beim Erzeugen von B64 zu dekomprimieren.

Bitte füge zwei Callbacks hinzu: OnMessageFinished und OnImagesFinished.

Optimieren Sie die Gemini-Methode, um automatisch die Methode basierend auf bStream zu erhalten.

Fügen Sie einige Blueprint-Funktionen hinzu, um das Umwandeln von Wrapper in tatsächliche Typen zu erleichtern und Response-Nachrichten und Fehler abzurufen.

#### Bug Fix

Behebung des Problems mit mehrfachem Aufruf von "Request Finish".

### v1.5.0 - 2025.01.29

####Neue Funktion

* Unterstützung für die Audioübertragung an Gemini

* Die Editor-Tools unterstützen das Senden von Audio und Aufnahmen.

#### Bug Fix

* Behebung des Bugs beim Kopieren von Sitzungen

### v1.4.1 - 2025.01.04

####Problembehebung

* Der Chat-Tool unterstützt das Senden von Bildern ohne Textnachrichten.

* Behebung des Problems mit dem Senden von Bildern über die OpenAI-Schnittstelle fehlgeschlagen.

Beheben der fehlenden Parameter Quality, Style und ApiVersion in den Einstellungen von OpanAI und Azure-Chat-Tools.

### v1.4.0 - 2024.12.30

####Neue Funktionen

* (Experimentelle Funktion) Cllama (llama.cpp) unterstützt multimodale Modelle und kann Bilder verarbeiten.

Alle Blauprint-Typenparameter wurden mit detaillierten Hinweisen versehen.

### v1.3.4 - 2024.12.05

####Neue Funktionen

* OpenAI unterstützt die Vision-API

####Fehlerbehebung

* Behebung des Fehlers, wenn OpenAI stream=false ist.

### v1.3.3 - 2024.11.25

####Neue Funktionen

Unterstützt UE-5.5.

####Problembehebung

Fixing the issue of certain blueprints not working.

### v1.3.2 - 2024.10.10

####Fehlerbehebung

* Beheben Sie den Absturz von cllama beim manuellen Stoppen der Anfrage.

* Behebung des Problems, dass die ggml.dll und llama.dll Dateien in der heruntergeladenen Win-Version des Marktplatzes nicht gefunden werden können.

Beim Erstellen der Anfrage überprüfen, ob sich im GameThread befindet.

### v1.3.1 - 2024.9.30

####Neue Funktion

Fügen Sie einen SystemTemplateViewer hinzu, mit dem Sie Hunderte von Systemeinstellungs-Templates anzeigen und verwenden können.

####Fehlerbehebung

Repariere das Plugin, das aus dem App Store heruntergeladen wurde. Llama.cpp kann die Verknüpfungsbibliothek nicht finden.

Behebung des Problems mit zu langen Pfaden in LLAMACpp.

Beheben Sie den Linkfehler llama.dll nach dem Windows-Paket.

Beheben Sie das Problem beim Lesen des Dateipfads in iOS/Android.

* Behebung des Namensfehlers in den Cllame-Einstellungen

### v1.3.0 - 2024.9.23

####Wichtige neue Funktionen

Integriert llama.cpp, unterstützt die Ausführung großer Modelle offline lokal.

### v1.2.0 - 2024.08.20

####Neue Funktion

* Unterstützung für OpenAI Bildbearbeitung/Bildvariation

Unterstützt Ollama API, um die Liste der von Ollama unterstützten Modelle automatisch abzurufen.

### v1.1.0 - 2024.08.07

####Neue Funktionen

Unterstützung der Blaupause

### v1.0.0 - 2024.08.05

####Neue Funktion

* Vollständige Grundfunktionen

* Unterstützung für OpenAI, Azure, Claude, Gemini

* Integrierter, funktionaler Editor-Chat-Tool

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte hinterlassen Sie Ihr [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)weist auf etwaige Auslassungen hin. 
