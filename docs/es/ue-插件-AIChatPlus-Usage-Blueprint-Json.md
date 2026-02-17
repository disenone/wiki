---
layout: post
title: Operaciones con Json
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
- AI Chat
- Chatbot
- Image Generation
- OpenAI
- Azure
- Claude
- Gemini
- Ollama
- Json
- Blueprint
description: Operaciones con Json
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Json 操作" />

#Capítulo del Plano Maestro - Operaciones con Json

<!-- Se necesita imagen: mostrar una descripción general de todos los nodos relacionados con Json, incluyendo los nodos bajo las categorías JsonObject, JsonArray y JsonLibrary -->
![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_all.png)

##Resumen

AIChatPlus ofrece soporte completo para operaciones con esquemas JSON, facilitando el manejo de datos JSON en los esquemas. Principalmente incluye tres clases:

* **UAIChatPlus_JsonObject**: Clase de operación de objetos JSON, utilizada para manejar JSON en formato `{}`.
* **UAIChatPlus_JsonArray**: Clase de operación de arreglos JSON, utilizada para manejar JSON en formato `[]`.
* **UAIChatPlus_JsonLibrary**: Biblioteca de utilidades JSON, proporciona funciones de utilidad estáticas.

Estas clases admiten:
* Crear, analizar, serializar JSON
* Leer y establecer valores de campo
* Consulta de rutas anidadas
* Conversión entre JSON y USTRUCT
* Lectura y escritura de archivos
* Encadenamiento de métodos

##Operaciones básicas de JsonObject

###Crear JsonObject

Usa `Create Json Object` para crear un objeto JSON vacío:

<!-- Necesita imagen: captura de pantalla que muestre la búsqueda con clic derecho en el plano de "Create Json Object" y la creación del nodo -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_create_1.png)

###Analizar desde la cadena

Usar `Parse Json Object` para crear un objeto desde una cadena JSON:

<!-- Se necesita imagen: mostrar el nodo Parse Json Object, ingresar una cadena JSON como '{"name":"test","value":123}', y mostrar las salidas JsonObject, bSuccess, ErrorMessage -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_parse_1.png)

###Establecer el valor del campo

JsonObject ofrece varios métodos Set que admiten llamadas en cadena:

| Función | Descripción |
|-----|------|
| `Establecer Campo de Cadena` | 设置字符串字段 |
| `Establecer Campo Numérico` | Configurar campo de número de punto flotante |
| `Establecer Campo Entero` | Configurar campo de número entero |
| `Set Boolean Field` | Establecer campo booleano |
| `Establecer campo de objeto` | Configurar campo de objeto anidado |
| `Establecer campo de matriz` | Configurar campo de matriz |
| `Establecer Campo Nulo` | Configurar campo como nulo |

<!-- Necesita imagen: muestra un diagrama de flujo de configuración de múltiples campos encadenados, como Crear Objeto Json -> Establecer Campo String("nombre", "jugador1") -> Establecer Campo Entero("nivel", 10) -> Establecer Campo Booleano("activo", verdadero) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_set_1.png)

###Obtener el valor del campo

JsonObject ofrece varios métodos Get:

| Función | Descripción |
|-----|------|
| `Get String Field` | Obtener campo de cadena |
| `Get Number Field` | Obtener campo numérico flotante |
| `Obtener Campo Entero` | 获取整数字段 |
| `Get Boolean Field` | Obtener campo booleano |
| `Obtener Campo del Objeto` | Obtener campo de objeto anidado |
| `Get Array Field` | Obtener campo de array |

Aquí está la traducción al español del texto proporcionado:

<!-- Se necesita una imagen: muestra el diagrama de flujo para obtener valores de campos desde JsonObject, usando Get String Field para el campo "name", mostrando los parámetros DefaultValue y bSuccess -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_get_1.png)

###Comprobación de campos

| Función | Descripción |
|-----|------|
| `Tiene Campo` | Verifica si el campo existe |
| `Get Field Type` | Obtener tipo de campo |
| `Get Field Names` | Obtener todos los nombres de campo |
| `Remove Field` | Eliminar campo |
| `Clear` | Borrar todos los campos |

