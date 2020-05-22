#!/usr/bin/env python3

from simple_term_menu import TerminalMenu
import os
import time

def main():
    main_title = "### PENSEC ###"
    main_items = ["Configure", "Run", "Exit"]
    main_menu_exit = False
    main_menu = TerminalMenu(
        menu_entries=main_items,
        title=main_title
    )

    while not main_menu_exit:
        os.system("clear")
        main_item_selected = main_menu.show()
        if main_item_selected == 0:
            print("configure")
            time.sleep(2)
        elif main_item_selected == 1:
            print("run")
            time.sleep(2)
        elif main_item_selected == 2:
            print("cya")
            main_menu_exit = True

if __name__ == "__main__":
    main()