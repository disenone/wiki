---
layout: post
title: CllamaServer (llama.cpp server)
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
- llama.cpp
- CllamaServer
description: CllamaServer (llama.cpp server)
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - CllamaServer (llama.cpp server)" />

#Plan Maestro - CllamaServer (servidor llama.cpp)

<!-- Se necesita una imagen: mostrar una visión general de todos los nodos de blueprints relacionados con CllamaServer, similar a xxx_all.png en otras documentaciones -->
![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_all.png)

##Resumen

CllamaServer está implementado en el modo Server de llama.cpp, que permite iniciar localmente un servidor compatible con la API de OpenAI y soporta múltiples funciones:

* **Servicio local de inferencia**: Inicia un servidor de inferencia de IA localmente, sin necesidad de depender de API externas.
* **Compatibilidad con la API de OpenAI**: Utiliza un formato de API compatible con OpenAI, facilitando la migración e integración.
* **Soporte para múltiples sesiones**: Admite múltiples solicitudes simultáneas
* **Llamada de herramientas**: Soporta la funcionalidad de llamada a funciones.
* **Voz a texto**: Compatible con la función Speech-to-Text
* **Gestión visual**: El editor incluye una interfaz de gestión de servidores integrada.

Diferencias con Cllama:
* **Cllama**: Carga directamente el modelo dentro del proceso para la inferencia, solo puede manejar una solicitud a la vez.
* **CllamaServer**: Inicia un servidor HTTP independiente capaz de manejar múltiples solicitudes concurrentes, compatible con la API en formato OpenAI.

##Preparativos

Al ejecutarse localmente, es necesario preparar primero los archivos del modelo offline, como descargar desde HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloca el modelo en alguna carpeta, por ejemplo, dentro del directorio del proyecto del juego en `Content/LLAMA`.

##Crear CllamaServer

###Crear un servidor usando Blueprint

Haz clic derecho en el plano para crear el nodo `Crear Servidor Cllama En El Mundo`.

<!-- Necesita imagen: captura de pantalla que muestre el clic derecho en el plano para buscar "Crear servidor Cllama" y crear el nodo -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_1.png)

###Configurar parámetros del Servidor

Crear el nodo `Cllama Server Param` y configurar los parámetros clave:

* **Modelo**: Ruta del archivo del modelo (obligatorio)
* **Puerto**: Puerto del servidor (0 indica asignación automática)
* **Host**: Dirección de escucha, por defecto `127.0.0.1`
* **NGpuLayers**: Número de capas de GPU (-1 significa usar toda la GPU)

<!-- Se requiere imagen: captura de pantalla que muestre la creación del nodo FAIChatPlus_CllamaServerParam, configurando parámetros como la ruta del Modelo, Puerto, NGpuLayers, etc. -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_2.png)

###Vincular eventos de devolución de llamada

Vinculación de eventos de retroalimentación del Servidor:

* **On Started**: Se activa cuando el servidor se inicia correctamente.
* **On Stopped**: Se activa cuando el servidor se detiene
* **On Failed**: Se activa cuando falla el inicio del servidor

<!-- se necesita una imagen: mostrando los diagramas de eventos OnStartedListeners, OnStoppedListeners y OnFailedListeners -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_3.png)

###Plan completo de creación

El plan completo para la creación del servidor es el siguiente:

<!-- Se necesita una imagen: que muestre una vista completa del esquema de creación de un Servidor, incluyendo la configuración de parámetros, la creación de nodos y el enlace de devoluciones de llamada -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_4.png)

Después de ejecutar el plano, el inicio exitoso del servidor desencadenará el evento `On Started`.

<!-- Se necesita imagen: que muestre el resultado operativo tras el inicio exitoso del Server, mostrando el registro o la salida en pantalla del arranque exitoso -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_5.png) -->

##Detalles de los parámetros del servidor

La estructura `FAIChatPlus_CllamaServerParam` contiene los siguientes parámetros:

###Parámetros comunes

| Parámetro | Tipo | Valor predeterminado | Descripción |
|-----|------|-------|------|
| Modelo | FString | - | Ruta del archivo del modelo (requerido) |
| Puerto | int32 | 0 | Puerto de escucha, 0 indica asignación automática |
| Host | FString | 127.0.0.1 | Dirección de escucha |
| NGpuLayers | int32 | -1 | Capas de GPU, -1 significa todas |
| bUseJinja | bool | false | Utilizar plantilla Jinja |
| MMProj | FString | - | Ruta del archivo de proyección multimodal |
| Temperatura | float | 0.8 | Temperatura de muestreo |

