---
layout: post
title: Json-Operationen
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
- Json
- Blueprint
description: Json-Operationen
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Json 操作" />

#Blauplan-Kapitel - JSON-Operationen

<!-- Benötigt ein Bild: Überblick über alle Blueprint-Knoten im Zusammenhang mit Json, einschließlich der Kategorien JsonObject, JsonArray und JsonLibrary -->
![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_all.png)

##Überblick

AIChatPlus bietet eine umfassende Unterstützung für JSON-Blueprint-Operationen, was die Verarbeitung von JSON-Daten in Blueprints erleichtert. Es umfasst hauptsächlich drei Klassen:

* **UAIChatPlus_JsonObject**: JSON-Objektoperationsklasse zur Verarbeitung von JSON im Format `{}`
* **UAIChatPlus_JsonArray**: JSON-Array-Klasse zur Verarbeitung von JSON im `[]`-Format
* **UAIChatPlus_JsonLibrary**: JSON-Hilfsfunktionsbibliothek, bietet statische Hilfsfunktionen

Diese Klassen unterstützen:
* Erstellen, Analysieren und Serialisieren von JSON
* Lesen und Setzen von Feldwerten
* Verschachtelte Pfadabfrage
* JSON und USTRUCT gegenseitig konvertieren
* Dateioperationen (Lesen und Schreiben)
* Method-Chaining

##JsonObject Grundoperationen

###Erstellen eines JsonObject

Verwenden Sie `Create Json Object`, um ein leeres JSON-Objekt zu erstellen:

<!-- benötigte Bilder: Screenshot, der das Rechtsklick-Suchmenü in der Blueprint mit "Create Json Object" und die Erstellung des Knotens zeigt -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_create_1.png)

###Aus der Zeichenfolge parsen

Verwenden Sie `Parse Json Object`, um ein Objekt aus einem JSON-String zu erstellen:

<!-- Benötigt ein Bild: Zeigt den Parse Json Object-Knoten, der einen JSON-String wie '{"name":"test","value":123}' eingibt und JsonObject, bSuccess, ErrorMessage ausgibt -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_parse_1.png)

###Feldwert festlegen

JsonObject bietet verschiedene Set-Methoden, die Methodenverkettung unterstützen:

| Funktion | Beschreibung |
|-----|------|
| `Set String Field` | Zeichenfolgenfeld festlegen |
| `Set Number Field` | Gleitkommazahlfeld festlegen |
| `Set Integer Field` | Ganzzahlfeld festlegen |
| `Set Boolean Field` | Boolesches Feld setzen |
| `Set Object Field` | Verschachteltes Objektfeld festlegen |
| `Set Array Field` | Array-Feld festlegen |
| `Set Null Field` | Null-Feld setzen |

<!-- Benötigt Bild: Darstellung einer Blueprint mit Methodenverkettung zum Setzen mehrerer Felder, wie z.B. Create Json Object -> Set String Field("name", "player1") -> Set Integer Field("level", 10) -> Set Boolean Field("active", true) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_set_1.png)

###Feldwert abrufen

JsonObject bietet verschiedene Get-Methoden:

| Funktion | Beschreibung |
|-----|------|
| `Get String Field` | Holen Sie sich das String-Feld |
| `Get Number Field` | Erhalte Gleitkommazahlenfeld |
| `Ganzzahliges Feld abrufen` | 获取整数字段 |
| `Get Boolean Field` | Boolean-Feld abrufen |
| `Get Object Field` | Erhalte Feld des verschachtelten Objekts |
| `Get Array Field` | Array-Feld abrufen |

<!-- Bild benötigt: Ein Blueprint, das das Abrufen eines Feldwerts aus einem JsonObject zeigt, wobei "Get String Field" verwendet wird, um das Feld "name" zu erhalten, mit den Parametern DefaultValue und bSuccess angezeigt. -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_get_1.png)

###Feldprüfung

| Funktion | Beschreibung |
|-----|------|
| `Has Field` | Überprüft, ob das Feld existiert |
| `Get Field Type` | Feldtyp abrufen |
| `Get Field Names` | Alle Feldnamen abrufen |
| `Remove Field` | Feld löschen |
| `Clear` | Alle Felder leeren |

