import netifaces
import socket
import os
import sys
from PackageManager import *
from Constants import *
import time

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

    # Envia o pacote de HELLO
    packet = packageManager.buildFullPack(DST_MAC, DST_IP, DST_PORT, OSPF_HELLO)
    s.sendto(packet, (INTERFACE_NAME, 0))
    print "Pacote HELLO enviado"

    # Envia 10 pacotes de DBD
    for i in range(0, 10):
        if (i == 10):
            packet = packageManager.buildFullPack(DST_MAC, DST_IP, DST_PORT, OSPF_DBD, True)
        else:
            packet = packageManager.buildFullPack(DST_MAC, DST_IP, DST_PORT, OSPF_DBD, False)
        s.sendto(packet, (INTERFACE_NAME, 0))
        print "Pacote DBD ", packageManager.currentDBD, " enviado"

    # Envia o pacote de HELLO constantemente a cada 10 segundos
    while (True):
        packet = packageManager.buildFullPack(DST_MAC, DST_IP, DST_PORT, OSPF_HELLO)
        s.sendto(packet, (INTERFACE_NAME, 0))
        print "Pacote HELLO enviado"
        time.sleep(10)

