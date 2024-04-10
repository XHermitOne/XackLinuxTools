#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"""

import socket
import os
import ctypes
import struct

__version__ = (0, 0, 0, 1)

# узел для прослушивания
HOST = socket.gethostbyname(socket.gethostname())


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


def sniff(host):
	# должно быть знакомо по предыдущему примеру
	if os.name == 'nt':
		socket_protocol = socket.IPPROTO_IP
	else:
		socket_protocol = socket.IPPROTO_ICMP
	sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
	sniffer.bind((host, 0))
	sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
	if os.name == 'nt':
		sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
	try:
		while True:
			# читаем пакет
			raw_buffer = sniffer.recvfrom(65535)[0]
			# создаем IP-заголовок из первых 20 байтов
			ip_header = IP(raw_buffer[0:20])
			# выводим обнаруженные протокол и адреса
			print('Protocol: %s %s -> %s' % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))
	except KeyboardInterrupt:
		# если мы в Windows, выключаем неизбирательный режим
		if os.name == 'nt':
			sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


def main():
	# создаем сырой сокет и привязываем к общедоступному интерфейсу
	if os.name == 'nt':
		socket_protocol = socket.IPPROTO_IP
	else:
		socket_protocol = socket.IPPROTO_ICMP

	sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
	sniffer.bind((HOST, 0))
	# делаем так, чтобы захватывался IP-заголовок
	sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
	if os.name == 'nt':
		sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
	# читаем один пакет
	print(sniffer.recvfrom(65565))

	# если мы в Windows, выключаем неизбирательный режим
	if os.name == 'nt':
		sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


if __name__ == '__main__':
	main()
