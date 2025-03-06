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

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 编辑器篇 - Get Started" />

#Editorial Section - Get Started

##Editor-Chat-Tool

Das Menü Tools -> AIChatPlus -> AIChat ermöglicht den Zugriff auf das Chat-Tool des Plugins.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


Das Tool unterstützt die Generierung von Texten, Text-Chats, die Generierung von Bildern und die Bildanalyse.

Die Benutzeroberfläche des Tools sieht ungefähr so aus:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

##Hauptfunktion

* **Offline Big Model**: Integration of llama.cpp library, supporting local offline execution of big models.

* **Textnachrichten**: Klicken Sie auf die Schaltfläche `Neuer Chat` in der linken unteren Ecke, um eine neue Textnachrichtenunterhaltung zu erstellen.

* **Bildgenerierung**: Klicken Sie auf die Schaltfläche "Neuer Bild-Chat" in der linken unteren Ecke, um eine neue Bildgenerierungssitzung zu erstellen.

* **Bildanalyse**: Einige Chat-Dienste in `New Chat` unterstützen das Versenden von Bildern, z.B. Claude, Google Gemini. Klicken Sie einfach auf die Schaltfläche 🖼️ oder 🎨 über dem Eingabefeld, um das zu sendende Bild zu laden.

* **Audioverarbeitung**: Das Tool ermöglicht das Lesen von Audiodateien (.wav) und Aufnahmefunktionen, um das aufgenommene Audio mit KI zu verwenden.

* **Wählen Sie die aktuelle Chat-Rolle aus**: Das Dropdown-Menü oben im Chatfenster ermöglicht es Ihnen, die Rolle auszuwählen, von der aus Textnachrichten gesendet werden sollen. Auf diese Weise können verschiedene Rollen simuliert werden, um das KI-Chatverhalten anzupassen.

* **Chatverlauf löschen**: Durch Klicken auf das ❌-Symbol oben im Chatfenster können Sie den Verlauf der aktuellen Unterhaltung löschen.

* **Dialogvorlagen**: Enthält Hunderte von vorgefertigten Dialogvorlagen, um häufige Probleme einfach zu lösen.

* **Global Settings**: Durch Klicken auf die Schaltfläche `Einstellungen` in der linken unteren Ecke können Sie das Fenster für globale Einstellungen öffnen. Hier können Sie Standardtext-Chat, das API-Service für die Bildgenerierung einstellen und spezifische Parameter für jedes API-Service festlegen. Die Einstellungen werden automatisch im Verzeichnis des Projekts unter `$(ProjectFolder)/Saved/AIChatPlusEditor` gespeichert.

* **Konversationseinstellungen**: Durch Klicken auf die Schaltfläche "Einstellungen" oben im Chatfenster können Sie das Einstellungsfenster für die aktuelle Konversation öffnen. Es ermöglicht die Änderung des Konversationsnamens, die Änderung des API-Dienstes der Konversation und die individuelle Einstellung spezifischer Parameter für die Verwendung von APIs in jeder Konversation. Die Konversationseinstellungen werden automatisch im Ordner `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions` gespeichert.

* **Chat-Verlauf bearbeiten**: Wenn Sie mit der Maus über den Chat-Verlauf fahren, wird ein Einstellungsbutton für den jeweiligen Chat-Verlauf angezeigt. Hier können Sie den Inhalt neu generieren, bearbeiten, kopieren, löschen oder unterhalb des Chats neu erstellen (für vom Benutzer erstellte Inhalte).

* **Bildbetrachtung**: Beim Bildgenerieren wird beim Klicken auf das Bild das Bildbetrachtungsfenster (ImageViewer) geöffnet. Es unterstützt das Speichern von Bildern als PNG/UE-Texture. Die Texturen können direkt im Inhaltsbrowser (Content Browser) angezeigt werden, um die Verwendung von Bildern im Editor zu erleichtern. Außerdem werden Funktionen wie Bildlöschen, Bildneugenerierung, fortlaufende Bildgenerierung und andere unterstützt. Für Editoren unter Windows wird auch das Kopieren von Bildern unterstützt, um sie direkt in die Zwischenablage zu kopieren und bequem zu verwenden. Die vom Gespräch generierten Bilder werden automatisch im jeweiligen Sitzungsordner gespeichert, normalerweise im Pfad `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images`.

Global settings:

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

##Verwenden des Editor-Tools mit Offline-Modell Cllama (llama.cpp)

Hier sind die Anweisungen zur Verwendung des Offline-Modells llama.cpp im AIChatPlus-Editor-Tool.

