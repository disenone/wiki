---
layout: post
title: Developing Memory Leak Detector for Windows.
categories:
- c++
tags:
- dev
description: 'I recently finished reading "Self-Cultivation for Programmers: Linking,
  Loading, and Libraries" (hereinafter referred to as "Linking") and gained a lot
  from it. I''m thinking about whether I can create some related small codes. Coincidentally,
  I came across a memory leak detection tool called Visual Leak Detector for Windows
  (https://vld.codeplex.com/). This tool tracks memory allocation and release by replacing
  the DLL interface responsible for memory management in Windows. So, I decided to
  refer to Visual Leak Detector (hereinafter referred to as VLD) to create a simple
  memory leak detection tool and understand DLL linking.'
figures:
- assets/post_assets/2016-6-11-memory-leak-detector/depends.png
---


![](https://img.shields.io/badge/windows-10-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

## Foreword

Recently finished reading "Programmer's Self-cultivation: Linking, Loading, and Library" (referred to as "Linking" hereafter), gained a lot from it, and wondered if I could create some related code. Coincidentally, I came to know about a memory leak detection tool for Windows called [Visual Leak Detector](https://vld.codeplex.com/). This tool tracks memory allocation and deallocation by replacing the dll interface responsible for memory management in Windows. Therefore, I decided to refer to Visual Leak Detector (referred to as VLD hereafter) to create a simple memory leak detection tool and understand dll linking.

## Prerequisites
The book "Linking" provides a detailed explanation of the linking principles for executable files in Linux and Windows. The executable file format in Windows is called PE (Portable Executable) file. And here is the explanation of DLL files:

DLL, short for Dynamic-Link Library, is the abbreviation for a dynamic link library, which is equivalent to a shared object in Linux. The DLL mechanism is widely used in the Windows system, to the extent that even the structure of Windows kernel relies heavily on this mechanism. DLL files and EXE files in Windows are actually the same concept, both being binary files in PE format. The only difference is that there is a symbol in the PE file header indicating whether the file is an EXE or a DLL. Moreover, the file extension of a DLL does not necessarily have to be .dll; it could also be .ocx (OCX control) or .CPL (Control Panel Program), among others.

还有比如 Python 的扩展文件 .pyd。而 DLL 中有关我们这里内存泄露检测的概念是**符号导出导入表**。

There are also extension files in Python, such as .pyd. The concept related to memory leak detection in DLLs is symbol export/import table.

#### Symbol Export Table

When a PE needs to provide some functions or variables for other PE files to use, we call this behavior **Symbol Exporting**.

Simply put, in Windows PE, all exported symbols are stored in a structure called the **导出表 (Export Table)**, which provides a mapping between symbol names and symbol addresses. Symbols that need to be exported must be annotated with the modifier `__declspec(dllexport)`.

#### Symbol Import Table

The symbol import table is the key concept here, which corresponds to the symbol export table. Let's first look at the concept explanation:

If we use functions or variables from DLL in a certain program, we call this behavior **symbol importing**.

The structure in Windows PE that stores the symbols of the variables and functions that need to be imported, as well as the information about the modules they are located in, is called the **Import Table**. When Windows loads a PE file, one of the tasks is to determine the addresses of all the functions that need to be imported and adjust the elements in the import table to the correct addresses. This allows the program to locate the actual addresses of the functions and make calls at runtime by querying the import table. The most important structure in the import table is the **Import Address Table (IAT)**, which stores the actual addresses of the imported functions.

By now, I bet you've already guessed how we're going to implement memory leak detection :) That's right, we're going to hack the import table. Specifically, we're going to modify the addresses of the functions related to memory allocation and deallocation in the import table of the module we want to check. By doing this, we'll be able to track every memory allocation and deallocation made by the module, giving us the freedom to perform the detection we desire.

For more detailed knowledge about DLL linkage, you can refer to the book "Linkage" or other resources.

## Memory Leak Detector

Understood the principle, next is to implement memory leak detection based on the principle. The following explanation will be based on my own implementation, which I have placed on my Github: [LeakDetector](https://github.com/disenone/LeakDetector).

#### replace function

Let's start by looking at the key function, located in [RealDetector.cpp](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp):

```cpp linenums="1"
```plaintext
/* Replace a function in the Import Address Table (IAT) of importModule with a different function.
 * importModule calls a function from another module, which is the function that needs to be patched.
 * What we need to do is modify import module to call our custom function instead.
```
 *
* - importModule (IN): The module to be processed, which calls functions in other modules that need to be patched.
 *
* - exportModuleName (IN): Name of the module from which the function to be patched is sourced.
 *
- exportModulePath (IN): The path where the export module is located. First, try to load the export module using the path. If it fails, load it using the name.
- importName (IN): The name of the function.
 *
- replacement (IN): equivalent function pointer
 *
* Return Value: true if successful, otherwise false
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

Let's analyze this function, as the comment says, the purpose of this function is to change the address of a certain function in the IAT to the address of another function. Now let's look at lines 34-35:

``` ruby
idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
	TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
```

The `ImageDirectoryEntryToDataEx` function can return the address of a specified structure in the file header of a module. The `IMAGE_DIRECTORY_ENTRY_IMPORT` specifies the import table structure, so the returned `idte` points to the import table of the module.

Lines 36-40 check the validity of `idte`. Line 41, `idte->FirstThunk`, points to the actual Import Address Table (IAT). Therefore, lines 41-48 are used to search for the module that contains the functions to be replaced based on the module name. If the module is not found, it means that the module's functions are not being called, so an error message is displayed and returned.

After locating the module, naturally, we need to find the function to be replaced. On lines 55-62, we open the module to which the function belongs, and on line 64, we find the address of the function. Since the Import Address Table (IAT) does not store the names, we first need to locate the function based on its original address, and then modify that address. Lines 68-80 are where this is being done. Once the function has been successfully found, we simply replace its address with the address of `replacement`.

So far, we have successfully replaced the functions in IAT.

#### Module and Function Names

Although we have already implemented the replacement of the IAT function `patchImport`, this function requires specifying the module name and function name. So how do we know which module and function the program uses for memory allocation and deallocation? To clarify this issue, we need to use the Windows tool [Dependency Walker](http://www.dependencywalker.com/). In Visual Studio, create a new project and use `new` in the `main` function to allocate memory. Compile the debug version, and then use `depends.exe` to open the compiled exe file. You can see a similar interface as shown below (using my project [LeakDetectorTest](https://github.com/disenone/LeakDetector/tree/master/LeakDetectorTest) as an example):


![](assets/img/2016-6-11-memory-leak-detector/depends.png)

You can see that LeakDetectorTest.exe uses the `malloc` and `_free_dbg` functions from uscrtbased.dll (not displayed in the figure), which are the functions we need to replace. Note that the actual module function names may depend on your Windows and Visual Studio versions. Mine are Windows 10 and Visual Studio 2015. What you need to do is use depends.exe to see what functions are actually being called.

#### Analyzing Call Stack

Memory allocation recording requires recording the call stack information at that time. Here I don't intend to elaborate on how to obtain the current call stack information in Windows. The relevant function is `RtlCaptureStackBackTrace`, and there is plenty of related information available online. You can also take a look at the `printTrace` function in my code [here](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp).

#### Detecting Memory Leaks

So far, we have collected all the Dragon Balls. Now, we will formally summon Shenron.

I want to make it possible to detect memory leaks locally (this is different from VLD, which does global detection and supports multiple threads). So I added another layer of "LeakDetector" on top of the actual replacement function class "RealDetector" and exposed the interface of "LeakDetector" to the user. To use it, just instantiate "LeakDetector", which completes the function replacement and starts detecting memory leaks. When "LeakDetector" is destructed, the original function is restored, the memory leak detection is aborted, and the results of the memory leak detection are printed.

Test with the following code:

```
[to_be_replaced[x]]
```

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

The code directly `new` some memory, without releasing it and then exits. The program prints the result:


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

The program correctly identifies two memory allocations that have not been released and prints the complete call stack information. The required functionality has been completed at this point.

### Conclusion

When you are not familiar with program linking, loading, and libraries, you may be confused about how to find functions in shared libraries, let alone replacing library functions with our own functions. Here, we take memory leak detection as an example to discuss how to replace functions in Windows DLL. For a more detailed implementation, you can refer to the source code of VLD.

Additionally, I'd like to say that "The Self-Cultivation of Programmers: Linking, Loading and Libraries" is a really good book, just expressing my genuine admiration, not advertising.

> Original: <https://disenone.github.io/wiki>  
> This post is protected by [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by/4.0/deed.en) agreement, should be reproduced with attribution.


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