<!-- Benötigt Bild: Zeigt die Verwendung von Has Field zur Überprüfung der Feldvorhandenheit und Get Field Type zum Abrufen des Feldtyps im Blueprint -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_check_1.png)

###Serialisierung zu einer Zeichenkette

Verwenden Sie `To Json String`, um ein JsonObject in einen String umzuwandeln:

<!-- Benötigtes Bild: Zeigt den "To Json String"-Knoten, Eingabe eines JsonObjects, den Parameter bPrettyPrint und die Ausgabe eines formatierten JSON-Strings -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_tostring_1.png)

##JsonArray Grundoperationen

###JSON-Array erstellen

Verwenden Sie `Create Json Array`, um ein leeres JSON-Array zu erstellen:

<!-- Bild benötigt: Screenshot des Erstellens eines "Create Json Array"-Nodes in Blueprint -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_create_1.png)

###Element hinzufügen

JsonArray bietet verschiedene Add-Methoden, die Methodenverkettung unterstützen:

| Funktion | Beschreibung |
|-----|------|
| `Add String` | Zeichenkette hinzufügen |
| `Add Number` | Gleitkommazahl hinzufügen |
| `Add Integer` | Ganzzahliges Element hinzufügen |
| `Add Boolean` | Boolesches Element hinzufügen |
| `Add Object` | Objektelement hinzufügen |
| `Add Array` | Array-Element hinzufügen |
| `Add Null` | Füge Null-Element hinzu |

<!-- Bild benötigt: Blueprint zur Verkettung von Aufrufen zum Hinzufügen mehrerer Elemente, wie z.B. Create Json Array -> Add String("a") -> Add String("b") -> Add Integer(123) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_add_1.png)

###Element abrufen

JsonArray bietet Methoden zum Abrufen von Elementen über den Index:

| Funktion | Beschreibung |
|-----|------|
| `Get String` | Holen Sie sich das String-Element |
| `Get Number` | Fließkommazahl-Element abrufen |
| `Get Integer` | Hole ganzzahliges Element |
| `Get Boolean` | Boolesches Element abrufen |
| `Get Object` | Objektelement abrufen |
| `Get Array` | Array-Element abrufen |

<!-- Bild benötigt: Blueprint zeigt, wie mit "Get Object by Index" ein Objektelement aus einem Array abgerufen wird -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_get_1.png)

###Array-Operationen

| Funktion | Beschreibung |
|-----|------|
| `Length` | Ermittelt die Länge des Arrays |
| `Is Valid Index` | Überprüft, ob der Index gültig ist |
| `Get Element Type` | Hole den Elementtyp |
| `Remove At` | Entfernt das Element am angegebenen Index |
| `Clear` | Array leeren |

<!-- Bild benötigt: Zeigt die Verwendung von "Length", um die Länge eines Arrays zu erhalten, kombiniert mit einer "For Loop", um das Array zu durchlaufen -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_loop_1.png)

###Stapelkonvertierung

JsonArray unterstützt die Batch-Konvertierung mit UE-Arrays:

| Funktion | Beschreibung |
|-----|------|
| `From String Array` | Von Zeichenketten-Array erstellen |
| `To String Array` | In String-Array umwandeln |
| `From Integer Array` | Aus einem Integer-Array erstellen |
| `To Integer Array` | Zu Ganzzahl-Array konvertieren |

<!-- Bild benötigt: Beispiel zur Verwendung von From String Array und To String Array zeigen -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_batch_1.png)

##Pfadabfrage

JsonObject unterstützt den Zugriff auf verschachtelte Daten über Pfade mit Punktnotation, wie zum Beispiel `player.inventory.gold`.

###Wert nach Pfad abrufen

Verwenden Sie `Get String By Path`, um einen Zeichenfolgenwert nach Pfad abzurufen:

```json
{
    "player": {
        "name": "Hero",
        "inventory": {
            "gold": 1000
        }
    }
}
```

<!-- Bild benötigt: Blueprint-Anzeige mit dem "Get String By Path" Knoten, bei dem der Pfad auf "player.name" gesetzt ist, um einen verschachtelten Wert abzurufen -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_get_1.png)

###Wert nach Pfad festlegen

Verwenden Sie `Set String By Path`, um Werte nach Pfad festzulegen:

