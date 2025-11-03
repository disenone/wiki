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
description: Registros de versión
---

<meta property="og:title" content="UE 插件 AIChatPlus 版本日志" />

#Registro de versiones del complemento UE AIChatPlus.

## v1.8.0 - 2025.11.03

Actualizando llama.cpp a la versión b6792

## v1.7.0 - 2025.07.06

Actualizar llama.cpp b5536

Compatible con UE5.6.

Android 发布 shipping 会 crash，禁用掉 llama.cpp

Androide publicado se bloqueará al enviar, deshabilitar llama.cpp.

## v1.6.2 - 2025.03.17

###Nueva funcionalidad.

Añadir el parámetro KeepContext a Cllama, con el valor predeterminado false. El contexto se destruirá automáticamente después de que termine el Chat.

Añade el parámetro KeepAlive a Cllama para reducir la carga de solicitudes repetidas al modelo.

## v1.6.1 - 2025.03.07

### Bug Fix

OpenAI Image Chat admite la entrada de imágenes.

Herramienta de edición Cllama mmproj 模型允许空.

## v1.6.0 - 2025.03.02

###Nueva característica

Actualización de llama.cpp a la versión b4604.

Cllama supports GPU backends: cuda and metal.

La herramienta de chat Cllama admite el uso de GPU.

Apoyo para leer archivos de modelos empaquetados en Pak.

### Bug Fix

Reparación del problema de Cllama que causaba un fallo al recargar durante el razonamiento.

Reparar errores de compilación en iOS.

## v1.5.1 - 2025.01.30

###Nueva característica

Solo se permite que Gemini envíe archivos de audio.

Optimizar el método para obtener PCMData y descomprimir los datos de audio al generar B64.

* solicitud de añadir dos callbacks OnMessageFinished y OnImagesFinished

Optimizar el Método Gemini para que automáticamente obtenga el Método según bStream.

Añadir algunas funciones de Blueprint para facilitar la conversión del Wrapper al tipo real, y para obtener el Mensaje de Respuesta y el Error.

### Bug Fix

Corregir el problema de múltiples llamadas a Request Finish.

## v1.5.0 - 2025.01.29

###Nueva función

Apoyar el envío de audio a Gemini.

Las herramientas de edición admiten el envío de audio y grabaciones.

### Bug Fix

Corregir el error de copia de sesión fallida.

## v1.4.1 - 2025.01.04

###Reparación de problemas

La herramienta de chat admite enviar solo imágenes sin mensajes.

Reparar error al enviar imágenes a través de la interfaz de OpenAI.

Corregir la omisión de los parámetros Quality, Style y ApiVersion en la configuración de herramientas de chat de OpanAI y Azure.

## v1.4.0 - 2024.12.30

###Nueva función.

* (Función experimental) Cllama (llama.cpp) admite modelos multimodales y puede procesar imágenes.

Todos los parámetros de tipo de blueprint ahora cuentan con instrucciones detalladas.

## v1.3.4 - 2024.12.05

###Nueva característica.

OpenAI admite la API de visión.

###Reparaciones de problemas

Corregir el error al establecer OpenAI stream=false.

## v1.3.3 - 2024.11.25

###Nueva función

Soporta UE-5.5.

###Reparación de problemas

Reparar el problema de algunas plantillas que no funcionan.

## v1.3.2 - 2024.10.10

###Reparación de problemas

Reparar el fallo de cllama que ocurre al detener manualmente la solicitud.

Corregir el problema de la falta de archivos ggml.dll y llama.dll al empaquetar la versión de descarga de Win en la tienda.

Verificar al crear la solicitud si se encuentra en el hilo de juego.

## v1.3.1 - 2024.9.30

###Nueva función

Agregar un visor de plantillas de sistema que permita ver y utilizar cientos de plantillas de configuración del sistema.

###Reparación de problemas

Reparar el complemento descargado desde la tienda, llama.cpp no puede encontrar la biblioteca de enlace.

Solucionar el problema de la ruta demasiado larga en LLAMACpp.

Reparar el error de enlace de llama.dll después de empaquetar Windows.

Corregir el problema de lectura de la ruta del archivo en iOS/Android.

Corregir el error de configuración del nombre de Cllame.

## v1.3.0 - 2024.9.23

###Nueva y destacada función

Integrado llama.cpp, con soporte para ejecución offline de modelos grandes a nivel local.

## v1.2.0 - 2024.08.20

###Nueva función.

Apoyo para OpenAI Image Edit / Image Variation.

Compatible con la API de Ollama, admite la obtención automática de la lista de modelos admitidos por Ollama.

## v1.1.0 - 2024.08.07

###Nueva función

Apoyo a la propuesta.

## v1.0.0 - 2024.08.05

###Nueva funcionalidad.

Funcionalidad completa y sólida.

Apoyo a OpenAI, Azure, Claude, Gemini.

Herramienta de chat con editor incorporado y funciones completas.

--8<-- "footer_es.md"


> Este mensaje fue traducido utilizando ChatGPT, por favor [**comentarios**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
