import socket
import sys
from struct import *

class Packet(object):
	def __init__(self, name):
		self.name = name
		self.innerPackets = []

	def getName(self):
		return self.name

	def addPacket(self, pct):
		self.innerPackets.append(pct)

	def pack(self):
		packet = ""
		for item in enumerate(self.innerPackets):
			packet += item.pack(self)
		return packet

	def unpack(self):
		print "Unpack not implemented"