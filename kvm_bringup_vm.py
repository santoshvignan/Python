import paramiko
import time
import re

kvmlog = open("/home/vignan/device_bringup_log.txt","a")
kvmerrorlog = open("/home/vignan/device_error_log.txt","a")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('172.18.52.45',username='vignan',password="MANSANvig2908",look_for_keys=False, allow_agent=False)

connect = client.invoke_shell()

login_page = connect.recv(100000)
login_page_str = login_page.decode('utf-8')
#print (login_page_str)
kvmlog.writelines(login_page_str)
kvmlog.writelines("\n")

connect.send("cd device_images")
connect.send("\n")
connect.send("ls -ltr")
connect.send("\n")
time.sleep(5)

device_image_directory = connect.recv(100000)
device_image_directory_str = device_image_directory.decode('utf-8')
#print (device_image_directory_str)
kvmlog.writelines(device_image_directory_str)
kvmlog.writelines("\n")

for i in range(1,30):
    #print ("Starting the process to create %s CSR....." %i)
    #print ("Creating a copy of the qcow image.....")
    kvmlog.writelines("Starting the process to create %s CSR.....\n" %i)
    kvmlog.writelines("Creating a copy of the qcow image.....\n")

    connect.send("cp csr1000v-universalk9.17.02.01r-serial.qcow2 csr1000v-universalk9.17.02.01r-serial_" + str(i) + ".qcow2")
    connect.send("\n")
    time.sleep(5)

    connect.send("ls -ltr")
    connect.send("\n")
    time.sleep(5)

    device_image_directory_1 = connect.recv(100000)
    device_image_directory_str_1 = device_image_directory_1.decode('utf-8')
    #print (device_image_directory_str_1)
    kvmlog.writelines(device_image_directory_str_1)
    kvmlog.writelines("\n")

    device_name = "csr_" + str(i)
    #print ("Creating %s" %device_name)
    kvmlog.writelines("Creating %s \n" %device_name)

    disk_path = "/home/vignan/device_images/csr1000v-universalk9.17.02.01r-serial_" + str(i) + ".qcow2"
    #print ("Path to the image is %s" %disk_path)
    #print ("Creating the VM......")
    kvmlog.writelines("Path to the image is %s \n" %disk_path)
    kvmlog.writelines("Creating the VM...... \n")

    connect.send("virt-install --connect=qemu:///system --name=%s --os-type=linux --os-variant=rhel4.0 --arch=x86_64 "
                 "--cpu=host --vcpus=1,sockets=1,cores=1,threads=1 --ram=8192 --import "
                 "--disk path=%s,bus=ide,format=qcow2 "
                 "--network bridge=br0,model=virtio --network bridge=lan-br,model=virtio --noreboot" %(device_name,disk_path))

    connect.send("\n")
    time.sleep(10)

    connect.send("virsh list --all")
    connect.send("\n")
    time.sleep(5)

    vm_list = connect.recv(1000000)
    vm_list_str = vm_list.decode('utf-8')
    #print (vm_list_str)
    kvmlog.writelines(vm_list_str)
    kvmlog.writelines("\n")

    #print ("Starting the VM....")
    kvmlog.writelines("Starting the VM.... \n")
    connect.send("virsh start csr_%s" %i)
    connect.send("\n")

    connect.send("virsh list --all")
    connect.send("\n")
    time.sleep(5)

    start_vm = connect.recv(1000000)
    start_vm_str = start_vm.decode('utf-8')
    #print (start_vm_str)
    kvmlog.writelines(start_vm_str)
    kvmlog.writelines("\n")

    connect.send("virsh console csr_%s" %i)
    connect.send("\n")
    time.sleep(10)

    router_prompt = False
    while router_prompt==False:

        time.sleep(10)
        console_log = connect.recv(1000000)
        console_log_str = console_log.decode('utf-8')
        #print (console_log_str)
        kvmlog.writelines(console_log_str)
        kvmlog.writelines("\n")
        lines = console_log_str.splitlines()
        for line in lines:
            kvmerrorlog.writelines("I am currently processing \t" + str(line))
            con1 = re.search(r'Press RETURN',line)
            con2 = re.search(r'Press',line)
            con3 = re.search(r'RETURN',line)
            con4 = re.search(r'Would you like to enter the initial configuration dialog',line)
            con5 = re.search(r'yes/no',line)
            if con1:
                #print ("Box is getting ready....Found match for Condition1")
                kvmlog.writelines("Box is getting ready....Found match for Condition1 \n")
                #print (line)
                time.sleep(60)
                #print("Next Step")
                state = False
                while state == False:
                    connect.send("\r\n")
                    connect.send("\r\n")
                    connect.send("\r\n")
                    time.sleep(5)
                    login_prompt = connect.recv(1000000)
                    login_prompt_str = login_prompt.decode('utf-8')
                    #print(login_prompt_str)
                    kvmlog.writelines(login_prompt_str)
                    kvmlog.writelines("\n")
                    for line in login_prompt_str.splitlines():
                        prompt = re.search(r'Router>', line)
                        if prompt:
                            #print(login_prompt_str)
                            kvmlog.writelines(login_prompt_str)
                            kvmlog.writelines("\n")
                            state = True
                            break
                router_prompt = True
                break
            if con2:
                #print ("Box is getting ready....Found match for Condition2")
                kvmlog.writelines("Box is getting ready....Found match for Condition2 \n")
                #print (line)
                time.sleep(60)
                #print("Next Step")
                state = False
                while state == False:
                    connect.send("\r\n")
                    connect.send("\r\n")
                    connect.send("\r\n")
                    time.sleep(5)
                    login_prompt = connect.recv(1000000)
                    login_prompt_str = login_prompt.decode('utf-8')
                    #print(login_prompt_str)
                    kvmlog.writelines(login_prompt_str)
                    kvmlog.writelines("\n")
                    for line in login_prompt_str.splitlines():
                        prompt = re.search(r'Router>', line)
                        if prompt:
                            #print(login_prompt_str)
                            kvmlog.writelines(login_prompt_str)
                            kvmlog.writelines("\n")
                            state = True
                            break
                router_prompt = True
                break
            if con3:
                #print ("Box is getting ready....Found match for Condition3 \n")
                kvmlog.writelines("Box is getting ready....Found match for Condition3 \n")
                #print(line)
                time.sleep(60)
                #print("Next Step")
                state = False
                while state == False:
                    connect.send("\r\n")
                    connect.send("\r\n")
                    connect.send("\r\n")
                    time.sleep(5)
                    login_prompt = connect.recv(1000000)
                    login_prompt_str = login_prompt.decode('utf-8')
                    #print(login_prompt_str)
                    kvmlog.writelines(login_prompt_str)
                    kvmlog.writelines("\n")
                    for line in login_prompt_str.splitlines():
                        prompt = re.search(r'Router>', line)
                        if prompt:
                            #print(login_prompt_str)
                            kvmlog.writelines(login_prompt_str)
                            kvmlog.writelines("\n")
                            state = True
                            break
                router_prompt = True
                break
            if con4 or con5:
                #print ("Terminating auto-install... \n")
                kvmlog.writelines("Terminating auto-install... \n")
                #print (line)
                connect.send("no")
                connect.send("\n")
                time.sleep(5)
                conf_dialog = connect.recv(1000000)
                conf_dialog_str = conf_dialog.decode('utf-8')
                for ele in conf_dialog_str.splitlines():
                    con5 = re.search(r'Would you like to terminate autoinstall',ele)
                    if con5:
                        connect.send("yes")
                        connect.send("\n")
                        #print ("Terminated auto-install!!! \n")
                        kvmlog.writelines("Terminated auto-install!!! \n")
                        break

    print ("CSR %s is ONLINE!!!" %i)
    kvmlog.writelines("CSR %s is ONLINE!!! \n" %i)
    connect.send("\x1D")
    connect.send("\n")
    connect.send("\n")
    a = connect.recv(1000000)
    #print (a.decode('utf-8'))
    kvmlog.writelines(a.decode('utf-8'))
    kvmlog.writelines("\n")


kvmlog.close()
kvmerrorlog.close()



