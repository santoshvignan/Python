import paramiko
import time
from datetime import datetime,date
import argparse

#1. Log into the vEdge.
#2. Get output of "show system statistics | nomore" 3 times.
#3. Get output of "show bfd sessions | nomore".
#4. Get output of "show tunnel statistics bfd | nomore" 2 times.
#5. Get output of "show tunnel statistics ipsec | nomore" 2 times.
#6. Get output of "show omp tlocs | nomore | tab".
#7. Get output of "show internal ttm database".
#8. Get output of "tools internal fp-dump options '-E'" 3 times.

def DeviceDataCollection(hosts,username,password):
    for host in hosts.split(","):
        today = date.today()
        file_path = "/home/vignan/"
        filename = file_path + "logs_" + host + "_" + str(today) +".txt" 

        current_time = datetime.now()
        log = open(filename,"a")


        log.writelines("##################################################\n")
        log.writelines(str(current_time) + "\n")
        vedge_ip = host
        vedge_username = username
        vedge_password = password

        ve_ssh = paramiko.SSHClient()
        ve_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ve_ssh.connect(hostname=vedge_ip,username=vedge_username,password=vedge_password)
        time.sleep(5)


        ve_cmd = ve_ssh.invoke_shell()
        ve_recv = ve_cmd.recv(100000)
        print (ve_recv.decode('cp437'))
        log.writelines(ve_recv.decode('cp437') + "\n")
        time.sleep(5)

        ve_cmd.send("paginate false \n")
        ve_recv = ve_cmd.recv(100000)
        ve_cmd.send("\n")
        time.sleep(5)
        
        #2. Get output of "show system statistics | nomore" 3 times
        for i in range(0,3):
            log.writelines("###################### Iteration %s ########################" %str(i))
            ve_cmd.send("show system statistics | nomore \n")
            time.sleep(5)
            ve_recv = ve_cmd.recv(nbytes=100000)
            print (ve_recv.decode('cp437'))
            log.writelines(ve_recv.decode('cp437'))
            time.sleep(5)

        #3. Get output of "show bfd sessions | nomore"
        ve_cmd.send("show bfd sessions | nomore \n")
        time.sleep(5)
        ve_recv = ve_cmd.recv(nbytes=100000)
        print (ve_recv.decode('cp437'))
        log.writelines(ve_recv.decode('cp437'))

        #4. Get output of "show tunnel statistics bfd | nomore" 2 times.
        for i in range(0,3):
            log.writelines("#################### Iteration %s #######################" %i)
            ve_cmd.send("show tunnel statistics bfd| tab | nomore \n")
            time.sleep(5)
            ve_recv = ve_cmd.recv(nbytes=100000)
            print (ve_recv.decode('cp437'))
            log.writelines(ve_recv.decode('cp437'))

        #5. Get output of "show tunnel statistics ipsec | nomore" 2 times.
        for i in range(0,3):
            log.writelines("#################### Iteration %s #######################" %i)
            ve_cmd.send("show tunnel statistics ipsec | tab | nomore \n")
            time.sleep(5)
            ve_recv = ve_cmd.recv(nbytes=100000)
            print (ve_recv.decode('cp437'))
            log.writelines(ve_recv.decode('cp437'))


        #6. Get output of "show omp tlocs | nomore | tab"
        ve_cmd.send("show omp tlocs | nomore | tab \n")
        time.sleep(5)
        ve_recv = ve_cmd.recv(nbytes=100000)
        print (ve_recv.decode('cp437'))
        log.writelines(ve_recv.decode('cp437'))

        ve_cmd.send("unhide viptela_internal \n")
        ve_cmd.send("5mok!ngk!ll$\n")
        #7. Get output of "show internal ttm database"
        ve_cmd.send("show internal ttm database | nomore \n")
        time.sleep(5)
        ve_recv = ve_cmd.recv(nbytes=100000)
        print (ve_recv)
        print (type(ve_recv))
        print (ve_recv.decode('cp437'))
        log.writelines(ve_recv.decode('cp437'))

        #8. Get output of "tools internal fp-dump options '-E'" 3 times.
        for i in range(0,3):
            log.writelines("#################### Iteration %s #######################" %i)
            ve_cmd.send('tools internal fp-dump options "-E" | nomore \n')
            time.sleep(5)
            ve_recv = ve_cmd.recv(nbytes=100000)
            print (ve_recv)
            print (ve_recv.decode('cp437'))
            log.writelines(ve_recv.decode('cp437'))

        ve_ssh.close()


    log.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="python3 SSH_Command_Exec.py --ip 1.2.3.4,5.6.7.8 -u admin -p password")
    parser.add_argument("--ip",required=True,help="--ip <IP addresses of devices separated by comma>")
    parser.add_argument("--u",required=True,help="--u <username>")
    parser.add_argument("--p",required=True,help="--p <password>")
    hosts = parser.parse_args().ip
    username = parser.parse_args().u
    password = parser.parse_args().p
    DeviceDataCollection(hosts,username,password)