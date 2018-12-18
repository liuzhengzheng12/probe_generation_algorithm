# -*- coding: utf-8 -*-
from topology.fat_tree import FatTreeTopology
from naive_algorithm.generate_probe import naive_generate_probe_set
from query_primitives.query import PathQuery, NodeQuery
from utils.const import metadata_list
from random import randint
from time import time

if __name__ == '__main__':
    k_fwd = 100
    k_tele = 10
    fat_tree = FatTreeTopology()
    metadata_len = len(metadata_list)
    k = 5
    category = ['performance', 'failure']
    f = open('testsdata/fig6a_query_update_time_least.txt', 'w')

    node_query_list = []
    path_query_list = []
    for query_cnt in xrange(10, 20, 10):
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

    node_query_update_list = []
    path_query_update_list = []
    for query_update_cnt in xrange(10, 1000, 10):
        node_query_update_cnt = query_update_cnt / 2
        for index in xrange(node_query_update_cnt-5, node_query_update_cnt):
            node_query_where = {}
            node_query_return = {}
            for _ in xrange(index):
                node_query_where[metadata_list[randint(0, index) % metadata_len]] = {}
                node_query_return[metadata_list[randint(0, index) % metadata_len]] = {}
            node_query_update_list.append(NodeQuery(index, randint(0, k), node_query_where, randint(1, node_query_update_cnt),
                                             node_query_return, category[randint(0, 1)]))

        path_query_update_cnt = query_update_cnt / 2
        for index in xrange(path_query_update_cnt-5, path_query_update_cnt):
            path_query_where = {}
            path_query_return = {}
            for _ in xrange(index):
                path_query_where[metadata_list[randint(0, index) % metadata_len]] = {}
                path_query_return[metadata_list[randint(0, index) % metadata_len]] = {}
            path_query_update_list.append(PathQuery(index, randint(0, k), index + 1, randint(0, k),
                                             path_query_where, randint(1, path_query_update_cnt), path_query_return,
                                             category[randint(0, 1)]))
        add_query_list = node_query_update_list + path_query_update_list

        time_start = time()
        all_query_cluster_list = naive_generate_probe_set(add_query_list, fat_tree, k_fwd, k_tele)
        time_end = time()
        query_add_time = int((time_end - time_start) * 1000000)

        print query_update_cnt, query_add_time, 0
        f.write('{} {} {} \n'.format(query_update_cnt, query_add_time, 0))
    f.close()
