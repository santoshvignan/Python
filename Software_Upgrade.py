import requests
import os
import sys
import json
import time
import urllib3
import argparse
import paramiko
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Vmanage(object):
    def __init__(self,vmanage_host,username,password,upg_to_sw):
        self.vmanage_host = vmanage_host
        self.username = username
        self.password = password
        self.upg_to_sw = upg_to_sw
        #self.upg_flag = upg_flag



    def login_to_vmanage(self):
        
        login_url = "https://%s:8443/" %self.vmanage_host
        login_action = "j_security_check"
        login_data ={'j_username':self.username, 'j_password':self.password}

        login_to_vmanage = login_url + login_action

        vmanage = requests.session()
        login = vmanage.post(url=login_to_vmanage,data=login_data,verify=False)

        #print (login.status_code)
        #print (login.json())

        if login.status_code == 200:
            print ("Successflly logged into vManage..Now, let's get the Cookie")
            cookies = login.headers["Set-Cookie"]
            print ("First Cookie: " + cookies.split(";")[0])
            jsessionid = cookies.split(";")[0]

            headers = {'Cookie':jsessionid}
            vmanage_cookie_url = login_url + "dataservice/client/token"
            print (vmanage_cookie_url)

            get_vmanage_cookie = requests.get(vmanage_cookie_url,headers=headers,verify=False)
            token = get_vmanage_cookie.text
            print ("X-XSRF-Token: " + token)

            list_inst_sw_url = login_url + "dataservice/device/action/install/devices/vmanage"
            #print(list_inst_sw_url)
            list_inst_sw = requests.get(list_inst_sw_url, headers=headers, verify=False)
            list_inst_sw_data = list_inst_sw.json()

            curr_ver = list_inst_sw_data["data"][0]['current-partition']
            avail_ver = list_inst_sw_data["data"][0]['availableVersions']
            print("Current version running on the box: %s" % curr_ver)
            print("Available Softwares on vManage: %s" % str(avail_ver))
            if curr_ver == self.upg_to_sw:
                print("The device is already on the expected version of the code")
                sys.exit()
            elif self.upg_to_sw in avail_ver:
                print ("Software is already installed on the box..Proceeding with Activation of the software")
                self.Software_Activation(login_url,jsessionid,token)
            else:
                print ("Software is not present on the box..Starting Install")
                self.Software_Upgrade(login_url,jsessionid,token)
        
        else:
            print ("Connection has been unsuccessful")
    
    def Software_Upgrade(self,login_url,jsessionid,token):
        
        sw_repo_url = login_url + "dataservice/device/action/software"
        print (sw_repo_url)
        headers = {'Cookie':jsessionid}
        get_sw_repository_data = requests.get(sw_repo_url,headers=headers,verify=False)

        #print (get_sw_repository_data.json())
        sw_repo_data = get_sw_repository_data.json()
        sw_is_available = False
        for i in range(0,len(sw_repo_data["data"])):
            if self.upg_to_sw in sw_repo_data["data"][i]["versionName"]:
                #print (sw_repo_data["data"][i]["availableFiles"])
                #sw_index = i
                sw_is_available = True
        if sw_is_available == False:
            print ("Required Software is not available..Please upload the required software now")
            sys.exit()
        
        #INSTALL THE SOFTWARE ON THE VMANAGE
        print ("Starting the software installation process....")
        sw_install_url = login_url+"dataservice/device/action/install"
        print (sw_install_url)
        post_header = {'Cookie':jsessionid,'X-XSRF-TOKEN': token}
        sw_ins_device_data_str = """{"action":"install","input":{"vEdgeVPN":0,"vSmartVPN":0,"data":[{"family":"vmanage","version":"20.3.3"}],"versionType":"vmanage","reboot":false,"sync":true},"devices":[{"deviceIP":"5.1.1.1","deviceId":"6b1affd0-a61a-4a7b-8c55-36f443cae839"}],"deviceType":"vmanage"}"""
        sw_ins_device_data = json.loads(sw_ins_device_data_str)
        sw_install = requests.post(sw_install_url,json=sw_ins_device_data,headers=post_header,verify=False)
        print (sw_install.status_code)
        #time.sleep(10)
        if sw_install.status_code == 200:
            self.SW_INSTALL_MONITOR(login_url,jsessionid,token)

    def SW_INSTALL_MONITOR(self,login_url,jsessionid,token):
        print ("Software installation progress monitor...")
        headers = {'Cookie':jsessionid}
        sw_install_status = False
        active_tasks_url = login_url + "dataservice/device/action/status/tasks/activeCount"
        get_active_tasks_in_progress = requests.get(active_tasks_url,headers=headers,verify=False)
        print (get_active_tasks_in_progress.json())
        if get_active_tasks_in_progress.json()['data']['activeTaskCount'] > 0:
            tasks_url = login_url + "dataservice/device/action/status/tasks"
            get_tasks_in_progress = requests.get(tasks_url, headers=headers,verify=False)
            pid = get_tasks_in_progress.json()['runningTasks'][0]['processId']
            #pid = get_tasks_in_progress.json()
            print (pid)
        mon_sw_task_url = login_url + "dataservice/device/action/status/" + pid
        print (mon_sw_task_url)
        while sw_install_status == False:
            time.sleep(5)
            mon_sw_task = requests.get(mon_sw_task_url,headers=headers,verify=False)
            #print (mon_sw_task.json())
            sw_ins_task_status = mon_sw_task.json()
            print (sw_ins_task_status['data'][0]['status'])
            if sw_ins_task_status['data'][0]['status'] == 'Success':
                sw_install_status = True
                print ("Software has been successfully installed...Proceeding with Activation of the software")
                self.Software_Activation(login_url,jsessionid,token)
            elif sw_ins_task_status['data'][0]['status'] == "Failure":
                print ("Software Installation has Failed")
                sys.exit()
            time.sleep(10)

    def Software_Activation(self,login_url,jsessionid,token):
        headers={'Cookie':jsessionid}
        post_header = {'Cookie':jsessionid,'X-XSRF-TOKEN': token}
        sw_act_url = login_url + "dataservice/device/action/changepartition"
        sw_act_device_data_str = """{"action":"changepartition","devices":[{"version":"20.3.3","deviceIP":"5.1.1.1","deviceId":"6b1affd0-a61a-4a7b-8c55-36f443cae839"}],"deviceType":"controller"}"""
        sw_act_device_data = json.loads(sw_act_device_data_str)
        sw_activate = requests.post(sw_act_url,json=sw_act_device_data,headers=post_header,verify=False)
        print (sw_activate.status_code)
        if sw_activate.status_code == 200:
            status_message = "Software Activation in progress."
            for i in range(0,30):
                message = status_message+"."
                print (message)
                status_message = message
                time.sleep(1)
            self.vManage_SW_Activation_Mon(login_url,jsessionid,token)

    def vManage_SW_Activation_Mon(self,login_url,jsessionid,token):
        headers = {'Cookie': jsessionid}
        print ("vManage Software Activation Monitor")
        sw_activate_status = False
        is_vManage_GUI_UP = True
        list_inst_sw_url = login_url + "dataservice/device/action/install/devices/vmanage"
        while is_vManage_GUI_UP == True:
            list_inst_sw = requests.get(list_inst_sw_url, headers=headers, verify=False)
            if list_inst_sw.status_code == 200:
                list_inst_sw_data = list_inst_sw.json()
                curr_ver = list_inst_sw_data["data"][0]['current-partition']
                if curr_ver == self.upg_to_sw:
                    print ("Required Software is already installed..Bye")
                    sys.exit()
            else:
                is_vManage_GUI_UP = False
                print ("vManage GUI is DOWN.")

        time.sleep(10)
        message = "Waiting for vManage GUI to come online"
        is_vManage_SSH_up = False
        while is_vManage_SSH_up == False:
            is_vManage_up = os.system("ping -c 5 %s" %self.vmanage_host + ">/dev/null")
            if is_vManage_up == 0:
                try:
                    vManage_SSH = paramiko.SSHClient()
                    vManage_SSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    vManage_SSH.connect(self.vmanage_host,username=self.username,password=self.password)
                    vManage = vManage_SSH.invoke_shell()
                    login_ssh = vManage.recv(10000)
                    print (login_ssh.decode('utf-8'))
                    vManage.send("\n")
                    time.sleep(5)
                    login_ssh_1 = vManage.recv(1000)
                    print (login_ssh_1.decode('utf-8'))
                    if 'Welcome to Viptela CLI' in login_ssh_1.decode('utf-8'):
                        print ("******vManage SSH is UP******")
                        is_vManage_SSH_up = True
                    else:
                        print ("vManage is not ready..i am going to sleep for 20 seconds")
                        time.sleep(20)

                except:
                    status_message = message + "."
                    print(status_message)
                    message = status_message
                    time.sleep(1)

            else:
                print ("vManage is going through a reboot. Waiting for it to come back online")

        while is_vManage_SSH_up == True and sw_activate_status == False:

            print ("*******Now verifying the version of the vManage*******")
            vManage.send("show ver\n")
            vManage.send("\n")
            time.sleep(5)
            ver_info = vManage.recv(10000)
            print ("show version output is: %s " %ver_info)
            curr_ver = ver_info.decode('utf-8')
            print ("Current version on the box is: %s" %curr_ver)
            is_vManage_up_on_new_partition = re.search(self.upg_to_sw,curr_ver)
            if is_vManage_up_on_new_partition:
                print ("vManage has upgraded to the required version of the code")
                print ("Now, let us check the NMS Application server status")
                is_app_server_running = False
                while is_app_server_running== False:
                    vManage.send("request nms application-server status\n")
                    time.sleep(5)
                    app_server_status = vManage.recv(10000)
                    app_server = app_server_status.decode('utf-8')
                    print ("Application-server Status: %s" %app_server)
                    app_server_running = re.search(r'running',app_server)
                    app_server_pid = re.search(r'PID',app_server)
                    if app_server_running and app_server_pid:
                        is_app_server_running = True
                        time.sleep(10)

                is_vManage_GUI_UP = False
                while is_vManage_GUI_UP == False:

                    login_action = "j_security_check"
                    login_data = {'j_username': self.username, 'j_password': self.password}
                    login_to_vmanage = login_url + login_action
                    vmanage = requests.session()
                    login = vmanage.post(url=login_to_vmanage, data=login_data, verify=False)
                    if login.status_code == 200:
                        print ("GUI is UP")
                        is_vManage_GUI_UP = True
                        time.sleep(5)
                    else:
                        print ("GUI is still not online, Status code is: %s" %login.status_code)
                vmanage = requests.session()
                login = vmanage.post(url=login_to_vmanage, data=login_data, verify=False)
                cookies = login.headers["Set-Cookie"]
                print("New Cookie: " + cookies.split(";")[0])
                jsessionid = cookies.split(";")[0]

                headers = {'Cookie': jsessionid}
                list_inst_sw_url = login_url + "dataservice/device/action/install/devices/vmanage"
                list_inst_sw = requests.get(list_inst_sw_url, headers=headers, verify=False)
                list_inst_sw_data = list_inst_sw.json()

                curr_ver = list_inst_sw_data["data"][0]['current-partition']
                print("Current version running on the box: %s" % curr_ver)
                if curr_ver == self.upg_to_sw:
                    print ("vManage is currently UP on the 20.3.3 version of the code..Good Bye")
                    sys.exit()
                else:
                    print ("Some Failure has happened!")






if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", required=True, type=str, help="Enter the vManage ip information")
    parser.add_argument("-u", required=True, type=str, help="Enter the username for vManage")
    parser.add_argument("-p", required=True, type=str, help="Enter the password for vManage")
    parser.add_argument("-sw", required=True, type=str, help="Enter the software version we want to upgrade")
    #parser.add_argument("-upgflg",required=True,type=str,help="Enter the upgrade flag. Upgrade Flag is 3-bit value(vManage,vSmart,vBond).001 - only upgrade vBond")

    args = parser.parse_args()
    vmanage_host = args.ip
    username = args.u
    password = args.p
    upg_to_sw = args.sw
    #upg_flag = args.upgflg


    task = Vmanage(vmanage_host,username,password,upg_to_sw)
    login = task.login_to_vmanage()
