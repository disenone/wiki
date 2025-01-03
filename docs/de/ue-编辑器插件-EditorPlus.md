---
layout: post
title: UE EditorPlus Documentation über das UE-Editor-Plugin UE.EditorPlus
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
description: UE EditorPlus Plugin Documentation
---

<meta property="og:title" content="UE 编辑器插件 EditorPlus 说明文档" />

#UE 编辑器插件 UE.EditorPlus 说明文档 - Dokumentation zu UE.EditorPlus-Plugin

##Please find the translation below:

Vorstellungsvideo

![type:video](assets/img/2024-ue-editorplus/market/video.mp4)

##Plugin source code

[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Einkaufszentrum herunterladen

[EditorPlus](https://www.unrealengine.com/marketplace/zh-CN/product/editorplus)

##Add-on Plugin for the project EU.EditorPlus

Referenzdokumente:

Deutsch: [UE fügt Plugins durch das Hinzufügen von Plug-in-Quellcode hinzu](https://wiki.disenone.site/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)
- English: [UE adds plugins through the plugin source code](https://wiki.disenone.site/en/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)


##Plug-in description

UE.EditorPlus is a UE editor plugin that offers a convenient way to expand editor menus and supports advanced methods of extension, as well as including some practical editor tools. This plugin is compatible with UE5.3+.


##Erweitern Sie das Editor-Menü.

![](assets/img/2024-ue-editorplus/menu.png)

![](assets/img/2024-ue-editorplus/toolbar.png)

###Erklären

Unterstützung für die Erweiterung des Editor-Menüs auf verschiedene Arten:

- Pfadmethode: `RegisterPathAction("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action")`
Instanziierungsart: `EP_NEW_MENU(FEditorPlusMenuBar)("Bar")`
- Mischungsmodus: `RegisterPath("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",EP_NEW_MENU(FEditorPlusCommand)("Action")`

###Pfadmodus

Sie können ein Editor-Menübefehl auf diese Weise registrieren:

```cpp
FEditorPlusPath::RegisterPathAction(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",
    FExecuteAction::CreateLambda([]
        {
            // do action
        })
);
```

Auf diese Weise können Sie in der Menüleiste des Editors hinter "Hilfe" eine neue Menüleiste namens "Bar" hinzufügen. In der "Bar" können Sie ein Untermenü namens "SubMenu" erstellen, das eine Aktion enthält.

Die vollständige Pfadformatierung würde folgendermaßen aussehen: `/<Hook>HookName/<Type1>Name1/<Type2>Name2`, wobei der erste Pfad `<Hook>` sein muss. Die derzeit unterstützten Typen und Beschränkungen sind:

- `<Hook>`: indicates where the menu should be generated in which Hook position, with no `<Hook>` allowed in subsequent paths
- `<MenuBar>`: Menüleiste, Pfad darf nicht `<Hook>, <MenuBar>, <ToolBar>` enthalten
- `<ToolBar>`: Symbolleiste, die keinen `<Hook>, <MenuBar>, <ToolBar>` Pfad dahinter haben darf.
- `<Section>`: Menüabschnitt; hinter dem Pfad dürfen keine `<Hook>`, `<MenuBar>`, `<Section>` stehen.
- `<Separator>`: Trennzeichen im Menü, nachfolgender Pfad darf nicht `<Hook>, <MenuBar>` enthalten.
- `<SubMenu>`: Untermenü, die nachfolgende Pfade dürfen keine `<Hook>, <MenuBar>` enthalten.
- `<Command>`: Menübefehl, es darf kein Pfad dahinter stehen.
- `<Widget>`: Weitere anpassbare Slate UI-Komponenten, die erweitert werden können, ohne dass dabei ein Pfad folgt.

Eine einfachere Pfadform wäre: `/BarName/SubMenuName1/SubMenuName2/CommandName`. Wenn kein Typ angegeben ist, ist der erste Teil des Pfades `<MenuBar>`, der mittlere Teil `<SubMenu>` und der letzte Teil `<Command>`.

Wenn kein `<Hook>` angegeben ist, wird automatisch `<Hook>Help` hinzugefügt, um anzugeben, dass die Menüleiste hinter dem Hilfemenü hinzugefügt werden soll.

###Instantiation method

Der Pfadmodus erstellt automatisch alle Knoten basierend auf Typ und Standardparametern. Wir können auch die Instantiierung selbst steuern, um den Inhalt der Erweiterung genauer zu kontrollieren.

```cpp
EP_NEW_MENU(FEditorPlusMenuBar)("MyBar", "MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips"))
->RegisterPath()
->Content({
    EP_NEW_MENU(FEditorPlusSubMenu)("MySubMenu")
    ->Content({
        EP_NEW_MENU(FEditorPlusCommand)("MyAction")
        ->BindAction(FExecuteAction::CreateLambda([]
            {
                // do action
            })),
    })
});
```

Beim Instanziieren von `MyBar` können der Hook-Name, der lokalisierte Name und die lokalisierungshinweisenden Parameter (`"MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips")`) übergeben werden. Der obige Code entspricht dem Pfad `/<Hook>Help/<MenuBar>MyBar/<SubMenu>MySubMenu/<Command>MyAction`.

###Mischmodus

Natürlich können beide Methoden auch kombiniert werden:

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",
    EP_NEW_MENU(FEditorPlusCommand)("Action")
    ->BindAction(FExecuteAction::CreateLambda([]
        {
            // do action
        })),
);
```

In this situation, the plugin will automatically instantiate the nodes in the middle path, while the final path will utilize nodes instantiated by the user.

###Mehr Anwendungsbeispiele.

Header-Datei:

```cpp
#include <EditorPlusPath.h>
```

Die Lokalisierungssprache wird durch den Pfad festgelegt, `EP_FNAME_HOOK_AUTO` bedeutet, dass der Name des Hooks automatisch aus dem Dateipfad generiert wird:

```cpp
FEditorPlusPath::RegisterPathAction(
        "/Bar/Action",
        FExecuteAction::CreateLambda([]
        {
            // do action
        }),
        EP_FNAME_HOOK_AUTO,
        LOCTEXT("Action", "Action"),
        LOCTEXT("ActionTips", "ActionTips"));
```

Holen Sie sich den Knoten über den Pfad und setzen Sie die Lokalisierungstexte:

```cpp
FEditorPlusPath::GetNodeByPath("/MenuTest")
    ->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))
    ->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


Fügen Sie am Ende des Pfads eine Slate UI-Komponente hinzu.

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Widget>Widget",
    EP_NEW_MENU(FEditorPlusWidget)("Widget", LOCTEXT("Widget", "Widget"))
        ->BindWidget(SNew(SHorizontalBox)));
);
```

Fügen Sie einen neuen Knoten in den integrierten Hook von UE hinzu.

```cpp
FEditorPlusPath::RegisterPath("<Hook>EpicGamesHelp/<Separator>ExtendSeparator")
```

Wiederholte Angaben desselben Pfads werden als derselbe Pfad erkannt, daher kann derselbe Pfad kontinuierlich erweitert werden.

```cpp
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path1", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path1", "Path1"), LOCTEXT("Path1Tips", "Path1Tips"));
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path2", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path2", "Path2"), LOCTEXT("Path2Tips", "Path2Tips"));
```

Um einen Knoten auf dem Pfad fortzusetzen.

```cpp
auto node = FEditorPlusPath::GetNodeByPath("/MenuTest");
FEditorPlusPath::RegisterChildPath(node, "<SubMenu>Sub/<Separator>Sep");
```

Entfernen Sie einen Pfad.

```cpp
FEditorPlusPath::UnregisterPath("/MenuTest/SubMenu1/SubMenu1/Path1");
```

Erweiterte Symbolleiste.
```cpp
FEditorPlusPath::RegisterPath("/<Hook>ProjectSettings/<ToolBar>MenuTestToolBar")
->Content({
    EP_NEW_MENU(FEditorPlusCommand)("ToolBarCommand1")
    ->BindAction(...)
});
```

###Schnittstellenbeschreibung

```cpp
class EDITORPLUS_API FEditorPlusPath
{
public:

