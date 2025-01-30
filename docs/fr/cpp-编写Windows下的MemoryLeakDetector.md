---
layout: post
title: Rédigez un détecteur de fuites de mémoire pour Windows.
categories:
- c++
tags:
- dev
description: 这段时间我读完了《程序员的自我修养：链接、装载与库》（以下简称《链接》），收获颇丰，想着能否做一些相关的小代码。恰好知道在 Windows
  下有一个内存泄露检测工具 [Visual Leak Detector](https://vld.codeplex.com/)Ce outil fonctionne
  en remplaçant les interfaces dll responsables de la gestion de la mémoire sous Windows
  pour suivre l'allocation et la libération de mémoire. C'est pourquoi j'ai décidé
  de m'inspirer de Visual Leak Detector (abrégé VLD par la suite) pour créer un outil
  simple de détection de fuites de mémoire, en comprenant les liens des dll.
figures:
- assets/post_assets/2016-6-11-memory-leak-detector/depends.png
---

<meta property="og:title" content="编写 Windows 下的 Memory Leak Detector" />

![](https://img.shields.io/badge/windows-10-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##Préface

(https://vld.codeplex.com/)Ce dispositif fonctionne en remplaçant l'interface de la dll chargée de la gestion de la mémoire sous Windows afin de tracer les allocations et libérations de mémoire. Ainsi, j'ai décidé de m'inspirer de Visual Leak Detector (abrégé VLD par la suite) pour créer un outil simplifié de détection de fuites mémoire, en comprenant les liens des dll.

##Prérequis
Le livre 《链接》 explique en détail les principes de liaison des fichiers exécutables sous Linux et Windows, où le format de fichier exécutable sous Windows est appelé fichier PE (Portable Executable). L'explication des fichiers DLL est la suivante :

> DLL est l'abréviation de Dynamic-Link Library, qui correspond à l'objet partagé sous Linux. Le système Windows utilise largement ce mécanisme de DLL, même la structure du noyau de Windows dépend fortement du mécanisme de DLL. Les fichiers DLL et les fichiers EXE sous Windows sont en fait des concepts similaires, ce sont des fichiers binaires au format PE. La différence réside dans un symbole dans l'en-tête du fichier PE indiquant s'il s'agit d'un EXE ou d'un DLL. De plus, l'extension des fichiers DLL n'est pas forcément .dll, elle peut également être autre chose, comme .ocx (contrôle OCX) ou .CPL (programme du panneau de configuration).

Il y a aussi des fichiers d'extension comme .pyd pour Python. Quant au concept de détection de fuites de mémoire ici, dans les DLL, il s'agit de la **table des exportations et des importations de symboles**.

####Table d'exportation des symboles

> Lorsque un PE doit fournir certaines fonctions ou variables pour être utilisées par d'autres fichiers PE, nous appelons cette action **exportation de symbole (Symbol Exporting)**.

Pour comprendre simplement, dans Windows PE, tous les symboles exportés sont regroupés dans une structure appelée **Export Table**, qui fournit une correspondance entre le nom du symbole et son adresse. Les symboles devant être exportés doivent être précédés du modificateur `__declspec(dllexport)`.

####Table des caractères spéciaux

Le tableau d'importation de symboles est un concept clé ici, il correspond au tableau d'exportation de symboles, commençons par examiner les explications conceptuelles :

> Si nous utilisons des fonctions ou des variables provenant d'une DLL dans un certain programme, nous appelons ce comportement **importation de symboles (Symbol Importing)**.

Dans Windows PE, la structure contenant les symboles des variables et des fonctions à importer, ainsi que des informations sur le module, est appelée **table d'importation (Import Table)**. Lorsque Windows charge un fichier PE, l'une des tâches consiste à déterminer les adresses de toutes les fonctions à importer et à ajuster les éléments de la table d'importation vers les adresses correctes, permettant ainsi au programme, lors de l'exécution, de localiser l'adresse réelle des fonctions via la consultation de la table d'importation et de les appeler. La structure la plus importante de la table d'importation est **le tableau des adresses d'importation (Import Address Table, IAT)**, qui contient les adresses réelles des fonctions importées.

Vous avez probablement deviné comment nous allons réaliser la détection de fuites mémoire, n'est-ce pas ? Exactement, il s'agit de pirater la table d'importation. Plus précisément, il s'agit de remplacer par nos propres fonctions personnalisées les adresses des fonctions d'allocation et de libération de mémoire dans la table d'importation des modules à tester. Ainsi, nous pouvons suivre chaque allocation et libération de mémoire du module, ce qui nous permet de réaliser la détection que nous souhaitons.

Des informations plus détaillées sur les liens DLL peuvent être consultées dans le document "Lien" ou d'autres ressources.

## Memory Leak Detector

Une fois que vous avez compris le principe, il est temps de passer à la détection des fuites de mémoire basée sur ce principe. Les explications ci-dessous seront basées sur ma propre implémentation, que j'ai mise sur mon Github : [LeakDetector](https://github.com/disenone/LeakDetector)I'm sorry, but there is no text to translate.

####Remplacement de la fonction

Commençons par la fonction clé, située dans [RealDetector.cpp](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)Veuillez traduire le texte suivant en français :

```cpp linenums="1"
Remplacez une fonction de la table d'adresses d'importation (IAT) dans importModule par une autre fonction,
* importModule appelera une fonction d'un autre module, cette fonction est celle qui doit être patchée.
* Ce que nous devons faire, c'est remplacer l'importation du module par l'appel de notre fonction personnalisée.
 *
- importModule (IN): Le module à traiter, ce module appelle des fonctions d'autres modules qui doivent être patchées
 *
* - exportModuleName (IN) : le nom du module d'où provient la fonction nécessitant un patch
 *
* - exportModulePath (IN) : le chemin où se trouve le module d'exportation, d'abord essayer de charger le module d'exportation avec le chemin.
Si échec, charger avec name
- importName (IN): nom de la fonction
 *
* - replacement (IN): Pointeur de fonction alternatif
 *
Retour de la valeur : true si réussi, sinon false
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

Analysons cette fonction comme indiqué dans les commentaires. Cette fonction vise à remplacer l'adresse d'une fonction spécifique dans la table des adresses importées par une autre adresse. Examinons les lignes 34 à 35:

``` cpp
idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
	TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
```

La fonction `ImageDirectoryEntryToDataEx` peut renvoyer l'adresse d'une certaine structure dans l'en-tête du fichier du module, `IMAGE_DIRECTORY_ENTRY_IMPORT` spécifie la structure de table d'importation à rechercher, ainsi `idte` renvoie spécifiquement vers la table d'importation du module.

Les lignes 36 à 40 vérifient la validité de 'idte'. À la ligne 41, 'idte->FirstThunk' pointe vers l'IAT réel. Par conséquent, les lignes 41 à 48 recherchent le module contenant les fonctions à remplacer en fonction du nom du module. Si rien n'est trouvé, cela signifie que le module appelant les fonctions n'a pas été trouvé, il affiche alors un message d'erreur et retourne.

Une fois le module trouvé, naturellement, nous devons localiser la fonction à remplacer, ouvrir le module du 55e au 62e ligne, puis trouver l'adresse de la fonction à la 64e ligne. Comme l'IAT ne conserve pas le nom, il est nécessaire de localiser d'abord la fonction en fonction de son adresse d'origine, puis de modifier cette adresse de fonction, ce qui est ce que font les lignes 68 à 80. Une fois que la fonction est trouvée avec succès, il suffit de remplacer simplement l'adresse par l'adresse de `replacement`.

À ce stade, nous avons réussi à remplacer la fonction dans l'IAT.

####Noms de modules et de fonctions

Bien que nous ayons réussi à remplacer la fonction IAT `patchImport`, cette fonction nécessite de spécifier le nom du module et le nom de la fonction. Alors, comment savons-nous quel module et quelle fonction sont utilisés pour l'allocation et la libération de mémoire du programme ? Pour clarifier ce point, nous devons recourir à l'outil [Dependency Walker](http://www.dependencywalker.com/)Dans Visual Studio, créez un nouveau projet, puis utilisez `new` dans la fonction `main` pour allouer de la mémoire. Compilez la version Debug, puis utilisez `depends.exe` pour ouvrir le fichier exe compilé. Vous pourrez voir une interface similaire à celle-ci (avec mon projet [LeakDetectorTest](https://github.com/disenone/LeakDetector/tree/master/LeakDetectorTest)例如）：

![](assets/img/2016-6-11-memory-leak-detector/depends.png)

On peut voir que LeakDetectorTest.exe utilise les fonctions `malloc` et `_free_dbg` de uscrtbased.dll (non affichées dans l'image), ce sont les fonctions que nous devons remplacer. Il faut faire attention car les noms réels des fonctions peuvent varier en fonction de votre version de Windows et de Visual Studio, pour ma part j'utilise Windows 10 et Visual Studio 2015, votre démarche doit consister à utiliser depends.exe pour identifier les fonctions effectivement appelées.

####Analyse de la pile d'appels

Enregistrer l'allocation de mémoire nécessite de conserver les informations de la pile d'appels à ce moment-là. Je ne prévois pas de détailler comment obtenir les informations actuelles de la pile d'appels sous Windows. La fonction associée est `RtlCaptureStackBackTrace`, il existe de nombreuses ressources en ligne à ce sujet, vous pouvez également consulter la fonction dans mon code [`printTrace`](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)。

####Détection de fuites de mémoire

Jusqu'ici, nous avons maintenant rassemblé toutes les Dragon Balls, maintenant nous allons officiellement invoquer Shenron.

Je souhaite réaliser une détection de fuites de mémoire à un niveau local (ce qui est différent de VLD, qui effectue une détection globale et prend en charge le multithreading). Pour cela, j'ai encapsulé la classe de remplacement de fonction `RealDetector` avec une couche supplémentaire `LeakDetector`, et j'ai exposé l'interface de `LeakDetector` aux utilisateurs. Lors de son utilisation, il suffit de créer un `LeakDetector`, ce qui remplace la fonction et commence la détection des fuites de mémoire. Lors de la destruction de `LeakDetector`, la fonction d'origine est restaurée, la détection des fuites de mémoire est annulée, et les résultats de la détection des fuites de mémoire sont imprimés.

Testez avec le code ci-dessous :

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

Le code a alloué directement de la mémoire avec `new`, sans la libérer avant de sortir directement, ce qui a entraîné l'impression suivante du programme :

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

Le programme a correctement identifié que la mémoire demandée à deux endroits n'a pas été libérée et a imprimé des informations complètes sur la pile d'appels. La fonctionnalité dont nous avons besoin est désormais complétée.

###Conclusion

Lorsque vous ne comprenez pas encore les liens de programme, le chargement et les bibliothèques, vous pourriez être perdu quant à la façon de trouver les fonctions d'une bibliothèque partagée, sans parler de remplacer les fonctions de la bibliothèque par nos propres fonctions. Prenons l'exemple de la détection des fuites de mémoire pour explorer comment remplacer les fonctions d'un DLL Windows. Pour une mise en œuvre plus détaillée, vous pouvez consulter le code source de VLD.

Je tiens également à dire que "L'autoformation du programmeur : liaison, chargement et bibliothèques" est vraiment un bon livre, c'est juste un constat sans aucune intention publicitaire.

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT. Veuillez [**donner votre avis**](https://github.com/disenone/wiki_blog/issues/new)Veuillez indiquer toute omission. 
