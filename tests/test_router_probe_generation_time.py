# -*- coding: utf-8 -*-
from topology.fat_tree import FatTreeTopology
from optimize_algorithm.generate_probe import classify_queries, generate_derived_metadata_set, generate_primary_metadata_set, generate_probe
from query_primitives.query import PathQuery, NodeQuery
from utils.const import metadata_list
from random import randint
from time import time


def get_query_list(k, port_range):
    node_query_list = []
    path_query_list = []
    for index in xrange(500):
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
    metadata_len = len(metadata_list)
    category = ['performance', 'failure']
    f = open('testsdata/fig4_router_probe_generation_time.txt', 'w')

    for k in xrange(4, 102, 2):
        fat_tree = FatTreeTopology(k=k)
        router_cnt = 5 * k * k / 4
        if k <= 20:
            query_list = get_query_list(k / 2 - 1, router_cnt - 1)

        time_start = time()
        all_query_cluster_list = classify_queries(query_list)
        time_end = time()
        step1_time = int((time_end - time_start) * 1000000)

        time_start = time()
        all_query_cluster_primary_metadata_list = generate_primary_metadata_set(
            generate_derived_metadata_set(all_query_cluster_list, fat_tree))
        time_end = time()
        step2_time = int((time_end - time_start) * 1000000)

        time_start = time()
        optimize_probe_pkt_list = generate_probe(all_query_cluster_primary_metadata_list, fat_tree, k_fwd, k_tele)
        time_end = time()
        step3_time = int((time_end - time_start) * 1000000)

        optimize_probe_cnt = 0
        # print optimize_probe_pkt_list
        for probe_type in ['performance', 'failure']:
            probe_set_dict = optimize_probe_pkt_list[probe_type]
            for freq, probe_set in probe_set_dict.iteritems():
                optimize_probe_cnt += len(probe_set)

        print k, router_cnt, step1_time, step2_time, step3_time
        f.write('{} {} {} {} {}\n'.format(k, router_cnt, step1_time, step2_time, step3_time))
    f.close()
