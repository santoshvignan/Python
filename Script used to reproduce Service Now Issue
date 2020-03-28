import telnetlib
import time
from netmiko import ConnectHandler
import random

ve2k1 = ConnectHandler(device_type='linux',host='29.29.29.33',username='admin',password='admin')
random_time_list = [55,30,49,20,37,62,19]

host='172.18.52.22'
PORT = '2011'
password = 'MANSANvig2908'
tn = telnetlib.Telnet(host,PORT)

time.sleep(2)
tn.write("\r".encode('ascii'))

password_prompt = tn.read_until(b'Password: ',timeout=2)
print (password_prompt.decode('ascii'))
tn.write((password + "\r").encode('ascii'))

router_prompt = tn.read_until(b'ASR-1001hX-underlay>',timeout=2)
print (router_prompt.decode('ascii'))

tn.write(('en' + '\r').encode('ascii'))
router_enable_prompt = tn.read_until(b'ASR-1001hX-underlay#',timeout=2)
print (router_enable_prompt.decode('ascii'))


tn.write(('term length 0' + '\r').encode('ascii'))
tn.read_until(b'ASR-1001hX-underlay#',timeout=2)
time.sleep(2)

tn.write(('config t' + '\r').encode('ascii'))
time.sleep(2)
down = 0
up = 0
for i in range(0,50000):

	random_downtime = random.choice(random_time_list)
	device_clock = ve2k1.send_command("show clock")
	tn.write(('no ip route 150.1.1.1 255.255.255.255 92.92.92.10' + '\r').encode('ascii'))
	tn.write(('no ip route 150.1.1.1 255.255.255.255 91.91.91.10' + '\r').encode('ascii'))
	down = down + 1
	print ("Iteration " + str(down) + "." + " Control is down. " + "Downtime Chosen is " + str(random_downtime) + ".")
	for downtime in range(0,random_downtime):
		#print (downtime)
		ip_route_output = ve2k1.send_command('show ip route summary protocol omp')
		vpn1_ip_route_output = ip_route_output[193:240].split()
		received_routes = int(vpn1_ip_route_output[3])
		installed_routes = int(vpn1_ip_route_output[4])
		time.sleep(1)
	if received_routes < 30005 or installed_routes < 30005:
		print ("The downtime selected for iteration " + str(down) + " was " + str(random_downtime) + ". Problem started at " + device_clock )
		print ("Received Routes = ", received_routes)
		print ("Installed Routes = ", installed_routes)
		break
	random_uptime = random.choice(random_time_list)
	tn.write(('ip route 150.1.1.1 255.255.255.255 92.92.92.10' + '\r').encode('ascii'))
	tn.write(('ip route 150.1.1.1 255.255.255.255 91.91.91.10' + '\r').encode('ascii'))
	up = up + 1
	print ("Iteration " + str(up) + "." + " Control is up. " + "Uptime Chosen is " + str(random_uptime) + ".")
	for uptime in range(0,random_uptime):
		#print (uptime)
		time.sleep(1)


tn.write(('exit' + '\r').encode('ascii'))
time.sleep(1)
tn.write(('exit' + '\r').encode('ascii'))
