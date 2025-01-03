---
layout: post
title: Rédiger un détecteur de fuites de mémoire pour Windows
categories:
- c++
tags:
- dev
description: 'Traduisez ces textes en français:


  Récemment, j''ai terminé la lecture de "Programmation - Principes de base et pratiques"
  (abrégé en "Principes" par la suite). J''ai appris beaucoup de choses et je pense
  à faire quelques petits codes liés à cela. J''ai justement découvert qu''il existe
  un outil de détection de fuites de mémoire sur Windows [Visual Leak Detector](https://vld.codeplex.com/)，Ce
  outil est développé en remplaçant l''interface dll responsable de la gestion de
  la mémoire sous Windows pour suivre l''allocation et la libération de mémoire. Ainsi,
  j''ai décidé de m''inspirer du Visual Leak Detector (abrégé par VLD par la suite)
  pour créer un outil simple de détection de fuites de mémoire, en comprenant les
  liens dll.'
figures:
- assets/post_assets/2016-6-11-memory-leak-detector/depends.png
---

<meta property="og:title" content="编写 Windows 下的 Memory Leak Detector" />

![](https://img.shields.io/badge/windows-10-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##Préface

(https://vld.codeplex.com/)Ce outil fonctionne en remplaçant les interfaces dll responsables de la gestion de la mémoire sous Windows pour suivre l'allocation et la libération de mémoire. C'est pourquoi j'ai décidé de m'inspirer du Visual Leak Detector (abrégé par la suite en VLD) pour créer un outil de détection de fuites de mémoire simple, en comprenant les liens dll.

##Prérequis
Le livre "Linkage" explique en détail les principes de liaison des fichiers exécutables sous Linux et Windows, dont le format de fichier exécutable sous Windows est appelé PE (Portable Executable). Quant aux fichiers DLL, voici comment ils sont expliqués :

> DLL, ou Dynamic-Link Library en anglais, est l'équivalent des fichiers partagés sous Linux. Le système Windows utilise largement ce mécanisme de DLL, à tel point que même la structure du noyau de Windows dépend largement de ce mécanisme. Les fichiers DLL et EXE de Windows sont en réalité un concept similaire : ce sont des fichiers binaires au format PE. La seule différence notable est qu'un bit dans l'en-tête du fichier PE indique s'il s'agit d'un EXE ou d'un DLL, et que les fichiers DLL ne possèdent pas nécessairement l'extension .dll, pouvant également avoir d'autres comme .ocx (contrôles OCX) ou .CPL (programmes du Panneau de configuration).

Il y a aussi des fichiers d'extension comme les fichiers .pyd de Python. Quant au concept de détection de fuites de mémoire que nous abordons ici dans les DLL, il concerne les **tables d'exportation et d'importation de symboles**.

####Tableau d'exportation des caractères

> Lorsqu'un PE doit fournir des fonctions ou des variables à d'autres fichiers PE, nous appelons ce comportement **exportation de symboles (Symbol Exporting)**.

Pour simplifier, dans Windows PE, tous les symboles exportés sont regroupés dans une structure appelée **table d'exportation (Export Table)**, qui fournit une correspondance entre un nom de symbole et son adresse. Les symboles à exporter doivent être accompagnés du modificateur `__declspec(dllexport)`.

####Table d'importation des symboles

Le tableau d'importation de symboles est un concept clé ici, en opposition au tableau d'exportation de symboles. Commençons par examiner la définition du concept :

> Si nous utilisons des fonctions ou des variables provenant d'une DLL dans un programme, nous appelons ce processus **l'importation de symboles**.

Dans Windows PE, la structure qui contient les symboles des variables et des fonctions à importer, ainsi que des informations sur les modules où ils se trouvent, est appelée **table d'importation (Import Table)**. Lorsque Windows charge un fichier PE, l'une des tâches consiste à déterminer toutes les adresses des fonctions à importer, et à ajuster les éléments de la table d'importation à la bonne adresse. Ainsi, lors de l'exécution du programme, il est possible de localiser l'adresse réelle de la fonction en consultant la table d'importation, puis de l'appeler. La structure la plus importante de la table d'importation est l'**table des adresses d'importation (Import Address Table, IAT)**, qui contient les adresses réelles des fonctions importées.

Vous êtes-vous déjà rendu compte de comment nous allons réaliser la détection de fuites de mémoire ici :) ? En effet, nous allons pirater la table d'importation, plus précisément en remplaçant les adresses des fonctions d'allocation et de libération de mémoire des modules à tester par nos propres fonctions personnalisées. Ainsi, nous pourrons suivre chaque allocation et libération de mémoire du module et effectuer les vérifications nécessaires sans contraintes.

Pour plus d'informations détaillées sur les liens DLL, vous pouvez consulter "Linked" ou d'autres sources.

## Memory Leak Detector

Une fois le principe compris, il est temps de passer à la détection des fuites de mémoire en se basant sur ce principe. Les explications suivantes seront basées sur ma propre implémentation, que j'ai mise sur mon GitHub : [LeakDetector](https://github.com/disenone/LeakDetector)Translate these text into French language:

。

####Remplacement de la fonction.

Regardez d'abord la fonction clé, située dans [RealDetector.cpp](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)Veuillez me fournir le texte que vous souhaitez que je traduise en français.

```cpp linenums="1"
Remplacer une fonction spécifique de la table d'adresses d'importation (IAT) de importModule par une autre fonction,
importModule appellera une fonction d'un autre module, cette fonction est celle qui doit être patchée,
Ce que nous devons faire, c'est remplacer l'import du module par l'appel de notre fonction personnalisée.
 *
- importModule (IN) : Le module à traiter, ce module appelle des fonctions d'autres modules qui nécessitent un patch.
 *
- exportModuleName (IN): Nom du module source des fonctions nécessitant un correctif
 *
- exportModulePath (IN): chemin où se trouve le module d'export, d'abord essayé de charger le module d'export en utilisant le chemin.
Si l'échec se produit, charger avec le nom.
- importName (IN): Nom de la fonction
 *
- replacement (IN): pointeur de fonction de remplacement
 *
Retourne la valeur : true si réussi, sinon false
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

Analysons cette fonction comme dit dans le commentaire, elle a pour but de remplacer l'adresse d'une fonction à l'intérieur de l'IAT par l'adresse d'une autre fonction. Regardons les lignes 34 à 35 :

``` cpp
idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
	TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
```

La fonction `ImageDirectoryEntryToDataEx` peut renvoyer l'adresse d'une certaine structure de l'en-tête du fichier du module. L'entrée `IMAGE_DIRECTORY_ENTRY_IMPORT` spécifie la structure de la table d'importation, donc le `idte` renvoyé pointe vers la table d'importation du module.

Les lignes 36 à 40 vérifient si "idte" est valide. À la ligne 41, "idte->FirstThunk" pointe vers l'IAT réel. Ainsi, les lignes 41 à 48 recherchent le module contenant les fonctions à remplacer en fonction du nom du module. Si aucun n'est trouvé, cela signifie qu'aucune fonction du module n'a été appelée. Une erreur est alors signalée et le programme retourne.

Une fois le module trouvé, naturellement, nous devons localiser la fonction à remplacer, ouvrir le module auquel la fonction appartient aux lignes 55 à 62, et trouver l'adresse de la fonction à la ligne 64. Comme l'IAT ne conserve pas les noms, il est nécessaire de localiser tout d'abord la fonction en fonction de son adresse d'origine, puis de modifier cette adresse de fonction, éléments abordés aux lignes 68 à 80. Après avoir réussi à trouver la fonction, il suffit simplement de modifier l'adresse en remplaçant par celle de `replacement`.

À ce stade, nous avons réussi à remplacer les fonctions dans l'IAT.

####Noms de modules et de fonctions

Bien que nous ayons réussi à remplacer la fonction IAT `patchImport`, cette fonction nécessite de spécifier le nom du module et de la fonction. Comment saurons-nous alors quels modules et fonctions sont utilisés pour l'allocation et la libération de mémoire dans le programme ? Pour résoudre ce problème, nous aurons besoin de l'outil Windows [Dependency Walker](http://www.dependencywalker.com/)Créez un nouveau projet dans Visual Studio, utilisez `new` pour allouer de la mémoire dans la fonction `main`, compilez en mode Debug, puis utilisez `depends.exe` pour ouvrir le fichier exe compilé, vous verrez une interface similaire à celle-ci (en utilisant mon projet [LeakDetectorTest](https://github.com/disenone/LeakDetector/tree/master/LeakDetectorTest)Pour exemple :

![](assets/img/2016-6-11-memory-leak-detector/depends.png)

Il est possible de constater que LeakDetectorTest.exe utilise les fonctions `malloc` et `_free_dbg` provenant de uscrtbased.dll (non affichées dans l'image), ces deux fonctions sont celles que nous devons remplacer. Il convient de noter que les noms réels des fonctions de module peuvent varier en fonction de votre version de Windows et de Visual Studio. Les miennes sont Windows 10 et Visual Studio 2015. Ce que vous devez faire est d'utiliser depends.exe pour identifier quelles fonctions sont effectivement appelées.

####Analyser la pile d'appels

Enregistrer l'allocation de mémoire nécessite de conserver les informations de la pile d'appels à ce moment-là. Je ne prévois pas de détailler comment obtenir les informations actuelles de la pile d'appels sous Windows, la fonction associée est `RtlCaptureStackBackTrace`. Il existe de nombreux documents en ligne sur le sujet, vous pouvez également consulter la fonction [`printTrace`](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)。

####Vérifier les fuites de mémoire

Jusqu'à présent, nous avons rassemblé toutes les Dragon Balls, maintenant nous allons officiellement invoquer Shenron.

Je souhaite mettre en place une détection de fuites de mémoire locale (c'est différent de VLD, qui effectue une détection globale et prend en charge le multithreading). Pour cela, j'ai enveloppé la classe `RealDetector`, qui remplace effectivement les fonctions, dans une couche supplémentaire appelée `LeakDetector`, et je rends l'interface de `LeakDetector` accessible aux utilisateurs. Il suffit de créer un `LeakDetector` pour remplacer les fonctions et commencer la détection de fuites de mémoire. Lorsque `LeakDetector` est détruit, les fonctions d'origine sont restaurées, la détection de fuites de mémoire est interrompue et les résultats de la détection de fuites de mémoire sont imprimés.

Veuillez tester le code ci-dessous :

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

Le code a alloué de la mémoire avec `new`, mais n'a pas libéré la mémoire avant de quitter, voici le résultat affiché par le programme :

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

Le programme a correctement identifié deux endroits où la mémoire a été allouée mais pas libérée, et a affiché l'intégralité des informations de la pile d'appels. La fonctionnalité que nous recherchions est maintenant entièrement implémentée.

###Concluding Remarks

Lorsque vous ne maîtrisez pas encore les concepts de liaison, de chargement et de bibliothèque en programmation, il est possible que vous ayez du mal à trouver comment accéder aux fonctions des bibliothèques partagées, sans même parler de la substitution des fonctions des bibliothèques par nos propres fonctions. En prenant comme exemple la détection de fuites de mémoire, nous allons discuter comment remplacer les fonctions des DLL Windows. Pour une mise en œuvre plus détaillée, vous pouvez vous référer au code source de VLD.

Another thing I'd like to mention is that "The Self-Cultivation of Programmers: Linking, Loading, and Libraries" is actually a pretty good book, just my honest thoughts, not a soft promotion.

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez [**反馈**](https://github.com/disenone/wiki_blog/issues/new)Indiquez tout oubli. 
