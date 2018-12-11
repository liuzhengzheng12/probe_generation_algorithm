# -*- coding: utf-8 -*-

import networkx as nx
from copy import deepcopy
from utils.utils import transform_to_primary_metadata


class Query(object):
    """
    Query Base Class
    """
    def __init__(self, where, period, return_metadata, query_type):
        self.where = where
        self.period = period
        self.return_metadata = return_metadata
        self.query_type = query_type
        self.all_metadatas = deepcopy(where)
        self.all_metadatas.update(return_metadata)

    def decompose_derived_metadata(self):
        return set(self.all_metadatas)

    def decompose(self):
        primary_metadata_list = []
        for metadata in self.all_metadatas:
            primary_metadata_list.extend(transform_to_primary_metadata(metadata))
        return set(primary_metadata_list)

    def get_freq(self):
        return 1.0/self.period


class PathQuery(Query):
    def __init__(self, src_node, src_port, dst_node, dst_port, where, period, return_metadata, query_type):
        super(PathQuery, self).__init__(where, period, return_metadata, query_type)
        self.src_node = src_node
        self.src_port = src_port
        self.dst_node = dst_node
        self.dst_port = dst_port

    def get_tmy_path(self, topo_class):
        topology = topo_class.get_topology()

        if 'PathTrace' in self.where:
            path = []
            path_trace_list = self.where['PathTrace']
            for i, (node, port) in enumerate(path_trace_list):
                if i % 2 == 0:
                    path.append(node)
            yield path
        else:
            src = topo_class.get_sort_adjs(self.src_node)[self.src_port]
            dst = topo_class.get_sort_adjs(self.dst_node)[self.dst_port]
            path = nx.shortest_path(topology, src, dst)
            path.append(self.dst_node)
            path.insert(0, self.src_node)
            yield path


class NodeQuery(Query):
    def __init__(self, node, port, where, period, return_metadata, query_type):
        super(NodeQuery, self).__init__(where, period, return_metadata, query_type)
        self.node = node
        self.port = port
        self.ingress = False
        self.egress = False

    def get_fwd_path(self, topo_class):
        self.calc_direction()
        topology = topo_class.get_topology()

        if 'PathTrace' in self.where:
            path = []
            path_trace_list = self.where['PathTrace']
            for i, (node, port) in enumerate(path_trace_list):
                if i % 2 == 0:
                    path.append(node)
            yield path
        else:
            if self.ingress:
                src_node = topo_class.get_sort_adjs(self.node)[self.port]
                path = nx.shortest_path(topology, 0, src_node)
                path.extend(nx.shortest_path(topology, self.node, 0))
                yield path
            if self.egress:
                dst_node = topo_class.get_sort_adjs(self.node)[self.port]
                path = nx.shortest_path(topology, 0, self.node)
                path.extend(nx.shortest_path(topology, dst_node, 0))
                yield path

    def calc_direction(self):
        for metadata in self.all_metadatas:
            if metadata.startswith('ingress'):
                self.ingress = True
            if metadata.startswith('egress'):
                self.egress = True
        if not (self.ingress and self.egress):
            self.ingress = True
            self.egress = True
