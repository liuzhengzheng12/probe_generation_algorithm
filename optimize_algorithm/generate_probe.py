# -*- coding: utf-8 -*-
import networkx as nx
from scapy.all import *
from scapy.fields import *
import math

class SR_Header(Packet):
   fields_desc = [ BitField("cnt", 0, 8)]

def classify_queries(query_list):
    query_cluster_list = {'performance': {}, 'failure': {}}
    for query in query_list:
        pass
    query_cluster_list = {'performance': {}, 'failure': {}}
    return query_cluster_list


def generate_derived_metadata_set(query_cluster_list):
    for query_cluster in query_cluster_list:

    pass
