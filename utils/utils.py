# -*- coding: utf-8 -*-
import math
from const import bitmap_bias, derived_map_primary


def transform_fwd_path_to_fwd_label_list(topo_class, fwd_path):
    fwd_label_list = []
    path_len = len(fwd_path)
    src_node = fwd_path[0]
    for i in xrange(1, path_len):
        fwd_label_list.append(topo_class.get_outport(src_node, fwd_path[i]))
        src_node = fwd_path[i]
    return fwd_label_list


def create_bitmap(primary_metadata_set):
    bitmap = 0
    for primary_metadata_name in primary_metadata_set:
        bitmap += 1 << bitmap_bias[primary_metadata_name]
    return bitmap


def transform_to_primary_metadata(metadata_name):
    if metadata_name in derived_map_primary:
        return derived_map_primary[metadata_name]
    else:
        return [metadata_name]


def get_freq_class(query_freq):
    exp = math.ceil(math.log(query_freq, 2.0))
    return 2 ** exp
