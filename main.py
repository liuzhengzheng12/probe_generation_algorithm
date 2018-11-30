# -*- coding: utf-8 -*-
from topology.fat_tree import FatTreeTopology
from naive_algorithm.generate_probe import generate_probe
from query_primitives.query import PathQuery, NodeQuery

if __name__ == '__main__':
    query_list = [NodeQuery(1, 2, {'ingress_port': {}}, 1, {'egress_timestamp': {}}),
                  PathQuery(2, 3, 8, 1, {'ingress_port': {}}, 1, {'ingress_timestamp': {}})]
    fat_tree = FatTreeTopology()
    k_tele = 2
    generate_probe(query_list, fat_tree, k_tele)
