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

## v1.6.1 - 2025.03.07

### Bug Fix

OpenAI Image Chat Blueprint supports inputting images.

Herramienta de edición llamada mmproj permite modelo en blanco.

## v1.6.0 - 2025.03.02

###Nueva función

Actualiza el archivo llama.cpp a la versión b4604.

Cllama supports GPU backends: cuda and metal.

La herramienta de chat Cllama es compatible con el uso de GPU.

* Apoyar la lectura de archivos de modelos empaquetados en un archivo Pak.

### Bug Fix

Reparar el problema de la caída de Cllama al recargar durante el razonamiento.

Reparar error de compilación en iOS.

## v1.5.1 - 2025.01.30

###Nueva función. 

Solo se permite a Gemini enviar mensajes de audio.

Optimizar el método para obtener PCMData, descomprimir los datos de audio al generar B64.

Solicitar agregar dos devoluciones de llamada OnMessageFinished y OnImagesFinished.

Optimizar el Método Gemini para obtener automáticamente el Método basándose en bStream.

Agregar algunas funciones de Blueprint para facilitar la conversión de Wrapper a tipos reales, y obtener el mensaje de respuesta y el error.

### Bug Fix

Corregir el problema de múltiples llamadas a "Request Finish".

## v1.5.0 - 2025.01.29

###Nueva funcionalidad

Apoyar el envío de archivos de audio a Gemini.

Las herramientas del editor admiten el envío de archivos de audio y grabaciones.

### Bug Fix

Corregir el error que provoca que falle la copia de la sesión.

## v1.4.1 - 2025.01.04

###Reparación de problemas

La herramienta de chat admite enviar solo imágenes sin texto.

Reparar la falla al enviar imágenes a través de la interfaz de OpenAI.

Reparar el problema de configuración omitida de los parámetros Calidad, Estilo, ApiVersion en OpanAI y en las herramientas de chat de Azure.

## v1.4.0 - 2024.12.30

###Nueva función

* (Característica experimental) Cllama (llama.cpp) admite modelos multimodales y puede procesar imágenes.

Todos los parámetros de tipo de plano se les ha añadido una descripción detallada.

## v1.3.4 - 2024.12.05

###Nueva función.

OpenAI ofrece una API de visión.

###Reparación de problemas

Corregir el error al establecer OpenAI stream=false

## v1.3.3 - 2024.11.25

###Nueva función

Soporte para UE-5.5

###Reparación de problemas.

Corregir el problema de algunas plantillas que no funcionan.

## v1.3.2 - 2024.10.10

###Reparación de problemas

Reparar el fallo de cierre inesperado al detener manualmente la solicitud de cllama.

Reparar el problema de no encontrar los archivos ggml.dll y llama.dll al empaquetar la versión de descarga win de la tienda.

Revisar si se está en el hilo de juego al crear la solicitud.

## v1.3.1 - 2024.9.30

###Nueva función

Agregar un SystemTemplateViewer que permita visualizar y utilizar cientos de plantillas de configuración del sistema.

###Reparación de problemas.

Reparar el complemento descargado desde la tienda, llama.cpp no encuentra la biblioteca de enlace.

Corregir el problema de la longitud excesiva de la ruta de LLAMACpp.

Corregir el error de enlace de llama.dll después de empaquetar Windows.

Reparar el problema de la ruta del archivo al leer en iOS/Android.

Corregir error al establecer nombre en Cllame.

## v1.3.0 - 2024.9.23

###Importante nueva función.

Integrado llama.cpp para admitir la ejecución de grandes modelos de forma local sin conexión a Internet.

## v1.2.0 - 2024.08.20

###Nuevas características.

Apoyo para OpenAI Image Edit/Image Variation.

Admite la API de Ollama y la obtención automática de la lista de modelos admitidos por Ollama.

## v1.1.0 - 2024.08.07

###Nueva funcionalidad

Apoyo a la propuesta.

## v1.0.0 - 2024.08.05

###Nueva función.

Funcionalidad básica completa.

Apoyo a OpenAI, Azure, Claude, Gemini.

Herramienta de chat con editor integrado.

--8<-- "footer_es.md"


> Este post ha sido traducido utilizando ChatGPT, por favor [**反馈**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
