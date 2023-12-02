---
layout: post
title: Developing a Memory Leak Detector for Windows
categories:
- c++
tags:
- dev
description: 'Recently, I finished reading "The Self-Taught Programmer: Linking, Loading,
  and Libraries" (abbreviated as "Linking"). I gained a lot from it and thought about
  whether I could create some related code. Coincidentally, I found out about a memory
  leak detection tool for Windows called Visual Leak Detector (VLD) [https://vld.codeplex.com/].
  This tool tracks memory allocation and release by replacing the DLL interfaces responsible
  for memory management in Windows. Therefore, I decided to reference Visual Leak
  Detector and create a simple memory leak detection tool to understand DLL linking.'
figures:
- assets/post_assets/2016-6-11-memory-leak-detector/depends.png
---

<meta property="og:title" content="编写 Windows 下的 Memory Leak Detector" />

![](https://img.shields.io/badge/windows-10-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

## Preface

Recently, I finished reading "The Self-Taught Programmer: Linking, Loading, and Libraries" (referred to as "Linking" hereafter) and gained a lot of insights. I thought about whether I could create some related code snippets. Coincidentally, I learned about a memory leak detection tool called Visual Leak Detector for Windows [Visual Leak Detector](https://vld.codeplex.com/). This tool tracks memory allocation and deallocation by replacing the DLL interface responsible for memory management in Windows. Therefore, I have decided to reference Visual Leak Detector (referred to as VLD hereafter) and create a simplified memory leak detection tool to deepen my understanding of DLL linking.

## Background Knowledge

The book "Linking" provides a detailed explanation of the linking principles for executable files under Linux and Windows. In Windows, the executable file format is called Portable Executable (PE) file. The interpretation of DLL files is as follows:

DLL, short for Dynamic-Link Library, is the equivalent of shared objects in Linux. The DLL mechanism is widely used in the Windows system, to a great extent, even the structure of the Windows kernel relies heavily on the DLL mechanism. DLL files and EXE files in Windows are essentially the same concept, as they are both binary files in PE format. The only difference is that the PE file header contains a symbol that indicates whether the file is an EXE or a DLL. The extension of DLL files is not necessarily .dll, it could also be something else like .ocx (OCX control) or .CPL (Control Panel program).

There are also Python extension files like .pyd. The concept of memory leak detection that we are discussing here is called the symbol export/import table in DLLs.

#### Symbol Export Table

When a PE needs to provide some functions or variables to other PE files, we call this behavior **symbol exporting**.

Simply put, in Windows PE, all exported symbols are centrally stored in a structure called the **Export Table**, which provides a mapping between symbol names and symbol addresses. Symbols that need to be exported should be annotated with the modifier `__declspec(dllexport)`.

#### Symbol Import Table

Symbol import table is the key concept here, which corresponds to the symbol export table. Let's first take a look at the concept explanation:

If we use functions or variables from a DLL in a program, we refer to this behavior as **symbol importing**.

The structure in Windows PE that stores the symbols of variables and functions that modules need to import, as well as information about their location, is called the **Import Table**. When Windows loads a PE file, one of the tasks is to determine the addresses of all the functions that need to be imported and adjust the elements in the Import Table to the correct addresses. This allows the program to locate the actual addresses of the functions and make the necessary calls at runtime by querying the Import Table. The most important structure in the Import Table is the **Import Address Table (IAT)**, which stores the actual addresses of the imported functions.

By now, you might have already guessed how we are going to implement the memory leak detection :) That's right, it's by hacking the import table. Specifically, we will modify the addresses of the memory allocation and deallocation functions in the import table of the modules we want to monitor, replacing them with our own custom functions. This way, we will be able to track every memory allocation and deallocation made by the modules, giving us the freedom to perform the desired checks.

For more detailed knowledge about DLL linking, you can refer to the book "Linking" or other materials.

## Memory Leak Detector

After understanding the principle, the next step is to implement memory leak detection based on that principle. The following explanation will be based on my own implementation, which I have uploaded to my Github: [LeakDetector](https://github.com/disenone/LeakDetector).

#### Replace Function

Let's take a look at the key function, located in [RealDetector.cpp](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp):

```cpp linenums="1"
/* Replace a certain function in the IAT (Import Address Table) of importModule with another function.
   importModule calls a function from another module, and this is the function that needs to be patched.
   What we need to do is to make import module call our custom function instead.
 *
* - importModule (IN): The module to be processed. This module calls functions from other modules that need to be patched.
 *
- exportModuleName (IN): The name of the module from which the function to be patched is derived.
 *
* `- exportModulePath (IN): The path where the export module is located. It first tries to load the export module using the path, if that fails, it uses the name to load it.
* `- importName (IN): The name of the function.
 *
* - replacement (IN): a function pointer that serves as a substitute
 *
* Return Value: true if successful, false otherwise
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

Let's analyze this function, as the comment says, the purpose of this function is to change the address of a certain function in the IAT to the address of another function. Let's take a look at lines 34-35:

``` cpp
idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
	TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
```

The `ImageDirectoryEntryToDataEx` function can return the address of a certain structure in the file header of a module. The `IMAGE_DIRECTORY_ENTRY_IMPORT` specifies the import table structure, so the returned `idte` points to the import table of the module.

The code in lines 36-40 is checking the validity of `idte`. In line 41, `idte->FirstThunk` points to the actual Import Address Table (IAT). Therefore, lines 41-48 are used to search for the module that contains the function to be replaced based on the module name. If the module is not found, it means that the function from that module is not being called, and an error will be prompted and returned.

After finding the module, naturally, we need to locate the function to be replaced. On lines 55-62, we open the module to which the function belongs, and on line 64, we find the address of the function. Since the IAT does not save names, we need to first locate the function based on its original address, and then modify that address. Lines 68-80 are doing exactly that. Once the function is successfully found, we simply modify the address to `replacement`.

So far, we have successfully replaced the functions in IAT.

#### Module and Function Names

Although we have implemented the replacement of the IAT function `patchImport`, this function requires specifying the module name and function name. How can we know which module and function are used for memory allocation and deallocation in the program? To investigate this issue, we need to use the tool [Dependency Walker](http://www.dependencywalker.com/) on Windows. Create a new project in Visual Studio, use `new` to allocate memory in the `main` function, compile in Debug mode, and then use `depends.exe` to open the compiled exe file. You will see a similar interface as shown below (using my project [LeakDetectorTest](https://github.com/disenone/LeakDetector/tree/master/LeakDetectorTest) as an example):


![](assets/img/2016-6-11-memory-leak-detector/depends.png)

It can be seen that LeakDetectorTest.exe uses the `malloc` and `_free_dbg` functions from uscrtbased.dll (not shown in the image). These two functions are the ones we need to replace. Please note that the actual module function names may vary depending on your Windows and Visual Studio versions. In my case, I am using Windows 10 and Visual Studio 2015. What you need to do is use depends.exe to check the actual functions being called.

#### Analyzing Call Stack

To record memory allocation, it is necessary to record the call stack information at the time. Here, I don't intend to provide a detailed guide on how to obtain the current call stack information in Windows. The relevant function is `RtlCaptureStackBackTrace`, and there are many related resources available online. You can also take a look at the `printTrace` function in my code [here](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp).

#### Detecting Memory Leaks

[to_be_replace0]

At this point, we have collected all the Dragon Balls, and now it's time to officially summon Shenron.

I want to create a feature that can detect memory leaks locally (this is different from VLD, which performs global detection and supports multi-threading). So, I added another layer of encapsulation called `LeakDetector` on top of the actual replacement function class `RealDetector` and exposed the interface of `LeakDetector` to the user. To use it, simply construct a `LeakDetector`, which will replace the function and start detecting memory leaks. When the `LeakDetector` is destroyed, it will restore the original function, terminate the memory leak detection, and print the results of the memory leak detection.

Test with the following code:

[to_be_replaced[x]]

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

The code directly `new` some memory, without releasing it and then exits directly. The program prints the following result:

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

The program correctly identified the two instances where memory was allocated but not released, and printed out the complete call stack information. The required functionality has been completed up to this point.

### Conclusion

When you are not familiar with program linking, loading, and libraries, you may be confused about how to find functions in shared libraries, let alone replacing the library's functions with our own. Here, we take detecting memory leaks as an example and discuss how to replace functions in Windows DLLs. For a more detailed implementation, you can refer to the source code of VLD.

Also, I want to say that "The Self-Cultivation of Programmers: Linking, Loading, and Libraries" is really a good book. Just expressing my heartfelt admiration, not promotional content.

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
