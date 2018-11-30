# -*- coding: utf-8 -*-

from metadatas.derived_metadata import PathLevelMetadata


class PathLength(PathLevelMetadata):
    def __init__(self):
        super(PathLength, self).__init__()


class PathTrace(PathLevelMetadata):
    def __init__(self):
        super(PathTrace, self).__init__()


class PathRTT(PathLevelMetadata):
    def __init__(self):
        super(PathRTT, self).__init__()


class PathUtilization(PathLevelMetadata):
    def __init__(self):
        super(PathUtilization, self).__init__()


class PathThroughput(PathLevelMetadata):
    def __init__(self):
        super(PathThroughput, self).__init__()
