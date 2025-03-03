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

try:
    import rich_menu
except ImportError:
    print(u'Not found rich-menu library. Install: pip3 install rich-menu')
    sys.exit(1)

__version__ = (0, 0, 3, 2)

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


MAIN_MENUITEMS = [
    'Information / Информация',
    'Net tools / Сетевые инструменты',
    'Exit / Выход']


def main_menu(show_logo=True, show_menu=True):
    """
    Main menu function.
    :return:
    """
    if show_logo:
        print_logo()
    if show_menu:
        menu = rich_menu.Menu(*MAIN_MENUITEMS,
                              color='green',
                              title='*',
                              align='left',
                              panel_title='',
                              selection_char='=>',
                              )
        menu.ask(screen=False)
        target_idx = menu.index

        if target_idx == 0:
            information_menu(show_logo=False, show_menu=True)
        elif target_idx == 1:
            net_tools_menu(show_logo=False, show_menu=True)
        elif target_idx == len(MAIN_MENUITEMS) - 1:
            CONSOLE.print('...exit', style='green')  # excessive indenting
            return

    return main_menu(show_logo=True, show_menu=True)


INFORMATION_MENUITEMS = [
    'System information / Информация о системе',
    'Processes / Процессы',
    'System log / Системный журнал',
    'Kernel log / Журнал ядра',
    'Authorization log / Журнал входа пользователей в систему',
    'Return / Возврат']


def information_menu(show_logo=True, show_menu=True):
    """
    Information menu function.
    :return:
    """
    if show_logo:
        print_logo()
    if show_menu:
        menu = rich_menu.Menu(*INFORMATION_MENUITEMS,
                              color='green',
                              title='Information / Информация',
                              align='left',
                              panel_title='Information / Информация',
                              selection_char='=>',
                              )
        menu.ask(screen=False)
        target_idx = menu.index

        if target_idx == 0:
            CONSOLE.print(u'System Information / Информация о системе:', style='cyan')
            os.system('neofetch')
            os.system('uname -a')
            CONSOLE.print(u'Net Interfaces / Сетевые интерфейсы:', style='cyan')
            os.system('ip address')
            CONSOLE.print(u'Route Table / Таблица маршрутизации', style='cyan')
            os.system('route')
            os.system('echo -n "Press any key..."')
            os.system('read ANSWER')
        elif target_idx == 1:
            os.system('htop')
        elif target_idx == 2:
            os.system('lnav /var/log/syslog')
        elif target_idx == 3:
            os.system('lnav /var/log/kern.log')
        elif target_idx == 4:
            os.system('lnav /var/log/auth.log')
        elif target_idx == len(INFORMATION_MENUITEMS) - 1:
            return
        else:
            return information_menu(show_logo=False, show_menu=False)

    # print_logo()
    # CONSOLE.print(MAIN_MENUITEMS, style='green')
    return information_menu(show_logo=False, show_menu=True)


NET_TOOLS_MENUITEMS = [
    'My NetCat server / NetCat сервер',
    'My NetCat client / NetCat клиент',
    'Return / Возврат']


def net_tools_menu(show_logo=True, show_menu=True):
    """
    Net tools menu function.

    :return:
    """
    if show_logo:
        print_logo()
    if show_menu:
        menu = rich_menu.Menu(*NET_TOOLS_MENUITEMS,
                              color='green',
                              title='Net tools / Сетевые инструменты',
                              align='left',
                              panel_title='Net tools / Сетевые инструменты',
                              selection_char='=>',
                              )
        menu.ask(screen=False)
        target_idx = menu.index

        if target_idx == 0:
            os.system('python3 my_netcat.py --version')
            import my_netcat
            host_name = socket.gethostname()
            host_ip = my_netcat.get_my_host_ip()
            CONSOLE.print(u'Host name / Имя компьютера:', host_name, u'IP address / IP адрес:', host_ip, style='cyan')
            cmd = 'python3 my_netcat.py --debug --target=%s --port=5555 --listen --command' % host_ip
            CONSOLE.print(cmd, style='cyan')
            CONSOLE.print(u'Exit / Выход - Ctrl+C', style='cyan')
            os.system(cmd)
        elif target_idx == 1:
            os.system('python3 my_netcat.py --version')
            host = input(u'Enter the server address / Введите адрес сервера:')
            port = input(u'Enter the port / Введите порт:')
            cmd = 'python3 my_netcat.py --debug --target=%s --port=%s' % (host, port)
            CONSOLE.print(cmd, style='cyan')
            CONSOLE.print(u'Exit / Выход - exit', style='cyan')
            os.system(cmd)
        elif target_idx == len(NET_TOOLS_MENUITEMS) - 1:
            return
        else:
            return net_tools_menu(show_logo=False, show_menu=False)

    # print_logo()
    # CONSOLE.print(MAIN_MENUITEMS, style='green')
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
