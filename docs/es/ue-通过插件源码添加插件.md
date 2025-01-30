---
layout: post
title: UE agrega plugins a través del código fuente del plugin
date: 2023-12-01
categories:
- c++
- ue
catalog: true
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: Registrar de manera sencilla cómo añadir un plugin a UE teniendo el código
  fuente del plugin.
figures: []
---

<meta property="og:title" content="UE 通过插件源码添加插件" />

#UE agrega plugins a través del código fuente del plugin.

#Añadir complemento.

> Simplemente registra cómo agregar un complemento cuando tienes el código fuente del complemento.

con el plugin [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)Por favor, indica más contexto para poder proporcionarte una traducción precisa.

Coloque el código fuente en el directorio Plugins.
Modifica el archivo .uproject del proyecto añadiendo lo siguiente en el campo Plugins (puede omitirse este paso):
    ```json
        "Plugins": [
        {
            "Name": "EditorPlus",
            "Enabled": true,
            "TargetAllowList": [
                "Editor"
            ]
        }
    ```
Haz clic derecho en el archivo uproject, selecciona "Generar archivos del proyecto de Visual Studio" y actualiza el archivo del proyecto sln.
- Abre el archivo sln y compila el proyecto.

#Establecer idiomas múltiples.

Modifica el archivo de configuración del proyecto `DefaultEditor.ini`, añadiendo la nueva ruta:

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```


--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor [**反馈**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
