---
layout: post
title: UE 实现读取本地系统图片
tags: [dev, game, UE, UnreanEngine, UE4, UE5, UE Editor, UE Plugin, UE Image, UE Load Image, UE Load File]
description: UE 实现读取本地系统图片
---
<meta property="og:title" content="UE 实现读取本地系统图片" />

# UE 实现读取本地系统图片为 UTexture2D

> 以下代码都是以 UE5.3 版本为例。

## 通用方法

本方法在 编辑器 和 GamePlay 模式下都可行，支持的图片文件格式有 PNG, JPEG, BMP, ICO, EXR, ICNS, HDR, TIFF, DDS, TGA，基本能覆盖大部分的常用图片类型。

代码也很简洁：

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

返回的即是 UTexture2D。

## 编辑器专用方法

本方法可以额外支持更多的图片类型：UDIM 纹理贴图、IES 文件、PCX 、PSD。

代码实现上会更复杂一些：

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

实现是使用了 UTextureFactory 的 FactoryCreateBinary 函数，这个函数能够读取前面提到的额外文件类型。

## 源码

更多源码细节可在 UE 商城获取插件：[AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)


--8<-- "footer.md"

