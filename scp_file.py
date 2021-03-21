import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a",type=str,help="Do you want to copy to or from the server",required=True)
parser.add_argument("-f",type=str,help="PLEASE INPUT THE FILE YOU WANT TO COPY",required=True)
parser.add_argument("-ip",type=str,help="ENTER THE SERVER IP",required=True)
parser.add_argument("-d",type=str,help="Enter the destination directory",required=True)
parser.add_argument("-s",type=str,help="Enter the source directory",required=True)

args = parser.parse_args()

download_direc = "/Users/vignan/Downloads/"

if args.a == "from":
    scp_command = "scp vignan@" + args.ip + ":" + args.s + args.f + " " + args.d
    #print (scp_command)
    os.system(scp_command)

if args.a == "to":
    scp_command = "scp " + args.s + args.f + " vignan@" + args.ip +":" + args.d
    #print (scp_command)
    os.system(scp_command)



