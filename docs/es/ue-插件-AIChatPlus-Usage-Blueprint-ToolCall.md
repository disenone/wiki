---
layout: post
title: Tool Call
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
- Tool Call
- Function Calling
description: Tool Call
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Tool Call" />

#Plan Maestro - Llamada a Herramientas

La llamada a herramientas (Tool Calling), también conocida como llamada a funciones (Function Calling), se refiere a la capacidad de los modelos avanzados para determinar, según el contexto de la conversación, si es necesario invocar herramientas o funciones externas con el fin de obtener información o realizar acciones. El modelo devolverá el nombre de la función a invocar y los parámetros correspondientes, permitiendo que los desarrolladores ejecuten la llamada real y luego devuelvan el resultado al modelo para continuar con el diálogo.

AIChatPlus soporta la función Tool Call en las siguientes plataformas:

* OpenAI
* Claude
* Gemini
* Ollama
* Servidor Cllama (servidor llama.cpp)

##Conceptos clave

###Definición de Herramienta

La definición de Tool incluye los siguientes campos clave:

* **Tipo**: Tipo de herramienta, actualmente solo se admite `Function`.
* **Nombre**: Nombre de la función, debe estar compuesto por letras de la a-z, A-Z, números del 0-9, guiones bajos o medios, con una longitud máxima de 64.
* **Descripción**: Descripción de la función, el modelo utilizará esta descripción para determinar cuándo llamar a la función.
* **Propiedades**: Lista de parámetros de la función, donde cada parámetro contiene atributos como Nombre, Descripción, Tipo, Obligatorio, etc.

###Proceso de Llamada a Herramienta

El proceso completo de Tool Call es el siguiente:

1. **Enviar solicitud**: Enviar una solicitud de chat a el modelo que incluya la definición de Herramientas
2. **Evaluación del modelo**: El modelo determina si es necesario invocar una herramienta basándose en el contenido del diálogo.
3. **Devolución de Tool Calls**: Si es necesario llamarlos, el modelo devuelve el nombre de la función y los parámetros a utilizar
4. **Ejecución de funciones**: Los desarrolladores realizan la llamada real a la función basándose en la información devuelta.
5. **Devolver resultado**: Enviar el resultado de la ejecución de la función como un nuevo mensaje al modelo.
6. **Continuar el diálogo**: El modelo genera la respuesta final basándose en el resultado de la función.

##Ejemplo de llamada a herramienta de OpenAI

A continuación, utilizaremos OpenAI como ejemplo para demostrar cómo usar la función Tool Call.

###1. Definición de Tool

Primero, crea la definición de la Herramienta. En este ejemplo, definimos una función `get_delivery_date` para obtener el tiempo de entrega de un paquete de mensajería.

<!-- Se necesita una imagen: mostrando la creación del nodo FAIChatPlus_ChatRequestTool, configurando Type=Function, Name="get_current_weather", Description="Obtener el clima actual en una ubicación determinada" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_1.png)

###2. Definir parámetros de Tool

Agregar Properties (parámetros) al Tool. En este ejemplo, se añade un parámetro `order_id`, de tipo `string`, configurado como obligatorio.

<!-- Se necesita imagen: mostrando la creación del nodo FAIChatPlus_ChatRequestToolProperty, configurando Name="location", Description="La ciudad y el estado, ej. San Francisco, CA", Type="string", Required=true, y conectándolo mediante Make Array al campo Properties de Tool -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_2.png)

###3. Configuración de Opciones

Crear el nodo `Opciones de Solicitud de Chat OpenAI`, configurar la clave API y el Modelo, y conectar el arreglo de Herramientas a las Opciones.

<!-- Se necesita imagen: muestra la creación del nodo OpenAI Chat Request Options, configurando ApiKey, Model="gpt-4o-mini", y conectando la herramienta anterior al campo Tools mediante Make Array -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_3.png)

###4. Crear Mensajes

Crear mensajes de usuario para consultar sobre paquetes de mensajería.

<!-- Se necesita imagen: muestra la creación del arreglo Messages, añadiendo un Mensaje de Usuario con el Contenido establecido como "¿Cómo está el clima en Boston hoy?" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_4.png)

###5. Enviar solicitud y manejar Tool Call

Crear el nodo `Send OpenAI Chat Request In World` y vincular el evento `On Message Finished`. En el callback del evento, obtener el arreglo ToolCalls desde el Payload.

Cuando el modelo decide invocar una herramienta, el array ToolCalls no está vacío. Recorre el array para obtener la información de cada Tool Call:

* **Id**: Identificador único de Tool Call
* **FunctionName**: Nombre de la función a llamar
* **FunctionArguments**: Argumentos de función (formato de cadena JSON)

