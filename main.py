# -*- coding: utf-8 -*-
from topology.fat_tree import FatTreeTopology
from optimize_algorithm.generate_probe import generate_probe_set
from query_primitives.query import PathQuery, NodeQuery
from utils.const import metadata_list
from random import randint

if __name__ == '__main__':
    fat_tree = FatTreeTopology()
    k_fwd = 100
    k_tele = 20
    metadata_len = len(metadata_list)
    for query_cnt in xrange(10, 210, 10):
        node_query_list = [NodeQuery(index, 2, {metadata_list[randint(0, 1000) % metadata_len]: {}}, 1, {metadata_list[randint(0, 1000) % metadata_len]: {}}, 'failure') for index in xrange(query_cnt/2)]
        path_query_list = [PathQuery(index, 1, index+10, 1, {metadata_list[randint(0, 2000) % metadata_len]: {}}, 0.5, {metadata_list[randint(0, 2000) % metadata_len]: {}}, 'failure') for index in xrange(query_cnt/2)]
        query_list = node_query_list + path_query_list
        probe_pkt_list = generate_probe_set(query_list, fat_tree, k_fwd, k_tele)
        probe_cnt = 0
        for category in ['performance', 'failure']:
            probe_set_dict = probe_pkt_list[category]
            for freq, probe_set in probe_set_dict.iteritems():
                probe_cnt += len(probe_set)
        print query_cnt, probe_cnt
