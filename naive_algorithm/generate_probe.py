# -*- coding: utf-8 -*-
import networkx as nx

from query_primitives.query import PathQuery, NodeQuery
from utils.assemble_probe import assemble_probe
from utils.utils import transform_fwd_path_to_fwd_label_list, create_bitmap


def generate_probe_set(query_list, topo_class, k_fwd, k_tele):
    query_probe_list = []
    topology = topo_class.get_topology()
    for query in query_list:
        probe_set = set()
        primary_metadata_set = query.decompose()
        bitmap = create_bitmap(primary_metadata_set)
        # NodeQuery时
        if isinstance(query, NodeQuery):
            for fwd_path in query.get_fwd_path(topo_class):
                fwd_label_list = transform_fwd_path_to_fwd_label_list(topo_class, fwd_path)
                tmy_label_list = [(query.node, bitmap)]
                probe_pkt = assemble_probe(fwd_label_list, tmy_label_list)
                probe_set.add(probe_pkt)
        # PathQuery时
        if isinstance(query, PathQuery):
            for tmy_path in query.get_tmy_path(topo_class):
                src_node = tmy_path[0]
                tmy_path_len = len(tmy_path)
                pre_fwd_path = nx.shortest_path(topology, 0, src_node)
                mid_fwd_path = [src_node]
                before_pos_fwd_path = nx.shortest_path(topology, src_node, 0)
                for i in xrange(1, tmy_path_len):
                    mid_fwd_path.append(tmy_path[i])
                    now_pos_fwd_path = nx.shortest_path(topology, tmy_path[i], 0)
                    if len(mid_fwd_path) > k_tele or len(pre_fwd_path) + len(mid_fwd_path) + len(now_pos_fwd_path) - 2 > k_fwd:
                        pre_fwd_path.pop()
                        src_node = mid_fwd_path.pop()
                        before_pos_fwd_path.pop(0)
                        full_fwd_path = []
                        full_fwd_path.extend(pre_fwd_path)
                        full_fwd_path.extend(mid_fwd_path)
                        full_fwd_path.extend(before_pos_fwd_path)
                        print full_fwd_path
                        fwd_label_list = transform_fwd_path_to_fwd_label_list(topo_class, full_fwd_path)
                        tmy_label_list = [(node, bitmap) for node in mid_fwd_path]
                        probe_pkt = assemble_probe(fwd_label_list, tmy_label_list)
                        probe_set.add(probe_pkt)
                        mid_fwd_path = [src_node]
                        pre_fwd_path = nx.shortest_path(topology, 0, src_node)
                    before_pos_fwd_path = now_pos_fwd_path
            if mid_fwd_path:
                pre_fwd_path.pop()
                before_pos_fwd_path.pop(0)
                full_fwd_path = []
                full_fwd_path.extend(pre_fwd_path)
                full_fwd_path.extend(mid_fwd_path)
                full_fwd_path.extend(before_pos_fwd_path)
                print full_fwd_path
                fwd_label_list = transform_fwd_path_to_fwd_label_list(topo_class, full_fwd_path)
                tmy_label_list = [(node, bitmap) for node in mid_fwd_path]
                probe_pkt = assemble_probe(fwd_label_list, tmy_label_list)
                probe_set.add(probe_pkt)
        query_probe_list.append(probe_set)
    return query_probe_list