<!-- Bild benötigt: Blueprint-Darstellung der Verwendung des "Set String By Path"-Nodes zum Festlegen eines verschachtelten Pfadwerts, wobei die Parameter FAIChatPlus_JsonPathOptions (bCaseSensitive, bCreateMissing) angezeigt werden -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_set_1.png)

###Abfrageergebnis

Die Pfadabfrage gibt die Struktur `FAIChatPlus_JsonQueryResult` zurück, die Folgendes enthält:

* **bSuccess**: Gibt an, ob die Abfrage erfolgreich war.
* **ValueType**: Typ des Rückgabewerts
* **ErrorMessage**: Fehlermeldung (bei Fehlschlag)

<!-- Benötigt ein Bild: Zeigt den Knoten Break FAIChatPlus_JsonQueryResult an, mit den Feldern bSuccess, ValueType und ErrorMessage -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_result_1.png)

##JSON zu USTRUCT Konvertierung

AIChatPlus unterstützt die Konvertierung zwischen JSON und USTRUCT, was die Zusammenarbeit mit Blueprint-Strukturen erleichtert.

###JSON-Zeichenkette zu USTRUCT

Verwenden Sie `Json String To Struct`, um eine JSON-Zeichenkette direkt in eine USTRUCT umzuwandeln:

<!-- Benötigt Bild: Zeigt Json String To Struct Node, der einen JSON-String als Eingabe erhält und Parameter an eine benutzerdefinierte USTRUCT-Variable ausgibt (z.B. FAIChatPlus_OpenAIChatRequestOptions) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_1.png)

###USTRUCT in JSON-String konvertieren

Verwende `Struct To Json String`, um USTRUCT in einen JSON-String zu konvertieren:

<!-- Bild benötigt: Zeigt den Struct-To-Json-String-Knoten, der eine USTRUCT-Variable als Eingabe, den bPrettyPrint-Parameter und einen JSON-String als Ausgabe darstellt -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_2.png)

###JsonObject zu USTRUCT

Verwenden der `To Struct`-Methode von JsonObject:

<!-- Bild erforderlich: zeigt die Verwendung des To-Struct-Knotens für JsonObject -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_3.png)

###USTRUCT zu JsonObject konvertieren

Verwenden Sie die statische Methode `From Struct`, um aus einer USTRUCT ein JsonObject zu erstellen:

<!-- Bild benötigt: Zeigt "From Struct"-Knoten, Eingabe USTRUCT, Ausgabe JsonObject -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_4.png)

##JsonLibrary-Hilfsfunktionen

`UAIChatPlus_JsonLibrary` stellt eine Reihe von statischen Hilfsfunktionen bereit.

###Schnellerfassung

| Funktion | Beschreibung |
|-----|------|
| `Make Json Object With String Field` | Schnelle Erstellung eines JsonObjects mit einem einzelnen Feld |
| `Make Json Object From String Map` | Erstelle JsonObject aus einer Map |

<!-- Bild benötigt: Blaupause, die zeigt, wie man Make Json Object From String Map verwendet, mit Eingabe TMap<FString, FString> und Ausgabe JsonObject -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_make_1.png)

###Verifizierung

| Funktion | Beschreibung |
|-----|------|
| `Validate Json String` | Überprüfen, ob der JSON-String gültig ist |
| `Is Json Object` | Überprüft, ob es sich um ein JSON-Objekt handelt |
| `Is Json Array` | Prüft, ob es sich um ein JSON-Array handelt |

<!-- Bild benötigt: Blaupause zur Veranschaulichung der Validierung einer JSON-Zeichenkette mit "Validate Json String" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_validate_1.png)

###Formatieren

| Funktion | Beschreibung |
|-----|------|
| `Prettify Json` | JSON formatieren (Einzug und Zeilenumbrüche hinzufügen) |
| `Minify Json` | JSON minimieren (Leerzeichen entfernen) |

<!-- Bild benötigt: Demonstration der Formatierung eines JSON-Strings mit Prettify Json, zeigt eingegebenen komprimierten JSON und ausgegebenen formatierten JSON -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_format_1.png)

###Dateiverwaltung

