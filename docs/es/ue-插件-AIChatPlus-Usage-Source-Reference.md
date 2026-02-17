---
layout: post
title: API Reference
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
description: API Reference
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - API Reference" />

#C++ - Referencia de la API

Este documento proporciona la referencia de la API en C++ para el complemento AIChatPlus, incluyendo descripciones de todas las clases públicas, estructuras, enumeraciones y métodos clave.

##Tabla de contenidos

En español, el texto se traduciría como:

- [Tipo enumerado](##枚举类型)
-[Clases Básicas Fundamentales](##核心基类)
- [Clase Handler](##handler-类)
- [Clase Request](##request-类)
- [Clase de herramientas](##工具类)
- [Clase JSON](##json-类)

---

##Tipo de enumeración

### EAIChatPlus_ChatApiProvider

Proveedores enumerados de API de chat con IA.

```cpp
enum class EAIChatPlus_ChatApiProvider : uint8
{
    OpenAI,         // OpenAI API
    Azure,          // Azure OpenAI API
    Claude,         // Anthropic Claude API
    Gemini,         // Google Gemini API
Ollama,         // Servicio local de Ollama
Cllama,         // llamada directa de llama.cpp (obsoleta)
CllamaServer    // Modo servidor de llama.cpp
};
```

### EAIChatPlus_ImageApiProvider

Proveedores de API de generación de imágenes enumerados.

```cpp
enum class EAIChatPlus_ImageApiProvider : uint8
{
    OpenAI,   // OpenAI DALL-E
    Azure     // Azure OpenAI DALL-E
};
```

### EAIChatPlus_ChatRole

Enumeración de roles de mensajes.

```cpp
enum class EAIChatPlus_ChatRole : uint8
{
Sistema,     // Comandos del sistema (modelo antiguo)
Usuario,       // Mensaje del usuario
Asistente,  // Respuesta de IA
Desarrollador,  // Instrucciones para desarrolladores (modelo o1+)
    Herramienta        // Resultado de la llamada a herramientas
};
```

### EAIChatPlus_ImageChatType

Enumeración de tipos de operación de imágenes.

```cpp
enum class EAIChatPlus_ImageChatType : uint8
{
Generación,  // Generación de imágenes
Editar,        // Edición de imágenes
Variación    // Variante de imagen
};
```

### EAIChatPlus_JsonValueType

Enumeración de tipos de valores JSON.

```cpp
enum class EAIChatPlus_JsonValueType : uint8
{
Ninguno,    // Inválido
Null,     // Valor nulo
Cadena,   // Cadena de caracteres
Número,   // Número
Booleano,  // Booleano
Arreglo,    // Array
Objeto    // 对象
};
```

---

##Clase base central

### UAIChatPlus_RequestBase

La clase base para todas las solicitudes (clase abstracta).

**Métodos clave:**

| Método | Tipo de Retorno | Descripción |
|------|---------|------|
| `SendRequest()` | `bool` | Enviar solicitud |
| `StopRequest()` | `void` | Detener solicitud |
| `Activate()` | `void` | Activa el objeto de solicitud |
| `IsActivated()` | `bool` | Verifica si está activado |
| `SetIsAutoDestroy(bool)` | `void` | Configura si se destruye automáticamente al completarse |

**Encargo:**

| Nombre del delegado | Firma | Descripción |
|--------|------|------|
| `OnStartedListeners` | `void()` | Solicitud iniciada |
| `OnMessageListeners` | `void(const FString&)` | Recepción de mensajes en flujo |
| `OnFinishedListeners` | `void(const FAIChatPlus_PointerWrapper&)` | Solicitud completada |
| `OnFailedListeners` | `void(const FAIChatPlus_PointerWrapper&)` | Solicitud fallida |

---

### UAIChatPlus_ChatRequestBase

Clase base de solicitud de chat, hereda de `UAIChatPlus_RequestBase`.

**Métodos de fábrica estáticos:**

```cpp
// Crear solicitud por Proveedor
static UAIChatPlus_ChatRequestBase* CreateByApi(EAIChatPlus_ChatApiProvider InApiProvider);
static UAIChatPlus_ChatRequestBase* CreateByApiInWorld(EAIChatPlus_ChatApiProvider InApiProvider, const UObject* InWorldContext);
```

**Métodos clave:**

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `SetMessages(const TArray<FAIChatPlus_ChatRequestMessage>&)` | `void` | Establecer la lista de mensajes |
| `GetFullUrl()` | `FString` | Obtener la URL completa de la solicitud |
| `GetModelText()` | `FString` | Obtener el nombre del modelo |
| `GetTokenUsageText()` | `FString` | Obtiene la descripción del uso de tokens |
Aquí está la traducción al español:

| `GetApiProvider()` | `EAIChatPlus_ChatApiProvider` | Obtener el tipo de API Provider |

---

### UAIChatPlus_ImageRequestBase

Clase base de solicitud de imágenes, heredada de `UAIChatPlus_RequestBase`.

**Métodos de fábrica estáticos:**

```cpp
static UAIChatPlus_ImageRequestBase* CreateByApi(EAIChatPlus_ImageApiProvider InApiProvider);
static UAIChatPlus_ImageRequestBase* CreateByApiInWorld(EAIChatPlus_ImageApiProvider InApiProvider, const UObject* InWorldContext);
```

**Métodos clave:**

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `SetPrompt(const FString&)` | `void` | Establece la frase de aviso para la generación de imágenes |
| `SetImages(const TArray<UAIChatPlus_Texture*>&)` | `void` | Establecer imágenes de entrada (edición/variante) |
| `GetModelText()` | `FString` | Obtener el nombre del modelo |
| `GetStyleText()` | `FString` | Obtener el nombre del estilo |
| `GetRevisedPrompt()` | `FString` | Obtiene la frase de sugerencia revisada |
| `GetImageChatType()` | `FString` | Obtiene el tipo de operación de imagen |

---

### UAIChatPlus_ModelRequestBase

Clase base de solicitud de lista de modelos, hereda de `UAIChatPlus_RequestBase`.

**Métodos de fábrica estáticos:**

```cpp
static UAIChatPlus_ModelRequestBase* CreateByApi(EAIChatPlus_ChatApiProvider InApiProvider);
static UAIChatPlus_ModelRequestBase* CreateByApiInWorld(EAIChatPlus_ChatApiProvider InApiProvider, const UObject* InWorldContext);
```

---

##Clase Handler

### UAIChatPlus_HandlerBase

La clase base de todos los Handlers.

**Métodos clave:**

| Método | Tipo de Retorno | Descripción |
|------|---------|------|
| `SetIsAutoDestroy(bool)` | `void` | Establecer autodestrucción |
| `AutoDestroy()` | `void` | Ejecuta la autodestrucción |
| `Destroy()` | `void` | Destruye inmediatamente |

---

### UAIChatPlus_ChatHandlerBase

Chat Request Handler, hereda de `UAIChatPlus_HandlerBase`.

**Método de fábrica estático:**

```cpp
static UAIChatPlus_ChatHandlerBase* New();
```

**Métodos de vinculación:**

| Método | Descripción |
|------|------|
| `BindChatRequest(UAIChatPlus_ChatRequestBase*)` | Vincular solicitud de chat |
| `BindImageRequest(UAIChatPlus_ImageRequestBase*)` | Vincular solicitud de imagen |
| `BindModelRequest(UAIChatPlus_ModelRequestBase*)` | Vincular solicitud de modelo |
| `ClearDelegates()` | Limpiar todos los enlaces de delegados |

**Encargo:**

| Nombre del Mandato | Firma | Descripción |
|--------|------|------|
| `OnStarted` | `void()` | Solicitud iniciada |
| `OnStopped` | `void()` | Solicitud de detención |
| `OnMessage` | `void(const FString&)` | Mensajes en flujo |
| `OnMessageFinished` | `void(const FAIChatPlus_MessageFinishedPayload&)` | Mensaje completado |
| `OnUpdated` | `void(const FAIChatPlus_PointerWrapper&)` | Solicitud de actualización |
| `OnFinished` | `void(const FAIChatPlus_PointerWrapper&)` | Solicitud completada |
| `OnFailed` | `void(const FAIChatPlus_PointerWrapper&)` | Solicitud fallida |
| `OnImages` | `void(const TArray<UTexture2D*>&, bool)` | Generación de imágenes |
| `OnModels` | `void(const TArray<FString>&)` | Lista de modelos |

---

### UAIChatPlus_CllamaServerHandler

Manejador dedicado de CllamaServer。

**Métodos de fábrica estáticos:**

```cpp
static UAIChatPlus_CllamaServerHandler* CreateHandler();
```

**Encargo:**

| Nombre del mandato | Firma | Descripción |
|--------|------|------|
| `OnServerStarted` | `void(FGuid)` | Servidor iniciado |
| `OnServerStopped` | `void(FGuid)` | Servidor detenido |
| `OnServerFailed` | `void(FGuid, const FString&)` | Fallo del servidor |

---

##Clase Request

Todos los Request de los Provider siguen el mismo patrón de método fábrica:

###Patrón de método de fábrica genérico

```cpp
// Tomando OpenAI como ejemplo, otros Proveedores son similares
static UAIChatPlus_OpenAIChatRequest* Create();
static UAIChatPlus_OpenAIChatRequest* CreateWithOptions(const FAIChatPlus_OpenAIChatRequestOptions& InOptions);
static UAIChatPlus_OpenAIChatRequest* CreateWithOptionsAndMessages(
    const FAIChatPlus_OpenAIChatRequestOptions& InOptions,
    const TArray<FAIChatPlus_ChatRequestMessage>& InMessages);
static UAIChatPlus_OpenAIChatRequest* CreateInWorld(const UObject* InWorldContext);
static UAIChatPlus_OpenAIChatRequest* CreateInWorldWithOptions(
    const UObject* InWorldContext,
    const FAIChatPlus_OpenAIChatRequestOptions& InOptions);
static UAIChatPlus_OpenAIChatRequest* CreateInWorldWithOptionsAndMessages(
    const UObject* InWorldContext,
    const FAIChatPlus_OpenAIChatRequestOptions& InOptions,
    const TArray<FAIChatPlus_ChatRequestMessage>& InMessages);
```

###Métodos estáticos genéricos

Todos los clases Request proporcionan el método `CastWrapperToResponse` para la conversión de tipos:

```cpp
// Extraer los datos de respuesta de PointerWrapper
static FAIChatPlus_XXXResponseBody& CastWrapperToResponse(const FAIChatPlus_PointerWrapper& InWrapper);
static FAIChatPlus_PointerWrapper CastResponseToWrapper(const FAIChatPlus_XXXResponseBody& InResponse);
```

---

### UAIChatPlus_OpenAIChatRequest

Solicitud de chat de OpenAI.

**Archivo de cabecera:** `Common_OpenAI/AIChatPlus_OpenAIChatRequest.h`

**Tipo de Options:** `FAIChatPlus_OpenAIChatRequestOptions`

**Tipo de Respuesta:** `FAIChatPlus_OpenAIChatResponseBody`

---

### UAIChatPlus_AzureChatRequest

Solicitud de chat de Azure OpenAI.

**Archivo de encabezado:** `Common_Azure/AIChatPlus_AzureChatRequest.h`

**Tipo Options:** `FAIChatPlus_AzureChatRequestOptions`

**Tipo de respuesta:** `FAIChatPlus_AzureChatResponseBody`

---

### UAIChatPlus_ClaudeChatRequest

Solicitud de chat de Claude.

**Archivo de cabecera:** `Common_Claude/AIChatPlus_ClaudeChatRequest.h`

**Tipo de Options:** `FAIChatPlus_ClaudeChatRequestOptions`

**Tipo de Respuesta:** `FAIChatPlus_ClaudeChatResponseBody`

---

### UAIChatPlus_GeminiChatRequest

Solicitud de chat de Gemini.

**Archivo de encabezado:** `Common_Gemini/AIChatPlus_GeminiChatRequest.h`

**Tipo de Opciones:** `FAIChatPlus_GeminiChatRequestOptions`

**Tipo de Respuesta:** `FAIChatPlus_GeminiChatResponseBody`

---

### UAIChatPlus_OllamaChatRequest

Solicitud de chat Ollama.

**Archivo de cabecera:** `Common_Ollama/AIChatPlus_OllamaChatRequest.h`

**Tipo Options:** `FAIChatPlus_OllamaChatRequestOptions`

**Tipo de Respuesta:** `FAIChatPlus_OllamaChatResponseBody`

---

### UAIChatPlus_OllamaModelRequest

Solicitud de lista de modelos Ollama.

**Encabezado:** `Common_Ollama/AIChatPlus_OllamaModelRequest.h`

**Tipo de Options:** `FAIChatPlus_OllamaModelRequestOptions`

**Tipo de respuesta:** `FAIChatPlus_OllamaModelResponseBody`

**Métodos exclusivos:**

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `GetModelNames()` | `TArray<FString>` | Obtener la lista de nombres de modelos |

---

###UAIChatPlus_CllamaChatRequest (obsoleto)

Solicitud de chat fuera de línea de Cllama (obsoleta, se recomienda usar CllamaServer).

**Archivo de cabecera:** `Common_Cllama/AIChatPlus_CllamaChatRequest.h`

**Tipo de Opciones:** `FAIChatPlus_CllamaChatRequestOptions`

**Tipo de Respuesta:** `FAIChatPlus_CllamaChatResponseBody`

---

### UAIChatPlus_CllamaServerChatRequest

Solicitud de chat en CllamaServer.

**Archivo de encabezado:** `Common_CllamaServer/AIChatPlus_CllamaServerChatRequest.h`

**Tipo de Options:** `FAIChatPlus_CllamaServerChatRequestOptions`

**Tipo de Respuesta:** `FAIChatPlus_CllamaServerChatResponseBody`

---

### UAIChatPlus_OpenAIImageRequest

Solicitud de generación de imágenes de OpenAI.

**Archivo de cabecera:** `Common_OpenAI/AIChatPlus_OpenAIImageRequest.h`

**Tipo Options:** `FAIChatPlus_OpenAIImageRequestOptions`

**Tipo de respuesta:** `FAIChatPlus_OpenAIImageResponseBody`

---

### UAIChatPlus_AzureImageRequest

Solicitud de generación de imágenes en Azure.

**Archivo de encabezado:** `Common_Azure/AIChatPlus_AzureImageRequest.h`

**Tipo Options:** `FAIChatPlus_AzureImageRequestOptions`

**Tipo de respuesta:** `FAIChatPlus_AzureImageResponseBody`

---

### UAIChatPlus_CllamaServer

CllamaServer Clase de gestión de servidores.

**Archivo de encabezado:** `Common_CllamaServer/AIChatPlus_CllamaServer.h`

**Métodos de fábrica estáticos:**

```cpp
static UAIChatPlus_CllamaServer* CreateServer(
    const FAIChatPlus_CllamaServerParam& InParams,
    FGuid InServerID = FGuid());
static UAIChatPlus_CllamaServer* CreateServerInWorld(
    const UObject* InWorldContext,
    const FAIChatPlus_CllamaServerParam& InParams,
    FGuid InServerID = FGuid());
static UAIChatPlus_CllamaServer* CreateServerWithHandler(
    const FAIChatPlus_CllamaServerParam& InParams,
    UAIChatPlus_CllamaServerHandler* InHandler,
    FGuid InServerID = FGuid());
```

**Métodos de instancia:**

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `Activate()` | `void` | Activa el servidor |
| `DetenerServidor()` | `void` | Detiene el servidor |
| `IsRunning()` | `bool` | Comprueba si está en ejecución |
| `GetServerID()` | `FGuid` | Obtener ID del servidor |
| `GetHost()` | `FString` | Obtener la dirección del host |
Aquí está la traducción al español:

| `GetAddress()` | `FString` | Obtener dirección completa |
| `GetServerInfo(FAIChatPlus_CllamaServerInfo&)` | `bool` | Obtiene información del servidor |

**Métodos de gestión estática:**

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `IsServerValid(const FGuid&)` | `bool` | Verifica si el servidor es válido |
| `IsServerRunning(const FGuid&)` | `bool` | Verifica si el servidor está en ejecución |
| `StopServerByID(const FGuid&)` | `void` | Detener el servidor por ID |
| `StopAllServers()` | `void` | Detener todos los servidores |
| `GetServerByID(const FGuid&)` | `UAIChatPlus_CllamaServer*` | Obtener servidor por ID |
| `GetAllServerIDs()` | `TArray<FGuid>` | Obtener todos los IDs de servidor |

---

##Clase de Utilidades

### UAIChatPlus_Util

Clase de utilidad general, proporciona diversos métodos auxiliares estáticos.

**Archivo de cabecera:** `Common/AIChatPlus_Util.h`

####Registros relacionados

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `SetInternalLogVerbosity(EAIChatPlus_LogVerbosityType)` | `void` | Establece el nivel de registro interno |

####Conversión de envoltorio

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `CastWrapperToError(const FAIChatPlus_PointerWrapper&)` | `FAIChatPlus_ResponseErrorBase&` | Extraer mensaje de error |
| `CastWrapperToResponse(const FAIChatPlus_PointerWrapper&)` | `FAIChatPlus_ChatResponseBodyBase&` | Extraer datos de respuesta |
| `GetErrorWrapperDescription(const FAIChatPlus_PointerWrapper&)` | `FString` | Obtener la descripción del error |
| `GetResponseWrapperMessage(const FAIChatPlus_PointerWrapper&)` | `FString` | Obtener mensaje de respuesta |

####Herramientas de imagen

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `LoadImage(const FString&, bool)` | `UTexture2D*` | Carga una imagen desde un archivo |
| `SaveImage(UTexture2D*, const FString&)` | `bool` | Guarda la imagen en un archivo |
| `ImageToB64(UTexture2D*, int32)` | `FString` | Imagen a Base64 |
| `CopyTexture2D(UTexture2D*, UObject*, FName, EObjectFlags)` | `UTexture2D*` | Copiar textura |
| `FitImageSize(const FVector2D&, const FVector2D&)` | `FVector2D` | Calcula el tamaño de ajuste |
| `CopyTexture2DToClipboard(UTexture2D*)` | `void` | Copiar al Portapapeles |
| `IsCanCopyTexture2DToClipboard()` | `bool` | Comprueba si es compatible |

####Herramientas de audio

| Método | Tipo de devolución | Descripción |
|------|---------|------|
| `LoadSoundWav(const FString&)` | `USoundWave*` | Cargar audio desde un archivo |
| `SaveSoundWav(USoundWave*, const FString&)` | `bool` | Guardar audio en archivo |
| `SoundToB64(USoundWave*)` | `FString` | Audio a Base64 |
| `CopySoundWave(const USoundWave*, UObject*, FName)` | `USoundWave*` | Copiar onda sonora |
| `WavDataToSoundWave(const TArray<uint8>&, bool, bool)` | `USoundWave*` | Convertir datos WAV a onda sonora |
| `GetSoundWavePCMData(USoundWave*)` | `TArray<uint8>` | Obtener datos PCM |

####Herramientas JSON

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `MergeJsonObjects(const FString&, const FString&)` | `FString` | Combinar cadenas JSON |
| `LoadJsonString(const FString&)` | `TSharedPtr<FJsonObject>` | Analizar cadena JSON |
| `ToJsonString(const TSharedPtr<FJsonObject>&)` | `FString` | Convierte a cadena JSON |

####Herramienta Cllama

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `Cllama_IsValid()` | `bool` | Verifica si Cllama está disponible |
| `Cllama_IsSupportGpu()` | `bool` | Comprueba si hay soporte para GPU |
| `Cllama_GetSupportBackends()` | `TArray<FString>` | Obtener los backends soportados |
| `Cllama_PrepareModelPathFromPak(const FString&)` | `FString` | Prepara la ruta del modelo desde el Pak |

####Información del modelo

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `GetOpenAIChatDefaultModels()` | `const TArray<FName>&` | Lista de modelos predeterminados de OpenAI |
| `GetOpenAIChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | Obtener información del modelo OpenAI |
| `GetClaudeChatDefaultModels()` | `const TArray<FName>&` | Lista de modelos predeterminados de Claude |
| `GetClaudeChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | Obtener información del modelo Claude |
| `GetGeminiChatDefaultModels()` | `const TArray<FName>&` | Lista de modelos predeterminados de Gemini Chat |
| `GetGeminiChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | Obtener información del modelo Gemini |

---

### UAIChatPlus_Texture

Clase de envoltura de imágenes, compatible con carga asincrónica y conversión Base64.

**Archivo de encabezado:** `Common/AIChatPlus_Texture.h`

**Métodos de fábrica estáticos:**

```cpp
static UAIChatPlus_Texture* New(UTexture2D* InTexture = nullptr, const FString& InSourcePath = "");
static UAIChatPlus_Texture* CreateInBlueprint(UObject* WorldContextObject, UTexture2D* InTexture);
```

**Método:**

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `LoadFromFile(const FString&)` | `bool` | Cargar desde archivo (sincrónico) |
| `LoadFromFileAsync(const FString&, Callback)` | `FLoadingTaskType*` | Cargar desde archivo (asíncrono) |
| `LoadFromAsset(UObject*, const FString&)` | `bool` | Cargar desde activo (síncrono) |
| `LoadFromAssetAsync(UObject*, Callback, const FString&)` | `FLoadingTaskType*` | Cargar desde activo (asíncrono) |
| `ToB64()` | `const FString&` | Convertir a Base64 (sincrónico) |
| `ToB64Async(Callback)` | `FLoadingTaskType*` | Convertir a Base64 (asíncrono) |
| `GetBrush(bool)` | `const FSlateBrush*` | Obtener el pincel Slate |
| `GetBrushCopy(bool)` | `FSlateBrush` | Obtener copia del pincel |
| `GetSize()` | `FIntVector2` | Obtiene el tamaño |
| `GetSize2D()` | `FVector2D` | Obtener tamaño (en punto flotante) |
| `IsValid()` | `bool` | Comprueba si es válido |
| `IsLoading()` | `bool` | Comprueba si está cargando |
| `Reset()` | `void` | Reiniciar |
| `WaitLoadingComplete()` | `void` | Esperar a que la carga se complete |

---

### UAIChatPlus_Sound

Clase envoltorio de audio, compatible con carga asincrónica y conversión Base64.

**Archivo de cabecera:** `Common/AIChatPlus_Sound.h`

**Métodos de fábrica estáticos:**

```cpp
static UAIChatPlus_Sound* New(USoundWave* InSound = nullptr, const FString& InSourcePath = "");
static UAIChatPlus_Sound* CreateInBlueprint(UObject* WorldContextObject, USoundWave* InSound);
```

**Método:**

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `LoadFromFile(const FString&)` | `bool` | Cargar desde archivo (sincrónico) |
| `LoadFromFileAsync(const FString&, Callback)` | `FLoadingTaskType*` | Carga desde archivo (asíncrono) |
| `LoadFromAsset(UObject*, const FString&)` | `bool` | Cargar desde un activo (sincrónico) |
| `LoadFromAssetAsync(UObject*, Callback, const FString&)` | `FLoadingTaskType*` | Cargar desde activo (asíncrono) |
| `ToB64()` | `const FString&` | Convertir a Base64 (sincrónico) |
| `ToB64Async(Callback)` | `FLoadingTaskType*` | Convertir a Base64 (asíncrono) |
| `IsValid()` | `bool` | Verifica si es válido |
| `IsLoading()` | `bool` | Verifica si está cargando |
| `Reset()` | `void` | Reiniciar |
| `WaitLoadingComplete()` | `void` | Esperar a que la carga se complete |
| `PlayInEditor()` | `void` | Reproducir en el editor |

---

##Clase JSON

### UAIChatPlus_JsonObject

Clase de envoltura para objetos JSON.

**Archivo de encabezado:** `Common/Json/AIChatPlus_JsonObject.h`

**Métodos de fábrica estáticos:**

```cpp
static UAIChatPlus_JsonObject* Create();
static UAIChatPlus_JsonObject* Parse(const FString& JsonString, bool& bSuccess, FString& ErrorMessage);
static UAIChatPlus_JsonObject* FromStruct(const int32& Struct);  // CustomThunk
```

**Métodos de configuración de campos (admite llamadas encadenadas):**

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `SetStringField(const FString&, const FString&)` | `UAIChatPlus_JsonObject*` | Establecer campo de cadena |
| `SetNumberField(const FString&, float)` | `UAIChatPlus_JsonObject*` | Establecer campo numérico |
| `SetIntegerField(const FString&, int32)` | `UAIChatPlus_JsonObject*` | Establecer campo entero |
| `SetBooleanField(const FString&, bool)` | `UAIChatPlus_JsonObject*` | Establecer campo booleano |
| `SetObjectField(const FString&, UAIChatPlus_JsonObject*)` | `UAIChatPlus_JsonObject*` | Configurar campo de objeto |
| `SetArrayField(const FString&, UAIChatPlus_JsonArray*)` | `UAIChatPlus_JsonObject*` | Establecer campo de matriz |
| `SetNullField(const FString&)` | `UAIChatPlus_JsonObject*` | Establecer campo nulo |

**Métodos para obtener campos:**

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `GetStringField(const FString&, const FString&, bool&)` | `FString` | Obtener cadena de texto |
| `GetNumberField(const FString&, float, bool&)` | `float` | Obtener número |
| `GetIntegerField(const FString&, int32, bool&)` | `int32` | Obtener entero |
| `GetBooleanField(const FString&, bool, bool&)` | `bool` | Obtener booleano |
| `GetObjectField(const FString&, bool&)` | `UAIChatPlus_JsonObject*` | Obtener objeto |
| `GetArrayField(const FString&, bool&)` | `UAIChatPlus_JsonArray*` | Obtener Array |

**Otros métodos:**

| Método | Tipo de retorno | Descripción |
|------|---------|------|
Aquí está la traducción al español:

| `HasField(const FString&)` | `bool` | Verifica la existencia del campo |  

Mantuve la estructura de la tabla original y traduje únicamente el texto (sin modificar el código o los tipos de datos). La traducción es técnica pero natural en español para programación.
| `GetFieldType(const FString&)` | `EAIChatPlus_JsonValueType` | Obtener el tipo de campo |
| `RemoveField(const FString&)` | `UAIChatPlus_JsonObject*` | Eliminar campo |
| `Clear()` | `UAIChatPlus_JsonObject*` | Vacía todos los campos |
| `ToString(bool)` | `FString` | Convertir a cadena |
| `ToStruct(int32&)` | `bool` | Convertir a estructura |
| `Merge(UAIChatPlus_JsonObject*, bool)` | `UAIChatPlus_JsonObject*` | Fusionar objetos |
| `Duplicate()` | `UAIChatPlus_JsonObject*` | Duplicar objeto |
Aquí está la traducción al español:

| `IsValid()` | `bool` | Comprobar validez |

**Método de consulta de ruta:**

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `SetStringByPath(const FString&, const FString&, const FAIChatPlus_JsonPathOptions&)` | `UAIChatPlus_JsonObject*` | Establecer cadena por ruta |
| `GetStringByPath(const FString&, const FString&, FAIChatPlus_JsonQueryResult&)` | `FString` | Obtener cadena por ruta |

---

### UAIChatPlus_JsonArray

Clase envoltorio para matrices JSON.

**Archivo de encabezado:** `Common/Json/AIChatPlus_JsonArray.h`

**Métodos de fábrica estáticos:**

```cpp
static UAIChatPlus_JsonArray* Create();
static UAIChatPlus_JsonArray* Parse(const FString& JsonString, bool& bSuccess, FString& ErrorMessage);
static UAIChatPlus_JsonArray* FromStringArray(const TArray<FString>& Values);
static UAIChatPlus_JsonArray* FromIntegerArray(const TArray<int32>& Values);
```

**Método para añadir elementos (soporta llamadas en cadena):**

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `AddString(const FString&)` | `UAIChatPlus_JsonArray*` | Añadir cadena |
| `AddNumber(float)` | `UAIChatPlus_JsonArray*` | Añadir número |
| `AddInteger(int32)` | `UAIChatPlus_JsonArray*` | Añadir entero |
| `AddBoolean(bool)` | `UAIChatPlus_JsonArray*` | Agregar booleano |
| `AddObject(UAIChatPlus_JsonObject*)` | `UAIChatPlus_JsonArray*` | Añadir objeto |
| `AddArray(UAIChatPlus_JsonArray*)` | `UAIChatPlus_JsonArray*` | Agregar array |
| `AddNull()` | `UAIChatPlus_JsonArray*` | Añadir valor nulo |

**Métodos para obtener elementos:**

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `GetString(int32, const FString&, bool&)` | `FString` | Obtener cadena |
| `GetNumber(int32, float, bool&)` | `float` | Obtener número |
| `GetInteger(int32, int32, bool&)` | `int32` | Obtener entero |
| `GetBoolean(int32, bool, bool&)` | `bool` | Obtener booleano |
| `GetObject(int32, bool&)` | `UAIChatPlus_JsonObject*` | Obtener objeto |
| `GetArray(int32, bool&)` | `UAIChatPlus_JsonArray*` | Obtener array |

**Otros métodos:**

| Método | Tipo de Retorno | Descripción |
|------|---------|------|
| `Length()` | `int32` | Obtener longitud |
| `GetElementType(int32)` | `EAIChatPlus_JsonValueType` | Obtener el tipo de elemento |
| `SetString(int32, const FString&, bool&)` | `UAIChatPlus_JsonArray*` | Establecer cadena |
| `SetObject(int32, UAIChatPlus_JsonObject*, bool&)` | `UAIChatPlus_JsonArray*` | Establecer objeto |
| `RemoveAt(int32, bool&)` | `UAIChatPlus_JsonArray*` | Eliminar elemento |
| `Clear()` | `UAIChatPlus_JsonArray*` | Vacía el array |
| `ToString(bool)` | `FString` | Convertir a cadena |
| `Duplicate()` | `UAIChatPlus_JsonArray*` | Duplicar el arreglo |
| `IsValid()` | `bool` | Comprobar validez |

---

### UAIChatPlus_JsonLibrary

Librería estática de herramientas JSON.

**Archivo de cabecera:** `Common/Json/AIChatPlus_JsonLibrary.h`

**Métodos de creación:**

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `MakeJsonObjectWithStringField(const FString&, const FString&)` | `UAIChatPlus_JsonObject*` | Crear objeto con un solo campo |
| `MakeJsonObjectFromStringMap(const TMap<FString, FString>&)` | `UAIChatPlus_JsonObject*` | Crear objeto desde Map |

**Método de verificación:**

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `ValidateJsonString(const FString&, FString&)` | `bool` | Validar cadena JSON |
| `IsJsonObject(const FString&)` | `bool` | Comprueba si es un objeto |
| `IsJsonArray(const FString&)` | `bool` | Comprueba si es un arreglo |

**Métodos de formato:**

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `PrettifyJson(const FString&)` | `FString` | Embellecer JSON |
| `MinifyJson(const FString&)` | `FString` | Comprimir JSON |

**Conversión de estructuras (CustomThunk):**

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `JsonStringToStruct(const FString&, int32&)` | `bool` | Conversión de JSON a estructura |
| `StructToJsonString(const int32&, bool)` | `FString` | Estructura a JSON |

**Operación de archivos:**

| Método | Tipo de Retorno | Descripción |
|------|---------|------|
Here is the translation of the text into Spanish:

| `LoadJsonObjectFromFile(const FString&, bool&, FString&)` | `UAIChatPlus_JsonObject*` | Cargar objeto desde archivo |
| `SaveJsonObjectToFile(UAIChatPlus_JsonObject*, const FString&, bool, FString&)` | `bool` | Guardar objeto en archivo |
| `LoadJsonArrayFromFile(const FString&, bool&, FString&)` | `UAIChatPlus_JsonArray*` | Cargar un array desde un archivo |
| `SaveJsonArrayToFile(UAIChatPlus_JsonArray*, const FString&, bool, FString&)` | `bool` | Guardar un array en un archivo |

**Método de comparación:**

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `EqualsJsonObject(UAIChatPlus_JsonObject*, UAIChatPlus_JsonObject*)` | `bool` | Comparar objetos |
| `EqualsJsonArray(UAIChatPlus_JsonArray*, UAIChatPlus_JsonArray*)` | `bool` | Comparar arrays |

**Consulta de ruta:**

| Método | Tipo de retorno | Descripción |
|------|---------|------|
| `QueryStringByPath(UAIChatPlus_JsonObject*, const FString&, const FString&, FAIChatPlus_JsonQueryResult&)` | `FString` | Consultar cadena por ruta |
| `QueryObjectByPath(UAIChatPlus_JsonObject*, const FString&, FAIChatPlus_JsonQueryResult&)` | `UAIChatPlus_JsonObject*` | Consultar objeto por ruta |
| `QueryArrayByPath(UAIChatPlus_JsonObject*, const FString&, FAIChatPlus_JsonQueryResult&)` | `UAIChatPlus_JsonArray*` | Consultar array por ruta |

--8<-- "footer_es.md"


> Esta publicación ha sido traducida utilizando ChatGPT. Por favor, brinda tu [**retroalimentación**](https://github.com/disenone/wiki_blog/issues/new)Procederemos a señalar cualquier omisión en el texto. 
