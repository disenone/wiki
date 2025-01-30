---
layout: post
title: Python Plauderei 2 - Python3.12 Hot Update
tags:
- dev
- game
- python
- reload
- 热更新
description: Dokumentation zur Implementierung von Hot-Reload in Python 3.12
---

<meta property="og:title" content="Python 杂谈 2 - Python3.12 热更新" />

#Python Talk 2 - Python 3.12 Hotfix

> Dokumentiere, wie man Live-Updates in Python 3.12 implementiert.

##Heißes Update

Hot Reload kann als eine Technik verstanden werden, mit der Programme aktualisiert werden, ohne sie neu starten zu müssen. Diese Technik findet breite Anwendung in der Spieleindustrie, wenn Entwickler Probleme im Spiel beheben. Um die Spieler nicht zu beeinträchtigen, müssen sie oft eine Art von stillen Updates anwenden, das heißt Hot Reload.


##Python Live Update

Python selbst ist eine dynamische Sprache, alles ist ein Objekt und sie hat die Fähigkeit zur heißen Aktualisierung. Wir können grob die Objekte, die in Python aktualisiert werden müssen, in zwei Arten unterteilen: Daten und Funktionen.

Daten können als die Werte oder Einstellungen im Spiel verstanden werden, wie z.B. der Level, die Ausrüstung eines Spielers usw. Einige Daten sollten nicht live aktualisiert werden (z.B. der aktuelle Level eines Spielers, welche Ausrüstung der Spieler hat, diese Daten sollten nicht durch ein Live-Update geändert werden), während es andere Daten gibt, die wir gerne live aktualisieren möchten (z.B. die grundlegenden Werte der Ausrüstung, die grundlegenden Werte der Fähigkeiten, Texte auf der Benutzeroberfläche usw.).

Funktionen, die als Spiel-Logik verstanden werden können, sind im Grunde das, was wir heiß aktualisieren möchten. Logikfehler müssen meistens durch Hot-Update-Funktionen behoben werden.

Lassen Sie uns im Folgenden genauer betrachten, welche Methoden für die Durchführung von heißen Updates in Python 3.12 zur Verfügung stehen.

## Hotfix

Die erste Methode nennen wir Hotfix, bei der das Programm (sowohl die Client- als auch die Serveranwendung) einen bestimmten Python-Code ausführt, um eine heiße Aktualisierung von Daten und Funktionen zu ermöglichen. Ein einfacher Hotfix-Code könnte folgendermaßen aussehen:


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

Der obige Code zeigt einfach, wie ein Hotfix geschrieben wird. Nach der Änderung von Daten / Funktionen liest das Programm bei zukünftigen Zugriffen die neuen Daten / Funktionen und führt sie aus.

If you are meticulous, you may have a question: What happens if other code references these data and functions that need to be modified?

```python
# attack.py module

player_fire = player.Player.fire_func

def player_attack_by_gun(player, target):
    player_fire(player, target)
    # ...
```

Die Antwort ist, dass der vorherige Hotfix in dieser Situation nicht wirksam ist. Die Funktion `fire_func` fungiert als eine Kopie in anderen Modulen. Die Aufrufe in diesem Modul beziehen sich auf die Kopie der Funktion, sodass Änderungen am Original nicht wirksam sind.

Es ist daher wichtig, darauf zu achten, dass in allgemeinem Code die Datenreferenzen und Funktionsreferenzen auf Modulebene möglichst reduziert werden, um Situationen zu vermeiden, in denen Hotfixes nicht wirksam werden. Wenn der Code bereits so geschrieben ist, erfordert der Hotfix zusätzliche Anstrengungen.

```python
# hotfix code
# ...

import attack
attack.player_fire = player.Player.fire_func

```

Nach der Hotfix-Änderung des Daten-/Funktionskörpers sollten zusätzlich die Stellen, an denen diese referenziert werden, geändert werden. Diese zusätzlichen Änderungen können leicht übersehen werden, daher empfehlen wir, aus Gründen der Code-Normierung zu versuchen, Mehrfachreferenzen soweit wie möglich zu vermeiden.

In summary, Hotfixes can meet the basic requirements of live updates, but there are the following issues:

Wenn Daten/Funktionen von anderen Modulen explizit referenziert werden, ist ein zusätzliches Hotfix für diese Module erforderlich.
- Wenn eine große Menge an Daten/Funktionen einen Hotfix benötigt, wird der Hotfix-Code umfangreich, die Wartung wird schwieriger und die Fehleranfälligkeit steigt.

## Reload