Zunächst laden Sie das Offline-Modell von der HuggingFace-Website herunter: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Platzieren Sie das Modell in einem bestimmten Ordner, zum Beispiel im Verzeichnis Content/LLAMA des Spielprojekts.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Öffnen Sie das AIChatPlus Editor-Tool: Tools -> AIChatPlus -> AIChat, erstellen Sie eine neue Chat-Sitzung und öffnen Sie die Sitzungseinstellungen.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Stelle die API auf Cllama ein, aktiviere benutzerdefinierte API-Einstellungen, füge den Modellsuchpfad hinzu und wähle ein Modell aus.


![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Beginne zu chatten!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

##Die Editoreinstellungen verwenden das Offline-Modell Cllama (llama.cpp), um Bilder zu verarbeiten.

Laden Sie das Offline-Modell MobileVLM_V2-1.7B-GGUF von der HuggingFace-Website herunter und speichern Sie es im Verzeichnis Content/LLAMA unter dem Namen [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)(https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but I cannot provide a translation for this content as it does not contain any text to be translated.

Setzen Sie das Modell der Sitzung:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)


Send a picture to start a conversation.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

##Der Editor verwendet OpenAI Chat.

Öffnen Sie das Chat-Tool Tools -> AIChatPlus -> AIChat, erstellen Sie eine neue Chat-Sitzung New Chat, legen Sie die Sitzung ChatApi auf OpenAI fest, setzen Sie die Schnittstellenparameter.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Beginnen wir zu chatten:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Ändern Sie das Modell auf gpt-4o / gpt-4o-mini, um die Bildanalysefunktion von OpenAI nutzen zu können.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

##Der Editor nutzt OpenAI zur Bearbeitung von Bildern (Erstellung/Änderung/Variation).

In einem Chat-Tool eine neue Bildunterhaltung namens "Neue Bildunterhaltung" erstellen, die Konversationseinstellungen auf OpenAI ändern und Parameter festlegen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Erstellen von Bildern

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Ändern Sie das Bild, ändern Sie den Gesprächstyp des Bildes in "Bearbeiten" und laden Sie zwei Bilder hoch. Ein Bild ist das Originalbild, das andere ist ein Maskenbild, bei dem die transparente Stelle (Alpha-Kanal 0) die zu ändernde Stelle anzeigt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Ändern Sie das Bild, indem Sie den Chat-Modus "Image Chat Type" in "Variation" ändern und ein Bild hochladen. OpenAI wird eine Variation des Originalbilds zurückgeben.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

##Der Editor verwendet Azure.

Erstellen Sie eine neue Chat-Sitzung (New Chat), ändern Sie ChatApi zu Azure und konfigurieren Sie die Azure-API-Parameter.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Beginnen Sie mit dem Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

##Der Editor erstellt Bilder mit Azure.

Errichten Sie eine neue Bildunterhaltung (New Image Chat), ändern Sie ChatApi zu Azure und legen Sie die Azure-API-Parameter fest. Beachten Sie, dass bei dem dall-e-2-Modell die Parameter Quality und Stype auf not_use gesetzt werden müssen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Beginnen Sie mit der Unterhaltung, damit Azure ein Bild erstellen kann.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

##Der Editor verwendet Claude zum Chatten und Analysieren von Bildern.

Erstellen Sie eine neue Unterhaltung (New Chat), ändern Sie die ChatApi in Claude und konfigurieren Sie die Api-Parameter von Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Beginnen Sie die Unterhaltung.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

##Der Editor verwendet Ollama zum Chatten und Analysieren von Bildern.

Erstellen Sie einen neuen Chat, ändern Sie ChatApi in Ollama und konfigurieren Sie die Api-Parameter von Ollama. Wenn es sich um einen Text-Chat handelt, stellen Sie das Modell auf Textmodell wie Llama3.1 ein; wenn Bilder verarbeitet werden müssen, wählen Sie ein Modell aus, das Vision unterstützt, wie zum Beispiel Moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Beginnen Sie den Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)


###Der Editor verwendet Gemini.

Erstellen Sie einen neuen Chat (New Chat), ändern Sie ChatApi in Gemini und konfigurieren Sie die Api-Parameter von Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Begin conversation.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

##Der Editor verwendet Gemini, um Audiodateien zu senden.

Lese Audio aus Datei / Lese Audio aus Assets / Nehme Audio vom Mikrofon auf, um das zu sendende Audio zu erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

Beginnen Sie den Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

##Der Editor verwendet Deepseek.

* New Chat erstellen, ändere ChatApi zu OpenAi und konfiguriere die Api-Parameter von Deepseek. Füge ein neues Kandidatenmodell namens Deepseek-Chat hinzu und stelle das Modell auf Deepseek-Chat ein.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Beginne den Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte gib dein [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Erkennen Sie alle ausgelassenen Punkte. 
