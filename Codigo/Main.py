import netifaces
import socket
import os
import sys
from PackageManager import *
from Constants import *


"""
    Metodo principal.
"""
if __name__ == "__main__": 
    clear = lambda: os.system('clear')
    clear()

    # Tenta abrir o socket
    s = None
    try:
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
    except socket.error, msg:
        print 'Falha na criacao do socket. Codigo de error : ' + str(msg[0]) + ' Mensagem ' + msg[1]
        sys.exit()

    packageManager = PackageManager(SRC_MAC, SRC_IP, SRC_PORT, INTERFACE_NAME)
    packet = packageManager.buildFullPack(DST_MAC, DST_IP, DST_PORT, 1)
    print packet

    s.sendto(packet, (INTERFACE_NAME, 0))
