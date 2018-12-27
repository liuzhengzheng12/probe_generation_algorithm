# -*- coding: utf-8 -*-
from scapy.all import *
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP
from scapy.fields import BitField
from scapy.packet import Packet

from const import PORT_FWD


class FWD_header(Packet):
    fields_desc = [BitField('label_cnt', 0, 8)]


class FWD_label(Packet):
    fields_desc = [BitField('outport', 0, 16)]


class TMY_header(Packet):
    fields_desc = [BitField('label_cnt', 0, 8)]


class TMY_label(Packet):
    fields_desc = [BitField('switch_id', 0, 16),
                   BitField('bitmap', 0, 24)]


def assemble_probe(fwd_label_list, tmy_label_list):
    probe_pkt = Ether() / IP() / TCP(dport=PORT_FWD)

    fwd_len = len(fwd_label_list)
    probe_pkt = probe_pkt / FWD_header(label_cnt=fwd_len)
    for outport in fwd_label_list:
        probe_pkt = probe_pkt / FWD_label(outport=outport)

    tmy_len = len(tmy_label_list)
    probe_pkt = probe_pkt / TMY_header(label_cnt=tmy_len)
    for switch_id, bitmap in tmy_label_list:
        probe_pkt = probe_pkt / TMY_label(switch_id=switch_id, bitmap=bitmap)

    return probe_pkt
