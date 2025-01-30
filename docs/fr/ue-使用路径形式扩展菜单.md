---
layout: post
title: UE utilise le chemin d'accès pour étendre le menu
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
---

<meta property="og:title" content="UE 使用路径形式扩展菜单" />

> Notez comment mettre en place un menu déroulant étendu en forme de chemin dans UE.

Si vous n'êtes pas familiarisé avec le menu d'extension UE, il est conseillé de jeter un coup d'œil au : [Menu de l'éditeur d'extension UE](ue-扩展编辑器菜单.md)

Le code de cet article est basé sur le plugin : [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Gestion des nœuds

Organiser le menu selon une structure arborescente où les nœuds pères peuvent contenir des nœuds enfants :

```cpp
class EDITORPLUS_API FEditorPlusMenuBase: public TSharedFromThis<FEditorPlusMenuBase>
{
protected:
	// sub menus
	TArray<TSharedRef<FEditorPlusMenuBase>> Children;
}
```

Créez des nœuds enfants en même temps que vous créez des nœuds parents :

```cpp
void FEditorPlusMenuBase::Register(FMenuBuilder& MenuBuilder)
{
	for (const auto Menu: Children)
	{
		Menu->Register(MenuBuilder);
	}
}
```

Bien sûr, le comportement spécifique de création de chaque nœud sera un peu différent, en écrivant des fonctions virtuelles pour le mettre en œuvre :

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

##Générer un nœud à partir du chemin

Organisez le menu selon une structure arborescente, le format de chemin peut définir la structure arborescente d'un menu :

```cpp
"/<Hook>Help/<MenuBar>BarTest/<SubMenu>SubTest/<Command>Action"
```

Les éléments ci-dessus permettent de définir la création d'une série de menus:

- `<Hook>Aide` : situé après le menu ayant pour nom Hook Aide
- `<MenuBar>BarTest` : Crée un menu de type MenuBar, nommé BarTest.
- `<SubMenu>SubTest` : Créer un sous-nœud, type SubMenu, nom SubTest
- `<Command>Action` : Créer enfin une commande

La forme d'appel de l'interface peut être très simple :

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

##Générer des noeuds à l'aide de formulaires personnalisés.

Nous avons conservé une méthode lourde pour créer le menu, cette méthode lourde permet d'avoir des réglages plus détaillés, l'organisation du code ressemble un peu à la façon d'écrire de SlateUI dans UE :

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

##La forme mixte

Bien sûr, la forme du chemin lui-même et le menu généré de manière personnalisée sont identiques ; ils peuvent être utilisés de manière interchangeable, offrant ainsi une grande flexibilité.

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

Les menus définis à plusieurs endroits seront fusionnés dans une même structure arborescente, et les nœuds portant le même nom seront considérés comme un seul et même nœud. En d'autres termes, le chemin est unique, et un même chemin peut identifier de manière unique un nœud de menu.
Alors nous pouvons également identifier les nœuds, puis apporter des ajustements et des modifications :

```cpp
// set Name and Tips
FEditorPlusPath::GetNodeByPath("/<MenuBar>BarTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


--8<-- "footer_fr.md"


> Ce post a été traduit à l'aide de ChatGPT, veuillez laisser vos [**retours**](https://github.com/disenone/wiki_blog/issues/new)Signalez tout manquement. 
