from scapy.all import rdpcap
from scapy.layers.netflow import netflowv9_defragment,_netflowv9_defragment_packet
import pyshark
pkt_list = pyshark.FileCapture("/Users/vignan/Downloads/t1.pcap")

print (pkt_list)
#print (pkt_list[0].show())
#for i in range(0,len(pkt_list)):
#    print(netflowv9_defragment(pkt_list[i]))
