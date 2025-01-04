---
layout: post
title: 編寫 Windows 下的 Memory Leak Detector
categories:
- c++
tags:
- dev
description: (https://vld.codeplex.com/)這個工具是通過替換 Windows 下負責內存管理的 dll 介面來實現跟蹤內存分配釋放。所以決定參考
  Visual Leak Detector （後面簡稱 VLD）來做個簡易的內存洩漏檢測工具，理解 dll 鏈接。
figures:
- assets/post_assets/2016-6-11-memory-leak-detector/depends.png
---

<meta property="og:title" content="编写 Windows 下的 Memory Leak Detector" />

![](https://img.shields.io/badge/windows-10-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##前言

最近讀完了《程式設計師的自我修養：連結、載入與庫》（後稱《連結》），受益良多，想著能否寫些相關的小程式出來。剛好知道 Windows 下有個內存洩漏檢測工具 [Visual Leak Detector](https://vld.codeplex.com/)這工具透過取代 Windows 下負責記憶體管理的 dll 介面來追蹤記憶體分配和釋放。因此決定參考 Visual Leak Detector（簡稱 VLD）來開發一個簡易的記憶體洩漏檢測工具，以瞭解 dll 連結。

##預備知識
《連結》一書詳細解釋了在 Linux 和 Windows 下可執行檔的連結原理，其中 Windows 下的可執行檔格式稱為 PE（Portable Executable）檔案。而 DLL 檔案的解釋是這樣的：

> DLL 即為動態鏈接庫（Dynamic-Link Library）的縮寫，相當於 Linux 下的共享對象。Windows 系統廣泛採用這種 DLL 機制，甚至包括 Windows 內核結構在很大程度上都依賴於 DLL 機制。在 Windows 中，DLL 文件和 EXE 文件實際上是相同的概念，它們都是以 PE 格式存儲的二進制文件，僅有一點區別是在 PE 文件頭部有一個標誌位來表示該文件是EXE或是DLL，而 DLL 文件的擴展名並不一定是.dll，可能是其他如.ocx（OCX 控件）或是.CPL（控制面板程序）。

另外還有像是 Python 的擴展檔案 .pyd。而 DLL 中與我們這裡內存洩漏檢測相關的概念是**符號導出導入表**。

####符號導出表

> 當一個PE需要將一些函數或變量提供給其他PE文件使用時，我們把這種行為稱為**符號導出（Symbol Exporting）**

在 Windows PE 中，所有导出的符号都被集中存放在被稱為**導出表（Export Table）**的結構中，它提供了一個符號名與符號地址的對應關係。需要導出的符號需要加上修飾符`__declspec(dllexport)`。

####符號匯入表

符號導入表就是我們這裡的關鍵概念，它跟符號導出表相對應，先來看概念解釋：

> 如果我哋喺某個程序中使用咗來自 DLL 嘅函數或者變數，咁我哋就叫呢種行為為**符號導入（Symbol Importing）**。

Windows PE 中保存模組需要導入的變量和函數的符號以及所在的模組等信息的結構叫做**導入表（Import Table）**。當 Windows 加載 PE 檔案時，其中一個要做的事情就是將所有需要導入的函數地址確定並將導入表中的元素調整到正確的地址，使得運行時，程序通過查詢導入表來定位實際函數的地址，並進行調用。導入表中最重要的結構是**導入地址數組（Import Address Table，IAT）**，裡面存放的就是導入的函數實際地址。

看到這裡是不是已經猜到我們要實現的記憶體洩漏檢測是怎麼做 :)。沒錯就是 hack 導入表，具體地說就是把需要檢測的模組的導入表中，關於記憶體申請和釋放的函數的地址改成我們自定義的函數，那麼我們就可以知道模組每一次的記憶體申請和釋放情況了，可以盡情做我們想做的檢測。

關於 DLL 連結的更詳細知識可以自行查閱《連結》或其他資料。

## Memory Leak Detector

理解了原理，接下來就根據這個原理來實現內存洩漏檢測。以下的解說將基於我的個人實作，我已經將它放在我的 Github 上：[LeakDetector](https://github.com/disenone/LeakDetector)抱歉，我無法翻譯沒有內容的文字。

####替換函數

請看這個重要的函數，位於[RealDetector.cpp](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)I'm sorry, but I can't provide a translation without knowing the text that needs to be translated. How can I assist you today?

```cpp linenums="1"
將 importModule 中的 IAT (Import Address Table) 的某個函數替換為其他函數，
importModule 將會呼叫其他模組的函數，這個函數就是需要進行修補的函數，
我們要做的就是將 import module 改成呼叫我們自定義的函數。
 *
- importModule (IN): 欲處理的模組，該模組調用其他模組時需修補的函數
 *
* - exportModuleName（IN）：需要打補丁的函數來源的模組名稱
 *
- exportModulePath（IN）: export module所在的路徑，首先嘗試用path來加載export module，
如果失敗，則用 name 來載入
- importName (IN): Function Name
 *
- replacement (IN): 替代的函數指標
 *
Return Value: 成功為 true，否則為 false
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

讓我們來分析這個函數，就像註釋中所述，這個函數實際上的功能是將 IAT 裡某函數的位址更改為另一個函數的位址。首先我們看看第 34-35 行：

``` cpp
idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
	TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
```

`ImageDirectoryEntryToDataEx` 函數能夠返回模組的檔案頭中某個結構的地址，`IMAGE_DIRECTORY_ENTRY_IMPORT` 指定了要匯入表結構，因此返回的 `idte` 就指向了模組的匯入表。

36-40 行是用來檢查 `idte` 是否有效。第 41 行中 `idte->FirstThunk` 指向的即是實際的 IAT。因此 41-48 行是根據模組名稱來查找需要替換的函數模組，如果查無結果，則表示該模組的函數並未被調用，只能提示錯誤並返回。

找到模組後，自然地，我們需要找到替換的那個函數，55-62行打開函數所屬的模組，64行找到函數地址。因為 IAT 沒有保存名字，所以需要先根據原來的函數地址，定位到函數，再修改該函數地址，68-80行就是在做這個事情。成功找到函數之後，就簡單地把地址修改成“replacement”的地址。

這樣，我們已成功地替換了 IAT 中的函式。

####模組與函數名稱

雖然我們已經成功替換了 IAT 函數 `patchImport`，但這個函數需要指定模組名和函數名啊，那我們怎麼知道程式的記憶體分配和釋放使用了什麼模組和函數呢？為了搞清楚這個問題，我們需要依賴 Windows 下的工具 [Dependency Walker](http://www.dependencywalker.com/)在 Visual Studio 中新建一個專案，在 `main` 函式中使用 `new` 來配置記憶體，編譯 Debug 版本，然後使用 `depends.exe` 打開編譯出的 exe 檔案，你會看到類似這樣的界面（以我的專案 [LeakDetectorTest](https://github.com/disenone/LeakDetector/tree/master/LeakDetectorTest)為例）：

![](assets/img/2016-6-11-memory-leak-detector/depends.png)

在 LeakDetectorTest.exe 中，我們可以看到使用了 uscrtbased.dll 內的 `malloc` 和 `_free_dbg` 函數（未在圖中顯示）。這兩個函數是我們需要替換的目標。請注意，實際的模組函數名稱可能與您的 Windows 和 Visual Studio 版本有關，我的版本是 Windows 10 和 Visual Studio 2015。您需要做的就是使用 depends.exe 查看實際調用的函數是什麼。

####分析呼叫堆栈

記錄內存分配需要記錄當時的調用棧信息，這裡我不打算詳細介紹 Windows 下如何拿到當前的調用棧信息，相關的函數是 `RtlCaptureStackBackTrace`，網上有許多相關的資料，也可以看看我的程式碼裡面的函數 [`printTrace`](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)。

####檢測記憶體洩漏

迄今為止，我們已完全收集了龍珠，現在正式召喚神龍。

我想實現部分內存洩漏檢測（與VLD不同，VLD進行全局檢測，並支持多線程）。所以我在實際替換函數的`RealDetector`類上再包了一層`LeakDetector`，並將`LeakDetector`的接口暴露給使用者。使用時只需建構`LeakDetector`，即可完成函數替換並開始內存洩漏檢測。 `LeakDetector`解構時將恢復原函數，停止內存洩漏檢測並列印檢測結果。

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

程式碼直接使用 `new` 來配置一些記憶體，但在離開時沒有釋放掉它們，導致程式印出以下的結果：

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

程式正確地找出兩個地方申請的記憶體沒有釋放，並列印出完整的呼叫堆疊資訊，我們需要的功能至此已經完成了。

###結語

當你還不了解程式連結、載入與庫的時候，你可能會對如何找到共享連結庫的函數一頭霧水，更不要說要把連結庫的函數替換成我們自己的函數了。這裡就以檢測內存洩漏為例子，探討下了如何替換 Windows DLL 的函數，更詳細的實現可以參考 VLD 的源碼。

另外想說的是，《程序員的自我修養：鏈接、裝載與庫》真是本不錯的書呢，純感慨非軟廣。

--8<-- "footer_tc.md"


> 此貼文是透過 ChatGPT 翻譯的，請在 [**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
