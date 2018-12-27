# -*- coding: utf-8 -*-
from topology.fat_tree import FatTreeTopology
from optimize_algorithm.generate_probe import optimize_generate_probe_set
from query_primitives.query import PathQuery, NodeQuery
from utils.const import metadata_list
from random import randint
from psutil import Process


def get_query_list(k, port_range):
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
    query_list = node_query_list + path_query_list
    return query_list


if __name__ == '__main__':
    k_fwd = 100
    k_tele = 10
    p = Process()
    metadata_len = len(metadata_list)
    category = ['performance', 'failure']
    f = open('testsdata/fig_router_memory_100.txt', 'w')
    M_bytes = 2 ** 20.0

    for k in xrange(4, 100, 2):
        fat_tree = FatTreeTopology(k=k)
        router_cnt = 5 * k * k / 4
        query_list = get_query_list(k / 2 - 1, router_cnt - 1)

        optimize_probe_pkt_list = optimize_generate_probe_set(query_list, fat_tree, k_fwd, k_tele)
        memory = p.memory_info()[0] / M_bytes

        print '{} {} {}'.format(k, router_cnt, memory)

        f.write('{} {} {} \n'.format(k, router_cnt, memory))
    f.close()
