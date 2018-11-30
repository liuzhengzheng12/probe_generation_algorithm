# -*- coding: utf-8 -*-

from metadatas.metadata import Metadata


class DerivedMetadata(Metadata):
    """
    DerivedMetadata Base Class
    """
    def __init__(self):
        super(DerivedMetadata, self).__init__()


class PathLevelMetadata(DerivedMetadata):
    """
    PathLevelMetadata Base Class
    """
    def __init__(self):
        super(PathLevelMetadata, self).__init__()


class NodeLevelMetadata(DerivedMetadata):
    """
    NodeLevelMetadata Base Class
    """
    def __init__(self):
        super(NodeLevelMetadata, self).__init__()


class ProbeLevelMetadata(DerivedMetadata):
    """
    PathLevelMetadata Base Class
    """
    def __init__(self):
        super(ProbeLevelMetadata, self).__init__()
