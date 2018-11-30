# -*- coding: utf-8 -*-

import networkx as nx


class TopologyBase(object):

    def __init__(self):
        self.topology = nx.Graph()

    def create_topology(self):
        raise NotImplementedError
