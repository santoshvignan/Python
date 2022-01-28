from scapy.all import rdpcap
rx_pkts = rdpcap("/Users/vignan/Downloads/udp.pcap")
tx_pkts = rdpcap("/Users/vignan/Downloads/fec_tx.pcap")

print (len(tx_pkts))
print (len(rx_pkts))
count = 0
for i in range(0,len(tx_pkts)):
    for j in range(0,len(rx_pkts)):
        if tx_pkts[i]['IP'].src == rx_pkts[j]['IP'].src:
            #print (str(tx_pkts[i]['IP'].src) + " " + str(rx_pkts[j]['IP'].src))
            if tx_pkts[i]['IP'].id == rx_pkts[j]['IP'].id:
                #print(str(tx_pkts[i]['IP'].src) + " " + str(rx_pkts[j]['IP'].src))
                #print (str(tx_pkts[i]['IP'].id) + " " + str(rx_pkts[j]['IP'].id))
                count = count + 1

    if count == 1:
        print(str(tx_pkts[i]['IP'].src) + " " + str(tx_pkts[i]['IP'].id))
    if count > 1:
        #print (str(tx_pkts[i]['IP'].src) + " " + str(tx_pkts[i]['IP'].id))
        count = 0





