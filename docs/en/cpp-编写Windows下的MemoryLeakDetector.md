---
layout: post
title: Developing a Memory Leak Detector for Windows
categories:
- c++
tags:
- dev
description: 'Recently, I finished reading "The Self-Cultivation of Programmers: Linking,
  Loading, and Libraries" (hereafter referred to as "Linking") and gained a lot from
  it. I''m now thinking about whether I can create some related code. I happened to
  learn about a memory leak detection tool for Windows called Visual Leak Detector
  (VLD) (available at https://vld.codeplex.com/). This tool tracks memory allocation
  and deallocation by replacing the dll interfaces responsible for memory management
  on Windows. Therefore, I''ve decided to reference Visual Leak Detector and develop
  a simple memory leak detection tool to better understand dll linking.'
figures:
- assets/post_assets/2016-6-11-memory-leak-detector/depends.png
---

<meta property="og:title" content="编写 Windows 下的 Memory Leak Detector" />

![](https://img.shields.io/badge/windows-10-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

## Preface

Recently, I finished reading "The Self-Cultivation of Programmers: Linking, Loading, and Libraries" (hereinafter referred to as "Linking") and gained a lot of knowledge. I started to think about whether I can create some related small code. Coincidentally, I learned about a memory leak detection tool called Visual Leak Detector for Windows (https://vld.codeplex.com/). This tool tracks memory allocation and release by replacing the dll interfaces responsible for memory management in Windows. Therefore, I decided to refer to Visual Leak Detector (hereinafter referred to as VLD) and create a simple memory leak detection tool to understand dll linking.

## Background knowledge
The book "Linking" provides a detailed explanation of the linking principles for executable files in Linux and Windows, and the executable file format in Windows is called PE (Portable Executable) file. As for the DLL file, it is explained as follows:

DLL, short for Dynamic-Link Library, is the equivalent of shared objects in Linux. The DLL mechanism is widely used in the Windows system, to the extent that even the structure of the Windows kernel relies heavily on it. DLL files in Windows are conceptually similar to EXE files; they are both binary files in the PE format. The only difference is that the PE file header contains a flag indicating whether the file is an EXE or a DLL. The extension of a DLL file is not necessarily .dll, it could also be something else, such as .ocx (OCX controls) or .CPL (Control Panel programs).

There are also examples such as Python's extension file `.pyd`. And the concept of memory leak detection in DLL is **symbol export import table**.

#### Symbol Export Table

When a PE needs to provide some functions or variables to be used by other PE files, we call this behavior **symbol exporting**.

To understand it simply, in Windows PE, all exported symbols are centrally stored in a structure called the **Export Table**, which provides a mapping relationship between symbol names and symbol addresses. Symbols that need to be exported require the modifier `__declspec(dllexport)`.

#### Symbol Import Table

Symbol import table is the key concept here, it corresponds to the symbol export table. Let's first take a look at the concept explanation:

If we use functions or variables from a DLL in a program, this behavior is called **symbol importing**.

The structure in Windows PE that stores the symbols of variables and functions to be imported, as well as information about the modules in which they are located, is called the **Import Table**. When Windows loads a PE file, one of the tasks is to determine the addresses of all the functions to be imported and adjust the elements in the Import Table to the correct addresses. This allows the program to query the Import Table at runtime to locate the actual addresses of the functions and make the calls. The most important structure in the Import Table is the **Import Address Table (IAT)**, which contains the actual addresses of the imported functions.

Seeing this, I believe you've already guessed how we're going to implement memory leak detection :) That's right, it's about hacking the import table. Specifically, we modify the addresses of functions related to memory allocation and deallocation in the import table of the module we want to monitor, and replace them with our custom functions. This way, we can monitor the memory allocation and deallocation behavior of the module and perform the detection we desire.

For more detailed information about DLL linking, you can refer to the book "Linking" or other resources.

## Memory Leak Detector

Once the principle is understood, the following step is to implement memory leak detection based on this principle. The explanation below will be based on my own implementation, which I have uploaded to my GitHub: [LeakDetector](https://github.com/disenone/LeakDetector).

#### Replace Function

First, let's take a look at the key function, located in [RealDetector.cpp](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp):

```cpp linenums="1"
/* Replace a function in the IAT (Import Address Table) of importModule with another function.
 * importModule calls a function from another module, and this function is the one that needs to be patched.
 * What we need to do is to make importModule call our custom function instead.
 *
* `importModule (IN):` The module to be processed that calls functions from other modules that need to be patched.
 *
* `- exportModuleName (IN)`: Name of the module from which the function to be patched originates.
 *
- `exportModulePath` (IN): The path where the export module is located. First, attempt to load the export module using the `path`. If unsuccessful, use the `name` to load.
- `importName` (IN): The name of the function.
 *
- replacement (IN): substitute function pointer
 *
* Return Value: true if success, otherwise false.
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

Let's analyze this function, just as the comment suggests, the function's purpose is to change the address of a certain function in the IAT to the address of another function. Let's look at lines 34-35:

``` ruby
idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
	TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
```

The `ImageDirectoryEntryToDataEx` function can return the address of a certain structure in the file header of a module. The `IMAGE_DIRECTORY_ENTRY_IMPORT` specifies the import table structure, so the returned `idte` points to the import table of the module.

Lines 36-40 are checking the validity of `idte`. Line 41, `idte->FirstThunk`, points to the actual IAT. Therefore, lines 41-48 are searching for the module that contains the function to be replaced based on the module name. If it cannot be found, it means that the module's function is not being called, so an error message is displayed and returned.

After finding the module, naturally, we need to locate the function to be replaced. Open the module to which the function belongs on lines 55-62, and find the function address on line 64. Since IAT does not store names, we need to first locate the function based on its original address and then modify the function address. This process is carried out on lines 68-80. Once the function is successfully located, the address is simply modified to the address of `replacement`.

So far, we have successfully replaced the functions in IAT.

#### Module and Function Names

Although we have already implemented the replacement of the IAT function `patchImport`, this function requires specifying the module name and function name. How do we know which module and function are used for memory allocation and deallocation in the program? To clarify this issue, we need to use the tool [Dependency Walker](http://www.dependencywalker.com/) available on Windows. In Visual Studio, create a new project and use `new` in the `main` function to allocate memory. Compile the Debug version and then use `depends.exe` to open the compiled exe file. You will see a similar interface as shown below (using my project [LeakDetectorTest](https://github.com/disenone/LeakDetector/tree/master/LeakDetectorTest) as an example):

![](assets/img/2016-6-11-memory-leak-detector/depends.png)

You can see that LeakDetectorTest.exe uses the `malloc` and `_free_dbg` functions from the uscrtbased.dll (not shown in the image). These are the functions that we need to replace. Please note that the actual module function names may vary depending on your Windows and Visual Studio version. In my case, I am using Windows 10 and Visual Studio 2015. What you need to do is use depends.exe to see which functions are actually being called.

#### Analyzing Call Stack

To record the memory allocation, it is necessary to record the call stack information at that time. I do not intend to provide a detailed explanation of how to obtain the current call stack information under Windows. The relevant function is `RtlCaptureStackBackTrace`. There is a lot of information available online, and you can also take a look at the function `printTrace` in the code that I have provided [here](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp).

#### Detecting Memory Leaks

To this point, we have collected all of the Dragon Balls. Now, we're officially summoning Shenron.

I want to create a feature that can locally detect memory leaks (this is different from VLD, which does global detection and supports multi-threading). So, I wrapped another layer called `LeakDetector` around the actual replacement function class `RealDetector`, and exposed the interface of `LeakDetector` to the users. To use it, simply construct `LeakDetector`, which will replace the function and start detecting memory leaks. When `LeakDetector` is destructed, it will restore the original function, terminate memory leak detection, and print the results of memory leak detection.

Test with the following code:


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

The code directly allocated some memory using `new`, without releasing it before quitting. The program's output is:

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

The program correctly identified the two places where memory was allocated but not released and printed the complete call stack information. The desired functionality has been completed at this point.

### Conclusion

When you are not familiar with program links, loading, and libraries, you may feel confused about how to find functions in shared libraries, let alone replacing the library's functions with our own functions. Take memory leak detection as an example, here we will discuss how to replace functions in Windows DLL. For more detailed implementation, you can refer to the source code of VLD.

Another thing I'd like to mention is that "The Self-Cultivation of Programmers: Linking, Loading, and Libraries" is really a great book. It's not just a shameless promotion, but truly a good read.

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
