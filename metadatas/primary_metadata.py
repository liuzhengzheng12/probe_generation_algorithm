# -*- coding: utf-8 -*-

from metadatas.metadata import Metadata

class PrimaryMetadata(Metadata):
    '''
    PrimaryMetadata Base Class
    '''
    def __init__(self, bit_width):
        super(PrimaryMetadata, self).__init__()
        self._bit_width = bit_width
    
    @property
    def bit_width(self):
        return self._bit_width

    @bit_width.setter
    def bit_width(self, bit_width):
        self._bit_width = bit_width


class SwitchMetadata(PrimaryMetadata):
    '''
    SwitchMetadata Base Class
    '''
    def __init__(self, bit_width):
        super(SwitchMetadata, self).__init__(bit_width)


class IngressMetadata(PrimaryMetadata):
    '''
    IngressMetadata Base Class
    '''
    def __init__(self, bit_width):
        super(IngressMetadata, self).__init__(bit_width)


class EgressMetadata(PrimaryMetadata):
    '''
    EgressMetadata Base Class
    '''
    def __init__(self, bit_width):
        super(EgressMetadata, self).__init__(bit_width)


class BufferMetadata(PrimaryMetadata):
    '''
    BufferMetadata Base Class
    '''
    def __init__(self, bit_width):
        super(BufferMetadata, self).__init__(bit_width)


class PacketMetadata(PrimaryMetadata):
    '''
    PacketMetadata Base Class
    '''
    def __init__(self, bit_width):
        super(PacketMetadata, self).__init__(bit_width)