	static TSharedPtr<FEditorPlusMenuBase> RegisterPath(const FString& Path, const TSharedPtr<FEditorPlusMenuBase>& Menu=nullptr);
	static TSharedPtr<FEditorPlusMenuBase> RegisterPath(const FString& Path, const FText& FriendlyName, const FText& FriendlyTips);
	static TSharedPtr<FEditorPlusMenuBase> RegisterPathAction(
		const FString& Path, const FExecuteAction& ExecuteAction, const FName& Hook=EP_FNAME_HOOK_AUTO,
		const FText& FriendlyName=FText::GetEmpty(), const FText& FriendlyTips=FText::GetEmpty());

	static TSharedPtr<FEditorPlusMenuBase> RegisterChildPath(
		const TSharedRef<FEditorPlusMenuBase>& InParent, const FString& Path, const TSharedPtr<FEditorPlusMenuBase>& Menu=nullptr);
	static TSharedPtr<FEditorPlusMenuBase> RegisterChildPath(
		const TSharedRef<FEditorPlusMenuBase>& InParent, const FString& Path, const FText& FriendlyName, const FText& FriendlyTips);
	static TSharedPtr<FEditorPlusMenuBase> RegisterChildPathAction(
		const TSharedRef<FEditorPlusMenuBase>& InParent, const FString& Path, const FExecuteAction& ExecuteAction,
		const FName& Hook=EP_FNAME_HOOK_AUTO, const FText& FriendlyName=FText::GetEmpty(), const FText& FriendlyTips=FText::GetEmpty());

