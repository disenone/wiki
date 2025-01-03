---
layout: post
title: Python Discussions 2 - Mise à jour en direct de Python 3.12
tags:
- dev
- game
- python
- reload
- 热更新
description: Enregistrer comment réaliser une mise à jour à chaud dans Python 3.12
---

<meta property="og:title" content="Python 杂谈 2 - Python3.12 热更新" />

#Python Discussion 2 - Python 3.12 Hotfix

> Enregistrer comment implémenter une mise à jour en direct dans Python 3.12.

##Mise à jour en direct.

Le "Hot Reload" est une technologie qui permet de mettre à jour un programme sans avoir besoin de le redémarrer. Cette technique est largement utilisée dans l'industrie du jeu vidéo. Lorsque les développeurs corrigent des problèmes de jeu, ils utilisent souvent des mises à jour silencieuses, appelées "Hot Reload", afin de ne pas perturber les joueurs.


##Mise à jour dynamique des modules Python

Python is dynamically typed, everything is an object, and it's capable of hot updates. We can roughly divide the objects that need to be hot updated in Python into two types: data and functions.

Les données peuvent être comprises comme des valeurs ou des paramètres dans un jeu, comme le niveau du joueur, l'équipement, etc. Certaines données ne devraient pas être mises à jour dynamiquement (comme le niveau actuel du joueur, l'équipement qu'il possède), tandis que d'autres sont destinées à être mises à jour dynamiquement (comme les paramètres de base de l'équipement, les paramètres de base des compétences, le texte sur l'interface utilisateur, etc.).

Les fonctions peuvent être comprises comme la logique du jeu, c'est essentiellement ce que nous voulons mettre à jour fréquemment, les erreurs logiques doivent généralement être corrigées en mettant à jour les fonctions.

Ci-dessous, examinons en détail les méthodes pour mettre à jour Python 3.12 en temps réel.

## Hotfix

Nous appelons le premier méthode "Hotfix", qui consiste à exécuter un code Python spécifique (que ce soit le programme client ou serveur), pour mettre à jour les données et les fonctions en temps réel. Un exemple simple de code Hotfix pourrait être le suivant :


```python
# hotfix code

# hotfix data
import weapon_data
weapon_data.gun.damage = 100

# hotfix func
import player
def new_fire_func(self, target):
    target.health -= weapon_data.gun.damage
    # ...
player.Player.fire_func = new_fire_func
```

Le code ci-dessus montre simplement comment écrire un correctif rapide. Une fois que les données / fonctions ont été modifiées, le programme lira les nouvelles données / fonctions lors des visites ultérieures pour les exécuter.

Si tu es attentif, tu pourrais te demander : que se passe-t-il si d'autres parties du code font référence à ces données et fonctions à modifier ?

```python
# attack.py module

player_fire = player.Player.fire_func

def player_attack_by_gun(player, target):
    player_fire(player, target)
    # ...
```

La réponse est que le correctif rapide précédent ne s'applique pas à cette situation, la fonction `fire_func` agit comme une copie supplémentaire dans un autre module, et l'appel de cette fonction dans ce module se fait sur une copie. Ainsi, les modifications apportées au corps de la fonction ne sont pas répercutées sur la copie.

Il est donc essentiel de veiller à réduire autant que possible les références de données et de fonctions au niveau du module dans le code général, afin d'éviter les cas où ce genre de correctif d'urgence ne fonctionne pas. Si le code est déjà rédigé de cette manière, il faudra fournir des efforts supplémentaires lors de l'application de ce correctif.

```python
# hotfix code
# ...

import attack
attack.player_fire = player.Player.fire_func

```

Après avoir apporté des correctifs au niveau des données / fonctions principales, veillez à modifier également les références supplémentaires. Ces modifications supplémentaires sont souvent négligées, c'est pourquoi il est préférable de suivre les normes de codage pour éviter autant que possible les écritures avec plusieurs références.

Dans l'ensemble, les correctifs rapides peuvent répondre aux besoins essentiels des mises à jour fréquentes, mais présentent également les problèmes suivants :

Si les données / fonctions sont explicitement référencées par d'autres modules, des correctifs chauds supplémentaires doivent être appliqués à ces modules.
Si un grand nombre de données/fonctions nécessitent des correctifs urgents, le code des correctifs deviendra très volumineux, ce qui rendra la maintenance plus difficile et augmentera les risques d'erreurs.

## Reload

Ce chapitre est disponible en source à partir d'ici : [python_reloader](https://github.com/disenone/python_reloader)

Ce que nous préférons vraiment, c'est la mise à jour automatique en temps réel, sans avoir à écrire de correctifs d'urgence supplémentaires. Il suffit de mettre à jour les fichiers de code, d'exécuter une fonction de rechargement pour remplacer automatiquement les nouvelles fonctions et les nouvelles données. Nous appelons cette fonctionnalité de mise à jour automatique en temps réel "Rechargement".

Python3.12 introduces the importlib.reload function, which allows for module reloading, but it is a full reload and returns a new module object. However, references in other modules are not automatically updated. This means that if other modules import the reloaded module, they will still access the old module object. This feature doesn't offer much advantage over our Hotfix, especially since it's a full reload of the module and we cannot control which data should be preserved. We want to implement our own Reload function to meet these requirements:

Remplacement automatique de la fonction, les références à l'ancienne fonction restent valides et exécutent le contenu de la nouvelle fonction.
Remplacement automatique des données, permettant également un remplacement partiel contrôlable.
Conserver les références aux anciens modules pour accéder au nouveau contenu à travers ces anciens modules.
Les modules nécessitant un rechargement doivent être contrôlables.

