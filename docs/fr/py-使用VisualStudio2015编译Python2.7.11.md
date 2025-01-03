---
layout: post
title: Utiliser Visual Studio 2015 pour compiler Python 2.7.11
categories:
- python
catalog: true
tags:
- dev
description: Python 2.7's official version supports compiling with versions of Visual
  Studio 2010 and below. If you want to tinker with Python on Windows, such as compiling
  a debug version or modifying the source code yourself, the easiest way is to install
  VS2010. However, personally, I would prefer to use VS2015 to compile Python, mainly
  because...
figures:
- https://img.shields.io/badge/python-2.7.11-brightgreen.svg
- https://img.shields.io/badge/vs-2015-68217A.svg
nowidth: 1
---

<meta property="og:title" content="使用 Visual Studio 2015 编译 Python 2.7.11" />

![](https://img.shields.io/badge/python-2.7.11-brightgreen.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##Raison

La version officielle de Python 2.7 prend en charge la compilation avec les versions antérieures à Visual Studio 2010. Veuillez consulter `PCbuild\readme.txt` pour plus d'informations.


	1.  Install Microsoft Visual Studio 2008, any edition.
	2.  Install Microsoft Visual Studio 2010, any edition, or Windows SDK 7.1 and any version of Microsoft Visual Studio newer than 2010.


Si vous souhaitez bricoler avec Python sous Windows, par exemple compiler une version de débogage, modifier le code source, etc., alors la méthode la plus simple est d'installer Visual Studio 2010.
Cependant, personnellement, je préfère compiler Python avec VS2015, principalement pour les raisons suivantes :


VS2010 est un peu dépassé, il est beaucoup moins performant et moins convivial que VS2015. J'utilise constamment VS2015 et je ne veux vraiment pas réinstaller VS2010.
En raison de l'utilisation constante de VS2015, vous l'utiliserez pour écrire certains de vos propres programmes. Si vous souhaitez intégrer Python, vous devrez alors utiliser la même version de Visual Studio pour compiler votre programme. L'utilisation de différentes versions de VS pourrait entraîner divers incidents imprévus. [Voici une explication plus détaillée](http://siomsystems.com/mixing-visual-studio-versions/)I am sorry, but the text you provided does not contain any content for me to translate. Could you please provide me with more text to work on? Thank you.

Donc j'ai décidé de commencer à utiliser VS2015 pour gérer la version 2.7.11 de Python (la dernière version de Python 2.7 à ce jour).

Il convient de noter que **Python 3.x prend désormais en charge la compilation avec VS2015**.

##Téléchargement du code source

La version de Python est bien sûr 2.7.11, il y a aussi quelques modules tiers. Vous pouvez exécuter le script `PCbuild\get_externals.bat` dans le répertoire source de Python pour obtenir tous les modules nécessaires à la compilation. Assurez-vous d'installer svn et d'ajouter svn.exe au PATH système.

Le téléchargement peut être très instable, et tout le processus peut être interrompu en raison de problèmes de réseau, il est donc recommandé de télécharger directement le répertoire externe sur mon github: [ma version Python](https://github.com/disenone/wpython-2.7.11/tree/e13f43a3b72ae2bdf4d2950c6364750ae668cbf4/externals)

##Processus de compilation

###module tiers

Il faut d'abord régler les modules tiers, principalement tcl, tk, tcltk.

Modifier le fichier `externals/tcl-8.5.15.0/win/makefile.vc`, changer la ligne 434 en

	- cdebug = -Zi -WX $(DEBUGFLAGS)
	+ cdebug = -Zi -WX- $(DEBUGFLAGS)

En ce qui concerne l'option `WX`, vous pouvez consulter la documentation officielle de Microsoft : [/WX (Traiter les avertissements du lien comme des erreurs)](https://msdn.microsoft.com/en-us/library/ms235592.aspx)

Veuillez modifier à nouveau le fichier `PCbuild/tk.vcxproj` en l'ouvrant avec un éditeur de texte, puis faites les modifications aux lignes 63 et 64.

	- <TkOpts>msvcrt</TkOpts>
	- <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt</TkOpts>
	+ <TkOpts>msvcrt,noxp</TkOpts>
	+ <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt,noxp</TkOpts>

Modifiez `PCbuild/tcltk.props` en ouvrant le fichier avec un éditeur de texte, puis modifiez la ligne 41.

	- <BuildDirTop>$(BuildDirTop)_VC9</BuildDirTop>
	+ <BuildDirTop>$(BuildDirTop)_VC13</BuildDirTop>

En raison de la suppression de la définition de `timezone` dans VS2015, qui a été remplacée par `_timezone`, tous les endroits où `timezone` est utilisé dans le code doivent être modifiés en `_timezone`. Les modules tiers n'ont qu'à modifier le fichier `externals/tcl-8.5.15.0/win/tclWinTime.c` en ajoutant ceci au début du fichier :

	#if defined _MSC_VER && _MSC_VER >= 1900
	#define timezone _timezone
	#endif

###Modifier le code source de Python.

Le problème lié au `timezone` se trouve également dans le module `time` de Python, veuillez le modifier à la ligne 767.

	- #ifdef __CYGWIN__
	+ #if defined(__CYGWIN__) || defined(_MSC_VER) && _MSC_VER >= 1900

De plus, comme Python utilise une méthode spéciale pour vérifier la validité des handles de fichiers sous Windows, cette méthode a été complètement interdite dans VS2015, ce qui entraîne des erreurs de compilation. Il est donc nécessaire de rectifier cela en modifiant les lignes 73 et 80 du fichier `Include/fileobject.h`.

	73 - #if defined _MSC_VER && _MSC_VER >= 1400
	73 + #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

	80 - #elif defined _MSC_VER && _MSC_VER >= 1200
	80 + #elif defined _MSC_VER && _MSC_VER >= 1200 && _MSC_VER < 1400

Fichier `Modules/posixmodule.c`, ligne 532 :

	- #if defined _MSC_VER && _MSC_VER >= 1400
	+ #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

À ce stade, Python devrait être compilé avec succès. Vous pouvez consulter les détails des modifications dans mes commits : [modifier pour compiler avec vs2015](https://github.com/disenone/wpython-2.7.11/commit/4037e2d806518dbf06ffb8ee5c46f419ef8d7edf)


###Vérifier la poignée invalide

Bien que la compilation ait réussi, la méthode brute d'ignorer les handles de fichiers invalides a conduit directement à des conséquences telles que si un handle invalide est accédé (par exemple, si un même fichier est fermé deux fois), Python échouera directement à l'assertion, le programme plantera, rendant Python inutilisable. Python a adopté une approche spéciale pour éviter cette situation, mais malheureusement, cela ne fonctionne pas dans VS2015, comme expliqué dans les commentaires :

	Microsoft CRT in VS2005 and higher will verify that a filehandle is valid and raise an assertion if it isn't.


Heureusement qu'une solution a déjà été trouvée, je l'ai vue dans les problèmes de Python, l'adresse est la suivante : [issue23524](http://psf.upfronthosting.co.za/roundup/tracker/issue23524), [issue25759](http://psf.upfronthosting.co.za/roundup/tracker/issue25759)Ce type de méthode est également utilisé dans l'actuel Python 3.x.


Plus précisément, il s'agit de désactiver le mécanisme de plantage assert de Windows lors de l'utilisation des descripteurs de fichiers, pour le remplacer par la vérification des codes d'erreur. Comment pouvez-vous désactiver le mécanisme assert de Windows ? La réponse consiste à utiliser votre propre fonction de gestion des erreurs pour remplacer la fonction de gestion par défaut de Windows. Le code clé est le suivant:


Créez le fichier `PC/invalid_parameter_handler.c`, définissez notre propre fonction de gestion des erreurs qui peut temporairement ignorer les erreurs survenues.

```c++
#ifdef _MSC_VER

#include <stdlib.h>

#if _MSC_VER >= 1900
/* pyconfig.h uses this function in the _Py_BEGIN_SUPPRESS_IPH/_Py_END_SUPPRESS_IPH
 * macros. It does not need to be defined when building using MSVC
 * earlier than 14.0 (_MSC_VER == 1900).
 */

static void __cdecl _silent_invalid_parameter_handler(
    wchar_t const* expression,
    wchar_t const* function,
    wchar_t const* file,
    unsigned int line,
	uintptr_t pReserved) 
{}

_invalid_parameter_handler _Py_silent_invalid_parameter_handler = _silent_invalid_parameter_handler;

#endif

#endif
```

Définir deux macros pour faciliter le remplacement temporaire des fonctions de gestion des erreurs, à noter qu'il s'agit d'un remplacement temporaire, il faudra ensuite revenir aux paramètres par défaut du système.

```c++
#if defined _MSC_VER && _MSC_VER >= 1900

extern _invalid_parameter_handler _Py_silent_invalid_parameter_handler;
#define _Py_BEGIN_SUPPRESS_IPH { _invalid_parameter_handler _Py_old_handler = \
    _set_thread_local_invalid_parameter_handler(_Py_silent_invalid_parameter_handler);
#define _Py_END_SUPPRESS_IPH _set_thread_local_invalid_parameter_handler(_Py_old_handler); }

#else

#define _Py_BEGIN_SUPPRESS_IPH
#define _Py_END_SUPPRESS_IPH

#endif /* _MSC_VER >= 1900 */
```

Après, là où il pourrait y avoir des erreurs de gestion de fichiers Windows, ajoutez les macros `_Py_BEGIN_SUPPRESS_IPH` et `_Py_END_SUPPRESS_IPH` avant et après, puis vérifiez le code d'erreur. Il y a plusieurs endroits à modifier, consultez les commits d'autres personnes pour apporter les modifications nécessaires.
[Here](https://github.com/kovidgoyal/cpython/commit/a9ec814d466d3c0139d10b69666f88eed10e4940)

##Terminer

À ce stade, Python 2.7.11 peut être compilé et exécuté correctement dans VS2015. Cependant, il est important de noter que cette configuration n'est pas recommandée par les autorités de Python.

	***WARNING***
	Building Python 2.7 for Windows using any toolchain that doesn't link
	against MSVCRT90.dll is *unsupported* as the resulting python.exe will
	not be able to use precompiled extension modules that do link against
	MSVCRT90.dll.

Il est donc préférable de faire attention lorsque vous l'utilisez.

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, s'il vous plaît laissez vos [**commentaires**](https://github.com/disenone/wiki_blog/issues/new)Indiquez tout manquement. 
