# -*- coding: utf-8 -*-

from metadatas.primary_metadata import BufferMetadata

class EnqTimestamp(BufferMetadata):
    def __init__(self, bit_width):
        super(EnqTimestamp, self).__init__(bit_width)


class EnqDepth(BufferMetadata):
    def __init__(self, bit_width):
        super(EnqDepth, self).__init__(bit_width)


class HopLatency(BufferMetadata):
    def __init__(self, bit_width):
        super(HopLatency, self).__init__(bit_width)


class QueueOccupancy(BufferMetadata):
    def __init__(self, bit_width):
        super(QueueOccupancy, self).__init__(bit_width)
