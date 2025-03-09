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

#Editorials - Los geht's

##Text translated into German: 

Editor Chat-Tool

In der Menüleiste können Sie unter Tools -> AIChatPlus -> AIChat das vom Plugin bereitgestellte Chat-Editor-Tool öffnen.

![](assets/img/2024-ue-aichatplus/chat_tool3.png)


Das Tool unterstützt die Erstellung von Texten, Text-Chats, Bildgenerierung und Bildanalyse.

Die Benutzeroberfläche des Tools ist ungefähr wie folgt:

![text chat](assets/img/2024-ue-aichatplus/chat_tool2.png)

![image chat](assets/img/2024-ue-aichatplus/chat_tool.png)

##Hauptfunktion

**Offline Big Model**: Integration von llama.cpp-Bibliothek zur Unterstützung der lokalen Offline-Ausführung von großen Modellen

**Text-Chat**: Klicken Sie auf die Schaltfläche "Neuer Chat" unten links, um eine neue Text-Chat-Sitzung zu erstellen.

**Bildgenerierung**: Klicken Sie auf die Schaltfläche `Neuer Bild-Chat` in der linken unteren Ecke, um eine neue Bildgenerierungssitzung zu erstellen.

**Bildanalyse**: Einige Chatdienste von "New Chat" unterstützen das Senden von Bildern, wie zum Beispiel Claude, Google Gemini. Klicken Sie einfach auf die Schaltfläche 🖼️ oder 🎨 über dem Eingabefeld, um das zu sendende Bild zu laden.

**Audiobearbeitung**: Das Tool ermöglicht das Lesen von Audiodateien (.wav) und die Aufnahme von Audio, um mit KI zu interagieren.

**Aktuelle Chat-Rolle festlegen**: Das Dropdown-Menü oben im Chat-Fenster ermöglicht es, die aktuelle Chat-Rolle festzulegen, mit der der Text gesendet wird. Auf diese Weise können verschiedene Rollen simuliert werden, um den KI-Chat anzupassen.

**Clear chat**: Durch Klicken auf das ❌-Symbol über dem Chatfenster können Sie den Verlauf dieser Unterhaltung löschen.

**Konversationsvorlage**: Enthält Hunderte von voreingestellten Konversationsvorlagen, um gängige Probleme einfach zu behandeln.

**Global Settings**: Klicken Sie auf die Schaltfläche `Einstellung` unten links, um das Fenster für globale Einstellungen zu öffnen. Hier können Sie Standardeinstellungen für Text-Chats festlegen, die API-Services für Bildgenerierung konfigurieren und die spezifischen Parameter für jeden einzelnen Service einstellen. Die Einstellungen werden automatisch im Verzeichnis Ihres Projekts unter `$(ProjectFolder)/Saved/AIChatPlusEditor` gespeichert.

**Konversationseinstellungen**: Öffnen Sie das Einstellungsfenster der aktuellen Konversation, indem Sie oben auf die Schaltfläche für die Einstellungen im Chatfenster klicken. Es ist möglich, den Namen der Konversation zu ändern, den für die Konversation verwendeten API-Dienst zu ändern und spezifische Parameter für die Verwendung der API in jeder Konversation individuell festzulegen. Die Konversationseinstellungen werden automatisch unter `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions` gespeichert.

**Chat Content Editing**: Wenn Sie mit der Maus über den Chat-Inhalt fahren, erscheint ein Einstellungssymbol für den jeweiligen Chat-Inhalt. Sie können den Inhalt neu generieren, bearbeiten, kopieren, löschen oder unterhalb des Inhalts erneut generieren (für Inhalte, bei denen der Benutzer die Rolle des Charakters hat).

**Bildansicht**: Beim Generieren von Bildern können Sie durch Klicken auf ein Bild das Bildanzeigefenster (Bildbetrachter) öffnen, das das Speichern von Bildern als PNG/UE-Textur unterstützt. Die Textur kann direkt im Inhaltsbrowser (Inhaltsbrowser) angezeigt werden, um die Verwendung von Bildern im Editor zu erleichtern. Darüber hinaus können Bilder gelöscht, neu generiert oder weitere Bilder generiert werden. Für Editoren unter Windows werden auch das Kopieren von Bildern unterstützt, um Bilder direkt in die Zwischenablage zu kopieren und bequem zu verwenden. Die generierten Bilder werden automatisch im jeweiligen Sitzungsordner gespeichert, der normalerweise unter `$(ProjectFolder)/Saved/AIChatPlusEditor/Sessions/${GUID}/images` zu finden ist.

Global Settings:

![global settings](assets/img/2024-ue-aichatplus/global_setting.png)

Gesprächseinstellungen:

![session settings](assets/img/2024-ue-aichatplus/session_setting.png)

Ändern Sie den Chat-Inhalt:

![chat edit](assets/img/2024-ue-aichatplus/chat_edit.png)

Bildbetrachter:

![image viewer](assets/img/2024-ue-aichatplus/image_viewer.png)

Verwendung von Offline-Großmodellen

![offline model](assets/img/2024-ue-aichatplus/offline_model.png)

Gesprächsvorlage

![system template](assets/img/2024-ue-aichatplus/system_template.png)

##Verwenden Sie offline-Modell das Editor-Tool Cllama(llama.cpp)

Hier sind die Anweisungen zur Verwendung des Offline-Modells llama.cpp im AIChatPlus-Editor-Tool.

