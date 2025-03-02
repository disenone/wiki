---
layout: post
title: UE Plugin AIChatPlus User Manual
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
description: UE-Plugin AIChatPlus Benutzerhandbuch
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE 插件 AIChatPlus User Guide

##Öffentliches Lagerhaus

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Plugin erhalten

[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##Plugin-Beschreibung.

Dieses Plugin unterstützt UE5.2+.

UE.AIChatPlus ist ein UnrealEngine-Plugin, das die Kommunikation mit verschiedenen GPT KI-Chat-Services ermöglicht. Derzeit werden Dienste von OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama und local offline llama.cpp unterstützt. In Zukunft werden auch weitere Serviceprovider unterstützt. Die Implementierung basiert auf asynchronen REST-Anfragen, ist leistungsstark und erleichtert es Entwicklern in Unreal Engine, diese KI-Chat-Services zu integrieren.

UE.AIChatPlus enthält auch ein Editor-Tool, mit dem Sie direkt im Editor auf diese KI-Chat-Services zugreifen können, um Texte und Bilder zu erstellen, Bilder zu analysieren usw.

##Gebrauchsanleitung

###Editor-Chat-Tool

Die Menüleiste "Tools" -> "AIChatPlus" -> "AIChat" öffnet das Chat-Tool des Plugins.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


Das Tool unterstützt Texterstellung, Text-Chat, Bildgenerierung und Bildanalyse.

Die Benutzeroberfläche des Werkzeugs ist im Allgemeinen wie folgt:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

####Hauptfunktionen

Offline large model: Integration of the llama.cpp library, supporting local offline execution of large models 

Textnachricht: Klicke auf die Schaltfläche `Neuer Chat` in der linken unteren Ecke, um eine neue Textnachrichten-Sitzung zu erstellen.

Bildgenerierung: Klicken Sie auf die Schaltfläche "New Image Chat" in der linken unteren Ecke, um eine neue Bildgenerierungssitzung zu erstellen.

Bildanalyse: Einige Chat-Dienste von "New Chat" unterstützen das Senden von Bildern, wie zum Beispiel Claude, Google Gemini. Klicken Sie auf die Schaltfläche 🖼️ oder 🎨 über dem Eingabefeld, um das Bild, das Sie senden möchten, zu laden.

Unterstützung für Blaupausen (Blueprint): Unterstützung für die Erstellung von API-Anfragen über Blaupausen, um Funktionen wie Textnachrichten, Bildgenerierung usw. abzuschließen.

Legen Sie die aktuelle Chat-Rolle fest: Das Dropdown-Menü über dem Chatfenster kann die aktuelle Rolle für den Text festlegen, der gesendet wird. Sie können verschiedene Rollen simulieren, um den KI-Chat anzupassen.

Leeren Sie den Chat: Durch Klicken auf das ❌-Symbol oben im Chatfenster können Sie die Verlaufsnachrichten dieser Unterhaltung löschen.

Dialogvorlage: Hunderte von integrierten Dialogvorlagen für eine einfache Bearbeitung häufiger Fragen.

Global Settings: By clicking on the `Setting` button in the bottom left corner, you can open the global settings window. Here you can configure default text chat, image generation API services, and specify parameters for each API service. The settings will be automatically saved in the project's directory `$(ProjectFolder)/Saved/AIChatPlusEditor`.

Konversationseinstellungen: Klicken Sie auf die Schaltfläche "Einstellungen" oben im Chat-Fenster, um das Einstellungsfenster für die aktuelle Konversation zu öffnen. Es ermöglicht die Änderung des Konversationsnamens, die Änderung des für die Konversation verwendeten API-Dienstes und die individuelle Anpassung der spezifischen Parameter für jedes Gespräch, die die API verwendet. Die Konversationseinstellungen werden automatisch unter `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions` gespeichert.

Ändern des Chat-Inhalts: Wenn Sie mit der Maus über den Chat-Inhalt fahren, erscheint eine Schaltfläche zur Einstellung des jeweiligen Chat-Inhalts. Sie können den Inhalt neu generieren, bearbeiten, kopieren, löschen oder unten einen neuen Inhalt generieren (für Benutzerinhalte).

Bildbetrachtung: Beim Bildgenerieren öffnet ein Klick auf das Bild das Bildbetrachtungsfenster (ImageViewer), das das Speichern des Bildes als PNG/UE Texture unterstützt. Die Texture kann direkt im Inhaltsbrowser (Content Browser) angezeigt werden, um die Verwendung des Bildes im Editor zu erleichtern. Zudem gibt es Optionen wie das Löschen von Bildern, das erneute Generieren von Bildern und das fortlaufende Generieren weiterer Bilder. Für Editor unter Windows ist auch die Bildkopierfunktion verfügbar, um Bilder direkt in die Zwischenablage zu kopieren. Die generierten Bilder werden automatisch im Ordner jeder Sitzung gespeichert, in der Regel unter `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images.

Bauplan:

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

Globale Einstellungen:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Gesprächseinstellungen:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Bitte diese Text in die deutsche Sprache übersetzen:

Bearbeite den Chat-Inhalt: 

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Bildbetrachter:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Verwendung von Offline-Großmodellen

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Dialogvorlage

![system template](assets/img/2024-ue-aichatplus/system_template.png)

###Einführung in den Kerncode

Derzeit sind die Plugins in folgende Module unterteilt:

AIChatPlusCommon: Das Runtime-Modul ist verantwortlich für die Verarbeitung verschiedener AI-API-Anfragen und das Parsen von Antwortinhalten.

AIChatPlusEditor: Editor-Modul, das die Umsetzung des Editor-AI-Chat-Tools übernimmt.

AIChatPlusCllama: The runtime module responsible for encapsulating the interface and parameters of llama.cpp to achieve offline execution of large models.

Thirdparty/LLAMACpp: Runtime-Drittanbietermodul, das die dynamische Bibliothek und Header-Dateien von llama.cpp integriert.

Der UClass, der für das Senden von Anfragen verantwortlich ist, ist FAIChatPlus_xxxChatRequest. Jeder API-Service hat seinen eigenen Request UClass. Die Antworten auf Anfragen werden über die UClass UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase erhalten, man muss nur die entsprechende Callback-Delegierung registrieren.

Vor dem Senden einer Anfrage müssen die Parameter der API und die zu sendende Nachricht eingestellt werden, dies erfolgt durch die Verwendung von FAIChatPlus_xxxChatRequestBody. Die spezifischen Inhalte der Antwort werden auch in FAIChatPlus_xxxChatResponseBody analysiert, und beim Empfang des Rückrufs kann das ResponseBody über bestimmte Schnittstellen abgerufen werden.

Weitere Details zum Quellcode sind im UE-Shop erhältlich: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

## Cllama(llama.cpp)

###Verwenden Sie Offline-Modelle in der Bearbeitungswerkzeug Cllama (llama.cpp).

Bitte verwenden Sie das Offline-Modell llama.cpp im AIChatPlus-Editor-Tool.

Zunächst einmal, laden Sie das Offline-Modell von der HuggingFace-Website herunter: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Platzieren Sie das Modell in einem bestimmten Ordner, zum Beispiel im Verzeichnis Content/LLAMA des Spielprojekts.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Öffnen Sie das AIChatPlus-Editor-Werkzeug: Tools -> AIChatPlus -> AIChat, erstellen Sie eine neue Chat-Sitzung und öffnen Sie die Einstellungsseite der Sitzung.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Stellen Sie die API auf Cllama, aktivieren Sie die benutzerdefinierten API-Einstellungen, fügen Sie den Model-Suchpfad hinzu und wählen Sie ein Modell aus.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Beginne zu chatten!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

###Der Editor verwendet das Offline-Modell Cllama (llama.cpp), um Bilder zu verarbeiten.

Laden Sie das Offline-Modell MobileVLM_V2-1.7B-GGUF von der HuggingFace-Website herunter und speichern Sie es im Verzeichnis Content/LLAMA: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but there is no text to translate.

Konfigurieren des Sitzungsmodells:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Send pictures to start chatting.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

###Der Code verwendet das Offline-Modell Cllama(llama.cpp). 

Erläuterungen zur Verwendung des Offline-Modells llama.cpp im Code.

Zunächst muss die Modelldatei auch im Ordner Content/LLAMA heruntergeladen werden.

Ändern Sie den Code, fügen Sie einen Befehl hinzu und senden Sie über den Befehl eine Nachricht an das Offline-Modell.

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

Nach dem Neukompilieren können Sie im Editor Cmd den Befehl verwenden, um die Ausgabenergebnisse des großen Modells im Protokoll OutputLog zu sehen.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

###Verwenden Sie das Offline-Modell llama.cpp in der Blaupause.

Hier ist eine Anleitung darüber, wie man das Offline-Modell llama.cpp in der Blaupause verwendet.

In der Blueprnt rechts klicken und einen Knoten namens `Send Cllama Chat Request` erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Erstellen Sie den Options-Knoten und legen Sie `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"` fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Erstellen Sie Nachrichten, fügen Sie jeweils eine Systemnachricht und eine Benutzernachricht hinzu.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Erstellen Sie ein Delegate, das die Ausgabeinformationen des Modells entgegennimmt und auf dem Bildschirm ausgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Die vollständige Blaupause sieht wie folgt aus. Wenn die Blaupause ausgeführt wird, erscheint die Meldung zur Rückgabe des großen Modells auf dem Bildschirm.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

###llama.cpp is using the GPU.

"Fügen Sie die Optionen für Chat-Anfragen von Cllama hinzu" mit der Erweiterung "Num Gpu Layer", um das Gpu-Payload von llama.cpp festzulegen, wie im Bild dargestellt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

Sie können den Blueprint-Knoten verwenden, um festzustellen, ob die GPU in der aktuellen Umgebung unterstützt wird, und die unterstützten Backends der aktuellen Umgebung abrufen:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_2.png)

