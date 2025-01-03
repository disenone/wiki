---
layout: post
title: UE stellt mehrsprachige Lokalisierung ein
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: Dokumentiere, wie man in der UE Mehrsprachigkeit für Lokalisierung implementiert.
---

<meta property="og:title" content="UE 设置本地化多语言" />

#UE Einstellung für Lokalisierung von Multisprachen

> Aufzeichnen, wie man in UE mehrsprachige Lokalisierung implementiert.

Wenn du mit dem UE-Erweiterungsmenü nicht vertraut bist, empfehle ich dir, zuerst einen kurzen Blick darauf zu werfen: [UE Erweiterter Editor-Menü](ue-扩展编辑器菜单.md)，[Verwendung von Pfadform zum Erweitern des Menüs](ue-使用路径形式扩展菜单.md)

Dieser Text basiert auf dem Plugin: [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Funktionsbeschreibung

UE comes with tools that allow for localization in multiple languages, for example, we can localize the editor's menu:

Chinesische Menü:

![](assets/img/2023-ue-localization/chinese.png)

English menu:

![](assets/img/2023-ue-localization/english.png)

##Code Statement

Um die Lokalisierung des Menüs zu erreichen, müssen wir im Code explizit die Zeichenfolgen angeben, die von der UE verarbeitet werden sollen, unter Verwendung der von UE definierten Makros `LOCTEXT` und `NSLOCTEXT`:

- Global definition of files: Start by defining a macro called `LOCTEXT_NAMESPACE`, which contains the namespace where the multilingual texts are located. Afterwards, texts in the file can be defined using `LOCTEXT`, and the macro `LOCTEXT_NAMESPACE` should be removed at the end of the file.

```cpp
// #define LOCTEXT(InKey, InTextLiteral)

#define LOCTEXT_NAMESPACE "EditorPlusTools"
LOCTEXT("Key", "Content");
#undef LOCTEXT_NAMESPACE

```

Teile Definitionsmethode verwenden `NSLOCTEXT`, Name Raumparameter beim Definieren des Textes hinzufügen:

```cpp
// #define NSLOCTEXT(InNamespace, InKey, InTextLiteral)

NSLOCTEXT("EditorPlusTools", "Key", "Content");
```

UE工具通过查找宏 `LOCTEXT` 和 `NSLOCTEXT` 的出现来收集出所有需要翻译的文本。

##Verwenden Sie ein Übersetzungstool für den Text.

Assuming we have the following code defining text:

```cpp
#define LOCTEXT_NAMESPACE "EditorPlusTools"
// register path node loctext
FEditorPlusPath::GetNodeByPath("/MenuTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/<Hook>Help/<MenuBar>MenuTest/<SubMenu>SubMenu1/<Section>Section1")->SetFriendlyName(LOCTEXT("Section1", "Section1"))->SetFriendlyTips(LOCTEXT("Section1Tips", "Section1Tips"));
#undef LOCTEXT_NAMESPACE
```

Starten Sie zuerst das Übersetzungstool, öffnen Sie die Editor-Einstellungen unter `Bearbeiten - Editor-Präferenzen`, und aktivieren Sie das Kontrollkästchen `Allgemein - Experimentelle Funktionen - Tools - Übersetzungsauswahl`:

![](assets/img/2023-ue-localization/editor_enable_tool.png)


Öffnen Sie dann das Übersetzungstool "Tools - Lokale Steuerungstafel":

![](assets/img/2023-ue-localization/editor_open_tool.png)

Erstellen Sie ein neues Ziel (es ist auch möglich, es unter dem Standard Game zu erstellen; das Neue dient zur einfachen Verwaltung und Verschiebung dieser übersetzten Texte).

![](assets/img/2023-ue-localization/tool_new_target.png)

Setze die Parameter für das Ziel, ändere meinen Namen auf `EditorPlusTools`, lade die Richtlinie als `Editor`, sammle aus Texten und füge das Plugin-Verzeichnis hinzu, die Abhängigkeiten des Ziels sind `Engine, Editor`, andere Einstellungen bleiben unverändert:

![](assets/img/2023-ue-localization/tool_target_config.png)

Bitte fügen Sie eine Sprache hinzu, um sicherzustellen, dass sowohl Chinesisch (vereinfacht) als auch Englisch vorhanden sind. Stellen Sie sicher, dass beim Bewegen des Mauszeigers über den Sprachnamen jeweils `zh-Hans` und `en` angezeigt werden. Wählen Sie die Englische aus (da wir im Code Englisch für die Textdefinitionen verwenden. Wir müssen hier diese englischen Texte sammeln).

![](assets/img/2023-ue-localization/tool_target_lang.png)

Click to collect text:

![](assets/img/2023-ue-localization/tool_target_collect.png)

Es wird ein Fortschrittsfenster angezeigt, warten Sie auf den erfolgreichen Abschluss der Erfassung, dann wird ein grüner Haken angezeigt:

![](assets/img/2023-ue-localization/tool_target_collected.png)

Schließen Sie das Sammelfortschrittfenster, kehren Sie zur Übersetzungstool zurück und Sie sehen die Anzeige der gesammelten Menge in der englischen Zeile. Wir brauchen die Übersetzung des englischen Texts selbst nicht, klicken Sie auf die Schaltfläche "Übersetzen" in der chinesischen Zeile:

![](assets/img/2023-ue-localization/tool_go_trans.png)

Öffnen Sie die Seite, auf der die zu übersetzenden Texte stehen. Geben Sie die Übersetzungen in die Spalte auf der rechten Seite ein. Speichern Sie alles und schließen Sie das Fenster, wenn Sie mit den Übersetzungen fertig sind.

![](assets/img/2023-ue-localization/tool_trans.png)

Bitte zählen Sie die Wörter und Sie werden nach Abschluss die Anzahl der übersetzten Wörter in der chinesischen Spalte sehen:

![](assets/img/2023-ue-localization/tool_count.png)

Bitte, übersetze den Text ins Deutsche:

最后编译文本:

![](assets/img/2023-ue-localization/tool_build.png)

Die übersetzten Daten werden im Ordner `Content\Localization\EditorPlusTools` abgelegt, jeweils in einem Unterordner für jede Sprache. Im Ordner `zh-Hans` finden Sie zwei Dateien: `.archive` sammelt und übersetzt den Text, während `.locres` die kompilierten Daten enthält.

![](assets/img/2023-ue-localization/tool_ret.png)

![](assets/img/2023-ue-localization/tool_ret2.png)

##Die übersetzten Texte in das Plugin-Verzeichnis einfügen.

Wir haben die Übersetzungstexte, die wir für das Plugin erstellt haben, im Projektverzeichnis platziert. Wir müssen diese Texte in das Plugin verschieben, damit sie zusammen mit dem Plugin veröffentlicht werden können.

Verschieben Sie das Verzeichnis `Content\Localization\EditorPlusTools` in das Plugin-Verzeichnis Content. Bei mir lautet der Pfad `Plugins\UE.EditorPlus\Content\Localization\EditorPlusTools`.

Bearbeiten Sie die Konfigurationsdatei des Projekts `DefaultEditor.ini` und fügen Sie den neuen Pfad hinzu:

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```

Auf diese Weise können andere Projekte nach dem Erhalt des Plugins einfach die Datei `DefaultEditor.ini` bearbeiten, um die Übersetzungstexte direkt zu verwenden, ohne die Übersetzung erneut konfigurieren zu müssen.

##Bitte beachten Sie die Hinweise.

Bei der Erstellung von Übersetzungsdaten sind einige Probleme aufgetreten. Hier sind einige Punkte, die beachtet werden sollten:

Im Code müssen Texte mit den Makros `LOCTEXT` und `NSLOCTEXT` definiert werden. Die Texte müssen Zeichenkettenkonstanten sein, damit Unreal Engine sie sammeln kann.
Bitte übersetzen Sie den folgenden Text ins Deutsche:

- Der Zielname darf keine Punkte (`.`) enthalten. Die Verzeichnisnamen unter `Content\Localization\` dürfen keine Punkte (`.`) enthalten, da UE nur den Namen vor dem Punkt abschneidet. Dies kann dazu führen, dass UE beim Lesen des übersetzten Texts aufgrund eines falschen Namens fehlschlägt.
Für Editor-Plugins müssen wir überprüfen, ob sich das Plugin im Befehlszeilenmodus `IsRunningCommandlet()` befindet. In diesem Fall sollen keine Menüs oder SlateUI generiert werden, da im Befehlszeilenmodus das Slate-Modul nicht vorhanden ist und es zu einem Fehler führen kann, wenn Text gesammelt wird. In diesem Fall wird eine Fehlermeldung angezeigt `Assertion failed: CurrentApplication.IsValid()`. Wenn Sie mit einem ähnlichen Fehler konfrontiert sind, können Sie diesen Überprüfung hinzufügen. Genauere Fehlerinformationen:

    > Assertion failed: CurrentApplication.IsValid() [File:E:\UE\ue5.3_git\Engine\Source\Runtime\Slate\Public\Framework\Application\SlateApplication.h] [Line: 255] 

    ![](assets/img/2023-ue-localization/tool_error.png)

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte teilen Sie uns im [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Gibt jede Auslassung an. 