| Funktion | Beschreibung |
---|---|
|-----|------|
| `Load Json Object From File` | JsonObject aus Datei laden |
| `Json-Objekt in Datei speichern` | JsonObject in Datei speichern |
| `Load Json Array From File` | Json-Array aus Datei laden |
| `Json Array In Datei Speichern` | Speichere JsonArray in einer Datei |

<!-- Bild benötigt: Beispiel zur Verwendung von Save Json Object To File und Load Json Object From File zeigen -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_file_1.png)

###Vergleich

| Funktion | Beschreibung |
|-----|------|
| `Equals Json Object` | Vergleicht zwei JsonObjects auf Gleichheit |
| `Equals Json Array` | Vergleicht, ob zwei JsonArrays gleich sind |

<!-- Bild erforderlich: Darstellung einer Blueprint zum Vergleich von zwei JsonObject mit Equals Json Object -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_compare_1.png)

###Erweiterte Pfadabfrage

| Funktion | Beschreibung |
|-----|------|
| `Query String By Path` | String nach Pfad abfragen (Unterstützt Array-Indizes, z.B. `items[0].name`) |
| `Query Object By Path` | Objekt nach Pfad abfragen |
| `Query Array By Path` | Array nach Pfad abfragen |

<!-- Bild benötigt: Darstellung der Verwendung von Query String By Path zur Abfrage eines Pfads mit Array-Index, wie z.B. "data.items[0].name" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_query_1.png)

###Stapelverarbeitung

| Funktion | Beschreibung |
|-----|------|
| `Set String Fields From Map` | Mehrere Zeichenfolgenfelder festlegen |
| `Get String Fields To Map` | Mehrere Zeichenfolgenfelder abrufen |

<!-- Bild benötigt: Blauplan zur Massenvorrichtung von Feldern mittels Set String Fields From Map -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_batch_1.png)

##Weitere Operationen

###JsonObject zusammenführen

Verwenden Sie die Methode `Merge`, um zwei JsonObject-Objekte zusammenzuführen:

<!-- Bild benötigt: Zeigt einen Merge-Knoten, der zwei JsonObjecte zusammenführt, mit Darstellung des bOverwrite-Parameters -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_merge_1.png)

###Kopiere JsonObject

Verwenden Sie die Methode `Duplicate`, um eine tiefe Kopie eines JsonObjects zu erstellen:

<!-- Bild benötigt: Darstellung des Blueprints für das Duplizieren eines JsonObject durch den Duplicate-Knoten -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_dup_1.png)

##Praktische Anwendungsbeispiele

###API-Antwort analysieren

Extrahieren der Parameter für Tool Calls aus KI-Chat-Antworten:

<!-- Benötigt ein Bild: Zeigt ein vollständiges Beispiel-Parsing-Blueprint: vom FunctionArguments-String zum JsonObject geparst, dann mit Get String Field den Parameterwert abrufen -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_1.png)

###Aufbau der Anfrageparameter

Erstellen komplexer Anforderungsparameter mit JsonObject:

<!-- Benötigt Bild: Zeigt einen Bauplan für verschachtelte JSON-Strukturen, Erstellen eines JsonObject mit mehreren Feldern, darunter verschachtelte JsonObjecte und JsonArrays -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_2.png)

###Konfigurationsdatei lesen/schreiben

Laden der Konfiguration aus einer JSON-Datei, Änderungen vornehmen und speichern:

<!-- Bild benötigt: Darstellung des kompletten Konfigurations-Lese-/Schreibprozesses: Load Json Object From File -> Feld ändern -> Save Json Object To File -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_3.png)

##Typaufzählung

Die Aufzählung `EAIChatPlus_JsonValueType` definiert die Typen von JSON-Werten:

| Enumerationswert | Beschreibung |
|-------|------|
| `None` | Unbekannter Typ |
| `Null` | Null-Wert |
| `String` | Zeichenkette |
| `Number` | Zahl |
| `Boolean` | Boolescher Wert |
| `Array` | Array |
| `Object` | Objekt |

<!-- benötigte Abbildung: Darstellung eines Blueprints, der mit dem Switch-Knoten unterschiedliche Verarbeitungen basierend auf JsonValueType durchführt -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_type_1.png)

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte [**Feedback geben**](https://github.com/disenone/wiki_blog/issues/new)Wenn es darauf hinweist, bestimmte Punkte auszulassen. 
