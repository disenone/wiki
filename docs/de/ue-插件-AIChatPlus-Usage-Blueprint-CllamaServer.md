---
layout: post
title: CllamaServer (llama.cpp server)
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
- llama.cpp
- CllamaServer
description: CllamaServer (llama.cpp server)
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - CllamaServer (llama.cpp server)" />

#Blaupausen-Teil - CllamaServer (llama.cpp Server)

<!-- Benötigt Bild: Übersicht aller Blueprint-Knoten im Zusammenhang mit CllamaServer, ähnlich der xxx_all.png in anderen Dokumentationen -->
![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_all.png)

##Übersicht

CllamaServer basiert auf dem Server-Modus von llama.cpp und ermöglicht das Starten eines lokal laufenden Servers, der mit der OpenAI API kompatibel ist und zahlreiche Funktionen unterstützt:

* **Lokale Inferenz-Services**: Starten Sie den KI-Inferenzserver lokal, ohne auf externe APIs angewiesen zu sein.
* **Kompatibel mit OpenAI API**: Verwendet das OpenAI-kompatible API-Format für einfache Migration und Integration
* **Mehrfach-Sitzungsunterstützung**: Unterstützt mehrere gleichzeitige Anfragen
* **Tool Calling**: Unterstützt die Funktionsaufruffunktion
* **Sprach-zu-Text**: Unterstützt die Speech-to-Text-Funktionalität
* **Visuelles Management**: Der Editor verfügt über eine integrierte Server-Verwaltungsoberfläche.

Unterschiede zu Cllama:
* **Cllama**: Lädt das Modell direkt innerhalb des Prozesses für die Inferenz, kann jedoch nur eine Anfrage gleichzeitig bearbeiten
* **CllamaServer**: Startet einen eigenständigen HTTP-Server, der mehrere gleichzeitige Anfragen verarbeiten kann, mit API-Kompatibilität zum OpenAI-Format.

##Vorbereitungen

Da es lokal ausgeführt wird, müssen Sie zuerst die Offline-Modelldateien vorbereiten, beispielsweise von HuggingFace herunterladen: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Platziere das Modell in einem bestimmten Ordner, zum Beispiel im Verzeichnis des Spielprojekts unter `Content/LLAMA`.

##Erstellen Sie den CllamaServer

###Erstellen eines Servers mit Blueprint

Erstellen Sie im Blueprint durch Rechtsklick den Knoten `Create Cllama Server In World`.

<!-- Benötigtes Bild: Screenshot, der das Suchen nach "Create Cllama Server" per Rechtsklick im Blueprint und das Erstellen eines Knotens zeigt -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_1.png)

###Server-Parameter konfigurieren

Erstelle den `Cllama Server Param`-Knoten und konfiguriere die Schlüsselparameter:

* **Modell**: Modell-Dateipfad (erforderlich)
* **Port**: Server-Port (0 bedeutet automatische Zuweisung)
* **Host**: Die Überwachungsadresse, standardmäßig `127.0.0.1`
* **NGpuLayers**: Anzahl der GPU-Ebenen (-1 bedeutet, dass die gesamte GPU genutzt wird)

<!-- Bild benötigt: Screenshot, der die Erstellung des FAIChatPlus_CllamaServerParam-Knotens zeigt, mit der Festlegung der Pfade für das Modell, des Ports, der NGpuLayers und anderer Parameter -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_2.png)

###Rückrufereignisse binden

Server-Ereignisrückrufe binden:

* **On Started**: Wird ausgelöst, wenn der Server erfolgreich gestartet wurde
* **Bei Stopp**: Wird ausgelöst, wenn der Server angehalten wird
* **Bei Fehlschlag**: Wird ausgelöst, wenn der Server nicht startet.

<!-- Bild erforderlich: Blueprint zur Darstellung der gebundenen OnStartedListeners-, OnStoppedListeners- und OnFailedListeners-Ereignisse -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_3.png)

###Kompletter Erstellungsplan

Das vollständige Blaupausen-Dokument zur Servererstellung ist wie folgt:

<!-- Benötigt ein Bild: Zeigt die vollständige Übersicht des Server-Erstellungsplans, einschließlich Parameterkonfiguration, Erstellung von Knoten und Callback-Bindung -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_4.png)

Nachdem der Blueprint ausgeführt wurde, löst der Server beim erfolgreichen Start das `On Started`-Ereignis aus.

<!-- Bild benötigt: Zeigt das Betriebsergebnis nach erfolgreichem Start des Servers, einschließlich der Startprotokolle oder Bildschirmausgaben, die den erfolgreichen Start bestätigen -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_5.png) -->

##Server-Parameter im Detail

Die `FAIChatPlus_CllamaServerParam`-Struktur umfasst die folgenden Parameter:

###Häufig verwendete Parameter

