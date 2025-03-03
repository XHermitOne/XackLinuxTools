#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"""

import sys
import socket
import os
import ctypes
import struct

__version__ = (0, 0, 0, 1)

# узел для прослушивания
HOST = socket.gethostbyname(socket.gethostname())
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
			if ip_header.protocol == 'ICMP':
				print('Protocol: %s %s -> %s' % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))
				print(f'Version: {ip_header.version}')
				print(f'Header Length: {ip_header.ihl} TTL:	{ip_header.ttl}')
				# определяем, где начинается ICMP-пакет
				offset = ip_header.ihl * 4
				buf = raw_buffer[offset:offset + 8]
				# создаем структуру ICMP
				icmp_header = ICMP(buf)
				print('ICMP -> Type: %s Code: %s\n' % (icmp_header.type, icmp_header.code))
			else:
				# выводим обнаруженные протокол и адреса
				print('Protocol: %s %s -> %s' % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))
	except KeyboardInterrupt:
		# если мы в Windows, выключаем неизбирательный режим
		if os.name == 'nt':
			sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


if __name__ == '__main__':
	if len(sys.argv) == 2:
		host = sys.argv[1]
	else:
		host = HOST
	sniff(host)

