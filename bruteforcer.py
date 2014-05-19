#!/usr/bin/python
import redis, argparse, sys, subprocess
from bruteopt import SSHBrute, FTPBrute, POPBrute
from IPy import IP


r_server = redis.Redis("localhost")


print "\n---== Python Bruteforcer ==---\n"


def BruteManager(proto, port):
	scanners = {
	'ssh':[22, SSHBrute],
	'ftp':[21, FTPBrute],
	'pop3':[110, POPBrute]
	}

	if (port == "" or port == "None" and proto in scanners):

		r_server.set("Port", scanners[proto][0])

		print "Setting the default port %s for the %s protocol" % (r_server.get("Port"), proto)
		
		if (int(r_server.get("Option")) == 2):

			host = r_server.get("File")

			filelen = int(subprocess.check_output(["wc", "-l", str(r_server.get("File"))]).split()[0])

			mylist = open(r_server.get("File")).read().splitlines()

			for address in mylist:
				if ("/" in address):
					iprange = IP(address)
					for x in iprange:

						r_server.set("ActServer", x)

						if (r_server.get("LastServer") == r_server.get("ActServer")):

							print "Server already scanned"
							sys.exit(0)

						else:

							scanners[proto][1](r_server.get("ActServer"), int(r_server.get("Port")))
							r_server.set("LastServer", r_server.get("ActServer"))

		else:

			if ("/" in str(r_server.get("Host"))):

				iprange = IP(str(r_server.get("Host")))

				for x in iprange:
					scanners[proto][1](x, int(r_server.get("Port")))

			else:

				scanners[proto][1](r_server.get("Host"), int(r_server.get("Port")))


	elif (port != "" or "None" and proto in scanners):
		if (int(r_server.get("Option")) == 1):

			if ("/" in str(r_server.get("Host"))):

				iprange = IP(str(r_server.get("Host")))

				for x in iprange:
					scanners[proto][1](x, int(r_server.get("Port")))
			else:

				scanners[proto][1](r_server.get("Host"), int(r_server.get("Port")))

	else:
		print "Invalid Protocol"
		sys.exit(0)


def ManualBrute():
	option = int(raw_input("Choose an option:\n1- Specific Bruteforce\n2- IP list Bruteforce\n\nOption: "))

	if (option == 1):
		r_server.set("Option", 1)
		host = raw_input("\nType the host IP: ")
		protocol = raw_input("\nType the protocol (FTP, POP3, SSH): ")
		port = raw_input("\nType the port: ")
		r_server.set("Host", host)
		r_server.set("Protocol", protocol.lower())
		r_server.set("Port", port)
		
		BruteManager(r_server.get("Protocol"), r_server.get("Port"))

	elif (option == 2):
		r_server.set("Option", 2)
		print "\nMake sure that the file with the hosts IP are in the same folder\n"
		hostlist = raw_input("\nType the filename wich are the host IPs: ")
		protocol = raw_input("\nType the protocol (FTP, POP3, SSH): ")
		port = raw_input("\nType the port (Keep it empty if you want use default port): ")
		r_server.set("File", hostlist)
		r_server.set("Protocol", protocol.lower())
		r_server.set("Port", port)

		BruteManager(r_server.get("Protocol"), r_server.get("Port"))

	else:
		print ("Invalid option")
		sys.exit(0)


parser = argparse.ArgumentParser(description="---== Python Bruteforcer ==---")
parser.add_argument('-t', '--target',   dest='target', type=str, action='store', help='Server Address to Bruteforce')
parser.add_argument('-f', '--file', dest='file', type=str, action='store', help="File with the server's addresses")
parser.add_argument('-s', '--service', dest='protocol', type=str, action='store', help='Protocol to Bruteforce')
parser.add_argument('-p', '--port', dest='port', type=int, action='store', help='Service Port')

args = parser.parse_args()

if not any(vars(args).values()):
	ManualBrute()

elif (any(vars(args).values())):
	r_server.set("File", args.file)
	r_server.set("Host", args.target)
	r_server.set("Protocol", args.protocol)
	r_server.set("Port", args.port)

	if (r_server.get("Host") != "None" and r_server.get("File") != "None"):
		print "\nYou used both options -t and -f, you must specify only one"
		print r_server.get("Host")
		print r_server.get("File")
		sys.exit(0)

	elif (r_server.get("Protocol") == "None" or ""):
		print "\nYou need to specify the protocol"
		sys.exit(0)

	elif (r_server.get("Host") != "None"):
		r_server.set("Option", 1)
		BruteManager(r_server.get("Protocol"), r_server.get("Port"))

	elif (r_server.get("File") != "None"):
		r_server.set("Option", 2)
		BruteManager(r_server.get("Protocol"), r_server.get("Port"))

else:
	print("Fatal Error!")
	sys.exit(0)