<!-- Se necesita imagen: que muestre el uso de Has Field para verificar la existencia de un campo y Get Field Type para obtener el tipo de campo en un diagrama de flujo -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_check_1.png)

###Serializar a cadena

Utilizar `To Json String` para convertir JsonObject en una cadena de texto:

<!-- Se necesita imagen: muestra el nodo To Json String, entrada JsonObject, parámetro bPrettyPrint, salida cadena JSON formateada -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_tostring_1.png)

##Operaciones básicas de JsonArray

###Crear JsonArray

Usar `Create Json Array` para crear un arreglo JSON vacío:

<!-- Se necesita imagen: captura de pantalla que muestre la creación del nodo Create Json Array en el plano -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_create_1.png)

###Agregar elemento

JsonArray proporciona varios métodos Add, compatibles con llamadas en cadena:

| Función | Descripción |
|-----|------|
| `Add String` | Agregar elemento de cadena |
| `Add Number` | Agregar elemento de número flotante |
| `Add Integer` | Agregar elemento entero |
| `Add Boolean` | Añadir elemento booleano |
| `Add Object` | Añadir objeto |
| `Add Array` | Añadir elemento de matriz |
| `Add Null` | Añadir elemento nulo |

<!-- Se necesita imagen: Mostrar un esquema de llamadas encadenadas para agregar múltiples elementos, como Crear Matriz Json -> Agregar Cadena("a") -> Agregar Cadena("b") -> Agregar Entero(123) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_add_1.png)

###Obtener elemento

JsonArray proporciona métodos para obtener elementos por índice:

| Función | Descripción |
|-----|------|
| `Get String` | Obtener elemento de cadena |
| `Obtener Número` | Obtener elemento de número flotante |
| `Obtener Entero` | Conseguir elemento entero |
| `Get Boolean` | Obtener elemento booleano |
| `Obtener Objeto` | Obtener elemento del objeto |
| `Obtener Array` | Obtener elementos del array |

<!-- Se necesita imagen: mostrar el plano de cómo usar Get Object por índice para obtener elementos de objetos en un arreglo -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_get_1.png)

###Operaciones con arreglos

| Función | Descripción |
|-----|------|
| `Length` | Obtener la longitud del arreglo |
| `Es Índice Válido` | Comprobar si el índice es válido |
| `Obtener Tipo de Elemento` | Obtener tipo de elemento |
| `Remove At` | Eliminar el elemento en el índice especificado |
| `Clear` | Vaciar arreglo |

<!-- Se necesita una imagen: mostrar el uso de Length para obtener la longitud de un arreglo, junto con un For Loop para recorrer el arreglo en el plano -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_loop_1.png)

###Conversión por lotes

JsonArray admite la conversión masiva con arrays de UE:

| Función | Descripción |
|-----|------|
| `Desde Arreglo de Cadenas` | Crear a partir de un arreglo de cadenas |
| `To String Array` | Convertir a matriz de cadenas |
| `Desde Arreglo de Enteros` | Crear a partir de un arreglo de enteros |
| `To Integer Array` | Convertir a matriz de enteros |

<!-- Se necesita imagen: ejemplo de uso que muestre From String Array y To String Array -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_batch_1.png)

##Consulta de ruta

JsonObject admite el acceso a datos anidados mediante rutas separadas por puntos, como `player.inventory.gold`.

###Obtener valor por ruta

Obtener el valor de cadena mediante la ruta utilizando `Get String By Path`:

```json
{
    "player": {
        "name": "Hero",
        "inventory": {
            "gold": 1000
        }
    }
}
```

<!-- Se necesita imagen: mostrar el uso del nodo Get String By Path, con la Path configurada como "player.name", obteniendo el valor anidado en el diagrama de flujo -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_get_1.png)

###Establecer valor por ruta

Usar `Set String By Path` para establecer valores por ruta:

<!-- Se necesita imagen: mostrar un blueprint utilizando el nodo Set String By Path para establecer valores de rutas anidadas, mostrando el parámetro FAIChatPlus_JsonPathOptions (bCaseSensitive, bCreateMissing) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_set_1.png)

