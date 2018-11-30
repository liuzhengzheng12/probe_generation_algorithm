# -*- coding: utf-8 -*-

import networkx as nx
from topology.topology_base import TopologyBase


class FatTreeTopology(TopologyBase):

    def __init__(self, k=40):
        super(FatTreeTopology, self).__init__()
        self.k = k
        self.pods = k               # pod数量
        self.cores = (k/2)**2       # 核心层交换机总数
        self.pod_aggs = k/2         # 一个pod的聚合层交换机数
        self.pod_edges = k/2        # 一个pod的边缘层交换机数
        self.create_topology()

    def create_topology(self):
        aggs = self.pod_aggs * self.pods
        edges = self.pod_edges * self.pods
        for i in xrange(self.pods):
            edge_lo = i * self.pod_edges
            edge_hi = edge_lo + self.pod_edges
            agg_lo = edges + edge_lo
            agg_hi = edges + edge_hi
            # edge层连接agg层
            for edge in xrange(edge_lo, edge_hi):
                for agg in xrange(agg_lo, agg_hi):
                    self.topology.add_edge(edge, agg)
            # agg层连接core层
            for agg in xrange(agg_lo, agg_hi):
                j = (agg - edges) % (self.k/2)
                core_lo = edges + aggs + (self.k/2)*j
                core_hi = core_lo + self.k/2
                for core in xrange(core_lo, core_hi):
                    self.topology.add_edge(agg, core)

    def get_sort_adjs(self, v):
        sort_adjs = self.topology.adj[v].keys()
        sort_adjs.sort()
        return sort_adjs

    def get_topology(self):
        return self.topology