###Bearbeitung der Modelldateien in der .Pak-Datei nach dem Verpacken.

Nach dem Starten von Pak werden alle Ressourcendateien des Projekts in der .Pak-Datei gespeichert, einschließlich der Offline-Modell gguf-Datei.

Da die llama.cpp keine direkte Unterstützung für das Lesen von .Pak-Dateien bietet, müssen die Offline-Modelldateien aus der .Pak-Datei ins Dateisystem kopiert werden.

AIChatPlus bietet eine Funktion, die automatisch Modelldateien aus der .Pak-Datei kopiert und sie im Ordner "Saved" platziert:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

Oder Sie können die Modelldateien in der .Pak-Datei selbst bearbeiten, das Wichtige ist, die Dateien korrekt zu kopieren, weil llama.cpp die .Pak nicht korrekt lesen kann.

## OpenAI

###Der Editor verwendet OpenAI Chat.

Öffnen Sie das Chat-Tool Tools -> AIChatPlus -> AIChat, erstellen Sie eine neue Chat-Sitzung New Chat, setzen Sie die Sitzung ChatApi auf OpenAI, und geben Sie die Schnittstellenparameter ein.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Beginnen Sie mit dem Chat:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Ändern Sie das Modell auf gpt-4o / gpt-4o-mini, um die Bildanalysefunktionen von OpenAI nutzen zu können.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

