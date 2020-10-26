import telnetlib
import time
from netmiko import ConnectHandler
import re
import paramiko

host='172.18.52.22'
PORT = '2005'
password = 'MANSANvig2908'

asr = ConnectHandler(device_type='cisco_ios',host='29.29.29.19',username='admin',password='MANSANvig2908')
vman_priv1_color_state = False
ctrl_conn_op = asr.send_command("show sdwan control connections | inc vmanage")
vman_conn = re.search(r'vmanage',ctrl_conn_op)
color = re.search(r'private1',ctrl_conn_op)
state = re.search(r'up',ctrl_conn_op)
if vman_conn and color and state:
    vman_priv1_color_state = True
initial_biz_pub_port = 0
initial_priv1_pub_port = 0

ctrl_local_op = asr.send_command('show sdwan control local-properties "wan-interface-list"')
for line in ctrl_local_op.splitlines():
    a = re.search(r'GigabitEthernet0/0/0',line)
    b = re.search(r'GigabitEthernet0/0/1',line)
    if a:
        initial_priv1_pub_port = line.split()[2]
    if b:
        initial_biz_pub_port = line.split()[2]
print ("Initial private1 public port is: %s" %initial_priv1_pub_port )
print ("Initial private1 public port is: %s" %initial_biz_pub_port )
initial_glob_ipsec_drops = 0
glob_drops = asr.send_command("show platform hardware qfp active statistics drops")
for line in glob_drops.splitlines():
    c = re.search(r'IpsecInput',line)
    if c:
        initial_glob_ipsec_drops = line.split()[2]
print ("Initial global ipsec drops: %s" %initial_glob_ipsec_drops)

initial_ipsec_drops = 0
ipsec_drops = asr.send_command("show platform hardware qfp active feature ipsec datapath drops")
for line in ipsec_drops.splitlines():
    d = re.search(r'IN_US_V4_PKT_SA_NOT_FOUND_SPI',line)
    if d:
        initial_ipsec_drops = line.split()[2]
print ("Initial datapath ipsec drops: %s" %initial_ipsec_drops)

def monitor_asr(initial_priv1_pub_port,initial_biz_pub_port,initial_glob_ipsec_drops,initial_ipsec_drops):

    priv1_pub_port = 0
    biz_pub_port = 0
    global priv1_port_state
    global biz_port_state
    ctrl_local_op_after_acl_apply = asr.send_command('show sdwan control local-properties "wan-interface-list"')
    print (ctrl_local_op_after_acl_apply)
    for line in ctrl_local_op_after_acl_apply.splitlines():
        a = re.search(r'GigabitEthernet0/0/0', line)
        b = re.search(r'GigabitEthernet0/0/1', line)
        if a:
            priv1_pub_port = line.split()[2]
        if b:
            biz_pub_port = line.split()[2]
    if initial_priv1_pub_port == priv1_pub_port:
        print ("Private1 Port has not changed")
        priv1_port_state = 0
    if initial_biz_pub_port == biz_pub_port:
        print ("Biz-internet port has not changed")
        biz_port_state = 0
    if initial_priv1_pub_port != priv1_pub_port:
        print ("Private1 port has changed to " + str(priv1_pub_port))
        priv1_port_state = 1
    if initial_biz_pub_port != biz_pub_port:
        print ("Biz-internet port has changed to " + str(biz_pub_port))
        biz_port_state = 1

    bfd_output = asr.send_command('show sdwan bfd sessions "system-ip 1.1.255.1"')
    for line in bfd_output.splitlines():
        a = re.search(r'up',line)
        if a:
            print ("bfd-sessions are UP")
            repro_state = False
            glob_ipsec_drops = 0
            glob_drops = asr.send_command("show platform hardware qfp active statistics drops")
            for line in glob_drops.splitlines():
                c = re.search(r'IpsecInput', line)
                if c:
                    glob_ipsec_drops = line.split()[2]
            if glob_ipsec_drops > initial_glob_ipsec_drops:
                print ("Global IPSEC drops have increased but bfd is UP")
                print ("New Ipsec drop count: %s " %glob_ipsec_drops)
                #initial_glob_ipsec_drops = glob_ipsec_drops
                datapath_ipsec_drops = 0
                ipsec_drops = asr.send_command("show platform hardware qfp active feature ipsec datapath drops")
                for line in ipsec_drops.splitlines():
                    d = re.search(r'IN_US_V4_PKT_SA_NOT_FOUND_SPI', line)
                    if d:
                        datapath_ipsec_drops = line.split()[2]
                if datapath_ipsec_drops > initial_ipsec_drops:
                    print ("SPI drops have increased but BFD is still UP")
                    print ("NEW SPI drop count: %s" %datapath_ipsec_drops)
                    #initial_ipsec_drops = datapath_ipsec_drops
            return repro_state

        b = re.search(r'down', line)
        if b:
            print("bfd-sessions are DOWN")
            glob_ipsec_drops = 0
            glob_drops = asr.send_command("show platform hardware qfp active statistics drops")
            for line in glob_drops.splitlines():
                c = re.search(r'IpsecInput', line)
                if c:
                    glob_ipsec_drops = line.split()[2]
            if glob_ipsec_drops > initial_glob_ipsec_drops:
                print("Global IPSEC drops have increased")
                print("New Ipsec drop count: %s " % glob_ipsec_drops)
                datapath_ipsec_drops = 0
                ipsec_drops = asr.send_command("show platform hardware qfp active feature ipsec datapath drops")
                for line in ipsec_drops.splitlines():
                    d = re.search(r'IN_US_V4_PKT_SA_NOT_FOUND_SPI', line)
                    if d:
                        datapath_ipsec_drops = line.split()[2]
                if datapath_ipsec_drops > initial_ipsec_drops:
                    print("SPI drops have increased")
                    print("NEW SPI drop count: %s" % datapath_ipsec_drops)
                    print ("Problem has been reproduced")
                    repro_state = True
                    return repro_state

