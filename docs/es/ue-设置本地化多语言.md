---
layout: post
title: UE (Unreal Engine) permite la configuración de localización y soporte para
  múltiples idiomas.
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: Registrar cómo implementar la localización y el soporte de varios idiomas
  en UE.
---

<meta property="og:title" content="UE 设置本地化多语言" />

#UE Configuración de localización multilingüe

> # Cómo implementar la localización multilingüe en UE

En este documento se registrarán los pasos para lograr la localización multilingüe en UE.

## Paso 1: Preparación del proyecto

Antes de comenzar con la implementación de la localización multilingüe, es importante asegurarse de que el proyecto esté configurado correctamente. Asegúrese de que se hayan instalado los paquetes de idioma necesarios y de que el proyecto esté configurado para admitir múltiples idiomas.

## Paso 2: Preparación de cadenas de texto

El siguiente paso es identificar todas las cadenas de texto en el proyecto que necesitan ser localizadas. Esto incluye elementos como mensajes de error, etiquetas de botones y texto de interfaz de usuario. Asegúrese de que todas estas cadenas de texto estén separadas y sean fácilmente accesibles para su traducción.

## Paso 3: Traducción de cadenas de texto

Una vez que todas las cadenas de texto estén identificadas y preparadas, es momento de proceder con su traducción. Contrate a un traductor profesional para que traduzca todas las cadenas de texto al idioma deseado. Asegúrese de mantener una comunicación clara y precisa con el traductor para garantizar una traducción de alta calidad.

## Paso 4: Implementación de las traducciones

Una vez que las cadenas de texto hayan sido traducidas al idioma deseado, es momento de implementar las nuevas traducciones en el proyecto. Esto generalmente implica reemplazar las cadenas de texto originales con las traducidas en el código o archivos de recursos correspondientes.

## Paso 5: Prueba y revisión

Después de implementar las traducciones, asegúrese de realizar pruebas exhaustivas para garantizar que todo funcione correctamente. Realice un análisis en profundidad de cada parte del proyecto para verificar la precisión y coherencia de las traducciones.

## Paso 6: Mantenimiento continuo

La localización multilingüe es un proceso continuo. Asegúrese de tener un sistema en marcha para mantener y actualizar las traducciones a medida que el proyecto evoluciona. Realice revisiones regulares y responda a los comentarios de los usuarios para mejorar y refinar aún más la experiencia multilingüe.

¡Listo! Siguiendo estos pasos, podrá implementar con éxito la localización multilingüe en su proyecto de UE.

Si no estás familiarizado con el menú de extensión de UE, te recomendaría echar un vistazo rápido a: [Menu de Editor de Extensión de UE](ue-扩展编辑器菜单.md), [ue-Usar la forma de ruta extendida para expandir el menú](ue-使用路径形式扩展菜单.md)

