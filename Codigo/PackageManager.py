import socket
import netifaces as ni
from Constants import *
from struct import *

"""
    Gerencia pacotes.
"""
class PackageManager(object):

    """
        Inicializa uma nova instancia de UDPConnection
    """
    def __init__(self, mac, ip, port, interface):
        self.MAC        = mac
        self.IP         = ip
        self.Port       = port
        self.Interface  = interface

    """
        Monta o cabecalho Ethernet.
         0                   1                   2                   3
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |       Ethernet destination address (first 32 bits)            |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        | Ethernet dest (last 16 bits)  |Ethernet source (first 16 bits)|
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |       Ethernet source address (last 32 bits)                  |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |        Type code              |                               |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    """
    def buildEth(self, srcMac, dstMac):
        ethertype = 0x0800 # IPv4
        srcMac = srcMac.replace(":", "").decode("hex")
        dstMac = dstMac.replace(":", "").decode("hex")
        return pack("!6s6sH", dstMac, srcMac, ethertype)

    """
        Monta o cabecalho IP.
         0                   1                   2                   3
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |Version|  IHL  |Type of Service|          Total Length         |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |         Identification        |Flags|      Fragment Offset    |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |  Time to Live |    Protocol   |         Header Checksum       |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                       Source Address                          |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                    Destination Address                        |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                    Options                    |    Padding    |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    """
    def buildIp(self, srcIp, dstIp, lenOspf):

        # Configuracao basica do IP
        ip_ver = 4
        ip_ihl = 5
        ip_tos = 0
        ip_tot_len = 20 + lenOspf
        identification = 0
        ip_id = 54321
        ip_frag_off = 0
        ip_ttl = 1
        ip_proto = 89   # Protocolo seguinte: OSPF.
        ip_check = 0    # O proprio kernel vai inserir o checksum correto.
        ip_saddr = socket.inet_aton(srcIp)
        ip_daddr = socket.inet_aton(dstIp)

        ip_ihl_ver = (ip_ver << 4) + ip_ihl
        ip_header = pack('!BBHHHBB4s4s' , ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_saddr, ip_daddr)  

        ip_check = socket.htons(self.checksum(ip_header))

        # Empacota num header
        ip_header = pack('!BBHHHBBH4s4s' , ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)  
        return ip_header


    """
        Monta o cabecalho OSPF.
    """
    def buildOspf(self, ospfType, data):
        ospf_version = 2
        ospf_type = ospfType
        ospf_length = 24 + len(data)
        ospf_router_id = 0xffffff
        ospf_area_id = 0
        ospf_checksum = 0
        ospf_auth_type = 0
        ospf_auth = 0

        ospf_header = pack('!BBHIIHHQ', ospf_version, ospf_type, ospf_length, ospf_router_id, ospf_area_id, ospf_checksum, ospf_auth_type, ospf_auth)
        ospf_checksum = socket.htons(self.checksum(ospf_header + data))

        ospf_header = pack('!BBHIIHHQ', ospf_version, ospf_type, ospf_length, ospf_router_id, ospf_area_id, ospf_checksum, ospf_auth_type, ospf_auth)
        return ospf_header

    """
        Monta o cabecalho OSPF Hello.
    """
    def buildOspfHello(self, neighbours):
        ospf_net_mask = socket.inet_aton(NET_MASK)
        ospf_hello_interval = 0xA
        ospf_options = 0x2
        ospf_router_priority = 0
        ospf_dead_interval = 0x28
        ospf_designated_router = socket.inet_aton(DST_IP)
        ospf_backup_router = socket.inet_aton("0.0.0.0")
        ospf_neighbor = neighbours

        p = pack('!4sHBBI4s4s', ospf_net_mask, ospf_hello_interval, ospf_options, ospf_router_priority, ospf_dead_interval, ospf_designated_router, ospf_backup_router)

        for n in ospf_neighbor:
            p = p + pack('!4s', n)

        return p

    """
        Monta o cabecalho OSPF DBD.
    """
    def buildOspfDBD(self, sequence):
        ospf_mtu = 1500
        ospf_options = 0
        ospf_flags = 0
        ospf_sequence = sequence

        return pack('!HBBI', self.mtu, self.options, self.flags, self.sequence)

    """
        Calcula o checksum de um pacote.
    """
    def checksum(self, data):
        check = 0
        for i in range(0, len(data), 2):
            word = ord(data[i]) + (ord(data[i+1]) << 8)
            check += word

        check = (check >> 16) + (check & 0xffff)
        check = check + (check >> 16)
        return ~check & 0xffff

    """
        Constroi o pacote completo Ethernet-IPv4-UDP com as informacoes fornecidas.
    """
    def buildFullPack(self, dstMac, dstIp, dstPort, ospfType):

        # Monta a mensagem (Hello ou DBD)
        data = None
        if (ospfType == 1):
            data = self.buildOspfHello([socket.inet_aton(DST_ID)])
        else:
            data = self.buildOspfDBD()

        # Monta header UDP
        ospfHeader = self.buildOspf(ospfType, data)

        # Monta header IPv4
        ipHeader = self.buildIp(self.IP, dstIp, len(ospfHeader + data))

        # Monta header Ethernet
        ethHeader = self.buildEth(self.MAC, dstMac)

        # Junta os pacotes num so
        pct = ethHeader + ipHeader + ospfHeader + data
        return pct
