import telnetlib
import time

f = open("/home/vignan/mpls-router.txt",'w')

host='172.18.52.22'
PORT = '2005'
password = 'MANSANvig2908'
tn = telnetlib.Telnet(host,PORT)


time.sleep(2)
tn.write("\r".encode('ascii'))

password_prompt = tn.read_until(b'Password: ',timeout=2)
f.write(password_prompt.decode('ascii'))
f.write('\n')
tn.write((password + "\r").encode('ascii'))

router_prompt = tn.read_until(b'mpls>',timeout=2)
f.write(router_prompt.decode('ascii'))
f.write('\n')

tn.write(('en' + '\r').encode('ascii'))
router_enable_prompt = tn.read_until(b'mpls#',timeout=2)
f.write(router_enable_prompt.decode('ascii'))
f.write('\n')

tn.write(('term length 0' + '\r').encode('ascii'))
tn.read_until(b'mpls#',timeout=2)
time.sleep(2)

#tn.write(('show ip access-lists' + "\r").encode('ascii'))
#b = tn.read_until(b'mpls#',timeout=2)
#print (b.decode('ascii'))

tn.write(('conf t'+'\r').encode('ascii'))
tn.read_until(b'mpls(config)#',timeout=2)

tn.write(('interface GigabitEthernet0/0.160'+'\r').encode('ascii'))
c = tn.read_until(b'mpls(config-subif)#',timeout=2)
time.sleep(2)
#print (c.decode('ascii'))

for i in range(0,10000000):
    f.write('Flap'+ ' ' + str(i) + '\n')
    tn.write(('ip access-group block_bfd in'+'\r').encode('ascii'))
    d = tn.read_until(b'mpls(config-subif)#',timeout=2)
    #print (d.decode('ascii'))

    time.sleep(10)

    tn.write(('no ip access-group block_bfd in'+'\r').encode('ascii'))
    tn.read_until(b'mpls(config-subif)#',timeout=2)

    time.sleep(10)

tn.write(('end'+'\r').encode('ascii'))
time.sleep(2)
tn.write('\r'.encode('ascii'))
tn.write(('logout'+'\r').encode('ascii'))
f.close()
