import os

c = os.system("ping -c 5 172.18.52.52 > /dev/null")
print (c)
