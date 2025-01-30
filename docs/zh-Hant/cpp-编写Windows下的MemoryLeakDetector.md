---
layout: post
title: 編寫 Windows 下的記憶體洩漏檢測工具
categories:
- c++
tags:
- dev
description: 這一陣子讀完了《程序員的自我修養：鏈接、裝載與庫》（後面簡稱《鏈接》），收穫良多，尋思著能不能做些相關的小代碼出來。剛好知道 Windows
  下有個內存洩漏檢測工具 [Visual Leak Detector](https://vld.codeplex.com/)，這個工具是透過替換 Windows
  下負責記憶體管理的 dll 介面來實現跟蹤記憶體分配釋放。所以決定參考 Visual Leak Detector （後面簡稱 VLD）來做個簡易的記憶體洩漏檢測工具，理解
  dll 聯結。
figures:
- assets/post_assets/2016-6-11-memory-leak-detector/depends.png
---

<meta property="og:title" content="编写 Windows 下的 Memory Leak Detector" />

![](https://img.shields.io/badge/windows-10-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##前言

這一陣子讀完了《程序員的自我修養：鏈接、裝載與庫》（後面簡稱《鏈接》），收穫良多，尋思著能不能做些相關的小程式出來。剛好知道 Windows 下有個內存泄漏檢測工具 [Visual Leak Detector](https://vld.codeplex.com/)這個工具是透過替換 Windows 下負責記憶體管理的 dll 接口來實現跟蹤記憶體分配釋放。所以決定參考 Visual Leak Detector（後面簡稱 VLD）來做個簡易的記憶體洩漏檢測工具，以理解 dll 連結。

##預備知識
《链接》一書詳細解釋了在 Linux 和 Windows 下可執行文件的鏈接原理，其中 Windows 下的可執行文件格式叫做 PE（Portable Executable）文件。而 DLL 文件的解釋是這樣的：

> DLL 即動態連結庫（Dynamic-Link Library）的縮寫，它相當於 Linux 下的共享物件。Windows 系統中大量採用了這種 DLL 機制，甚至包括 Windows 的核心結構都在很大程度上依賴於 DLL 機制。Windows 下的 DLL 檔案和 EXE 檔案實際上是一個概念，它們都是符合 PE 格式的二進制檔案，稍微有些不同的是 PE 檔案標頭中有個符號位表示該檔案是 EXE 還是 DLL，而 DLL 檔案的擴展名不一定是 .dll，也有可能是其它像是 .ocx（OCX 控制項）或是 .CPL（控制面板程式）。

還有例如 Python 的擴展文件 .pyd。而 DLL 中有關我們這裡記憶體洩漏檢測的概念是**符號導出導入表**。

####符號導出表

> 當一個 PE 需要將一些函數或變量提供給其他 PE 文件使用時，我們把這種行為叫做**符號導出（Symbol Exporting）**

簡單地理解，在 Windows PE 中，所有導出的符號被集中存放在被稱作**導出表（Export Table）**的結構中，它提供了一個符號名與符號地址的映射關係。需要導出的符號需要加上修飾符`__declspec(dllexport)`。

####符號導入表

符號導入表就是我們這裡的關鍵概念，它跟符號導出表相對應，先來看概念解釋：

> 如果我們在某個程序中使用到了來自 DLL 的函數或者變量，那麼我們就把這種行為叫做**符號導入（Symbol Importing）**。

在 Windows PE 中，保存模块需要导入的變量和函數的符號以及所在的模塊等信息的結構叫做**導入表（Import Table）**。當 Windows 加載 PE 文件時，其中一個要做的事情就是將所有需要導入的函數地址確定並將導入表中的元素調整到正確的地址，使得在運行時，程序通過查詢導入表來定位實際函數的地址，並進行調用。導入表中最重要的結構是**導入地址數組（Import Address Table，IAT）**，裡面存放的就是導入的函數實際地址。

看到這裡是不是已經猜到我們要實現的記憶體洩漏檢測是怎麼做的。沒錯，就是 hack 導入表，具體來說就是把需要檢測的模組的導入表中，關於記憶體申請和釋放的函數地址改成我們自定義的函數，這樣我們就可以知道模組每一次的記憶體申請和釋放情況了，可以盡情做我們想做的檢測。

有關 DLL 連結的更詳細知識可以自行查閱《連結》或其他資料。

## Memory Leak Detector

知道了原理，接下來就是根據原理來實現內存泄漏檢測。下面的講解將基於我自己的實現，我放在了我的 Github 上：[LeakDetector](https://github.com/disenone/LeakDetector)。

####取代函數

先來看關鍵的函數，位於[RealDetector.cpp](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)I'm sorry, but I can't translate what you've provided as it doesn't contain any text to be translated. If you provide me with the text you want to be translated into Traditional Chinese, I'll be happy to help.

```cpp linenums="1"
/* 把 importModule 中的 IAT (導入位址表) 的某個函數替換成別的函數，
* importModule 會調用到別的 module 的函數，這個函數就是需要 patch 的函數，
* 我們要做的就是讓 import module 改成調用我們自定義的函數。
 *
* - importModule (IN): 要處理的 module，這個 module 調用到其他 module 的需要 patch 的函數
 *
- exportModuleName (IN): 要打補丁的函數來自的模組名稱
 *
* - exportModulePath (IN): export module 所在的路徑，首先嘗試用 path 來加載 export module，
如果失敗，則用 name 來加載
- importName（IN): 函式名稱
 *
- replacement (IN): 替代的函式指標
 *
返回值: 若成功則為 true，否則為 false
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

我們來分析一下這個函數，就像註釋所說的，這個函數實現的功能就是把 IAT 裡面的某函數的地址改成另一個函數的地址。先來看第 34-35 行：

``` cpp
idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
	TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
```

`ImageDirectoryEntryToDataEx` 函式可回傳模組檔案標頭中特定結構的位址，`IMAGE_DIRECTORY_ENTRY_IMPORT` 指定欲匯入的表格結構，因此所回傳的 `idte` 就指向了模組匯入表。

36-40行是檢查`idte`的有效性。41行`idte->FirstThunk`指向的就是實際的IAT了。所以41-48行就是在根據模塊名字查找需要替換的函數的模塊，如果找不到，說明沒有調用到該模塊的函數，只能提示錯誤並返回。

找到模組後，自然地，我們需要找到替換的那個函數，55-62 行打開函數所屬的模組，64 行找到函數地址。因為 IAT 沒有保存名字，所以需要先根據原來的函數地址，定位到函數，再修改該函數地址，68-80 行就是在做這個事情。成功找到函數之後，就簡單地把地址修改成 `replacement` 的地址。

我們已成功取代了 IAT 中的函數。

####模組和函數名稱

雖然我們已經實現了替換 IAT 函數 `patchImport`，但這個函數需要指定模塊名字和函數名字呀，那我們怎麼知道程序的內存分配和釋放用了什麼模塊和函數呢？為了搞清楚這個問題，我們需要借助 Windows 下的工具 [Dependency Walker](http://www.dependencywalker.com/)。Visual Studio 下新建一個工程，在 `main` 函數裡面使用 `new` 來申請內存，編譯 Debug 版，之後使用 `depends.exe` 來打開編譯出來的 exe 文件，可以看到以下類似的界面（以我的工程 [LeakDetectorTest](https://github.com/disenone/LeakDetector/tree/master/LeakDetectorTest)作為例子）：

![](assets/img/2016-6-11-memory-leak-detector/depends.png)

可以看到 LeakDetectorTest.exe 使用了 uscrtbased.dll 裡面的 `malloc` 和 `_free_dbg` （沒有在圖中顯示出來），這兩個函數就是我們需要替換的函數了。要注意實際的模組函數名字可能跟你的 Windows 和 Visual Studio 版本有關，我的是 Windows 10 和 Visual Studio 2015，你需要做的就是用 depends.exe 看看實際調用的是什麼函數。

####分析調用堆疊

記錄內存分配需要記錄當時的調用堆疊資訊，這裡我不打算詳細介紹 Windows 下如何拿到當前的調用堆疊資訊，相關的函數是 `RtlCaptureStackBackTrace`，網路上有許多相關的資料，也可以看看我的程式碼裡面的函數 [`printTrace`](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)。

####檢測記憶體洩漏

至此，我們已經把龍珠都收集全了，接下來正式召喚神龍。

我希望做一個可以部分檢測記憶洩漏的功能（這與 VLD 不同，VLD 進行全局檢測並支持多線程）。因此在實際替換函數的`RealDetector`類上又包了一層`LeakDetector`，並將`LeakDetector`的接口開放給使用者。使用時只需建立`LeakDetector`，即可完成函數的替換並開始檢測記憶洩漏，`LeakDetector`析構時會還原原來的函數，停止記憶洩漏檢測，並列印記憶洩漏檢測結果。

用下面的代碼測試一下：

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

代碼直接 `new` 了一些內存出來，沒有釋放掉就直接退出，程序打印的結果：

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

程式正確地找出有兩個地方申請的記憶體沒有釋放，並且列印出完整的呼叫堆疊訊息，我們需要的功能至此已經完成了。

###結論

當你還不了解程序鏈接、裝載與庫的時候，你可能會對如何找到共享鏈接庫的函數一頭霧水，更不要說要把鏈接庫的函數替換成我們自己的函數了。這裡就以檢測內存洩露為例子，探討下了如何替換 Windows DLL 的函數，更詳細的實現可以參考 VLD 的源碼。

另外想說的是，《程式設計師的自我修養：連結、載入與程式庫》真是本不錯的書呢，純粹感嘆非軟廣。

--8<-- "footer_tc.md"


> 這篇帖子是由 ChatGPT 翻譯的，請在 [**反饋**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遺漏之處。 
