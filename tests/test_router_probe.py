# -*- coding: utf-8 -*-
from topology.fat_tree import FatTreeTopology
from optimize_algorithm.generate_probe import optimize_generate_probe_set
from query_primitives.query import PathQuery, NodeQuery
from utils.const import metadata_list
from random import randint
from copy import deepcopy


def get_query_list_dict(k, port_range):
    query_list_dict = {100: [], 500: [], 1000: []}
    node_query_list = []
    path_query_list = []
    for index in xrange(50):
        node_query_where = {}
        node_query_return = {}
        for _ in xrange(index):
            node_query_where[metadata_list[randint(0, index) % metadata_len]] = {}
            node_query_return[metadata_list[randint(0, index) % metadata_len]] = {}
        node_query_list.append(NodeQuery(randint(0, port_range), randint(0, k), node_query_where, randint(1, index + 1),
                                         node_query_return, category[randint(0, 1)]))
        path_query_where = {}
        path_query_return = {}
        for _ in xrange(index):
            path_query_where[metadata_list[randint(0, index) % metadata_len]] = {}
            path_query_return[metadata_list[randint(0, index) % metadata_len]] = {}
        path_query_list.append(PathQuery(randint(0, port_range), randint(0, k), randint(0, port_range), randint(0, k),
                                         path_query_where, randint(1, index + 1), path_query_return,
                                         category[randint(0, 1)]))
    query_list_dict[100] = node_query_list + path_query_list

    query_list_dict[500] = deepcopy(query_list_dict[100])
    for index in xrange(100, 300):
        node_query_where = {}
        node_query_return = {}
        for _ in xrange(index):
            node_query_where[metadata_list[randint(0, index) % metadata_len]] = {}
            node_query_return[metadata_list[randint(0, index) % metadata_len]] = {}
        query_list_dict[500].append(
            NodeQuery(randint(0, port_range), randint(0, k), node_query_where, randint(1, index),
                      node_query_return, category[randint(0, 1)]))
        path_query_where = {}
        path_query_return = {}
        for _ in xrange(index):
            path_query_where[metadata_list[randint(0, index) % metadata_len]] = {}
            path_query_return[metadata_list[randint(0, index) % metadata_len]] = {}
        query_list_dict[500].append(
            PathQuery(randint(0, port_range), randint(0, k), randint(0, port_range), randint(0, k),
                      path_query_where, randint(1, index), path_query_return,
                      category[randint(0, 1)]))

    query_list_dict[1000] = deepcopy(query_list_dict[500])
    for index in xrange(300, 550):
        node_query_where = {}
        node_query_return = {}
        for _ in xrange(index):
            node_query_where[metadata_list[randint(0, index) % metadata_len]] = {}
            node_query_return[metadata_list[randint(0, index) % metadata_len]] = {}
        query_list_dict[1000].append(
            NodeQuery(randint(0, port_range), randint(0, k), node_query_where, randint(1, index),
                      node_query_return, category[randint(0, 1)]))
        path_query_where = {}
        path_query_return = {}
        for _ in xrange(index):
            path_query_where[metadata_list[randint(0, index) % metadata_len]] = {}
            path_query_return[metadata_list[randint(0, index) % metadata_len]] = {}
        query_list_dict[1000].append(
            PathQuery(randint(0, port_range), randint(0, k), randint(0, port_range), randint(0, k),
                      path_query_where, randint(1, index), path_query_return,
                      category[randint(0, 1)]))

    return query_list_dict


if __name__ == '__main__':
    k_fwd = 20
    k_tele = 10
    metadata_len = len(metadata_list)
    category = ['performance', 'failure']
    f = open('testsdata/fig3_router_probe.txt', 'w')

    for k in xrange(4, 100, 2):
        fat_tree = FatTreeTopology(k=k)
        router_cnt = 5 * k * k / 4
        query_list_dict = get_query_list_dict(k/2-1, router_cnt-1)

        optimize_probe_pkt_list = optimize_generate_probe_set(query_list_dict[100], fat_tree, k_fwd, k_tele)
        optimize_probe_cnt_100 = 0
        for probe_type in ['performance', 'failure']:
            probe_set_dict = optimize_probe_pkt_list[probe_type]
            for freq, probe_set in probe_set_dict.iteritems():
                optimize_probe_cnt_100 += len(probe_set)

        optimize_probe_pkt_list = optimize_generate_probe_set(query_list_dict[500], fat_tree, k_fwd, k_tele)
        optimize_probe_cnt_500 = 0
        for probe_type in ['performance', 'failure']:
            probe_set_dict = optimize_probe_pkt_list[probe_type]
            for freq, probe_set in probe_set_dict.iteritems():
                optimize_probe_cnt_500 += len(probe_set)

        optimize_probe_pkt_list = optimize_generate_probe_set(query_list_dict[1000], fat_tree, k_fwd, k_tele)
        optimize_probe_cnt_1000 = 0
        for probe_type in ['performance', 'failure']:
            probe_set_dict = optimize_probe_pkt_list[probe_type]
            for freq, probe_set in probe_set_dict.iteritems():
                optimize_probe_cnt_1000 += len(probe_set)

        host_cnt = (k ** 3) / 4
        mesh_probe_cnt = int(host_cnt * (host_cnt - 1) / 20.0)

        print k, router_cnt, optimize_probe_cnt_100, optimize_probe_cnt_500, optimize_probe_cnt_1000, mesh_probe_cnt
        f.write('{} {} {} {} {} {}\n'.format(k, router_cnt, optimize_probe_cnt_100, optimize_probe_cnt_500, optimize_probe_cnt_1000, mesh_probe_cnt))
    f.close()
