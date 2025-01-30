---
layout: post
title: Write a Memory Leak Detector for Windows
categories:
- c++
tags:
- dev
description: 'Recently, I finished reading "The Programmer''s Self-Improvement: Linking,
  Loading, and Libraries" (hereafter referred to as "Linking") and gained a lot from
  it. I''m wondering if I could create some related small code. I happened to find
  out that there is a memory leak detection tool for Windows called [Visual Leak Detector](https://vld.codeplex.com/)This
  tool works by replacing the DLL interface responsible for memory management in Windows
  to track memory allocation and deallocation. Therefore, I''ve decided to create
  a simple memory leak detection tool, referred to as Visual Leak Detector (hereinafter
  VLD), to understand DLL linking.'
figures:
- assets/post_assets/2016-6-11-memory-leak-detector/depends.png
---

<meta property="og:title" content="编写 Windows 下的 Memory Leak Detector" />

![](https://img.shields.io/badge/windows-10-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##Preface

Recently finished reading "The Self-cultivation of Programmers: Linking, Loading, and Libraries" (referred to as "Linking" for short), gained a lot, and thinking about whether I can create some related short code. Happened to know about a memory leak detection tool [Visual Leak Detector](https://vld.codeplex.com/)This tool implements memory allocation and deallocation tracking by replacing the DLL interfaces responsible for memory management in Windows. Therefore, we decided to create a simple memory leak detection tool by referencing the Visual Leak Detector (hereinafter referred to as VLD) to understand DLL linkage.

##Prerequisites
The book "Linking" provides a detailed explanation of the linking principles of executable files under Linux and Windows, where the executable file format in Windows is called PE (Portable Executable) files. The explanation for DLL files is as follows:

> DLL stands for Dynamic-Link Library, which is analogous to shared objects in Linux. This DLL mechanism is widely adopted in Windows systems, and even the structure of the Windows kernel largely relies on it. In Windows, DLL files and EXE files are essentially the same concept; both are binary files in PE format. The only slight difference is that the PE file header contains a flag indicating whether the file is an EXE or a DLL. Additionally, DLL files do not necessarily have the .dll extension; they can also have other extensions, such as .ocx (for OCX controls) or .CPL (for control panel programs).

There are also extension files like .pyd for Python. The concept related to memory leak detection in DLLs here is the **export and import table of symbols**.

####Symbol export table

> When a PE needs to provide some functions or variables for use by other PE files, we refer to this action as **Symbol Exporting**.

To put it simply, in Windows PE, all exported symbols are centrally stored in a structure known as the **Export Table**, which provides a mapping between symbol names and their addresses. Symbols that need to be exported must be marked with the modifier `__declspec(dllexport)`.

####Symbol Import Table

The symbol import table is the key concept here, corresponding to the symbol export table. Let's start with an explanation of the concept:

> If we use functions or variables from a DLL in a program, we refer to this behavior as **Symbol Importing**.

The structure in Windows PE that stores the symbols of variables and functions to be imported, as well as information about the modules containing them, is called the **Import Table**. When Windows loads a PE file, one of the tasks is to resolve the addresses of all the functions that need to be imported and adjust the elements in the import table to the correct addresses. This way, during execution, the program can determine the actual addresses of the functions by querying the import table and make calls accordingly. The most important structure in the import table is the **Import Address Table (IAT)**, which contains the actual addresses of the imported functions.

By now, you might have guessed how we are going to achieve memory leak detection, right? Yes, it's by hacking the import table. To be more specific, we modify the addresses of memory allocation and deallocation functions in the import table of the modules we want to monitor to our custom functions. This way, we can track every memory allocation and deallocation of the module, enabling us to carry out the detection we desire without constraints.

More detailed knowledge about DLL linking can be found in "Linking" or other resources.

## Memory Leak Detector

Having understood the principle, the next step is to implement memory leak detection based on that principle. The following explanation will be based on my own implementation, which I have placed on my GitHub: [LeakDetector](https://github.com/disenone/LeakDetector).

####Replace function

First, let's take a look at the key function, located in [RealDetector.cpp](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)Please provide the text you would like translated into English.

```cpp linenums="1"
Replace a function in the Import Address Table (IAT) of importModule with a different function,
The "importModule" will call functions from another module, and the function that needs to be patched is...
* What we need to do is change import module to call our custom function.
 *
* - importModule (IN): The module to be processed, which requires patching functions that are called from other modules.
 *
- exportModuleName (IN): The name of the module from which the function needing patch comes.
 *
- exportModulePath (IN): The path where the export module is located, first attempt to load the export module using the path.
* If it fails, then load with name.
- importName (IN): Function name
 *
* - replacement (IN): Alternative function pointer
 *
Return Value: true if successful, false otherwise
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

Let's analyze this function. As the comments indicate, the purpose of this function is to change the address of a certain function in the IAT to the address of another function. First, let's take a look at lines 34-35:

``` cpp
idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
	TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
```

The function `ImageDirectoryEntryToDataEx` can return the address of a certain structure in the file header of a module. `IMAGE_DIRECTORY_ENTRY_IMPORT` specifies the import table structure, so the returned `idte` points to the module's import table.

Lines 36 to 40 are checking the validity of `idte`. At line 41, `idte->FirstThunk` points to the actual IAT. Therefore, lines 41 to 48 are about searching for the module that contains the functions needing replacement based on the module name. If it cannot be found, it means the functions of that module are not called, an error message should be prompted, and return.

After locating the module, we naturally need to find the function that needs to be replaced. Lines 55-62 open the module to which the function belongs, and line 64 locates the function's address. Since the IAT does not store names, we first need to locate the function based on its original address before modifying that function's address. Lines 68-80 are doing just that. Once the function is successfully found, we simply change the address to that of the `replacement`.

By now, we have successfully replaced the function in the IAT.

####Module and function names

Although we have already implemented the replacement of the IAT function `patchImport`, this function requires specifying the module name and function name. How can we determine which modules and functions are used for memory allocation and release in the program? To clarify this issue, we need to use the tool [Dependency Walker](http://www.dependencywalker.com/)In Visual Studio, create a new project, and use `new` in the `main` function to allocate memory. Compile the Debug version, then use `depends.exe` to open the outputted exe file, and you should see an interface similar to the one below (using my project [LeakDetectorTest](https://github.com/disenone/LeakDetector/tree/master/LeakDetectorTest)For example):

![](assets/img/2016-6-11-memory-leak-detector/depends.png)

It can be seen that LeakDetectorTest.exe is utilizing functions `malloc` and `_free_dbg` from uscrtbased.dll (not shown in the image), which are the functions we need to replace. Please note that the actual module function names may vary depending on your Windows and Visual Studio versions. Mine are Windows 10 and Visual Studio 2015. All you need to do is use depends.exe to determine the actual functions being called.

####Analyze the call stack.

(https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)。

####Detecting memory leaks

At this point, we have gathered all the Dragon Balls, so let's formally summon the Dragon.

I want to create a feature for detecting memory leaks locally (which is different from VLD, as VLD performs global detection and supports multi-threading). Therefore, I encapsulated another layer called `LeakDetector` on top of the class `RealDetector` that actually replaces the functions, and exposed the interface of `LeakDetector` to the users. When using it, simply construct `LeakDetector` to replace the functions and start detecting memory leaks. When `LeakDetector` is destructed, it will restore the original functions, terminate the memory leak detection, and print the results of the memory leak detection.

Test it with the code below:

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

The code directly `new` some memory without releasing it and just exited, the result printed by the program:

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

The program correctly identified instances where memory was allocated but not released at two specific locations, and printed out the complete call stack information. The desired functionality has been successfully implemented up to this point.

###Closing remarks

When you are not yet familiar with program linking, loading, and libraries, you might be bewildered about how to locate functions in shared link libraries, let alone replacing the functions of the link library with your own. Taking memory leak detection as an example, let's discuss how to replace functions in Windows DLLs. For a more detailed implementation, you can refer to the source code of VLD.

Additionally, I'd like to mention that "The Self-Improvement of a Programmer: Linking, Loading, and Libraries" is truly a great book, just my genuine thoughts and not a promotional mention.

--8<-- "footer_en.md"


> This post was translated using ChatGPT. Please provide feedback in [**反馈**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
