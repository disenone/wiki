---
layout: post
title: UE 實現各種圖片 (UTexture2D) 操作（讀取、保存、複製、剪貼板...）
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
description: UE 實現讀取本地系統圖片
---

<meta property="og:title" content="UE 实现读取本地系统图片" />

#UE 實現各種圖片 (UTexture2D) 操作（讀取、儲存、複製、剪貼板...）

> 以下程式碼都是以 UE5.3 版本為例。

##Source code

您可以在UE商城获取[AiChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##讀取：UE 實現讀取本地系統圖片為 UTexture2D

###通用方法

這種方法在編輯器和遊戲模式下都適用，支援的圖片檔案格式包括 PNG、JPEG、BMP、ICO、EXR、ICNS、HDR、TIFF、DDS、TGA，基本上能應對大部分常見的圖片類型。

程式碼也非常簡潔：

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

###編輯器專用方法

這種方法可以進一步支援更多圖片類型：UDIM 紋理貼圖、IES 檔案、PCX、PSD。

程式碼的實現會更加複雜一些：

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

透過使用 UTextureFactory 的 FactoryCreateBinary 函式，成功實現了這一步，該函式能夠讀取前述提及的額外檔案類型。

##複製：UE 實現複製 UTexture2D

有時候需要複製一個 UTexture2D 出來，再對這個複製出來的圖片進行修改，複製圖片需要使用到引擎內建的函式 `FImageCore::CopyImage`，只要設定好兩個圖片的參數，呼叫這個介面即可。

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

##保存：UE 實現將 UTexture2D 保存到文件

重點在於使用引擎函數 `FImageUtils::SaveImageAutoFormat`，實作起來相對簡單，但需注意處理失敗重試的情況。

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

##保存：使用者界面實現將 UTexture2D 保存為資產

將存放在記憶體中的 UTexture2D 儲存至資產 (Asset) 中，並可於資源瀏覽器 (Content Browser) 中檢視。

核心功能需要使用上述实現的 `CopyTexture2D`，我們需要先複製出一張新圖片，然後再呼叫 `UPackage::SavePackage` 將圖片所在的 `Package` 保存為資產。

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

##剪貼板：UE 實現複製圖片 (UTexture2D) 到 Windows 剪貼板 (Clipboard)

###Windows相關函數

我們將使用以下與 Windows 剪貼簿相關的函數：

* [OpenClipboard](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-openclipboard)打開剪貼板，取得剪貼板的處理器。
* [EmptyClipboard](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-emptyclipboard)清空剪贴板，並將剪貼板的所有權分配給當前的視窗。
* [SetClipboardData](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-setclipboarddata)設置剪貼板的資料，圖片的資料是通過這個接口發送給剪貼板。
* [CloseClipboard](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-closeclipboard)設置好資料後，關閉剪貼板。

###剪貯板的圖片格式

(https://learn.microsoft.com/zh-cn/windows/win32/dataxchg/standard-clipboard-formats)該文件介紹了可用的剪貼簿格式，其中 `CF_DIBV5` 可以用於設置圖片。

CF_DIBV5 要求的格式具體定義 [BITMAPV5HEADER 結構](https://learn.microsoft.com/zh-cn/windows/win32/api/wingdi/ns-wingdi-bitmapv5header)我們在這裡選用以下配置。

```cpp
BITMAPV5HEADER Header;
Header.bV5CSType        = LCS_sRGB;
Header.bV5Compression   = BI_BITFIELDS;
```

###設定 UTexture2D

我們在上面選擇了剪貼板圖片的顏色空間是 `LCS_sRGB`，即 sRGB 顏色空間，那麼 UTexture2D 也需要先設定到對應的格式：

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

ConvertTextureToStandard 負責將 UTexture2D 轉換為標準格式：TC_VectorDisplacementmap（RGBA8）和 SRGB 色彩空間。一旦對齊了 UTexture2D 和 Windows 剪貼簿的圖片格式，我們就能將圖片數據複製到剪貼簿上。

###具體程式碼

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

###UTexture2D 與 Base64 之間的轉換

這個實現起來比較簡單，直接上程式碼。

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


--8<-- "footer_tc.md"


> 此帖文係透過 ChatGPT 翻譯嘅，如有[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
