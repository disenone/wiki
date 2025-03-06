---
layout: post
title: UE에서는 각종 이미지 (UTexture2D) 작업을 수행할 수 있습니다 (로드, 저장, 복사, 클립보드...).
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
- Copy
- Save
- Clipboard
description: UE는 로컬 시스템 이미지를 읽는 기능을 구현합니다.
---

<meta property="og:title" content="UE 实现读取本地系统图片" />

#UE에서는 다양한 이미지(UTexture2D) 작업을 수행할 수 있습니다 (로드, 저장, 복사, 클립보드...).

> 아래 코드는 UE5.3 버전을 기준으로 합니다.

##원본 코드

UE 스토어에서 플러그인 [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##이 텍스트를 한국어로 번역하시겠습니까?

###범용 방법

이 방법은 편집기 및 GamePlay 모드에서 모두 작동하며 지원하는 이미지 파일 형식은 PNG, JPEG, BMP, ICO, EXR, ICNS, HDR, TIFF, DDS, TGA로 대부분의 일반 이미지 유형을 기본적으로 처리할 수 있습니다.

소스 코드도 매우 간결합니다:

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

반환되는 것은 UTexture2D입니다.

###에디터 전용 메소드

이 방법은 더 많은 이미지 유형을 추가로 지원할 수 있습니다: UDIM 텍스처 맵, IES 파일, PCX, PSD.

코드 구현 부분은 조금 더 복잡해질 것입니다:

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

실제로는 UTextureFactory의 FactoryCreateBinary 함수를 사용하여 구현되었습니다. 이 함수는 이전에 언급된 추가 파일 유형을 읽을 수 있습니다.

##복사: UE에서 UTexture2D를 복사합니다.

가끔은 UTexture2D를 복제하여 복제된 이미지를 수정해야 할 때가 있습니다. 이미지를 복제하려면 엔진의 내장 함수 'FImageCore::CopyImage'를 사용해야 합니다. 두 이미지의 매개변수를 설정하고 이 인터페이스를 호출하면 됩니다.

```cpp
UTexture2D* CopyTexture2D(UTexture2D* InTexture, UObject* Outer, FName Name, EObjectFlags Flags)
{
	// src texture info, src ImageView
	FTextureMipDataLockGuard InTextureGuard(InTexture);
	uint8* SrcMipData = InTextureGuard.Lock(LOCK_READ_ONLY);        // Texture->GetPlatformData()->Mips[0].BulkData.Lock(InLockFlag)
	const int32 InSizeX = InTexture->GetSizeX();
	const int32 InSizeY = InTexture->GetSizeY();
	const EPixelFormat InFormat = InTexture->GetPixelFormat();
	const FImageView SrcMipImage(
		SrcMipData, InSizeX, InSizeY, 1, GetRawImageFormat(InFormat), InTexture->GetGammaSpace());

	// create dst texture
	UTexture2D* NewTexture = NewObject<UTexture2D>(Outer, Name, Flags);
	NewTexture->SetPlatformData(new FTexturePlatformData());
	NewTexture->GetPlatformData()->SizeX = InSizeX;
	NewTexture->GetPlatformData()->SizeY = InSizeY;
	NewTexture->GetPlatformData()->SetNumSlices(1);
	NewTexture->GetPlatformData()->PixelFormat = InFormat;

	// Allocate first mipmap.
	int32 NumBlocksX = InSizeX / GPixelFormats[InFormat].BlockSizeX;
	int32 NumBlocksY = InSizeY / GPixelFormats[InFormat].BlockSizeY;
	FTexture2DMipMap* Mip = new FTexture2DMipMap();
	Mip->SizeX = InSizeX;
	Mip->SizeY = InSizeY;
	Mip->SizeX = 1;
	NewTexture->GetPlatformData()->Mips.Add(Mip);
	Mip->BulkData.Lock(LOCK_READ_WRITE);
	Mip->BulkData.Realloc((int64)NumBlocksX * NumBlocksY * GPixelFormats[InFormat].BlockBytes);
	Mip->BulkData.Unlock();

	// dst texture ImageView
	uint8* DstMipData = static_cast<uint8*>(NewTexture->GetPlatformData()->Mips[0].BulkData.Lock(LOCK_READ_WRITE));
	const FImageView DstMipImage(
		DstMipData, InSizeX, InSizeY, 1, GetRawImageFormat(InFormat), InTexture->GetGammaSpace());

	// run CopyImage
	FImageCore::CopyImage(SrcMipImage,DstMipImage);

#if WITH_EDITORONLY_DATA
	NewTexture->Source.Init(
		InSizeX, InSizeY, 1, 1,
		FImageCoreUtils::ConvertToTextureSourceFormat(GetRawImageFormat(InFormat)), DstMipData);
#endif

	// cleanup
	NewTexture->GetPlatformData()->Mips[0].BulkData.Unlock();
	NewTexture->UpdateResource();

	return NewTexture;
}
```

##저장: UE에서 UTexture2D를 파일로 저장하는 기능을 구현하세요.

핵심은 엔진 함수 'FImageUtils::SaveImageAutoFormat'를 사용하여 구현하는 것은 꽤 간단하지만 실패 시 재시도를 주의해야 합니다.

```cpp
void SaveImage(UTexture2D* InImage, const FString& InSavePath)
{
	if (!InImage) return;
	FImage ImageInfo;
	if (FImageUtils::GetTexture2DSourceImage(InImage, ImageInfo))
	{
		FImageUtils::SaveImageAutoFormat(*InSavePath, ImageInfo);
	}
	else
	{
		// if prev save failed
		// use ConvertTextureToStandard to change InImage to Standard format, and try again
		// then revert InImage's origin format
		// this is what FTextureMipDataLockGuard does
		FTextureMipDataLockGuard InImageGuard(InImage);

		uint8* MipData = InImageGuard.Lock(LOCK_READ_ONLY);
		check( MipData != nullptr );

		const FImageView MipImage(
			MipData, InImage->GetSizeX(), InImage->GetSizeY(), 1,
			GetRawImageFormat(InImage->GetPixelFormat()), InImage->GetGammaSpace());

		FImageUtils::SaveImageAutoFormat(*InSavePath, MipImage);
	}
}
```

##저장: UE에서 UTexture2D를 에셋으로 저장합니다.

내부 메모리에 있는 UTexture2D를 에셋으로 저장하고 콘텐츠 브라우저(Content Browser)에서 확인할 수 있습니다.

핵심 함수에서는 이전에 구현한 `CopyTexture2D`를 사용해야 합니다. 먼저 새 이미지를 복사한 다음 `UPackage::SavePackage`를 호출하여 이미지가 있는 패키지를 Asset으로 저장해야 합니다.

```cpp

void SaveTextureToAsset(UTexture2D* InTexture)
{
	if (!InTexture) return;

	// open save asset dialog, choose where/which to save
	FSaveAssetDialogConfig SaveAssetDialogConfig;

	SaveAssetDialogConfig.DefaultPath =  FEditorDirectories::Get().GetLastDirectory(ELastDirectory::NEW_ASSET);
	SaveAssetDialogConfig.AssetClassNames.Add(UTexture2D::StaticClass()->GetClassPathName());
	SaveAssetDialogConfig.ExistingAssetPolicy = ESaveAssetDialogExistingAssetPolicy::AllowButWarn;
	SaveAssetDialogConfig.DialogTitleOverride = FAIChatPlusEditor_Constants::FCText::SaveAsAsset;

	const FContentBrowserModule& ContentBrowserModule = FModuleManager::LoadModuleChecked<FContentBrowserModule>("ContentBrowser");
	const FString SaveObjectPath = ContentBrowserModule.Get().CreateModalSaveAssetDialog(SaveAssetDialogConfig);

	if (SaveObjectPath.IsEmpty()) return;

	// init save info
	const FString PackageName = FPackageName::ObjectPathToPackageName(SaveObjectPath);
	const FString PackageFileName = FPackageName::LongPackageNameToFilename(PackageName, FPackageName::GetAssetPackageExtension());
	const FString PackagePath = FPaths::GetPath(PackageFileName);
	const FString TextureName = FPaths::GetBaseFilename(PackageName);

	// create new UPackage to put the new texture in
	UPackage* const NewPackage = CreatePackage(*PackageName);
	NewPackage->FullyLoad();

	// copy texture
	UTexture2D* NewTexture = UAIChatPlus_Util::CopyTexture2D(
		InTexture, NewPackage, FName(TextureName), RF_Public | RF_Standalone | RF_Transactional);

	// Generate the thumbnail
	// if not doing so, the texture will not have thumbnail in content browser
	FObjectThumbnail NewThumbnail;
	ThumbnailTools::RenderThumbnail(
		NewTexture, NewTexture->GetSizeX(), NewTexture->GetSizeY(),
		ThumbnailTools::EThumbnailTextureFlushMode::NeverFlush, NULL,
		&NewThumbnail);
	ThumbnailTools::CacheThumbnail(NewTexture->GetFullName(), &NewThumbnail, NewPackage);

	// setting up new package and new texture
	NewPackage->MarkPackageDirty();
	FAssetRegistryModule::AssetCreated(NewTexture);
	FEditorDirectories::Get().SetLastDirectory(ELastDirectory::NEW_ASSET, FPaths::GetPath(PackageName));

	// save args
	FSavePackageArgs SaveArgs;
	SaveArgs.TopLevelFlags = RF_Public | RF_Standalone;
	SaveArgs.bForceByteSwapping = true;
	SaveArgs.bWarnOfLongFilename = true;

	// save it
	if (!UPackage::SavePackage(NewPackage, NewTexture, *PackageFileName, SaveArgs))
	{
		UE_LOG(AIChatPlusEditor, Error, TEXT("Failed to save Asset: [%s]\n"), *PackageFileName);
	}
}
```

##클립보드: UE에서 Windows 클립보드로 이미지(UTexture2D)를 복사하는 것을 구현합니다.

###윈도우 관련 함수

다음과 같은 Windows 클립보드 관련 함수를 사용할 것입니다:

* [OpenClipboard](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-openclipboard)클립 보드를 열고 클립 보드의 핸들러를 가져옵니다.
* [EmptyClipboard](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-emptyclipboard)현재 클립 보드를 지우고, 클립 보드의 모든 권한을 현재 창에 할당하십시오.
* [SetClipboardData](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-setclipboarddata)클립보드 데이터 및 이미지 데이터는 이 인터페이스를 통해 전송됩니다.
* [CloseClipboard](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-closeclipboard)데이터를 설정한 뒤 클립 보드를 닫으십시오.

###클립보드의 이미지 형식

(https://learn.microsoft.com/zh-cn/windows/win32/dataxchg/standard-clipboard-formats)내부에는 사용 가능한 클립 보드 형식이 소개되어 있으며, 그 중 `CF_DIBV5`은 이미지를 설정하는 데 사용할 수 있습니다.

CF_DIBV5에서 요구하는 형식은 구체적으로 정의되어 있습니다 [BITMAPV5HEADER 구조](https://learn.microsoft.com/zh-cn/windows/win32/api/wingdi/ns-wingdi-bitmapv5header)여기서는 다음 구성을 선택합니다.

```cpp
BITMAPV5HEADER Header;
Header.bV5CSType        = LCS_sRGB;
Header.bV5Compression   = BI_BITFIELDS;
```

###UTexture2D 설정

위에서 우리가 복사한 이미지의 색 공간은 `LCS_sRGB`로 선택했는데, 즉 sRGB 색 공간입니다. 따라서 UTexture2D도 해당 형식으로 먼저 설정해야 합니다:

```cpp
bool ConvertTextureToStandard(UTexture2D* InTexture)
{
	if (InTexture->CompressionSettings != TC_VectorDisplacementmap)
	{
		InTexture->CompressionSettings = TC_VectorDisplacementmap;
		IsChanged = true;
	}
	if (InTexture->SRGB != true)
	{
		InTexture->SRGB = true;
		IsChanged = true;
	}
	if (IsChanged)
	{
		InTexture->UpdateResource();
	}
}
```

ConvertTextureToStandard 함수는 UTexture2D를 TC_VectorDisplacementmap (RGBA8) 및 SRGB 색 공간으로 변환하는 역할을 합니다. UTexture2D 및 Windows 클립 보드의 이미지 형식을 맞춘 후 이미지 데이터를 클립 보드로 복사할 수 있습니다.

###구체적인 코드

```cpp
void CopyTexture2DToClipboard(UTexture2D* InTexture)
{
	if (!InTexture) return;

	FTextureMipDataLockGuard InTextureGuard(InTexture);
	// get InTexture info
	uint8* SrcMipData = InTextureGuard.Lock(LOCK_READ_ONLY);
	const int32 InSizeX = InTexture->GetSizeX();
	const int32 InSizeY = InTexture->GetSizeY();
	const EPixelFormat InFormat = InTexture->GetPixelFormat();
	const FImageView SrcMipImage(
		SrcMipData, InSizeX, InSizeY, 1, GetRawImageFormat(InTexture), InTexture->GetGammaSpace());

	// set clipboard Texture info
	const EPixelFormat OutFormat = PF_B8G8R8A8;
	const int32 NumBlocksX = InSizeX / GPixelFormats[OutFormat].BlockSizeX;
	const int32 NumBlocksY = InSizeY / GPixelFormats[OutFormat].BlockSizeY;
	const int64 BufSize = static_cast<int64>(NumBlocksX) * NumBlocksY * GPixelFormats[InFormat].BlockBytes;

	// set header info
	BITMAPV5HEADER Header;
	Header.bV5Size          = sizeof(BITMAPV5HEADER);
	Header.bV5Width         = InSizeX;
	Header.bV5Height        = -InSizeY;
	Header.bV5Planes        = 1;
	Header.bV5BitCount      = 32;
	Header.bV5Compression   = BI_BITFIELDS;
	Header.bV5SizeImage		= BufSize;
	Header.bV5XPelsPerMeter = 0;
	Header.bV5YPelsPerMeter = 0;
	Header.bV5ClrUsed       = 0;
	Header.bV5ClrImportant  = 0;
	Header.bV5RedMask       = 0x00FF0000;
	Header.bV5GreenMask     = 0x0000FF00;
	Header.bV5BlueMask      = 0x000000FF;
	Header.bV5AlphaMask     = 0xFF000000;
	Header.bV5CSType        = LCS_sRGB;
	// Header.bV5Endpoints;    // ignored
	Header.bV5GammaRed      = 0;
	Header.bV5GammaGreen    = 0;
	Header.bV5GammaBlue     = 0;
	Header.bV5Intent        = 0;
	Header.bV5ProfileData   = 0;
	Header.bV5ProfileSize   = 0;
	Header.bV5Reserved      = 0;

	HGLOBAL WinBuf = GlobalAlloc(GMEM_MOVEABLE, sizeof(BITMAPV5HEADER) + BufSize);
	if (WinBuf == NULL)
		return;

	HWND WinHandler = GetActiveWindow();
	if (!OpenClipboard(WinHandler)) {
		GlobalFree(WinBuf);
		return;
	}
	verify(EmptyClipboard());

	// copy InTexture into BGRA8 sRGB Standard Texture
	FTexture2DMipMap* DstMip = new FTexture2DMipMap();
	DstMip->SizeX = InSizeX;
	DstMip->SizeY = InSizeY;
	DstMip->SizeZ = 1;
	DstMip->BulkData.Lock(LOCK_READ_WRITE);
	uint8* DstMipData = static_cast<uint8*>(DstMip->BulkData.Realloc(BufSize));
	const FImageView DstMipImage(
		DstMipData, InSizeX, InSizeY, 1, ERawImageFormat::BGRA8, EGammaSpace::sRGB);

	FImageCore::CopyImage(SrcMipImage,DstMipImage);
	DstMip->BulkData.Unlock();

	// copy Standard Texture data into Clipboard
	void * WinLockedBuf = GlobalLock(WinBuf);
	if (WinLockedBuf) {
		memcpy(WinLockedBuf, &Header, sizeof(BITMAPV5HEADER));
		memcpy((char*)WinLockedBuf + sizeof(BITMAPV5HEADER), DstMipData, BufSize);
	}
	GlobalUnlock(WinLockedBuf);

	if (!SetClipboardData(CF_DIBV5, WinBuf))
	{
		UE_LOG(AIChatPlus_Internal, Fatal, TEXT("SetClipboardData failed with error code %i"), (uint32)GetLastError() );
	}

	// finish, close clipboard
	verify(CloseClipboard());

	delete DstMip;
}
```

###UTexture2D와 Base64 간의 변환

이 구현은 상대적으로 간단합니다. 직접 코드를 작성하세요.

```cpp
#include <Misc/Base64.h>
#include <ImageUtils.h>

UTexture2D* B64ToImage(const FString& B64)
{
	TArray<uint8> Data;
	FBase64::Decode(B64, Data);
	return FImageUtils::ImportBufferAsTexture2D(Data);
}

FString ImageToB64(UTexture2D* InTexture, const int32 InQuality)
{
	FTextureMipDataLockGuard InTextureGuard(InTexture);

	uint8* MipData = InTextureGuard.Lock(LOCK_READ_ONLY);
	check(MipData != nullptr);

	const FImageView InImage(
		MipData, InTexture->GetSizeX(), InTexture->GetSizeY(), 1,
		GetRawImageFormat(InTexture->GetPixelFormat()), InTexture->GetGammaSpace());

	TArray64<uint8> Buffer;
	FString Ret;
	if (FImageUtils::CompressImage(Buffer, TEXT("png"), InImage, InQuality))
	{
		Ret = FBase64::Encode(Buffer.GetData(), Buffer.Num());
	}
	return Ret;
}

```


--8<-- "footer_ko.md"


> 이 포스트는 ChatGPT로 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)중요한 부분을 간과하지 마십시오. 
