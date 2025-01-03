---
layout: post
title: Plugin de l'éditeur UE.EditorPlus de l'UE - Documentation
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
description: Plugin de l'éditeur UE  UE.EditorPlus  Documentation
---

<meta property="og:title" content="UE 编辑器插件 EditorPlus 说明文档" />

#Plugin UE.EditorPlus documentation

##Vidéo d'introduction

![type:video](assets/img/2024-ue-editorplus/market/video.mp4)

##Code source du plug-in

[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Téléchargement du magasin

[EditorPlus](https://www.unrealengine.com/marketplace/zh-CN/product/editorplus)

##Ajouter un plug-in de code source au projet EU.EditorPlus.

Références :

- Chinese: [Adding plugins through plugin source code in UE](https://wiki.disenone.site/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)
- English: [UE adds plugins through the plugin source code](https://wiki.disenone.site/en/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)


##Description du module complémentaire

UE.EditorPlus is a UE editor plugin that offers a convenient way to extend the editor menu and supports advanced methods of expansion, while also including some practical editor tools. This plugin is compatible with UE5.3+.


##Élargir le menu de l'éditeur

![](assets/img/2024-ue-editorplus/menu.png)

![](assets/img/2024-ue-editorplus/toolbar.png)

###Explication

Prise en charge de plusieurs options d'extension du menu de l'éditeur :

Voie d'enregistrement : `RegisterPathAction("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action")`
Méthode d'instanciation : `EP_NEW_MENU(FEditorPlusMenuBar)("Bar")`
- Mode mixte : `RegisterPath("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",EP_NEW_MENU(FEditorPlusCommand)("Action")`

###Mode de route

Il est possible de s'inscrire à une commande de menu d'éditeur de cette manière :

```cpp
FEditorPlusPath::RegisterPathAction(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",
    FExecuteAction::CreateLambda([]
        {
            // do action
        })
);
```

Ainsi, vous pouvez ajouter une barre de menu Bar derrière l'option Help de la barre de menu de l'éditeur, avec un sous-menu SubMenu contenant une commande Action.

Le format complet du chemin serait le suivant : `/<Hook>HookName/<Type1>Nom1/<Type2>Nom2`, le premier chemin doit être `<Hook>`, les types pris en charge actuellement et leurs restrictions :

- `<Hook>`：Indique à quel emplacement du Hook générer le menu, les chemins ultérieurs ne peuvent pas contenir `<Hook>`
- `<MenuBar>` : Barre de menu, les noms de chemin à l'arrière ne peuvent inclure `<Hook>, <MenuBar>, <ToolBar>`
- `<ToolBar>` : Barre d'outils, ne doit pas être suivi des éléments `<Hook>, <MenuBar>, <ToolBar>`
- `<Section>` : Section de menu, aucun chemin ne doit contenir `<Hook>, <MenuBar>, <Section>` après.
- `<Separator>`: Séparateur de menu, aucun chemin ne doit contenir `<Hook>, <MenuBar>`
- `<SubMenu>`: Sous-menu, aucun chemin ne peut être suivi de `<Hook>, <MenuBar>`
- `<Command>` : Commande de menu, aucun chemin ne doit suivre.
- `<Widget>`: Composant Slate UI plus personnalisable et extensible, aucun chemin ne doit être spécifié après.

Une forme de chemin plus simple : `/NomBarre/NomSousMenu1/NomSousMenu2/NomCommande`, si le type n'est pas spécifié, le premier élément du chemin est `<BarreMenu>`, le milieu est `<SousMenu>`, et le dernier est `<Commande>`.

Si `<Hook>` n'est pas spécifié, ajoute automatiquement `<Hook>Help` en premier, ce qui signifie ajouter une barre de menu après le menu Aide.

###Méthode d'instanciation

Le mode de chemin crée automatiquement toutes les nœuds en fonction de leur type et des paramètres par défaut, mais nous pouvons également gérer nous-mêmes l'instanciation pour un contrôle plus précis de l'extension du contenu.

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

Lors de l'instanciation de `MyBar`, vous pouvez transmettre le nom du Hook, le nom de localisation et les paramètres de localisation pour astuces (`"MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips")`). Le code ci-dessus équivaut au chemin `<Hook>Help/<MenuBar>MyBar/<SubMenu>MySubMenu/<Command>MyAction`.

###Méthode de mélange

Bien sûr, il est possible de combiner les deux méthodes :

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

Dans ce cas, le plug-in instanciera automatiquement les noeuds du chemin intermédiaire, tandis que les noeuds du chemin final seront ceux instanciés par l'utilisateur lui-même.

###Plus d'exemples

Fichier d'en-tête :

```cpp
#include <EditorPlusPath.h>
```

Le chemin désigne la langue de localisation, `EP_FNAME_HOOK_AUTO` indique l'utilisation automatique du nom du chemin comme nom du `Hook`:

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

Obtenir les nœuds via le chemin d'accès et définir le texte localisé :

```cpp
FEditorPlusPath::GetNodeByPath("/MenuTest")
    ->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))
    ->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


Ajoutez un composant Slate UI à la fin du chemin.

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Widget>Widget",
    EP_NEW_MENU(FEditorPlusWidget)("Widget", LOCTEXT("Widget", "Widget"))
        ->BindWidget(SNew(SHorizontalBox)));
);
```

Ajouter de nouveaux nœuds dans le Hook fourni par l'UE.

```cpp
FEditorPlusPath::RegisterPath("<Hook>EpicGamesHelp/<Separator>ExtendSeparator")
```

Répéter le même chemin à plusieurs reprises fait qu'il est reconnu comme un seul chemin, ce qui permet d'étendre continuellement le même chemin.

```cpp
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path1", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path1", "Path1"), LOCTEXT("Path1Tips", "Path1Tips"));
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path2", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path2", "Path2"), LOCTEXT("Path2Tips", "Path2Tips"));
```

Étendre le chemin pour un nœud supplémentaire.

```cpp
auto node = FEditorPlusPath::GetNodeByPath("/MenuTest");
FEditorPlusPath::RegisterChildPath(node, "<SubMenu>Sub/<Separator>Sep");
```

Supprimer un chemin

```cpp
FEditorPlusPath::UnregisterPath("/MenuTest/SubMenu1/SubMenu1/Path1");
```

Étendre la barre d'outils
```cpp
FEditorPlusPath::RegisterPath("/<Hook>ProjectSettings/<ToolBar>MenuTestToolBar")
->Content({
    EP_NEW_MENU(FEditorPlusCommand)("ToolBarCommand1")
    ->BindAction(...)
});
```

###Description de l'interface

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

- `RegisterPath`: Créer un menu de chemins
- `RegisterPathAction`: Create a path menu and automatically bind an operation to the end `<Command>` node.
`RegisterChildPath`：Pour générer des sous-chemins pour un nœud spécifié.
`RegisterChildPathAction`：CreateChildPathAction pour générer automatiquement des sous-chemins à partir du nœud spécifié et lier l'action
- `UnregisterPath`: Supprimer le chemin. `Leaf` permet de spécifier une correspondance stricte lorsque plusieurs nœuds terminaux portent le même nom. Lors de la suppression, les nœuds intermédiaires seront remontés, et un nœud intermédiaire sera également supprimé s'il ne contient plus aucun enfant.
- `GetNodeByPath`: Obtenir le nœud par le chemin


Type de nœud

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

Pour plus d'exemples et d'explications sur les interfaces, veuillez consulter le code source [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)，Test cases [MenuTest.cpp](https://github.com/disenone/UE.EditorPlus/blob/ue5.3/Source/EditorPlusTools/Private/MenuTest/MenuTest.cpp)


###Gestion modulaire

UE.EditorPlus offre également un cadre de gestion modulaire pour le menu des extensions, prenant en charge le chargement et le déchargement automatiques des menus d'extension lors du chargement et du déchargement des plugins.

Faites en sorte que la classe du menu hérite de `IEditorPlusToolInterface` et remplacez les fonctions `OnStartup` et `OnShutdown`. `OnStartup` est responsable de la création du menu, tandis que `OnShutdown` appelle la fonction `Destroy` des nœuds pour nettoyer le menu. Lorsque le nombre de références du nœud tombe à 0, un nettoyage automatique est effectué.

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

La classe de gestion de menu hérite de `IEditorPlusToolManagerInterface` et remplace la fonction `AddTools`, pour y ajouter la classe de menu.

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

Lors du chargement et du déchargement des plugins, les fonctions `StartupTools` et `ShutdownTools` de la classe de gestion sont respectivement appelées.

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

Une fois ces adaptations terminées, le menu des extensions sera automatiquement chargé et déchargé lors de l'activation et de la désactivation des plugins.


##Outil d'édition

UE.EditorPlus offers a range of practical editor tools.

##Créer une fenêtre d'édition

Avec EditorPlus, il est facile de créer une nouvelle fenêtre d'édition.

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

ClassBrowser is a UE Class viewer, opened through the menu EditorPlusTools -> ClassBrowser.

![](assets/img/2024-ue-editorplus/classbrowser_menu.png)

![](assets/img/2024-ue-editorplus/classbrowser.png)

Basé sur le reflet d'UE, il est facile de consulter les informations des différents types de membres de l'UE, y compris les indications et les conseils, avec prise en charge de la recherche floue et la possibilité d'accéder aux informations de la classe parent.

### MenuCollections

MenuCollections is a menu command quick search and collection tool that can help you quickly find the menu commands you need to execute and can bookmark frequently used commands to enhance efficiency.

![](assets/img/2024-ue-editorplus/menucollection_find.png)

![](assets/img/2024-ue-editorplus/menucollection_star.png)


### SlateResourceBrowser

SlateResourceBrowser est un outil qui permet de visualiser rapidement les ressources Slate UI, vous aidant ainsi à parcourir et trouver les ressources de l'éditeur dont vous avez besoin, facilitant ainsi l'extension de l'éditeur.

![](assets/img/2024-ue-editorplus/slateresourcebrowser_color.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_icon.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_font.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_widgetstyle.png)

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez [**donner votre avis**](https://github.com/disenone/wiki_blog/issues/new)Signalez toute omission. 
