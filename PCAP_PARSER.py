from scapy.all import rdpcap

tx_packets = rdpcap("/Users/vignan/Downloads/tx.pcap")
rx_packets = rdpcap("/Users/vignan/Downloads/rx.pcap")

count = 0

for tx_packet in tx_packets:
    for rx_packet in rx_packets:
        if tx_packet['IP'].id == rx_packet['IP'].id:
            count = count + 1
    if count > 1:
        print(tx_packet['IP'].id)
        count = 0
    else:
        count = 0