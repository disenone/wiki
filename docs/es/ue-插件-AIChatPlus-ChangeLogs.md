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

#Registro de versiones del complemento UE AIChatPlus.

## v1.6.0 - 2025.03.02

###Nueva función.

Actualiza llama.cpp a la versión b4604.

Cllama supports GPU backends: cuda and metal.

La herramienta de chat Cllama admite el uso de GPU.

Soportar la lectura de archivos de modelos empaquetados en Pak.

### Bug Fix

Corregir el problema de Cllama que causa que se bloquee al recargar durante el razonamiento.

Reparar error de compilación en iOS.

## v1.5.1 - 2025.01.30

###Nueva función

Solo se permite enviar archivos de audio a través de Gemini.

Optimizar el método para obtener PCMData, descomprimir los datos de audio al generar B64.

Solicitud: Agregar dos callbacks OnMessageFinished y OnImagesFinished

Optimizar el Método Gemini, obteniendo automáticamente el Método según bStream.

Agregar algunas funciones de blueprint para facilitar la conversión de un Wrapper a un tipo real, y así poder obtener el mensaje de respuesta y el error.

### Bug Fix

Arreglar el problema de múltiples llamadas a Request Finish.

## v1.5.0 - 2025.01.29

###Nueva función

Apoyar el envío de audio a Gemini.

Las herramientas del editor admiten el envío de audio y grabaciones.

### Bug Fix

Corregir el error de copia de sesión fallida.

## v1.4.1 - 2025.01.04

###Reparación de problemas

La herramienta de chat permite enviar solo imágenes sin mensaje.

Reparar la falla al enviar imágenes a través de la interfaz de OpenAI.

Reparar problemas de configuración de herramientas de chat OpanAI y Azure que omitieron los parámetros Quality, Style, ApiVersion.

## v1.4.0 - 2024.12.30

###Nueva funcionalidad

* (Función experimental) Cllama (llama.cpp) admite modelos multimodales y puede procesar imágenes.

Todos los parámetros de tipo de plano ahora tienen instrucciones detalladas adjuntas.

## v1.3.4 - 2024.12.05

###Nueva función.

OpenAI admite la API de visión.

###Reparación de problemas

Corregir el error al establecer OpenAI stream=false.

## v1.3.3 - 2024.11.25

###Nueva funcionalidad

Compatibilidad con UE-5.5

###Reparación de problemas

Reparación del problema de las partes de los planos que no funcionan.

## v1.3.2 - 2024.10.10

###Reparación de problemas

Reparación de falla en cllama que ocurre al detener manualmente la solicitud.

Arreglar el problema de la versión de descarga de Win del centro comercial que no puede encontrar los archivos ggml.dll y llama.dll al empaquetar.

Comprobar si se está en el hilo de juego al crear la solicitud.

## v1.3.1 - 2024.9.30

###Nueva función.

Agregar un SystemTemplateViewer que permita visualizar y utilizar cientos de plantillas de configuración de sistema.

###Solución de problemas

Reparar el complemento descargado desde la tienda llamado llama.cpp que no encuentra la biblioteca de enlace.

Corregir el problema de la ruta demasiado larga en LLAMACpp.

Corregir el error de enlace de llama.dll después de empaquetar Windows.

Corregir el problema de lectura de la ruta de archivos en iOS/Android.

Corregir el error en la configuración del nombre Cllame.

## v1.3.0 - 2024.9.23

###Importante nueva característica.

Integrando llama.cpp para admitir la ejecución local sin conexión de grandes modelos.

## v1.2.0 - 2024.08.20

###Nueva función

Apoyo a OpenAI Image Edit/Image Variation.

Admite la API de Ollama, admite la obtención automática de la lista de modelos admitidos por Ollama.

## v1.1.0 - 2024.08.07

###Nueva función.

Apoyo al plan estratégico.

## v1.0.0 - 2024.08.05

###Nueva función

Funcionalidad básica completa

Apoyo a OpenAI, Azure, Claude, Gemini.

Herramienta de chat con editor integrado y funciones completas.

--8<-- "footer_es.md"


> Este mensaje fue traducido utilizando ChatGPT. Por favor, [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
