---
layout: post
title: Windows 운영 체제에서 Memory Leak Detector 작성하기
categories:
- c++
tags:
- dev
description: '이번에 "프로그래머의 자기 계발: 링크, 로딩 및 라이브러리"라는 책을 읽고 많은 것을 얻었어요. 관련된 작은 코드를 만들어볼
  수 있을까 고민 중이에요. 우연히 Windows에서 내부 메모리 누수 검출 도구인 [비주얼 누수 감지기](https://vld.codeplex.com/)，이
  도구는 Windows에서 담당하는 메모리 관리를 대신하는 dll 인터페이스를 바꾸어 메모리 할당 및 해제를 추적하는 것입니다. 그래서 Visual
  Leak Detector를 참고하여 간단한 메모리 누수 검사 도구를 만들기로 결정했습니다 (이후 VLD로 간략히 표기), dll 링킹을 이해합니다.'
figures:
- assets/post_assets/2016-6-11-memory-leak-detector/depends.png
---

<meta property="og:title" content="编写 Windows 下的 Memory Leak Detector" />

![](https://img.shields.io/badge/windows-10-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##서론

이번에 '프로그래머의 자기계발: 링크, 로딩 및 라이브러리'를 다 읽었어. 많은 것을 얻고, 이와 관련된 작은 코드를 만들어볼 수 있을까 고민 중이야. 우연히 Windows에서 메모리 누수를 검사하는 도구인 [Visual Leak Detector](https://vld.codeplex.com/)이 도구는 Windows에서 메모리 관리를 담당하는 dll 인터페이스를 대체함으로써 메모리 할당 해제를 추적하는 것을 실현합니다. 따라서, Visual Leak Detector(이하 VLD로 간략히 표기)를 참고하여 간단한 메모리 누수 검사 도구를 만들기로 결정했습니다. dll 링킹을 이해하는 것이 중요합니다.

##준비 지식
"Linkers"라는 책은 Linux 및 Windows에서 실행 파일 링킹의 원리를 자세히 설명하며, Windows에서 실행 파일 형식은 PE(Portable Executable) 파일이라고합니다. DLL 파일은 다음과 같이 설명됩니다:

> DLL은 Dynamic-Link Library의 약자로, Linux에서의 공유 라이브러리와 유사한 역할을 한다. Windows 시스템에서는 이러한 DLL 메커니즘을 대규모로 활용하며, 심지어 Windows 커널의 구조도 크게 DLL 메커니즘에 의존하고 있다. Windows의 DLL 파일과 EXE 파일은 사실상 동일한 개념으로, 둘 다 PE 형식의 바이너리 파일이다. 약간 다른 점은 PE 파일 헤더에 파일이 EXE인지 DLL인지를 나타내는 플래그가 있으며, DLL 파일의 확장자가 반드시 .dll일 필요는 없고, .ocx(OCX 컨트롤)나 .CPL(컨트롤패널 프로그램) 등 다른 확장자를 가질 수도 있다.

파이썬의 확장 파일인 .pyd와 같은 것도 있습니다. 그리고 DLL에서는 여기서의 메모리 누수 감지와 관련된 개념으로 **심볼 내보내기/가져오기 테이블**이 있습니다.

####기호 출력 표

> 다른 PE 파일에서 일부 함수 또는 변수를 사용할 수 있도록 PE가 제공해야 할 때, 우리는 이를 "심볼 내보내기(Symbol Exporting)"라고 부릅니다.

Windows PE에서 간단히 설명하면, 모든 내보낸 심볼은 **Export Table**이라고 불리는 구조에 집중적으로 저장됩니다. 이는 심볼 이름과 심볼 주소 간의 매핑을 제공합니다. 내보내야 하는 심볼에는 `__declspec(dllexport)` 수식어를 추가해야 합니다.

####기호 도입 표

기호 가져오기 표는 여기서의 핵심 개념이에요. 이는 기호 내보내기 표와 대응하는데, 먼저 개념 설명을 살펴봅시다:

> 만약 우리가 DLL에서 함수나 변수를 사용한다면, 이러한 행위를 **심볼 가져오기(Symbol Importing)**라고 부릅니다.

Windows PE에서 모듈이 필요로 하는 변수와 함수의 심볼, 그리고 해당 모듈에 대한 정보를 저장하는 구조를 **Import Table(가져오기 테이블)**이라고 합니다. Windows가 PE 파일을 로드할 때 해야 할 일 중 하나는 모든 필요한 함수 주소를 결정하고 Import Table의 요소를 올바른 주소로 조정하여 실행 중에 프로그램이 실제 함수의 주소를 찾고 호출할 수 있도록 하는 것입니다. Import Table에서 가장 중요한 구조는 **Import Address Table(IAT, 가져오기 주소 배열)**이며, 여기에는 가져온 함수의 실제 주소가 저장됩니다.

여기까지 읽었을 때 우리가 달성하려는 메모리 누수 감지 방법을 이미 짐작했나요 :) ? 맞아요, 바로 import table을 해킹하는 것인데, 구체적으로 말하면 검사해야 하는 모듈의 import table에서 메모리 할당 및 해제 함수의 주소를 우리가 정의한 함수로 바꿔버리는 것이죠. 그러면 모듈이 메모리를 할당하고 해제하는 상황을 모두 파악할 수 있게 되어 우리가 원하는 검사를 마음껏 할 수 있게 됩니다.

DLL 링크에 대한 더 자세한 정보는 "링크"나 다른 자료를 참조하시기 바랍니다.

## Memory Leak Detector

원리를 이해했으니, 이제는 그 원리를 기반으로 메모리 누수 검사를 구현하는 것이다. 다음 설명은 나의 구현에 기반하여 이루어지며, 이를 내 GitHub에 올려두었습니다: [LeakDetector](https://github.com/disenone/LeakDetector)Thank you for providing the text. Here is the translation into Korean:

"。" -> "。"

####함수 대체

주요 함수인 [RealDetector.cpp](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)I'm sorry, but I cannot provide a translation for this text as it does not contain any content. If you provide me with a text to translate, I'll be happy to assist you.

```cpp linenums="1"
importModule에서 IAT(Import Address Table)의 특정 함수를 다른 함수로 교체합니다.
importModule은 다른 모듈의 함수를 호출하게 됩니다. 이 함수가 바꿔야 하는 함수입니다.
우리가 해야 할 일은 import 모듈을 우리가 만든 함수를 호출하도록 변경하는 것이다.
 *
- importModule (IN): 패치가 필요한 다른 모듈을 호출하는 모듈에서 처리해야 할 모듈
 *
- exportModuleName (IN): 패치가 필요한 함수가 속한 모듈 이름
 *
-exportModulePath (IN): export module가 있는 경로입니다. export module을로드하기 위해 먼저 경로를 사용하여 export module을로드하고,
만약 실패하면, 'name'을 사용하여로드하세요.
- importName (IN): 함수명
 *
- replacement (IN): 替代 함수 포인터
 *
반환 값: 성공 true, 그렇지 않으면 false
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

우리가 이 함수를 분석해 보겠습니다. 주석에 쓰여 있는 대로, 이 함수의 목적은 IAT 안에 있는 특정 함수의 주소를 다른 함수의 주소로 변경하는 것입니다. 먼저 34-35 줄을 살펴봅시다:

``` cpp
idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
	TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
```

`ImageDirectoryEntryToDataEx` 함수는 모듈의 파일 헤더에서 특정한 구조체의 주소를 반환할 수 있습니다. `IMAGE_DIRECTORY_ENTRY_IMPORT`은 가져올 테이블 구조체를 지정하는데, 그래서 반환된 `idte`는 모듈의 가져오기 테이블을 가리키게 됩니다.

36-40번 라인은 'idte'를 확인하는 부분이야. 41번 라인에서 'idte->FirstThunk'가 실제 IAT를 가리키고 있어. 그래서 41-48번 라인은 모듈 이름을 기반으로 대체해야 하는 함수를 찾고 있어. 모듈을 찾을 수 없다면 해당 모듈을 호출하지 않은 거니까 에러를 알리고 반환해야 해.

모듈을 찾은 후에는 자연스럽게 교체해야 할 그 함수를 찾아야 해. 55-62번 줄에서 함수가 속한 모듈을 열고, 64번 줄에서 함수 주소를 찾아. IAT가 이름을 저장하지 않았기 때문에 기존 함수 주소로 함수를 찾아 수정한 후, 68-80번 줄에서 이 작업을 수행해. 함수를 성공적으로 찾으면 단순하게 주소를 '대체'의 주소로 수정해.

여기까지, 우리는 성공적으로 IAT에서 함수를 대체했습니다.

####모듈과 함수 이름

IAT 함수 `patchImport`를 대체하는 데 성공했지만, 이 함수는 모듈 이름과 함수 이름을 지정해야 해. 그러면 프로그램의 메모리 할당 및 해제에 어떤 모듈과 함수가 사용되었는지 어떻게 알 수 있을까? 이 문제를 해결하기 위해 Windows 도구인 [Dependency Walker](http://www.dependencywalker.com/)Visual Studio에서 새 프로젝트를 만들고 `main` 함수에서 `new`를 사용하여 메모리를 할당하십시오. 디버그 버전으로 컴파일한 후 `depends.exe`를 사용하여 컴파일된 exe 파일을 열면 [LeakDetectorTest](https://github.com/disenone/LeakDetector/tree/master/LeakDetectorTest)예를 들어) : 

![](assets/img/2016-6-11-memory-leak-detector/depends.png)

LeakDetectorTest.exe에서 uscrtbased.dll의 'malloc' 및 '_free_dbg' 기능을 사용했다는 것을 알 수 있습니다. 이 두 함수가 우리가 대체해야 하는 함수입니다. 실제 모듈 함수 이름은 Windows 및 Visual Studio 버전에 따라 다를 수 있습니다. 제 시스템은 Windows 10 및 Visual Studio 2015이기 때문에, 실제 호출되는 함수를 확인하려면 depends.exe를 사용해야 합니다.

####호출 스택 분석

(https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)。

####메모리 누수 검사

지금까지 우리는 용띠도 모두 모았어. 이제 공식적으로 신룡을 소환하자.

저는 부분 메모리 누수를 감지할 수 있는 기능을 가진 걸 만들고 싶어요. 이건 VLD와는 다르게 작동해요. VLD는 전역적인 감지를 하고 여러 쓰레드를 지원해요. 그래서 실제 함수를 바꾸는 `RealDetector` 클래스에 다시 `LeakDetector` 라는 층을 덧씌웠어요. 그리고 `LeakDetector`의 인터페이스를 사용자에게 노출시켰어요. 사용할 때는 `LeakDetector`를 작성하면 됩니다. 함수를 대체하고 메모리 누수를 감지할 수 있어요. `LeakDetector`가 소멸될 때 원래 함수를 복원하고 메모리 누수를 중지하며 감지 결과를 인쇄해요.

아래 코드를 사용하여 테스트해보세요:

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

코드가 메모리를 직접 `new`해서 할당하고 프로그램이 해제하지 않은 채로 종료되어서 출력된 결과:

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

프로그램이 메모리를 두 군데에서 요청했지만 해제하지 않은 부분을 정확하게 찾아내어 완전한 호출 스택 정보를 출력했습니다. 우리가 필요로 했던 기능은 여기까지 완료되었습니다.

###맺음말

프로그램 링크, 로딩 및 라이브러리에 대해 잘 모르는 경우에는 공유 라이브러리 함수를 어떻게 찾아야 할지 혼란스러울 수 있습니다. 특히 라이브러리 함수를 우리 자신의 함수로 교체하는 것은 더욱 어려울 수 있습니다. 예를 들어 메모리 누수 검사를 위해 Windows DLL 함수를 교체하는 방법에 대해 살펴보겠습니다. 더 자세한 구현은 VLD 소스 코드를 참조하십시오.

그리고 더 말하고 싶은 게, "프로그래머의 자기 성장: 링크, 로딩 및 라이브러리"는 정말 좋은 책이에요. 순수한 감회에 소프트 광고가 전혀 아니에요.

--8<-- "footer_ko.md"


> 본 게시물은 ChatGPT를 사용하여 번역된 것이니, 문제 발견 시 [**피드백**](https://github.com/disenone/wiki_blog/issues/new)모든 빠진 부분을 지적하세요. 
