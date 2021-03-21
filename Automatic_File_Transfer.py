import subprocess
import sys
import datetime


#Get the latest modified file
current_working_dir = "/Users/vignan/PycharmProjects/pythonProject/venv/"
latest_mod_file = subprocess.run('find . -type f -mmin -1',shell=True,capture_output=True,cwd=current_working_dir)
#print (latest_mod_file.stdout.decode('utf-8'))

if len(latest_mod_file.stdout) == 0:
    #print ("No file has been modified")
    sys.exit()
else:
    file_to_be_transferred = latest_mod_file.stdout.decode('utf-8').split('/')[1].rstrip()
    #print (file_to_be_transferred)
    current_time = datetime.datetime.now()
    source_dir = current_working_dir
    dest_dir = "/home/vignan/Python/"

    print (str(current_time) + " -- " + "Transferring file " + file_to_be_transferred + ".....")
    scp_command = "scp " + source_dir + file_to_be_transferred + " " + "vignan@172.18.52.79:" + dest_dir
    scp_file = subprocess.run(scp_command,shell=True,capture_output=True)




