import socket
import sys
from struct import *

class Packet(object):
    def __init__(self, name, innerPackage):
        self.name = name
        self.innerPacket = innerPackage

    def getName(self):
        return self.name

    def addPacket(self, pct):
        self.innerPacket = pct

    def pack(self):
        return self.innerPacket.pack()

    def checksum(self):
        return self.innerPacket.checksum()

    def unpack(self):
        print "Unpack not implemented"
