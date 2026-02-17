---
layout: post
title: API Reference
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
description: API Reference
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - API Reference" />

#C++ Kapitel - API-Referenz

Dieses Dokument bietet eine Referenz zur C++ API des AIChatPlus-Plugins, einschließlich Beschreibungen aller öffentlichen Klassen, Strukturen, Enumerationen und wichtiger Methoden.

##Inhaltsverzeichnis

- [Aufzählungstyp](##枚举类型)
- [Kernbasisklassen](##核心基类)
- [Handler-Klasse](##handler-类)
- [Request-Klasse](##request-类)
- [Werkzeugkategorie](##工具类)
- [JSON-Klasse](##json-类)

---

##Aufzählungstyp

### EAIChatPlus_ChatApiProvider

Aufzählung von Anbietern für Chat-API mit KI.

```cpp
enum class EAIChatPlus_ChatApiProvider : uint8
{
    OpenAI,         // OpenAI API
    Azure,          // Azure OpenAI API
    Claude,         // Anthropic Claude API
    Gemini,         // Google Gemini API
Ollama,         // Ollama lokaler Dienst
Cllama,         // Direktaufruf von llama.cpp (veraltet)
CllamaServer    // llama.cpp Servermodus
};
```

### EAIChatPlus_ImageApiProvider

Anbieterliste für Bildgenerierung APIs.

```cpp
enum class EAIChatPlus_ImageApiProvider : uint8
{
    OpenAI,   // OpenAI DALL-E
    Azure     // Azure OpenAI DALL-E
};
```

### EAIChatPlus_ChatRole

Nachrichtenrollen-Enumeration.

```cpp
enum class EAIChatPlus_ChatRole : uint8
{
System,     // Systemanweisungen (altes Modell)
Benutzer,       // Benutzernachricht
Assistent,  // KI-Antwort
Entwickler,  // Entwickleranweisung (o1+ Modell)
Werkzeug        // Werkzeugaufrufergebnis
};
```

### EAIChatPlus_ImageChatType

Bildbearbeitungstyp-Enumeration.

```cpp
enum class EAIChatPlus_ImageChatType : uint8
{
Generation,  // Bildgenerierung
Bearbeiten,       // Bildbearbeitung
    Variation    // Bildvariante
};
```

### EAIChatPlus_JsonValueType

JSON Werttypen-Enumeration.

```cpp
enum class EAIChatPlus_JsonValueType : uint8
{
Keine,     // Ungültig
Null,     // Nullwert
String,   // Zeichenkette
Zahl,   // Zahl
Boolean,  // Boolesch
Array,    // Feld
Objekt    // 对象
};
```

---

##Kernbasisklasse

### UAIChatPlus_RequestBase

Die Basisklasse für alle Anfragen (abstrakte Klasse).

**Schlüsselmethoden:**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `SendRequest()` | `bool` | Anfrage senden |
| `StopRequest()` | `void` | Anfrage stoppen |
| `Activate()` | `void` | Aktiviert das Anfrageobjekt |
| `IsActivated()` | `bool` | Überprüft, ob aktiviert wurde |
| `SetIsAutoDestroy(bool)` | `void` | Automatische Zerstörung nach Abschluss der Einstellung |

**Auftrag:**

| Auftragsname | Unterschrift | Beschreibung |
|--------|------|------|
| `OnStartedListeners` | `void()` | Anfrage gestartet |
| `OnMessageListeners` | `void(const FString&)` | Streaming-Nachricht empfangen |
| `OnFinishedListeners` | `void(const FAIChatPlus_PointerWrapper&)` | Anfrage abgeschlossen |
| `OnFailedListeners` | `void(const FAIChatPlus_PointerWrapper&)` | Anfrage fehlgeschlagen |

---

### UAIChatPlus_ChatRequestBase

Chat-Anfrage-Basisklasse, erbt von `UAIChatPlus_RequestBase`.

**Statische Fabrikmethode:**

```cpp
// Anfrage nach Anbieter erstellen
static UAIChatPlus_ChatRequestBase* CreateByApi(EAIChatPlus_ChatApiProvider InApiProvider);
static UAIChatPlus_ChatRequestBase* CreateByApiInWorld(EAIChatPlus_ChatApiProvider InApiProvider, const UObject* InWorldContext);
```

**Schlüsselmethode:**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `SetMessages(const TArray<FAIChatPlus_ChatRequestMessage>&)` | `void` | Legt die Nachrichtenliste fest |
| `GetFullUrl()` | `FString` | Ermittelt die vollständige Anfrage-URL |
| `GetModelText()` | `FString` | Ruft den Modellnamen ab |
| `GetTokenUsageText()` | `FString` | Gibt die Beschreibung der Token-Nutzung zurück |
| `GetApiProvider()` | `EAIChatPlus_ChatApiProvider` | Ermittelt den API Provider Typ |

---

### UAIChatPlus_ImageRequestBase

Bildanforderungsbasisklasse, erbt von `UAIChatPlus_RequestBase`.

**Statische Fabrikmethode:**

```cpp
static UAIChatPlus_ImageRequestBase* CreateByApi(EAIChatPlus_ImageApiProvider InApiProvider);
static UAIChatPlus_ImageRequestBase* CreateByApiInWorld(EAIChatPlus_ImageApiProvider InApiProvider, const UObject* InWorldContext);
```

**Wichtige Methoden:**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `SetPrompt(const FString&)` | `void` | Legt das Bildgenerierungs-Prompt fest |
| `SetImages(const TArray<UAIChatPlus_Texture*>&)` | `void` | Eingabebilder festlegen (Bearbeiten/Variation) |
| `GetModelText()` | `FString` | Ruft den Modellnamen ab |
| `GetStyleText()` | `FString` | Ruft den Stilnamen ab |
| `GetRevisedPrompt()` | `FString` | Ruft den überarbeiteten Aufforderungstext ab |
| `GetImageChatType()` | `FString` | Ruft den Typ der Bildoperation ab |

---

### UAIChatPlus_ModelRequestBase

Modellisten-Anfrage-Basisklasse, erbt von `UAIChatPlus_RequestBase`.

**Statische Fabrikmethode:**

```cpp
static UAIChatPlus_ModelRequestBase* CreateByApi(EAIChatPlus_ChatApiProvider InApiProvider);
static UAIChatPlus_ModelRequestBase* CreateByApiInWorld(EAIChatPlus_ChatApiProvider InApiProvider, const UObject* InWorldContext);
```

---

##Handler-Klasse

### UAIChatPlus_HandlerBase

Die Basisklasse aller Handler.

**Schlüsselmethode:**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `SetIsAutoDestroy(bool)` | `void` | Legt die automatische Zerstörung fest |
| `AutoDestroy()` | `void` | Führt die automatische Zerstörung aus |
| `Destroy()` | `void` | Sofort zerstören |

---

### UAIChatPlus_ChatHandlerBase

Chat-Anfragen-Handler, erbt von `UAIChatPlus_HandlerBase`.

**Statische Fabrikmethode:**

```cpp
static UAIChatPlus_ChatHandlerBase* New();
```

**Bindungsmethode:**

| Methode | Beschreibung |
|------|------|
| `BindChatRequest(UAIChatPlus_ChatRequestBase*)` | Chat-Anfrage binden |
| `BindImageRequest(UAIChatPlus_ImageRequestBase*)` | Bildanfrage binden |
| `BindModelRequest(UAIChatPlus_ModelRequestBase*)` | Modellanfrage binden |
| `ClearDelegates()` | Löscht alle Delegate-Bindungen |

**Auftrag:**

| Auftragsname | Unterschrift | Beschreibung |
|--------|------|------|
| `OnStarted` | `void()` | Anfrage gestartet |
| `OnStopped` | `void()` | Anforderung zum Stoppen |
| `OnMessage` | `void(const FString&)` | Stream-Nachrichten |
| `OnMessageFinished` | `void(const FAIChatPlus_MessageFinishedPayload&)` | Nachricht abgeschlossen |
| `OnUpdated` | `void(const FAIChatPlus_PointerWrapper&)` | Aktualisierungsanfrage |
| `OnFinished` | `void(const FAIChatPlus_PointerWrapper&)` | Anfrage abgeschlossen |
| `OnFailed` | `void(const FAIChatPlus_PointerWrapper&)` | Anfrage fehlgeschlagen |
| `OnImages` | `void(const TArray<UTexture2D*>&, bool)` | Bilderzeugung |
| `OnModels` | `void(const TArray<FString>&)` | Modellliste |

---

### UAIChatPlus_CllamaServerHandler

CllamaServer-spezifischer Handler.

**Statische Fabrikmethode:**

```cpp
static UAIChatPlus_CllamaServerHandler* CreateHandler();
```

**Auftrag:**

| Beauftragungsname | Unterschrift | Beschreibung |
|--------|------|------|
| `OnServerStarted` | `void(FGuid)` | Server startet |
| `OnServerStopped` | `void(FGuid)` | Server gestoppt |
| `OnServerFailed` | `void(FGuid, const FString&)` | Server fehlgeschlagen |

---

##Request-Klasse

Alle Request-Klassen von Providern folgen demselben Factory-Method-Pattern:

###Allgemeines Fabrikmethodenmuster

```cpp
// Nehmen wir OpenAI als Beispiel, andere Provider sind ähnlich.
static UAIChatPlus_OpenAIChatRequest* Create();
static UAIChatPlus_OpenAIChatRequest* CreateWithOptions(const FAIChatPlus_OpenAIChatRequestOptions& InOptions);
static UAIChatPlus_OpenAIChatRequest* CreateWithOptionsAndMessages(
    const FAIChatPlus_OpenAIChatRequestOptions& InOptions,
    const TArray<FAIChatPlus_ChatRequestMessage>& InMessages);
static UAIChatPlus_OpenAIChatRequest* CreateInWorld(const UObject* InWorldContext);
static UAIChatPlus_OpenAIChatRequest* CreateInWorldWithOptions(
    const UObject* InWorldContext,
    const FAIChatPlus_OpenAIChatRequestOptions& InOptions);
static UAIChatPlus_OpenAIChatRequest* CreateInWorldWithOptionsAndMessages(
    const UObject* InWorldContext,
    const FAIChatPlus_OpenAIChatRequestOptions& InOptions,
    const TArray<FAIChatPlus_ChatRequestMessage>& InMessages);
```

###Allgemeine statische Methoden

Alle Request-Klassen bieten die Methode `CastWrapperToResponse` für Typumwandlungen an:

```cpp
// Antwortdaten aus PointerWrapper extrahieren
static FAIChatPlus_XXXResponseBody& CastWrapperToResponse(const FAIChatPlus_PointerWrapper& InWrapper);
static FAIChatPlus_PointerWrapper CastResponseToWrapper(const FAIChatPlus_XXXResponseBody& InResponse);
```

---

### UAIChatPlus_OpenAIChatRequest

OpenAI-Chatanfrage.

**Header-Datei:** `Common_OpenAI/AIChatPlus_OpenAIChatRequest.h`

**Typ der Optionen:** `FAIChatPlus_OpenAIChatRequestOptions`

**Antworttyp:** `FAIChatPlus_OpenAIChatResponseBody`

---

### UAIChatPlus_AzureChatRequest

Azure OpenAI Chat-Anfrage.

**Header-Datei:** `Common_Azure/AIChatPlus_AzureChatRequest.h`

**Options-Typ:** `FAIChatPlus_AzureChatRequestOptions`

**Antworttyp:** `FAIChatPlus_AzureChatResponseBody`

---

### UAIChatPlus_ClaudeChatRequest

Claude Chat-Anfrage.

**Header-Datei:** `Common_Claude/AIChatPlus_ClaudeChatRequest.h`

**Options Typ:** `FAIChatPlus_ClaudeChatRequestOptions`

**Antworttyp:** `FAIChatPlus_ClaudeChatResponseBody`

---

### UAIChatPlus_GeminiChatRequest

Gemini-Chat-Anfrage.

**Header-Datei:** `Common_Gemini/AIChatPlus_GeminiChatRequest.h`

**Options-Typ:** `FAIChatPlus_GeminiChatRequestOptions`

**Antworttyp:** `FAIChatPlus_GeminiChatResponseBody`

---

### UAIChatPlus_OllamaChatRequest

Ollama Chat-Anfrage.

**Header-Datei:** `Common_Ollama/AIChatPlus_OllamaChatRequest.h`

**Optionen Typ:** `FAIChatPlus_OllamaChatRequestOptions`

**Antworttyp:** `FAIChatPlus_OllamaChatResponseBody`

---

### UAIChatPlus_OllamaModelRequest

Anfrage der Ollama Modellliste.

**Header-Datei:** `Common_Ollama/AIChatPlus_OllamaModelRequest.h`

**Optionen Typ:** `FAIChatPlus_OllamaModelRequestOptions`

**Antworttyp:** `FAIChatPlus_OllamaModelResponseBody`

**Spezifische Methoden:**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `GetModelNames()` | `TArray<FString>` | Gibt eine Liste von Modellnamen zurück |

---

###UAIChatPlus_CllamaChatRequest (veraltet)

Cllama Offline-Chat-Anfrage (veraltet, empfohlen wird die Verwendung von CllamaServer).

**Header-Datei:** `Common_Cllama/AIChatPlus_CllamaChatRequest.h`

**Options Typ:** `FAIChatPlus_CllamaChatRequestOptions`

**Antworttyp:** `FAIChatPlus_CllamaChatResponseBody`

---

### UAIChatPlus_CllamaServerChatRequest

CllamaServer Chat-Anfrage.

**Header-Datei:** `Common_CllamaServer/AIChatPlus_CllamaServerChatRequest.h`

**Optionstyp:** `FAIChatPlus_CllamaServerChatRequestOptions`

**Antworttyp:** `FAIChatPlus_CllamaServerChatResponseBody`

---

### UAIChatPlus_OpenAIImageRequest

OpenAI Bildgenerierungsanfrage.

**Header-Datei:** `Common_OpenAI/AIChatPlus_OpenAIImageRequest.h`

**Options-Typ:** `FAIChatPlus_OpenAIImageRequestOptions`

**Antworttyp:** `FAIChatPlus_OpenAIImageResponseBody`

---

### UAIChatPlus_AzureImageRequest

Azure Bildgenerierungsanfrage.

**Header-Datei:** `Common_Azure/AIChatPlus_AzureImageRequest.h`

**Options-Typ:** `FAIChatPlus_AzureImageRequestOptions`

**Antworttyp:** `FAIChatPlus_AzureImageResponseBody`

---

### UAIChatPlus_CllamaServer

CllamaServer Server-Verwaltungsklasse.

**Header-Datei:** `Common_CllamaServer/AIChatPlus_CllamaServer.h`

**Statische Fabrikmethode:**

```cpp
static UAIChatPlus_CllamaServer* CreateServer(
    const FAIChatPlus_CllamaServerParam& InParams,
    FGuid InServerID = FGuid());
static UAIChatPlus_CllamaServer* CreateServerInWorld(
    const UObject* InWorldContext,
    const FAIChatPlus_CllamaServerParam& InParams,
    FGuid InServerID = FGuid());
static UAIChatPlus_CllamaServer* CreateServerWithHandler(
    const FAIChatPlus_CllamaServerParam& InParams,
    UAIChatPlus_CllamaServerHandler* InHandler,
    FGuid InServerID = FGuid());
```

**Instanzmethoden:**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `Activate()` | `void` | Startet den Server |
| `StopServer()` | `void` | Server stoppen |
| `IsRunning()` | `bool` | Überprüft, ob etwas ausgeführt wird |
| `GetServerID()` | `FGuid` | Ermittelt die Server-ID |
| `GetHost()` | `FString` | Ruft die Host-Adresse ab |
| `GetAddress()` | `FString` | Ermittelt die vollständige Adresse |
| `GetServerInfo(FAIChatPlus_CllamaServerInfo&)` | `bool` | Ruft Serverinformationen ab |

**Statische Verwaltungsmethoden:**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `IsServerValid(const FGuid&)` | `bool` | Überprüft, ob der Server gültig ist |
| `IsServerRunning(const FGuid&)` | `bool` | Überprüft, ob der Server läuft |
| `StopServerByID(const FGuid&)` | `void` | Stoppt den Server anhand der ID |
| `StopAllServers()` | `void` | Stoppt alle Server |
| `GetServerByID(const FGuid&)` | `UAIChatPlus_CllamaServer*` | Server nach ID abrufen |
| `GetAllServerIDs()` | `TArray<FGuid>` | Ermittelt alle Server-IDs |

---

##Hilfsklasse

### UAIChatPlus_Util

Allgemeine Hilfsklasse, bietet verschiedene statische Hilfsmethoden.

**Header-Datei:** `Common/AIChatPlus_Util.h`

####Logbuchbezogene Themen

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `SetInternalLogVerbosity(EAIChatPlus_LogVerbosityType)` | `void` | Legt den internen Log-Level fest |

####Wrapper-Konvertierung

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `CastWrapperToError(const FAIChatPlus_PointerWrapper&)` | `FAIChatPlus_ResponseErrorBase&` | Fehlerinformationen extrahieren |
| `CastWrapperToResponse(const FAIChatPlus_PointerWrapper&)` | `FAIChatPlus_ChatResponseBodyBase&` | Extrahiert die Antwortdaten |
| `GetErrorWrapperDescription(const FAIChatPlus_PointerWrapper&)` | `FString` | Ruft die Fehlerbeschreibung ab |
| `GetResponseWrapperMessage(const FAIChatPlus_PointerWrapper&)` | `FString` | Holen Sie sich die Antwortnachricht |

####Bildwerkzeuge

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `LoadImage(const FString&, bool)` | `UTexture2D*` | Lädt ein Bild aus einer Datei |
| `SaveImage(UTexture2D*, const FString&)` | `bool` | Speichert ein Bild in einer Datei |
| `ImageToB64(UTexture2D*, int32)` | `FString` | Bild zu Base64 konvertieren |
| `CopyTexture2D(UTexture2D*, UObject*, FName, EObjectFlags)` | `UTexture2D*` | Textur kopieren |
| `FitImageSize(const FVector2D&, const FVector2D&)` | `FVector2D` | Berechnet die angepasste Größe |
| `CopyTexture2DToClipboard(UTexture2D*)` | `void` | In die Zwischenablage kopieren |
| `IsCanCopyTexture2DToClipboard()` | `bool` | Überprüft, ob die Funktion unterstützt wird |

####Audiowerkzeuge

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `LoadSoundWav(const FString&)` | `USoundWave*` | Lädt eine Audiodatei aus einer Datei |
| `SaveSoundWav(USoundWave*, const FString&)` | `bool` | Speichert die Audiodatei in einer Datei |
| `SoundToB64(USoundWave*)` | `FString` | Audio in Base64 umwandeln |
| `CopySoundWave(const USoundWave*, UObject*, FName)` | `USoundWave*` | Klangwelle kopieren |
| `WavDataToSoundWave(const TArray<uint8>&, bool, bool)` | `USoundWave*` | Konvertierung von WAV-Daten in einen Soundwave |
| `GetSoundWavePCMData(USoundWave*)` | `TArray<uint8>` | Holt die PCM-Daten |

####JSON Werkzeuge

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `MergeJsonObjects(const FString&, const FString&)` | `FString` | JSON-Strings zusammenführen |
| `LoadJsonString(const FString&)` | `TSharedPtr<FJsonObject>` | JSON-Zeichenkette analysieren |
| `ToJsonString(const TSharedPtr<FJsonObject>&)` | `FString` | In JSON-Zeichenkette umwandeln |

####Cllama-Werkzeug

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `Cllama_IsValid()` | `bool` | Überprüft, ob Cllama verfügbar ist |
| `Cllama_IsSupportGpu()` | `bool` | Überprüft, ob GPU unterstützt wird |
| `Cllama_GetSupportBackends()` | `TArray<FString>` | Ruft die unterstützten Backends ab |
| `Cllama_PrepareModelPathFromPak(const FString&)` | `FString` | Bereitet den Modellpfad aus dem Pak vor |

####Modellinformationen

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `GetOpenAIChatDefaultModels()` | `const TArray<FName>&` | Liste der standardmäßigen OpenAI-Modelle |
| `GetOpenAIChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | OpenAI-Modellinformationen abrufen |
| `GetClaudeChatDefaultModels()` | `const TArray<FName>&` | Standardmodellliste von Claude |
| `GetClaudeChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | Ermittelt Claude-Modellinformationen |
| `GetGeminiChatDefaultModels()` | `const TArray<FName>&` | Liste der Standardmodelle für Gemini-Chat |
| `GetGeminiChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | Informationen zum Gemini-Modell abrufen |

---

### UAIChatPlus_Texture

Bildverpackungsklasse, unterstützt asynchrones Laden und Base64-Umwandlung.

**Header-Datei:** `Common/AIChatPlus_Texture.h`

**Statische Fabrikmethode:**

```cpp
static UAIChatPlus_Texture* New(UTexture2D* InTexture = nullptr, const FString& InSourcePath = "");
static UAIChatPlus_Texture* CreateInBlueprint(UObject* WorldContextObject, UTexture2D* InTexture);
```

**Methode:**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `LoadFromFile(const FString&)` | `bool` | Aus Datei laden (synchron) |
| `LoadFromFileAsync(const FString&, Callback)` | `FLoadingTaskType*` | Laden aus Datei (asynchron) |
| `LoadFromAsset(UObject*, const FString&)` | `bool` | Lädt aus einer Asset-Datei (synchron) |
| `LoadFromAssetAsync(UObject*, Callback, const FString&)` | `FLoadingTaskType*` | Aus Asset laden (asynchron) |
| `ToB64()` | `const FString&` | Konvertiert zu Base64 (synchron) |
| `ToB64Async(Callback)` | `FLoadingTaskType*` | In Base64 konvertieren (asynchron) |
| `GetBrush(bool)` | `const FSlateBrush*` | Holt den Slate-Pinsel |
| `GetBrushCopy(bool)` | `FSlateBrush` | Ruft eine Kopie des Pinsels ab |
| `GetSize()` | `FIntVector2` | Größe abrufen |
| `GetSize2D()` | `FVector2D` | Ermittle die Größe (Floating-Point) |
| `IsValid()` | `bool` | Überprüft, ob gültig |
| `IsLoading()` | `bool` | Prüft, ob ein Laden stattfindet |
| `Reset()` | `void` | Zurücksetzen |
| `WaitLoadingComplete()` | `void` | Wartet auf den Abschluss des Ladevorgangs |

---

### UAIChatPlus_Sound

Audio-Wrapper-Klasse, unterstützt asynchrones Laden und Base64-Konvertierung.

**Header-Datei:** `Common/AIChatPlus_Sound.h`

**Statische Fabrikmethode:**

```cpp
static UAIChatPlus_Sound* New(USoundWave* InSound = nullptr, const FString& InSourcePath = "");
static UAIChatPlus_Sound* CreateInBlueprint(UObject* WorldContextObject, USoundWave* InSound);
```

**Methode:**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `LoadFromFile(const FString&)` | `bool` | Lädt aus einer Datei (synchron) |
| `LoadFromFileAsync(const FString&, Callback)` | `FLoadingTaskType*` | Aus Datei laden (asynchron) |
| `LoadFromAsset(UObject*, const FString&)` | `bool` | Lädt aus einer Asset-Datei (synchron) |
| `LoadFromAssetAsync(UObject*, Callback, const FString&)` | `FLoadingTaskType*` | Laden aus Asset (asynchron) |
| `ToB64()` | `const FString&` | In Base64 konvertieren (synchron) |
| `ToB64Async(Callback)` | `FLoadingTaskType*` | Zu Base64 konvertieren (asynchron) |
| `IsValid()` | `bool` | Überprüft, ob gültig |
| `IsLoading()` | `bool` | Überprüft, ob geladen wird |
| `Reset()` | `void` | Zurücksetzen |
| `WaitLoadingComplete()` | `void` | Warten auf den Abschluss des Ladens |
| `PlayInEditor()` | `void` | Im Editor abspielen |

---

##JSON-Klasse

### UAIChatPlus_JsonObject

JSON Objekt-Wrapper-Klasse.

**Header-Datei:** `Common/Json/AIChatPlus_JsonObject.h`

**Statische Fabrikmethode:**

```cpp
static UAIChatPlus_JsonObject* Create();
static UAIChatPlus_JsonObject* Parse(const FString& JsonString, bool& bSuccess, FString& ErrorMessage);
static UAIChatPlus_JsonObject* FromStruct(const int32& Struct);  // CustomThunk
```

**Methode zum Setzen von Feldern (unterstützt Methodenverkettung):**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `SetStringField(const FString&, const FString&)` | `UAIChatPlus_JsonObject*` | Zeichenkettenfeld setzen |
| `SetNumberField(const FString&, float)` | `UAIChatPlus_JsonObject*` | Numerisches Feld setzen |
| `SetIntegerField(const FString&, int32)` | `UAIChatPlus_JsonObject*` | Ganzzahliges Feld setzen |
| `SetBooleanField(const FString&, bool)` | `UAIChatPlus_JsonObject*` | Boolesches Feld setzen |
| `SetObjectField(const FString&, UAIChatPlus_JsonObject*)` | `UAIChatPlus_JsonObject*` | Objektfeld setzen |
| `SetArrayField(const FString&, UAIChatPlus_JsonArray*)` | `UAIChatPlus_JsonObject*` | Array-Feld setzen |
| `SetNullField(const FString&)` | `UAIChatPlus_JsonObject*` | Nullfeld setzen |

**Feldabrufmethoden:**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `GetStringField(const FString&, const FString&, bool&)` | `FString` | Zeichenkette abrufen |
| `GetNumberField(const FString&, float, bool&)` | `float` | Ermittelt eine Zahl |
| `GetIntegerField(const FString&, int32, bool&)` | `int32` | Ganzzahl abrufen |
| `GetBooleanField(const FString&, bool, bool&)` | `bool` | Booleschen Wert abrufen |
| `GetObjectField(const FString&, bool&)` | `UAIChatPlus_JsonObject*` | Objekt abrufen |
| `GetArrayField(const FString&, bool&)` | `UAIChatPlus_JsonArray*` | Array abrufen |

**Andere Methoden:**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `HasField(const FString&)` | `bool` | Überprüft das Vorhandensein eines Felds |
| `GetFieldType(const FString&)` | `EAIChatPlus_JsonValueType` | Feldtyp abrufen |
| `RemoveField(const FString&)` | `UAIChatPlus_JsonObject*` | Feld entfernen |
| `Clear()` | `UAIChatPlus_JsonObject*` | Löscht alle Felder |
| `ToString(bool)` | `FString` | Konvertiert in Zeichenkette |
| `ToStruct(int32&)` | `bool` | In Struktur umwandeln |
| `Merge(UAIChatPlus_JsonObject*, bool)` | `UAIChatPlus_JsonObject*` | Objekte zusammenführen |
| `Duplicate()` | `UAIChatPlus_JsonObject*` | Objekt duplizieren |
| `IsValid()` | `bool` | Prüft die Gültigkeit |

**Pfadabfragemethode:**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `SetStringByPath(const FString&, const FString&, const FAIChatPlus_JsonPathOptions&)` | `UAIChatPlus_JsonObject*` | Einen String nach Pfad setzen |
| `GetStringByPath(const FString&, const FString&, FAIChatPlus_JsonQueryResult&)` | `FString` | String nach Pfad abrufen |

---

### UAIChatPlus_JsonArray

JSON-Array-Wrapper-Klasse.

**Header-Datei:** `Common/Json/AIChatPlus_JsonArray.h`

**Statische Fabrikmethoden:**

```cpp
static UAIChatPlus_JsonArray* Create();
static UAIChatPlus_JsonArray* Parse(const FString& JsonString, bool& bSuccess, FString& ErrorMessage);
static UAIChatPlus_JsonArray* FromStringArray(const TArray<FString>& Values);
static UAIChatPlus_JsonArray* FromIntegerArray(const TArray<int32>& Values);
```

**Methode zum Hinzufügen von Elementen (unterstützt Methodenverkettung):**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `AddString(const FString&)` | `UAIChatPlus_JsonArray*` | String hinzufügen |
| `AddNumber(float)` | `UAIChatPlus_JsonArray*` | Zahl hinzufügen |
| `AddInteger(int32)` | `UAIChatPlus_JsonArray*` | Integer hinzufügen |
| `AddBoolean(bool)` | `UAIChatPlus_JsonArray*` | Booleschen Wert hinzufügen |
| `AddObject(UAIChatPlus_JsonObject*)` | `UAIChatPlus_JsonArray*` | Objekt hinzufügen |
| `AddArray(UAIChatPlus_JsonArray*)` | `UAIChatPlus_JsonArray*` | Array hinzufügen |
| `AddNull()` | `UAIChatPlus_JsonArray*` | Fügt einen Nullwert hinzu |

**Methoden zum Abrufen von Elementen:**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `GetString(int32, const FString&, bool&)` | `FString` | String abrufen |
| `GetNumber(int32, float, bool&)` | `float` | Zahl abrufen |
| `GetInteger(int32, int32, bool&)` | `int32` | Ganzzahl abrufen |
| `GetBoolean(int32, bool, bool&)` | `bool` | Boolean abrufen |
| `GetObject(int32, bool&)` | `UAIChatPlus_JsonObject*` | Objekt abrufen |
| `GetArray(int32, bool&)` | `UAIChatPlus_JsonArray*` | Array abrufen |

**Andere Methoden:**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `Length()` | `int32` | Länge abrufen |
| `GetElementType(int32)` | `EAIChatPlus_JsonValueType` | Ermittelt den Elementtyp |
| `SetString(int32, const FString&, bool&)` | `UAIChatPlus_JsonArray*` | Zeichenkette setzen |
| `SetObject(int32, UAIChatPlus_JsonObject*, bool&)` | `UAIChatPlus_JsonArray*` | Objekt setzen |
| `RemoveAt(int32, bool&)` | `UAIChatPlus_JsonArray*` | Element entfernen |
| `Clear()` | `UAIChatPlus_JsonArray*` | Array leeren |
| `ToString(bool)` | `FString` | In String umwandeln |
| `Duplicate()` | `UAIChatPlus_JsonArray*` | Kopiert das Array |
| `IsValid()` | `bool` | Überprüft die Gültigkeit |

---

### UAIChatPlus_JsonLibrary

JSON statische Werkzeugbibliothek.

**Header-Datei:** `Common/Json/AIChatPlus_JsonLibrary.h`

**Erstellungsmethode:**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `MakeJsonObjectWithStringField(const FString&, const FString&)` | `UAIChatPlus_JsonObject*` | Erstellt ein Objekt mit einem einzelnen Feld |
| `MakeJsonObjectFromStringMap(const TMap<FString, FString>&)` | `UAIChatPlus_JsonObject*` | Erzeugt ein Objekt aus einer Map |

**Verifizierungsmethode:**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `ValidateJsonString(const FString&, FString&)` | `bool` | JSON-Zeichenkette überprüfen |
| `IsJsonObject(const FString&)` | `bool` | Überprüft, ob es sich um ein Objekt handelt |
| `IsJsonArray(const FString&)` | `bool` | Prüft, ob es sich um ein Array handelt |

**Formatierungsmethode:**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `PrettifyJson(const FString&)` | `FString` | JSON verschönern |
| `MinifyJson(const FString&)` | `FString` | JSON minimieren |

**Strukturumwandlung (CustomThunk):**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `JsonStringToStruct(const FString&, int32&)` | `bool` | JSON in Struktur umwandeln |
| `StructToJsonString(const int32&, bool)` | `FString` | Struktur zu JSON |

**Dateiverwaltung:**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `LoadJsonObjectFromFile(const FString&, bool&, FString&)` | `UAIChatPlus_JsonObject*` | Lädt ein Objekt aus einer Datei |
| `SaveJsonObjectToFile(UAIChatPlus_JsonObject*, const FString&, bool, FString&)` | `bool` | Objekt in Datei speichern |
| `LoadJsonArrayFromFile(const FString&, bool&, FString&)` | `UAIChatPlus_JsonArray*` | Ein Array aus einer Datei laden |
| `SaveJsonArrayToFile(UAIChatPlus_JsonArray*, const FString&, bool, FString&)` | `bool` | Speichert ein Array in einer Datei |

**Vergleichsmethode:**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `EqualsJsonObject(UAIChatPlus_JsonObject*, UAIChatPlus_JsonObject*)` | `bool` | Objekte vergleichen |
| `EqualsJsonArray(UAIChatPlus_JsonArray*, UAIChatPlus_JsonArray*)` | `bool` | Vergleich von Arrays |

**Pfadabfrage:**

| Methode | Rückgabetyp | Beschreibung |
|------|---------|------|
| `QueryStringByPath(UAIChatPlus_JsonObject*, const FString&, const FString&, FAIChatPlus_JsonQueryResult&)` | `FString` | Zeichenkette nach Pfad abfragen |
| `QueryObjectByPath(UAIChatPlus_JsonObject*, const FString&, FAIChatPlus_JsonQueryResult&)` | `UAIChatPlus_JsonObject*` | Objekt nach Pfad abfragen |
| `QueryArrayByPath(UAIChatPlus_JsonObject*, const FString&, FAIChatPlus_JsonQueryResult&)` | `UAIChatPlus_JsonArray*` | Array nach Pfad abfragen |

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte geben Sie Ihr [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)um auf etwaige Auslassungen hinzuweisen. 
