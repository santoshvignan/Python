import re


com_bfd_flaps = open("/Users/vignan/Downloads/com_bfd_flaps_RCHIv4Jul13.txt","r")
bfd_events_list = []
for i in com_bfd_flaps.readlines():
    bfd_events_list.append(i)

#print (bfd_events_list)

bfd_down_events = []
for bfd_event in bfd_events_list:
    is_down = re.search(r'new-state:down',bfd_event)
    is_false = re.search(r'deleted:false',bfd_event)
    if is_down and is_false:
        bfd_down_events.append(bfd_event)

print (bfd_down_events)
print (len(bfd_down_events))

j = []
for line in bfd_down_events:
    bfd_session = line.split()
    date = bfd_session[1] + " "  + bfd_session[2] + " " + bfd_session[3]
    #print (date)
    j.append(date)

print (j)
k = dict.fromkeys(j)

for i in k:
    bfd_down_events_per_timestamp = []
    for line in bfd_down_events:
        bfd_session = line.split()
        date = bfd_session[1] + " " +bfd_session[2] + " " + bfd_session[3]
        if i == date:
            bfd_down_events_per_timestamp.append(line)
    if len(bfd_down_events_per_timestamp) > 3:
        print ("************BFD Sessions down at " + i + ".**********************")
        print (len(bfd_down_events_per_timestamp))
        for flap in bfd_down_events_per_timestamp:
            print (flap)

    #if len(bfd_down_events_per_timestamp) > 1:
    #   for flap in bfd_down_events_per_timestamp:
    #       dest_ip =