###Resultados de la consulta

La consulta de ruta devuelve la estructura `FAIChatPlus_JsonQueryResult`, que incluye:

* **bSuccess**: Consulta si fue exitosa
* **ValueType**: Tipo del valor de retorno
* **ErrorMessage**: Mensaje de error (si falla)

<!-- Se necesita imagen: mostrar el nodo Break FAIChatPlus_JsonQueryResult, mostrando los campos bSuccess, ValueType, ErrorMessage -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_result_1.png)

##JSON a USTRUCT Conversión

AIChatPlus permite la conversión entre JSON y USTRUCT, facilitando su uso con estructuras de planos gráficos.

###Cadena JSON a USTRUCT

Utilizar `Json String To Struct` para convertir directamente una cadena JSON en USTRUCT:

<!-- Se necesita imagen: mostrar el nodo Json String To Struct, con entrada de cadena JSON y salida conectada a una variable USTRUCT personalizada (por ejemplo, FAIChatPlus_OpenAIChatRequestOptions) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_1.png)

###USTRUCT a cadena JSON

Usar `Struct To Json String` para convertir USTRUCT a una cadena JSON:

<!-- Se necesita una imagen: mostrar el nodo Struct To Json String, ingresar una variable USTRUCT, el parámetro bPrettyPrint, y generar una cadena JSON -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_2.png)

###JsonObject a USTRUCT

Utilizando el método `To Struct` de JsonObject:

<!-- Se necesita imagen: mostrar el uso del nodo To Struct de JsonObject -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_3.png)

###USTRUCT a JsonObject

Utiliza el método estático `From Struct` para crear un JsonObject desde un USTRUCT:

# <!-- Imagen necesaria: mostrando el nodo From Struct, entrada USTRUCT, salida JsonObject -->

Nota: Solo traduje el texto proporcionado, manteniendo los comentarios HTML y el formato tal como fue solicitado. La parte que comienza con "#" es un comentario en formato Markdown que indica la necesidad de una imagen.
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_4.png)

##Funciones de utilidad JsonLibrary

`UAIChatPlus_JsonLibrary` ofrece una serie de funciones estáticas de utilidad.

###Creación rápida

| Función | Descripción |
|-----|------|
| `Crear Objeto Json Con Campo String` | Creación rápida de un JsonObject con un solo campo |
| `Make Json Object From String Map` | Crear JsonObject desde un Map |

<!-- Se necesita imagen: Mostrando el uso de Make Json Object From String Map, entrada TMap<FString, FString>, salida JsonObject en el diagrama de flujo -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_make_1.png)

###Verificación

| Función | Descripción |
|-----|------|
| `Validar Cadena Json` | Verificar si la cadena JSON es válida |
| `Is Json Object` | Verificar si es un objeto JSON |
| `Es Arreglo Json` | Comprobar si es un arreglo JSON |

<!-- requiere imagen: muestra el esquema de validación de una cadena JSON utilizando Validate Json String -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_validate_1.png)

###Formatear

| Función | Descripción |
|-----|------|
| `Prettify Json` | Formatear JSON (añadir sangría y saltos de línea) |
| `Minificar Json` | Comprimir JSON (eliminar espacios en blanco) |

<!-- Se necesita imagen: muestra el uso de Prettify Json para formatear una cadena JSON, mostrando la entrada de JSON comprimido y la salida de JSON formateado -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_format_1.png)

###Operaciones de archivo

| Función | Descripción |
|---|---|
|-----|------|
| `Load Json Object From File` | Cargar Objeto Json Desde Archivo |
| `Guardar Objeto Json En Archivo` | Guardar JsonObject en archivo |
| `Cargar Arreglo Json Desde Archivo` | 从文件加载 JsonArray |
| `Guardar Matriz Json en Archivo` | Guardar JsonArray en archivo |

<!-- Se necesita imagen: mostrando ejemplos de uso de Guardar Objeto Json en Archivo y Cargar Objeto Json desde Archivo -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_file_1.png)

###Comparar

