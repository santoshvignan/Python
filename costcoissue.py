from netmiko import ConnectHandler
import sys
import time

vEdge1k_rtr2 = {'device_type':'linux',
                'host':'29.29.29.20',
                'username':'admin',
                'password':'admin'
               }

vEdge1k_rtr1 = {'device_type':'linux',
		'host':'29.29.29.23',
		'username':'admin',
		'password':'admin'
                }

ve1k_rtr2 = ConnectHandler(**vEdge1k_rtr2)
ve1k_rtr1 = ConnectHandler(**vEdge1k_rtr1)


ve1k_rtr2.send_command("paginate false")
ve1k_rtr1.send_command("paginate false")

class rangusky():
	def check_control_connection_good():
		print ("************Checking control connections after pub-int is brought up************")
		lte = 0
		pub_int = 0
		while pub_int < 2:
			ctrl_conn = ve1k_rtr2.send_command("show control connections")
			print (ctrl_conn)
			for row in ctrl_conn.split('\n'):
				if 'vsmart' in row and 'lte' in row and 'up' in row:
					lte = lte+1
				if 'vsmart' in row and 'public-internet' in row and 'up' in row:
					pub_int = pub_int + 1
			time.sleep(6)
		omp_lte = 0
		omp_pub_int = 0
		omp_route_output = ve1k_rtr2.send_command("show omp routes vpn 60 70.1.1.0/24 | tab")
		for route in omp_route_output.split('\n'):
			if '2.1.1.3' in route and '1.1.250.3' in route and 'public-internet' in route:
				omp_pub_int = 1
			if '2.1.1.3' in route and '1.1.250.3' in route and 'lte' in route:
				omp_lte = 1
		if omp_pub_int != 1:
			print ("************Box has gone into problem state************ \n")
			print (omp_route_output)
			ve1k_rtr2.send_command("clear omp all")
		elif omp_pub_int == 1:
			print ("************Box is good************ \n")
			print (omp_route_output)

	def check_control_connection_bad():
		print ("************Checking control connections after pub-int is down************ \n")
		pub_int = 2

		while pub_int != 0:
			ctrl_conn = ve1k_rtr2.send_command("show control connections")
			print (ctrl_conn)
			temp_list = []
			for row in ctrl_conn.split('\n'):
				if 'vsmart' in row and 'public-internet' in row and 'up' in row:
					temp_list.append(row)
				if 'vsmart' in row and 'lte' in row and 'up' in row:
					temp_list.append(row)
			#print (temp_list)
			if len(temp_list) == 2:
				pub_int = 0

			time.sleep(5)
		omp_lte = 0
		omp_pub_int = 0
		omp_route_output = ve1k_rtr2.send_command(" show omp routes vpn 60 70.1.1.0/24 | tab")
		for route in omp_route_output.split('\n'):
			if '2.1.1.3' in route and '1.1.250.3' in route and 'public-internet' in route:
				omp_pub_int = 1
			if '2.1.1.3' in route and '1.1.250.3' in route and 'lte' in route:
				omp_lte = 1
		print (omp_route_output)
		time.sleep(60)
		rangusky.unshut_interface_rtr1()

	def unshut_interface_rtr1():
		print ("*************Unshutting the public-internet interface************ \n")
		print (ve1k_rtr1.find_prompt())
		ve1k_rtr1.send_command("config ; vpn 0 ; interface ge0/1.11 ; no shut ; commit and-quit")
		#print (ve1k_rtr1.find_prompt())
		#time.sleep(60)
		rangusky.check_control_connection_good()

	def shut_interface_rtr1():
		print ("************Shutting the public-internet interface************ \n")
		print (ve1k_rtr1.find_prompt())
		ve1k_rtr1.send_command("config ; vpn 0 ; interface ge0/1.11 ; shut ; commit and-quit")
		#print (ve1k_rtr1.find_prompt())
		#time.sleep(60)
		rangusky.check_control_connection_bad()


if __name__ == '__main__':

	#Check control connections
	ctrl_conn = ve1k_rtr2.send_command("show control connections")

	lte=0
	pub_int=0
	for row in ctrl_conn.split('\n'):
		#print (row)
		if 'vsmart' in row  and 'lte' in row and 'up' in row:
			lte = lte + 1
		elif 'vsmart' in row and 'public-internet' in row and 'up' in row:
			pub_int = pub_int + 1

	print ("vSmart Control connections over lte circuit = ", lte)
	print ("vSmart Control connections over public-internet circuit = ", pub_int)

	if pub_int == 0:
		rangusky.unshut_interface_rtr1()
	if pub_int == 2:
		rangusky.shut_interface_rtr1()
