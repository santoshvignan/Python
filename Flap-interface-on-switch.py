import telnetlib
import netmiko
from netmiko import ConnectHandler
import time

switch_connect = ConnectHandler(device_type='cisco_ios', host='29.29.29.21', username='admin', password='MANSANvig2908')
cEdge_connect = ConnectHandler(device_type='cisco_ios', host='29.29.29.31', username='admin',password='admin')
vEdge_connect = ConnectHandler(device_type='linux', host='29.29.29.23',username='admin',password='admin')

switch_connection = switch_connect.find_prompt()
#print switch_connection
cEdge_connection = cEdge_connect.find_prompt()
#print cEdge_connection
vEdge_connection = vEdge_connect.find_prompt()
#print vEdge_connection

vEdge_nat_session_output = vEdge_connect.send_command('show ip nat filter |tab |inc "30.1.1.5 | 40.1.1.5" | nomore')
print vEdge_nat_session_output

cEdge_bfd_sessions_output = cEdge_connect.send_command("show sdwan bfd sessions")
print cEdge_bfd_sessions_output

switch_command_output = switch_connect.send_command("show interface description")
print switch_command_output

switch_port_config_command = switch_connect.send_config_set('interface Gig1/0/12')
print switch_port_config_command

#switch_command_output = switch_connect.send_command("show interface description")
#print switch_port_shut_command
#switch_port_shut_command = switch_connect.send_config_set('shut')
#print switch_command_output

#time.sleep(30)

#switch_port_noshut_command = switch_connect.send_config_set('no shut')
#print switch_port_noshut_command
#switch_command_output = switch_connect.send_command("show interface description")
#print switch_command_output

#time.sleep(30)
#vEdge_nat_session_output = vEdge_connect.send_command('show ip nat filter |tab |inc "30.1.1.5 | 40.1.1.5" | nomore')
#print vEdge_nat_session_output

#cEdge_bfd_sessions_output = cEdge_connect.send_command("show sdwan bfd sessions")
#print cEdge_bfd_sessions_output




#net