<!-- Se necesita una imagen: mostrando el plano completo de envío de solicitud, creando el nodo "Enviar solicitud de chat OpenAI en el mundo", conectando "Opciones" y "Mensajes", vinculando el evento "Al finalizar el mensaje", y utilizando el nodo "Interrupción" en la devolución de llamada del evento para obtener "ToolCalls" del "Payload".-->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_5.png)

<!-- Se necesita una imagen: mostrar el diagrama de flujo que recorre el array ToolCalls utilizando un bucle For Each Loop, donde para cada elemento se emplea un nodo Break para obtener los campos Id, FunctionName, FunctionArguments y luego imprimirlos. -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_6.png) -->

###6. Ejecutar la función y devolver el resultado

Ejecuta la lógica de la función correspondiente según `FunctionName` (en este caso, simulando obtener el tiempo de entrega de un paquete postal) y luego devuelve el resultado como un mensaje de tipo `ToolCallResult` al modelo.

Para crear un nuevo Mensaje, es necesario configurar:

* **Rol**: Establecido como `Herramienta`
* **Contenido**: Resultado de la ejecución de la función
* **ToolCallResults**: Agregar un `FAIChatPlus_ChatRequestToolCallResult`, configurar el Id (utilizar el Tool Call Id anterior), FunctionName y FunctionResult.

<!-- Necesita imagen: mostrar el esquema para crear un mensaje de rol Tool, crear un nuevo Mensaje, Role=Tool, Content configurado con datos meteorológicos simulados como '{"temperature": "22", "unit": "celsius", "description": "Sunny"}', y agregar la información de resultados correspondiente en ToolCallResults -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_7.png)

###7. Continuar la conversación

Agrega el mensaje que contiene el resultado de ToolCallResult al historial de mensajes y envía la solicitud nuevamente. El modelo generará una respuesta final en lenguaje natural basada en los resultados devueltos por la función.

<!-- Se necesita una imagen: mostrar el plan de solicitud completo para la segunda vez, combinando el Mensaje original del Usuario, el Mensaje del Asistente devuelto por el modelo (incluyendo ToolCalls) y el Mensaje de resultado de la Herramienta en un nuevo arreglo de Mensajes, para volver a llamar a Enviar Solicitud de Chat OpenAI en el Mundo -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_8.png)

### 9. Plan maestro completo

El esquema completo de Tool Call luce así:

<!-- Se necesita una imagen: mostrando el panorama completo del flujo de Tool Call, incluyendo la definición de Tool, la primera solicitud, el procesamiento de Tool Call y la segunda solicitud en un flujo completo -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_9.png) -->

### 10. Resultados de la ejecución

Ejecuta el esquema y verás que el modelo devuelve una respuesta en lenguaje natural con la información del clima.

<!-- Se necesita imagen: captura de pantalla del resultado de la ejecución, mostrando la respuesta final del modelo, similar a "El clima actual en Boston es soleado con una temperatura de 22°C." -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_10.png) -->

##Uso avanzado

###Herramientas múltiples

Puedes definir múltiples Tools al mismo tiempo, y el modelo seleccionará cuál o cuáles funciones llamar según sea necesario.

<!-- Necesita imagen: muestra un diagrama de definición de múltiples Tools, por ejemplo, definiendo simultáneamente dos Tools como get_current_weather y get_stock_price, combinados en un array Tools mediante Make Array -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_multi_tools.png)

###Tipos de parámetros complejos

El parámetro Tool admite varios tipos, y se pueden agregar definiciones de parámetros más complejas, como tipos de enumeración, a través de los campos `ExtraJsonString` o `ExtraJsonObject`:

```json
{"enum": ["Beijing", "HongKong"]}
```

<!-- Se necesita una imagen: que muestre el uso de ExtraJsonString para configurar parámetros de enumeración en el blueprint, rellenando el campo ExtraJsonString del nodo Property con '{"enum": ["celsius", "fahrenheit"]}' -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_extra_json.png)

###Otras plataformas

El uso de Tool Call en Claude, Gemini, Ollama y CllamaServer es similar al de OpenAI, solo hay que reemplazar los nodos correspondientes de Request y Options. Las estructuras de datos principales en cada plataforma (como `FAIChatPlus_ChatRequestTool`, `FAIChatPlus_ChatResponseToolCall`, etc.) son universales.

--8<-- "footer_es.md"


> Este post está traducido usando ChatGPT. Por favor, envía tus comentarios en [**retroalimentación**](https://github.com/disenone/wiki_blog/issues/new)Señalar cualquier omisión en el indicado. 
