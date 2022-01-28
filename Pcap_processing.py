from scapy.all import rdpcap
import sys

rx_pkts = rdpcap("/Users/vignan/Downloads/fec_rx_2_1.pcap")
tx_pkts = rdpcap("/Users/vignan/Downloads/fex_tx_2_2.pcap")

print ("Number of packets transmitted: %s" % str(len(tx_pkts)))
print ("Number of packets received: %s" % str(len(rx_pkts)))

#count = 0

for i in range(0,len(rx_pkts)):
    pkt_present = False
    for j in range(0,len(tx_pkts)):
        if rx_pkts[i].dport == tx_pkts[j].dport and rx_pkts[i].sport == tx_pkts[j].sport and rx_pkts[i]['IP'].id == tx_pkts[j]['IP'].id:
            pkt_present = True
            print ("Processed packet %s" % str(i))

            
    if pkt_present==False:
        #print ("Count is: %s" % str(count))
        print (rx_pkts[i].show())
        print (str(rx_pkts[i]['IP'].src) + "," + str(rx_pkts[i]['IP'].dst) + "," + str(rx_pkts[i]['IP'].id) + "," + str(rx_pkts[i].sport) + "," + str(rx_pkts[i].dport))
    #count = 0





















