from Packet import Packet

class IPV4(Packet):
    def __init__(self, innerPackage):
        Packet.__init__(self, "IPV4", innerPackage)
        self.version_ihl = (4 << 4) + 5
        self.tos = 0
        self.total_length = 20
        self.identification = 0
        self.flags_fragment_offset = 0
        self.ttl = 64
        self.protocol = 89  # OSPF
        self.checksum = 0
        self.src_addr = None
        self.dst_addr = None
        self.structure = '!BBHHHBBH4s4s'

    def setSrc(self, addr):
        self.src_addr = addr

    def setDst(self, addr):
        self.dst_addr = addr

    def pack(self):
        return pack(self.structure, self.version_ihl, self.tos, self.total_length, self.identification, self.flags_fragment_offset, self.ttl, self.protocol, self.checksum, self.src_addr, self.dst_addr)

    def unpack(self, data):
        self.version_ihl, self.tos, self.total_length, self.identification, self.flags_fragment_offset, self.ttl, self.protocol, self.checksum, self.src_addr, self.dst_addr = unpack(self.structure, data)
