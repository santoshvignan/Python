import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json

vmanip = "29.29.29.5"
login_url = "https://%s:8443/" %vmanip
login_action = "j_security_check"
login_data ={'j_username':'admin', 'j_password':'MANSANvig2908'}
login_to_vmanage = login_url + login_action

vmanage = requests.session()
login = vmanage.post(url=login_to_vmanage,data=login_data,verify=False)

cookies = login.headers["Set-Cookie"]
print ("First Cookie: " + cookies.split(";")[0])
jsessionid = cookies.split(";")[0]

headers = {'Cookie':jsessionid}
vmanage_cookie_url = login_url + "dataservice/client/token"
print (vmanage_cookie_url)

get_vmanage_cookie = requests.get(vmanage_cookie_url,headers=headers,verify=False)
token = get_vmanage_cookie.text
print ("X-XSRF-Token: " + token)

dpi_url = "dataservice/statistics/dpi/aggregation"
dpi_str = """{"query":{"condition":"AND","rules":[{"value":["24"],"field":"entry_time","type":"date","operator":"last_n_hours"},{"value":["1.1.202.1"],"field":"vdevice_name","type":"string","operator":"in"}]},"aggregation":{"field":[{"property":"family","size":200,"sequence":1}],"metrics":[{"property":"octets","type":"sum","order":"desc"}]}}"""
dpi_json = json.loads(dpi_str)
dpi_agg_url = login_url + dpi_url
print (dpi_agg_url)
post_header = {'Cookie':jsessionid,'X-XSRF-TOKEN': token}
dpi_data = vmanage.post(dpi_agg_url,json=dpi_json,headers=post_header,verify=False)
print (dpi_data.status_code)
print (dpi_data.content.decode('utf-8'))