Der Quellcode dieses Kapitels ist hier erhältlich: [python_reloader](https://github.com/disenone/python_reloader)

Was wir uns mehr wünschen, ist ein automatisches Hot-Reload, das keine zusätzlichen Hotfixes erfordert. Es genügt, die Code-Dateien zu aktualisieren und eine Reload-Funktion auszuführen, um automatisch die neuen Funktionen und Daten zu ersetzen. Diese Funktion des automatischen Hot-Reloads nennen wir Reload.

Python 3.12 bietet die Funktion importlib.reload, mit der Module neu geladen werden können. Es handelt sich jedoch um ein vollständiges Neuladen, das ein neues Modulobjekt zurückgibt. Dies bedeutet, dass Verweise in anderen Modulen nicht automatisch aktualisiert werden. Wenn also ein anderes Modul das neu geladene Modul importiert hat, wird immer noch auf das alte Modulobjekt zugegriffen. Diese Funktion ist kaum besser als unser Hotfix, vor allem da sie Module komplett neu lädt und wir nicht kontrollieren können, welche Daten erhalten bleiben. Wir möchten eine Reload-Funktion implementieren, die diesen Anforderungen gerecht wird:

- Automatische Ersetzungsfunktion, während die Referenzen auf die alte Funktion weiterhin gültig sind und den Inhalt der neuen Funktion ausführen.
- Automatischer Datenaustausch mit der Möglichkeit, Teile zu ersetzen
- Behalten Sie die Referenz zum alten Modul bei, über das alte Modul können Sie auf die neuen Inhalte zugreifen.
- Die zu ladenden Module sind steuerbar.

Um diese Anforderungen zu erfüllen, müssen wir die Mechanismen von meta_path in Python nutzen. Eine ausführliche Einführung finden Sie in der offiziellen Dokumentation [the-meta-path](https://docs.python.org/zh-cn/3/reference/import.html?highlight=meta_path#the-meta-path)。

Die sys.meta_path ermöglicht die Definition unseres Meta-Pfadsuchers, zum Beispiel können wir den Sucher, der für das Neuladen verwendet wird, als reload_finder bezeichnen. Der reload_finder muss eine Funktion find_spec implementieren und ein spec-Objekt zurückgeben. Wenn Python das spec-Objekt erhält, werden spec.loader.create_module und spec.loader.exec_module nacheinander ausgeführt, um den Import des Moduls abzuschließen.

Wenn wir in diesem Prozess neuen Modulkode ausführen und die Funktionen sowie die benötigten Daten aus dem neuen Modul in das alte Modul kopieren, können wir das Ziel Reload erreichen:

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

Wie oben beschrieben, lädt `find_spec` den neuesten Quellcode des Moduls und führt den Code des neuen Moduls im `__dict__` des alten Moduls aus. Danach rufen wir `ReloadModule` auf, um die Referenzen und Ersetzungen von Klassen / Funktionen / Daten zu verarbeiten. Das Ziel von `MetaLoader` ist es, den meta_path-Mechanismus anzupassen und der Python-virtuellen Maschine das von uns bearbeitete Modulobjekt zurückzugeben.

Nachdem der Ladevorgang abgeschlossen ist, werfen wir einen Blick auf die grobe Implementierung von `ReloadModule`.

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

In `ReloadDict` wird zwischen verschiedenen Arten von Objekten unterschieden.

- Wenn es sich um eine Klasse handelt, wird `ReloadClass` aufgerufen, das eine Referenz auf das alte Modul zurückgibt und die Mitglieder der Klasse aktualisiert.
Wenn es sich um eine Funktion / Methode handelt, wird durch den Aufruf von `ReloadFunction` die Referenz auf das alte Modul zurückgegeben und die internen Daten der Funktion aktualisiert.
Wenn es sich um Daten handelt und sie beibehalten werden müssen, wird `new_dict[attr_name] = old_attr` rückgängig gemacht.
- Die übrigen bleiben im neuen Zitat.
Entfernen von Funktionen, die in neuen Modulen nicht existieren.

Die spezifischen Codes für `ReloadClass` und `ReloadFunction` werden hier nicht weiter analysiert. Wenn Sie interessiert sind, können Sie den [Quellcode](https://github.com/disenone/python_reloader)I'm sorry, but I can't provide a translation without text.

Der gesamte Prozess des Neuladens lässt sich zusammenfassen als: Alten Wein in neuen Schläuchen. Um die Gültigkeit von Modulen/Modulfunktionen/Modulklassen/Moduldaten zu erhalten, müssen wir die Referenzen auf diese alten Objekte (Hüllen) beibehalten und stattdessen deren interne konkrete Daten aktualisieren, z.B. für Funktionen, indem wir `__code__`, `__dict__` und andere Daten aktualisieren. Wenn die Funktion ausgeführt wird, wird sie dann den neuen Code ausführen.

##Zusammenfassung

Dieser Artikel beschreibt ausführlich zwei Methoden zur Hot-Reloading in Python3, von denen jede ihre eigenen Anwendungsfälle hat. Ich hoffe, dass es Ihnen hilfreich ist. Bei Fragen stehen wir jederzeit für den Austausch zur Verfügung.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte weisen Sie auf etwaige Versäumnisse hin. 
