# -*- coding: utf-8 -*-

from metadatas.primary_metadata import EgressMetadata

class EgressPort(EgressMetadata):
    def __init__(self, bit_width):
        super(EgressPort, self).__init__(bit_width)


class EgressTimestamp(EgressMetadata):
    def __init__(self, bit_width):
        super(EgressTimestamp, self).__init__(bit_width)


class EgressPacketCount(EgressMetadata):
    def __init__(self, bit_width):
        super(EgressPacketCount, self).__init__(bit_width)


class EgressByteCount(EgressMetadata):
    def __init__(self, bit_width):
        super(EgressByteCount, self).__init__(bit_width)
        

class EgressDropCount(EgressMetadata):
    def __init__(self, bit_width):
        super(EgressDropCount, self).__init__(bit_width)


class EgressUtilization(EgressMetadata):
    def __init__(self, bit_width):
        super(EgressUtilization, self).__init__(bit_width)
