import paramiko
import time
from datetime import date, datetime



def connect_to_device(device_ip,device_username,device_password):
    device = paramiko.SSHClient()
    device.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        device.connect(hostname=device_ip,username=device_username,password=device_password)
        device_shell = device.invoke_shell()
        return device_shell

    except:
        print (f"Unable to login to {device_ip}. Please use a different username/password")
        return False
    
def collect_show_command_outputs(device_list,device_username,device_password):
    for device in device_list:
        device_shell = connect_to_device(device.strip(),device_username,device_password)
        if (device_shell):
            current_date_time = date.today()
            #print (current_date_time)
            device_log_name = device.strip()+"_"+str(current_date_time)+".txt"
            device_log = open(device_log_name,"w")
            device_log.writelines(str(datetime.now())+"\n")
            device_shell.send("paginate false\n")
            time.sleep(2)
            device_command_read = open("command_list","r")
            device_commands = device_command_read.readlines()
            for command in device_commands:
                device_shell.send(command.strip() + "\n")
                time.sleep(20)
                device_recv_data = device_shell.recv(10000000)
                print (device_recv_data.decode('utf-8'))
                device_log.writelines(device_recv_data.decode('utf-8'))
        
        else:
            print (f"Could not connect to {device.strip()}")
        
        device_log.close()
        return device_log_name

def main():
    #global device_username,device_password
    device_username = input("Enter the username: ")
    device_password = input("Enter the password: ")
    device_list_read = open("device_list","r")
    device_list = device_list_read.readlines()
    print (f"The commands are going to be collected from the following devices: {device_list}")
    collect_show_command_outputs(device_list,device_username,device_password)

if __name__ == "__main__":
    main()
