from time import strptime
import pandas as pd
import numpy as np
import csv
from datetime import date, datetime

csv_file_read = open("/Users/vignan//Downloads/bfd-data.csv",'r')

csv_file_write = open("/Users/vignan/Downloads/bfd-data-analysis.csv",'w')

lg = csv.reader(csv_file_read,delimiter=" ")

lg_w = csv.writer(csv_file_write)
headers = ["Filename","Month","Date","Time","Hostname","Process-Name","Log-Info-1","Log-Info-2","Date-UTC","Time-UTC","Event-type","Severity","host-name","system-ip","src-ip","dst-ip","proto","src-port","dst-port","local-system-ip","local-color","remote-system-ip","remote-color","new-state","deleted","flap-reason"]
lg_w.writerow(headers)
for i in lg: 
    lg_w.writerow(i)

csv_file_write.close()
csv_file_read.close()
data = pd.read_csv("/Users/vignan/Downloads/bfd-data-analysis.csv",index_col=False)
# print (len(data.index))
# for i in data.index:
#     print ("value of i is %s" % i)
#     for j in range(i+1,len(data.index)):
#         print (j)
# len_data = len(data)
delete_j = []
for i in data.index:
    print (delete_j)
    if i not in delete_j:
        print ("value of i is %s" %i)
        row1 = data.iloc[i]
        for j in range(i+1,len(data.index)):
            if j not in delete_j:
                print ("value of j is %s" % j)
                row2 = data.iloc[j]
                if row1["Date-UTC"] == row2["Date-UTC"]:
                    #print (row1["local-system-ip"] + " " + row1["remote-system-ip"] + " " + row1["local-color"]+ " " + row1["remote-color"] + " " + row1["new-state"] + " " + row1["deleted"])
                    #print (row2["local-system-ip"] + " " + row2["remote-system-ip"] + " " + row2["local-color"]+ " " + row2["remote-color"] + " " + row2["new-state"] + " " + row2["deleted"])
                    if (row1["local-system-ip"] == row2["local-system-ip"] and row1["remote-system-ip"] == row2["remote-system-ip"] and row1["local-color"] == row2["local-color"] and row1["remote-color"] == row2["remote-color"]):
                        #print ("Comparing the same sessions %s and %s" %(i,j))
                        #print (row1["new-state"] + " " + row2["new-state"])
                        if (row1["new-state"] == "new-state:down" and row2["new-state"] == "new-state:up"):
                            print (str(i) + " " + str(j))
                            print ("BFD changed from down to up")
                            #print (row1["Time-UTC"] + "-->" + row2["Time-UTC"] )
                            print (datetime.strptime(row1["Date-UTC"] + " " + row1["Time-UTC"],'%m/%d/%Y %H:%M:%S'))
                            print (datetime.strptime(row2["Date-UTC"] + " " + row2["Time-UTC"],'%m/%d/%Y %H:%M:%S'))
                            row1_time = datetime.strptime(row1["Date-UTC"] + " " + row1["Time-UTC"],'%m/%d/%Y %H:%M:%S')
                            row2_time = datetime.strptime(row2["Date-UTC"] + " " + row2["Time-UTC"],'%m/%d/%Y %H:%M:%S')
                            time_diff_bw_down_up = row2_time - row1_time
                            print (row1["local-system-ip"] + " " + row1["remote-system-ip"] + " " + row1["local-color"]+ " " + row1["remote-color"] + " " + row1["new-state"] + " " + row1["deleted"])
                            print (row2["local-system-ip"] + " " + row2["remote-system-ip"] + " " + row2["local-color"]+ " " + row2["remote-color"] + " " + row2["new-state"] + " " + row2["deleted"])
                            print ("The BFD's came up within %s seconds" %(time_diff_bw_down_up.seconds))
                            #print (row1)
                            #print (row2)
                            
                            data.drop([i,j],axis=0,inplace=True)
                            #print (len(data))
                            delete_j.append(j)
                            #print (delete_j)
                            print (data)
                            #len_data = len(data)
                            break
                        
                        if (row1["new-state"] == "new-state:down" and row2["new-state"] == "new-state:down" and row2["deleted"] == "deleted:true" and row1["deleted"] == "deleted:false"):
                            print ("This is an instance of a bfd session getting deleted from the bfd db. We dont need the delete:true entry for comparison")
                            data.drop(j,axis=0,inplace=True)
                            print ("Contents after deleting the deleted:true entry \n")
                            print (data)
                            delete_j.append(j)
                            

