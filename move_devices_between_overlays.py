#1. Get old and new vManage IP, Username, Password, vEdge Username, Password - Done
#2. Login to the vEdge and get the current organization-name, sp-organization-name, vBond ip details - Done
#3. Get the org-name,sp-org-name, vbond details of the future overlay - Done
#4. Login to the vEdge and get the chassis-number, serial-number and device type info - Done
#5. Login to the new overlay vManage and check if this device is present in the device's list- Done
#6. If it is present, then check if it is in valid/invalid/staging state under certificate tab. If it is in invalid/staging state, Move it to valid state and do send to controllers - Done
#7. Login to the old overlay and move this device to invalid state and do send to controllers. - Done
#8. Login to the vEdge and configure the new org-name, sp-org-name, vbond IP - Done
#9. Install the root-cert-chain of the new overlay on the device -
#10. Keep checking the control connections output to see if the device has formed connections with the new overlay.
#11. Do an API check from the new vManage as well to check if the device has synced with the new vManage.


import requests
import paramiko
import time
import json
import subprocess
import sys
requests.packages.urllib3.disable_warnings()


old_vmanage_ip = input("Please enter the old vManage IP: ")
new_vmanage_ip = input("Enter the new vManage IP: ")
vmanage_username = input ("Please enter the vManage username: ")
vmanage_password = input ("Please enter the vManage password: ")
device_mgmt_ip = input("Enter the Management IP for the vEdge: ")
device_username = input ("Enter the device username: ")
device_password = input ("Enter the device password: ")
new_org_name = input("Enter the new org-name: ")
new_vbond_ip = input("Enter the new vBond information: ")
new_sp_org_name = new_org_name
new_org_root_cert = input("Enter the name of the new root cert which needs to be installed: ")


#Logging into the device and get the old device information
device_ssh = paramiko.SSHClient()
device_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
device_ssh.connect(hostname=device_mgmt_ip, username=device_username,password=device_password)

device = device_ssh.invoke_shell()
device.send("\n")
time.sleep(2)

temp_data = device.recv(10000)

device.send("\n")
device_login = device.recv(10000)
print (device_login.decode('utf-8'))

device.send("\n")

device.send("show run system | nomore \n")
time.sleep(2)
device_system_info = device.recv(10000)


for i in device_system_info.decode('utf-8').split("\n"):
    if (i.lstrip()).startswith("system-ip"):
        device_system_ip = i.split()[1]
    if (i.lstrip()).startswith("organization-name"):
        device_old_org_name = i.split()[1]
        device_old_sp_org_name = device_old_org_name
    if (i.lstrip()).startswith("vbond"):
        device_old_vbond_ip = i.split()[1]

device.send("\n")
temp_data = device.recv(10000)

device.send("show system status | nomore | inc Model \n")
time.sleep(2)

device_system_status_info = device.recv(10000)
for j in device_system_status_info.decode('utf-8').split("\n"):
    if j.startswith("Model name:"):
        temp_var = j.split()
        device_model = temp_var[len(temp_var) - 1]

device.send("\n")
random_data = device.recv(10000)

device.send("show certificate serial \n")
time.sleep(5)
device_cert_info = device.recv(10000)

print (device_cert_info.decode('utf-8'))

device_serial_number = device_cert_info.decode('utf-8').split("Board")[1].split("number:")[1].split("\r")[0].strip()
#print (device_serial_number)

device_chassis_number =  device_cert_info.decode('utf-8').split("Board")[0].split("number:")[1].strip()
#print (device_chassis_number)

print ("The vEdge's old system information is:\nSystem-ip -> %s\nOrganization-name -> %s\nSp-Organizatio-Name -> %s\n"
       "vBond Information -> %s\nDevice-Model -> %s\nChassis number -> %s\nCertificate Serial Number -> %s"
       %(device_system_ip, device_old_org_name,device_old_sp_org_name,device_old_vbond_ip,device_model,
         device_chassis_number,device_serial_number))

device.close()

