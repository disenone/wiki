---
layout: post
title: UE utilise le chemin pour étendre le menu
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
---

<meta property="og:title" content="UE 使用路径形式扩展菜单" />

> Veuillez traduire ce texte en français :
> Enregistrer comment mettre en place une extension de menu sous forme de chemin dans UE.

Si vous n'êtes pas familier avec le menu d'extension de l'UE, il est conseillé de le consulter brièvement : [Menu de l'éditeur d'extension de l'UE](ue-扩展编辑器菜单.md)

Ce texte est basé sur le plugin: [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Gestion des nœuds

Organiser le menu selon la structure d'un arbre, où les nœuds principaux peuvent inclure des sous-éléments :

```cpp
class EDITORPLUS_API FEditorPlusMenuBase: public TSharedFromThis<FEditorPlusMenuBase>
{
protected:
	// sub menus
	TArray<TSharedRef<FEditorPlusMenuBase>> Children;
}
```

Créez des nœuds enfants en même temps que le nœud parent:

```cpp
void FEditorPlusMenuBase::Register(FMenuBuilder& MenuBuilder)
{
	for (const auto Menu: Children)
	{
		Menu->Register(MenuBuilder);
	}
}
```

Bien sûr, le comportement spécifique à la création de chaque nœud peut varier légèrement, en écrivant des fonctions virtuelles pour le mettre en œuvre :

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

##Générer des nœuds via un chemin.

Organisez les menus selon une structure arborescente, le format du chemin permet de définir la structure arborescente d'un menu :

```cpp
"/<Hook>Help/<MenuBar>BarTest/<SubMenu>SubTest/<Command>Action"
```

Les textes suivants peuvent être traduits en langue française :

Les expressions ci-dessus peuvent être interprétées comme définissant la création d'une série de menus :

`<Hook>Help`：Positionné après le menu nommé Help de Hook
`<MenuBar>BarTest` : Crée un menu de type MenuBar nommé BarTest.
- `<SubMenu>SubTest`：Crée un sous-noeud, de type Sous-menu, nommé SubTest
`<Command>Action`：Finaliser la création d'une commande

Le format des appels d'API peut être très concis :


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

##Créer des nœuds à partir de formulaires personnalisés

Nous continuons à utiliser une approche lourde pour créer les menus, ce qui permet des réglages plus détaillés. La structure du code ressemble un peu à la façon dont SlateUI de UE est écrit :

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

##Forme mixte

Bien sûr, les formats de chemin par défaut et les menus générés sur mesure sont identiques et peuvent être combinés pour offrir une grande flexibilité.

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

Les menus définis à partir de plusieurs endroits seront regroupés dans une même structure arborescente, où les nœuds de même nom seront considérés comme uniques. Autrement dit, le chemin est unique, une même trajectoire pouvant identifier de façon unique un nœud de menu.
Nous pouvons alors identifier les nœuds, et procéder à des ajustements et modifications supplémentaires :

```cpp
// set Name and Tips
FEditorPlusPath::GetNodeByPath("/<MenuBar>BarTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez faire part de vos remarques dans [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)S'il vous plaît signaler toute omission. 
