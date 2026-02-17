---
layout: post
title: Registro de versiones
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
description: Registro de versiones
---

<meta property="og:title" content="UE 插件 AIChatPlus 版本日志" />

#Registro de cambios del plugin UE AIChatPlus

## v2.0.0 - 2026.02.14

* **Compatibilidad con múltiples plataformas en Tool Calling**: Se han añadido funciones de llamada a herramientas/llamada a funciones para cinco grandes plataformas: OpenAI, Claude, Gemini, Ollama y CllamaServer.
* **Integración de Cllama Server**: Compatibilidad completa con el servidor local llama.cpp, incluyendo creación, gestión, conversión de voz a texto, y ofrece una interfaz visual de gestión en el editor.
* **Biblioteca de planos JSON**: Se han añadido las clases de operación de planos JsonObject/JsonArray que permiten la conversión entre JSON y USTRUCT.
* **OpenAI Audio**: Compatible con entrada y salida de audio de OpenAI, el editor puede previsualizar respuestas de audio

## v1.8.0 - 2025.11.03

* Actualizar llama.cpp b6792

## v1.7.0 - 2025.07.06

* Actualizar llama.cpp b5536

* Compatible con UE5.6

* Android falla en el lanzamiento de shipping, hay que desactivar llama.cpp

## v1.6.2 - 2025.03.17

###Nueva función

* Cllama añade el parámetro KeepContext, predeterminado en false. El Context se destruye automáticamente al finalizar el Chat.

* Cllama añade el parámetro KeepAlive, lo que puede reducir la lectura repetida del modelo

## v1.6.1 - 2025.03.07

### Bug Fix

* El boceto de OpenAI Image Chat admite la entrada de imágenes.

* El modelo Cllama mmproj de la herramienta Editor permite vacío

## v1.6.0 - 2025.03.02

###Nueva función

* llama.cpp actualizado a la versión b4604

* Cllama admite backends de GPU: cuda y metal

* La herramienta de chat Cllama admite el uso de GPU

* Compatibilidad con la lectura de archivos de modelo dentro de paquetes Pak

### Bug Fix

* Solucionado el problema de que Cllama se bloqueaba al recargar durante la inferencia.

* Corregir errores de compilación en iOS

## v1.5.1 - 2025.01.30

###Nueva función

* Solo se permite que Gemini envíe audio

* Optimizar el método para obtener PCMData, descomprimiendo los datos de audio al generar B64

* solicitud agregar dos callbacks OnMessageFinished y OnImagesFinished

* Optimizar Gemini Method, obteniendo automáticamente el Method según bStream

* Agregar algunas funciones de blueprint para facilitar la conversión de Wrapper a tipos reales, así como para obtener Response Message y Error.

### Bug Fix

* Corrección del problema de llamadas múltiples a Request Finish

## v1.5.0 - 2025.01.29

###Nueva función

* Soporta el envío de audio a Gemini.

* Las herramientas del editor permiten enviar audio y grabaciones

### Bug Fix

* Corregido el error de fallo en la copia de Sesión

## v1.4.1 - 2025.01.04

###Corrección de problemas

* La herramienta de chat admite enviar solo imágenes sin mensajes

* Solucionado el problema de fallo en el envío de imágenes mediante la interfaz OpenAI

* Corrección del problema en las herramientas de chat OpanAI y Azure donde se omitían los parámetros Quality, Style y ApiVersion=

## v1.4.0 - 2024.12.30

###Nueva función

* (Función experimental) Cllama(llama.cpp) admite modelos multimodales y puede procesar imágenes.

* Se han añadido notas detalladas a todos los parámetros de tipo plano.

## v1.3.4 - 2024.12.05

###Nueva funcionalidad

* OpenAI admite la API de visión

###Corrección de problemas

* Corregir error cuando OpenAI stream=false

## v1.3.3 - 2024.11.25

###Nueva función

* Compatible con UE-5.5

###Corrección de problemas

* Se corrigió el problema de que algunos planos no surtían efecto

## v1.3.2 - 2024.10.10

###Problemas corregidos

* Solucionado: El cllama se bloqueaba al detener manualmente una solicitud.

* Solucionado el problema de que la versión descargable de la tienda no encuentra los archivos ggml.dll y llama.dll al empaquetar para Windows.

* Al crear una solicitud, verifica si estás en el GameThread, CreateRequest comprueba en el hilo del juego

## v1.3.1 - 2024.9.30

###Nueva función

* Añadir un SystemTemplateViewer que permita visualizar y utilizar cientos de plantillas de configuración del sistema.

###Problemas corregidos

* Corregido un problema donde los complementos descargados desde la tienda no encontraban las bibliotecas enlazadas de llama.cpp

* Solucionado el problema de rutas demasiado largas en LLAMACpp

* Corrección del error en el enlace de llama.dll después del empaquetado en Windows.

* Solucionado el problema de lectura de rutas de archivos en iOS/Android

* Corrección del error al establecer el nombre en el Cllame

## v1.3.0 - 2024.9.23

###Nuevas características importantes

* Integrado con llama.cpp, compatible con la ejecución local fuera de línea de modelos grandes.

## v1.2.0 - 2024.08.20

###Nueva función

* Soporta OpenAI Image Edit/Image Variation

* Compatibilidad con la API de Ollama, soporte para la obtención automática de la lista de modelos compatibles con Ollama.

## v1.1.0 - 2024.08.07

###Nueva función

* Soporte de planos

## v1.0.0 - 2024.08.05

###Nuevas Funciones

* Funciones básicas completas

* Compatible con OpenAI, Azure, Claude, Gemini

* Herramienta de chat con editor integrado completamente funcional

--8<-- "footer_es.md"


> Este post fue traducido utilizando ChatGPT, por favor proporciona tu [**retroalimentación**](https://github.com/disenone/wiki_blog/issues/new)Por favor señale cualquier omisión. 