# def parse_data(data):
#     print (data)
#     for i in range(0,len(data)):
#         row1 = data.iloc[i]
#         for j in range(i+1,len(data)):
#             row2 = data.iloc[j]
#             if row1["Date-UTC"] == row2["Date-UTC"]:
#                 #print (row1["local-system-ip"] + " " + row1["remote-system-ip"] + " " + row1["local-color"]+ " " + row1["remote-color"] + " " + row1["new-state"] + " " + row1["deleted"])
#                 #print (row2["local-system-ip"] + " " + row2["remote-system-ip"] + " " + row2["local-color"]+ " " + row2["remote-color"] + " " + row2["new-state"] + " " + row2["deleted"])
#                 if (row1["local-system-ip"] == row2["local-system-ip"] and row1["remote-system-ip"] == row2["remote-system-ip"] and row1["local-color"] == row2["local-color"] and row1["remote-color"] == row2["remote-color"]):
#                     print ("Comparing the same sessions %s and %s" %(i,j))
#                     #print (row1["new-state"] + " " + row2["new-state"])
#                     analyse_bfd_up_down(row1,row2,i,j)


# def analyse_bfd_up_down(row1,row2,i,j):
#     if (row1["new-state"] == "new-state:down" and row2["new-state"] == "new-state:up"):
#         print ("BFD changed from down to up")
#         #print (row1["Time-UTC"] + "-->" + row2["Time-UTC"] )
#         print (datetime.strptime(row1["Date-UTC"] + " " + row1["Time-UTC"],'%m/%d/%Y %H:%M:%S'))
#         print (datetime.strptime(row2["Date-UTC"] + " " + row2["Time-UTC"],'%m/%d/%Y %H:%M:%S'))
#         row1_time = datetime.strptime(row1["Date-UTC"] + " " + row1["Time-UTC"],'%m/%d/%Y %H:%M:%S')
#         row2_time = datetime.strptime(row2["Date-UTC"] + " " + row2["Time-UTC"],'%m/%d/%Y %H:%M:%S')
#         time_diff_bw_down_up = row2_time - row1_time
#         print (row1["local-system-ip"] + " " + row1["remote-system-ip"] + " " + row1["local-color"]+ " " + row1["remote-color"] + " " + row1["new-state"] + " " + row1["deleted"])
#         print (row2["local-system-ip"] + " " + row2["remote-system-ip"] + " " + row2["local-color"]+ " " + row2["remote-color"] + " " + row2["new-state"] + " " + row2["deleted"])
#         print ("The BFD's came up within %s seconds" %(time_diff_bw_down_up.seconds))          
#         data.drop([i,j],axis=0,inplace=True)
#         #print (len(data))
#         print ("Contents after deleting the bfd-state transition entries \n")
#         print (data)
#         parse_data(data)
    
#     if (row1["new-state"] == "new-state:down" and row2["new-state"] == "new-state:down" and row2["deleted"] == "deleted:true" and row1["deleted"] == "deleted:false"):
#         print ("This is an instance of a bfd session getting deleted from the bfd db. We dont need the delete:true entry for comparison")
#         data.drop(j,axis=0,inplace=True)
#         print ("Contents after deleting the deleted:true entry \n")
#         print (data)
#         parse_data(data)


# if __name__ == "__main__":
#     csv_file_read = open("/Users/vignan//Downloads/bfd-data.csv",'r')

#     csv_file_write = open("/Users/vignan/Downloads/bfd-data-analysis.csv",'w')

#     lg = csv.reader(csv_file_read,delimiter=" ")

#     lg_w = csv.writer(csv_file_write)
#     headers = ["Filename","Month","Date","Time","Hostname","Process-Name","Log-Info-1","Log-Info-2","Date-UTC","Time-UTC","Event-type","Severity","host-name","system-ip","src-ip","dst-ip","proto","src-port","dst-port","local-system-ip","local-color","remote-system-ip","remote-color","new-state","deleted","flap-reason"]
#     lg_w.writerow(headers)
#     for i in lg: 
#         lg_w.writerow(i)

#     csv_file_write.close()
#     csv_file_read.close()
#     data = pd.read_csv("/Users/vignan/Downloads/bfd-data-analysis.csv",index_col=False)

#     parse_data(data)