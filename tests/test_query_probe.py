# -*- coding: utf-8 -*-
from topology.fat_tree import FatTreeTopology
from naive_algorithm.generate_probe import naive_generate_probe_set
from optimize_algorithm.generate_probe import optimize_generate_probe_set
from query_primitives.query import PathQuery, NodeQuery
from utils.const import metadata_list
from random import randint

if __name__ == '__main__':
    fat_tree = FatTreeTopology()
    k_fwd = 100
    k_tele = 5
    metadata_len = len(metadata_list)
    k = 5
    category = ['performance', 'failure']
    f = open('testsdata/fig2_query_probe.txt', 'w')

    node_query_list = []
    path_query_list = []
    for query_cnt in xrange(10, 1010, 10):
        node_query_cnt = query_cnt / 2
        for index in xrange(node_query_cnt-5, node_query_cnt):
            node_query_where = {}
            node_query_return = {}
            for _ in xrange(index):
                node_query_where[metadata_list[randint(0, index) % metadata_len]] = {}
                node_query_return[metadata_list[randint(0, index) % metadata_len]] = {}
            node_query_list.append(NodeQuery(index, randint(0, k), node_query_where, randint(1, node_query_cnt),
                                             node_query_return, category[randint(0, 1)]))

        path_query_cnt = query_cnt / 2
        for index in xrange(path_query_cnt-5, path_query_cnt):
            path_query_where = {}
            path_query_return = {}
            for _ in xrange(index):
                path_query_where[metadata_list[randint(0, index) % metadata_len]] = {}
                path_query_return[metadata_list[randint(0, index) % metadata_len]] = {}
            path_query_list.append(PathQuery(index, randint(0, k), index+1, randint(0, k),
                                             path_query_where, randint(1, path_query_cnt), path_query_return,
                                             category[randint(0, 1)]))

        query_list = node_query_list + path_query_list
        naive_probe_pkt_list = naive_generate_probe_set(query_list, fat_tree, k_fwd, k_tele)
        naive_probe_cnt = 0
        for probe_set in naive_probe_pkt_list:
            naive_probe_cnt += len(probe_set)

        optimize_probe_pkt_list = optimize_generate_probe_set(query_list, fat_tree, k_fwd, k_tele)
        optimize_probe_cnt = 0
        # print optimize_probe_pkt_list
        for probe_type in ['performance', 'failure']:
            probe_set_dict = optimize_probe_pkt_list[probe_type]
            for freq, probe_set in probe_set_dict.iteritems():
                optimize_probe_cnt += len(probe_set)

        print query_cnt, naive_probe_cnt, optimize_probe_cnt
        f.write('{} {} {}\n'.format(query_cnt, naive_probe_cnt, optimize_probe_cnt))
    f.close()
