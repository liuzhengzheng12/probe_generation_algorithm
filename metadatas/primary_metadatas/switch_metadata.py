# -*- coding: utf-8 -*-

from metadatas.primary_metadata import SwitchMetadata

class SwitchId(SwitchMetadata):
    def __init__(self, bit_width):
        super(SwitchId, self).__init__(bit_width)


class ControlPlaneStateVersion(SwitchMetadata):
    def __init__(self, bit_width):
        super(ControlPlaneStateVersion, self).__init__(bit_width)