This text is based on the plugin: [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##**Funcionalidad**

-

UE 自带工具可以实现本地化多语言，譬如我们可以为编辑器菜单实现本地化：

Las herramientas incorporadas de UE permiten la localización multilingüe, por ejemplo, podemos localizar el menú del editor.

Menú en chino:

![](assets/img/2023-ue-localization/chinese.png)

**Menú en inglés:**



![](assets/img/2023-ue-localization/english.png)

### Código de Declaración


Para lograr la localización del menú, necesitamos declarar explícitamente las cadenas que deben ser tratadas por UE en el código, utilizando las macrodefiniciones `LOCTEXT` y `NSLOCTEXT` proporcionadas por UE.

- Forma de definición global de archivos, primero se define una macro llamada `LOCTEXT_NAMESPACE`, cuyo contenido es el espacio de nombres actual donde se encuentra el texto multilingüe. Luego, se puede usar `LOCTEXT` para definir los textos en el archivo y, finalmente, se cancela la macro `LOCTEXT_NAMESPACE`.

```cpp
// #define LOCTEXT(InKey, InTextLiteral)

#define LOCTEXT_NAMESPACE "EditorPlusTools"
LOCTEXT("Key", "Content");
#undef LOCTEXT_NAMESPACE

```

- La forma de definir localmente, utilizando `NSLOCTEXT`, es añadir el espacio de nombres como parámetro al definir el texto:

```cpp
// #define NSLOCTEXT(InNamespace, InKey, InTextLiteral)

NSLOCTEXT("EditorPlusTools", "Key", "Content");
```

UE 工具通过查找宏 `LOCTEXT` 和 `NSLOCTEXT` 的出现来收集出所有需要翻译的文本。

##**Usar una herramienta de traducción para traducir el texto**

Supongamos que tenemos el siguiente código definiendo un texto:

```cpp
#define LOCTEXT_NAMESPACE "EditorPlusTools"
// register path node loctext
FEditorPlusPath::GetNodeByPath("/MenuTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/<Hook>Help/<MenuBar>MenuTest/<SubMenu>SubMenu1/<Section>Section1")->SetFriendlyName(LOCTEXT("Section1", "Section1"))->SetFriendlyTips(LOCTEXT("Section1Tips", "Section1Tips"));
#undef LOCTEXT_NAMESPACE
```

Primero, abre la herramienta de traducción y ve a la configuración del editor mediante `Editar - Preferencias del editor`. Luego, activa la opción `General - Funciones experimentales - Herramientas - Selector de traducción`.

![](assets/img/2023-ue-localization/editor_enable_tool.png)


Luego abre la herramienta de traducción `Herramientas - Panel de localización`:

![](assets/img/2023-ue-localization/editor_open_tool.png)

Crea un nuevo objetivo (puede ser debajo de "Game" por defecto, pero crear uno nuevo es para facilitar la gestión y el movimiento de estos textos de traducción).

![](assets/img/2023-ue-localization/tool_new_target.png)

Configurar los parámetros del objetivo, cambio el nombre aquí a `EditorPlusTools`, cargar la política es `Editor`, recopilar desde el texto y agregar el directorio de complementos, las dependencias del objetivo son `Engine, Editor`, mantener las demás configuraciones sin cambios:

![](assets/img/2023-ue-localization/tool_target_config.png)

Agregar idiomas para garantizar que haya dos opciones: chino simplificado (zh-Hans) e inglés (en). Asegúrate de que al pasar el ratón por encima de cada idioma se muestren correctamente sus respectivos códigos ("zh-Hans" y "en"). Selecciona el idioma inglés, ya que en nuestro código utilizamos texto en inglés y necesitamos recopilar esas cadenas.

![](assets/img/2023-ue-localization/tool_target_lang.png)

Haz clic para recopilar el texto:

![](assets/img/2023-ue-localization/tool_target_collect.png)

Se desplegará el cuadro de diálogo de recopilación. Espere a que la recopilación sea exitosa, se mostrará una marca de verificación verde.

![](assets/img/2023-ue-localization/tool_target_collected.png)

Apaga el cuadro de progreso de la recolección y regresa a la herramienta de traducción. Ahí podrás ver que en la línea de texto en inglés aparece la cantidad de elementos recolectados. No es necesario traducir el texto en inglés en sí mismo. Haz clic en el botón de traducción en la línea de texto en chino:

![](assets/img/2023-ue-localization/tool_go_trans.png)

Abra la ventana y podrá ver un campo sin traducir con contenido. En el lado derecho del texto en inglés, ingrese el contenido traducido. Después de completar todas las traducciones, guarde y cierre la ventana.

![](assets/img/2023-ue-localization/tool_trans.png)

Haga clic para contar palabras y, al finalizar, verá que en la columna de Chino aparece la cantidad de traducciones realizadas:

![](assets/img/2023-ue-localization/tool_count.png)

**Título**: Último texto compilado:

**Traducción**:


![](assets/img/2023-ue-localization/tool_build.png)

Los datos traducidos se guardarán en `Content\Localization\EditorPlusTools`, con una carpeta por cada idioma. Dentro de la carpeta `zh-Hans` encontrarás dos archivos. `.archive` contiene los textos recopilados y traducidos, mientras que `.locres` es la información compilada después de la traducción.

![](assets/img/2023-ue-localization/tool_ret.png)

![](assets/img/2023-ue-localization/tool_ret2.png)

##Coloca el texto traducido en el directorio de complementos.

Nosotros hemos colocado el texto de traducción generado por encima en el directorio del proyecto, ahora necesitamos mover esos textos dentro del complemento para que pueda ser publicado junto al complemento y sea más conveniente.

Mueva la carpeta `Content\Localization\EditorPlusTools` dentro del directorio de complementos `Content`, en mi caso sería `Plugins\UE.EditorPlus\Content\Localization\EditorPlusTools`.

Modificar el archivo de configuración del proyecto `DefaultEditor.ini` y agregar la nueva ruta:

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```

De esta manera, una vez que los demás proyectos obtengan el complemento, simplemente necesitarán modificar `DefaultEditor.ini` para poder utilizar el texto traducido, sin necesidad de configurar la traducción nuevamente.

##**注**：Esta traducción está en chino, no en español. El texto original no necesita ser traducido.

En el proceso de generación de datos para la traducción, hemos encontrado algunos problemas. A continuación, se resumen los puntos a tener en cuenta:

Dentro del código, es necesario utilizar las macros `LOCTEXT` y `NSLOCTEXT` para definir el texto, y este debe ser una constante de cadena de caracteres, de esta manera UE lo recolectará.
- El nombre del objetivo de traducción no puede contener los caracteres `.`. Los nombres de directorio en `Content\Localization\` no pueden contener `.` ya que UE solo tomará el nombre antes del `.`. Esto podría resultar en una falla en la lectura de los textos traducidos por parte de UE debido a errores en los nombres.
- Para los complementos del editor, necesitamos verificar si estamos en modo de línea de comandos `IsRunningCommandlet()` y en ese caso no generar los menús y SlateUI, ya que en modo de línea de comandos no se carga el módulo Slate, lo que podría resultar en un error al recopilar texto `Assertion failed: CurrentApplication.IsValid()`. Si también te encuentras con un error similar, puedes intentar agregar esta verificación. Aquí está la información específica del error:

    > Assertion failed: CurrentApplication.IsValid() [File:E:\UE\ue5.3_git\Engine\Source\Runtime\Slate\Public\Framework\Application\SlateApplication.h] [Line: 255] 

    ![](assets/img/2023-ue-localization/tool_error.png)

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
