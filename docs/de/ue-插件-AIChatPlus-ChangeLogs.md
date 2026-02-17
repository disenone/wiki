---
layout: post
title: Versionsverlauf
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
description: Änderungsprotokoll
---

<meta property="og:title" content="UE 插件 AIChatPlus 版本日志" />

#UE-Plugin AIChatPlus Versionshistorie

## v2.0.0 - 2026.02.14

* **Tool Calling Mehrplattform-Unterstützung**: Zusätzliche Tool-Aufruf-/Funktionsaufruf-Funktionen für fünf große Plattformen: OpenAI, Claude, Gemini, Ollama und CllamaServer.
* **Cllama Server Integration**: Vollständige Unterstützung für den lokalen llama.cpp Server, einschließlich Erstellung, Verwaltung, Sprach-zu-Text und bietet eine visuelle Verwaltungsoberfläche im Editor.
* **JSON Blueprint-Bibliothek**: Neue Blueprint-Operationen für JsonObject/JsonArray hinzugefügt, unterstützen die Umwandlung zwischen JSON und USTRUCT.
* **OpenAI Audio**: Unterstützt die Audio-Ein- und Ausgabe von OpenAI, der Editor ermöglicht eine Vorschau der Audioantworten

## v1.8.0 - 2025.11.03

* Upgrade llama.cpp b6792

## v1.7.0 - 2025.07.06

* Upgrade auf llama.cpp b5536

* Unterstützt UE5.6

* Android-Version stürzt beim Shipping ab, deaktiviere llama.cpp

## v1.6.2 - 2025.03.17

###Neue Funktionen

* Cllama fügt den KeepContext-Parameter hinzu, standardmäßig false; Context wird nach Beendigung des Chats automatisch zerstört

* Cllama fügt den Parameter KeepAlive hinzu, wodurch das wiederholte Laden des Modells reduziert werden kann.

## v1.6.1 - 2025.03.07

### Bug Fix

* OpenAI Image Chat Blaupause unterstützt die Eingabe von Bildern

* Editor Tool Cllama mmproj Modell erlaubt Leerwerte

## v1.6.0 - 2025.03.02

###Neue Funktion

* llama.cpp auf Version b4604 aktualisiert

* Cllama unterstützt GPU-Backends: cuda und metal

* Chat-Tool Cllama unterstützt die Nutzung von GPU

* Unterstützt das Lesen von Modell-Dateien in gepackten Pak-Dateien

### Bug Fix

* Behebung des Problems, dass Cllama beim Schlussfolgern abstürzt, wenn reload durchgeführt wird

* Behebung von Fehlern beim iOS-Kompilierungsvorgang

## v1.5.1 - 2025.01.30

###Neue Funktionen

* Nur Gemini darf Audiodateien senden

* Optimierung der Methode zum Abrufen von PCMData, Dekomprimierung der Audiodaten erst bei der Erzeugung von B64

* Anfrage: Zwei zusätzliche Rückrufe hinzufügen - OnMessageFinished und OnImagesFinished

* Optimierung der Gemini-Methode, automatisches Abrufen der Methode basierend auf bStream

* Füge einige Blueprint-Funktionen hinzu, um die Konvertierung von Wrapper- in tatsächliche Typen zu erleichtern sowie Response Message und Error zu erhalten.

### Bug Fix

* Problem der wiederholten Aufrufe von Request Finish behoben

## v1.5.0 - 2025.01.29

###Neue Funktionen

* Unterstützung für das Senden von Audio an Gemini

* Der Editor unterstützt das Senden von Audiodateien und Sprachaufnahmen

### Bug Fix

* Fehler behoben, bei dem das Kopieren der Sitzung fehlschlug

## v1.4.1 - 2025.01.04

###Problembehebung

* Chat-Tools unterstützen das Senden von nur Bildern ohne Nachricht

* Behobenes Problem mit fehlgeschlagenen Bildern beim Senden über die OpenAI-Schnittstelle

* Korrektur des Problems mit fehlenden Parametern Quality, Style und ApiVersion in den Einstellungen der OpenAI- und Azure-Chat-Tools =

## v1.4.0 - 2024.12.30

###Neue Funktionen

* (Experimentelle Funktion) Cllama(llama.cpp) unterstützt multimodale Modelle und kann Bilder verarbeiten

* Alle Parameter für Blaupausentypen wurden mit detaillierten Hinweisen versehen

## v1.3.4 - 2024.12.05

###Neue Funktionen

* OpenAI unterstützt die Vision-API

###Problembehebung

* Fehler bei OpenAI stream=false behoben

## v1.3.3 - 2024.11.25

###Neue Funktionen

* Unterstützt UE-5.5

###Problembehebung

* Behebung des Problems, dass einige Blaupausen nicht wirksam waren

## v1.3.2 - 2024.10.10

###Problembehebung

* Behebung Absturz von cllama bei manueller Unterbrechung des Requests

* Behebung des Problems, dass beim Packen der Win-Version für den Store-Download die Dateien ggml.dll und llama.dll nicht gefunden werden

* Überprüfen Sie während der Erstellung der Anfrage, ob Sie sich im GameThread befinden, CreateRequest-Prüfung im Spielthread

## v1.3.1 - 2024.9.30

###Neue Funktionen

* Ein SystemTemplateViewer wurde hinzugefügt, der das Anzeigen und Nutzen von Hunderten von Systemeinstellungsvorlagen ermöglicht.

###Problembehebung

* Fehlerbehebung beim Herunterladen von Plugins aus dem Shop, bei dem llama.cpp die verknüpften Bibliotheken nicht finden konnte

* Problem mit zu langem Pfad für LLAMACpp behoben

* Behobener Fehler mit der Verknüpfung llama.dll nach der Windows-Paketierung

* Behebung des Problems beim Lesen von Dateipfaden auf iOS/Android

* Behebung des Fehlers bei der Namenseinstellung von Cllame

## v1.3.0 - 2024.9.23

###Wichtige neue Funktionen

* Integriert llama.cpp und unterstützt die lokale Offline-Ausführung großer Modelle

## v1.2.0 - 2024.08.20

###Neue Funktionen

* Unterstützt OpenAI Bildbearbeitung/Bildvariation

* Unterstützung für die Ollama API, einschließlich automatischer Abruf der von Ollama unterstützten Modellliste

## v1.1.0 - 2024.08.07

###Neue Funktionen

* Unterstützung für Blaupausen

## v1.0.0 - 2024.08.05

###Neue Funktionen

* Grundlegende Vollfunktionalität

* Unterstützt OpenAI, Azure, Claude, Gemini

* Integrierter Chat-Tool mit funktionsreichem Editor

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte teilen Sie uns Ihr [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Hinweise auf etwaige Auslassungen. 