###Der Editor verwendet OpenAI, um Bilder zu bearbeiten (erstellen/ändern/variiert).

In Chat-Tool neue Bild-Unterhaltung "Neue Bild-Chat" erstellen, Chat-Einstellungen auf OpenAI ändern und Parameter festlegen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Erstellen von Bildern

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Ändern Sie das Bild, ändern Sie den Gesprächstyp des Bildes in "Bearbeiten" und laden Sie zwei Bilder hoch, eines ist das Originalbild, das andere ist das Bild, bei dem die transparente Stelle maskiert ist (Alpha-Kanal ist 0), was den zu ändernden Bereich darstellt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Ändern Sie das Bild, ändern Sie den Typ des Bildchats in 'Variation' und laden Sie ein Bild hoch. OpenAI wird eine Variante des Originalbildes zurückgeben.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

###Blueprints verwenden OpenAI-Modelle für Chats.

In der Blaupause mit der rechten Maustaste einen Knoten erstellen: `Send OpenAI Chat Request In World`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Erstellen Sie den Options-Knoten und legen Sie `Stream=true, Api Key="Ihr API-Schlüssel von OpenAI"` fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Erstellen Sie Nachrichten, fügen Sie jeweils eine Systemnachricht und eine Benutzernachricht hinzu.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Erstellen Sie eine Delegierte, die die Ausgabeinformationen des Modells annimmt und auf dem Bildschirm anzeigt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

