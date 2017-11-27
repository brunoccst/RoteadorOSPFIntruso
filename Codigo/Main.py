import os
from Packet import *
from OSPF import *
from IPV4 import *
from Ethernet import *

def main():
    # Limpa o console e apresenta mensagem inicial
    clear()
    print "Iniciando ataque OSPF."

    # Cria pacote de ataque OSPF
    pctOSPF = OSPF()
    pctIPV4 = IPV4(pctOSPF)
    pctETH = Ethernet(pctOSPF)
    pctFull = Packet("OSPF-Attack", pctETH)

    print pctFull.unpack()
    

if __name__ == "__main__":
    clear = lambda: os.system('clear')
    main()
