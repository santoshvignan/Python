import time
from netmiko import SSHDetect,ConnectHandler,NetMikoTimeoutException,NetMikoAuthenticationException,\
    NetmikoTimeoutError,NetmikoAuthError

HOST = ['29.29.29.14','29.29.29.11','29.29.29.12','29.29.29.13','29.29.29.20']
USERNAME = 'admin'
PASSWORD = ['MANSANvig2908','admin']


def get_hostname_and_mgmt_ipaddr(var1):
    temp_list1 = []
    for i in range(0,len(var1)):
        if var1[i] is '':
            continue
        else:
            temp_list1.append(var1[i])
    return temp_list1

for IP in HOST:
    try:
        guesser = SSHDetect(ip=IP,username=USERNAME,password=PASSWORD[0],device_type="autodetect")
        best_match = guesser.autodetect()
        print(best_match)
        #print(type(best_match))
        #print (guesser.potential_matches)

    except (NetMikoTimeoutException,NetmikoTimeoutError) as excptn:
        print (excptn)
        continue

    except:
        guesser = SSHDetect(ip=IP, username=USERNAME, password=PASSWORD[1], device_type="autodetect")
        best_match = guesser.autodetect()
        print(best_match)


    if best_match is None:
        try:
            connect = ConnectHandler(ip=IP,username=USERNAME,password=PASSWORD[0],device_type='linux')
            #print (connect.find_prompt())
            hostname = connect.send_command("show running-config system host-name")
            #print ((hostname.splitlines()[1]).split(' '))
            host_name = get_hostname_and_mgmt_ipaddr((hostname.splitlines()[1]).split(' '))
            print (host_name)
            mgmt_intf = connect.send_command("show interface vpn 512")
            #print ((mgmt_intf.splitlines()[1]).split(' '))
            mgmtintf = get_hostname_and_mgmt_ipaddr((mgmt_intf.splitlines()[1]).split(' '))
            print (mgmtintf)

        except:
            connect = ConnectHandler(ip=IP, username=USERNAME, password=PASSWORD[1], device_type='linux')
            # print (connect.find_prompt())
            hostname = connect.send_command("show running-config system host-name")
            # print ((hostname.splitlines()[1]).split(' '))
            host_name = get_hostname_and_mgmt_ipaddr((hostname.splitlines()[1]).split(' '))
            print(host_name)
            mgmt_intf = connect.send_command("show interface vpn 512")
            # print ((mgmt_intf.splitlines()[1]).split(' '))
            mgmtintf = get_hostname_and_mgmt_ipaddr((mgmt_intf.splitlines()[1]).split(' '))
            print(mgmtintf)


    elif best_match is 'cisco_ios':
        try:
            connect = ConnectHandler(ip=IP,username=USERNAME,password=PASSWORD[0],device_type='cisco_ios')
            #print (connect.find_prompt())
            hostname = connect.send_command('show sdwan running-config | inc hostname')
            #print ((hostname.splitlines()[0]).split(' '))
            host_name = get_hostname_and_mgmt_ipaddr((hostname.splitlines()[0]).split(' '))
            print (host_name)

            mgmt_intf = connect.send_command('show ip int brief')
            for j in mgmt_intf.splitlines():
                if '29.29' in j:
                    mgmtintf = get_hostname_and_mgmt_ipaddr(j.split(' '))
                else:
                    continue
            print (mgmtintf)
        except:
            connect = ConnectHandler(ip=IP, username=USERNAME, password=PASSWORD[1], device_type='cisco_ios')
            #print(connect.find_prompt())
            hostname = connect.send_command('show sdwan running-config | inc hostname')
            #print((hostname.splitlines()[0]).split(' '))
            host_name = get_hostname_and_mgmt_ipaddr((hostname.splitlines()[0]).split(' '))
            print(host_name)

            mgmt_intf = connect.send_command('show ip int brief')
            for j in mgmt_intf.splitlines():
                if '29.29' in j:
                    mgmtintf = get_hostname_and_mgmt_ipaddr(j.split(' '))
                else:
                    continue
            print(mgmtintf)

    else:
        print ("Could not connect to " + IP)



