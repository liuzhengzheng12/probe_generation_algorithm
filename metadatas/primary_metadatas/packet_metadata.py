# -*- coding: utf-8 -*-

from metadatas.primary_metadata import PacketMetadata

class PacketLength(PacketMetadata):
    def __init__(self, bit_width):
        super(PacketLength, self).__init__(bit_width)


class InstanceType(PacketMetadata):
    def __init__(self, bit_width):
        super(InstanceType, self).__init__(bit_width)