	static bool UnregisterPath(
		const FString& Path, const TSharedPtr<FEditorPlusMenuBase>& Leaf=nullptr);

	static TSharedPtr<FEditorPlusMenuBase> GetNodeByPath(const FString& Path);
};
```

`RegisterPath`: Erstellung des Pfadmenüs
- `RegisterPathAction`: Erzeugt ein Pfadmenü und verknüpft automatisch die Aktionen mit dem Endknoten `<Command>`.
`RegisterChildPath`: Erzeugt fortlaufend Kindpfade für den angegebenen Knoten.
`RegisterChildPathAction`: Erzeugt automatisch Subpfade für den angegebenen Knoten und verknüpft die Aktionen automatisch.
`UnregisterPath`: Lösche den Pfad, `Leaf` kann für strenges Matching verwendet werden, wenn es mehrere Endknoten mit demselben Namen gibt. Während des Löschvorgangs wird der Vorgang zurückverfolgt und ein Zwischenknoten wird gelöscht, sobald er keine weiteren Knoten enthält.
`GetNodeByPath`: Holen Sie den Knoten anhand des Pfads.


Knotentyp

```cpp
// base class of all node
class EDITORPLUS_API FEditorPlusMenuBase: public TSharedFromThis<FEditorPlusMenuBase> {}

class EDITORPLUS_API FEditorPlusHook: public TEditorPlusMenuBaseRoot {}

class EDITORPLUS_API FEditorPlusMenuBar: public TEditorPlusMenuBaseNode {}

class EDITORPLUS_API FEditorPlusToolBar: public TEditorPlusMenuBaseNode {}

class EDITORPLUS_API FEditorPlusSection: public TEditorPlusMenuBaseNode {}

class EDITORPLUS_API FEditorPlusSeparator: public TEditorPlusMenuBaseNode{}

class EDITORPLUS_API FEditorPlusSubMenu: public TEditorPlusMenuBaseNode {}

class EDITORPLUS_API FEditorPlusCommand: public TEditorPlusMenuBaseLeaf {}

class EDITORPLUS_API FEditorPlusWidget: public TEditorPlusMenuBaseLeaf {}
```

Für weitere Beispiele und Schnittstellenbeschreibungen bitte im Quellcode nachsehen [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)"Test case [MenuTest.cpp](https://github.com/disenone/UE.EditorPlus/blob/ue5.3/Source/EditorPlusTools/Private/MenuTest/MenuTest.cpp)


###Modulares Management

UE.EditorPlus bietet auch ein Framework zur modularen Verwaltung von Erweiterungsmenüs an, das das automatische Laden und Entladen von Menüerweiterungen beim Laden und Entladen von Plugins unterstützt.

Lassen Sie die Menüklasse `IEditorPlusToolInterface` erben und überschreiben Sie die Funktionen `OnStartup` und `OnShutdown`. `OnStartup` ist für das Erstellen des Menüs zuständig, `OnShutdown` ruft die `Destroy`-Funktion des Knotens auf, um das Menü zu bereinigen. Sobald die Referenzzahl eines Knotens auf 0 fällt, wird eine automatische Bereinigung durchgeführt.

```cpp
class FMenuTest: public IEditorPlusToolInterface
{
public:
	virtual void OnStartup() override;
	virtual void OnShutdown() override;
}

