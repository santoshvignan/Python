import csv

a = open("/Users/vignan/Downloads/t1.csv", "w",newline='')
b = csv.writer(a,delimiter=' ')
b.writerow("shakila")
b.writerow("sha")

a.close()


device_ssh = paramiko.SSHClient()
device_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
device_ssh.connect(hostname=<ip address>,username=<username>,password=<password>)

device = device_ssh.invoke_shell()
device.send("\n")
time.sleep(2)

temp_data = device.recv(1000)

device.send("conf \n")
device.send("system \n")
device.send("organization-name %s \n" %new_org_name)
device.send("sp-organization-name %s \n" %new_sp_org_name)
device.send("vbond %s \n" %new_vbond_ip)
device.send("\n")
device.send("commit and-quit \n")
time.sleep(2)