The complete blueprint looks like this, run the blueprint and you will see the message returned on the game screen printing the large model.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Die Blaupause nutzt OpenAI, um Bilder zu erstellen.

Erstellen Sie mit der rechten Maustaste einen Knoten "Send OpenAI Image Request" in der Blaupause und legen Sie "In Prompt="a beautiful butterfly"" fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Erstellen Sie den Options-Knoten und setzen Sie `Api Key="Ihr API-Schlüssel von OpenAI"` ein.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Binden Sie das Ereignis "On Images" und speichern Sie das Bild auf der lokalen Festplatte.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

Die vollständige Blaupause sieht so aus, führen Sie die Blaupause aus und Sie können sehen, dass das Bild an der angegebenen Stelle gespeichert wird.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

## Azure

###Der Editor verwendet Azure.

Erstellen Sie einen neuen Chat, ändern Sie ChatApi in Azure und konfigurieren Sie die Azure-API-Parameter.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Beginne die Unterhaltung

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

###Die Anwendung erstellt das Bild mit Azure.

Erstellen Sie eine neue Bildunterhaltung (New Image Chat), ändern Sie ChatApi in Azure und konfigurieren Sie die Azure-API-Parameter. Beachten Sie, dass bei Verwendung des Modells dall-e-2 die Parameter Quality und Stype auf not_use gesetzt werden müssen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Beginnen Sie das Gespräch, damit Azure ein Bild erstellt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

###Blueprint nutzen Azure Chat.

Erstellen Sie das folgende Schema, konfigurieren Sie die Azure-Optionen, klicken Sie auf "Ausführen" und sehen Sie die vom Azure zurückgegebenen Chat-Nachrichten auf dem Bildschirm.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

###Erstellen Sie mit Azure ein Bild mithilfe der Blaupause.

Erstelle das folgende Schema, konfiguriere die Azure-Optionen, klicke auf Ausführen. Wenn das Erstellen des Bildes erfolgreich ist, siehst du die Meldung "Create Image Done" auf dem Bildschirm.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

Gemäß den Einstellungen auf der obigen Blaupause wird das Bild im Pfad D:\Downloads\butterfly.png gespeichert.

## Claude

###Der Editor verwendet Claude zum Chatten und Analysieren von Bildern.

Erstellen Sie einen neuen Chat, ändern Sie ChatApi in Claude um und legen Sie die Api-Parameter für Claude fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Beginnen Sie das Gespräch.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

###Verwendung von Claude, um Bilder zu chatten und zu analysieren.

In der Blaupause mit der rechten Maustaste einen Knoten mit der Bezeichnung `Claude-Chatanfrage senden` erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Erstellen Sie den Options-Knoten und legen Sie `Stream=true, Api Key="Ihr API-Schlüssel von Clude", Max Output Tokens=1024` fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Erstellen Sie Nachrichten, erstellen Sie aus einer Datei einen Texture2D und erstellen Sie aus dem Texture2D ein AIChatPlusTexture. Fügen Sie das AIChatPlusTexture zur Nachricht hinzu.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Folgen Sie dem oben genannten Tutorial, erstellen Sie ein Ereignis und drucken Sie die Informationen auf den Bildschirm des Spiels.

Die vollständige Blaupause sieht so aus, führen Sie die Blaupause aus, um die Nachricht zurückzukehren, die den Bildschirm des Spiels beim Drucken des großen Modells anzeigt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)

## Ollama

###Erhalten Ollama

