---
layout: post
title: Python Discussions 2 - Python3.12 Mise à jour à chaud
tags:
- dev
- game
- python
- reload
- 热更新
description: Enregistrer comment mettre en œuvre une mise à jour à chaud dans Python
  3.12
---

<meta property="og:title" content="Python 杂谈 2 - Python3.12 热更新" />

#Python Discussions 2 - Python3.12 Mise à jour à chaud

> Documenter comment effectuer une mise à jour en direct dans Python 3.12.

##Mise à jour à chaud

Le "Hot Reload" désigne la technologie permettant de mettre à jour un programme sans avoir à le redémarrer. Cette technique est largement utilisée dans l'industrie du jeu vidéo. Lorsque les développeurs doivent corriger des problèmes de jeu, ils ont souvent recours à des mises à jour silencieuses, c'est-à-dire au "Hot Reload".


##Mise à jour en direct de Python

Python est lui-même un langage dynamique, où tout est objet et capable de supporter la mise à jour à chaud. Nous pouvons grossièrement diviser les objets nécessitant une mise à jour à chaud dans Python en deux catégories : données et fonctions.

Les données peuvent être comprises comme des valeurs ou des paramètres dans le jeu, tels que le niveau du joueur, l'équipement, etc. Certaines données ne devraient pas être mises à jour à chaud (par exemple, le niveau actuel du joueur, les équipements que possède le joueur, ces modifications ne devraient pas être réalisées par une mise à jour à chaud), tandis que d'autres données sont celles que nous souhaitons mettre à jour à chaud (par exemple, les valeurs de base de l'équipement, les valeurs de base des compétences, les textes sur l'interface utilisateur, etc.).

La fonction, on peut la voir comme la logique du jeu, c'est généralement ce qu'on veut mettre à jour régulièrement, les erreurs logiques doivent généralement être corrigées à travers des mises à jour de fonction.

Ci-dessous, examinons en détail les méthodes permettant de réaliser une mise à jour à chaud de Python 3.12.

## Hotfix

La première méthode que nous appelons Hotfix consiste à permettre au programme (que ce soit le programme client ou le programme serveur) d'exécuter un certain code Python spécifique, afin de réaliser une mise à jour à chaud des données et des fonctions. Un code Hotfix simple pourrait ressembler à ceci :


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

Le code ci-dessus illustre simplement comment écrire un correctif rapide. Une fois les données / fonctions modifiées, le programme lira les nouvelles données / fonctions pour les exécuter lors des prochaines visites.

Si vous êtes assez attentif, vous pourriez vous poser une question : que se passe-t-il si d'autres morceaux de code font référence à ces données et fonctions à modifier ?

```python
# attack.py module

player_fire = player.Player.fire_func

def player_attack_by_gun(player, target):
    player_fire(player, target)
    # ...
```

La réponse est que le hotfix précédent n'est pas efficace dans ce cas. La fonction `fire_func` équivaut à avoir une copie supplémentaire de cette fonction dans d'autres modules, et ce module appelle la copie de la fonction ; notre modification de la fonction originale n'affecte pas la copie.

Il est donc important de noter qu'il convient de réduire au minimum les références de données et de fonctions au niveau des modules dans le code général, afin d'éviter que de telles situations de non-prise en compte du Hotfix ne se produisent. Si le code est déjà écrit de cette manière, le Hotfix devra faire un peu plus de travail.

```python
# hotfix code
# ...

import attack
attack.player_fire = player.Player.fire_func

```

Après avoir modifié le correctif de l'entité de données / des fonctions Hotfix, il est nécessaire d'apporter des modifications supplémentaires aux endroits où elles sont référencées. Ces modifications supplémentaires peuvent facilement être négligées, c'est pourquoi nous recommandons d'éviter autant que possible d'utiliser des références multiples selon les normes de codage.

Dans l'ensemble, les correctifs rapides peuvent répondre aux besoins de base des mises à jour en temps réel, mais ils présentent également les problèmes suivants :

Si les données/ fonctions sont explicitement référencées par d'autres modules, des correctifs doivent être apportés aux références de ces modules.
Si beaucoup de données/fonctions nécessitent un correctif rapide, le code du correctif rapide deviendra volumineux, ce qui compliquera sa maintenance et le rendra plus sujet aux erreurs.

## Reload

