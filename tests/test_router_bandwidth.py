# -*- coding: utf-8 -*-
from topology.fat_tree import FatTreeTopology
from optimize_algorithm.generate_probe import optimize_generate_probe_set
from query_primitives.query import PathQuery, NodeQuery
from utils.const import metadata_list
from random import randint


# 计算100,500,1000Hz下的500个query
def get_query_list_dict(port_range, router_range):
    query_list_dict = {100: [], 500: [], 1000: []}
    for index in xrange(250):
        node_query_where = {}
        node_query_return = {}
        for _ in xrange(index):
            node_query_where[metadata_list[randint(0, index) % metadata_len]] = {}
            node_query_return[metadata_list[randint(0, index) % metadata_len]] = {}
        node = randint(0, router_range)
        port = randint(0, port_range)
        cat = category[randint(0, 1)]
        query_list_dict[100].append(NodeQuery(node, port, node_query_where, 100, node_query_return, cat))
        query_list_dict[500].append(NodeQuery(node, port, node_query_where, 500, node_query_return, cat))
        query_list_dict[1000].append(NodeQuery(node, port, node_query_where, 1000, node_query_return, cat))

        path_query_where = {}
        path_query_return = {}
        for _ in xrange(index):
            path_query_where[metadata_list[randint(0, index) % metadata_len]] = {}
            path_query_return[metadata_list[randint(0, index) % metadata_len]] = {}
        src_node = randint(0, router_range)
        src_port = randint(0, port_range)
        dst_node = randint(0, router_range)
        dst_port = randint(0, port_range)
        cat = category[randint(0, 1)]
        query_list_dict[100].append(PathQuery(src_node, src_port, dst_node, dst_port,
                                              path_query_where, 100, path_query_return,
                                              cat))
        query_list_dict[500].append(PathQuery(src_node, src_port, dst_node, dst_port,
                                              path_query_where, 500, path_query_return,
                                              cat))
        query_list_dict[1000].append(PathQuery(src_node, src_port, dst_node, dst_port,
                                               path_query_where, 1000, path_query_return,
                                               cat))

    return query_list_dict


if __name__ == '__main__':
    k_fwd = 100
    k_tele = 10
    metadata_len = len(metadata_list)
    category = ['performance', 'failure']
    f = open('testsdata/fig_router_bandwidth.txt', 'w')

    for k in xrange(4, 100, 2):
        fat_tree = FatTreeTopology(k=k)
        router_cnt = 5 * k * k / 4
        query_list_dict = get_query_list_dict(k / 2 - 1, router_cnt - 1)

        optimize_probe_pkt_list = optimize_generate_probe_set(query_list_dict[100], fat_tree, k_fwd, k_tele)
        bandwidth_100 = 0
        for probe_type in ['performance', 'failure']:
            probe_set_dict = optimize_probe_pkt_list[probe_type]
            for freq, probe_set in probe_set_dict.iteritems():
                for probe in probe_set:
                    bandwidth_100 += len(probe)
        bandwidth_100 *= 100
        bandwidth_100 /= 1000000.0

        optimize_probe_pkt_list = optimize_generate_probe_set(query_list_dict[500], fat_tree, k_fwd, k_tele)
        bandwidth_500 = 0
        for probe_type in ['performance', 'failure']:
            probe_set_dict = optimize_probe_pkt_list[probe_type]
            for freq, probe_set in probe_set_dict.iteritems():
                for probe in probe_set:
                    bandwidth_500 += len(probe)
        bandwidth_500 *= 500
        bandwidth_500 /= 1000000.0

        optimize_probe_pkt_list = optimize_generate_probe_set(query_list_dict[1000], fat_tree, k_fwd, k_tele)
        bandwidth_1000 = 0
        for probe_type in ['performance', 'failure']:
            probe_set_dict = optimize_probe_pkt_list[probe_type]
            for freq, probe_set in probe_set_dict.iteritems():
                for probe in probe_set:
                    bandwidth_1000 += len(probe)
        bandwidth_1000 *= 1000
        bandwidth_1000 /= 1000000.0

        print k, router_cnt, bandwidth_100, bandwidth_500, bandwidth_1000

        f.write('{} {} {} {} {} \n'.format(k, router_cnt, bandwidth_100, bandwidth_500, bandwidth_1000))
    f.close()
