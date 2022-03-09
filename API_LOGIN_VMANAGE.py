import requests
#import json
import time

#vmanage_ip = input("Enter the vmanage ip: ")
vmanage_username = input("Enter the vmanage username: ")
vmanage_password = input("Enter the vManage password: ")

login_url = "https://%s:8443/" %vmanage_ip
login_action = "j_security_check"
login_data = {'j_username':vmanage_username,'j_password':vmanage_password}
login_to_vmanage = login_url + login_action
print (login_to_vmanage)

vmanage = requests.session()
login = vmanage.post(url=login_to_vmanage,data=login_data,verify=False)

print (login.status_code)
#print (login.json())

# print("Successfully logged into vManage..Now, let's get the Cookie")
cookies = login.headers["Set-Cookie"]
print("First Cookie: " + cookies.split(";")[0])
jsessionid = cookies.split(";")[0]


for i in range(0,51):
    print("***********" + str(i) + "******************")
    login_headers = {'Cookie': jsessionid}
    vmanage_cookie_url = login_url + "dataservice/client/token"
    #print(vmanage_cookie_url)

    get_vmanage_cookie = requests.get(vmanage_cookie_url, headers=login_headers, verify=False)
    old_vmanage_token = get_vmanage_cookie.text
    #print("X-XSRF-Token: " + old_vmanage_token)
    vmanage_controller_vedge_sync_status = login_url + "dataservice/system/device/controllers/vedge/status"
    get_vmanage_controller_vedge_sync_status = requests.get(vmanage_controller_vedge_sync_status,headers=login_headers,verify=False)

    vmanage_sync_data = get_vmanage_controller_vedge_sync_status.json()

    #print (vmanage_sync_data["data"])
    #time.sleep(1)
