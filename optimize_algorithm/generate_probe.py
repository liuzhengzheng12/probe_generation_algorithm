# -*- coding: utf-8 -*-
import networkx as nx
from utils.assemble_probe import assemble_probe
from utils.utils import get_freq_class, create_bitmap, transform_to_primary_metadata, transform_fwd_path_to_fwd_label_list
from query_primitives.query import NodeQuery, PathQuery


def classify_queries(query_list):
    all_query_cluster_list = {'performance': {}, 'failure': {}}
    for query in query_list:
        freq = query.get_freq()
        freq_class = get_freq_class(freq)
        if query.query_type in ['performance', 'failure']:
            if freq_class not in all_query_cluster_list[query.query_type]:
                all_query_cluster_list[query.query_type][freq_class] = []
            all_query_cluster_list[query.query_type][freq_class].append(query)

    return all_query_cluster_list


# 合并query cluster中的derived metadata
def generate_derived_metadata_set(all_query_cluster_list, topo_class):
    all_query_cluster_derived_metadata_list = {'performance': {}, 'failure': {}}
    for category in ['performance', 'failure']:
        query_cluster_list = all_query_cluster_list[category]
        query_cluster_derived_metadata_list = all_query_cluster_derived_metadata_list[category]
        for freq_class, query_cluster in query_cluster_list.items():
            query_cluster_derived_metadata_list[freq_class] = {}
            freq_derived_metadata = query_cluster_derived_metadata_list[freq_class]
            for query in query_cluster:
                derived_metadata_set = query.decompose_derived_metadata()
                # print derived_metadata_set
                if isinstance(query, NodeQuery):
                    if query.node not in freq_derived_metadata:
                        freq_derived_metadata[query.node] = set()
                    freq_derived_metadata[query.node] |= derived_metadata_set
                if isinstance(query, PathQuery):
                    node_set = set()
                    for path in query.get_tmy_path(topo_class):
                        node_set |= set(path)
                    for node in node_set:
                        if node not in freq_derived_metadata:
                            freq_derived_metadata[node] = set()
                        freq_derived_metadata[node] |= derived_metadata_set
    return all_query_cluster_derived_metadata_list


# 合并query cluster中的primary metadata
def generate_primary_metadata_set(all_query_cluster_derived_metadata_list):
    all_query_cluster_primary_metadata_list = {'performance': {}, 'failure': {}}
    for category in ['performance', 'failure']:
        query_cluster_list = all_query_cluster_derived_metadata_list[category]
        query_cluster_primary_metadata_list = all_query_cluster_primary_metadata_list[category]
        for freq_class, derived_metadata_cluster in query_cluster_list.items():
            query_cluster_primary_metadata_list[freq_class] = {}
            freq_primary_metadata = query_cluster_primary_metadata_list[freq_class]
            for node, derived_metadata_set in derived_metadata_cluster.items():
                freq_primary_metadata[node] = set()
                for derived_metadata in derived_metadata_set:
                    freq_primary_metadata[node] |= set(transform_to_primary_metadata(derived_metadata))
    return all_query_cluster_primary_metadata_list


def get_nearest_node(from_node, topology, node_list):
    min_dist = 0x7fffffff
    min_dist_path = None
    for now_node in node_list:
        now_dist_path = nx.shortest_path(topology, from_node, now_node)
        now_dist = len(now_dist_path)
        if now_dist < min_dist:
            min_dist = now_dist
            min_dist_path = now_dist_path
    return min_dist_path


def merge_path(path, pos_path):
    assert(path[-1] == pos_path[0])
    path.pop()
    path.extend(pos_path)
    return path


