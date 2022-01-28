import subprocess
import paramiko
import time
import csv

unreachableips = open("/Users/vignan/Downloads/ip_not_in_use.csv",'w',newline='')
ip_not_in_use_csv = csv.writer(unreachableips, delimiter='.')
all_routers = []
ip_not_in_use = []
for i in range(2,5):
    ip_to_ping = "29.29.28."+str(i)
    print ("Pinging IP: %s" % ip_to_ping)
    icmp = subprocess.run(["ping","-c","5",ip_to_ping],shell=False,capture_output=True)
    if icmp.returncode == 0:
        #print (icmp.stdout.decode('utf-8'))
        #print (icmp.returncode)
        icmp_str = icmp.stdout.decode('utf-8')
        print (icmp_str.split('\n'))
        all_routers.append(ip_to_ping)

    else:
        print ("%s is not reachable" %ip_to_ping)
        ip_not_in_use.append(ip_to_ping)




print ("Devices reachable: %s" %all_routers)
print ("IP addresses not in use are: %s" %ip_not_in_use)
for i in ip_not_in_use:
    ip_not_in_use_csv.writerow(i)

unreachableips.close()

#if len(all_routers) > 0:
#    for device in all_routers:
#        try:
#            ssh_to_device = paramiko.SSHClient()
#            ssh_to_device.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#            ssh_to_device.connect(hostname=device,username='admin',password='admin')
#
#        #login_device = ssh_to_device.invoke_shell()
#        #time.sleep(3)
#        #
#        #login_device.send("show run | host-name")
#        #host_name = login_device.recv(10000)
#        #
#        #print (host_name)