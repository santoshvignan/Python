import re
import requests
import time

bfd = open("/home/vignan/RASHv1Jul13.txt","r")
com_bfd_flaps = open("/home/vignan/com_bfd_flaps_RASHv1Jul13.txt","w")

API_ENDPOINT ="https://tools.keycdn.com/geo.json?host="

dest_ip_list = []
for line in bfd.readlines():
    #print (line)
    for i in line.split():
        b = re.search(r"^dst-ip",i)
        if b:
            c = (i.split(':')[1])
            dest_ip_list.append(c)

bfd.seek(0)
print(dest_ip_list)
dict_dest_ip_list = dict.fromkeys(dest_ip_list)

comcast_ip_list = []

for ip in dict_dest_ip_list:

    URL = API_ENDPOINT + ip
    print ("Sending Request to " + URL)
    x = requests.get(URL)
    y = x.json()
    #print (y["data"]["geo"]["isp"])

    isp = y["data"]["geo"]["isp"]

    if isp == "CABLE-NET-1":
        comcast_ip_list.append(ip)
    time.sleep(5)

print (comcast_ip_list)
for ip in comcast_ip_list:
    for line in bfd.readlines():
        for i in line.split():
            b = re.search(r"^dst-ip",i)
            if b:
                c = i.split(':')[1]
                if ip == c:
                    com_bfd_flaps.writelines(line)
    bfd.seek(0)

bfd.close()
com_bfd_flaps.close()

