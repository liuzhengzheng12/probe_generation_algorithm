# -*- coding: utf-8 -*-
import networkx as nx
import math
from query_primitives.query import PathQuery, NodeQuery


def generate_probe_set(query_list, topo_class, k_fwd, k_tele):
    probe_list = []
    topology = topo_class.get_topology()
    for query in query_list:
        probe_set = set()
        primary_metadata_set = query.decompose()
        if isinstance(query, NodeQuery):
            for fwd_path in query.get_fwd_path(topo_class):
                print fwd_path
                probe_set.add((tuple(fwd_path), (query.node,)))
        if isinstance(query, PathQuery):
            for tmy_path in query.get_tmy_path(topo_class):
                #print tmy_path
                probe_cnt = int(math.ceil(len(tmy_path)*1.0/k_tele))
                #print probe_cnt
                for i in xrange(probe_cnt):
                    start = i*k_tele
                    final = min(start + k_tele, len(tmy_path)-1)
                    fwd_path = nx.shortest_path(topology, 0, tmy_path[start])
                    fwd_path.extend(tmy_path[start+1:final])
                    if start == final:
                        fwd_path.pop()
                    fwd_path.extend(nx.shortest_path(topology, tmy_path[final], 0))
                    #print fwd_path
                    probe_set.add((tuple(fwd_path), tuple(tmy_path[start+1:final])))
        probe_list.append((probe_set, primary_metadata_set))