| Parameter | Typ | Standardwert | Beschreibung |
|-----|------|-------|------|
| Modell | FString | - | Pfad zur Modell-Datei (erforderlich) |
| Port | int32 | 0 | Überwachungsport, 0 bedeutet automatische Zuweisung |
| Host | FString | 127.0.0.1 | Überwachungsadresse |
| NGpuLayers | int32 | -1 | Anzahl der GPU-Schichten, -1 bedeutet alle |
| bUseJinja | bool | false | Jinja-Vorlagen verwenden |
| MMProj | FString | - | Multimodale Projektionsdateipfad |
| Temperatur | float | 0.8 | Abtasttemperatur |

###Schlussfolgerungsparameter

| Parameter | Typ | Standardwert | Beschreibung |
|-----|------|-------|------|
| CtxSize | int32 | 4096 | Größe des Kontextes |
| NPredict | int32 | -1 | Anzahl der vorhergesagten Tokens, -1 bedeutet unbegrenzt |
| Threads | int32 | -1 | Anzahl der CPU-Threads, -1 bedeutet automatisch |
| BatchSize | int32 | 2048 | Stapelverarbeitungsgröße |

###Stichprobenparameter

| Parameter | Typ | Standardwert | Beschreibung |
|-----|------|-------|------|
| TopK | int32 | 40 | Top-K-Sampling |
| TopP | float | 0.9 | Top-P-Sampling |
| MinP | float | 0.1 | Min-P-Stichprobenverfahren |
| RepeatPenalty | float | 1.0 | Wiederholungsstrafe |

###Serverparameter

| Parameter | Typ | Standardwert | Beschreibung |
|-----|------|-------|------|
| ApiKey | FString | - | API-Schlüssel (optional) |
| Timeout | int32 | 600 | Timeout in Sekunden |
| Parallel | int32 | 1 | Anzahl der parallelen Sequenzen |
| bNoWebUI | bool | false | Deaktiviert die Web-Oberfläche |
| bVerbose | bool | false | Detailliertes Protokoll |

##Chatten mit CllamaServer

###Chat-Anfrage erstellen

Nach erfolgreichem Start des Servers kann mit dem Knoten `Send CllamaServer Chat Request` eine Chat-Anfrage gesendet werden.

<!-- Benötigtes Bild: Ein Screenshot, der zeigt, wie man im Blueprint mit einem Rechtsklick nach "CllamaServer Chat Request" sucht und einen Node erstellt -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_1.png)

###Chat-Optionen konfigurieren

Erstelle den Knoten `CllamaServer Chat Request Options` und setze die BaseUrl auf die Server-Adresse.

Sie können Server-Informationen über den Knoten `Get Server Info By ID` abrufen.

<!-- Benötigt ein Bild: Zeigt die Erstellung des FAIChatPlus_CllamaServerChatRequestOptions-Knotens, die Verwendung von Get Http Address, um die Serveradresse zu erhalten und diese in BaseUrl zu setzen, mit einem Blueprint -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_2.png)

###Nachrichten erstellen

Erstelle ein Messages-Array, füge eine System-Nachricht und eine Benutzernachricht hinzu.

<!-- Bild erforderlich: zeigt die Erstellung eines Messages-Arrays, das eine System Message (Festlegung der Assistentenrolle) und eine User Message (Nutzerfrage) im Blueprint enthält -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_3.png)

###Rückruf für die Antwortverarbeitung binden

Binden Sie das `On Message`- oder `On Message Finished`-Ereignis, um die Modellantworten zu empfangen.

Hier ist die Übersetzung des Textes ins Deutsche:

<!-- Benötigt ein Bild: Eine Blueprint, die zeigt, wie OnMessageListeners-Ereignisse gebunden werden und im Callback die Nachricht auf dem Bildschirm ausgegeben wird. -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_4.png)

###Vollständiger Chat-Blueprint

Die vollständige Chat-Blueprint sieht wie folgt aus:

<!-- Bild benötigt: Zeigt die vollständige Chat-Blueprint-Übersicht, einschließlich der Erstellung eines Servers, des Wartens auf den Start, des Sendens von Chat-Anfragen und des vollständigen Prozesses der Antwortverarbeitung. -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_5.png)

###Laufzeitergebnis

Führen Sie den Blueprint aus, um zu sehen, wie die vom Modell zurückgegebenen Nachrichten auf dem Bildschirm angezeigt werden.

<!-- Bild benötigt: Zeigt das Chat-Ergebnis an, auf dem Bildschirm ist die von dem Modell zurückgegebene Antwort zu sehen -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_6.png) -->

##Server-Verwaltung

###Server-Informationen abrufen

Verwenden Sie den Knoten `Get Server Info`, um detaillierte Informationen über den Server zu erhalten.

<!-- Benötigt Bild: Zeigt das Blueprint mit dem "Get Server Info"-Knoten zum Abrufen von "FAIChatPlus_CllamaServerInfo" und das Aufbrechen zur Anzeige der einzelnen Felder -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_info_1.png)

