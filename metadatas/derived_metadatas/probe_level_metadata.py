# -*- coding: utf-8 -*-

from metadatas.derived_metadata import ProbeLevelMetadata

class SendProbeCount(ProbeLevelMetadata):
    def __init__(self):
        super(SendProbeCount, self).__init__()


class SendProbeTimestamp(ProbeLevelMetadata):
    def __init__(self):
        super(SendProbeTimestamp, self).__init__()


class ReceiveProbeCount(ProbeLevelMetadata):
    def __init__(self):
        super(ReceiveProbeCount, self).__init__()


class ReceiveProbeTimestamp(ProbeLevelMetadata):
    def __init__(self):
        super(ReceiveProbeTimestamp, self).__init__()