###Argumentos de razonamiento

| Parámetro | Tipo | Valor por defecto | Descripción |
|-----|------|-------|------|
| CtxSize | int32 | 4096 | Tamaño del contexto |
| NPredict | int32 | -1 | Cantidad de Tokens a predecir, -1 significa infinito |
| Hilos | int32 | -1 | Número de hilos de CPU, -1 indica automático |
| BatchSize | int32 | 2048 | Tamaño del lote |

###Parámetros de muestreo

| Parámetro | Tipo | Valor predeterminado | Descripción |
|-----|------|-------|------|
| TopK | int32 | 40 | Muestreo Top-K |
| TopP | flotante | 0.9 | Muestreo Top-P |
| MinP | flotante | 0.1 | Muestreo Min-P |
| RepeatPenalty | float | 1.0 | Penalización por repetición |

###Parámetros del servidor

| Parámetro | Tipo | Valor predeterminado | Descripción |
|-----|------|-------|------|
| ApiKey | FString | - | Clave API (opcional) |
| Tiempo de espera | int32 | 600 | Tiempo límite (segundos) |
| Paralelo | int32 | 1 | Número de secuencias paralelas |
| bNoWebUI | bool | false | Deshabilitar la interfaz web |
| bVerbose | bool | false | Registro detallado |

##Usar CllamaServer para chatear

###Crear Solicitud de Chat

Una vez que el servidor se haya iniciado con éxito, puedes utilizar el nodo `Send CllamaServer Chat Request` para enviar solicitudes de chat.

<!-- Se necesita imagen: captura de pantalla mostrando la búsqueda con clic derecho en el plano de "CllamaServer Chat Request" y la creación del nodo -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_1.png)

###Configurar Opciones del Chat

Crear el nodo `CllamaServer Chat Request Options`, establecer BaseUrl como la dirección del servidor.

Se puede obtener la información del servidor mediante el nodo `Get Server Info By ID`.

<!-- Se necesita una imagen: muestra la creación del nodo FAIChatPlus_CllamaServerChatRequestOptions, utilizando Get Http Address para obtener la dirección del Servidor y configurarla en BaseUrl en el diagrama de flujo -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_2.png)

###Crear Mensajes

Crear un arreglo de Messages, agregar System Message y User Message.

<!-- Se necesita imagen: esquema que muestre la creación de un array Messages, incluyendo System Message (configuración del rol del asistente) y User Message (pregunta del usuario) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_3.png)

###Vincular retrollamada para manejar la respuesta

Vincula los eventos `On Message` o `On Message Finished` para recibir respuestas del modelo.

<!-- Se necesita una imagen: un diagrama que muestre la vinculación de eventos OnMessageListeners y la impresión de mensajes en pantalla dentro de la devolución de llamada -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_4.png)

###Plan maestro de chat completo

El plan completo del chat es el siguiente:

<!-- Se requiere imagen: mostrar el panorama completo del esquema de chat, incluyendo el flujo completo de crear un servidor, esperar su inicio, enviar solicitudes de chat y procesar las respuestas -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_5.png)

###Resultado de la ejecución

Ejecuta el esquema y verás que el mensaje devuelto por el modelo se muestra en la pantalla.

<!-- Se necesita una imagen: muestra el resultado de la ejecución del chat, en pantalla aparece la respuesta generada por el modelo -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_6.png) -->

##Gestión del Servidor

###Obtener información del Servidor

Usa el nodo `Get Server Info` para obtener los detalles del Servidor.

<!-- Imagen requerida: Muestra el uso del nodo Get Server Info para obtener FAIChatPlus_CllamaServerInfo en el diagrama de flujo, y Break para mostrar cada campo -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_info_1.png)

Server Info contiene la siguiente información:
* **ServerID**: ID único del servidor
* **Anfitrión**: Dirección de escucha
* **Puerto**: Puerto de escucha
* **Dirección**: Dirección completa (host:port)
* **HttpAddress**: Dirección HTTP (http://host:port)
* **bIsRunning**: ¿Se está ejecutando?
* **Param**: Parámetro del servidor

###Detener Servidor

Utiliza el nodo `Stop Server By ID` para detener el servidor actual.

<!-- Se necesita imagen: Mostrando el gráfico de llamada al nodo Stop Cllama Server -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_stop_1.png)

