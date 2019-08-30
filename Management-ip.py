import os
reachablehosts = []
unreachablehosts = []
for ip in range(1,110):
    host = '29.29.29.'+ str(ip)
    print "Currently pinging the following ip" + " " + host
    response = os.system("ping -c 5 " + host + ">/dev/null")
    if response == 0:
        reachablehosts.append(host)
    else:
        unreachablehosts.append(host)

print reachablehosts

print unreachablehosts
