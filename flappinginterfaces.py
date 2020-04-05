import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.5.5.16',port=22,username='admin',password='MANSANvig2908')
time.sleep(2)

#Invoke shell
command = ssh.invoke_shell()

#Receive output 

output = command.recv(1000000)

print output

time.sleep(5)
#Send commands

command.send("config\n")
time.sleep(2)
command.send("vpn 0\n")
command.send("\n")
time.sleep(2)

#For loop to continuously flap the tunnel interface
i = 0
while i < 1000000:
	command.send("interface eth0\n")
	#time.sleep(2)
	command.send("shut \n")
	time.sleep(2)
	command.send("commit\n")
	time.sleep(8)
	command.send("no shut \n")
	#time.sleep(2)
	command.send("commit\n")
	i = i+1

ssh.close() 
