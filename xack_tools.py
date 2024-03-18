#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"""

import sys
import os
try:
    import rich.console
except ImportError:
    print(u'Not found rich library. Install: sudo apt install python3-rich')
    sys.exit(1)

__version__ = (0, 0, 1, 1)

CONSOLE = rich.console.Console()

PROGRAM_LOGO = '''
▒██   ██▒ ▄▄▄       ▄████▄   ██ ▄█▀    ██▓     ██▓ ███▄    █  █    ██ ▒██   ██▒   ▄▄▄█████▓ ▒█████   ▒█████   ██▓      ██████ 
▒▒ █ █ ▒░▒████▄    ▒██▀ ▀█   ██▄█▒    ▓██▒    ▓██▒ ██ ▀█   █  ██  ▓██▒▒▒ █ █ ▒░   ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    ▒██    ▒ 
░░  █   ░▒██  ▀█▄  ▒▓█    ▄ ▓███▄░    ▒██░    ▒██▒▓██  ▀█ ██▒▓██  ▒██░░░  █   ░   ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░    ░ ▓██▄   
 ░ █ █ ▒ ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄    ▒██░    ░██░▓██▒  ▐▌██▒▓▓█  ░██░ ░ █ █ ▒    ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░      ▒   ██▒
▒██▒ ▒██▒ ▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄   ░██████▒░██░▒██░   ▓██░▒▒█████▓ ▒██▒ ▒██▒     ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒▒██████▒▒
▒▒ ░ ░▓ ░ ▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒   ░ ▒░▓  ░░▓  ░ ▒░   ▒ ▒ ░▒▓▒ ▒ ▒ ▒▒ ░ ░▓ ░     ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░▒ ▒▓▒ ▒ ░
░░   ░▒ ░  ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░   ░ ░ ▒  ░ ▒ ░░ ░░   ░ ▒░░░▒░ ░ ░ ░░   ░▒ ░       ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░░ ░▒  ░ ░
 ░    ░    ░   ▒   ░        ░ ░░ ░      ░ ░    ▒ ░   ░   ░ ░  ░░░ ░ ░  ░    ░       ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░   ░  ░  ░  
 ░    ░        ░  ░░ ░      ░  ░          ░  ░ ░           ░    ░      ░    ░                  ░ ░      ░ ░      ░  ░      ░  
                   ░                                                                                                          
'''


def print_logo():
    """
    Print program logo.
    :return:
    """
    CONSOLE.clear()
    CONSOLE.print(PROGRAM_LOGO, style='bold green')


MAIN_MENUITEMS = '''
1. Information / Информация
0. Exit / Выход
'''  # assuming you want to display menulist, having it as a tuple is useless


def main_menu():
    """
    Main menu function.
    :return:
    """
    print_logo()
    CONSOLE.print(MAIN_MENUITEMS, style='green')

    target = CONSOLE.input('Pick an item from the menu / Выберите номер элемента меню: ')

    if target == '1':  # this is an equality operator, whereas = is used to assign a variable (This checks the equality basically)
        information_menu()
    elif target == '0':
        CONSOLE.print('...exit', style='green')  # excessive indenting
        return

    return main_menu()


INFORMATION_MENUITEMS = '''
1. System information / Информация о системе
2. Processes / Процессы
0. Return / Возврат
'''


def information_menu():
    """
    Information menu function.
    :return:
    """
    print_logo()
    CONSOLE.print(INFORMATION_MENUITEMS, style='green')

    target = CONSOLE.input('Pick an item from the menu / Выберите номер элемента меню: ')

    if target == '1':
        CONSOLE.print(u'System Information / Информация о системе:', style='cyan')
        os.system('neofetch')
        os.system('uname -a')
        CONSOLE.print(u'Net Interfaces / Сетевые интерфейсы:', style='cyan')
        os.system('ip address')
        CONSOLE.print(u'Route Table / Таблица маршрутизации', style='cyan')
        os.system('route')
        os.system('echo -n "Press any key..."')
        os.system('read ANSWER')
        return information_menu()
    elif target == '2':
        os.system('htop')
        return information_menu()
    elif target == '0':
        return

    return information_menu()


def main():
    """
    Main function.
    :return:
    """
    try:
        main_menu()
    except:
        CONSOLE.print_exception()


if __name__ == '__main__':
    main()