#Log into new vManage and check if the device is present in the device list.
login_url = "https://%s:8443/" % new_vmanage_ip
login_action = "j_security_check"
login_data = {'j_username': vmanage_username, 'j_password': vmanage_password}

login_to_vmanage = login_url + login_action

vmanage = requests.session()
login = vmanage.post(url=login_to_vmanage, data=login_data, verify=False)

if login.status_code == 200:
    #print("Successfully logged into vManage..Now, let's get the Cookie")
    cookies = login.headers["Set-Cookie"]
    #print("First Cookie: " + cookies.split(";")[0])
    jsessionid = cookies.split(";")[0]

    headers = {'Cookie': jsessionid}
    vmanage_cookie_url = login_url + "dataservice/client/token"
    #print(vmanage_cookie_url)

    get_vmanage_cookie = requests.get(vmanage_cookie_url, headers=headers, verify=False)
    token = get_vmanage_cookie.text
    #print("X-XSRF-Token: " + token)

devicelist_url = login_url + "dataservice/certificate/vedge/list"

devicelist_data = requests.get(devicelist_url, headers=headers,verify=False)
devicelist_data_json = devicelist_data.json()

device_present = False
device_validity = False

for device in devicelist_data_json["data"]:
    if device["uuid"] == device_chassis_number:
        print ("Device is present in the new vManage")
        device_present = True
        if device["validity"] == 'valid':
            device_validity = True
            print ("Device is in valid State. Now,let us move the device to invalid state on the old vManage.")
        else:
            print ("Moving the device to valid state...")
            move_device_to_valid_state_url = login_url + "dataservice/certificate/save/vedge/list"
            post_header = {'Cookie':jsessionid,'X-XSRF-TOKEN': token}
            device_data_dict = {}
            device_data_dict['chasisNumber']=device_chassis_number
            device_data_dict["serialNumber"]=device_serial_number
            device_data_dict["validity"]="valid"
            print (device_data_dict)

            device_data_json = json.dumps(device_data_dict)
            print (device_data_json)

            move_device_to_valid_state = requests.post(move_device_to_valid_state_url,json=device_data_json,headers=post_header,verify=False)
            if move_device_to_valid_state.status_code == 200:
                send_to_controllers_url = login_url + "dataservice/certificate/vedge/list?action=push"
                send_to_controllers = requests.post(send_to_controllers_url,headers=post_header,verify=False)
                if send_to_controllers.status_code == 200:
                    print ("Device has moved to valid state. Now, let us move the device to invalid state in the old vManage.")


if device_present == False:
    print ("The new overlay does not have the vEdge in its vEdge list. Please upload the vEdge serial to the vManage \n")
    sys.exit()


#Logging into old vManage and moving the device to invalid state

old_vmanage_login_url = "https://%s:8443/" % old_vmanage_ip
login_action = "j_security_check"
login_data = {'j_username': vmanage_username, 'j_password': vmanage_password}

login_to_vmanage = old_vmanage_login_url + login_action

old_vmanage = requests.session()
login = vmanage.post(url=login_to_vmanage, data=login_data, verify=False)

if login.status_code == 200:
    #print("Successfully logged into vManage..Now, let's get the Cookie")
    cookies = login.headers["Set-Cookie"]
    #print("First Cookie: " + cookies.split(";")[0])
    old_vmanage_jsessionid = cookies.split(";")[0]

    headers = {'Cookie': jsessionid}
    vmanage_cookie_url = login_url + "dataservice/client/token"
    #print(vmanage_cookie_url)

    get_vmanage_cookie = requests.get(vmanage_cookie_url, headers=headers, verify=False)
    old_vmanage_token = get_vmanage_cookie.text
    #print("X-XSRF-Token: " + old_vmanage_token)

print ("Moving the device to invalid state...")
move_device_to_invalid_state_url = old_vmanage_login_url + "dataservice/certificate/save/vedge/list"
post_header = {'Cookie':old_vmanage_jsessionid,'X-XSRF-TOKEN': old_vmanage_token}
device_data_dict = {}
device_data_dict['chasisNumber']=device_chassis_number
device_data_dict["serialNumber"]=device_serial_number
device_data_dict["validity"]="invalid"
#print (device_data_dict)

