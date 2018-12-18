# -*- coding: utf-8 -*-
from topology.fat_tree import FatTreeTopology
from optimize_algorithm.generate_probe import optimize_generate_probe_set
from query_primitives.query import PathQuery, NodeQuery
from utils.const import metadata_list
from random import randint
from psutil import Process
from time import time

if __name__ == '__main__':
    p = Process()
    # print p.cmdline()
    k_fwd = 100
    k_tele = 10
    metadata_len = len(metadata_list)
    k = 5
    category = ['performance', 'failure']
    f = open('testsdata/fig_router_cpu_times.txt', 'w')

    query_list_dict = {10: [], 50: [], 100: []}

    node_query_list = []
    path_query_list = []
    for query_cnt in [10, 50, 100]:
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
            path_query_list.append(PathQuery(index, randint(0, k), index + 1, randint(0, k),
                                             path_query_where, randint(1, path_query_cnt), path_query_return,
                                             category[randint(0, 1)]))

        query_list_dict[query_cnt] = node_query_list + path_query_list

    for k in xrange(20, 100, 2):
        fat_tree = FatTreeTopology(k=k)
        router_cnt = 5 * k * k / 4

        start_user_cpu_times, start_sys_cpu_times, _, _ = p.cpu_times()
        optimize_generate_probe_set(query_list_dict[10], fat_tree, k_fwd, k_tele)
        end_user_cpu_times, end_sys_cpu_times, _, _ = p.cpu_times()
        cpu_times_10 = (end_user_cpu_times - start_user_cpu_times) + (end_sys_cpu_times - start_sys_cpu_times)

        start_user_cpu_times, start_sys_cpu_times, _, _ = p.cpu_times()
        optimize_generate_probe_set(query_list_dict[50], fat_tree, k_fwd, k_tele)
        end_user_cpu_times, end_sys_cpu_times, _, _ = p.cpu_times()
        cpu_times_50 = (end_user_cpu_times - start_user_cpu_times) + (end_sys_cpu_times - start_sys_cpu_times)

        start_user_cpu_times, start_sys_cpu_times, _, _ = p.cpu_times()
        start_time = time()
        optimize_generate_probe_set(query_list_dict[100], fat_tree, k_fwd, k_tele)
        end_time = time()
        end_user_cpu_times, end_sys_cpu_times, _, _ = p.cpu_times()
        cpu_times_100 = (end_user_cpu_times - start_user_cpu_times) + (end_sys_cpu_times - start_sys_cpu_times)

        print k, router_cnt, cpu_times_10, cpu_times_50, cpu_times_100, end_time - start_time
        f.write('{} {} {} {} {} \n'.format(k, router_cnt, cpu_times_10, cpu_times_50, cpu_times_100))
    f.close()
