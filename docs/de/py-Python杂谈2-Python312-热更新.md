---
layout: post
title: Python Discussion 2 - Python 3.12 Hotfix
tags:
- dev
- game
- python
- reload
- 热更新
description: Notieren, wie man ein Hotfix in Python 3.12 implementiert
---

<meta property="og:title" content="Python 杂谈 2 - Python3.12 热更新" />

#Python Talk 2 - Python 3.12 Hotfix

> Bitte übersetzen Sie den folgenden Text ins Deutsche:

> Notieren Sie, wie Hot Updates in Python 3.12 implementiert werden können.

##Live-Update

"Hot Reload" bezeichnet die Technologie, mit der Aktualisierungen ohne Neustart des Programms durchgeführt werden können. In der Spielebranche wird diese Technik weit verbreitet eingesetzt. Entwickler müssen oft Probleme in Spielen beheben, ohne die Spieler zu beeinträchtigen. Daher wird häufig auf stille Updates zurückgegriffen, also auf "Hot Reload".


##Python Hot Update

Python ist an sich eine dynamische Sprache, in der alles Objekte sind und die die Möglichkeit hat, Hot-Updates durchzuführen. In Python können wir grob die Objekte identifizieren, die für ein Hot-Update benötigt werden, in zwei Kategorien aufteilen: Daten und Funktionen.

Daten können als Zahlen oder Einstellungen im Spiel verstanden werden, wie z.B. Spielerlevel, Ausrüstung und andere Daten. Einige Daten sollten nicht heiß aktualisiert werden (zum Beispiel das aktuelle Spielerlevel, welche Ausrüstung der Spieler hat, diese Daten sollten nicht durch ein heißes Update geändert werden), während wir andere Daten heiß aktualisieren möchten (zum Beispiel Grundwerte der Ausrüstung, Grundwerte von Fähigkeiten, Texte auf der Benutzeroberfläche usw.).

Funktionen können als Spiellogik verstanden werden, das ist im Grunde das, was wir aktualisieren möchten, und logische Fehler müssen im Wesentlichen durch die Aktualisierung von Funktionen behoben werden.

Im Folgenden werden wir genauer untersuchen, welche Methoden es gibt, um ein Hotfix für Python 3.12 durchzuführen.

## Hotfix

Die erste Methode nennen wir Hotfix. Dabei wird spezifischer Python-Code ausgeführt, um eine Aktualisierung von Daten und Funktionen zu ermöglichen. Ein einfaches Hotfix-Codebeispiel könnte so aussehen:


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

Der obige Code zeigt einfach, wie Hotfix geschrieben wird. Nach der Änderung von Daten / Funktionen wird das Programm bei zukünftigen Zugriffen die neuen Daten / Funktionen lesen und ausführen.

If you are observant, you might have a question: What would happen if other code references these data and functions that need to be modified?

```python
# attack.py module

player_fire = player.Player.fire_func

def player_attack_by_gun(player, target):
    player_fire(player, target)
    # ...
```

Die Antwort ist, dass der vorherige Hotfix in dieser Situation nicht wirksam ist. Die Funktion `fire_func` ist im Grunde eine zusätzliche Kopie in einem anderen Modul. Im Modul wird die Kopie der Funktion aufgerufen, daher wirken Änderungen am eigentlichen Funktionstext nicht auf die Kopie.

Deshalb ist es wichtig, in Ihrem Code die Verweise auf Modul- und Funktionsniveau so weit wie möglich zu reduzieren, um zu vermeiden, dass Hotfixes nicht wirksam werden. Wenn Ihr Code bereits so geschrieben ist, müssen für Hotfixes zusätzliche Maßnahmen ergriffen werden:

```python
# hotfix code
# ...

import attack
attack.player_fire = player.Player.fire_func

```

Nach der Änderung des Daten- / Funktionskörpers durch Hotfix sollte auch die Referenzen an diesen Stellen angepasst werden. Diese zusätzlichen Änderungen werden oft übersehen, daher empfehlen wir weiterhin, mehrfache Verweise im Code aus Gründen der Klarheit weitgehend zu vermeiden.

Zusammenfassend erfüllt Hotfix die grundlegenden Anforderungen für Live-Updates, hat jedoch folgende Probleme:

Wenn Daten/Funktionen von anderen Modulen explizit referenziert werden, muss zusätzlich ein Hotfix für diese Module bereitgestellt werden.
If there is a large amount of data/functions that need to be hotfixed, the hotfix code will become very large, maintenance difficulty will increase, and it will be more prone to errors.

## Reload

This chapter's source code can be obtained here: [python_reloader](https://github.com/disenone/python_reloader)

Was wir wirklich brauchen, ist ein automatisches Heißupdate. Es sollte kein zusätzliches Hotfix geschrieben werden müssen. Es reicht aus, die Code-Dateien zu aktualisieren und die Ausführung einer "Reload"-Funktion wird automatisch die neuen Funktionen und Daten ersetzen. Wir nennen diese automatische Heißupdate-Funktion "Reload".

