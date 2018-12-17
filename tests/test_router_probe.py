# -*- coding: utf-8 -*-
from topology.fat_tree import FatTreeTopology
from naive_algorithm.generate_probe import naive_generate_probe_set
from optimize_algorithm.generate_probe import optimize_generate_probe_set
from query_primitives.query import PathQuery, NodeQuery
from utils.const import metadata_list
from random import randint

if __name__ == '__main__':
    k_fwd = 100
    k_tele = 5
    metadata_len = len(metadata_list)
    k = 5
    category = ['performance', 'failure']
    f = open('testsdata/fig3_router_probe.txt', 'w')

    query_list_dict = {1:[], 10: [], 100: []}
    path_query_where = {}
    path_query_return = {}
    path_query_where[metadata_list[randint(0, 500) % metadata_len]] = {}
    path_query_return[metadata_list[randint(0, 500) % metadata_len]] = {}
    query_list_dict[1].append(PathQuery(randint(0, 500), randint(0, k), randint(0, 500), randint(0, k),
                                     path_query_where, randint(1, 500), path_query_return,
                                     category[randint(0, 1)]))

    node_query_list = []
    path_query_list = []
    for query_cnt in [10, 100]:
        node_query_cnt = query_cnt / 2
        for index in xrange(node_query_cnt):
            node_query_where = {}
            node_query_return = {}
            for _ in xrange(index):
                node_query_where[metadata_list[randint(0, index) % metadata_len]] = {}
                node_query_return[metadata_list[randint(0, index) % metadata_len]] = {}
            node_query_list.append(NodeQuery(index, randint(0, k), node_query_where, randint(1, node_query_cnt),
                                             node_query_return, category[randint(0, 1)]))

        path_query_cnt = query_cnt / 2
        for index in xrange(path_query_cnt):
            path_query_where = {}
            path_query_return = {}
            for _ in xrange(index):
                path_query_where[metadata_list[randint(0, index) % metadata_len]] = {}
                path_query_return[metadata_list[randint(0, index) % metadata_len]] = {}
            path_query_list.append(PathQuery(index, randint(0, k), index+1, randint(0, k),
                                             path_query_where, randint(1, path_query_cnt), path_query_return,
                                             category[randint(0, 1)]))

        query_list_dict[query_cnt] = node_query_list + path_query_list

    for k in xrange(20, 100, 2):
        fat_tree = FatTreeTopology(k=k)
        router_cnt = 5 * k * k / 4

        optimize_probe_pkt_list = optimize_generate_probe_set(query_list_dict[1], fat_tree, k_fwd, k_tele)
        optimize_probe_cnt_1 = 0
        for probe_type in ['performance', 'failure']:
            probe_set_dict = optimize_probe_pkt_list[probe_type]
            for freq, probe_set in probe_set_dict.iteritems():
                optimize_probe_cnt_1 += len(probe_set)

        optimize_probe_pkt_list = optimize_generate_probe_set(query_list_dict[10], fat_tree, k_fwd, k_tele)
        optimize_probe_cnt_10 = 0
        for probe_type in ['performance', 'failure']:
            probe_set_dict = optimize_probe_pkt_list[probe_type]
            for freq, probe_set in probe_set_dict.iteritems():
                optimize_probe_cnt_10 += len(probe_set)

        optimize_probe_pkt_list = optimize_generate_probe_set(query_list_dict[100], fat_tree, k_fwd, k_tele)
        optimize_probe_cnt_100 = 0
        for probe_type in ['performance', 'failure']:
            probe_set_dict = optimize_probe_pkt_list[probe_type]
            for freq, probe_set in probe_set_dict.iteritems():
                optimize_probe_cnt_100 += len(probe_set)

        host_cnt = (k ** 3) / 4
        mesh_probe_cnt = int(host_cnt * (host_cnt - 1) / 20.0)

        print k, router_cnt, optimize_probe_cnt_1, optimize_probe_cnt_10, optimize_probe_cnt_100, mesh_probe_cnt
        f.write('{} {} {} {} {} {}\n'.format(k, router_cnt, optimize_probe_cnt_1, optimize_probe_cnt_10, optimize_probe_cnt_100, mesh_probe_cnt))
    f.close()
