# -*- coding: utf-8 -*-
derived_map_primary = {
    # Path-level Metadata
    'PathLength': [],
    'PathTrace': ['Ingress_port_id', 'Egress_port_id'],
    'PathRTT': ['Ingress_timestamp', 'Egress_timestamp'],
    'PathUtilization': ['Ingress_port_RX_utilization', 'Egress_port_TX_utilization'],
    'PathThroughput': ['Ingress_port_RX_pkt_count', 'Egress_port_TX_pkt_count'],
    # Node-level Metadata
    'SwitchWorkload': ['Ingress_port_RX_pkt_count', 'Egress_port_RX_pkt_count'],
    'SwitchForwardPacketCount': ['Egress_port_TX_pkt_count'],
    'SwitchDropPacketCount': ['Ingress_port_RX_drop_count', 'Queue_drop_count', 'Egress_port_TX_drop_count'],
    'AlivePortCount': ['Ingress_port_id', 'Egress_port_id']
}


def transform_to_primary_metadata(metadata_name):
    if metadata_name in derived_map_primary:
        return derived_map_primary[metadata_name]
    else:
        return [metadata_name]
