# -*- coding: utf-8 -*-

from metadatas.derived_metadata import NodeLevelMetadata

class SwitchWorkload(NodeLevelMetadata):
    def __init__(self):
        super(SwitchWorkload, self).__init__()


class SwitchForwardPacketCount(NodeLevelMetadata):
    def __init__(self):
        super(SwitchForwardPacketCount, self).__init__()


class SwitchDropPacketCount(NodeLevelMetadata):
    def __init__(self):
        super(SwitchDropPacketCount, self).__init__()


class AlivePortCount(NodeLevelMetadata):
    def __init__(self):
        super(AlivePortCount, self).__init__()
