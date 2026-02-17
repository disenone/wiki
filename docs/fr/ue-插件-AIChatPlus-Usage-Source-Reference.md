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

#Référence des API - Chapitre C++

Ce document fournit des références API en C++ pour l'extension AIChatPlus, incluant les descriptions de toutes les classes publiques, structures, énumérations et méthodes clés.

##Table des matières

- [Type énuméré](##枚举类型)
- [Classes de base fondamentales](##核心基类)
- [Classe Handler](##handler-类)
- [Classe Request](##request-类)
- [Utilitaires](##工具类)
[JSON Class](##json-类)

---

##Type énuméré

### EAIChatPlus_ChatApiProvider

Fournisseurs d'API de chat IA énumérés.

```cpp
enum class EAIChatPlus_ChatApiProvider : uint8
{
    OpenAI,         // OpenAI API
    Azure,          // Azure OpenAI API
    Claude,         // Anthropic Claude API
    Gemini,         // Google Gemini API
Ollama,         // Service local Ollama
Cllama,         // Appel direct à llama.cpp (obsolète)
CllamaServer    // Mode serveur de llama.cpp
};
```

### EAIChatPlus_ImageApiProvider

Fournisseurs d'API de génération d'images énumérés.

```cpp
enum class EAIChatPlus_ImageApiProvider : uint8
{
    OpenAI,   // OpenAI DALL-E
    Azure     // Azure OpenAI DALL-E
};
```

### EAIChatPlus_ChatRole

Enumération des rôles de message.

```cpp
enum class EAIChatPlus_ChatRole : uint8
{
Système,     // Instruction système (ancien modèle)
Utilisateur,       // Message utilisateur
Assistant, // Réponse IA
Développeur,  // Instruction pour le développeur (modèle o1+)
Outil        // Résultat de l'appel d'outil
};
```

### EAIChatPlus_ImageChatType

Enumération des types d'opérations sur les images.

```cpp
enum class EAIChatPlus_ImageChatType : uint8
{
Génération,  // Génération d'images
Éditer,        // Édition d'image
Variation    // Variante d'image
};
```

### EAIChatPlus_JsonValueType

Énumération des types de valeur JSON.

```cpp
enum class EAIChatPlus_JsonValueType : uint8
{
Aucun,     // Invalide
Null,     // Valeur nulle
String,   // Chaîne de caractères
Nombre,   // Numéro
Boolean, // Booléen
Tableau,    // Tableau
Objet    // 对象
};
```

---

##Classe de base centrale

### UAIChatPlus_RequestBase

La classe de base pour toutes les requêtes (classe abstraite).

**Méthodes clés :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `SendRequest()` | `bool` | Envoie une requête |
| `StopRequest()` | `void` | Arrêter la demande |
| `Activate()` | `void` | Active l'objet de requête |
| `IsActivated()` | `bool` | Vérifie si l'activation a été effectuée |
| `SetIsAutoDestroy(bool)` | `void` | Définit la destruction automatique une fois terminé |

**Mandat :**

| Nom du mandant | Signature | Description |
|--------|------|------|
| `OnStartedListeners` | `void()` | Début de la demande |
| `OnMessageListeners` | `void(const FString&)` | Réception de messages en streaming |
| `OnFinishedListeners` | `void(const FAIChatPlus_PointerWrapper&)` | Requête terminée |
| `OnFailedListeners` | `void(const FAIChatPlus_PointerWrapper&)` | Requête échouée |

---

### UAIChatPlus_ChatRequestBase

Classe de base pour les requêtes de chat, héritant de `UAIChatPlus_RequestBase`.

**Méthodes de fabrique statiques :**

```cpp
// Créer une requête par Provider
static UAIChatPlus_ChatRequestBase* CreateByApi(EAIChatPlus_ChatApiProvider InApiProvider);
static UAIChatPlus_ChatRequestBase* CreateByApiInWorld(EAIChatPlus_ChatApiProvider InApiProvider, const UObject* InWorldContext);
```

**Méthodes clés :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `SetMessages(const TArray<FAIChatPlus_ChatRequestMessage>&)` | `void` | Définir la liste des messages |
| `GetFullUrl()` | `FString` | Obtient l'URL complète de la requête |
| `GetModelText()` | `FString` | Obtenir le nom du modèle |
| `GetTokenUsageText()` | `FString` | Obtenir la description de l'utilisation des jetons |
| `GetApiProvider()` | `EAIChatPlus_ChatApiProvider` | Obtient le type de API Provider |

---

### UAIChatPlus_ImageRequestBase

Classe de base pour les requêtes d'images, héritant de `UAIChatPlus_RequestBase`.

**Méthodes de fabrique statiques :**

```cpp
static UAIChatPlus_ImageRequestBase* CreateByApi(EAIChatPlus_ImageApiProvider InApiProvider);
static UAIChatPlus_ImageRequestBase* CreateByApiInWorld(EAIChatPlus_ImageApiProvider InApiProvider, const UObject* InWorldContext);
```

**Méthodes clés :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `SetPrompt(const FString&)` | `void` | Définit le mot-clé de génération d'image |
| `SetImages(const TArray<UAIChatPlus_Texture*>&)` | `void` | Définir les images d'entrée (édition/variante) |
| `GetModelText()` | `FString` | Obtenir le nom du modèle |
| `GetStyleText()` | `FString` | Obtenir le nom du style |
| `GetRevisedPrompt()` | `FString` | Obtient le mot-clé révisé |
| `GetImageChatType()` | `FString` | Récupère le type d'opération sur l'image |

---

### UAIChatPlus_ModelRequestBase

Classe de base de demande de liste de modèles, héritant de `UAIChatPlus_RequestBase`.

**Méthodes de fabrique statiques :**

```cpp
static UAIChatPlus_ModelRequestBase* CreateByApi(EAIChatPlus_ChatApiProvider InApiProvider);
static UAIChatPlus_ModelRequestBase* CreateByApiInWorld(EAIChatPlus_ChatApiProvider InApiProvider, const UObject* InWorldContext);
```

---

##Classe Handler

### UAIChatPlus_HandlerBase

La classe de base pour tous les Handlers.

**Méthodes clés :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `SetIsAutoDestroy(bool)` | `void` | Définit la destruction automatique |
| `AutoDestroy()` | `void` | Exécute l'autodestruction |
Voici la traduction en français :

| `Destroy()` | `void` | Détruire immédiatement |

---

### UAIChatPlus_ChatHandlerBase

Gestionnaire de demande de chat, hérite de `UAIChatPlus_HandlerBase`.

**Méthodes de fabrique statiques :**

```cpp
static UAIChatPlus_ChatHandlerBase* New();
```

**Méthodes de liaison :**

| Méthode | Description |
|------|------|
`BindChatRequest(UAIChatPlus_ChatRequestBase*)` | Lier la demande de chat
| `BindImageRequest(UAIChatPlus_ImageRequestBase*)` | Associer une requête d'image |
| `BindModelRequest(UAIChatPlus_ModelRequestBase*)` | Liaison de la requête de modèle |
| `ClearDelegates()` | Efface toutes les liaisons de délégués |

**Mandat :**

| Nom du mandant | Signature | Description |
|--------|------|------|
| `OnStarted` | `void()` | Début de la requête |
| `OnStopped` | `void()` | Demande d'arrêt |
| `OnMessage` | `void(const FString&)` | Message en continu |
| `OnMessageFinished` | `void(const FAIChatPlus_MessageFinishedPayload&)` | Message terminée |
| `OnUpdated` | `void(const FAIChatPlus_PointerWrapper&)` | Demande de mise à jour |
| `OnFinished` | `void(const FAIChatPlus_PointerWrapper&)` | Requête terminée |
| `OnFailed` | `void(const FAIChatPlus_PointerWrapper&)` | Échec de la requête |
| `OnImages` | `void(const TArray<UTexture2D*>&, bool)` | Génération d'images |
| `OnModels` | `void(const TArray<FString>&)` | Liste des modèles |

---

### UAIChatPlus_CllamaServerHandler

Handler dédié à CllamaServer.

**Méthodes de fabrique statiques :**

```cpp
static UAIChatPlus_CllamaServerHandler* CreateHandler();
```

**Mandat :**

| Nom du mandat | Signature | Description |
|--------|------|------|
| `OnServerStarted` | `void(FGuid)` | Serveur démarré |
| `OnServerStopped` | `void(FGuid)` | Arrêt du serveur |
| `OnServerFailed` | `void(FGuid, const FString&)` | Serveur échoué |

---

##Classe Request

Toutes les classes Request des Providers suivent le même modèle de méthode usine :

###Modèle de méthode d'usine générique

```cpp
// Prenez OpenAI comme exemple, les autres fournisseurs sont similaires
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

###Méthodes statiques génériques

Toutes les classes Request fournissent la méthode `CastWrapperToResponse` pour la conversion de type :

```cpp
// Extraire les données de réponse depuis PointerWrapper
static FAIChatPlus_XXXResponseBody& CastWrapperToResponse(const FAIChatPlus_PointerWrapper& InWrapper);
static FAIChatPlus_PointerWrapper CastResponseToWrapper(const FAIChatPlus_XXXResponseBody& InResponse);
```

---

### UAIChatPlus_OpenAIChatRequest

Requêtes de discussion OpenAI.

**Fichier d'en-tête :** `Common_OpenAI/AIChatPlus_OpenAIChatRequest.h`

**Type d'Options :** `FAIChatPlus_OpenAIChatRequestOptions`

**Type de Réponse :** `FAIChatPlus_OpenAIChatResponseBody`

---

### UAIChatPlus_AzureChatRequest

Requête de discussion Azure OpenAI.

**En-tête :** `Common_Azure/AIChatPlus_AzureChatRequest.h`

**Type d'Options :** `FAIChatPlus_AzureChatRequestOptions`

**Type de réponse :** `FAIChatPlus_AzureChatResponseBody`

---

### UAIChatPlus_ClaudeChatRequest

Requête de conversation avec Claude.

**Fichier d'en-tête :** `Common_Claude/AIChatPlus_ClaudeChatRequest.h`

**Type des Options :** `FAIChatPlus_ClaudeChatRequestOptions`

**Type de réponse :** `FAIChatPlus_ClaudeChatResponseBody`

---

### UAIChatPlus_GeminiChatRequest

Demande de discussion Gemini.

**Fichier d'en-tête :** `Common_Gemini/AIChatPlus_GeminiChatRequest.h`

**Type d'options :** `FAIChatPlus_GeminiChatRequestOptions`

**Type de réponse :** `FAIChatPlus_GeminiChatResponseBody`

---

### UAIChatPlus_OllamaChatRequest

Requête de chat Ollama.

**Fichier d'en-tête :** `Common_Ollama/AIChatPlus_OllamaChatRequest.h`

**Type d'Options :** `FAIChatPlus_OllamaChatRequestOptions`

**Type de réponse :** `FAIChatPlus_OllamaChatResponseBody`

---

### UAIChatPlus_OllamaModelRequest

Demande de liste des modèles Ollama.

**Fichier d'en-tête :** `Common_Ollama/AIChatPlus_OllamaModelRequest.h`

**Type d'options :** `FAIChatPlus_OllamaModelRequestOptions`

**Type de réponse :** `FAIChatPlus_OllamaModelResponseBody`

**Méthodes uniques :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `GetModelNames()` | `TArray<FString>` | Obtenir la liste des noms de modèles |

---

###UAIChatPlus_CllamaChatRequest (obsolète)

Demande de discussion hors ligne Cllama (obsolète, CllamaServer est recommandé).

**Fichier d'en-tête :** `Common_Cllama/AIChatPlus_CllamaChatRequest.h`

**Type d'options :** `FAIChatPlus_CllamaChatRequestOptions`

**Type de réponse :** `FAIChatPlus_CllamaChatResponseBody`

---

### UAIChatPlus_CllamaServerChatRequest

Demande de discussion CllamaServer.

**Fichier d'en-tête :** `Common_CllamaServer/AIChatPlus_CllamaServerChatRequest.h`

**Type d'Options :** `FAIChatPlus_CllamaServerChatRequestOptions`

**Type de réponse :** `FAIChatPlus_CllamaServerChatResponseBody`

---

### UAIChatPlus_OpenAIImageRequest

Requête de génération d'images OpenAI.

**Fichier d'en-tête :** `Common_OpenAI/AIChatPlus_OpenAIImageRequest.h`

**Type d'Options :** `FAIChatPlus_OpenAIImageRequestOptions`

**Type de réponse :** `FAIChatPlus_OpenAIImageResponseBody`

---

### UAIChatPlus_AzureImageRequest

Demande de génération d'image Azure.

**Fichier d'en-tête :** `Common_Azure/AIChatPlus_AzureImageRequest.h`

**Type Options :** `FAIChatPlus_AzureImageRequestOptions`

**Type de réponse :** `FAIChatPlus_AzureImageResponseBody`

---

### UAIChatPlus_CllamaServer

Classe de gestion de serveur CllamaServer.

**Fichier d'en-tête :** `Common_CllamaServer/AIChatPlus_CllamaServer.h`

**Méthodes de fabrique statiques :**

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

**Méthodes d’instance :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `Activate()` | `void` | Démarrer le serveur |
| `StopServer()` | `void` | Arrête le serveur |
| `IsRunning()` | `bool` | Vérifie si c'est en cours d'exécution |
| `GetServerID()` | `FGuid` | Obtenir l'ID du serveur |
| `GetHost()` | `FString` | Obtient l'adresse de l'hôte |
| `GetAddress()` | `FString` | Obtenir l'adresse complète |
| `GetServerInfo(FAIChatPlus_CllamaServerInfo&)` | `bool` | Obtenir les informations du serveur |

**Méthodes de gestion statique :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `IsServerValid(const FGuid&)` | `bool` | Vérifie si le serveur est valide |
| `IsServerRunning(const FGuid&)` | `bool` | Vérifie si le serveur est en cours d'exécution |
| `StopServerByID(const FGuid&)` | `void` | Arrêter le serveur par ID |
| `StopAllServers()` | `void` | Arrêter tous les serveurs |
| `GetServerByID(const FGuid&)` | `UAIChatPlus_CllamaServer*` | Obtenir un serveur par ID |
| `GetAllServerIDs()` | `TArray<FGuid>` | Obtenir tous les IDs de serveur |

---

##Classe utilitaire

### UAIChatPlus_Util

Classe utilitaire générale, fournissant diverses méthodes d'assistance statiques.

**Fichier d'en-tête :** `Common/AIChatPlus_Util.h`

####Journalisation

| Méthode | Type de retour | Description |
|------|---------|------|
| `SetInternalLogVerbosity(EAIChatPlus_LogVerbosityType)` | `void` | Définit le niveau de verbosité des journaux internes |

####Conversion d'encapsulage

| Méthode | Type de retour | Description |
|------|---------|------|
| `CastWrapperToError(const FAIChatPlus_PointerWrapper&)` | `FAIChatPlus_ResponseErrorBase&` | Extraire les informations d'erreur |
| `CastWrapperToResponse(const FAIChatPlus_PointerWrapper&)` | `FAIChatPlus_ChatResponseBodyBase&` | Extraire les données de réponse |
| `GetErrorWrapperDescription(const FAIChatPlus_PointerWrapper&)` | `FString` | Obtenir la description de l'erreur |
| `GetResponseWrapperMessage(const FAIChatPlus_PointerWrapper&)` | `FString` | Obtenir le message de réponse |

####Outil d'image

| Méthode | Type de retour | Description |
|------|---------|------|
| `LoadImage(const FString&, bool)` | `UTexture2D*` | Charge une image depuis un fichier |
| `SaveImage(UTexture2D*, const FString&)` | `bool` | Sauvegarder l'image dans un fichier |
| `ImageToB64(UTexture2D*, int32)` | `FString` | Conversion d'image en Base64 |
| `CopyTexture2D(UTexture2D*, UObject*, FName, EObjectFlags)` | `UTexture2D*` | Copier la texture |
| `FitImageSize(const FVector2D&, const FVector2D&)` | `FVector2D` | Calcule la taille adaptée |
| `CopierTexture2DDansPressePapiers(UTexture2D*)` | `vide` | Copier dans le presse-papiers |
| `IsCanCopyTexture2DToClipboard()` | `bool` | Vérifie si la fonction est prise en charge |

####Outil audio

| Méthode | Type de retour | Description |
|------|---------|------|
| `LoadSoundWav(const FString&)` | `USoundWave*` | Charger un audio depuis un fichier |
| `SaveSoundWav(USoundWave*, const FString&)` | `bool` | Sauvegarder l'audio dans un fichier |
| `SoundToB64(USoundWave*)` | `FString` | Conversion audio en Base64 |
| `CopySoundWave(const USoundWave*, UObject*, FName)` | `USoundWave*` | Copie d'onde sonore |
| `WavDataToSoundWave(const TArray<uint8>&, bool, bool)` | `USoundWave*` | Conversion de données WAV en onde sonore |
| `GetSoundWavePCMData(USoundWave*)` | `TArray<uint8>` | Obtenir les données PCM |

####Outils JSON

| Méthode | Type de retour | Description |
|------|---------|------|
| `MergeJsonObjects(const FString&, const FString&)` | `FString` | Fusionner des chaînes JSON |
| `LoadJsonString(const FString&)` | `TSharedPtr<FJsonObject>` | Analyse une chaîne JSON |
| `ToJsonString(const TSharedPtr<FJsonObject>&)` | `FString` | Convertit en chaîne JSON |

####Outil Cllama

| Méthode | Type de retour | Description |
|------|---------|------|
| `Cllama_IsValid()` | `bool` | Vérifie si Cllama est disponible |
| `Cllama_IsSupportGpu()` | `bool` | Vérifie si le GPU est pris en charge |
| `Cllama_GetSupportBackends()` | `TArray<FString>` | Obtenir les backends pris en charge |
| `Cllama_PrepareModelPathFromPak(const FString&)` | `FString` | Préparer le chemin du modèle à partir du Pak |

####Informations sur le modèle

| Méthode | Type de retour | Description |
|------|---------|------|
| `GetOpenAIChatDefaultModels()` | `const TArray<FName>&` | Liste des modèles par défaut d'OpenAI |
| `GetOpenAIChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | Obtenir les informations sur le modèle OpenAI |
| `GetClaudeChatDefaultModels()` | `const TArray<FName>&` | Liste des modèles par défaut de Claude |
| `GetClaudeChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | Obtenir les informations du modèle Claude |
| `GetGeminiChatDefaultModels()` | `const TArray<FName>&` | Liste des modèles par défaut de Gemini |
| `GetGeminiChatModelInfo(const FString&)` | `FAIChatPlus_ChatModelInfo` | Obtenir les informations sur le modèle Gemini |

---

### UAIChatPlus_Texture

Classe d'emballage d'images, prenant en charge le chargement asynchrone et la conversion Base64.

**Fichier d'en-tête :** `Common/AIChatPlus_Texture.h`

**Méthodes de fabrique statiques :**

```cpp
static UAIChatPlus_Texture* New(UTexture2D* InTexture = nullptr, const FString& InSourcePath = "");
static UAIChatPlus_Texture* CreateInBlueprint(UObject* WorldContextObject, UTexture2D* InTexture);
```

**Méthode :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `LoadFromFile(const FString&)` | `bool` | Charger depuis un fichier (synchrone) |
| `LoadFromFileAsync(const FString&, Callback)` | `FLoadingTaskType*` | Charger depuis un fichier (asynchrone) |
| `LoadFromAsset(UObject*, const FString&)` | `bool` | Charger à partir d'un actif (synchrone) |
| `LoadFromAssetAsync(UObject*, Callback, const FString&)` | `FLoadingTaskType*` | Chargement depuis un actif (asynchrone) |
| `ToB64()` | `const FString&` | Convertit en Base64 (synchrone) |
| `ToB64Async(Callback)` | `FLoadingTaskType*` | Convertir en Base64 (asynchrone) |
| `GetBrush(bool)` | `const FSlateBrush*` | Obtenir le pinceau Slate |
| `GetBrushCopy(bool)` | `FSlateBrush` | Obtient une copie du pinceau |
| `GetSize()` | `FIntVector2` | Obtient les dimensions |
| `GetSize2D()` | `FVector2D` | Obtenir la taille (flottante) |
| `IsValid()` | `bool` | Vérifie si c'est valide |
| `IsLoading()` | `bool` | Vérifie si un chargement est en cours |
| `Reset()` | `void` | Réinitialiser |
| `WaitLoadingComplete()` | `void` | Attend que le chargement soit terminé |

---

### UAIChatPlus_Sound

Classe d'emballage audio, prenant en charge le chargement asynchrone et la conversion Base64.

**Fichier d'en-tête :** `Common/AIChatPlus_Sound.h`

**Méthodes d'usine statiques :**

```cpp
static UAIChatPlus_Sound* New(USoundWave* InSound = nullptr, const FString& InSourcePath = "");
static UAIChatPlus_Sound* CreateInBlueprint(UObject* WorldContextObject, USoundWave* InSound);
```

**Méthode :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `LoadFromFile(const FString&)` | `bool` | Chargement à partir d'un fichier (synchrone) |
| `LoadFromFileAsync(const FString&, Callback)` | `FLoadingTaskType*` | Chargement à partir d'un fichier (asynchrone) |
| `LoadFromAsset(UObject*, const FString&)` | `bool` | Charger depuis un actif (synchrone) |
| `LoadFromAssetAsync(UObject*, Callback, const FString&)` | `FLoadingTaskType*` | Chargement depuis un actif (asynchrone) |
| `ToB64()` | `const FString&` | Convertit en Base64 (synchrone) |
| `ToB64Async(Callback)` | `FLoadingTaskType*` | Convertir en Base64 (asynchrone) |
| `IsValid()` | `bool` | Vérifie si c'est valide |
| `IsLoading()` | `bool` | Vérifie si le chargement est en cours |
| `Reset()` | `void` | Réinitialiser |
| `WaitLoadingComplete()` | `void` | Attend la fin du chargement |
| `PlayInEditor()` | `void` | Joue dans l'éditeur |

---

##Classe JSON

### UAIChatPlus_JsonObject

Classe d'encapsulation d'objets JSON.

**Fichier d'en-tête :** `Common/Json/AIChatPlus_JsonObject.h`

**Méthodes de fabrique statiques :**

```cpp
static UAIChatPlus_JsonObject* Create();
static UAIChatPlus_JsonObject* Parse(const FString& JsonString, bool& bSuccess, FString& ErrorMessage);
static UAIChatPlus_JsonObject* FromStruct(const int32& Struct);  // CustomThunk
```

**Méthodes de configuration des champs (prise en charge de l'enchaînement d'appels) :**

| Méthode      | Type de retour | Description            |
|------|---------|------|
| `SetStringField(const FString&, const FString&)` | `UAIChatPlus_JsonObject*` | Définir un champ de chaîne de caractères |
| `SetNumberField(const FString&, float)` | `UAIChatPlus_JsonObject*` | Définir un champ numérique |
| `SetIntegerField(const FString&, int32)` | `UAIChatPlus_JsonObject*` | Définir un champ entier |
| `SetBooleanField(const FString&, bool)` | `UAIChatPlus_JsonObject*` | Définir un champ booléen |
| `SetObjectField(const FString&, UAIChatPlus_JsonObject*)` | `UAIChatPlus_JsonObject*` | Définir un champ d'objet |
| `SetArrayField(const FString&, UAIChatPlus_JsonArray*)` | `UAIChatPlus_JsonObject*` | Définir un champ de tableau |
| `SetNullField(const FString&)` | `UAIChatPlus_JsonObject*` | Définir un champ nul |

**Méthodes d'obtention des champs :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `GetStringField(const FString&, const FString&, bool&)` | `FString` | Obtenir une chaîne de caractères |
| `GetNumberField(const FString&, float, bool&)` | `float` | Obtenir un nombre |
| `GetIntegerField(const FString&, int32, bool&)` | `int32` | Obtenir un entier |
| `GetBooleanField(const FString&, bool, bool&)` | `bool` | Obtenir un booléen |
| `GetObjectField(const FString&, bool&)` | `UAIChatPlus_JsonObject*` | Récupérer l'objet |
| `GetArrayField(const FString&, bool&)` | `UAIChatPlus_JsonArray*` | Obtenir un tableau |

**Autres méthodes :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `HasField(const FString&)` | `bool` | Vérifie l'existence du champ |
| `GetFieldType(const FString&)` | `EAIChatPlus_JsonValueType` | Obtenir le type du champ |
| `RemoveField(const FString&)` | `UAIChatPlus_JsonObject*` | Supprimer le champ |
| `Clear()` | `UAIChatPlus_JsonObject*` | Vide tous les champs |
| `ToString(bool)` | `FString` | Convertir en chaîne de caractères |
| `ToStruct(int32&)` | `bool` | Convertir en structure |
Voici la traduction en français :

| `Merge(UAIChatPlus_JsonObject*, bool)` | `UAIChatPlus_JsonObject*` | Fusionner des objets |
| `Duplicate()` | `UAIChatPlus_JsonObject*` | Dupliquer l'objet |
| `IsValid()` | `bool` | Vérifie la validité |

**Méthode de recherche de chemin :**

| Méthode | Type retourné | Description |
|------|---------|------|
| `SetStringByPath(const FString&, const FString&, const FAIChatPlus_JsonPathOptions&)` | `UAIChatPlus_JsonObject*` | Définir une chaîne par chemin |
| `GetStringByPath(const FString&, const FString&, FAIChatPlus_JsonQueryResult&)` | `FString` | Obtenir une chaîne par chemin |

---

### UAIChatPlus_JsonArray

Classe wrapper pour les tableaux JSON.

**Fichier d'en-tête :** `Common/Json/AIChatPlus_JsonArray.h`

**Méthodes de fabrique statiques :**

```cpp
static UAIChatPlus_JsonArray* Create();
static UAIChatPlus_JsonArray* Parse(const FString& JsonString, bool& bSuccess, FString& ErrorMessage);
static UAIChatPlus_JsonArray* FromStringArray(const TArray<FString>& Values);
static UAIChatPlus_JsonArray* FromIntegerArray(const TArray<int32>& Values);
```

**Méthode d'ajout d'éléments (supporte les appels chaînés) :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `AddString(const FString&)` | `UAIChatPlus_JsonArray*` | Ajouter une chaîne de caractères |
| `AddNumber(float)` | `UAIChatPlus_JsonArray*` | Ajouter un nombre |
| `AddInteger(int32)` | `UAIChatPlus_JsonArray*` | Ajouter un entier |
Voici la traduction en français :

| `AddBoolean(bool)` | `UAIChatPlus_JsonArray*` | Ajouter un booléen |
| `AddObject(UAIChatPlus_JsonObject*)` | `UAIChatPlus_JsonArray*` | Ajouter un objet |
| `AddArray(UAIChatPlus_JsonArray*)` | `UAIChatPlus_JsonArray*` | Ajouter un tableau |
| `AddNull()` | `UAIChatPlus_JsonArray*` | Ajouter une valeur nulle |

**Méthodes d'obtention d'éléments :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `GetString(int32, const FString&, bool&)` | `FString` | Obtenir une chaîne de caractères |
| `GetNumber(int32, float, bool&)` | `float` | Obtenir un nombre |
| `GetInteger(int32, int32, bool&)` | `int32` | Obtenir un entier |
| `GetBoolean(int32, bool, bool&)` | `bool` | Obtenir un booléen |
| `GetObject(int32, bool&)` | `UAIChatPlus_JsonObject*` | Obtenir l'objet |
| `GetArray(int32, bool&)` | `UAIChatPlus_JsonArray*` | Obtenir un tableau |

**Autres méthodes :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `Length()` | `int32` | Obtenir la longueur |
| `GetElementType(int32)` | `EAIChatPlus_JsonValueType` | Obtient le type d'élément |
| `SetString(int32, const FString&, bool&)` | `UAIChatPlus_JsonArray*` | Définir une chaîne de caractères |
| `SetObject(int32, UAIChatPlus_JsonObject*, bool&)` | `UAIChatPlus_JsonArray*` | Définir un objet |
| `RemoveAt(int32, bool&)` | `UAIChatPlus_JsonArray*` | Supprimer un élément |
| `Clear()` | `UAIChatPlus_JsonArray*` | Vide le tableau |
| `ToString(bool)` | `FString` | Convertir en chaîne de caractères |
| `Duplicate()` | `UAIChatPlus_JsonArray*` | Dupliquer le tableau |
| `IsValid()` | `bool` | Vérifie la validité |

---

### UAIChatPlus_JsonLibrary

Bibliothèque utilitaire statique JSON.

**Fichier d'en-tête :** `Common/Json/AIChatPlus_JsonLibrary.h`

**Méthode de création :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `MakeJsonObjectWithStringField(const FString&, const FString&)` | `UAIChatPlus_JsonObject*` | Créer un objet avec un seul champ |
| `MakeJsonObjectFromStringMap(const TMap<FString, FString>&)` | `UAIChatPlus_JsonObject*` | Crée un objet depuis une Map |

**Méthode de vérification :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `ValidateJsonString(const FString&, FString&)` | `bool` | Valider une chaîne JSON |
| `IsJsonObject(const FString&)` | `bool` | Vérifie si c'est un objet |
| `IsJsonArray(const FString&)` | `bool` | Vérifie si c'est un tableau |

**Méthodes de formatage :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `PrettifyJson(const FString&)` | `FString` | Embelli JSON |
Here is the translation:

| `MinifyJson(const FString&)` | `FString` | Minifier le JSON |

**Conversion de structure (CustomThunk) :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `JsonStringToStruct(const FString&, int32&)` | `bool` | Conversion JSON vers structure |
| `StructToJsonString(const int32&, bool)` | `FString` | Conversion de structure en JSON |

**Manipulation de fichiers :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `LoadJsonObjectFromFile(const FString&, bool&, FString&)` | `UAIChatPlus_JsonObject*` | Charger un objet depuis un fichier |
| `SaveJsonObjectToFile(UAIChatPlus_JsonObject*, const FString&, bool, FString&)` | `bool` | Sauvegarder l'objet dans un fichier |
| `LoadJsonArrayFromFile(const FString&, bool&, FString&)` | `UAIChatPlus_JsonArray*` | Charger un tableau à partir d'un fichier |
| `SaveJsonArrayToFile(UAIChatPlus_JsonArray*, const FString&, bool, FString&)` | `bool` | Sauvegarde un tableau dans un fichier |

**Méthode de comparaison :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `EqualsJsonObject(UAIChatPlus_JsonObject*, UAIChatPlus_JsonObject*)` | `bool` | Comparer les objets |
| `EqualsJsonArray(UAIChatPlus_JsonArray*, UAIChatPlus_JsonArray*)` | `bool` | Compare des tableaux |

**Recherche de chemin :**

| Méthode | Type de retour | Description |
|------|---------|------|
| `QueryStringByPath(UAIChatPlus_JsonObject*, const FString&, const FString&, FAIChatPlus_JsonQueryResult&)` | `FString` | Interroger une chaîne par chemin |
| `QueryObjectByPath(UAIChatPlus_JsonObject*, const FString&, FAIChatPlus_JsonQueryResult&)` | `UAIChatPlus_JsonObject*` | Requête d'objet par chemin |
| `QueryArrayByPath(UAIChatPlus_JsonObject*, const FString&, FAIChatPlus_JsonQueryResult&)` | `UAIChatPlus_JsonArray*` | Requête de tableau par chemin |

--8<-- "footer_fr.md"


> Ce message a été traduit par ChatGPT. Veuillez nous faire part de vos [**retours**](https://github.com/disenone/wiki_blog/issues/new)Signaler tout oubli relevé. 
