---
layout: post
title: UE Editor Plugin UE.EditorPlus Documento de Instrucciones
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
description: 'Traduce estos textos al idioma español:


  UE 编辑器插件  UE.EditorPlus 说明文档'
---

<meta property="og:title" content="UE 编辑器插件 EditorPlus 说明文档" />

#UE Editor Plugin UE.EditorPlus Documento de Instrucciones

##Presentación en video

![type:video](assets/img/2024-ue-editorplus/market/video.mp4)

##Código fuente del plugin

[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Descarga de la tienda

[EditorPlus](https://www.unrealengine.com/marketplace/zh-CN/product/editorplus)

##Proyecto agregar plugin de código fuente EU.EditorPlus

Documento de referencia:

- Español: [Agregar un complemento a través del código fuente del complemento en UE.](https://wiki.disenone.site/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)
- English: [UE adds plugins through the plugin source code](https://wiki.disenone.site/en/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)


##Descripción del complemento

UE.EditorPlus es un complemento para el editor de UE que ofrece una forma conveniente de ampliar el menú del editor, además de soportar métodos avanzados para la expansión, incluyendo algunas herramientas útiles para el editor. Este complemento es compatible con UE5.3+.


##Extender el menú del editor

![](assets/img/2024-ue-editorplus/menu.png)

![](assets/img/2024-ue-editorplus/toolbar.png)

###Explicación

Apoyo para ampliar el menú del editor de varias formas:

- Método de ruta: `RegisterPathAction("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action")`
Forma de instanciar: `EP_NEW_MENU(FEditorPlusMenuBar)("Bar")`
- Método de mezcla: `RegisterPath("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",EP_NEW_MENU(FEditorPlusCommand)("Action")`

###método de ruta

Puedes registrar un comando de menú del editor de esta manera:

```cpp
FEditorPlusPath::RegisterPathAction(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",
    FExecuteAction::CreateLambda([]
        {
            // do action
        })
);
```

De esta manera, se puede agregar una barra de menú llamada Bar detrás de la opción Help en la barra de menús del editor. Dentro de Bar, se puede incluir un submenú llamado SubMenu, y en SubMenu se puede añadir un comando llamado Action.

El formato completo de la ruta sería el siguiente: `/<Hook>HookName/<Type1>Name1/<Type2>Name2`, la primera ruta debe ser `<Hook>`, tipos y restricciones actualmente soportados:

- `<Hook>`: Indica en qué posición del gancho se debe generar el menú. No debe haber ningún `<Hook>` en la ruta posterior.
- `<MenuBar>`: barra de menú, la ruta posterior no puede contener `<Hook>, <MenuBar>, <ToolBar>`
- `<ToolBar>`: Barra de herramientas, no se permite tener `<Hook>, <MenuBar>, <ToolBar>` en el camino posterior.  
- `<Section>`: Sección del menú, después de este camino no puede haber `<Hook>, <MenuBar>, <Section>`
- `<Separator>`: Separador de menú, la ruta posterior no puede contener `<Hook>, <MenuBar>`
- `<SubMenu>`: Submenú, no puede contener los siguientes elementos en su ruta `<Hook>, <MenuBar>`
- `<Command>`: comando del menú, no puede llevar ninguna ruta después.
- `<Widget>`: Componentes de interfaz de usuario de Slate con más opciones de personalización y extensibilidad, sin ninguna ruta posterior.

Una forma de ruta más sencilla: `/BarName/SubMenuName1/SubMenuName2/CommandName`, si no se especifica el tipo, el primer elemento de la ruta por defecto es `<MenuBar>`, el del medio es `<SubMenu>` y el último es `<Command>`.

Si no se especifica `<Hook>`, se agrega automáticamente al principio `<Hook>Help`, lo que indica que se debe añadir una barra de menú después del menú Ayuda.

###Forma de instanciar

El modo de ruta instancia automáticamente todos los nodos según su tipo y parámetros por defecto. También podemos controlar la instancia nosotros mismos, lo que nos permite tener un control más detallado sobre el contenido de la extensión.

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

Al instanciar `MyBar`, se puede pasar el nombre del Hook, el nombre localizado y el parámetro de sugerencia localizado (`"MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips")`). El código anterior es equivalente a la forma de ruta `/<Hook>Help/<MenuBar>MyBar/<SubMenu>MySubMenu/<Command>MyAction`.

###Método de mezcla.

Por supuesto, también se pueden combinar de dos maneras.

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

En este caso, el plugin instanciará automáticamente los nodos del camino intermedio, y el camino final utilizará los nodos instanciados por el propio usuario.

###Más casos de uso

Archivo de cabecera:

```cpp
#include <EditorPlusPath.h>
```

La especificación del idioma local a través de la ruta, `EP_FNAME_HOOK_AUTO`, indica que se utilizará automáticamente el nombre de la ruta como nombre del `Hook`:

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

Obtener nodos a través de la ruta y establecer texto localizado:

```cpp
FEditorPlusPath::GetNodeByPath("/MenuTest")
    ->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))
    ->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


Agregar un componente de interfaz de usuario Slate al final de la ruta.

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Widget>Widget",
    EP_NEW_MENU(FEditorPlusWidget)("Widget", LOCTEXT("Widget", "Widget"))
        ->BindWidget(SNew(SHorizontalBox)));
);
```

Añadir un nuevo nodo en el Hook incorporado de la UE.

```cpp
FEditorPlusPath::RegisterPath("<Hook>EpicGamesHelp/<Separator>ExtendSeparator")
```

Repetir varias veces la misma ruta hace que se reconozca como la misma ruta, lo que permite expandirla continuamente.

```cpp
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path1", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path1", "Path1"), LOCTEXT("Path1Tips", "Path1Tips"));
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path2", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path2", "Path2"), LOCTEXT("Path2Tips", "Path2Tips"));
```

Ampliar el camino para un nodo.

```cpp
auto node = FEditorPlusPath::GetNodeByPath("/MenuTest");
FEditorPlusPath::RegisterChildPath(node, "<SubMenu>Sub/<Separator>Sep");
```

Eliminar una ruta

```cpp
FEditorPlusPath::UnregisterPath("/MenuTest/SubMenu1/SubMenu1/Path1");
```

Extender la barra de herramientas
```cpp
FEditorPlusPath::RegisterPath("/<Hook>ProjectSettings/<ToolBar>MenuTestToolBar")
->Content({
    EP_NEW_MENU(FEditorPlusCommand)("ToolBarCommand1")
    ->BindAction(...)
});
```

###Descripción de la interfaz

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

- `RegisterPath`: menú de generación de rutas
- `RegisterPathAction`: genera un menú de ruta y vincula automáticamente la operación para el nodo `<Command>` final.
`RegisterChildPath`: Generar caminos secundarios para el nodo especificado.
- `RegisterChildPathAction`: Continúa generando subrutas para el nodo especificado y vincula automáticamente la operación.
`UnregisterPath`: Elimina la ruta. "Leaf" se utiliza para especificar una coincidencia estricta cuando hay múltiples nodos finales con el mismo nombre. Durante el proceso de eliminación, se retrocederá en los nodos intermedios y si un nodo intermedio no tiene hijos también será eliminado.
- `GetNodeByPath`: Obtener nodo por ruta


Tipo de nodo

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

Para más ejemplos y la descripción de las interfaces, consulte el código fuente [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)，caso de prueba [MenuTest.cpp](https://github.com/disenone/UE.EditorPlus/blob/ue5.3/Source/EditorPlusTools/Private/MenuTest/MenuTest.cpp)


###Gestión modular

UE.EditorPlus también proporciona un marco de gestión modular para el menú de extensiones, que soporta la carga y descarga automática del menú de extensiones al cargar y descargar complementos.

Haz que la clase del menú herede de `IEditorPlusToolInterface` y sobrescribe las funciones `OnStartup` y `OnShutdown`. `OnStartup` se encarga de crear el menú, `OnShutdown` llama a la función `Destroy` del nodo para limpiar el menú. Cuando la cantidad de referencias al nodo es 0, se realiza la limpieza automáticamente.

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

La clase de gestión de menús hereda de `IEditorPlusToolManagerInterface` y sobrescribe la función `AddTools`, añadiendo la clase del menú dentro de `AddTools`.

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

Se llaman las funciones `StartupTools` y `ShutdownTools` de la clase de gestión al cargar y descargar el complemento, respectivamente.

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

Una vez completada la adaptación anterior, se podrán cargar y descargar automáticamente los menús de extensiones al cargar y descargar plugins.


##Herramienta del editor.

UE.EditorPlus también ofrece algunas herramientas de edición útiles.

##Crear ventana del editor.

Con EditorPlus, puedes crear fácilmente una nueva ventana de editor.

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

`SClassBrowserTab` es un control UI personalizado.

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

ClassBrowser es un visor de clases de UE, que se puede abrir a través del menú EditorPlusTools -> ClassBrowser.

![](assets/img/2024-ue-editorplus/classbrowser_menu.png)

![](assets/img/2024-ue-editorplus/classbrowser.png)

Basado en la reflexión de UE, resulta fácil visualizar la información de los diferentes tipos de miembros de UE, incluyendo descripciones y sugerencias, con soporte para búsquedas difusas y la capacidad de abrir la información de la clase padre.

### MenuCollections

MenuCollections es una herramienta de búsqueda y organización rápida de comandos de menú que te ayuda a localizar rápidamente los comandos de menú que necesitas ejecutar, y también te permite guardar los comandos más utilizados para aumentar la eficiencia.

![](assets/img/2024-ue-editorplus/menucollection_find.png)

![](assets/img/2024-ue-editorplus/menucollection_star.png)


### SlateResourceBrowser

SlateResourceBrowser es una herramienta que te permite visualizar rápidamente los recursos de la interfaz de usuario de Slate, ayudándote a navegar y encontrar los recursos del editor que necesitas, facilitando así la expansión del editor.

![](assets/img/2024-ue-editorplus/slateresourcebrowser_color.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_icon.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_font.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_widgetstyle.png)

--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor [**反馈**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
