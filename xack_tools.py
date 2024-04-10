#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"""

import sys
import os
import socket
try:
    import rich.console
except ImportError:
    print(u'Not found rich library. Install: pip3 install rich')
    sys.exit(1)

__version__ = (0, 0, 2, 2)

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
2. Net tools / Сетевые инструменты
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
    elif target == '2':
        net_tools_menu(show_logo=False, show_menu=True)
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


NET_TOOLS_MENUITEMS = '''
1. My NetCat server / NetCat сервер
2. My NetCat client / NetCat клиент
0. Return / Возврат
'''


def net_tools_menu(show_logo=True, show_menu=True):
    """
    Net tools menu function.

    :return:
    """
    if show_logo:
        print_logo()
    if show_menu:
        CONSOLE.print(NET_TOOLS_MENUITEMS, style='green')

    target = CONSOLE.input('Pick an item from the menu / Выберите номер элемента меню: ')

    if target == '1':
        os.system('python3 my_netcat.py --version')
        import my_netcat
        host_name = socket.gethostname()
        host_ip = my_netcat.get_my_host_ip()
        CONSOLE.print(u'Host name / Имя компьютера:', host_name, u'IP address / IP адрес:', host_ip, style='cyan')
        cmd = 'python3 my_netcat.py --debug --target=%s --port=5555 --listen --command' % host_ip
        CONSOLE.print(cmd, style='cyan')
        CONSOLE.print(u'Exit / Выход - Ctrl+C', style='cyan')
        os.system(cmd)
    elif target == '2':
        os.system('python3 my_netcat.py --version')
        host = input(u'Enter the server address / Введите адрес сервера:')
        port = input(u'Enter the port / Введите порт:')
        cmd = 'python3 my_netcat.py --debug --target=%s --port=%s' % (host, port)
        CONSOLE.print(cmd, style='cyan')
        CONSOLE.print(u'Exit / Выход - exit', style='cyan')
        os.system(cmd)
    elif target == '0':
        return
    else:
        return net_tools_menu(show_logo=False, show_menu=False)

    print_logo()
    CONSOLE.print(MAIN_MENUITEMS, style='green')
    return net_tools_menu(show_logo=False, show_menu=True)


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