void FMenuTest::OnStartup()
{
	BuildPathMenu();
	BuildCustomMenu();
	BuildMixMenu();
	BuildExtendMenu();
}

void FMenuTest::OnShutdown()
{
	for(auto Menu: Menus)
	{
		if(Menu.IsValid()) Menu->Destroy();
	}
	Menus.Empty();
}
```

Die Menuverwaltungsklasse erbt von `IEditorPlusToolManagerInterface` und überschreibt die Funktion `AddTools`, um die Menüklasse hinzuzufügen.

```cpp
class FEditorPlusToolsImpl: public IEditorPlusToolManagerInterface
{
public:
	virtual void AddTools() override;
}

void FEditorPlusToolsImpl::AddTools()
{
	if (!Tools.Num())
	{
		Tools.Emplace(MakeShared<FMenuTest>());
	}

}
```

Bei der  Lade- und Entladefunktion von Plugins werden die Funktionen `StartupTools` und `ShutdownTools` der Verwaltungsklasse aufgerufen.

```cpp
void FEditorPlusToolsModule::StartupModule()
{
	Impl = FEditorPlusToolsImpl::Get();
	Impl->StartupTools();

}
void FEditorPlusToolsModule::ShutdownModule()
{
	Impl->ShutdownTools();
}
```

Nachdem die oben genannten Anpassungen abgeschlossen wurden, wird das Menü der Erweiterungen automatisch geladen und entladen, wenn die Plugins geladen und entladen werden.


##Editor-Tool

UE.EditorPlus bietet auch einige praktische Editor-Tools an.

##Erstellen eines Editorfensters.

Mit EditorPlus können Sie ganz einfach ein neues Editorfenster erstellen.

```cpp
// register spawn tab
Tab = MakeShared<FEditorPlusTab>(LOCTEXT("ClassBrowser", "ClassBrowser"), LOCTEXT("ClassBrowserTip", "Open the ClassBrowser"));
Tab->Register<SClassBrowserTab>();

// register menu action to spawn tab
FEditorPlusPath::RegisterPathAction(
    "/EditorPlusTools/ClassBrowser",
    FExecuteAction::CreateSP(Tab.ToSharedRef(), &FEditorPlusTab::TryInvokeTab),
);
```

`SClassBrowserTab` is a custom UI control.

```cpp
class SClassBrowserTab final : public SCompoundWidget
{
	SLATE_BEGIN_ARGS(SClassBrowserTab)
	{}
	SLATE_END_ARGS()
    // ...
}
```

### ClassBrowser

Der ClassBrowser ist ein UE-Class-Viewer, der über das Menü EditorPlusTools -> ClassBrowser geöffnet werden kann.

![](assets/img/2024-ue-editorplus/classbrowser_menu.png)

![](assets/img/2024-ue-editorplus/classbrowser.png)

Basierend auf der UE-Reflexion realisiert, können Sie bequem verschiedene Arten von UE-Mitgliedsinformationen anzeigen, Erklärungen und Hinweise erhalten, unterstützen eine verschwommene Suche und ermöglichen das Öffnen von Informationen der Elternklasse.

### MenuCollections

MenuCollections ist ein Tool zur schnellen Suche und Sammlung von Menübefehlen. Es hilft Ihnen, schnell die benötigten Menübefehle zu finden und häufig verwendete Befehle zu speichern, um die Effizienz zu steigern.

![](assets/img/2024-ue-editorplus/menucollection_find.png)

![](assets/img/2024-ue-editorplus/menucollection_star.png)


### SlateResourceBrowser

SlateResourceBrowser ist ein Tool, mit dem Sie schnell Slate UI-Ressourcen anzeigen können. Es hilft Ihnen dabei, die benötigten Editor-Ressourcen zu durchsuchen und zu finden, um den Editor einfach zu erweitern.

![](assets/img/2024-ue-editorplus/slateresourcebrowser_color.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_icon.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_font.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_widgetstyle.png)

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte[ **feedback**](https://github.com/disenone/wiki_blog/issues/new)Führen Sie eventuelle Auslassungen bitte an. 
