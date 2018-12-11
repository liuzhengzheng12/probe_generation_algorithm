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


def generate_probe(all_query_cluster_primary_metadata_list, topo_class, k_fwd, k_tele):
    query_probe_list = {'performance': {}, 'failure': {}}
    topology = topo_class.get_topology()
    for category in ['performance', 'failure']:
        primary_metadata_set_list = all_query_cluster_primary_metadata_list[category]
        max_freq = max(primary_metadata_set_list.keys())
        max_freq_primary_metadata_dict = {}
        for primary_metadata_cluster in primary_metadata_set_list.values():
            for node, primary_metadata_set in primary_metadata_cluster.items():
                if node not in max_freq_primary_metadata_dict:
                    max_freq_primary_metadata_dict[node] = set()
                max_freq_primary_metadata_dict[node] |= primary_metadata_set
        probe_set = set()
        start_node = 0
        node_list = max_freq_primary_metadata_dict.keys()
        min_dist_len = 0x7fffffff
        min_path = None
        min_node = None
        for now_node in node_list:
            now_path = nx.shortest_path(topology, start_node, now_node)
            if len(now_path) < min_dist_len:
                min_node = now_node
                min_path = now_path
                min_dist_len = len(now_path)
        node_list.remove(min_node)
        before_fwd_path = nx.shortest_path(topology, min_node, 0)
        start_node = min_node
        fwd_path = min_path
        tmy_path = [min_node]
        if len(node_list) == 0:
            fwd_path.pop()
            fwd_path.extend(before_fwd_path)
            fwd_label_list = transform_fwd_path_to_fwd_label_list(topo_class, fwd_path)
            tmy_label_list = [(node, create_bitmap(max_freq_primary_metadata_dict[node])) for node in tmy_path]
            probe_pkt = assemble_probe(fwd_label_list, tmy_label_list)
            probe_set.add(probe_pkt)
        while node_list:
            min_dist_len = 0x7fffffff
            min_path = None
            min_node = None
            for now_node in node_list:
                now_path = nx.shortest_path(topology, start_node, now_node)
                if len(now_path) < min_dist_len:
                    min_node = now_node
                    min_path = now_path
                    min_dist_len = len(now_path)
            now_fwd_path = nx.shortest_path(topology, min_node, 0)
            node_list.remove(min_node)
            start_node = min_node
            if len(tmy_path) + min_dist_len - 1 > k_tele or \
               len(fwd_path) + min_dist_len - 2 + len(now_fwd_path) > k_fwd:
                fwd_path.pop()
                fwd_path.extend(before_fwd_path)
                print 'in fwd_path, ', fwd_path
                print 'in tmy_path, ', tmy_path
                fwd_label_list = transform_fwd_path_to_fwd_label_list(topo_class, fwd_path)
                tmy_label_list = [(node, create_bitmap(max_freq_primary_metadata_dict[node])) for node in tmy_path]
                probe_pkt = assemble_probe(fwd_label_list, tmy_label_list)
                probe_set.add(probe_pkt)
                fwd_path = nx.shortest_path(topology, 0, min_node)
                tmy_path = [min_node]
            else:
                fwd_path.pop()
                fwd_path.extend(min_path)
                tmy_path.pop()
                tmy_path.extend(min_path)
            if len(node_list) == 0:
                fwd_path.pop()
                fwd_path.extend(now_fwd_path)
                print 'in fwd_path, ', fwd_path
                print 'in tmy_path, ', tmy_path
                fwd_label_list = transform_fwd_path_to_fwd_label_list(topo_class, fwd_path)
                tmy_label_list = [(node, create_bitmap(max_freq_primary_metadata_dict[node])) for node in tmy_path]
                probe_pkt = assemble_probe(fwd_label_list, tmy_label_list)
                probe_set.add(probe_pkt)
            before_fwd_path = now_fwd_path
        query_probe_list[category][max_freq] = probe_set

    return query_probe_list


def generate_probe_set(query_list, topo_class, k_fwd, k_tele):
    all_query_cluster_list = classify_queries(query_list)
    all_query_cluster_derived_metadata_list = generate_derived_metadata_set(all_query_cluster_list, topo_class)
    all_query_cluster_primary_metadata_list = generate_primary_metadata_set(all_query_cluster_derived_metadata_list)
    probe_pkt_list = generate_probe(all_query_cluster_primary_metadata_list, topo_class, k_fwd, k_tele)

    return probe_pkt_list