Bitte laden Sie zuerst das Offline-Modell von der HuggingFace-Website herunter: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Platzieren Sie das Modell in einem bestimmten Ordner, zum Beispiel im Verzeichnis des Spielprojekts Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA
> ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Öffnen Sie das AIChatPlus-Editor-Tool: Tools -> AIChatPlus -> AIChat, erstellen Sie eine neue Chat-Sitzung und öffnen Sie die Sitzungseinstellungen-Seite.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_1.png)

Setzen Sie die Api auf Cllama, aktivieren Sie die benutzerdefinierten Api-Einstellungen und fügen Sie einen Modellsuchpfad hinzu. Wählen Sie dann ein Modell aus.

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_2.png)

Beginnen wir mit dem Chatten!

![guide editor](assets/img/2024-ue-aichatplus/guide_editor_3.png)

##Verwenden Sie das Offline-Modell Cllama (llama.cpp) im Editor-Tool zur Bildverarbeitung.

Laden Sie das Offline-Modell MobileVLM_V2-1.7B-GGUF von der HuggingFace-Website herunter und legen Sie es ebenfalls im Verzeichnis Content/LLAMA ab: [ggml-model-q4_k.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/ggml-model-q4_k.gguf)和 [mmproj-model-f16.gguf](https://huggingface.co/ZiangWu/MobileVLM_V2-1.7B-GGUF/resolve/main/mmproj-model-f16.gguf)I'm sorry, but there is no text to translate.

Legen Sie das Sitzungsmodell fest:

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_1.png)

Beginnen Sie mit dem Versand von Bildern, um das Gespräch zu starten.

![guide editor](assets/img/2024-ue-aichatplus/guide_cllama_vision_2.png)

##Der Editor benutzt OpenAI zum Chatten.

Öffnen Sie das Chat-Tool Tools -> AIChatPlus -> AIChat, erstellen Sie einen neuen Chat New Chat, konfigurieren Sie die Sitzung ChatApi auf OpenAI, setzen Sie die Schnittstellenparameter.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_1.png)

Beginnen wir zu chatten:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_2.png)

Ändern Sie das Modell auf gpt-4o / gpt-4o-mini, um die Bilderkennungsfunktion von OpenAI zu nutzen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_chat_3.png)

##Der Editor verwendet OpenAI zur Bearbeitung von Bildern (Erstellung/Anpassung/Varianten).

Erstellen Sie in Ihrem Chat-Tool einen neuen Bild-Chat, passen Sie die Chat-Einstellungen an OpenAI an und konfigurieren Sie die Parameter.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_1.png)

Erstellen Sie ein Bild.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_2.png)

Bearbeiten Sie das Bild, ändern Sie den Gesprächstyp "Image Chat Type" in "Edit" und laden Sie zwei Bilder hoch: ein Originalbild und ein Bild, bei dem die transparenten Stellen (Alpha-Kanal 0) die zu ändernden Bereiche anzeigen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_4.png)

Ändern Sie das Bild, ändern Sie den Chat-Typ von "Bild" in "Variation" und laden Sie ein Bild hoch. OpenAI wird eine Variante des Originalbildes zurückgeben.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_tool_image_5.png)

##Der Editor verwendet Azure.

Erstellen Sie eine neue Unterhaltung (New Chat), ändern Sie ChatApi auf Azure und konfigurieren Sie die API-Parameter von Azure.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_1.png)

Beginnen wir mit dem Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_chat_2.png)

##Der Editor verwendet Azure, um Bilder zu erstellen.

Erstellen Sie eine neue Bildunterhaltung (New Image Chat), ändern Sie ChatApi auf Azure und konfigurieren Sie die Azure-API-Parameter. Bitte beachten Sie, dass bei Verwendung des dall-e-2-Modells die Parameter Quality und Stype auf not_use gesetzt werden müssen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_1.png)

Starten Sie die Unterhaltung und lassen Sie Azure ein Bild erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_tool_image_2.png)

##Der Editor verwendet Claude, um zu chatten und Bilder zu analysieren.

Erstellen Sie einen neuen Chat und ändern Sie ChatApi in Claude, und konfigurieren Sie die API-Parameter von Claude.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_1.png)

Start chatting.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_tool_chat_2.png)

##Der Editor verwendet Ollama zum Chatten und Analysieren von Bildern.

Erstellen Sie einen neuen Chat und ändern Sie ChatApi in Ollama, und konfigurieren Sie die Api-Parameter von Ollama. Wenn es sich um einen Text-Chat handelt, setzen Sie das Modell auf das Textmodell, z. B. Llama3.1; wenn Bilder verarbeitet werden müssen, setzen Sie das Modell auf ein Modell mit Vision-Unterstützung, z. B. Moondream.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_1.png)

Beginnen Sie die Unterhaltung.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_tool_chat_2.png)

###Der Editor verwendet Gemini.

Erstellen Sie einen neuen Chat, ändern Sie ChatApi in Gemini und konfigurieren Sie die API-Parameter von Gemini.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_1.png)

Beginne mit dem Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_chat_2.png)

##Der Editor verwendet Gemini zum Versenden von Audiodateien.

Lese Audio aus einer Datei, aus den Assets oder vom Mikrofon, um das zu sendende Audio zu erzeugen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_1.png)

Beginnen Sie mit dem Chat.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_tool_sound_2.png)

##Der Text lautet: Der Editor verwendet Deepseek.

Erstellen Sie einen neuen Chat und ändern Sie ChatApi in OpenAi um. Legen Sie die API-Parameter von Deepseek fest. Fügen Sie ein neues Kandidatenmodell namens "deepseek-chat" hinzu und setzen Sie das Modell auf "deepseek-chat".

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_1.png)

Begin chatting.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_deepseek_tool_chat_2.png)

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Gib jegliche Auslassungen an. 
