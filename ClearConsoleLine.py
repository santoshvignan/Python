import telnetlib
import time

HOST="172.18.52.22"
USERNAME="vignan"
PASSWORD="MANSANvig2908"

clear_line = input("What line do you want to clear? ")
#print (clear_line)

tn = telnetlib.Telnet(HOST)
tn.set_debuglevel(1)
tn.msg('******Debugs Enabled********')
tn.read_until(b"Username: ")
tn.write(USERNAME.encode('ascii') + b'\n')

tn.read_until(b'Password: ')
tn.write(PASSWORD.encode('ascii') + b'\n')
time.sleep(2)
flag = 0

if clear_line == "ALL" or clear_line == "all" or clear_line == "All":
    flag = 1

if flag == 1:
    print ("FLAG is set to 1")
    for i in range(3,19):
        command = "clear line " + str(i)
        #print (command)
        tn.write(command.encode('ascii') + b'\n')
        time.sleep(1)
        tn.write(b'\n')

    tn.write("exit".encode('ascii') + b'\n')

if flag == 0:
    lines_to_clear = clear_line.split(',')
    if len(lines_to_clear) == 1:
        command = "clear line " + clear_line
        #print (command)
        tn.write(command.encode('ascii') + b'\n')
        time.sleep(2)
        tn.write(b"\n")
        time.sleep(2)
        tn.write("exit".encode('ascii') + b'\n')

    else:
        for i in lines_to_clear:
            command = "clear line " + i
            tn.write(command.encode('ascii') + b'\n')
            time.sleep(2)
            tn.write(b"\n")
            time.sleep(2)
        tn.write("exit".encode('ascii') + b'\n')

