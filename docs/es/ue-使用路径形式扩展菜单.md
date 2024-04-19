---
layout: post
title: UE utiliza la extensión de menú en forma de ruta.
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
---

<meta property="og:title" content="UE 使用路径形式扩展菜单" />

> ### Cómo implementar menús de extensión en forma de ruta en UE

En este tutorial se explicará cómo implementar menús de extensión en forma de ruta en Unreal Engine (UE). 

Cada paso será detallado para que puedas entender el proceso correctamente. 

¡Comencemos!

Si no estás familiarizado con el menú de extensiones de UE, te recomiendo que eches un vistazo rápido a: [Menú de edición de extensiones de UE](ue-扩展编辑器菜单.md)

Este texto está basado en el complemento: [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##**节点管理**

Organiza el menú siguiendo la estructura de un árbol, donde los nodos padres pueden contener hijos:

```cpp
class EDITORPLUS_API FEditorPlusMenuBase: public TSharedFromThis<FEditorPlusMenuBase>
{
protected:
	// sub menus
	TArray<TSharedRef<FEditorPlusMenuBase>> Children;
}
```

En el momento de crear el nodo padre, crea también el nodo hijo:

```cpp
void FEditorPlusMenuBase::Register(FMenuBuilder& MenuBuilder)
{
	for (const auto Menu: Children)
	{
		Menu->Register(MenuBuilder);
	}
}
```

Por supuesto, el comportamiento específico de creación de cada nodo puede variar un poco, se sobrescribe una función virtual para implementarlo:

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

##Through the creation of nodes via paths.

De acuerdo con la estructura en forma de árbol, organiza el menú de manera adecuada y el formato de la ruta puede definir la estructura en forma de árbol de un menú.

```cpp
"/<Hook>Help/<MenuBar>BarTest/<SubMenu>SubTest/<Command>Action"
```

La línea anterior define la creación de una serie de menús:

- `<Hook>Help`: Posicionado después del menú con el nombre de Hook Help.
- `<MenuBar>BarTest`: Crea un menú de tipo Barra de Menú con el nombre BarTest.
- `<SubMenu>SubTest`: Crea un subnodo de tipo SubMenu con el nombre SubTest.
- `<Command>Action`：Finalmente crear un comando

La forma de llamar a la interfaz puede ser muy simple:

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

##Crear nodos con formas personalizadas

Aún mantenemos el método engorroso para crear menús, que permite una configuración más detallada. La forma de organizar el código se asemeja a la escritura de UE's SlateUI:

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

##**混合形式**

*Traducción al español*

**Forma mixta**

Por supuesto, tanto la forma de la ruta original como el menú generado personalizado son iguales, se pueden combinar libremente y son muy flexibles:

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

**多个地方定义的菜单，会合并到同一个树形结构中，名字相同的节点会认为是同一个节点。换言之，路径是唯一的，同一个路径可以唯一确定一个菜单节点。**

Varios menús definidos en diferentes lugares se fusionarán en una única estructura de árbol, los nodos con el mismo nombre se considerarán como el mismo nodo. En otras palabras, el camino es único, un mismo camino puede determinar de manera única un nodo de menú.
Entonces también podemos localizar los nodos y hacer algunos ajustes y modificaciones:

```cpp
// set Name and Tips
FEditorPlusPath::GetNodeByPath("/<MenuBar>BarTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
