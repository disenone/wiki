---
layout: post
title: UE achieves reading local system images.
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
description: Implement reading local system images in UE.
---

<meta property="og:title" content="UE 实现读取本地系统图片" />

#Realize reading local system images as UTexture2D

> The following code examples are based on version UE5.3.

##Universal Method

This method is feasible in both the editor and GamePlay modes, supporting image file formats such as PNG, JPEG, BMP, ICO, EXR, ICNS, HDR, TIFF, DDS, TGA, and can basically cover most common image types.

The code is also very clean:

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

The returned value is UTexture2D.

##Editor-specific methods

This method can additionally support more types of images: UDIM texture maps, IES files, PCX, PSD.

The implementation of the code will be more complex:

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

The implementation uses the FactoryCreateBinary function of UTextureFactory, which is capable of reading the additional file types mentioned earlier.

##Source code

For more source code details, you can obtain the plugin from the UE marketplace: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)


--8<-- "footer_en.md"



> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
