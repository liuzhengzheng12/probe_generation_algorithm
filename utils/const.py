# -*- coding: utf-8 -*-

# port of forward and telemetry
PORT_FWD = 0xffff
PORT_TMY = 0xfffe

# bitmap bias of primary metadata
bitmap_bias = {
    'state': 0,
    'ingress_port': 1,
    'ingress_tstamp': 2,
    'ingress_pkt_cnt': 3,
    'ingress_byte_cnt': 4,
    'ingress_drop_cnt': 5,
    'egress_port': 6,
    'egress_tstamp': 7,
    'egress_pkt_cnt': 8,
    'egress_byte_cnt': 9,
    'egress_drop_cnt': 10,
    'enq_tstamp': 11,
    'enq_qdepth': 12,
    'hop_latency': 13,
    'q_occupancy': 14,
    'pkt_len': 15,
    'inst_type': 16
}


# derived metadata map to primary metadata
derived_map_primary = {
    # Path-level Metadata
    'path_length': [],
    'path_trace': ['ingress_port', 'egress_port'],
    'path_rtt': ['ingress_tstamp', 'egress_tstamp'],
    'path_throughput': ['ingress_pkt_cnt', 'egress_pkt_cnt'],
    # Node-level Metadata
    'switch_workload': ['ingress_pkt_cnt', 'egress_pkt_cnt'],
    'switch_forward_packet_cnt': ['egress_pkt_cnt'],
    'switch_drop_packet_cnt': ['ingress_drop_cnt', 'egress_drop_cnt'],
    'alive_port_cnt': ['ingress_port', 'egress_port']
}

metadata_list = [
    'state',
    'ingress_port',
    'ingress_tstamp',
    'ingress_pkt_cnt',
    'ingress_byte_cnt',
    'ingress_drop_cnt',
    'egress_port',
    'egress_tstamp',
    'egress_pkt_cnt',
    'egress_byte_cnt',
    'egress_drop_cnt',
    'enq_tstamp',
    'enq_qdepth',
    'hop_latency',
    'q_occupancy',
    'pkt_len',
    'inst_type',
    'path_length',
    'path_trace',
    'path_rtt',
    'path_throughput',
    'switch_workload',
    'switch_forward_packet_cnt',
    'switch_drop_packet_cnt',
    'alive_port_cnt'
]
