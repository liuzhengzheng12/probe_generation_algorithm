# -*- coding: utf-8 -*-

from metadatas.primary_metadata import IngressMetadata

class IngressPort(IngressMetadata):
    def __init__(self, bit_width):
        super(IngressPort, self).__init__(bit_width)


class IngressTimestamp(IngressMetadata):
    def __init__(self, bit_width):
        super(IngressTimestamp, self).__init__(bit_width)


class IngressPacketCount(IngressMetadata):
    def __init__(self, bit_width):
        super(IngressPacketCount, self).__init__(bit_width)


class IngressByteCount(IngressMetadata):
    def __init__(self, bit_width):
        super(IngressByteCount, self).__init__(bit_width)
        

class IngressDropCount(IngressMetadata):
    def __init__(self, bit_width):
        super(IngressDropCount, self).__init__(bit_width)


class IngressUtilization(IngressMetadata):
    def __init__(self, bit_width):
        super(IngressUtilization, self).__init__(bit_width)