tn = telnetlib.Telnet(host,PORT)
time.sleep(2)
tn.write("\r".encode('ascii'))

password_prompt = tn.read_until(b'Password: ',timeout=2)
tn.write((password + "\r").encode('ascii'))

router_prompt = tn.read_until(b'mpls>',timeout=2)


tn.write(('en' + '\r').encode('ascii'))
router_enable_prompt = tn.read_until(b'mpls#',timeout=2)


tn.write(('term length 0' + '\r').encode('ascii'))
tn.read_until(b'mpls#',timeout=2)
time.sleep(2)

tn.write(('conf t'+'\r').encode('ascii'))
tn.read_until(b'mpls(config)#',timeout=2)

tn.write(('interface GigabitEthernet0/0.100'+'\r').encode('ascii'))
c = tn.read_until(b'mpls(config-subif)#',timeout=2)
time.sleep(2)
#print (c.decode('ascii'))

for i in range(0,3):

    tn.write(('ip access-group vman in'+'\r').encode('ascii'))
    d = tn.read_until(b'mpls(config-subif)#',timeout=2)
    #print (d.decode('ascii'))
    vbond_conn_state_up = 0
    while vbond_conn_state_up == 0:
        ctrl_conn_op = asr.send_command("show sdwan control connections")
        for line in ctrl_conn_op.splitlines():
            a = re.search(r'vbond',line)
            b = re.search(r'up', line)
            if a and b:
                vbond_conn_state_up = 1
        time.sleep(1)
    time.sleep(20)

    tn.write(('no ip access-group vman in'+'\r').encode('ascii'))
    tn.read_until(b'mpls(config-subif)#',timeout=2)

    time.sleep(30)

    repro_state = monitor_asr(initial_priv1_pub_port,initial_biz_pub_port,initial_glob_ipsec_drops,initial_ipsec_drops)

    if priv1_port_state == 1 and biz_port_state == 1:
        print ("Removing vbond poke a hole ACL")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('29.29.29.19', username='admin', password='MANSANvig2908', look_for_keys=False,allow_agent=False)
        connect = client.invoke_shell()
        connect.send("config-transaction")
        connect.send("\n")
        connect.send("sdwan")
        connect.send("\n")
        connect.send("interface GigabitEthernet0/0/0")
        connect.send("\n")
        connect.send("no access-list block_vbond_poke out")
        connect.send("\n")
        connect.send("interface GigabitEthernet0/0/1")
        connect.send("\n")
        connect.send("no access-list block_vbond_poke out")
        connect.send("\n")
        connect.send("commit")
        connect.send("\n")
        connect.send("end")
        connect.send("\n")
        client.close()



    if priv1_port_state == 0 and biz_port_state == 0:
        print ("Adding vbond poke a hole ACL")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('29.29.29.19', username='admin', password='MANSANvig2908', look_for_keys=False,allow_agent=False)
        connect = client.invoke_shell()
        connect.send("config-transaction")
        connect.send("\n")
        connect.send("sdwan")
        connect.send("\n")
        connect.send("interface GigabitEthernet0/0/0")
        connect.send("\n")
        connect.send("access-list block_vbond_poke out")
        connect.send("\n")
        connect.send("interface GigabitEthernet0/0/1")
        connect.send("\n")
        connect.send("access-list block_vbond_poke out")
        connect.send("\n")
        connect.send("commit")
        connect.send("\n")
        connect.send("end")
        connect.send("\n")
        client.close()

    if repro_state == True:
        break


tn.write(('end'+'\r').encode('ascii'))
time.sleep(2)
tn.write('\r'.encode('ascii'))
tn.write(('logout'+'\r').encode('ascii'))
asr.disconnect()