| Función | Descripción |
|-----|------|
| `Equals Json Object` | Compara si dos JsonObject son iguales |
| `Equals Json Array` | Compara si dos JsonArray son iguales |

<!-- Se necesita imagen: Mostrando el diagrama de flujo para comparar dos JsonObject utilizando Equals Json Object -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_compare_1.png)

###Consulta avanzada de rutas

Aquí está la traducción al español:

| Función | Descripción |
|-----|------|
| `Query String By Path` | Consultar cadena por ruta (admite índices de matriz, como `items[0].name`) |
| `Query Object By Path` | Consultar objeto por ruta |
| `Consultar Arreglo Por Ruta` | Consultar arreglo por ruta |

<!-- Necesita imagen: mostrar el uso de Query String By Path para consultar una ruta con índices de arreglo, como "data.items[0].name" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_query_1.png)

###Operaciones por lotes

| Función | Descripción |
|-----|------|
| `Establecer Campos de Cadena Desde Mapa` | Configuración masiva de campos de texto |
| `Obtener Campos de Cadena para Asignar` | Obtención masiva de campos de cadena |

<!-- Se necesita imagen: mostrando el esquema para establecer campos de cadena desde un mapa de manera masiva -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_batch_1.png)

##Otras operaciones

###Fusionar JsonObject

Usa el método `Merge` para combinar dos JsonObject:

<!-- Se necesita imagen: mostrar el nodo Merge, combinando dos JsonObject, mostrando el parámetro bOverwrite -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_merge_1.png)

###Copiar JsonObject

Usar el método `Duplicate` para copiar profundamente un JsonObject:

<!-- Se necesita imagen: mostrar el esquema de nodo Duplicate duplicando JsonObject -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_dup_1.png)

##Ejemplo de aplicación práctica

###Analizar la respuesta de la API

Extraer los parámetros de Tool Call desde la respuesta del chat de IA:

<!-- Se necesita imagen: mostrar un ejemplo completo de esquema de análisis: desde FunctionArguments String Parse hasta JsonObject, luego usar Get String Field para obtener el valor del parámetro -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_1.png)

###Construir parámetros de solicitud

Uso de JsonObject para construir parámetros de solicitud complejos:

<!-- Necesita imagen: mostrar un esquema de construcción de estructura JSON anidada, crear JsonObject configurando múltiples campos, incluyendo JsonObject y JsonArray anidados -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_2.png)

###Lectura y escritura de archivos de configuración

Cargar la configuración desde un archivo JSON, modificarla y guardarla:

Necesita imagen: mostrar el flujo completo de configuración de lectura/escritura: Cargar Objeto JSON desde Archivo -> Modificar campo -> Guardar Objeto JSON en Archivo  

Nota: El texto entre <!-- --> es un comentario en HTML, por lo que se ha mantenido en el idioma original. Sin embargo, he traducido la parte que describe el proceso dentro del comentario.  

Si prefieres que también se traduzcan los elementos dentro de los símbolos <!-- -->, quedaría así:  

<!-- Necesita imagen: mostrar el flujo completo de configuración de lectura/escritura: Cargar Objeto JSON desde Archivo -> Modificar campo -> Guardar Objeto JSON en Archivo -->  

Indícame cuál de las dos opciones prefieres para futuras traducciones.
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_3.png)

##Enumeración de tipos

El enumerado `EAIChatPlus_JsonValueType` define los tipos de valores JSON:

| Valor de enumeración | Descripción |
|-------|------|
| `None` | Tipo desconocido |
| `Null` | valor nulo |
| `String` | Cadena |
| `Number` | Número |
| `Boolean` | Booleano |
| `Array` | Arreglo |
| `Objeto` | Objeto |

<!-- Se necesita imagen: mostrar el diagrama de flujo que utiliza el nodo Switch para manejar diferentes tratamientos según JsonValueType -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_type_1.png)

--8<-- "footer_es.md"


> Este post está traducido usando ChatGPT, por favor proporciona tu [**retroalimentación**](https://github.com/disenone/wiki_blog/issues/new)Señalar cualquier omisión en la nota. 
