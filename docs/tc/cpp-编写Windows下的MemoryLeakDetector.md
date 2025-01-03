---
layout: post
title: 編寫 Windows 下的記憶洩漏檢測器
categories:
- c++
tags:
- dev
description: 這一陣子讀完了《程序員的自我修養：鏈接、裝載與庫》（後面簡稱《鏈接》），收穫良多，尋思著能不能做些相關的小程式出來。剛好知道 Windows
  下有個內存洩漏檢測工具 [Visual Leak Detector](https://vld.codeplex.com/)這個工具是通過替換 Windows 下負責內存管理的
  dll 接口來實現跟蹤內存分配釋放。所以決定參考 Visual Leak Detector （後面簡稱 VLD）來做個簡易的內存洩漏檢測工具，理解 dll 鏈接。
figures:
- assets/post_assets/2016-6-11-memory-leak-detector/depends.png
---

<meta property="og:title" content="编写 Windows 下的 Memory Leak Detector" />

![](https://img.shields.io/badge/windows-10-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##前言

最近讀完了《程式設計師的自我修養：連結、載入與庫》（簡稱《連結》），獲益良多，想著能不能寫一些相關的小程式出來。剛好知道 Windows 下有一個內存洩漏檢測工具[Visual Leak Detector](https://vld.codeplex.com/)這個工具是透過替換 Windows 下負責記憶體管理的 dll 介面來實現追蹤記憶體分配釋放。所以決定參考 Visual Leak Detector （後面簡稱 VLD）來做個簡易的記憶體洩漏檢測工具，理解 dll 連結。

##預備知識
《連結》一書詳細解釋了在 Linux 和 Windows 下可執行檔的連結原理，其中 Windows 下的可執行檔格式叫做 PE（Portable Executable）檔。而 DLL 檔的解釋是這樣的：

> DLL 即動態鏈接庫（Dynamic-Link Library）的縮寫，它相當於 Linux 下的共享對象。Windows 系統中大量採用了這種 DLL 機制，甚至包括 Windows 的內核的結構都很大程度依賴於 DLL 機制。Windows 下的 DLL 檔案和 EXE 檔案實際上是一個概念，它們都是有 PE 格式的二進制文件，稍微有些不同的是 PE 檔案頭部中有個符號位表示該檔案是 EXE 或是 DLL，而 DLL 檔案的擴展名不一定是 .dll，也有可能是別的比如 .ocx（OCX 控件）或是 .CPL（控制面板程式）。

另外，例如 Python 的擴展文件 .pyd。而 DLL 中關於我們這裡內存洩漏檢測的概念是**符號導出導入表**。

####符號導出表

> 當一個 PE 需要將一些函數或變量提供給其他 PE 檔案使用時，我們把這種行為稱為**符號導出（Symbol Exporting）**

簡單來說，在 Windows PE 中，所有導出的符號都被集中存放在被稱為**導出表（Export Table）**的結構中，它提供了符號名稱與地址之間的對應關係。希望要導出的符號必須加上修飾符`__declspec(dllexport)`。

####符號匯入表

符號導入表就是我們這裡關鍵的概念，它與符號導出表相對應，先來看概念解釋：

> 如果我們在某個程式中使用到了來自 DLL 的函數或者變數，那麼我們就把這種行為叫做**符號匯入（Symbol Importing）**。

Windows PE 中保存模組需要匯入的變量和函數的符號以及所在的模組等信息的結構叫做**導入表（Import Table）**。Windows 加載 PE 文件時，其中一個要做的事情就是將所有需要匯入的函數地址確定並將導入表中的元素調整到正確的地址，使得執行時，程式通過查詢導入表來定位實際函數的地址，並進行調用。導入表中最重要的結構是**導入地址陣列（Import Address Table，IAT）**，裡面存放的就是匯入的函數實際地址。

看到這裡是不是已經猜到我們要實現的內存洩漏檢測是怎麼做 :)。沒錯就是 hack 導入表，具體地說就是把需要檢測的模組的導入表中，關於內存申請和釋放的函數的地址改成我們自定義的函數，那麼我們就可以知道模組每一次的內存申請和釋放情況了，可以盡情做我們想做的檢測。

有關 DLL 連結的更詳細知識可以自行查閱《連結》或其他資料。

## Memory Leak Detector

理解了原理後，接下來要根據這個原理來實現內存洩漏檢測。以下的解說將基於我自己的實作，並且已經放在我的 Github 上：[LeakDetector](https://github.com/disenone/LeakDetector)Sorry, I am unable to translate the provided text as it does not contain any content to be translated.

####取代函數

請查看重要的函數，位於[RealDetector.cpp](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)抱歉，我無法翻譯沒有任何內容的文字。是否有其他文本需要翻譯？

```cpp linenums="1"
/* 將 importModule 中的 IAT (Import Address Table) 的某個函數替換為其他函數，
importModule 會呼叫其他模組的函數，這個函數就是需要打補丁的函數，
我們要做的就是讓 import module 改成調用我們自定義的函數。
 *
- importModule (IN): 欲處理的模組，該模組調用到其他模組需要修補的函數
 *
- exportModuleName (IN): 需要 patch 的函數來自的 module 名稱
 *
- exportModulePath (IN): export module所在的路徑，首先嘗試用路徑來加載export module，
如果失敗，則用名稱來加載
-importName（IN）：函數名
 *
- replacement (IN): 替代的函數指標
 *
返回值: 若成功為 true，否則為 false
*/
bool RealDetector::patchImport(
	HMODULE importModule,
	LPCSTR exportModuleName,
	LPCSTR exportModulePath,
	LPCSTR importName,
	LPCVOID replacement)
{
	HMODULE                  exportmodule;
	IMAGE_THUNK_DATA        *iate;
	IMAGE_IMPORT_DESCRIPTOR *idte;
	FARPROC                  import;
	DWORD                    protect;
	IMAGE_SECTION_HEADER    *section;
	ULONG                    size;

	assert(exportModuleName != NULL);

	idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
		TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
	if (idte == NULL) 
	{
		logMessage("patchImport failed: idte == NULL\n");
		return false;
	}
	while (idte->FirstThunk != 0x0) 
	{
		if (strcmp((PCHAR)R2VA(importModule, idte->Name), exportModuleName) == 0) 
		{
			break;
		}
		idte++;
	}
	if (idte->FirstThunk == 0x0) 
	{
		logMessage("patchImport failed: idte->FirstThunk == 0x0\n");
		return false;
	}

	if (exportModulePath != NULL) 
	{
		exportmodule = GetModuleHandleA(exportModulePath);
	}
	else 
	{
		exportmodule = GetModuleHandleA(exportModuleName);
	}
	assert(exportmodule != NULL);
	import = GetProcAddress(exportmodule, importName);
	assert(import != NULL);

	iate = (IMAGE_THUNK_DATA*)R2VA(importModule, idte->FirstThunk);
	while (iate->u1.Function != 0x0) 
	{
		if (iate->u1.Function == (DWORD_PTR)import) 
		{
			VirtualProtect(&iate->u1.Function, sizeof(iate->u1.Function), 
				PAGE_READWRITE, &protect);
			iate->u1.Function = (DWORD_PTR)replacement;
			VirtualProtect(&iate->u1.Function, sizeof(iate->u1.Function), 
				protect, &protect);
			return true;
		}
		iate++;
	}

	return false;
}

```

讓我們來分析這個函數，就像註釋所說的那樣，這個函數的功能是將 IAT 中某函數的地址更改為另一個函數的地址。讓我們看看第 34-35 行：

``` cpp
idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
	TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
```

`ImageDirectoryEntryToDataEx` 函式能夠回傳模組的檔案標頭特定結構的位址，`IMAGE_DIRECTORY_ENTRY_IMPORT` 指定要尋找的導入表結構，因此回傳的 `idte` 就對應至該模組的導入表。

36-40行是在檢查`idte`是否有效。第41行`idte->FirstThunk`指向的就是實際的IAT。所以41-48行是根據模塊名稱查找需要替換的函數模塊，如果找不到，說明沒有調用到該模塊的函數，只能提示錯誤並返回。

找到模組後，自然地，我們需要找到替換的那個函數，55-62行打開函數所屬的模組，64行找到函數地址。因為IAT沒有保存名字，所以需要先根據原來的函數地址，定位到函數，再修改該函數地址，68-80行就是在做這個事情。成功找到函數之後，就簡單地把地址修改成 `replacement` 的地址。

到這裡，我們已成功地替換了 IAT 中的函數。

####模組與函數名稱

儘管我們已經實現了替換 IAT 函數 `patchImport`，但這個函數需要指定模塊名稱和函數名稱啊，那我們怎麼知道程式的記憶體分配和釋放用了什麼模塊和函數呢？為了搞清楚這個問題，我們需要借助 Windows 下的工具 [Dependency Walker](http://www.dependencywalker.com/)在 Visual Studio 中建立一個新專案，在 `main` 函式中使用 `new` 來配置記憶體，編譯 Debug 版本後，使用 `depends.exe` 開啟所編譯的 exe 檔案，即可看到類似下列界面（使用我的專案名稱 [LeakDetectorTest](https://github.com/disenone/LeakDetector/tree/master/LeakDetectorTest)為例）：

![](assets/img/2016-6-11-memory-leak-detector/depends.png)

我們可以看到 LeakDetectorTest.exe 使用了 uscrtbased.dll 裡面的 `malloc` 和 `_free_dbg` ，這兩個函數就是我們需要替換的函數了。需要注意的是，實際模塊函數的名稱可能與您的Windows和Visual Studio版本有關。我的是Windows 10和Visual Studio 2015，您需要做的就是使用 depends.exe 觀察實際調用的函數是什麼。

####分析呼叫堆栈

記錄記憶體分配需要記錄當時的調用堆疊資訊，這裡我不打算詳細介紹 Windows 下如何取得當前的調用堆疊資訊，相關的函數是 `RtlCaptureStackBackTrace`，網上有許多相關的資料，也可以看看我的程式碼裡的函數 [`printTrace`](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)。

####檢測記憶體洩漏

迄今為止，我們已經收集齊所有龍珠，接下來正式召喚神龍。

我希望能夠實現局部檢測內存洩漏（這與 VLD 不同，VLD 做的是全局檢測並支持多線程）。因此我在實際替換函數的類`RealDetector`上再包了一層`LeakDetector`，並將`LeakDetector`的接口提供給使用者。使用時只需建構`LeakDetector`，即完成函數的替換並開始檢測內存洩漏，`LeakDetector`解構時會恢復原來的函數，中止內存洩漏檢測，並列印內存洩漏檢測結果。

請使用以下程式碼進行測試：

```cpp
#include "LeakDetector.h"
#include <iostream>
using namespace std;

void new_some_mem()
{
	char* c = new char[12];
	int* i = new int[4];
}

int main()
{
	auto ld = LDTools::LeakDetector("LeakDetectorTest.exe");
	new_some_mem();
    return 0;
}

```

程式碼直接使用 `new` 配置了一些記憶體，卻沒有釋放就直接退出，程式列印的結果：

```
============== LeakDetector::start ===============
LeakDetector init success.
============== LeakDetector::stop ================
Memory Leak Detected: total 2

Num 1:
    e:\program\github\leakdetector\leakdetector\realdetector.cpp (109): LeakDetector.dll!LDTools::RealDetector::_malloc() + 0x1c bytes
    f:\dd\vctools\crt\vcstartup\src\heap\new_scalar.cpp (19): LeakDetectorTest.exe!operator new() + 0x9 bytes
    f:\dd\vctools\crt\vcstartup\src\heap\new_array.cpp (15): LeakDetectorTest.exe!operator new[]() + 0x9 bytes
    e:\program\github\leakdetector\leakdetectortest\leakdetectortest.cpp (12): LeakDetectorTest.exe!new_some_mem() + 0x7 bytes
    e:\program\github\leakdetector\leakdetectortest\leakdetectortest.cpp (19): LeakDetectorTest.exe!main()
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (74): LeakDetectorTest.exe!invoke_main() + 0x1b bytes
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (264): LeakDetectorTest.exe!__scrt_common_main_seh() + 0x5 bytes
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (309): LeakDetectorTest.exe!__scrt_common_main()
    f:\dd\vctools\crt\vcstartup\src\startup\exe_main.cpp (17): LeakDetectorTest.exe!mainCRTStartup()
    KERNEL32.DLL!BaseThreadInitThunk() + 0x24 bytes
    ntdll.dll!RtlUnicodeStringToInteger() + 0x253 bytes
    ntdll.dll!RtlUnicodeStringToInteger() + 0x21e bytes

Num 2:
    e:\program\github\leakdetector\leakdetector\realdetector.cpp (109): LeakDetector.dll!LDTools::RealDetector::_malloc() + 0x1c bytes
    f:\dd\vctools\crt\vcstartup\src\heap\new_scalar.cpp (19): LeakDetectorTest.exe!operator new() + 0x9 bytes
    f:\dd\vctools\crt\vcstartup\src\heap\new_array.cpp (15): LeakDetectorTest.exe!operator new[]() + 0x9 bytes
    e:\program\github\leakdetector\leakdetectortest\leakdetectortest.cpp (11): LeakDetectorTest.exe!new_some_mem() + 0x7 bytes
    e:\program\github\leakdetector\leakdetectortest\leakdetectortest.cpp (19): LeakDetectorTest.exe!main()
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (74): LeakDetectorTest.exe!invoke_main() + 0x1b bytes
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (264): LeakDetectorTest.exe!__scrt_common_main_seh() + 0x5 bytes
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (309): LeakDetectorTest.exe!__scrt_common_main()
    f:\dd\vctools\crt\vcstartup\src\startup\exe_main.cpp (17): LeakDetectorTest.exe!mainCRTStartup()
    KERNEL32.DLL!BaseThreadInitThunk() + 0x24 bytes
    ntdll.dll!RtlUnicodeStringToInteger() + 0x253 bytes
    ntdll.dll!RtlUnicodeStringToInteger() + 0x21e bytes
```

程式正確地找出有兩個地方申請的記憶體沒有釋放，並且列印出完整的呼叫堆疊資訊，我們需要的功能至此已經完成了。

###結語

當你還不熟悉程式連結、載入以及庫時，可能會對如何找到共享庫函數感到困惑，更別說要將庫函數替換為我們自己的函數了。這裡以檢測記憶體洩漏為例，探討如何替換 Windows DLL 函數，更詳細的實現可參考 VLD 的源碼。

另外想說的是，《程序員的自我修養：鏈接、裝載與庫》真是本不錯的書呢，純感慨非軟廣。

--8<-- "footer_tc.md"


> 此篇文章是由 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
