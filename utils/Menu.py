#!/usr/bin/env python3

from simple_term_menu import TerminalMenu
import os

class Entry(object):
    # passa-se nome da opção mais callback quando selecionada
    def __init__(self, item, callback):
        self.item = item
        self.callback = callback

class Entries(object):
    def __init__(self, entries=None):
        self.entries = entries or None
    def addEntry(self, entry):
        self.entries.append(entry)
    def getItems(self):
        items = map(lambda e: e.item, self.entries)
        return list(items)
    def getCallbacks(self):
        callback = map(lambda e: e.callback, self.entries)
        return list(callbacks)
    def __getitem__(self, index):
        return self.entries[index]

class Menu(object):
    EXIT = -1
    def __init__(self, title, entries):
        self.entries = entries
        self.menu = TerminalMenu(
            menu_entries = entries.getItems(),
            title = title
        )
    def run(self):
        while True:
            os.system("clear")
            selected = self.menu.show()
            if selected is None:
                break
            res = self.entries[selected].callback()
            if res == Menu.EXIT:
                break

#
# TESTING
#
def dummy(message):
    import time
    def closure():
        print(message)
        time.sleep(1)
        if message == "cya": return Menu.EXIT
    return closure

def test_menu():
    nested_entries = Entries([Entry("cool", dummy("cool")), Entry("dummy", dummy("cya"))])
    nested_menu = Menu("### NESTED ###", nested_entries)

    # No futuro estaremos a invocar funções de outro lado
    entries = Entries([
        Entry("Configure", dummy("configure")),
        Entry("Run", dummy("run")),
        Entry("Nested", nested_menu.run),
        Entry("Exit", dummy("cya"))
    ])
    main_menu = Menu("### PENSEC ###", entries)
    main_menu.run()

if __name__ == "__main__":
    test_menu()