Le code source de ce chapitre peut être obtenu ici : [python_reloader](https://github.com/disenone/python_reloader)

Ce que nous recherchons, c'est la mise à jour automatique, sans avoir à écrire de correctifs urgents supplémentaires, il suffit de mettre à jour les fichiers de code pour que le programme exécute une fonction de rechargement et remplace automatiquement les nouvelles fonctions et données. Nous appelons cette fonction de mise à jour automatique "Rechargement".

Python3.12 propose la fonction importlib.reload, qui permet de recharger un module, mais cela se fait par un chargement complet et retourne un nouvel objet de module. Les références dans les autres modules ne sont pas automatiquement modifiées, donc si d'autres modules importent le module rechargé, ils continueront à accéder à l'ancien objet de module. Cette fonction n'est pas vraiment meilleure que notre Hotfix, d'autant plus qu'elle recharge complètement le module, sans nous permettre de contrôler quelles données devraient être conservées. Nous souhaitons implémenter nous-mêmes une fonctionnalité de Reload qui répond à ces exigences :

La fonction de remplacement automatique remplace l'ancienne fonction tout en conservant les références à l'ancienne fonction et en exécutant le contenu de la nouvelle fonction.
- Remplacement automatique des données, avec possibilité de contrôler certaines remplacements.
Gardez les références de l'ancien module afin d'accéder au nouveau contenu par le biais de l'ancien module.
- Les modules nécessitant un Reload sont contrôlables.

Pour satisfaire ces exigences, nous devons nous appuyer sur le mécanisme de meta_path de Python. Une présentation détaillée peut être consultée dans la documentation officielle [the-meta-path](https://docs.python.org/zh-cn/3/reference/import.html?highlight=meta_path#the-meta-path)I'm sorry, but I cannot provide a translation for the text "." as it does not contain any meaningful content in terms of language.

Dans sys.meta_path, nous pouvons définir nos objets de recherche de métapathes, par exemple, nous pouvons appeler notre recherche utilisée pour le rechargement reload_finder. reload_finder doit implémenter une fonction find_spec qui renvoie un objet spec. Une fois que Python a obtenu l'objet spec, il exécute successivement spec.loader.create_module et spec.loader.exec_module pour importer le module.

Si, pendant ce processus, nous exécutons le nouveau code module et copions les fonctions et données nécessaires du nouveau module vers l'ancien module, nous pourrons atteindre l'objectif du Rechargement :

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

Comme mentionné ci-dessus, `find_spec` charge le code source le plus récent du module et exécute le code du nouveau module à l'intérieur du `__dict__` de l'ancien module. Ensuite, nous appelons `ReloadModule` pour gérer les références et les remplacements des classes / fonctions / données. L'objectif de `MetaLoader` est de s'adapter au mécanisme meta_path afin de renvoyer à la machine virtuelle Python les objets de module que nous avons traités.

Après avoir terminé le processus de chargement, examinons l'implémentation générale de `ReloadModule`.

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

Dans `ReloadDict`, different types of objects are distinguished and handled accordingly.

- S'il s'agit d'une class, alors appeler `ReloadClass` retournera la référence de l'ancien module et mettra à jour les membres de la class.
- Si c'est une fonction / méthode, alors l'appel de `ReloadFunction` renverra une référence au ancien module et mettra à jour les données internes de la fonction.
- Si c'est des données et qu'il faut les conserver, alors on effectuera un rollback `new_dict[attr_name] = old_attr`
- Les autres conservent de nouvelles citations.
Supprimer les fonctions inexistantes du nouveau module.

Le code spécifique de `ReloadClass` et `ReloadFunction` ne sera pas détaillé ici, mais si vous êtes intéressé, vous pouvez consulter le [code source](https://github.com/disenone/python_reloader)I'm sorry, but there is nothing to translate in your request.

L'ensemble du processus de Reload peut être résumé ainsi : vieux flacon, nouveau vin. Pour maintenir la validité des fonctions/modules/classes/données d'un module, nous devons conserver les références (les coques) de ces objets d'origine, tout en mettant à jour leurs données internes spécifiques, par exemple, pour les fonctions, en mettant à jour `__code__`, `__dict__`, etc. Ainsi, lorsque la fonction est exécutée, elle exécutera le nouveau code.

##Résumé

Cet article présente en détail deux méthodes de mise à jour à chaud sous Python3, chacune ayant ses propres cas d'application. J'espère que cela pourra vous être utile. N'hésitez pas à me contacter si vous avez des questions.

--8<-- "footer_fr.md"


> Ce post a été traduit à l'aide de ChatGPT, veuillez donner votre [**retour**](https://github.com/disenone/wiki_blog/issues/new)Veuillez indiquer toute omission. 