device_data_json = json.dumps(device_data_dict)
#print (device_data_json)

move_device_to_invalid_state = requests.post(move_device_to_invalid_state_url,json=device_data_json,headers=post_header,verify=False)
if move_device_to_invalid_state.status_code == 200:
    send_to_controllers_url = old_vmanage_login_url + "dataservice/certificate/vedge/list?action=push"
    send_to_controllers = requests.post(send_to_controllers_url,headers=post_header,verify=False)
    if send_to_controllers.status_code == 200:
        print ("Device has moved to invalid state.")

#Log into the device and configure the new org-name, sp-org-name, vbond information
device_ssh = paramiko.SSHClient()
device_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
device_ssh.connect(hostname=device_mgmt_ip,username=device_username,password=device_password)

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
time.sleep(10)
device_config_commit = device.recv(100000)


device.send("show run system | nomore \n")
time.sleep(2)

device_system_info = device.recv(100000)
#print (device_system_info.decode('utf-8'))
for i in device_system_info.decode('utf-8').split("\n"):
    if (i.lstrip()).startswith("organization-name"):
        device_new_org_name = i.split()[1]
    if (i.lstrip()).startswith("sp-organization-name"):
        device_new_sp_org_name = i.split()[1]
    if (i.lstrip()).startswith("vbond"):
        device_new_vbond_ip = i.split()[1]

if device_new_org_name == new_org_name and device_new_sp_org_name == new_sp_org_name and device_new_vbond_ip == new_vbond_ip:
    print ("Device has been configured with the new organization-name, sp-organization-name and vbond information")

else:
    print ("There was an error configuring the device. Please check the device and configure it")
    sys.exit()

#Install the new root-cert-chain on the device

device.send("request root-cert-chain install vpn 512 scp://vignan@29.29.29.3:/home/vignan/rootcerts/%s \n" %new_org_root_cert)
time.sleep(10)
device.send("MANSANvig2908\n")

device.send("show certificate root-ca-cert | inc Issuer | inc %s" %new_org_name)
time.sleep(2)
device_root_cert_info = device.recv(100000)
print (device_root_cert_info.decode('utf-8'))

if new_org_name in device_root_cert_info.decode('utf-8'):
    print ("New root chain has been successfully installed")
else:
    print ("New root chain is not installed")
    sys.exit()

#Do an API check from the new vManage as well to check if the device has synced with the new vManage.
login_url = "https://%s:8443/" % new_vmanage_ip
login_action = "j_security_check"
login_data = {'j_username': vmanage_username, 'j_password': vmanage_password}

login_to_vmanage = login_url + login_action

vmanage = requests.session()
login = vmanage.post(url=login_to_vmanage, data=login_data, verify=False)

if login.status_code == 200:
    #print("Successfully logged into vManage..Now, let's get the Cookie")
    cookies = login.headers["Set-Cookie"]
    #print("First Cookie: " + cookies.split(";")[0])
    jsessionid = cookies.split(";")[0]

    headers = {'Cookie': jsessionid}
    vmanage_cookie_url = login_url + "dataservice/client/token"
    #print(vmanage_cookie_url)

    get_vmanage_cookie = requests.get(vmanage_cookie_url, headers=headers, verify=False)
    token = get_vmanage_cookie.text
    #print("X-XSRF-Token: " + token)

devicemonitor_url = login_url + "dataservice/device"
device_reachable = False
i = 1
while (i <= 30 and device_reachable == False):
    print ("%s/30 Checking Device reachability with vManage" %str(i))
    device_data = requests.get(devicemonitor_url,headers=headers,verify=False)
    device_data_json = device_data.json()
    #print (device_data_json)
    for device in device_data_json["data"]:
        if (device["uuid"] == device_chassis_number) and (device["system-ip"]==device_system_ip) and (device["reachability"] == "reachable"):
            print ("Device is online with vManage")
            device_reachable = True
    i = i+1
    time.sleep(10)



