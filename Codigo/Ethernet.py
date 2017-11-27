from Packet import Packet

class Ethernet(Packet):
    def __init__(self, innerPackage):
        Packet.__init__(self, "IPV4", innerPackage)
        self.src = None
        self.dst = None
        self.eth_type = 0x0800  # ipv4

    def setSrc(self, src):
        self.src = src

    def setDst(self, dst):
        self.dst = dst

    def pack(self):
        return pack('!6s6sH', self.dst, self.src, self.eth_type)

    def unpack(self, data):
        self.dst, self.src, self.eth_type = unpack("!6s6sH", data)
