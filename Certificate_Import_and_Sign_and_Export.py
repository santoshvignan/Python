import requests
requests.packages.urllib3.disable_warnings()
import time
import subprocess

login_username = input("Please enter the username to login into the vmanage: ")
login_password = input("Please enter the password: ")
vmanage_ip = input("Please enter the vmanage ip and port details: ")
#vmanage_ip = '172.18.52.16'

#Login Details
username = login_username ; password = login_password

#username = 'admin' ; password = 'MANSANvig2908'

#Creating a dictionary with the login  details to be passed with the api call
login_data = {'j_username':username,'j_password':password}

#Constructing the URL

login_url = "https://%s/" %vmanage_ip

#Starting a session
vmanage = requests.Session()

#Logging into the vManage
login_to_vmanage = vmanage.post(login_url+"j_security_check",data=login_data,verify=False)

#Device_Details
payload = {"deviceIP":"2.1.1.1"}

#Retreive the CSR from the vManage

download_csr = vmanage.post("https://172.18.52.16/dataservice/certificate/generate/csr",verify=False,json = payload)

CSR_API_JSON_RESPONSE = download_csr.json()

device_CSR = CSR_API_JSON_RESPONSE["data"][0]["deviceCSR"]
device_CSR_NAME = CSR_API_JSON_RESPONSE["data"][0]["host-name"]

print (device_CSR)
print (device_CSR_NAME)

CSR_File = open("/Users/vignan/Documents/testbed/certs/vignan2/newcsr/"+device_CSR_NAME+".csr",'w')

for i in device_CSR:
    CSR_File.write(i)

CSR_File.close()

time.sleep(10)
#Defining the directories where the Self-Sign-Certificate process is going to happen
wd = '/Users/vignan/Documents/testbed/certs/vignan2'

csr ='/Users/vignan/Documents/testbed/certs/vignan2/newcsr'

cer = '/Users/vignan/Documents/testbed/certs/vignan2/newcerts'

#Listing the CSR files which need to be signed
p1 = subprocess.run(['ls'],cwd=csr,capture_output=True,text=True)

csr_dir_files = p1.stdout.split('\n')
#print (csr_dir_files)

#The following code block does the following: We take every csr file, generate the name of the signed cert,
#Sign the CSR using the openssl command, if the operation is successful, print the result with the new certificate
#name
for every_csr_file in csr_dir_files:
    if every_csr_file != '':
        #print (every_csr_file)

        new_cert_name = every_csr_file.split('.')

        temp_cert_name = "newcerts/"+new_cert_name[0]+'.pem'

        temp_csr_name ="newcsr/"+every_csr_file

        print ('I am currently processing' + ' ' + every_csr_file)

        sign_csr =subprocess.run(['openssl ca -batch -passin pass:12344321 -config openssl.cnf -in' + ' '
                                  + temp_csr_name +' ' + '-out' + ' ' + temp_cert_name],cwd=wd,shell=True,
                                  capture_output=True,text=True)
        #print (p2.returncode)
        #print (p2.stderr)
        if sign_csr.returncode == 0:

            print("Finished signing" + ' ' + every_csr_file + '.' + ' The new cert name is ' + new_cert_name[0]+'.pem')
            #cert_signing_result = p2.stdout
            #
            #print (cert_signing_result)
            #
            #p3 = subprocess.run(['openssl x509 -in' + ' ' + new_cert_name[0] + ' ' '-noout -text'],cwd=cer,shell=True,
            #                    capture_output=True,text=True)
            #
            #print (p3.stdout)


delete_csr = subprocess.run(['rm -rf *'],shell=True,cwd=csr,capture_output=True)

#print (delete_csr.stderr)