###Funciones de gestión estática

AIChatPlus ofrece una serie de funciones estáticas para gestionar todos los Servidores.

| Función | Descripción |
|-----|------|
| `Is Server Valid (Static)` | Comprueba si el servidor es válido |
| `Is Server Running (Static)` | Verificar si el Servidor está en funcionamiento |
| `Stop Server By ID` | Detener Servidor Específico por ID |
| `Stop All Servers` | Detener todos los Servidores |
| `Get Server Info By ID` | Obtener información del servidor por ID |
| `Obtener todos los IDs de servidor` | Obtener todos los IDs de servidor |
| `Obtener Servidor por ID` | Obtener instancia de Servidor mediante ID |

<!-- Se necesita imagen: ejemplo de plano que muestra el uso de funciones de gestión estática como Obtener Todos los IDs de Servidores y Detener Todos los Servidores -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_static_1.png)

##Soporte multimodal

CllamaServer admite modelos multimodales (como Moondream, Qwen2-VL, etc.).

###Configurar parámetros multimodales

En el parámetro del Servidor, establece `MMProj` (ruta del archivo de proyección multimodal):

<!-- Se necesita imagen: muestra el diagrama de configuración de las dos rutas Model y MMProj en Server Param -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_1.png)

###Enviar mensaje de imagen

Agregar imágenes en Mensajes:

<!-- Se necesita una imagen: muestra la lectura de un archivo de imagen, la creación de un Message que contenga la imagen y el esquema de envío de solicitud a través de CllamaServer -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_2.png)

### Resultados de la ejecución

<!-- Se necesita imagen: mostrar los resultados de ejecución del reconocimiento de imágenes, la pantalla muestra la descripción del contenido de la imagen por parte del modelo -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_3.png) -->

## Tool Calling

CllamaServer es compatible con la función Tool Calling (llamada de funciones), cuyo uso es similar al de OpenAI.

Para un uso detallado, consulte [Tool Call](ue-插件-AIChatPlus-Usage-Blueprint-ToolCall.md)Documento.

Al usar CllamaServer para Tool Call, es necesario:
1. En los parámetros del Server, configura `bUseJinja = true`
2. Definir herramientas en el campo Tools de Chat Options

<!-- Se necesita imagen: mostrar el esquema completo de CllamaServer Tool Call, incluyendo la configuración de bUseJinja=true y la definición de Tools -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_tool_1.png)

##Editor Administración del Servidor

AIChatPlus ofrece una interfaz visual de gestión de CllamaServer dentro de sus herramientas de editor, facilitando la creación, supervisión y administración de múltiples servidores.

Abre la herramienta del editor: `Herramientas -> AIChatPlus -> AIChat`, abre la pestaña del Administrador del Servidor Cllama.

<!-- Se necesita imagen: captura de pantalla de la interfaz de administración de CllamaServer en el editor, mostrando la lista de servidores, botón de creación, información de estado, etc. -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_editor_1.png)

En el editor puedes:
* Crear nuevo Servidor
* Verificar el estado del Servidor en ejecución
* Detener el Servidor especificado
* Configurar parámetros del servidor
* La configuración del servidor se guardará automáticamente

<!-- Necesita imagen: mostrar la interfaz de creación de un nuevo Servidor en el editor, mostrando el panel de configuración de parámetros -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_editor_2.png)

##Relación con otras API

Dado que CllamaServer es compatible con el formato de API de OpenAI, también puedes utilizar el nodo Chat Request de OpenAI para comunicarte con CllamaServer, solo necesitas configurar `BaseUrl` con la dirección de CllamaServer.

<!-- Necesita imagen: ejemplo de diagrama de flujo que muestra el nodo OpenAI Chat Request, pero con BaseUrl configurado en la dirección CllamaServer -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_openai_1.png) -->

--8<-- "footer_es.md"


> Esta publicación ha sido traducida usando ChatGPT. Por favor, proporciona tus comentarios en [**retroalimentación**](https://github.com/disenone/wiki_blog/issues/new)Señalar cualquier omisión en el texto. 