Python 3.12 bietet die Funktion "importlib.reload", um Module neu zu laden. Es lädt jedoch das gesamte Modul neu und gibt ein neues Modulobjekt zurück. Referenzen in anderen Modulen werden nicht automatisch aktualisiert. Wenn also ein anderes Modul ein neu geladenes Modul importiert, wird immer noch auf das alte Modulobjekt zugegriffen. Diese Funktion ist nicht viel besser als unser Hotfix, zumal sie das gesamte Modul neu lädt und wir nicht kontrollieren können, welche Daten beibehalten werden sollen. Wir möchten unsere eigene Reload-Funktion implementieren, die diese Anforderungen erfüllt:

- Automatische Funktionser-setzung, wobei alte Funktionsaufrufe weiterhin wirksam sind und der Inhalt der neuen Funktion ausgeführt wird.
Automatischer Datenaustausch mit teilweiser Steuerung der Ersetzung.
Behalten Sie die Verweise auf das alte Modul bei, damit über das alte Modul auf den neuen Inhalt zugegriffen werden kann.
Die Module, die ein Reload erfordern, sind steuerbar.

Um diese Anforderungen zu erfüllen, müssen wir den Mechanismus von meta_path in Python verwenden. Für eine ausführliche Erklärung können Sie die offizielle Dokumentation [the-meta-path](https://docs.python.org/zh-cn/3/reference/import.html?highlight=meta_path#the-meta-path)I'm sorry, but the text you provided is already in German and doesn't require translation.

Die sys.meta_path ermöglicht es uns, unsere Metapfad-Suchobjekte zu definieren, zum Beispiel nennen wir den Sucher für das Neuladen reload_finder. Der reload_finder muss eine Funktion find_spec implementieren und ein spec-Objekt zurückgeben. Nachdem Python das spec-Objekt erhalten hat, wird es die Funktionen spec.loader.create_module und spec.loader.exec_module nacheinander ausführen, um den Import des Moduls abzuschließen.

Wenn wir in diesem Prozess den neuen Modulcode ausführen und die Funktionen und erforderlichen Daten des neuen Moduls in das alte Modul kopieren, können wir das Ziel des Neuladens erreichen:

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

Wie erwähnt, lädt `find_spec` den neuesten Quellcode des Moduls und führt den Code des neuen Moduls im `__dict__` des alten Moduls aus. Anschließend rufen wir `ReloadModule` auf, um Referenzen und Ersetzungen von Klassen/Funktionen/Daten zu verarbeiten. Der Zweck des `MetaLoader` besteht darin, das `meta_path`-Mechanismus anzupassen, um dem Python-Interpreter die von uns behandelten Modulobjekte zurückzugeben.

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

In `ReloadDict`, different types of objects will be distinguished and processed accordingly.

Wenn es sich um eine Klasse handelt, rufen Sie 'ReloadClass' auf, um eine Referenz auf das alte Modul zurückzugeben und die Attribute der Klasse zu aktualisieren.
Wenn es sich um eine Funktion / Methode handelt, wird durch den Aufruf von `ReloadFunction` die Referenz des alten Moduls zurückgegeben und die internen Daten der Funktion aktualisiert.
Wenn es sich um Daten handelt und sie erhalten bleiben müssen, wird `new_dict[attr_name] = old_attr` rückgängig gemacht.
Bitte behalten Sie die anderen Zitate neu.
Entfernen Sie Funktionen, die in neuen Modulen nicht vorhanden sind.

Die spezifischen Codes für `ReloadClass` und `ReloadFunction` werden hier nicht weiter analysiert. Bei Interesse können Sie den [Quellcode](https://github.com/disenone/python_reloader)Ich entschuldige mich, aber der Text "。" hat keine Bedeutung und kann nicht übersetzt werden. Gibt es noch etwas, bei dem ich Ihnen helfen kann?

Der gesamte Reload-Vorgang kann als eine Art „alter Wein in neuen Schläuchen“ zusammengefasst werden. Um die Gültigkeit von Modulen/Modulfunktionen/Modulklassen/Moduldaten aufrechtzuerhalten, müssen wir die Verweise auf diese alten Objekte (die Hüllen) beibehalten und dann die konkreten Daten darin aktualisieren. Zum Beispiel, bei Funktionen mögen wir das `__code__` oder `__dict__` aktualisieren, sodass die Funktion letztendlich den neuen Code ausführt, wenn sie aufgerufen wird.

##Zusammenfassung

Dieser Text beschreibt ausführlich zwei Arten von Hot-Update-Methoden in Python3, von denen jede ihre entsprechenden Anwendungsfälle hat. Hoffentlich ist dies für Sie hilfreich. Wenn Sie Fragen haben, zögern Sie bitte nicht, sie jederzeit mit uns zu besprechen.

--8<-- "footer_de.md"


> Dieser Beitrag wurde von ChatGPT übersetzt. Bitte gib dein [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte geben Sie alle übersehenen Stellen an. 
