# -*- coding: utf-8 -*-
from topology.fat_tree import FatTreeTopology
from optimize_algorithm.generate_probe import generate_probe_set
from query_primitives.query import PathQuery, NodeQuery

if __name__ == '__main__':
    node_query_list = [NodeQuery(2, 2, {'ingress_port': {}}, 1, {'egress_tstamp': {}}, 'failure')]
    path_query_list = [PathQuery(2, 3, 8, 1, {'ingress_port': {}}, 0.5, {'ingress_tstamp': {}}, 'failure')]
    query_list = node_query_list + path_query_list
    fat_tree = FatTreeTopology()
    k_fwd = 100
    k_tele = 5

    probe_pkt_list = generate_probe_set(query_list, fat_tree, k_fwd, k_tele)
