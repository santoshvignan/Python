import paramiko
import os
import time

host_name = "172.18.52.52"
user_name = "admin"
pass_word = "MANSANvig2908"


def vedge_connect(host_name,user_name,pass_word):
    vedge_login = paramiko.SSHClient()
    vedge_login.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    vedge_login.connect(hostname=host_name, username=user_name, password=pass_word)
    vedge_shell = vedge_login.invoke_shell()
    time.sleep(5)
    vedge_login = vedge_shell.recv(10000).decode('utf-8')
    print ("vEdge login info: %s" % vedge_login)
    return vedge_shell

def upgrade_downgrade(sw_ver):
    vedge_shell = vedge_connect(host_name,user_name,pass_word)
    print ("Activating %s software now.." % sw_ver)
    vedge_shell.send("request software active now %s \n" % sw_ver)
    time.sleep(30)
    vedge_shell.close()


upgrade_downgrade("18.4.5")


"""
##vedge_shell.send("paginate false \n")
    vedge_shell.send("show version \n")
    time.sleep(1)
    sw_version_info = vedge_shell.recv(10000).decode('utf-8')
    print (sw_version_info)

if sw_version_info == "20.3.4":
    print ("Device is on the expected software version..let us reset the modem and test")
    vedge_shell.send("request internal modem reset \n")
    time.sleep(15)
    vedge_shell.send("\n")
    vedge_shell.send("show cellular modem \n")
    modem_state_bad = False
    cellular_modem_info = vedge_shell.recv(10000).decode('utf-8')
    print (cellular_modem_info)
    
    if modem_state_bad == False:
        print ("Let us reboot the router and test")
        vedge_shell.send("reboot now \n")
        vedge_login.close()
        time.sleep(300)
        vedge_login = paramiko.SSHClient()
        vedge_login.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        vedge_login.connect(hostname=host_name, username=user_name, password=pass_word)
        vedge_shell = vedge_login.invoke_shell()
        vedge_shell.send("show cellular modem \n")
        cellular_modem_info = vedge_shell.recv(10000).decode('utf-8')

        if modem_state_bad == False:
            print ("Let us try downgrade/upgrade route")
            vedge_shell.send("request software active now 18.4.5 \n")"""






