---
layout: post
title: UE realizar la lectura de imágenes del sistema local
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
- UE Editor
- UE Plugin
- UE Image
- UE Load Image
- UE Load File
description: UE implementa la lectura de imágenes del sistema local.
---

<meta property="og:title" content="UE 实现读取本地系统图片" />

#Implementación de la lectura de imágenes del sistema local a UTexture2D.

> Las siguientes líneas de código están basadas en la versión 5.3 de UE.

##Método genérico

Este método es válido tanto en el modo Editor como en el modo Juego, admite formatos de archivos de imagen como PNG, JPEG, BMP, ICO, EXR, ICNS, HDR, TIFF, DDS, TGA, y en general cubre la mayoría de los tipos de imágenes comunes.

El código también es muy limpio:

```cpp
#include <Engine/Texture2D.h>
#include <ImageUtils.h>

UTexture2D* LoadImage(const FString& InLoadPath)
{
	FImage ImageInfo;
	FImageUtils::LoadImage(*InLoadPath, ImageInfo);
	return FImageUtils::CreateTexture2DFromImage(ImageInfo);
}

```

El resultado es UTexture2D.

##Método exclusivo para editores

Este método puede admitir tipos adicionales de imágenes: texturas UDIM, archivos IES, PCX, PSD.

La implementación del código será un poco más complicada:

```cpp
#include <Engine/Texture2D.h>
#include <Misc/FileHelper.h>
#include <Misc/Paths.h>
#include <UObject/UObjectGlobals.h>

#if WITH_EDITOR
UTexture2D* LoadImage(const FString& InLoadPath)
{

	TArray64<uint8> Buffer;
	if (!FFileHelper::LoadFileToArray(Buffer, *InLoadPath))
	{
		return nullptr;
	}

	const FString TextureName;
	const FString Extension = FPaths::GetExtension(InLoadPath).ToLower();
	const uint8* BufferPtr = Buffer.GetData();

	auto TextureFact = NewObject<UTextureFactory>();
	UTexture2D* Ret = Cast<UTexture2D>(TextureFact->FactoryCreateBinary(
		UTexture2D::StaticClass(), GetTransientPackage(), *TextureName, RF_Transient,
		NULL, *Extension, BufferPtr, BufferPtr + Buffer.Num(), GWarn));

	return Ret;
}
#endif
```

La implementación se realizó utilizando la función FactoryCreateBinary de UTextureFactory, la cual puede leer los tipos de archivo adicionales mencionados anteriormente.

##Código fuente

Para obtener más detalles del código fuente, puedes encontrar el complemento en la tienda de UE: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)


--8<-- "footer_en.md"



> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
