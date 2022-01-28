import paramiko
import time
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('172.18.52.45',username='vignan',password="MANSANvig2908",look_for_keys=False, allow_agent=False)

connect = client.invoke_shell()

b = connect.recv(1000)
print (b)

connect.send("\n")

connect.send("virsh list --all")
connect.send("\n")
time.sleep(5)
f = connect.recv(1000000)
g = f.decode('utf-8')
print (g)

connect.send("virsh console csr1")
connect.send("\n")
time.sleep(5)

connect.send("\n")
connect.send("en")
connect.send("\n")
time.sleep(5)
h = connect.recv(1000000)
i = h.decode('utf-8')
print (i)

connect.send("show ver | inc mode")
connect.send("\n")
time.sleep(5)
j = connect.recv(1000000)
k = j.decode('utf-8')
print (k)

connect.send(b'\x5E'+ b'\x5D')
connect.send("\n")
time.sleep(5)

l = connect.recv(1000000)
m = l.decode('utf-8')
print (m)
