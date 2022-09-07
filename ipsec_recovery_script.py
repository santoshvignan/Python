import paramiko
import time
from datetime import datetime,date
import base64
import os


#1. Log into the vEdge
#2. Check if the rx_window_drops are increasing.
#3. If drops are increasing, collect outputs and do a clear omp all

hosts = ["29.29.29.20"]

file_path = "/home/vignan/"
# vedge_username = input("Enter the username: ")
# vedge_password = input("Enter the password: ")
# recovery_cmd = input("Enter the recovery command")


vedge_username = "admin"
vedge_password = "admin"
recovery_cmd = "clear omp all"

for host in hosts:
    today = date.today()
    filename = file_path + "ipsec_logs_" + host + "_" + str(today) +".txt" 
    if (os.path.exists(filename)):
        log_file_size = os.stat(filename).st_size

        if (log_file_size >= 10000000):
            os.remove(filename)
            filename = file_path + "ipsec_logs_" + host + "_" + str(today) +".txt"

    current_time = datetime.now()
    log = open(filename,"a")


    log.writelines("########################################\n")
    log.writelines(str(current_time) + "\n")
    vedge_ip = host

    ve_ssh = paramiko.SSHClient()
    ve_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ve_ssh.connect(hostname=vedge_ip,username=vedge_username,password=vedge_password)
    time.sleep(5)


    ve_cmd = ve_ssh.invoke_shell()
    ve_recv = ve_cmd.recv(100000)
    print (ve_recv.decode('utf-8'))
    log.writelines(ve_recv.decode('utf-8') + "\n")
    time.sleep(5)

    ve_cmd.send("paginate false \n")
    ve_recv = ve_cmd.recv(100000)
    ve_cmd.send("\n")
    time.sleep(5)
    
    rx_window_stats ={"rx_window_drops_0":[],"rx_window_drops_1":[],"rx_window_drops_2":[],"rx_window_drops_3":[],"rx_window_drops_4":[],"rx_window_drops_5":[],"rx_window_drops_6":[],"rx_window_drops_7":[]}
    #system_stats = []
    for i in range(0,3):
        log.writelines("*****************Iteration_" + str(i) + "********************\n")
        ve_cmd.send("show system statistics | nomore | inc rx_window_drops \n")
        time.sleep(5)
        ve_recv = ve_cmd.recv(10000)
        #print (ve_recv.decode('utf-8'))
        log.writelines(ve_recv.decode('utf-8') + "\n")
        for window_drops in ve_recv.decode('utf-8').split("\n"):
            #print (window_drops.strip())
            if "rx_window_drops_tc0" in window_drops.strip():
                #print (window_drops.strip())
                #log.writelines(window_drops.strip() + "\n")
                #system_stats.append(window_drops.strip().split(":")[1].strip())
                rx_window_stats["rx_window_drops_0"].append(window_drops.strip().split(":")[1].strip())
                
            if "rx_window_drops_tc1" in window_drops.strip():
                #print (window_drops.strip())
                #log.writelines(window_drops.strip() + "\n")
                #system_stats.append(window_drops.strip().split(":")[1].strip())
                rx_window_stats["rx_window_drops_1"].append(window_drops.strip().split(":")[1].strip())

            if "rx_window_drops_tc2" in window_drops.strip():
                #print (window_drops.strip())
                #log.writelines(window_drops.strip() + "\n")
                #system_stats.append(window_drops.strip().split(":")[1].strip())
                rx_window_stats["rx_window_drops_2"].append(window_drops.strip().split(":")[1].strip())

            if "rx_window_drops_tc3" in window_drops.strip():
                #print (window_drops.strip())
                #log.writelines(window_drops.strip() + "\n")
                #system_stats.append(window_drops.strip().split(":")[1].strip())
                rx_window_stats["rx_window_drops_3"].append(window_drops.strip().split(":")[1].strip())
 
            if "rx_window_drops_tc4" in window_drops.strip():
                #print (window_drops.strip())
                #log.writelines(window_drops.strip() + "\n")
                #system_stats.append(window_drops.strip().split(":")[1].strip())
                rx_window_stats["rx_window_drops_4"].append(window_drops.strip().split(":")[1].strip())

            if "rx_window_drops_tc5" in window_drops.strip():
                #print (window_drops.strip())
                #log.writelines(window_drops.strip() + "\n")
                #system_stats.append(window_drops.strip().split(":")[1].strip())
                rx_window_stats["rx_window_drops_5"].append(window_drops.strip().split(":")[1].strip())

            if "rx_window_drops_tc6" in window_drops.strip():
                #print (window_drops.strip())
                #log.writelines(window_drops.strip() + "\n")
                #system_stats.append(window_drops.strip().split(":")[1].strip())
                rx_window_stats["rx_window_drops_6"].append(window_drops.strip().split(":")[1].strip())
            
            if "rx_window_drops_tc7" in window_drops.strip():
                #print (window_drops.strip())
                #log.writelines(window_drops.strip() + "\n")
                #system_stats.append(window_drops.strip().split(":")[1].strip())
                rx_window_stats["rx_window_drops_7"].append(window_drops.strip().split(":")[1].strip())

        time.sleep(5)


    # print (system_stats)
    # log.writelines(str(system_stats) + "\n")
    print (rx_window_stats)
    log.writelines(str(rx_window_stats) + "\n")
    are_ipsec_window_drops_increasing=False
    if ((int(rx_window_stats["rx_window_drops_0"][1]) - int(rx_window_stats["rx_window_drops_0"][0]) >=10) or (int(rx_window_stats["rx_window_drops_0"][2]) - int(rx_window_stats["rx_window_drops_0"][0]) >=10) or (int(rx_window_stats["rx_window_drops_0"][2]) - int(rx_window_stats["rx_window_drops_0"][1]) >=10)):
        are_ipsec_window_drops_increasing=True
    if ((int(rx_window_stats["rx_window_drops_1"][1]) - int(rx_window_stats["rx_window_drops_1"][0]) >=10) or (int(rx_window_stats["rx_window_drops_1"][2]) - int(rx_window_stats["rx_window_drops_1"][0]) >=10) or (int(rx_window_stats["rx_window_drops_1"][2]) - int(rx_window_stats["rx_window_drops_1"][1]) >=10)):
        are_ipsec_window_drops_increasing=True
    if ((int(rx_window_stats["rx_window_drops_2"][1]) - int(rx_window_stats["rx_window_drops_2"][0]) >=10) or (int(rx_window_stats["rx_window_drops_2"][2]) - int(rx_window_stats["rx_window_drops_2"][0]) >=10) or (int(rx_window_stats["rx_window_drops_2"][2]) - int(rx_window_stats["rx_window_drops_2"][1]) >=10)):
        are_ipsec_window_drops_increasing=True
    if ((int(rx_window_stats["rx_window_drops_3"][1]) - int(rx_window_stats["rx_window_drops_3"][0]) >=10) or (int(rx_window_stats["rx_window_drops_3"][2]) - int(rx_window_stats["rx_window_drops_3"][0]) >=10) or (int(rx_window_stats["rx_window_drops_3"][2]) - int(rx_window_stats["rx_window_drops_3"][1]) >=10)):
        are_ipsec_window_drops_increasing=True
    if ((int(rx_window_stats["rx_window_drops_4"][1]) - int(rx_window_stats["rx_window_drops_4"][0]) >=10) or (int(rx_window_stats["rx_window_drops_4"][2]) - int(rx_window_stats["rx_window_drops_4"][0]) >=10) or (int(rx_window_stats["rx_window_drops_4"][2]) - int(rx_window_stats["rx_window_drops_4"][1]) >=10)):
        are_ipsec_window_drops_increasing=True
    if ((int(rx_window_stats["rx_window_drops_5"][1]) - int(rx_window_stats["rx_window_drops_5"][0]) >=10) or (int(rx_window_stats["rx_window_drops_5"][2]) - int(rx_window_stats["rx_window_drops_5"][0]) >=10) or (int(rx_window_stats["rx_window_drops_5"][2]) - int(rx_window_stats["rx_window_drops_5"][1]) >=10)):
        are_ipsec_window_drops_increasing=True
    if ((int(rx_window_stats["rx_window_drops_6"][1]) - int(rx_window_stats["rx_window_drops_6"][0]) >=10) or (int(rx_window_stats["rx_window_drops_6"][2]) - int(rx_window_stats["rx_window_drops_6"][0]) >=10) or (int(rx_window_stats["rx_window_drops_6"][2]) - int(rx_window_stats["rx_window_drops_6"][1]) >=10)):
        are_ipsec_window_drops_increasing=True
    if ((int(rx_window_stats["rx_window_drops_7"][1]) - int(rx_window_stats["rx_window_drops_7"][0]) >=10) or (int(rx_window_stats["rx_window_drops_7"][2]) - int(rx_window_stats["rx_window_drops_7"][0]) >=10) or (int(rx_window_stats["rx_window_drops_7"][2]) - int(rx_window_stats["rx_window_drops_7"][1]) >=10)):
        are_ipsec_window_drops_increasing=True
    
    
    if are_ipsec_window_drops_increasing==True:
        log.writelines("Box in problem state, collecting show command data \n")
        ve_cmd.send("show bfd sessions | nomore \n")
        time.sleep(5)
        ve_recv = ve_cmd.recv(nbytes=100000)
        print (ve_recv.decode('cp437'))
        log.writelines(ve_recv.decode('cp437')+"\n")

        #4. Get output of "show tunnel statistics bfd | nomore" 2 times.
        for i in range(0,2):
            log.writelines("#################### Iteration %s #######################" %i)
            ve_cmd.send("show tunnel statistics bfd| tab | nomore \n")
            time.sleep(5)
            ve_recv = ve_cmd.recv(nbytes=100000)
            print (ve_recv.decode('cp437'))
            log.writelines(ve_recv.decode('cp437')+"\n")

        #5. Get output of "show tunnel statistics ipsec | nomore" 2 times.
        for i in range(0,2):
            log.writelines("#################### Iteration %s #######################" %i)
            ve_cmd.send("show tunnel statistics ipsec | tab | nomore \n")
            time.sleep(5)
            ve_recv = ve_cmd.recv(nbytes=100000)
            print (ve_recv.decode('cp437'))
            log.writelines(ve_recv.decode('cp437')+"\n")


        #6. Get output of "show omp tlocs | nomore | tab"
        ve_cmd.send("show omp tlocs | nomore | tab \n")
        time.sleep(5)
        ve_recv = ve_cmd.recv(nbytes=100000)
        print (ve_recv.decode('cp437'))
        log.writelines(ve_recv.decode('cp437')+"\n")

        ve_cmd.send("show ip route | nomore \n")
        time.sleep(5)
        ve_recv = ve_cmd.recv(nbytes=100000)
        print (ve_recv.decode('cp437'))
        log.writelines(ve_recv.decode('cp437')+"\n")

        ve_cmd.send("unhide viptela_internal \n")
        ve_cmd.send(base64.b64decode(b'NW1vayFuZ2shbGwk').decode("utf-8")+"\n")
        #7. Get output of "show internal ttm database"
        ve_cmd.send("show internal ttm database | nomore \n")
        time.sleep(5)
        ve_recv = ve_cmd.recv(nbytes=100000)
        #print (ve_recv)
        #print (type(ve_recv))
        #print (ve_recv.decode('cp437'))
        log.writelines(ve_recv.decode('cp437')+"\n")

        #8. Get output of "tools internal fp-dump options '-E'" 3 times.
        for i in range(0,2):
            log.writelines("#################### Iteration %s #######################" %i)
            ve_cmd.send('tools internal fp-dump options "-E" | nomore \n')
            time.sleep(5)
            ve_recv = ve_cmd.recv(nbytes=100000)
            print (ve_recv)
            print (ve_recv.decode('cp437'))
            log.writelines(ve_recv.decode('cp437')+"\n")

        ve_cmd.send(recovery_cmd + "\n")
        log.writelines("Performed %s at %s \n" %(recovery_cmd,current_time))


    else:
        print ("Box not in problem state. Check after 15 minutes")
        log.writelines("Box not in problem state. Check after 15 minutes \n")
        did_we_rekey = False

    ve_ssh.close()

log.close()

