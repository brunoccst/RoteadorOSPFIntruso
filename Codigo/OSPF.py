from Packet import Packet

class OSPF(Packet):
    def __init__(self):
        Packet.__init__(self, "OSPF", None)
        self.version = 2
        self.type = 1
        self.length = 0
        self.router_id = 99999
        self.area_id = 0
        self.checksum = 0
        self.auth_type = 0
        self.auth = 0
        self.structure = '!BBHIIHHQ'

    def pack(self):
        return pack(self.structure, self.version, self.type, self.length, self.router_id,
                    self.area_id, self.checksum, self.auth_type, self.auth)

    def unpack(self, data):
        self.version, self.type, self.length, self.router_id, self.area_id, self.checksum, self.auth_type, self.auth = unpack(self.structure, data)
