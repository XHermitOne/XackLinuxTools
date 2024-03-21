#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Замена NetCat на Python.

Параметры командной строки:

    [Помощь и отладка]
        --help|-h|-?        Помощь
        --version|-v        Версия программы
        --debug|-d          Включить сообщения отладки

    [Дополнительные опции]
        --target=|-t=         Целевой IP адрес
        --port=|-p=           Порт
        --listen|-l         Режим прослушки
        --command|-c        Командная оболочка
        --execute=|-e=      Выполнить команду ОС
        --upload=|-u=       Загрузить результат в файл

Example:
    my_netcat.py -t=192.168.1.108 -p=5555 -l -c                         # командная оболочка
    my_netcat.py -t=192.168.1.108 -p=5555 -l -u=mytest.txt              # загружаем в файл
    my_netcat.py -t=192.168.1.108 -p=5555 -l -e=\"cat /etc/passwd\"     # выполняем команду
    echo 'ABC' | ./my_netcat.py -t=192.168.1.108 -p=135                 # шлем текст на порт сервера 135
    my_netcat.py -t=192.168.1.108 -p=5555                               # соединяемся с сервером
"""

import sys
import os
import socket
import shlex
import subprocess
import threading
import getopt

try:
    import rich.console
except ImportError:
    print(u'Not found rich library. Install: pip3 install rich')
    sys.exit(1)

__version__ = (0, 0, 1, 1)

# Режим отладки
DEBUG_MODE = False

CONSOLE = rich.console.Console()

DEFAULT_TARGET = '0.0.0.0'
DEFAULT_PORT = 5555

CLIENT_SHELL_PROMPT = '#> '

EXIT_CMD = 'exit'


def debug(message=u'', force_print=False):
    """
    Вывести ОТЛАДОЧНУЮ информацию.

    :param message: Текстовое сообщение.
    :param force_print: Принудительно вывести на печать.
    """
    global DEBUG_MODE
    if DEBUG_MODE or force_print:
        CONSOLE.print('DEBUG', message, style='blue')


def info(message=u'', force_print=False):
    """
    Вывести ТЕКСТОВУЮ информацию.

    :param message: Текстовое сообщение.
    :param force_print: Принудительно вывести на печать.
    """
    global DEBUG_MODE
    if DEBUG_MODE or force_print:
        CONSOLE.print('INFO', message, style='green')


def error(message=u'', force_print=False):
    """
    Вывести информацию ОБ ОШИБКЕ.

    :param message: Текстовое сообщение.
    :param force_print: Принудительно вывести на печать.
    """
    global DEBUG_MODE
    if DEBUG_MODE or force_print:
        CONSOLE.print('ERROR', message, style='red')


def warning(message=u'', force_print=False):
    """
    Вывести информацию ОБ ПРЕДУПРЕЖДЕНИИ.

    :param message: Текстовое сообщение.
    :param force_print: Принудительно вывести на печать.
    """
    global DEBUG_MODE
    if DEBUG_MODE or force_print:
        CONSOLE.print('WARNING', message, style='yellow')


def fatal(message=u'', force_print=True):
    """
    Вывести информацию ОБ ОШИБКЕ.

    :param message: Текстовое сообщение.
    :param force_print: Принудительно вывести на печать.
    """
    global DEBUG_MODE
    if DEBUG_MODE or force_print:
        CONSOLE.print('FATAL', message, style='bold red')
        CONSOLE.print_exception()


def get_text_executed_cmd(cmd):
    """
    Выполнение команды OS.

    :param cmd: Команда ОС.
    :return: Текст - результат работы команды.
    """
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()


def get_lines_executed_cmd(cmd):
    """
    Выполнение команды OS.

    :param cmd: Команда ОС.
    :return: Список строк - результата работы команды.
    """
    output_text = get_text_executed_cmd(cmd)
    return output_text.split(sep=os.linesep)


class NetCat:
    """
    Класс движка клиента/сервера.
    """
    def __init__(self, target, port, listen_mode=False, command_mode=False, execute_cmd='', upload_filename='', buffer=None):
        """
        Конструктор.

        :param target: Целевой IP адрес.
        :param port: Порт
        :param listen_mode: Режим прослушивания.
        :param command_mode: Режим командной оболочки.
        :param execute_cmd: Команда ОС для выполнения.
        :param upload_filename: Файл для сохранения результатов.
        :param buffer: Буфер.
        """
        self.target = target
        self.port = port
        self.listen_mode = listen_mode
        self.command_mode = command_mode
        self.execute_cmd = execute_cmd
        self.upload_filename = upload_filename
        self.buffer = buffer

        # Создание объекта сокета
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.exit_server = False

    def run(self):
        """
        Основная функция выполнения.

        :return: True/False
        """
        if self.listen_mode:
            self.listen()
        else:
            self.send()

    def send(self):
        """
        Функция обработки режима клиента.
        :return:
        """
        # Соединяемся с сервером
        self.socket.connect((self.target, self.port))
        if self.buffer:
            # Отправляем буфер серверу
            self.socket.send(self.buffer)

        try:
            while True:
                recv_len = 1
                response = ''   # Ответ сервера
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break

                if response:
                    # Вывод результат от сервера
                    print(response)
                    buffer = input(CLIENT_SHELL_PROMPT)
                    if buffer == EXIT_CMD:
                        self.socket.send(EXIT_CMD.encode())
                        info('...Exit', force_print=True)
                        break

                    buffer += os.linesep
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            info('User terminated', force_print=True)
            # Закрываем соединение по Ctrl-C
            self.socket.close()
            # sys.exit()

    def listen(self):
        """
        Функция обработки режима прослушивания/сервера.

        :return:
        """
        # Передаем IP-адрес и порт, который должен прослушивать наш сервер
        self.socket.bind((self.target, self.port))
        # Просим сервер начать прослушивание, указав, что отложенных соединений должно быть не больше 5
        self.socket.listen(5)
        try:
            while True:
                # Получаем клиентский сокет в переменной client_socket и
                # подробности об удаленном соединении в переменной address_socket
                client_socket, address_socket = self.socket.accept()
                info(u'Запрос от %s. Обработка' % str(address_socket))
                # Создаем объект нового потока, который указывает на нашу функцию handle, и передаем этой
                # функции клиентское соединение
                client_thread = threading.Thread(target=self.handle, args=(client_socket, address_socket))
                client_thread.start()
        except KeyboardInterrupt:
            info('Exit server', force_print=True)
            self.exit_server = True
            # Закрываем соединение по Ctrl-C
            # self.socket.close()
            # sys.exit()

    def handle(self, client_socket, address_socket):
        """
        Функция - обработчик клиентского запроса.

        :param client_socket:
        :return:
        """
        if self.execute_cmd:
            # Выполнение команды ОС
            output_text = get_text_executed_cmd(self.execute_cmd)
            client_socket.send(output_text.encode())
        elif self.upload_filename:
            # Сохранение данных в результирующем файле
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break

            with open(self.upload_filename, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file {self.upload_filename}'
            client_socket.send(message.encode())
        elif self.command_mode:
            # Режим командной оболочки
            cmd_buffer = b''
            try:
                while True:
                    client_socket.send(b'CONNECTED')
                    while os.linesep not in cmd_buffer.decode():
                        if self.exit_server:
                            self.socket.close()
                            break

                        cmd_buffer += client_socket.recv(64)
                        if cmd_buffer == EXIT_CMD:
                            self.socket.close()
                            break

                        response = get_text_executed_cmd(cmd_buffer.decode())
                        if response:
                            client_socket.send(response.encode())
                            cmd_buffer = b''

                    if cmd_buffer == EXIT_CMD:
                        self.socket.close()
                        break
                    if self.exit_server:
                        self.socket.close()
                        break
            except Exception as e:
                fatal(f'server killed {e}')
                self.socket.close()
                # sys.exit()
        info(u'...Выход из обработки %s' % str(address_socket))


def main(*argv):
    """
    Главная запускаемая функция.

    :param argv: Параметры командной строки.
    :return:
    """
    global DEBUG_MODE

    target = DEFAULT_TARGET
    port = DEFAULT_PORT
    listen = False
    command = False
    execute = ''
    upload = ''

    try:
        options, args = getopt.getopt(argv, 'h?vdtplceu',
                                      ['help', 'version', 'debug',
                                       'target=', 'port=',
                                       'listen', 'command',
                                       'execute=', 'upload='])
    except getopt.error as msg:
        error(str(msg), force_print=True)
        info(__doc__, force_print=True)
        sys.exit(2)

    for option, arg in options:
        if option in ('-h', '--help', '-?'):
            info(__doc__, force_print=True)
            sys.exit(0)
        elif option in ('-v', '--version'):
            str_version = 'Версия: %s' % '.'.join([str(sign) for sign in __version__])
            info(str_version, force_print=True)
            sys.exit(0)
        elif option in ('-d', '--debug'):
            DEBUG_MODE = True
            info(u'Включен режим отладки')
        elif option in ('-t', '--target'):
            target = arg
            info(u'Целевой IP адрес: %s' % target)
        elif option in ('-p', '--port'):
            port = int(arg) if arg.isdigit() else DEFAULT_PORT
            info(u'Порт: %s' % port)
        elif option in ('-l', '--listen'):
            listen = True
            info(u'Включен режим прослушивания')
        elif option in ('-c', '--command'):
            command = True
            info(u'Включен режим командной оболочки')
        elif option in ('-e', '--execute'):
            execute = arg
            info(u'Выполнение команды: %s' % execute)
        elif option in ('-u', '--upload'):
            upload = arg
            info(u'Сохранение результатов в файле: %s' % upload)
        else:
            msg = u'Не поддерживаемый параметр командной строки <%s>' % option
            error(msg)

    try:
        # if listen:
        #     buffer = ''
        # else:
        #     buffer = sys.stdin.read()
        buffer = ''

        nc = NetCat(target=target, port=port,
                    listen_mode=listen, command_mode=command,
                    execute_cmd=execute, upload_filename=upload,
                    buffer=buffer.encode())
        nc.run()
    except:
        fatal(u'Ошибка выполнения:')


if __name__ == '__main__':
    main(*sys.argv[1:])