Sie können das Installationspaket von der Ollama-Website herunterladen und lokal installieren: [ollama.com](https://ollama.com/)

Sie können Ollama über die von anderen bereitgestellte Ollama-Schnittstelle nutzen.

###Der Editor verwendet Ollama zum Chatten und Analysieren von Bildern.

Erstellen Sie einen neuen Chat, ändern Sie ChatApi in Ollama und konfigurieren Sie die Api-Parameter von Ollama. Wenn es sich um einen Text-Chat handelt, setzen Sie das Modell auf einen Text-Modell wie Llama3.1; wenn Bilder verarbeitet werden müssen, setzen Sie das Modell auf ein visionunterstützendes Modell wie Moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Beginnen wir mit dem Chatten.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Blueprint mit Ollama chatten und Bilder analysieren.

Erstellen Sie die folgende Blaupause, konfigurieren Sie die Ollama-Optionen, klicken Sie auf Ausführen, um die Chat-Informationen von Ollama auf dem Bildschirm angezeigt zu bekommen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

## Gemini

###Der Editor verwendet Gemini.

Erstellen Sie eine neue Chat-Sitzung, ändern Sie ChatApi in Gemini und konfigurieren Sie die API-Parameter von Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

* Beginne den Chat

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

###Der Editor verwendet Gemini, um Audio zu senden.

Wählen Sie aus, ob Sie Audio aus einer Datei, aus einem Asset oder über das Mikrofon aufnehmen möchten, um das zu sendende Audio zu erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

Beginnen Sie mit dem Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

###Blueprint verwenden Gemini Chat.

Erstellen Sie das folgende Schema, konfigurieren Sie die Gemini-Optionen, klicken Sie auf Ausführen, und Sie sehen die Chat-Nachrichten, die Gemini zurückgibt, auf dem Bildschirm.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###Verwenden Sie Gemini, um den Sound mit blauem Druck zu senden.

Erstellen Sie die folgende Blaupause, setzen Sie das Laden von Audiodateien ein, konfigurieren Sie die Gemini-Optionen, klicken Sie auf Ausführen, um die Chatnachrichten zu sehen, die Gemini nach der Audiobearbeitung auf dem Bildschirm ausgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

## Deepseek

###Der Editor verwendet Deepseek.

Erstellen Sie einen neuen Chat, ändern Sie ChatAPI in OpenAI und konfigurieren Sie die API-Parameter von Deepseek. Fügen Sie ein neues Kandidatenmodell namens "deepseek-chat" hinzu und setzen Sie das Modell auf "deepseek-chat".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Beginnen Sie mit dem Chatten.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

###Blueprint verwendet Deepseek Chat.

Erstellen Sie das folgende Schema und konfigurieren Sie die mit Deepseek verbundenen Anforderungsoptionen, einschließlich Modell, Basis-URL, Endpunkt-URL, API-Key usw. Klicken Sie auf Ausführen, um die Chatnachrichten anzeigen zu lassen, die von Gemini zurückkommen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_blueprint_chat_2.png)

##Zusätzlich bereitgestellte Blaupausen-Funktionsknoten

###Cllama related

"Cllama Is Valid": Überprüfen, ob Cllama llama.cpp ordnungsgemäß initialisiert wurde.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama unterstützt die GPU"：Feststellung, ob llama.cpp die GPU-Unterstützung in der aktuellen Umgebung bietet

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Holen Sie sich die Support-Backends von Llama": Get all backends supported by current llama.cpp.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama bereitet Modelldatei in Pak vor": Automatically copies model files from Pak to the file system.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###Bildbezogen

Konvertiere UTexture2D in Base64: Wandeln Sie das Bild von UTexture2D in das PNG Base64-Format um.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

"Speichern Sie UTexture2D als .png Datei": Speichern Sie UTexture2D als .png-Datei

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

"Laden Sie die .png-Datei in UTexture2D"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Duplicate UTexture2D": Dupliziere UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###Audio-related

"Lade die .wav-Datei in USoundWave"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

"Konvertiere .wav-Daten in USoundWave": 把 wav 二进制数据转成 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

"Speichern Sie USoundWave in einer .wav-Datei."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

"Holen Sie sich die USoundWave Roh-PCM-Daten": Konvertieren Sie USoundWave in binäre Audiodaten

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"USoundWave" in Base64 umwandeln: Konvertiere USoundWave in Base64-Daten

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicate USoundWave": Dupliziere USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

"Konvertiere Audioaufnahmedaten in eine USoundWave"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

##Aktualisierungshinweise

### v1.6.0 - 2025.03.02

####Neue Funktion

Aktualisierung der Datei llama.cpp auf Version b4604.

Cllama supports GPU backends: cuda and metal.

Das Chat-Tool Cllama unterstützt die Verwendung von Grafikprozessoren (GPU).

Unterstützung für das Lesen von Modelldateien aus einem gepackten Pak.

