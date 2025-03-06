---
layout: post
title: Cllama (llama.cpp)
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
description: Cllama (llama.cpp)
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Cllama (llama.cpp)" />

#Sección Blueprint - Cllama (llama.cpp)

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_all.png)

##Modelo sin conexión

Cllama está implementado basado en llama.cpp y es compatible con el uso offline de modelos de inferencia de IA.

Debido a que estamos trabajando sin conexión, es necesario preparar previamente los archivos del modelo, como descargar el modelo fuera de línea desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloca el modelo en una carpeta específica, por ejemplo, en el directorio Content/LLAMA del proyecto de juego.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA > ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Una vez que tengamos el archivo del modelo sin conexión, podemos utilizar Cllama para realizar chats de inteligencia artificial.

##Conversación de texto

Utilice Cllama para chatear por texto.

En el diagrama, haz clic derecho para crear un nodo llamado `Enviar solicitud de chat de Cllama`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Crear un nodo de Options y establecer `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Crea mensajes, agrega un mensaje del sistema y un mensaje de usuario.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Crear un delegado que reciba la información de salida del modelo y la imprima en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

El diseño completo se ve así, ejecuta el diseño y podrás ver en la pantalla del juego el mensaje devuelto al imprimir el gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##Generador de texto de imagen.

Cllama también experimentó apoyando la biblioteca llava, brindando la capacidad de Vision.

Por favor, asegúrate de tener listo el archivo del modelo offline multimodal, como por ejemplo Moondream ([moondream2-text-model-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-text-model-f16.gguf), [moondream2-mmproj-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-mmproj-f16.gguf)）或者 Qwen2-VL（[Qwen2-VL-7B-Instruct-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/Qwen2-VL-7B-Instruct-Q8_0.gguf), [mmproj-Qwen2-VL-7B-Instruct-f16.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-7B-Instruct-f16.gguf)O cualquier otro modelo multimodal compatible con llama.cpp.

Crear un nodo de opciones, configurando los parámetros "Model Path" y "MMProject Model Path" con los archivos del modelo multimodal correspondiente.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_1.png)

Crear un nodo para leer el archivo de imagen flower.png y configurar los mensajes.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_3.png)

Crear finalmente el nodo, recibir la información devuelta y mostrarla en pantalla, el diseño completo se vería así:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_4.png)

Ejecutar el diagrama de flujo para visualizar el texto devuelto.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_5.png)

##El archivo llama.cpp utiliza la GPU.

Añadir la opción de solicitud de chat "Cllama Chat Request Options" con el parámetro "Num Gpu Layer", que permite configurar la carga de GPU en llama.cpp, lo que controla el número de capas que se deben calcular en la GPU. Referirse a la imagen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

##Manipular archivos de modelos en el archivo .Pak después de empaquetar.

Una vez que se inicia el empaquetado Pak, todos los archivos de recursos del proyecto se colocarán en el archivo .Pak, incluidos los archivos de modelo fuera de línea gguf.

Debido a que llama.cpp no puede leer directamente los archivos .Pak, es necesario copiar los archivos de modelos sin conexión del archivo .Pak al sistema de archivos.

AIChatPlus ofrece una función que automáticamente copia y procesa los archivos de modelos en .Pak, colocándolos en la carpeta Saved.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

O también puedes gestionar los archivos de modelo en .Pak tú mismo, la clave es copiar los archivos porque llama.cpp no puede leer correctamente .Pak.

##Nodo de funcionalidad.

Cllama proporciona algunos nodos funcionales para acceder fácilmente al estado actual del entorno.


"Cllama Is Valid": Verificar si Cllama está correctamente inicializado en llama.cpp.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu"：Determinar si llama.cpp es compatible con el backend de GPU en el entorno actual.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Obtener Soporte Backends de llamada": Obtener todos los backends compatibles con llama.cpp en uso actual.


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama Prepare ModelFile In Pak": Copia automáticamente los archivos de modelo de Pak al sistema de archivos.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)


--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor déjenos sus comentarios en [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
