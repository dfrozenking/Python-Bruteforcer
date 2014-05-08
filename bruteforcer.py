#!/usr/bin/python
import redis
import datetime, os, sys
import argparse

r_server = redis.Redis("localhost")

print "\n---== Python Bruteforcer ==---\n"

def log(msg):
	timestamp = datetime.datetime.now().strftime('%b %d %H:%M:%S')
	print "%s Bruteforcer[%d]: %s" % (timestamp, os.getpid(), msg)
	sys.stdout.flush()

def BruteManager(proto, port):
	scanners = {
	'ssh':[22],
	'ftp':[21],
	'pop3':[110]
	}

	if (port == "" and proto in scanners):
		r_server.set("Port", scanners[proto][0])
		print "Setting the default port %s for the %s protocol" %(port, proto)
		scanners[proto][1]()

	if (port != "" and proto in scanners):
		print scanners[proto][1]()
	else:
		print "Fatal Error!"

def ManualBrute():
	option = int(raw_input("Choose an option:\n1- Specific Bruteforce\n2- IP list Bruteforce\n"))

	if (option == 1):
		host = raw_input("Type the host IP: ")
		protocol = raw_input("Type the protocol (FTP(21), POP3(110), SSH(22)): ")
		port = raw_input("Type the port: ")
		r_server.set("Host", host)
		r_server.set("Protocol", protocol)
		r_server.set("Port", port)
		print BruteManager("ssh")

		print "You are goin to scan the server %s at the %s and %s" %(r_server.get("Host"), r_server.get("Protocol"), r_server.get("Port"))

	if (option == 2):
		print "Make sure that the file with the hosts IP are in the same folder\n"
		hostlist = raw_input("Type the filename wich are the host IPs: ")
		protocol = raw_input("Type the protocol (FTP, POP3, SSH): ")
		port = raw_input("Type the port (Keep it empty if you want use default port): ")
		r_server.set("File", hostlist)
		r_server.set("Protocol", protocol)
		r_server.set("Port", port)
		print BruteManager(r_server.get("Protocol"), r_server.get("Port"))

	else:
		print ("Invalid option")
		sys.exit(0)

#def SSHBrute():

#def FTPBrute():

#def POPBrute():


parser = argparse.ArgumentParser(description="Python Bruteforcer")
parser.add_argument('-t', '--target',   dest='target', type=int, action='store', help='Server Address to Bruteforce')
parser.add_argument('-f', '--file', dest='file', type=str, action='store', help="File with the server's addresses")
parser.add_argument('-p', '--protocol', dest='protocol', type=str, action='store', help='Protocol to Bruteforce')
args = parser.parse_args()

if not any(vars(args).values()):
	ManualBrute()
else:
	print("Fatal Error!")
	sys.exit(0)