(https://docs.python.org/zh-cn/3/reference/import.html?highlight=meta_path#the-meta-path)Translate these text into French language:

。

La variable sys.meta_path permet de définir notre propre objet de recherche de chemin d'accès, par exemple, si nous appelons notre objet de recherche utilisé pour le rechargement "reload_finder", ce dernier doit mettre en œuvre une fonction "find_spec" et renvoyer un objet "spec". Une fois que Python obtient l'objet "spec", il exécute successivement "spec.loader.create_module" et "spec.loader.exec_module" pour terminer l'importation du module.

Si nous exécutons de nouveaux codes de module dans ce processus et copions les fonctions et les données nécessaires du nouveau module dans l'ancien module, nous pouvons atteindre l'objectif de rechargement :

```python linenums="1"
class MetaFinder:
    def __init__(self, reloader):
        self._reloader = reloader

    def find_spec(self, fullname, path, target=None):
        # find source file
        finder = importlib.machinery.PathFinder()
        spec = finder.find_spec(fullname, path)
        if not spec:
            return

        old_module = self._reloader.GetOldModule(fullname)
        if old_module:
            # run new code in old module dict
            code = spec.loader.get_code(fullname)
            exec(code, old_module.__dict__)
            module = old_module
        else:
            # if old module not exists, just create a new one
            module = import_util.module_from_spec(spec)
            spec.loader.exec_module(module)

        try:
            self._reloader.ReloadModule(module)
        except:
            sys.excepthook(*sys.exc_info())

        return import_util.spec_from_loader(fullname, MetaLoader(module))


class MetaLoader:
    def __init__(self, module):
        self._module = module

    def create_module(self, spec):
        return self._module

    def exec_module(self, module):
        # restore __spec__
        module.__spec__ = module.__dict__.pop('__backup_spec__')
        module.__loader__ = module.__dict__.pop('__backup_loader__')
```

Comme indiqué précédemment, `find_spec` charge le code source le plus récent du module, exécute ce code dans le `__dict__` de l'ancien module, puis nous utilisons `ReloadModule` pour gérer les références et les remplacements de classes / fonctions / données. L'objectif de `MetaLoader` est d'adapter le mécanisme de meta_path en renvoyant à la machine virtuelle Python les objets de module que nous avons traités.

Une fois le processus de chargement terminé, examinons maintenant l'implémentation générale de `ReloadModule`.

```python linenums="1"
# ...
def ReloadModule(self, module):
    old_module_info = self._old_module_infos.get(module.__name__)
    if not old_module_info:
        return

    self.ReloadDict(module, old_module_info, module.__dict__)

def ReloadDict(self, module, old_dict, new_dict, _reload_all_data=False, _del_func=False):
    dels = []

    for attr_name, old_attr in old_dict.items():

        if attr_name in self.IGNORE_ATTRS:
            continue

        if attr_name not in new_dict:
            if _del_func and (inspect.isfunction(old_attr) or inspect.ismethod(old_attr)):
                dels.append(attr_name)
            continue

        new_attr = new_dict[attr_name]

        if inspect.isclass(old_attr):
            new_dict[attr_name] = self.ReloadClass(module, old_attr, new_attr)

        elif inspect.isfunction(old_attr):
            new_dict[attr_name] = self.ReloadFunction(module, old_attr, new_attr)

        elif inspect.ismethod(old_attr) or isinstance(old_attr, classmethod) or isinstance(old_attr, staticmethod):
            self.ReloadFunction(module, old_attr.__func__, new_attr.__func__)
            new_dict[attr_name] = old_attr

        elif inspect.isbuiltin(old_attr) \
                or inspect.ismodule(old_attr) \
                or inspect.ismethoddescriptor(old_attr) \
                or isinstance(old_attr, property):
            # keep new
            pass

        elif not _reload_all_data and not self.NeedUpdateData(module, new_dict, attr_name):
            # keep old data
            new_dict[attr_name] = old_attr

    if dels:
        for name in dels:
            old_dict.pop(name)
# ...

```

La classe `ReloadDict` différenciera et traitera les objets de types différents.

Si c'est une classe, appelez `ReloadClass`, elle renverra la référence de l'ancien module et mettra à jour les membres de la classe.
Si c'est une fonction/méthode, appeler `ReloadFunction` renverra la référence du module précédent et mettra à jour les données internes de la fonction.
Si c'est un ensemble de données et qu'il doit être conservé, alors il reviendra en arrière : `new_dict[attr_name] = old_attr`
Maintenez les autres citations en cours comme nouvelles.
Remove functions that do not exist in the new module.

Les codes spécifiques de `ReloadClass` et `ReloadFunction` ne seront pas détaillés ici. Si vous êtes intéressé, vous pouvez consulter directement le [code source](https://github.com/disenone/python_reloader)。

Le processus complet de rechargement peut être résumé ainsi : donner un coup de jeune à une vieille histoire. Pour maintenir la validité des modules/fonctions/classes de modules/données de modules, il est nécessaire de conserver les références des objets originaux (leur enveloppe), et ensuite de mettre à jour spécifiquement leurs données internes. Par exemple, pour les fonctions, on met à jour  `__code__`, `__dict__`,` et autres données. Lors de l'exécution de la fonction, elle passera à l'exécution du nouveau code.

##Résumé

Ce texte présente en détail les deux méthodes de mise à jour à chaud de Python3, chacune ayant ses propres cas d'utilisation. J'espère que cela vous sera utile. N'hésitez pas à poser des questions ou à échanger à tout moment.

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez en [**反馈**](https://github.com/disenone/wiki_blog/issues/new)Identifier toute omission. 
