---
layout: post
title: Versionsprotokoll
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
description: Versionsprotokoll
---

<meta property="og:title" content="UE 插件 AIChatPlus 版本日志" />

#UE 插件 AIChatPlus 版本日志

Translated to German:

UE Plugin AIChatPlus Versionsprotokoll

## v1.6.1 - 2025.03.07

### Bug Fix

OpenAI Image Chat Blueprint unterstützt die Eingabe von Bildern.

Editor-Tool Cllama mmproj model allows vacuum

## v1.6.0 - 2025.03.02

###Neue Funktion

llama.cpp upgraded to version b4604

Cllama unterstützt GPU-Backends: cuda und metal.

Das Chat-Tool Cllama unterstützt die Verwendung von GPU.

Unterstützung zum Lesen von Modelldateien aus dem gepackten Pak。

### Bug Fix

Repariere das Problem mit dem Absturz von Cllama während des Nachladens in der Deduktion.

Fix iOS compilation errors.

## v1.5.1 - 2025.01.30

###Neue Funktion

Erlauben Sie nur Gemini, Audio abzuspielen.

Optimiere die Methode zum Abrufen von PCM-Daten, um die Audiodaten erst beim Generieren von B64 zu dekomprimieren.

Bitte füge zwei Callbacks OnMessageFinished und OnImagesFinished hinzu.

Optimiere die Gemini-Methode, um automatisch die Methode basierend auf bStream zu erhalten.

Fügen Sie einige Blueprint-Funktionen hinzu, um das Wrapper in tatsächliche Typen zu konvertieren und Response-Meldungen und Fehler abzurufen.

### Bug Fix

Beheben des Problems mit mehrfachem Aufruf von Request Finish.

## v1.5.0 - 2025.01.29

###Neue Funktion

Unterstützung für Audio-Ausgabe an Gemini geben.

Die Editor-Tool-Unterstützung für den Versand von Audio und Aufnahmen.

### Bug Fix

Behebung des Fehlers beim Kopieren der Sitzung.

## v1.4.1 - 2025.01.04

###Problembehebung

Die Chat-Plattform ermöglicht das Versenden von Bildern ohne Text.

Repariere den Fehler bei der Übermittlung von Bildern über die OpenAI-Schnittstelle.

Behebe das Problem mit den fehlenden Parametern Quality, Style und ApiVersion in den Einstellungen von OpanAI und Azure-Chat-Tools.

## v1.4.0 - 2024.12.30

###Neue Funktion

* (Experimental feature) Cllama (llama.cpp) supports multimodal models and can handle images.

Alle Blaupausen-Typenparameter wurden mit detaillierten Hinweisen versehen.

## v1.3.4 - 2024.12.05

###Neue Funktion

OpenAI unterstützt Vision-API.

###Problembehebung

Fix the error when OpenAI stream=false.

## v1.3.3 - 2024.11.25

###Neue Funktion

Unterstützung für UE-5.5

###Problembehebung

Behebung des Problems mit nicht funktionierenden Teilen des Bauplans.

## v1.3.2 - 2024.10.10

###Problembehebung

Behebung des Absturzes von cllama beim manuellen Stoppen des Requests.

Behebung des Problems beim Laden der win-Paketversion im Store, bei dem die Dateien ggml.dll und llama.dll nicht gefunden werden konnten.

Prüfe beim Erstellen der Anfrage, ob sich der Vorgang im GameThread befindet.

## v1.3.1 - 2024.9.30

###Neue Funktion

Füge einen SystemTemplateViewer hinzu, um Hunderte von Systemeinstellungsvorlagen anzeigen und verwenden zu können.

###Fehlerbehebung

Beheben Sie das Problem mit dem heruntergeladenen Plugin aus dem Shop, llama.cpp kann die Verknüpfungsbibliothek nicht finden.

Behebung des Problems mit der zu langen Pfadlänge in LLAMACpp.

Beheben Sie den Fehler mit dem Link llama.dll nach dem Kompilieren von Windows.

Fixing issues with reading file paths on iOS/Android.

Bitte reparieren Sie den Fehler beim Einstellen des Namens in Cllame.

## v1.3.0 - 2024.9.23

###Bitte geben Sie mehr Kontext für diese Textübersetzung.

Integriert llama.cpp zur Unterstützung der lokalen Offline-Ausführung großer Modelle.

## v1.2.0 - 2024.08.20

###Neue Funktion

Unterstützung für OpenAI Image Edit/Image Variation

Unterstützung der Ollama-API, Unterstützung für die automatische Abrufung der Liste der von Ollama unterstützten Modelle.

## v1.1.0 - 2024.08.07

###Neue Funktion

Unterstütze die Blaupause.

## v1.0.0 - 2024.08.05

###Neue Funktion

Grundlegende vollständige Funktion.

Unterstützung für OpenAI, Azure, Claude, Gemini.

Mit integriertem, umfassendem Editor-Chat-Tool.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte gib dein [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Identify any omissions. 
