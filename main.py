# -*- coding: utf-8 -*-
from topology.fat_tree import FatTreeTopology
from optimize_algorithm.generate_probe import generate_probe_set
from query_primitives.query import PathQuery, NodeQuery

if __name__ == '__main__':
    query_list = [NodeQuery(1, 2, {'ingress_port': {}}, 1, {'egress_tstamp': {}}, 'performance'),
                  PathQuery(2, 3, 8, 1, {'ingress_port': {}}, 1, {'ingress_tstamp': {}}, 'failure')]
    fat_tree = FatTreeTopology()
    k_fwd = 10
    k_tele = 2

    probe_pkt_list = generate_probe_set(query_list, fat_tree, k_fwd, k_tele)
