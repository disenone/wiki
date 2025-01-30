---
layout: post
title: Utiliser Visual Studio 2015 pour compiler Python 2.7.11
categories:
- python
catalog: true
tags:
- dev
description: La version officielle de Python 2.7 prend en charge les versions inférieures
  à Visual Studio 2010 pour la compilation. Si vous souhaitez manipuler Python sous
  Windows, par exemple, compiler une version Debug ou modifier le code source, la
  manière la plus simple est d'installer VS2010. Cependant, personnellement, je préfère
  utiliser VS2015 pour compiler Python, principalement pour les raisons suivantes...
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


Si vous voulez bricoler avec Python sous Windows, par exemple compiler une version Debug ou modifier le code source vous-même, le moyen le plus simple est d'installer Visual Studio 2010.
Cependant, personnellement, je préfère compiler Python avec VS2015, principalement pour les raisons suivantes :


- VS2010 est vraiment un peu obsolète, ses fonctionnalités et son expérience d'utilisation sont bien inférieures à celles de VS2015. Utilisant déjà VS2015, je ne suis vraiment pas enclin à réinstaller VS2010.
(http://siomsystems.com/mixing-visual-studio-versions/)I'm afraid I cannot provide a translation as the text you provided appears to be empty or not recognizable.

Donc, j'ai commencé à travailler avec VS2015 pour installer la version Python 2.7.11 (la dernière version actuelle de Python 2.7).

Il faut noter que **Python 3.x est désormais compatible avec la compilation en utilisant VS2015**.

##Téléchargement du code source

La version de Python est bien sûr la 2.7.11, et il y a aussi certains modules tiers. Vous pouvez exécuter le script `PCbuild\get_externals.bat` dans le répertoire source de Python pour obtenir tous les modules de compilation nécessaires. Assurez-vous d'avoir installé svn et ajouté svn.exe au chemin d'accès système.

Le téléchargement peut être instable et le processus entier risque d'être interrompu en raison de problèmes de réseau, il est donc recommandé de télécharger directement le répertoire externe sur mon GitHub : [ma version Python](https://github.com/disenone/wpython-2.7.11/tree/e13f43a3b72ae2bdf4d2950c6364750ae668cbf4/externals)

##Processus de compilation

###Module tiers

Tout d'abord, il faut résoudre les modules tiers, principalement tcl, tk, tcltk.

Veuillez modifier le fichier `externals/tcl-8.5.15.0/win/makefile.vc` en remplaçant la ligne 434 par

	- cdebug = -Zi -WX $(DEBUGFLAGS)
	+ cdebug = -Zi -WX- $(DEBUGFLAGS)

Concernant l'option `WX`, vous pouvez consulter la documentation officielle de Microsoft : [/WX (Traiter les avertissements du compilateur comme des erreurs)](https://msdn.microsoft.com/en-us/library/ms235592.aspx)

Veuillez modifier à nouveau le fichier `PCbuild/tk.vcxproj` en l'ouvrant avec un éditeur de texte et en modifiant les lignes 63 et 64.

	- <TkOpts>msvcrt</TkOpts>
	- <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt</TkOpts>
	+ <TkOpts>msvcrt,noxp</TkOpts>
	+ <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt,noxp</TkOpts>

Modifiez `PCbuild/tcltk.props` en l'ouvrant avec un éditeur de texte, puis modifiez la ligne 41.

	- <BuildDirTop>$(BuildDirTop)_VC9</BuildDirTop>
	+ <BuildDirTop>$(BuildDirTop)_VC13</BuildDirTop>

En raison de l'annulation de la définition de `timezone` dans VS2015, qui a été remplacée par `_timezone`, tous les endroits où `timezone` est utilisé dans le code doivent être modifiés en `_timezone`. Les modules tiers n'ont qu'à modifier le fichier `externals/tcl-8.5.15.0/win/tclWinTime.c` et ajouter ceci au début du fichier :

	#if defined _MSC_VER && _MSC_VER >= 1900
	#define timezone _timezone
	#endif

###Modifier le code source Python

Le problème de `timezone` se trouve également dans le module `time` de Python, modifiez la ligne 767.

	- #ifdef __CYGWIN__
	+ #if defined(__CYGWIN__) || defined(_MSC_VER) && _MSC_VER >= 1900

De plus, en raison d'une méthode particulière utilisée par Python sur Windows pour vérifier la validité des descripteurs de fichiers, et comme cette méthode est complètement interdite dans VS2015, cela entraînera des erreurs de compilation, il est donc nécessaire de la modifier. Fichier `Include/fileobject.h`, lignes 73 et 80 :

	73 - #if defined _MSC_VER && _MSC_VER >= 1400
	73 + #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

	80 - #elif defined _MSC_VER && _MSC_VER >= 1200
	80 + #elif defined _MSC_VER && _MSC_VER >= 1200 && _MSC_VER < 1400

Fichier `Modules/posixmodule.c`, ligne 532 :

	- #if defined _MSC_VER && _MSC_VER >= 1400
	+ #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

À ce stade, Python peut être compilé avec succès. Pour des modifications plus précises, vous pouvez consulter le contenu de mes commits : [modifier pour construire avec vs2015](https://github.com/disenone/wpython-2.7.11/commit/4037e2d806518dbf06ffb8ee5c46f419ef8d7edf)


###Vérifier la poignée invalide

Bien que la compilation ait réussi, l'approche brutale d'ignorer les handles de fichiers invalides a conduit directement à des conséquences graves. Dès qu'un handle invalide est accédé (par exemple, en fermant deux fois le même fichier), Python échoue directement avec une assertion et le programme plante. Ce genre de Python est tout simplement inutilisable. Python a recours à une méthode particulière pour éviter ce genre de situation, malheureusement, cela ne fonctionne pas dans VS2015. L'explication donnée dans les commentaires est la suivante :

	Microsoft CRT in VS2005 and higher will verify that a filehandle is valid and raise an assertion if it isn't.


Heureusement, il existe déjà une solution. Je l'ai vue dans un problème Python, l'adresse est ici : [issue23524](http://psf.upfronthosting.co.za/roundup/tracker/issue23524), [issue25759](http://psf.upfronthosting.co.za/roundup/tracker/issue25759)Cette méthode est également utilisée dans la version actuelle de Python 3.x.


Plus précisément, il s'agit de désactiver le mécanisme de crash assert de Windows lors de l'utilisation des handles de fichiers, pour le remplacer par la vérification des codes d'erreur. Comment désactiver le mécanisme assert de Windows ? La réponse est d'utiliser sa propre fonction de gestion des erreurs pour remplacer la fonction par défaut de Windows. Le code clé :


Créez le fichier `PC/invalid_parameter_handler.c`, définissez notre propre fonction de gestion des erreurs, vous pouvez temporairement ignorer les erreurs survenues.

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

Définissez deux macros pour faciliter le remplacement temporaire des fonctions de gestion des erreurs, en veillant à revenir ensuite aux paramètres par défaut du système.

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

Après cela, placez respectivement la macro `_Py_BEGIN_SUPPRESS_IPH` et `_Py_END_SUPPRESS_IPH` avant et après les emplacements susceptibles de déclencher une erreur de gestion des fichiers Windows. Ensuite, il suffit de vérifier le code d'erreur. Il y a plusieurs endroits à modifier, référez-vous aux commits d'autres personnes pour effectuer les modifications nécessaires :
[ici](https://github.com/kovidgoyal/cpython/commit/a9ec814d466d3c0139d10b69666f88eed10e4940)

##Fin

À ce stade, Python 2.7.11 peut être compilé et exécuté normalement dans VS2015, mais en raison du fait que l'équipe Python ne recommande pas de configurer ainsi.

	***WARNING***
	Building Python 2.7 for Windows using any toolchain that doesn't link
	against MSVCRT90.dll is *unsupported* as the resulting python.exe will
	not be able to use precompiled extension modules that do link against
	MSVCRT90.dll.

Il est donc préférable de faire attention lors de son utilisation.

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez fournir votre [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Identifier toute omission possible. 