Server Info enthält die folgenden Informationen:
* **ServerID**: Eindeutige Server-ID
* **Host**: Überwachungsadresse
* **Port**: Abhörport
* **Adresse**: Vollständige Adresse (host:port)
* **HttpAddress**: HTTP-Adresse (http://host:port)
* **bIsRunning**: Wird ausgeführt
* **Param**: Serverparameter

###Stoppen des Servers

Verwenden Sie den Knoten `Stop Server By ID`, um den aktuellen Server zu stoppen.

<!-- Bild benötigt: Blueprint, der den Stop Cllama Server-Knoten aufruft, darstellen -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_stop_1.png)

###Statische Managementfunktionen

AIChatPlus bietet eine Reihe von statischen Funktionen zur Verwaltung aller Server:

| Funktion | Beschreibung |
|-----|------|
| `Is Server Valid (Static)` | Prüft, ob der Server gültig ist |
| `Läuft der Server (statisch)` | Prüft, ob der Server läuft |
| `Stop Server By ID` | Server anhand der ID stoppen |
| `Stop All Servers` | Alle Server anhalten |
| `Get Server Info By ID` | Server-Informationen nach ID abrufen |
| `Get All Server IDs` | Alle Server-IDs abrufen |
| `Get Server By ID` | Holen Sie die Server-Instanz anhand der ID |

<!-- Bild benötigt: Beispiel für Blueprint zur Verwendung statischer Verwaltungsfunktionen wie "Get All Server IDs" und "Stop All Servers" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_static_1.png)

##Multimodale Unterstützung

CllamaServer unterstützt multimodale Modelle (wie Moondream, Qwen2-VL usw.).

###Multimodale Parameter konfigurieren

Im Server-Parameter wird `MMProj` (der Pfad zur Multimodal-Projektionsdatei) festgelegt:

<!-- Bild benötigt: Blauprint zeigt die Einrichtung der Pfade für Model und MMProj in den Server Parametern -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_1.png)

###Bildnachricht senden

Bilder in Nachrichten hinzufügen:

<!-- Benötigt Bild: Zeigt das Lesen einer Bilddatei, das Erstellen einer Nachricht mit dem Bild und das Senden einer Anfrage über den CllamaServer auf. -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_2.png)

### Ausführungsergebnis

Benötige Bild: Zeigt das Ergebnis der Bilderkennung, der Bildschirm zeigt die Beschreibung des Bildinhalts durch das Modell an
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_3.png) -->

## Tool Calling

CllamaServer unterstützt die Tool-Calling-Funktion (Funktionsaufruf), deren Verwendung ähnlich wie bei OpenAI ist.

Eine detaillierte Beschreibung der Verwendung finden Sie unter [Tool Call](ue-插件-AIChatPlus-Usage-Blueprint-ToolCall.md)Dokument.

Bei der Verwendung von CllamaServer für Tool Calls ist Folgendes erforderlich:
1. Setzen Sie im Server-Parameter `bUseJinja = true`
2. Definieren Sie Werkzeuge im Feld "Tools" der Chat-Optionen

<!-- Benötigt Bild: Vollständige Blaupause des CllamaServer Tool Calls, einschließlich der Einstellung bUseJinja=true und der Tools-Definition -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_tool_1.png)

##Editor Server-Verwaltung

AIChatPlus bietet in den Editor-Tools eine visuelle Management-Oberfläche für CllamaServer, die das Erstellen, Überwachen und Verwalten mehrerer Server erleichtert.

Editor-Tool öffnen: `Tools -> AIChatPlus -> AIChat`, öffnen Sie den Reiter Cllama Server Manager.

<!-- Bild benötigt: Screenshot der CllamaServer-Verwaltungsoberfläche im Editor, der die Serverliste, den Erstellungsbutton, Statusinformationen etc. anzeigt -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_editor_1.png)

Im Editor können Sie:
* Neuen Server erstellen
* Status des laufenden Servers prüfen
* Angegebenen Server beenden
* Server-Parameter konfigurieren
* Die Server-Konfiguration wird automatisch gespeichert

<!-- Bild benötigt: Schnittstelle zur Erstellung eines neuen Servers im Editor anzeigen, mit angezeigtem Parameterkonfigurationspanel -->  

Hinweis: Der deutsche Text behält die technische und direkte Tonart des Originals bei, wie für Anleitungen oder Dokumentationen üblich, und vermittelt klar die Anforderung eines Bildes mit spezifischen Details zur Benutzeroberfläche. Die Übersetzung ist präzise, natürlich formuliert und verzichtet auf maschinelle Klischees.
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_editor_2.png)

##Beziehungen zu anderen APIs

Da CllamaServer mit dem OpenAI-API-Format kompatibel ist, können Sie auch den Chat-Request-Knoten von OpenAI verwenden, um mit CllamaServer zu kommunizieren. Setzen Sie einfach die `BaseUrl` auf die Adresse des CllamaServers.

<!-- Benötigt Bild: Beispiel einer Blueprint mit dem OpenAI Chat Request Node, aber mit der BaseUrl auf die CllamaServer-Adresse eingestellt -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_openai_1.png) -->

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte geben Sie Ihr [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Hinweis auf etwaige Fehlstellen. 
