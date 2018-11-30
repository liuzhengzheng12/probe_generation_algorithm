# -*- coding: utf-8 -*-
from scapy.all import *
from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr1

p = sr1(IP(dst=sys.argv[1])/ICMP())
if p:
    p.show()