#### Bug Fix

Behebung des Problems, bei dem Cllama abstürzt, wenn es während des Denkens neu geladen wird.

Beheben Sie den Kompilierungsfehler von iOS.

### v1.5.1 - 2025.01.30

####Neue Funktion

* Nur Gemini darf Audio abspielen.

Optimiere die Methode zum Abrufen von PCMData, dekomprimiere die Audiodaten erst beim Generieren von B64.

Bitte fügen Sie zwei Rückrufe hinzu: OnMessageFinished und OnImagesFinished.

Optimieren Sie die Gemini-Methode, um automatisch die Methode basierend auf bStream zu erhalten.

Fügen Sie einige Blueprint-Funktionen hinzu, um das Konvertieren des Wrappers in den tatsächlichen Typ zu erleichtern und Response-Nachricht und Fehler abzurufen.

#### Bug Fix

Beheben Sie das Problem mit mehrfachen Aufrufen von Request Finish.

### v1.5.0 - 2025.01.29

####Neue Funktion

Unterstützung für das Senden von Audio an Gemini.

Die Editoren unterstützen das Versenden von Audio und Aufnahmen.

#### Bug Fix

Beheben Sie den Fehler beim Kopieren der Sitzung.

### v1.4.1 - 2025.01.04

####Fehlerbehebung

Die Chat-Plattform unterstützt das Versenden von Bildern ohne Text.

Behebung des Fehlers beim Senden von Bildern über die OpenAI-Schnittstelle.

Reparatur des fehlenden Parameters Quality, Style, ApiVersion in den Einstellungen von OpanAI und Azure Chat-Tools.

### v1.4.0 - 2024.12.30

####Neue Funktion

（Experimental Feature）Cllama (llama.cpp) unterstützt Multi-Modal-Modelle und kann Bilder verarbeiten.

Alle Blueprint-Typ-Parameter sind mit ausführlichen Hinweisen versehen.

### v1.3.4 - 2024.12.05

####Neue Funktion

OpenAI unterstützt die Vision API.

####Ein problem behoben.

Fixing the error when OpenAI stream=false.

### v1.3.3 - 2024.11.25

####Neue Funktion

Unterstützt UE-5.5.

####Fehlerbehebung

Fixing the issue of certain blueprints not working.

### v1.3.2 - 2024.10.10

####Problembehebung

Behebung des Absturzes von cllama beim manuellen Stoppen der Anfrage.

Fixing the issue of the win version of the mall download package not finding the ggml.dll and llama.dll files.

Beim Erstellen der Anfrage wird überprüft, ob sich der Vorgang im GameThread befindet.

### v1.3.1 - 2024.9.30

####Neue Funktion

Fügen Sie einen SystemTemplateViewer hinzu, um Hunderte von Systemeinstellungs-Templates anzuzeigen und zu verwenden.

####Fehlerbehebung

Repariere das Plugin, das aus dem Shop heruntergeladen wurde. Die Datei llama.cpp kann die Bibliothek nicht finden.

Behebung des Problems mit der zu langen LLAMACpp-Pfadlänge.

Behebung des llama.dll-Fehlers nach dem Verpacken von Windows.

Beheben Sie das Problem mit dem Dateipfad für das Lesen von Dateien auf iOS/Android.

Behebung des Fehlers beim Einstellen des Namens in Cllame.

### v1.3.0 - 2024.9.23

####Wichtige neue Funktion

Integrierte llama.cpp zur Unterstützung der lokalen Offline-Ausführung großer Modelle.

### v1.2.0 - 2024.08.20

####Neue Funktion.

Unterstützung für OpenAI Image Edit/Image Variation.

Unterstützung der Ollama API, Unterstützung bei der automatischen Erfassung der Liste der Modelle, die von Ollama unterstützt werden.

### v1.1.0 - 2024.08.07

####Neue Funktion

Unterstützung des Blaupausenplans

### v1.0.0 - 2024.08.05

####Neue Funktion

Grundlegende vollständige Funktionen

Unterstützen Sie OpenAI, Azure, Claude, Gemini.

Mit integriertem Editor bietet das Tool eine umfassende Chat-Funktion.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte gib dein [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Identifizieren Sie etwaige Auslassungen. 
