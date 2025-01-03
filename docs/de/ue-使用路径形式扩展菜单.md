---
layout: post
title: Verwenden Sie Pfadform zur Erweiterung des Menüs.
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
---

<meta property="og:title" content="UE 使用路径形式扩展菜单" />

> Protokollieren, wie ein Pfadmenü in UE implementiert wird. 

Wenn du mit dem UE-Erweiterungsmenü nicht vertraut bist, empfehle ich dir, zuerst einen kurzen Blick darauf zu werfen: [UE-Erweiterungs-Editor-Menü](ue-扩展编辑器菜单.md)

Dieser Text basiert auf dem Plugin: [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Node Management

Organisieren Sie das Menü nach dem Baumstrukturprinzip, wobei Elternknoten Kinder enthalten können:

```cpp
class EDITORPLUS_API FEditorPlusMenuBase: public TSharedFromThis<FEditorPlusMenuBase>
{
protected:
	// sub menus
	TArray<TSharedRef<FEditorPlusMenuBase>> Children;
}
```

Beim Erstellen eines Elternelements gleichzeitig ein Unterelement erstellen:

```cpp
void FEditorPlusMenuBase::Register(FMenuBuilder& MenuBuilder)
{
	for (const auto Menu: Children)
	{
		Menu->Register(MenuBuilder);
	}
}
```

Natürlich wird das konkrete Erstellungsverhalten für jeden Knoten etwas unterschiedlich sein, indem die virtuelle Funktion überschrieben wird:

```cpp
// Menubar
void FEditorPlusMenuBar::Register(FMenuBarBuilder& MenuBarBuilder)
{
	MenuBarBuilder.AddPullDownMenu(
		GetFriendlyName(),
		GetFriendlyTips(),
        // Delegate to call Register
		FEditorPlusMenuManager::GetDelegate<FNewMenuDelegate>(GetUniqueId()),       
		Hook);
}

// Section
void FEditorPlusSection::Register(FMenuBuilder& MenuBuilder)
{
	MenuBuilder.BeginSection(Hook, GetFriendlyName());
	FEditorPlusMenuBase::Register(MenuBuilder);
	MenuBuilder.EndSection();
}

// Separator
void FEditorPlusSeparator::Register(FMenuBuilder& MenuBuilder)
{
	MenuBuilder.AddMenuSeparator(Hook);
	FEditorPlusMenuBase::Register(MenuBuilder);
}

// SubMenu
void FEditorPlusSubMenu::Register(FMenuBuilder& MenuBuilder)
{
	MenuBuilder.AddSubMenu(
		GetFriendlyName(),
		GetFriendlyTips(),
		FNewMenuDelegate::CreateSP(this, &FEditorPlusSubMenu::MakeSubMenu),
		false,
		FSlateIcon(),
		true,
		Hook
	);
}

// Command
void FEditorPlusCommand::Register(FMenuBuilder& MenuBuilder)
{
    MenuBuilder.AddMenuEntry(
        CommandInfo->Label, CommandInfo->Tips, CommandInfo->Icon,
        CommandInfo->ExecuteAction, CommandInfo->Hook, CommandInfo->Type);
}

// ......
```

##Erstellen Sie Knoten durch den Pfad.

Organisieren Sie das Menü in Baumstruktur, dann können Sie mit dem Pfadformat die Struktur eines Menüs definieren:

```cpp
"/<Hook>Help/<MenuBar>BarTest/<SubMenu>SubTest/<Command>Action"
```

Die oben genannte Methode ermöglicht die Erstellung einer Reihe von Menüs:

- `<Hook>Help`: Positioniert hinter dem Menü mit dem Hook-Namen Help.
`<MenuBar>BarTest`：Erstellt ein Menü vom Typ Menüleiste mit dem Namen BarTest.
- `<SubMenu>SubTest`：Create a sub-node, type SubMenu, named SubTest.
- `<Command>Action`: Erstellen Sie schließlich einen Befehl.

Die Aufrufmethode der Schnittstelle kann sehr einfach sein:

```cpp
const FString Path = "/<Hook>Help/<MenuBar>BarTest/<SubMenu>SubTest/<Command>Action";
FEditorPlusPath::RegisterPathAction(
	Path, 
    FExecuteAction::CreateLambda([]
    {
        // do action
    })
);
```

##Erstellen von Knoten aus benutzerdefinierten Formen.

Wir halten immer noch an der umständlichen Methode fest, Menüs zu erstellen. Diese umständliche Methode ermöglicht detailliertere Einstellungen und ähnelt der Organisationsstruktur von UE's SlateUI-Schreibweise.

```cpp
EP_NEW_MENU(FEditorPlusMenuBar)("BarTest")
->RegisterPath()
->Content({
    EP_NEW_MENU(FEditorPlusSubMenu)("SubTest")
    ->Content({
        EP_NEW_MENU(FEditorPlusCommand)("Action")
        ->BindAction(FExecuteAction::CreateLambda([]
            {
                // do action
            })),
    })
});
```

##Gemischte Form

Natürlich sind sowohl die vorgegebenen Pfadformen als auch benutzerdefinierte Menüs identisch und können flexibel kombiniert werden.

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>BarTest/<SubMenu>SubMenu/<Command>Action1", 
    EP_NEW_MENU(FEditorPlusCommand)("Action1")
    ->BindAction(FExecuteAction::CreateLambda([]
        {
            // do action
        })),
);

FEditorPlusPath::RegisterPath(
    "/<MenuBar>BarTest/<SubMenu>SubMenu/<Command>Action2", 
    EP_NEW_MENU(FEditorPlusCommand)("Action2")
    ->BindAction(FExecuteAction::CreateLambda([]
        {
            // do action
        })),
);
```

Menüs, die an verschiedenen Stellen definiert sind, werden in einer einzigen Baumstruktur zusammengeführt, wobei Knoten mit demselben Namen als derselbe Knoten betrachtet werden. Anders ausgedrückt, der Pfad ist eindeutig; ein und derselbe Pfad kann einen Menüknoten eindeutig bestimmen.
Dann können wir auch die Knoten finden, neu konfigurieren und anpassen:

```cpp
// set Name and Tips
FEditorPlusPath::GetNodeByPath("/<MenuBar>BarTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


--8<-- "footer_de.md"


> Dieser Text wurde mit ChatGPT übersetzt. Bitte geben Sie [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Benennen Sie alle Übersehenen Stellen. 
