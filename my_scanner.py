#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"""

import ipaddress
import os
import socket
import struct
import ctypes
import sys
import threading
import time

__version__ = (0, 0, 0, 1)

# сканируемая подсеть
SUBNET = '192.168.1.0/24'

# волшебная строка, которую мы будем искать в ICMP-ответах
MESSAGE = 'PYTHONRULES!'

# Протоколы
PROTOCOL_MAP = {1: 'ICMP',
				6: 'TCP',
				17: 'UDP'}


class IP(ctypes.Structure):
	"""
	IP-заголовок.
	"""
	_fields_ = [
		('ihl', ctypes.c_ubyte, 4), 			# 4-битный беззнаковый тип char
		('version', ctypes.c_ubyte, 4), 		# 4-битный беззнаковый тип char
		('tos', ctypes.c_ubyte, 8), 			# 1-байтный тип char
		('len', ctypes.c_ushort, 16), 			# 2-байтный беззнаковый тип short
		('id', ctypes.c_ushort, 16), 			# 2-байтный беззнаковый тип short
		('offset', ctypes.c_ushort, 16), 		# 2-байтный беззнаковый тип short
		('ttl', ctypes.c_ubyte, 8), 			# 1-байтный тип char
		('protocol_num', ctypes.c_ubyte, 8), 	# 1-байтный тип char
		('sum', ctypes.c_ushort, 16), 			# 2-байтный беззнаковый тип short
		('src', ctypes.c_uint32, 32), 			# 4-байтный беззнаковый тип int
		('dst', ctypes.c_uint32, 32)			# 4-байтный беззнаковый тип int
	]

	def __new__(cls, socket_buffer=None):
		return cls.from_buffer_copy(socket_buffer)

	def __init__(self, socket_buffer=None):
		"""
		Конструктор.

		:param socket_buffer:
		"""
		# human readable IP addresses
		self.src_address = socket.inet_ntoa(struct.pack('<L', self.src))
		self.dst_address = socket.inet_ntoa(struct.pack('<L', self.dst))
		try:
			self.protocol = PROTOCOL_MAP.get(self.protocol_num, None)
			if self.protocol is None:
				self.protocol = socket.getservbyport(self.protocol_num)
		except Exception as e:
			print('%s No protocol for %s' % (e, self.protocol_num))
			self.protocol = str(self.protocol_num)

class ICMP(ctypes.Structure):
	"""
	IP-заголовок.
	"""
	_fields_ = [
		('type', ctypes.c_ubyte, 8),
		('code', ctypes.c_ubyte, 8),
		('sum', ctypes.c_ushort, 16),
		('id', ctypes.c_ushort, 16),
		('seq', ctypes.c_ushort, 16),
	]

	def __new__(cls, socket_buffer=None):
		return cls.from_buffer_copy(socket_buffer)

	def __init__(self, socket_buffer=None):
		"""
		Конструктор.

		:param socket_buffer:
		"""
		pass


# эта функция добавляет в UDP-датаграммы наше волшебное сообщение
def udp_sender():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(SUBNET).hosts():
            sender.sendto(bytes(MESSAGE, 'utf8'), (str(ip), 65212))

class Scanner:
    def __init__(self, host):
        self.host = host
        if os.name == 'nt':
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        self.socket.bind((host, 0))
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        if os.name == 'nt':
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    def sniff(self):
        hosts_up = set([f'{str(self.host)} *'])
        try:
            while True:
                # читаем пакет
                raw_buffer = self.socket.recvfrom(65535)[0]
                # создаем IP-заголовок из первых 20 байт
                ip_header = IP(raw_buffer[0:20])
                # нас интересует ICMP
                if ip_header.protocol == "ICMP":
                    offset = ip_header.ihl * 4
                    buf = raw_buffer[offset:offset + 8]
                    icmp_header = ICMP(buf)
                    # ищем тип и код 3
                    if icmp_header.code == 3 and icmp_header.type == 3:
                        if ipaddress.ip_address(ip_header.src_address) in  ipaddress.IPv4Network(SUBNET):
                            # проверяем, содержит ли буфер наше волшебное сообщение
                            if raw_buffer[len(raw_buffer) - len(MESSAGE):] == bytes(MESSAGE, 'utf8'):
                                tgt = str(ip_header.src_address)
                                if tgt != self.host and tgt not in hosts_up:
                                    hosts_up.add(str(ip_header.src_address))
                                    print(f'Host Up: {tgt}')
        # обрабатываем Ctrl+C
        except KeyboardInterrupt:
            if os.name == 'nt':
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            print('\nUser interrupted.')
            if hosts_up:
                print(f'\n\nSummary: Hosts up on {SUBNET}')
            for host in sorted(hosts_up):
                print(f'{host}')
                print('')
            sys.exit()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = '192.168.1.203'
    s = Scanner(host)
    time.sleep(5)
    t = threading.Thread(target=udp_sender)
    t.start()
    s.sniff()
