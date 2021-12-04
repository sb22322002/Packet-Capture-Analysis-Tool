# Packet-Capture-Analysis-Tool
#
# The packet capture analysis tool will consist of three main phases
#### Packet Filtering: keep only the packets we want to analyze
#### Packet Parsing: read relevant packet fields into memory for processing
#### Compute Metrics: using packet fields to compute metrics
#
# Filters select ICMP packets out of packet captures containing ~8000 packets and collects across 4 nodes and computes 13 metrics from them