def generate_probe(all_query_cluster_primary_metadata_list, topo_class, k_fwd, k_tele):
    query_probe_list = {'performance': {}, 'failure': {}}
    topology = topo_class.get_topology()
    for category in ['performance', 'failure']:
        primary_metadata_set_list = all_query_cluster_primary_metadata_list[category]
        freq_list = primary_metadata_set_list.keys()
        freq_list.sort(reverse=True)
        if not freq_list:
            continue
        print category
        freq_len = len(freq_list)
        for i in xrange(freq_len):
            high_freq = freq_list[i]
            high_freq_node_list = primary_metadata_set_list[high_freq].keys()
            if len(high_freq_node_list) == 0:
                continue

            probe_set = set()
            from_node = 0
            whole_fwd_path = [0]
            while high_freq_node_list:
                min_dist_path = get_nearest_node(from_node, topology, high_freq_node_list)
                whole_fwd_path = merge_path(whole_fwd_path, min_dist_path)
                from_node = min_dist_path[-1]
                high_freq_node_list.remove(from_node)
            whole_fwd_path = merge_path(whole_fwd_path, nx.shortest_path(topology, from_node, 0))
            whole_tmy_info_dict = {}
            for fwd_node in whole_fwd_path:
                for j in xrange(i, freq_len):
                    low_freq = freq_list[j]
                    if fwd_node in primary_metadata_set_list[low_freq]:
                        if fwd_node not in whole_tmy_info_dict:
                            whole_tmy_info_dict[fwd_node] = set()
                        whole_tmy_info_dict[fwd_node] |= primary_metadata_set_list[low_freq][fwd_node]
                        primary_metadata_set_list[low_freq].pop(fwd_node)

            if whole_tmy_info_dict:
                from_node = 0
                before_fwd_path = None
                fwd_path = [0]
                tmy_path = []
                for node in whole_fwd_path:
                    path = nx.shortest_path(topology, from_node, node)
                    now_fwd_path = nx.shortest_path(topology, node, 0)
                    from_node = node
                    k_fwd_condition = len(fwd_path) + len(path) + len(now_fwd_path) - 2 <= k_fwd
                    if node in whole_tmy_info_dict:
                        is_tmy_node = 1
                    else:
                        is_tmy_node = 0
                    k_tele_condition = len(tmy_path) + is_tmy_node <= k_tele
                    if k_fwd_condition and k_tele_condition:
                        # print 'fwd_path, ', fwd_path
                        # print 'path, ', path
                        fwd_path = merge_path(fwd_path, path)
                        if node in whole_tmy_info_dict:
                            tmy_path.append(node)
                    else:
                        fwd_path = merge_path(fwd_path, before_fwd_path)
                        # print 'final fwd_path, ', fwd_path
                        # print 'final tmy_path, ', tmy_path
                        # for tmy_node in tmy_path:
                            # print 'node: ', tmy_node
                            # print whole_tmy_info_dict[tmy_node]
                        fwd_label_list = transform_fwd_path_to_fwd_label_list(topo_class, fwd_path)
                        tmy_label_list = [(tmy_node, create_bitmap(whole_tmy_info_dict[tmy_node])) for tmy_node in
                                          tmy_path]
                        probe_pkt = assemble_probe(fwd_label_list, tmy_label_list)
                        probe_set.add(probe_pkt)
                        fwd_path = nx.shortest_path(topology, 0, node)
                        tmy_path = [node] if node in whole_tmy_info_dict else []
                    before_fwd_path = now_fwd_path
                if tmy_path:
                    # print 'final fwd_path, ', fwd_path
                    # print 'final tmy_path, ', tmy_path
                    fwd_path = merge_path(fwd_path, nx.shortest_path(topology, tmy_path[-1], 0))
                    fwd_label_list = transform_fwd_path_to_fwd_label_list(topo_class, fwd_path)
                    tmy_label_list = [(tmy_node, create_bitmap(whole_tmy_info_dict[tmy_node])) for tmy_node in
                                      tmy_path]
                    probe_pkt = assemble_probe(fwd_label_list, tmy_label_list)
                    probe_set.add(probe_pkt)

    return query_probe_list


def generate_probe_set(query_list, topo_class, k_fwd, k_tele):
    all_query_cluster_list = classify_queries(query_list)
    all_query_cluster_derived_metadata_list = generate_derived_metadata_set(all_query_cluster_list, topo_class)
    all_query_cluster_primary_metadata_list = generate_primary_metadata_set(all_query_cluster_derived_metadata_list)
    print all_query_cluster_primary_metadata_list
    probe_pkt_list = generate_probe(all_query_cluster_primary_metadata_list, topo_class, k_fwd, k_tele)

    return probe_pkt_list
