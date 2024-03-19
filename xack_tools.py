#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"""

import sys
import os
try:
    import rich.console
except ImportError:
    print(u'Not found rich library. Install: pip3 install rich')
    sys.exit(1)

__version__ = (0, 0, 1, 2)

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


def main_menu(show_logo=True, show_menu=True):
    """
    Main menu function.
    :return:
    """
    if show_logo:
        print_logo()
    if show_menu:
        CONSOLE.print(MAIN_MENUITEMS, style='green')

    target = CONSOLE.input('Pick an item from the menu / Выберите номер элемента меню: ')

    if target == '1':  # this is an equality operator, whereas = is used to assign a variable (This checks the equality basically)
        information_menu(show_logo=False, show_menu=True)
    elif target == '0':
        CONSOLE.print('...exit', style='green')  # excessive indenting
        return

    return main_menu(show_logo=True, show_menu=True)


INFORMATION_MENUITEMS = '''
1. System information / Информация о системе
2. Processes / Процессы
3. System log / Системный журнал
4. Kernel log / Журнал ядра
5. Authorization log / Журнал входа пользователей в систему
0. Return / Возврат
'''


def information_menu(show_logo=True, show_menu=True):
    """
    Information menu function.
    :return:
    """
    if show_logo:
        print_logo()
    if show_menu:
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
    elif target == '2':
        os.system('htop')
    elif target == '3':
        os.system('lnav /var/log/syslog')
    elif target == '4':
        os.system('lnav /var/log/kern.log')
    elif target == '5':
        os.system('lnav /var/log/auth.log')
    elif target == '0':
        return
    else:
        return information_menu(show_logo=False, show_menu=False)

    print_logo()
    CONSOLE.print(MAIN_MENUITEMS, style='green')
    return information_menu(show_logo=False, show_menu=True)


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
