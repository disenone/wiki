---
layout: post
title: يتم تحقيق تشغيل مختلف العمليات على الصور (UTexture2D) في UE (قراءة، حفظ، نسخ،
  الحافظة...)
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
description: UE يقوم بقراءة الصور من النظام المحلي
---

<meta property="og:title" content="UE 实现读取本地系统图片" />

#يو إي تنفذ مجموعة متنوعة من عمليات الصور (UTexture2D) (قراءة، حفظ، نسخ، حافظة...)

> جميع شفرات البرنامج معروضة باعتبار الإصدار  UE5.3 كمثال.

##شفرة المصدر

يمكن الحصول على مزيد من تفاصيل الكود المصدري من متجر UE عبر الإضافة: [AIChatPlus](https://www.unrealengine.com/marketplace/zh-CN/product/aichatplus-ai-chat-integration-openai-azure-claude-gemini)

##قراءة: تقوم UE بتحميل صور النظام المحلي كـ UTexture2D

###طرق عامة

يمكن تنفيذ هذا الأسلوب في وضعي التحرير واللعب، ويدعم صيغ ملفات الصور التالية: PNG، JPEG، BMP، ICO، EXR، ICNS، HDR، TIFF، DDS، TGA. يمكنه تقريبًا التعامل مع معظم أنواع الصور الشائعة.

الكود بسيط جدًا أيضًا:

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
العودة هي UTexture2D.

###طرق خاصة للمحرر

يمكن لهذه الطريقة دعم المزيد من أنواع الصور الإضافية: خرائط قوام UDIM، ملفات IES، PCX، PSD.

سيكون تنفيذ الشيفرة أكثر تعقيدًا بعض الشيء:

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

التحقيق يتم من خلال استخدام دالة FactoryCreateBinary من UTextureFactory، والتي تستطيع قراءة أنواع الملفات الإضافية التي تم ذكرها سابقًا.

##نسخ: تنفيذ UE لنسخ UTexture2D

في بعض الأحيان يحتاج الشخص إلى نسخ UTexture2D ثم تعديل الصورة المنسوخة، لنسخ الصورة يجب استخدام الدالة المدمجة في المحرك `FImageCore::CopyImage`، كل ما عليك فعله هو تعيين معلمات الصورتين واستدعاء هذه الواجهة.

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

##حفظ: UE تنفيذ حفظ UTexture2D إلى ملف

الأساس هو استخدام وظيفة المحرك `FImageUtils::SaveImageAutoFormat`، وتنفيذها يبدو بسيطًا، لكن يجب أن ننتبه إلى حالات إعادة المحاولة في حال الفشل

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

##حافظة: يو إي - تنفيذ حافظة UTexture2D إلى الأصلية

حفظ UTexture2D في الذاكرة إلى الأصل، ويمكن مشاهدته في متصفح الموارد (Content Browser).

تحتاج الدالة الأساسية إلى استخدام "CopyTexture2D" التي تم تنفيذها في الأعلى، علينا أن نقوم أولاً بنسخ صورة جديدة، ثم بعد ذلك نقوم با

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

##الحافظة: تنفيذ UE لنسخ الصورة (UTexture2D) إلى حافظة ويندوز (Clipboard)

###دوال متعلقة بـ Windows

سنستخدم الدوال المتعلقة بحافظة Windows التالية:

* [OpenClipboard](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-openclipboard): افتح الحافظة، واحصل على مُعالج الحافظة.
* [EmptyClipboard](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-emptyclipboard): مسح الحافظة، وتخصيص ملكية الحافظة لنافذة الحالية.
* [SetClipboardData](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-setclipboarddata)قم بتعيين بيانات الحافظة، وبيانات الصور تُرسل إلى الحافظة عبر هذه الواجهة.
* [CloseClipboard](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-closeclipboard)بعد ضبط البيانات، قم بإغلاق الحافظة.

###تنسيق صور الحافظة

(https://learn.microsoft.com/zh-cn/windows/win32/dataxchg/standard-clipboard-formats)تم تقديم تنسيقات الحافظة المتاحة في الداخل، حيث يمكن استخدام `CF_DIBV5` لضبط الصورة.

التعريف الدقيق لتنسيق الحقل CF_DIBV5 المطلوب [هيكل BITMAPV5HEADER](https://learn.microsoft.com/zh-cn/windows/win32/api/wingdi/ns-wingdi-bitmapv5header)نحن نستخدم هذه التكوينات هنا

```cpp
BITMAPV5HEADER Header;
Header.bV5CSType        = LCS_sRGB;
Header.bV5Compression   = BI_BITFIELDS;
```

###UTexture2D التعيين

لقد اخترنا في الأعلى مساحة لونية لصور الحافظة هي `LCS_sRGB`، أي مساحة لون sRGB، لذلك يجب ضبط UTexture2D مسبقًا على التنسيق المقابل:

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

ConvertTextureToStandard هي المسؤولة عن تحويل UTexture2D إلى تنسيق قياسي: TC_VectorDisplacementmap (RGBA8) و SRGB لفضاء الألوان. بعد محاذاة UTexture2D مع تنسيق صورة الحافظة في Windows، يمكننا نسخ بيانات الصورة إلى الحافظة.

###رمز محدد

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

###تحويل بين UTexture2D و Base64

هذا من السهل تنفيذه، لنبدأ مباشرة بالشيفرة

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


--8<-- "footer_ar.md"


> هذا المنشور تم ترجمته باستخدام ChatGPT، يرجى في [**التعليقات**](https://github.com/disenone/wiki_blog/issues/new)يرجى تحديد أي نقص.  
